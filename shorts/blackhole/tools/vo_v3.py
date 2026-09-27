"""The narration as a continuous performance: ElevenLabs v3 reads the whole script in one go (several seeds), each
read is cut into its lines at the character timestamps, keeping the breath before each line and its natural tail,
and the best version of every line goes into the cache that tools/vo.py places on the beat sheet.

    python tools/vo_v3.py            # fetch (cached) reads, rank every line across them, write build/vo_XX.json

Why: lines generated one at a time with eleven_multilingual_v2 sounded read-out (the user: "too scripted, feels like
a robot").  A continuous v3 read keeps the rhythm, energy and intonation of one person talking.  v3 ignores the
speed setting and reads slower, so the beat sheet's slots use the real gaps between beats, and a line that still
doesn't fit may be tightened by WSOLA, at most 8% (more would itself sound processed).
The API key is read from ELEVENLABS_API_KEY and never written anywhere.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vo  # noqa: E402
import vo_takes  # noqa: E402

SR = vo.SR
READS = os.path.join(vo.BUILD, 'vo_v3', vo.VOICE)
# (seed, stability): v3 accepts 0.0 (creative), 0.5 (natural) or 1.0 (robust)
TAKES = [(7, 0.5), (19, 0.5), (31, 0.5), (43, 0.5), (59, 0.0), (71, 0.0), (83, 0.5), (97, 0.0)]
MAX_SQUEEZE = 0.92
PRE, POST = 0.35, 0.28              # breath before, natural decay after (never into a neighbouring line)


def order():
    return sorted(range(len(vo.LINES)), key=lambda i: vo.LINES[i][0])


def script():
    return '\n'.join(vo.plain(vo.LINES[i][3]) for i in order())


# lines that also get short context reads.  "Black hole." is the script's last sentence, and every full read ended
# it with a creaky final drop (f0 at or below 60 Hz); the video loops, so it is read the way a viewer hears it,
# followed by the opening line, and cut out of the middle.
CONTEXT = {11: "Everything else? Black hole. This dot? It's the whole universe."}   # (index 11 = "Black hole.")


def fetch(seed, stability, text=None):
    os.makedirs(READS, exist_ok=True)
    text = text or script()
    tag = '' if text == script() else '_ctx%08x' % (abs(hash(text)) % 0xffffffff)
    path = os.path.join(READS, f'read_s{seed}_st{stability}{tag}.json')
    if os.path.exists(path):
        d = json.load(open(path))
        if d['text'] == text:
            return d
    body = dict(text=text, model_id='eleven_v3', seed=seed, voice_settings=dict(stability=stability, similarity_boost=0.75))
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{vo.VOICE}/with-timestamps?output_format=mp3_44100_192',
        data=json.dumps(body).encode(), headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    d = dict(text=text, seed=seed, stability=stability, audio=d['audio_base64'], al=d['alignment'])
    json.dump(d, open(path, 'w'))
    return d


def decode(b64):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-f', 'f32le', '-ac', '1', '-ar', str(SR), 'pipe:1'],
                       input=base64.b64decode(b64), capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def squeeze(x, ratio):
    """WSOLA time compression (ratio < 1 = shorter), pitch unchanged."""
    from audiotsm import wsola
    from audiotsm.io.array import ArrayReader, ArrayWriter
    reader = ArrayReader(x[None, :].astype(np.float32))
    writer = ArrayWriter(1)
    wsola(1, speed=1.0 / ratio).run(reader, writer)
    return writer.data[0].astype(np.float32)


def cut(read, pcm, only=None):
    """-> {line index: dict(pcm, al, lead, speech)} for one read.  With only=i the read is a context read and just
    line i is cut from it.

    v3's timestamps are only a rough guide: they give the pause before a sentence to its first letter and can drift
    by half a second over a read (cuts made from them clipped word endings).  So the audio decides: sentences are
    split at the quietest 100 ms near each pause, each line's speech runs from its first frame within 26 dB of its
    loudest to its last within 38 dB, and the letters' times are stretched onto that span for the captions."""
    ch, st, en = read['al']['characters'], read['al']['character_start_times_seconds'], read['al']['character_end_times_seconds']
    full = ''.join(ch)
    names, spans, pos = [], {}, 0
    targets = [only] if only is not None else order()
    for i in targets:
        s = vo.plain(vo.LINES[i][3]); k = full.find(s, pos); pos = k + len(s)
        spans[i] = (k, k + len(s)); names.append(i)
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(pcm.astype(np.float64) ** 2, np.ones(hop) / hop, 'same'))[::hop]
    smooth = np.convolve(rms, np.ones(10) / 10, 'same')
    T = len(rms) / 100.0

    def quietest(t_a, t_b):
        a, b = max(0, int(t_a * 100)), min(len(smooth) - 1, int(t_b * 100))
        return (a + int(np.argmin(smooth[a:b + 1]))) / 100.0 if b > a else t_a

    # boundaries: before the first target, between targets, after the last
    k_first, k_last = spans[names[0]][0], spans[names[-1]][1]
    bounds = [quietest(st[k_first] - 0.8, st[k_first] + 0.2) if k_first > 0 else 0.0]
    for n in range(len(names) - 1):
        e_prev, s_next = en[spans[names[n]][1] - 1], st[spans[names[n + 1]][0]]
        mid = 0.5 * (e_prev + s_next)
        bounds.append(quietest(mid - 0.8, mid + 0.8))
    bounds.append(quietest(en[k_last - 1] - 0.2, en[k_last - 1] + 0.8) if k_last < len(ch) - 1 else T)
    out = {}
    for n, i in enumerate(names):
        g0, g1 = bounds[n], bounds[n + 1]
        a_, b_ = int(g0 * 100), int(g1 * 100)
        if b_ - a_ < 30:
            continue                                   # a pause wasn't found where expected: skip this candidate
        seg_rms = rms[a_:b_ + 1]
        peak = seg_rms.max()
        on = np.nonzero(seg_rms > peak * 10 ** (-26 / 20))[0]
        off = np.nonzero(seg_rms > peak * 10 ** (-38 / 20))[0]
        s0 = (a_ + on[0]) / 100.0; s1 = (a_ + off[-1] + 1) / 100.0
        k0, k1 = spans[i]
        o0, o1 = st[k0], en[k1 - 1]
        m = lambda t: s0 + (t - o0) * (s1 - s0) / max(o1 - o0, 1e-3)
        a = max(g0, s0 - PRE); b = min(g1, s1 + POST)
        seg = pcm[int(a * SR):int(b * SR)].copy()
        if len(seg) < int(0.3 * SR):
            continue
        f = int(0.03 * SR); seg[:f] *= np.linspace(0, 1, f) ** 2
        g = int(0.07 * SR); seg[-g:] *= np.linspace(1, 0, g) ** 1.5
        cs = [m(t) for t in st[k0:k1]]; ce = [m(t) for t in en[k0:k1]]
        # a caption chunk that starts mid-line (after "Hover here," or "around it?") starts where the voice does:
        # the first frame within 26 dB of the line's peak after the quietest moment near the stretched estimate
        text = vo.plain(vo.LINES[i][3]); starts = [j for j in range(len(text)) if text[j] != ' ' and (j == 0 or text[j - 1] == ' ')]
        wi = 0
        for chunk in vo.marked_chunks(vo.LINES[i][3])[:-1]:
            wi += len(chunk)
            j0 = starts[wi]; j1 = starts[wi + 1] if wi + 1 < len(starts) else len(text)
            if text[j0 - 2] not in ',.?!':
                continue                               # no pause to find ("fills exactly"): keep the estimate
            t_est = cs[j0]
            q0, q1 = int((t_est - 0.35) * 100), int((t_est + 0.25) * 100)
            if q1 - q0 < 5:
                continue
            tq = q0 + int(np.argmin(smooth[q0:q1]))
            up = np.nonzero(rms[tq:q1 + 20] > peak * 10 ** (-26 / 20))[0]
            if len(up):
                t_on = (tq + up[0]) / 100.0
                for j in range(j0, j1):
                    cs[j] = max(cs[j], t_on) if cs[j] < t_on else cs[j]
                cs[j0] = t_on
        al = dict(characters=ch[k0:k1], character_start_times_seconds=[t - a for t in cs],
                  character_end_times_seconds=[t - a for t in ce])
        out[i] = dict(pcm=seg, al=al, lead=s0 - a, speech=s1 - s0)
    return out


