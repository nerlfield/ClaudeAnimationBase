"""E2: the back of your own head, seen in the line of light at the photon sphere.

At 1.5 horizon radii light can circle the black hole, so light leaving the back of your head goes all the way round
and arrives from straight ahead: the bright line across the sky is you, seen from behind (APOD 2013-07-02).  For
real, that image is a hair-thin sliver stretched around the whole sky; here the line is magnified until the helmet
reads, which the video labels.  The helmet is the same signed-distance astronaut as the diagram shot, raymarched
from behind and lit the way it would be there: bright, bluish sky light from above, nothing from the black hole
below, and a warm rim from the lensed disk.
"""
import math

import cv2
import numba as nb
import numpy as np

from .diagram import astro_sdf
from .frame import SPP4

# the window of the astronaut shown (local coords: x forward, y left, z up), seen from behind
WIN_Y, WIN_Z0, WIN_Z1 = 0.36, 0.26, 0.86


@nb.njit(parallel=True, cache=True)
def render_back(out, W, H, turn, spp):
    """RGBA of the astronaut's back (helmet, shoulders, pack) by orthographic raymarch along +x."""
    for yy in nb.prange(H):
        for xx in range(W):
            ar = 0.0; ag = 0.0; ab = 0.0; aa = 0.0
            for s in range(spp.shape[0]):
                # seen from behind, screen-right is the astronaut's left (+y)
                py = (((xx + spp[s, 0]) / W) * 2.0 - 1.0) * WIN_Y
                pz = WIN_Z1 - ((yy + spp[s, 1]) / H) * (WIN_Z1 - WIN_Z0)
                px = -0.6
                hit = False
                for _ in range(80):
                    d, m = astro_sdf(px, py, pz, turn)
                    if d < 0.0006:
                        hit = True
                        break
                    px += d * 0.9
                    if px > 0.6:
                        break
                if not hit:
                    continue
                e = 0.0015
                n1, _ = astro_sdf(px + e, py, pz, turn); n2, _ = astro_sdf(px - e, py, pz, turn)
                n3, _ = astro_sdf(px, py + e, pz, turn); n4, _ = astro_sdf(px, py - e, pz, turn)
                n5, _ = astro_sdf(px, py, pz + e, turn); n6, _ = astro_sdf(px, py, pz - e, turn)
                gx, gy, gz = n1 - n2, n3 - n4, n5 - n6
                gl = math.sqrt(gx * gx + gy * gy + gz * gz) + 1e-9
                gx /= gl; gy /= gl; gz /= gl
                # sky light: the bright outer hemisphere is "up" (radially out); the black hole below gives nothing
                sky = max(0.0, 0.06 + 0.94 * gz) ** 1.3
                back = max(0.0, -gx) * 0.22                       # a little of the looping light, from behind
                rim = max(0.0, gz * 0.4 + gy * 0.6) ** 3              # warm lensed-disk light, upper left
                ao = 1.0
                for k in range(1, 4):
                    hh = 0.025 * k
                    dd, _ = astro_sdf(px + gx * hh, py + gy * hh, pz + gz * hh, turn)
                    ao -= (hh - dd) * (0.9 / k)
                ao = min(1.0, max(0.3, ao))
                alb = 0.88 if m == 0 else (0.55 if m == 2 else 0.12)
                ar += alb * ((sky + back) * 0.78 * ao) + rim * 0.55
                ag += alb * ((sky + back) * 0.90 * ao) + rim * 0.36
                ab += alb * ((sky + back) * 1.10 * ao) + rim * 0.18
                aa += 1.0
            n = spp.shape[0]
            out[yy, xx, 0] = ar / n; out[yy, xx, 1] = ag / n; out[yy, xx, 2] = ab / n; out[yy, xx, 3] = aa / n


def line_row(cam, h):
    """Screen row of the photon-sphere line (view direction perpendicular to the radial direction) at centre."""
    P = cam.P / np.linalg.norm(cam.P)
    ty = math.tan(math.radians(cam.vfov) / 2)
    b = ty * float(np.dot(cam.U, P))
    yn = -float(np.dot(cam.F, P)) / b if abs(b) > 1e-9 else 0.0
    return (1 - yn) / 2 * h


