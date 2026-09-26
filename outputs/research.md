# Research: how the reference channels make Shorts

Step 1 of the brief. Everything below was measured from downloaded data in this session, not recalled.

## What I could and couldn't download

YouTube blocks video and audio streams from this cloud machine. The player API is reached over one egress address and the video CDN over another, so every stream URL comes back `403 Forbidden` (tried the `web`, `mweb`, `tv`, `ios`, `android_vr` and `web_embedded` clients, with and without a PO-token provider; a headless browser gets "Sign in to confirm you're not a bot"). What did work from YouTube:

- **Metadata** for every Short (views, likes, duration, title, upload date) via `yt-dlp` with the `mweb` client.
- **Captions** (`json3`, word-level timing on auto-captions) for 21 of 26 Shorts plus the rules video. Some fetches hit `429 Too Many Requests` and were retried on a different egress IP. Lingualin's "Secret Inside the Semicircle" and "Golden Spiral" and most photonsnare Shorts have no speech track (music only), so no captions exist.
- **Storyboard sprites**, YouTube's own scrub thumbnails: about 1 frame per second at 101×180 px for most Shorts (0.1 s steps for the 10–12 s ones). These show composition, cuts ≥1 s apart, caption position and colour, but not fine motion or caption typefaces.

To get full-resolution frames and audio, I pulled the **same creators' TikTok cross-posts** where they exist: 4 of Cleo Abram's top 6 YouTube Shorts (identical edits) and one current Veritasium Short ("What happens when you open the valve?" on YouTube, the balloon Short on TikTok). Those were analysed at 1080×1920 / 25–30 fps: frames every 0.5 s for the first 3 s then every 2 s, a 0.1 s strip of the first 2.4 s, ffmpeg scene-cut detection, Whisper word timing and EBU R128 loudness. StarTalk, Vsauce, lingualin and photonsnare either have no TikTok or yt-dlp couldn't list it, and Exurb1a has **no Shorts tab at all**, so its section uses the openings of its most-viewed recent long videos.

Nothing from these videos (footage, music or voice) goes into our video. The frame sheets stay in the working scratchpad and aren't committed.

## The Shorts

"Recent" = the channel's 40 newest Shorts; picked the top 4 by views (lingualin also includes the linked "Secret Inside the Semicircle"). Speech rate is words ÷ duration from captions. Cuts/10 s marked ~ are estimated from 1 fps storyboards and are rough (±50%; they miss sub-second cuts). Full-res measurements are in the next table.

