#!/usr/bin/env python3
"""Mix the Short's soundtrack: voice + music + SFX -> short/audio/mix.wav and mix.m4a (65.6 s).

    python3 short/audio/mix.py            # re-run after editing cues.json (takes ~20 s)
    python3 short/audio/mix.py --stems DIR   # also write the voice/music/SFX stems (at master gain)

Inputs (all re-read on every run):
  short/voice/voice.wav, short/voice/words.json   narration + word times (speech windows)
  short/audio/music.wav                           music on the 116.3 bpm / 0.11 s grid (build_music.py)
  short/audio/cues.json                           SFX timing: the single source of truth
  short/audio/sfx/library.json + sfx/*.wav        the SFX sounds

cues.json entries: {"t": s, "sfx": name, "gain_db": dB, "note": "..."} plus optional
  "rate": playback-rate factor (1.2 = 20% faster and higher; handy for repeats of one sound)
  "dur": s  -> cut the sound short (150 ms fade)
  "sfx": "~music_dip" with "dur": s   -> dips the music by gain_db for dur seconds at t
t is when the sound's hit lands: files start on their attack; whooshes/risers are shifted earlier
by their library 'pre' so their peak lands on t.

Rule 10 targets: music >= 6 dB under the voice at all times and sidechain-ducked under speech;
SFX lightly ducked under speech; master about -14 LUFS integrated, true peak <= -1 dBTP.
"""
import json, os, re, subprocess, sys, tempfile
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SHORT = os.path.dirname(HERE)
SR, DURATION = 48000, 65.6
N = int(round(SR * DURATION))

# ---- levels (dB) --------------------------------------------------------------------------------
MUSIC_GAIN_DB = -20.0          # static music gain before ducking
# music level automation (t, dB) breakpoints, linear in dB: lift the quiet intro and the sparse tail
# of the arrangement a little so the pulse is audible under the hook (the groove bars are ~12 dB
# louder in the raw take)
MUSIC_AUTOMATION = [(0.0, 6.0), (18.40, 6.0), (18.66, 0.0), (57.85, 0.0), (58.60, 5.0), (DURATION, 5.0)]
MUSIC_EQ = "highpass=f=35,lowshelf=f=100:g=-6,equalizer=f=2800:t=q:w=1.2:g=-3"   # less sub, a dip where speech lives
SFX_BUS_DB = -8.0              # all SFX; per-cue gain_db on top
VOICE_CHAIN = ("highpass=f=80,acompressor=threshold=0.063:ratio=3:attack=5:release=80:knee=4,"   # body
               "aresample=192000,alimiter=limit=0.16:attack=0.5:release=25:level=false:latency=true,"  # plosive peaks
               "aresample=48000:resampler=soxr")
# sidechain ducking keyed by the (processed) voice, fed KEY_LOOKAHEAD s early so the duck is down
# before each word starts
KEY_LOOKAHEAD = 0.04
DUCK_MUSIC = "sidechaincompress=threshold=0.025:ratio=8:attack=10:release=600:knee=3:detection=rms"
DUCK_SFX = "sidechaincompress=threshold=0.05:ratio=3:attack=5:release=200:knee=3:detection=rms"
TARGET_LUFS = -14.0
TP_MAX = -1.0                  # dBTP, checked on both mix.wav and mix.m4a
LIMIT_DB = -1.8                # limiter ceiling (4x oversampled), leaves room for the AAC encode


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def read(path):
    y, sr = sf.read(path, dtype="float32", always_2d=True)
    if sr != SR:
        g = Fraction(SR, sr)
        y = resample_poly(y, g.numerator, g.denominator, axis=0).astype(np.float32)
    return y


def fit(y, n=N):
    return y[:n] if len(y) >= n else np.concatenate([y, np.zeros((n - len(y), y.shape[1]), np.float32)])


def ffilter(y, chain, tmp, name):
    a, b = os.path.join(tmp, name + "_in.wav"), os.path.join(tmp, name + "_out.wav")
    sf.write(a, y, SR, subtype="FLOAT")
    run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", chain, "-c:a", "pcm_f32le", b])
    return read(b)


