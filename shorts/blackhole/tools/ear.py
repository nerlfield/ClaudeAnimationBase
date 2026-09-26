"""A stand-in ear for choosing sounds without listening: signal metrics plus CLAP audio-text similarity.

    python tools/ear.py build/audio/sfx2/*.wav             # metrics + CLAP descriptor table
    from tools.ear import metrics, Clap                     # used by tools/sfx.py to rank takes

Metrics: attack (ms from 10% to peak of the 5 ms envelope), crest factor (dB), spectral centroid (Hz), and the
share of energy in the harsh 2-5 kHz band, above 6 kHz (hiss) and below 150 Hz (sub).
"""
import os
import sys

import numpy as np
import scipy.signal as ss
import soundfile as sf

DESCRIPTORS = ['a soft deep cinematic boom', 'a smooth airy whoosh', 'a harsh piercing high-pitched noise',
               'a glitchy weird electronic sound', 'a gentle shimmering chime', 'a sharp loud click', 'white noise hiss',
               'a low rumble', 'a rising cinematic riser', 'a soft bubble pop']
BAD = ['a harsh piercing high-pitched noise', 'a glitchy weird electronic sound', 'a sharp loud click', 'white noise hiss',
       'distorted clipping noise', 'a person speaking', 'music with drums']


def mono(y):
    return y.mean(axis=1) if y.ndim > 1 else y


def metrics(y, sr):
    x = mono(y).astype(np.float64)
    env = np.abs(ss.hilbert(x))
    k = max(1, int(0.005 * sr))
    env = np.convolve(env, np.ones(k) / k, 'same')
    pk, ip = env.max(), env.argmax()
    i10 = np.argmax(env > 0.1 * pk)
    f, P = ss.welch(x, sr, nperseg=min(4096, len(x)))
    P = P / (P.sum() + 1e-20)
    return dict(dur=len(x) / sr, attack_ms=(ip - i10) / sr * 1000,
                crest=20 * np.log10(np.abs(x).max() / (np.sqrt((x ** 2).mean()) + 1e-12) + 1e-12),
                centroid=float((f * P).sum()), harsh=float(P[(f > 2000) & (f < 5000)].sum()),
                hiss=float(P[f > 6000].sum()), sub=float(P[f < 150].sum()), mid=float(P[(f > 200) & (f < 2000)].sum()))


def phone_drop(y, sr):
    """Loudness lost through a phone-speaker model (2nd-order high-pass at 350 Hz, low-pass at 8 kHz), in LU.
    Above ~12 LU the sound all but disappears on a phone."""
    import pyloudnorm as pyln
    x = y if y.ndim == 2 else y[:, None]
    sos1 = ss.butter(2, 350 / (sr / 2), 'high', output='sos'); sos2 = ss.butter(2, 8000 / (sr / 2), 'low', output='sos')
    ph = ss.sosfilt(sos2, ss.sosfilt(sos1, x, axis=0), axis=0)
    m = pyln.Meter(sr, block_size=min(0.4, len(x) / sr * 0.9))
    return m.integrated_loudness(x) - m.integrated_loudness(ph)


class Clap:
    """laion/clap-htsat-unfused on CPU; similarity of a clip to text descriptors."""

    def __init__(self):
        import torch
        from transformers import ClapModel, ClapProcessor
        self.torch = torch
        self.m = ClapModel.from_pretrained('laion/clap-htsat-unfused').eval()
        self.p = ClapProcessor.from_pretrained('laion/clap-htsat-unfused')

    @staticmethod
    def _vec(out):
        v = out if hasattr(out, 'norm') else getattr(out, 'pooler_output', None)
        if v is None or not hasattr(v, 'norm'):
            v = out[0] if not hasattr(out, 'text_embeds') else out.text_embeds
        return v / v.norm(dim=-1, keepdim=True)

    def text(self, labels):
        with self.torch.no_grad():
            ti = self.p(text=labels, return_tensors='pt', padding=True)
            return self._vec(self.m.get_text_features(**ti))

    def audio(self, y, sr):
        x = ss.resample_poly(mono(y), 48000, sr).astype(np.float32)
        with self.torch.no_grad():
            ai = self.p(audio=[x], sampling_rate=48000, return_tensors='pt')
            return self._vec(self.m.get_audio_features(**ai))

    def probs(self, y, sr, labels):
        te = self.text(labels)
        sim = (self.audio(y, sr) @ te.T)[0].numpy()
        pr = np.exp(sim * 30); return pr / pr.sum()

    def score(self, y, sr, want):
        """How much more the clip matches `want` than the generic bad descriptors (higher is better)."""
        te = self.text([want] + BAD)
        sim = (self.audio(y, sr) @ te.T)[0].numpy()
        return float(sim[0] - sim[1:].max())


def main():
    clap = Clap()
    for path in sys.argv[1:]:
        y, sr = sf.read(path, always_2d=True)
        m = metrics(y, sr)
        pr = clap.probs(y, sr, DESCRIPTORS)
        top = np.argsort(-pr)[:3]
        print('%-16s %4.1fs atk %5.0fms crest %4.1f cent %5.0f harsh %.2f hiss %.2f sub %.2f | %s' % (
            os.path.basename(path)[:-4][:16], m['dur'], m['attack_ms'], m['crest'], m['centroid'], m['harsh'], m['hiss'],
            m['sub'], '  '.join('%s %.2f' % (DESCRIPTORS[i][2:24], pr[i]) for i in top)))


if __name__ == '__main__':
    main()
