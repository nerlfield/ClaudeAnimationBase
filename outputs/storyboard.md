# Storyboard: "This dot is the whole universe"

*Version 3, after the final-cut critique (round 3 in critique.md): the tiny depth gauge became a big live distance counter, the silent dive got a line ("Let's fly in. Way closer."), the black half in D is tagged BLACK HOLE, the sky inside the end dot turns while the camera pushes in (so the loop never sits still), and A's opening is re-matched to the bigger dot. Version 2 came from two rounds of frames-sheet critique: a cold open on the video's most surprising image that ends on exactly that frame, the G callouts, the arrowed light path in E, whole-phrase captions and B tilted to 58°.*

**Logline.** The viewer thinks a black hole is a black ball that hides what's behind it, but its gravity bends light so hard that on the way down you'd see the back of its disk over the top, then the back of your own head, so if you hovered just above its edge, the whole universe would be one glowing dot over your head and everything else would be black hole.

**Length.** 37.33 s = 14 bars at 90 BPM (one bar = 2.667 s); cuts and payoffs sit on bar lines. 30 fps, 1080×1920. The last frame is the first frame, so it loops seamlessly.

**World.** One non-spinning black hole with a thin, hot accretion disk (inner edge at the last stable orbit, 3× the horizon radius; outer edge 12×), seen by an observer hovering on rockets. All light is emissive: the disk (blackbody colours, Doppler-beamed, gravitationally shifted) and the lensed star field and Milky Way. No lamps.

| role | hex | where |
|---|---|---|
| void | `#05070D` | space; the shadow is black under grain and bloom haze |
| dust indigo | `#1C2140` | Milky Way band and faint nebula |
| ember | `#FF7A1F` | receding (redshifted) side of the disk; "FRONT" label |
| gold | `#FFD27A` | hot inner disk; caption highlight `#FFC24A` |
| ice | `#8FC3FF` | approaching side, the disk's back half (tagged in B), the blueshifted universe dot, data labels |

**Colour arc.** Ice-blue dot in black (O) → warm gold and ember while we look at the disk (A–B, with the back half tagged ice) → a hard split of black and cold light at the photon sphere (D) → the universe collapses back into the ice-blue dot (F–G), which is where the video began.

**Motif: the circle of light.** In O it's the rim of the universe-dot. In A it's the thin photon ring around the shadow; the O → A cut swaps a light circle in dark for a dark circle in light, the same size in the same place. At the photon sphere (D) the circle is seen edge-on as the bright line across your sky; in E the line opens back into a circle that light runs around. At the end (F–G) it's the rim of the dot again, and the loop closes. The dot's rim and the shadow's rim are literally the same family of light rays: the ones that skim the photon sphere.

**Tools.** O, A–D and F–G: a custom Schwarzschild ray tracer in numba. Per frame, it integrates a table of null geodesics for the camera's radius; each pixel then looks up its disk crossings (with Doppler and gravitational shift) and its escape direction (lensed stars with an image-space point spread, so magnified stars brighten instead of bloating). E: the same star and disk shaders unlensed, a raymarched signed-distance-field astronaut, and the light pulse. Post: bloom, hue-preserving filmic tone curve, faint chromatic fringe, vignette, per-frame grain, temporal supersampling on fast moves, and a caption scrim that darkens bright backgrounds under the captions. Every frame is a pure function of t.

