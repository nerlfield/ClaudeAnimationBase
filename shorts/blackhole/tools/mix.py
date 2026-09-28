"""Mix VO + music bed + SFX to build/mix.wav, then master to -14 LUFS integrated, true peak <= -1 dBTP.

Music is kept at least 8 dB under the voice (short-term loudness while the voice speaks) and is
sidechain-ducked a further ~5 dB under speech.  All cue times are video seconds (see outputs/script.md).
"""
import json
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import scipy.signal as ss
import soundfile as sf
import numba as nb
from scipy.ndimage import minimum_filter1d, uniform_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..', 'build')
A = os.path.join(B, 'audio')
SR = 44100
import sys as _sys0
_sys0.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from bh import shots  # noqa: E402
DUR = shots.DUR                   # 74.667 s (112 beats) since round 11
N = int(round(DUR * SR))
MUSIC_SHIFT = 0.06                 # the music's bar lines sit 60 ms late; pull it earlier


def load(path, sr=SR):
    y, s = sf.read(path, always_2d=True)
    if s != sr:
        y = ss.resample_poly(y, sr, s, axis=0)
    return y.astype(np.float32)


def decode(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), 'pipe:1'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def db(x):
    return 10 ** (x / 20.0)


def lowpass(y, hz):
    b, a = ss.butter(2, hz / (SR / 2), 'low')
    return ss.lfilter(b, a, y, axis=0).astype(np.float32)


def highpass(y, hz):
    b, a = ss.butter(2, hz / (SR / 2), 'high')
    return ss.lfilter(b, a, y, axis=0).astype(np.float32)


