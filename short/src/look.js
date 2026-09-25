// look.js: the one look of the Short, defined once (see short/STYLE.md). Every shot paints through these helpers,
// so no shot invents its own colours, type, screens, coins or UI. All pure functions of time.
//
// Frame: 1080×1920. Safe zone: key action in x 40..900, y 200..1110. Captions own the band y 1130..1250.
// Below 1250 is for secondary things only (desk, props, the character's feet); below 1440 is YouTube's UI.

// ---------- palette ----------
const C = {
  night: '#16181B', nightHi: '#1F2327', deep: '#0F2A1F', deepHi: '#173A2B', bezel: '#101214', panel: '#22262B', panelHi: '#2D3238',
  grid: '#39404A', ink: '#1E1B22',
  up: '#389A57', upLt: '#62C482', upDk: '#236B3B',            // Limitless green.500 (Up / Yes)
  down: '#ED5023', downLt: '#F4865C', downDk: '#A63A18',      // Limitless red.500 (Down / No)
  neon: '#C3FF00',                                            // caption highlight only
  cream: '#F4EEDC', creamDim: '#A9A493', mute: '#6B7079',
  gold: '#E7B447', goldDk: '#A9771F', goldLt: '#F7DB8E',      // the $1 coin
  twap: '#7F8FFF', twapDk: '#4E5BC9',                         // the Chainlink 60-second average
  tape: '#E9E3D0',                                            // the fast exchange's price line
  you: '#8E9FE0', youDk: '#5F6DB0', youLt: '#BCC7F2',         // the trader ("you")
  them: '#C98BC4', themDk: '#8F558B', themLt: '#E6BEE2',      // the stranger
};
const FONT = '"Lilita One"';
const SAFE = { x0: 40, x1: 900, y0: 200, y1: 1110, capY: 1190 };

// ---------- type (in-world numbers and labels; captions live in captions.js) ----------
// txt: Lilita One, cream by default, with a soft ink drop shadow. Placed through the camera like letter().
function txt(s, x, y, size, col = C.cream, o = {}) {
  letter(s, x, y, size, col, { font: `${size}px ${FONT}`, ...o });
}
// A painted pill with a label: the one on-screen term/number at a time. k = 0..1 pop.
function pill(s, x, y, size, o = {}) {
  const k = o.k ?? 1; if (k <= .01) return;
  const w = (o.w || s.length * size * .52 + size * .9) * backOut(k), h = size * 1.45 * backOut(k);
  boilSeed('pill' + (o.key || s));
  paint(rrPts(x - w / 2, y - h / 2, w, h, h / 2, 1.2), { wash: o.bg || C.panelHi, washOp: o.bgOp ?? 255, ink: o.ink ?? C.ink, sw: o.sw ?? .9 });
  txt(s, x, y + size * .04, size * backOut(k), o.col || C.cream, { ink: false, alpha: clamp(k * 2) });
}

// ---------- ground and light ----------
// The room: a dark ground with slow green and violet blooms, so the frame is never flat. Oversized for camera moves.
function room(t, o = {}) {
  boilSeed('room');
  if (!plate(o.plate || 'room')) paint(rectPts(-300, -300, W + 600, H + 600), { wash: o.col || C.night, ink: null });
  const b = o.bloom ?? 1;   // soft pools of screen light, added (never painted, so they stay clean on the dark ground)
  if (b > 0) {
    glow(330 + 40 * wob(t, .05), 460, 700, '#1F6B45', .4 * b);
    glow(820, 1300 + 30 * wob(t, .04, .3), 560, '#3B3470', .35 * b);
  }
}
// Dust motes drifting in the screen light: stable per mote (hash), moving in closed form.
function motes(t, n = 26, box = [0, 0, W, 1250], col = C.cream) {
  for (let i = 0; i < n; i++) {
    boilSeed('mote' + i);
    const x = box[0] + frac(hash(i) + t * (.004 + .01 * hash(i + 7))) * box[2], y = box[1] + frac(hash(i + 3) - t * (.006 + .012 * hash(i + 9))) * box[3];
    const tw = .5 + .5 * Math.sin(t * (1 + hash(i + 5) * 2) + i);
    paint(ellPts(x, y, 2 + 2.5 * hash(i + 2), 2 + 2.5 * hash(i + 2), 8), { wash: col, washOp: 60 + 80 * tw, ink: null });
  }
}

