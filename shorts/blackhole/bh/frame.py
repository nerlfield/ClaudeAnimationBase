"""Camera maths and the HDR frame renderer (a pure function of the camera and time)."""
import math
from functools import lru_cache
import numpy as np

from .geodesic import Table
from . import shade

W_FULL, H_FULL = 1080, 1920

# 2x2 rotated-grid supersampling, and a 3x3 pattern for final renders
SPP4 = np.array([[0.375, 0.125], [0.875, 0.375], [0.125, 0.625], [0.625, 0.875]], np.float64)
SPP9 = np.array([[(i + 0.5 + 0.25 * ((j % 2) * 2 - 1) * 0.5) / 3, (j + 0.5) / 3] for j in range(3) for i in range(3)], np.float64)


def norm(v):
    v = np.asarray(v, np.float64)
    return v / np.linalg.norm(v)


def basis(F, U):
    F = norm(F)
    U = norm(np.asarray(U, np.float64) - np.dot(U, F) * F)
    R = norm(np.cross(F, U))
    return F, R, U


def rotate(v, axis, ang):
    """Rodrigues rotation of v about unit axis by ang radians."""
    v = np.asarray(v, np.float64); k = norm(axis)
    return v * math.cos(ang) + np.cross(k, v) * math.sin(ang) + k * np.dot(k, v) * (1 - math.cos(ang))


@lru_cache(maxsize=6)
def table_for(r0):
    return Table(float(r0))


class Cam:
    def __init__(self, r0, P, F, U, vfov=60.0):
        self.r0 = float(r0)
        self.P = norm(P)
        self.F, self.R, self.U = basis(F, U)
        self.vfov = vfov

    def project(self, d):
        """World direction -> pixel (x, y) at full res, or None if behind the camera."""
        d = norm(d)
        z = np.dot(d, self.F)
        if z <= 1e-6:
            return None
        ty = math.tan(math.radians(self.vfov) / 2); tx = ty * W_FULL / H_FULL
        xn = np.dot(d, self.R) / z / tx; yn = np.dot(d, self.U) / z / ty
        return (xn + 1) / 2 * W_FULL, (1 - yn) / 2 * H_FULL


def render_hdr(cam, t, w=W_FULL, h=H_FULL, spp=SPP4, tint=0.0, disk_gain=1.0, sky_gain=1.0,
               rin=3.0, rout=12.0, spin_rate=2.2, spin_sign=1.0):
    """Linear HDR image (h, w, 3) float32 for camera cam at video time t."""
    T = table_for(round(cam.r0, 9))
    ty = math.tan(math.radians(cam.vfov) / 2)
    tx = ty * w / h
    out = np.zeros((h, w, 3), np.float32)
    star_sigma = 0.75 * (2 * ty / h)
    shade.render(out, w, h, 0, 0, spp, cam.P, cam.F, cam.R, cam.U, tx, ty,
                 T.psi, T.phi, T.u, T.cnt, T.status, T.phi_end, T.pc, T.k, T.r0,
                 float(t), rin, rout, shade.BB, float(tint), spin_rate, disk_gain, sky_gain, spin_sign, star_sigma)
    return out
