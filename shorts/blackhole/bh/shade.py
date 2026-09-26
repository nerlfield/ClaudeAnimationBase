"""Per-pixel shading: camera rays -> geodesic table lookups -> disk emission + lensed sky.

Everything here is a pure function of its inputs (camera, table, time), so frames render in any order.
"""
import math
import numpy as np
import numba as nb

# ---------------------------------------------------------------- colour helpers

def _bb_srgb(T):
    """Approximate sRGB of a blackbody (Tanner Helland fit), 0..1, gamma-encoded."""
    t = T / 100.0
    if t <= 66:
        r = 255.0
        g = 99.4708025861 * math.log(t) - 161.1195681661
        b = 0.0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307
    else:
        r = 329.698727446 * (t - 60) ** -0.1332047592
        g = 288.1221695283 * (t - 60) ** -0.0755148492
        b = 255.0
    return [min(255.0, max(0.0, c)) / 255.0 for c in (r, g, b)]


def make_bb_table(n=512, tmin=1000.0, tmax=40000.0):
    """Linear-light blackbody chromaticity (luminance normalised to 1), indexed by log T."""
    tab = np.zeros((n, 3), np.float32)
    for i in range(n):
        T = tmin * (tmax / tmin) ** (i / (n - 1))
        c = np.array(_bb_srgb(T)) ** 2.2
        lum = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
        tab[i] = c / max(lum, 1e-6)
    return tab


BB = make_bb_table()
BB_LOGMIN, BB_LOGMAX = math.log(1000.0), math.log(40000.0)


@nb.njit(cache=True, inline='always')
def bb(T, tab):
    x = (math.log(max(T, 1000.0)) - BB_LOGMIN) / (BB_LOGMAX - BB_LOGMIN)
    x = min(max(x, 0.0), 1.0) * (tab.shape[0] - 1)
    i = int(x)
    if i >= tab.shape[0] - 1:
        i = tab.shape[0] - 2
    f = x - i
    return (tab[i, 0] * (1 - f) + tab[i + 1, 0] * f,
            tab[i, 1] * (1 - f) + tab[i + 1, 1] * f,
            tab[i, 2] * (1 - f) + tab[i + 1, 2] * f)


# ---------------------------------------------------------------- noise

@nb.njit(cache=True, inline='always')
def hash3(i, j, k):
    h = (i * 73856093) ^ (j * 19349663) ^ (k * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF) / 16777216.0


@nb.njit(cache=True, inline='always')
def _fade(t):
    return t * t * (3.0 - 2.0 * t)


@nb.njit(cache=True)
def vnoise(x, y, z):
    ix, iy, iz = math.floor(x), math.floor(y), math.floor(z)
    fx, fy, fz = x - ix, y - iy, z - iz
    ix, iy, iz = int(ix), int(iy), int(iz)
    ux, uy, uz = _fade(fx), _fade(fy), _fade(fz)
    a = hash3(ix, iy, iz); b = hash3(ix + 1, iy, iz)
    c = hash3(ix, iy + 1, iz); d = hash3(ix + 1, iy + 1, iz)
    e = hash3(ix, iy, iz + 1); f = hash3(ix + 1, iy, iz + 1)
    g = hash3(ix, iy + 1, iz + 1); h = hash3(ix + 1, iy + 1, iz + 1)
    x1 = a + (b - a) * ux; x2 = c + (d - c) * ux; x3 = e + (f - e) * ux; x4 = g + (h - g) * ux
    y1 = x1 + (x2 - x1) * uy; y2 = x3 + (x4 - x3) * uy
    return y1 + (y2 - y1) * uz


@nb.njit(cache=True)
def fbm(x, y, z, octaves):
    s = 0.0; a = 0.5; f = 1.0; norm = 0.0
    for _ in range(octaves):
        s += a * vnoise(x * f, y * f, z * f)
        norm += a; a *= 0.5; f *= 2.03
    return s / norm


# ---------------------------------------------------------------- sky

