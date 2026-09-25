// stills.js: the three style frames for STYLE.md (hook, mid-video explanation, final frame), as standalone loops.
//   node render.mjs --page=short.html --loop=hook --stills=0 --out=short/style
// Each loop maps its time to a video time for the captions (LOOP.captions), so the frame shows the right caption.
// The set pieces here (desk, books, press) are the first drafts the shots will build on.

// ---------- the desk: two stacked screens and the trader ----------
const DESK = { mx: 70, my: 210, mw: 630, mh: 470, tx: 70, ty: 730, tw: 630, th: 270, top: 1060 };
function desk(t, st = {}) {
  room(t);
  // the desk surface and its front edge
  boilSeed('desk');
  paint(rectPts(-400, DESK.top, W + 800, 1400, 2), { wash: '#1D1A1F', ink: null });
  inkLine([[-400, DESK.top], [W / 2, DESK.top - 4], [W + 400, DESK.top + 2]], 1.1, C.ink, 'ink', .4);
  paint(rectPts(-400, DESK.top + 4, W + 800, 26, 1), { wash: '#2A2530', ink: null });
  // the market screen
  screen(DESK.mx, DESK.my, DESK.mw, DESK.mh, { key: 'mkt', glowCol: '#3E8F63', glow: .5 + .4 * (st.upGlow || 0) });
  card(DESK.mx + 14, DESK.my + 10, DESK.mw - 28, st.card || {});
  // the other screen: a fast exchange's BTC ticker; its name tag stays a "?" until it's revealed
  screen(DESK.tx, DESK.ty, DESK.tw, DESK.th, { key: 'tick', glowCol: '#8C8672', glow: .35 });
  const fn = st.fn || (tt => btcPath(tt));
  ticker(DESK.tx + 10, DESK.ty + 58, DESK.tw - 20, DESK.th - 70, { t, span: 14, fn, lo: 84380, hi: 84620, ptb: st.ptb, key: 'desk' });
  txt('BTC / USDT', DESK.tx + 34, DESK.ty + 36, 30, C.creamDim, { align: 'left', ink: false });
  pill(st.named ? 'BINANCE' : '?', DESK.tx + DESK.tw - 120, DESK.ty + 36, 28, { key: 'name', bg: C.panelHi, col: C.cream, w: 170 });
  txt('$' + Math.round(fn(t)).toLocaleString('en-US'), DESK.tx + DESK.tw / 2 + 40, DESK.ty + 36, 32, C.tape, { ink: false });
  // a mug, a cable: the desk is a place
  boilSeed('mug');
  paint(rrPts(120, 1110, 90, 110, 14, 1), { wash: '#3A3446', ink: C.ink, sw: 1 });
  paint(ellPts(165, 1112, 45, 10, 16, .5), { wash: '#241F2A', ink: C.ink, sw: .7 });
  inkLine([[240, 1215], [320, 1190], [420, 1230], [560, 1200]], .9, '#34303A', 'ink', .6);
  // the trader, standing on the desk to the right of the screens, looking at them
  const look = st.look ?? -.6;
  if ((st.hide ?? 0) < 1) you(800, DESK.top + 190 * (st.hide || 0), 21, { ...feel(st.mood || 'thinking', t, { view: 'q', flip: true, lookX: .9, lookY: look }), ...YOU });
}

// ---------- inside the market: the two order books ----------
// Rows are depth bars with no labels; only the one price being spoken gets a tag. asks sit above the spread, bids below.
function book(x, y, w, h, side, st = {}) {
  const up = side === 'up', col = up ? C.up : C.down, dk = up ? C.upDk : C.downDk, rows = 5, rh = (h - 150) / (rows * 2);
  boilSeed('book' + side);
  paint(rrPts(x, y, w, h, 26, 1.5), { wash: C.panel, ink: C.ink, sw: 1.1 });
  // header: the side's colour and arrow
  paint(rrPts(x + 16, y + 16, w - 32, 70, 20, 1), { wash: col, ink: null });
  const ax = x + w / 2, ay = y + 51;
  paint(up ? [[ax, ay - 24], [ax + 22, ay + 2], [ax + 8, ay + 2], [ax + 8, ay + 24], [ax - 8, ay + 24], [ax - 8, ay + 2], [ax - 22, ay + 2]]
           : [[ax, ay + 24], [ax + 22, ay - 2], [ax + 8, ay - 2], [ax + 8, ay - 24], [ax - 8, ay - 24], [ax - 8, ay - 2], [ax - 22, ay - 2]], { wash: C.cream, ink: null });
  const y0 = y + 110, sy = y0 + rows * rh, gap = 34;
  const asks = st.asks || [.35, .55, .4, .7, .5], bids = st.bids || [.8, .6, .9, .45, .65];
  for (let i = 0; i < rows; i++) {   // asks: the lowest ask sits just above the spread
    const k = (st.askK ?? 1), len = (w - 60) * asks[i] * k, yy = y0 + i * rh;
    if (len > 4) paint(rrPts(x + w - 30 - len, yy + 6, len, rh - 12, 8, .8), { wash: mixCol(dk, C.panel, .35), washOp: 255 * (st.askOp ?? 1), ink: mixCol(col, C.panel, .3), sw: .6 });
  }
  if (st.spread) { const g = st.spread; glow(x + w / 2, sy + gap / 2, w * .5, '#E9E3D0', .35 * g); inkLine([[x + 30, sy + gap / 2], [x + w - 30, sy + gap / 2]], .8 * g, C.cream, 'inkfine', 0); }
  for (let i = 0; i < rows; i++) {   // bids: the highest bid sits just below the spread
    const k = (st.bidK ?? 1), len = (w - 60) * bids[i] * k, yy = sy + gap + i * rh;
    if (len > 4) paint(rrPts(x + 30, yy + 6, len, rh - 12, 8, .8), { wash: col, ink: C.ink, sw: .6 });
  }
  return { sy, gap, rh, bidY: sy + gap + rh / 2, askY: sy - rh / 2 };
}
function press(x, y, drop) {   // the exchange's stamp: a knob, a neck and a heavy block, slamming down by `drop` px
  boilSeed('press');
  const Y = y + drop;
  paint(ellPts(x, Y - 250, 58, 50, 20, 1), { wash: '#6B5A8E', ink: C.ink, sw: 1.1 });                    // knob
  paint(rrPts(x - 26, Y - 210, 52, 90, 10, 1), { wash: '#4E4468', ink: C.ink, sw: 1 });                  // neck
  paint(rrPts(x - 160, Y - 130, 320, 96, 26, 1.5), { wash: '#5A4F7A', ink: C.ink, sw: 1.2 });            // block
  paint(rrPts(x - 176, Y - 44, 352, 34, 10, 1), { wash: '#3A3350', ink: C.ink, sw: 1 });                 // die face
}
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
  const U = book(60, 540, 390, 560, 'up', { askOp: .35 }), D = book(470, 540, 390, 560, 'down', { askOp: .35 });
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
