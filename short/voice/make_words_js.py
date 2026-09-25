# make_words_js.py: words.json + segments.json → words.js (pages opened from file:// can't fetch JSON).
import json, os
H = os.path.dirname(os.path.abspath(__file__))
w, s = json.load(open(f'{H}/words.json')), json.load(open(f'{H}/segments.json'))
open(f'{H}/words.js', 'w').write('// generated from words.json / segments.json by short/voice/make_words_js.py\nconst WORDS = ' + json.dumps(w) + ';\nconst SEGS = ' + json.dumps(s) + ';\n')
