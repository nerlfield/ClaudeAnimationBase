"""Check every caption and label against the Shorts safe zone, every 0.1 s.

Text and arrows must stay out of the bottom 20% (title, channel, audio row) and out of the right-hand
column where the like/comment/share buttons sit (x > 87% of the width, below 40% of the height).
Prints each violation window and exits 1 if there are any.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from bh import shots, diagram, overlay as ov, timeline_overlay as tov  # noqa: E402

W, H = ov.W, ov.H
BOTTOM = 0.80 * H
RIGHT_X, RIGHT_Y = 0.87 * W, 0.40 * H


def alpha_at(t):
    st = shots.state(t)
    you = diagram.you_px(st['t']) if st['diagram'] is not None else None
    base = ov._layer()
    for l in tov.layers(t, you, st):
        if l is not None:
            base.alpha_composite(l)
    return np.asarray(base)[..., 3] > 40


def main():
    bad = []
    for t in np.arange(0, shots.DUR, 0.1):
        a = alpha_at(float(t))
        ys, xs = np.nonzero(a)
        if not len(ys):
            continue
        low = ys >= BOTTOM
        right = (xs >= RIGHT_X) & (ys >= RIGHT_Y)
        if low.any() or right.any():
            why = []
            if low.any():
                why.append('bottom: y up to %.3f H' % (ys[low].max() / H))
            if right.any():
                why.append('right: x up to %.3f W at y %d-%d' % (xs[right].max() / W, ys[right].min(), ys[right].max()))
            bad.append((t, '; '.join(why)))
    for t, why in bad:
        print('%5.1f s  %s' % (t, why))
    print('%d violations' % len(bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