@nb.njit(cache=True)
def _face(nx, ny, nz):
    ax, ay, az = abs(nx), abs(ny), abs(nz)
    if ax >= ay and ax >= az:
        return (0 if nx > 0 else 1), ny / ax, nz / ax
    if ay >= az:
        return (2 if ny > 0 else 3), nx / ay, nz / ay
    return (4 if nz > 0 else 5), nx / az, ny / az


@nb.njit(cache=True)
def _unface(f, a, b):
    if f == 0: x, y, z = 1.0, a, b
    elif f == 1: x, y, z = -1.0, a, b
    elif f == 2: x, y, z = a, 1.0, b
    elif f == 3: x, y, z = a, -1.0, b
    elif f == 4: x, y, z = a, b, 1.0
    else: x, y, z = a, b, -1.0
    n = math.sqrt(x * x + y * y + z * z)
    return x / n, y / n, z / n


@nb.njit(cache=True)
def stars(nx, ny, nz, trx, tr_y, trz, ttx, tty, ttz, jr, jt, sigma, tab):
    f, a, b = _face(nx, ny, nz)
    r = 0.0; g = 0.0; bl = 0.0
    for layer in range(3):
        if layer == 0:
            G = 13; dens = 0.30; bmin = 5.0; pw = 1.5
        elif layer == 1:
            G = 48; dens = 0.32; bmin = 0.9; pw = 1.2
        else:
            G = 150; dens = 0.34; bmin = 0.22; pw = 1.0
        ca = (a + 1.0) * 0.5 * G; cb = (b + 1.0) * 0.5 * G
        ia, ib = int(math.floor(ca)), int(math.floor(cb))
        for di in range(-1, 2):
            for dj in range(-1, 2):
                i, j = ia + di, ib + dj
                if i < 0 or j < 0 or i >= G or j >= G:
                    continue
                seed = f * 1000003 + layer * 7919
                h0 = hash3(i, j, seed)
                if h0 > dens:
                    continue
                sa = (i + 0.15 + 0.7 * hash3(i, j, seed + 1)) / G * 2.0 - 1.0
                sb = (j + 0.15 + 0.7 * hash3(i, j, seed + 2)) / G * 2.0 - 1.0
                sx, sy, sz = _unface(f, sa, sb)
                ox, oy, oz = sx - nx, sy - ny, sz - nz
                dr = (ox * trx + oy * tr_y + oz * trz) / jr      # offsets mapped back to image space
                dt = (ox * ttx + oy * tty + oz * ttz) / jt
                d2 = dr * dr + dt * dt
                s2 = sigma * sigma
                if d2 > 60.0 * s2:
                    continue
                h3 = hash3(i, j, seed + 3)
                bright = bmin * (1.0 / (0.02 + h3)) ** pw * 0.08
                T = 2800.0 + 11000.0 * hash3(i, j, seed + 4) ** 2
                cr, cg, cb2 = bb(T, tab)
                mu = min(25.0, 1.0 / max(1e-6, jr * jt))           # point sources get brighter, not bigger
                w = mu * bright * (math.exp(-d2 / (2.0 * s2)) + 0.012 * math.exp(-d2 / (2.0 * 25.0 * s2)))
                r += w * cr; g += w * cg; bl += w * cb2
    return r, g, bl


