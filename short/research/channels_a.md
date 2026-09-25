# Reference channels A: Zack D. Films and Kurzgesagt (Shorts)

Researched 2026-09-25 for the 15-minute Up/Down Limitless explainer. The references are for learning style only. None of their footage, music or voice will be used.

## 1. What I could and couldn't get

**Video and audio downloads were blocked for all 11 videos.** Everything below comes from metadata, YouTube's word-timed auto-captions, storyboard sprites and full-resolution thumbnail frames. I measured nothing from the video files or the soundtracks themselves.

| Asset | Result | How |
|---|---|---|
| Channel Shorts lists (views) | OK | `yt-dlp --flat-playlist` on `/shorts` (2,200 Zack items, 138 Kurzgesagt items) |
| Per-video metadata (upload date, duration, likes) | OK | `player_client=web_safari`, `--ignore-no-formats-error` |
| Video/audio files (all 11) | **Blocked** | default, tv, tv_simply, tv_embedded, ios, android, android_vr, web_creator: "Sign in to confirm you're not a bot" (or "page needs to be reloaded" / "Please sign in"). web_safari: "Only images are available". mweb and web_embedded with node JS runtime, nightly yt-dlp 2026.09.16 and a bgutil PO-token server got format URLs, but every googlevideo.com request returned **HTTP 403** (URLs are IP-bound to an IPv6 address that differs from our rotating IPv4 egress). `-f worst` made no difference. |
| Transcripts with word timestamps | OK for 10 of 11 | `player_client=mweb;fetch_pot=always` + bgutil PO token, `--write-auto-subs --sub-format json3` (ASR `en-orig`, word offsets). `youtube-transcript-api` returned IpBlocked. |
| Transcript for Kurzgesagt `2cK8l5Yg5w8` | **None exists** | yt-dlp reports "has no subtitles" for this video on two clients, so I analysed it from visuals only. |
| Frames | Partial | Storyboard `sb0` sprites: 101x180 px, **one frame per ~1.0 s** (not the requested 0.5 s / 2 s schedule). I checked the 1.0 s spacing against ASR word times: burned-in captions line up with the spoken words within about 0.5 s in 12 spot checks. I also have full-res frames: `frame0.jpg` (268x480, the first frame) and `oar1/2/3.jpg` (1080x1920, three frames YouTube picks; their times are not known exactly). |

Per-frame timestamps are ±0.5 s. A cut shorter than 1 s is invisible in the storyboards, so all cut counts are **lower bounds**. I couldn't listen to anything. The only audio evidence is indirect (see section 5).

## 2. Videos analysed

For each channel I ranked Shorts uploaded between 2025-09-25 and 2026-09-25 by view count.

| # | Channel | ID | Title | Uploaded | Dur (s) | Views | Likes |
|---|---|---|---|---|---|---|---|
| Z1 | Zack D. Films | iFCaw7dfyaI | The Boy With The Empty Pot | 2025-10-03 | 61 | 90.6M | 3.51M |
| Z2 | Zack D. Films | 7OvwC_oF8jE | Can You Outrun Night Forever? | 2025-10-19 | 46 | 81.9M | 2.54M |
| Z3 | Zack D. Films | dNoKZ7-Td3U | Why You Always See A Trash Can At Disney | 2025-12-18 | 30 | 81.0M | 2.25M |
| Z4 | Zack D. Films | mVdSNzuhGCE | He Survived Three Gunshots | 2025-10-02 | 24 | 79.1M | 1.71M |
| Z5 | Zack D. Films | CJT21lc0Mkw | The Best Way To Cut A Watermelon | 2025-10-17 | 29 | 79.3M | 1.85M |
| K1 | Kurzgesagt | UC5Mpc-GQCg | The Moon's Invisible Threat | 2025-12-18 | 84 | 5.22M | 218k |
| K2 | Kurzgesagt | 2cK8l5Yg5w8 | The Deadliest Thing in Your Kitchen | 2026-07-23 | 67 | 4.58M | 178k |
| K3 | Kurzgesagt | KTu2V65Iiho | Why Does Cocaine Feel So Good? | 2026-02-19 | 72 | 4.20M | 258k |
| K4 | Kurzgesagt | tZ8i1RxGSYM | Can Earth Run Out of Water? | 2026-08-31 | 78 | 3.60M | 181k |
| K5 | Kurzgesagt | hDU9WcmQA2E | Let's Cook a Planet! | 2026-01-12 | 71 | 3.46M | 173k |
| K6 | Kurzgesagt | VYhUa3WC4nU | Why Being Poor Is Expensive | 2026-04-16 | 72 | 3.41M | 197k |

