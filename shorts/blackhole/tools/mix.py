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
DUR = 14 * 4 * 60 / 90.0          # 37.333 s
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


# (video time, file, gain dB, options)
CUES = [
    (0.00, 'impact_b', -16, dict(lp=1800)),
    (0.00, 'shimmer_a', -17, dict(fade_out=(2.3, 2.67))),
    (0.62, 'reverse_a', -15, dict(fade_out=(2.60, 2.70))),
    (2.29, 'whoosh_b', -13, {}),
    (2.67, 'impact_b', -9, {}),
    (5.72, 'whoosh_a', -18, {}),
    (7.10, 'tick_b', -16, {}),
    (7.30, 'tick_b', -18, {}),
    (8.60, 'whoosh_b', -16, {}),
    (9.28, 'whoosh_a', -16, {}),
    (10.67, 'impact_b', -7, {}),
    (10.90, 'tick_b', -20, {}),
    (11.15, 'tick_b', -22, {}),
    (13.21, 'riser_a', -22, {}),
    (16.00, 'dive_a', -10, {}),
    (16.00, 'boom_a', -22, dict(lp=400, fade_in=0.4, fade_out=(18.2, 18.7))),
    (18.67, 'impact_b', -7, {}),
    (18.67, 'shimmer_a', -20, dict(fade_out=(21.8, 22.2))),
    (20.79, 'zip_b', -17, {}),
    (21.82, 'whoosh_b', -15, {}),
    (22.70, 'zip_a', -13, {}),
    (24.00, 'ping_a', -9, {}),
    (25.15, 'whip_a', -13, {}),
    (25.90, 'whip_a', -19, {}),
    (26.29, 'whoosh_b', -15, {}),
    (26.54, 'riser_a', -19, {}),
    (32.00, 'impact_b', -9, {}),
    (32.00, 'shimmer_a', -16, dict(fade_out=(36.4, 37.0))),
    (34.90, 'impact_b', -17, dict(lp=900)),
    (35.13, 'reverse_a', -19, dict(fade_out=(37.10, 37.33))),
]


def place(bus, t0, y, gain, opts):
    y = y * db(gain)
    if 'lp' in opts:
        y = lowpass(y, opts['lp'])
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


def main():
    meter = pyln.Meter(SR)
    # ---- voice
    vo = load(os.path.join(B, 'vo.wav'))
    vo = np.repeat(vo[:, :1], 2, axis=1)[:N]
    vo = np.pad(vo, ((0, N - len(vo)), (0, 0)))
    vo = highpass(vo, 70)
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
    vox = np.abs(vo).max(axis=1)
    env = envelope(vox, 0.03, 0.35)
    duck = 1.0 - (1.0 - db(-5.0)) * np.clip(env / 0.05, 0, 1)
    mu = mu * duck[:, None]
    # short fades at the ends so the loop seam has no click
    f = int(0.02 * SR)
    mu[:f] *= np.linspace(0, 1, f)[:, None]; mu[-f:] *= np.linspace(1, 0, f)[:, None]

    # ---- sfx
    sfx = np.zeros((N, 2), np.float32)
    cache = {}
    for t0, name, g, opts in CUES:
        if name not in cache:
            cache[name] = load(os.path.join(A, 'sfx', name + '.wav'))
            if cache[name].shape[1] == 1:
                cache[name] = np.repeat(cache[name], 2, axis=1)
        place(sfx, t0, cache[name], g, opts)

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


if __name__ == '__main__':
    main()
