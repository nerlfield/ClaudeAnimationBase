"""Which overlays are on screen at time t.  Captions come from build/words.json (TTS alignment) when it
exists, else from the planned timings below.  Line text uses '|' for chunk breaks and '*' for gold words."""
import json
import math
import os

import numpy as np

from . import overlay as ov
from .overlay import _ease_out
from .shots import T_A, T_B, T_C, T_D, T_E, T_E2, T_F, T_G, BAR, DUR, T_A_REAL, dot_tau, state, seg, unwarp

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_JSON = os.path.join(HERE, '..', 'build', 'words.json')
MID_LEAD = 0.12
# top of the finished dot's rim against the end camera's clock (tau), measured on the rendered frames: the push-in
# carries it up and left a little
DOT_RIM = [(33.0, 533, 538), (36.0, 529, 533), (39.3, 526, 528), (40.5, 525, 526), (41.5, 524, 524), (42.5, 522, 522),
           (43.3, 522, 521)]


def dot_top(t):
    ts, xs, ys = zip(*DOT_RIM)
    return float(np.interp(t, ts, xs)), float(np.interp(t, ts, ys))

# (start, end, text) -- the same lines tools/vo.py speaks
LINES = [
    (0.15, 2.10, 'This dot is | the whole *universe.'),
    (2.85, 5.20, 'To see it, | fly down | to a *black *hole.'),
    (6.00, 7.60, 'The disk around it | is *flat.'),
    (9.00, 10.60, 'So why does it | look like *this?'),
    (12.00, 15.00, "That's the *back | of the disk, | bent over the top | by gravity."),
    (19.00, 21.90, 'Hover here, | and the black hole | fills exactly | *half your sky.'),
    (22.30, 24.00, 'And light goes | around it in *circles.'),
    (24.20, 25.90, "That's the back | of your own *head."),
    (26.90, 28.80, 'Now hover | just above the *edge.'),
    (29.00, 32.30, 'The whole universe | gets squeezed | into one *dot | above your head.'),
    (33.40, 34.20, 'Everything else?'),
    (35.00, 35.70, '*Black *hole.'),
]


def parse(text):
    """-> list of chunks, each a list of (word, hot)."""
    out = []
    for part in text.split('|'):
        ws = [(w.lstrip('*'), w.startswith('*')) for w in part.split()]
        if ws:
            out.append(ws)
    return out


def chunks():
    """[(start, end, [words], [hot words])]"""
    if os.path.exists(WORDS_JSON):
        data = json.load(open(WORDS_JSON))
        out = [[c['start'], c['end'], c['words'], c.get('hot', [])] for c in data['chunks']]
        # a chunk that follows mid-sentence (no pause) switches 0.12 s early: the TTS alignment puts a word's
        # start at its first letter, which ears (and Whisper) hear slightly before
        for prev, cur in zip(out, out[1:]):
            if abs(cur[0] - prev[1]) < 0.02 and not prev[2][-1].endswith(('.', '?', '!')):
                cur[0] -= MID_LEAD; prev[1] -= MID_LEAD
        out = _split_long(out, data['words'])
        for c in out:
            if c[0] < 0.3:
                c[0] = 0.0                                  # the claim is on screen from frame 0
            if c[2][-1] == 'universe.' and c[1] < 2.67:
                c[1] = T_A - 0.05                           # hold it to the cut instead of leaving a gap
            c[3] = c[3] + [w for w in c[2] if w.strip('.,?!').lower() in EXTRA_HOT]
        return [tuple(c) for c in out]
    out = []
    for a, b, text in LINES:
        cs = parse(text)
        n = sum(len(c) for c in cs); dt = (b - a) / n; i = 0
        for c in cs:
            out.append((a + i * dt, a + (i + len(c)) * dt + (0.35 if c is cs[-1] else 0), [w for w, _ in c], [w for w, h in c if h]))
            i += len(c)
    return out


# a chunk that would need a smaller font is split at a phrase boundary, timed from the TTS word starts
SPLITS = {('The', 'whole', 'universe', 'gets', 'squeezed'): 3}     # (earlier wording; kept for the Chris cut)
EXTRA_HOT = {'squeezed', 'shrinks'}


