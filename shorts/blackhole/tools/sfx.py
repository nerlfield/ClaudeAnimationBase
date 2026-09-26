"""Sound kit v2: every effect is either synthesised here or generated with ElevenLabs sound generation.

    python tools/sfx.py synth                 # write the synthesised designs to build/audio/sfx2/syn_*.wav
    python tools/sfx.py el                    # fetch ElevenLabs takes (cached) to build/audio/el/*.wav
    python tools/sfx.py pick                  # rank every candidate per role, write build/audio/sfx2/<role>.wav

Design rules (the v1 kit, from Mirelo, measured 90% of the dive whoosh above 6 kHz and 99% of a whoosh in the
harsh 2-5 kHz band): soft attacks (>= 4 ms, raised cosine), no energy above ~9 kHz, a harmonic "body" on every
low hit so it still reads on phone speakers, and pitched material on one chord (E major add9) so hits, pops and
shimmers agree with each other.  The ElevenLabs key is read from ELEVENLABS_API_KEY and never written anywhere.
"""
import json
import os
import re
import sys
import urllib.request

import numpy as np
import scipy.signal as ss
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'build', 'audio', 'sfx2')
ELD = os.path.join(HERE, '..', 'build', 'audio', 'el')
SR = 44100
# the music bed (ElevenLabs) centres on A, E and D (chroma 0.65 / 0.60 / 0.59, between A major and D minor), so
# every pitched effect uses only A, D and E: an open "sus" colour that can't clash with either reading
A4, D5, E5 = 440.0, 587.33, 659.26
KEY_HZ = [A4 / 8 * 2 ** k for k in range(8)] + [D5 / 16 * 2 ** k for k in range(8)] + [E5 / 16 * 2 ** k for k in range(8)]
CHORD = [A4 * 2, E5 * 2, D5 * 2, A4 * 4, E5 * 4]          # A5 E6 D6 A6 E7


# ---------------------------------------------------------------- helpers
def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def rc_attack(t, a):
    """Raised-cosine attack over a seconds (no click)."""
    return np.where(t < a, 0.5 - 0.5 * np.cos(np.pi * np.clip(t / max(a, 1e-6), 0, 1)), 1.0)


def fade_out(x, d=0.05):
    n = min(len(x), int(d * SR))
    x = x.copy(); x[-n:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n)))[:, None] if x.ndim == 2 else (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n)))
    return x


def lp(x, hz, order=2):
    sos = ss.butter(order, hz / (SR / 2), 'low', output='sos'); return ss.sosfilt(sos, x, axis=0)


def hp(x, hz, order=2):
    sos = ss.butter(order, hz / (SR / 2), 'high', output='sos'); return ss.sosfilt(sos, x, axis=0)


def shelf_high(x, hz, gain_db):
    """First-order high shelf (gain above hz)."""
    g = 10 ** (gain_db / 20)
    return x + (g - 1) * hp(x, hz, 1)


def pink(n, rng):
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR); f[0] = f[1]
    y = np.fft.irfft(X / np.sqrt(f), n)
    return y / np.abs(y).max()


def band_sweep(noise, fc_of_t, octaves=1.0):
    """Time-varying band-pass by STFT masking: a Gaussian band (in log frequency) centred on fc(t)."""
    f, tt, Z = ss.stft(noise, SR, nperseg=2048, noverlap=1536)
    lf = np.log2(np.maximum(f, 1.0))[:, None]
    fc = np.log2(np.maximum(fc_of_t(tt), 20.0))[None, :]
    Z = Z * np.exp(-0.5 * ((lf - fc) / (octaves / 2)) ** 2)
    _, y = ss.istft(Z, SR, nperseg=2048, noverlap=1536)
    y = y[:len(noise)]
    return np.pad(y, (0, len(noise) - len(y)))


def pan(mono, p):
    """Equal-power pan; p in -1..1 (scalar or per-sample)."""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([mono * np.cos(a), mono * np.sin(a)], axis=1)


def widen(mono, ms=9.0):
    d = int(ms / 1000 * SR)
    return np.stack([mono, np.concatenate([np.zeros(d), mono[:-d]])], axis=1) * 0.85