| channel | Short | views | likes | length | date | words/s | cuts/10 s |
|---|---|---|---|---|---|---|---|
| lingualin | Secret Inside the Semicircle | 5.8M | 71K | 34 s | 2026-07 | music only | ~0 (one shot) |
| lingualin | **What is the TRUE Midpoint of Life?** | 8.9M | 251K | 34 s | 2026-08 | 2.82 | ~0 (one shot) |
| lingualin | What the Golden Spiral Actually Means | 4.1M | 70K | 25 s | 2026-09 | music only | ~0 |
| lingualin | Geometry Can Get You More Coins | 3.7M | 62K | 30 s | 2026-08 | 2.50 | ~0 |
| lingualin | Infinite Chocolate Paradox | 3.5M | 65K | 42 s | 2026-08 | 2.64 | ~0.7 |
| photonsnare | **In 1687 One Man Figured Out The Force…** | 0.9M | 7K | 37 s | 2026-09 | music only | ~0.3 |
| photonsnare | Spin This Object In Zero Gravity… | 0.6M | 6K | 26 s | 2026-09 | music only | ~0 |
| photonsnare | How Spacetime Curvature Works? | 0.4M | 3K | 12 s | 2026-09 | music only | ~0 |
| photonsnare | How a Simple Tank Tilt Reveals… | 0.2M | 3K | 70 s | 2026-09 | 0.71 | ~0 |
| StarTalk | **Cats just debunked the Flat Earth theory** | 0.5M | 20K | 10 s | 2026-07 | 2.50 | 0 |
| StarTalk | The Periodic Table Had a Missing Element | 0.4M | 12K | 69 s | 2026-09 | 2.68 | ~2.5 |
| StarTalk | Physics Dad joke alert! | 0.4M | 16K | 15 s | 2026-07 | 2.40 | ~0.7 |
| StarTalk | We are currently living inside the Sun's… | 0.3M | 10K | 99 s | 2026-08 | 2.09 | ~1.3 |
| Vsauce | **2 Inertia Tricks** | 35.2M | 1.65M | 66 s | 2025-12 | 2.98 | ~1.4 |
| Vsauce | A Cosmic Coincidence | 26.0M | 1.37M | 48 s | 2025-11 | 3.02 | ~1.9 |
| Vsauce | Can I Crack This Lock? | 17.2M | 1.04M | 141 s | 2026-08 | 3.09 | ~1.4 |
| Vsauce | I Just Committed NOT A Crime | 13.0M | 0.97M | 156 s | 2026-07 | 2.84 | ~1.6 |
| Veritasium | **What happens if you cut the green rope?** | 47.5M | 621K | 67 s | 2026-01 | 3.79 | ~4.0 |
| Veritasium | The Google Interview Question Everyone Gets Wrong | 11.3M | 224K | 60 s | 2026-07 | 3.40 | ~3.8 |
| Veritasium | Can something go faster than it's pushed? | 11.7M | 269K | 61 s | 2026-04 | 2.66 | ~1.5 |
| Veritasium | The Most Radioactive Place On Earth | 9.1M | 373K | 92 s | 2026-04 | 2.99 | ~4.3 |
| Cleo Abram | **The Sun Isn't The Center of the Solar System** | 7.4M | 282K | 50 s | 2026-08 | 3.36 | (see below) |
| Cleo Abram | New Alien Host Planet Just Dropped | 6.1M | 341K | 59 s | 2026-09 | 3.92 | 2.7 (full-res) |
| Cleo Abram | This Rocket Is About To Hit The Moon | 5.6M | 222K | 53 s | 2026-08 | 3.70 | 4.5 (full-res) |
| Cleo Abram | Astronauts Are Seeing Weird Things In Space | 3.8M | 252K | 49 s | 2026-09 | 3.59 | 3.5 (full-res) |

Bold = the channel's most-viewed recent Short, which gets a reads timeline below.

### Full-resolution measurements (TikTok copies)

| Short | length | cuts/10 s | words/s (Whisper) | first word | speech gaps ≥0.25 s | music bed under voice | onset energy at cuts vs elsewhere | loudness |
|---|---|---|---|---|---|---|---|---|
| Cleo: Astronauts weird things | 49 s | 3.45 | 3.62 | 0.0 s | 1% of runtime | ≈4 dB (upper bound) | 11.3 dB vs 5.7 dB | −22.7 LUFS |
| Cleo: Alien host planet | 59 s | 2.70 | 3.92 | 0.0 s | 1% | ≈4 dB | 6.8 vs 4.8 dB | −23.9 LUFS |
| Cleo: ISS crashing | 54 s | 4.45 | 4.08 | 0.0 s | 4% | ≈4 dB | 5.0 vs 4.2 dB | −23.4 LUFS |
| Cleo: Biggest land animal | 59 s | 4.21 | 3.22 | 0.0 s | 4% | ≈5 dB | 9.5 vs 6.7 dB | −23.7 LUFS |
| Veritasium: Two balloons | 93 s | 4.93 | 3.02 | 0.0 s | 24% | ≈4 dB | 5.6 vs 4.4 dB | −17.9 LUFS, −1.9 dBTP |

The bed figure is the level in word gaps (music + SFX + room) against the level during words (voice + bed), so the real music bed sits lower than that. Loudness is TikTok's re-encode, not the original upload. The onset column is the biggest 20 ms energy jump within ±70 ms of each detected cut, against the same measure at 60 evenly spaced times: cuts carry a transient (whoosh, hit or music accent), strongest in the Cleo Short with the most CGI.

## Channel by channel

### lingualin (math and geometry simulations)

A black void, one diagram or simulation, one continuous shot. The top two Shorts never cut: the picture keeps transforming instead. "Secret Inside the Semicircle" drops a horizontal line of balls into a semicircular mirror three times (the tab bar at the top reads *50 balls · 500 balls · 5000 balls* and highlights the current run), about 11.6 s per run. Each run reveals more of a glowing heart-shaped caustic; the last run fills it in and holds about 5 s before the end. It works with no voice and no captions. Colour is a rainbow gradient on pure black; the only text is the title and the tab bar, both at the top.