def composite(hdr, cam, open_k, turn):
    """Open the line into a band holding the back of the helmet (open_k 0..1), in exposed HDR space."""
    if open_k <= 1e-3:
        return hdr
    h, w = hdr.shape[:2]
    yl = line_row(cam, h)
    full_h = int(0.26 * h)                                  # helmet window height when fully open
    full_w = int(full_h * (2 * WIN_Y) / (WIN_Z1 - WIN_Z0))
    img = np.zeros((full_h, full_w, 4), np.float32)
    render_back(img, full_w, full_h, float(turn), SPP4)
    disp_h = max(2, int(round(full_h * open_k)))
    img = cv2.resize(img, (full_w, disp_h), interpolation=cv2.INTER_AREA)
    y0 = int(round(yl - disp_h / 2)); x0 = (w - full_w) // 2
    # the band: the line itself, opening into a lens (widest in the middle, pinching back into the line at the frame
    # edges), filled with its own cold light and rimmed brighter; the helmet is seen inside it
    ice = np.array([0.52, 0.72, 1.0], np.float32)
    half = 0.5 * (disp_h + 0.05 * h * open_k)
    xs = np.arange(w, dtype=np.float32)
    u = np.clip(np.abs(xs - w / 2) / (0.5 * w), 0, 1)
    hh = np.maximum(0.7, half * (1 - u ** 2) ** 0.8)                          # half-height per column
    ys = np.arange(h, dtype=np.float32)[:, None]
    dist = np.abs(ys - yl) - hh[None, :]                                      # <0 inside the lens
    inside = np.clip(-dist / max(1.5, 0.002 * h), 0, 1)
    rim = np.exp(-(dist / max(1.5, 0.004 * h)) ** 2)
    depth = np.clip(1 - np.abs(ys - yl) / np.maximum(hh[None, :], 1), 0, 1)   # 1 on the centre line, 0 at the rim
    k = min(1.0, open_k * 3)
    fill = (0.30 + 0.25 * depth)[..., None] * ice
    hdr[:] = hdr * (1 - inside[..., None] * k) + (fill * inside[..., None] + rim[..., None] * ice * 1.6) * k
    # the helmet, clipped to the lens
    ya, yb = max(0, y0), min(h, y0 + disp_h)
    xa, xb = max(0, x0), min(w, x0 + full_w)
    if yb > ya and xb > xa:
        part = img[ya - y0:yb - y0, xa - x0:xb - x0]
        al = part[..., 3:4] * inside[ya:yb, xa:xb, None] * min(1.0, open_k * 2.5)
        hdr[ya:yb, xa:xb] = hdr[ya:yb, xa:xb] * (1 - al) + part[..., :3] * 1.15 * al
    return hdr
    h, w = hdr.shape[:2]
    yl = line_row(cam, h)
    full_h = int(0.26 * h)                                  # helmet window height when fully open
    full_w = int(full_h * (2 * WIN_Y) / (WIN_Z1 - WIN_Z0))
    img = np.zeros((full_h, full_w, 4), np.float32)
    render_back(img, full_w, full_h, float(turn), SPP4)
    disp_h = max(2, int(round(full_h * open_k)))
    img = cv2.resize(img, (full_w, disp_h), interpolation=cv2.INTER_AREA)
    y0 = int(round(yl - disp_h / 2)); x0 = (w - full_w) // 2
    # the band: the line's light (bluish, like the blueshifted sky just above it), opened into a luminous slit with
    # bright edges, fading out towards the sides of the frame
    above = hdr[max(0, int(yl) - int(0.06 * h)):max(1, int(yl) - 2)].reshape(-1, 3)
    sky_col = np.percentile(above, 75, axis=0) if len(above) else np.array([0.3, 0.35, 0.45], np.float32)
    line_col = np.maximum(sky_col * 2.2, np.array([0.34, 0.42, 0.62], np.float32))
    band_h = disp_h + int(0.05 * h * open_k)
    by0 = int(round(yl - band_h / 2))
    ys = np.arange(band_h, dtype=np.float32) / max(1, band_h - 1)
    edge = np.exp(-(np.minimum(ys, 1 - ys) * band_h / max(2.0, 0.012 * h)) ** 2)        # bright rims
    fill = 0.55 + 0.45 * np.cos(np.pi * (ys - 0.5)) ** 2
    v = np.clip(np.minimum(ys, 1 - ys) * band_h / max(1.0, 0.006 * h), 0, 1)
    xs = np.arange(w, dtype=np.float32)
    hmask = np.clip(1.0 - np.abs(xs - w / 2) / (0.5 * w), 0, 1) ** 0.5
    k = min(1.0, open_k * 3)
    a_band = (v[:, None] * hmask[None, :] * k).astype(np.float32)[..., None]
    col = (fill[:, None, None] * line_col[None, None, :] + edge[:, None, None] * line_col[None, None, :] * 2.5)
    ya, yb = max(0, by0), min(h, by0 + band_h)
    hdr[ya:yb] = hdr[ya:yb] * (1 - a_band[ya - by0:yb - by0] * 0.9) + col[ya - by0:yb - by0] * a_band[ya - by0:yb - by0]
    # the helmet itself, on top of the band
    ya, yb = max(0, y0), min(h, y0 + disp_h)
    xa, xb = max(0, x0), min(w, x0 + full_w)
    if yb > ya and xb > xa:
        part = img[ya - y0:yb - y0, xa - x0:xb - x0]
        al = part[..., 3:4] * min(1.0, open_k * 2.5)
        hdr[ya:yb, xa:xb] = hdr[ya:yb, xa:xb] * (1 - al) + part[..., :3] * 1.1 * al
    return hdr