# (video time, file under build/audio, gain dB, options).  Sound kit v2 (tools/sfx.py): ElevenLabs takes (el/) and
# effects synthesised in-house (sfx2/syn_*); no other sources.  align: 'start' (default), 'peak' (the loudest moment
# lands on the time, so hits and whoosh apexes sit on the cut) or 'end' (risers and reverse swells finish on it).
# duck: extra sidechain dB under the voice for cues that play under speech.
# every cue in VIDEO time (round 11 re-timed the picture around the narration: bh/shots.py WARP).  Picture events
# are given by their story time through V(); word cues by name, resolved from the captions.
V = shots.unwarp
TG = shots.T_G_REAL                 # the dot lands
CUES = [
    # O: the dot, then (v2) the real photo of M87* on "look at this."; the cut to the simulation is under the photo
    (0.00, 'sfx2/syn_shimmer', -21, dict(fade_out=('PHOTO_IN', -0.5, 0.2))),
    ('PHOTO_IN', 'sfx2/syn_reverse', -19, dict(align='end')),
    ('PHOTO_IN', 'el/boom_0', -19, dict(noduck=True, align='peak')),
    ('PHOTO_IN', 'sfx2/syn_boom', -18, dict(noduck=True, align='peak')),
    ('CIRCLE', 'el/pop_1', -19, {}),
    ('PHOTO_OUT', 'el/whoosh_1', -20, dict(align='peak', fade_in=0.03)),
    # B: rise, labels, swing down, the arch
    (V(6.20), 'sfx2/syn_whoosh_long', -21, dict(align='peak')),
    ('BACK', 'el/pop_1', -19, {}),
    ('FRONT', 'sfx2/syn_pop_low2', -20, {}),
    (V(9.60), 'el/whoosh_1', -17, dict(align='peak', fade_in=0.03)),
    (V(10.67), 'el/boom_big_1', -20, dict(noduck=True, align='peak', trim_pre=0.35)),
    (V(10.67), 'sfx2/syn_boom_big', -18, dict(noduck=True, align='peak')),
    (V(10.90), 'el/pop_1', -21, {}),
    (V(16.00), 'el/riser_2', -22, dict(align='end', duck=6)),
    # C: the dive (under "Now let's fly in closer. Much closer.")
    (V(16.00), 'sfx2/syn_dive', -16, dict(duck=8)),
    (V(16.00), 'el/dive_1', -16, dict(duck=6, fade_out=(V(18.5), V(18.9)))),
    # D: arrival at the photon sphere, the sweep along the line
    (V(18.67), 'sfx2/syn_land2', -18, dict(noduck=True, align='peak')),
    (V(18.67), 'sfx2/syn_boom', -17, dict(noduck=True, align='peak')),
    (V(18.67), 'sfx2/syn_shimmer', -23, dict(fade_out=(V(21.8), V(22.2)), duck=3)),
    (V(22.20), 'el/whoosh_0', -19, dict(align='peak', fade_in=0.03, fade_out=(V(22.3), V(22.55)))),
    # E: the light's lap (now ~6 s, under "going around... all the way around... and come back to you"), the flash
    (V(22.70), 'sfx2/syn_gliss_slow', -17, dict(duck=3)),
    (V(24.00), 'el/chime_1_key', -16, dict(align='peak', fade_out=(V(24.9), V(25.4)))),
    (V(24.00), 'sfx2/syn_chime', -19, dict(align='peak', fade_out=(V(24.9), V(25.4)))),
    # E2: back to first person; the line opens into the back of your own head, then closes
    (V(24.55), 'el/whoosh_1', -21, dict(align='peak', fade_in=0.03)),
    (V(24.95), 'sfx2/syn_shimmer', -21, dict(fade_out=(V(26.1), V(26.45)), duck=2)),
    (V(26.45), 'el/whoosh_0', -18, dict(align='peak', fade_in=0.03)),
    (V(26.67), 'el/boom_1', -19, dict(align='peak', trim_pre=0.1)),
    # F: the squeeze
    (V(31.90), 'sfx2/syn_riser_long', -20, dict(align='end', duck=6)),
    (V(31.90), 'sfx2/syn_land2', -17, dict(align='peak')),
    # G: the dot lands; the time lines; "That's the black hole."; the swell back into the loop
    (TG, 'el/boom_big_1', -21, dict(noduck=True, align='peak', trim_pre=0.35)),
    (TG, 'sfx2/syn_boom_big', -19, dict(noduck=True, align='peak')),
    # the dot's shimmer, chained (5.2 s each) to carry the ending; each takes over under the last one's fade
    (TG, 'sfx2/syn_shimmer_long', -21, dict(fade_out=(TG + 4.4, TG + 5.0))),
    (TG + 4.3, 'sfx2/syn_shimmer_long', -21, dict(fade_in=0.7, fade_out=(TG + 8.7, TG + 9.3))),
    (TG + 8.6, 'sfx2/syn_shimmer_long', -22, dict(fade_in=0.8, fade_out=(DUR - 0.9, DUR - 0.3))),
    # v2 references: Luminet's dots, Interstellar
    ('STIPPLE', 'sfx2/syn_chime', -25, {}),
    ('INTERSTELLAR', 'sfx2/syn_pop_low2', -20, {}),
    ('MINUTE', 'sfx2/syn_pop_low2', -21, {}),
    ('HOUR', 'el/pop_1', -19, {}),
    ('BLACK_HOLE', 'el/boom_2', -19, dict(align='peak', trim_pre=0.1)),
    ('BLACK_HOLE', 'sfx2/syn_pop_low2', -21, {}),
    (DUR, 'sfx2/syn_reverse_long', -21, dict(align='end')),
]


def peak_time(y):
    x = np.abs(y).max(axis=1)
    k = max(1, int(0.01 * SR))
    return float(np.argmax(np.convolve(x, np.ones(k) / k, 'same'))) / SR


