"""Caption sync check: compare each caption chunk's on-screen start with when Whisper hears its first word.

    python tools/captionsync.py build/check/whisper_words.json

Whisper runs on the final mixed audio (independent of the TTS alignment the captions were built from).
Positive lag = caption appears after the word starts.  Whisper stretches a word that follows a pause back
into the silence, so each first word's start is refined to the voice stem's energy onset inside Whisper's span.
"""
import json
import os
import re
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from bh import timeline_overlay as tov  # noqa: E402


NUMS = {'30': 'thirty'}


def norm(w):
    w = w.lower().strip('.,?!')
    return re.sub(r"[^a-z']", '', NUMS.get(w, w))


def onset_finder():
    y, sr = sf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'stem_vo.wav'), always_2d=True)
    hop = int(0.005 * sr)
    x = y[:, 0][: len(y) // hop * hop].reshape(-1, hop)
    rms = np.sqrt((x ** 2).mean(axis=1))
    thr = rms.max() * 10 ** (-32 / 20)

    def onset(a, b):
        i0, i1 = int(a / 0.005), int((b + 0.3) / 0.005)
        on = rms[i0:i1] > thr
        if b - a > 0.6:
            # a span this long swallowed a pause (and maybe the previous word's tail): start after the pause
            quiet = np.convolve(~on, np.ones(12), 'valid') == 12          # 60 ms of silence
            q = np.nonzero(quiet)[0]
            if len(q):
                on[:q[0] + 12] = False
        k = np.nonzero(on)[0]
        return (i0 + k[0]) * 0.005 if len(k) else a
    return onset


def main():
    heard = [(a, b, norm(w)) for a, b, w in json.load(open(sys.argv[1]))]
    onset = onset_finder()
    j = 0
    lags = []
    for a, b, words, _ in tov.chunks():
        first = norm(words[0])
        while j < len(heard) and heard[j][2] != first:
            j += 1
        if j == len(heard):
            print('%-40s not heard' % ' '.join(words)); j = 0; continue
        start = onset(heard[j][0], heard[j][1])
        lag = a - start
        lags.append(lag)
        print('%6.2f  heard %6.2f  lag %+5.2f  %s' % (a, start, lag, ' '.join(words)))
        j += len(words)
    print('max late %.2f s, max early %.2f s' % (max(lags), -min(lags)))


if __name__ == '__main__':
    main()