def finish(x, top=9000.0):
    """Every effect ends here: gentle top roll-off, -2 dB shelf above 5 kHz, short fades, peak at -1 dBFS."""
    x = np.atleast_2d(x.T).T if x.ndim == 1 else x
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    x = lp(x, top, 2)
    x = shelf_high(x, 5000.0, -2.0)
    n = int(0.003 * SR); x[:n] *= np.linspace(0, 1, n)[:, None]
    x = fade_out(x, 0.04)
    return (x / (np.abs(x).max() + 1e-9) * 10 ** (-1 / 20)).astype(np.float32)


def sine_glide(t, f_of_t, phase=0.0):
    return np.sin(2 * np.pi * np.cumsum(f_of_t(t)) / SR + phase)


# ---------------------------------------------------------------- synthesised designs
def syn_boom(dur=3.2, f0=82.41, f1=41.2, big=False, seed=1, sub_g=0.6, drive=3.0, knock_g=0.8, skin_g=0.9):
    """Soft cinematic hit in three layers: a pitch-dropping sub (felt on headphones), a saturated knock whose
    harmonics carry the hit on phone speakers, and a muffled "skin" of band noise at 0.4-1.5 kHz.  Every layer has a
    rounded attack of 5 ms or more, and nothing above ~2.5 kHz except the bloom on big hits."""
    rng = np.random.default_rng(seed); t = t_axis(dur)
    f = f1 + (f0 - f1) * np.exp(-t / 0.22)
    sub = sine_glide(t, lambda _: f) * rc_attack(t, 0.010) * np.exp(-t / (1.3 if big else 0.9))
    knock = sine_glide(t, lambda tt: f0 * 1.33 + f0 * 1.6 * np.exp(-tt / 0.03)) * np.exp(-t / 0.16)
    # saturate first, then shape the attack: saturating a rising edge would squash a 9 ms attack to ~3 ms
    knock = lp(np.tanh(drive * knock) / np.tanh(drive), 1800, 2) * rc_attack(t, 0.012)
    skin = band_sweep(pink(len(t), rng), lambda tt: 1100 * np.exp(-tt / 0.12) + 420, 1.2)
    skin = lp(skin, 2500, 2) * rc_attack(t, 0.010) * np.exp(-t / 0.11)
    air = lp(pink(len(t), rng), 900, 2) * rc_attack(t, 0.006) * np.exp(-t / 0.3) * 0.3
    x = widen(sub * sub_g + knock * knock_g) + widen(skin * skin_g / (np.abs(skin).max() + 1e-9) * 0.5, 17) + widen(air, 13)
    if big:
        # a bright bloom on the A-sus chord that rises out of the hit and rings for the "wow"
        bl = sum(np.sin(2 * np.pi * fr / 2 * t * (1 + 0.0015 * s)) * g for fr, g in zip(CHORD[:5], [0.5, 0.35, 0.3, 0.2, 0.12])
                 for s in (-1, 1))
        bl = bl * rc_attack(t, 0.25) * np.exp(-np.maximum(t - 0.25, 0) / 1.6) * 0.09
        x = x + widen(lp(bl, 5000), 11)
    return finish(x, 6000)


def syn_whoosh(dur=1.3, f_lo=260.0, f_hi=1300.0, peak=0.6, direction=1, seed=2, air=0.0):
    """Airy pass-by: pink noise through a band that swells up and back down, panned across."""
    rng = np.random.default_rng(seed); t = t_axis(dur); T = dur
    u = np.clip(t / T, 0, 1)
    def fc(tt):
        uu = np.clip(tt / T, 0, 1)
        k = np.where(uu < peak, uu / peak, 1 - (uu - peak) / (1 - peak))
        return f_lo * (f_hi / f_lo) ** (np.sin(np.pi / 2 * k) ** 1.5)
    env = np.sin(np.pi * np.clip(np.where(u < peak, u / peak * 0.5, 0.5 + (u - peak) / (1 - peak) * 0.5), 0, 1)) ** 2
    nL = band_sweep(pink(len(t), rng), fc, 1.2); nR = band_sweep(pink(len(t), rng), fc, 1.2)
    x = np.stack([nL, nR], axis=1) * env[:, None]
    p = direction * (-0.7 + 1.4 * u)
    x = x * np.stack([np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)], axis=1) * 1.4
    if air:
        x = x + air * np.stack([lp(hp(pink(len(t), rng), 2000), 6000)] * 2, axis=1) * env[:, None] * 0.2
    return finish(x, 7000)


