# Script and beat sheet (v5)

**Voice.** ElevenLabs "Liam – Energetic, Social Media Creator" (`TX3LPaxmHKxFdv7VOQHJ`, premade, young American male), the user's pick, on `eleven_v3` at stability 0.0 ("creative"). The whole narration is **one continuous performance**: a single v3 read of the full script (seed 179), chosen from sixteen by `tools/vo_flow.py`. Inside each line nothing is touched: the breath before it, the words, and its natural tail are the read's own. To fit the picture, only the silent middle of a pause gets longer or shorter, and four lines are tightened by WSOLA by 1–6% (the cap is 8%). Under the whole track runs a bed of room tone made from the read's own pauses, so the voice's background never switches on and off, and each line crossfades into it over 0.1–0.3 s. The time-dilation beat was rewritten after the read was chosen (round 9: "Out there, time is on fast-forward" was too quick to land). Its two new lines are re-read together with the same seed and settings, with three lines of run-up before them and the last line after, so they carry the read's voice. The take is chosen from eight seeds: every word heard exactly, pitch closest to the lines either side (103 and 115 Hz against 116), and pace no quicker than theirs. It is then level-matched and spliced in. An ellipsis in "Stay for one minute..." makes the voice take a half-second beat before the payoff; with a comma, it ran on. Processing (`tools/mix.py`): an 80 Hz high-pass, a light de-esser, 2.5:1 soft-knee compression, and a touch of the effects' room.

Earlier versions picked each line from whichever read did it best. That put lines from different performances side by side (one at 99 Hz, the next at 146 Hz), and every line faded in and out of digital silence. The user heard it as "transitions in speech… super unnatural and sharp".

**Pace.** 115 words over 43.3 s: 2.7 words/s overall. The voice runs at Liam's own v3 pace inside a line and pauses where he paused (research.md: the median narrated Short is ≈3.0 words/s, with real pauses at payoffs as in Vsauce and Veritasium).

## Narration

> See this dot? That's the whole universe.
>
> Here's how. This is a black hole.
>
> That disk is actually flat. Back half, front half.
>
> So why does it look like this?
>
> That's the back of the disk, bent over the top by gravity, and under the bottom.
>
> Now let's fly in. Way closer.
>
> Hover here, and the black hole fills exactly half your sky.
>
> Here, light goes in circles.
>
> That line? The back of your own head.
>
> Now hover just above the horizon, and the whole universe shrinks to one dot overhead.
>
> And down here, time runs slower.
>
> Stay for one minute... and half an hour goes by out there.
>
> All that darkness around it? That's the black hole.
>
> *(loop)* See this dot? That's the whole universe.

Each line and its reaction:

- The claim over the dot: *wtf*.
- "Here's how. This is a black hole.": the promise, then the thing itself.
- "That disk is actually flat. Back half, front half.": said while the camera shows the flat ring and the two halves light up, so the words and the picture arrive together.
- "So why does it look like this?", then the back of the disk over the top and under the bottom: *wow*.
- Half your sky: *wow*.
- "That line? The back of your own head.", while the line opens into your own helmet: *lol*.
- The universe in one dot: *omg*, and a callback to the first line.
- "And down here, time runs slower. Stay for one minute... and half an hour goes by out there.": a second *omg* on the same image, told as something you could do. On screen, 1 MIN counts up to 32 MIN. To a hovering observer here, everything outside runs 31.6× fast, so a minute here is 31.6 minutes out there.
- "All that darkness around it? That's the black hole.": the answer to the whole video. Then 1.35 s of quiet on the dot before the loop comes back to "See this dot?".
- Round 9 (the user: the time line "sounds fast and is not natural… maybe explain it a bit more… it's okay if the short will be a bit longer"; "the video ends exactly on phrase end… can you make the phrase end, then wait a moment"): "Out there, time is on fast-forward." became two unhurried sentences with a concrete example. The video grew from 37.3 to 43.3 s, and the last word now ends 1.35 s before the loop.
- Round 7 (the user: "we need to make speech more natural during the whole video"): every line was rewritten to sound spoken, not read. Each line points at what is on screen ("See this dot?", "That disk is…", "That line?"), and the transitions say why we move on ("Here's how.", "Now let's fly in.", "Out there,"). The fact about the inner edge at half light speed was cut. It was the one line that had nothing on screen to point at.

