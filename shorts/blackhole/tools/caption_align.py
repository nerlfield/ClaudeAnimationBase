"""Set every caption chunk's start from the finished voice track: Whisper word timings on build/vo.wav, each refined
to the voice's own onset (Whisper stretches a word that follows a pause back into the silence).  Rewrites the chunk
starts in build/words.json; tools/captionsync.py then checks the result independently against the full mix.

    python tools/caption_align.py            # after tools/vo.py
"""
import json
import os
import re
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, '..', 'build')
NUMS = {'30': 'thirty', '32': 'thirtytwo', '1': 'one'}


def norm(w):
    w = w.lower().strip('.,?!')
    return re.sub(r"[^a-z']", '', NUMS.get(w, w)).replace('disc', 'disk')


def onset_at(rms, thr, a, b):
    """The voice's own onset for a word Whisper puts at [a, b] (rms: 5 ms frames, thr: 'voice on' level)."""
    i0, i1 = int(a / 0.005), min(len(rms), int((b + 0.3) / 0.005))
    on = rms[i0:i1] > thr
    if b - a > 0.45:                         # a span this long swallowed a pause: start after it
        quiet = np.convolve(~on, np.ones(12), 'valid') == 12
        q = np.nonzero(quiet)[0]
        if len(q):
            on[:q[0] + 12] = False
    k = np.nonzero(np.convolve(on, np.ones(3), 'valid') == 3)[0]    # on for 15 ms: a lone 5 ms blip isn't speech
    if not len(k):
        return a
    t = i0 + k[0]
    if k[0] == 0:                            # already speaking at Whisper's start (it can squash a word to 0 s):
        j, run = t, 0                        # walk back, over dips shorter than 60 ms, to the pause the word
        while j > 0 and t - j < 70 and run < 12:     # starts from; none within 0.35 s: keep Whisper's time
            j -= 1
            run = run + 1 if rms[j] <= thr else 0
        if run == 12:
            t = j + 12
    return t * 0.005


def main():
    from faster_whisper import WhisperModel
    y, sr = sf.read(os.path.join(BUILD, 'vo.wav'), always_2d=True)
    x = y[:, 0].astype(np.float32)
    import librosa
    x16 = librosa.resample(x, orig_sr=sr, target_sr=16000)
    model = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
    segs, _ = model.transcribe(x16, language='en', word_timestamps=True, beam_size=5, vad_filter=False)
    heard = [(w.start, w.end, norm(w.word)) for s in segs for w in s.words]
    hop = int(0.005 * sr)
    xr = x[: len(x) // hop * hop].reshape(-1, hop)
    rms = np.sqrt((xr.astype(np.float64) ** 2).mean(axis=1))
    thr = rms.max() * 10 ** (-32 / 20)

    onset = lambda a, b: onset_at(rms, thr, a, b)

    data = json.load(open(os.path.join(BUILD, 'words.json')))
    old_starts = [c['start'] for c in data['chunks']]
    j = 0
    moved = []
    for c in data['chunks']:
        first = norm(c['words'][0])
        k = j
        while k < len(heard) and heard[k][2] != first:
            k += 1
        if k == len(heard):
            continue
        t_on = onset(heard[k][0], heard[k][1])
        if abs(t_on - c['start']) < 0.6:
            moved.append((c['start'], t_on, ' '.join(c['words'])))
            c['start'] = round(t_on, 3)
        j = k + len(c['words'])
    for n, (a, b) in enumerate(zip(data['chunks'], data['chunks'][1:])):
        if abs(a['end'] - old_starts[n + 1]) < 0.02:        # chunks that ran into each other still do
            a['end'] = b['start']
        else:
            a['end'] = round(min(a['end'], b['start']), 3)
    json.dump(data, open(os.path.join(BUILD, 'words.json'), 'w'), indent=1)
    for a, b, w in moved:
        if abs(a - b) > 0.04:
            print('%6.2f -> %6.2f  %s' % (a, b, w))


if __name__ == '__main__':
    main()