def syn_dive(dur=2.75, seed=3):
    """The dive: a long accelerating rush that swells low and wide, then brakes into the arrival."""
    rng = np.random.default_rng(seed); t = t_axis(dur); u = t / dur
    fc = lambda tt: 260 * (1900 / 260) ** (np.clip(tt / dur, 0, 1) ** 1.4)
    rush = np.stack([band_sweep(pink(len(t), rng), fc, 1.5), band_sweep(pink(len(t), rng), fc, 1.5)], axis=1) * 2.2
    env = (np.clip(u / 0.85, 0, 1) ** 1.8) * np.where(u > 0.9, np.clip((1 - u) / 0.1, 0, 1) ** 0.7, 1.0)
    rumble = lp(pink(len(t), rng), 110, 4) * 1.1 * env
    tone = sine_glide(t, lambda tt: 55 * (1 + 1.2 * (tt / dur) ** 2)) * env * 0.25        # a deep engine-like glide
    body = lp(np.tanh(2.0 * tone), 400)
    x = rush * env[:, None] + widen(rumble + tone + body * 0.6, 7)
    return finish(x, 6000)


def syn_riser(dur=2.6, seed=4, tone=True):
    """Tension into a cut: a noise band climbing to ~2.5 kHz and an octave glide on the chord root, ending on time."""
    rng = np.random.default_rng(seed); t = t_axis(dur); u = t / dur
    fc = lambda tt: 180 * (2500 / 180) ** np.clip(tt / dur, 0, 1)
    wash = np.stack([band_sweep(pink(len(t), rng), fc, 1.0), band_sweep(pink(len(t), rng), fc, 1.0)], axis=1)
    env = u ** 2.2
    x = wash * env[:, None] * 0.8
    if tone:
        g = sine_glide(t, lambda tt: 110.0 * 2 ** (np.clip(tt / dur, 0, 1) * 1.0))       # A2 -> A3
        g2 = sine_glide(t, lambda tt: 164.81 * 2 ** (np.clip(tt / dur, 0, 1) * 1.0))     # E3 -> E4
        x = x + widen((g * 0.5 + g2 * 0.3) * env * 0.5, 8)
    n = int(0.03 * SR); x[-n:] *= np.linspace(1, 0, n)[:, None]
    return finish(x, 6500)


def syn_shimmer(dur=3.0, seed=5, attack=0.45, level_drift=True, sparkle=0.5):
    """A glassy halo on A-sus (A5 E6 D6 A6 E7): detuned pairs beat slowly, each partial breathes on its own slow
    LFO, and soft in-key sparkle grains twinkle over it.  Soft attack, long release."""
    rng = np.random.default_rng(seed); t = t_axis(dur)
    parts = list(zip(CHORD, [0.42, 0.3, 0.2, 0.15, 0.06]))
    L = np.zeros(len(t)); R = np.zeros(len(t))
    for fr, g in parts:
        ph = rng.uniform(0, 2 * np.pi, 3)
        lfo = 1 + (0.25 * np.sin(2 * np.pi * rng.uniform(0.2, 0.6) * t + ph[2]) if level_drift else 0)
        L += g * lfo * np.sin(2 * np.pi * fr * (1 - 0.0011) * t + ph[0])
        R += g * lfo * np.sin(2 * np.pi * fr * (1 + 0.0011) * t + ph[1])
    if sparkle:
        for _ in range(int(dur * 7)):
            t0 = rng.uniform(0, dur - 0.3); fr = rng.choice(CHORD[1:]) * rng.choice([1, 2])
            n = int(0.35 * SR); i0 = int(t0 * SR); tt = np.arange(n) / SR
            g = np.sin(2 * np.pi * min(fr, 5300) * tt) * rc_attack(tt, 0.012) * np.exp(-tt / 0.09) * sparkle * 0.12
            pp = rng.uniform(-0.8, 0.8)
            L[i0:i0 + n] += g[:len(L) - i0] * np.cos((pp + 1) * np.pi / 4); R[i0:i0 + n] += g[:len(R) - i0] * np.sin((pp + 1) * np.pi / 4)
    env = rc_attack(t, attack) * np.clip((dur - t) / 0.8, 0, 1)
    x = np.stack([L, R], axis=1) * env[:, None]
    return finish(lp(x, 5500), 6000)


