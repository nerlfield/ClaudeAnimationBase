"""Beat-grid measurement shared by build_music.py (and handy on its own).

The generated takes have a steady eighth-note tick, so the most precise tempo/phase estimate is a
least-squares fit of onset peaks to an eighth-note grid (residual ~1-2 ms), not librosa's
beat_track (which wanders by a few tens of ms on syncopated material).

    python3 short/audio/beatgrid.py FILE [approx_bpm] [grid_bpm grid_offset]
"""
import sys
import numpy as np
import librosa

HOP = 64
SR = 22050


def _env(y, sr):
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=HOP))
    return librosa.onset.onset_strength(S=librosa.amplitude_to_db(S, ref=np.max), sr=sr, hop_length=HOP)


def onset_peaks(y, sr=SR):
    """Onset peaks as an (N, 2) array of (time s, strength), parabolic-refined."""
    o = np.ascontiguousarray(_env(y, sr), dtype=np.float32)
    pk = librosa.util.peak_pick(o, pre_max=10, post_max=10, pre_avg=40, post_avg=40,
                                delta=float(np.percentile(o, 90) * 0.5), wait=20)
    out = []
    fr = sr / HOP
    for j in pk:
        d = 0.0
        if 0 < j < len(o) - 1:
            a, b, c = o[j - 1], o[j], o[j + 1]
            d = 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
        out.append(((j + d) / fr, o[j]))
    return np.array(out)


def fit_eighths(peaks, approx_bpm):
    """Fit onset peaks to an eighth-note grid. Returns (bpm, eighth0 phase s, on-grid peak times, residuals)."""
    E0 = 60 / approx_bpm / 2
    hist, edges = np.histogram(peaks[:, 0] % E0, bins=64, range=(0, E0), weights=peaks[:, 1])
    off0 = edges[np.argmax(hist)] + E0 / 128
    idx = np.round((peaks[:, 0] - off0) / E0)
    sel = np.abs(peaks[:, 0] - (off0 + idx * E0)) < 0.2 * E0
    t, k = peaks[sel, 0], idx[sel]
    for _ in range(4):
        E, off = np.polyfit(k, t, 1)
        r = t - (off + k * E)
        keep = np.abs(r) < max(3 * np.std(r), 0.004)
        t, k = t[keep], k[keep]
    E, off = np.polyfit(k, t, 1)
    r = t - (off + k * E)
    return 60 / (2 * E), off % E, t, r


def measure(path_or_y, approx_bpm=116.0, sr=SR):
    y = path_or_y if isinstance(path_or_y, np.ndarray) else librosa.load(path_or_y, sr=sr, mono=True)[0]
    return fit_eighths(onset_peaks(y, sr), approx_bpm)


def grid_report(ticks, bpm, offset, label=""):
    """Error of on-grid tick peaks against a target grid (nearest eighth of bpm/offset)."""
    half = 60 / bpm / 2
    err = ticks - (offset + np.round((ticks - offset) / half) * half)
    print(f"{label}vs grid {bpm} bpm @ {offset}s: n={len(err)} mean {np.mean(err)*1000:+.2f} ms, "
          f"rms {np.sqrt(np.mean(err**2))*1000:.2f} ms, max |err| {np.max(np.abs(err))*1000:.2f} ms")
    return err


if __name__ == "__main__":
    f = sys.argv[1]
    ab = float(sys.argv[2]) if len(sys.argv) > 2 else 116.0
    bpm, e0, ticks, r = measure(f, ab)
    print(f"{f}: {bpm:.4f} bpm, first eighth at {e0:.4f}s, {len(ticks)} ticks, fit residual rms {np.std(r)*1000:.2f} ms")
    if len(sys.argv) > 4:
        gb, go = float(sys.argv[3]), float(sys.argv[4])
        err = grid_report(ticks, gb, go)
        beats = go + np.arange(0, 200) * 60 / gb
        on_beat = [(t, e) for t, e in zip(ticks, err) if np.min(np.abs(beats - (t - e))) < 1e-6]
        for a in range(0, int(ticks.max()) + 1, 10):
            s = [e for t, e in on_beat if a <= t < a + 10]
            if s:
                print(f"   {a:2d}-{a+10:2d}s  beats n={len(s):2d} mean {np.mean(s)*1000:+6.2f} ms  max {np.max(np.abs(s))*1000:5.2f} ms")
