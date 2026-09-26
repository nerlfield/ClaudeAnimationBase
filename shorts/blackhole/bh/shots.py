"""The video's timeline: camera and render parameters as pure functions of video time t (seconds).

Bars at 90 BPM: one bar = 2.6667 s.  Shot boundaries and payoffs sit on bars (see outputs/storyboard.md).
"""
import math
import numpy as np

from .frame import Cam, norm, rotate
from .geodesic import B_CRIT

BPM = 90.0
BAR = 4 * 60.0 / BPM
DUR = 14 * BAR                     # 37.333 s
FPS = 30
N_FRAMES = int(round(DUR * FPS))   # 1120

# shot boundaries (v2 storyboard)
T_A, T_B, T_C, T_D, T_E, T_F, T_G = BAR, 2 * BAR, 6 * BAR, 7 * BAR, 22.2, 10 * BAR, 12 * BAR
HOLE_Y = 0.42                      # the black hole (and the final dot) sit at 42% of frame height


# ---------------------------------------------------------------- easing

def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= b)


def ease(x):          # smootherstep in/out
    x = clamp(x); return x * x * x * (x * (6 * x - 15) + 10)


def ease_in(x):
    x = clamp(x); return x * x * x


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def back_out(x, s=1.2):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1


def kf(t, keys, fn=ease):
    """Keyframes [(t, v), ...] with easing between them."""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * fn(seg(t, t0, t1))
    return keys[-1][1]


# ---------------------------------------------------------------- orientation helpers

