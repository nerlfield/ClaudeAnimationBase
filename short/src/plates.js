// plates.js: watercolour grounds, painted once with real p5.brush fills and reused as images.
// Fills cost over a second each on software GL, so the big textured backgrounds are baked:
//   node render.mjs --page=short.html --soft-gl --loop=plate_room --stills=0 --out=short/plates/raw_room
//   python3 short/plates/pack.py      (→ short/plates/plates.js, the images as data URIs)
// room() and stage() in look.js draw them. A plate never boils (like the kit's paper); everything on top of it does.
const PLATES = {};
window.preloadAssets = async () => {
  for (const [k, src] of Object.entries(window.PLATE_SRC || {})) PLATES[k] = await loadImage(src);
};
// Draw a plate over the whole view, oversized so camera moves never show its edge.
function plate(name, x = -270, y = -480, w = W * 1.5, h = H * 1.5) {
  const img = PLATES[name]; if (!img) return false;
  flushBrush(); image(img, x, y, w, h); return true;
}

// Watercolour darkens like pigment, so a dark ground is painted the way a painter would: a mid-tone ground, then
// layers of dark pigment over it, leaving the light pools where the screens shine.
function bakeGround(base, darks) {
  window.BAKE = true;
  boilSeed('bake');
  paint(rectPts(-60, -60, W + 120, H + 120), { wash: base, ink: null });
  for (const [x, y, rx, ry, col, op, bleed] of darks) {
    paint(ellPts(x, y, rx, ry, 30, rx * .1), { fill: col, fillOp: op, bleed: bleed ?? .22, tex: .8, border: .6, ink: null });
  }
  window.BAKE = false;
}
// The desk room: green light pooled where the market screen sits, violet where the desk falls into shadow.
LOOPS.plate_room = t => bakeGround('#3C4A42', [
  [860, 300, 620, 520, '#101316', 230], [150, 1500, 700, 700, '#121318', 230], [900, 1450, 600, 700, '#171429', 220],
  [540, 1850, 900, 400, '#0E0F12', 240], [80, 150, 380, 360, '#111A16', 200], [700, 950, 380, 300, '#14231C', 160],
  [330, 500, 420, 360, '#1E4A33', 120, .3], [980, 820, 300, 520, '#121416', 220],
]);
LOOPS.plate_room.len = 1;
// Inside the market: a darker green-black stage, Up's green light on the left, Down's red-orange on the right.
LOOPS.plate_stage = t => bakeGround('#394238', [
  [540, 180, 700, 330, '#101413', 230], [540, 1700, 800, 520, '#0F1113', 240], [60, 1150, 300, 600, '#111614', 220],
  [1020, 1150, 300, 600, '#161112', 220], [260, 800, 360, 480, '#1A4730', 130, .3], [820, 800, 340, 480, '#4E2014', 120, .3],
  [540, 400, 300, 200, '#2A2616', 120], [540, 1250, 520, 260, '#14161C', 200],
]);
LOOPS.plate_stage.len = 1;