## Beat sheet

Bars at 90 BPM: 0.00, 2.67, 5.33, 8.00, 10.67, 13.33, 16.00, 18.67, 21.33, 24.00, 26.67, 29.33, 32.00, 34.67, 37.33, 40.00; the video ends on the 65th beat, 43.33. Voice times are the placed speech (from `tools/vo_flow.py`); labels and their pops are timed from the caption words that name them.

| time | narration | visual | read (eye) | SFX / music | on-screen text | transition |
|---|---|---|---|---|---|---|
| 0.00–2.67 | "See this dot? That's the whole universe." (0.14–2.66) | glowing ice dot, about half the width, in black; the sky inside it turns, slow push-in | the dot | high shimmer tone; soft sub | REAL PHYSICS SIMULATION (top, 0.5–2.55) | seamless loop from G |
| 2.67–5.33 | "Here's how. This is a black hole." (2.87–5.30) | the black hole, shadow at the dot's size and place; push-in | the shadow, then the arch | whoosh and low hit on 2.67; music pulse enters | — | **inverted match cut**, dot → shadow, as a 0.16 s dissolve |
| 5.33–7.10 | "That disk is actually flat." (5.44–7.4) | camera rises; the disk opens into a tilted ring | ride the disk | airy whoosh | — | camera move |
| 7.10–9.00 | "Back half, front half." (7.5–8.9) | far half turns ice, near half stays gold | BACK, then FRONT | a soft tick with each tag | BACK (ice, 7.50), FRONT (gold, 8.25), each on its word | — |
| 9.00–10.67 | "So why does it look like this?" (9.17–10.64) | swing down to the side | the ice half | whoosh down plus a riser | tags fade by 9.1 | — |
| 10.67–11.00 | — | **the ice arch over the hole** | the arch | deep hit on 10.67 | BACK (on the arch, 10.9) | — |
| 11.11–15.45 | "That's the back of the disk, bent over the top by gravity, and under the bottom." | slow push; ice fades to gold from 13.5 | the arch, then the lower ice arc | music | a small BACK on the lower arc as the voice says "and under" (14.3) | — |
| 15.30–16.00 | — | settle | the counter | riser | distance counter fades in: 20×, YOUR DISTANCE · HORIZON = 1× | — |
| 16.00–18.67 | "Now let's fly in. Way closer." (16.02–18.53) | the dive 20× → 1.5×, streaks, pitch to the horizon | the swelling black; the counter | big dive whoosh plus rumble, ducked under the voice | the counter counts down live | camera move, braked arrival |
| 18.67–19.90 | — | half black, half bright sky, a line across the middle | label → line | impact on 18.67 plus shimmer | the counter lands: 1.5× / THE PHOTON SPHERE | arrival |
| 18.72–22.25 | "Hover here, and the black hole fills exactly half your sky." | yaw; stars zip along the line; a glow sweeps along it at 21.3 | the halves, then the line | shimmer bed; rising tone with the sweep | BLACK HOLE (gold, in the black half, 19.55–22.0) | — |
| 22.20–24.55 | "Here, light goes in circles." (22.58–24.19) | edge-on line opens into a ring around a black sphere; astronaut on it; a pulse runs the lap from the back of the helmet and **flashes in the visor** (24.0) | the ring, the pulse, the visor | whoosh-in; a harp glissando with the pulse; bright chime on 24.00 | YOU (22.5, leader to the helmet); * DIAGRAM, NOT TO SCALE | **match cut**, line → circle, as a 0.24 s dissolve |
| 24.55–24.95 | "That line?" (24.42–24.9) | first person at the photon sphere, pushing in on the line | the line | whoosh into the cut | — | 0.24 s dissolve, diagram → first person |
| 24.95–26.30 | "The back of your own head." (25.4–26.66) | **the line opens like an eye into the back of your own helmet**; the head turns (25.5–25.95); the lens closes (25.95–26.3) | the helmet | glassy shimmer while it's open | * MAGNIFIED ILLUSTRATION | — |
| 26.30–26.67 | — | whip pull-out into F | the line | whoosh out, soft hit | — | **continuous** into F |
| 27.09–29.8 | "Now hover just above the horizon," | sinking and tilting up; the bright sky rolls up into a circle | the sky | long riser starts | LOOKING UP ↑ (26.95–28.25); the counter returns at 28.3 | — |
| 28.9–31.89 | "…and the whole universe shrinks to one dot overhead." | the circle shrinks to the dot, turning ice | the circle, the counter | riser peaks | the counter counts 1.2× → 1.001× | — |
| 31.90–32.68 | — | **the dot**, as in frame 0 | the dot | hit on 32.00; music drops to one high tone that decays to silence by 41 s | the counter lands: 1.001× / 0.1% ABOVE THE EDGE (to 35.57) | — |
| 32.68–34.87 | "And down here, time runs slower." | the push-in and the turning sky | the dot, the 1.001× | shimmer | — | — |
| 35.49–38.75 | "Stay for one minute... and half an hour goes by out there." | ↑ | the number | low pop on "Stay" (35.57); pop on "and half" (37.09) | 1 MIN / DOWN HERE (35.57), counting up to 32 MIN / OUT THERE over 0.9 s from 37.09, to 39.24 | — |
| 39.26–41.98 | "All that darkness around it? That's the black hole." | creep | the dot, then out into the black | low soft hit on "That's the black hole" (40.87) | THE UNIVERSE (ice leader on the dot, 39.34); BLACK HOLE (gold, four arrows pointing out into the black, 40.87) | — |
| 41.98–43.33 | *(quiet: 1.35 s)* | labels hold, then fade (42.58–43.03); the push-in and the turning sky continue | the dot | shimmer; a reverse swell into the loop | — | **seamless loop** into frame 0 |