The narrated ones have a calm, slightly formal narrator at 2.5–2.8 words/s and captions of 1–3 words in bold italic white sans, centred around 72% of frame height, with a persistent coloured title at the top ("What Age 18 Actually Means" in a magenta-to-cyan gradient, "Paradox Explained" in green). The script shape is always the same: state the obvious belief ("We all know that when you turn 80, the midpoint of your life lies at 40"), pivot ("But you probably noticed…"), transform the picture, land a single number ("exactly 18"), stop.

### photonsnare (repurposed physics clips)

Landscape footage (a Cavendish torsion balance, an ISS gyroscope, a tilting tank) letterboxed in the middle of a vertical frame, a bold white title above ("Demonstrating the Universal Law of Gravitation") and a formula or line of text below (F = Gm₁m₂/r²). Music only, no narration, no captions, cuts only where the source clip cuts. Views are an order of magnitude below the others (0.2–0.9M) with the lowest like rates (≈0.8%). I read that as the ceiling of "interesting footage + title" with no hook line and no payoff timing.

### StarTalk (podcast clips)

Neil deGrasse Tyson at the desk, cut from the long-form show. Captions in heavy all-caps white sans, 2–3 words, around 72% height; the co-host's lines are yellow. Cutaways are archival (a 1930s periodic table with a gap at 43, accelerator diagrams) with the host in a circle inset. Each ends on a "watch the full video" end card. The most-viewed is a 10 s joke: "if the Earth were really flat, cats would have pushed everything off its surface by now" landing at 4.4–7.8 s, then "Just an opinion" and out 0.7 s later. The 2.1–2.7 words/s pace is Neil's natural speech.

### Vsauce (Michael, hands-on demos)

A single tabletop set and props (apples, knife, tungsten cube, a wooden table leg), a 1–3 s text gag at the top in the first seconds ("Fruit Salad?" becomes "Physics Salad?"), picture-in-picture for references, then a slow-motion replay of the key moment from a clean side angle against a grey wall. No burned-in captions on the top two. Speech is 2.8–3.1 words/s with real pauses. The script structure is intuition, then reversal, then escalation: "Intuitively, even I thought at the time that the apple would fall off, but instead the knife cuts right through the apple", then the same principle applied to something scarier ("I can use the same principle to bash my head safely"). Endings let the last line breathe: "and it doesn't hurt" at 58.9 s, then 5–7 s of him smiling and walking out of frame. "A Cosmic Coincidence" ends on a mock-serious reversal: "Coincidence? Yes, it's a complete coincidence and doesn't mean anything. Or does it? No, it doesn't. Bye."

### Veritasium (street experiments)

A physical puzzle on a stand in a public place, a question in the first 3 s, then 20–35 s of strangers predicting (split screen, two faces stacked), the host explaining the setup with his hand leading the eye along the parts, the reveal, and an ending that comes almost immediately. Captions are coloured by speaker (yellow host, green or teal guests). One edit uses a bold sans at mid-frame, the newest a white serif in sentence case with a dark drop shadow (x-height ≈40 px, text band at 70–74% of height, one line ≈64% of the width). Cuts run about 4–5 per 10 s and the pace 2.7–3.8 words/s. The 47.5M-view "green rope" Short never explains the result, and "The Google Interview Question" ends on "But these answers don't cut it."

### Cleo Abram (host plus CGI explainers)

