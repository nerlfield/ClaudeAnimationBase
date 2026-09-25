# tts_segments.py: the narration, one ElevenLabs request per sentence (with the neighbouring sentences passed as
# context so the delivery stays continuous), trimmed to its words and joined with the designed gaps from segments.txt.
#   ELEVEN_KEY_FILE=<path outside the repo> python3 short/voice/tts_segments.py [voice_id] [speed]
# Writes short/voice/voice.wav (48 kHz mono), words.json ([{w, start, end, seg}] in video seconds) and
# segments.json ([{id, text, start, end}]). Cached per sentence in short/voice/seg/, so re-running only re-joins.
import base64, json, os, subprocess, sys, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
voice = sys.argv[1] if len(sys.argv) > 1 else 'aGfQDyfOrmWWfC7ZnTbv'   # "James H - Tech Explainer"
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.15
SEG = []
for line in open(os.path.join(HERE, 'segments.txt')):
    if line.strip() and not line.startswith('#'):
        sid, gap, text = [x.strip() for x in line.split('|', 2)]
        SEG.append({'id': sid, 'gap': float(gap), 'text': text})
os.makedirs(os.path.join(HERE, 'seg'), exist_ok=True)
key = open(os.environ['ELEVEN_KEY_FILE']).read().strip() if 'ELEVEN_KEY_FILE' in os.environ else None

def tts(i):
    s, base = SEG[i], os.path.join(HERE, 'seg', SEG[i]['id'])
    if os.path.exists(base + '.json'): return json.load(open(base + '.json'))
    body = {'text': s['text'], 'model_id': 'eleven_multilingual_v2',
            'previous_text': ' '.join(x['text'] for x in SEG[max(0, i - 2):i]) or None,
            'next_text': ' '.join(x['text'] for x in SEG[i + 1:i + 3]) or None,
            'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.25, 'use_speaker_boost': True, 'speed': speed}}
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192',
                                 data=json.dumps(body).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req))
    open(base + '.mp3', 'wb').write(base64.b64decode(r['audio_base64']))
    json.dump(r['alignment'], open(base + '.json', 'w'))
    return r['alignment']

def words_of(al):
    out, cur = [], None
    for c, a, b in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c.isspace():
            if cur: out.append(cur); cur = None
            continue
        if cur is None: cur = {'w': '', 'start': a, 'end': b}
        cur['w'] += c
        if c.isalnum(): cur['end'] = b   # punctuation carries the pause after a word, so it doesn't count
    if cur: out.append(cur)
    return out

PRE, POST = 0.04, 0.10          # keep a breath of attack before the first word and the decay after the last
t, words, segs, parts = 0.0, [], [], []
for i, s in enumerate(SEG):
    w = words_of(tts(i))
    a, b = max(0.0, w[0]['start'] - PRE), w[-1]['end'] + POST
    wav = os.path.join(HERE, 'seg', s['id'] + '.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(HERE, 'seg', s['id'] + '.mp3'), '-ss', f'{a:.3f}', '-to', f'{b:.3f}',
                    '-af', 'afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,areverse', '-ar', '48000', '-ac', '1', wav], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
    for x in w: words.append({'w': x['w'], 'start': round(t + x['start'] - a, 3), 'end': round(t + x['end'] - a, 3), 'seg': s['id']})
    segs.append({'id': s['id'], 'text': s['text'], 'start': round(t, 3), 'end': round(t + dur, 3)})
    parts.append((wav, s['gap']))
    t += dur + s['gap']
# join: each sentence followed by its gap of silence
inputs, filt = [], []
for k, (wav, gap) in enumerate(parts):
    inputs += ['-i', wav]
    filt.append(f'[{k}]apad=pad_dur={gap:.3f}[p{k}]')
filt.append(''.join(f'[p{k}]' for k in range(len(parts))) + f'concat=n={len(parts)}:v=0:a=1[out]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(filt), '-map', '[out]', '-ar', '48000', '-ac', '1',
                os.path.join(HERE, 'voice.wav')], check=True)
json.dump(words, open(os.path.join(HERE, 'words.json'), 'w'), indent=0)
json.dump(segs, open(os.path.join(HERE, 'segments.json'), 'w'), indent=1)
print(f'{len(words)} words, voice ends {t:.2f} s, {len(words) / t:.2f} wps overall')
