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
1. **The dive has a voice:** "Let's get closer. Much closer." (16.1–17.8, same ElevenLabs voice; reworded in round 4, below). The other twelve takes were reused bit for bit, and the dive whoosh is sidechained 9 dB under the new line (voice 13 dB above music plus SFX there).
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

## Round 4: sound design and voice (after the user's note: "very sharp, some of them very-very weird")

I can't listen, so every sound was judged by measurement plus a stand-in ear (`tools/ear.py`). The ear combines signal metrics (attack, crest, share of energy in the harsh 2–5 kHz band, hiss above 6 kHz, sub, and loss through a phone-speaker model) with CLAP (`laion/clap-htsat-unfused`) audio-text similarity against good and bad descriptors ("slide whistle", "glitchy weird electronic sound", "white noise hiss", "harsh piercing"…). The ear agreed with the note before anything changed:
- the old dive whoosh: 90% of its energy above 6 kHz, "white noise hiss";
- one whoosh: 99% in 2–5 kHz, "harsh piercing";
- the zip: "glitchy weird";
- the reverse swell: "harsh piercing".

**New kit** (`tools/sfx.py`, no Mirelo, only ElevenLabs sound generation and sounds synthesised here):
1. **Round 1:** 19 synthesised designs plus 27 ElevenLabs takes, ranked per role.
   - Three fixes after the first ranking:
     - a matching bug;
     - hits that were pure sub (a 22–27 LU loss through the phone model, so they vanish on a phone);
     - ElevenLabs tonal takes out of the music's key (the chime at F6 against the bed's E).
   - The bed centres on A, E and D (chroma), so every pitched effect now uses only A, D and E, and the chime take was retuned −1.17 semitones.
   - Hits got a saturated knock and a soft band-noise "skin" (phone loss 10 LU).
2. **Round 2:** the ear flagged my rising sine for the light's lap as a "slide whistle" (1.00), the swish too (0.76), and the sparkle sweep as "glitchy weird" (0.99). The lap is now a harp glissando up the A-sus notes (0.97 "harp"), the swish is a slice from the peak of a clean ElevenLabs whoosh, the pops and the counter "land" are built on the ElevenLabs bubble pop (0.90–0.97 "bubble pop"), and the sweep was dropped.
3. **Round 3:** leave-one-out over every flagged window.
   - Every ElevenLabs long riser ended in a whine, so the synthesised one is used.
   - The big bass drop's 1.1 s build-up read as weird; it is trimmed to 0.35 s before the hit.
   - Two whooshes overlapped at the diagram cut; one was removed.
   - Chime tails rang under the next line; they now fade by 25.4 s.
   - The saturation had squashed the knock's attack to about 3 ms; the attack is now applied after it.
4. **Mix:**
   - Hits are peak-aligned to their cuts.
   - Every effect shares one warm synthetic room.
   - Music and effects duck on phrases (300 ms smoothing, 80/600 ms) instead of per syllable. The old sidechain moved the bed by up to 4.5 dB inside one phrase, and the ear heard that pumping as "glitchy".
   - Hits that land in speech gaps are never ducked.

| effects bus | v1 (Mirelo) | v2 |
|---|---|---|
| energy in the harsh 2–5 kHz band | 25.7% | 0.1% |
| energy above 6 kHz (hiss) | 5.5% | 0.0% |
| cue windows whose best CLAP label is a bad one | 23 of 34 | 0 of 34 (one borderline mixed window at 43% "bad" whose best label is "shimmering chime"; every sound in it is clean alone) |
| attack steepness (5 ms envelope, 99.5th percentile) | 1.9 dB/ms | 2.1 dB/ms |

**Voice.** Pitch tracking (pyin) showed that three first takes were off:
- the hook "This dot is the whole universe." was only 24% voiced at 83 Hz with 1.0 semitone of movement (vocal fry);
- "Black hole." was 24% voiced and flat;
- the new dive line was whispered (0% voiced).

`tools/vo_takes.py` generated six to eight seeded takes per suspect line and kept only takes that are at least 40% voiced, sit at 90–145 Hz, move at least 1.5 semitones, fit the slot and transcribe exactly. It then ranked them toward the narrator's usual 115 Hz. Six lines were replaced: the hook, "The disk around it is flat", "So why does it look like this?" (the old take sat at 215 Hz), "Now hover just above the edge" (monotone), "Black hole." and the dive line. The dive line whispered in all six seeds as "Let's get closer. Much closer." and in about half of the takes of any rewording, so it became "Let's fly in. Way closer." (a seeded take at 108 Hz, 56% voiced).