def syn_reverse_swell(dur=1.8, seed=6):
    """A reversed bloom that swells into the cut (reversed shimmer plus a reversed dark wash)."""
    rng = np.random.default_rng(seed); t = t_axis(dur)
    bloom = syn_shimmer(dur, seed, attack=0.01, level_drift=False, sparkle=0).astype(np.float64)
    decay = np.exp(-t / 0.55)[:, None]
    wash = np.stack([lp(pink(len(t), rng), 2500), lp(pink(len(t), rng), 2500)], axis=1) * np.exp(-t / 0.4)[:, None] * 0.5
    x = (bloom * decay + wash)[::-1]
    n = int(0.02 * SR); x[-n:] *= np.linspace(1, 0, n)[:, None]
    return finish(x, 6000)


def syn_pop(f0=520.0, f1=1100.0, dur=0.3, seed=7, thump=0.0):
    """A soft, round bubble pop: a fast upward sine chirp (a bubble's resonance rises as it closes) with a warm
    body an octave down; no noise click."""
    t = t_axis(dur)
    f = f1 - (f1 - f0) * np.exp(-t / 0.022)
    s = sine_glide(t, lambda _: f) * rc_attack(t, 0.007) * np.exp(-t / 0.06)
    body = sine_glide(t, lambda _: f / 2) * rc_attack(t, 0.008) * np.exp(-t / 0.05) * 0.4
    x = s + body
    if thump:
        th = sine_glide(t, lambda tt: 55 + 55 * np.exp(-tt / 0.03)) * rc_attack(t, 0.008) * np.exp(-t / 0.18)
        x = x + thump * (th + lp(np.tanh(2.5 * th), 350) * 0.5)
    return finish(widen(x, 4), 7000)


def syn_chime(dur=2.2, seed=8):
    """The visor flash: a soft FM bell on A5 with a warm A4 and E5 under it."""
    t = t_axis(dur); fc = A4 * 2; fm = fc * 1.4
    idx = 2.2 * np.exp(-t / 0.35) + 0.2
    bell = np.sin(2 * np.pi * fc * t + idx * np.sin(2 * np.pi * fm * t)) * rc_attack(t, 0.004) * np.exp(-t / 0.9)
    warm = np.sin(2 * np.pi * A4 * t) * rc_attack(t, 0.006) * np.exp(-t / 1.1) * 0.55
    fifth = np.sin(2 * np.pi * E5 * t) * rc_attack(t, 0.02) * np.exp(-t / 0.7) * 0.2
    x = widen(bell * 0.6 + warm + fifth, 6)
    return finish(lp(x, 6500), 7000)


def syn_glide(dur=1.35, seed=9):
    """The pulse's lap around the ring: a smooth rising tone with a soft airy trail, panned left to right."""
    rng = np.random.default_rng(seed); t = t_axis(dur); u = t / dur
    f = lambda tt: A4 * (3.0 ** np.clip(tt / dur, 0, 1)) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt))     # A4 -> E6
    tone = sine_glide(t, f) + 0.25 * sine_glide(t, lambda tt: 2 * f(tt))
    trail = band_sweep(pink(len(t), rng), lambda tt: 2 * f(tt), 0.6) * 0.6
    env = rc_attack(t, 0.18) * np.clip((dur - t) / 0.08, 0, 1)
    x = pan((tone * 0.6 + trail) * env, -0.6 + 1.2 * u)
    return finish(x, 7000)


def pluck(fr, dur, t_attack=0.008):
    """An additive harp-like pluck: harmonics fall off in level and the higher ones decay faster."""
    t = t_axis(dur); x = np.zeros(len(t))
    for h in range(1, 9):
        if fr * h > 7000:
            break
        x += h ** -1.3 * np.sin(2 * np.pi * fr * h * t * (1 + 0.0004 * h * h)) * np.exp(-t / (1.1 / h ** 0.8))
    return x * rc_attack(t, t_attack)


def syn_gliss(dur=1.4, seed=20):
    """The pulse's lap: a soft harp glissando up the A-sus notes, travelling left to right, so the chime that
    follows (A5 + E6) lands as its resolution.  Replaces a pure rising sine that read as a slide whistle."""
    notes = [A4 / 2, D5 / 2, E5 / 2, A4, D5, E5, A4 * 2, D5 * 2, E5 * 2]
    n = int((dur + 1.2) * SR); x = np.zeros((n, 2))
    for k, fr in enumerate(notes):
        t0 = dur * (k / (len(notes) - 1)) ** 0.85 * 0.92
        p = pluck(fr, 1.2) * (0.55 + 0.45 * k / len(notes))
        i0 = int(t0 * SR); pp = -0.7 + 1.4 * k / (len(notes) - 1)
        seg = pan(p, pp); m = min(len(seg), n - i0)
        x[i0:i0 + m] += seg[:m]
    return finish(lp(x, 6000), 6500)


