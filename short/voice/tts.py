# tts.py: narration with character timestamps from ElevenLabs, turned into word timestamps.
#   ELEVEN_KEY_FILE=<path> python3 short/voice/tts.py <voice_id> <out_prefix> [speed]
# Writes <out_prefix>.mp3 and <out_prefix>.words.json ([{w, start, end}], seconds). The key is read from a file
# outside the repo and never written into it.
import base64, json, os, re, sys, urllib.request
voice, out = sys.argv[1], sys.argv[2]
speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
key = open(os.environ['ELEVEN_KEY_FILE']).read().strip()
text = open(os.path.join(os.path.dirname(__file__), 'script.txt')).read().strip().replace('\n', ' ')
body = {'text': text, 'model_id': 'eleven_multilingual_v2',
        'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.25, 'use_speaker_boost': True, 'speed': speed}}
req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192',
                             data=json.dumps(body).encode(), headers={'xi-api-key': key, 'Content-Type': 'application/json'})
r = json.load(urllib.request.urlopen(req))
open(out + '.mp3', 'wb').write(base64.b64decode(r['audio_base64']))
al = r['alignment']
chars, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
words, cur = [], None
for c, a, b in zip(chars, st, en):
    if c.isspace():
        if cur: words.append(cur); cur = None
        continue
    if cur is None: cur = {'w': '', 'start': a, 'end': b}
    cur['w'] += c
    if c.isalnum(): cur['end'] = b   # punctuation carries the pause after a word, so it doesn't count
if cur: words.append(cur)
json.dump(words, open(out + '.words.json', 'w'), indent=0)
json.dump(al, open(out + '.alignment.json', 'w'))
dur = words[-1]['end']
print(f'{len(words)} words, {dur:.2f} s, {len(words) / dur:.2f} wps')
