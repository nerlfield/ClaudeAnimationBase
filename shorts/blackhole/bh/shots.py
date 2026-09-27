"""The video's timeline: camera and render parameters as pure functions of video time t (seconds).

Two clocks.  The animation was built on a 43.33 s "story" clock (bars at 90 BPM; the T_* times and every keyframe
below are story times).  Since round 11 the video runs 74.67 s around a slower, plainer narration, so state(t)
takes VIDEO time and maps it to story time through WARP: holds stretch to fit the lines about them, a camera move
finishes before the line about its result starts, and cuts land where the words need them.
"""
import math
import numpy as np

from .frame import Cam, norm, rotate
from .geodesic import B_CRIT

BPM = 90.0
BAR = 4 * 60.0 / BPM
STORY_DUR = 65 * BAR / 4           # the animation's own clock: 43.333 s (the whole video until round 10)
DUR = 112 * BAR / 4                 # 74.667 s = 112 beats: the video since round 11, re-timed around the narration
FPS = 30
N_FRAMES = int(round(DUR * FPS))   # 2240

# shot boundaries (v2 storyboard)
T_A, T_B, T_C, T_D, T_E, T_F, T_G = BAR, 2 * BAR, 6 * BAR, 7 * BAR, 22.2, 10 * BAR, 12 * BAR
T_E2 = 24.55                      # E2: first person again, the line opens into the back of your own head
HOLE_Y = 0.42                      # the black hole (and the final dot) sit at 42% of frame height

# video time -> story time, knot by knot, read off the placed narration (build/words.json, round 11):
WARP = [
    (0.00, 0.000),
    (5.35, T_A),      # the black hole appears just after "Let me show you why."
    (11.55, 5.05),    # A holds through "This is a black hole. And this bright ring is hot gas, spinning around it."
    (12.05, T_B),     # "Let's look at it from above." ... the rise starts as the sentence ends
    (14.00, 7.10),    # the rise is over before "See? The disk is actually flat." (14.3)
    (17.80, 7.50),    # the back half turns ice on "This is the *back half" (tint 7.50 -> 7.80)
    (18.20, 7.80),
    (22.10, 8.60),    # the swing down starts on "as we go back down"
    (24.00, 10.67),   # the arch lands; 0.66 s of silence before "The black hole bends its light"
    (30.10, 13.50),   # the arch (ice) holds through "...and under the bottom", then fades to gold
    (31.80, T_C),     # the dive starts on "fly in"
    (34.50, T_D),     # arrival at the photon sphere, 0.5 s before "If you hover right here"
    (40.00, 21.30),   # the glow sweeps along the line on "And see this thin line?"
    (41.40, T_E),     # the line opens into the diagram's circle on "That's light, going around..."
    (42.40, 23.00),
    (48.00, 24.00),   # the light's lap ends in the visor flash on "...and come back to you."
    (48.75, T_E2),    # first person again for "So in this line,"
    (49.30, 24.90),   # the line opens...
    (50.30, 25.50),   # ...onto the back of your head for "you see the back of your own head"
    (51.60, 25.95),
    (52.20, 26.30),
    (52.80, T_F),     # pull-out done as "Now let's go lower" starts
    (56.50, 27.80),   # sinking (the bright sky shrinks) through "...hover just above the edge."
    (58.90, 29.50),   # "Then look up." ... straight up by "The whole universe shrinks"
    (62.00, T_G),     # the dot lands after "...into one small dot above you."
]
T_G_REAL = WARP[-1][0]
T_A_REAL = WARP[1][0]
# after the dot lands (and in the cold open, which continues it) the ending runs on its own steady clock, so the
# loop point joins two moments moving at the same speed
DOT_RATE = (STORY_DUR - T_G) / (DUR - T_G_REAL)
END_TAU = STORY_DUR + DOT_RATE * T_A_REAL          # the end camera's clock when the cold open cuts to A


def _slopes():
    """Monotone cubic (Fritsch-Carlson) slopes at the WARP knots; the last one matches the dot's clock."""
    x = np.array([k[0] for k in WARP]); y = np.array([k[1] for k in WARP])
    d = np.diff(y) / np.diff(x)
    m = np.empty(len(x))
    m[0] = d[0]; m[-1] = DOT_RATE
    for i in range(1, len(x) - 1):
        m[i] = 0.0 if d[i - 1] * d[i] <= 0 else 2.0 / (1.0 / d[i - 1] + 1.0 / d[i])   # harmonic mean
    return x, y, m


