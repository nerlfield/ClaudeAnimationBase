"""Measure the effects bus of a mix: harshness, hiss, how sharp its transients are, phone audibility, and a CLAP
verdict around every cue.  Compares any number of SFX stems (e.g. v1 vs v2).

    python tools/mixcheck.py build/stem_sfx_v1.wav build/stem_sfx.wav
"""
import os
import sys

import numpy as np
import scipy.signal as ss
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ear import Clap, phone_drop  # noqa: E402

SR = 44100


def band_share(x, lo, hi):
    f, P = ss.welch(x, SR, nperseg=4096)
    return P[(f >= lo) & (f < hi)].sum() / P.sum()


def sharpness(x):
    """Steepest rise of the 5 ms RMS envelope (1 ms hop), in dB per ms, over loud moments (within 20 dB of the
    peak), 99.5th percentile.  5 ms windows keep a noise texture's own flicker from reading as an attack."""
    k = int(0.005 * SR); h = int(0.001 * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(k) / k, 'same') + 1e-12)[::h]
    d = 20 * np.log10(e + 1e-9)
    rise = (d[5:] - d[:-5]) / 5.0
    loud = d[5:] > d.max() - 20
    return float(np.percentile(rise[loud], 99.5)) if loud.any() else 0.0


GOOD = ['a soft deep cinematic boom', 'a huge warm cinematic bass drop', 'a smooth airy whoosh', 'a soft bubble pop',
        'a gentle shimmering chime', 'a soft glass bell chime', 'a reverse cymbal swell', 'a rising cinematic riser',
        'a soft harp glissando', 'a low rumble']
BADL = ['a slide whistle', 'a glitchy weird electronic sound', 'a sharp loud click', 'a harsh piercing high-pitched noise',
        'white noise hiss', 'a siren', 'distorted clipping noise']


def windows_report(y, clap, cues):
    """For every cue, the 1.5 s around it: the best-matching label among good and bad descriptors."""
    rows = []
    labels = GOOD + BADL
    for t0, name in cues:
        a = int(max(0, t0 - 0.4) * SR); b = int(min(len(y) / SR, t0 + 1.1) * SR)
        seg = y[a:b]
        if np.abs(seg).max() < 1e-4:
            continue
        pr = clap.probs(seg, SR, labels)
        i = int(np.argmax(pr))
        rows.append((t0, name, labels[i], pr[i], float(pr[len(GOOD):].sum())))
    return rows


def main():
    clap = Clap()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import mix
    cues = [(t, n) for t, n, g, o in mix.CUES]
    for path in sys.argv[1:]:
        y, sr = sf.read(path, always_2d=True)
        x = y.mean(axis=1)
        print('== %s' % path)
        print('   2-5 kHz share %.3f   >6 kHz share %.3f   transient sharpness %.1f dB/ms   phone drop %.1f LU' % (
            band_share(x, 2000, 5000), band_share(x, 6000, 22050), sharpness(x), phone_drop(y, sr)))
        rows = windows_report(y, clap, cues)
        bad = [r for r in rows if r[2] in BADL or r[4] > 0.4]
        print('   CLAP around %d cues: %d whose best label is a bad one (or bad labels > 40%%)' % (len(rows), len(bad)))
        for t, n, lab, p, pb in rows:
            print('     %6.2f %-24s %-34s %.2f  bad total %.2f%s' % (t, n, lab[2:], p, pb, '  <-' if (lab in BADL or pb > 0.4) else ''))


if __name__ == '__main__':
    main()