// ---------- screens ----------
// A painted monitor: a bezel, a face, and the light it throws. glowCol tints the halo (additive, under what follows).
function screen(x, y, w, h, o = {}) {
  boilSeed('screen' + (o.key || x + ',' + y));
  if (o.glow !== 0) glow(x + w / 2, y + h / 2, Math.max(w, h) * .75, o.glowCol || '#3E8F63', o.glow ?? .45);
  paint(rrPts(x - 16, y - 16, w + 32, h + 32, 30, 1.5), { wash: C.bezel, ink: C.ink, sw: 1.2 });
  paint(rrPts(x, y, w, h, 18, 1), { wash: o.face || C.panel, ink: null });
  if (o.scan !== false) for (let i = 1; i < 6; i++) inkLine([[x + 14, y + h * i / 6], [x + w - 14, y + h * i / 6]], .35, C.grid, 'inkfine', 0);
}

// ---------- the $1 coin and its two halves (the motif) ----------
// coin(x, y, r): a gold dollar. o.label (default "$1"), o.rot, o.k (0..1 pop), o.shine.
function coin(x, y, r, o = {}) {
  const k = o.k ?? 1; if (k <= .01) return; r *= backOut(k);
  boilSeed('coin' + (o.key || ''));
  if (o.glow) glow(x, y, r * 2.6, '#FFD46A', o.glow);
  push(); translate(x, y); rotate(o.rot || 0);
  paint(ellPts(0, r * .09, r, r, 30, .8), { wash: C.goldDk, ink: null });                       // edge
  paint(ellPts(0, 0, r, r, 30, .8), { wash: C.gold, ink: C.ink, sw: clamp(r / 90, .5, 1.3) });
  paint(ellPts(0, 0, r * .78, r * .78, 26, .6), { wash: mixCol(C.gold, C.goldLt, .35), ink: C.goldDk, sw: clamp(r / 140, .35, .9) });
  pop();
  if (o.label !== null) txt(o.label || '$1', x, y + r * .05, r * .82, C.goldDk, { ink: false, rot: o.rot || 0 });
}
// half(x, y, r, side): one half of the dollar. side 'up' (green, the left half, arrow up) or 'down' (red, right half).
// The two halves drawn at the same (x, y) make the whole coin. o.rot, o.k pop, o.crumble 0..1 (ash), o.bite 0..1 (fee).
function half(x, y, r, side, o = {}) {
  const k = o.k ?? 1; if (k <= .01) return; r *= backOut(k);
  const up = side === 'up', s = up ? -1 : 1, col = up ? C.up : C.down, dk = up ? C.upDk : C.downDk, lt = up ? C.upLt : C.downLt;
  boilSeed('half' + side + (o.key || ''));
  if (o.glow) glow(x + s * r * .4, y, r * 2, up ? '#6BE08E' : '#FF8A5C', o.glow);
  push(); translate(x, y); rotate(o.rot || 0);
  const cr = clamp(o.crumble || 0), P = [], zz = yy => r * .05 * Math.sin(yy / r * Math.PI * 2.5);   // the torn seam both halves share
  for (let i = 0; i <= 18; i++) { const a = (up ? Math.PI / 2 : -Math.PI / 2) + Math.PI * i / 18; P.push([Math.cos(a) * r, Math.sin(a) * r]); }
  for (let i = 1; i < 8; i++) { const yy = up ? -r + i * 2 * r / 8 : r - i * 2 * r / 8; P.push([zz(yy), yy]); }
  const bite = clamp(o.bite || 0);
  const Q = bite > 0 ? P.map(([a, b]) => { const d = Math.hypot(a - s * r * .75, b + r * .55), R = r * .5 * bite; return d < R ? [s * r * .75 + (a - s * r * .75) / d * R, -r * .55 + (b + r * .55) / d * R] : [a, b]; }) : P;
  const fall = cr * cr * r * 1.6;
  paint(Q.map(([a, b]) => [a, b + r * .09 + fall]), { wash: dk, ink: null });
  paint(Q.map(([a, b]) => [a, b + fall]), { wash: mixCol(col, '#4A4640', cr * .8), ink: C.ink, sw: clamp(r / 90, .5, 1.3) });
  // arrow
  const ax = s * r * .45, ay = fall;
  if (cr < .6) paint(up ? [[ax, ay - r * .42], [ax + r * .26, ay - r * .06], [ax + r * .1, ay - r * .06], [ax + r * .1, ay + r * .38], [ax - r * .1, ay + r * .38], [ax - r * .1, ay - r * .06], [ax - r * .26, ay - r * .06]]
                          : [[ax, ay + r * .42], [ax + r * .26, ay + r * .06], [ax + r * .1, ay + r * .06], [ax + r * .1, ay - r * .38], [ax - r * .1, ay - r * .38], [ax - r * .1, ay + r * .06], [ax - r * .26, ay + r * .06]],
                     { wash: lt, washOp: 255 * (1 - cr), ink: null });
  if (cr > 0) for (let i = 0; i < 14; i++) {   // ash flakes falling away
    const a = hash(i + (up ? 0 : 50)), q = clamp(cr * 1.4 - a * .4), fx = s * r * (.2 + .7 * hash(i + 3)), fy = -r * .8 + 1.6 * r * hash(i + 9) + q * q * r * 3;
    if (q > 0 && q < 1) paint(ellPts(fx + wob(q, 2, a) * 10, fy, r * .07, r * .05, 6, 1), { wash: mixCol(col, '#3A3632', .7), washOp: 255 * (1 - q), ink: null });
  }
  pop();
}

