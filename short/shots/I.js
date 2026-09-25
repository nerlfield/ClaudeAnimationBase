// I.js: RISK, THEN LOOP (58.923 → 65.6). See STORYBOARD.md, shot I.
//   Continuous from H, in the same world (the ticker screen seen up close, H.js's window.HI kit). You sit in the ash with
//   your last two coins. On "fees" a fee jaw chomps one and carries it off; on "half-second delay" an hourglass pill
//   ("0.5 s") flips and runs; on "whole stake" the last coin in your hands cracks and crumbles to dust, held.
//   On "the close" the blue average's final point locks; the old chart crumbles to ash while the camera pulls back out
//   of the screen to the desk, and the locked point slides left, stretching into a new dashed line: the next round's
//   Price to Beat. The market card flips to a fresh round (Up 50¢, Down 50¢, 15:00), the ticker's tag flips back to "?",
//   you sink behind the desk, and the camera settles on the hook's framing: the last frame is A's frame 0 (HOOK0).
(() => {
  const { HX, HY, HS, hd, X_END, PTB, tx, price, TW0, T, SIT, camDesk } = HI;
  // times, on or just before their words
  const E = {
    coins: CUT.I + .01, jawIn: wt('I1', 'Add') + .05, chomp: wt('I1', 'fees') - .02, jawOut: wt('I1', 'fees') + .08,
    glass: wt('I1', 'half-second') - .06, glassOut: wte('I1', 'delay') + .15, shiver: wt('I1', 'lose'), crack: wt('I1', 'your') + .02,
    crumble: 61.5,                                            // beat 119, on "whole"
    look: wt('I2', 'Then') + .05, lock: wt('I2', 'close') - .02, gone: wt('I2', 'close') + .07,
    pull: 63.0, slide: 63.02, slideEnd: 63.45, line: 63.3, lineEnd: 63.62, land: 63.62,
    flip: 63.56,                                              // beat 123, the new round
    sink: 64.0, sunk: 64.42, hookIn: wt('I2', 'Price') + .08, lite: 64.5, dashOut: 65.0,
  };
  const END = CUT.END;
  // your acting in I (added to H's keys: one continuous track across the cut)
  HI.act.push(
    [E.chomp + .05, 'surprised'], [E.jawOut + .45, 'sad'], [E.glass + .1, 'nervous', { lookX: -.75, lookY: -.85 }],
    [E.crumble + .05, 'cry'], [E.look, 'sad', { lookX: .8, lookY: .1 }], [E.land - .05, 'sad', { lookX: -.6, lookY: -.3 }],
  );

  // ---------- where an arm tip is (so props can be handed around in world space) ----------
  // Mirrors clawd()'s arm transform for the front view. which: 'L' | 'R'.
  function armTip(x, y, u, o, which) {
    const L = which === 'L', dir = L ? -1 : 1, px = L ? -4.9 : 4.9, a = L ? (o.aL ?? .2) : (o.aR ?? .2);
    const sq = (o.sq || 0) + (o.take || 0), sxk = (o.sx ?? 1) * (1 + sq * .6), syk = (o.sy ?? 1) * (1 - sq);
    const rx = (px + dir * .55 * clamp((Math.abs(a) - .7) / .9)) * u + dir * 2.2 * u * Math.cos(a), ry = -4.5 * u - 2.2 * u * Math.sin(a);
    const c = Math.cos(o.rot || 0), s = Math.sin(o.rot || 0), X = rx * sxk, Y = ry * syk;
    return [x + (o.dx || 0) * u + X * c - Y * s, y + (o.dy || 0) * u + X * s + Y * c];
  }

  // ---------- props ----------
  // The fee jaw: a little chomper, hinge at (x, y), mouth facing left. open 0..1.
  function jaw(x, y, s, open, t) {
    const a = .6 * open;
    boilSeed('feejaw');
    for (const sg of [1, -1]) {                                // lower jaw first, the upper one over it
      push(); translate(x, y); rotate(-sg * a);
      paint([[-s * 1.1, 0], [-s * .95, sg * s * .5], [-s * .25, sg * s * .72], [s * .35, sg * s * .55], [s * .45, 0]], { wash: sg < 0 ? '#5A4B78' : '#4B3F63', ink: C.ink, sw: 1.3, curv: .45 });
      for (let i = 0; i < 5; i++) { const x0 = -s * 1.02 + i * s * .27; paint([[x0, 0], [x0 + s * .135, -sg * s * .24], [x0 + s * .27, 0]], { wash: C.cream, ink: C.ink, sw: .8 }); }
      if (sg < 0) { paint(ellPts(-s * .3, -s * .38, s * .16, s * .19, 12), { wash: C.cream, ink: C.ink, sw: .9 }); paint(ellPts(-s * .36, -s * .36, s * .07, s * .09, 8), { wash: C.ink, ink: null }); }
      pop();
    }
  }
  // An hourglass, flipped by `rot`, with sand k (0 = all on top, 1 = all run through).
  function hourglass(x, y, s, rot, k) {
    boilSeed('hourglass');
    push(); translate(x, y); rotate(rot);
    paint(rrPts(-s * .62, -s * 1.08, s * 1.24, s * .2, s * .06), { wash: '#8C6A45', ink: C.ink, sw: .9 });
    paint(rrPts(-s * .62, s * .88, s * 1.24, s * .2, s * .06), { wash: '#8C6A45', ink: C.ink, sw: .9 });
    paint([[-s * .5, -s * .88], [s * .5, -s * .88], [s * .08, 0], [s * .5, s * .88], [-s * .5, s * .88], [-s * .08, 0]], { wash: '#3A4150', ink: C.ink, sw: .9 });
    const top = 1 - k, bot = k, sand = '#E7B447';
    if (top > .02) paint([[-s * .42 * top, -s * .72 * top], [s * .42 * top, -s * .72 * top], [s * .06, -s * .05], [-s * .06, -s * .05]], { wash: sand, ink: null });
    if (bot > .02) paint([[-s * .44, s * .86], [s * .44, s * .86], [s * .4 * (1 - bot * .5), s * .86 - s * .7 * bot], [-s * .4 * (1 - bot * .5), s * .86 - s * .7 * bot]], { wash: sand, ink: null });
    if (k > .02 && k < .98) inkLine([[0, -s * .05], [0, s * .85 - s * .7 * bot]], .8, sand, 'inkfine', 0);
    pop();
  }
  // The last coin: it shivers, cracks, then breaks into shards that fall and turn to dust. p = seconds since the break.
  function crumbleCoin(x, y, r, t) {
    const p = t - E.crumble;
    if (p < 0) {
      const sh = seg(t, E.shiver, E.crumble), dx = Math.sin(t * 70) * 3 * sh;
      coin(x + dx, y, r, { label: null, key: 'last' });
      const cr = seg(t, E.crack, E.crumble);
      if (cr > 0) { boilSeed('cracks'); inkLine([[x + dx - r * .1, y - r * .9], [x + dx + r * .15, y - r * .2 * cr], [x + dx - r * .2 * cr, y + r * .5 * cr]], 1, '#5A3F12', 'inkfine', .2); if (cr > .5) inkLine([[x + dx + r * .8, y - r * .3], [x + dx + r * .1, y + r * .1]], .9, '#5A3F12', 'inkfine', .2); }
      return;
    }
    for (let i = 0; i < 6; i++) {   // six wedges fall, spin and grey out
      const a0 = i / 6 * TAU + .3, a1 = a0 + TAU / 6, g = clamp(p / .55), vx = Math.cos(a0 + .5) * (40 + 30 * hash(i)) * p, vy = 420 * p * p - 60 * p;
      const cx = x + vx, cy = y + vy, rot = (hash(i + 3) - .5) * 6 * p, col = mixCol(C.gold, '#6E6A66', g), sc = 1 - .5 * g;
      if (p > .75) continue;
      const P = [[0, 0]]; for (let k = 0; k <= 3; k++) { const a = lerp(a0, a1, k / 3); P.push([Math.cos(a) * r * sc, Math.sin(a) * r * sc]); }
      boilSeed('shard' + i);
      push(); translate(cx, cy); rotate(rot); paint(P, { wash: col, washOp: 255 * (1 - seg(p, .45, .75)), ink: g < .6 ? C.goldDk : null, sw: .8 }); pop();
    }
    for (let i = 0; i < 14; i++) {  // the dust
      const q = clamp((p - .02 * i) / .9); if (q <= 0 || q >= 1) continue;
      const ang = hash(i + 20) * TAU, d = (20 + 50 * hash(i + 21)) * easeOut(q);
      boilSeed('dust' + i);
      paint(ellPts(x + Math.cos(ang) * d, y + Math.sin(ang) * d * .6 + 80 * q * q, 6 + 12 * q, 5 + 9 * q, 8, 1), { wash: '#8E8983', washOp: 150 * (1 - q), ink: null });
    }
  }

  // ---------- the camera ----------
  const CAMK = [   // I-tight, in H space
    [CUT.I, 660, 560, 1.06], [E.glass, 610, 520, 1.12], [E.crumble + .3, 600, 535, 1.18], [E.look, 610, 540, 1.16],
    [E.lock - .05, 735, 610, 1.14], [E.pull, 745, 612, 1.15],
  ];
  const tight = t => [kf(t, CAMK.map(k => [k[0], k[1]])), kf(t, CAMK.map(k => [k[0], k[2]])), Math.exp(kf(t, CAMK.map(k => [k[0], Math.log(k[3])])))];
  const ANCH = hd(X_END, TW0);                                // the pull-back is anchored on the locked point
  const WIDE = [470, 640, 1];
  const DESKK = [[E.land, ...WIDE], [E.sink + .1, 462, 636, 1.02], [E.hookIn + .62, ...HOOK0.cam]];
  // desk-space camera at t: [x, y, zoom] (the stage-centre world point) and the loop-drift blend
  function camAt(t) {
    if (t < E.pull) { const [x, y, z] = tight(t), [a, b] = hd(x, y); return [a, b, z * HS]; }
    if (t < E.land) {
      const [x0, y0, z0] = tight(E.pull), zd0 = z0 * HS, [cx0, cy0] = hd(x0, y0);
      const s0 = [STAGE.x + (ANCH[0] - cx0) * zd0, STAGE.y + (ANCH[1] - cy0) * zd0], s1 = [STAGE.x + ANCH[0] - WIDE[0], STAGE.y + ANCH[1] - WIDE[1]];
      const k = seg(t, E.pull, E.land), kz = ease(Math.pow(k, .8)), ka = ease(k);
      const z = Math.exp(lerp(Math.log(zd0), Math.log(WIDE[2]), kz)), s = [lerp(s0[0], s1[0], ka), lerp(s0[1], s1[1], ka)];
      return [ANCH[0] - (s[0] - STAGE.x) / z, ANCH[1] - (s[1] - STAGE.y) / z, z];
    }
    return [kf(t, DESKK.map(k => [k[0], k[1]])), kf(t, DESKK.map(k => [k[0], k[2]])), Math.exp(kf(t, DESKK.map(k => [k[0], Math.log(k[3])])))];
  }
  const loopK = t => ease(seg(t, 63.1, 63.9));

  // ---------- your pose in I ----------
  // Sitting (H's sitPose), the coins come up in both hands, the jaw's recoil, the slump after the crumble, a crouch
  // before the hop out of the screen; then the hop (screen-locked: you're between us and the screen) and the desk.
  const coinsK = t => backOut(seg(t, E.coins, E.coins + .14));
  const pre = t => Math.sin(Math.PI * seg(t, E.pull - .1, E.pull + .08));
  function sitArms(t, m) {
    const s = HI.sitPose(t, m), up = coinsK(t), hold = .38 + .06 * Math.sin(t * 2.3);
    const recoil = t > E.chomp ? Math.exp(-(t - E.chomp) * 5) * Math.sin((t - E.chomp) * 18) * .5 : 0;
    const aR = t < E.chomp ? lerp(s.aR, hold, up) : lerp(hold + .1 + recoil, -.7, ease(seg(t, E.jawOut + .1, E.jawOut + .6)));
    const aL = lerp(lerp(s.aL, hold + .05, up), -.55 + .25 * Math.sin(t * 5), ease(seg(t, E.crumble + .05, E.crumble + .45)));
    return { ...s, aL, aR, sq: s.sq + .2 * pre(t) };
  }
  const youI = t => { const m = HI.mood(t); return { ...m, view: 'front', ...sitArms(t, m) }; };
  const deskArms = m => [m.aL * .4 - .3, m.aR * .4 - .3];
  const GRAB = armTip(SIT.x, SIT.y, 30, youI(E.chomp), 'R');   // where the jaw bites
  // the camera exactly as camBegin gets it (drift included), for handing you from H space to the screen
  function camParams(t) {
    const c = camAt(t), kl = loopK(t), d = (m, td) => [6 * m * wob(td, .11), 5 * m * wob(td, .09, .4), .004 * m * wob(td, .07, .2)];
    const a = d(1 / HS, t), b = d(1, t - END), D = a.map((v, i) => lerp(v, b[i], kl));
    return { cx: c[0] + (W / 2 - STAGE.x) / c[2] + D[0], cy: c[1] + (H / 2 - STAGE.y) / c[2] + D[1], zoom: c[2] * (1 + D[2]), rot: 0 };
  }
  // the hop: screen position of your feet and your screen size, from where you sat to the desk
  function hop(t) {
    const c0 = camParams(E.pull), f0 = hd(SIT.x, SIT.y), s0 = toScreen(f0[0], f0[1], c0), u0 = 30 * c0.zoom / HS;
    const s1 = toScreen(DESK.youX, DESK.top), u1 = 21 * CAM.zoom, k = ease(seg(t, E.pull, E.land)), air = Math.sin(Math.PI * k);
    return { s: [lerp(s0[0], s1[0], k), lerp(s0[1], s1[1], k) - 150 * air], u: lerp(u0, u1, k), air, k };
  }

  function shotI(t, lt, dur) {
    const c = camAt(t), kl = loopK(t);
    camDesk(t, c[0], c[1], c[2], kl);
    const V = [(CAM.cx - W / 2 / CAM.zoom - HX) * HS, (CAM.cy - H / 2 / CAM.zoom - HY) * HS, (CAM.cx + W / 2 / CAM.zoom - HX) * HS, (CAM.cy + H / 2 / CAM.zoom - HY) * HS];
    // the set: the resolved round (Down won) until the card flips to a fresh one
    const fresh = t >= E.flip, flipK = t < E.flip ? 1 - easeIn(seg(t, E.flip - .14, E.flip)) : backOut(seg(t, E.flip, E.flip + .17));
    const cardSt = fresh ? { up: 50, clock: Math.min(900, 899 + (END - t)), hi: 'up', pulse: .12 + .1 * Math.sin((t - END) * 34), example: true }
                         : { up: 0, clock: 0, hi: 'down', pulse: .25, example: true };
    const set = { tl: t - END, card: cardSt, cardFlip: flipK, upGlow: ease(seg(t, E.flip, E.flip + .25)), tickGlow: .6,
      fn: HOOK0.btc, lo: HOOK0.lo, hi: HOOK0.hi, named: 1 - ease(seg(t, E.flip + .06, E.flip + .34)), lineK: ease(seg(t, E.line, E.lineEnd)) };
    if (t >= E.lite) desk(t - END, { card: cardSt, upGlow: 1, tickGlow: .6, fn: HOOK0.btc, lo: HOOK0.lo, hi: HOOK0.hi, hide: 1, named: 0 });
    else HI.deskLite(set);

    // ---- the old chart, until it crumbles at the close ----
    const gone = ease(seg(t, E.gone, E.gone + .28)), slide = ease(seg(t, E.slide, E.slideEnd));
    const dotX = lerp(X_END, HI.X_LEFT, slide), dotA = 1 - seg(t, E.slideEnd - .06, E.slideEnd + .06);
    HI.inH(() => {
      if (gone < 1) {
        const st = HI.chart(t, V, { fade: gone });
        if (gone < .5) HI.average(t, 0, { a: 1 - gone });
        HI.candle(t, { sp: 1, bodyTop: price(0), fade: gone });
        HI.smoke(t, X_END + 30, 250, T.burn + .1, 9, 2, .8 * (1 - gone));
      }
      if (gone > 0) {   // the old line and its average break into ash that drifts up and away
        for (let i = 0; i < 36; i++) {
          const s = -118 + 117 * i / 35, x = tx(s), y = i % 2 ? price(s) : HI.twap(Math.max(-60, s)), q = clamp(gone * 1.3 - hash(i) * .3);
          if (q <= 0 || q >= 1 || (x < V[0] - 60 || x > V[2] + 60)) continue;
          boilSeed('cash' + i);
          paint(ellPts(x + 20 * Math.sin(i + q * 3), y - 140 * q * (.5 + hash(i + 2)), 5 + 4 * hash(i + 4), 4, 7, .8, i), { wash: i % 2 ? '#9A958C' : '#7C84B8', washOp: 220 * (1 - q), ink: null });
        }
      }
      // the locked point: a ring clamps on at the close, then it slides left
      if (t > E.lock - .14 && dotA > 0) {
        const ring = t < E.lock ? lerp(64, 22, easeIn(seg(t, E.lock - .14, E.lock))) : 18 + 5 * backOut(seg(t, E.lock, E.lock + .2)) - 5 * seg(t, E.lock, E.lock + .2);
        const fl = t > E.lock ? Math.exp(-(t - E.lock) * 5) : 0;
        glow(dotX, TW0, 90 + 200 * fl, '#8C9BFF', (.6 + .6 * fl) * dotA);
        boilSeed('lock');
        paint(ellPts(dotX, TW0, 12 * dotA, 12 * dotA, 16), { wash: t > E.lock ? '#DDE2FF' : '#AEB8FF', ink: C.twapDk, sw: 1.2 });
        if (t > E.lock - .14) inkLine(ellPts(dotX, TW0, ring * dotA, ring * dotA, 20).concat([ellPts(dotX, TW0, ring * dotA, ring * dotA, 20)[0]]), 1.6, C.cream, 'ink', .8);
      }
      // you, in the ash (until the pull-back takes over)
      if (t < E.pull) {
        const o = youI(t);
        // the fee jaw goes behind your coin hand, the coins in front of your arms
        const tipR = armTip(SIT.x, SIT.y, 30, o, 'R'), tipL = armTip(SIT.x, SIT.y, 30, o, 'L');
        HI.drawYou({ x: SIT.x, y: SIT.y, o });
        HI.smoke(t, SIT.x - 40, SIT.y - 190, T.burn + .2, 3, 3, 1 - seg(t, 60.5, 62));
        const ck = coinsK(t);
        // right coin: until the jaw takes it
        const grab = [GRAB[0] + 40, GRAB[1] - 4];
        const jx = t < E.chomp - .1 ? lerp(1400, grab[0] + 55, easeOut(seg(t, E.jawIn, E.chomp - .1))) : lerp(grab[0] + 55, grab[0], easeIn(seg(t, E.chomp - .1, E.chomp)));
        const away = t < E.jawOut ? grab : arcPt(grab, [1500, grab[1] - 60], 80, easeIn(seg(t, E.jawOut, E.jawOut + .5)));
        if (t < E.chomp) { if (ck > .02) coin(tipR[0] + 6, tipR[1] - 8, 30 * ck, { label: null, key: 'r' }); }
        else if (t < E.jawOut + .5) coin(away[0] - 34, away[1] - 4, 30, { label: null, key: 'r' });
        if (t > E.jawIn && t < E.jawOut + .5) {
          const open = t < E.chomp - .1 ? 1 : 1 - easeIn(seg(t, E.chomp - .1, E.chomp)), [x, y] = t < E.chomp ? [jx, grab[1]] : away;
          const bite = t > E.chomp ? Math.sin((t - E.chomp) * 40) * Math.exp(-(t - E.chomp) * 9) * .15 : 0;
          jaw(x, y - 4, 64, clamp(open + bite), t);
          if (t > E.chomp && t < E.chomp + .5) for (let i = 0; i < 4; i++) {   // gold crumbs
            const p = t - E.chomp; boilSeed('crumb' + i);
            paint(ellPts(grab[0] - 20 + 14 * i, grab[1] + 10 + 400 * p * p + 30 * p * hash(i), 5, 4, 6), { wash: C.gold, washOp: 255 * (1 - p * 2), ink: null });
          }
        }
        // left coin: the last one
        if (t < E.crumble + 1 && ck > .02) crumbleCoin(tipL[0] - 6, tipL[1] - 8, 30 * ck, t);
      }
    });
    // the half-second delay: an hourglass pill
    const gk = seg(t, E.glass, E.glass + .16) * (1 - seg(t, E.glassOut - .16, E.glassOut));
    if (gk > 0) {
      const px = 420, py = 300;
      HI.hPill('0.5 s', px + 20, py, 50, { k: gk, w: 240, dx: 26, bg: C.panelHi, key: 'delay' });
      HI.inH(() => hourglass(px - 58, py, 22 * backOut(gk), Math.PI * easeOut(seg(t, E.glass, E.glass + .22)), ease(seg(t, E.glass + .2, E.glass + .7))));
    }

    // ---- the new line: the close stretches into the next round's Price to Beat ----
    const Yd = HY + TW0 / HS, dashK = j => 1 - ease(seg(t, E.dashOut + .02 * (20 - j), E.dashOut + .25 + .02 * (20 - j)));
    if (t > E.slide) {
      const n = Math.floor(570 / 26), dx = HX + dotX / HS;
      boilSeed('newptb');
      for (let i = 0; i < n; i += 2) {
        const a = lerp(100, 670, i / n), b = lerp(100, 670, (i + 1) / n), a2 = Math.max(a, dx), k = dashK(i);
        if (b <= a2 + .5 || k <= .02) continue;
        const m = (a2 + b) / 2, h = (b - a2) / 2 * k;
        inkLine([[m - h, Yd], [m + h, Yd]], .8, C.cream, 'inkfine', 0);
      }
    }

    // ---- you: the hop out of the screen onto the desk, then down behind it ----
    if (t >= E.pull && t < E.sunk + .02) {
      const m = HI.mood(t), [dL, dR] = deskArms(m);
      if (t < E.land) {   // screen-locked, drawn at screen size
        const d = hop(t), s = sitArms(t, m), w = [CAM.cx + (d.s[0] - W / 2) / CAM.zoom, CAM.cy + (d.s[1] - H / 2) / CAM.zoom];
        push(); translate(w[0], w[1]); scale(1 / CAM.zoom);
        you(0, 0, d.u, { ...m, view: d.k < .55 ? 'front' : 'q', flip: d.k >= .55, sq: s.sq * (1 - d.k) - .14 * d.air, dy: s.dy * (1 - d.k),
          aL: lerp(lerp(s.aL, dL, d.k), .95, d.air), aR: lerp(lerp(s.aR, dR, d.k), 1.05, d.air), boilKey: 'you' });
        pop();
      } else {            // on the desk: a sad beat, a little rise (anticipation), then down behind the desk
        const land = Math.exp(-(t - E.land) * 7) * Math.cos((t - E.land) * 16);
        const hide = t < E.sink ? 0 : t < E.sink + .08 ? -.05 * Math.sin(Math.PI / 2 * seg(t, E.sink, E.sink + .08)) : lerp(-.05, 1, easeIn(seg(t, E.sink + .08, E.sunk)));
        you(DESK.youX, DESK.top + 200 * hide, 21, { ...m, view: 'q', flip: true, sq: .22 * land + (hide > .1 ? -.08 : 0), aL: dL, aR: dR + .8 * seg(hide, .1, .6), boilKey: 'you' });
        if (hide > 0) HI.deskFront(DESK.youX - 118);
      }
    }
    camEnd();
    HI.ash(t, 1 - seg(t, 63.0, 64.0));
  }
  shots([[CUT.I, shotI]]);
})();
