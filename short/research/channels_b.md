# Reference channels B: Humphrey Yang + Coin Bureau (finance/crypto explainers)

Research date: 2026-09-25. Topic we're making: 15-minute crypto Up/Down prediction markets on Limitless Exchange, 45–60 s, painted 2D, TTS voice.
We studied these for style only. None of their footage, music or voice goes into the video.

## 0. Channel choice and what I could get

- **Whiteboard Crypto has only 2 Shorts** on `/@WhiteboardCrypto/shorts` (channel UCsYYksPHiGqXHPoHI-fm5sg): `AWaHYF_kKvc` "Crypto 'Reserve' vs 'Stockpile'" (2025-03-11, 10.9k views, 87 s) and `dt6NaDjLMeo` "Crypto Scam Revealed #1" (2022-01-11, 75k views, 55 s). That's too few to go on, so I used **Coin Bureau** (`/@CoinBureau/shorts`) instead, as instructed.
- **Humphrey Yang:** I listed 450 Shorts and sampled upload dates by position to find the 12-month cutoff (entry 156 is dated 2025-09-24). The 5 videos below are the most-viewed among entries 1–156. The McDonald's-dividend Short (2.18M views) was dated 2025-08-25, outside the window, so I dropped it.
- **Coin Bureau:** the Shorts tab lists 44 entries, from 2025-09-15 to 2026-09-24. The top 5 by views all fall between 15.5k and 17.9k. One of them (`7M2s98f_JBI`, 2025-09-18) is 12 months plus 1 week old.

### Download status (measured, not assumed)

| What | Result |
|---|---|
| Video/audio files (all 10) | **FAILED.** Default, `tv_simply`, `ios`, `android`, `android_vr`: "Sign in to confirm you're not a bot". `tv`: "The page needs to be reloaded". `web_safari`/`mweb`/`web_embedded`: only storyboard images offered, or with `formats=missing_pot` the googlevideo URLs return **HTTP 403**. Nightly yt-dlp 2026.09.16, `yt-dlp[default]`, curl_cffi, and a bgutil PO-token provider (tokens were generated) all still got 403 on googlevideo. `-f worst`, format 18, HLS 91–96 and audio-only 140/251 all got 403. |
| `youtube-transcript-api` | FAILED (`IpBlocked`). |
| Metadata (`info.json`) | OK via `player_client=mweb` / `web_safari` + `--ignore-no-formats-error`. |
| Transcripts | **OK:** YouTube auto-captions (`en-orig`, json3) with **word-level timestamps**, via yt-dlp `mweb` + bgutil PO token. These are ASR, so a few numbers are wrong; corrections noted inline. |
| Frames | **OK, but only at ~1 fps:** storyboard `sb0` (101×180 px, 3×3 sprites, one frame every 0.93–0.99 s). The requested 0.5 s sampling over the first 3 s wasn't possible. |
| Full-res stills | **OK:** `i.ytimg.com/vi/<id>/oar1/oar2/oar3.jpg` are 1080×1920 frames from within each video (they look like auto-picked frames around 25/50/75%). All caption measurements come from these. |

**Consequences:**
- **Nothing about audio was measured.** No loudness, music level or SFX figures exist in this report. The only audio clue is the ASR `[music]` tag (§4).
- **Cut counts are 1-fps lower bounds.** Two cuts less than about 1 s apart are merged.

Method: I split the sprites into frames and tiled them with timestamps (PIL). Then I **looked at every sheet** and hand-counted shot changes. I cross-checked those counts against an automatic colour-histogram difference (≥0.15) between consecutive storyboard frames.

---

## 1. Per-video table

WPS = ASR tokens ÷ (last word onset − first word onset + 0.3 s). ">>" speaker marks and `[music]` tags are excluded. A number like "$50,326" counts as one token, so spoken WPS is higher on number-heavy lines. Cuts/10 s: **manual** count from the 1-fps sheets (auto histogram count in brackets). The first-payoff time is the word-onset timestamp of the first surprising claim or number.