// ---------- the market card (a painted echo of a 15-minute Up/Down market) ----------
// card(x, y, w, st): st = { up: price in cents, clock: seconds left of 900, hi: 'up'|'down'|null (which button glows),
//   pulse: 0..1, title: false to hide the title, bar: true to show the probability bar }
function card(x, y, w, st = {}) {
  const h = w * .78, up = st.up ?? 50, dn = 100 - up;
  boilSeed('card');
  if (st.title !== false) {
    txt('BTC Up or Down', x + 40, y + 62, 54, C.cream, { align: 'left' });
    txt('15 min', x + 40, y + 118, 36, C.creamDim, { align: 'left', ink: false });
  }
  clock(x + w - 92, y + 88, 62, st.clock ?? 900);
  const by = y + 165, bw = (w - 110) / 2, bh = h - 225;
  const hi = st.hi, pu = hi === 'up' ? st.pulse || 0 : 0, pd = hi === 'down' ? st.pulse || 0 : 0;
  button(x + 40, by, bw, bh, 'Up', up, C.up, C.upDk, pu, 'up');
  button(x + 70 + bw, by, bw, bh, 'Down', dn, C.down, C.downDk, pd, 'down');
  if (st.bar !== false) {   // the probability bar: Up share in green, Down in red
    const yb = by + bh + 28, xm = x + 40 + (w - 80) * up / 100;
    boilSeed('bar');
    paint(rrPts(x + 40, yb, xm - x - 40, 18, 9, .6), { wash: C.up, ink: null });
    paint(rrPts(xm, yb, x + w - 40 - xm, 18, 9, .6), { wash: C.down, ink: null });
  }
}
function button(x, y, w, h, label, cents, col, dk, pulse = 0, key = '') {
  boilSeed('btn' + key);
  if (pulse > 0) glow(x + w / 2, y + h / 2, w * .9, col === C.up ? '#6BE08E' : '#FF8A5C', .8 * pulse);
  paint(rrPts(x, y + 8, w, h, 22, 1), { wash: dk, ink: null });
  paint(rrPts(x, y - 4 * pulse, w, h, 22, 1), { wash: col, ink: C.ink, sw: 1 });
  txt(label, x + w / 2, y + h * .27 - 4 * pulse, h * .2, C.cream, { ink: false });
  txt(`${Math.round(cents)}¢`, x + w / 2, y + h * .64 - 4 * pulse, h * .48 * (1 + .1 * pulse), C.cream);
}
// The countdown ring: a full ring is 15 minutes. secs = seconds left.
function clock(x, y, r, secs) {
  boilSeed('clock');
  paint(ellPts(x, y, r, r, 30, .6), { wash: C.panelHi, ink: C.ink, sw: .8 });
  const k = clamp(secs / 900), n = Math.max(2, Math.ceil(40 * k)), P = [];
  for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 + TAU * k * i / n; P.push([x + Math.cos(a) * r * .8, y + Math.sin(a) * r * .8]); }
  if (k > .005) inkLine(P, 1.6, secs < 90 ? C.down : C.cream, 'ink', .3);
  const m = Math.floor(secs / 60), s = Math.floor(secs % 60);
  txt(`${m}:${String(s).padStart(2, '0')}`, x, y + 3, r * .5, C.cream, { ink: false });
}

