# Critique log

Each round: what the fresh-eyes critic saw (a subagent given only the frames and the narration or audio, never the script or storyboard), what my own checks found, and what I changed.

## Round 1: storyboard frames sheet v1 (8 key stills)

**Fresh-eyes critic, in short.**
- **A (0:01.2):** "An Interstellar-style black hole… beautiful, but it's the most-seen black hole image online… I give it half a second." The "REAL PHYSICS SIMULATION" kicker is "microscopic".
- **B1 (flat disk, face-on):** "a fuzzy donut or an iris". "Flat" isn't visible, the blue/orange split is unexplained, and the caption "AROUND IT IS FLAT." reads as broken English.
- **B2 (arch):** "blue = the far half?" It only works if you linked it to B1.
- **C (dive):** "Nothing shows light orbiting." Gauge ticks are ~8 px on a phone, "×" of what?, and HORIZON collides with the caption.
- **D:** the black half "reads as empty ground"; "the only line I see looks like a disk streak."
- **E:** "the astronaut is the best element in the video", but the YOU pointer ends in empty space, the light path isn't visible in the still, and "IT'S THE BACK" cuts the punchline.
- **F–G:** "looks like a failed render"; ~8 s of near-black including 2.6 s of silence; "I'd swipe away before 'Black hole.'"
- **Comment they'd leave:** "Wait, which line is my head? I only saw the disk."

**My own sheet checks (before the critic).** The gauge collides with captions in C/D; gold caption words lose contrast over the bright disk in E; the final dot reads as a ring outline, not a bright dot; the B tint is pale lavender rather than ice.

