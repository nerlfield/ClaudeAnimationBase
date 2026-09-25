// C.js: TWO ORDER BOOKS (14.555 → 18.683). See STORYBOARD.md, shot C.
//   In (continuous from B): B's pie-coin cracks open into its two halves on the cut's beat; they squeeze, then
//   whip apart (14.78, on the half-beat), spinning a quarter turn and flattening into the two book headers, which
//   land on the beat (15.07) as the camera tilts down to the books. The ladders unroll on "order book", the bids
//   slide in solid from the left on "Bids", the asks dim and hollow from the right on "asks", and the gap between
//   them glows (with a small bracket ping) on "spread". No labels: bar length is depth.
//   Out (C→D contract): the stage plate, cam(t, ...BOOK.cam), books(t, { bidK: 1, askK: 1, askOp: 1, spread: .6 }),
//   nothing else. Every extra (dust, header light, bracket) has faded out by 18.45.
(() => {
  const COIN = { x: 460, y: 591, r: 190 };            // B.js's coin, where this shot starts
  const B_CAM = [436, 606, 1.12];                      // B.js's camera at the cut
  const beatAt = n => OFF + n * BEAT;
  const tCrack = CUT.C + .045, tWhip = beatAt(28.5) - .03 /* 14.78 */, tLand = beatAt(29) /* 15.07 */;
  const tRows = wt('C1', 'order') - .32, tBids = wt('C2', 'Bids') - .17, tAsks = wt('C2', 'asks') - .17, tSpread = wt('C2', 'spread') - .02;
  const tClean = 18.45;                                 // from here on, only the contract's frame (plus its drift)
  const HW = BOOK.U[2] - 32, HH = 70;                   // a book header's size (see book() in sets.js)
  const head = s => [BOOK[s][0] + BOOK[s][2] / 2, BOOK[s][1] + 51];

  const dec = (t, t0, k) => t < t0 ? 0 : Math.exp(-(t - t0) * k);
  const inout = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  function around(x, y, sx, sy, draw) { push(); translate(x, y); scale(sx, sy); translate(-x, -y); draw(); pop(); }
  // Dust in the market's light: the same motes as B.js, fading out before the seam.
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
  function streaks(x, y, dir, k, col, key) {   // painted smears trailing a fast-moving half (dir: +1 moving right)
    if (k <= .03) return;
    boilSeed('streak' + key);
    for (let i = 0; i < 3; i++) {
      const yy = y + (i - 1) * 46 + (hash(i + key.length * 3) - .5) * 16, len = (170 + 120 * hash(i + 11)) * k, x1 = x - dir * (10 + 30 * hash(i + 5));
      paint(rrPts(Math.min(x1, x1 - dir * len), yy - 8, len, 16, 8, 1.5), { wash: col, washOp: 110 * k, ink: null });
    }
  }
  function sparks(x, y, age, life, n, rad, col, key, a0 = 0, spread = TAU) {
    if (age < 0 || age > life) return; const a = age / life;
    boilSeed('sparks' + key);
    for (let i = 0; i < n; i++) {
      const ang = a0 + (i + .5) / n * spread + (hash(i * 7 + key.length) - .5) * .35, d = rad * (.3 + .7 * easeOut(a)) * (.75 + .5 * hash(i * 3 + 1));
      paint(starPts(x + Math.cos(ang) * d, y + Math.sin(ang) * d, 15 * (1 - a) + 2, .3, 4, ang), { wash: col, washOp: 255 * (1 - a * a), ink: null });
    }
  }
  function wedge(x, y, r, f, g) {   // B's Up share of the dollar, still on the coin as it cracks
    const n = Math.max(3, Math.ceil(40 * f)), P = [[x, y]];
    for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 - TAU * f * i / n; P.push([x + Math.cos(a) * r, y + Math.sin(a) * r]); }
    glow(x - r * .35, y + r * .1, r * 1.9, '#6BE08E', g);
    boilSeed('wedge');
    paint(P, { wash: C.up, ink: C.ink, sw: .8 });
  }

  // ---- camera: hold on the coin, whip-tilt down to the books as the halves fly, a slow breath, then exactly BOOK.cam ----
  function camera(t) {
    if (t >= tClean) return cam(t, ...BOOK.cam);
    const w = inout(seg(t, tWhip - .02, tWhip + .5)), b = seg(t, tLand + .25, 18.35), hump = .5 - .5 * Math.cos(TAU * b);
    const x = lerp(lerp(B_CAM[0], 440, seg(t, CUT.C, tWhip)), BOOK.cam[0], w);
    const y = lerp(lerp(B_CAM[1], 602, seg(t, CUT.C, tWhip)), BOOK.cam[1], w) + 16 * hump;
    const z = Math.exp(lerp(Math.log(lerp(B_CAM[2], 1.13, seg(t, CUT.C, tWhip))), 0, w)) * (1 + .025 * hump);
    cam(t, x, y, z);
  }

  // ---- the coin cracks into its halves, which whip apart and flatten into the headers ----
  function split(t) {
    const { x: X, r: R } = COIN, Y = COIN.y + 4 * wob(t, .35) * (1 - seg(t, tWhip, tLand));   // B's coin bob, until the whip
    const kc = 1 - seg(t, tCrack, tCrack + .1);
    // the halves: first the whole coin under the cracking gold, then a squeeze (anticipation) and the whip
    const sq = ease(seg(t, tCrack + .05, tWhip)) * (1 - seg(t, tWhip, tWhip + .05)), trem = 2.5 * sq;
    const s = seg(t, tWhip, tLand), gone = ease(seg(t, tLand - .03, tLand + .07));
    if (gone < 1) {
      const H2 = ['up', 'down'].map(side => {
        const up = side === 'up', dir = up ? -1 : 1, [hx, hy] = head(up ? 'U' : 'D'), m = ease(seg(s, .25, 1));
        const sy = lerp(1, HH / R, m), sx = lerp(1, HW / (2 * R), m) * (1 + .22 * Math.sin(Math.PI * s));
        const arc = 70 * Math.sin(Math.PI * s), px = lerp(X, hx, easeOut(s)) + trem * Math.sin(t * (up ? 91 : 84)), py = lerp(Y, hy + dir * R * sy / 2, easeOut(s)) - arc;
        return { side, up, dir, sx, sy, px, py, cy: lerp(Y, hy, easeOut(s)) - arc, rot: -Math.PI / 2 * ease(seg(s, 0, .75)) };
      });
      // the smears go behind both halves (each trails back through the gap they leave)
      for (const h of H2) streaks(h.px, h.cy, h.dir, Math.sin(Math.PI * s), h.up ? C.upLt : C.downLt, h.side);
      const ex = (1 - .09 * sq) * (1 - gone), ey = (1 + .07 * sq) * (1 - gone);
      for (const h of H2) around(s > 0 ? h.px : X, s > 0 ? h.py : Y, h.sx * ex, h.sy * ey, () => half(h.px, h.py, R, h.side, { rot: h.rot, glow: .3 + .3 * sq + .4 * Math.sin(Math.PI * s) }));
    }
    // the gold (with B's 62% wedge) bursts off the top of the halves
    if (kc > 0) {
      glow(X, Y, R * 2.4, '#FFD46A', (.45 + .1 * wob(t, .5)) * kc);
      coin(X, Y, R, { k: kc, label: null });
      wedge(X, Y, R * .74 * backOut(kc), .62, (.3 + .1 * wob(t, .45)) * kc);
    }
    const cf = dec(t, tCrack, 6) * seg(t, tCrack - .02, tCrack + .02);
    if (cf > .02) glow(X, Y, R * 1.7, '#FFF1C8', .9 * cf);
    sparks(X, Y, t - tWhip, .45, 10, 230, C.goldLt, 'whip');
  }

  function shotC(t, lt, dur) {
    room(t, { plate: 'stage', bloom: 0 });
    camera(t);
    if (t >= tClean) { books(t, { bidK: 1, askK: 1, askOp: 1, spread: .6 }); camEnd(); return; }
    const out = 1 - seg(t, 17.95, tClean - .02);   // extras fade before the seam
    dust(t, out);
    // the books: each pops out of its landing header, unrolls, fills bids then asks; D lags U a hair (no twinning)
    const sp = t < tSpread - .2 ? 0 : kf(t, [[tSpread - .2, 0], [tSpread, 1.45], [tSpread + .55, .6]], ease);
    const R = {};
    for (const [s, lag] of [['U', 0], ['D', .06]]) {
      const [hx, hy] = head(s), side = s === 'U' ? 'up' : 'down';
      const bo = backOut(seg(t, tLand - .05 + lag * .3, tLand + .2 + lag * .3));
      if (bo <= .01) continue;
      const st = { header: 1, rows: seg(t, tRows + lag, tRows + .6 + lag), bidK: seg(t, tBids + lag, tBids + .55 + lag),
        askK: seg(t, tAsks + lag, tAsks + .55 + lag), askOp: lerp(.45, 1, seg(t, tAsks + lag, tAsks + .5 + lag)), spread: sp };
      const lit = dec(t, tLand, 3) * seg(t, tLand - .04, tLand);
      glow(hx, hy, 230, side === 'up' ? '#6BE08E' : '#FF8A5C', (.9 * lit + .16 + .06 * wob(t, .5, s === 'U' ? 0 : .4)) * out);
      around(hx, hy, lerp(.85, 1, bo), lerp(.45, 1, bo), () => { R[s] = book(...BOOK[s], side, st); });
    }
    // "a spread between": the gap pings with a small bracket, then settles into the contract's glow
    const pa = seg(t, tSpread - .12, tSpread) * (1 - seg(t, tSpread + .4, tClean - .05));
    if (pa > .01) for (const s of ['U', 'D']) {
      const r = R[s]; if (!r) continue;
      const cx = head(s)[0], y0 = r.askY(4) + r.rh / 2 - 6, y1 = r.bidY(0) - r.rh / 2 + 6, pop = backOut(seg(t, tSpread - .12, tSpread + .08));
      const col = mixCol(C.panel, C.cream, pa), hw = 34 * pop;
      glow(cx, r.spreadY, 170, '#E9E3D0', .3 * pa * (1 + dec(t, tSpread, 3)));
      boilSeed('bracket' + s);
      inkLine([[cx - hw, y0 + 2], [cx + hw, y0 + 2]], 1.4, col, 'ink', 0);
      inkLine([[cx - hw, y1 - 2], [cx + hw, y1 - 2]], 1.4, col, 'ink', 0);
      inkLine([[cx, y0 + 2], [cx, y1 - 2]], 1.2, col, 'ink', 0);
    }
    if (t < tLand + .12) split(t);
    for (const s of ['U', 'D']) { const [hx, hy] = head(s), lit = dec(t, tLand, 4) * seg(t, tLand - .04, tLand); if (lit > .02) glow(hx, hy, 190, s === 'U' ? '#6BE08E' : '#FF8A5C', .7 * lit); }
    for (const s of ['U', 'D']) { const [hx, hy] = head(s); sparks(hx, hy, t - tLand, .45, 8, 200, s === 'U' ? C.upLt : C.downLt, 'land' + s); }
    camEnd();
  }
  shots([[CUT.C, shotC]]);
})();