def syn_sparkle_sweep(dur=0.95, seed=21):
    """The glow running along the horizon line: a soft air swoosh left to right with three sparkle plucks."""
    rng = np.random.default_rng(seed)
    base = syn_whoosh(dur, 350.0, 1400.0, 0.7, seed=seed).astype(np.float64) * 0.7
    n = len(base) + int(0.9 * SR); x = np.zeros((n, 2)); x[:len(base)] += base
    for k, fr in enumerate([A4 * 2, D5 * 2, E5 * 2]):
        i0 = int(dur * (0.35 + 0.25 * k) * SR)
        seg = pan(pluck(fr, 0.9) * 0.25, -0.3 + 0.5 * k); m = min(len(seg), n - i0)
        x[i0:i0 + m] += seg[:m]
    return finish(x, 7000)


def syn_swish(dur=0.32, seed=10, hi=1400.0, lo=420.0):
    """A quick soft swish for the double take."""
    return syn_whoosh(dur, lo, hi, peak=0.35, seed=seed)


def syn_sweep_tone(dur=0.95, seed=11):
    """The glow running along the horizon line: a short riser that follows it left to right."""
    rng = np.random.default_rng(seed); t = t_axis(dur); u = t / dur
    g = sine_glide(t, lambda tt: E5 * (A4 * 2 / E5) ** np.clip(tt / dur, 0, 1))       # E5 -> A5
    wash = band_sweep(pink(len(t), rng), lambda tt: 600 * 4 ** np.clip(tt / dur, 0, 1), 0.8)
    env = np.sin(np.pi * np.clip(u, 0, 1)) ** 1.5
    x = pan((g * 0.45 + wash * 0.8) * env, -0.8 + 1.6 * u)
    return finish(x, 7000)


def from_take(name):
    y, sr = sf.read(os.path.join(ELD, name + '.wav'), always_2d=True)
    return y.astype(np.float64)


def repitch(y, ratio):
    """Tape-style pitch change (ratio > 1 = higher and shorter)."""
    from fractions import Fraction
    fr = Fraction(ratio).limit_denominator(200)
    return ss.resample_poly(y, fr.denominator, fr.numerator, axis=0)


def land_sound():
    """The counter locking onto a value: the ElevenLabs pop a fifth lower, on a soft knock."""
    pop = repitch(from_take('pop_1'), 2 / 3)
    knock = syn_boom(1.2, 82.41, 41.2, seed=22, sub_g=0.3, knock_g=1.0, skin_g=0.6).astype(np.float64)
    n = max(len(pop), len(knock)); x = np.zeros((n, 2))
    x[:len(pop)] += pop / np.abs(pop).max(); x[:len(knock)] += knock * 0.55
    return finish(x, 6000)


def swish_sound(seed=0):
    """A short swish cut from the peak of a clean ElevenLabs whoosh (0.34 s, soft fades)."""
    y = from_take('whoosh_1')
    k = int(0.01 * SR); e = np.convolve(np.abs(y).max(axis=1), np.ones(k) / k, 'same'); ip = int(np.argmax(e))
    a = max(0, ip - int(0.2 * SR)); seg = y[a:a + int(0.34 * SR)].copy()
    n = int(0.12 * SR); seg[:n] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n)))[:, None]
    m = int(0.14 * SR); seg[-m:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, m)))[:, None]
    return finish(repitch(seg, 1.12), 7000)


SYNTH = {
    'boom': lambda: syn_boom(),
    'boom_big': lambda: syn_boom(4.2, 110.0, 55.0, big=True, seed=12),
    'boom_soft': lambda: syn_boom(2.6, 82.41, 41.2, seed=13),
    'whoosh': lambda: syn_whoosh(),
    'whoosh_long': lambda: syn_whoosh(1.8, 200.0, 1100.0, 0.55, seed=14),
    'dive': lambda: syn_dive(),
    'riser': lambda: syn_riser(),
    'riser_long': lambda: syn_riser(4.9, seed=15),
    'shimmer': lambda: syn_shimmer(3.0),
    'shimmer_long': lambda: syn_shimmer(5.2, seed=16),
    'reverse': lambda: syn_reverse_swell(1.8),
    'reverse_long': lambda: syn_reverse_swell(2.1, seed=17),
    'pop': lambda: syn_pop(),
    'pop_low': lambda: syn_pop(390.0, 830.0, seed=18),
    'land': lambda: syn_pop(330.0, 660.0, 0.6, seed=19, thump=0.8),
    'chime': lambda: syn_chime(),
    'glide': lambda: syn_glide(),
    'gliss': lambda: syn_gliss(),
    'land2': lambda: land_sound(),
    'pop_low2': lambda: finish(repitch(from_take('pop_1'), 0.84)),
    'swish2': lambda: swish_sound(),
    'sparkle': lambda: syn_sparkle_sweep(),
    'swish': lambda: syn_swish(),
    'sweep': lambda: syn_sweep_tone(),
}