**What changed (storyboard v2, then the render).**
1. **New cold open on the most surprising image.** The video now starts on the universe-dot with "This dot is the whole universe." and ends on that exact frame (G continues seamlessly into O). The O → A cut is an inverted match: the bright dot becomes the black shadow at the same size and place.
2. **"Flat" is now shown, not asserted.** The camera rises to 40° (a tilted ring like Saturn's) instead of face-on, and the halves are labelled BACK (ice) and FRONT (gold), so the ice arch in B2 pays off with the sound off.
3. **The dive no longer claims orbiting light** (no VO there). "Light goes around in circles" moved to E, where the pulse visibly does it.
4. **The line is led:** a glow sweeps along D's line as the VO turns to it, and E opens exactly edge-on so the line visibly continues across the cut and opens into the circle.
5. **E:** the YOU leader line touches the helmet, the pulse's path stays drawn as a trail, and the punchline is one line: "That's the back of your own head."
6. **Ending:** the dot is bigger (35% of the width, at a 45° field of view), brighter (the mean starlight surface brightness is now included and the exposure follows the blueshift), and held 1.3 s before the next line. The dead air is cut from 2.6 s to under 1.2 s.
7. **Gauge:** a "DISTANCE (HORIZON = 1×)" title, 34 px labels, the YOU marker on the left of the line so it never covers a tick, YOU never parked on HORIZON while the VO says "just above", and the whole gauge moved up to y 330–1080.
8. **Captions:** phrase-boundary chunks (hand-marked), a scrim that darkens bright backgrounds under the caption band, and the REAL PHYSICS SIMULATION kicker enlarged to 46 px.

## Round 2: storyboard frames sheet v2 (9 key stills, new cold open)

**Fresh-eyes critic, in short.**
- **What works now:** A is "the strongest image" and B's BACK/FRONT split is "smart, the labels add information". On B2 11.3: "this is where it clicks."
- **O:** "a glass marble… 60% empty black"; the orb needs to be much bigger. The claim only half lands.
- **Captions:** fragments ("TO SEE IT,", "IS FLAT.", "GETS SQUEEZED") mean nothing with the sound off.
- **C:** the ruler has no explanation and "(HORIZON = 1×)" is unreadable. "I'm lost here, and this is where I'd get bored."
- **D:** the YOU/1.5× tick lines up with the bright line, so the ruler looks like part of the scene.
- **E:** "the most mind-blowing line has no visual"; no arrows on the ring and no light ray (in the still).
- **G:** "BLACK HOLE. sits right under the orb so it reads as a *label for the orb*. That is exactly backwards."
- **Comment:** "Wait, how is the back of my head in the sky?? Also isn't the dot the black hole?"

**What changed.**
1. **G:** "Black hole." is no longer a caption under the dot. The dot gets an ice leader label, "THE UNIVERSE", and "BLACK HOLE" appears in gold with arrows pointing out into the surrounding black, word-synced to the VO.
2. **E:** arrowheads along the light's lap (back of the helmet → all the way round → visor) that stay on screen through the punchline, a bigger astronaut (scale 0.95 → 1.2), and the punchline as one caption: "THAT'S THE BACK OF YOUR OWN HEAD."
3. **Captions:** whole phrases (2–8 words), at most two balanced lines at one consistent size (80 px). This supersedes research rule 7's "1–4 words".
4. **O:** the dot is now 41% of the frame width (telephoto end view, vertical field of view 34°). A opens at 46° so its shadow is exactly the same size at the cut (measured: 0.407 vs 0.407 of the width). REAL PHYSICS SIMULATION is up to 56 px.
5. **Ruler:** titled "YOUR DISTANCE", bottom tick "1× = HORIZON", moved up so the 1.5× tick no longer sits on D's line. It's hidden during the diagram (it cluttered the ring), and it fades out before the dot's labels in G.
6. **F:** a "LOOKING UP ↑" kicker as the camera tilts, and the 1.001× label moved into the gap between the two VO lines so it doesn't compete with a caption.
7. **B:** the tilt is now 58° above the disk (from 50°) so it reads as a flat ring, and a second BACK tag marks the lensed underside below the shadow.
8. **VO:** explicit per-line speeds (the punchline at 0.88× instead of an auto speed-up to 1.15×).

The storyboard sheet from these two rounds gated the render; after round 3, outputs/storyboard_sheet.jpg shows the v3 key stills taken from the final frames (the v2 sheet is in git history).

## Round 3: the rendered final cut

**My own checks on the render (before the critic).**
- **Safe zone, every 0.1 s** (`tools/safezone.py`): the top label reached 89% of the width, long captions 88%, and the BLACK HOLE arrows 81% of the height. Captions are now capped at 780 px wide, the top label is 50 px and the arrows are shorter. The check now finds nothing in the bottom 20% or the right-hand button column.
- **Caption sync against Whisper** on the final audio (`tools/captionsync.py`): chunks that switch mid-sentence came in up to 0.16 s late, because the TTS alignment marks a word's first letter and ears hear it slightly earlier. Those switches now lead by 0.12 s. Every chunk appears between 0.18 s early and 0.04 s late.
- **One frame per second:** at 19 s and 32 s, "YOUR DISTANCE" sat on the same line as "THE PHOTON SPHERE" / "0.1% ABOVE THE EDGE", and at 31–32.7 s the "1× = HORIZON" tick ran into the dot. This was fixed first and then made moot by the counter below.
- **Artifacts** (frame-to-frame difference over all 1120 frames): the only jumps are the planned cuts at 2.67 s, 22.2 s and the ring collapse at 26.4–26.6 s. The loop seam (last frame → first) differs less than an average pair of neighbouring frames.

**Fresh-eyes critic** (given only frame sheets, 0.1 s strips and a Whisper transcript), in short:
- **Hook:** "only just." The claim carries it, but the orb "looks like a marble or an eyeball" and nothing moves for 2.7 s; the caption leaves a gap from 2.0 to 2.7.
- **Swipe point:** 15.5–18.8. "Bent over the top by gravity" sounds like the end, then there are about 4 s with no voice and a gauge too small to read.
- **D:** the flat black lower half "looks like a letterbox or caption bar, not the black hole."
- **Text:**
  - the gauge, THE PHOTON SPHERE, DIAGRAM NOT TO SCALE and THE UNIVERSE are too small;
  - LOOKING UP is nearly invisible over the disk streak;
  - the lower BACK tag is never explained;
  - the BLACK HOLE callout is lopsided (three arrows, one jammed against the E);
  - "THE WHOLE UNIVERSE GETS SQUEEZED" is set smaller and has no gold word.
- **Loop:** the voice ends at 35.4, so across the seam there are about 4.5 s of a still dot.
- **Understood:** yes. They retold the whole chain correctly (flat disk → far side bent over the top → half the sky at 1.5× → back of your head → the universe as a dot just above the horizon).
- **Comment:** "Wait, the dot at the start is what you see right above the horizon?? Rewatched."

**What changed.**
1. **The dive has a voice:** "Let's get closer. Much closer." (16.1–17.8, same ElevenLabs voice). The other twelve takes were reused bit for bit, and the dive whoosh is sidechained 9 dB under the new line (voice 13 dB above music plus SFX there).
2. **The gauge became a big distance counter** at the top that counts down live with the camera: 20× → 1.5× through the dive, landing with a pop on "1.5× / THE PHOTON SPHERE", then 1.2× → 1.001× through the last descent, landing on "1.001× / 0.1% ABOVE THE EDGE". Its sub-label reads "YOUR DISTANCE · HORIZON = 1×". It sits on a soft dark backing so it reads over the disk.
3. **D:** a gold "BLACK HOLE" tag sits in the black half, just under the line, from "the black hole fills".
4. **The end and the cold open move:** the sky inside the dot turns 6°/s about the radial axis (the dot stays put) while the camera pushes in (the dot goes from 49% to 54% of the width over G and O). The seam is still the same camera function on both sides. A's opening field of view went from 42.4° to 35.8° so the shadow still matches the dot at the cut (0.538 of the width both sides).
5. **Captions:**
   - "THIS DOT IS" is up from frame 0, and "THE WHOLE UNIVERSE." holds to the cut, closing the 2.0–2.7 gap;
   - "THE WHOLE UNIVERSE / GETS SQUEEZED" is split into two chunks at full size, with SQUEEZED in gold.
6. **Labels:**
   - the opening caption is fully up on frame 0 (no pop), so the first frame reads;
   - the lower BACK tag (and its tick) is gone;
   - LOOKING UP has a soft dark backing;
   - the BLACK HOLE callout has four symmetric arrows inside the safe zone;
   - the big-value sub-labels go from 36 to 44 px, THE UNIVERSE from 46 to 56 px and the diagram tag from 26 to 32 px.

**Not changed, and why.**
- **The cuts into and out of the diagram at 22.2 and 26.67:** they are match cuts on the line and circle. Seen at 0.1 s steps they read as jumps, but in motion they carry the line across.
- **The one-frame white bloom at 2.6:** the designed flash into A on the downbeat hit.
- **The astronaut's snap-round at 25.2:** the comedy double take.
- **The E diagram:** "the astronaut looks like he's sitting on the ball" is fair, but the shot is labelled as a diagram and the pulse lap is visible in motion.
