# Storyboard: "This dot is the whole universe"

*Version 7 (round 11): a plainer, slower narration ("This is a black hole. And this bright ring is hot gas, spinning around it.", "Let's look at it from above." → "See? The disk is actually flat.", "This is the back half. And this is the front half.") read as one take at its own pace. The picture is re-timed around it by a time map (below), so the video runs 74.67 s. **The shot sections below keep their original story-clock times; the table maps them to video time, and script.md's beat sheet gives every beat in video time.** Version 6 (round 9): the time-dilation beat is two unhurried sentences with an example ("And down here, time runs slower. Stay for one minute... and half an hour goes by out there.", with 1 MIN counting up to 32 MIN), and the video runs 43.33 s so the last line has 1.35 s of quiet before the loop. Version 5 (rounds 7–8): the narration is conversational and points at what is on screen ("See this dot?", "That disk is actually flat. Back half, front half.", "That line? The back of your own head.", "All that darkness around it? That's the black hole."), and it is one continuous voice take. The cuts at 2.67, 22.2 and 24.55 are short dissolves, captions and labels ease in and out, and every label pops on the word that names it. The ghost frame after the self-view is gone. Version 4 (round 6): after "That's the back of your own head" the video now shows it. A first-person shot (E2) opens the photon-sphere line into a magnified image of the back of your helmet. The narration carries three more facts: the disk's inner edge at half the speed of light, the far side imaged under the bottom as well as over the top, and the universe in 31.6× fast-forward just above the horizon. Version 3 (round 3): the live distance counter, the dive line, the BLACK HOLE tag in D, and the turning, pushing end dot. Version 2: the cold open on the dot, whole-phrase captions and the G callouts.*

**Logline.** The viewer thinks a black hole is a black ball that hides what's behind it, but its gravity bends light so hard that on the way down you'd see the back of its disk over the top, then the back of your own head, so if you hovered just above its edge, the whole universe would be one glowing dot over your head and everything else would be black hole.

**Length.** 74.67 s = 112 beats at 90 BPM. The animation is built on a 43.33 s story clock; `bh/shots.py` maps video time to it with a smooth, always-forward curve (`WARP`), knot by knot from the placed narration:

| story time (shot sections below) | video time | what the voice is doing |
|---|---|---|
| 0.00 → 2.67 (O, the dot) | 0.00 → 5.35 | "See this glowing dot? That's the whole universe. Let me show you why." |
| 2.67 → 5.05 (A) | 5.35 → 11.55 | "This is a black hole. And this bright ring is hot gas, spinning around it." |
| 5.33 → 7.10 (B, the rise) | 12.05 → 14.00 | right after "Let's look at it from above." |
| 7.10 → 8.60 (B, flat ring; ice on 7.50–7.80) | 14.00 → 22.10 | "See? The disk is actually flat. This is the back half (ice at 17.8–18.2). And this is the front half. Now watch the back half," |
| 8.60 → 10.67 (B, the swing down) | 22.10 → 24.00 | "as we go back down." |
| 10.67 → 13.50 (the arch) | 24.00 → 30.10 | 0.66 s of silence, then "The black hole bends its light, up over the top... and under the bottom." |
| 13.50 → 16.00 (gold again, counter in) | 30.10 → 31.80 | "Now let's fly in" |
| 16.00 → 18.67 (C, the dive) | 31.80 → 34.50 | "closer. Much closer." |
| 18.67 → 22.20 (D, sweep 21.3–22.2) | 34.50 → 41.40 | "If you hover right here, the black hole fills exactly half your sky. And see this thin line?" |
| 22.20 → 24.00 (E, lap 22.7–24.0) | 41.40 → 48.00 | "That's light, going around the black hole in a circle. Light can go all the way around... and come back to you." |
| 24.55 → 26.67 (E2) | 48.75 → 52.80 | "So in this line, you see the back of your own head." |
| 26.67 → 32.00 (F) | 52.80 → 62.00 | "Now let's go lower, and hover just above the edge. Then look up. The whole universe shrinks into one small dot above you." |
| 32.00 → 43.33 (G, then into O) | 62.00 → 74.67 | the time lines, "And all this darkness around the dot? That's the black hole.", 1.3 s of quiet |