| Channel | ID | Title | Date | Dur | Views | WPS all / first 5 s / rest | Cuts/10 s manual (auto) | First payoff | Caption (words/caption, position) | Ending |
|---|---|---|---|---|---|---|---|---|---|---|
| Humphrey | 6nGGHe2HMaE | Selling My 10 Ounce Silver Bar | 2025-09-24 | 83 s | 20.2M | 3.15 / 5.0 / 3.02 | 1.8 (1.5) | Cold open at the counter at 0 s ("sell this silver bar"). First number "$150" at 8.2 s. Price board at ~19–21 s. | 2–3 words, 75 %; white for Humphrey, **yellow for the dealer** | Cuts off mid-sentence ("Nice to see you again as", 82.7 of 83 s). No CTA. |
| Humphrey | 7w6v3NKPzeI | Part 1: I went to a Gold Factory in Switzerland | 2025-11-05 | 56 s | 14.8M | 3.68 / 3.6 / 3.68 | 4.3 (3.2) | "worth about a **million** dollars" at 3.36 s. Bar in frame from 0.0 s. | 3–6 words, 80 % | Selfie-cam CTA: captions "If you want more…" and "you're subscribed" (read off the storyboard, approximate) and "content like this." (full-res still). Title says "Subscribe for Part 2!" |
| Humphrey | 6EDOgQdOQss | Explaining Netflix's 10:1 Stock Split Today | 2025-11-17 | 27 s | 2.85M | 3.35 / 2.8 / 3.48 | 2.6 (2.6) | "$1,100 to **$110**" at 2.48 s, then twist "It didn't actually crash" at 5.0 s | 4–6 words, 50 %; **yellow** on "$110" and "stock split" | Ends on the other character's punchline: "…but I'm only buying what I can afford." (26.6 of 27 s). No CTA. |
| Humphrey | 0LprsBrwXRo | How Long Should You Keep Your Car? | 2026-01-19 | 57 s | 2.26M | 3.85 / 4.0 / 3.83 | 1.9 (1.75) | Claim "we're brainwashed" at 3.9 s. First number "20%" at 13.9 s. | 3–4 words in a **green rounded box**, 50 % | Last line "Buy a car once, drive it into the ground, and that will save you the most" (ASR). Speech runs to 0.12 s before the end. No CTA. |
| Humphrey | nFVAmP96lYg | Pepsi is a Dividend King | 2025-11-15 | 50 s | 1.84M | 3.77 / 3.8 / 3.76 | 3.2 (4.4, includes graphic pop-ins) | "one of the **rarest stocks** in the world" at 2.0 s. "3.12%" at 11.4 s. | 3–5 words (up to 3 lines on b-roll), 44–66 %; **yellow** "rarest stocks", **green** "paid" / "of passive income." | Caveat line, then caption "Follow me if you liked this!" (read off the 101×180 storyboard, so approximate) |
| Coin Bureau | X51NGfet-dU | Is Altseason Imminent? | 2025-10-13 | 103 s | 17.9k | 3.31 / 2.6 / 3.34 | 3.0 (3.2) | Joke "piloted a light aircraft" at 9.0 s. First content "liquidity index" at 23 s. | **1 word**, 61 % | Ends on banter ("…need girls to play this game." / "Oh."). It's a livestream clip. |
| Coin Bureau | 3PUYfo7yyyc | How To Find Hidden Crypto Gems | 2025-10-02 | 117 s | 17.8k | 2.91 / 3.6 / 2.87 | 2.2 (2.3) | "100x crypto" at 28.8 s | **1 word**, 63 % | Ends on the last tip. No CTA. It's a cutdown of a long video. |
| Coin Bureau | 7M2s98f_JBI | Beginner Crypto Traders: Learn Candles & Wicks | 2025-09-18 | 84 s | 17.7k | 2.95 / 2.6 / 2.97 | 2.1 (2.0) | "chances are other cryptos will be too" at 6.8 s | 2–4 words, 72 %, **blue box on the active word** | Ends on the last if/then rule. No CTA. |
| Coin Bureau | klwBCmu_pFk | STOP Chasing 12,000% Yields! | 2025-10-08 | 105 s | 17.5k | 3.01 / 3.0 / 3.00 | 2.6 (2.7) | "meaningless" at 1.8 s. "12,000% APY" at 27.4 s. | **1 word**, 60 % | Ends mid-quote ("…vulnerable to attack or bugs."). No CTA. It's a cutdown. |
| Coin Bureau | 4pbCucoVh6Q | Will Trump's $1B crypto stake destroy the CLARITY Act? | 2026-09-12 | 48 s | 15.6k | 2.72 / 2.0 / 2.81 | 2.6 (1.9) | "billion-dollar" at 1.04 s (inside the question hook) | Headline card (2–5 words, 63 %) plus running caption (5–8 words, 72–74 %) | Question plus CTA: "So, should politicians hold crypto while making the laws? Let me know your thoughts in the comments." |

