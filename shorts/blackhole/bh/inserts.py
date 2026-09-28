"""Version 2's inserts: real imagery and reference cards between the simulation and the captions, each keyed to
the words that introduce it (build/words.json).

    the M87* photo    "look at this."  ...  "And up close,"   (the dot becomes the real photo, the photo the sim)
    solar system      "is this tiny circle."   a circle at true scale inside the photo
    Luminet 1979      "In 1979, Jean-Pierre Luminet drew this by hand, dot by dot."   our frame redrawn in dots
    Interstellar      "And Interstellar's black hole used the same physics."   a title card

Assets (assets/v2, licences in outputs/sources.md): the Event Horizon Telescope's M87* image (ESO/EHT, CC BY 4.0).
(Round 15: the GPS card over Apollo 17's Earth is cut with its line.)
"""
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from . import overlay as ov
from .shots import HOLE_Y, seg

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets', 'v2')
WORDS_JSON = os.path.join(HERE, '..', 'build', 'words.json')
W, H = ov.W, ov.H
CX, CY = W // 2, int(round(HOLE_Y * H))        # the dot and the photo's ring sit here
DOT_R = 282.0                                  # the dot's rim radius in frame 0 (measured)
RING_R = 495.0                                 # M87*'s ring (brightest ridge, fitted along 72 rays) in the ESO image
SOLAR = 0.112                                  # Pluto's orbit (79 AU) / the ring (42 uas at 16.8 Mpc = 705 AU)


# ---------------------------------------------------------------- word times

_WORDS = [None]


def _words():
    if _WORDS[0] is None:
        d = json.load(open(WORDS_JSON)) if os.path.exists(WORDS_JSON) else dict(words=[], chunks=[])
        _WORDS[0] = d
    return _WORDS[0]


def chunk_at(first, after=0.0, default=None):
    """Start of the first caption chunk after `after` whose first words are `first`."""
    for c in _words()['chunks']:
        if c['start'] > after and [w.strip('.,?!') for w in c['words'][:len(first)]] == first:
            return c['start']
    return default


def word_at(word, after=0.0, default=None):
    for w in _words()['words']:
        if w['s'] > after and w['w'].strip('.,?!').lower() == word.lower():
            return w['s']
    return default


def times():
    """Every insert's key times (video seconds)."""
    t_photo = word_at('this', after=3.0, default=4.3) + 0.35          # fully in (as in tools/vo_flow.py PHOTO_IN)
    t_close = chunk_at(['And', 'up', 'close'], after=10.0, default=16.3) + 0.10
    t_circle = chunk_at(['is', 'this', 'tiny'], after=5.0, default=13.5) + 0.30
    t_1979 = chunk_at(['In', '1979'], after=30.0, default=40.5) - 0.10
    t_inter = chunk_at(['And', "Interstellar's"], after=30.0, default=45.5)
    t_fly = chunk_at(['Now', "let's", 'fly'], after=30.0, default=48.9)
    return dict(photo_in0=t_photo - 0.55, photo_in1=t_photo, photo_out0=t_close, photo_out1=t_close + 0.6,
                circle=t_circle, stipple0=t_1979, stipple1=t_inter - 0.05, inter0=t_inter, inter1=t_fly - 0.15)


# ---------------------------------------------------------------- images

_CACHE = {}


def _img(name):
    if name not in _CACHE:
        _CACHE[name] = cv2.imread(os.path.join(ASSETS, name))[..., ::-1].astype(np.float32) / 255.0
    return _CACHE[name]


def _photo_frame(push):
    """The M87* photo framed so its ring lands on the dot (radius DOT_R at CX, CY), pushed in by `push`."""
    im = _img('m87_eht2019_crop.jpg')                 # ring centre at (950, 1700) in the crop (eso1907a (3700, 1980))
    k = DOT_R / RING_R * push
    M = np.float32([[k, 0, CX - 950 * k], [0, k, CY - 1700 * k]])
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    return out * 1.08