def _split_long(out, words):
    res = []
    for c in out:
        k = SPLITS.get(tuple(c[2]))
        if k is None:
            res.append(c); continue
        ws = [w for w in words if c[0] - 0.2 <= w['s'] < c[1] + 0.05][:len(c[2])]
        mid = ws[k]['s'] - MID_LEAD
        res.append([c[0], mid, c[2][:k], [h for h in c[3] if h in c[2][:k]]])
        res.append([mid, c[1], c[2][k:], [h for h in c[3] if h in c[2][k:]]])
    return res


def chunk_time(first_words, after=30.0, default=None):
    """When the voice starts the caption chunk beginning with these words (labels pop with the words)."""
    for a, b, words, hot in chunks():
        if a > after and [w.strip('.,?!') for w in words[:len(first_words)]] == first_words:
            return a
    return default


def back_front_times():
    """When BACK and FRONT pop on the flat disk: on "This is the back half." and "And this is the front half."
    (the pops' sounds too)."""
    return (chunk_time(['This', 'is', 'the', 'back'], after=5.0, default=17.3),
            chunk_time(['And', 'this', 'is', 'the', 'front'], after=5.0, default=18.9))


def minute_times():
    """When 1 MIN pops ("Stay for one minute"), when it counts up to 32 ("and half an hour"), and when it goes."""
    t_min = chunk_time(['Stay', 'for'], default=65.4)
    t_hour = chunk_time(['and', 'half'], default=67.3)
    return t_min, t_hour, chunk_time(['And', 'all', 'this'], default=70.0) - 0.1


def black_hole_time():
    """When the voice says "That's the black hole." (the callout pops with it)."""
    return chunk_time(["That's", 'the', 'black'], default=35.65)


def caption_layer(t):
    """The caption(s) on screen at t: each fades in softly; one followed by a gap fades out over 0.12 s, and one
    followed straight away by the next cross-fades into it over 0.08 s."""
    cs = [c for c in chunks() if not (c[0] > 30 and c[2][:3] == ["That's", 'the', 'black'])]   # that one is the callout
    out = []
    for n, (a, b, words, hot) in enumerate(cs):
        nxt = cs[n + 1][0] if n + 1 < len(cs) else 99.0
        joined = nxt - b < 0.05
        hot_u = [h.strip('.,?!').upper() for h in hot]
        if a <= t < b:
            age = t - a if a > 0 else 1.0          # the opening caption is already up on frame 0 (no fade)
            fo = 1.0 if joined else min(1.0, max(0.0, (b - t) / 0.12))
            out.append(ov.caption(words, hot_u, age, fo))
        elif joined and b <= t < b + 0.08:
            out.append(ov.caption(words, hot_u, 1.0, 1.0 - (t - b) / 0.08))
    if not out:
        return None
    lay = out[0]
    for extra in out[1:]:
        lay.alpha_composite(extra)
    return lay


