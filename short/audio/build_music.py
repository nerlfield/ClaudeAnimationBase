#!/usr/bin/env python3
"""Build short/audio/music.wav from the raw ElevenLabs Music take (src/music_take2.mp3).

1. measure the take's tempo and downbeat phase (eighth-note onset fit, see beatgrid.py)
2. re-arrange it bar by bar (EDIT below) so its sections sit on the video's shots
3. time-stretch to the video grid (config.js: 116.3 bpm, first beat 0.11 s) with rubberband
4. re-measure, pad/trim so bar 0's downbeat sits exactly on 0.11 s, cut to 65.6 s, fade the tail
5. print measured beats against the grid

    python3 short/audio/build_music.py
"""
import os, subprocess, tempfile
import numpy as np
import soundfile as sf
import librosa
import beatgrid

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src", "music_take2.mp3")
OUT = os.path.join(HERE, "music.wav")
SR = 48000
GRID_BPM, GRID_OFFSET = 116.3, 0.11   # must match short/config.js
DURATION = 65.6
FADE_OUT = 1.0                        # s, ends exactly at DURATION (the video loops)
CUTS = [5.269, 14.555, 18.683, 27.969, 37.255, 42.414, 51.185, 58.923]

# Take 2's structure (bars of 4 beats, bar 0 = first downbeat): bars 0-7 a quiet ticking intro (4-bar
# chord cycle, bar 7 has a sub swell into the drop), 8-13 the full groove, 14 hats out, 15 near-silence
# + riser, 16-30 groove, 31 riser, 32 end hit.
# EDIT: (first video bar, source bar, number of bars). Video bar v starts at 0.11 + v * 4 * 60/116.3 s.
EDIT = [
    (0, 0, 7),    # 0.11-14.55   intro bars 0-6 under the hook and "Up or down" (A, B)
    (7, 3, 1),    # 14.55-16.62  intro bar 3 again (same chord as bar 7): one extra bar, so...
    (8, 7, 20),   # 16.62-57.89  ...the swell is bar 8 and the groove drops on the D cut (18.683, beat 36);
                  #              hats-out bar at 31.06, near-silence + riser 33.13-35.19 (whip to the
                  #              fee hill), groove back at 35.19 on the flip-flops
    (28, 4, 3),   # 57.89-64.08  the burn (57.96): drop to the sparse intro texture (bars 4-6)
    (31, 3, 1),   # 64.08-end    intro bar 3 (its chord leads into bar 0, so the loop is seamless)
]
LEAD, XF = 0.020, 0.030   # splice 20 ms before each downbeat with a 30 ms equal-power crossfade


def decode(path):
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-af", "aresample=48000:resampler=soxr",
                        "-ac", "2", "-c:a", "pcm_f32le", tmp.name], check=True)
        y, sr = sf.read(tmp.name, dtype="float32")
    return y, sr


def stretch(y, factor):
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        sf.write(a, y, SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", f"rubberband=tempo={factor:.8f}:transients=crisp",
                        "-c:a", "pcm_f32le", b], check=True)
        out, _ = sf.read(b, dtype="float32")
    return out


def main():
    y, sr = decode(SRC)
    mono22 = librosa.resample(y.mean(1), orig_sr=SR, target_sr=beatgrid.SR)
    bpm, e0, ticks, r = beatgrid.measure(mono22, 116.0)
    bar = 4 * 60 / bpm
    print(f"source take: {bpm:.4f} bpm, first downbeat {e0:.4f}s (fit residual rms {np.std(r)*1000:.2f} ms)")
    # 2) bar re-arrangement in the source tempo domain
    db = lambda k: e0 + k * bar                    # source downbeat of bar k
    out_len = int((db(EDIT[-1][0] + EDIT[-1][2]) + 0.5) * SR)
    out = np.zeros((out_len, 2), np.float32)
    x = int(XF * SR)
    ramp = np.sin(np.linspace(0, np.pi / 2, x))[:, None].astype(np.float32)
    for n, (vb, sb, nb) in enumerate(EDIT):
        s0 = 0.0 if n == 0 else db(sb) - LEAD - XF / 2        # first segment keeps the pre-roll
        s1 = db(sb + nb) - LEAD + XF / 2
        o0 = 0.0 if n == 0 else db(vb) - LEAD - XF / 2
        seg = y[int(round(s0 * SR)):int(round(s1 * SR))].copy()
        if n > 0:
            seg[:x] *= ramp
        if n < len(EDIT) - 1:
            seg[-x:] *= ramp[::-1]
        i = int(round(o0 * SR))
        seg = seg[:max(0, out_len - i)]
        out[i:i + len(seg)] += seg
    # 3) stretch to the grid tempo
    factor = GRID_BPM / bpm
    st = stretch(out, factor)
    # 4) re-measure and align bar 0's downbeat to GRID_OFFSET
    bpm2, e2, ticks2, r2 = beatgrid.measure(librosa.resample(st.mean(1), orig_sr=SR, target_sr=beatgrid.SR), 116.3)
    expected = e0 / factor
    half = 60 / bpm2 / 2
    first_db = e2 + np.round((expected - e2) / half) * half   # the fitted eighth nearest the expected downbeat
    shift = GRID_OFFSET - first_db
    print(f"stretched x{factor:.6f}: {bpm2:.4f} bpm, bar-0 downbeat at {first_db:.4f}s -> shift {shift*1000:+.1f} ms")
    n = int(round(shift * SR))
    st = np.concatenate([np.zeros((n, 2), np.float32), st]) if n >= 0 else st[-n:]
    total = int(round(DURATION * SR))
    st = st[:total]
    if len(st) < total:
        st = np.concatenate([st, np.zeros((total - len(st), 2), np.float32)])
    f = int(FADE_OUT * SR)
    st[-f:] *= (np.cos(np.linspace(0, np.pi / 2, f)) ** 2)[:, None].astype(np.float32)
    st[:int(0.003 * SR)] *= np.linspace(0, 1, int(0.003 * SR))[:, None].astype(np.float32)
    peak = np.max(np.abs(st))
    if peak > 0.97:
        st *= 0.97 / peak
    sf.write(OUT, st, SR, subtype="PCM_24")
    print(f"wrote {OUT}: {len(st)/SR:.3f}s, 48 kHz stereo, peak {20*np.log10(np.max(np.abs(st))):.2f} dBFS")
    # 5) verify
    bpm3, e3, ticks3, r3 = beatgrid.measure(OUT, 116.3)
    print(f"final music.wav: measured {bpm3:.4f} bpm (target {GRID_BPM}), fit residual rms {np.std(r3)*1000:.2f} ms")
    err = beatgrid.grid_report(ticks3, GRID_BPM, GRID_OFFSET, "  all ticks ")
    P = 60 / GRID_BPM
    beats = GRID_OFFSET + np.arange(int(DURATION / P) + 1) * P
    rows = []
    for c in CUTS + [0.11, 25.84, 43.446, 57.892]:
        near = ticks3[np.argmin(np.abs(ticks3 - c))]
        g = beats[np.argmin(np.abs(beats - c))]
        rows.append(f"{c:7.3f}(grid {g:6.3f}): tick {near:6.3f} err {1000*(near-g):+5.1f} ms")
    print("  cut/accent beats, nearest measured tick vs grid beat:\n   " + "\n   ".join(rows))


if __name__ == "__main__":
    main()