Other measured numbers:

| ID | Words | Sentences | Mean / median words per sentence | "you/your" per 100 words | Questions | Numeric tokens | Gaps > 0.8 s between words | Last word to video end |
|---|---|---|---|---|---|---|---|---|
| 6nGGHe2HMaE | 261 | 39 | 7.3 / 7 | 4.2 | 6 | 28 | 12 | 0.28 s |
| 7w6v3NKPzeI | 196 | 12 | 16.3 / 12.5 | 1.5 ("you guys") | 1 | 3 | 1 | 2.9 s (the selfie CTA is not in the ASR) |
| 6EDOgQdOQss | 90 | 10 | 9.3 / 7.5 | 0 (first-person skit) | 1 | 9 | 4 | 0.44 s |
| 0LprsBrwXRo | 220 | 16 | 13.8 / 15 | **8.6** | 1 | 15 | 5 | 0.12 s |
| nFVAmP96lYg | 187 | 14 | 13.4 / 11.5 | 5.3 | 1 | 3 | 2 | 0.56 s |
| X51NGfet-dU | 338 | 33 | 10.8 / 7 | 2.4 | 8 | 2 | 9 | 1.08 s |
| 3PUYfo7yyyc | 339 | 19 | 17.8 / 18 | 3.5 | 0 | 5 | 8 | 0.60 s |
| 7M2s98f_JBI | 246 | 15 | 16.4 / 15 | 1.6 | 0 | 0 | 2 | 0.96 s |
| klwBCmu_pFk | 314 | 16 | **19.6** / 19 | 6.4 | 1 | 2 | 7 | 0.76 s |
| 4pbCucoVh6Q | 128 | 9 | 14.2 / 17 | 0.8 | 2 | 0 | 9 | 1.32 s |

---

## 2. Hook lines (verbatim, from ASR) and first frames

| ID | First sentence | First frame (0.0 s) and first ~2 s |
|---|---|---|
| 6nGGHe2HMaE | "Hey, how you doing?" then "I was wondering if I could sell this silver bar to you today." | Handheld point-of-view at a coin-shop counter, dealer in the background. Yellow caption "Hey, how you doing?" at 75 %. By 1 s the silver bar is in the foreground hand. |
| 7w6v3NKPzeI | "This 12.5 kilo gold bar is worth about a million dollars." (ASR: "12 1.5"; on-screen caption says 12.5) | Extreme close-up of a gold bar with "999.607" written on it, in white-gloved hands. The caption lands by 1 s. |
| 6EDOgQdOQss | "Dude, Netflix stock just went from $1,100 to $110 per share." then "It crashed 90%." | Humphrey (outfit A, black overshirt) mid-shot in his kitchen, mid-word, caption "Dude," at 50 %. At 0.9 s a white price-chart screenshot card pops in over his torso. |
| 0LprsBrwXRo | "How long should you keep your car before getting a new one?" | Wide shot of Humphrey in a parking lot next to a car. At 1.0 s a big yellow all-caps title "HOW LONG SHOULD YOU KEEP YOUR CAR?" sits in the top 10–25 % for ~2 s. |
| nFVAmP96lYg | "Did you know that Pepsi is one of the rarest stocks in the world?" | Talking-head close-up, caption "Did you know that" at 52 %. Cut at ~1 s to a Pepsi-can macro, with "rarest stocks" in yellow. |
| X51NGfet-dU | "Welcome one and all." | **Black frame**, then the studio host at 1 s |
| 3PUYfo7yyyc | "Now, once you've got a list of a few promising looking cryptos, then take note of four things." | **White blur-flash transition**, then stock footage of hands on a phone at 1 s |
| 7M2s98f_JBI | "BTC needs to be trending higher for other cryptos to rally." | **Blurred transition frame** with the caption "BTC NEEDS TO BE" already on it. Presenter at 1 s. |
| klwBCmu_pFk | "The APR you get is meaningless if the crypto is looking bearish on a high time frame." | **Motion-blur whoosh frame**, then presenter at 1 s |
| 4pbCucoVh6Q | "Will Trump's billion-dollar crypto stake destroy the Clarity Act?" | **Blur-flash frame**. Presenter at 1 s. Headline card "TRUMP'S $1B STAKE vs THE CLARITY ACT" wipes in at 1–2 s. |

