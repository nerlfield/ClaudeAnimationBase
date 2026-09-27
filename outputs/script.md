# Script and beat sheet (v7, round 12)

**Voice.** ElevenLabs "Liam – Energetic, Social Media Creator" (`TX3LPaxmHKxFdv7VOQHJ`, premade, young American male), the user's pick, on `eleven_v3` at stability 0.5. The narration is **one continuous read** of the whole script: seed 19, chosen from six auditioned reads by `tools/vo_flow.py --audition`. It was the only take with every line heard exactly by Whisper and none whispered or in vocal fry. It also had the most pitch movement (5.5 semitones on average). Nothing inside a line is edited, and no line is squeezed. Each line keeps its breath before and its natural tail. A bed of room tone made from the read's own pauses runs under the whole track, so the voice's background never switches on and off.

**The picture follows the voice.** Until round 10, the voice was fitted into a fixed picture, and its pauses were shortened to fit. Now the voice is placed at its own pace. The picture is re-timed around it by a smooth time map from video time to the animation's clock (`bh/shots.py` `WARP`):
- holds stretch to fit the lines about them;
- each camera move finishes before the line that describes its result;
- cuts land on the words that need them.

Processing (`tools/mix.py`): an 80 Hz high-pass, a light de-esser, 2.5:1 soft-knee compression, and a touch of the effects' room.

**Pace.** 186 words in 68.7 s (2.7 words/s overall, 3.1 words/s inside a line). Round 12 shortened the pauses (the user: "sometimes it's way too large pause in between phrases"):
- **Between lines:** 0.25–0.55 s, the read's own pause capped at 0.55 s (it was up to 1.1 s).
- **Inside a line:** the "..." beats are cut to at most 0.45 s (they ran 1.0–1.2 s).
- **Camera moves:** about 1 s, only where the picture moves before a line: the reveal, the rise, the swing down, the dive and the dot landing.
- **The end:** 1.4 s of quiet before the loop. This is slower than the reference median (≈3.0 words/s) on purpose. The user asked for speech that is "smooth, clear, direct, clean", as if explaining to a three-year-old, and said a longer video is fine.

**How it's written.** The user's notes, in order:
- "too scripted, feels like a robot";
- "the disk you see is actually flat… we need to make speech more natural";
- "transitions in speech and video feel super unnatural and sharp";
- "it's too fast and it's not clear or direct enough… you're using too little of phrases like: this is, there is".

So the script now:
- says one idea per sentence, in everyday words;
- points at what is on screen ("See this glowing dot?", "This is a black hole.", "This is the back half. And this is the front half.", "And see this thin line?");
- announces each move before it happens ("Let me show you why.", "Let's look at it from above.", "Now let's fly in closer.", "Now let's go lower… Then look up.");
- names the result only after the picture has shown it ("See? The disk is actually flat." starts 0.3 s after the rise ends).

The writing rules from the brief still hold: no em dashes, no "it's not X, it's Y", no hype words, no moral at the end.

## Narration

> See this glowing dot? That's the whole universe.
>
> Let me show you why.
>
> This is a black hole. And this bright ring is hot gas, spinning around it.
>
> Let's look at it from above.
>
> See? The disk is actually flat.
>
> This is the back half. And this is the front half.
>
> Now watch the back half, as we go back down.
>
> The black hole bends its light, up over the top... and under the bottom.
>
> Now let's fly in closer. Much closer.
>
> If you hover right here, the black hole fills exactly half your sky.
>
> And see this thin line? That's light, going around the black hole in a circle.
>
> Light can go all the way around... and come back to you.
>
> So in this line, you see the back of your own head.
>
> Now let's go lower, and hover just above the edge. Then look up.
>
> The whole universe shrinks into one small dot above you.
>
> And down here, time runs slower.
>
> Stay for one minute... and half an hour goes by out there.
>
> And all this darkness around the dot? That's the black hole.
>
> *(1.3 s of quiet, then the loop)* See this glowing dot?

The reactions it's built for:
- **wtf:** the claim over the dot.
- **wow:** the back half rising over the top.
- **wow:** half your sky.
- **lol:** the back of your own head, shown in the line.
- **omg:** the universe in one dot, a callback to the first line.
- **omg:** half an hour for your one minute, on the same image.
- **The answer:** "That's the black hole." It turns the first line around, and the loop brings the question back.

## Beat sheet

