"""One finished video frame at time t: physics or diagram render -> post -> overlays."""
import numpy as np

from . import shots, diagram, shade, post
from .frame import render_hdr, SPP4, W_FULL, H_FULL
from . import timeline_overlay as tov
from . import overlay as ov


def frame(t, scale=1.0, spp=SPP4, overlays=True, motion_blur=1):
    """Float RGB (h, w, 3) in 0..1.  motion_blur = number of sub-frame samples over a 180-degree shutter."""
    w, h = int(round(W_FULL * scale)), int(round(H_FULL * scale))
    st = shots.state(t)
    you = None
    samples = []
    offs = [0.0] if motion_blur <= 1 else [(i + 0.5) / motion_blur - 0.5 for i in range(motion_blur)]
    for o in offs:
        ts = t + o * (0.5 / shots.FPS)
        s2 = shots.state(ts)
        if s2['diagram'] is not None:
            hdr, info = diagram.render_e(ts, w, h, spp, shade.BB)
            if abs(o) < 1e-9 or you is None:
                you = info['you']
            exp = 0.8
        else:
            hdr = render_hdr(s2['cam'], ts, w, h, spp, tint=s2['tint'], disk_gain=s2['disk_gain'], sky_gain=s2['sky_gain'])
            exp = s2['exposure']
        samples.append(hdr * exp)
    hdr = np.mean(samples, axis=0)
    if st.get('sweep', 0) > 0 and st['cam'] is not None:
        hdr = line_sweep(hdr, st['cam'], st['sweep'])
    img = post.finish(hdr, exposure=1.0, bloom_amt=st['bloom'], seed=int(round(t * shots.FPS)) + 17)
    if overlays:
        if tov.caption_layer(t) is not None:
            img = scrim(img)
        if you is not None and scale != 1.0:
            you = (you[0] / scale, you[1] / scale)
        img = ov.composite(img, tov.layers(t, you, st))
    return np.clip(img, 0, 1)


def scrim(img, y0=0.585, y1=0.745, strength=0.5):
    """Darken bright backgrounds under the caption band so captions keep contrast (no effect on dark areas)."""
    h = img.shape[0]
    yy = np.arange(h, dtype=np.float32) / h
    band = np.clip(np.minimum((yy - (y0 - 0.05)) / 0.05, ((y1 + 0.05) - yy) / 0.05), 0, 1)
    lum = img.mean(axis=2)
    k = strength * band[:, None] * np.clip((lum - 0.12) / 0.5, 0, 1)
    return img * (1.0 - k[..., None])


def line_sweep(hdr, cam, k):
    """D: a glow that runs along the horizon line (where the sky meets the black) to lead the eye to it."""
    import cv2, math
    h, w = hdr.shape[:2]
    # the horizon line is where the view direction is perpendicular to the radial direction P
    ty = math.tan(math.radians(cam.vfov) / 2); tx = ty * w / h
    pts = []
    for xn in np.linspace(-1.2, 1.2, 64):
        # solve for yn with (F + xn tx R + yn ty U) . P = 0
        a = np.dot(cam.F, cam.P) + xn * tx * np.dot(cam.R, cam.P); b = ty * np.dot(cam.U, cam.P)
        if abs(b) < 1e-9:
            continue
        yn = -a / b
        pts.append(((xn + 1) / 2 * w, (1 - yn) / 2 * h))
    layer = np.zeros((h, w), np.float32)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        xm = 0.5 * (x0 + x1) / w
        head = math.exp(-((xm - (-0.1 + 1.2 * k)) / 0.10) ** 2)          # bright head moving left to right
        lit = 0.35 * (1.0 if xm < (-0.1 + 1.2 * k) else 0.0)               # the line stays lit behind it
        v = (head * 3.0 + lit) * math.sin(math.pi * min(1.0, k * 1.25)) ** 0.5
        cv2.line(layer, (int(x0 * 16), int(y0 * 16)), (int(x1 * 16), int(y1 * 16)), float(v), 2, cv2.LINE_AA, shift=4)
    glow = cv2.GaussianBlur(layer, (0, 0), 1.5) * 2.0 + cv2.GaussianBlur(layer, (0, 0), 12.0) * 3.0
    return hdr + glow[..., None] * np.array([0.55, 0.8, 1.3], np.float32)[None, None, :] * 0.6
