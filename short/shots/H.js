// H.js: THE 60-SECOND TWIST (51.185 → 58.923). See STORYBOARD.md, shot H.
//   G pushed into the ticker; H opens on its bare panel (C.panel) and reveals the chart up close: the fast exchange's
//   price line, the dashed Price to Beat, and a shaded window over the last 60 seconds. On "sixty-second average" a heavy
//   blue ribbon (Chainlink's 60-second average) draws slowly through the window, just under the line. On "spike" the
//   price shoots up in the last second: a tall green candle with a little flame on its wick. On "barely" the blue
//   average's end nudges up a hair and stays under the line. The nudge is computed, not drawn: the ribbon IS the running
//   60-second mean of the drawn price line, so one second of spike moves it by about 1/60 of the spike's height.
//   You run in after the candle, grab it, and on "burn" it WHOOMPs: your Up half burns to ash, you go ko, then cry.
//
//   One world for H and I: "H space" is the desk's ticker screen magnified 8×, so I can pull back to the desk in one
//   continuous camera move. H space is laid out like screen pixels at H's resting camera; hd() maps it to desk space.
//   The kit below (window.HI) is shared with I.js; I.js adds its acting keys to HI.act.
(() => {
  // ---------- H space ----------
  const HX = 561.25, HY = 846.5, HS = 8;                    // desk = (HX + hx / HS, HY + hy / HS)
  const hd = (x, y) => [HX + x / HS, HY + y / HS];
  const X_END = 840, PXS = 9.8, PTB = 640;                   // the close's x, pixels per second, the old Price to Beat
  const tx = s => X_END + s * PXS;                           // chart time (s before the close) → x
  const X_LEFT = (100 - HX) * HS;                            // the ticker plot's left end (desk x 100)

  // ---------- the price line and its 60-second average (y in H space: smaller = higher price) ----------
  const SPK = 430;                                           // how far the last-second spike climbs
  const A = s => 42 * Math.sin(.19 * s + .7) + 24 * Math.sin(.47 * s + 2.1) + 13 * Math.sin(1.13 * s + .4) + 7 * Math.sin(2.9 * s + 1.3);
  let C0 = 0;
  const base = s => PTB + C0 + A(s) + (s < -60 ? -38 * Math.sin(.045 * s + 1.1) * Math.min(1, (-60 - s) / 40) : 0);
  const price = s => s <= -1 ? base(s) : base(-1) - SPK * (1 - Math.exp(-(s + 1) * 9)) / (1 - Math.exp(-9));
  const twap = s => { let a = 0; const n = 120; for (let i = 0; i < n; i++) a += price(s - 60 + (i + .5) * 60 / n); return a / n; };
  for (let k = 0; k < 3; k++) C0 += 24 - (twap(-1) - PTB);   // the average sits 24 px under the line before the spike
  const OPEN = price(-1), CLOSE = price(0), HIGH = CLOSE - 42, LOW = OPEN + 12, TW0 = twap(0);

  // ---------- times (video seconds), all on or just before their words ----------
  const T = {
    reveal: CUT.H, win: wt('H1', 'this') + .1, bracket: wt('H1', 'sixty-second') - .2, ribbon: wt('H1', 'sixty-second') - .03,
    ribbonEnd: wte('H1', 'average') + .05, labelOut: wt('H2', 'A'), dip: wt('H2', 'spike') - .32, spike: wt('H2', 'spike') - .17,
    peak: wt('H2', 'spike') - .03, nudge: wt('H2', 'barely') - .22, thud: wt('H2', 'barely') - .02,
    run: wt('H2', 'so') - .13, leap: wt('H2', 'candle') + .01, cling: wt('H2', 'candle') + .31, burn: 57.89,   // beat 112
    land: 58.34, cry: 58.62,
  };

  // ---------- painting helpers ----------
  // A flat colour area, painted natively. Identical to a 255 wash on screen (the paper grain multiplies over both), but
  // free on software GL, where a full-frame wash costs ~1 s. For big flat grounds only; edges get ink lines.
  function flat(pts, col, a = 255) {
    if (a <= 0) return;
    flushBrush(); push(); noStroke(); const c = color(col); c.setAlpha(a); fill(c);
    beginShape(); for (const p of pts) vertex(p[0], p[1]); endShape(CLOSE); pop();
  }
  // screen() from look.js with native grounds (same shapes, same boil seeds).
  function screenLite(x, y, w, h, o) {
    boilSeed('screen' + o.key);
    if (o.glow !== 0) glow(x + w / 2, y + h / 2, Math.max(w, h) * .75, o.glowCol, o.glow ?? .45);
    const bz = rrPts(x - 16, y - 16, w + 32, h + 32, 30, 1.5);
    flat(bz, C.bezel); paint(bz, { ink: C.ink, sw: 1.2 });
    flat(rrPts(x, y, w, h, 18, 1), o.face || C.panel);
    for (let i = 1; i < 6; i++) inkLine([[x + 14, y + h * i / 6], [x + w - 14, y + h * i / 6]], .35, C.grid, 'inkfine', 0);
  }
  // ticker() from look.js, drawing only the first k of its line (the new round's line draws in).
  function tickerLite(x, y, w, h, st, k) {
    if (k >= 1) return ticker(x, y, w, h, st);
    const { t, span = 20, fn, lo, hi } = st, n = 60, P = [];
    const Y = v => y + h - 20 - (v - lo) / (hi - lo) * (h - 40);
    const m = n * clamp(k); if (m < 1) return;
    for (let i = 0; i <= Math.floor(m); i++) { const tt = t - span + span * i / n; P.push([x + 20 + (w - 40) * i / n, Y(fn(tt))]); }
    const tt = t - span + span * m / n; P.push([x + 20 + (w - 40) * m / n, Y(fn(tt))]);
    boilSeed('tick' + (st.key || ''));
    inkLine(P, 1.4, C.tape, 'ink', .4);
    const last = P[P.length - 1];
    paint(ellPts(last[0], last[1], 9, 9, 12), { wash: C.tape, ink: null });
    glow(last[0], last[1], 40, '#E9E3D0', .5);
  }
  // desk() from sets.js, rebuilt so the pull-back can afford it (native grounds, parts outside the view skipped) and act
  // on it: st.cardFlip squeezes the card (0..1 width), st.lineK draws the ticker's line in, st.over() paints between the
  // set and the desk's front edge... Same boil seeds as desk(), so switching to desk() on a boil tick shows no seam.
  //   st = { tl (the set's clock: room drift, ticker time), card, fn, lo, hi, named, upGlow, tickGlow, lineK, cardFlip }
  function deskLite(st) {
    const tl = st.tl, cm = CAM, zw = W / 2 / cm.zoom, zh = H / 2 / cm.zoom, V = [cm.cx - zw, cm.cy - zh, cm.cx + zw, cm.cy + zh];
    const vis = (x0, y0, x1, y1) => x1 > V[0] && x0 < V[2] && y1 > V[1] && y0 < V[3];
    room(tl);
    boilSeed('desk');
    flat(rectPts(-400, DESK.top, W + 800, 1400, 2), '#1D1A1F');
    inkLine([[-400, DESK.top], [W / 2, DESK.top - 4], [W + 400, DESK.top + 2]], 1.1, C.ink, 'ink', .4);
    flat(rectPts(-400, DESK.top + 4, W + 800, 26, 1), '#2A2530');
    if (vis(DESK.mx - 16, DESK.my - 16, DESK.mx + DESK.mw + 16, DESK.my + DESK.mh + 16)) {
      screenLite(DESK.mx, DESK.my, DESK.mw, DESK.mh, { key: 'mkt', glowCol: '#3E8F63', glow: .5 + .4 * (st.upGlow || 0) });
      const f = st.cardFlip ?? 1;
      if (f >= 1) card(CARD.x, CARD.y, CARD.w, st.card || {});
      else if (f > .02) {   // a card flip: the painted card squeezes about its centre; its lettering follows and fades
        const cx = CARD.x + CARD.w / 2, cy = CARD.y + CARD.w * .39, n0 = LETTERS.length, sx = toScreen(cx, cy)[0];
        push(); translate(cx, cy); scale(f, 1); translate(-cx, -cy); card(CARD.x, CARD.y, CARD.w, st.card || {}); pop();
        for (const L of LETTERS.slice(n0)) { L.x = sx + (L.x - sx) * f; L.alpha = (L.alpha ?? 1) * clamp((f - .25) / .5); }
      }
    }
    screenLite(DESK.tx, DESK.ty, DESK.tw, DESK.th, { key: 'tick', glowCol: '#8C8672', glow: .35 + .4 * (st.tickGlow || 0) });
    const fn = st.fn || (tt => btcPath(tt));
    tickerLite(DESK.tx + 10, DESK.ty + 58, DESK.tw - 20, DESK.th - 70, { t: tl, span: 14, fn, lo: st.lo || 84380, hi: st.hi || 84620, key: 'desk' }, st.lineK ?? 1);
    if (vis(DESK.tx, DESK.ty, DESK.tx + DESK.tw, DESK.ty + 60)) {
      txt('BTC / USDT', DESK.tx + 34, DESK.ty + 36, 30, C.creamDim, { align: 'left', ink: false });
      txt('$' + Math.round(fn(tl)).toLocaleString('en-US'), DESK.tx + DESK.tw / 2 + 40, DESK.ty + 36, 32, C.tape, { ink: false });
      const named = clamp(st.named || 0), flip = Math.abs(Math.cos(named * Math.PI));
      pill(named < .5 ? '?' : 'BINANCE', DESK.tx + DESK.tw - 120, DESK.ty + 36, 28, { key: 'name', bg: named < .5 ? C.panelHi : '#3A3A2A', col: C.cream, w: 170 * Math.max(.05, flip) });
    }
    if (vis(100, 1100, 580, 1240)) {
      boilSeed('mug');
      paint(rrPts(120, 1110, 90, 110, 14, 1), { wash: '#3A3446', ink: C.ink, sw: 1 });
      paint(ellPts(165, 1112, 45, 10, 16, .5), { wash: '#241F2A', ink: C.ink, sw: .7 });
      inkLine([[240, 1215], [320, 1190], [420, 1230], [560, 1200]], .9, '#34303A', 'ink', .6);
    }
  }
  // Paint the desk's front edge again over whatever stands behind it (for sinking behind the desk), x ≥ x0 only.
  function deskFront(x0) {
    boilSeed('desk');
    const R = rectPts(-400, DESK.top, W + 800, 1400, 2);
    flat([[x0, DESK.top + 1], [W + 400, DESK.top + 3], [W + 400, DESK.top + 1400], [x0, DESK.top + 1400]], '#1D1A1F');
    inkLine([[-400, DESK.top], [W / 2, DESK.top - 4], [W + 400, DESK.top + 2]], 1.1, C.ink, 'ink', .4);
    flat([[x0, DESK.top + 4], [W + 400, DESK.top + 4], [W + 400, DESK.top + 30], [x0, DESK.top + 30]], '#2A2530');
    return R;
  }

  // ---------- the camera ----------
  // Desk-space camera with cam()'s drift. The drift blends from H's (1/8 of a desk unit per unit, on video time) to the
  // loop's (A's cam(t) at t = video time − 65.6), so the last frame's camera is exactly A's frame 0.
  function camDesk(t, wx, wy, z, kLoop = 0) {
    const d = (m, td) => [6 * m * wob(td, .11), 5 * m * wob(td, .09, .4), .004 * m * wob(td, .07, .2)];
    const a = d(1 / HS, t), b = d(1, t - CUT.END), D = a.map((v, i) => lerp(v, b[i], kLoop));
    camBegin(wx + (W / 2 - STAGE.x) / z + D[0], wy + (H / 2 - STAGE.y) / z + D[1], z * (1 + D[2]));
  }
  const camH = (t, hx, hy, z, sh = [0, 0]) => camDesk(t, ...hd(hx + sh[0], hy + sh[1]), z * HS);
  const inH = draw => { push(); translate(HX, HY); scale(1 / HS); draw(); pop(); };   // paint in H space
  // pill() for H space: the shape is painted in H space (so its wobble isn't magnified 8×), the label placed in desk space.
  function hPill(s, x, y, size, o = {}) {
    const k = o.k ?? 1; if (k <= .01) return;
    const w = (o.w || s.length * size * .52 + size * .9) * backOut(k), h = size * 1.45 * backOut(k);
    inH(() => { boilSeed('pill' + (o.key || s)); paint(rrPts(x - w / 2, y - h / 2, w, h, h / 2, 1.2), { wash: o.bg || C.panelHi, ink: o.ink ?? C.ink, sw: o.sw ?? 1.1 }); });
    const [a, b] = hd(x + (o.dx || 0), y + size * .04); txt(s, a, b, size * backOut(k) / HS, o.col || C.cream, { ink: false, alpha: clamp(k * 2) });
  }

  // ---------- the chart (H space) ----------
  const dashes = (x0, x1, y, col, sw, dash, V, keep = () => 1) => {
    for (let x = x0, i = 0; x < x1; x += dash * 2, i++) {
      const a = x, b = Math.min(x1, x + dash), k = keep(i, a, b); if (k <= .02 || b < V[0] - 40 || a > V[2] + 40) continue;
      const m = (a + b) / 2, h = (b - a) / 2 * k;
      inkLine([[m - h, y], [m + h, y]], sw, col, 'inkfine', 0);
    }
  };
  // The tape (the fast exchange's line) up to chart time `end`, the tip nudged by `tipDy`.
  function tape(end, tipDy, col = C.tape) {
    // p5.brush drops a stroke whose span is much longer than the canvas, so the line is two overlapping strokes,
    // starting just off the left of any H framing
    const P = [], R = [];
    for (let s = -118; s < -57; s += .5) P.push([tx(s), price(s)]);
    for (let s = -61; s < -1; s += .5) R.push([tx(s), price(s)]);
    R.push([tx(-1), price(-1) + (end <= -1 ? tipDy : 0)]);
    boilSeed('hi-tape');
    inkLine(P, 2.3, col, 'ink', .35);
    inkLine(R, 2.3, col, 'ink', .35);
    if (end <= -1) return R[R.length - 1];
    const Q = [];   // the last second, its own stroke: it shoots straight up
    for (let k = 0; k <= 4; k++) { const s = -1 + (end + 1) * k / 4; Q.push([tx(s), price(s) + (k === 4 ? tipDy : 0)]); }
    inkLine(Q, 2.3, col, 'ink', 0);
    return Q[Q.length - 1];
  }
  function ribbonPts(end) {
    const P = []; for (let s = -60; s < end; s += 1.5) P.push([tx(s), twap(s)]);
    P.push([tx(end), twap(end)]);
    return P;
  }
  // Everything on the old chart at time t. o.fade 0..1 crumbles it away (I, at the close).
  function chart(t, V, o = {}) {
    const gone = o.fade || 0;
    // the window over the last 60 seconds, sliding in from the right edge
    const wl = lerp(1110, 252, easeOut(seg(t, T.win, T.win + .7)));
    if (wl < 1100 && gone < 1) {
      boilSeed('hi-win');
      flat(rrPts(wl, 170, X_END + 18 - wl, 720, 16, 2), '#29303F', 255 * (1 - gone));
      inkLine([[wl, 176], [wl, 884]], 1.2, '#56608A', 'inkfine', 0);
    }
    // the old Price to Beat
    boilSeed('hi-ptb');
    dashes(X_LEFT, 872, PTB, C.cream, 1.25, 30, V, () => 1 - ease(seg(gone, 0, .7)));
    // the price line; before the spike its tip ticks like a live feed and dips just before the spike (anticipation)
    const sp = seg(t, T.spike, T.peak), end = t < T.spike ? -1 : -1 + easeOut(sp) * .999;
    const dip = 14 * Math.sin(Math.PI * seg(t, T.dip, T.spike));
    const tick = t < T.dip ? 3 * Math.sin(t * 9) + 2 * Math.sin(t * 23 + 1) : 0;
    const bodyTop = OPEN + (CLOSE - OPEN) * backOut(sp);
    let tip = null;
    if (gone < .5) tip = tape(end, t < T.spike ? dip + tick : bodyTop - price(end));
    if (tip) { glow(tip[0], tip[1], 60, '#E9E3D0', .6); boilSeed('hi-tip'); paint(ellPts(tip[0], tip[1], 9, 9, 12), { wash: C.tape, ink: null }); }
    return { tip, bodyTop, sp };
  }
  // the 60 s bracket under the window, drawn out from its centre
  function bracket(t) {
    const k = easeOut(seg(t, T.bracket, T.bracket + .28)) * (1 - ease(seg(t, T.run - .2, T.run + .1)));
    if (k <= .01) return;
    const c = (252 + X_END) / 2, hw = (X_END - 252) / 2 * k, y = 915;
    boilSeed('hi-bracket');
    inkLine([[c - hw, y - 20 * seg(k, .85, 1)], [c - hw, y], [c + hw, y], [c + hw, y - 20 * seg(k, .85, 1)]], 1.7, '#9AA6FF', 'ink', 0);
    inkLine([[c, y], [c, y + 16 * k]], 1.7, '#9AA6FF', 'ink', 0);
  }
  // The blue average: a heavy ribbon from the window's start to chart time `end`, with a glowing end dot.
  function average(t, end, o = {}) {
    if (end <= -59.5) return null;
    const P = ribbonPts(end);
    for (let i = 0; i < P.length; i += 8) glow(P[i][0], P[i][1], 120, '#6F7FFF', .32 * (o.a ?? 1));
    boilSeed('hi-ribbon');
    paint(ribbon(P, 17, 17), { wash: C.twap, ink: C.twapDk, sw: 1.1 });
    inkLine(P.map(([x, y]) => [x, y - 3]), .7, '#B7C0FF', 'inkfine', .4);
    const [x, y] = P[P.length - 1], th = o.thud || 0, r = 12;
    glow(x, y, 70, '#8C9BFF', .7);
    paint(ellPts(x, y, r * (1 + .25 * th), r * (1 - .22 * th), 16), { wash: '#AEB8FF', ink: C.twapDk, sw: 1.2 });
    return [x, y];
  }
  // A flame: a teardrop with a swaying tip, in three layers. k 0..1 grows it.
  function flame(x, y, w, h, t, seed, k = 1) {
    if (k <= .02) return;
    const sway = w * (.35 * Math.sin(t * 13 + seed * 5) + .15 * Math.sin(t * 23 + seed)) * k;
    const hh = h * k * (1 + .12 * Math.sin(t * 19 + seed * 3) + .08 * Math.sin(t * 31 + seed));
    const tear = (s, dy) => {
      const r = w * s / 2 * k, cy = y - r - dy, P = [[x + sway * s, y - dy - hh * s], [x + r * .75 + sway * .45 * s, cy - (hh * s - r) * .45]];
      for (let i = 0; i <= 6; i++) { const a = -.1 + (Math.PI + .2) * i / 6; P.push([x + Math.cos(a) * r, cy + Math.sin(a) * r]); }
      P.push([x - r * .75 + sway * .45 * s, cy - (hh * s - r) * .45]);
      return P;
    };
    boilSeed('flame' + seed);
    paint(tear(1, 0), { wash: '#E8542A', ink: '#8A2A12', sw: .8, curv: .6 });
    paint(tear(.66, w * .06), { wash: '#F7963A', ink: null, curv: .6 });
    paint(tear(.36, w * .1), { wash: '#FFD86E', ink: null, curv: .6 });
  }
  // The candle: a green body from the open to the close, with a wick up to the high and a little flame on it.
  function candle(t, st) {
    if (st.sp <= 0) return;
    const cx = X_END + 30, bw = 36, char = ease(seg(t, T.burn, T.burn + .35)), gone = st.fade || 0;
    const wickTop = OPEN + (HIGH - OPEN) * easeOut(clamp(st.sp / .75)), top = Math.min(st.bodyTop, OPEN - 6);
    const body = mixCol(C.up, '#34302C', char), lt = mixCol(C.upLt, '#4A4540', char);
    if (char < 1) glow(cx, (top + OPEN) / 2, 190, '#6BE08E', .5 * (1 - char) * st.sp);
    boilSeed('hi-candle');
    if (gone < .6) {
      inkLine([[cx, wickTop], [cx, LOW]], 2.4, mixCol(C.upDk, '#2A2622', char), 'ink', 0);
      paint(rrPts(cx - bw / 2, top, bw, OPEN - top, 5, 1), { wash: body, ink: C.ink, sw: 1.3 });
      paint(rrPts(cx - bw / 2 + 5, top + 6, 9, Math.max(4, OPEN - top - 12), 4, .6), { wash: lt, ink: null });
    }
    // the literal little flame on the wick; it flares and leans toward you just before the burn
    const flare = seg(t, T.burn - .14, T.burn), fk = easeOut(seg(t, T.peak - .03, T.peak + .15)) * (1 - seg(t, T.burn + .05, T.burn + .2));
    if (fk > .02) {
      glow(cx, wickTop - 20, 80 + 120 * flare, '#FFB05A', .75);
      flame(cx - 30 * flare, wickTop + 4, 24 + 26 * flare, 48 + 70 * flare, t, 1, fk);
    }
    return { cx, wickTop };
  }
  // Smoke: curling grey wisps rising from (x, y), born from t0 on, each wisp looping every ~1.7 s.
  function smoke(t, x, y, t0, seed, n = 3, sc = 1) {
    if (t < t0) return;
    for (let i = 0; i < n; i++) {
      const per = 1.6 + .3 * hash(seed + i), age = frac((t - t0) / per + hash(seed + i * 7)), life = Math.min(1, (t - t0) / .4);
      if (age < .02) continue;
      const hgt = (90 + 170 * age) * sc, P = [];
      for (let k = 0; k <= 5; k++) { const q = k / 5; P.push([x + (hash(seed + i * 3) - .5) * 40 * sc + Math.sin(q * 3.2 + t * 1.6 + i * 2) * 22 * sc * q, y - hgt * q]); }
      boilSeed('smoke' + seed + '-' + i);
      paint(ribbon(P, 24 * sc * (1 - .3 * age), 6 * sc), { wash: mixCol('#6E6A66', '#A9A493', age), washOp: 170 * (1 - age) * life, ink: null });
    }
  }
  // Ash and dust flakes drifting over the frame (screen space, in front of everything). k scales how many.
  function ash(t, k, n = 22) {
    for (let i = 0; i < n * clamp(k); i++) {
      const x = frac(hash(i * 3.1) + t * (.012 + .02 * hash(i + 2))) * (W + 80) - 40, y = frac(hash(i * 5.7) - t * (.02 + .03 * hash(i + 9))) * 1300;
      const r = 3 + 5 * hash(i + 4), a = Math.sin(t * (.8 + hash(i)) + i) * .5 + .5;
      boilSeed('ash' + i);
      paint(ellPts(x, y, r, r * .7, 7, .8, t * (1 + hash(i)) + i), { wash: i % 3 ? '#8A8580' : '#C9C2B4', washOp: (90 + 110 * a) * Math.min(1, k * 1.5), ink: null });
    }
  }

  // ---------- you: acting and poses (shared with I.js) ----------
  const SOOT = '#3C3632';
  const act = [
    [0, 'determined'], [T.burn, 'ko'], [T.cry, 'cry'],
  ];
  const sootK = t => t < T.burn ? 0 : .78 * ease(seg(t, T.burn, T.burn + .12)) * (1 - .8 * ease(seg(t, 59.2, 64.0)));
  // Your emotion at t, with the soot of the burn painted over the body colour.
  function mood(t, over = {}) {
    const m = actYou(t, HI.act, { take: .8 }), c = tintCols(m), k = sootK(t);
    return { ...m, tint: null, col: mixCol(c.col, SOOT, k), dk: mixCol(c.dk, mixCol(SOOT, C.ink, .4), k), lt: mixCol(c.lt, '#6A625A', k * .9), ...over };
  }
  const SIT = { x: 600, y: PTB };   // where you land after the burn (feet on the old Price to Beat line)
  // The Up half in your near hand, kept upright against the arm's angle.
  const holdHalf = (o) => (u, sw) => half(u * .95, -u * .1, u * 1.2, 'up', { key: 'you', rot: o.rot || 0, crumble: o.cr || 0, k: o.k ?? 1 });

  // Your pose in H: off-screen, then the run, the leap, the cling, the burn, the fall, sitting in the ash.
  function youH(t) {
    if (t < T.run) return null;
    const m = mood(t);
    const cr = ease(seg(t, T.burn + .06, T.burn + .7)), hk = 1 - seg(t, T.burn + .7, T.burn + .85);
    if (t < T.leap - .06) {   // the run: side view, leaning in, the Up half held out in front
      const k = seg(t, T.run, T.leap - .06), x = lerp(-190, 648, k * (1.35 - .35 * k)), ph = (t - T.run) * 3.9;
      const aL = .95 + .15 * Math.sin(ph * TAU), rot = .13;
      return { x, y: PTB, o: { ...m, view: 'side', walk: ph, dy: -.55 * Math.abs(Math.sin(ph * TAU)), rot, aL, sq: -.04, armL: holdHalf({ rot: -(rot + .7 - aL) }) } };
    }
    const crouch = Math.sin(Math.PI * seg(t, T.leap - .06, T.leap + .04));
    if (t < T.cling) {         // the leap: a crouch, then an arc up onto the candle's side
      const k = seg(t, T.leap + .02, T.cling), [x, y] = arcPt([648, PTB], [726, 548], 70, easeOut(k)), air = Math.sin(Math.PI * k);
      const view = k < .35 ? 'side' : 'q', aL = 1.25, rot = .08 - .1 * k;
      return { x, y, o: { ...m, view, sq: .22 * crouch - .14 * air, aL, aR: 1.1 + .3 * k, rot, armL: holdHalf({ rot: view === 'side' ? -(rot + .7 - aL) : rot + aL }) } };
    }
    if (t < T.burn + .15) {    // clinging to the candle; the flame leans down... WHOOMP, blown back
      const blast = easeOut(seg(t, T.burn, T.burn + .1)), shiver = Math.sin(t * 60) * .03 * (1 - blast);
      const aL = 1.25 + .2 * blast, rot = -.02 + shiver - .22 * blast;
      return { x: 726 - 26 * blast, y: 548 - 10 * blast, o: { ...m, view: 'q', aL, aR: 1.35 + .15 * blast, rot, sq: -.1 * blast, armL: holdHalf({ rot: rot + aL, cr, k: hk }) } };
    }
    if (t < T.land) {          // the fall back down to the line, turning to face us
      const k = seg(t, T.burn + .15, T.land), [x, y] = arcPt([700, 538], [SIT.x, SIT.y], 40, easeIn(k));
      const aL = 1.4 - 1.6 * k, rot = -.22 + .3 * k;
      return { x, y, o: { ...m, view: k < .5 ? 'q' : 'front', aL, aR: 1.2 - 1.5 * k, rot, sq: -.08, armL: holdHalf({ rot: rot + aL, cr, k: hk }) } };
    }
    return { x: SIT.x, y: SIT.y, o: { ...m, view: 'front', ...sitPose(t, m), armL: hk > 0 ? holdHalf({ rot: -.75, cr, k: hk }) : null } };
  }
  // Sitting in the ash after the fall: a squash on landing that settles, arms slumped (I.js builds on this).
  function sitPose(t, m) {
    const land = Math.exp(-(t - T.land) * 5) * Math.cos((t - T.land) * 14);
    return { sq: .18 + .22 * land, dy: m.dy * .3, aL: -.75 + m.aL * .15, aR: -.8 + m.aR * .15 };
  }
  const drawYou = p => p && you(p.x, p.y, 30, { ...p.o, boilKey: 'you' });

  // The WHOOMP: flames burst up around you and the candle, then die down to embers.
  function fire(t, cx, cy, front) {
    if (t < T.burn - .02 || t > T.burn + .75) return;
    const a = t - T.burn, grow = backOut(clamp(a / .09)), die = 1 - ease(seg(a, .22, .7));
    if (!front) { glow(cx, cy - 40, 520 * (.7 + .3 * grow), '#FF7A30', .95 * die); glow(cx, cy - 80, 260, '#FFD27A', .8 * die * (1 - seg(a, 0, .3))); }
    for (let i = front ? 1 : 0; i < 11; i += 2) {
      const ang = (i / 10 - .5) * 2.6, r = 90 + 60 * hash(i + 11), fx = cx + Math.sin(ang) * r * 1.4, fy = cy + 70 - Math.cos(ang) * r * .3 + 70 * hash(i + 5);
      const h = (230 + 190 * hash(i + 7)) * (1 - .3 * Math.abs(ang)) * (front ? .8 : 1);
      flame(fx, fy, (70 + 40 * hash(i + 3)) * (front ? .85 : 1), h, t, 20 + i, grow * die * (1 - .35 * hash(i + 2) * seg(a, .1, .5)));
    }
  }

  window.HI = { HX, HY, HS, hd, X_END, X_LEFT, PXS, PTB, tx, price, twap, TW0, T, act, SIT, SOOT,
    flat, screenLite, deskLite, deskFront, camDesk, camH, inH, hPill, dashes, chart, bracket, average, candle, flame, smoke, ash,
    mood, youH, drawYou, fire, holdHalf, sootK, sitPose };

  // ---------- the shot ----------
  // camera in H space: [t, x, y, zoom]; eased; shaken on the spike and the burn
  const CAMK = [
    [T.reveal, 430, 690, .9], [T.reveal + 1.25, 470, 655, 1], [T.spike - .3, 520, 650, 1.05], [T.peak + .12, 545, 600, 1.0],
    [T.thud + .1, 670, 635, 1.17], [T.run + .02, 640, 628, 1.15], [T.run + .35, 480, 575, .95], [T.leap, 585, 548, .97],
    [T.burn - .05, 640, 520, 1.0], [T.land + .1, 650, 560, 1.03], [CUT.I, 660, 560, 1.06],
  ];
  function camera(t) {
    const x = kf(t, CAMK.map(k => [k[0], k[1]])), y = kf(t, CAMK.map(k => [k[0], k[2]])), z = Math.exp(kf(t, CAMK.map(k => [k[0], Math.log(k[3])])));
    const sh = shakeXY(t, 5 * Math.exp(-Math.max(0, t - T.peak) * 8) * (t > T.peak ? 1 : 0) + 16 * Math.exp(-Math.max(0, t - T.burn) * 6) * (t > T.burn ? 1 : 0));
    camH(t, x, y, z, sh);
    return z;
  }

  function shotH(t, lt, dur) {
    camera(t);
    const V = (() => { const c = CAM, zw = W / 2 / c.zoom, zh = H / 2 / c.zoom; return [(c.cx - zw - HX) * HS, (c.cy - zh - HY) * HS, (c.cx + zw - HX) * HS, (c.cy + zh - HY) * HS]; })();
    deskLite({ tl: t - CUT.END, lineK: 0, named: 1, tickGlow: .6, fn: HOOK0.btc, lo: HOOK0.lo, hi: HOOK0.hi });
    let tip, flameAt;
    inH(() => {
      const st = chart(t, V);
      bracket(t);
      // the average draws slowly through the window, then its last second arrives with the spike: a nudge and a thud
      const end = t < T.nudge ? -60 + 59 * ease(seg(t, T.ribbon, T.ribbonEnd)) : -1 + easeOut(seg(t, T.nudge, T.thud));
      const thud = t > T.thud ? Math.exp(-(t - T.thud) * 7) * Math.cos((t - T.thud) * 22) : 0;
      average(t, end, { thud });
      flameAt = candle(t, st);
      // you, the fire, the smoke
      const p = youH(t);
      fire(t, 745, 470, false);
      drawYou(p);
      fire(t, 745, 470, true);
      if (t > T.burn + .15) { smoke(t, SIT.x - 40, SIT.y - 190, T.burn + .2, 3, 3); smoke(t, X_END + 30, 250, T.burn + .1, 9, 2, .8); }
      if (t > T.burn && t < T.burn + .5) { const a = t - T.burn; glow(745, 430, 900, '#FF8A3C', .6 * Math.exp(-a * 7)); }
    });
    // the 60 s label, only while the voice says it
    const lk = seg(t, T.bracket + .06, T.bracket + .2) * (1 - seg(t, T.labelOut - .15, T.labelOut));
    if (lk > 0) hPill('60 s', 546, 985, 46, { k: lk, bg: C.twapDk, col: C.cream, key: 'hi60' });
    camEnd();
    ash(t, seg(t, T.burn, T.burn + .6));
    // in: G's full-frame panel wash lifts off the chart
    const cover = 1 - easeOut(seg(t, T.reveal, T.reveal + .3));
    if (cover > 0) flat(rectPts(-40, -40, W + 80, H + 80), C.panel, 255 * cover);
  }
  shots([[CUT.H, shotH]]);
})();