# ---------------------------------------------------------------- ElevenLabs takes
# (role, prompt, seconds, prompt influence)
EL_PROMPTS = [
    ('boom', 'Deep soft cinematic sub boom impact, warm and round, smooth low tail, no crack, no click, no distortion', 3.0, 0.6),
    ('boom_big', 'Huge warm cinematic bass drop with a soft glowing shimmer tail, awe, space documentary, smooth, no crack', 4.0, 0.6),
    ('whoosh', 'Soft airy whoosh passing by, smooth wind swell, gentle, no hiss, no whistle', 1.4, 0.6),
    ('dive', 'Smooth deep whooshing rush accelerating toward something, warm low wind and rumble building, cinematic space dive, no hiss', 3.0, 0.55),
    ('riser', 'Gentle cinematic riser, smooth swelling tone and soft air building tension, warm, no harsh noise', 2.6, 0.55),
    ('shimmer', 'Soft glassy shimmering pad, gentle high twinkle halo, calm space ambience, warm, smooth', 3.0, 0.5),
    ('chime', 'Single soft glass bell chime, warm and bright, gentle attack, clean ring', 2.0, 0.6),
    ('pop', 'Soft round bubble pop, satisfying user interface pop, warm, gentle', 0.5, 0.6),
    ('reverse', 'Soft reverse cymbal swell rising smoothly, warm, gentle, cinematic', 2.0, 0.55),
    ('riser_long', 'Slow cinematic riser building tension over five seconds, warm swelling tone and soft air rising smoothly, no harsh noise, no hiss', 5.0, 0.55),
    ('swish', 'Quick soft whip swish, short airy cartoon head turn, gentle, no hiss', 0.5, 0.6),
    ('whoosh_mid', 'Soft breathy whoosh of air passing close by, mid-range, smooth, like a quick camera pan, no rumble, no hiss', 1.4, 0.6),
]


def el_fetch(role, prompt, dur, influence, take):
    os.makedirs(ELD, exist_ok=True)
    path = os.path.join(ELD, f'{role}_{take}.wav')
    if os.path.exists(path):
        return path
    body = dict(text=prompt, duration_seconds=dur, prompt_influence=influence, model_id='eleven_text_to_sound_v2')
    req = urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation?output_format=pcm_44100',
                                 data=json.dumps(body).encode(),
                                 headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        pcm = np.frombuffer(r.read(), '<i2').astype(np.float32) / 32768.0
    x = pcm.reshape(-1, 2)
    sf.write(path, finish(x.astype(np.float64)), SR, subtype='FLOAT')
    json.dump(dict(prompt=prompt, seconds=dur, prompt_influence=influence, model='eleven_text_to_sound_v2'),
              open(path[:-4] + '.json', 'w'))
    return path


# ---------------------------------------------------------------- ranking
WANT = {
    'boom': 'a soft deep cinematic boom', 'boom_big': 'a huge warm cinematic bass drop with a shimmering tail',
    'boom_soft': 'a soft deep cinematic boom', 'whoosh': 'a smooth airy whoosh', 'whoosh_long': 'a smooth airy whoosh',
    'dive': 'a deep whooshing rush accelerating', 'riser': 'a rising cinematic riser', 'riser_long': 'a rising cinematic riser',
    'shimmer': 'a gentle shimmering chime', 'shimmer_long': 'a gentle shimmering chime', 'reverse': 'a reverse cymbal swell',
    'reverse_long': 'a reverse cymbal swell', 'pop': 'a soft bubble pop', 'pop_low': 'a soft bubble pop',
    'land': 'a soft bubble pop with a low thump', 'chime': 'a soft glass bell chime', 'glide': 'a smooth rising tone',
    'swish': 'a quick soft whoosh', 'sweep': 'a smooth rising tone', 'gliss': 'a soft harp glissando',
    'sparkle': 'a soft airy swoosh with sparkles', 'land2': 'a soft bubble pop with a low thump', 'swish2': 'a quick soft whoosh',
}


