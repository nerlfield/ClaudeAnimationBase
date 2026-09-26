"""Shot E: an outside, diagram-style view of the photon sphere with a small astronaut on it.

Not lensed (it's labelled a diagram).  Background stars and the disk reuse the same shading functions as
the physical shots so the world matches; the astronaut is a raymarched signed-distance field.
"""
import math
import numpy as np
import numba as nb
import cv2

from . import shade
from .frame import norm, rotate

RING_R = 1.5
ASTRO_SCALE = 1.2


@nb.njit(cache=True, inline='always')
def _sdcap(px, py, pz, ax, ay, az, bx, by, bz, r):
    pax, pay, paz = px - ax, py - ay, pz - az
    bax, bay, baz = bx - ax, by - ay, bz - az
    h = (pax * bax + pay * bay + paz * baz) / (bax * bax + bay * bay + baz * baz)
    h = min(1.0, max(0.0, h))
    dx, dy, dz = pax - bax * h, pay - bay * h, paz - baz * h
    return math.sqrt(dx * dx + dy * dy + dz * dz) - r


@nb.njit(cache=True, inline='always')
def _sdrbox(px, py, pz, cx, cy, cz, hx, hy, hz, r):
    qx = abs(px - cx) - hx + r; qy = abs(py - cy) - hy + r; qz = abs(pz - cz) - hz + r
    ox, oy, oz = max(qx, 0.0), max(qy, 0.0), max(qz, 0.0)
    return math.sqrt(ox * ox + oy * oy + oz * oz) + min(max(qx, max(qy, qz)), 0.0) - r