After the dot lands, and in the cold open (which continues it), the camera runs on one steady clock (0.895× story speed). The loop point therefore joins two moments moving at the same speed. The disk's own motion always runs in video time. The dissolves are 0.16–0.24 s of story time, which is 0.34–0.37 s on screen. 30 fps, 1080×1920. The last frame is the first frame, so it loops seamlessly.

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
  - 0.14–2.66: VO "See this dot? That's the whole universe." Caption "SEE THIS DOT?" from frame 0, then "THAT'S THE WHOLE UNIVERSE." held to the cut.
  - 0.50–2.55: top label "REAL PHYSICS SIMULATION" (50 px, bright). It tells you this isn't art.
- **Out.** On the 2.67 bar, a match cut with inversion: the bright dot becomes the black hole's dark shadow, same size and position, under a whoosh and a low hit. Both shots are rendered across a 0.16 s dissolve, so the dot melts into the shadow instead of popping.

### A: The black hole · 2.67–5.33 · [in: inverted match cut]
- **Seen.** The black hole from 22× the horizon radius, 8° above the disk plane. The shadow opens at exactly the dot's size (54% of the frame width) at 42% height, ringed by the thin photon ring. The disk's back arches over the top and its underside shows under the bottom; the left (approaching) side is brighter and bluer.
- **Event.** The camera pushes in slowly while the disk's hot clumps stream around.
- **Camera.** Push r 26.2 → 24.5 while the field of view opens 35.8° → 38° (35.8° makes the shadow match the dot at the cut), 0.6° roll drift; a 1° dip at 5.1 (anticipation of the rise).
- **Reads.**
  - 2.67–3.60: a black hole (the eye goes to the shadow, where the dot just was).
  - 2.80–5.23: VO "Here's how. This is a black hole." Captions "HERE'S HOW." then "THIS IS A BLACK HOLE."
- **Out.** Camera move into B.

### B: Flat, then not · 5.33–16.00 · [in: continuous camera move]
- **Seen.** The camera rises to 58° above the disk: the disk is now obviously a flat tilted ring, like Saturn's rings, with the hole in its middle. The far half lights up ice with a label "BACK", the near half keeps its gold with "FRONT". The camera swings back down to the side, and the ice half rises and bends over the top of the hole into the arch. It was the back of the disk all along.
- **Event.** Flat tilted ring → arch, with the ice tag carrying the identity across.
- **Camera.** Rise 5.33 → 7.10 (θ 82° → 32° from the pole, pulling back to r 34 and widening the field of view from 38° to 60° so the ring fits), hold with a 3° yaw drift until 8.6, swing down 8.6 → 10.67 with a 2° overshoot and settle on the 10.67 bar, then a slow push to 16.0.
- **Reads.**
  - 5.33–7.10: the view tilts and the disk opens into an ellipse. The eye rides the disk.
  - 5.37–7.40: VO "That disk is actually flat." The eye is on the tilted ring.
  - 7.50–8.90: VO "Back half, front half." BACK (ice) pops on "Back" (7.50) and FRONT (gold) on "front" (8.25), each with a soft tick. The eye goes to BACK, the brighter, colder half.
  - 8.60–10.67: the swing down. The labels fade by 9.1 and the eye tracks the ice half. VO "So why does it look like this?" (9.04–10.51).
  - 10.67–11.00: **the ice arch stands over the hole.** A small "BACK" re-pops on the arch at 10.9.
  - 10.98–15.32: VO "That's the back of the disk, bent over the top by gravity, and under the bottom." The eye goes from the arch to the lower ice arc, which gets its own small BACK tag as the voice says "and under" (14.3); the ice slowly returns to gold from 13.5.
  - 15.30–16.00: the distance counter fades in at the top (20×). A riser starts.
- **Out.** Camera move into C.

### C: The dive · 16.00–18.67 · [in: camera move]
- **Seen.** We plunge from 22× to 1.5×, pitching from "hole ahead" to "hole below". The disk sweeps past as a streaking band and the shadow's edge swells up from the bottom of the frame.
- **Event.** 20× → 1.5×, with the counter at the top counting down live.
- **Camera.** Eased dive in log-radius with a braked arrival on the 18.67 bar; motion blur (3 sub-frames).
- **Reads.**
  - 16.00–18.67: we're diving in. VO "Now let's fly in. Way closer." (16.02–18.53) over the dive rush (sidechained 11 dB under the voice). The eye follows the swelling black and the counter.
- **Out.** A braked arrival with an impact on the bar; same camera into D.