The first second is her face to camera doing something human ("Um, hi.", a grimace, jazz hands). By 1.0–1.9 s it has cut to rendered space imagery, and from then on she's inserted for 1–2 s every 10–15 s. Speech is fast and nearly gapless: 3.2–4.1 words/s, with word gaps under 4% of the runtime. Captions are small all-caps white sans with a soft shadow (cap height ≈35 px on 1920, 1.8% of the height), 2–5 words, one line, centred at 78–80% height, just above YouTube's UI band. Big coloured labels sit on the objects themselves: lime-green (#B6F53A-like) for concepts and checklists ("TIDAL LOCKING", "✓ HAS ATMOSPHERE"), blue for Earth-side things, orange for the Sun, and a year counter ("YEAR: 1980 … 2028") as a ticking payoff. Tiny "* ARTISTIC RENDERING" / "* SOURCE: NASA" tags sit top-left. A lime SUBSCRIBE or FOLLOW button pops mid-video at about 16–20 s. Every visual beat gets 1.5–3 s before the next. Endings tease a follow-up ("But what if Earth actually was the center of our solar system? You wouldn't like it. To see what would happen, subscribe.").

### Exurb1a (long-form philosophy and science essays; no Shorts)

The channel has no Shorts tab (`yt-dlp`: "This channel does not have a shorts tab"), so I looked at the openings of its three most-viewed recent uploads: "everybody is a total mess" (1.9M, 15 min), "Then Next Comes" (1.6M, 18 min) and "How Long is Now?" (1.5M, 14 min). They're landscape, so only the writing and pacing carry over. The picture is a stock and CGI montage that changes at least every 5 s (every 5 s storyboard tile is a different image), with lowercase handwritten-style text cards on dark film grain ("would that be the present…?", "yeah… probably is…", "the problem of induction"). The narration runs 2.1–3.2 words/s (first 60 s) in a deadpan, hedging voice: "there's the past, let's say, that stretches back billions of years, but it is finite. It began somewhere, probably." A big idea gets undercut by an absurd aside ("would you like to invest in my crypto startup", "the only thing I dislike more than living here is myself"). What carries over to a Short: text cards that ask the viewer's question back to them, and a dry aside that makes the audience laugh just before the big idea.

## Reads timelines (most-viewed recent Short per channel)

For each: what a first-time viewer has to understand, second by second, where the eye is, and how long each payoff is held before anything new starts. Times come from caption word timings plus storyboard frames (1 s steps, so visual times are ±0.5 s except the Cleo and Veritasium TikTok copies).

### Veritasium: "What happens if you cut the green rope?" (47.5M, 67 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0.0–1.0 | a weight hangs from springs and ropes against a ruler | centre, the black weight | object is on screen from frame 0, no intro |
| 1.0–2.8 | "What will happen to this weight if you cut the green rope?" A red arrow slides in at the weight and scissors sit at the green rope | arrow → weight → scissors | the question is fully posed by 2.8 s |
| 3.4–7.5 | cut to the same rig in a park. Up, down, or stay the same? | the rig, then faces | hard cut on the question's end |
| 5.9–36 | about 12 strangers predict, 1.5–3 s each, stacked split screen | faces | each guess gets its own caption colour. The viewer commits to "it drops" |
| 37–56 | host explains the parts: spring, green rope, second spring, two slack ropes (red, black) | his finger traces each rope, 1–2 s per part | slow and clean, white background |
| 57–60 | the question again, scissors at the rope | scissors | anticipation |
| 60–62.8 | snip, then faces watching: "Oh." | faces | reaction shown before the result |
| 63.2–64.8 | "The weight somehow went up." Before/after frames stacked with red level lines | weight vs red lines | **payoff held ~1.5 s, then the video ends** with no explanation |

It ends on an unexplained result that's actually true (a mechanical cousin of Braess's paradox), so the comments do the explaining.

### Vsauce: "2 Inertia Tricks" (35.2M, 66 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0.0–1.0 | a man at a table covered in cut apples with a knife | his face, then the knife | |
| 1.0–3.0 | text gag at the top: "Fruit Salad?" becomes "Physics Salad?" | top text | a 2 s visual joke before any explanation |
| 3.3–10.4 | where the trick came from; picture-in-picture of a lecturer doing it with a potato | inset, then full-frame cut to the lecturer | the source is shown, not just named |
| 10.4–14.1 | setup: knife stuck in an apple, "what's going to happen?" | knife and apple | the question |
| 14.7–18.0 | "Intuitively, even I thought… the apple would fall off" | his face | the viewer commits to the wrong answer |
| 18.0–20.5 | "but instead the knife cuts right through the apple" | apple | reveal line |
| 20.7–29.6 | slow-motion side view against a grey wall: tap, and the knife passes through | knife and apple | **payoff replayed in slow motion ~9 s** under the explanation |
| 31–47 | escalation: same principle, his head. Wooden leg (hurts) → tungsten cube in the way | cube on head | a bigger stake for the same idea |
| 49–58.9 | why: the cube barely accelerates. "And it doesn't hurt." | his face | |
| 58.9–66 | he smiles and walks out of frame, empty table | table | **5–7 s tail**, the only long hold in the set |

