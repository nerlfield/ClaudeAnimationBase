"""The Short's cover: the glowing dot from the video's first frame, big, with THE ENTIRE UNIVERSE and an arrow to it.

    python tools/thumbnail.py        # -> outputs/thumbnail.jpg (1080 x 1920) and a phone-size preview

It says the title's claim in other words (YouTube shows the title under the cover), keeps every mark out of the bottom
20% (where the Shorts shelf lays the title over the cover), and leaves the black around the dot empty: that black is
the answer the video gives.  The design is centred on the image (y 400-1530) so a preview that crops the top and
bottom, down to a 4:5 centre crop, still shows all of it.
"""
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from bh import overlay as ov  # noqa: E402

W, H = ov.W, ov.H
FRAME = os.path.join(HERE, '..', 'build', 'base', '02539.png')     # the clean dot the video opens and loops on
OUT = os.path.join(HERE, '..', '..', '..', 'outputs', 'thumbnail.jpg')
DOT = (540, 806, 300)          # the dot in the frame: centre and a radius that takes in its glow
DOT_R = 278                    # the dot's visible radius in the frame
CENTRE, SCALE = (540, 1180), 1.18
TEXT_Y = 400                   # top of THE ENTIRE


def dot_layer():
    """The dot, scaled up onto black, with a little extra bloom so it reads at feed size."""
    img = cv2.imread(FRAME)[..., ::-1].astype(np.float32) / 255.0
    cx, cy, r = DOT
    crop = img[cy - r:cy + r, cx - r:cx + r]
    n = int(round(2 * r * SCALE))
    crop = cv2.resize(crop, (n, n), interpolation=cv2.INTER_CUBIC)
    yy, xx = np.mgrid[0:n, 0:n]
    fall = np.clip((n / 2 - np.hypot(xx - n / 2, yy - n / 2)) / (0.12 * n), 0, 1)[..., None]   # soft edge into black
    out = np.zeros((H, W, 3), np.float32)
    x0, y0 = CENTRE[0] - n // 2, CENTRE[1] - n // 2
    out[y0:y0 + n, x0:x0 + n] = crop * fall
    bloom = cv2.GaussianBlur(out, (0, 0), 38)
    out = 1 - (1 - out) * (1 - 0.45 * bloom)                    # screen a little bloom over it
    return np.clip(out, 0, 1)


def text_layer():
    lay = ov._layer(); d = ImageDraw.Draw(lay)
    f1 = ov.font('Montserrat-Black.ttf', 108)
    f2 = ov.font('Montserrat-Black.ttf', 162)
    for txt, f, col, y in (('THE ENTIRE', f1, ov.WHITE, TEXT_Y), ('UNIVERSE', f2, ov.GOLD, TEXT_Y + 106)):
        d.text((W / 2 - f.getlength(txt) / 2, y), txt, font=f, fill=col + (255,))
    lay = ov._glow(lay, ov.GOLD, 26, 0.35)
    return ov._shadowed(lay, 14, (0, 8), 0.95)


def arrow_layer():
    """A hand-drawn-looking arrow from under UNIVERSE, curving down onto the dot's rim."""
    lay = ov._layer(); d = ImageDraw.Draw(lay)
    r = DOT_R * SCALE + 45                                       # ends just outside the rim, up and to the right
    p2 = (CENTRE[0] + r * math.cos(math.radians(50)), CENTRE[1] - r * math.sin(math.radians(50)))
    p0, p1 = (p2[0], TEXT_Y + 296), (p2[0] + 125, TEXT_Y + 400)  # quadratic Bezier from under UNIVERSE
    pts = []
    for k in range(41):
        s = k / 40
        pts.append(((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * p1[0] + s * s * p2[0],
                    (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * p1[1] + s * s * p2[1]))
    d.line(pts, fill=ov.GOLD + (255,), width=18, joint='curve')
    ax, ay = pts[-1]; bx, by = pts[-4]
    ang = math.atan2(ay - by, ax - bx)
    tip = (ax + 22 * math.cos(ang), ay + 22 * math.sin(ang))
    head = [tip] + [(tip[0] - 70 * math.cos(ang + s * 0.5), tip[1] - 70 * math.sin(ang + s * 0.5)) for s in (1, -1)]
    d.polygon(head, fill=ov.GOLD + (255,))
    return ov._shadowed(ov._glow(lay, ov.GOLD, 18, 0.45), 12, (0, 6), 0.9)


def main():
    base = dot_layer()
    img = ov.composite(base, [text_layer(), arrow_layer()])
    im = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8))
    im.save(OUT, quality=93, optimize=True)
    im.resize((180, 320), Image.LANCZOS).save(os.path.join(os.path.dirname(OUT), '..', 'shorts', 'blackhole', 'build',
                                                          'check', 'thumb_small.png'))
    print('->', os.path.relpath(OUT), '%.0f KB' % (os.path.getsize(OUT) / 1024))


if __name__ == '__main__':
    main()
