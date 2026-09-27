# Script and beat sheet: version 2 (round 13)

Version 1's script is in `outputs/v1/script.md`.

**What changed from version 1.** The user: "it feels like there's not too much content… Cleo Abram usually gives you lots of interesting facts, references… in our video there is only a black hole object". A study of 18 Cleo Abram and 13 Veritasium Shorts (research.md, "Version 2 research") found our fact rate close to theirs. What was missing: references (named people, dates, real objects), real imagery as proof next to the simulation, visual variety, and an everyday stake. Version 2 keeps version 1's plain, pointing narration and adds:
- **The real thing first:** the Event Horizon Telescope's photo of M87*, the first photo of a black hole (released 2019). The glowing dot turns into it, and it turns into our simulation.
- **A number with an anchor:** "It's as heavy as six and a half billion Suns. And our whole solar system is this tiny circle." Pluto's orbit is drawn to scale inside the photo.
- **Expectation, then reversal (Veritasium):** "As we go back down, you'd expect it to hide behind the black hole. But gravity bends its light…"
- **Named, dated references:** Jean-Pierre Luminet drew the first picture of this by hand in 1979, shown over our frame redrawn in dots. Interstellar's black hole used the same physics.
- **An everyday stake:** "Even GPS feels this. Up in orbit, clocks run fast, and without a fix, your map would drift ten kilometers a day." This plays over Apollo 17's photo of Earth.

**Voice.** ElevenLabs "Liam" (`TX3LPaxmHKxFdv7VOQHJ`) on `eleven_v3`.
- **The take:** one continuous read of the whole script, seed 163 at stability 0.0, chosen from three auditioned reads. It was the only one with every line heard exactly and none whispered.
- **Re-read lines:** after the fresh-eyes critic, three reworded lines were re-read in context with three lines of run-up, choosing each group's take by pitch and pace against its neighbours (seed 19 for the photo lines, seed 7 for GPS). They were level-matched and spliced in. A re-read's end is taken where its voice decays, not where its room tone fades: the GPS re-read's tail had put the line 0.8 s long, its captions late and a dead pause after it (round 14).
- **Pauses:** 0.14–0.55 s between lines, the read's own. The "..." beats inside lines are capped at 0.45 s. Longer waits only where the picture moves first: the solar-system circle, the rise, the swing down, the dive, the lens, the dot, and the Earth card in and out.
- **The picture follows the voice:** `bh/warp.json`, computed from the placed words.

**Pace.** 256 words in 92.7 s: 2.8 words/s overall, about 3.1 inside a line.

## Narration

> See this glowing dot? That's the whole universe.
>
> To see why, look at this.
>
> This is the first real photo of a black hole, released in 2019.
>
> It's as heavy as six and a half billion Suns. And our whole solar system is this tiny circle.
>
> And up close, it would look like this. The bright ring is hot gas, spinning around it.
>
> Let's look at it from above.
>
> See? The disk is actually flat.
>
> This is the back half. And this is the front half.
>
> As we go back down, you'd expect it to hide behind the black hole.
>
> But gravity bends its light, up over the top... and under the bottom.
>
> In 1979, Jean-Pierre Luminet drew this by hand, dot by dot.
>
> And Interstellar's black hole used the same physics.
>
> Now let's fly in closer. Much closer.
>
> If you hover right here, the black hole fills exactly half your sky.
>
> And see this thin line? It's light that goes all the way around the black hole... and comes back to you.
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
> Even GPS feels this. Up in orbit, clocks run fast, and without a fix, your map would drift ten kilometers a day.
>
> And all this darkness around the dot? That's the black hole.
>
> *(1.8 s of quiet, then the loop)* See this glowing dot?

**Facts and references.** 17 facts in 93 s (1.8 per 10 s). The spoken references:
- M87*'s photo, released 2019
- 6.5 billion Suns
- our solar system
- Jean-Pierre Luminet, 1979
- Interstellar
- GPS, 10 km a day

On-screen-only references: the Event Horizon Telescope, Pluto's orbit, the IBM 7040, Kip Thorne and 2014, Apollo 17 and 1972. That's 11 in all, 1.2 per 10 s.

## Beat sheet

Video time on the left. Picture events follow the words (`bh/warp.json`). Labels and inserts are timed from the words that name them.