The processing chain:
- each line matched to −22.5 LUFS, which cut the line-to-line loudness spread from 4.2 to 1.5 LU;
- 8 ms edges;
- a light de-esser (at most 4.9 dB, active on 0.69 s of the whole track);
- 2.5:1 soft-knee compression;
- the effects' room at −26 dB.

Whisper hears all 13 lines exactly, and captions land between 0.20 s early and 0.10 s late.

**Master:** −14.1 LUFS integrated, −1.4 dBTP true peak (ffmpeg ebur128 on the encoded final.mp4). The voice sits 13 dB or more above the music while speaking, and 15 dB above music plus effects over the dive line.

**Second fresh-eyes critic on the round-3 cut (7/10, "no, not as is"), and what was done.**
- **Fixed in this pass:**
  - the gold BLACK HOLE tag sat on the caption "AND THE BLACK HOLE FILLS"; it moved up under the line;
  - LOOKING UP ↑ was small and grey; it is now 64 px on a backing and held 1.3 s;
  - the counter dimmed for one frame when it landed; a landing value now pops without fading in;
  - the dark backing behind the counter smudged the bright disk; it is softer.
- **Not changed:**
  - the "dead air" after "Black hole." (the music is composed to 14 bars; the push-in and turning sky now keep the dot moving, and the new reverse swell carries into the loop);
  - the 19–22 s stretch, now tagged and voiced;
  - the unlabelled lower image of the disk's far side;
  - the diagram's art style.

## Round 5: a new, more natural voice (the user: "I don't like the voice… I liked Liam", then "too scripted, feels like a robot")

