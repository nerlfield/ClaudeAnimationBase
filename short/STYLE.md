# Style bible: "The other screen"

One look, defined once in [src/look.js](src/look.js). Every shot paints through it.

## Medium

The repo's painted look, as you asked, not the guide's default of WebGL 3D. That means p5.brush in 2D: flat washes, ink outlines that boil 10 times a second (each drawing holds 3 frames at 30 fps), paper grain and a vignette multiplied over everything, and `glow()` for anything that emits light. There is no 3D and no projection. Depth comes from overlap, scale and light.

Two concessions to rendering without a GPU:

- **Watercolour texture is baked.** p5.brush's watercolour fills cost over a second each on software GL, so the big textured grounds (the room, the stage inside the market) are painted once with real fills and reused as images ([src/plates.js](src/plates.js)).
- **Moving things use washes.** Anything that moves (characters, coins, UI) paints its shading as flat translucent washes (`PROJECT.fills = 'wash'`). This cut the character from 9.7 s to about 0.2 s a frame.

## Frame

- 1080×1920, 30 fps.
- **Stage:** key action lives in x 40–900, y 200–1110. The camera helper `cam(t, x, y, zoom)` centres on that stage, not on the frame.
- **Caption band:** y 1130–1250.
- **y 1250–1440:** secondary things only (the desk, feet, disclaimer tags).
- **Below 1440 and right of 918:** YouTube's UI, so nothing that matters goes there.

## Palette (hex)

The UI colours echo Limitless's own (from their CSS). Everything else is ours.

| role | colour |
|---|---|
| night ground | `#16181B` (plates graded to a mean of ~`#191C1F`) |
| screen panel / hi / bezel | `#22262B` / `#2D3238` / `#101214` |
| ink (outlines, never pure black) | `#1E1B22` |
| **Up** / light / dark | `#389A57` / `#62C482` / `#236B3B` (Limitless green.500) |
| **Down** / light / dark | `#ED5023` / `#F4865C` / `#A63A18` (Limitless red.500) |
| text cream / dim | `#F4EEDC` / `#A9A493` (never pure white) |
| the $1 coin | `#E7B447`, rim `#A9771F`, face `#F7DB8E` |
| Chainlink 60-second average | `#7F8FFF` |
| the fast exchange's price line | `#E9E3D0` |
| you (the trader) | periwinkle `#8E9FE0` / `#5F6DB0` |
| the stranger | orchid `#C98BC4` / `#8F558B` |
| caption highlight (only) | lime `#C3FF00` (Limitless brand neon) |

**Colour arc:** the film starts green-lit (Up rocketing), turns gold at the mint, and goes cool blue at the Chainlink twist. At the burn it drains to grey-ash, then snaps back to green for the loop.

## Light

- **Key light:** the screens themselves. Each throws an additive glow in its colour (the market in green, the ticker in warm cream). Buttons glow when their price moves.
- **Fill:** two soft pools baked into the room plate, green upper-left and violet lower-right.
- **Accents:** the gold coin glows at the mint, and the Chainlink average carries a blue halo.
- Nothing is lit flat: every scene has at least one glow source that breathes.

## Materials

- **Screens:** a thick bezel with an ink outline, a flat panel with faint scan lines, and 18px corners.
- **Buttons:** a raised wash with a darker drop edge, which lifts when pressed.
- **Coin:** a gold disc with a darker edge and an inner face. It splits into an **Up half** (green, left, ↑) and a **Down half** (red, right, ↓) along one torn seam, so the two halves always fit.
- **Order books:** depth bars only, with no row labels. Asks are dim and hollow, bids are solid. The only tag is the one price being spoken.
- **Characters:** the kit's character, recoloured so it never reads as Up or Down.
  - **You** are periwinkle with headphones.
  - **The stranger** is orchid with a beanie.

## Post

- Paper grain and a warm vignette are multiplied over the painted frame (the kit's).
- Glows are additive, under the grain.
- There's no bloom filter, no chromatic aberration and no fake depth of field. Softness comes from the plates.

## Type

- **Lilita One** (OFL, vendored in `fonts/`) for everything: captions and the painted numbers.
- Permanent Marker is loaded only because the kit's engine expects it.

## Captions

- 1–3 words, synced to the narration's word timestamps and drawn over the grain so they stay crisp.
- Lilita One at 86 px (cap height ≈ 3% of the frame, which matches Zack D. Films), cream with a 15 px ink stroke and a soft drop shadow.
- **One lime key word** per caption at most.
- Centred at x 540, y 1190 (62%), never wider than 820 px. Each pops in over 0.1 s with a slight overshoot.

## Disclaimers

Small cream-on-ink pills under the caption band (y 1330):

- "Not financial advice" at 58.9–61.2 s
- "Unofficial explainer · not affiliated with Limitless" from 62.9 s to the end

## Camera language

- It never parks: a slow drift (6 px, 0.1 Hz) under every move.
- **Push-ins** go *through* screens to enter the market world, and **pull-backs** come out of them.
- **Whip pans** land on beats and carry a painted smear.
- There are small shakes on impacts only: the stamp and the burn.

## Transition vocabulary

- **Push through a screen** into the world it shows, or pull back out of it.
- **Match on the coin:** the coin → a pie of odds → the two book headers, and the burned half → ash → the next round's price line.
- **Whip pan with smear**, on a beat.
- **Continuous camera move** across a beat change.
- **Smash cut**, reserved for the burn.