K2 is #2 by views but has no caption track, so I added K6 (#6) to get five Kurzgesagt transcripts. K2 is used for visuals only.

**Medium note:** all five Zack videos are **3D CG** (lit, textured characters and sets), not 2D. Zack is our benchmark for format and pacing, not for look. Kurzgesagt's flat vector illustration is the closer match to our medium.

## 3. Per-video measurements

WPS = words per second, from the ASR word start times (first word to last word + 0.4 s). Sentence lengths use YouTube's auto-punctuation, so treat them as approximate. For cuts I counted visible shot changes by eye on the 1 s storyboards and give them per 10 s. The `ffmpeg select='gt(scene,0.3)'` count ran on the same storyboard frames, with the caption band masked.

| # | Words | WPS all | WPS first 5 s | WPS rest | Pauses ≥0.9 s | Sent. mean / median (words) | "you" words | Questions | Cuts/10 s (eye, lower bound) | ffmpeg scene>0.3 per 10 s | First payoff |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Z1 | 163 | 2.72 | 3.00 | 2.69 | 0 | 12.5 / 14 | 1.2% | 0 | ~6.6 (≈40 in 61 s) | 1.1 | 6.1 s stakes ("the king was old… heir"); first reveal 21.5 s "nothing ever grew"; twist 45.0 s "boiled" |
| Z2 | 141 | 3.14 | 3.40 | 3.10 | 1 | 17.6 / 18 | 5.7% | 1 | 5.2–5.9 (24–27 in 46 s) | 1.3 | 9.4 s "faster than the Earth spins" (W/E arrows on screen from ~8 s); twist 31.0 s "the sun doesn't set" |
| Z3 | 85 | 2.92 | 3.20 | 2.86 | 0 | 21.2 / 20 | 3.5% | 0 | 6.7–7.0 (20–21 in 30 s) | 1.6 | 4.4 s Walt tosses the wrapper (shown ~5–6 s); answer 12.2 s "about 30 steps" with a hand-written "30" on a notepad at ~12 s |
| Z4 | 66 | 2.88 | 3.40 | 2.74 | 0 | 16.5 / 21 | 0% | 0 | 5.4–5.8 (13–14 in 24 s) | 1.2 | 3.9–5.9 s "each bullet headed towards a different part of his uniform" (orange tracer lines from ~3 s) |
| Z5 | 88 | 3.08 | 3.20 | 3.06 | 0 | 17.6 / 16 | 8.0% | 0 | 6.9–8.6 (20–25 in 29 s) | 1.0 | problem shown from 0 s; fix 13.0 s "Instead, cut… on the short side"; grid reveal ~19–22 s |
| K1 | 263 | 3.13 | 3.40 | 3.12 | 1 | 14.6 / 15 | 0% | 0 | ~2.4 (≈20 in 85 s) | 1.0 | 1.4 s "silent killer" (title card); 5.0 s "millions of dust particles" with dust blasting off the Moon at ~5 s |
| K2 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | ~3.8 (≈26 in 69 s) | 3.0 | visual only: a "suspect" (banana, spice bowl, sugar) gets a yellow tape label every ~2 s from 1 s |
| K3 | 218 | 3.06 | 3.20 | 3.05 | 3 | 12.8 / 13 | 8.3% | 1 | ~2.6 (≈18–19 in 72 s) | 1.6 | 2.6 s "Let's try it so you don't have to" (she snorts at ~3 s); first fact 16.0 s "within seconds" |
| K4 | 207 | 2.67 | 2.80 | 2.66 | 5 | 14.8 / 14 | 0.5% | 0 | ~3.3 (≈26 in 79 s) | 2.5 | 3.8 s "40% more fresh water than Earth can supply" (the pond turns red at ~5 s) |
| K5 | 215 | 3.07 | 2.80 | 3.10 | 3 | 12.6 / 13 | 3.3% | 0 | ~3.1 (≈22 in 72 s) | 1.4 | 3.8 s "swirl huge amounts of dust" (a "Dust Crispies" bag pours into the pot at ~3–4 s) |
| K6 | 204 | 2.84 | 2.60 | 2.86 | 3 | 13.6 / 14 | 4.9% | 0 | ~3.2 (≈23 in 73 s) | 2.3 | 2.1 s "Here's how the trap works" (spiral trap ~3 s); 5.8 s "one setback can snowball" (smashed piggy bank ~5 s) |