- **Voice:** ElevenLabs "Liam – Energetic, Social Media Creator" (`TX3LPaxmHKxFdv7VOQHJ`), found in the account's voice list.
- **Why it sounded scripted:** every line was generated on its own with `eleven_multilingual_v2` and trimmed tight. That flattens the intonation between sentences and throws away the breaths.
- **What changed:**
  - **Model:** `eleven_v3`, the expressive model. Its lines move 4–11 semitones in pitch, against 2–4 for the old takes.
  - **One continuous read:** Liam reads the whole script in one go; eight seeds at "natural" and "creative" stability (`tools/vo_v3.py`).
  - **Cut by the audio, not the timestamps:** v3's timestamps give each pause to the next sentence and drifted up to 0.7 s within a read. Cuts made from them started captions early and clipped word endings (Whisper heard "gravid" and "over half"). Each read is now split at the quietest point in each pause. Each line starts and ends where its sound does, and its letters' times are stretched onto that span. Caption changes that follow a comma or question mark snap to the voice's onset after the pause.
  - **Breaths kept:** each line keeps the breath before it (up to 0.35 s, placed so the first word still lands on its beat) and a natural 0.28 s tail.
  - **Picking the best version of each line:** across the reads, a line must transcribe exactly and not be whispered (at least 20% voiced) or in fry (median pitch at least 72% of the narrator's 108 Hz). The pitch-consistency limit was dropped: v3's questions rise well above the centre, and that is the naturalness asked for. The pick then favours more voicing and more pitch movement, stays near the narrator's usual pitch, and prefers lines that need no squeeze.
- **"Black hole.":** as the last sentence of every full read it came out creaky (60 Hz or below, flat). It is now cut from a short read of "Everything else? Black hole. This dot? It's the whole universe.", which is how the loop plays (132 Hz, a level deadpan, as scripted).
- **Wording, loosened for speech:**
  - "This dot? It's the whole universe."
  - "The disk around it? Flat."
  - "The whole universe shrinks to one dot overhead." Every read of "…gets squeezed into one dot above your head" took 3.6–4.4 s for a 3.0 s slot. Squeezing it 15–30% would have sounded processed.
- **Timing:** v3 reads slower and ignores the speed setting, so slots now use the real gaps between beats. "That's the back of your own head." moved to 24.78 s, a breath after the visor flash. WSOLA tightens only one line, "So why does it look like this?", by 2.4%; the cap was 8%.
- **Checks:**
  - Whisper hears all 13 lines exactly.
  - Every line starts on its beat, and captions land between 0.15 s early and 0.05 s late.
  - The voice sits at least 13.5 dB above the music while speaking, and 16.6 dB above music plus effects over the dive line.
  - Master: −14.1 LUFS, −1.4 dBTP.

## Round 6: show the head, and more facts per second (the user: "would be great to see own head in black hole when you say that light here is looped"; "it wants more facts… Vsauce and Cleo Abram give much more interesting information per unit of time")

**The back of your own head, shown.** A new first-person shot, E2 (24.55–26.67), replaces the diagram's double take:
- **Framing:** it uses the same camera F opens on, so it flows straight into F.
- **Push-in:** it pushes in on the photon-sphere line and tilts 3° down, so the line sits at 40% of the height. The first try put the opened line on top of the caption.
- **The self-view:** the line opens like an eye into a lens of its own cold light. Inside it is the back of the astronaut's helmet (the same signed-distance astronaut as the diagram, raymarched from behind), lit from above by the bright sky with nothing from the black hole below. The head turns once.
- **Hand-off:** the lens closes and the view whips back out to exactly F's first frame.
- **Label and honesty note:** "* MAGNIFIED ILLUSTRATION". sources.md says the real image is a hair-thin sliver stretched around the whole line.
- **Two looks were rejected on the way:** a pink rectangle (the band had sampled the disk's warm light, and read as an interface box) and a helmet standing on the horizon (the band behind it was dark).

**Density.** The visuals are fixed, so the narration does the work:
- **Words:** 87 → 104 in the same 37.3 s (2.3 → 2.8 words/s overall). The silent holds are cut back to the two payoffs (the arch reveal, now 0.9 s, and the dot landing).
- **Three new facts, checked in sources.md:**
  - "its inner edge racing at half the speed of light" (a circular orbit at the ISCO moves at c/2 for a local observer);
  - "bent over the top by gravity, and under the bottom" (the far side's second image, which also answers both critics' question about the lower arc);
  - "And it's playing thirty times fast", with a 31.6× number on screen (time dilation for a hovering observer at 1.001×).
- **Ending:** "Everything else? Black hole." now lands at 34.5–36.3, one second before the loop, so it snaps straight back into "This dot?".

**Voice.** New continuous Liam reads of the new script, cut and picked as before. Two fixes to caption timing:
- Captions that start mid-line now take their start from Whisper's word timings on the chosen take. The stretched v3 timestamps were up to 0.5 s off where the read had no pause at a comma, as in "Hover here and…".
- Those Whisper starts are then refined to the voice's own onset, because Whisper stretches a word that follows a pause back into the silence.

Only "So why does it look like this?" is tightened, by 5%.

**Checks:**
- Whisper hears all 14 lines exactly, and captions land between 0.15 s early and 0.11 s late.
- Nothing is in the bottom 20% or the button column.
- The voice sits at least 13.6 dB above the music.
- Master: −14.1 LUFS, −1.4 dBTP.

## Round 7: the ghost frame, the ending, and speech that sounds spoken (the user: "there is artifact right after you show the back of the head"; "the ending… feels not like the proper ending"; "we need to make speech more natural during the whole video")

- **The ghost frame.** Frame 800 (26.67 s, the pull-out after the self-view) showed a faint copy of the diagram for one frame. One of its motion-blur samples was taken a fraction of a frame earlier, which fell in the diagram shot. Blur samples now never cross a shot boundary, and the pull-out is rendered from E2's own camera.
- **Speech that sounds spoken.** Every line was rewritten to point at what is on screen and to say why we move on:
  - "This dot? It's the whole universe." → "See this dot? That's the whole universe."
  - "To see it, fly down to a black hole. The disk is flat, its inner edge racing at half the speed of light." → "Here's how. This is a black hole. That disk is actually flat. Back half, front half." The disk line now arrives as the camera shows the flat ring, which is the user's own example. The half-light-speed fact was cut: it was the one fact with nothing on screen to point at.
  - "And light goes around it in circles." → "Here, light goes in circles."
  - "That's the back of your own head." → "That line? The back of your own head.", said while we look along the line and it opens.
  - "Now hover just above the edge." → "Now hover just above the horizon, and…"
- **The ending.** "Everything else? Black hole." sounded like a tag, not an ending. It is now "All that darkness around it? That's the black hole.", the answer the whole video builds to. THE UNIVERSE labels the dot on "around it", and the BLACK HOLE arrows pop on "That's the black hole". Then the loop runs into "See this dot?".
- **Labels on words.** BACK and FRONT pop on "Back half, front half", the lower BACK on "and under", and 32× on the time line. Each label's time is read from the caption words, so it follows the voice.

## Round 8: transitions (the user: "it feels like transitions in speech and video feels super unnatural and sharp")

**Speech.** Two causes, both fixed by `tools/vo_flow.py`:
- **Lines came from different performances.** Each line had been picked from whichever of eight reads did it best, so neighbours didn't match: one line sat at 99 Hz and the next at 146 Hz, with different energy. The narration is now **one read of the whole script** (seed 179 of sixteen, stability 0.0). It was chosen because every line in it is heard exactly by Whisper, none is in fry, and it fits the picture with the least squeezing. Inside a line nothing is changed. Only the silent middle of a pause gets longer or shorter, and four lines are tightened by 1–6%.
- **Every line faded in from digital silence.** A read's pauses carry faint room sound. Cutting lines out and dropping them onto silence switched that sound on and off at every line. A bed of the read's own room tone now runs under the whole track, made from its quiet stretches (no breaths) joined with 25 ms crossfades. Each line keeps up to 0.38 s of its breath before and 0.45 s of tail after, and crossfades into the bed over most of that.
- **One reworded line.** "Out there, time's in fast-forward" is heard, by Whisper and by ear, as "times and fast forward". It is now "Out there, time is on fast-forward." Rather than change the whole performance, that line is re-read with the same voice, seed and stability, with three lines of run-up before it. That matches its pace (16.8 characters/s against the neighbours' 18.2) and pitch (111 Hz against 116). It is then level-matched (+1.6 dB) and spliced in.

**Picture.**
- **Dissolves.** The cuts at 2.67 (dot → shadow, 0.16 s), 22.2 (line → diagram, 0.24 s) and 24.55 (diagram → first person, 0.24 s) are now dissolves. Both shots are rendered and blended in linear light with a smoothstep curve. The rest of the seams were already continuous camera moves.
- **Captions and labels.** Captions ease in (a fade with scale 0.965 → 1). A caption followed by a pause fades out over 0.12 s, and one followed straight away by the next cross-fades into it over 0.08 s. The labels and the big numbers ease in and out the same way, instead of snapping.
- **Sound follows the labels.** The BACK and FRONT ticks had stayed at their old times (7.10 and 7.30 s) when the tags moved onto the words (7.50 and 8.25 s). They now use the same word-timed cue as the tags.

**Captions.** Chunk starts come from Whisper's word timings on the finished voice track, refined to the voice's own onset. The onset rule is shared by `tools/caption_align.py` and the checker, `tools/captionsync.py`. It now also walks back when Whisper squashes a word to zero length: "This is a black hole" had shown 0.19 s late.

**Checks:**
- Whisper on the final mix hears all 12 lines exactly.
- Captions land between 0.12 s early and 0.13 s late. The checker flags "and the whole universe" as 0.32 s late, but Whisper merged "horizon, and" across a 40 ms dip there. The energy trace puts the caption 0.04 s ahead of the voice.
- No stray frames: no frame differs from both neighbours more than they differ from each other.
- Nothing is in the bottom 20% or the button column.
- The voice sits at least 12.9 dB above the music.
- Master: −14.2 LUFS integrated, −1.3 dBTP after AAC encoding.

## Round 9: the time line, and a breath before the loop (the user: the time line "sounds fast and is not natural… maybe explain it a bit more. I think it's okay if the short will be a bit longer"; "the video ends exactly on phrase end… can you make the phrase end, then wait a moment and then end the video?")

- **The time line.** "Out there, time is on fast-forward." packed the whole idea into five quick words, 2.1 s. It is now two sentences with a concrete example: "And down here, time runs slower. Stay for one minute... and half an hour goes by out there." (a minute at 1.001× is 31.6 minutes far away). On screen, 1 MIN / DOWN HERE pops on "Stay for one minute", then counts up to 32 MIN / OUT THERE on "and half an hour". The 32× label it replaces said the same number more abstractly.
- **Recording.** The two lines are re-read together by the same voice, seed and stability as the rest of the narration. The read includes three lines of run-up and the line after, and the take is chosen from eight. Pace now counts against a take only if it is quicker than the lines around it, not slower. The first pick ran "Stay one minute and half an hour…" together in 2.5 s, with no beat before the payoff. An ellipsis ("Stay for one minute...") gets a half-second beat there, and that take was chosen: 103 and 115 Hz against the neighbours' 116 Hz.
- **Length.** 37.33 → 43.33 s (65 beats). Everything up to the dot landing at 32.0 is unchanged. The dot then holds through the two new lines, "All that darkness around it? That's the black hole.", and 1.35 s of quiet. The labels stay through the quiet and fade out over its last half-second, so the last frames are frame 0's clean dot. The music's final decay is time-stretched to fill the longer ending, the dot's shimmer is chained to carry it, and the reverse swell still ends exactly on the loop.
- **Fitting.** When a line didn't fit its window with its natural pause, the planner used to drop that pause to the 0.14 s minimum. It now gives up only as much pause as it needs to fit. That stopped "All that darkness" arriving 0.2 s after "out there" (and squeezed by 8%); it now comes 0.5 s later, unsqueezed. The same rule moved lines 1–4 later by 0.07–0.13 s, keeping more of their natural pauses.
- **Checks:**
  - Whisper on the final mix hears all 13 lines exactly.
  - Captions land within 0.12 s of the voice, except the checker's known false alarm on "and the whole universe" (see round 8).
  - The music decays smoothly to silence by 41 s, and the final pause sits at −35 dB (shimmer and swell).
