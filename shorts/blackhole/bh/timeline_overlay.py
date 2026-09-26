"""Which overlays are on screen at time t.  Captions come from build/words.json (TTS alignment) when it
exists, else from the planned timings below.  Line text uses '|' for chunk breaks and '*' for gold words."""
import json
import math
import os

from . import overlay as ov
from .shots import T_A, T_B, T_C, T_D, T_E, T_F, T_G, BAR, DUR, state, seg

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_JSON = os.path.join(HERE, '..', 'build', 'words.json')

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
        return [(c['start'], c['end'], c['words'], c.get('hot', [])) for c in data['chunks']]
    out = []
    for a, b, text in LINES:
        cs = parse(text)
        n = sum(len(c) for c in cs); dt = (b - a) / n; i = 0
        for c in cs:
            out.append((a + i * dt, a + (i + len(c)) * dt + (0.35 if c is cs[-1] else 0), [w for w, _ in c], [w for w, h in c if h]))
            i += len(c)
    return out


def caption_layer(t):
    for a, b, words, hot in chunks():
        if a >= 34.5:          # "Black hole." is shown as a callout into the black, not as a caption under the dot
            continue
        if a <= t < b:
            return ov.caption(words, [h.strip('.,?!').upper() for h in hot], t - a)
    return None


def layers(t, you_px=None, st=None):
    """All overlay layers for time t (full-res RGBA PIL images)."""
    L = []
    st = st or state(t)
    if 0.5 <= t < 2.55:
        L.append(ov.top_label('Real physics simulation', t - 0.6, fade=1.0 - seg(t, 2.25, 2.55)))
    # disk tags
    lab = st.get('labels') or {}
    if 7.10 <= t < 9.10 and lab:
        f = 1.0 - seg(t, 8.8, 9.1)
        L.append(ov.disk_tag('BACK', lab.get('back'), ov.ICE, t - 7.10, f))
        if t >= 7.30:
            L.append(ov.disk_tag('FRONT', lab.get('front'), ov.GOLD, t - 7.30, f))
    if 10.9 <= t < 12.9:
        f = 1.0 - seg(t, 12.5, 12.9)
        L.append(ov.disk_tag('BACK', (540, 470), ov.ICE, t - 10.9, f))
        if t >= 11.15:
            L.append(ov.disk_tag('BACK', (540, 1080), ov.ICE, t - 11.15, f, size=48))
    # depth gauge
    if 15.0 <= t < T_E or T_F <= t < 33.9:
        if t < T_E:
            fade = min(seg(t, 15.0, 15.5), 1.0 - seg(t, T_E - 0.3, T_E))
        else:
            fade = min(seg(t, T_F, T_F + 0.3), 1.0 - seg(t, 33.3, 33.9))
        cam = st['cam']
        r = cam.r0 if cam is not None else 1.5
        hot = '1.5\u00d7' if T_D <= t < T_E else ('HORIZON' if t >= 30.0 else None)
        L.append(ov.gauge(r, fade, hot))
    # ladder values
    if T_D <= t < T_D + 1.35:
        L.append(ov.big_value('1.5\u00d7', 'the photon sphere', t - T_D, fade=1.0 - seg(t, T_D + 1.05, T_D + 1.35)))
    if 26.95 <= t < 27.95:
        L.append(ov.top_label('Looking up \u2191', t - 26.95, fade=1.0 - seg(t, 27.65, 27.95)))
    if 28.2 <= t < 29.6:
        L.append(ov.big_value('1.001\u00d7', '0.1% above the edge', t - 28.2, fade=1.0 - seg(t, 29.3, 29.6)))
    # diagram tags
    if T_E <= t < T_F:
        f = min(seg(t, T_E, T_E + 0.3), 1.0 - seg(t, T_F - 0.3, T_F))
        L.append(ov.corner_tag('* diagram, not to scale', f))
        if you_px is not None and 22.5 <= t < 26.3:
            L.append(ov.point_label('you', you_px, t - 22.5, fade=1.0 - seg(t, 26.0, 26.3), dx=80, dy=-90))
    # the dot's label
    if 32.1 <= t < 33.2:
        L.append(ov.point_label('starlight: 30\u00d7 bluer', (540, 806 + 250), t - 32.1,
                                fade=1.0 - seg(t, 32.9, 33.2), dx=-205, dy=0, size=38, line=False))
    if 33.3 <= t < 36.8:
        L.append(ov.point_label('the universe', (540, 806 - 225), t - 33.3, fade=1.0 - seg(t, 36.4, 36.8),
                                dx=-150, dy=-120, size=46))
    if 34.9 <= t < 36.8:
        L.append(ov.callout_black(t - 34.9, fade=1.0 - seg(t, 36.4, 36.8)))
    L.append(caption_layer(t))
    return L