def quat_from_basis(R, U, F):
    """Rotation (quaternion w,x,y,z) of the right-handed frame (U x F, U, F).  R is ignored."""
    F = norm(F); U = norm(np.asarray(U, np.float64) - np.dot(U, F) * F)
    M = np.array([np.cross(U, F), U, F]).T
    tr = M[0, 0] + M[1, 1] + M[2, 2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        q = [0.25 * s, (M[2, 1] - M[1, 2]) / s, (M[0, 2] - M[2, 0]) / s, (M[1, 0] - M[0, 1]) / s]
    elif M[0, 0] > M[1, 1] and M[0, 0] > M[2, 2]:
        s = math.sqrt(1.0 + M[0, 0] - M[1, 1] - M[2, 2]) * 2
        q = [(M[2, 1] - M[1, 2]) / s, 0.25 * s, (M[0, 1] + M[1, 0]) / s, (M[0, 2] + M[2, 0]) / s]
    elif M[1, 1] > M[2, 2]:
        s = math.sqrt(1.0 + M[1, 1] - M[0, 0] - M[2, 2]) * 2
        q = [(M[0, 2] - M[2, 0]) / s, (M[0, 1] + M[1, 0]) / s, 0.25 * s, (M[1, 2] + M[2, 1]) / s]
    else:
        s = math.sqrt(1.0 + M[2, 2] - M[0, 0] - M[1, 1]) * 2
        q = [(M[1, 0] - M[0, 1]) / s, (M[0, 2] + M[2, 0]) / s, (M[1, 2] + M[2, 1]) / s, 0.25 * s]
    q = np.array(q); return q / np.linalg.norm(q)


def quat_to_basis(q):
    w, x, y, z = q
    M = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    return M[:, 0], M[:, 1], M[:, 2]          # R, U, F


def slerp(q0, q1, s):
    d = float(np.dot(q0, q1))
    if d < 0:
        q1, d = -q1, -d
    if d > 0.9995:
        q = q0 + s * (q1 - q0); return q / np.linalg.norm(q)
    th = math.acos(d)
    return (math.sin((1 - s) * th) * q0 + math.sin(s * th) * q1) / math.sin(th)


# ---------------------------------------------------------------- geometry of the camera path

def pos(theta_deg, az_deg=0.0):
    """Unit position on the sphere: polar angle from the disk normal (+z), azimuth about z."""
    th, az = math.radians(theta_deg), math.radians(az_deg)
    p = np.array([0.0, -math.sin(th), math.cos(th)])
    return rotate(p, [0, 0, 1], az)


def look_at_hole(P, theta_deg, az_deg, vfov, y_frac=HOLE_Y, roll_deg=0.0):
    """Camera looking at the hole, which appears at y_frac of frame height."""
    th, az = math.radians(theta_deg), math.radians(az_deg)
    F = -P
    U = rotate(np.array([0.0, math.cos(th), math.sin(th)]), [0, 0, 1], az)
    R = np.cross(F, U)
    off = math.atan((1 - 2 * y_frac) * math.tan(math.radians(vfov) / 2))
    F2, U2 = rotate(F, R, -off), rotate(U, R, -off)
    if roll_deg:
        U2 = rotate(U2, F2, math.radians(roll_deg))
    return F2, U2


def tangent_view(P, az_deg, yaw_deg=0.0, roll_deg=0.0):
    """Looking along the horizon (the tangent direction e_phi), with the hole straight below."""
    ephi = rotate(np.array([1.0, 0.0, 0.0]), [0, 0, 1], math.radians(az_deg))
    F = rotate(ephi, P, math.radians(yaw_deg))
    U = P.copy()
    if roll_deg:
        U = rotate(U, F, math.radians(roll_deg))
    return F, U


def r_for_cone(half_deg):
    """Radius (r_s units, < 1.5) whose escape cone has this half-angle (static observer)."""
    s = math.sin(math.radians(half_deg))
    lo, hi = 1.0 + 1e-9, 1.5
    for _ in range(80):                     # f(r) = B r^-1 sqrt(1 - 1/r) is increasing on (1, 1.5)
        m = 0.5 * (lo + hi)
        if B_CRIT * math.sqrt(1 - 1 / m) / m < s:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- the timeline

def end_view(tau):
    """F-G-O: sinking toward the horizon and looking up while the sky closes into a dot.
    tau runs from T_F through DUR and on past it: O at time t uses tau = t + DUR, so the loop has no seam."""
    cone = kf(tau, [(T_F, 89.9), (T_G, 4.706), (DUR + BAR, 4.0)], lambda x: ease(x) if tau < T_G else x)
    r0 = r_for_cone(cone) if cone < 89.9 else 1.5
    az = 10.0
    P = pos(60.0, az)
    Fa, Ua = tangent_view(P, az, 6.0)
    vfov = kf(tau, [(T_F + 0.3, 60.0), (31.0, 34.0)])
    Fb = P.copy(); Ub = -rotate(np.array([1.0, 0.0, 0.0]), [0, 0, 1], math.radians(az))
    Rb = np.cross(Fb, Ub)
    off = math.atan((1 - 2 * HOLE_Y) * math.tan(math.radians(vfov) / 2))
    Fb, Ub = rotate(Fb, Rb, -off), rotate(Ub, Rb, -off)
    qa = quat_from_basis(None, Ua, Fa)
    qb = quat_from_basis(None, Ub, Fb)
    q = slerp(qa, qb, ease(seg(tau, T_F, 29.5)))
    R, U, F = quat_to_basis(q)
    U = rotate(U, F, math.radians(0.35 * (tau - T_F)))
    gs = 1 / math.sqrt(1 - 1 / r0)
    glow = 1.0 + 1.8 * ease(seg(tau, 29.0, T_G))       # the finished dot glows: all the sky's light in one place
    return Cam(r0, P, F, U, vfov), 0.5 * glow / gs ** 3.3


def state(t):
    """Everything the renderer needs at time t: a camera (or None for the diagram shot) and parameters."""
    p = dict(t=t, tint=0.0, exposure=0.55, disk_gain=1.0, sky_gain=1.0, shot='A', bloom=0.09, cam=None,
             diagram=None, labels={})
    if t < T_A:
        # O: the cold open is the end of the journey, continued past the loop point
        p['shot'] = 'O'
        p['cam'], p['exposure'] = end_view(t + DUR)
        p['bloom'] = 0.16
    elif t < T_C:
        # A + B: hover at ~26 r_s; rise until the disk is a tilted flat ring, then swing back down
        p['shot'] = 'A' if t < T_B else 'B'
        theta = kf(t, [(T_A, 82.0), (5.05, 82.0), (T_B, 83.2), (7.10, 32.0), (8.60, 32.0), (10.45, 84.4), (10.95, 82.0), (T_C, 81.0)])
        r0 = kf(t, [(T_A, 26.2), (T_B, 24.5), (7.10, 34.0), (8.60, 34.0), (10.67, 24.0), (T_C, 20.5)])
        vfov = kf(t, [(T_A, 46.2), (T_B, 47.5), (7.10, 60.0)])
        az = kf(t, [(T_A, 0.0), (7.1, 1.5), (8.6, 4.0), (10.67, 5.0), (T_C, 7.0)])
        roll = 0.6 * math.sin(t * 0.45)
        P = pos(theta, az)
        F, U = look_at_hole(P, theta, az, vfov, HOLE_Y, roll)
        p['cam'] = Cam(r0, P, F, U, vfov)
        p['tint'] = kf(t, [(7.05, 0.0), (7.45, 1.0), (13.5, 1.0), (15.2, 0.0)])
        # label anchors on the disk (unlensed projection is close enough at this distance)
        cam = p['cam']
        far = np.array([0.0, 7.5, 0.0]); near = np.array([0.0, -5.0, 0.0])
        far = rotate(far, [0, 0, 1], math.radians(az)); near = rotate(near, [0, 0, 1], math.radians(az))
        p['labels'] = dict(back=cam.project(far - r0 * P), front=cam.project(near - r0 * P))
    elif t < T_D:
        # C: the dive, 20.5 -> 1.5 r_s, turning from "hole ahead" to "hole below"
        p['shot'] = 'C'
        s = seg(t, T_C, T_D)
        lr = math.log(20.5) + (math.log(1.5) - math.log(20.5)) * ease(s)
        r0 = math.exp(lr)
        theta = 81.0 + (60.0 - 81.0) * ease(s)
        az = 7.0 + 3.0 * s
        P = pos(theta, az)
        Fa, Ua = look_at_hole(P, theta, az, 60.0, HOLE_Y)
        Fb, Ub = tangent_view(P, az, 0.0)
        q = slerp(quat_from_basis(None, Ua, Fa), quat_from_basis(None, Ub, Fb), ease(seg(s, 0.12, 0.96)))
        R, U, F = quat_to_basis(q)
        p['cam'] = Cam(r0, P, F, U, 60.0)
        p['exposure'] = kf(t, [(T_C, 0.55), (T_D, 0.5)])
    elif t < T_E:
        # D: hovering at the photon sphere, looking along the horizon
        p['shot'] = 'D'
        az = 10.0
        P = pos(60.0, az)
        F, U = tangent_view(P, az, yaw_deg=kf(t, [(T_D, 0.0), (T_E, 6.0)], lambda x: x), roll_deg=0.4 * math.sin(t * 0.8))
        p['cam'] = Cam(1.5, P, F, U, 60.0)
        p['exposure'] = 0.5
        p['sweep'] = seg(t, 21.3, T_E)
    elif t < T_F:
        p['shot'] = 'E'
        p['diagram'] = dict(t=t)
    else:
        p['shot'] = 'F' if t < T_G else 'G'
        p['cam'], p['exposure'] = end_view(t)
        p['bloom'] = 0.09 + 0.07 * seg(t, T_F + 2.0, 31.0)
    return p