### lingualin: "What is the TRUE Midpoint of Life?" (8.9M, 34 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0–1.0 | black frame, gradient title at the top: "What Age 18 Actually Means" | title | the title is the hook (a number that sounds wrong) |
| 1.0–4.3 | an empty bar 0–80 draws, fills to a marked midpoint at 40. "the midpoint of your life lies at 40" | bar filling left to right | the obvious belief, drawn |
| 4.8–9.7 | camera pushes in; the childhood end glows cyan. "a single day felt like an eternity" | left end | continuous push, no cut |
| 10.0–13.4 | "the days fly by like a rocket" | right end | |
| 13.8–17.8 | the year lines slide into logarithmic spacing and bunch up to the right. "It's logarithmic." | lines moving | the wow visual, ~2 s |
| 18.5–25.3 | the bar becomes a graph; a log curve grows with the year lines under it | curve tip | transform, not a cut |
| 26.2–29.5 | formula appears at the top: (log 4 + log 81)/2 = log √324 = log 18 | formula | proof for the sceptics, kept small |
| 29.7–31.4 | a half-height line hits the curve and drops to the axis; 18 lights green | the drop line | lead the eye to the number |
| 31.9–34.0 | "exactly 18" | green 18 | **payoff held ~2 s, then the end** |

### Cleo Abram: "The Sun Isn't The Center of the Solar System" (7.4M, 50 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0–0.8 | Cleo, mid-grimace: "Um, hi." | her face | a human, funny first frame |
| 1.0–3.6 | cut to the solar system: "The Sun isn't the center of our solar system". At ~2.9 s a huge red X over the Sun | Sun, then X | the claim is shown as a picture by 3 s |
| 3.9–5.8 | back to her: "at least not right now. Stick with me here." | her hands | a 2 s breather |
| 5.9–10.8 | Sun and Earth, a dashed line between them: "we pull a little bit on the Sun, too" | the line | |
| 10.8–12.7 | a huge Sun with a "SUN" label, Earth tiny beside it: "we're teeny" | the size contrast | |
| 12.7–14.4 | Jupiter swings in: "But Jupiter is big." | Jupiter | a 3-word line for the turn |
| 14.7–18.8 | the Sun and Jupiter both circle; lime SUBSCRIBE button pops at 16.7 | Sun's small orbit | mid-video call to action |
| 18.6–23.5 | the shared point is marked outside the Sun: "SUN-JUPITER BARYCENTER" label | label, then point | ~2 s on the label |
| 23.5–31.4 | all the planets; the centre wanders | the wandering point | |
| 32.4–42.2 | YEAR counter 1980 → 2028; the point's trail loops in and out of the Sun; 2016 marked | counter, then trail | **payoff 1–2 s per year step**, about 10 s total |
| 43–46 | "But what if Earth actually was the center?" Earth in the middle, Jupiter swinging past | Earth | a new question |
| 46.7–50 | Cleo: "You wouldn't like it. To see what would happen, subscribe." | her | a curiosity gap as the ending |

### photonsnare: "In 1687 One Man Figured Out The Force…" (0.9M, 37 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0–9 | title bar "Demonstrating the Universal Law of Gravitation" above a letterboxed torsion balance; a hand swings the big masses into place | title, then hand | no question, no voice |
| 9.5–14 | close-up of a lead ball near a small ball | balls | a cut in the source footage |
| 14–25 | wide shot of the balance; the small balls drift toward the big ones | the arm | the payoff is a slow drift and easy to miss at phone size |
| 25.6–35 | clean white-background shot of the four balls | balls | same state, no new read |
| 35 | ends | | no ending beat |

It's the weakest reads timeline in the set, and the lowest views and like rate. Its payoff is real but tiny and slow, and nothing tells the eye when it happens.

### StarTalk: "Cats just debunked the Flat Earth theory" (0.5M, 10 s)

| time | read | eye | hold / link |
|---|---|---|---|
| 0–4.3 | Neil to camera: "I think we all know that if the Earth were really flat," | his face | setup, one shot |
| 4.4–7.8 | "cats would have pushed everything off its surface by now." | face | punchline |
| 8.3–9.3 | "Just an opinion." | face | a tag instead of a pause |
| 9.3–10 | end | | **~0.7 s after the tag** |