## Captions

Burned in and word-synced. Each chunk's start comes from Whisper's word timings on the finished voice track, refined to the voice's own onset (`tools/caption_align.py`), and a chunk that starts mid-line appears 0.12 s before its first word. Each chunk is a whole phrase, split only where the voice breathes, and wraps to two balanced lines when it is long:

- SEE THIS DOT? (from frame 0) / THAT'S THE WHOLE UNIVERSE. (held to the 2.67 cut)
- HERE'S HOW. / THIS IS A BLACK HOLE.
- THAT DISK IS ACTUALLY FLAT. / BACK HALF, / FRONT HALF.
- SO WHY DOES IT LOOK LIKE THIS?
- THAT'S THE BACK OF THE DISK, / BENT OVER THE TOP BY GRAVITY, / AND UNDER THE BOTTOM.
- NOW LET'S FLY IN. / WAY CLOSER.
- HOVER HERE, / AND THE BLACK HOLE FILLS / EXACTLY HALF YOUR SKY.
- HERE, LIGHT GOES / IN CIRCLES.
- THAT LINE? / THE BACK OF YOUR OWN HEAD.
- NOW HOVER JUST ABOVE THE HORIZON, / AND THE WHOLE UNIVERSE / SHRINKS TO ONE DOT OVERHEAD.
- AND DOWN HERE, / TIME RUNS SLOWER.
- STAY FOR ONE MINUTE... / AND HALF AN HOUR GOES BY OUT THERE.
- ALL THAT DARKNESS AROUND IT?
- "That's the black hole." is not captioned under the dot. It appears as the gold BLACK HOLE callout with arrows pointing out into the black.

Style: Montserrat Black 80 px (cap height ≈56 px, 2.9% of 1920; shrinks to 60 px at most for a long chunk), white with a soft dark shadow and thin dark stroke. One gold `#FFC24A` key word per line: *universe, black hole* (A only), *flat, back, front, this, back, closer, half, circles, head, shrinks, dot, slower, minute, hour, darkness*. Centred at x = 540, max width 780 px (so it clears the right-hand button column), baseline at 69% of the height, clear of the bottom 20%. Each chunk eases in (scale 0.965 → 1.0 with a fade); one followed by a pause fades out over 0.12 s, and one followed straight away by the next cross-fades into it over 0.08 s. A soft scrim darkens only bright backgrounds behind the caption band.
