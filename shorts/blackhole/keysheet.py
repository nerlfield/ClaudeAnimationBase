"""Render key stills (full res, final look, captions) and assemble a labelled sheet.

    python keysheet.py --out ../../outputs/storyboard_sheet.jpg 1.2:A 5.9:B 9.0:B 14.8:C 17.4:D 21.45:E 30.8:F 34.9:G
"""
import argparse
import os
import time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

from bh import video
from bh.frame import SPP4

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('keys', nargs='+', help='time:label pairs')
    ap.add_argument('--out', required=True)
    ap.add_argument('--stills', default=os.path.join(HERE, 'build', 'stills'))
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--cols', type=int, default=4)
    ap.add_argument('--tile', type=int, default=405)
    a = ap.parse_args()
    os.makedirs(a.stills, exist_ok=True)
    tiles = []
    for k in a.keys:
        t, lab = k.split(':')
        t = float(t)
        t0 = time.time()
        img = video.frame(t, a.scale, SPP4)
        p = os.path.join(a.stills, f'key_{t:05.2f}_{lab}.jpg')
        cv2.imwrite(p, (img[..., ::-1] * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 93])
        print(f'{lab} t={t} {time.time() - t0:.1f}s -> {p}', flush=True)
        tiles.append((t, lab, p))
    tw = a.tile; th = int(tw * 16 / 9)
    rows = (len(tiles) + a.cols - 1) // a.cols
    pad, head = 14, 58
    sheet = Image.new('RGB', (a.cols * (tw + pad) + pad, rows * (th + head + pad) + pad), (14, 15, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'assets', 'fonts', 'Inter-ExtraBold.ttf'), 30)
    for i, (t, lab, p) in enumerate(tiles):
        x = pad + (i % a.cols) * (tw + pad); y = pad + (i // a.cols) * (th + head + pad)
        im = Image.open(p).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y + head))
        m, s = divmod(t, 60)
        d.text((x + 4, y + 12), f'{lab}  {int(m):01d}:{s:05.2f}', font=f, fill=(255, 194, 74))
    sheet.save(a.out, quality=92)
    print('sheet ->', a.out)


if __name__ == '__main__':
    main()