_WX, _WY, _WM = _slopes()


def warp(t):
    """Video time -> story time (smooth and increasing)."""
    if t >= _WX[-1]:
        return T_G + DOT_RATE * (t - _WX[-1])
    if t <= 0.0:
        return t * _WM[0]
    i = int(np.searchsorted(_WX, t)) - 1
    h = _WX[i + 1] - _WX[i]; u = (t - _WX[i]) / h
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
    return float(h00 * _WY[i] + h10 * h * _WM[i] + h01 * _WY[i + 1] + h11 * h * _WM[i + 1])


def unwarp(s):
    """Story time -> video time (bisection on warp)."""
    lo, hi = -1.0, DUR + 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if warp(mid) < s:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def dot_tau(t):
    """The end camera's clock for video time t in the cold open (first half of the video: it runs on past the
    cut while the dissolve into A still shows it) or in the ending (second half)."""
    return STORY_DUR + DOT_RATE * t if t < DUR / 2 else T_G + DOT_RATE * (t - T_G_REAL)


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
    tau runs from T_F through STORY_DUR and on past it: O at time t uses tau = t + STORY_DUR, so the loop has no seam."""
    cone = kf(tau, [(T_F, 89.9), (T_G, 4.706), (END_TAU, 4.0)], lambda x: ease(x) if tau < T_G else x)
    r0 = r_for_cone(cone) if cone < 89.9 else 1.5
    az = 10.0
    P = pos(60.0, az)
    Fa, Ua = tangent_view(P, az, 6.0)
    vfov = kf(tau, [(T_F + 0.3, 60.0), (31.0, 34.0), (END_TAU, 26.0)], lambda x: ease(x) if tau < 31.0 else x)
    Fb = P.copy(); Ub = -rotate(np.array([1.0, 0.0, 0.0]), [0, 0, 1], math.radians(az))
    Rb = np.cross(Fb, Ub)
    off = math.atan((1 - 2 * HOLE_Y) * math.tan(math.radians(vfov) / 2))
    Fb, Ub = rotate(Fb, Rb, -off), rotate(Ub, Rb, -off)
    qa = quat_from_basis(None, Ua, Fa)
    qb = quat_from_basis(None, Ub, Fb)
    q = slerp(qa, qb, ease(seg(tau, T_F, 29.5)))
    R, U, F = quat_to_basis(q)
    U = rotate(U, F, math.radians(0.35 * (tau - T_F)))
    # once the dot has formed, the sky inside it turns slowly about the radial axis: the dot stays put, its
    # stars and Milky Way keep moving through the ending and the cold open
    spin = math.radians(6.0 * max(0.0, tau - T_G))
    Pn = P / np.linalg.norm(P)
    F, U = rotate(F, Pn, spin), rotate(U, Pn, spin)
    gs = 1 / math.sqrt(1 - 1 / r0)
    glow = 1.0 + 1.8 * ease(seg(tau, 29.0, T_G))       # the finished dot glows: all the sky's light in one place
    return Cam(r0, P, F, U, vfov), 0.5 * glow / gs ** 3.3


# cuts that dissolve instead of cutting hard: (time, shot before, shot after, dissolve length in s)
DISSOLVES = [(T_A, 'O', 'A', 0.16), (T_E, 'D', 'E', 0.24), (T_E2, 'E', 'E2', 0.24)]


def group_at(t):
    """Which branch of state() owns time t."""
    if t < T_A:
        return 'O'
    if t < T_C:
        return 'AB'
    if t < T_D:
        return 'C'
    if t < T_E:
        return 'D'
    if t < T_E2:
        return 'E'
    if t < T_F:
        return 'E2'
    return 'FG'


def state(t, force=None):
    """Everything the renderer needs at VIDEO time t: a camera (or None for the diagram shot) and parameters.
    p['t'] is the story time the shot branches run on; p['t_real'] the video time.
    force: evaluate a given shot's branch ('O', 'AB', 'C', 'D', 'E', 'E2', 'FG') even outside its time range
    (used to render both sides of a dissolve)."""
    t_real, t = t, warp(t)
    p = dict(t=t, t_real=t_real, tint=0.0, exposure=0.55, disk_gain=1.0, sky_gain=1.0, shot='A', bloom=0.09, cam=None,
             diagram=None, labels={}, selfview=None)
    g = force or group_at(t)
    if g == 'O':
        # O: the cold open is the end of the journey, continued past the loop point
        p['shot'] = 'O'
        p['cam'], p['exposure'] = end_view(dot_tau(t_real))
        p['bloom'] = 0.16
        k = seg(t, T_A - 0.1, T_A)
        p['exposure'] *= 1.0 + 2.5 * k * k; p['bloom'] += 0.12 * k
    elif g == 'AB':
        # A + B: hover at ~26 r_s; rise until the disk is a tilted flat ring, then swing back down
        p['shot'] = 'A' if t < T_B else 'B'
        theta = kf(t, [(T_A, 82.0), (5.05, 82.0), (T_B, 83.2), (7.10, 32.0), (8.60, 32.0), (10.45, 84.4), (10.95, 82.0), (T_C, 81.0)])
        r0 = kf(t, [(T_A, 26.2), (T_B, 24.5), (7.10, 34.0), (8.60, 34.0), (10.67, 24.0), (T_C, 20.5)])
        vfov = kf(t, [(T_A, 35.8), (T_B, 38.0), (7.10, 60.0)])     # 35.8: the shadow matches the dot at the cut
        az = kf(t, [(T_A, 0.0), (7.1, 1.5), (8.6, 4.0), (10.67, 5.0), (T_C, 7.0)])
        roll = 0.6 * math.sin(t * 0.45)
        P = pos(theta, az)
        F, U = look_at_hole(P, theta, az, vfov, HOLE_Y, roll)
        p['cam'] = Cam(r0, P, F, U, vfov)
        fl = 1.0 - seg(t, T_A, T_A + 0.16)
        p['exposure'] = 0.55 * (1.0 + 1.6 * fl * fl); p['bloom'] = 0.09 + 0.1 * fl
        p['tint'] = kf(t, [(7.50, 0.0), (7.80, 1.0), (13.5, 1.0), (15.2, 0.0)])     # ice on "the back half"
        # label anchors on the disk (unlensed projection is close enough at this distance)
        cam = p['cam']
        far = np.array([0.0, 7.5, 0.0]); near = np.array([0.0, -5.0, 0.0])
        far = rotate(far, [0, 0, 1], math.radians(az)); near = rotate(near, [0, 0, 1], math.radians(az))
        p['labels'] = dict(back=cam.project(far - r0 * P), front=cam.project(near - r0 * P))
    elif g == 'C':
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
    elif g == 'D':
        # D: hovering at the photon sphere, looking along the horizon
        p['shot'] = 'D'
        az = 10.0
        P = pos(60.0, az)
        F, U = tangent_view(P, az, yaw_deg=kf(t, [(T_D, 0.0), (T_E, 6.0)], lambda x: x), roll_deg=0.4 * math.sin(t * 0.8))
        p['cam'] = Cam(1.5, P, F, U, 60.0)
        p['exposure'] = 0.5
        p['sweep'] = seg(t, 21.3, T_E)
    elif g == 'E':
        p['shot'] = 'E'
        p['diagram'] = dict(t=t)
    elif g == 'E2':
        # E2: back at the photon sphere in first person, with F's opening camera.  The view pushes in on the line
        # while it opens into a (magnified) image of the back of your own helmet, then snaps back out into F.
        p['shot'] = 'E2'
        cam, p['exposure'] = end_view(T_F)
        vfov = kf(t, [(T_E2, 44.0), (25.35, 30.0), (26.0, 29.5), (T_F, 60.0)],
                  lambda x: ease(x))
        # look ~3 degrees down while zoomed in, so the line (and the lens that opens from it) sits at ~40% of the
        # frame height, clear of the captions; eased out again for the hand-off to F
        a = math.radians(3.1) * min(ease(seg(t, T_E2, 25.3)), 1.0 - ease(seg(t, 26.0, T_F)))
        F2 = math.cos(a) * cam.F - math.sin(a) * cam.U
        U2 = math.sin(a) * cam.F + math.cos(a) * cam.U
        p['cam'] = Cam(cam.r0, cam.P, F2, U2, vfov)
        p['bloom'] = 0.09
        p['selfview'] = dict(open=min(ease(seg(t, 24.9, 25.5)), 1.0 - ease(seg(t, 25.95, 26.3))),
                             turn=0.45 * math.sin(math.pi * seg(t, 25.5, 25.95)))
    else:
        p['shot'] = 'F' if t < T_G else 'G'
        p['cam'], p['exposure'] = end_view(t if t_real < T_G_REAL else dot_tau(t_real))
        p['bloom'] = 0.09 + 0.07 * seg(t, T_F + 2.0, 31.0)
    return p