@nb.njit(cache=True)
def sky(nx, ny, nz, trx, tr_y, trz, ttx, tty, ttz, jr, jt, sigma, tab, shift):
    """Lensed-sky radiance for escape direction n.  shift = frequency ratio seen by the observer."""
    r, g, b = stars(nx, ny, nz, trx, tr_y, trz, ttx, tty, ttz, jr, jt, sigma, tab)
    # Milky Way band: a great circle tilted across the scene, with dust lanes
    mx, my, mz = 0.552, 0.080, 0.830
    lat = nx * mx + ny * my + nz * mz
    band = math.exp(-(lat * lat) / 0.018)
    if band > 0.002:
        cloud = fbm(nx * 3.1 + 11.0, ny * 3.1 - 4.0, nz * 3.1 + 7.0, 5)
        dust = fbm(nx * 7.0 - 3.0, ny * 7.0 + 9.0, nz * 7.0 + 1.0, 4)
        dens = band * (0.35 + 1.1 * cloud * cloud) * (1.0 - 0.75 * max(0.0, dust - 0.45) * 2.2)
        dens = max(dens, 0.0)
        # indigo body, warm core where denser
        warm = min(1.0, max(0.0, (cloud - 0.55) * 3.0)) * band
        r += dens * (0.030 + 0.050 * warm); g += dens * (0.034 + 0.030 * warm); b += dens * (0.085 + 0.012 * warm)
        # faint unresolved stars in the band
        grain = hash3(int(nx * 2400.0), int(ny * 2400.0), int(nz * 2400.0))
        r += band * grain * 0.010; g += band * grain * 0.011; b += band * grain * 0.014
    # base void #05070D-ish plus a very faint nebula wash
    neb = fbm(nx * 1.6 - 2.0, ny * 1.6 + 5.0, nz * 1.6, 3)
    r += 0.0016 + 0.004 * neb * neb; g += 0.0021 + 0.003 * neb * neb; b += 0.0045 + 0.010 * neb * neb
    # mean surface brightness of unresolved starlight (conserved under lensing; matters once the sky is compressed)
    r += 0.0030; g += 0.0034; b += 0.0042
    if shift != 1.0:
        # blueshift: brighter, and colours pushed toward ice
        k = min(1.0, max(0.0, (shift - 1.0) / 6.0))
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        boost = shift ** 4          # same g^4 law as the disk
        r = (r * (1 - k) + lum * 0.62 * k) * boost
        g = (g * (1 - k) + lum * 0.86 * k) * boost
        b = (b * (1 - k) + lum * 1.35 * k) * boost
    return r, g, b


# ---------------------------------------------------------------- disk

@nb.njit(cache=True)
def disk_emit(x, y, r, g, t, rin, rout, tab, tint, spin_rate):
    """Emission (rgb) and opacity of the thin disk at plane point (x, y), radius r, frequency ratio g."""
    if r < rin or r > rout:
        return 0.0, 0.0, 0.0, 0.0
    # Novikov-Thorne-like flux profile (Newtonian thin disk)
    q = rin / r
    flux = (q ** 3) * max(0.0, 1.0 - math.sqrt(q))
    flux /= 0.0567  # peak = 1 at r = 1.36 rin (q = 36/49)
    Tv = 1450.0 + 2700.0 * flux ** 0.4       # visible-range temperature map (ember rim, gold core)
    # Keplerian shear: pattern angle advances by Omega(r) * time
    om = math.sqrt(0.5 / (r * r * r))
    ang = math.atan2(y, x) - om * t * spin_rate
    ca, sa = math.cos(ang), math.sin(ang)
    lr = math.log(r)
    turb = fbm(ca * 2.2, sa * 2.2, lr * 5.5, 5)
    streak = fbm(ca * 7.0, sa * 7.0, lr * 34.0, 4)            # thin filaments along the orbit
    rings = 0.5 + 0.5 * math.sin(lr * 58.0 + 6.0 * turb)       # fine ringlets in radius
    clump = fbm(ca * 4.0 + 13.0, sa * 4.0, lr * 9.0 + 3.0, 3)
    tex = 0.18 + 1.2 * turb * turb + 0.9 * streak ** 3 * 3.0 * (0.6 + 0.4 * rings) + 1.4 * max(0.0, clump - 0.55) ** 2 * 4.0
    edge = min(1.0, (r - rin) / 0.35) * min(1.0, max(0.0, (rout - r) / (0.35 * rout)))
    inten = flux * tex * edge * (g ** 4) * 2.2
    cr, cg, cb = bb(Tv * g, tab)
    if tint > 0.0:
        w = tint * min(1.0, max(0.0, (y + 0.6) / 1.2))
        cr = cr * (1 - w) + 0.22 * w; cg = cg * (1 - w) + 0.80 * w; cb = cb * (1 - w) + 1.75 * w
    alpha = min(0.97, 0.55 + 0.6 * turb) * edge
    return inten * cr, inten * cg, inten * cb, alpha