@nb.njit(cache=True, inline='always')
def _smin(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * 0.25


@nb.njit(cache=True)
def astro_sdf(px, py, pz, turn):
    """Astronaut in local coords: x forward, y left, z up; feet near z=0, helmet top ~0.8.
    Returns (distance, material): 0 suit, 1 visor, 2 backpack/boots."""
    # upper body yaws by `turn` (radians) about z through the torso axis
    c, s = math.cos(-turn), math.sin(-turn)
    ux, uy = c * px - s * py, s * px + c * py
    uz = pz
    helmet = math.sqrt(ux * ux + uy * uy + (uz - 0.64) ** 2) - 0.165
    torso = _sdrbox(ux, uy, uz, 0.0, 0.0, 0.36, 0.105, 0.145, 0.16, 0.06)
    pack = _sdrbox(ux, uy, uz, -0.15, 0.0, 0.40, 0.055, 0.125, 0.15, 0.03)
    arm_l = _sdcap(ux, uy, uz, 0.0, 0.17, 0.47, 0.10, 0.25, 0.26, 0.052)
    arm_r = _sdcap(ux, uy, uz, 0.0, -0.17, 0.47, 0.13, -0.22, 0.30, 0.052)
    leg_l = _sdcap(px, py, pz, 0.0, 0.075, 0.21, 0.05, 0.10, -0.02, 0.064)
    leg_r = _sdcap(px, py, pz, 0.0, -0.075, 0.21, -0.04, -0.09, 0.0, 0.064)
    body = _smin(torso, helmet, 0.05)
    body = _smin(body, arm_l, 0.04); body = _smin(body, arm_r, 0.04)
    body = _smin(body, leg_l, 0.05); body = _smin(body, leg_r, 0.05)
    visor = max(math.sqrt((ux - 0.035) ** 2 + uy * uy + (uz - 0.645) ** 2) - 0.14, -(ux - 0.07))
    d = body; m = 0
    if pack < d:
        d = pack; m = 2
    if visor < d + 0.004:
        d = min(d, visor); m = 1
    return d, m


@nb.njit(parallel=True, cache=True)
def render_diagram(out, W, H, C, F, R, U, tx, ty, t, tab, star_sigma, disk_gain,
                   A, Af, Al, Au, turn, spp):
    """Background (stars, disk, horizon sphere) plus the astronaut, unlensed."""
    for yy in nb.prange(H):
        for xx in range(W):
            ar = 0.0; ag = 0.0; ab = 0.0
            for s in range(spp.shape[0]):
                xn = ((xx + spp[s, 0]) / W) * 2.0 - 1.0
                yn = 1.0 - ((yy + spp[s, 1]) / H) * 2.0
                dx = F[0] + xn * tx * R[0] + yn * ty * U[0]
                dy = F[1] + xn * tx * R[1] + yn * ty * U[1]
                dz = F[2] + xn * tx * R[2] + yn * ty * U[2]
                dn = math.sqrt(dx * dx + dy * dy + dz * dz); dx /= dn; dy /= dn; dz /= dn
                cr = 0.0; cg = 0.0; cb = 0.0
                tmax = 1e9
                # horizon sphere (radius 1 at origin): black with a faint ice rim so it separates
                bq = C[0] * dx + C[1] * dy + C[2] * dz
                cq = C[0] * C[0] + C[1] * C[1] + C[2] * C[2] - 1.0
                disc = bq * bq - cq
                hit_sphere = False
                if disc > 0:
                    th = -bq - math.sqrt(disc)
                    if th > 0:
                        tmax = th; hit_sphere = True
                        nx, ny, nz = C[0] + dx * th, C[1] + dy * th, C[2] + dz * th
                        fres = (1.0 + (nx * dx + ny * dy + nz * dz)) ** 5
                        cr = 0.10 * fres; cg = 0.18 * fres; cb = 0.34 * fres
                # astronaut: raymarch only near its bounding sphere
                ox, oy, oz = C[0] - A[0], C[1] - A[1], C[2] - A[2]
                bs = ox * dx + oy * dy + oz * dz
                cs = ox * ox + oy * oy + oz * oz - (0.9 * ASTRO_SCALE) ** 2
                ds = bs * bs - cs
                hit_astro = False
                if ds > 0:
                    tt = max(0.0, -bs - math.sqrt(ds))
                    t1 = -bs + math.sqrt(ds)
                    for _ in range(96):
                        wx, wy, wz = C[0] + dx * tt, C[1] + dy * tt, C[2] + dz * tt
                        lx, ly, lz = wx - A[0], wy - A[1], wz - A[2]
                        qx = (lx * Af[0] + ly * Af[1] + lz * Af[2]) / ASTRO_SCALE
                        qy = (lx * Al[0] + ly * Al[1] + lz * Al[2]) / ASTRO_SCALE
                        qz = (lx * Au[0] + ly * Au[1] + lz * Au[2]) / ASTRO_SCALE + 0.4
                        d, m = astro_sdf(qx, qy, qz, turn)
                        d *= ASTRO_SCALE
                        if d < 0.0008:
                            if tt < tmax:
                                hit_astro = True
                                # normal by central differences in local space
                                e = 0.002
                                n1, _ = astro_sdf(qx + e, qy, qz, turn); n2, _ = astro_sdf(qx - e, qy, qz, turn)
                                n3, _ = astro_sdf(qx, qy + e, qz, turn); n4, _ = astro_sdf(qx, qy - e, qz, turn)
                                n5, _ = astro_sdf(qx, qy, qz + e, turn); n6, _ = astro_sdf(qx, qy, qz - e, turn)
                                gx, gy, gz = n1 - n2, n3 - n4, n5 - n6
                                gl = math.sqrt(gx * gx + gy * gy + gz * gz) + 1e-9
                                gx /= gl; gy /= gl; gz /= gl
                                # to world
                                nx = gx * Af[0] + gy * Al[0] + gz * Au[0]
                                ny = gx * Af[1] + gy * Al[1] + gz * Au[1]
                                nz = gx * Af[2] + gy * Al[2] + gz * Au[2]
                                # lights: warm disk glow from below/outside, ice rim from the ring light, dim fill
                                kx, ky, kz = -0.35 * wx, -0.35 * wy, -1.0
                                kl = math.sqrt(kx * kx + ky * ky + kz * kz); kx /= -kl; ky /= -kl; kz /= -kl
                                key = max(0.0, nx * kx + ny * ky + nz * kz)
                                rimv = (1.0 + (nx * dx + ny * dy + nz * dz)) ** 3
                                top = max(0.0, nz) * 0.25
                                # cheap AO: sample the field along the normal
                                ao = 1.0
                                for k in range(1, 4):
                                    hh = 0.03 * k
                                    dd, _ = astro_sdf(qx + gx * hh, qy + gy * hh, qz + gz * hh, turn)
                                    ao -= (hh - dd) * (0.9 / k)
                                ao = min(1.0, max(0.25, ao))
                                if m == 0:
                                    alb = (0.86, 0.87, 0.9)
                                elif m == 2:
                                    alb = (0.55, 0.57, 0.62)
                                else:
                                    alb = (0.06, 0.05, 0.03)
                                cr = alb[0] * (1.9 * key * 1.0 + 0.05 + top * 0.3) * ao + rimv * 0.55 * 0.56
                                cg = alb[1] * (1.9 * key * 0.72 + 0.06 + top * 0.35) * ao + rimv * 0.55 * 0.76
                                cb = alb[2] * (1.9 * key * 0.40 + 0.09 + top * 0.5) * ao + rimv * 0.55 * 1.0
                                if m == 1:   # gold visor: specular of the warm disk + ice rim
                                    rr = dz - 2.0 * (nx * dx + ny * dy + nz * dz) * nz
                                    spec = max(0.0, -rr) ** 2
                                    fres2 = 0.3 + 0.7 * rimv
                                    cr += (0.9 * spec + 0.25) * fres2 * 1.2
                                    cg += (0.62 * spec + 0.16) * fres2 * 1.2
                                    cb += (0.22 * spec + 0.06) * fres2 * 1.2
                            break
                        tt += d * 0.9
                        if tt > t1:
                            break
                if not hit_astro and not hit_sphere:
                    # disk plane z = 0 (diagram: unlensed, dimmed)
                    if abs(dz) > 1e-6:
                        tp = -C[2] / dz
                        if tp > 0:
                            X = C[0] + dx * tp; Y = C[1] + dy * tp
                            rr = math.sqrt(X * X + Y * Y)
                            er, eg, eb, al = shade.disk_emit(X, Y, rr, 1.0, t, 3.0, 12.0, tab, 0.0, 2.2)
                            cr += al * er * disk_gain; cg += al * eg * disk_gain; cb += al * eb * disk_gain
                            trans = 1.0 - al
                        else:
                            trans = 1.0
                    else:
                        trans = 1.0
                    # stars behind
                    if abs(dz) < 0.9:
                        ax_, ay_, az_ = 0.0, 0.0, 1.0
                    else:
                        ax_, ay_, az_ = 1.0, 0.0, 0.0
                    t1x = dy * az_ - dz * ay_; t1y = dz * ax_ - dx * az_; t1z = dx * ay_ - dy * ax_
                    t1l = math.sqrt(t1x * t1x + t1y * t1y + t1z * t1z); t1x /= t1l; t1y /= t1l; t1z /= t1l
                    t2x = dy * t1z - dz * t1y; t2y = dz * t1x - dx * t1z; t2z = dx * t1y - dy * t1x
                    sr, sg, sb = shade.sky(dx, dy, dz, t1x, t1y, t1z, t2x, t2y, t2z, 1.0, 1.0, star_sigma, tab, 1.0)
                    cr += trans * sr; cg += trans * sg; cb += trans * sb
                ar += cr; ag += cg; ab += cb
            inv = 1.0 / spp.shape[0]
            out[yy, xx, 0] = ar * inv; out[yy, xx, 1] = ag * inv; out[yy, xx, 2] = ab * inv


def ring_point(alpha):
    return np.array([RING_R * math.cos(alpha), RING_R * math.sin(alpha), 0.0])


def occluded(C, P):
    """Is world point P hidden behind the horizon sphere as seen from C?"""
    d = P - C; L = np.linalg.norm(d); d = d / L
    b = np.dot(C, d); c = np.dot(C, C) - 1.0
    disc = b * b - c
    if disc <= 0:
        return False
    t0 = -b - math.sqrt(disc)
    return 0 < t0 < L


def project(C, F, R, U, tx, ty, W, H, P):
    d = P - C; z = np.dot(d, F)
    if z <= 1e-6:
        return None
    return ((np.dot(d, R) / z / tx + 1) / 2 * W, (1 - np.dot(d, U) / z / ty) / 2 * H)


def glow_layer(W, H, pts, sigma_px, color, weights=None):
    """Additive glow of a polyline of screen points (list of (x, y) or None)."""
    img = np.zeros((H, W), np.float32)
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if a is None or b is None:
            continue
        w = 1.0 if weights is None else 0.5 * (weights[i] + weights[i + 1])
        if w <= 0:
            continue
        cv2.line(img, (int(a[0] * 16), int(a[1] * 16)), (int(b[0] * 16), int(b[1] * 16)), float(w), 1, cv2.LINE_AA, shift=4)
    core = cv2.GaussianBlur(img, (0, 0), max(0.6, sigma_px * 0.35))
    halo = cv2.GaussianBlur(img, (0, 0), sigma_px * 3.0)
    g = core * 1.6 + halo * 2.2
    return g[..., None] * np.array(color, np.float32)[None, None, :]


# ---------------------------------------------------------------- shot E, assembled

def e_state(t, T_E=22.2, T_F=26.6667, lap0=22.7, lap1=24.0):
    """Camera, astronaut and pulse for shot E at time t (pure function of t)."""
    from .shots import kf, seg, ease, ease_out, back_out
    el = kf(t, [(T_E, -2.0), (T_E + 0.8, -31.0), (T_F - 0.4, -34.0), (T_F, -2.0)],
            lambda x: ease_out(x) if t < T_E + 0.8 else (x if t < T_F - 0.4 else ease(x)))
    az = math.radians(-90.0 + kf(t, [(T_E, 0.0), (T_F, 5.0)], lambda x: x))
    dist = 8.6
    e = math.radians(el)
    C = np.array([dist * math.cos(e) * math.cos(az), dist * math.cos(e) * math.sin(az), dist * math.sin(e)])
    F = norm(-C)
    U = norm(np.array([0.0, 0.0, 1.0]) - np.dot([0.0, 0.0, 1.0], F) * F)
    R = norm(np.cross(F, U))
    # astronaut on the ring, front-right of the hole, facing +alpha (counter-clockwise)
    a0 = az + math.radians(-14.0)
    Tdir = np.array([-math.sin(a0), math.cos(a0), 0.0])
    Au = np.array([0.0, 0.0, 1.0])
    Al = norm(np.cross(Au, Tdir))
    Af = Tdir
    A = ring_point(a0) - Au * (0.64 - 0.4) * ASTRO_SCALE
    # the double take: anticipation, fast turn over the shoulder, hold, turn back
    turn = math.radians(kf(t, [(25.0, 0.0), (25.15, -8.0), (25.5, 80.0), (25.9, 80.0), (26.3, 0.0)],
                           lambda x: back_out(x, 1.1) if 25.15 <= t < 25.5 else ease(x)))
    # the pulse: leaves the back of the helmet going -alpha, runs the lap, enters the visor
    delta = 0.11
    s = seg(t, lap0, lap1)
    s = s * s * (3 - 2 * s) * 0.15 + s * 0.85          # light is steady; only a hint of ease at launch
    alive = lap0 <= t <= lap1 + 0.05
    ap = a0 - delta - s * (2 * math.pi - 2 * delta)
    return dict(C=C, F=F, R=R, U=U, A=A, Af=Af, Al=Al, Au=Au, turn=turn, a0=a0, ap=ap, alive=alive,
                s=s, lap_done=t > lap1, lap1=lap1, flash=max(0.0, 1.0 - (t - lap1) / 0.5) if t > lap1 else 0.0, vfov=38.0,
                trail_fade=1.0 - seg(t, 25.6, T_F - 0.3))


def render_e(t, w, h, spp, tab):
    st = e_state(t)
    ty = math.tan(math.radians(st['vfov']) / 2); tx = ty * w / h
    out = np.zeros((h, w, 3), np.float32)
    render_diagram(out, w, h, st['C'], st['F'], st['R'], st['U'], tx, ty, t, tab, 0.75 * 2 * ty / h, 0.17,
                   st['A'], st['Af'], st['Al'], st['Au'], st['turn'], spp)
    C, F, R, U = st['C'], st['F'], st['R'], st['U']
    # the photon-sphere ring: faint everywhere, bright along the pulse's trail; hidden behind the sphere
    n = 720
    alphas = [st['a0'] - 2 * math.pi * i / n for i in range(n + 1)]
    pts, wts = [], []
    for a in alphas:
        P = ring_point(a)
        pts.append(None if occluded(C, P) else project(C, F, R, U, tx, ty, w, h, P))
        base = 0.22
        trail = 0.0
        if st['alive'] or st['lap_done']:
            back = (st['a0'] - 0.11) - a                       # how far along the lap this point is
            ahead = (st['a0'] - 0.11) - st['ap']
            if 0 <= back <= ahead:
                # a bright comet tail behind the pulse, and a faint path that stays drawn after it
                head = math.exp(-(ahead - back) / 0.9) * (1.0 if not st['lap_done'] else max(0.0, 1 - (t - st['lap1']) / 0.9))
                trail = max(head, 0.28 * st['trail_fade'])
        wts.append(base + 2.5 * trail)
    glow = glow_layer(w, h, pts, 2.2 * w / 1080, (0.55, 0.78, 1.25), wts)
    # the pulse head and the visor flash
    extra = np.zeros((h, w), np.float32)
    if st['alive']:
        P = ring_point(st['ap'])
        q = None if occluded(C, P) else project(C, F, R, U, tx, ty, w, h, P)
        if q is not None:
            cv2.circle(extra, (int(q[0] * 16), int(q[1] * 16)), int(3.0 * w / 1080 * 16), 30.0, -1, cv2.LINE_AA, shift=4)
    if st['flash'] > 0:
        head = st['A'] + st['Au'] * (0.64 - 0.4) * ASTRO_SCALE + st['Af'] * 0.1 * ASTRO_SCALE
        q = project(C, F, R, U, tx, ty, w, h, head)
        if q is not None:
            cv2.circle(extra, (int(q[0] * 16), int(q[1] * 16)), int(9.0 * w / 1080 * 16), 25.0 * st['flash'] ** 1.5, -1, cv2.LINE_AA, shift=4)
    extra = cv2.GaussianBlur(extra, (0, 0), 1.2 * w / 1080) + cv2.GaussianBlur(extra, (0, 0), 14.0 * w / 1080) * 0.35
    out += glow + extra[..., None] * np.array([0.75, 0.9, 1.2], np.float32)[None, None, :]
    # arrowheads along the path the light took: from the back of the helmet, all the way round, into the visor
    if t >= 22.8:
        ch = np.zeros((h, w), np.float32)
        done = (st['a0'] - 0.11) - st['ap']
        for j in range(1, 9):
            a = st['a0'] - 0.11 - j * (2 * math.pi - 0.22) / 9
            if (st['a0'] - 0.11) - a > done + 1e-6:
                continue
            P0, P1 = ring_point(a + 0.06), ring_point(a - 0.06)
            if occluded(C, P0):
                continue
            q0 = project(C, F, R, U, tx, ty, w, h, P0); q1 = project(C, F, R, U, tx, ty, w, h, P1)
            if q0 is None or q1 is None:
                continue
            dx, dy = q1[0] - q0[0], q1[1] - q0[1]; L = math.hypot(dx, dy) or 1.0
            ux, uy = dx / L, dy / L; sz = 13.0 * w / 1080
            tip = (q1[0], q1[1])
            for sgn in (1, -1):
                bx = tip[0] - ux * sz + sgn * uy * sz * 0.8; by = tip[1] - uy * sz - sgn * ux * sz * 0.8
                cv2.line(ch, (int(tip[0] * 16), int(tip[1] * 16)), (int(bx * 16), int(by * 16)), 1.0, max(1, int(2 * w / 1080)), cv2.LINE_AA, shift=4)
        fade = st['trail_fade']
        out += (cv2.GaussianBlur(ch, (0, 0), 0.8) * 2.2 + cv2.GaussianBlur(ch, (0, 0), 5.0) * 1.5)[..., None] * \
            np.array([0.6, 0.85, 1.3], np.float32)[None, None, :] * fade
    you = project(C, F, R, U, tx, ty, w, h, st['A'] + st['Au'] * (0.64 - 0.4 + 0.19) * ASTRO_SCALE)
    return out, dict(you=you)
