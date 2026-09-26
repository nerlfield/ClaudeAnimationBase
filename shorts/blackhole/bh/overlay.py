"""Captions, labels and the depth gauge, composited over a finished (display-referred) frame.

All text is drawn at full resolution with PIL and scaled if the frame is smaller.  Styles follow
research.md: heavy geometric sans, white with a soft dark shadow, one key word in gold.
"""
import os
import math
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'assets', 'fonts')
W, H = 1080, 1920

WHITE = (246, 244, 238)
GOLD = (255, 194, 74)        # #FFC24A
ICE = (143, 195, 255)        # #8FC3FF
SHADOW = (5, 7, 13)          # #05070D

CAP_SIZE = 80                # Montserrat Black at 80 px -> cap height ~56 px (2.9% of 1920)
CAP_Y = int(0.69 * H)        # caption baseline
CAP_MAXW = 800


@lru_cache(maxsize=32)
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def _ease_back(x, s=1.4):
    x = min(1.0, max(0.0, x)) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


def _layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def _shadowed(layer, blur=10, offset=(0, 5), opacity=0.8):
    """Soft dark drop shadow under a text layer."""
    a = layer.split()[3]
    sh = Image.new('RGBA', layer.size, SHADOW + (0,))
    sh.putalpha(a.point(lambda v: int(v * opacity)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = _layer()
    out.alpha_composite(sh, (offset[0], offset[1]))
    out.alpha_composite(layer)
    return out


def _glow(layer, color, blur=18, amount=0.9):
    a = layer.split()[3]
    g = Image.new('RGBA', layer.size, color + (0,))
    g.putalpha(a.point(lambda v: int(v * amount)))
    g = g.filter(ImageFilter.GaussianBlur(blur))
    out = _layer()
    out.alpha_composite(g)
    out.alpha_composite(layer)
    return out


def _wrap(f, words, maxw):
    space = f.getlength(' ')
    lines, cur, cw = [], [], 0.0
    for w in words:
        wl = f.getlength(w)
        if cur and cw + space + wl > maxw:
            lines.append(cur); cur, cw = [], 0.0
        cur.append(w); cw += (space if len(cur) > 1 else 0) + wl
    if cur:
        lines.append(cur)
    return lines


def caption(words, hot=(), age=1.0):
    """One caption chunk (a whole phrase), at most two lines; the font shrinks to fit rather than wrapping to 3."""
    words = [w.upper() for w in words]
    size = CAP_SIZE
    while True:
        f = font('Montserrat-Black.ttf', size)
        lines = _wrap(f, words, CAP_MAXW)
        if len(lines) <= 2 or size <= 66:
            break
        size -= 4
    if len(lines) == 2:                               # balance the two lines
        best = None
        for k in range(1, len(words)):
            a, b = ' '.join(words[:k]), ' '.join(words[k:])
            wa, wb = f.getlength(a), f.getlength(b)
            if max(wa, wb) <= CAP_MAXW and (best is None or abs(wa - wb) < best[0]):
                best = (abs(wa - wb), k)
        if best:
            lines = [words[:best[1]], words[best[1]:]]
    space = f.getlength(' ')
    lay = _layer(); d = ImageDraw.Draw(lay)
    lh = int(size * 1.08)
    y0 = CAP_Y - lh * (len(lines) - 1) - int(size * 0.78)
    hotset = {h.upper() for h in hot}
    for li, ln in enumerate(lines):
        total = sum(f.getlength(w) for w in ln) + space * (len(ln) - 1)
        x = W / 2 - total / 2
        for w in ln:
            col = GOLD if w.strip('.,?!') in hotset else WHITE
            d.text((x, y0 + li * lh), w, font=f, fill=col + (255,), stroke_width=3, stroke_fill=SHADOW + (150,))
            x += f.getlength(w) + space
    lay = _shadowed(lay, blur=12, offset=(0, 6), opacity=0.85)
    k = _ease_back(age / 0.12) if age < 0.12 else 1.0
    alpha = min(1.0, age / 0.06)
    return _pop(lay, k * 0.08 + 0.92, alpha, (W // 2, CAP_Y - size // 3))


def _pop(lay, scale, alpha, center):
    if abs(scale - 1.0) > 1e-3:
        cw, ch = int(W * scale), int(H * scale)
        big = lay.resize((cw, ch), Image.BICUBIC)
        out = _layer()
        out.alpha_composite(big, (int(center[0] - center[0] * scale), int(center[1] - center[1] * scale)))
        lay = out
    if alpha < 1.0:
        a = lay.split()[3].point(lambda v: int(v * alpha))
        lay.putalpha(a)
    return lay


def top_label(text, age=1.0, fade=1.0):
    """Letter-spaced label near the top, e.g. REAL PHYSICS SIMULATION."""
    f = font('Inter-ExtraBold.ttf', 56)
    lay = _layer(); d = ImageDraw.Draw(lay)
    spaced = text.upper()
    tw = f.getlength(spaced) + 3.0 * len(spaced)
    x = W / 2 - tw / 2; y = 236
    for ch in spaced:
        d.text((x, y), ch, font=f, fill=WHITE + (225,))
        x += f.getlength(ch) + 3.0
    d.line([(W / 2 - 70, y + 78), (W / 2 + 70, y + 78)], fill=ICE + (220,), width=5)
    lay = _shadowed(lay, 6, (0, 3), 0.8)
    return _pop(lay, 1.0, min(1.0, age / 0.25) * fade, (W // 2, y))


def corner_tag(text, fade=1.0):
    f = font('Inter-ExtraBold.ttf', 26)
    lay = _layer(); d = ImageDraw.Draw(lay)
    d.text((64, 214), text.upper(), font=f, fill=(210, 214, 224, 200))
    return _pop(_shadowed(lay, 5, (0, 2), 0.8), 1.0, fade, (0, 0))


def big_value(value, sub, age=1.0, fade=1.0, y=262):
    """The ladder's giant label: e.g. 1.5x with a small sub-label."""
    fv = font('Montserrat-Black.ttf', 190); fs = font('Inter-ExtraBold.ttf', 36)
    lay = _layer(); d = ImageDraw.Draw(lay)
    tw = fv.getlength(value)
    d.text((W / 2 - tw / 2, y - 150), value, font=fv, fill=ICE + (255,))
    sw = fs.getlength(sub.upper()) + 2.0 * len(sub)
    x = W / 2 - sw / 2
    for ch in sub.upper():
        d.text((x, y + 70), ch, font=fs, fill=WHITE + (235,)); x += fs.getlength(ch) + 2.0
    lay = _glow(lay, ICE, 22, 0.55)
    lay = _shadowed(lay, 10, (0, 5), 0.8)
    k = _ease_back(age / 0.16) if age < 0.16 else 1.0
    return _pop(lay, 0.85 + 0.15 * k, min(1.0, age / 0.08) * fade, (W // 2, y))


def point_label(text, at, age=1.0, fade=1.0, dx=34, dy=-60, size=40, color=ICE, line=True):
    """A small label with a leader line to a screen point."""
    if at is None:
        return None
    f = font('Inter-ExtraBold.ttf', size)
    lay = _layer(); d = ImageDraw.Draw(lay)
    ax, ay = at
    tx, ty = ax + dx, ay + dy
    if line:
        L = math.hypot(dx, dy) or 1.0
        d.line([(ax + dx / L * 10, ay + dy / L * 10), (tx - 4, ty + size * 0.55)], fill=color + (230,), width=4)
    d.text((tx, ty - size * 0.1), text.upper(), font=f, fill=color + (255,))
    lay = _shadowed(lay, 6, (0, 3), 0.85)
    return _pop(lay, 1.0, min(1.0, age / 0.15) * fade, (int(tx), int(ty)))


# gauge: depth ladder on the left edge, sqrt-log scale in distance from the centre (r_s units)
G_X = 150
G_TOP, G_BOT = 430, 1000
TICKS = [(25.0, '25\u00d7'), (10.0, '10\u00d7'), (3.0, '3\u00d7'), (1.5, '1.5\u00d7'), (1.0, '1\u00d7 = HORIZON')]


def gauge_y(r):
    """sqrt-log scale: spreads the last stretch above the horizon so the final descent is visible."""
    f = math.sqrt(max(0.0, math.log(max(r, 1.0))) / math.log(26.0))
    return G_BOT - min(1.0, f) * (G_BOT - G_TOP)


def gauge(r, fade=1.0, hot=None):
    f = font('Inter-ExtraBold.ttf', 34); fy = font('Inter-ExtraBold.ttf', 32); ft = font('Inter-ExtraBold.ttf', 30)
    fs = font('Inter-ExtraBold.ttf', 22)
    lay = _layer(); d = ImageDraw.Draw(lay)
    d.text((G_X - 96, G_TOP - 78), 'YOUR DISTANCE', font=ft, fill=(240, 240, 245, 235))
    d.line([(G_X, G_TOP - 18), (G_X, G_BOT)], fill=(220, 225, 235, 160), width=4)
    for rv, lab in TICKS:
        y = gauge_y(rv)
        big = rv == 1.0
        d.line([(G_X - 12, y), (G_X + 12, y)], fill=(230, 232, 240, 220), width=6 if big else 4)
        col = (240, 240, 245, 235) if lab != hot else GOLD + (255,)
        d.text((G_X + 22, y - 20), lab, font=f, fill=col)
    # YOU marker sits left of the line so it never covers a label; it stays visibly above the horizon
    y = min(gauge_y(r), G_BOT - 22) if r > 1.0 else G_BOT
    d.polygon([(G_X - 10, y), (G_X - 30, y - 13), (G_X - 30, y + 13)], fill=ICE + (255,))
    d.text((G_X - 108, y - 19), 'YOU', font=fy, fill=ICE + (255,))
    lay = _glow(lay, ICE, 8, 0.35)
    lay = _shadowed(lay, 5, (0, 2), 0.9)
    return _pop(lay, 1.0, fade, (0, 0))


def disk_tag(text, at, color, age=1.0, fade=1.0, size=64):
    """A bold tag sitting on part of the disk (BACK / FRONT)."""
    if at is None:
        return None
    f = font('Montserrat-Black.ttf', size)
    lay = _layer(); d = ImageDraw.Draw(lay)
    tw = f.getlength(text)
    d.text((at[0] - tw / 2, at[1] - 40), text, font=f, fill=color + (255,), stroke_width=3, stroke_fill=SHADOW + (170,))
    lay = _shadowed(lay, 10, (0, 5), 0.85)
    k = _ease_back(age / 0.14) if age < 0.14 else 1.0
    return _pop(lay, 0.8 + 0.2 * k, min(1.0, age / 0.07) * fade, (int(at[0]), int(at[1])))


def callout_black(age=1.0, fade=1.0, y=1250):
    """BLACK HOLE, with arrows pointing out into the surrounding black (not at the dot)."""
    f = font('Montserrat-Black.ttf', 96)
    lay = _layer(); d = ImageDraw.Draw(lay)
    text = 'BLACK HOLE'
    tw = f.getlength(text)
    d.text((W / 2 - tw / 2, y - 60), text, font=f, fill=GOLD + (255,), stroke_width=3, stroke_fill=SHADOW + (160,))
    # four arrows pointing outward, away from the dot, into the black
    for (x0, y0, x1, y1) in [(W / 2 - tw / 2 - 16, y + 10, 90, y + 300), (W / 2 + tw / 2 + 16, y + 10, W - 170, y + 300),
                             (W / 2 - tw / 2 - 16, y - 40, 70, y - 150)]:
        d.line([(x0, y0), (x1, y1)], fill=GOLD + (230,), width=6)
        ang = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            d.line([(x1, y1), (x1 + 34 * math.cos(ang + da), y1 + 34 * math.sin(ang + da))], fill=GOLD + (230,), width=6)
    lay = _shadowed(lay, 10, (0, 5), 0.85)
    k = _ease_back(age / 0.16) if age < 0.16 else 1.0
    return _pop(lay, 0.9 + 0.1 * k, min(1.0, age / 0.08) * fade, (W // 2, y))


def composite(img, layers):
    """img: float (h, w, 3) in 0..1.  layers: list of RGBA PIL images at full res (or None)."""
    layers = [l for l in layers if l is not None]
    if not layers:
        return img
    base = _layer()
    for l in layers:
        base.alpha_composite(l)
    h, w = img.shape[:2]
    if (w, h) != (W, H):
        base = base.resize((w, h), Image.LANCZOS)
    a = np.asarray(base, np.float32) / 255.0
    return img * (1 - a[..., 3:4]) + a[..., :3] * a[..., 3:4]
