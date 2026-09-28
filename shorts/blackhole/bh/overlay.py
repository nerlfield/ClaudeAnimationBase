"""Captions, labels and the distance counter, composited over a finished (display-referred) frame.

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
CAP_MAXW = 780


@lru_cache(maxsize=32)
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def _ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def _smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


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


def caption(words, hot=(), age=1.0, out=1.0):
    """One caption chunk (a whole phrase), at most two lines; the font shrinks to fit rather than wrapping to 3."""
    words = [w.upper() for w in words]
    size = CAP_SIZE
    while True:
        f = font('Montserrat-Black.ttf', size)
        lines = _wrap(f, words, CAP_MAXW)
        if len(lines) <= 2 or size <= 60:
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
    # a soft arrival: fade in over 0.12 s while settling from 96.5% scale, no overshoot; `out` fades it away
    k = _ease_out(age / 0.18)
    alpha = _smooth(age / 0.12) * out
    return _pop(lay, 0.965 + 0.035 * k, alpha, (W // 2, CAP_Y - size // 3))


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


def top_label(text, age=1.0, fade=1.0, size=50):
    """Letter-spaced label near the top, e.g. REAL PHYSICS SIMULATION."""
    f = font('Inter-ExtraBold.ttf', size)
    lay = _layer(); d = ImageDraw.Draw(lay)
    spaced = text.upper()
    tw = f.getlength(spaced) + 3.0 * len(spaced)
    x = W / 2 - tw / 2; y = 236
    for ch in spaced:
        d.text((x, y), ch, font=f, fill=WHITE + (225,))
        x += f.getlength(ch) + 3.0
    d.line([(W / 2 - 70, y + size + 28), (W / 2 + 70, y + size + 28)], fill=ICE + (220,), width=5)
    lay = _shadowed(lay, 6, (0, 3), 0.8)
    return _pop(lay, 1.0, min(1.0, age / 0.25) * fade, (W // 2, y))


def big_value(value, sub, age=1.0, fade=1.0, y=262, fade_in=True, unit=''):
    """The ladder's giant label: e.g. 1.5x with a sub-label, and an optional smaller unit after the number
    ("1 MIN").  Digits sit in fixed-width cells so a live count (the distance counter) doesn't jitter; age
    restarts the pop when the value lands."""
    fv = font('Montserrat-Black.ttf', 190); fs = font('Inter-ExtraBold.ttf', 44); fu = font('Montserrat-Black.ttf', 96)
    lay = _layer(); d = ImageDraw.Draw(lay)
    cell = max(fv.getlength(c) for c in '0123456789')
    adv = [cell if c.isdigit() else fv.getlength(c) for c in value]
    uw = fu.getlength(unit) + 22 if unit else 0.0
    x = W / 2 - (sum(adv) + uw) / 2
    for c, a in zip(value, adv):
        d.text((x + (a - fv.getlength(c)) / 2, y - 150), c, font=fv, fill=ICE + (255,)); x += a
    if unit:
        d.text((x + 22, y - 150 + fv.getmetrics()[0]), unit, font=fu, fill=ICE + (255,), anchor='ls')
    adv = adv + [uw]
    sw = fs.getlength(sub.upper()) + 2.0 * len(sub)
    x = W / 2 - sw / 2
    for ch in sub.upper():
        d.text((x, y + 70), ch, font=fs, fill=WHITE + (240,)); x += fs.getlength(ch) + 2.0
    # (round 15: no dark backing behind it; the glow and the drop shadow carry it)
    lay = _glow(lay, ICE, 22, 0.55)
    lay = _shadowed(lay, 10, (0, 5), 0.85)
    k = _ease_out(age / 0.25)
    # a value that lands in place of the live counter settles without fading in (no one-frame dip)
    return _pop(lay, 0.94 + 0.06 * k, (_smooth(age / 0.18) if fade_in else 1.0) * fade, (W // 2, y))


def distance_text(r):
    """The counter's reading, in horizon radii, with more decimals the closer you get."""
    if r >= 9.95:
        return '%d\u00d7' % round(r)
    if r >= 1.995:
        return '%.1f\u00d7' % r
    if r >= 1.1:
        return '%.2f\u00d7' % r
    return '%.3f\u00d7' % max(r, 1.001)


