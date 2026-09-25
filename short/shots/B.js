// B.js: UP OR DOWN, AND THE DOLLAR (5.269 → 14.555). See STORYBOARD.md, shot B.
//   In: A pushed through the Up button, so B opens deep inside the Up zone's green (full-frame C.up) and pulls out of
//   it to reveal the market's stage: a dashed starting line, Up's zone tinted green above it and Down's red below.
//   A Bitcoin marker rides a fast-forwarded 15-minute path while a clock ring empties; it dips below, climbs back and
//   finishes ABOVE the line on "above", and the Up zone flares (7.08). The start dot pulses on "started".
//   Then the Up half slides in from the left ("Up") and the Down half from the right ("Down"); they tremble, pull back
//   and SNAP into the gold dollar on the beat (9.91), the camera lifting; "$1" stamps on for "dollar".
//   "And the winner takes it": the coin bursts back into its halves, Up hops, then swells back into the whole coin
//   while Down is knocked aside and crumbles to ash (11.2). The coin re-forms, a green wedge sweeps 62% of it as the
//   "62¢" tag lands (11.98), and the tag becomes "62%" (13.01), held to the cut with the light breathing.
//   Out: C.js cracks this coin into its halves and whips them apart into the two book headers.
(() => {
  const COIN = { x: 460, y: 591, r: 190 };   // C.js starts from this coin (its halves become the book headers)
  const LINE = 640, ZX0 = 70, ZX1 = 870, ZTOP = 300, ZBOT = 980;   // the race: starting line and the two zones
  const beatAt = n => OFF + n * BEAT;
  // ---- times (video seconds), each read on its word or just before ----
  const tGo = 5.58, tFin = 7.03, tFlare = beatAt(13.5) /* 7.075, "above" 7.083 */, tStart = wt('B1', 'started') - .08, tClr = 7.86;
  const tUpIn = wt('B2', 'Up') - .2, tDnIn = wt('B2', 'Down') - .2, tSnap = beatAt(19) /* 9.912 */;
  const tLbl = wt('B2', 'one', 2) - .04, tSplit = wt('B2', 'and') - .02, tWin = wt('B2', 'winner') - .04, tTake = wt('B2', 'takes') - .02;
  const tCrumble = beatAt(21.5) /* 11.20 */, tSweep = wt('B3', 'So') - .06, tTag = beatAt(23) /* 11.976 */, tFlip = beatAt(25) /* 13.008 */;
  const tTagOut = 14.36;
  const bobY = t => 4 * wob(t, .35) * seg(t, 11.62, 12.3);   // same as C.js's (where it's fully on)

  // ---- the Bitcoin path: a closed-form wander through keys (px above the line), ending well above it ----
  const PK = [0, 72, 30, -30, -84, -36, 48, 112];
  function dev(p) {
    const n = PK.length - 1, f = clamp(p) * n, i = Math.min(n - 1, Math.floor(f)), u = f - i;
    const p0 = PK[Math.max(0, i - 1)], p1 = PK[i], p2 = PK[i + 1], p3 = PK[Math.min(n, i + 2)];
    const base = .5 * (2 * p1 + (p2 - p0) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (3 * p1 - p0 - 3 * p2 + p3) * u * u * u);
    return base + Math.sin(Math.PI * clamp(p)) * (13 * Math.sin(p * 43 + 1) + 7 * Math.sin(p * 97 + 2) + 4 * Math.sin(p * 181));
  }
  const mX = p => lerp(ZX0 + 45, ZX1 - 75, p), mY = p => LINE - dev(p);
  const prog = t => { const s = seg(t, tGo, tFin); return lerp(s, ease(s), .5); };

  // ---- shot-only painting helpers ----
  function band(x0, y0, x1, y1, rt, rb) {   // a zone: a rectangle with rounded top (rt) or bottom (rb) corners
    const P = [], arc = (cx, cy, r, a0) => { for (let i = 0; i <= 5; i++) { const a = a0 + i / 5 * Math.PI / 2; P.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
    if (rt) { arc(x0 + rt, y0 + rt, rt, Math.PI); arc(x1 - rt, y0 + rt, rt, -Math.PI / 2); } else P.push([x0, y0], [x1, y0]);
    if (rb) { arc(x1 - rb, y1 - rb, rb, 0); arc(x0 + rb, y1 - rb, rb, Math.PI / 2); } else P.push([x1, y1], [x0, y1]);
    return P;
  }
  // Is a world point (radius r) inside the frame? The reveal starts at 6.5x zoom, where strokes cost a lot even
  // off-screen, so things out of view are skipped.
  const onScreen = (x, y, r) => { if (!CAM) return true; const [sx, sy] = toScreen(x, y), rr = r * CAM.zoom; return sx > -rr && sx < W + rr && sy > -rr && sy < H + rr; };
  function dashLine(x0, x1, y, xr, col, sw) {   // fixed dashes from x0, drawn up to xr (so a growing line doesn't slide)
    for (let x = x0; x < Math.min(x1, xr) - 4; x += 52) if (onScreen(x + 14, y, 20)) inkLine([[x, y], [Math.min(x + 28, xr, x1), y]], sw, col, 'inkfine', 0);
  }
  function ring15(x, y, r, left, o = {}) {   // the round's clock as a ring that empties (no digits: no extra number)
    const k = o.k ?? 1; if (k <= .01) return; r *= backOut(k);
    boilSeed('ring15');
    if (o.flash > 0) glow(x, y, r * 2.6, '#E9E3D0', .7 * o.flash);
    paint(ellPts(x, y, r, r, 26, .5), { wash: C.panelHi, ink: C.ink, sw: .8 });
    const q = clamp(left), n = Math.max(2, Math.ceil(36 * q)), P = [];
    for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 + TAU * q * i / n; P.push([x + Math.cos(a) * r * .72, y + Math.sin(a) * r * .72]); }
    if (q > .01) inkLine(P, 1.5, q < .12 ? C.downLt : C.cream, 'ink', .3);
    const a = -Math.PI / 2 + TAU * q;
    inkLine([[x, y], [x + Math.cos(a) * r * .5, y + Math.sin(a) * r * .5]], 1, C.cream, 'ink', 0);
    paint(ellPts(x, y, r * .12, r * .12, 8), { wash: C.cream, ink: null });
  }
  function btc(x, y, r, o = {}) {   // the Bitcoin marker: an orange painted coin with a ₿ drawn in strokes
    const k = o.k ?? 1; if (k <= .01) return; r *= backOut(k);
    boilSeed('btc');
    glow(x, y, r * 3.2, '#FFB35C', o.glow ?? .55);
    push(); translate(x, y); rotate(o.rot || 0); scale(1 + (o.sq || 0), 1 - (o.sq || 0));
    paint(ellPts(0, r * .14, r, r, 20, .4), { wash: '#A8561A', ink: null });
    paint(ellPts(0, 0, r, r, 20, .4), { wash: '#F2972E', ink: C.ink, sw: .8 });
    const s = r * .46, c = C.cream, w = 1.4, L = -s * .45;
    inkLine([[L, -s], [L, s]], w, c, 'ink', 0);
    inkLine([[L, -s], [s * .18, -s], [s * .6, -s * .55], [s * .2, -s * .06], [L, -s * .06]], w, c, 'ink', .5);
    inkLine([[L, -s * .06], [s * .3, -s * .06], [s * .78, s * .46], [s * .3, s], [L, s]], w, c, 'ink', .5);
    for (const xx of [-s * .12, s * .22]) { inkLine([[xx, -s * 1.34], [xx, -s]], w, c, 'ink', 0); inkLine([[xx, s], [xx, s * 1.34]], w, c, 'ink', 0); }
    pop();
  }
  function sparks(x, y, age, life, n, rad, col, key, a0 = 0, spread = TAU) {   // a burst of painted four-point stars
    if (age < 0 || age > life) return; const a = age / life;
    boilSeed('sparks' + key);
    for (let i = 0; i < n; i++) {
      const ang = a0 + (i + .5) / n * spread + (hash(i * 7 + key.length) - .5) * .35, d = rad * (.3 + .7 * easeOut(a)) * (.75 + .5 * hash(i * 3 + 1));
      paint(starPts(x + Math.cos(ang) * d, y + Math.sin(ang) * d, 17 * (1 - a) + 2, .3, 4, ang), { wash: col, washOp: 255 * (1 - a * a), ink: null });
    }
  }
  function puff(x, y, age, life) {   // a small cloud of ash where the loser crumbles
    if (age < 0 || age > life) return; const a = age / life;
    boilSeed('puff');
    for (let i = 0; i < 6; i++) {
      const ang = -Math.PI / 2 + (i - 2.5) * .5, d = 40 + 90 * easeOut(a) * (.7 + .5 * hash(i + 40)), s = (22 + 16 * hash(i + 41)) * (.6 + .8 * easeOut(a));
      paint(ellPts(x + Math.cos(ang) * d, y + Math.sin(ang) * d * .7 + 30 * a, s, s * .8, 12, 2), { wash: '#5A534C', washOp: 150 * (1 - a), ink: null });
    }
  }
  function streaks(x, y, dir, k, col, key) {   // painted smears trailing a fast-moving half (dir: +1 moving right)
    if (k <= .03) return;
    boilSeed('streak' + key);
    for (let i = 0; i < 3; i++) {
      const yy = y + (i - 1) * 82 + (hash(i + key.length * 3) - .5) * 24, len = (150 + 110 * hash(i + 11)) * k, x1 = x - dir * (20 + 30 * hash(i + 5));
      paint(rrPts(Math.min(x1, x1 - dir * len), yy - 9, len, 18, 9, 1.5), { wash: col, washOp: 150 * k, ink: null });
    }
  }
  function around(x, y, sx, sy, draw) { push(); translate(x, y); scale(sx, sy); translate(-x, -y); draw(); pop(); }
  // Dust in the market's light (look.js motes(), with an opacity so it can fade in and out). Same in C.js.
  function dust(t, a = 1) {
    if (a <= .01) return;
    const col = mixCol(C.cream, C.upLt, .45);
    for (let i = 0; i < 22; i++) {
      boilSeed('mote' + i);
      const x = frac(hash(i) + t * (.004 + .01 * hash(i + 7))) * W, y = 150 + frac(hash(i + 3) - t * (.006 + .012 * hash(i + 9))) * 1000;
      const tw = .5 + .5 * Math.sin(t * (1 + hash(i + 5) * 2) + i), s = 2 + 2.5 * hash(i + 2);
      paint(ellPts(x, y, s, s, 8), { wash: col, washOp: (60 + 80 * tw) * a, ink: null });
    }
  }

  // ---- camera: out of the green, a slow push that leans after the marker, a lift at the snap, then in on the pie ----
  const LZ = Math.log;
  const dec = (t, t0, k) => t < t0 ? 0 : Math.exp(-(t - t0) * k);
  function camera(t, lt) {
    const rv = ease(seg(lt, 0, .45));
    const z0 = Math.exp(kf(t, [[5.72, LZ(1)], [tFin, LZ(1.045)], [tClr, LZ(1.05)], [8.4, LZ(.98)], [9.8, LZ(1.02)], [10.4, LZ(1.035)], [CUT.C, LZ(1.12)]], ease));
    const x0 = kf(t, [[5.72, 470], [tFin, 492], [tClr, 488], [8.4, 460], [11.6, 452], [CUT.C, 436]], ease);
    const y0 = kf(t, [[5.72, 640], [tFin, 628], [tClr, 628], [8.4, 626], [11.6, 620], [CUT.C, 606]], ease);
    const lift = t < tSnap ? 0 : easeOut(seg(t, tSnap, tSnap + .12)) * dec(t, tSnap + .12, 2.4);
    const z = z0 * Math.exp(lerp(LZ(6.5), 0, rv)) * (1 + .03 * clamp((t - tFlare + .05) / .05) * dec(t, tFlare, 5) + .035 * lift + .015 * dec(t, tTake + .1, 4) * seg(t, tTake, tTake + .1));
    cam(t, x0, lerp(420, y0, rv) - 18 * lift, z);
  }

  // ---- the race: zones, starting line, the marker's path, the clock ----
  function race(t, lt) {
    if (t > tClr + .42) return;
    const clr = ease(seg(t, tClr, tClr + .36)), rv = seg(lt, .06, .42), p = prog(t);
    const fl = t < tFlare - .05 ? 0 : clamp((t - tFlare + .05) / .05) * dec(t, tFlare, 2.6), won = seg(t, tFlare - .05, tFlare + .1);
    boilSeed('zones');
    paint(band(ZX0, ZTOP, ZX1, LINE, 30, 0), { wash: C.up, washOp: (lerp(255, 58, ease(rv)) + 100 * fl + 28 * won) * (1 - clr), ink: null });
    paint(band(ZX0, LINE, ZX1, ZBOT, 0, 30), { wash: C.down, washOp: (78 - 34 * won) * (1 - clr), ink: null });
    // the zones' light breathes; the Up zone flares when the marker finishes above
    const br = .5 + .5 * wob(t, .55);
    glow(470, 470, 420, '#2F8A55', ((.22 + .08 * br) * (1 + 1.2 * won) + 1.1 * fl) * (1 - clr) * seg(lt, .3, .55));
    glow(470, 810, 400, '#C0441C', (.3 + .08 * (1 - br)) * (1 - .6 * won) * (1 - clr) * seg(lt, .3, .55));
    // the starting line draws itself from the start dot; it brightens on "started"
    const ps = t < tStart ? 0 : Math.exp(-(t - tStart) * 3) * clamp((t - tStart) / .08);
    const lc = mixCol(mixCol(C.cream, C.creamDim, .25 - .25 * ps), '#1F2624', clr);
    boilSeed('line');
    dashLine(ZX0 + 24, ZX1 - 24, LINE, lerp(ZX0 + 24, ZX1, easeOut(seg(lt, .1, .45))), lc, 1.25 + .5 * ps);
    if (ps > .02) glow(mX(0), LINE, 90, '#E9E3D0', .7 * ps);
    if (onScreen(mX(0), LINE, 20)) paint(ellPts(mX(0), LINE, 11 + 4 * ps, 11 + 4 * ps, 12, .4), { wash: lc, ink: C.ink, sw: .6 });
    // the path so far (it rolls up into the marker as the chart clears)
    const q = p * clr;
    if (p - q > .004) { const P = []; for (let i = 0; i <= 44; i++) { const u = lerp(q, p, i / 44); P.push([mX(u), mY(u)]); } boilSeed('trail'); inkLine(P, 1.3, C.tape, 'ink', .3); }
    // the clock ring empties with the race
    const done = t < tFin ? 0 : dec(t, tFin, 3);
    if (onScreen(792, 230, 80)) ring15(792, 230, 58, 1 - p, { k: 1 - seg(t, tClr, tClr + .3), flash: done });
    // the marker: crouches, races, lands above the line and hops on the flare
    const hop = jump(t, tFlare, tFlare + .3, 34), an = t < tGo ? .14 * ease(seg(t, tGo - .16, tGo)) : 0;
    const slope = (dev(clamp(p + .02)) - dev(clamp(p - .02))) / (mX(.02) - mX(0)) / 2, racing = t > tGo && t < tFin;
    const mx = mX(p), my = mY(p) + hop.dy - (t > tFlare + .3 ? 5 * wob(t, .9) : 0);
    if (onScreen(mx, my, 60)) btc(mx, my, 36, { k: 1 - seg(t, tClr + .08, tClr + .26), rot: racing ? clamp(-slope * .5, -.35, .35) + .12 : .05 * wob(t, .7), sq: an + hop.sq * .8, glow: .5 + .5 * won * (1 - clr) });
    sparks(mx, my, t - tFlare, .5, 10, 150, C.upLt, 'flare', -Math.PI, Math.PI);
  }

  // ---- the dollar: halves in, snap, $1, the winner takes it, the pie ----
  function dollar(t) {
    const { x: X, y: Y, r: R } = COIN;
    if (t < tUpIn) return;
    // --- the two halves slide in, tremble, pull back and snap ---
    if (t < tSnap + .1) {
      const inU = seg(t, tUpIn, tUpIn + .45), inD = seg(t, tDnIn, tDnIn + .42), ten = ease(seg(t, 9.25, 9.72)), ant = ease(seg(t, 9.72, 9.8)), sn = easeIn(seg(t, 9.8, tSnap));
      const trem = 3.5 * seg(t, 9.3, 9.72) * (1 - ant), bob = 1 - seg(t, 9.6, 9.8), g = .22 + .08 * wob(t, .6) + .45 * seg(t, 9.3, 9.8);
      const xu = lerp(lerp(-280, 280, backOut(inU)) + 38 * ten - 16 * ant, X, sn) + trem * Math.sin(t * 95);
      const xd = lerp(lerp(1260, 640, backOut(inD)) - 38 * ten + 16 * ant, X, sn) + trem * Math.sin(t * 88 + 1);
      const yu = Y + 7 * wob(t, .8) * bob + trem * .6 * Math.cos(t * 83), yd = Y + 7 * wob(t, .8, .37) * bob + trem * .6 * Math.cos(t * 79);
      streaks(xu - R, yu, 1, Math.max(seg(t, tUpIn, tUpIn + .05) * (1 - seg(t, tUpIn + .12, tUpIn + .3)), sn * (1 - seg(t, tSnap, tSnap + .06))), C.upDk, 'u');
      if (t >= tDnIn) streaks(xd + R, yd, -1, Math.max(seg(t, tDnIn, tDnIn + .05) * (1 - seg(t, tDnIn + .12, tDnIn + .3)), sn * (1 - seg(t, tSnap, tSnap + .06))), C.downDk, 'd');
      half(xu, yu, R, 'up', { rot: lerp(-.5, 0, backOut(inU)) + .03 * wob(t, .7) * bob, glow: g });
      if (t >= tDnIn) half(xd, yd, R, 'down', { rot: lerp(.5, 0, backOut(inD)) + .03 * wob(t, .7, .5) * bob, glow: g });
    }
    // --- the snap: the halves turn into the gold dollar, which squashes, hops and settles; "$1" stamps on ---
    const fl = dec(t, tSnap, 4.5);
    if (t >= tSnap && t < tSplit + .12) {
      const kc = t < tSplit ? seg(t, tSnap, tSnap + .22) : 1 - seg(t, tSplit, tSplit + .1);
      const sq = .16 * spring(t, tSnap, 8, 26), hy = -14 * Math.sin(Math.PI * seg(t, tSnap, tSnap + .3));
      if (t >= tSplit) splitHalves(t);
      glow(X, Y, R * 2.3, '#FFD46A', .4 + .1 * wob(t, .5) + .9 * fl);
      around(X, Y + hy, 1 + sq, 1 - sq, () => coin(X, Y + hy, R, { k: kc, label: null }));
      if (t > tLbl) txt('$1', X, Y + hy + R * .05, R * .82, C.goldDk, { ink: false, pop: (t - tLbl) * 5, alpha: 1 - seg(t, tSplit - .06, tSplit + .03) });
      sparks(X, Y, t - tSnap, .55, 12, 300, C.goldLt, 'snap');
    }
    if (t >= tSplit + .12) splitHalves(t);
  }
  // "And the winner takes it": the halves spring apart; Up hops, then swells back into the whole coin; Down is
  // knocked aside and crumbles. The re-formed coin becomes a pie: a green wedge sweeps to 62%, tagged 62¢ → 62%.
  function splitHalves(t) {
    const { x: X, y: Y, r: R } = COIN;
    const d = 55 * backOut(seg(t, tSplit, tSplit + .2)), crack = dec(t, tSplit, 7);
    if (crack > .02) glow(X, Y, R * 1.6, '#FFF1C8', .9 * crack);
    // the loser (drawn behind the coin): droops on "winner", is shoved aside on "takes", crumbles to ash and is gone
    const cr = seg(t, tCrumble, tCrumble + .55), gone = ease(seg(t, tCrumble + .3, tCrumble + .62));
    if (gone < 1) {
      const kn = easeOut(seg(t, tTake, tTake + .2)), droop = ease(seg(t, tWin, tWin + .2)), shiver = 3 * droop * (1 - seg(t, tCrumble + .1, tCrumble + .3));
      const xd = X + d + 115 * kn + shiver * Math.sin(t * 70), yd = Y + 8 * droop + 30 * kn;
      around(xd + R * .4, yd + R, 1 - gone * .7, 1 - gone, () => half(xd, yd, R, 'down', { rot: .1 * droop + .45 * kn, crumble: cr, glow: .15 * (1 - droop) }));
    }
    puff(X + 55 + 115 + R * .45, Y + 40 + R * .2, t - tCrumble, .7);
    // the coin re-forms behind the winner
    const kc = seg(t, tTake, tTake + .24);
    if (kc > 0) {
      const tf = seg(t, tTag - .05, tTag + .1) * dec(t, tTag + .1, 2.5) + seg(t, tFlip - .02, tFlip + .06) * dec(t, tFlip + .06, 2.2);
      const Yb = Y + bobY(t);   // the re-formed coin floats (C.js continues the same bob)
      glow(X, Yb, R * 2.4, '#FFD46A', .45 + .1 * wob(t, .5) + .8 * dec(t, tTake, 3) * kc);
      coin(X, Yb, R, { k: kc, label: null });
      const wf = .62 * easeOut(seg(t, tSweep, tTag)) + .025 * Math.sin(Math.PI * seg(t, tTag - .06, tTag + .3));
      if (wf > .004) wedge(X, Yb, R * .74, wf, t < tTag + .05 ? seg(t, tSweep, tSweep + .05) * (1 - seg(t, tTag, tTag + .06)) : 0, .3 + .1 * wob(t, .45) + .6 * tf);
    }
    // the winner: pops out left, hops on "winner", slides home onto the coin and sinks into it
    const hop = jump(t, tWin, tWin + .26, 30), home = ease(seg(t, tTake, tTake + .18)), melt = ease(seg(t, tTake + .2, tTake + .46));
    if (melt < 1) {
      const xu = lerp(X - d, X, home), yu = Y + hop.dy;
      around(X, Y, 1 - melt, 1 - melt, () => around(xu - R * .4, yu + R, 1 + hop.sq * .7, 1 - hop.sq, () => half(xu, yu, R, 'up', { glow: .25 + .7 * seg(t, tWin - .05, tWin + .1) * (1 - melt) })));
    }
    // the tag: "62¢" lands with the wedge, becomes "62%", and leaves before the cut
    const tk = t < tFlip - .06 ? seg(t, tTag - .14, tTag) : t < tFlip - .02 ? lerp(1, .04, easeIn(seg(t, tFlip - .075, tFlip - .02))) : lerp(.04, 1, seg(t, tFlip - .02, tFlip + .12));
    const k = Math.min(tk, 1 - seg(t, tTagOut, tTagOut + .12)), tx = X - R * 1.02, ty = Y + bobY(t) - R * .62 + 3 * wob(t, .6);
    if (k > .01) {
      const lf = dec(t, tTag, 3) * seg(t, tTag - .05, tTag) + dec(t, tFlip, 2.5) * seg(t, tFlip - .02, tFlip + .02);
      if (lf > .02) glow(tx, ty, 150, '#6BE08E', .8 * lf);
      pill(t < tFlip - .02 ? '62¢' : '62%', tx, ty, 78, { k, bg: C.upDk, key: 'tag62', sw: 1 });
    }
  }
  function wedge(x, y, r, f, edge, g) {   // the Up share of the dollar, swept counter-clockwise from 12 o'clock
    const n = Math.max(3, Math.ceil(40 * f)), P = [[x, y]], a1 = -Math.PI / 2 - TAU * f;
    for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 - TAU * f * i / n; P.push([x + Math.cos(a) * r, y + Math.sin(a) * r]); }
    glow(x - r * .35, y + r * .1, r * 1.9, '#6BE08E', g);
    boilSeed('wedge');
    paint(P, { wash: C.up, ink: C.ink, sw: .8 });
    if (edge > .02) inkLine([[x, y], [x + Math.cos(a1) * r, y + Math.sin(a1) * r]], 1.4, C.upLt, 'ink', 0);
  }

  function shotB(t, lt, dur) {
    room(t, { plate: 'stage', bloom: 0 });
    camera(t, lt);
    dust(t, seg(lt, .4, .9));
    race(t, lt);
    dollar(t);
    camEnd();
  }
  shots([[CUT.B, shotB]]);
})();
