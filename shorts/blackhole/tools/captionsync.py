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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bh import timeline_overlay as tov  # noqa: E402
import caption_align  # noqa: E402  (same onset rule: Whisper's word spans swallow pauses and squash words)


NUMS = {'30': 'thirty', '32': 'thirtytwo', '1': 'one', '10': 'ten', '6': 'six'}


def norm(w):
    w = w.strip().lower()
    w = w.strip('.,?!').split('-')[0] or w.strip('.,?!-')   # "Jean-Pierre" ~ Whisper's "Jean" "-Pierre"
    return re.sub(r"[^a-z']", '', NUMS.get(w, w))


def onset_finder():
    y, sr = sf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'build', 'stem_vo.wav'), always_2d=True)
    rms = caption_align.envelope(y[:, 0], sr)
    thr = rms.max() * 10 ** (-32 / 20)

    return lambda a, b: caption_align.onset_at(rms, thr, a, b)


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
