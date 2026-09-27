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
VOICE = 'TX3LPaxmHKxFdv7VOQHJ'          # Liam - Energetic, Social Media Creator (premade; the user's pick)
# earlier cut: 'iP95p4xoKVk53GoZ742B', Chris - Charming, Down-to-Earth (takes kept in build/vo_chris/)
MODEL = 'eleven_v3'                   # read as one continuous performance by tools/vo_v3.py (v2 lines sounded read-out)
SR = 44100
LINE_LUFS = -22.5                   # each line is matched to this before placement

# (start time in the video, latest end, text) -- '|' marks caption chunk breaks, '*' marks gold words
# Round 8: one person talking you through the picture, read as ONE continuous performance (tools/vo_flow.py).
# (start, end) is each line's window on the beat sheet: the earliest it may start and the latest it must end.
LINES = [
    # Round 11 (the user: "imagine you explaining it to a 3 year old… smooth, clear, direct, clean"; "you're using too
    # little of phrases like: this is, there is"): plain words, one idea per sentence, each line pointing at what is
    # on screen, and every camera move finished before the line about its result starts.  The first number is the
    # earliest a line may start (the picture is then re-timed around the voice: bh/shots.py WARP); none must end
    # by a deadline, so no line is squeezed.
    (0.15, 99, 1.00, "See this glowing *dot? | That's the whole *universe."),
    (3.75, 99, 1.00, "Let me show you *why."),
    (5.80, 99, 1.00, "This is a *black *hole. | And this bright ring is hot *gas, | spinning around it."),
    (11.10, 99, 1.00, "Let's look at it from *above."),
    (14.30, 99, 1.00, "See? | The disk is actually *flat."),
    (17.20, 99, 1.00, "This is the *back half. | And this is the *front half."),
    (20.80, 99, 1.00, "Now watch the *back half, | as we go back down."),
    (24.60, 99, 1.00, "The black hole *bends its light, | up over the *top... | and under the *bottom."),
    (30.30, 99, 1.00, "Now let's fly in *closer. | Much *closer."),
    (34.90, 99, 1.00, "If you hover right here, | the black hole fills | exactly *half your sky."),
    (38.90, 99, 1.00, "And see this thin *line? | That's light, | going around the black hole in a *circle."),
    (43.70, 99, 1.00, "Light can go all the way *around... | and come back to *you."),
    (48.10, 99, 1.00, "So in this line, | you see the back of your own *head."),
    (52.00, 99, 1.00, "Now let's go lower, | and hover just above the *edge. | Then look *up."),
    (56.90, 99, 1.00, "The whole universe *shrinks | into one small *dot above you."),
    # to a hovering observer at 1.001x, everything outside runs 1/sqrt(1 - 1/1.001) = 31.6x fast: one minute
    # down here is 31.6 minutes out there (said "half an hour", shown as 1 min -> 32 min)
    (62.80, 99, 1.00, "And down here, | time runs *slower."),
    (64.40, 99, 1.00, "Stay for one *minute... | and half an *hour goes by out there."),
    (69.90, 99, 1.00, "And all this *darkness around the dot? | That's the black hole."),
]
ORDER = sorted(range(len(LINES)), key=lambda i: LINES[i][0])     # lines in time order


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
    total = 65 * 60 / 90.0
    mix = np.zeros(int(total * SR) + SR, np.float32)
    all_words, chunks, report = [], [], []
    for i, (t0, t1, speed0, text) in enumerate(LINES):
        k = ORDER.index(i)
        prev_text = ' '.join(plain(LINES[j][3]) for j in ORDER[max(0, k - 2):k])
        next_text = plain(LINES[ORDER[k + 1]][3]) if k + 1 < len(ORDER) else ''
        spoken = plain(text)
        cache = os.path.join(BUILD, f'vo_{i:02d}.json')
        speed = speed0
        for attempt in range(4):
            if os.path.exists(cache):
                c = json.load(open(cache))
                if c['text'] == spoken and c['speed'] == speed and c.get('voice') == VOICE and c.get('model', 'eleven_multilingual_v2') == MODEL:
                    pcm = np.frombuffer(base64.b64decode(c['pcm']), np.float32); al = c['al']
                else:
                    pcm = None
            else:
                pcm = None
            if pcm is None:
                if MODEL == 'eleven_v3':
                    raise SystemExit(f'line {i}: no v3 take cached for "{spoken}"; run tools/vo_v3.py first')
                raw, al = tts(spoken, prev_text, next_text, speed)
                pcm, al, _ = trim(raw, al)
                json.dump(dict(text=spoken, speed=speed, voice=VOICE, pcm=base64.b64encode(pcm.astype(np.float32).tobytes()).decode(), al=al),
                          open(cache, 'w'))
            dur = len(pcm) / SR
            lead = c.get('lead', 0.0) if pcm is not None and os.path.exists(cache) else 0.0
            if MODEL == 'eleven_v3' or t0 + dur - lead <= t1 + 0.05 or speed >= 1.12:
                break
            speed = round(min(1.12, speed * (dur / (t1 - t0)) * 1.02), 3)
        # every line at the same loudness (the takes came out between -21 and -25 LUFS), with 8 ms edges
        import pyloudnorm as pyln
        lv = pyln.Meter(SR, block_size=min(0.4, 0.9 * len(pcm) / SR)).integrated_loudness(pcm.astype(np.float64))
        pcm = (pcm * 10 ** ((LINE_LUFS - lv) / 20)).astype(np.float32)
        e = int(0.008 * SR); pcm = pcm.copy(); pcm[:e] *= np.linspace(0, 1, e); pcm[-e:] *= np.linspace(1, 0, e)
        # a v3 line carries the breath before it: the words still start at t0, the breath just before
        a = int(round((t0 - lead) * SR))
        mix[a:a + len(pcm)] += pcm
        # clamp the alignment to the trimmed audio: the last word's end otherwise includes trailing silence
        spoken_end = (np.where(np.abs(pcm) > 0.01)[0][-1] + 1) / SR
        al = dict(al)
        al['character_end_times_seconds'] = [min(e, spoken_end) for e in al['character_end_times_seconds']]
        al['character_start_times_seconds'] = [min(s0, spoken_end) for s0 in al['character_start_times_seconds']]
        ws = words_from_alignment(al, t0 - lead)
        all_words += [dict(w=w, s=round(s, 3), e=round(e, 3)) for w, s, e in ws]
        k = 0
        for mc in marked_chunks(text):
            c = ws[k:k + len(mc)]; k += len(mc)
            chunks.append(dict(start=round(c[0][1], 3), end=round(c[-1][2], 3), words=[w for w, _, _ in c],
                               hot=[w for (w, _, _), (_, h) in zip(c, mc) if h]))
        assert k == len(ws), (text, len(ws), k)
        report.append(f'{t0:6.2f}-{t0 + dur - lead:6.2f} (slot to {t1:5.2f}) speed {speed:.3f}  {len(spoken.split()) / dur:.2f} w/s  {spoken}')
    chunks.sort(key=lambda c: c['start']); all_words.sort(key=lambda w: w['s'])
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