Video time on the left (the 68.67 s cut). The music's drop is the dot landing (57.11), and its bars are placed back from there on the 90 BPM grid. Each line's time is its placed speech. Labels and their pops are timed from the words that name them; the rest follow the picture.

| time | narration | visual | read (eye) | SFX / music | on-screen text | transition |
|---|---|---|---|---|---|---|
| 0.00–5.08 | "See this glowing dot? That's the whole universe." (0.14–3.20) "Let me show you why." (3.68–4.83) | the glowing ice dot, about half the width, in black; the sky inside it turns, slow push-in | the dot | high shimmer; the music's sparse first bars | REAL PHYSICS SIMULATION (top, 0.5–4.8) | seamless loop from the end |
| 5.08 | — | **the black hole**, its shadow the size and place of the dot | the shadow | whoosh and a low hit | — | inverted match cut, dot → shadow, as a 0.35 s dissolve |
| 5.43–9.97 | "This is a black hole. And this bright ring is hot gas, spinning around it." | slow push-in; the disk's clumps stream round | the shadow, then the ring | the arpeggio groove | DISK OF HOT GAS (gold, on the ring's near side, 7.21) | — |
| 10.52–11.60 | "Let's look at it from above." | a small dip, and the rise starts on "at it" (10.9) | the disk | airy whoosh | — | camera move |
| 10.91–12.41 | ↑ | the camera rises; the disk opens into a flat, tilted ring | ride the disk | ↑ | — | — |
| 12.66–15.07 | "See? The disk is actually flat." | the flat ring, hole in the middle, slow drift | the ring | — | — | — |
| 15.46–18.51 | "This is the back half. And this is the front half." | the far half turns ice on "back half" (16.1–16.5) | BACK, then FRONT | a soft tick with each tag | BACK (ice, 15.49), FRONT (gold, 17.10) | — |
| 19.06–21.33 | "Now watch the back half, as we go back down." | the swing down starts on "as we go back down" (20.5) | the ice half | whoosh down | tags fade as the swing starts | camera move |
| 22.03 | — | **the ice arch stands over the hole** (0.4 s of silence) | the arch | deep hit | BACK (on the arch) | — |
| 22.43–26.47 | "The black hole bends its light, up over the top... and under the bottom." | slow push; the lower ice arc; ice fades to gold from 26.6 | the arch, then the lower arc | groove | a small BACK on the lower arc on "and under" (25.57), fading with the ice | — |
| 27.02–30.09 | "Now let's fly in closer. Much closer." | the counter fades in; the dive starts on "fly in" (28.0) | the swelling black; the counter | riser, then the dive rush under the voice | 20× counting down live | camera move, braked arrival |
| 30.42 | — | arrival: half black, half bright sky, a line across the middle | label → line | impact plus shimmer | 1.5× / THE PHOTON SPHERE; BLACK HOLE in the black half (30.9) | arrival |
| 30.77–35.28 | "If you hover right here, the black hole fills exactly half your sky." | slow yaw; stars slide along the line | the two halves | shimmer bed | BLACK HOLE (gold, to 37.0) | — |
| 35.65–40.15 | "And see this thin line? That's light, going around the black hole in a circle." | a glow sweeps along the line (35.8–37.0); the line opens into the diagram's circle (37.0–38.0) | the line, then the circle | whoosh in | LIGHT (pointer to the line, 35.72); then * DIAGRAM, NOT TO SCALE; YOU | match cut, line → circle, as a 0.3 s dissolve |
| 40.41–43.78 | "Light can go all the way around... and come back to you." | a pulse of light leaves the back of the helmet and runs the whole lap (37.6–43.6), **flashing in the visor** on "you" | the pulse, then the visor | a slow harp run following the pulse; chime on the flash | — | — |
| 44.38–47.48 | "So in this line, you see the back of your own head." | first person at the line again; it opens like an eye (44.7–45.9) into the back of your own helmet, which turns; the lens closes (47.0–47.6) | the helmet | whoosh in; glassy shimmer while it's open | * MAGNIFIED ILLUSTRATION | 0.3 s dissolve, diagram → first person |
| 47.63–48.18 | — | whip pull-out | the line | whoosh out, soft hit | — | continuous |
| 48.08–52.34 | "Now let's go lower, and hover just above the edge. Then look up." | sinking: the bright half of the sky rolls up; the tilt up runs on "Then look up" | the sky; the counter | long riser starts | the distance counter returns on "Now let's go lower" (48.5) and counts down from 1.5× | — |
| 52.89–56.96 | "The whole universe shrinks into one small dot above you." | the bright circle shrinks into the dot, turning ice | the circle; the counter (→ 1.001×) | riser peaks; the music's build ends | the counter | — |
| 57.11 | — | **the dot lands**, as in frame 0 | the dot | hit; the music drops to one high tone that decays to silence | 1.001× / 0.1% ABOVE THE EDGE | — |
| 57.56–59.68 | "And down here, time runs slower." | push-in, the sky inside the dot turning | the dot | shimmer | ↑ | — |
| 60.06–63.83 | "Stay for one minute... and half an hour goes by out there." | on "and half an hour goes by out there" the whole sky inside the dot sweeps one full turn, like a clock hand racing (61.76–63.88) | the number, the turning dot | low pop on "Stay"; pop on "and half" | 1 MIN / DOWN HERE (60.19), counting up to 32 MIN / OUT THERE with the turn (61.73–63.88) | — |
| 64.08–67.28 | "And all this darkness around the dot? That's the black hole." | ↑ | the dot, then out into the black | soft hit on "That's the black hole" (66.24) | THE UNIVERSE (leader to the dot's rim, 64.21); BLACK HOLE (gold, four arrows out into the black, 66.24) | — |
| 67.28–68.67 | *(quiet)* | labels fade (67.9–68.4); the push-in and the turning sky continue | the dot | shimmer; a reverse swell into the loop | — | **seamless loop** into frame 0 |

## Captions

Burned in and word-synced. Each chunk's start comes from Whisper's word timings on the finished voice track, refined to the voice's own onset (`tools/caption_align.py`). A chunk that starts mid-sentence appears 0.12 s before its first word. The same text is in `captions_en.srt` for upload. Each chunk is a whole phrase, split only where the voice breathes, and wraps to two balanced lines when it is long.

- SEE THIS GLOWING DOT? / THAT'S THE WHOLE UNIVERSE.
- LET ME SHOW YOU WHY.
- THIS IS A BLACK HOLE. / AND THIS BRIGHT RING IS HOT GAS, / SPINNING AROUND IT.
- LET'S LOOK AT IT FROM ABOVE.
- SEE? / THE DISK IS ACTUALLY FLAT.
- THIS IS THE BACK HALF. / AND THIS IS THE FRONT HALF.
- NOW WATCH THE BACK HALF, / AS WE GO BACK DOWN.
- THE BLACK HOLE BENDS ITS LIGHT, / UP OVER THE TOP... / AND UNDER THE BOTTOM.
- NOW LET'S FLY IN CLOSER. / MUCH CLOSER.
- IF YOU HOVER RIGHT HERE, / THE BLACK HOLE FILLS / EXACTLY HALF YOUR SKY.
- AND SEE THIS THIN LINE? / THAT'S LIGHT, / GOING AROUND THE BLACK HOLE IN A CIRCLE.
- LIGHT CAN GO ALL THE WAY AROUND... / AND COME BACK TO YOU.
- SO IN THIS LINE, / YOU SEE THE BACK OF YOUR OWN HEAD.
- NOW LET'S GO LOWER, / AND HOVER JUST ABOVE THE EDGE. / THEN LOOK UP.
- THE WHOLE UNIVERSE SHRINKS / INTO ONE SMALL DOT ABOVE YOU.
- AND DOWN HERE, / TIME RUNS SLOWER.
- STAY FOR ONE MINUTE... / AND HALF AN HOUR GOES BY OUT THERE.
- AND ALL THIS DARKNESS AROUND THE DOT?
- "That's the black hole." is not captioned under the dot. It appears as the gold BLACK HOLE callout, with arrows pointing out into the black.

**Style.**
- **Font:** Montserrat Black 80 px (cap height ≈56 px, 2.9% of 1920), shrinking to no less than 60 px for a long chunk; white with a soft dark shadow and a thin dark stroke.
- **Gold words:** the key words in gold `#FFC24A`: *dot, universe, why, black hole, gas, above, flat, back, front, bends, top, bottom, closer, half, line, circle, around, you, head, edge, up, shrinks, dot, slower, minute, hour, darkness*.
- **Position:** centred at x = 540, max width 780 px so it clears the right-hand button column, baseline at 69% of the height, clear of the bottom 20%.
- **Motion:** each chunk eases in (a fade, scaling 0.965 → 1.0). A chunk followed by a pause fades out over 0.12 s; one followed straight away by the next cross-fades into it over 0.08 s.
- **Contrast:** a soft scrim darkens only bright backgrounds behind the caption band.