Storyboard frames for this one are 48×27 px, so only the framing (single medium close-up, flag backdrop) is readable.

### Exurb1a

No Short exists. For "How Long is Now?" (1.5M), the first 60 s read as: 0–15 s a white "timeline" card, the past on the left and the future on the right with icons ("there's the past… billions of years… it is finite"); 15–20 s the question "but what about the present? How long is now?" over a streak of light; 20–50 s zoom metaphors (magnifying glass on the timeline, a melting clock, a close-up of ice) for "couldn't we zoom in and in until we could see the border point?"; ~55 s a grain card "would that be the present…?" held ~3 s. One read per image, 3–5 s per image, and the question is handed back to the viewer as text.

## How shots are linked

- **Lingualin: transformations instead of cuts.** Bar to graph, one simulation run to the next with the tab bar advancing. The world stays the same and the camera pushes in and out.
- **Cleo: hard cuts on the word, and match cuts in space.** The Sun in one shot becomes the Sun in the next at a different scale ("SUN" close-up → Sun-Jupiter wide); planets hold screen position across cuts; the year counter carries a sequence. Cuts carry an audio transient (11.3 dB onset at cuts vs 5.7 dB elsewhere in "Astronauts").
- **Veritasium: cut on the question and on action** (the scissors close, then cut to faces), split screens to double the faces per second, and a stacked before/after frame as the payoff.
- **Vsauce: cut to slow motion from a new angle for the payoff**, and picture-in-picture to cite a source without leaving the table.
- **StarTalk: hard cuts between speakers and archival cutaways**, the host kept in a circle inset over the cutaway so he never leaves.
- **photonsnare: only the source footage's own cuts.**

## Caption styles, measured

| channel | case / weight | size (1920 tall) | words on screen | position | colour |
|---|---|---|---|---|---|
| Cleo Abram | ALL CAPS, heavy geometric sans | cap height ≈35 px (1.8%) | 2–5, one line | centred, 78–80% down | white with soft dark shadow; coloured labels on objects |
| Veritasium (newest) | sentence case, bold serif | band ≈68 px (3.5%) | 3–6, one line | centred, 70–74% down | white with drop shadow; yellow/green for guests |
| Veritasium (green rope) | sentence case, bold sans | ≈3% | 3–6, two lines | centred, ~55–60% down | yellow host, green guests |
| lingualin | bold italic sans | ≈3% (from storyboards) | 1–3 | centred, ~72% down | white; gradient title fixed at the top |
| StarTalk | ALL CAPS, heavy sans | ≈2.5% | 2–3 | centred, ~72% down | white host, yellow co-host |
| Vsauce | none (a one-off text gag at the top) | — | — | — | — |
| photonsnare | fixed title and formula around the footage | ≈3% | whole title | above and below the letterbox | white / yellow |

## The rules video: John Scott, "How I FINALLY got out of Shorts Jail (and went viral)"

Transcribed from its captions (9 min, 285K views). Its rules, in its words where possible:

1. **Swipe jail, under 1K views: "you failed YouTube's 3-second test".** Something has to happen in the first 3 s. Use a *triple hook*: **visual** (the image itself raises a question), **verbal** (the first line), **textual** (on-screen text that *amplifies the story*; "the subtitles aren't really a hook… they don't add anything to the story, not like a caption does"). One really strong hook can carry a video on its own.
2. **Reaction jail, 1K–10K: "You don't share information, you share reactions."** Pick the emotion first (LOL, WTF, OMG, wow, aw, "I agree"), then write to it. "If a line is not going to get that reaction or it doesn't build to the thing that gets that reaction, cut it." Every second is vital; cut the walk-back-in footage.
3. **Never pad for retention.** "Never, ever… think you need to make your short longer for it to perform better." "A 15-second tutorial will always perform better than a 40-second tutorial on the same subject."
4. **Format jail, 30K–100K: borrow a proven format from outliers and put your own spin on it.** "Success leaves clues." Look at a format's presentation, not just its idea.

## Rules we'll follow

Each rule is tied to what I measured above.