def _stipple(img, t):
    """The frame redrawn as white ink dots on black, denser where it is brighter (Luminet's 1979 way of drawing)."""
    h, w = img.shape[:2]
    step = max(2, int(round(4 * w / W)))
    lum = cv2.resize(img.mean(axis=2), (w // step, h // step), interpolation=cv2.INTER_AREA)
    lum = np.clip(lum / max(1e-3, np.percentile(lum, 99.5)), 0, 1)
    lum = 0.62 * np.clip((lum - 0.10) / 0.90, 0, 1) ** 1.1      # at most 62% ink; the dark sky stays clean paper
    rng = np.random.default_rng(1979)                  # the same dot pattern every frame: the drawing holds still
    thr = rng.random(lum.shape).astype(np.float32)
    dots = (lum > thr).astype(np.float32)
    big = cv2.resize(dots, (w, h), interpolation=cv2.INTER_NEAREST)
    big = cv2.GaussianBlur(big, (0, 0), 0.55 * w / W + 0.2)
    ink = np.clip(big * 1.25, 0, 1)
    paper = np.array([0.02, 0.02, 0.025], np.float32)
    return paper + ink[..., None] * np.array([0.93, 0.92, 0.88], np.float32)


# ---------------------------------------------------------------- text helpers (full-res RGBA layers)

def _text(lines, y, fade=1.0, plate=True):
    """Centred lines [(text, font, size, colour)] from y; a soft dark plate behind them."""
    lay = ov._layer(); d = ImageDraw.Draw(lay)
    fonts = [(t, ov.font(f, s), c) for t, f, s, c in lines]
    ys, yy = [], y
    for t, f, c in fonts:
        ys.append(yy); yy += f.size * 1.25
    if plate:
        wmax = max(f.getlength(t) for t, f, c in fonts)
        pl = ov._layer()
        ImageDraw.Draw(pl).rounded_rectangle([CX - wmax / 2 - 40, y - 26, CX + wmax / 2 + 40, yy + 10], 36, fill=ov.SHADOW + (175,))
        lay.alpha_composite(pl.filter(ImageFilter.GaussianBlur(12)))
    for (t, f, c), yl in zip(fonts, ys):
        d.text((CX - f.getlength(t) / 2, yl), t, font=f, fill=c + (255,))
    lay = ov._shadowed(lay, 6, (0, 3), 0.8)
    return ov._pop(lay, 1.0, fade, (CX, y))


def _credit(text, fade=1.0):
    """Small attribution, bottom right but clear of the bottom 20% and the button column."""
    f = ov.font('Inter-ExtraBold.ttf', 26)
    lay = ov._layer(); d = ImageDraw.Draw(lay)
    x = 0.86 * W - f.getlength(text)
    d.text((x, 0.775 * H), text, font=f, fill=(215, 218, 226, 210))
    return ov._pop(ov._shadowed(lay, 4, (0, 2), 0.8), 1.0, fade, (0, 0))


def _circle(r, age, fade):
    """Pluto's orbit at M87*'s scale, with its label."""
    k = ov._ease_out(age / 0.3)
    lay = ov._layer(); d = ImageDraw.Draw(lay)
    rr = r * (0.6 + 0.4 * k) + 18 * math.exp(-age / 0.25) * k                      # a small overshoot pop
    d.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], outline=ov.GOLD + (255,), width=6)
    d.ellipse([CX - 4, CY - 4, CX + 4, CY + 4], fill=ov.GOLD + (255,))           # the Sun
    d.line([(CX, CY - rr - 8), (CX, CY - 150)], fill=ov.GOLD + (230,), width=3)          # leader up to the label
    f1 = ov.font('Montserrat-Black.ttf', 52); f2 = ov.font('Inter-ExtraBold.ttf', 32)
    for txt, f, c, y in (('OUR SOLAR SYSTEM', f1, ov.GOLD, CY - 250), ("(PLUTO'S ORBIT, TO SCALE)", f2, ov.WHITE, CY - 196)):
        d.text((CX - f.getlength(txt) / 2, y), txt, font=f, fill=c + (255,))
    return ov._pop(ov._glow(ov._shadowed(lay, 8, (0, 3), 0.9), ov.GOLD, 10, 0.6), 1.0, fade * ov._smooth(age / 0.2), (CX, CY))