Observed: Humphrey is on content at 0.0 s in 5 of 5 videos. Coin Bureau starts on a transition (blur, flash or black) in 5 of 5 and reaches content at ~1 s.

---

## 3. Per-channel summary

### Humphrey Yang (5 videos, 1.8M–20.2M views, 27–83 s, mean 54.6 s)

- **Format:** the top two by views are object-plus-price mini-vlogs (a silver bar sold at a coin shop, a million-dollar gold bar at a refinery). The other three explain one money mechanism: a self-dialogue skit (two outfits = two characters), a walk-and-talk with a table, and a b-roll voice-over.
- **Pace:** 3.15–3.85 WPS, **mean 3.56**. The three single-narrator explainers run 3.68–3.85, flat from the first 5 s to the end. The silver-bar cold open is dialogue at 5.0 WPS.
- **First payoff:** a number or bold claim in the **first 2.0–3.9 s** in 4 of 5 (Pepsi 2.0 s, Netflix 2.48 s, gold 3.36 s, car 3.9 s). The silver bar puts the object on screen at ~1 s and says the first number at 8.2 s.
- **Cuts:** 1.8–4.3 per 10 s (1-fps lower bound), **mean 2.8**. Between cuts there are frequent graphic pop-ins: price-chart screenshot (Netflix 0.9 s), "🍕 = $110" black pill (Netflix ~20 s), "$50,326" blue price tag (car 32 s), a "Cost Per Year" table that gains one row per spoken number (car 38–50 s), a "3.12% Dividend Yield" badge (Pepsi 14 s). In the car video he walks toward the camera for the entire take, so the frame never sits still.
- **Captions** (measured on 1080×1920 stills):
  - White bold sans in sentence case with punctuation, soft dark drop shadow, no outline.
  - Cap height **36–42 px = 1.9–2.2 % of frame height**, so they're small. Usually one line, 2–6 words; up to 3 lines over b-roll.
  - Vertical centre varies by video: 50 % (Netflix, car), 52 % (Pepsi), 75 % (silver), 80 % (gold).
  - Highlight: **yellow** on the key number or term ("$110", "stock split", "rarest stocks") and **green** on money words ("paid", "of passive income.").
  - Colour also marks speaker: a second speaker is captioned in yellow (silver dealer).
  - The car video puts every caption in a **green rounded box** (box 83 px = 4.3 % tall).
- **Endings:** no outro card in 3 of 5. The voice runs to within **0.12–0.56 s** of the end in 4 of 5, and two stop mid-sentence (silver, car per ASR). CTAs appear only in Pepsi ("Follow me if you liked this!") and the gold Part 1 (subscribe).

### Coin Bureau (5 videos, 15.6k–17.9k views, 48–117 s, mean 91 s)

- **Format:** mostly **cutdowns** of long videos and livestreams (descriptions say "Full Video: …" / "Tune in: …live"). A studio presenter at a desk is intercut with stock footage, website/chart screenshots and simple diagrams (candle anatomy). Only `4pbCucoVh6Q` is a purpose-written Short, with a question hook and a CTA.
- **Pace:** 2.72–3.31 WPS, **mean 2.98**, slower than Humphrey. First-5-s WPS is 2.0–3.6 (mean 2.76); there is no speed-up at the top.
- **First payoff:** only the purpose-written Short and the yields cutdown land a claim in under 2 s ("billion-dollar" 1.04 s, "meaningless" 1.8 s). The cutdowns take 6.8–28.8 s to reach their payoff because they start mid-argument ("Now, once you've got a list…").
- **Cuts:** 2.1–3.0 per 10 s, **mean 2.5**. Many are **punch-ins**: the same presenter shot re-cropped wide/tight every 2–4 s (clear in the candles and gems sheets). Screenshots hold for 5–10 s while one-word captions keep changing.
- **Captions:** three systems, one per video type.
  1. **One word at a time**: heavy comic italic caps, white fill with grey lower gradient, thick black outline plus shadow. **~94–100 px tall = 4.9–5.2 % of frame height**, centred at **60–63 %** (gems, yields, live).
  2. 2–4 words, heavy geometric all-caps sans, white with shadow, cap ≈52 px (2.7 %), centred at 72 %. The **active word sits on a blue rounded box** (karaoke style) (candles).
  3. Two layers (clarity): a **headline card** of 2–5 words in heavy italic caps, white line plus **yellow** line, cap ≈42 px (2.2 %), at ~63 %; under it a **running caption** of 5–8 words in cream regular-weight caps, cap ≈33 px (1.7 %), at 72–74 %.