def penalty(m, role):
    """Hard rules from the v1 failures: hiss, harsh band, clicky attacks."""
    p = 0.0
    p += max(0.0, m['hiss'] - 0.08) * 2.0
    p += max(0.0, m['harsh'] - (0.35 if role in ('chime', 'shimmer', 'shimmer_long', 'glide', 'sweep') else 0.2)) * 1.5
    if m['attack_ms'] < 4.0:
        p += 0.3
    if m['crest'] > 24:
        p += 0.2
    if role in ('whoosh', 'whoosh_long', 'dive', 'swish') and m['mid'] < 0.15:
        p += 0.25                    # nearly all below 200 Hz: a phone speaker plays almost none of it
    return p


TONAL = ('chime',)          # ElevenLabs roles with a clear pitch: only their in-key retunes are candidates


def retune(path):
    """Resample a take so its strongest spectral peak lands on the nearest A, D or E (pitch and length change
    together, like a tape-speed change).  Writes <take>_key.wav and returns its path."""
    out = path[:-4] + '_key.wav'
    y, sr = sf.read(path, always_2d=True)
    f, P = ss.welch(y.mean(axis=1), sr, nperseg=16384)
    band = (f > 150) & (f < 5000)
    f0 = f[band][np.argmax(P[band])]
    target = min(KEY_HZ, key=lambda k: abs(np.log2(k / f0)))
    ratio = target / f0
    from fractions import Fraction
    fr = Fraction(ratio).limit_denominator(400)
    z = ss.resample_poly(y, fr.denominator, fr.numerator, axis=0)       # fewer samples at the same rate = higher pitch
    sf.write(out, finish(z), sr, subtype='FLOAT')
    print('retune %s: %.0f Hz -> %.0f Hz (%+.2f semitones)' % (os.path.basename(path), f0, target, 12 * np.log2(ratio)))
    return out


def pick():
    sys.path.insert(0, HERE)
    from ear import Clap, metrics
    clap = Clap()
    os.makedirs(OUT, exist_ok=True)
    report = []
    for role in SYNTH:
        cands = [os.path.join(OUT, f'syn_{role}.wav')]
        el_role = role if any(r == role for r, *_ in EL_PROMPTS) else None
        if el_role:
            takes = sorted(os.path.join(ELD, f) for f in os.listdir(ELD) if re.fullmatch(re.escape(el_role) + r'(_mid)?_\d+\.wav', f))
            cands += [retune(tk) for tk in takes] if role in TONAL else takes
        rows = []
        for c in cands:
            y, sr = sf.read(c, always_2d=True)
            m = metrics(y, sr)
            s = clap.score(y, sr, WANT[role]) - penalty(m, role)
            rows.append((s, c, m))
        rows.sort(key=lambda r: -r[0])
        best = rows[0]
        y, sr = sf.read(best[1], always_2d=True)
        sf.write(os.path.join(OUT, role + '.wav'), y, sr, subtype='FLOAT')
        for s, c, m in rows:
            report.append('%-12s %-22s score %+.3f  atk %5.0fms crest %4.1f cent %5.0f harsh %.2f hiss %.2f%s' % (
                role, os.path.basename(c)[:-4], s, m['attack_ms'], m['crest'], m['centroid'], m['harsh'], m['hiss'],
                '  <- picked' if c == best[1] else ''))
    open(os.path.join(OUT, 'pick_report.txt'), 'w').write('\n'.join(report) + '\n')
    print('\n'.join(report))


def main():
    cmd = sys.argv[1]
    if cmd == 'synth':
        os.makedirs(OUT, exist_ok=True)
        for name, fn in SYNTH.items():
            sf.write(os.path.join(OUT, f'syn_{name}.wav'), fn(), SR, subtype='FLOAT')
            print('syn', name)
    elif cmd == 'el':
        takes = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        for role, prompt, dur, inf in EL_PROMPTS:
            for k in range(takes):
                print(el_fetch(role, prompt, dur, inf, k), flush=True)
    elif cmd == 'pick':
        pick()


if __name__ == '__main__':
    main()
