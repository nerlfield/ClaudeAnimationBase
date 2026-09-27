"""How loud each effects moment is against the voice: the effects stem's loudest 400 ms (K-weighted, as LUFS
momentary loudness) around each cue, minus the voice's median momentary loudness while speaking, plus the
effects' sample peak against the voice's.  Stems are pre-master, so they share one gain.

    python tools/sfxlevels.py            # after tools/mix.py
"""
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import mix  # noqa: E402
from bh.timeline_overlay import back_front_times, black_hole_time, minute_times  # noqa: E402

B = os.path.join(HERE, '..', 'build')


def cue_time(t0):
    if t0 == 'BLACK_HOLE':
        return black_hole_time()
    if t0 in ('BACK', 'FRONT'):
        return back_front_times()[t0 == 'FRONT']
    if t0 in ('MINUTE', 'HOUR'):
        return minute_times()[t0 == 'HOUR']
    from bh.inserts import cue_times
    return cue_times().get(t0, t0)


def momentary(x, sr, meter):
    """400 ms K-weighted loudness every 50 ms -> (times, LUFS)."""
    w, h = int(0.4 * sr), int(0.05 * sr)
    ts, ls = [], []
    for i in range(0, len(x) - w, h):
        blk = x[i:i + w]
        ls.append(meter.integrated_loudness(blk) if np.abs(blk).max() > 1e-6 else -120.0)
        ts.append((i + w / 2) / sr)
    return np.array(ts), np.array(ls)


def main():
    vo, sr = sf.read(os.path.join(B, 'stem_vo.wav'), always_2d=True)
    fx, _ = sf.read(os.path.join(B, 'stem_sfx.wav'), always_2d=True)
    meter = pyln.Meter(sr, block_size=0.4)
    tv, lv = momentary(vo, sr, meter)
    tf, lf = momentary(fx, sr, meter)
    v_med = float(np.median(lv[lv > -40]))
    v_peak = 20 * np.log10(np.abs(vo).max())
    groups = {}
    for t0, name, g, opts in mix.CUES:
        t = round(float(cue_time(t0)), 2)
        k = next((k for k in groups if abs(k - t) < 0.3), t)
        groups.setdefault(k, []).append(name)
    print('voice: median momentary %.1f LUFS while speaking, peak %.1f dBFS' % (v_med, v_peak))
    print('  time   fx-voice(LU)  fx peak-voice peak(dB)  voice there  cues')
    for t in sorted(groups):
        m = (tf > t - 0.3) & (tf < t + 1.2)
        seg = fx[int(max(0, t - 0.3) * sr):int((t + 1.2) * sr)]
        mv = (tv > t - 0.3) & (tv < t + 1.2)
        vo_there = lv[mv].max() if mv.any() else -120
        print('%6.2f  %+6.1f        %+6.1f               %6.1f     %s' % (
            t, lf[m].max() - v_med, 20 * np.log10(np.abs(seg).max() + 1e-9) - v_peak, vo_there, ', '.join(groups[t])))


if __name__ == '__main__':
    main()
