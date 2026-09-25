# Build brief for shot builders

You're building one or two shots of a 65.6 s vertical explainer Short about 15-minute BTC Up/Down markets on Limitless, in the repo's hand-painted p5.brush look. The narration, captions, look, sets and the hook shot (A) already exist. Read these before you write code:

1. `short/SHORTS_GUIDE.md`: rules 2–7 (voice drives the clock, text supports and never tells, something happens in every shot, timing reads, alive and continuous) and workflow steps 4–5.
2. `ANIMATION_GUIDE.md`: the animation principles, timing ("reads"), the engine and the character API (`clawd()` options, `emotions()`, `feel()`, `jump`, `take`, `spring`, `arcPt`, …). Its "No text" rule is replaced by SHORTS_GUIDE rule 3, and its 1920×1080 canvas is now 1080×1920.
3. `short/STYLE.md`, then **your rows** in `short/STORYBOARD.md` (the words with timestamps, the reads, beats and SFX).
4. `short/src/look.js`, `short/src/sets.js`, `short/src/captions.js` and `short/shots/A.js` (a finished shot to copy the patterns from).
5. `short/sources.md`: every number you put on screen must match it.

## Rules of the house

- **Edit only your own shot files** (`short/shots/X.js`). Each is an IIFE that ends `shots([[CUT.X, shotX]])`, with `shotX(t, lt, dur)` a pure function of time: no state between frames, no `Math.random()` (use `hash(i)`, and `jit()`/`random()` only for boil). Put shot-only helpers inside your IIFE.
- **Never edit** `short/src/*`, `short.html`, `short/config.js`, other shots or `src/`. If a shared helper has a bug or you need a shared change, append it to `short/BUGS.md` (file, problem, proposed fix) and work around it in your file.
- **Time everything to words:** `wt('D4', 'mints')` is the word's start time in video seconds and `wte()` its end; `CUT.X` is each shot's start. A visual read lands **on its word or up to 0.2 s before, never after**. Hits may sit on the beat grid (`BEAT`, `beatN`, `pulse`: 116.3 bpm, offset 0.11) when that's within those limits.
- **Frame:** 1080×1920. Key action stays in x 40–900, y 200–1110. Captions are drawn automatically at y ≈ 1190 (band 1130–1250), so keep it clear. Below 1250 is for secondary things; below 1440 and right of 918 are covered by YouTube's UI. Use `cam(t, x, y, zoom)` from look.js: it puts world (x, y) at the stage centre (470, 655) and adds a drift. The camera never parks.
- **Text:** at most ONE on-screen term or number at a time besides the caption (a `pill()` or `txt()`), shown only while the voice says it. No slides, no labelled diagrams, no row labels on the books. Show it, don't write it.
- **Look:** paint through look.js/sets.js (`room`, `screen`, `card`, `coin`, `half`, `books`, `chip`, `pill`, `txt`, `glow`, `motes`, `whip`, the palette `C`). Inside the market, the ground is `room(t, { plate: 'stage', bloom: 0 })`; at the desk it's `desk()`. Characters: `you(x, y, u, actYou(t, keys))` / `them(…, actThem(…))` / `feelYou` / `feelThem`. **Always** use these, never raw `emotions()`, or the body turns terracotta. The characters are big: u 24–40 in medium shots.
- **Every shot has an event,** a beat every 5–8 s, one read at a time, a hold of ≥ 1.2 s after each new concept lands, anticipation and follow-through on every move, nothing mechanical (ease everything, offset parts, no twinning). A frame static for more than 1.5 s is a bug.
- **Cost:** there's no GPU. A frame costs 1.5–4 s to render and must stay **≤ 4 s**.
  - `paint()` fills are automatically turned into washes (`PROJECT.fills = 'wash'`).
  - A full-frame `wash` costs ~1 s, so use one only for a few transition frames.
  - Never use the kit's `brushWipe` (it hatches: very slow).
  - Keep shape counts in the tens, not thousands.
  - Measure real cost with `node render.mjs --page=short.html --soft-gl --stills=T1,T2 --out=out/check/perf_X`, which prints ms per still (~0.5 s of that is PNG encoding). The ms numbers `--sheet` prints are NOT real cost.
- **CPU is shared** by five agents on 4 cores. Keep checks small: sheets of ≤ 12 frames at `--w=270`, strips of ≤ 1 s. Never render the whole video.

## How to look at your work (do it, and open every image with Read)

```bash
export CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
node render.mjs --page=short.html --soft-gl --sheet=6.0,6.5,7.1 --cols=6 --w=270 --out=out/check/X_sheet.jpg
node render.mjs --page=short.html --soft-gl --strip=25.6:26.2 --cols=6 --w=270 --out=out/check/X_strip.jpg
node render.mjs --page=short.html --soft-gl --sheet=25.9 --crop=200,300,600,600 --w=600 --out=out/check/X_crop.jpg
```

(`[page error] … reading 'type'` from p5's device-motion listener is harmless; ignore it.) Budget: at least one sheet per shot at the read times, a strip for every transition and wow beat, and a crop for each face that acts. Check the reads against the words, the safe zone, the seam frames, and the motion (anticipation, overshoot, no pops). Fix, then look again.

## Seam contracts (fixed; both sides must honour them)

| seam | time | contract |
|---|---|---|
| A→B | 5.269 | A ends on a full-frame `C.up` wash (opaque at the cut). **B opens on full-frame `C.up`** and reveals its stage out of that green within ~0.35 s (the green becomes the Up zone). |
| B→C | 14.555 | Both built by the same agent. |
| C→D | 18.683 | Continuous. At the seam: `room(t, { plate: 'stage', bloom: 0 })`, `cam(t, ...BOOK.cam)`, `books(t, { bidK: 1, askK: 1, askOp: 1, spread: .6 })`, and nothing else on screen. D may start moving 0.2 s later. |
| D→E | 27.969 | Both built by the same agent. |
| E→F | 37.255 | At the seam: the stage plate, `cam(t, 470, 700, 1)`, `feeHill(t, 1)` (the full hill), and no characters (E's dizzy trader has tumbled out of frame by ~37.15). F opens by flattening the hill into a balance beam (`feeHill(t, k)`, k 1→0 over ~0.4 s). |
| F→G | 42.414 | Both built by the same agent (pull back OUT of the market screen to the desk). |
| G→H | 51.185 | G pushes into the ticker screen and ends on a full-frame `C.panel` wash (opaque at the cut). **H opens on full-frame `C.panel`** and reveals the chart within ~0.3 s. |
| H→I | 58.923 | Both built by the same agent. |
| I→(loop)→A | 65.6 | I's last frame must match A's frame 0: `cam(t, ...HOOK0.cam)`, `desk(t, { card: HOOK0.card, fn: HOOK0.btc, lo: HOOK0.lo, hi: HOOK0.hi, hide: 1, named: 0 })` (see sets.js). |

## When you're done

Reply with, in ≤ 300 words:
- what each shot shows and the times of its reads and hits;
- the SFX cue list for your shots as JSON (`[{"t": 25.84, "sfx": "stamp", "note": "..."}]`) using your final hit times;
- the measured cost per frame;
- anything you added to `BUGS.md`, and anything you couldn't do.

Don't commit.
