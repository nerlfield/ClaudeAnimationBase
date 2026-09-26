# Storyboard: "This dot is the whole universe"

*Version 2, after two rounds of frames-sheet critique (critique.md). Round-2 changes: the G callouts, arrowed light path and bigger astronaut in E, whole-phrase captions, a 41%-wide dot with A's opening field of view matched to it, the gauge relabelled and hidden during E, and B tilted to 58°. v1 opened on a far view of the black hole, which the fresh-eyes critic called "the most-seen black hole image online", and it lost them on the flat-disk still, the dive and the near-black ending. v2 opens on the video's most surprising image and ends on exactly that frame.*

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

**HUD: the depth gauge.** A vertical ladder at the left edge (x 60–260, y 330–1080, clear of captions and the right-side UI), titled "DISTANCE" with a small "(HORIZON = 1×)". Ticks at 25×, 10×, 3×, 1.5× and 1× HORIZON, labels 34 px. An ice "YOU ▸" marker sits on the left of the line (so it never covers a label) and slides during the moves, never touching the HORIZON tick until the very end. Visible 15.0–22.2 and 26.67–36.9.

---

## Shots

### O: Cold open, the dot · 0.00–2.67 · [in: the loop from G, identical frame]
- **Seen.** A glowing ice-blue circle (35% of frame width, centred at 42% height) in black. Inside it, the whole sky squeezed and blueshifted: the disk as a bright ring, the Milky Way as a pale band, stars. Soft bloom haze around it; grain in the black.
- **Event.** The dot slowly rolls and shrinks a hair as we creep closer (continuous with G).
- **Camera.** Looking straight up from 1.001× the horizon radius, vertical field of view 45°, a 0.35°/s roll.
- **Reads.**
  - 0.00–0.90: a glowing orb in darkness. The eye lands on the dot.
  - 0.15–2.10: VO "This dot is the whole universe." Caption "THIS DOT IS / THE WHOLE UNIVERSE."
  - 0.60–2.50: top label "REAL PHYSICS SIMULATION" (46 px, bright). It tells you this isn't art.
- **Out.** On the 2.67 bar, a match cut with inversion: the bright dot becomes the black hole's dark shadow, same size and position, under a whoosh and a rim flash.

### A: The black hole · 2.67–5.33 · [in: inverted match cut]
- **Seen.** The black hole from 22× the horizon radius, 8° above the disk plane. The shadow is 35% of the frame width at 42% height, ringed by the thin photon ring. The disk's back arches over the top and its underside shows under the bottom; the left (approaching) side is brighter and bluer.
- **Event.** The camera pushes in slowly while the disk's hot clumps stream around.
- **Camera.** Push r 22.3 → 21, 0.6° roll drift; a 1° dip at 5.1 (anticipation of the rise).
- **Reads.**
  - 2.67–3.60: a black hole (the eye goes to the shadow, where the dot just was).
  - 2.85–5.20: VO "To see it, fly down to a black hole." Caption "TO SEE IT, / FLY DOWN / TO A BLACK HOLE."
- **Out.** Camera move into B.

### B: Flat, then not · 5.33–16.00 · [in: continuous camera move]
- **Seen.** The camera rises to 40° above the disk: the disk is now obviously a flat tilted ring, like Saturn's rings, with the hole in its middle. The far half lights up ice with a label "BACK", the near half keeps its gold with "FRONT". The camera swings back down to the side, and the ice half rises and bends over the top of the hole into the arch. It was the back of the disk all along.
- **Event.** Flat tilted ring → arch, with the ice tag carrying the identity across.
- **Camera.** Rise 5.33 → 7.10 (θ 82° → 40°, pulling back to r 30 so the ring fits), hold with a 3° yaw drift until 8.6, swing down 8.6 → 10.67 with a 2° overshoot and settle on the 10.67 bar, then a slow push to 16.0.
- **Reads.**
  - 5.33–7.10: the view tilts and the disk opens into an ellipse. The eye rides the disk.
  - 6.00–7.60: VO "The disk around it is flat." The eye is on the tilted ring.
  - 7.10–8.60: BACK (ice) and FRONT (gold) pop on the two halves, 0.2 s apart. The eye goes to BACK, the brighter, colder half.
  - 8.60–10.67: the swing down. The labels fade at 9.0 and the eye tracks the ice half. VO "So why does it look like this?" (9.0–10.6).
  - 10.67–12.00: **the ice arch stands over the hole.** No voice. A small "BACK" re-pops on the arch at 10.9.
  - 12.00–15.00: VO "That's the back of the disk, bent over the top by gravity." The ice slowly returns to gold from 13.5.
  - 15.00–16.00: the gauge fades in (YOU at 22×). A riser starts.
- **Out.** Camera move into C.

### C: The dive · 16.00–18.67 · [in: camera move]
- **Seen.** We plunge from 22× to 1.5×, pitching from "hole ahead" to "hole below". The disk sweeps past as a streaking band and the shadow's edge swells up from the bottom of the frame.
- **Event.** 22× → 1.5× (the YOU marker slides all the way down the gauge).
- **Camera.** Eased dive in log-radius with a braked arrival on the 18.67 bar; motion blur (3 sub-frames).
- **Reads.**
  - 16.00–18.67: we're diving in. The eye follows the swelling black and the sliding YOU. No voice (spectacle and whoosh).
