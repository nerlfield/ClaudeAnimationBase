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

## From shots F and G

- **Perf: desk() frames cost about 2× stage frames, and zoomed desk frames 1.5–2× more again.** In the same runs, under
  the shared load (load average 9–12 on 4 cores, so absolute numbers are inflated): F (stage) 1.4–3.7 s; G at zoom
  ~1 5.6–8.5 s; A's own desk frame (4.4) 6.8–10.9 s; G at zoom 1.9–3 (its pull-back out of the Up button and its push
  into the ticker) 11–17 s; A's push at zoom 5–9 (5.15, 5.25) 22–23 s. Cost scales with zoom for the whole frame (the
  same F frame: 2.9–3.6 s empty, 4–5.5 s at zoom 1.2, 10–19 s at zoom 4.5), because every wash and stroke covers more
  pixels. Removing any single element made no measurable difference. Each glow() costs about 0.1–0.2 s.
  Proposed: (1) cull off-screen pieces inside desk() (B/C's `onScreen`). (2) Bake the desk's static parts (both
  screens' bezels, faces and scan lines, the desk slab and edge, the mug, the cable) into a plate like the room, so a
  desk frame paints only the card, the ticker line, the lettering and the trader. (3) Keep deep pushes to 2 or 3 frames
  above zoom ~2 and put them under the seam colour. F and G do this: F's last two frames are solid C.up, G's first
  frame is solid C.up, and G's last three frames are solid C.panel.
- **sets.js `desk()`: the screens' lettering lands on top of the trader.** txt()/pill() lettering is composited after the
  whole frame, so when you() overlaps the card (G's leap onto the ticker's top bezel), "38¢" is painted over its body.
  G calls `flushLetters()` right after `desk(..., { hide: 1 })` and draws you() itself. Proposed: call `flushLetters()`
  in desk() just before the trader is drawn (A's trader stands clear of the text, so it doesn't show there yet).
