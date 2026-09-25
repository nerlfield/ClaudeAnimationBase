// sets.js: the set pieces more than one shot uses, with fixed geometry so shots agree at every seam.
// Shot files (short/shots/*.js) build on these and on look.js; anything only one shot needs lives in that shot's file.

// ---------- timing ----------
// Cut times: every cut sits on a beat (116.3 bpm, offset 0.11) inside a pause in the narration.
const CUT = { A: 0, B: 5.269, C: 14.555, D: 18.683, E: 27.969, F: 37.255, G: 42.414, H: 51.185, I: 58.923, END: 65.6 };
// wt(seg, word, n): the start time (video seconds) of the n-th occurrence of `word` in sentence `seg` (words.json).
// wt('A1', 'eighty') → 2.89. Matching ignores case and punctuation. wte(): the word's end time.
const _norm = s => s.toLowerCase().replace(/[^a-z0-9'-]/g, '');
function _word(seg, word, n = 0) {
  const hits = WORDS.filter(w => w.seg === seg && _norm(w.w) === _norm(word));
  if (!hits[n]) { console.error(`wt: no "${word}" #${n} in ${seg}`); return { start: 0, end: 0 }; }
  return hits[n];
}
const wt = (seg, word, n = 0) => _word(seg, word, n).start;
const wte = (seg, word, n = 0) => _word(seg, word, n).end;
const segStart = id => SEGS.find(s => s.id === id).start, segEnd = id => SEGS.find(s => s.id === id).end;

// ---------- the desk: two stacked screens and the trader (shots A, G, I) ----------
const DESK = { mx: 70, my: 210, mw: 630, mh: 470, tx: 70, ty: 730, tw: 630, th: 270, top: 1060, youX: 800 };
// The market card inside the market screen, and its Up button (for pushes into it).
const CARD = { x: DESK.mx + 14, y: DESK.my + 10, w: DESK.mw - 28 };
const UPBTN = { cx: 247, cy: 507, w: 246, h: 245 };
// The framings every desk shot uses: HOOK is frame 0 (and the loop's last frame); WIDE shows the trader too.
const FRAME = { HOOK: [385, 605, 1.15], WIDE: [470, 640, 1.0] };
// desk(t, st): the whole desk scene. st = {
//   card: {...} for card() in look.js (up, clock, hi, pulse, title, bar, example),
//   fn: tt → BTC price for the ticker (default btcPath), lo/hi: ticker range, span: seconds shown, ptb: dashed level,
//   named: 0..1 flips the ticker's tag from "?" to "BINANCE", tagPulse: 0..1,
//   hide: 0..1 (1 = the trader is ducked out of sight behind the desk), you: {...} options for you() (a pose/emotion),
//   upGlow / tickGlow: extra screen light 0..1 }
function desk(t, st = {}) {
  room(t);
  boilSeed('desk');
  paint(rectPts(-400, DESK.top, W + 800, 1400, 2), { wash: '#1D1A1F', ink: null });
  inkLine([[-400, DESK.top], [W / 2, DESK.top - 4], [W + 400, DESK.top + 2]], 1.1, C.ink, 'ink', .4);
  paint(rectPts(-400, DESK.top + 4, W + 800, 26, 1), { wash: '#2A2530', ink: null });
  // the market screen
  screen(DESK.mx, DESK.my, DESK.mw, DESK.mh, { key: 'mkt', glowCol: '#3E8F63', glow: .5 + .4 * (st.upGlow || 0) });
  card(CARD.x, CARD.y, CARD.w, st.card || {});
  // the other screen: a fast exchange's BTC ticker; its name tag is a "?" until it's revealed
  screen(DESK.tx, DESK.ty, DESK.tw, DESK.th, { key: 'tick', glowCol: '#8C8672', glow: .35 + .4 * (st.tickGlow || 0) });
  const fn = st.fn || (tt => btcPath(tt));
  const tk = ticker(DESK.tx + 10, DESK.ty + 58, DESK.tw - 20, DESK.th - 70, { t, span: st.span || 14, fn, lo: st.lo || 84380, hi: st.hi || 84620, ptb: st.ptb, key: 'desk' });
  txt('BTC / USDT', DESK.tx + 34, DESK.ty + 36, 30, C.creamDim, { align: 'left', ink: false });
  txt('$' + Math.round(fn(t)).toLocaleString('en-US'), DESK.tx + DESK.tw / 2 + 40, DESK.ty + 36, 32, C.tape, { ink: false });
  const named = clamp(st.named || 0), tp = st.tagPulse || 0, flip = Math.abs(Math.cos(named * Math.PI));   // a card flip
  if (tp > 0) glow(DESK.tx + DESK.tw - 120, DESK.ty + 36, 110, '#E9E3D0', .7 * tp);
  pill(named < .5 ? '?' : 'BINANCE', DESK.tx + DESK.tw - 120, DESK.ty + 36, 28 * (1 + .25 * tp), { key: 'name', bg: named < .5 ? C.panelHi : '#3A3A2A', col: C.cream, w: 170 * Math.max(.05, flip) });
  // a mug and a cable: the desk is a place
  boilSeed('mug');
  paint(rrPts(120, 1110, 90, 110, 14, 1), { wash: '#3A3446', ink: C.ink, sw: 1 });
  paint(ellPts(165, 1112, 45, 10, 16, .5), { wash: '#241F2A', ink: C.ink, sw: .7 });
  inkLine([[240, 1215], [320, 1190], [420, 1230], [560, 1200]], .9, '#34303A', 'ink', .6);
  // the trader, standing on the desk to the right of the screens
  const hide = Math.min(1, st.hide ?? 0);   // may go below 0: an overshoot above the desk when popping up
  if (hide < 1) you(DESK.youX, DESK.top + 200 * hide, 21, { view: 'q', flip: true, ...(st.you || feelYou('thinking', t, { view: 'q', flip: true })) });
  return tk;
}

// Frame 0 of the video, which shot I must end on so the loop is seamless: a fresh round (Up 50¢, 14:59 left), the
// camera at HOOK0.cam, the trader hidden, the ticker's tag a "?", and the fast screen about to surge (HOOK0.btc).
const HOOK0 = {
  cam: [360, 600, 1.12],
  card: { up: 50, clock: 899, hi: 'up', pulse: .12, example: true },
  btc: tt => btcPath(tt, 84430) + 150 * easeOut(seg(tt, -.3, 1.8)), lo: 84360, hi: 84660,
};

// ---------- inside the market: the two order books (shots C, D, E, F) ----------
// Fixed layout so C, D, E and F agree: Up book on the left, Down on the right, the mint zone above them.
const BOOK = { U: [60, 540, 390, 560], D: [470, 540, 390, 560], mint: [465, 330], cam: [460, 760, 1] };
// book(x, y, w, h, side, st): depth bars with no labels; asks above the spread (dim, hollow), bids below (solid).
// st = { asks: [5 sizes], bids: [5 sizes], askK / bidK: 0..1 how far the bars have slid in, askOp: 0..1 ask opacity,
//   spread: 0..1 glow on the gap, header: 0..1 (the header's scale pop), rows: 0..1 ladder unroll }
// Returns row positions: { bidY(i), askY(i), bidX0, spreadY } so shots can put chips and tags on rows.
function book(x, y, w, h, side, st = {}) {
  const up = side === 'up', col = up ? C.up : C.down, dk = up ? C.upDk : C.downDk, rows = 5, rh = (h - 150) / (rows * 2);
  const unroll = st.rows ?? 1, hk = st.header ?? 1;
  boilSeed('book' + side);
  const hh = lerp(96, h, ease(unroll));
  if (hh > 20) paint(rrPts(x, y, w, hh, 26, 1.5), { wash: C.panel, ink: C.ink, sw: 1.1 });
  if (hk > .01) {   // header: the side's colour and arrow
    const s = backOut(hk), cx = x + w / 2, cy = y + 51, hw = (w - 32) * s, ht = 70 * s;
    paint(rrPts(cx - hw / 2, cy - ht / 2, hw, ht, 20 * s, 1), { wash: col, ink: null });
    const a = 24 * s;
    paint(up ? [[cx, cy - a], [cx + a * .9, cy + a * .1], [cx + a * .33, cy + a * .1], [cx + a * .33, cy + a], [cx - a * .33, cy + a], [cx - a * .33, cy + a * .1], [cx - a * .9, cy + a * .1]]
             : [[cx, cy + a], [cx + a * .9, cy - a * .1], [cx + a * .33, cy - a * .1], [cx + a * .33, cy - a], [cx - a * .33, cy - a], [cx - a * .33, cy - a * .1], [cx - a * .9, cy - a * .1]], { wash: C.cream, ink: null });
  }
  const y0 = y + 110, sy = y0 + rows * rh, gap = 34;
  const asks = st.asks || [.35, .55, .4, .7, .5], bids = st.bids || [.8, .6, .9, .45, .65];
  const vis = yy => unroll >= 1 || yy + rh < y + hh - 10;
  for (let i = 0; i < rows; i++) {   // asks: row 4 (the lowest ask) sits just above the spread
    const k = ease(clamp((st.askK ?? 1) * 1.6 - (rows - 1 - i) * .15)), len = (w - 60) * asks[i] * k, yy = y0 + i * rh;
    if (len > 4 && vis(yy)) paint(rrPts(x + w - 30 - len, yy + 6, len, rh - 12, 8, .8), { wash: mixCol(dk, C.panel, .35), washOp: 255 * (st.askOp ?? 1), ink: mixCol(col, C.panel, .3), sw: .6 });
  }
  if (st.spread) { const g = st.spread; glow(x + w / 2, sy + gap / 2, w * .5, '#E9E3D0', .35 * g); inkLine([[x + 30, sy + gap / 2], [x + w - 30, sy + gap / 2]], .8 * g, C.cream, 'inkfine', 0); }
  for (let i = 0; i < rows; i++) {   // bids: row 0 (the highest bid) sits just below the spread
    const k = ease(clamp((st.bidK ?? 1) * 1.6 - i * .15)), len = (w - 60) * bids[i] * k, yy = sy + gap + i * rh;
    if (len > 4 && vis(yy)) paint(rrPts(x + 30, yy + 6, len, rh - 12, 8, .8), { wash: col, ink: C.ink, sw: .6 });
  }
  return { bidY: i => sy + gap + i * rh + rh / 2, askY: i => y0 + i * rh + rh / 2, bidX0: x + 30, askX1: x + w - 30, spreadY: sy + gap / 2, rh };
}
// Both books at their fixed places. st.U / st.D are per-book states (see book()); returns { U, D } row positions.
function books(t, st = {}) {
  return { U: book(...BOOK.U, 'up', { ...st, ...(st.U || {}) }), D: book(...BOOK.D, 'down', { ...st, ...(st.D || {}) }) };
}
// A price chip: a small painted token with its price, the thing a hand places on a bid row.
function chip(x, y, label, col, o = {}) {
  const k = o.k ?? 1; if (k <= .01) return; const r = 46 * backOut(k) * (o.s || 1);
  boilSeed('chip' + label);
  if (o.glow) glow(x, y, r * 2.4, col === C.up ? '#6BE08E' : '#FF8A5C', o.glow);
  paint(ellPts(x, y + r * .12, r, r * .9, 20, .6), { wash: mixCol(col, C.ink, .4), ink: null });
  paint(ellPts(x, y, r, r * .9, 20, .6), { wash: col, ink: C.ink, sw: .9 });
  txt(label, x, y + 2, r * .72, C.cream, { ink: false });
}

// ---------- the exchange's stamp (shot D) ----------
function press(x, y, drop) {   // a knob, a neck and a heavy block with a die face, slammed down by `drop` px
  boilSeed('press');
  const Y = y + drop;
  paint(ellPts(x, Y - 250, 58, 50, 20, 1), { wash: '#6B5A8E', ink: C.ink, sw: 1.1 });
  paint(rrPts(x - 26, Y - 210, 52, 90, 10, 1), { wash: '#4E4468', ink: C.ink, sw: 1 });
  paint(rrPts(x - 160, Y - 130, 320, 96, 26, 1.5), { wash: '#5A4F7A', ink: C.ink, sw: 1.2 });
  paint(rrPts(x - 176, Y - 44, 352, 34, 10, 1), { wash: '#3A3350', ink: C.ink, sw: 1 });
}

// ---------- the fee hill (shots E → F: the hill flattens into the scale's beam) ----------
// A price track from 1¢ (left) to 99¢ (right) at baseline y, humping up in the middle (the sell fee peaks at 50¢).
// k = 1 full hill, 0 flat (a straight beam). Returns the point at price p (0..1) for putting things on it.
const HILL = { x0: 90, x1: 850, y: 900, h: 330 };
function feeHill(t, k = 1, o = {}) {
  const P = [], n = 36, at = p => [lerp(HILL.x0, HILL.x1, p), HILL.y - k * HILL.h * Math.pow(Math.sin(p * Math.PI), 1.6)];
  for (let i = 0; i <= n; i++) P.push(at(i / n));
  boilSeed('hill');
  paint([...P, [HILL.x1, HILL.y + 40], [HILL.x0, HILL.y + 40]], { wash: o.col || '#2E3A33', ink: null });
  inkLine(P, 1.4, o.line || C.cream, 'ink', .5);
  return at;
}
