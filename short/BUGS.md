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

## From shots H and I

- **The I→A contract leaves out two things A passes at t = 0.** The seam table says `desk(t, { card: HOOK0.card, fn, lo,
  hi, hide: 1, named: 0 })`, but A.js's frame 0 also has `upGlow: 1` (`exp(-max(0, t - tLand) * 1.5)` is 1 before the
  landing) and `tickGlow: .6`. I.js matches A's actual frame (it passes both, and calls desk(t − 65.6) and
  cam(t − 65.6, …HOOK0.cam) so the room drift, the ticker and the camera drift line up too). Proposed: put them in HOOK0
  (e.g. `HOOK0.set = { upGlow: 1, tickGlow: .6 }`) so the table and A agree.
- **sets.js `desk()`: `hide` doesn't hide.** The trader is drawn after the desk slab, so for 0 < hide < 1 it slides down
  in front of the desk (A's pop-up at 3.57–3.73 rises from in front of it). I.js sinks the trader behind the desk by
  repainting the slab's front over it (same boil seed and edge stroke). Proposed: draw the trader before the slab.
- **Perf: a wash costs ~15–40 ms a shape plus its area; a native p5 fill of the same points looks identical** (flat colour,
  the paper grain multiplies over both) and costs next to nothing. Strokes are cheap. A glow costs a full-frame pass
  once it's magnified past the frame. H.js has `flat()` / `fillInk()` (native fill under the brush's ink outline) and
  `deskLite()`, a desk() rebuilt that way (native fills, the screens' big glows faded in only below zoom ~1.5, parts
  outside the view skipped): ~0.6× desk()'s cost at the hook framing and ~0.6× at zoom 1.7. Proposed: the same inside
  screen()/card()/desk() (keep the ink, fill natively).
- **p5.brush drops a stroke whose span is much longer than the canvas** (a 4500 px inkLine vanished at zoom 1, a 1150 px
  one at zoom 1.17). Split long lines into overlapping strokes under ~1000 screen px.
- **I.js depends on H.js** (`window.HI`: the shared chart, camera and deskLite kit), so H.js must load first, as it does
  in short.html.

## Perf: p5.brush shapes just off-canvas are slow (found building D/E)
- **Where:** any shot; seen with `you()`/`them()` in `short/shots/E.js`.
- **Problem:** a character sitting a few px to a few hundred px outside the canvas (e.g. panned off the left edge) made
  frames cost +30–60% compared with the same frame with that character skipped or fully on screen (measured as a ratio to
  A's frame at 2.0 s, interleaved to cancel the machine load). Moving the camera 150 px so the character left the canvas
  raised the cost from 1.0× to 1.3×; not drawing it brought it back to 0.9×.
- **Workaround (in E.js / D.js):** `DE.onCanvas(x, y, u, pad, l, r)` tests a character's screen box through the current
  camera; shots skip characters (and what they hold) once the camera has left them. Proposed shared fix: a
  `onCanvas()` helper in look.js that `you()`/`them()` call themselves (skip when fully off-canvas).
- **Also:** a full-frame `paint(rectPts(...), { wash })` behind a whip cost ~2–3× a whole frame here; keep whip camera
  travel inside the plate's margin (the plate covers world x −270..1350, y −480..2400) instead of painting a backdrop.
- **E.js depends on D.js** (`window.DE`: the cast's positions, pose/held-half functions, `armTip`, `halfC`, `veil`,
  `onCanvas`), so D.js must load first, as it does in short.html.