def layers(t, you_px=None, st=None):
    """All overlay layers for VIDEO time t (full-res RGBA PIL images).  Labels on a picture event follow the story
    clock (u = st['t']); labels on a word follow the voice (t)."""
    L = []
    st = st or state(t)
    u = st['t']
    if 0.5 <= t < T_A_REAL - 0.3:
        L.append(ov.top_label('Real physics simulation', t - 0.6, fade=1.0 - seg(t, T_A_REAL - 0.8, T_A_REAL - 0.3)))
    # disk tags: BACK / FRONT pop on "This is the back half." / "And this is the front half.", go as the swing starts
    lab = st.get('labels') or {}
    t_back, t_front = back_front_times()
    if t_back <= t and u < 9.10 and lab:
        f = 1.0 - seg(u, 8.8, 9.1)
        L.append(ov.disk_tag('BACK', lab.get('back'), ov.ICE, t - t_back, f))
        if t >= t_front:
            L.append(ov.disk_tag('FRONT', lab.get('front'), ov.GOLD, t - t_front, f))
    if 10.9 <= u < 12.9:
        L.append(ov.disk_tag('BACK', (540, 470), ov.ICE, t - unwarp(10.9), 1.0 - seg(u, 12.5, 12.9)))
    # "...and under the bottom": the lower image of the disk's far side gets its own tag
    t_under = chunk_time(['and', 'under'], after=10.0, default=28.9)
    if t_under <= t and u < 16.0:
        L.append(ov.disk_tag('BACK', (540, 1080), ov.ICE, t - t_under, 1.0 - seg(u, 15.65, 16.0), size=48))
    # distance counter: counts down live through the dive and the last descent, lands on each ladder value
    cam = st['cam']
    if 15.3 <= u < T_D:
        L.append(ov.big_value(ov.distance_text(cam.r0), 'your distance \u00b7 horizon = 1\u00d7', 1.0, seg(u, 15.3, 15.6)))
    if T_D <= u < T_D + 1.35:
        L.append(ov.big_value('1.5\u00d7', 'the photon sphere', t - unwarp(T_D), fade=1.0 - seg(u, T_D + 1.05, T_D + 1.35),
                              fade_in=False))
    if 28.3 <= u < 31.9:
        L.append(ov.big_value(ov.distance_text(cam.r0), 'your distance \u00b7 horizon = 1\u00d7', 1.0, seg(u, 28.3, 28.6)))
    # "And down here, time runs slower. Stay for one minute... and half an hour goes by out there."
    # To a hovering observer at 1.001x the rest of the universe runs 1/sqrt(1 - 1/1.001) = 31.6x fast: one minute
    # here is 31.6 minutes out there.  1 MIN pops on "Stay for one minute", then counts up to 32 on "half an hour".
    t_min, t_hour, t_end = minute_times()
    if u >= 31.9 and t < t_min:
        L.append(ov.big_value('1.001\u00d7', '0.1% above the edge', t - unwarp(31.9), fade=1.0 - seg(t, t_min - 0.25, t_min),
                              fade_in=False))
    if t_min <= t < t_hour:
        L.append(ov.big_value('1', 'down here', t - t_min, unit='MIN'))
    if t_hour <= t < t_end:
        n = 1 + round(31 * _ease_out(seg(t, t_hour, t_hour + 0.9)))
        L.append(ov.big_value('%d' % n, 'out there', t - t_hour, fade=1.0 - seg(t, t_end - 0.3, t_end), fade_in=False,
                              unit='MIN'))
    # D: the black half is the black hole
    if 19.55 <= u < 22.0:
        L.append(ov.disk_tag('BLACK HOLE', (540, 1030), ov.GOLD, t - unwarp(19.55), 1.0 - seg(u, 21.7, 22.0), size=64))
    # F: LOOKING UP on "Then look up."
    t_up = chunk_time(['Then', 'look'], after=40.0, default=56.6)
    if t_up <= t < t_up + 1.6:
        L.append(ov.top_label('Looking up \u2191', t - t_up, fade=1.0 - seg(t, t_up + 1.3, t_up + 1.6), plate=True, size=64))
    # diagram tags
    if T_E <= u < T_E2:
        f = min(seg(u, T_E, T_E + 0.3), 1.0 - seg(u, T_E2 - 0.3, T_E2))
        L.append(ov.corner_tag('* diagram, not to scale', f))
        if you_px is not None and 22.5 <= u < T_E2:
            L.append(ov.point_label('you', you_px, t - unwarp(22.5), fade=1.0 - seg(u, T_E2 - 0.35, T_E2 - 0.05), dx=80, dy=-90))
    if 24.95 <= u < 26.45:
        L.append(ov.corner_tag('* magnified illustration', min(seg(u, 24.95, 25.2), 1.0 - seg(u, 26.2, 26.45))))
    # the dot's label and the black-hole callout: they stay through the pause after the last word, then fade so
    # the last frames are the clean dot of frame 0
    t_uni = chunk_time(['And', 'all', 'this'], after=40.0, default=DUR - 5.0)
    if t_uni <= t < DUR - 0.3:
        L.append(ov.point_label('the universe', dot_top(dot_tau(t)), t - t_uni, fade=1.0 - seg(t, DUR - 0.75, DUR - 0.3),
                                dx=0, dy=-130, size=56, center=True, inset=2))       # the leader touches the rim
    t_bh = black_hole_time()
    if t_bh <= t < DUR - 0.3:
        L.append(ov.callout_black(t - t_bh, fade=1.0 - seg(t, DUR - 0.75, DUR - 0.3)))
    L.append(caption_layer(t))
    return L