def point_label(text, at, age=1.0, fade=1.0, dx=34, dy=-60, size=40, color=ICE, line=True, center=False, inset=10):
    """A small label with a leader line to a screen point.  The label's left edge (or, with center=True, its
    centre) sits dx, dy from the point; the leader runs from the point to the nearest edge of the lettering and
    stops short of it (it used to end at the label's left end, and cut through the first letter).  inset: how far
    from the point the leader starts."""
    if at is None:
        return None
    f = font('Inter-ExtraBold.ttf', size)
    lay = _layer(); d = ImageDraw.Draw(lay)
    ax, ay = at
    tx, ty = ax + dx, ay + dy
    if center:
        tx -= f.getlength(text.upper()) / 2
    x0, y0, x1, y1 = d.textbbox((tx, ty - size * 0.1), text.upper(), font=f)
    if line:
        gap = 12
        px, py = min(max(ax, x0 - gap), x1 + gap), min(max(ay, y0 - gap), y1 + gap)
        L = math.hypot(px - ax, py - ay) or 1.0
        d.line([(ax + (px - ax) / L * inset, ay + (py - ay) / L * inset), (px, py)], fill=color + (230,), width=4)
    d.text((tx, ty - size * 0.1), text.upper(), font=f, fill=color + (255,))
    lay = _shadowed(lay, 6, (0, 3), 0.85)
    return _pop(lay, 1.0, _smooth(age / 0.25) * fade, (int(tx), int(ty)))


def disk_tag(text, at, color, age=1.0, fade=1.0, size=64):
    """A bold tag sitting on part of the disk (BACK / FRONT)."""
    if at is None:
        return None
    f = font('Montserrat-Black.ttf', size)
    lay = _layer(); d = ImageDraw.Draw(lay)
    tw = f.getlength(text)
    d.text((at[0] - tw / 2, at[1] - 40), text, font=f, fill=color + (255,), stroke_width=3, stroke_fill=SHADOW + (170,))
    lay = _shadowed(lay, 10, (0, 5), 0.85)
    k = _ease_out(age / 0.25)
    return _pop(lay, 0.9 + 0.1 * k, _smooth(age / 0.18) * fade, (int(at[0]), int(at[1])))


def callout_black(age=1.0, fade=1.0, y=1250):
    """BLACK HOLE, with four arrows pointing out into the surrounding black (not at the dot)."""
    f = font('Montserrat-Black.ttf', 88)
    lay = _layer(); d = ImageDraw.Draw(lay)
    text = 'BLACK HOLE'
    tw = f.getlength(text)
    d.text((W / 2 - tw / 2, y - 55), text, font=f, fill=GOLD + (255,), stroke_width=3, stroke_fill=SHADOW + (160,))
    x0 = W / 2 + tw / 2 + 16
    reach = min(115.0, 0.86 * W - x0)                      # keep the right arrows out of the button column
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax, ay = W / 2 + sx * (tw / 2 + 16), y - 12 + sy * 42
            bx, by = ax + sx * reach, ay + sy * reach
            d.line([(ax, ay), (bx, by)], fill=GOLD + (235,), width=7)
            ang = math.atan2(by - ay, bx - ax)
            for da in (2.55, -2.55):
                d.line([(bx, by), (bx + 34 * math.cos(ang + da), by + 34 * math.sin(ang + da))], fill=GOLD + (235,), width=7)
    lay = _shadowed(lay, 10, (0, 5), 0.85)
    k = _ease_out(age / 0.25)
    return _pop(lay, 0.95 + 0.05 * k, _smooth(age / 0.18) * fade, (W // 2, y))


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