### D: The photon sphere · 18.67–22.20 · [in: arrival]
- **Seen.** Hovering at 1.5×, looking along the horizon. The bottom half is pure black; the top half is the whole outside sky, brighter and bluer, with the disk's lensed light arching across. A razor-thin bright line runs straight across the middle where the halves meet.
- **Event.** A slow yaw; stars that pass behind the hole zip along the line. At 21.3 a glow sweeps along the line from left to right and it brightens (lead the eye).
- **Camera.** 6° yaw drift, 0.4° roll wobble.
- **Reads.**
  - 18.67–19.90: half black, half light. The counter lands on "1.5×" with "THE PHOTON SPHERE" and a pop, then fades by 20.0. The eye goes label → line.
  - 18.72–22.25: VO "Hover here, and the black hole fills exactly half your sky." The eye moves between the halves.
  - 19.55–22.00: a gold "BLACK HOLE" tag sits in the black half just under the line, so the black reads as the hole and not as a letterbox.
  - 21.30–22.20: the sweep along the line. The eye is on the line.
- **Out.** Match cut on the line, as a 0.24 s dissolve: E opens exactly edge-on, so the bright line continues across the cut before it opens into a circle.

### E: Light goes round · 22.20–24.55 · [in: match cut, line → circle]
- **Seen.** Diagram, labelled "* DIAGRAM, NOT TO SCALE"; the hole sits at 40% height once the ring opens so the lap stays clear of the captions. From below the ring plane: the black horizon sphere, the photon sphere drawn as a thin circle of light, and on it an astronaut labelled "YOU". A pulse of light leaves the back of the helmet, runs the whole lap with arrowheads, and flashes in the visor.
- **Event.** The line opens into a circle (22.2–23.0); the pulse's lap (22.7 → 24.0); the flash (24.0).
- **Camera.** Elevation −2° → −31° (ease-out), slow orbit.
- **Reads.**
  - 22.20–23.00: the line becomes a ring around a black sphere, with the astronaut on it. "YOU" pops at 22.5.
  - 22.58–24.19: VO "Here, light goes in circles." The eye follows the pulse, the only moving bright thing.
  - 24.00–24.55: **the flash in the visor.**
- **Out.** A 0.24 s dissolve to first person (E2).

### E2: The back of your own head · 24.55–26.67 · [in: dissolve, diagram → first person]
- **Seen.** First person at the photon sphere again, with the camera F opens on: the bright sky above, the black hole below, the line where they meet. The view pushes in on the line and tilts 3° down, so the line sits at 40% of the height, clear of the captions. The line then opens like an eye into a lens of cold light, and inside it is **the back of your own helmet**. The helmet is lit from above by the bright sky, nothing comes from the black hole below, and there is a warm rim from the disk. At 25.5–25.95 the head turns, the way yours just did. Labelled "* MAGNIFIED ILLUSTRATION". For real, the image of your head is a hair-thin sliver stretched around the whole line (APOD 2013-07-02; sources.md).
- **Event.** The line → the lens with your head (24.9–25.5) → back to the line (25.95–26.3) → a whip pull-out into F.
- **Camera.** F's opening camera; field of view 44° → 30° (push-in, 24.55–25.35), then 29.5° → 60° from 26.0 so the frame at 26.67 is exactly F's first. Every frame of the pull-out is rendered with motion blur from E2's own camera; before round 7 one blur sample reached back across the cut and drew a ghost of the diagram into frame 800.
- **Reads.**
  - 24.42–24.90: we're looking along the line. VO "That line?"
  - 24.95–26.30: the line opens; the eye goes to the helmet, the only object in the frame. VO "The back of your own head." (25.4–26.66)
  - 26.30–26.67: the lens has closed and the view pulls out.
- **Out.** Continuous into F (same camera).