The ffmpeg scene detector misses most of Zack's cuts because consecutive shots from the same set look alike at 101x180. My counts by eye are the numbers to use. Neither is a true cut rate, because 1 fps sampling hides fast cuts.

**First payoff** is the first moment the viewer gets a concrete, surprising answer or reveal tied to the hook. I took the voice time from ASR and the visual time from the storyboards (±0.5 s).

## 4. Hook lines, first frames and endings (verbatim ASR, auto-punctuated)

| # | Hook line (first sentence) | First frame (t=0), as seen | Last line | How it ends (seen) |
|---|---|---|---|---|
| Z1 | "The king gave each boy a seed and told them to grow the best plant they could." | Mid-action: the king's hand drops seeds into a boy's cupped hands, a queue of boys, red palace doors. No text. | "But Ping was honest and the king knew that honesty was more important than results." | The last shot (boy with his empty pot, the king's hand on his shoulder) is held from ~55 s to the end. A moral. No loop, no CTA. |
| Z2 | "If you're afraid of the dark, could you hop in a plane and chase the sunset, avoiding nighttime forever?" | Mid-action: a man climbing airplane stairs at sunset. No text. | "…just hop on a flight to the South Pole, where the sun is just rising for another 6 months." | Plane on the polar runway with a rising sun (the sunset opening flipped to sunrise). No loop, no CTA. |
| Z3 | "Walt Disney took a bite of the hot dog, counted his steps, then tossed the [wrapper] on the ground, according to the legend, and he watched other guests do the same." | Walt in a suit mid-gesture holding a hot dog, castle and Mickey balloons behind. No text. | "So now, when you walk through a Disney theme park, you'll find a trash can exactly when you need it." | A modern guest drops trash into a can. No loop, no CTA. |
| Z4 | "He was shot three times after a fight broke out in a bar, but each bullet headed towards a different part of his uniform." | Mid-action: a man lunges at a police officer in a blue-lit bar. No text. | "He walked away with only minor injuries." | Close-up of the officer touching his face. No CTA. |
| Z5 | "When you slice a watermelon in half and in half again, then cut it into wedges, the sticky juices cover your face as you eat." | Mid-action: a knife already in the watermelon on a blue table. No text. | "When you pull out a piece, most of them will be the perfect size to fit in your mouth." | The last shot is the man eating a perfect cube, from ~24 s. No loop, no CTA. |
| K1 | "Our moon has a silent killer." | Title card: "Silent Killer On The Moon!" ("Killer" in pink) over a dark silhouette with red eyes in purple clouds. Held about 0–2 s. | "Every landing stirs up clouds of dust that floats, clings, and cuts." | **Loops:** the astronaut in dust clouds dissolves into the frame-0 title card at ~84 s. |
| K2 | n/a (no transcript) | Title card: "Something in Your Kitchen Killed You!" on yellow crime-tape over a slumped victim at a kitchen table. | n/a | Cuts back to the victim image (~63 s), then "Case closed!" with a banana behind bars. |
| K3 | "Why does cocaine feel so good? Let's try it so you don't have to." | Title card: "WHY DOES COCAINE FEEL SO GOOD?" (cyan glow) over a wide-eyed girl. Held about 0–2 s. | "…so you should know what it's doing to you." | The channel's bird mascot in glasses. No loop. |
| K4 | "We're running out of water." | Title card: "We Are Running Out of Water!" over an Earth with a tap. A tiny sponsor note sits at the top. | "…but for the price of a coffee a week, we can still protect what's left." | Returns to the first scene's pond (sun and clouds now in sunglasses), a kid holding a coffee with a "$2.03" tag. |
| K5 | "Let's cook an Earthlike planet from scratch." | Title card: "How To Cook a Planet" over a chef character at a cooking pot. | "…you might end up with rainstorms of molten glass and ice clouds." | Failed-recipe planets. No loop. |
| K6 | "Being poor is expensive. Here's how the trap works." | Title card: "Being Poor Is Expensive" over a man holding a wallet, with price tags floating round him. | "Breaking the cycle requires government intervention from universal health care and housing security to access to affordable credit." | **Loops:** at 72–73 s it returns to the frame-0 man with price tags (title text off). |

**No verbal CTA** ("subscribe", "follow") appears in any of the 10 transcripts. In all 10 transcribed videos the voice starts at 0.00–0.40 s. The last word starts 0.5–1.4 s before the end of the file.

## 5. Caption style (measured on 1080x1920 frames)

I measured with a pixel scan for white text next to dark outline pixels on 32 of the 33 full-res frames (one had no caption), and checked the scan by eye on the crops (`sheets_a/*_caption_crops.jpg`).

| | Zack D. Films | Kurzgesagt |
|---|---|---|
| Vertical position | Text box 76.6–80.2% of frame height, centre **78.0–78.5%** (all 5 videos identical) | Text box 77.3–80.2%, centre **78.3–79.0%** (all 6 identical) |
| Size | Ascender-to-baseline **57 px = 3.0% of H**; with descenders 71 px = 3.7% | Ascender-to-baseline **38 px = 2.0% of H**; with descenders 54 px = 2.8% |
| Width | 25–59% of frame width | 16–40% of frame width |
| Weight / face | Heavy, wide humanist sans (Verdana-Bold-like), white | Medium weight geometric sans, white |
| Stroke / shadow | Dark outline ~3 px plus a soft drop shadow down-right (by eye) | Thin dark outline ~2 px, no visible drop shadow (by eye) |
| Words per caption | Read from storyboards: mean 2.4 (range 1–4, n=21, Z2) | Mean 2.6 (range 1–4, n=43, K1) |
| Case / punctuation | Sentence case, commas dropped, "?" kept ("forever?") | Sentence case, keeps commas and full stops ("begins to race.") |
| Highlight colour | **None seen.** Every caption word is white. | **None in captions.** Colour emphasis appears only in the frame-0 title card ("Killer" in pink, "COCAINE" in cyan) and in label pills. |
| At t=0 | No caption in frame 0 (all 5); captions appear by the 1 s storyboard frame | No caption in frame 0 (title card instead); captions appear under the title card within the first ~2 s |
| Other on-screen text | Only inside the 3D world: a hand-written "30" on a notepad, "30 Steps" painted on a path, W/E arrows, calendar pages "18/20", the brand as a shop sign or uniform name tag | Rounded pill labels for terms and stats ("~70% of Aquifers…", "Transporter Protein", "SAFFRON ~$10/g"), one big bouncy term ("Water Bankruptcy"), game HUD bars ("Monthly Budget", "Bills"), a caveat pill at the top ("According to rat studies – human responses may differ!") |

**Sync of numbers and labels** (1 s resolution): Kurzgesagt's labels appear on the storyboard frame at or just after the spoken word. Examples: "1,000°C" spoken 24.56 s, label on the 25 s frame. "water bankruptcy" 15.8–16.1 s, big text on the 16 s frame. "70%" 17.0 s, pill on the 18 s frame. "seven" 63.4 s, "$1 → $7" on the 63 s frame. Zack's "30 steps" is spoken 20.8 s and painted on the ground from the 21 s frame. At this resolution I can't check the guide's ≤0.2 s rule.

## 6. Music and SFX: not measured

I couldn't run `ebur128`, `astats` or `volumedetect` because no audio could be downloaded. The only indirect evidence (inferred, not measured) is below.

- YouTube's ASR inserted **[music] markers** 2–8 times per Kurzgesagt video (K1: 6, K3: 8, K4: 5, K5: 2, K6: 6). Several fall mid-speech (for example K4 at 22.3, 28.8, 38.6 s), which suggests a music bed audible under the voice.
- There were **zero** [music] markers in all 5 Zack videos. That is inconclusive: Zack's voice barely pauses (only one word-start gap ≥0.9 s across 5 videos), so the ASR gets little chance to tag music.
- Nothing about SFX on cuts can be detected without audio.

Someone should listen to these before we fix the mix. Rule 10's numbers (music ≥6 dB under the voice, -14 LUFS) still stand without reference data.

## 7. Per-channel summary

**Zack D. Films** (format benchmark; 3D CG; 24–61 s)
- **Pace:** 2.93 WPS pooled (2.72–3.14). Slightly faster in the first 5 s: 3.24 vs 2.88 for the rest. Almost no pauses (1 gap ≥0.9 s in 186 s of speech).
- **Cuts:** a new shot about every 1.5 s, roughly 5–8 cuts per 10 s by eye (lower bound). Shot types rotate fast: wide, extreme close-up (hands, objects), face reaction, top-down, aerial, cutaway diagram (Z4's X-ray of the uniform with yellow impact rings).
- **Hook:** frame 0 is always mid-action with no text. The first sentence is long (17–31 words) scene-setting narration that already contains the premise and often the promise: "…but each bullet headed towards a different part of his uniform."
- **First payoff:** 4–13 s in the explainers (median ~9 s). The stories (Z1) hold the twist until ~45 s.
- **Captions:** heavy white, 3.0% cap height, centre at ~78% of H, 2–4 words, no highlight colour.
- **Endings:** the last line is the concrete result ("He walked away with only minor injuries."). The video cuts ~1 s after the last word. No CTA and no loop to frame 0. The ending often rhymes with the opening (Z2's sunset becomes a sunrise; Z1's empty pot).
- **Branding:** only inside the world ("ZACK D FILMS" on a shop sign in Z1 at ~20 s, on a uniform name tag in Z4 at ~7 s, "KD" livery on the plane in Z2). Descriptions and tags are empty.

**Kurzgesagt** (look benchmark; flat vector 2D; 67–84 s)
- **Pace:** 2.96 WPS pooled (2.67–3.13). Flat from the first 5 s to the rest (2.96 vs 2.96). About 1 s of air after key stats and terms: K4 pauses after "…than Earth can supply." (6.0 s) and after "…water bankruptcy." (16.1 s). That makes 15 gaps ≥0.9 s across 5 videos.
- **Cuts:** fewer, about 2.4–3.8 per 10 s (a shot every ~3 s). But inside a shot something new arrives every 1–2 s: a circular magnifier inset joined to the object by a line (K1, K2, K3, K5), a label pill, a HUD bar draining, a toggle flipping. Transitions are motivated: diagonal wipes (K4 25 s, K5 17 s), a paper-tear (K3 48 s), dissolves.
- **Hook:** frame 0 is a **title card**, with big bold title text (lines 3.5–6.5% of H, placed 11–30% down the frame) over a character. It is held ~2 s while the voice says a 4–7-word hook: "Our moon has a silent killer." / "We're running out of water." / "Being poor is expensive."
- **First payoff:** 2–6 s (median ~3.8 s), usually the first concrete number or the first mechanism shot.
- **Captions:** medium-weight white, 2.0% cap height, centre at ~78.5% of H, 1–4 words, punctuation kept, no highlight colour.
- **Look (sampled):** deep navy and indigo backgrounds (#07002a to #120056 in K1), purples (#4523b9, #440a7b), and bright accents in cyan (#15f7ec, #1ddfc4), yellow (#f8bf1a, #fade20) and magenta (#d168e6, #e188c5). I sampled these by median-cut on three JPEG frames per video, so they are approximate. Style: flat shapes, no line art, glows and light rays behind the key object, big-eyed characters, objects given faces (knives, sugar box, brain).
- **Metaphor worlds:** each video runs on one metaphor that comes back. A cooking pot and chef (K5 returns to it at 29, 57 and 64 s), a snake as "the trap" (K6: 3, 9–20, 35 and 60–65 s), a crime scene and suspect lineup (K2). Game UI stands in for abstract quantities: a spacecraft health bar (K1 12–16 s), "Monthly Budget / Bills" HUD bars (K6 9–17 s), a "CREDIT BOOST" power-up card (K6 14–16 s), a gravity "G ON/OFF" toggle (K5 3–10 s), a "▶▶▶" fast-forward icon for time skips (K5 13–16 and 44–48 s).
- **Endings:** 2 of 5 loop exactly to the frame-0 image (K1, K6). K4 returns to its first scene. The last line is a "we" line or a stinger ("…floats, clings, and cuts."). No CTA. Descriptions are 1–2 sentences plus a sources link.

## 8. Phrasing patterns (from the transcripts)

- **Sentence length:** Zack mean 16.0 words (median 16, n=34); Kurzgesagt 13.7 (median 14, n=81). Kurzgesagt mixes in punchy sentences of 6 words or fewer: "And it gets worse." "Your brain adapts fast." "Scientists call this water bankruptcy." "It's a downward spiral." (12 such sentences in 5 videos, against 3 in Zack's 5.)
- **"You":** 3.7% of Zack's words and 3.3% of Kurzgesagt's. It jumps where the viewer is the subject: Z5 8.0% ("the sticky juices cover your face as you eat"), K3 8.3% ("Your heart begins to race, your blood pressure spikes").
- **Questions:** one per channel, both as the hook: "…could you hop in a plane and chase the sunset, avoiding nighttime forever?" and "Why does cocaine feel so good?"
- **Zack's devices:**
  - "You see," to deliver the explanation or twist (3 times: "You see, the king had previously boiled all of the seeds so they couldn't grow.").
  - "Oh, and" to add a beat ("Oh, and the aircraft would need to mostly run on autopilot…").
  - "Meaning" for the consequence.
  - Sentences chained with "and" (19 uses).
  - Openers: "When…" (4), "But…" (4), "He…" (4), "And…" (4).
- **Kurzgesagt's devices:**
  - An escalation line: "And it gets worse."
  - Naming the term with a pause after it: "Scientists call this water bankruptcy."
  - Imperative "recipe" voice: "First, swirl huge amounts of dust and gas around a newborn star. Turn on gravity…"
  - Money in daily units: "about 1% of global GDP or 29 cents per person a day", "for the price of a coffee a week".
  - Caveat lines: "We're not here to tell you what to do, but…"
  - Openers: "But" (4), "And" (4), "As" (4), "When" (3), "So" (3), "Even" (3).
- **Watch-outs (rule 11):** Kurzgesagt uses "Here's how the trap works." (close to the banned "Here's the thing") and ends K1 on a triple ("floats, clings, and cuts"). Z1 ends on a tidy moral. Don't copy these.

## 9. Patterns worth copying (each tied to an observation)

1. **Aim for about 2.9–3.0 words per second, which is 130–180 words for 45–60 s.** Both channels measured 2.93 and 2.96 WPS pooled, and no video fell outside 2.67–3.14.
2. **Open on frame 0 mid-action with the voice starting at once.** All 5 Zack first frames are mid-action with no text (seeds dropping into hands, a knife in the melon, a lunge in a bar). The voice starts at 0.00–0.40 s in all 10 transcribed videos. For us, that means the Up price already climbing on frame 0, with no title card. We are not copying Kurzgesagt's title card: rule 4 forbids it, and Zack's 80–90M views show it isn't needed.
3. **Keep the hook sentence short and flat, then put the first concrete number or mechanism on screen before ~5 s.** Kurzgesagt's hooks are 4–7 words and reach the first payoff at 2–6 s (K4: "40% more fresh water" at 3.8 s, the pond turning red at ~5 s).
4. **Change the picture every ~1.5 s, or bring in a new element inside a held shot every 1–2 s.** Zack cuts about every 1.5 s. Kurzgesagt holds shots ~3 s but adds an inset, pill or HUD change every 1–2 s. For a painted 2D film, the Kurzgesagt version (fewer cuts, constant in-shot arrivals) is cheaper and keeps rule 7.
5. **Show numbers as in-world objects or small pills, timed to the word.** Examples: Zack's notepad "30" and "30 Steps" painted on the path; Kurzgesagt's "SAFFRON ~$10/g" tag, "$1 → $7" and "29 cents" coin, all on the frame of the spoken number. For us: 62¢ on a price tag, $1 as a coin that splits into YES and NO.
6. **Turn abstract quantities into game UI.** Kurzgesagt's spacecraft health bar, "Monthly Budget / Bills" HUD bars draining as a snake bites, a gravity ON/OFF toggle and a ▶▶▶ time-skip icon each made an abstract idea readable without a slide. Order-book depth as two HUD bars and the 15-minute clock as a ▶▶▶ skip fit this directly.
7. **Use a circular magnifier inset to zoom into mechanisms.** It appears in K1, K2, K3 and K5: a circle joined by a line to the object, showing the inside while the context stays on screen. It suits bid-bid minting, where we zoom into the "exchange" and see $1 of collateral become a YES+NO pair.
8. **Pick one metaphor world and return to it.** K5 keeps coming back to the pot and chef; K6's snake is "the trap" at 3, 9, 35 and 60 s. For us, one recurring object (for example, the $1 coin) carries the thread.
9. **Leave about 1 s of air after the key term or number.** Kurzgesagt left 15 gaps ≥0.9 s, placed after stats and terms ("…water bankruptcy." then a 0.9 s gap). Zack has none but is shorter and more narrative. We need that air after "bid-bid" and the fee twist.
10. **End on the concrete result, cut within ~1 s of the last word, and loop the last image into frame 0.** K1 and K6 dissolve back to their first frame. Every video ends 0.5–1.4 s after the last word starts, with no CTA in any of the 10.
11. **Captions: white, 2–3 words, heavy weight at about 3% cap height (Zack's size), thin outline plus a soft shadow.** Both channels put captions at 76.6–80.2% of frame height, but that sits inside the bottom-25% band rule 9 tells us to avoid, so we centre ours at ≤72% of H. Neither channel uses a highlight colour in captions. Rule 3's single highlight colour is our own addition, so keep it to one key word per caption at most.
12. **Put required disclaimers in a small top pill.** Kurzgesagt shows "This short was made possible through a grant by the Gates Foundation" as a tiny grey pill in the top ~3% of frame 0 (K4, K6) and a caveat pill ("According to rat studies – human responses may differ!") at the top of K2 around 7–9 s. Our "Not financial advice" and "unofficial explainer" tags can use the same treatment, kept below the top 10% safe margin.

## 10. Files

- Contact sheets (JPEG, ≤250 KB each) are in `/home/user/ClaudeAnimationBase/short/research/sheets_a/`:
  - `*_sb_00-23s.jpg`: storyboard frames 0–23 s at 1 s spacing, timestamps burned in.
  - `*_hires.jpg`: the t=0 frame plus YouTube's three full-res auto frames.
  - `*_ending.jpg` and `*_loop-ending.jpg`: the last frames of Z1, K1 and K6.
  - `zack_first_frames.jpg` and `kurz_first_frames.jpg`: all first frames side by side.
  - `*_caption_crops.jpg`: caption close-ups at 1080p.
- Raw working data (not committed) is in `/tmp/claude-0/-home-user-ClaudeAnimationBase/b9e37835-d4c1-5268-ba1c-9734d2deae34/scratchpad/yt_a/`:
  - `subs/<id>.en-orig.json3`: word-timed ASR.
  - `meta/<id>.json`: metadata.
  - `frames/<id>/`: storyboard frames.
  - `tx_stats.json`: per-video transcript stats.
  - `zack_list_full.txt` and `kurz_list.txt`: channel lists with views.