- **Endings:** the purpose-written Short ends on a question plus "Let me know your thoughts in the comments" (the on-screen headline repeats the question). The cutdowns simply stop, one of them mid-quote.
- **Caveat:** at ~16k views against Humphrey's millions, Coin Bureau Shorts are evidence of how a crypto channel *explains* things, not of what *performs*.

---

## 4. Music and SFX (NOT measured)

- No audio could be downloaded, so there are **no ebur128, astats or volumedetect figures** for either channel.
- **Only indirect evidence:** YouTube's ASR inserted `[music]` tags mid-speech.
  - `klwBCmu_pFk`: 9 tags spread from 21.6 s to 96.9 s. Music is flagged under the voice throughout.
  - `nFVAmP96lYg`: at 36.0 s and 41.9 s.
  - `7w6v3NKPzeI`: at 45.9 s.
  - The other 7 have no tags. That does **not** prove silence, because ASR only tags music it notices.
- **SFX on cuts:** unknown. The whoosh/flash transition frames at 0.0 s on all 5 Coin Bureau videos *suggest* (inferred, not heard) a transition sound at the top.

---

## 5. Phrasing patterns (quotes are verbatim ASR; bracketed numbers are corrected from the on-screen graphics)

**Sentence length.** Humphrey's single-narrator explainers average 13–16 words per sentence; his dialogue videos average 7–9. Coin Bureau averages 14–20 (klwBCmu_pFk 19.6).

**Second person.** Humphrey's car video: 8.6 "you/your" per 100 words, e.g. "Look at how much you save if you hold on to a car for more than 5 years." Pepsi: 5.3 per 100, e.g. "For every share of Pepsi that you own, you get paid 3.12%." Coin Bureau is lower (0.8–6.4) and often hedged: "you want to make sure…", "chances are you'll be buying their bags."

**Questions.**
- As the hook: "How long should you keep your car before getting a new one?", "Did you know that Pepsi is one of the rarest stocks in the world?", "Will Trump's billion-dollar crypto stake destroy the Clarity Act?"
- Asked by a character: "What's a stock split?" (Netflix skit).
- As a rhetorical jab: "Do you want to earn a yield on something that's tanking?"

**How a number is explained.**
- *Shock, then correction:* "Netflix stock just went from $1,100 to $110 per share. It crashed 90%. It didn't actually crash. Netflix is just doing a 10-to-1 stock split." The twist lands at 5.0 s.
- *Everyday analogy with a stated price:* "Imagine a share of Netflix is a huge pizza, and that pizza costs $1,100." Then "they'll slice the pizza into 10 different slices, each slice costing $110." The equation stays on screen as a "🍕 = $110" card.
- *Same number, re-divided:* "You're paying $50,326 to use the car for one year. But if you own the car for 3 years, your cost per year is $16,775. At 5 years, it's [$10,065]. And if you can drive the car for 10 years, your cost per year is [$5,033]." A table gains one row per sentence.
- *Number first, term second:* "you get paid 3.12%. This is known as the dividend yield…" and "A dividend king is a company that has had 50 years or more of consecutive dividend increases."
- *Checking the maths in dialogue:* "So, if a spot is $43.92, you're paying $42.92?" / "correct?" / "And so, that's just your spread for doing business."
- *Rule-of-thumb bands (Coin Bureau):* "as a rule of thumb, a market cap of under $100 million is a small market cap. 100 million to 1 billion is a midsize market cap and $1 billion plus is a large market cap."
- *An absurd number as the warning:* "if something is paying 12,000% APY, it's safe to say that nobody wants it and it's not worth your time."

**How a mechanism is explained (Coin Bureau candles).** Name the part, say what it shows, then give if/then rules:
- "The wick at the top of the candle shows you the highest price that was hit that day"
- "a large wick on the top of a candle means lots of people are selling, while a large wick at the bottom of a candle means lots of people are buying."
- "If the candles are green but getting smaller, then that means prices could start falling."

**Risk and disclaimers.** Both channels keep them short and concrete. Neither says "not financial advice" in these 10 transcripts.
- Humphrey (Pepsi): "Now, dividend yields do change from year to year, and you do have to pay taxes on your dividends, but that's for another video." He also hedges inline: "more or less guarantees you a true form of passive income."
- Coin Bureau:
  - "A smaller market cap means bigger potential gains but also higher risks. So if you're a conservative investor, then stick to the larger cap cryptos you found."
  - Hedge words in the transcripts: "chances are", "typically", "probably", "could", "suggest", "it's safe to say".
  - Both sides in one line each: "Critics argue…" / "On the flip side, supporters say…".

