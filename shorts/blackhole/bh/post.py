"""Film-style post: bloom, tone mapping, chromatic fringe, vignette, grain.  Pure functions of the input."""
import numpy as np
import cv2


def bloom(hdr, strength=0.08, radii=(3, 9, 27, 81)):
    """Energy-weighted glow from several blur scales, computed on downsampled copies for speed."""
    h, w = hdr.shape[:2]
    acc = np.zeros_like(hdr)
    wsum = 0.0
    for i, r in enumerate(radii):
        f = max(1, r // 3)
        small = cv2.resize(hdr, (max(1, w // f), max(1, h // f)), interpolation=cv2.INTER_AREA)
        sig = r / f
        k = int(sig * 3) * 2 + 1
        small = cv2.GaussianBlur(small, (k, k), sig)
        acc += cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR) * (1.0 / (i + 1))
        wsum += 1.0 / (i + 1)
    return hdr * (1.0 - strength) + acc * (strength / wsum)


def aces(x):
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0)


def srgb(x):
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.maximum(x, 0), 1 / 2.4) - 0.055)


def chroma(img, amt=0.0012):
    """Radial red/blue fringe that grows toward the edges."""
    h, w = img.shape[:2]
    out = img.copy()
    for c, s in ((0, 1 + amt), (2, 1 - amt)):
        M = np.float32([[s, 0, (1 - s) * w / 2], [0, s, (1 - s) * h / 2]])
        out[..., c] = cv2.warpAffine(img[..., c], M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out


def vignette(img, strength=0.22):
    h, w = img.shape[:2]
    y, x = np.ogrid[:h, :w]
    d = ((x - w / 2) / (w / 2)) ** 2 * 0.6 + ((y - h * 0.45) / (h / 2)) ** 2
    v = 1.0 - strength * np.clip(d, 0, 1.6) / 1.6
    return img * v[..., None].astype(np.float32)


def grain(img, seed, amt=0.022):
    rng = np.random.default_rng(seed)
    h, w = img.shape[:2]
    n = rng.standard_normal((h // 2 + 1, w // 2 + 1)).astype(np.float32)
    n = cv2.resize(n, (w, h), interpolation=cv2.INTER_LINEAR)
    lum = img.mean(axis=2, keepdims=True)
    # grain is strongest in the mids, still present in the blacks (so black never goes flat)
    wgt = 0.35 + 0.65 * np.sqrt(np.clip(lum, 0, 1)) * (1.2 - np.clip(lum, 0, 1))
    return img + n[..., None] * amt * wgt


def tonemap(x, desat=0.35):
    """Hue-preserving filmic curve on luminance, with a gentle roll to white in the brightest highlights."""
    L = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
    Lm = aces(L)
    k = (Lm / np.maximum(L, 1e-8))[..., None]
    y = x * k
    # highlights (Lm > 0.6) drift toward white like film, keeping hue in the mids
    w = (np.clip((Lm - 0.6) / 0.4, 0, 1) ** 2 * desat)[..., None]
    y = y * (1 - w) + Lm[..., None] * w
    return np.clip(y, 0, 1)


def finish(hdr, exposure=1.0, bloom_amt=0.08, seed=0, grain_amt=0.022, vig=0.22, ca=0.0012, lift=0.0):
    x = bloom(hdr.astype(np.float32) * exposure, bloom_amt)
    x = tonemap(x)
    x = srgb(x).astype(np.float32)
    if lift:
        x = x + lift * (1 - x)
    if ca:
        x = chroma(x, ca)
    x = vignette(x, vig)
    x = grain(x, seed, grain_amt)
    return np.clip(x, 0, 1)