# the music (composed for the 43.3 s cut: 6 bars of intro and orbit, 6 of build, a drop at bar 12 that decays to
# silence) re-arranged bar by bar for the 74.7 s cut.  Bars are placed on the video's beat grid so the drop's
# downbeat is the dot landing (62.0 s); the reveal, the arch and the visor flash fall on beats of the same grid.
# Bar 4-5, the steady arpeggio groove, loops under the explanations; the build (bars 6-11) runs from the light's lap
# to the dot.  After the drop's first second, its decay is stretched to fill the ending (a tone and its room tail).
def music_bars():
    """As many whole bars as fit before the drop: the opening four, the groove looped, the six-bar build."""
    n = int(shots.T_G_REAL // (4 * 60 / 90.0))
    return [0, 1, 2, 3] + [4, 5] * ((n - 10) // 2) + [4] * ((n - 10) % 2) + [6, 7, 8, 9, 10, 11]


def arrange_music(mu):
    bar = int(round(4 * 60 / 90.0 * SR)); xf = int(0.04 * SR)
    ramp = np.linspace(0, 1, xf)[:, None].astype(np.float32)
    MUSIC_BARS = music_bars()
    start = int(round((shots.T_G_REAL - len(MUSIC_BARS) * 4 * 60 / 90.0) * SR))     # under a bar in
    out = np.zeros((N + 2 * bar, mu.shape[1]), np.float32)
    pos = start
    for k, b in enumerate(MUSIC_BARS):
        seg = mu[b * bar:(b + 1) * bar + xf].copy()     # one bar plus a 40 ms overlap into the next
        seg[-xf:] *= 1 - ramp
        if k:
            seg[:xf] *= ramp                            # consecutive bars sum back to the original exactly
        out[pos:pos + len(seg)] += seg
        pos += bar
    # the drop: its first second as composed, the rest of its decay stretched to the end of the video
    import librosa
    a0, a1, b1 = 12 * bar, 12 * bar + SR, 14 * bar
    tail = np.stack([librosa.effects.time_stretch(np.ascontiguousarray(mu[a1:b1, c]), rate=(b1 - a1) / max(1, N - pos - SR))
                     for c in range(mu.shape[1])], axis=1).astype(np.float32)
    drop = np.concatenate([mu[a0:a1], tail])
    drop[:xf] *= ramp
    m = min(len(drop), len(out) - pos)
    out[pos:pos + m] += drop[:m]
    return out[:N]


def place(bus, t0, y, gain, opts):
    y = y * db(gain)
    if 'lp' in opts:
        y = lowpass(y, opts['lp'])
    align = opts.get('align', 'start')
    if align == 'peak':
        pt = peak_time(y)
        if 'trim_pre' in opts and pt > opts['trim_pre']:
            # keep only the last trim_pre seconds before the peak, faded in (a long build-up can read as a whine)
            k = int((pt - opts['trim_pre']) * SR); y = y[k:].copy(); pt = opts['trim_pre']
            n = int(opts['trim_pre'] * SR); y[:n] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n)))[:, None]
        t0 = t0 - pt
    elif align == 'end':
        t0 = t0 - len(y) / SR
    n = len(y)
    tt = t0 + np.arange(n) / SR
    env = np.ones(n, np.float32)
    if 'fade_in' in opts:
        env *= np.clip((tt - t0) / opts['fade_in'], 0, 1)
    if 'fade_out' in opts:
        a, b = opts['fade_out']
        env *= np.clip((b - tt) / (b - a), 0, 1)
    y = y * env[:, None]
    i0 = int(round(t0 * SR))
    j0 = max(0, -i0); i0 = max(0, i0)
    m = min(n - j0, N - i0)
    if m > 0:
        bus[i0:i0 + m] += y[j0:j0 + m]