def ebur128(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = out[out.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", summary).group(1))
    lra = float(re.search(r"LRA:\s+(-?[\d.]+) LU", summary).group(1))
    return I, tp, lra, summary.strip()


def speech_windows(words, join=0.3):
    win = []
    for w in words:
        if win and w["start"] - win[-1][1] < join:
            win[-1][1] = max(win[-1][1], w["end"])
        else:
            win.append([w["start"], w["end"]])
    return win


def db(x):
    return 10 * np.log10(np.mean(np.square(x, dtype=np.float64)) + 1e-12)


def main():
    cues = json.load(open(os.path.join(HERE, "cues.json")))
    lib = json.load(open(os.path.join(HERE, "sfx", "library.json")))
    words = json.load(open(os.path.join(SHORT, "voice", "words.json")))
    t = np.arange(N) / SR
    with tempfile.TemporaryDirectory() as tmp:
        # voice: mono -> light compression -> dual mono
        voice = fit(read(os.path.join(SHORT, "voice", "voice.wav")))
        voice = ffilter(voice[:, :1], VOICE_CHAIN, tmp, "voice")
        voice = fit(np.repeat(voice[:, :1], 2, axis=1))

        # music: static gain + automation + dips from cues.json
        music = fit(read(os.path.join(HERE, "music.wav")))
        at, ad = zip(*MUSIC_AUTOMATION)
        gdb = MUSIC_GAIN_DB + np.interp(t, at, ad)
        for c in cues:
            if c["sfx"] == "~music_dip":
                t0, d, g = c["t"], c.get("dur", 0.4), c["gain_db"]
                env = np.interp(t, [t0 - 0.03, t0, t0 + d, t0 + d + 0.15], [0, g, g, 0], left=0, right=0)
                gdb = gdb + env
        music = music * (10 ** (gdb / 20)).astype(np.float32)[:, None]

        # SFX stem from the cue sheet
        sfx = np.zeros((N, 2), np.float32)
        cache = {}
        missing = []
        for c in cues:
            name = c["sfx"]
            if name.startswith("~"):
                continue
            if name not in lib:
                missing.append(name); continue
            rate = float(c.get("rate", 1.0))
            key = (name, rate)
            if key not in cache:
                y = read(os.path.join(HERE, "sfx", lib[name]["file"]))
                if rate != 1.0:
                    fr = Fraction(rate).limit_denominator(200)
                    y = resample_poly(y, fr.denominator, fr.numerator, axis=0).astype(np.float32)
                cache[key] = y
            y = cache[key] * np.float32(10 ** ((SFX_BUS_DB + c.get("gain_db", 0)) / 20))
            if "dur" in c:                             # optional: cut the sound short with a 150 ms fade
                n = int(c["dur"] * SR); fo = min(int(0.15 * SR), n)
                y = y[:n].copy(); y[n - fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            start = int(round((c["t"] - lib[name]["pre"] / rate) * SR))
            a, b = max(0, start), min(N, start + len(y))
            if b > a:
                sfx[a:b] += y[a - start:b - start]
        if missing:
            sys.exit(f"cues.json names unknown sounds: {sorted(set(missing))} (see sfx/library.json)")

        # sidechain ducking (ffmpeg sidechaincompress keyed by the voice)
        paths = {}
        la = int(KEY_LOOKAHEAD * SR)
        key = np.concatenate([voice[la:], np.zeros((la, 2), np.float32)])
        for k, y in (("key", key), ("music", music), ("sfx", sfx)):
            paths[k] = os.path.join(tmp, k + ".wav"); sf.write(paths[k], y, SR, subtype="FLOAT")
        md, sd = os.path.join(tmp, "music_duck.wav"), os.path.join(tmp, "sfx_duck.wav")
        graph = (f"[0:a]asplit=2[k1][k2];[1:a]{MUSIC_EQ}[m];[m][k1]{DUCK_MUSIC}[md];"
                 f"[2:a][k2]{DUCK_SFX}[sd]")
        run(["ffmpeg", "-v", "error", "-y", "-i", paths["key"], "-i", paths["music"], "-i", paths["sfx"],
             "-filter_complex", graph, "-map", "[md]", "-c:a", "pcm_f32le", md,
             "-map", "[sd]", "-c:a", "pcm_f32le", sd])
        music_d, sfx_d = fit(read(md)), fit(read(sd))
        premix = voice + music_d + sfx_d

        # master: measured gain + 4x-oversampled limiter, iterate to the loudness target
        pre_path = os.path.join(tmp, "premix.wav")
        sf.write(pre_path, premix, SR, subtype="FLOAT")
        I0 = ebur128(pre_path)[0]
        gain, limit = TARGET_LUFS - I0, LIMIT_DB
        out_wav, out_m4a = os.path.join(HERE, "mix.wav"), os.path.join(HERE, "mix.m4a")
        for it in range(6):
            chain = (f"volume={gain:.3f}dB,aresample=192000,alimiter=limit={10**(limit/20):.5f}:attack=1:"
                     f"release=60:level=false:latency=true,aresample=48000:resampler=soxr")
            y = fit(ffilter(premix, chain, tmp, "master"))
            fo = int(0.008 * SR)                       # click-free loop point
            y[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
            y[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR), dtype=np.float32)[:, None]
            sf.write(out_wav, y, SR, subtype="PCM_24")
            run(["ffmpeg", "-v", "error", "-y", "-i", out_wav, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                 "-ac", "2", "-movflags", "+faststart", out_m4a])
            I, tp, _, _ = ebur128(out_wav)
            tp_m4a = ebur128(out_m4a)[1]
            print(f"  master pass {it+1}: gain {gain:+.2f} dB, limiter {limit:.2f} dB -> {I:.2f} LUFS, "
                  f"TP wav {tp:.2f} / m4a {tp_m4a:.2f} dBTP")
            ok_i, ok_tp = abs(I - TARGET_LUFS) <= 0.2, max(tp, tp_m4a) <= TP_MAX
            if ok_i and ok_tp:
                break
            if not ok_tp:
                limit -= max(tp, tp_m4a) - TP_MAX + 0.1
            gain += TARGET_LUFS - I

        # ---- report ----------------------------------------------------------------------------
        print("\n== ebur128 (mix.wav) ==")
        print(ebur128(out_wav)[3])
        print("\n== ebur128 (mix.m4a) ==")
        print(ebur128(out_m4a)[3])
        st = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out_wav, "-af",
                             "astats=measure_perchannel=none",
                             "-f", "null", "-"], capture_output=True, text=True).stderr
        print("\n== astats (mix.wav, overall) ==")
        print("\n".join(l.split("] ", 1)[-1] for l in st.splitlines() if "Parsed_astats" in l and ":" in l))
        dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out_m4a]).stdout)
        print(f"\nmix.wav {len(y)/SR:.4f} s ({len(y)} samples), mix.m4a {dur:.4f} s")

        # voice vs music margin during speech, on the stems at master gain (pre-limiter)
        g = 10 ** (gain / 20)
        V, M, S = voice[:, 0] * g, music_d.mean(1) * g, sfx_d.mean(1) * g
        win = speech_windows(words)
        mask = np.zeros(N, bool)
        for a, b in win:
            mask[int(a * SR):int(b * SR)] = True
        print("\n== music under voice ==")
        if "--stems" in sys.argv:                      # python3 mix.py --stems DIR: stems at master gain
            d = sys.argv[sys.argv.index("--stems") + 1]; os.makedirs(d, exist_ok=True)
            for k, z in (("voice", voice), ("music", music_d), ("sfx", sfx_d)):
                sf.write(os.path.join(d, k + ".wav"), z * g, SR, subtype="FLOAT")
        Mpre = music.mean(1) * g
        print(f"  ducking (+ sub shelf and 2.8 kHz dip) over speech: {db(Mpre[mask]) - db(M[mask]):.1f} dB "
              f"(music {db(Mpre[mask]):.1f} -> {db(M[mask]):.1f} dBFS RMS)")
        print(f"  over all speech: voice {db(V[mask]):.1f} dBFS RMS, music {db(M[mask]):.1f} dBFS RMS "
              f"-> music {db(V[mask]) - db(M[mask]):.1f} dB under the voice")
        # per word, and per clearly voiced 50 ms frame (voice within 10 dB of its average level)
        vavg = db(V[mask]); n5, h5 = int(0.05 * SR), int(0.025 * SR)
        pw = sorted((db(V[int(w["start"] * SR):int(w["end"] * SR)]) - db(M[int(w["start"] * SR):int(w["end"] * SR)]), w["start"], w["w"])
                    for w in words if w["end"] - w["start"] >= 0.1)
        print(f"  per word ({len(pw)} words >= 0.1 s): music under the voice by min {pw[0][0]:.1f} dB "
              f"('{pw[0][2]}' {pw[0][1]:.2f} s), median {np.median([p[0] for p in pw]):.1f} dB")
        fm = []
        for s0 in range(0, N - n5, h5):
            if mask[s0:s0 + n5].all():
                lv = db(V[s0:s0 + n5])
                if lv > vavg - 10:
                    fm.append((lv - db(M[s0:s0 + n5]), s0 / SR))
        fm.sort()
        print(f"  voiced 50 ms frames ({len(fm)}): music under the voice by min {fm[0][0]:.1f} dB (at {fm[0][1]:.2f} s), "
              f"1st pct {np.percentile([f for f, _ in fm], 1):.1f} dB, median {np.median([f for f, _ in fm]):.1f} dB")
        from scipy.signal import butter, sosfilt                    # same frames, speech band only
        sb = butter(4, [200, 5000], btype="band", fs=SR, output="sos")
        Vb, Mb = sosfilt(sb, V), sosfilt(sb, M)
        fb = sorted(db(Vb[int(q * SR):int(q * SR) + n5]) - db(Mb[int(q * SR):int(q * SR) + n5]) for _, q in fm)
        print(f"  same frames, 200 Hz-5 kHz speech band: min {fb[0]:.1f} dB, 1st pct {np.percentile(fb, 1):.1f} dB, "
              f"median {np.median(fb):.1f} dB")
        w4 = int(0.4 * SR)
        gap_lv = [(db(M[s0:s0 + w4]), s0 / SR) for s0 in range(0, N - w4, w4 // 4) if not mask[s0:s0 + w4].any()]
        gl = max(gap_lv)
        print(f"  between phrases (ducker released): loudest 400 ms of music {gl[0]:.1f} dBFS (at {gl[1]:.2f} s), "
              f"{vavg - gl[0]:.1f} dB under the average speech level")
        per = []
        for w in words:
            a, b = int(w["start"] * SR), int(w["end"] * SR)
            if b - a >= int(0.1 * SR) and db(V[a:b]) > vavg - 15:
                per.append((db(V[a:b]) - db(S[a:b]), w["start"], w["w"]))
        per.sort()
        print("  SFX vs voice per word, closest calls (voice minus SFX RMS over the word; > 0 = voice on top):")
        print("   " + ", ".join(f"'{p[2]}' {p[1]:.2f}s {p[0]:+.1f} dB" for p in per[:6]))
        # how hard the limiter works
        pre = premix.mean(1) * g
        post = y.mean(1)
        n = int(0.01 * SR)
        k = np.arange(0, N - n, n)
        gr = np.array([20 * np.log10((np.max(np.abs(pre[i:i + n])) + 1e-9) / (np.max(np.abs(post[i:i + n])) + 1e-9)) for i in k])
        top = np.argsort(gr)[::-1]
        seen = []
        for i in top:
            if len(seen) >= 8: break
            if all(abs(k[i] / SR - q) > 0.3 for q, _ in seen): seen.append((k[i] / SR, gr[i]))
        print("  limiter hot spots: " + ", ".join(f"{q:.2f}s {d:.1f} dB" for q, d in sorted(seen)))
        print(f"  limiter: gain reduction > 1 dB in {np.mean(gr > 1) * 100:.1f}% of 10 ms blocks, > 3 dB in {np.mean(gr > 3) * 100:.1f}%, max {gr.max():.1f} dB")
        print(f"  SFX stem RMS {db(S):.1f} dBFS, music stem RMS {db(M):.1f} dBFS, voice stem RMS {db(V):.1f} dBFS")


if __name__ == "__main__":
    main()
