# Research: how the reference Shorts are made

Researched on 2026-09-25 by two subagents with yt-dlp, across four channels and 21 Shorts. The full per-video tables, quotes and contact sheets are in:

- [research/channels_a.md](research/channels_a.md) for Zack D. Films and Kurzgesagt (sheets in `research/sheets_a/`)
- [research/channels_b.md](research/channels_b.md) for Humphrey Yang and Coin Bureau (sheets in `research/sheets_b/`)

Whiteboard Crypto has only two Shorts, so Coin Bureau replaced it.

## What we could and couldn't get

**Blocked.** YouTube refused every video and audio download for all 21 Shorts: either a "Sign in to confirm you're not a bot" check, or HTTP 403 on the media URLs even with a PO token. As a result:

- Nothing about audio was measured: no loudness, no music level under the voice, no SFX timing.
- The only audio evidence is YouTube's `[music]` caption tags, so audio rules below come from the guide, not from the references.

**Got.**

- Metadata for every video.
- Word-timed auto-captions for 20 of 21 (Kurzgesagt `2cK8l5Yg5w8` has no caption track).
- Storyboard frames at about 1 fps. That's coarser than the 0.5 s / 2 s schedule we asked for, so cut counts are lower bounds.
- Three full-resolution 1080×1920 frames per video.

We looked at every sheet.

## Measurements (pooled per channel)

| | Zack D. Films | Kurzgesagt | Humphrey Yang | Coin Bureau |
|---|---|---|---|---|
| Medium | 3D CG | flat vector | talking head + pop-in graphics | talking head / clips |
| Views of the Shorts analysed | 79–91M | 3.4–5.2M | 1.8–20M | ~16k |
| Words per second | 2.93 (2.72–3.14) | 2.96 (2.67–3.13) | 3.56 (3.68–3.85 in narrated explainers) | 2.98 |
| First concrete payoff | 3.9–9.4 s | 2–6 s | 2.0–3.4 s (a hard number) | 1–29 s |
| Cuts per 10 s (by eye, lower bound) | 5–8 | 2.4–3.8, plus an inset or HUD change every 1–2 s | 2.5–2.8, plus graphic pop-ins | 2.5–2.8 |
| First frame | mid-action, no text (5/5) | title card (5/5) | content at frame 0 (5/5) | blur, flash or black (5/5) |
| Captions | white, heavy, 2–3 words, ~3.0% cap height, centred ~78% down | white, medium, 2–3 words, ~2.0%, ~78% down | 2–6 words, sentence case, white + shadow, yellow highlight on numbers, ~2% | 1 word, outlined comic caps, ~5% |
| Ending | no CTA, cut 0.5–1.4 s after the last word | no CTA; K1 and K6 loop back to frame 0 | voice runs to within 0.1–0.6 s of the end (4/5) | CTA question |

## Phrasing patterns (from transcripts)

- Hooks are short and flat, 4–7 words (Kurzgesagt), or a number plus a correction: "It crashed 90%. It didn't actually crash." (Humphrey, 3.9–5.8 s).
- Sentences average 12–18 words. Kurzgesagt uses "you" in under 1–8% of words, and Humphrey addresses the viewer directly.
- A number is always paired with an object. Humphrey pins "🍕 = $110" while he talks, and Kurzgesagt puts "29 cents" on a coin.
- Kurzgesagt leaves ≥ 0.9 s of air after a key term or statistic, 3–5 times per video.
- Risk gets one short factual sentence near the end (Humphrey, Coin Bureau), never a lecture.

## Rules we'll follow (each tied to an observation)

1. **Voice at ~3.6 words per second.** The topic is dense, like Humphrey's money explainers (3.68–3.85 WPS, 1.8–20M views), not a Zack story (2.9). That gives ~210 words for ~60 s.
2. **A hard number by 2.5 s.** Humphrey's explainers land one at 2.0–3.4 s. Our first line says "fifty cents to eighty" by ~2.5 s, while the Up price is visibly climbing.
3. **Frame 0 mid-action, voice at 0.0 s.** Zack is 5/5 mid-action and the Humphrey Shorts analysed are 5/5 on content, with voices starting at 0.00–0.40 s. There's no title card. Kurzgesagt's title cards are the pattern we don't copy (rule 4).
4. **A change on screen every 1.5–3 s.** Zack cuts every ~1.5 s. Kurzgesagt holds ~3 s but brings in an inset or HUD change every 1–2 s. For a painted film we take Kurzgesagt's model: fewer cuts, and constant arrivals inside each shot.
5. **Numbers are objects, timed to the word.** 62¢ lives on a price tag, $1 is a coin that splits into Up and Down, and the order book is a HUD-style ladder that fills as the voice speaks. This follows Humphrey's "🍕 = $110" and Kurzgesagt's "29 cents" coin and budget bars.
6. **One recurring object carries the thread.** Kurzgesagt's snake returns at 3, 9, 35 and 60 s. Ours is the $1 coin that splits into an Up half and a Down half: it appears in the basics, the mint, the fee bite, the resolution and the loop.
7. **Air after the big terms.** Kurzgesagt leaves 0.9 s after key statistics. We leave 0.3–0.6 s after "fills you both", "three percent" and "barely moves it" (guide rule 2).
8. **Captions: white, heavy, 1–3 words, one lime highlight.** This follows Zack (3% cap height, heavy) and Humphrey's single highlight colour on the key number. Both reference channels centre captions at ~78% of frame height, inside the bottom-25% band our guide forbids. Ours centre at ~66%.
9. **One short risk sentence, then keep moving.** Humphrey and Coin Bureau each give risk a single factual line. Ours: "you can lose your whole stake", plus the on-screen "Not financial advice" tag.
10. **End on the mechanism and loop to frame 0, with no CTA.** None of the 10 Zack and Kurzgesagt Shorts has a CTA, and two Kurzgesagt ones loop back to their first frame. Our last line ("the close becomes the next round's Price to Beat") hands straight into the hook frame.
11. **Disclaimers as small pills, below the top 10%.** Kurzgesagt shows grant and caveat notes as tiny pills near the top. "Not financial advice" and "unofficial explainer" use the same treatment.