def chunk_starts_from_whisper(pcm, al, marked, whisper):
    """Caption chunks that start mid-line get their start from Whisper's word timing on the chosen take (the
    stretched v3 timestamps can be 0.2-0.5 s off inside a line, and a comma is not always a pause)."""
    import librosa
    words = vo.plain(marked).split()
    y = librosa.resample(pcm.astype(np.float64), orig_sr=SR, target_sr=16000).astype(np.float32)
    segs, _ = whisper.transcribe(y, language='en', word_timestamps=True, beam_size=5)
    heard = [w for sg in segs for w in sg.words]
    if len(heard) != len(words):
        return al
    text = vo.plain(marked)
    starts = [j for j in range(len(text)) if text[j] != ' ' and (j == 0 or text[j - 1] == ' ')]
    cs = list(al['character_start_times_seconds'])
    # Whisper stretches a word that follows a pause back into the silence: start at the voice's own onset instead
    # (first 5 ms frame within 32 dB of the take's peak, after any 60 ms of quiet inside Whisper's span)
    hop = int(0.005 * SR)
    x = pcm[: len(pcm) // hop * hop].reshape(-1, hop)
    rms = np.sqrt((x.astype(np.float64) ** 2).mean(axis=1))
    thr = rms.max() * 10 ** (-32 / 20)

    def onset(a, b):
        i0, i1 = int(a / 0.005), min(len(rms), int((b + 0.3) / 0.005))
        on = rms[i0:i1] > thr
        quiet = np.convolve(~on, np.ones(12), 'valid') == 12
        q = np.nonzero(quiet)[0]
        if len(q):
            on[:q[0] + 12] = False
        k = np.nonzero(on)[0]
        return (i0 + k[0]) * 0.005 if len(k) else a
    wi = 0
    for chunk in vo.marked_chunks(marked)[:-1]:
        wi += len(chunk)
        j0 = starts[wi]; j1 = starts[wi + 1] if wi + 1 < len(starts) else len(text)
        t_on = onset(heard[wi].start, heard[wi].end)
        for j in range(j0, j1):
            cs[j] = max(cs[j], t_on)
        cs[j0] = t_on
    al = dict(al); al['character_start_times_seconds'] = cs
    return al


def main():
    from faster_whisper import WhisperModel
    whisper = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2)
    reads = []
    for seed, stab in TAKES:
        d = fetch(seed, stab)
        reads.append((f's{seed}/st{stab}', cut(d, decode(d['audio']))))
        print('read', seed, stab, flush=True)
    for i, text in CONTEXT.items():
        for seed, stab in TAKES:
            d = fetch(seed, stab, text)
            reads.append((f'ctx s{seed}/st{stab}', cut(d, decode(d['audio']), only=i)))
    idx = order()
    # measure every candidate once
    cands = {i: [] for i in idx}
    for name, lines in reads:
        for i, c in lines.items():
            lead = c['lead']
            speech = c['pcm'][int(lead * SR):]
            m = vo_takes.measure(speech, vo.plain(vo.LINES[i][3]), whisper)
            cands[i].append((name, c, m))
    center = float(np.median([m['f0'] for i in idx for _, _, m in cands[i] if m['voiced'] >= 0.4 and m['f0'] > 0]))
    print('narrator pitch centre (median of well-voiced lines): %.0f Hz' % center)
    for n, i in enumerate(idx):
        t0, t1, speed, text = vo.LINES[i]
        spoken = vo.plain(text)
        prev_t1 = vo.LINES[idx[n - 1]][1] if n else 0.0
        max_lead = max(0.05, t0 - prev_t1)
        rows = []
        for name, c, m in cands[i]:
            lead = min(c['lead'], max_lead)
            pcm = c['pcm'][int((c['lead'] - lead) * SR):]
            al = dict(c['al']); sh = c['lead'] - lead
            al['character_start_times_seconds'] = [t - sh for t in al['character_start_times_seconds']]
            al['character_end_times_seconds'] = [t - sh for t in al['character_end_times_seconds']]
            room = t1 + 0.05 - t0 + lead                    # seconds available from the cut's start
            ratio = min(1.0, room / (len(pcm) / SR))
            # hard rules reject only defects: wrong words, a whisper (almost nothing voiced), vocal fry (a median far
            # below the narrator's), or no fit.  v3 is expressive, so questions may sit well above the centre.
            ok = m['exact'] and m['voiced'] >= 0.2 and m['f0'] >= 0.72 * center and ratio >= MAX_SQUEEZE
            score = (m['voiced'] + 0.08 * min(m['spread'], 6.0) - 0.3 * abs(np.log2(max(m['f0'], 1) / center))
                     - 3.0 * (1 - ratio)) if ok else -np.inf
            rows.append((score, name, ratio, lead, pcm, al, m))
        rows.sort(key=lambda r: -r[0])
        best = rows[0]
        print(f'line {i:2d} "{spoken}" slot {t0:.2f}-{t1:.2f}')
        for score, name, ratio, lead, pcm, al, m in rows:
            print('   %-10s %6s  speech %.2fs voiced %.2f f0 %3.0f spread %.1f  fit x%.3f  %s%s' % (
                name, '%.2f' % score if np.isfinite(score) else 'fail', m['dur'], m['voiced'], m['f0'], m['spread'], ratio,
                'exact' if m['exact'] else 'heard "%s"' % m['heard'], '  <- picked' if name == best[1] else ''))
        if not np.isfinite(best[0]):
            raise SystemExit(f'line {i}: no read fits; loosen the slot or rephrase')
        score, name, ratio, lead, pcm, al, m = best
        if ratio < 1.0:
            pcm = squeeze(pcm, ratio); lead *= ratio
            for k in ('character_start_times_seconds', 'character_end_times_seconds'):
                al[k] = [t * ratio for t in al[k]]
        al = chunk_starts_from_whisper(pcm, al, text, whisper)
        json.dump(dict(text=spoken, speed=speed, voice=vo.VOICE, model='eleven_v3', read=name, squeeze=ratio, lead=lead,
                       pcm=base64.b64encode(pcm.astype(np.float32).tobytes()).decode(), al=al),
                  open(os.path.join(vo.BUILD, f'vo_{i:02d}.json'), 'w'))


if __name__ == '__main__':
    main()