// ---------- the fast exchange's ticker ----------
// Closed-form BTC path (dollars) around a base, with optional spikes [{t, amp, w}]. Deterministic in t.
function btcPath(t, base = 84468, spikes = []) {
  let v = base + 22 * Math.sin(t * .9) + 13 * Math.sin(t * 2.3 + 1) + 7 * Math.sin(t * 5.1 + 2) + 4 * Math.sin(t * 11.7);
  for (const s of spikes) { const d = (t - s.t) / s.w; v += s.amp * Math.exp(-d * d); }
  return v;
}
// ticker(x, y, w, h, st): the line chart in a screen. st = { t, span (seconds shown), fn (t → price), lo, hi, label,
//   ptb (a Price-to-Beat level, dashed), col }
function ticker(x, y, w, h, st) {
  const { t, span = 20, fn, lo, hi } = st, n = 60, P = [];
  const Y = v => y + h - 20 - (v - lo) / (hi - lo) * (h - 40);
  for (let i = 0; i <= n; i++) { const tt = t - span + span * i / n; P.push([x + 20 + (w - 40) * i / n, Y(fn(tt))]); }
  boilSeed('tick' + (st.key || ''));
  if (st.ptb != null) dashed(x + 20, Y(st.ptb), x + w - 20, Y(st.ptb), C.cream, .8);
  inkLine(P, 1.4, st.col || C.tape, 'ink', .4);
  const last = P[P.length - 1];
  paint(ellPts(last[0], last[1], 9, 9, 12), { wash: st.col || C.tape, ink: null });
  glow(last[0], last[1], 40, '#E9E3D0', .5);
  return { Y, last };
}
function dashed(x0, y0, x1, y1, col = C.cream, sw = .8, dash = 26) {
  const L = Math.hypot(x1 - x0, y1 - y0), n = Math.floor(L / dash);
  for (let i = 0; i < n; i += 2) inkLine([[lerp(x0, x1, i / n), lerp(y0, y1, i / n)], [lerp(x0, x1, (i + 1) / n), lerp(y0, y1, (i + 1) / n)]], sw, col, 'inkfine', 0);
}

// ---------- characters ----------
// You: the trader, a periwinkle block with headphones (the kit's character, recoloured so it never reads as Up or Down).
const YOU = { col: C.you, dk: C.youDk, lt: C.youLt, hat: 'headphones' };
const THEM = { col: C.them, dk: C.themDk, lt: C.themLt, hat: 'beanie' };
function you(x, y, u, o = {}) { clawd(x, y, u, { ...YOU, ...o }); }
function them(x, y, u, o = {}) { clawd(x, y, u, { ...THEM, ...o }); }

// ---------- camera helpers ----------
// A camera that never parks. cam(t, wx, wy, z) puts world point (wx, wy) at the centre of the safe stage (470, 655),
// with a slow drift on top. World coordinates equal screen coordinates at cam(t, 470, 655, 1) (drift aside).
const STAGE = { x: 470, y: 655 };
function cam(t, wx, wy, z = 1, rot = 0, drift = 1) {
  const cx = wx + (W / 2 - STAGE.x) / z, cy = wy + (H / 2 - STAGE.y) / z;
  camBegin(cx + 6 * drift * wob(t, .11), cy + 5 * drift * wob(t, .09, .4), z * (1 + .004 * drift * wob(t, .07, .2)), rot);
}
// Whip-pan smear: streaks across the frame in screen space. p 0..1 through the whip; dir ±1.
function whip(p, dir = 1, col = C.nightHi) {
  if (p <= 0 || p >= 1) return;
  const k = Math.sin(p * Math.PI);
  boilSeed('whip');
  for (let i = 0; i < 16; i++) {
    const y = (i + .5) / 16 * H + jit(10), len = W * (.6 + .8 * hash(i)) * k, x = (dir > 0 ? lerp(-W, W * 2, p) : lerp(W * 2, -W, p)) + (hash(i + 4) - .5) * 600;
    paint(rrPts(x - len / 2, y - 60 * k, len, 120 * k + 20, 40, 6), { wash: i % 3 ? col : C.panelHi, washOp: 230 * k, ink: null });
  }
}
