"""Render frames, review strips and the final video.

    python render.py strip 0:5.33 --step 0.1 --scale 0.25 --out build/check/strip.jpg   # every 0.1 s
    python render.py sheet 0.1,2.6,2.7 --scale 0.4 --out build/check/sheet.jpg            # chosen times
    python render.py base 0:1120 [--scale 1]                                                # physics frames, no text, resumable
    python render.py composite 0:1120                                                       # base + captions/labels -> frames
    python render.py encode --out build/video_noaudio.mp4                                  # frames -> mp4
"""
import argparse
import os
import sys
import time
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

from bh import video, shots
from bh.frame import SPP4, SPP9

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, 'build', 'frames')
BASE = os.path.join(HERE, 'build', 'base')


def mb_for(t):
    """Motion-blur sub-samples by shot: more where the camera moves fast."""
    if shots.T_C <= t < shots.T_D:
        return 3
    if 8.6 <= t < 10.8 or shots.T_B <= t < 7.2 or shots.T_F <= t < 29.6 or 26.0 <= t < shots.T_F:
        return 2
    if shots.T_A - 0.12 <= t < shots.T_A + 0.12:
        return 1
    return 1


def grid(images, labels, cols, out, tile_w):
    th = int(tile_w * 16 / 9); pad, head = 6, 26
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tile_w + pad) + pad, rows * (th + head + pad) + pad), (14, 15, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'assets', 'fonts', 'Inter-ExtraBold.ttf'), 18)
    for i, (im, lab) in enumerate(zip(images, labels)):
        x = pad + (i % cols) * (tile_w + pad); y = pad + (i // cols) * (th + head + pad)
        sheet.paste(Image.fromarray(im).resize((tile_w, th), Image.LANCZOS), (x, y + head))
        d.text((x + 3, y + 4), lab, font=f, fill=(255, 194, 74))
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    sheet.save(out, quality=90)
    print('->', out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('arg', nargs='?')
    ap.add_argument('--scale', type=float, default=0.25)
    ap.add_argument('--step', type=float, default=0.1)
    ap.add_argument('--cols', type=int, default=10)
    ap.add_argument('--tile', type=int, default=180)
    ap.add_argument('--out', default=None)
    ap.add_argument('--nomb', action='store_true')
    ap.add_argument('--spp', type=int, default=4)
    ap.add_argument('--every', type=int, default=1)     # split work across processes: every Nth frame...
    ap.add_argument('--phase', type=int, default=0)     # ...starting at this offset
    a = ap.parse_args()
    spp = SPP9 if a.spp == 9 else SPP4

    if a.cmd in ('strip', 'sheet'):
        if a.cmd == 'strip':
            t0, t1 = [float(x) for x in a.arg.split(':')]
            ts = list(np.arange(t0, t1 + 1e-6, a.step))
        else:
            ts = [float(x) for x in a.arg.split(',')]
        ims, labs = [], []
        for t in ts:
            img = video.frame(t, a.scale, spp, motion_blur=1 if a.nomb else mb_for(t))
            ims.append((img * 255).astype(np.uint8)); labs.append(f'{t:.2f}')
        grid(ims, labs, a.cols, a.out or os.path.join(HERE, 'build', 'check', f'{a.cmd}.jpg'), a.tile)

    elif a.cmd == 'base':
        i0, i1 = [int(x) for x in a.arg.split(':')]
        os.makedirs(BASE, exist_ok=True)
        for i in range(i0 + a.phase, i1, a.every):
            p = os.path.join(BASE, f'{i:05d}.png')
            if os.path.exists(p):
                continue
            t = i / shots.FPS
            t_start = time.time()
            img = video.base_frame(t, a.scale if a.scale != 0.25 else 1.0, spp, motion_blur=mb_for(t))
            tmp = p + '.tmp.png'
            cv2.imwrite(tmp, (img[..., ::-1] * 255 + 0.5).astype(np.uint8))
            os.replace(tmp, p)
            print(f'base {i} t={t:.3f} {time.time() - t_start:.1f}s', flush=True)

    elif a.cmd == 'composite':
        i0, i1 = [int(x) for x in (a.arg or f'0:{shots.N_FRAMES}').split(':')]
        os.makedirs(FRAMES, exist_ok=True)
        for i in range(i0, i1):
            t = i / shots.FPS
            img = cv2.imread(os.path.join(BASE, f'{i:05d}.png'))[..., ::-1].astype(np.float32) / 255.0
            img = video.overlay_frame(img, t)
            cv2.imwrite(os.path.join(FRAMES, f'{i:05d}.png'), (img[..., ::-1] * 255 + 0.5).astype(np.uint8))
        print('composited', i1 - i0, 'frames ->', FRAMES)

    elif a.cmd == 'final':
        out = a.out or os.path.join(HERE, '..', '..', 'outputs', 'final.mp4')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(shots.FPS), '-i', os.path.join(FRAMES, '%05d.png'),
                        '-i', os.path.join(HERE, 'build', 'mix.wav'),
                        '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest',
                        '-movflags', '+faststart', out], check=True)
        print('->', out)

    elif a.cmd == 'encode':
        out = a.out or os.path.join(HERE, 'build', 'video_noaudio.mp4')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(shots.FPS), '-i', os.path.join(FRAMES, '%05d.png'),
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
        print('->', out)


if __name__ == '__main__':
    main()