def room_ir(seconds=1.6, seed=3):
    """A soft synthetic room for the effects bus: decorrelated decaying noise, darker as it decays."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t / (seconds / 6.9))[:, None]
    lo = lowpass(ir, 2500); hi = ir - lowpass(ir, 2500)
    ir = lo + hi * np.exp(-t / 0.08)[:, None]                  # highs die fast: a warm tail, no fizz
    ir[:int(0.018 * SR)] = 0                                   # 18 ms pre-delay keeps the dry hit clear
    return (ir / np.sqrt((ir ** 2).sum(axis=0))).astype(np.float32)


@nb.njit(cache=True)
def _follow(x, a, r):
    out = np.zeros_like(x); e = 0.0
    for i in range(x.shape[0]):
        v = x[i]
        c = a if v > e else r
        e = c * e + (1 - c) * v
        out[i] = e
    return out


@nb.njit(cache=True)
def _release(need, rel):
    g = np.ones_like(need); cur = 1.0
    for i in range(need.shape[0]):
        v = need[i]
        cur = v if v < cur else rel * cur + (1 - rel) * v
        g[i] = cur
    return g


def envelope(x, attack, release):
    """Peak-follower envelope (mono), attack/release in seconds."""
    return _follow(x.astype(np.float64), np.exp(-1.0 / (attack * SR)), np.exp(-1.0 / (release * SR)))


def true_peak_db(y):
    up = ss.resample_poly(y, 4, 1, axis=0)
    return 20 * np.log10(np.abs(up).max() + 1e-12)


def limiter(y, ceiling_db=-1.6, lookahead=0.005, release=0.08):
    """Lookahead brickwall on the 4x-oversampled peak estimate (applied at base rate with a safety margin)."""
    up = np.abs(ss.resample_poly(y, 4, 1, axis=0)).max(axis=1)
    pk = up.reshape(-1, 4).max(axis=1)[:len(y)] if len(up) >= 4 * len(y) else np.pad(up[::4], (0, len(y) - len(up[::4])))
    ceil = db(ceiling_db)
    need = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    la = int(lookahead * SR)
    need = minimum_filter1d(need, 2 * la + 1)              # look ahead and behind
    g = _release(need.astype(np.float64), np.exp(-1.0 / (release * SR)))
    g = uniform_filter1d(g, la)                             # smooth the gain so it doesn't click
    g = np.minimum(g, need)                                # never above what the peaks allow
    return (y * g[:, None]).astype(np.float32)


@nb.njit(cache=True)
def _gain_computer(lev_db, thr, ratio, knee, att, rel):
    """Soft-knee downward compressor gain (dB) from a level track, smoothed with attack/release coefficients."""
    g = np.zeros_like(lev_db); cur = 0.0
    for i in range(lev_db.shape[0]):
        over = lev_db[i] - thr
        if over <= -knee / 2:
            tgt = 0.0
        elif over >= knee / 2:
            tgt = -over * (1 - 1 / ratio)
        else:
            tgt = -(1 - 1 / ratio) * (over + knee / 2) ** 2 / (2 * knee)
        c = att if tgt < cur else rel
        cur = c * cur + (1 - c) * tgt
        g[i] = cur
    return g


def voice_chain(v):
    """De-ess, then gently compress, then a touch of the effects room (so voice and effects share a space)."""
    x = v[:, 0].astype(np.float64)
    coef = lambda s: np.exp(-1.0 / (s * SR))
    # de-esser: the 5-10 kHz band is held toward 14 dB under typical vowel level (4:1, at most 6 dB of reduction)
    sos = ss.butter(4, [5000 / (SR / 2), 10000 / (SR / 2)], 'band', output='sos')
    sib = ss.sosfilt(sos, x)
    body = ss.sosfilt(ss.butter(4, [150 / (SR / 2), 1500 / (SR / 2)], 'band', output='sos'), x)
    w = int(0.005 * SR)
    se = np.sqrt(np.maximum(uniform_filter1d(sib ** 2, w), 1e-20))
    be = np.sqrt(np.maximum(uniform_filter1d(body ** 2, int(0.01 * SR)), 1e-20))
    vowel = np.percentile(be[be > be.max() * 0.03], 90)
    gd = _gain_computer(20 * np.log10(se), 20 * np.log10(vowel) - 14.0, 4.0, 4.0, coef(0.002), coef(0.06))
    gd = np.maximum(gd, -6.0)
    x = x - (1 - 10 ** (gd / 20)) * sib
    # compressor: 2.5:1 with a 6 dB knee on a 10 ms RMS, 10 ms attack, 150 ms release (about 3 dB on peaks)
    lev = 20 * np.log10(np.sqrt(np.maximum(uniform_filter1d(x ** 2, int(0.01 * SR)), 1e-20)))
    act = lev > lev.max() - 30
    thr = np.percentile(lev[act], 70)
    gc = _gain_computer(lev, thr, 2.5, 6.0, coef(0.010), coef(0.150))
    x = x * 10 ** (gc / 20)
    y = np.stack([x, x], axis=1).astype(np.float32)
    wet = ss.fftconvolve(y, room_ir(1.2, seed=5), axes=0)[:len(y)].astype(np.float32)
    return y + wet * db(-26.0)


def main():
    meter = pyln.Meter(SR)
    # ---- voice
    vo = load(os.path.join(B, 'vo.wav'))
    vo = np.repeat(vo[:, :1], 2, axis=1)[:N]
    vo = np.pad(vo, ((0, N - len(vo)), (0, 0)))
    vo = voice_chain(highpass(vo, 80))
    # speech mask from the voice signal itself (40 ms RMS above -45 dBFS, bridged over short gaps)
    w40 = int(0.04 * SR)
    r = np.sqrt(np.maximum(uniform_filter1d(vo[:, 0] ** 2, w40), 0))
    speech = r > db(-45)
    speech = uniform_filter1d(speech.astype(float), int(0.15 * SR)) > 0
    vo_l = meter.integrated_loudness(vo[speech])
    vo *= db(-16.0 - vo_l)                           # voice stem at -16 LUFS over its speech

    # ---- music: pull onto the bar grid, set 9 dB under the voice, duck under speech
    mu = decode(os.path.join(A, 'music_v2.mp3'))
    mu = mu[int(MUSIC_SHIFT * SR):]
    mu = arrange_music(mu)
    mu = np.pad(mu, ((0, max(0, N - len(mu))), (0, 0)))[:N]
    mu_l = meter.integrated_loudness(mu)
    mu *= db(-16.0 - 9.0 - mu_l)
    # time-varying ceiling: the bed's 400 ms RMS never exceeds the voice's typical speech RMS minus 9 dB
    w4 = int(0.4 * SR)
    vr = np.sqrt(np.maximum(uniform_filter1d(vo[:, 0] ** 2, w4), 0))
    v_ref = np.median(20 * np.log10(vr[speech] + 1e-9))
    mr = np.sqrt(np.maximum(uniform_filter1d((mu ** 2).mean(axis=1), w4), 0))
    # while speaking, also stay 8 dB under the voice's own local level (quiet words included)
    ceil_db = np.full(N, v_ref - 9.0)
    ceil_db[speech] = np.minimum(v_ref - 9.0, 20 * np.log10(vr[speech] + 1e-9) - 8.0)
    ceil = db(ceil_db)
    g_ceil = np.minimum(1.0, ceil / np.maximum(mr, 1e-9))
    g_ceil = minimum_filter1d(g_ceil, w4)
    g_ceil = uniform_filter1d(g_ceil, w4)
    mu = mu * g_ceil[:, None].astype(np.float32)
    # sidechain on phrases, not syllables: the speech mask smoothed over 300 ms, 80 ms attack, 600 ms release.
    # (v1 followed the voice envelope word by word, which pumped the bed and the effects by up to 4.5 dB per phrase)
    presence = envelope(uniform_filter1d(speech.astype(float), int(0.3 * SR)), 0.08, 0.6)
    vk = np.clip(presence / 0.5, 0, 1)                         # 0 = silence, 1 = speaking
    env = vk
    duck = 1.0 - (1.0 - db(-5.0)) * vk
    mu = mu * duck[:, None]
    # short fades at the ends so the loop seam has no click
    f = int(0.02 * SR)
    mu[:f] *= np.linspace(0, 1, f)[:, None]; mu[-f:] *= np.linspace(1, 0, f)[:, None]

    # ---- sfx
    sfx = np.zeros((N, 2), np.float32)
    cache = {}
    import sys as _sys
    _sys.path.insert(0, os.path.join(HERE, '..'))
    from bh.timeline_overlay import back_front_times, black_hole_time, minute_times
    from bh.inserts import cue_times
    IC = cue_times()
    for t0, name, g, opts in CUES:
        if t0 == 'BLACK_HOLE':
            t0 = black_hole_time()                             # the hit lands with "That's the black hole."
        elif t0 in ('BACK', 'FRONT'):
            t0 = back_front_times()[t0 == 'FRONT']              # the tag pops land with "Back half, front half."
        elif t0 in IC:
            t0 = IC[t0]
        elif t0 in ('MINUTE', 'HOUR'):
            t0 = minute_times()[t0 == 'HOUR']                   # 1 MIN pops, then counts up to 32 MIN
        if 'fade_out' in opts and isinstance(opts['fade_out'][0], str):      # (cue, from, to) relative to a named cue
            c, d0, d1 = opts['fade_out']; opts = dict(opts, fade_out=(IC[c] + d0, IC[c] + d1))
        if name not in cache:
            cache[name] = load(os.path.join(A, name + '.wav'))
            if cache[name].shape[1] == 1:
                cache[name] = np.repeat(cache[name], 2, axis=1)
        bus = np.zeros((N, 2), np.float32)
        place(bus, t0, cache[name], g, opts)
        # every effect dips 3 dB under the voice; cues that play under speech are sidechained further
        d = 0.0 if opts.get('noduck') else 3.0 + opts.get('duck', 0)     # hits land in speech gaps: never ducked
        sfx += bus * (1.0 - (1.0 - db(-d)) * vk)[:, None].astype(np.float32)
    # one shared warm room so the effects sit in the same space as each other (send at -12 dB, unit-energy IR)
    wet = ss.fftconvolve(sfx, room_ir(), axes=0)[:N].astype(np.float32)
    sfx = sfx + wet * db(-12.0)
    sfx = (sfx - (1 - db(-1.5)) * (sfx - lowpass(sfx, 6000))).astype(np.float32)   # -1.5 dB above 6 kHz

    mix = vo + mu + sfx
    # ---- master: limiter then linear gain to -14 LUFS, limiter again for the true-peak ceiling
    for _ in range(3):
        L = meter.integrated_loudness(mix)
        mix = mix * db(-14.0 - L)
        mix = limiter(mix, -1.6)
    sf.write(os.path.join(B, 'mix.wav'), mix, SR, subtype='FLOAT')
    sf.write(os.path.join(B, 'stem_vo.wav'), vo, SR, subtype='FLOAT')
    sf.write(os.path.join(B, 'stem_music.wav'), mu, SR, subtype='FLOAT')
    sf.write(os.path.join(B, 'stem_sfx.wav'), sfx, SR, subtype='FLOAT')
    # ---- report: music vs voice while speaking (400 ms windows)
    w = int(0.4 * SR)
    diffs = []
    for i in range(0, N - w, w):
        if speech[i:i + w].mean() > 0.9:
            v = 20 * np.log10(np.sqrt((vo[i:i + w] ** 2).mean()) + 1e-9)
            m = 20 * np.log10(np.sqrt((mu[i:i + w] ** 2).mean()) + 1e-9)
            diffs.append(v - m)
    print('integrated %.2f LUFS, true peak %.2f dBTP' % (meter.integrated_loudness(mix), true_peak_db(mix)))
    print('voice minus music while speaking (RMS, 400 ms windows): min %.1f dB, median %.1f dB' % (min(diffs), np.median(diffs)))
    print('music peak amplitude relative to voice peak: %.2f' % (np.abs(mu).max() / np.abs(vo).max()))
    a, b = int(16.0 * SR), int(17.8 * SR)
    sp = speech[a:b]
    print('dive line: voice minus (music + sfx) %.1f dB' % (20 * np.log10(np.sqrt((vo[a:b][sp] ** 2).mean()) /
                                                               np.sqrt(((mu + sfx)[a:b][sp] ** 2).mean()))))


if __name__ == '__main__':
    main()