**Lines our rule 11 forbids (seen here, do not copy):** "But here's what nobody tells you." (car, 22 s) and the tidy-moral ending "The lesson here is simple. Buy a car once, drive it into the ground…" (car, 52 s).

---

## 6. Patterns worth copying (each tied to an observation)

1. **Say a concrete number by ~2.5 s.** Humphrey's explainers hit theirs at 2.0–3.4 s ("$110" 2.48 s, "million dollars" 3.36 s), and Coin Bureau's only purpose-written Short says "billion-dollar" at 1.04 s. The cutdowns that start mid-argument take 7–29 s to reach any payoff. *For us:* the first line should name the price and the 15 minutes.
2. **Shock, then correction, inside 5 s.** "It crashed 90%. It didn't actually crash." (3.9–5.8 s) makes the misunderstanding the hook. *For us:* a line like "You're betting on Bitcoin in the next 15 minutes" followed by the plain correction of what's actually happening.
3. **One everyday analogy, pinned as an equation card.** The pizza carries the whole split mechanism, and "🍕 = $110" stays on screen while he talks. *For us:* one painted object for the YES/NO share, with a "= $0.62" style card.
4. **Grow a number table in sync with the voice.** The car video adds one row per spoken duration from 38 to 50 s. The eye has something new every ~3 s with no cut. *For us:* a price ladder or share-price table that fills in as the voice says each value.
5. **Voice at ~3.6–3.8 WPS, flat from start to end.** Humphrey's single-narrator explainers measured 3.68–3.85, with the same rate in the first 5 s. Coin Bureau is slower (mean 2.98) and gets far fewer views. At 3.7 WPS, 50 s of speech is about 185 words.
6. **A visual change every ~3–4 s.** Both channels average 2.5–2.8 cuts per 10 s (lower bound), with graphic pop-ins or camera moves between cuts. Nothing holds still longer than one sentence.
7. **Pick one caption system and use it all the way through.** Humphrey: 2–6 words, sentence case, one line, white with shadow, one highlight colour on the key number (yellow) and green for money words. Coin Bureau's one-word comic caps are ~2.5× larger (4.9–5.2 % vs 1.9–2.2 % cap height). All measured caption centres sit between **44 % and 80 %** of frame height, and none sit in the bottom 20 %. *For us:* keep captions around 60–72 % and keep the painted focal object above them.
8. **Start on content at frame 0.** Humphrey: 5 of 5 open on content. Coin Bureau: 5 of 5 open on a blur, flash or black frame and show content at ~1 s. This is a correlation with views, not proof of cause.
9. **One short, factual risk sentence near the end.** Example: "dividend yields do change from year to year, and you do have to pay taxes… but that's for another video." *For us:* one line on how you can lose your stake if the price closes the other way, then move on.
10. **Don't wind down at the end.** The voice runs to within 0.12–0.56 s of the end in 4 of 5 Humphrey Shorts, with no outro. When there is a CTA, it's a single question ("should politicians hold crypto…? Let me know your thoughts in the comments"). *For us:* end on the last mechanism beat or a one-line question, not a tidy moral (rule 11).

---

## 7. Files

- Scratch (videos, JSON, transcripts, all frames): `/tmp/claude-0/-home-user-ClaudeAnimationBase/b9e37835-d4c1-5268-ba1c-9734d2deae34/scratchpad/yt_b/v/<id>/` (`words.json` = word timestamps, `transcript.txt`, `frames/`).
- Contact sheets in `short/research/sheets_b/`, three per video, all ≤ 245 KB:
  - `<channel>_<slug>_a_first10s.jpg`: first 10 storyboard frames (~0–9 s) at 3×, with timestamps.
  - `<channel>_<slug>_b_all_1fps.jpg`: every storyboard frame (~1 fps), labelled in seconds.
  - `<channel>_<slug>_c_fullres_frames.jpg`: the three 1080×1920 stills, with 10 % height gridlines.
  - `caption_crops_0.jpg` / `caption_crops_1.jpg`: full-res caption crops with a pixel ruler (absolute y in a 1920-px frame), used for the size and position figures.
