// config.js for the Short: a vertical 1080×1920 frame at 30 fps. The narration (short/voice) sets the length;
// bpm and offset are set to the music once it's picked, so cuts and hits land on beats.
//   boil: 10 drawings a second, so each boil drawing holds exactly 3 frames at 30 fps.
const PROJECT = { duration: 65.6, bpm: 100, offset: 0, fps: 30, w: 1080, h: 1920, boil: 10,
  fonts: ['"Lilita One"'], audio: 'short/audio/mix.m4a',
  fills: 'wash' };   // no GPU here: watercolour texture comes from baked plates (look.js), live shapes use washes
