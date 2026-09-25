# Making an explainer Short

Read this whole file before you write a line of script or code. The person prompting you decides **what** the video is about. This guide decides **how** it's made. If they ask for something a rule below forbids, do what they ask.

The engine and review tooling come from [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase). Clone it and read its `ANIMATION_GUIDE.md` sections on timing, animation principles and the review loop. They apply here unchanged. This guide replaces its rules on medium, text, format and sound, because an explainer Short is a different kind of film from a silent cartoon.

---

## The three goals

- **One idea lands.** The viewer leaves understanding one surprising thing they didn't know 60 seconds ago. Everything that doesn't serve that idea gets cut, however good it looks.
- **Always a reason to stay.** There is always an open question on screen or in the voice. Answer one, open the next. The hook opens the biggest one, and the ending answers it.
- **One piece.** One medium, one world, one palette, one voice, one thread. It should feel like a short film, not a pile of clips from different tools.

Underneath all three, the viewer has to be able to follow it at full speed, once, on a phone. Timing is where generated video fails most often.

## The rules

### 1. One medium, chosen once

- **Default medium: stylised 3D in WebGL** (three.js plus custom GLSL), rendered in headless Chrome through the ClaudeAnimationBase harness (`studio.html`, `render.mjs`, contact sheets). Swap its p5.brush painting layer for a three.js scene and keep everything else.
- **Frames are pure functions of time.** A shot is `fn(t, lt, dur)`. It draws the same frame for the same `t` every time: no state carried between frames, no `Math.random()`, and no physics that steps frame by frame. Precompute simulations to a baked JSON/binary keyed by frame, or use closed-form motion. Use `hash(i)` for stable randomness.
- **One look, defined once** in the style bible (workflow step 2): one palette, one lighting rig, one set of materials and one post stack (bloom, filmic tone map, subtle grain, vignette, depth of field where it helps). Every shot uses the shared look module, so no shot invents its own.
- **Other sources get absorbed into the world, not pasted on top.** A math animation, a stock clip or a real photo appears on a surface inside the scene (a screen, a card, a window, a hologram), graded to the palette. It never takes over the full frame raw.
- Blender or manim may replace WebGL for the whole video if the style bible chooses it. Pick one; don't mix engines shot by shot.

### 2. The voice drives the clock

- **Script first, then voice, then picture.** Generate the narration with word-level timestamps before building any shot. The timeline is derived from those timestamps, not guessed.
- **A visual read lands on the word that names it**, or up to 0.2 s before it. Never after.
- **Leave air.** After each wow beat, a 0.3–0.6 s gap in the voice lets the picture land. Trim TTS pauses elsewhere.
- **Music sets the pulse.** Once the track is picked, set `bpm` and `offset` so cuts, hits and camera accents land on beats.

### 3. Text supports the story; it never tells it

- **Captions:** burned in, 1–3 words at a time, synced to the word timestamps, one highlight colour for the key word, and a style taken from the research. Keep them inside the safe zone (rule 9).
- **At most one other on-screen element at a time:** one number, one term, one short equation. Show it only while the narration is saying it.
- **No slides.** No bullet lists, titled cards, labelled diagrams with five callouts, or "Step 1 / Step 2". If a frame needs a legend to make sense, redesign the frame.
- **Show it, don't write it.** If the voice says "the price rockets", the viewer sees something rocket.

### 4. The hook is the first 2 seconds

- **The first frame is already mid-action.** No logo, no title card, no fade from black, no "in this video".
- **The strongest visual in the film appears in the first 2 s**, or a teaser of it does, together with one spoken line that opens a question.
- The hook makes a promise the ending must keep. Write both at the same time.

### 5. Something happens in every shot

- **Every shot has an event:** something changes between its first frame and its last. A camera slowly orbiting a pretty object is not an event.
- **One focal read at a time.** Cause, then effect, in sequence.
- **A new wow / lol / omg / wtf beat every 5–8 s**, each bigger than the last or a twist on it. Mark them in the storyboard; if a 10 s stretch has none, cut it or rewrite it.
- **Pay off every setup.** Anything shown with emphasis gets resolved.

### 6. Timing: model the viewer

Use ClaudeAnimationBase's "reads" method as written: list what the viewer must understand in each shot, give each read time to be found, understood and registered, and never overlap two important reads. On top of that:

- **Phone scale:** anything smaller than about 1/15 of the frame height takes longer to find. Make the important thing big.
- **Explanations need more held time than gags.** A new concept holds for at least 1.2 s after its visual lands, before the next concept starts.
- **Fast actions, slow meanings.** Cut and move quickly through transitions; hold on the moment of understanding.

### 7. Alive and continuous

- **Nothing is ever still:** the camera drifts, pushes or orbits, particles move, lights breathe. No static frame longer than about 1.5 s.
- **Every seam gets a motivated transition:** a match cut on shape, a push into an object that becomes the next scene, a whip pan on the beat, or a continuous camera move. A plain cut only on action or as a deliberate smash cut.
- **One world:** props, colours and motifs carry across cuts, and the ending rhymes with the hook.

### 8. True

- **Every factual claim has a source** in `sources.md`. Simplify, but never say something false. Every on-screen number matches its source.
- **When the topic moves fast** (prices, product rules, fees), check the primary source at build time, not from memory.
- **Money, health or safety topics:** no promises and no "easy" framing. Name the real risk once, on screen.

### 9. The vertical frame

