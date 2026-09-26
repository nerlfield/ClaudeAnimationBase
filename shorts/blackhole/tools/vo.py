"""Generate the voiceover line by line with ElevenLabs (character timestamps), place each line on the beat
sheet, and write build/vo.wav plus build/words.json (word timings and caption chunks).

The API key is read from the ELEVENLABS_API_KEY environment variable and never written anywhere.
"""
import base64
import json
import math
import os
import subprocess
import sys
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, '..', 'build')
VOICE = 'iP95p4xoKVk53GoZ742B'          # Chris - Charming, Down-to-Earth (premade)
MODEL = 'eleven_multilingual_v2'
SR = 44100

# (start time in the video, latest end, text) -- '|' marks caption chunk breaks, '*' marks gold words
LINES = [
    (0.15, 2.40, 0.92, 'This dot is | the whole *universe.'),
    (2.85, 5.25, 0.95, 'To see it, fly down to a *black *hole.'),
    (6.00, 7.75, 0.95, 'The disk around it is *flat.'),
    (8.95, 10.65, 0.86, 'So why does it look like *this?'),
    (11.95, 15.30, 1.04, "That's the *back of the disk, | bent over the top by gravity."),
    (18.85, 22.15, 1.04, 'Hover here, | and the black hole fills | exactly *half your sky.'),
    (22.30, 24.05, 1.00, 'And light goes around it in *circles.'),
    (24.15, 26.05, 0.88, "That's the back of your own *head."),
    (26.90, 28.60, 0.95, 'Now hover just above the *edge.'),
    (28.90, 32.15, 0.98, 'The whole universe gets squeezed | into one *dot above your head.'),
    (33.30, 34.30, 0.90, 'Everything else?'),
    (34.90, 35.90, 0.85, 'Black hole.'),
]


def plain(text):
    return ' '.join(w.lstrip('*') for w in text.replace('|', ' ').split())


def marked_chunks(text):
    """[[(word, hot), ...], ...] following the '|' marks."""
    return [[(w.lstrip('*'), w.startswith('*')) for w in part.split()] for part in text.split('|') if part.split()]


def tts(text, prev_text, next_text, speed):
    key = os.environ['ELEVENLABS_API_KEY']
    body = dict(text=text, model_id=MODEL, previous_text=prev_text, next_text=next_text,
                voice_settings=dict(stability=0.42, similarity_boost=0.8, style=0.25, use_speaker_boost=True, speed=speed))
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_192',
        data=json.dumps(body).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    mp3 = base64.b64decode(d['audio_base64'])
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(SR), 'pipe:1'],
                       input=mp3, capture_output=True, check=True)
    pcm = np.frombuffer(r.stdout, np.float32).copy()
    return pcm, d['alignment']


def trim(pcm, al, thresh=0.01):
    """Drop leading/trailing silence; shift the alignment accordingly."""
    idx = np.where(np.abs(pcm) > thresh)[0]
    if len(idx) == 0:
        return pcm, al, 0.0
    a = max(0, idx[0] - int(0.02 * SR)); b = min(len(pcm), idx[-1] + int(0.12 * SR))
    off = a / SR
    al = dict(al)
    al['character_start_times_seconds'] = [x - off for x in al['character_start_times_seconds']]
    al['character_end_times_seconds'] = [x - off for x in al['character_end_times_seconds']]
    return pcm[a:b], al, off


def words_from_alignment(al, t0):
    chars = al['characters']; st = al['character_start_times_seconds']; en = al['character_end_times_seconds']
    words, cur, cs, ce = [], '', None, None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                words.append((cur, cs + t0, ce + t0)); cur = ''
            continue
        if not cur:
            cs = s
        cur += c; ce = e
    if cur:
        words.append((cur, cs + t0, ce + t0))
    return words


def chunk_words(words, maxw=4):
    """Caption chunks of <= maxw words, breaking after punctuation first."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        punct = w[0][-1] in ',.?!'
        if len(cur) >= maxw or punct:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    # merge a lone trailing word into the previous chunk when it fits
    merged = []
    for c in out:
        if merged and len(c) == 1 and len(merged[-1]) < maxw and merged[-1][-1][0][-1] not in '.?!':
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    return merged


def main():
    os.makedirs(BUILD, exist_ok=True)
    total = 37.3333
    mix = np.zeros(int(total * SR) + SR, np.float32)
    all_words, chunks, report = [], [], []
    for i, (t0, t1, speed0, text) in enumerate(LINES):
        prev_text = ' '.join(plain(l[3]) for l in LINES[max(0, i - 2):i])
        next_text = plain(LINES[i + 1][3]) if i + 1 < len(LINES) else ''
        spoken = plain(text)
        cache = os.path.join(BUILD, f'vo_{i:02d}.json')
        speed = speed0
        for attempt in range(4):
            if os.path.exists(cache):
                c = json.load(open(cache))
                if c['text'] == spoken and c['speed'] == speed:
                    pcm = np.frombuffer(base64.b64decode(c['pcm']), np.float32); al = c['al']
                else:
                    pcm = None
            else:
                pcm = None
            if pcm is None:
                raw, al = tts(spoken, prev_text, next_text, speed)
                pcm, al, _ = trim(raw, al)
                json.dump(dict(text=spoken, speed=speed, pcm=base64.b64encode(pcm.astype(np.float32).tobytes()).decode(), al=al),
                          open(cache, 'w'))
            dur = len(pcm) / SR
            if t0 + dur <= t1 + 0.05 or speed >= 1.12:
                break
            speed = round(min(1.12, speed * (dur / (t1 - t0)) * 1.02), 3)
        a = int(t0 * SR)
        mix[a:a + len(pcm)] += pcm
        ws = words_from_alignment(al, t0)
        all_words += [dict(w=w, s=round(s, 3), e=round(e, 3)) for w, s, e in ws]
        k = 0
        for mc in marked_chunks(text):
            c = ws[k:k + len(mc)]; k += len(mc)
            chunks.append(dict(start=round(c[0][1], 3), end=round(c[-1][2], 3), words=[w for w, _, _ in c],
                               hot=[w for (w, _, _), (_, h) in zip(c, mc) if h]))
        assert k == len(ws), (text, len(ws), k)
        report.append(f'{t0:6.2f}-{t0 + dur:6.2f} (slot to {t1:5.2f}) speed {speed:.3f}  {len(spoken.split()) / dur:.2f} w/s  {spoken}')
    # chunks stay up until the next one starts (or 0.35 s after their last word)
    for j, c in enumerate(chunks):
        nxt = chunks[j + 1]['start'] if j + 1 < len(chunks) else 99
        c['end'] = round(min(nxt, c['end'] + 0.35), 3)
    mix = mix[:int(total * SR)]
    pk = np.abs(mix).max()
    with open(os.path.join(BUILD, 'vo.f32'), 'wb') as f:
        f.write(mix.astype(np.float32).tobytes())
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', os.path.join(BUILD, 'vo.f32'),
                    os.path.join(BUILD, 'vo.wav')], check=True)
    json.dump(dict(words=all_words, chunks=chunks), open(os.path.join(BUILD, 'words.json'), 'w'), indent=1)
    print('\n'.join(report)); print('peak', pk, 'chunks', len(chunks))


if __name__ == '__main__':
    main()
