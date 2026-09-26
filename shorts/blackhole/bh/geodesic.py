"""Null geodesics of the Schwarzschild metric for a static (hovering) observer.

Units: Schwarzschild radius r_s = 1, c = 1 (so GM = 1/2).

A ray leaving the camera at radius r0, at angle psi from the outward radial direction, stays in the
plane spanned by the radial direction e1 and its tangential direction e2.  In that plane its path is
u(phi) = 1/r(phi) with   u'' = -u + 1.5 u^2,   u(0) = 1/r0,   u'(0) = -sqrt(1 - 1/r0) cos(psi) / (r0 sin(psi)).

For every frame we tabulate u(phi) for a fan of psi values, dense near the critical angle where rays
wind around the photon sphere.  Pixels then only look things up in the table.
"""
import math
import numpy as np
import numba as nb

B_CRIT = 1.5 * math.sqrt(3.0)       # critical impact parameter 3*sqrt(3)/2 r_s
PHI_MAX = 6.0 * math.pi             # rays still orbiting after 3 turns are treated as captured
MAX_STEPS = 2600


def psi_crit(r0):
    """Angle from the outward radial direction that separates escaping from captured rays."""
    s = min(1.0, B_CRIT * math.sqrt(max(0.0, 1.0 - 1.0 / r0)) / r0)
    a = math.asin(s)
    return math.pi - a if r0 > 1.5 else a


class Table:
    """psi-fan of traced rays for one camera radius."""

    def __init__(self, r0, n=4096, k=10.0):
        self.r0, self.n, self.k = r0, n, k
        self.pc = psi_crit(r0)
        s = np.linspace(-1.0, 1.0, n)
        self.psi = psi_of_s(s, self.pc, k)
        self.phi = np.zeros((n, MAX_STEPS), np.float32)
        self.u = np.zeros((n, MAX_STEPS), np.float32)
        self.cnt = np.zeros(n, np.int32)
        self.status = np.zeros(n, np.int8)      # 0 escaped, 1 captured
        self.phi_end = np.zeros(n, np.float64)
        trace_fan(r0, self.psi, self.phi, self.u, self.cnt, self.status, self.phi_end)


def psi_of_s(s, pc, k):
    """Map s in [-1, 1] to psi in [0, pi], clustering samples exponentially around pc."""
    s = np.asarray(s, np.float64)
    a = (np.exp(k * np.abs(s)) - 1.0) / (math.exp(k) - 1.0)
    return np.where(s < 0, pc - a * pc, pc + a * (math.pi - pc))


@nb.njit(cache=True, fastmath=False)
def _deriv(u, du):
    return du, -u + 1.5 * u * u


@nb.njit(cache=True)
def trace_one(r0, psi, phis, us):
    """Trace one ray; fill phis/us; return (count, status, phi_end)."""
    sp, cp = math.sin(psi), math.cos(psi)
    u = 1.0 / r0
    if sp < 1e-9:                                   # radial ray
        phis[0] = 0.0; us[0] = u
        if cp > 0:
            phis[1] = 0.0; us[1] = 0.0
            return 2, 0, 0.0
        phis[1] = 0.0; us[1] = 1.0
        return 2, 1, 0.0
    du = -math.sqrt(1.0 - 1.0 / r0) * cp / (r0 * sp)
    phi = 0.0
    n = 0
    phis[0] = 0.0; us[0] = u; n = 1
    while True:
        h = 0.01
        lim = 0.004 / (abs(du) + 1e-12)
        if lim < h:
            h = lim
        if h < 1e-7:
            h = 1e-7
        k1u, k1d = _deriv(u, du)
        k2u, k2d = _deriv(u + 0.5 * h * k1u, du + 0.5 * h * k1d)
        k3u, k3d = _deriv(u + 0.5 * h * k2u, du + 0.5 * h * k2d)
        k4u, k4d = _deriv(u + h * k3u, du + h * k3d)
        un = u + h / 6.0 * (k1u + 2 * k2u + 2 * k3u + k4u)
        dn = du + h / 6.0 * (k1d + 2 * k2d + 2 * k3d + k4d)
        if un <= 0.0:                               # escaped: interpolate the zero crossing
            pe = phi + h * u / (u - un)
            phis[n] = pe; us[n] = 0.0
            return n + 1, 0, pe
        if un >= 1.0:                               # crossed the horizon
            pe = phi + h * (1.0 - u) / (un - u)
            phis[n] = pe; us[n] = 1.0
            return n + 1, 1, pe
        phi += h
        u, du = un, dn
        if n < phis.shape[0] - 1:
            phis[n] = phi; us[n] = u; n += 1
        else:                                       # out of storage: keep the last sample moving
            phis[n - 1] = phi; us[n - 1] = u
        if phi > PHI_MAX:
            return n, 1, phi


@nb.njit(parallel=True, cache=True)
def trace_fan(r0, psis, phi, u, cnt, status, phi_end):
    for i in nb.prange(psis.shape[0]):
        c, s, pe = trace_one(r0, psis[i], phi[i], u[i])
        cnt[i] = c; status[i] = s; phi_end[i] = pe


def escape_half_angle_deg(r0):
    """Half-angle of the escape cone for a static observer (Synge 1966), in degrees."""
    s = min(1.0, B_CRIT * math.sqrt(max(0.0, 1.0 - 1.0 / r0)) / r0)
    a = math.degrees(math.asin(s))
    return 180.0 - a if r0 > 1.5 else a
