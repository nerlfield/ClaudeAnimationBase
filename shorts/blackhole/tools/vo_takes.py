"""Alternative takes for chosen voice lines, measured and ranked; the winner replaces that line's cached take.

    python tools/vo_takes.py 0 11 12            # generate takes for lines 0, 11 and 12, rank, and install the best
    python tools/vo_takes.py 0 --report         # only rank the takes already generated

A take must be spoken in a normal voice (pyin voiced fraction >= 0.4: the first pass whispered line 12 and
fried line 0), sit in the narrator's range (median f0 90-145 Hz), move (f0 spread >= 1.5 semitones, except the
deadpan "Black hole."), fit its slot, and transcribe exactly.  Same voice (Chris) and model as tools/vo.py; the
API key is read from ELEVENLABS_API_KEY.
"""
import base64
import json
import os
import re
import shutil
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vo  # noqa: E402

TAKES = os.path.join(vo.BUILD, 'vo_takes')
SETTINGS = [  # (seed, stability, style)
    (11, 0.50, 0.20), (23, 0.50, 0.20), (37, 0.60, 0.10), (41, 0.60, 0.10), (53, 0.45, 0.30), (67, 0.45, 0.30),
    (71, 0.50, 0.30), (83, 0.55, 0.20)]


def tts(text, prev_text, next_text, speed, seed, stability, style):
    import urllib.request
    import subprocess
    body = dict(text=text, model_id=vo.MODEL, previous_text=prev_text, next_text=next_text, seed=seed,
                voice_settings=dict(stability=stability, similarity_boost=0.8, style=style, use_speaker_boost=True, speed=speed))
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{vo.VOICE}/with-timestamps?output_format=mp3_44100_192',
        data=json.dumps(body).encode(), headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(vo.SR), 'pipe:1'],
                       input=base64.b64decode(d['audio_base64']), capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy(), d['alignment']


def measure(pcm, text, whisper):
    import librosa
    import pyloudnorm as pyln
    y = librosa.resample(pcm.astype(np.float64), orig_sr=vo.SR, target_sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=60, fmax=320, sr=16000, frame_length=1024)
    v = ~np.isnan(f0)
    f0v = f0[v]
    med = float(np.median(f0v)) if v.any() else 0.0
    spread = float(np.std(12 * np.log2(f0v / med))) if v.sum() > 3 else 0.0
    segs, _ = whisper.transcribe(y.astype(np.float32), language='en', beam_size=5)
    heard = ' '.join(s.text for s in segs)
    norm = lambda s: re.sub(r"[^a-z' ]", '', s.lower().replace('disc', 'disk')).split()
    return dict(dur=len(pcm) / vo.SR, voiced=float(v.mean()), f0=med, spread=spread, heard=heard.strip(),
                exact=norm(heard) == norm(text), lufs=pyln.Meter(vo.SR, block_size=0.2).integrated_loudness(pcm.astype(np.float64)))


def score(m, slot, deadpan):
    """Higher is better; -inf if a hard rule fails."""
    if not m['exact'] or m['dur'] > slot + 0.05 or m['voiced'] < 0.4 or not (90 <= m['f0'] <= 145):
        return -np.inf
    if not deadpan and m['spread'] < 1.5:
        return -np.inf
    # ...and stays near the narrator's usual pitch (median of the accepted lines, ~115 Hz) so lines match
    return m['voiced'] + 0.15 * min(m['spread'], 4.0) - 0.3 * abs(m['dur'] - 0.85 * slot) - 0.02 * abs(m['f0'] - 115)


def main():
    from faster_whisper import WhisperModel
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    report_only = '--report' in sys.argv
    whisper = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2)
    os.makedirs(TAKES, exist_ok=True)
    order = sorted(range(len(vo.LINES)), key=lambda i: vo.LINES[i][0])
    for a in args:
        i = int(a)
        t0, t1, speed, text = vo.LINES[i]
        spoken = vo.plain(text)
        k = order.index(i)
        prev_text = ' '.join(vo.plain(vo.LINES[j][3]) for j in order[max(0, k - 2):k])
        next_text = vo.plain(vo.LINES[order[k + 1]][3]) if k + 1 < len(order) else ''
        rows = []
        cands = [('current', os.path.join(vo.BUILD, f'vo_{i:02d}.json'))]
        for seed, stab, style in SETTINGS:
            path = os.path.join(TAKES, f'vo_{i:02d}_s{seed}.json')
            if not os.path.exists(path) and not report_only:
                raw, al = tts(spoken, prev_text, next_text, speed, seed, stab, style)
                pcm, al, _ = vo.trim(raw, al)
                json.dump(dict(text=spoken, speed=speed, pcm=base64.b64encode(pcm.astype(np.float32).tobytes()).decode(), al=al,
                               seed=seed, stability=stab, style=style), open(path, 'w'))
            if os.path.exists(path):
                cands.append((f's{seed} stab {stab} style {style}', path))
        for name, path in cands:
            c = json.load(open(path))
            pcm = np.frombuffer(base64.b64decode(c['pcm']), np.float32)
            m = measure(pcm, spoken, whisper)
            s = score(m, t1 - t0, deadpan=(spoken == 'Black hole.'))
            rows.append((s, name, path, m))
        rows.sort(key=lambda r: -r[0])
        print(f'line {i}: "{spoken}" (slot {t1 - t0:.2f} s)')
        for s, name, path, m in rows:
            print('  %-26s score %6s  %.2fs voiced %.2f f0 %3.0f spread %.1f st  %5.1f LUFS  %s%s' % (
                name, '%.2f' % s if np.isfinite(s) else 'fail', m['dur'], m['voiced'], m['f0'], m['spread'], m['lufs'],
                'exact' if m['exact'] else 'heard "%s"' % m['heard'], '  <- best' if (s, name) == rows[0][:2] else ''))
        best = rows[0]
        if np.isfinite(best[0]) and best[1] != 'current' and not report_only:
            dst = os.path.join(vo.BUILD, f'vo_{i:02d}.json')
            bak = os.path.join(TAKES, f'vo_{i:02d}_original.json')
            if not os.path.exists(bak):
                shutil.copy(dst, bak)
            c = json.load(open(best[2]))
            json.dump(dict(text=c['text'], speed=c['speed'], pcm=c['pcm'], al=c['al']), open(dst, 'w'))
            print('  installed', os.path.basename(best[2]))


if __name__ == '__main__':
    main()
