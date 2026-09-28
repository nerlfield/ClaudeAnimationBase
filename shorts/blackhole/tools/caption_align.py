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
NUMS = {'30': 'thirty', '32': 'thirtytwo', '1': 'one', '10': 'ten', '6': 'six'}


def norm(w):
    w = w.strip().lower()
    w = w.strip('.,?!').split('-')[0] or w.strip('.,?!-')   # "Jean-Pierre" ~ Whisper's "Jean" "-Pierre"
    return re.sub(r"[^a-z']", '', NUMS.get(w, w)).replace('disc', 'disk')


def envelope(x, sr):
    """RMS in exact 5 ms frames (frame i starts at i * 0.005 s): the audio is resampled to 48 kHz first, since
    at 44.1 kHz a 5 ms hop is 220.5 samples and int() made it 220, a clock 0.23% fast (0.19 s off by 85 s)."""
    import librosa
    x48 = librosa.resample(np.asarray(x, np.float64), orig_sr=sr, target_sr=48000)
    xr = x48[: len(x48) // 240 * 240].reshape(-1, 240)
    return np.sqrt((xr ** 2).mean(axis=1))


def onset_at(rms, thr, a, b):
    """The voice's own onset for a word Whisper puts at [a, b] (rms: 5 ms frames, thr: 'voice on' level)."""
    i0, i1 = int(a / 0.005), min(len(rms), int((b + 0.3) / 0.005))
    on = rms[i0:i1] > thr
    # Whisper often starts a word in the pause before it (or in the last word's tail): if there is a pause of at
    # least 40 ms in the first 60% of its span, the word starts after it.  (A gap later in the span is inside the
    # word: the stop in "exact-ly".)
    head = int(0.6 * (b - a) / 0.005)
    quiet = np.convolve(~on[:max(head, 8)], np.ones(8), 'valid') == 8
    q = np.nonzero(quiet)[0]
    if len(q):
        on[:q[-1] + 8] = False
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
        else:
            # or Whisper started it on the last word's tail and the word itself comes after a pause inside its
            # span ("lower, | and hover"): a pause of 120 ms or more is no stop inside a word
            gap = np.nonzero(np.convolve(~on, np.ones(24), 'valid') == 24)[0]
            if len(gap):
                later = np.nonzero(on[gap[0] + 24:])[0]
                if len(later):
                    t = i0 + gap[0] + 24 + later[0]
    return t * 0.005


def after_pause(rms, thr, t):
    """Whether t is a voice onset straight after a real pause (at least 60 ms of quiet; shorter dips happen
    between words inside a phrase, "would | drift")."""
    i = int(round(t / 0.005))
    return i >= 12 and bool((rms[i - 12:i] <= thr).all())


def pause_end_near(rms, thr, t, win=0.12):
    """The voice onset nearest t (within win) that follows a pause of at least 60 ms, or None."""
    best = None
    for i in range(max(12, int((t - win) / 0.005)), min(len(rms) - 3, int((t + win) / 0.005))):
        if (rms[i:i + 3] > thr).all() and (rms[i - 12:i] <= thr).all():
            if best is None or abs(i * 0.005 - t) < abs(best - t):
                best = i * 0.005
    return best


def main():
    from faster_whisper import WhisperModel
    y, sr = sf.read(os.path.join(BUILD, 'vo.wav'), always_2d=True)
    x = y[:, 0].astype(np.float32)
    import librosa
    x16 = librosa.resample(x, orig_sr=sr, target_sr=16000)
    model = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
    segs, _ = model.transcribe(x16, language='en', word_timestamps=True, beam_size=5, vad_filter=False)
    heard = []
    for w in (w for s in segs for w in s.words):
        if w.word.strip() == '.5':                        # "six and a half" heard as "6" ".5"
            heard += [(w.start, w.end, t) for t in ('and', 'a', 'half')]
        else:
            heard.append((w.start, w.end, norm(w.word)))
    rms = envelope(x, sr)
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
        if not after_pause(rms, thr, t_on):
            # Whisper put the word inside running speech, where it can be a word off ("drift | ten" had "ten" on
            # "drift"): if the script's own time sits on a real pause, the word starts there
            p = pause_end_near(rms, thr, c['start'])
            if p is not None:
                t_on = p
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
