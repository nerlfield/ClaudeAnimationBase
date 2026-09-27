"""The narration as ONE performance: pick the single ElevenLabs v3 read of the whole script that carries every line,
keep it intact inside each line (its breath before, its natural tail after), and fit it to the picture by changing
only the silent middles of the pauses.  A room-tone bed made from the read's own pauses runs underneath, so the
voice's background never switches on and off.  Writes build/vo.wav and build/words.json (then run
tools/caption_align.py).

    python tools/vo_flow.py                  # fetch (cached) reads, choose one, build the track

Why: picking each line from whichever read scored best (tools/vo_v3.py) put neighbouring lines from different
performances side by side (e.g. 99 Hz then 146 Hz), and every line started and ended on a short fade into digital
silence; the user heard it as "transitions … super unnatural and sharp".
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vo  # noqa: E402
import vo_takes  # noqa: E402
import vo_v3  # noqa: E402

SR = vo.SR
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from bh.shots import DUR as TOTAL  # noqa: E402
MIN_GAP = 0.14            # shortest pause between lines
MAX_KEEP_GAP = 1.1        # longest natural pause kept before the picture's window takes over
MAX_SQUEEZE = 0.92
LEAD, TAIL = 0.38, 0.45   # at most this much breath before / decay after each line comes from the read
# the chosen performance (from `python tools/vo_flow.py --search`), kept under the script it was read from
PIN = (179, 0.0)
# lines reworded after the read was chosen: re-read together, in their neighbours' company, with the pinned read's
# settings (seeds tried in turn) and spliced in.  The pinned read said "Out there, time's in fast-forward." here:
# heard as "times and fast forward" and, even reworded, too quick to land (round 9).
PATCH = {(10, 11): [179, 7, 19, 31, 43, 59, 71, 83]}


def tokens(text):
    """Words as compared with Whisper: lower case, no punctuation or apostrophes, hyphens split, digits spelled."""
    import re
    out = []
    for w in text.lower().replace('-', ' ').split():
        w = w.strip('.,?!')
        w = {'32': 'thirty two', '30': 'thirty', '1': 'one'}.get(w, w).replace('disc', 'disk')
        out += [re.sub(r"[^a-z]", '', x) for x in w.split()]
    return [x for x in out if x]


def segment(read, pcm, whisper, idx=None):
    """Per line (time order): speech onset s0 and end s1 in the read, the quiet points g0/g1 around it, the
    letters' times stretched onto [s0, s1], and whether Whisper heard exactly the line's words there.

    Line boundaries come from Whisper's word timings on the whole read, matched to the script (v3's own
    timestamps drift by up to 0.7 s and hand the pause before a sentence to its first letter).  The line texts are
    the read's own (one per text line), so a read keeps working after the script is reworded; idx names the script
    lines it holds (default: all of them, in time order)."""
    import difflib
    import librosa
    ch, st, en = read['al']['characters'], read['al']['character_start_times_seconds'], read['al']['character_end_times_seconds']
    full = ''.join(ch)
    idx = idx or vo_v3.order()
    texts = dict(zip(idx, read['text'].split('\n')))
    y16 = librosa.resample(pcm.astype(np.float64), orig_sr=SR, target_sr=16000).astype(np.float32)
    segs_w, _ = whisper.transcribe(y16, language='en', word_timestamps=True, beam_size=5, vad_filter=False)
    heard = [(w.start, w.end, t) for sw in segs_w for w in sw.words for t in tokens(w.word)]
    script_words, owner = [], []
    for i in idx:
        for t in tokens(texts[i]):
            script_words.append(t); owner.append(i)
    sm = difflib.SequenceMatcher(a=script_words, b=[h[2] for h in heard], autojunk=False)
    match = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            match[blk.a + k] = blk.b + k
    hop = int(0.01 * SR)
    rms = np.sqrt(np.convolve(pcm.astype(np.float64) ** 2, np.ones(hop) / hop, 'same'))[::hop]
    smooth = np.convolve(rms, np.ones(10) / 10, 'same')
    T = len(rms) / 100.0

    def quietest(a, b):
        a, b = max(0, int(a * 100)), min(len(smooth) - 1, int(b * 100))
        return (a + int(np.argmin(smooth[a:b + 1]))) / 100.0 if b > a else a / 100.0

    first, last, exact = {}, {}, {}
    for i in idx:
        ks = [k for k, o in enumerate(owner) if o == i]
        exact[i] = all(k in match for k in ks) and (match.get(ks[-1], -9) - match.get(ks[0], 0) == len(ks) - 1)
        mk = [match[k] for k in ks if k in match]
        first[i] = heard[mk[0]] if mk else None
        last[i] = heard[mk[-1]] if mk else None
    bounds = [0.0]
    for n in range(len(idx) - 1):
        i, j = idx[n], idx[n + 1]
        if last[i] is None or first[j] is None:
            return None, rms
        bounds.append(quietest(last[i][1] - 0.05, max(first[j][0] + 0.4, last[i][1] + 0.1)))
    bounds.append(T)
    out = {}
    spans, pos = {}, 0
    for i in idx:
        s_ = texts[i]; k = full.find(s_, pos); pos = k + len(s_)
        spans[i] = (k, k + len(s_))
    for n, i in enumerate(idx):
        g0, g1 = bounds[n], bounds[n + 1]
        seg = rms[int(g0 * 100):int(g1 * 100) + 1]
        if len(seg) < 20:
            return None, rms
        peak = seg.max()
        on = np.nonzero(seg > peak * 10 ** (-26 / 20))[0]
        off = np.nonzero(seg > peak * 10 ** (-38 / 20))[0]
        s0 = g0 + on[0] / 100.0; s1 = g0 + (off[-1] + 1) / 100.0
        k0, k1 = spans[i]
        o0, o1 = st[k0], en[k1 - 1]
        m = lambda t: s0 + (t - o0) * (s1 - s0) / max(o1 - o0, 1e-3)
        out[i] = dict(g0=g0, g1=g1, s0=s0, s1=s1, chars=ch[k0:k1], cs=[m(t) for t in st[k0:k1]],
                      ce=[m(t) for t in en[k0:k1]], exact=exact[i], text=texts[i],
                      gap=s0 - out[idx[n - 1]]['s1'] if n else 0.0)
    return out, rms


_last_fit = [None]


def plan(segs):
    _last_fit[0] = None
    """Place every line in its window, keeping the read's own pauses where the picture allows.
    -> [(i, start, ratio)] or None if the read can't be fitted."""
    idx = vo_v3.order()
    placed, prev_end, prev = [], 0.0, None
    for i in idx:
        w0, w1 = vo.LINES[i][0], vo.LINES[i][1]
        g = segs[i]
        dur = g['s1'] - g['s0']
        natural = g['gap'] if prev is not None else 0.0
        start = max(w0, prev_end + min(max(natural, MIN_GAP), MAX_KEEP_GAP))
        ratio = 1.0
        if start + dur > w1:
            # give up only as much of the pause as it takes to fit; squeeze only if even the shortest pause won't do
            start = max(w0, prev_end + MIN_GAP, w1 - dur)
            ratio = min(1.0, (w1 - start) / dur)
            if ratio < MAX_SQUEEZE:
                return None
        placed.append((i, start, ratio))
        _last_fit[0] = i
        prev_end, prev = start + dur * ratio, i
    return placed


