# Concept: step 2

The `blender-shorts-ideation` skill's asset pack (`shorts_research/`: taxonomy, corpus, scorer) isn't in this repo. So instead of its corpus numbers I applied its method (a legible ladder, one variable per rung, a cold open, every rung bigger than the last) and scored against the brief's four criteria, using what research.md measured.

Scores are 1–10 on each criterion: **W** = a wow in the first 2 s with zero context, **T** = a counter-intuitive claim that is actually true, **S** = "you have to see this" shareability, **R** = we can render it beautifully on this machine (4 CPU cores, no GPU; Cycles measured at ~90 s per 1080×1920 frame, so custom numba/taichi renderers).

| # | idea | the claim | W | T | S | R | total |
|---|---|---|---|---|---|---|---|
| 1 | **Hover down to a black hole in three stops** | its back side shows over the top; at 1.5× the horizon it fills exactly half your sky and you see the back of your own head; just above the edge the whole universe squeezes into a dot overhead | 9 | 9 | 8 | 9 | **35** |
| 2 | 1,000 double pendulums, a billionth of a degree apart | identical starts, total chaos in 10 s | 8 | 9 | 6 | 9 | 32 |
| 3 | A photon's escape from the Sun | 8 minutes to Earth, but 10,000–170,000 years to get out of the Sun; your sunlight is older than the pyramids | 7 | 9 | 8 | 8 | 32 |
| 4 | Spaghetti never snaps in two | Feynman couldn't explain it; a snap-back wave causes the extra breaks | 8 | 9 | 9 | 5 | 31 |
| 5 | Ball stack to space | each extra ball multiplies the bounce; 12 balls reach escape velocity in the ideal limit | 7 | 7 | 8 | 9 | 31 |
| 6 | Tautochrone | balls released from any height on a cycloid arrive at the same instant | 6 | 9 | 7 | 9 | 31 |
| 7 | Mars sunsets are blue | fine dust scatters blue light forward, around the Sun | 7 | 9 | 7 | 8 | 31 |
| 8 | Chaos game | random dice rolls draw a perfect fractal fern | 6 | 9 | 7 | 9 | 31 |
| 9 | Hairy ball theorem | somewhere on Earth the wind isn't blowing right now | 6 | 9 | 8 | 7 | 30 |
| 10 | Drunk man vs. drunk bird (Pólya) | a random walker in 2D always gets home; in 3D it may never | 5 | 9 | 8 | 8 | 30 |
| 11 | Newton's cannon on a tiny planet | the ISS is falling the whole time, and missing | 6 | 8 | 6 | 9 | 29 |

**Pick: #1.** It has the strongest zero-context first frame of the set, every beat is a true and escalating surprise along a single variable (how close you are), a table-driven Schwarzschild ray tracer can render it at Shadertoy-level quality on four cores, and the last image (a bright dot in black) inverts the first (a black disk in light), so it loops.

The one fact that would change the pick: the "universe in a dot" view is only real for an observer **hovering** on rockets. A free-falling observer sees something else (Hamilton, JILA), so the script says "hover" and never "fall in".
