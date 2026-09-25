# "The other screen": a 65.6 s vertical Short on 15-minute BTC Up/Down markets

It's made with this repo's painted p5.brush engine, following [SHORTS_GUIDE.md](SHORTS_GUIDE.md) for the brief in [TOPIC.md](TOPIC.md).

| file | what |
|---|---|
| `final.mp4` | the video (1080×1920, 30 fps, AAC) |
| [STORYBOARD.md](STORYBOARD.md) · [STYLE.md](STYLE.md) · [research.md](research.md) · [sources.md](sources.md) | the plan, the look, the reference research, and facts plus asset licences |
| [UPLOAD.md](UPLOAD.md) | title, description, hashtags and pinned comment |
| `voice/` | the script (`segments.txt`), the narration and its word timestamps |
| `audio/` | the cue sheet, music build and mix scripts. The generated music and SFX files stay out of git (ElevenLabs terms). |
| `src/` | the shared look, sets, captions and baked watercolour plates |
| `shots/A.js … I.js` | one file per shot |

## Rebuild

This needs Node, Chromium or Chrome, and ffmpeg. With no GPU, pass `--soft-gl`; frames take about 1.5–4 s each.

```bash
npm install
node render.mjs --page=short.html --soft-gl --sheet=2.7,25.9,43.5 --out=out/check/sheet.jpg     # look at moments
node render.mjs --page=short.html --soft-gl --frames --workers=4 --frames-dir=out/frames_short  # all 1968 frames
node render.mjs --encode --fps=30 --frames-dir=out/frames_short --audio=short/audio/mix.m4a --out=short/final.mp4
```

- **Audio:** `python3 short/audio/mix.py` re-mixes from `audio/cues.json`. It needs the generated stems on disk (`audio/music.wav`, `audio/sfx/*.wav`).
- **Voice:** `ELEVEN_KEY_FILE=<path> python3 short/voice/tts_segments.py` regenerates the narration, then run `python3 short/voice/make_words_js.py`.
