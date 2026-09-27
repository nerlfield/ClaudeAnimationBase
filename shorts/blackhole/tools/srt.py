"""Write outputs/captions_en.srt from the burned-in caption chunks (build/words.json), for upload as a text track.

    python tools/srt.py            # after tools/caption_align.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def stamp(t):
    ms = int(round(t * 1000))
    return '%02d:%02d:%02d,%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


def main():
    chunks = json.load(open(os.path.join(HERE, '..', 'build', 'words.json')))['chunks']
    out = []
    for n, c in enumerate(chunks, 1):
        out.append('%d\n%s --> %s\n%s\n' % (n, stamp(c['start']), stamp(c['end']), ' '.join(c['words'])))
    path = os.path.join(HERE, '..', '..', '..', 'outputs', 'captions_en.srt')
    open(path, 'w').write('\n'.join(out))
    print('%d cues -> %s' % (len(chunks), os.path.relpath(path)))


if __name__ == '__main__':
    main()