def room_tone(pcm, rms, seconds):
    """A continuous bed from the read's own quiet stretches (runs of at least 80 ms below its 15th-percentile level,
    so no breaths), joined with 25 ms equal-power crossfades and looped."""
    thr = np.percentile(rms, 15)
    quiet = rms <= thr
    hop = int(0.01 * SR)
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if j - i >= 8:
                runs.append(pcm[(i + 1) * hop:(j - 1) * hop].astype(np.float32))
            i = j
        else:
            i += 1
    if not runs:
        return np.zeros(int(seconds * SR), np.float32)
    xf = int(0.025 * SR)
    bed = runs[0]
    k = 0
    while len(bed) < seconds * SR + xf:
        r = runs[(k + 1) % len(runs)]; k += 1
        if len(r) <= 2 * xf:
            if k > 10 * len(runs):
                break
            continue
        fade = np.sin(np.linspace(0, np.pi / 2, xf)) ** 2
        bed = np.concatenate([bed[:-xf], bed[-xf:] * (1 - fade) + r[:xf] * fade, r[xf:]])
    return bed[:int(seconds * SR)]


def speech_level(pcm, g):
    """RMS of the loud part of a line (frames within 20 dB of its peak), for matching a patch to its neighbours."""
    x = pcm[int(g['s0'] * SR):int(g['s1'] * SR)].astype(np.float64)
    hop = int(0.02 * SR)
    r = np.sqrt((x[:len(x) // hop * hop].reshape(-1, hop) ** 2).mean(axis=1))
    return float(np.sqrt((r[r > r.max() * 0.1] ** 2).mean()))


def keys_for(read):
    """The script line each of a read's text lines is (by its words); a line since reworded gets an 'old' key."""
    by_text = {vo.plain(vo.LINES[i][3]): i for i in vo_v3.order()}
    return [by_text.get(t, 'old%d' % n) for n, t in enumerate(read['text'].split('\n'))]


def patch(segs, pcm, whisper):
    """Replace each PATCH group of lines with the best of its context re-reads: every line heard exactly, spoken
    voice, and closest in pitch and pace to the pinned read's lines either side."""
    idx = vo_v3.order()
    for group, seeds in PATCH.items():
        k0, k1 = idx.index(group[0]), idx.index(group[-1])
        near = [idx[k] for k in (k0 - 1, k1 + 1) if 0 <= k < len(idx)]
        ref = [vo_takes.measure(pcm[int(segs[j]['s0'] * SR):int(segs[j]['s1'] * SR)], segs[j]['text'], whisper) for j in near]
        f0_ref = float(np.mean([m['f0'] for m in ref]))
        level_ref = float(np.mean([speech_level(pcm, segs[j]) for j in near]))
        rate_ref = float(np.mean([len(segs[j]['text']) / (segs[j]['s1'] - segs[j]['s0']) for j in near]))
        best = None
        # read with three lines of run-up before (closer to the full read's pace) and the next line after
        for seed in seeds:
            ctx = idx[max(0, k0 - 3):k1 + 2]
            d = vo_v3.fetch(seed, PIN[1], '\n'.join(vo.plain(vo.LINES[j][3]) for j in ctx))
            pp = vo_v3.decode(d['audio'])
            sp, _ = segment(d, pp, whisper, idx=ctx)
            if sp is None:
                print('  patch %s s%-3d  lines not found' % (group, seed)); continue
            cost, ok, rows = 0.0, True, []
            for i in group:
                g = sp[i]
                m = vo_takes.measure(pp[int(g['s0'] * SR):int(g['s1'] * SR)], g['text'], whisper)
                dur = g['s1'] - g['s0']
                rate = len(g['text']) / dur
                ok &= bool(g['exact'] and m['exact'] and m['voiced'] >= 0.3 and dur * MAX_SQUEEZE <= vo.LINES[i][1] - vo.LINES[i][0])
                # pace: never quicker than the lines around it (the user: "it sounds fast"), and not drawn out either
                pace = 3 * max(0.0, np.log(rate / rate_ref)) + 3 * max(0.0, np.log(0.7 * rate_ref / rate))
                cost += abs(12 * np.log2(max(m['f0'], 1) / f0_ref)) + pace - 0.1 * min(m['spread'], 4)
                rows.append('"%s" %.2fs f0 %3.0f rate %.1f' % (m['heard'], dur, m['f0'], rate))
            print('  patch %s s%-3d  %-6s cost %5.2f  (neighbours f0 %3.0f, rate %.1f c/s)  %s' % (
                group, seed, 'ok' if ok else 'reject', cost, f0_ref, rate_ref, ' | '.join(rows)))
            if ok and (best is None or cost < best[0]):
                gain = level_ref / float(np.mean([speech_level(pp, sp[i]) for i in group]))
                best = (cost, seed, {i: dict(sp[i], pcm=pp, gain=gain) for i in group}, sp, gain)
        if best is None:
            raise SystemExit('no re-read of lines %s passes: add seeds to PATCH' % (group,))
        cost, seed, new, sp, gain = best
        segs.update(new)
        if k1 + 1 < len(idx):
            segs[idx[k1 + 1]]['gap'] = sp[idx[k1 + 1]]['gap']      # the pause after them, as the re-read has it
        print('  patch %s: using s%d (gain %+.1f dB)' % (group, seed, 20 * np.log10(gain)))


def main():
    from faster_whisper import WhisperModel
    whisper = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
    idx = vo_v3.order()
    if '--search' not in sys.argv:
        d = json.load(open(os.path.join(vo_v3.READS, 'read_s%d_st%.1f.json' % PIN)))
        pcm = vo_v3.decode(d['audio'])
        segs, rms = segment(d, pcm, whisper, idx=keys_for(d))
        patch(segs, pcm, whisper)
        p = plan(segs)
        if not p:
            raise SystemExit('the pinned read no longer fits the windows (after line %s)' % _last_fit[0])
        build(PIN[0], PIN[1], pcm, segs, rms, p)
        return
    candidates = []
    for seed, stab in vo_v3.TAKES:
        d = vo_v3.fetch(seed, stab)
        pcm = vo_v3.decode(d['audio'])
        segs, rms = segment(d, pcm, whisper)
        if segs is None:
            print('read s%-3d st%.1f  reject  (lines not found in the transcript)' % (seed, stab))
            continue
        ms = {}
        for i in idx:
            g = segs[i]
            ms[i] = vo_takes.measure(pcm[int(g['s0'] * SR):int(g['s1'] * SR)], vo.plain(vo.LINES[i][3]), whisper)
            ms[i]['exact'] = g['exact']                    # judged on the whole read's transcript
        bad = [i for i in idx if not (ms[i]['exact'] and ms[i]['voiced'] >= 0.25)]
        f0s = [ms[i]['f0'] for i in idx if ms[i]['voiced'] >= 0.3 and ms[i]['f0'] > 0]
        centre = float(np.median(f0s)) if f0s else 0
        fry = [i for i in idx if ms[i]['f0'] < 0.72 * centre]
        p = plan(segs)
        if not p:
            j = vo_v3.order()[vo_v3.order().index(_last_fit[0]) + 1] if _last_fit[0] is not None else vo_v3.order()[0]
            print('      line %d needs %.2f s; window %.2f s' % (j, segs[j]['s1'] - segs[j]['s0'], vo.LINES[j][1] - vo.LINES[j][0]))
        verdict = 'ok' if (not bad and not fry and p) else 'reject'
        squeeze = sum(1 - r for _, _, r in p) if p else 9
        spread = float(np.mean([min(ms[i]['spread'], 6) for i in idx]))
        score = spread * 0.1 + np.mean([ms[i]['voiced'] for i in idx]) - 3 * squeeze
        print('read s%-3d st%.1f  %-6s  wrong/whisper %s  fry %s  fit %s  squeeze %.3f  expressiveness %.2f  score %.2f' % (
            seed, stab, verdict, bad or '-', fry or '-', 'yes' if p else 'NO (after line %s)' % _last_fit[0],
            squeeze if p else -1, spread, score))
        if verdict == 'ok':
            candidates.append((score, seed, stab, d, pcm, segs, rms, p))
    if not candidates:
        raise SystemExit('no single read carries the whole script: add seeds to vo_v3.TAKES or loosen a window')
    score, seed, stab, d, pcm, segs, rms, p = max(candidates, key=lambda c: c[0])
    print('using read s%d st%.1f (pin it in PIN)' % (seed, stab))
    build(seed, stab, pcm, segs, rms, p)


def build(seed, stab, pcm, segs, rms, p):
    n = int(TOTAL * SR)
    track = room_tone(pcm, rms, TOTAL) * 1.0
    words_all, chunks = [], []
    starts = {i: s for i, s, _ in p}
    for k, (i, start, ratio) in enumerate(p):
        g = segs[i]
        lead = min(LEAD, g['s0'] - g['g0'])
        tail = min(TAIL, g['g1'] - g['s1'])
        a, b = g['s0'] - lead, g['s1'] + tail
        seg = g.get('pcm', pcm)[int(a * SR):int(b * SR)].astype(np.float32) * g.get('gain', 1.0)
        if ratio < 1.0:
            seg = vo_v3.squeeze(seg, ratio)
        # the edges sit in the read's own pause noise, which matches the bed: long, gentle crossfades
        fi = int(max(0.02, lead * 0.8 * ratio) * SR); fo = int(max(0.04, tail * 0.8 * ratio) * SR)
        env = np.ones(len(seg), np.float32)
        env[:fi] = np.sin(np.linspace(0, np.pi / 2, fi)) ** 2
        env[-fo:] = np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
        p0 = int(round((start - lead * ratio) * SR))
        m = min(len(seg), n - p0)
        track[p0:p0 + m] = track[p0:p0 + m] * (1 - env[:m]) + seg[:m] * env[:m]
        # words for the captions: the read's letters, stretched onto the placed speech
        t_of = lambda t: start + (t - g['s0']) * ratio
        al = dict(characters=g['chars'], character_start_times_seconds=[t_of(t) for t in g['cs']],
                  character_end_times_seconds=[t_of(t) for t in g['ce']])
        ws = vo.words_from_alignment(al, 0.0)
        words_all += [dict(w=w, s=round(s, 3), e=round(e, 3)) for w, s, e in ws]
        q = 0
        for mc in vo.marked_chunks(vo.LINES[i][3]):
            c = ws[q:q + len(mc)]; q += len(mc)
            chunks.append(dict(start=round(c[0][1], 3), end=round(c[-1][2], 3), words=[w for w, _, _ in c],
                               hot=[w for (w, _, _), (_, h) in zip(c, mc) if h]))
        print('  line %2d  %6.2f-%6.2f  (window %.2f-%.2f)%s  %s' % (
            i, start, start + (g['s1'] - g['s0']) * ratio, vo.LINES[i][0], vo.LINES[i][1],
            '  squeeze x%.3f' % ratio if ratio < 1 else '', g['text']))
    chunks.sort(key=lambda c: c['start'])
    for j, c in enumerate(chunks):
        nxt = chunks[j + 1]['start'] if j + 1 < len(chunks) else 99
        c['end'] = round(min(nxt, c['end'] + 0.35), 3)
    with open(os.path.join(vo.BUILD, 'vo.f32'), 'wb') as f:
        f.write(track.astype(np.float32).tobytes())
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i',
                    os.path.join(vo.BUILD, 'vo.f32'), os.path.join(vo.BUILD, 'vo.wav')], check=True)
    json.dump(dict(words=words_all, chunks=chunks, read='s%d/st%.1f' % (seed, stab),
                   patched={str(i): 'context re-read' for g in PATCH for i in g} if '--search' not in sys.argv else {}),
              open(os.path.join(vo.BUILD, 'words.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