- 1080×1920, 30 fps (60 fps if fast motion strobes at 30).
- **Safe zone:** keep captions, faces and key action out of roughly the bottom 25% and the right-hand 15% (YouTube's buttons and title) and the top 10%. The centre band is where the eye lives.
- Compose for the vertical frame. Don't letterbox a 16:9 idea.

### 10. Sound

- **Voice:** a TTS voice whose energy matches the research. Note which voice and why.
- **SFX on every cut and wow beat:** whooshes, impacts, ticks, risers. Sound sells the motion.
- **Music:** royalty-free, license recorded. At least 6 dB below the voice at all times (≤50% amplitude), sidechain-ducked under speech.
- **Master:** about -14 LUFS integrated, true peak ≤ -1 dBTP. Measure with `ffmpeg -af ebur128` and `astats`; never judge by ear.

### 11. Writing voice

Script and on-screen text sound like the reference channels, not like an AI assistant. Avoid:

- em dashes;
- "It's not X, it's Y";
- "Here's the thing" / "Here's where it gets interesting";
- adjectives in threes;
- "mind-blowing", "fascinating", "game-changer", "let's dive in";
- ending on a tidy moral.

Base phrasing on patterns measured in the research transcripts. Short spoken sentences, concrete nouns, second person.

---

## Workflow

### 1. Research → `research.md`

Split the references across subagents. For each channel, pull its 3–5 most-viewed recent Shorts with yt-dlp: metadata, transcript, and frames (every 0.5 s for the first 3 s, then every 2 s). Look at the frames. Measure:

- time to first payoff;
- cuts per 10 s;
- words per second;
- caption style;
- how music and SFX sit under the voice;
- how the video ends.

Transcribe any "rules" video the person gives and pull out its rules. End with "rules we'll follow", each tied to an observation.

If a download is blocked, say which one and work from what you got. Never present a style from memory as analysis. References are for learning style only; none of their footage, music or voice goes into the video.

### 2. Style bible → `STYLE.md` + 3 stills

Write down the palette (hex), lighting rig, materials, post stack, caption style (font, size, highlight colour), camera language and transition vocabulary. Render three stills (the hook frame, a mid-video explanation frame and the final frame) and look at them. If a person is present, show them the stills and the one-line logline before building. This is the cheapest point to change direction.

### 3. Script, voice, storyboard → `STORYBOARD.md`

Write the script, generate the voice with word timestamps, then storyboard against those timestamps:

```
Logline: one sentence. The viewer thinks ___, but actually ___, because ___.
Hook promise: the question opened in 0–2 s, and the shot that answers it.
World: setting, palette, light, how colour shifts across the video.
Motif: the thing that recurs and pays off (and rhymes the ending with the hook).
Shots:
  A  0.00–2.10  [in: none, mid-action]  what's seen · the EVENT · camera · SFX
     words:  "…"  (timestamps)
     reads:  0.00–0.80  first thing the viewer must understand
             0.80–2.10  the next (where is the eye when it starts?)
     beat:   WOW / LOL / OMG / WTF, or none
  B  2.10–5.40  [transition: ___] ...
  [out: loop back to the hook frame, or the last line held]
```

Check it against the rules. Is there an event in every shot? Does every read land before the next starts? Is there a beat every 5–8 s? Are there any slides? Does the ending keep the hook's promise?

### 4. Build

One file per shot in `src/shots/`, sharing the look module. Build the hook first and get it right before anything else. For long videos, brief parallel subagents with this guide, `STYLE.md` and their rows of the storyboard. Each subagent edits only its own shot file and reports any bug in a shared file instead of fixing it.

### 5. Look at it: the review loop

Use `render.mjs` contact sheets (`--sheet`), strips (`--strip`) and crops (`--crop`, `--crop-at`), exactly as ClaudeAnimationBase describes. Open every image and look. Check:

- **Hook:** would the first 2 s alone stop a scroll? Look at the first frame on its own.
- **Reads:** is each shot's event clear from its sheet alone? Does every read have its time?
- **Sync:** does each visual land on or just before its word?
- **Frame:** is the key action inside the safe zone? Is it big enough on a phone?
- **Look:** is every shot on the style bible? Any raw pasted media, default styling, or flat lighting?
- **Motion:** in the strips, is there anticipation and follow-through, and any pops or dead stretches?
- **Truth:** does every number on screen match `sources.md`?

Fix what you find and look again. Budget: one sheet per shot, a strip per transition and per wow beat.

### 6. Mix, render, verify

Mix the audio and measure it against rule 10. Render the final video, extract one frame per second and look at every one. Re-check the hook, the captions and the safe zone. Fix and re-render until everything passes.

### 7. Deliver

`final.mp4`, `STORYBOARD.md`, `STYLE.md`, `research.md`, `sources.md` (facts and asset licenses), and an upload pack: title, description, 3–5 hashtags, pinned comment. End with a few lines on what you made, what you changed from the plan, and what you couldn't do.

---

## Common failures

These make an explainer Short look generated:

- a slow open: logo, title card, fade-in, "have you ever wondered"
- slides: bullet lists, labelled diagrams, step cards, text doing the explaining
- a different look in every shot because each came from a different tool
- stock footage dropped in raw, full frame, ungraded
- visuals arriving after the words that describe them
- one constant pace: no holds on the moments of understanding
- two ideas explained at once
- a long middle stretch with no new beat
- captions under the YouTube buttons, or text too small for a phone
- the camera parked on a static frame
- music fighting the voice
- a claim that's slightly wrong because it was written from memory
- an ending that summarises instead of paying off the hook