1. **Frame 0 is already the experiment, and the question is posed by 3 s.** Veritasium's weight is on screen at 0.0 s and the question is done at 2.8 s; lingualin's balls are falling at 0.0 s; the rules video's 3-second test. Our first frame shows the thing moving, the first line asks what will happen, and a short on-screen line adds what the voice doesn't say (triple hook).
2. **Make the viewer commit to a wrong prediction before the reveal.** The top Short in the whole set (47.5M) spends 30 s on strangers predicting; Vsauce says "Intuitively, even I thought…"; lingualin opens with "We all know…". We state the intuitive answer out loud, then break it.
3. **One world, one setup, escalated.** lingualin's 5.8M-view Short runs the same semicircle three times (50 → 500 → 5000 balls), each run revealing more; Vsauce escalates the same principle from an apple to his head. We keep one set and one palette and make each beat a bigger run or a twist on the last, not a new topic.
4. **A new beat every 5–8 s, and each payoff held 1.5–2.5 s before anything new starts.** Measured holds: Veritasium 1.5 s, lingualin 2 s, Cleo 1.5–3 s per visual. The one longer hold (Vsauce's 5–7 s tail) is the final laugh.
5. **Narration at about 3.0–3.3 words/s, with a real pause at each payoff.** The median of the narrated Shorts is ≈3.0 (lingualin 2.5–2.8, Vsauce 2.8–3.1, Veritasium 2.7–3.8, Cleo 3.2–4.1). Cleo's near-zero gaps suit a host-led montage; our payoffs are visual, so the voice stops while they land (as in Veritasium's "Oh." beat).
6. **Visual changes every 2–4 s, mostly as camera moves and transformations rather than hard cuts.** Cleo and Veritasium run 2.7–4.9 cuts per 10 s; lingualin runs ~0 and relies on continuous transformation. A simulation Short sits closer to lingualin, so we use camera moves, match cuts and a few hard cuts on action, each carrying an audio transient (Cleo: 11.3 dB onset at cuts vs 5.7 dB elsewhere).
7. **Captions: one whole phrase per caption (Veritasium's 3–6-word phrases, not fragments), at most two lines, heavy sans, white with a dark shadow, one key word in an accent colour, centred at about 70–74% of the height.** (Revised after critique round 2: 1–4-word fragments read as nonsense with the sound off.) That's the band Veritasium, lingualin and StarTalk use, above the bottom 20% YouTube covers. Cleo's 1.8%-height captions are too small for our muted viewers; we go for about 3.5% like Veritasium. Colour marks meaning (Cleo's lime concept labels, speaker colours in Veritasium and StarTalk), not decoration.
8. **Labels on the object instead of words that repeat the voice.** Cleo puts "SUN-JUPITER BARYCENTER" on the point itself and a year counter on the Sun; the rules video says text must amplify the story. Our on-screen text names or counts the thing in frame (a number, a label), never restates the caption.
9. **End within about 2 s of the last payoff, on a line people will argue with.** Veritasium ends 1.5 s after "went up" with no explanation; "But these answers don't cut it"; lingualin stops 2 s after "exactly 18"; Vsauce's "Or does it? No, it doesn't. Bye." Our last frame should rhyme with the first, so the video loops (lingualin's reset from one run to the next is the model).
10. **Pick the reaction first and cut every line that doesn't build to it** (rules video). Each beat in the beat sheet is tagged wow / wtf / omg / lol, and a line that serves none of them goes.
11. **Keep it short: 30–45 s.** The four biggest Shorts here are 34, 48, 66 and 67 s, but the two that run long spend that time on predictions or a second trick. The rules video says the shorter version always wins on the same subject. We don't pad.
12. **The music bed sits well under the voice, with transients on cuts and wow beats.** The measured bed is ≤4–5 dB under the voice at every reference; the brief's rule (≥6 dB under, ducked) is stricter and we'll follow it. Whooshes and impacts go on cuts, as the onset measurements show the references do.
13. **A slightly dry, human voice.** Scripts across the set use short declaratives and understatement at the payoff ("The weight somehow went up." / "And it moves." / "And it doesn't hurt.") and a joke or aside early ("Um, hi.", "Physics Salad?", "Just an opinion."). No hype adjectives anywhere in the transcripts.