**HUD: the distance counter.** A big ice number at the top centre (Montserrat Black 190 px on a soft dark backing, digits in fixed-width cells so it doesn't jitter) with the sub-label "YOUR DISTANCE · HORIZON = 1×" (44 px). It counts down live with the camera: 20× → 1.5× through the dive (15.3–18.67), landing with a pop on "1.5× / THE PHOTON SPHERE"; then 1.2× → 1.001× through the last descent (28.3–31.9), landing on "1.001× / 0.1% ABOVE THE EDGE". More decimals appear the closer you get (18×, 4.9×, 1.97×, 1.044×, 1.002×). It replaced a left-edge ladder gauge that the round-3 critic couldn't read on a phone.

---

## Shots

### O: Cold open, the dot · 0.00–2.67 · [in: the loop from G, identical frame]
- **Seen.** A glowing ice-blue circle (about half the frame width, centred at 42% height) in black. Inside it, the whole sky squeezed and blueshifted: the disk as a bright ring, the Milky Way as a pale band, stars. Soft bloom haze around it; grain in the black.
- **Event.** The sky inside the dot turns slowly (6°/s about the radial axis, so the dot itself stays put) while the camera pushes in; both continue straight on from G.
- **Camera.** Looking straight up from 1.001× the horizon radius; vertical field of view 28.4° → 26° (a slow push-in; the dot grows from 52% to 54% of the width), the sky turning 6°/s.
- **Reads.**
  - 0.00–0.90: a glowing orb in darkness. The eye lands on the dot.
  - 0.15–1.62: VO "This dot is the whole universe." Caption "THIS DOT IS" from frame 0, then "THE WHOLE UNIVERSE." held to the cut.
  - 0.60–2.50: top label "REAL PHYSICS SIMULATION" (50 px, bright). It tells you this isn't art.
- **Out.** On the 2.67 bar, a match cut with inversion: the bright dot becomes the black hole's dark shadow, same size and position, under a whoosh and a rim flash.

### A: The black hole · 2.67–5.33 · [in: inverted match cut]
- **Seen.** The black hole from 22× the horizon radius, 8° above the disk plane. The shadow opens at exactly the dot's size (54% of the frame width) at 42% height, ringed by the thin photon ring. The disk's back arches over the top and its underside shows under the bottom; the left (approaching) side is brighter and bluer.
- **Event.** The camera pushes in slowly while the disk's hot clumps stream around.
- **Camera.** Push r 26.2 → 24.5 while the field of view opens 35.8° → 38° (35.8° makes the shadow match the dot at the cut), 0.6° roll drift; a 1° dip at 5.1 (anticipation of the rise).
- **Reads.**
  - 2.67–3.60: a black hole (the eye goes to the shadow, where the dot just was).
  - 2.85–5.20: VO "To see it, fly down to a black hole." Caption "TO SEE IT, / FLY DOWN / TO A BLACK HOLE."
- **Out.** Camera move into B.

### B: Flat, then not · 5.33–16.00 · [in: continuous camera move]
- **Seen.** The camera rises to 58° above the disk: the disk is now obviously a flat tilted ring, like Saturn's rings, with the hole in its middle. The far half lights up ice with a label "BACK", the near half keeps its gold with "FRONT". The camera swings back down to the side, and the ice half rises and bends over the top of the hole into the arch. It was the back of the disk all along.
- **Event.** Flat tilted ring → arch, with the ice tag carrying the identity across.
- **Camera.** Rise 5.33 → 7.10 (θ 82° → 32° from the pole, pulling back to r 34 and widening the field of view from 38° to 60° so the ring fits), hold with a 3° yaw drift until 8.6, swing down 8.6 → 10.67 with a 2° overshoot and settle on the 10.67 bar, then a slow push to 16.0.
- **Reads.**
  - 5.33–7.10: the view tilts and the disk opens into an ellipse. The eye rides the disk.
  - 6.00–7.60: VO "The disk around it is flat." The eye is on the tilted ring.
  - 7.10–8.60: BACK (ice) and FRONT (gold) pop on the two halves, 0.2 s apart. The eye goes to BACK, the brighter, colder half.
  - 8.60–10.67: the swing down. The labels fade at 9.0 and the eye tracks the ice half. VO "So why does it look like this?" (9.0–10.6).
  - 10.67–12.00: **the ice arch stands over the hole.** No voice. A small "BACK" re-pops on the arch at 10.9.
  - 12.00–15.00: VO "That's the back of the disk, bent over the top by gravity." The ice slowly returns to gold from 13.5.
  - 15.30–16.00: the distance counter fades in at the top (20×). A riser starts.
- **Out.** Camera move into C.

### C: The dive · 16.00–18.67 · [in: camera move]
- **Seen.** We plunge from 22× to 1.5×, pitching from "hole ahead" to "hole below". The disk sweeps past as a streaking band and the shadow's edge swells up from the bottom of the frame.
- **Event.** 20× → 1.5×, with the counter at the top counting down live.
- **Camera.** Eased dive in log-radius with a braked arrival on the 18.67 bar; motion blur (3 sub-frames).
- **Reads.**
  - 16.00–18.67: we're diving in. VO "Let's fly in. Way closer." (16.1–17.7) over the dive rush (sidechained 11 dB under the voice). The eye follows the swelling black and the counter.
- **Out.** A braked arrival with an impact on the bar; same camera into D.

### D: The photon sphere · 18.67–22.20 · [in: arrival]
- **Seen.** Hovering at 1.5×, looking along the horizon. The bottom half is pure black; the top half is the whole outside sky, brighter and bluer, with the disk's lensed light arching across. A razor-thin bright line runs straight across the middle where the halves meet.
- **Event.** A slow yaw; stars that pass behind the hole zip along the line. At 21.3 a glow sweeps along the line from left to right and it brightens (lead the eye).
- **Camera.** 6° yaw drift, 0.4° roll wobble.
- **Reads.**
  - 18.67–19.90: half black, half light. The counter lands on "1.5×" with "THE PHOTON SPHERE" and a pop, then fades by 20.0. The eye goes label → line.
  - 19.00–21.90: VO "Hover here, and the black hole fills exactly half your sky." The eye moves between the halves.
  - 19.55–22.00: a gold "BLACK HOLE" tag sits in the black half just under the line, so the black reads as the hole and not as a letterbox.
  - 21.30–22.20: the sweep along the line. The eye is on the line.
- **Out.** Match cut on the line: E opens exactly edge-on, so the bright line continues across the cut before it opens into a circle.

### E: The back of your head · 22.20–26.67 · [in: match cut, line → circle]
- **Seen.** Diagram, labelled "* DIAGRAM, NOT TO SCALE"; the hole sits at 40% height once the ring opens so the lap stays clear of the captions. From below the ring plane: the black horizon sphere, the photon sphere drawn as a thin circle of light, and on it an astronaut (≈18% of frame width, in the upper half) labelled "YOU" with a leader line to the helmet. A pulse of light leaves the back of the helmet, runs the whole lap and hits the visor with a flash; its path stays drawn as a faint trail with arrowheads showing the direction.
- **Event.** The line opens into a circle (22.2–23.0); the pulse's lap (22.7 → 24.0); the flash; the double take (the helmet whips round to look behind, and back).
- **Camera.** Elevation −2° → −31° (ease-out), slow 5° orbit, back to −2° at 26.3–26.67.
- **Reads.**
  - 22.20–23.00: the line becomes a ring around a black sphere, with the astronaut on it. "YOU" pops at 22.5.
  - 22.30–24.00: VO "And light goes around it in circles." The eye follows the pulse, the only moving bright thing, for 1.3 s.
  - 24.00–24.80: **the flash in the visor.** VO "That's the back of your own head." (24.2–25.9)
  - 25.00–26.30: the double take (anticipation 0.15 s, whip 0.35 s, hold 0.4 s, back) as the laugh beat.
- **Out.** The camera drops back to edge-on and the circle collapses to a line, then a match cut to first person on the same line.

### F: Just above the edge · 26.67–32.00 · [in: match cut, circle → line]
- **Seen.** First person at 1.5× again. The camera sinks and tilts up to look straight away from the hole. The bright half of the sky rolls up and closes into a circle overhead, then shrinks (a hemisphere at 1.5×, 91° across at 1.1×, 30° at 1.01×, 9.4° at 1.001×: Synge's escape cone), turning ice-blue and brighter as it's blueshifted, until it's the dot from the first frame.
- **Event.** Half the sky → the dot. The counter comes back at 28.3 and counts 1.2× → 1.001×.
- **Camera.** Pitch to straight up (26.67–29.5, ease in/out), vertical field of view 60° → 34° by 31.0, the radius eased so the dot's size lands on the 32.0 bar, 0.35°/s roll.
- **Reads.**
  - 26.67–27.20: the match cut; we're back at the line.
  - 26.90–28.80: VO "Now hover just above the edge." The eye follows the bright sky as it rolls up.
  - 27.00–27.90: "LOOKING UP ↑" kicker at the top (on a soft dark backing, over the disk streak) as the camera tilts.
  - 29.00–31.85: VO "The whole universe gets squeezed into one dot above your head." Captions "THE WHOLE UNIVERSE / GETS SQUEEZED / INTO ONE DOT ABOVE YOUR HEAD." The eye is on the shrinking circle.
  - 32.00: the dot lands.
- **Out.** Continuous into G.

### G: Everything else · 32.00–37.33 · [out: the loop, this frame continues into O]
- **Seen.** The dot, the same framing as frame 0, the camera pushing in slowly while the sky inside it turns. The counter lands on "1.001×" with "0.1% ABOVE THE EDGE" (31.9–33.2); then "THE UNIVERSE" labels the dot (33.3) and "BLACK HOLE" appears with four arrows pointing out into the black (34.9), word-synced to the VO.
- **Event.** The push-in and the turning sky carry straight on into O; the labels fade by 36.8, so the final frames are identical to O's.
- **Camera.** The same continuous function as O (G at time t equals O at time t − 37.33), so the loop has no seam.
- **Reads.**
  - 32.00–33.30: **the dot, the whole universe, held 1.3 s**, with its 1.001× label.
  - 33.40–34.20: VO "Everything else?"
  - 34.20–35.00: a beat.
  - 35.00–35.70: VO "Black hole." The gold callout's arrows push the eye out into the black around the dot (no caption under the dot, so it can't read as the dot's name).
  - 35.70–37.33: hold. The last read gets 1.6 s to land, then the loop into "This dot is the whole universe."

---

## Storyboard checks

- **Every shot has an event.** O the turning sky and push-in; A the push and disk stream; B tilted ring → arch; C 22× → 1.5×; D stars zipping along the line and the sweep; E the line opens, the lap, the flash, the double take; F half the sky → the dot; G the creep and the fade to the loop frame.
- **Reads have time and don't overlap.** Text pops (REAL PHYSICS SIMULATION, BACK/FRONT, 1.5×, BLACK HOLE, YOU, 1.001×) each land on a settled frame and are ≤4 words. The VO names what's already on screen ("flat" after the tilt, "like this" as the arch rises, "circles" while the pulse runs, "back of your own head" after the flash).
- **No new idea lands on a payoff.** The arch (10.67–12.0), the flash (24.0, then the VO names it) and the dot (32.0–33.3) hold with no new information.
- **Every seam has a transition, and they vary.** Seamless loop (G→O), inverted match cut (O→A), camera move (A→B→C), braked arrival (C→D), match cut line → circle (D→E), circle → line (E→F), continuous (F→G).
- **The ending rhymes with the opening.** It *is* the opening frame: the dot, now understood.
- **Every setup pays off on screen.** The dot claim (O) pays off in F–G; the BACK tag in B pays off as the arch; the line in D is explained in E; the counter's "HORIZON = 1×" is approached to 1.001× in F; "hover" (said in D and F) is the condition the dot needs.
- **On-screen text never restates the image.** REAL PHYSICS SIMULATION, BACK/FRONT, the distance counter, 1.5× PHOTON SPHERE, the BLACK HOLE tag in D, YOU, * DIAGRAM, NOT TO SCALE, LOOKING UP ↑, 1.001× 0.1% ABOVE THE EDGE, THE UNIVERSE and the BLACK HOLE arrows each add something the picture and VO don't say.
- **Safe zone.** Captions sit at 60–73% of the height and labels in the upper third; nothing below 80% or in the right-hand button column (checked every 0.1 s by `tools/safezone.py`).