| time | narration | visual | on-screen text | SFX / music | transition |
|---|---|---|---|---|---|
| 0.00–3.76 | "See this glowing dot? That's the whole universe." (0.14–2.56) "To see why, look at this." (2.95–4.47) | the glowing ice dot; the sky inside it turns, slow push-in | REAL PHYSICS SIMULATION | high shimmer; the music's sparse first bars | seamless loop from the end |
| 3.76–4.31 | ↑ | **the dot becomes the real photo**: M87*'s ring laid exactly over the dot | FIRST PHOTO OF A BLACK HOLE / M87* · EVENT HORIZON TELESCOPE · 2019; credit "Image: EHT Collaboration, CC BY 4.0" | reverse swell and a low hit on "this" | 0.55 s dissolve, dot → photo (same size, same place) |
| 4.61–8.44 | "This is the first real photo of a black hole, released in 2019." | the photo, slow push-in | ↑ | groove begins | — |
| 8.99–14.83 | "It's as heavy as six and a half billion Suns. And our whole solar system is this tiny circle." | a gold circle pops inside the photo's dark centre on "tiny" (13.7) and holds | OUR SOLAR SYSTEM (PLUTO'S ORBIT, TO SCALE) | pop | — |
| 15.71–20.66 | "And up close, it would look like this. The bright ring is hot gas, spinning around it." | **the photo becomes our simulation** (15.8–16.4): the black hole side-on, the disk streaming | REAL PHYSICS SIMULATION; DISK OF HOT GAS on "The bright ring" | whoosh | 0.6 s dissolve, photo → simulation |
| 21.21–22.31 | "Let's look at it from above." | the rise starts on "at it" (21.7) | — | airy whoosh | camera move |
| 23.49–25.62 | "See? The disk is actually flat." | the flat ring from above | — | — | — |
| 26.09–29.16 | "This is the back half. And this is the front half." | the far half turns ice on "back half" (26.7–27.1) | BACK (26.1), FRONT (27.8) | a tick each | — |
| 29.62–32.90 | "As we go back down, you'd expect it to hide behind the black hole." | the swing down (29.6–33.0) | tags fade | whoosh down | camera move |
| 33.00 | — | **the ice arch over the hole** | BACK on the arch | deep hit | — |
| 33.35–37.90 | "But gravity bends its light, up over the top... and under the bottom." | slow push, the lower ice arc | a small BACK on the lower arc on "and under" (36.6) | groove | — |
| 38.28–43.06 | "In 1979, Jean-Pierre Luminet drew this by hand, dot by dot." | our frame turns into white ink dots on black, denser where brighter; underneath, the ice fades back to gold | 1979 · JEAN-PIERRE LUMINET / THE FIRST PICTURE OF THIS, COMPUTED ON AN IBM 7040 AND DRAWN BY HAND / * OUR SIMULATION, REDRAWN IN DOTS HIS WAY | a soft chime | 0.4 s dissolve in and out of the dots |
| 43.25–46.44 | "And Interstellar's black hole used the same physics." | the gold arch (as in the film), no film images | INTERSTELLAR (2014) / ITS BLACK HOLE WAS RENDERED FROM KIP THORNE'S EQUATIONS | low pop | — |
| 46.72–49.58 | "Now let's fly in closer. Much closer." | the counter fades in (46.7); the dive starts on "fly" (47.5) | 20× counting down live | riser, dive rush | camera move, braked arrival (49.9) |
| 50.26–54.47 | "If you hover right here, the black hole fills exactly half your sky." | half black, half bright sky, the line between | 1.5× / LIGHT CAN ORBIT HERE; BLACK HOLE in the black half | impact, shimmer | arrival |
| 54.98–60.61 | "And see this thin line? It's light that goes all the way around the black hole... and comes back to you." | a glow sweeps along the line; the line opens into the diagram's circle (56.3); a pulse runs the lap and **flashes in the visor** on "you" (60.05) | LIGHT (pointer); * DIAGRAM, NOT TO SCALE; YOU | whoosh; slow harp run; chime on the flash | match cut, line → circle (0.34 s dissolve) |
| 61.16–64.22 | "So in this line, you see the back of your own head." | first person at the line; it opens like an eye onto the back of your own helmet, which turns; it closes | * MAGNIFIED ILLUSTRATION | whoosh; glassy shimmer | 0.35 s dissolve, diagram → first person |
| 64.67–68.70 | "Now let's go lower, and hover just above the edge. Then look up." | sinking; the tilt up runs on "Then look up" | the counter returns (65.1) and counts down from 1.5× | long riser | continuous |
| 68.99–72.74 | "The whole universe shrinks into one small dot above you." | the bright circle shrinks into the dot | the counter (→ 1.001×) | riser peaks; the build ends | — |
| 72.89 | — | **the dot lands**, as in frame 0 | 1.001× / 0.1% ABOVE THE EDGE | hit; the music drops to one high tone | — |
| 73.34–79.17 | "And down here, time runs slower. Stay for one minute... and half an hour goes by out there." | the sky in the dot sweeps one full turn as the counter climbs (77.2–79.2) | 1 MIN / DOWN HERE (76.1) → 32 MIN / OUT THERE (77.4) | pops | — |
| 79.62–87.02 | "Even GPS feels this. Up in orbit, clocks run fast, and without a fix, your map would drift ten kilometers a day." | **Apollo 17's Earth** (1972) with a GPS orbit and a satellite going round | FASTER / WHERE GRAVITY IS WEAKER (82.4), then 10 KM / MAP DRIFT A DAY, IF NOT FIXED (85.7); credit "Earth: NASA, Apollo 17, 1972" | whoosh in; pops | 0.45 s dissolve in and out of the Earth card; it is gone before the next line |
| 87.57–90.91 | "And all this darkness around the dot? That's the black hole." | the dot again | THE UNIVERSE (87.8); BLACK HOLE with four arrows out into the black (89.9) | soft hit | — |
| 90.91–92.67 | *(quiet)* | labels fade; the push-in and turning sky continue | — | shimmer; a reverse swell into the loop | **seamless loop** into frame 0 |

## Captions

The captions are burned in and word-synced (`tools/caption_align.py`), and `captions_en.srt` has the same text for upload. Each chunk is a whole phrase; the style is as in version 1:
- Montserrat Black 80 px, white, with gold key words.
- Centred, with the baseline at 69% of the height, clear of the bottom 20% and the button column.
- Chunks ease in and cross-fade into each other.
