// stills.js: the three style frames for STYLE.md (hook, mid-video explanation, final frame), as standalone loops.
//   node render.mjs --page=short.html --loop=hook --stills=0 --out=short/style
// Each loop maps its time to a video time for the captions (LOOP.captions), so the frame shows the right caption.
// The set pieces here (desk, books, press) are the first drafts the shots will build on.

// The set pieces (desk, book, press) live in short/src/sets.js.

// ---------- the loops ----------
LOOPS.hook = t => {
  const vt = 2.62;
  cam(vt, 385, 605, 1.15);
  desk(vt, { card: { up: 74, clock: 612, hi: 'up', pulse: .8 }, upGlow: 1, fn: tt => btcPath(tt, 84468, [{ t: 2.1, amp: 95, w: .9 }]), hide: 1 });
  camEnd();
};
LOOPS.hook.len = 1; LOOPS.hook.captions = () => 2.95;

LOOPS.mint = t => {
  const vt = 25.95;
  room(vt, { plate: 'stage', bloom: 0 });
  cam(vt, 460, 700, 1);
  motes(vt, 20, [0, 150, W, 1000], C.upLt);
  books(vt, { askOp: .35 });
  glow(465, 380, 260, '#FFD46A', .7);
  coin(465, 390, 118, { glow: .5 });
  press(465, 250, 0);
  for (let i = 0; i < 10; i++) { const a = i / 10 * TAU + .3; paint(starPts(465 + Math.cos(a) * 190, 390 + Math.sin(a) * 150, 16, .28, 4, a), { wash: C.goldLt, ink: null }); }
  camEnd();
};
LOOPS.mint.len = 1; LOOPS.mint.captions = () => 25.95;

LOOPS.final = t => {
  const vt = 65.1;
  cam(vt, 385, 605, 1.15);
  desk(vt, { card: { up: 50, clock: 900 }, ptb: 84416, named: true, fn: tt => btcPath(tt, 84416), hide: 1 });
  camEnd();
};
LOOPS.final.len = 1; LOOPS.final.captions = () => 64.9;