### F: Just above the edge · 26.67–32.00 · [in: match cut, circle → line]
- **Seen.** First person at 1.5× again. The camera sinks and tilts up to look straight away from the hole. The bright half of the sky rolls up and closes into a circle overhead, then shrinks (a hemisphere at 1.5×, 91° across at 1.1×, 30° at 1.01×, 9.4° at 1.001×: Synge's escape cone), turning ice-blue and brighter as it's blueshifted, until it's the dot from the first frame.
- **Event.** Half the sky → the dot. The counter comes back at 28.3 and counts 1.2× → 1.001×.
- **Camera.** Pitch to straight up (26.67–29.5, ease in/out), vertical field of view 60° → 34° by 31.0, the radius eased so the dot's size lands on the 32.0 bar, 0.35°/s roll.
- **Reads.**
  - 26.67–27.20: the match cut; we're back at the line.
  - 27.09–28.9: VO "Now hover just above the horizon," The eye follows the bright sky as it rolls up.
  - 26.95–28.25: "LOOKING UP ↑" kicker at the top (on a soft dark backing, over the disk streak) as the camera tilts.
  - 28.9–31.89: VO "…and the whole universe shrinks to one dot overhead." Captions "AND THE WHOLE UNIVERSE / SHRINKS TO ONE DOT OVERHEAD." The eye is on the shrinking circle.
  - 32.00: the dot lands.
- **Out.** Continuous into G.

### G: All that darkness · 32.00–43.33 · [out: the loop, this frame continues into O]
- **Seen.** The dot, the same framing as frame 0, the camera pushing in slowly while the sky inside it turns. The counter lands on "1.001×" / "0.1% ABOVE THE EDGE" (31.9–35.57). "1 MIN" / "DOWN HERE" pops on "Stay for one minute" (35.57) and counts up to "32 MIN" / "OUT THERE" on "and half an hour" (37.09–39.24). Then "THE UNIVERSE" labels the dot (39.34), and "BLACK HOLE" appears with four arrows pointing out into the black on "That's the black hole" (40.87).
- **Event.** The push-in and the turning sky carry straight on into O; the labels fade by 37.15, so the final frames are identical to O's.
- **Camera.** The same continuous function as O (G at time t equals O at time t − 43.33), so the loop has no seam.
- **Reads.**
  - 32.00–32.30: **the dot lands** on the hit.
  - 32.68–34.87: VO "And down here, time runs slower." The 1.001× on screen says where "down here" is.
  - 35.49–38.75: VO "Stay for one minute... and half an hour goes by out there." To a hovering observer here, everything outside runs 31.6× fast (1/√(1 − 1/1.001)): 1 MIN counts up to 32 MIN as the voice says "half an hour".
  - 39.26–40.7: VO "All that darkness around it?" THE UNIVERSE labels the dot, so "it" is the universe.
  - 40.87–41.98: VO "That's the black hole." The gold callout's arrows push the eye out into the black around the dot.
  - 41.98–43.33: quiet. The labels hold, then fade (42.58–43.03), and the loop runs into "See this dot? That's the whole universe."

---

## Storyboard checks

- **Every shot has an event.** O the turning sky and push-in; A the push and disk stream; B tilted ring → arch; C 22× → 1.5×; D stars zipping along the line and the sweep; E the line opens, the lap, the flash, the double take; F half the sky → the dot; G the creep and the fade to the loop frame.
- **Reads have time and don't overlap.** Text pops (REAL PHYSICS SIMULATION, BACK/FRONT, 1.5×, BLACK HOLE, YOU, 1.001×) each land on a settled frame and are ≤4 words. The VO names what's already on screen ("flat" after the tilt, "back half, front half" as the tags pop, "like this" as the arch rises, "circles" while the pulse runs, "that line?" as we look along it, "the back of your own head" as it opens).
- **No new idea lands on a payoff.** The arch (10.67–12.0), the flash (24.0, then the VO names it) and the dot (32.0–33.3) hold with no new information.
- **Every seam has a transition, and they vary.** Seamless loop (G→O), inverted match cut as a 0.16 s dissolve (O→A), camera move (A→B→C), braked arrival (C→D), match cut line → circle as a 0.24 s dissolve (D→E), a 0.24 s dissolve after the flash to first person (E→E2), continuous with a whip pull-out (E2→F), continuous (F→G). No hard cut is left: the round-8 note was that the transitions felt "super unnatural and sharp".
- **The ending rhymes with the opening.** It *is* the opening frame: the dot, now understood.
- **Every setup pays off on screen.** The dot claim (O) pays off in F–G; the BACK tag in B pays off as the arch; the line in D is explained in E; the counter's "HORIZON = 1×" is approached to 1.001× in F; "hover" (said in D and F) is the condition the dot needs.
- **On-screen text never restates the image.** REAL PHYSICS SIMULATION, BACK/FRONT, the distance counter, 1.5× PHOTON SPHERE, the BLACK HOLE tag in D, YOU, * DIAGRAM, NOT TO SCALE, * MAGNIFIED ILLUSTRATION, LOOKING UP ↑, 1.001× 0.1% ABOVE THE EDGE, 1 MIN DOWN HERE → 32 MIN OUT THERE, THE UNIVERSE and the BLACK HOLE arrows each add something the picture and VO don't say.
- **Safe zone.** Captions sit at 60–73% of the height and labels in the upper third; nothing below 80% or in the right-hand button column (checked every 0.1 s by `tools/safezone.py`).