- **Out.** A braked arrival with an impact on the bar; same camera into D.

### D: The photon sphere · 18.67–22.20 · [in: arrival]
- **Seen.** Hovering at 1.5×, looking along the horizon. The bottom half is pure black; the top half is the whole outside sky, brighter and bluer, with the disk's lensed light arching across. A razor-thin bright line runs straight across the middle where the halves meet.
- **Event.** A slow yaw; stars that pass behind the hole zip along the line. At 21.3 a glow sweeps along the line from left to right and it brightens (lead the eye).
- **Camera.** 6° yaw drift, 0.4° roll wobble.
- **Reads.**
  - 18.67–19.90: half black, half light. A big "1.5×" with "PHOTON SPHERE" pops in the upper third, then shrinks into the gauge by 20.0. The eye goes label → line.
  - 19.00–21.90: VO "Hover here, and the black hole fills exactly half your sky." The eye moves between the halves.
  - 21.30–22.20: the sweep along the line. The eye is on the line.
- **Out.** Match cut on the line: E opens exactly edge-on, so the bright line continues across the cut before it opens into a circle.

### E: The back of your head · 22.20–26.67 · [in: match cut, line → circle]
- **Seen.** Diagram, labelled "* DIAGRAM, NOT TO SCALE". From below the ring plane: the black horizon sphere, the photon sphere drawn as a thin circle of light, and on it an astronaut (14% of frame width, in the upper half) labelled "YOU" with a leader line to the helmet. A pulse of light leaves the back of the helmet, runs the whole lap and hits the visor with a flash; its path stays drawn as a faint trail.
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
- **Event.** Half the sky → the dot. The gauge marker creeps to just above HORIZON.
- **Camera.** Pitch to straight up (26.67–29.5, ease in/out), vertical field of view 60° → 45°, the radius eased so the dot's size lands on the 32.0 bar, 0.35°/s roll.
- **Reads.**
  - 26.67–27.20: the match cut; we're back at the line.
  - 26.90–28.80: VO "Now hover just above the edge." The eye follows the bright sky as it rolls up.
  - 29.00–32.30: VO "The whole universe gets squeezed into one dot above your head." The eye is on the shrinking circle. "1.001×" with "0.1% ABOVE THE EDGE" pops in the upper third at 29.6–31.2.
  - 32.00: the dot lands.
- **Out.** Continuous into G.

### G: Everything else · 32.00–37.33 · [out: the loop, this frame continues into O]
- **Seen.** The dot, the same framing as frame 0, creeping smaller as we inch down. "STARLIGHT: 30× BLUER" sits under it (32.3–33.6).
- **Event.** The last creep; the gauge fades out (36.3–36.9) so the final frames are identical to O's.
- **Camera.** The same continuous function as O (G at time t equals O at time t − 37.33), so the loop has no seam.
- **Reads.**
  - 32.00–33.30: **the dot, the whole universe, held 1.3 s** with its label.
  - 33.40–34.20: VO "Everything else?"
  - 34.20–35.00: a beat.
  - 35.00–35.70: VO "Black hole." The eye takes in the black around the dot.
  - 35.70–37.33: hold. The last read gets 1.6 s to land, then the loop into "This dot is the whole universe."

---

## Storyboard checks

- **Every shot has an event.** O the roll and creep; A the push and disk stream; B tilted ring → arch; C 22× → 1.5×; D stars zipping along the line and the sweep; E the line opens, the lap, the flash, the double take; F half the sky → the dot; G the creep and the fade to the loop frame.
- **Reads have time and don't overlap.** Text pops (REAL PHYSICS SIMULATION, BACK/FRONT, 1.5×, YOU, 1.001×, STARLIGHT) each land on a settled frame and are ≤4 words. The VO names what's already on screen ("flat" after the tilt, "like this" as the arch rises, "circles" while the pulse runs, "back of your own head" after the flash).
- **No new idea lands on a payoff.** The arch (10.67–12.0), the flash (24.0, then the VO names it) and the dot (32.0–33.3) hold with no new information.
- **Every seam has a transition, and they vary.** Seamless loop (G→O), inverted match cut (O→A), camera move (A→B→C), braked arrival (C→D), match cut line → circle (D→E), circle → line (E→F), continuous (F→G).
- **The ending rhymes with the opening.** It *is* the opening frame: the dot, now understood.
- **Every setup pays off on screen.** The dot claim (O) pays off in F–G; the BACK tag in B pays off as the arch; the line in D is explained in E; the gauge's HORIZON tick is reached in F; "hover" (said in D and F) is the condition the dot needs.
- **On-screen text never restates the image.** REAL PHYSICS SIMULATION, BACK/FRONT, the gauge, 1.5× PHOTON SPHERE, YOU, * DIAGRAM, NOT TO SCALE, 1.001× 0.1% ABOVE THE EDGE and STARLIGHT: 30× BLUER each add something the picture and VO don't say.
- **Safe zone.** Captions sit at 60–73% of the height, labels in the upper third and the left gauge; nothing below 80% or in the right 12%.