# ---------------------------------------------------------------- the kernel

@nb.njit(cache=True, inline='always')
def _row_u(phi_row, u_row, cnt, st, phic):
    """u at angle phic along a traced row: 1 if captured before, 0 if escaped before."""
    if phic > phi_row[cnt - 1]:
        return 1.0 if st == 1 else 0.0
    lo, hi = 0, cnt - 1
    while hi - lo > 1:
        m = (lo + hi) >> 1
        if phi_row[m] <= phic:
            lo = m
        else:
            hi = m
    p0, p1 = phi_row[lo], phi_row[hi]
    w = 0.0 if p1 <= p0 else (phic - p0) / (p1 - p0)
    return u_row[lo] * (1 - w) + u_row[hi] * w


@nb.njit(parallel=True, cache=True, fastmath=True)
def render(out, W, H, x0, y0, spp, P, F, R, U, tx, ty,
           psi_tab, phi_tab, u_tab, cnt, status, phi_end, pc, kmap, r0,
           t, rin, rout, tab, tint, spin_rate, disk_gain, sky_gain, spin_sign, star_sigma):
    """Render rows y0..y0+out.shape[0] of a W x H frame into out (h, w, 3) linear HDR."""
    n = psi_tab.shape[0]
    ek1 = math.exp(kmap) - 1.0
    sq0 = math.sqrt(1.0 - 1.0 / r0)
    gsky = 1.0 / sq0
    for yy in nb.prange(out.shape[0]):
        py = y0 + yy
        for xx in range(out.shape[1]):
            px = x0 + xx
            ar = 0.0; ag = 0.0; ab = 0.0
            for s in range(spp.shape[0]):
                xn = ((px + spp[s, 0]) / W) * 2.0 - 1.0
                yn = 1.0 - ((py + spp[s, 1]) / H) * 2.0
                dx = F[0] + xn * tx * R[0] + yn * ty * U[0]
                dy = F[1] + xn * tx * R[1] + yn * ty * U[1]
                dz = F[2] + xn * tx * R[2] + yn * ty * U[2]
                dn = math.sqrt(dx * dx + dy * dy + dz * dz)
                dx /= dn; dy /= dn; dz /= dn
                cp = dx * P[0] + dy * P[1] + dz * P[2]
                cp = min(1.0, max(-1.0, cp))
                psi = math.acos(cp)
                # in-plane tangential basis
                e2x = dx - cp * P[0]; e2y = dy - cp * P[1]; e2z = dz - cp * P[2]
                l2 = math.sqrt(e2x * e2x + e2y * e2y + e2z * e2z)
                if l2 < 1e-9:
                    # radial ray: pick any perpendicular
                    if abs(P[2]) < 0.9:
                        e2x, e2y, e2z = -P[1], P[0], 0.0
                    else:
                        e2x, e2y, e2z = 0.0, -P[2], P[1]
                    l2 = math.sqrt(e2x * e2x + e2y * e2y + e2z * e2z)
                e2x /= l2; e2y /= l2; e2z /= l2
                # table coordinate
                if psi < pc:
                    a = (pc - psi) / pc
                    sgn = -1.0
                else:
                    a = (psi - pc) / (math.pi - pc)
                    sgn = 1.0
                sv = sgn * math.log(1.0 + a * ek1) / kmap
                fi = (sv + 1.0) * 0.5 * (n - 1)
                i0 = int(fi)
                if i0 >= n - 1:
                    i0 = n - 2
                if i0 < 0:
                    i0 = 0
                wi = fi - i0
                i1 = i0 + 1
                # impact parameter and photon angular momentum (physical photon, per unit energy)
                b = r0 * math.sin(psi) / sq0
                nzp = P[0] * e2y - P[1] * e2x      # z of e1 x e2
                Lz = -b * nzp * spin_sign
                # disk crossings: z(phi) = cos(phi) P_z + sin(phi) e2z = 0
                pend = phi_end[i0] * (1 - wi) + phi_end[i1] * wi
                pmax = max(phi_end[i0], phi_end[i1])
                cr = 0.0; cg = 0.0; cb = 0.0; trans = 1.0
                blocked = False
                if abs(P[2]) > 1e-12 or abs(e2z) > 1e-12:
                    ph0 = math.atan2(-P[2], e2z)
                    if ph0 < 0:
                        ph0 += math.pi
                    kk = 0
                    while kk < 8:
                        phc = ph0 + kk * math.pi
                        kk += 1
                        if phc > pmax:
                            break
                        u0 = _row_u(phi_tab[i0], u_tab[i0], cnt[i0], status[i0], phc)
                        u1 = _row_u(phi_tab[i1], u_tab[i1], cnt[i1], status[i1], phc)
                        u = u0 * (1 - wi) + u1 * wi
                        if u >= 0.999:
                            blocked = True
                            break
                        if u <= 1e-6:
                            break
                        rr = 1.0 / u
                        if rr < rin or rr > rout:
                            continue
                        cph, sph = math.cos(phc), math.sin(phc)
                        X = rr * (cph * P[0] + sph * e2x)
                        Y = rr * (cph * P[1] + sph * e2y)
                        ut = 1.0 / math.sqrt(max(1e-6, 1.0 - 1.5 / rr))
                        om = math.sqrt(0.5 / (rr * rr * rr))
                        g = 1.0 / (sq0 * ut * (1.0 - om * Lz))
                        er, eg, eb, al = disk_emit(X, Y, rr, g, t, rin, rout, tab, tint, spin_rate * spin_sign)
                        cr += trans * al * er * disk_gain
                        cg += trans * al * eg * disk_gain
                        cb += trans * al * eb * disk_gain
                        trans *= (1.0 - al)
                        if trans < 0.01:
                            break
                # what lies beyond: sky or horizon
                if trans > 0.01 and not blocked:
                    esc = (1.0 - status[i0]) * (1 - wi) + (1.0 - status[i1]) * wi
                    if esc > 0.0:
                        if status[i0] == 0 and status[i1] == 0:
                            pe = pend
                        elif status[i0] == 0:
                            pe = phi_end[i0]
                        else:
                            pe = phi_end[i1]
                        cph, sph = math.cos(pe), math.sin(pe)
                        nx = cph * P[0] + sph * e2x
                        ny = cph * P[1] + sph * e2y
                        nz = cph * P[2] + sph * e2z
                        # lens Jacobian: radial stretch dPhi/dpsi, tangential sin(Phi)/sin(psi)
                        dps = psi_tab[i1] - psi_tab[i0]
                        jr = 1.0
                        if dps > 1e-12 and status[i0] == 0 and status[i1] == 0:
                            jr = abs((phi_end[i1] - phi_end[i0]) / dps)
                        jr = max(jr, 0.02)
                        spsi = max(math.sin(psi), 1e-6)
                        jt = max(abs(sph) / spsi, 0.02) if spsi > 1e-4 else 1.0
                        trx = -sph * P[0] + cph * e2x; tr_y = -sph * P[1] + cph * e2y; trz = -sph * P[2] + cph * e2z
                        ttx = P[1] * e2z - P[2] * e2y; tty = P[2] * e2x - P[0] * e2z; ttz = P[0] * e2y - P[1] * e2x
                        sr, sg, sb = sky(nx, ny, nz, trx, tr_y, trz, ttx, tty, ttz, jr, jt, star_sigma, tab, gsky)
                        cr += trans * esc * sr * sky_gain
                        cg += trans * esc * sg * sky_gain
                        cb += trans * esc * sb * sky_gain
                ar += cr; ag += cg; ab += cb
            inv = 1.0 / spp.shape[0]
            out[yy, xx, 0] = ar * inv
            out[yy, xx, 1] = ag * inv
            out[yy, xx, 2] = ab * inv
