# Shared bugs and requests

Shot builders: don't edit `short/src/*.js` yourselves. Append what you find here (file, what's wrong, a proposed fix),
and work around it inside your own shot file meanwhile.


## From shots B and C

- **look.js `motes()`: no opacity.** Motes can't fade out before a seam that must show "nothing else" (C→D), so they
  pop. Proposed: `motes(t, n, box, col, a = 1)` with `washOp: (60 + 80 * tw) * a`. B.js/C.js use a local copy (`dust`).
- **look.js `half()` / `coin()`: `k` can't shrink an object away cleanly.** `r *= backOut(k)` swells to ~1.12 before it
  shrinks when k runs 1 → 0, and `half(..., { crumble: 1 })` still leaves the full-size ash body on screen. Proposed: an
  `o.s` scale (no overshoot) and `crumble` fading the body out past ~0.8. B/C wrap the calls in `push/scale` instead.
- **sets.js `book()` with `rows: 0` still paints the 96 px panel at full size**, so a book can't pop in from its header
  (`header` only scales the green/red bar). C.js scales the whole book about the header centre for the pop.
- **Perf (all shots): strokes cost even when they're off-screen at high zoom.** In B's pull-out from 6.5x, the clock
  ring, the marker's ₿ strokes and the dashed line (all out of view) made the first frames ~2.5x the cost of a normal
  frame; skipping anything off-screen fixed it. Proposed shared helper (B.js has it locally):
  `const onScreen = (x, y, r) => { if (!CAM) return true; const [sx, sy] = toScreen(x, y), rr = r * CAM.zoom; return sx > -rr && sx < W + rr && sy > -rr && sy < H + rr; };`