# ---------------------------------------------------------------- the pass

def apply(img, t):
    """img: float RGB (h, w, 3), the rendered frame; returns it with the inserts for video time t."""
    T = times()
    h, w = img.shape[:2]
    layers = []
    # the M87* photo, between the dot and the simulation
    if T['photo_in0'] <= t < T['photo_out1']:
        a = min(ov._smooth(seg(t, T['photo_in0'], T['photo_in1'])), 1.0 - ov._smooth(seg(t, T['photo_out0'], T['photo_out1'])))
        push = 1.0 + 0.05 * seg(t, T['photo_in0'], T['photo_out1'])
        ph = _photo_frame(push)
        if (w, h) != (W, H):
            ph = cv2.resize(ph, (w, h), interpolation=cv2.INTER_AREA)
        img = img * (1 - a) + ph * a
        f = a
        layers.append(_text([('FIRST PHOTO OF A BLACK HOLE', 'Montserrat-Black.ttf', 58, ov.WHITE),
                             ('M87* · EVENT HORIZON TELESCOPE · 2019', 'Inter-ExtraBold.ttf', 34, ov.ICE)], 230, f))
        layers.append(_credit('Image: EHT Collaboration, CC BY 4.0', f))
        if t >= T['circle']:
            layers.append(_circle(DOT_R * push * SOLAR, t - T['circle'], f))
    # Luminet, 1979: our frame, redrawn in dots
    if T['stipple0'] <= t < T['stipple1']:
        a = min(ov._smooth(seg(t, T['stipple0'], T['stipple0'] + 0.4)), 1.0 - ov._smooth(seg(t, T['stipple1'] - 0.4, T['stipple1'])))
        img = img * (1 - a) + _stipple(img, t) * a
        layers.append(_text([('1979 · JEAN-PIERRE LUMINET', 'Montserrat-Black.ttf', 54, ov.WHITE),
                             ('THE FIRST PICTURE OF THIS, COMPUTED', 'Inter-ExtraBold.ttf', 32, ov.ICE),
                             ('ON AN IBM 7040 AND DRAWN BY HAND', 'Inter-ExtraBold.ttf', 32, ov.ICE),
                             ('* OUR SIMULATION, REDRAWN IN DOTS HIS WAY', 'Inter-ExtraBold.ttf', 26, (200, 204, 214))], 200, a))
    # Interstellar
    if T['inter0'] <= t < T['inter1']:
        a = min(ov._smooth(seg(t, T['inter0'], T['inter0'] + 0.3)), 1.0 - ov._smooth(seg(t, T['inter1'] - 0.3, T['inter1'])))
        layers.append(_text([('INTERSTELLAR (2014)', 'Montserrat-Black.ttf', 60, ov.GOLD),
                             ("ITS BLACK HOLE WAS RENDERED", 'Inter-ExtraBold.ttf', 32, ov.WHITE),
                             ("FROM KIP THORNE'S EQUATIONS", 'Inter-ExtraBold.ttf', 32, ov.WHITE)], 200, a))
    if layers:
        img = ov.composite(img, layers)
    return img


def cue_times():
    """Moments for sound effects (tools/mix.py)."""
    T = times()
    return dict(PHOTO_IN=T['photo_in1'] - 0.15, PHOTO_OUT=T['photo_out0'] + 0.3, CIRCLE=T['circle'],
                STIPPLE=T['stipple0'] + 0.2, INTERSTELLAR=T['inter0'])
