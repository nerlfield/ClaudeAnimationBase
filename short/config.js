// config.js for the Short: a vertical 1080×1920 frame at 30 fps. The narration (short/voice) sets the length;
// bpm 116.3 / offset 0.11 were solved so a beat falls inside every pause where a shot cuts (see STORYBOARD.md);
// the music is stretched and aligned to that grid.
//   boil: 10 drawings a second, so each boil drawing holds exactly 3 frames at 30 fps.
const PROJECT = { duration: 65.6, bpm: 116.3, offset: 0.11, fps: 30, w: 1080, h: 1920, boil: 10,
  fonts: ['"Lilita One"'], audio: 'short/audio/mix.m4a',
  fills: 'wash' };   // no GPU here: watercolour texture comes from baked plates (look.js), live shapes use washes
