// E.js: WHO PAYS (27.969 → 37.255). See STORYBOARD.md, shot E.
//   Continuous from D: both hold their fresh halves. You lean back and doze ("You waited": zzz), then "0%" on
//   "nothing". The stranger's chip replays zipping in with speed lines ("filled instantly"); a pair of fee jaws drops in
//   and CHOMPS the stranger's Down half ("3%" on "three percent"); the stranger does a take.
//   Whip pan on the beat (33.13) to the fee hill: you trudge up it, the toll gate on the summit clunks on "most", "50/50"
//   on "fifty-fifty". "Flip-flopping": you flip your half Up↔Down three times, the gate bites it every time, it shrinks,
//   you go dizzy and tumble down out of frame. Out (E→F contract): the stage plate, cam(t, 470, 700, 1), feeHill(t, 1),
//   no characters.
(() => {
  const { U, YX, TX, FY, armTip, halfC, heldAt, sparks } = DE;
  const T = {
    waited: wt('E1', 'waited'), nothing: wt('E1', 'nothing'), stranger: wt('E2', 'stranger'), instantly: wt('E2', 'instantly'),
    three: wt('E2', 'three'), most: wt('E3', 'most'), fifty: wt('E3', 'fifty-fifty'), discourages: wt('E4', 'discourages'), flip: wt('E4', 'flip-flopping'),
  };
  const TWHIP = 33.128;                                           // the cut, on the beat (116.3 bpm, offset .11)
  const TZIP = T.instantly - .01, TCHOMP = T.three - .02;         // the replayed fill, the fee bite
  const EXCH = '#5A4F7A', EXCH_DK = '#3A3350', EXCH_LT = '#7C6FA3';   // the exchange's violet (its stamp, its fees)

  // ---------- the fee jaws: the exchange's bite. Mouth faces +x (rotated by ang), hinge at the back. ----------
  function jaws(x, y, s, open, ang, key) {
    boilSeed('jaws' + key);
    push(); translate(x, y); rotate(ang);
    const hx = -s * .95, A = open * .62, B = open * .42;
    const dome = (dir, k) => { const P = []; for (let i = 0; i <= 12; i++) { const a = Math.PI * i / 12; P.push([-Math.cos(a) * s * k, dir * Math.sin(a) * s * .7 * k]); } return P; };
    const teeth = (dir, k) => { for (let i = 0; i < 5; i++) { const tx = -s * .55 + i * s * .3 * k; paint([[tx, 0], [tx + s * .24, 0], [tx + s * .12, dir * s * .2]], { wash: C.cream, ink: C.ink, sw: .5 }); } };
    if (open > .05) paint([[hx, 0], [hx + 2 * s * Math.cos(A), -2 * s * Math.sin(A)], [hx + 1.8 * s * Math.cos(B), 1.8 * s * Math.sin(B)]], { wash: '#2A2238', ink: null });
    push(); translate(hx, 0); rotate(B); translate(-hx, 0);                      // lower jaw
    paint(dome(1, .85), { wash: EXCH, ink: C.ink, sw: .9 }); teeth(-1, .85);
    pop();
    push(); translate(hx, 0); rotate(-A); translate(-hx, 0);                     // upper jaw, with an eye
    paint(dome(-1, 1), { wash: EXCH_LT, ink: C.ink, sw: 1 }); teeth(1, 1);
    paint(ellPts(-s * .15, -s * .38, s * .13, s * .15, 12), { wash: C.cream, ink: C.ink, sw: .5 });
    paint(ellPts(-s * .1, -s * .36, s * .06, s * .07, 8), { wash: C.ink, ink: null });
    pop();
    pop();
  }
  function crumbs(x, y, t0, t, col, key) {
    const a = t - t0; if (a < 0 || a > .6) return;
    boilSeed('crumb' + key);
    for (let i = 0; i < 9; i++) {
      const vx = (hash(i + 7) - .5) * 260, vy = -120 - 140 * hash(i + 3), px = x + vx * a, py = y + vy * a + 1100 * a * a;
      paint(ellPts(px, py, 5 + 5 * hash(i), 4 + 3 * hash(i + 1), 6, 1, a * 8 + i), { wash: col, washOp: 255 * (1 - a / .6), ink: null });
    }
  }

  // ---------- E1: the two-shot (27.969 → 33.128) ----------
  const youKeys = [...DE.youKeys, [28.2, 'sleepy', { lookX: .3, lookY: .2 }], [29.86, 'smug', { lookX: .7, lookY: -.3 }],
    [32.2, 'nervous', { lookX: 1, lookY: -.3 }]];
  const themKeys = [...DE.themKeys, [28.36, 'happy', { lookX: .6, lookY: -.3 }], [TZIP + .04, 'proud', { lookX: .5, lookY: -.4, emote: null }],
    [TCHOMP + .06, 'surprised', { lookX: .2, lookY: -1, emote: '!!' }], [32.62, 'angry', { lookX: .5, lookY: -.7 }]];
  function youE1(t) {
    const m = actYou(t, youKeys, { take: .8 });
    const aD = 1.0 + .08 * Math.sin((t - DE.TCU) * 5) - .25 * spring(t, DE.TCU, 7, 20);      // D's hold, continued
    const aR = lerp(aD, kf(t, [[28.2, .05], [29.8, .05], [30.05, .55]]), ease(seg(t, 28.15, 28.6)));
    const rot = kf(t, [[28.2, 0], [28.6, -.09], [29.78, -.09], [30.0, .02], [30.3, 0]]) + (m.rot || 0) * ease(seg(t, 28.2, 28.6));
    return { x: YX, y: FY, o: { ...m, view: 'q', flip: false, aR, rot } };
  }
  function themE1(t) {
    const m = actThem(t, themKeys, { take: .8 });
    const aD = 1.0 + .08 * Math.sin((t - DE.TCD) * 4.3 + 1) - .25 * spring(t, DE.TCD, 7, 20);
    const aR = lerp(aD, .95 + .06 * Math.sin(t * 3.1) + .3 * spring(t, TZIP, 8, 20) - .35 * spring(t, TCHOMP, 7, 22), ease(seg(t, 28.3, 28.8)));
    return { x: TX, y: FY, o: { ...m, view: 'q', flip: true, aR, rot: (m.rot || 0) * ease(seg(t, 28.3, 28.8)) } };
  }
  function camE1(t) {
    const [x0, y0, z0] = DE.camEnd;
    // push in on you ("You waited… nothing"), then pan across to the stranger ("filled instantly… 3%")
    const x = kf(t, [[CUT.E, x0], [28.9, 285], [30.2, 292], [30.9, 640], [32.9, 652]], ease);
    const y = kf(t, [[CUT.E, y0], [28.9, 948], [30.2, 944], [30.9, 930], [32.9, 924]], ease);
    const z = kf(t, [[CUT.E, z0], [28.9, 1.22], [30.2, 1.24], [30.9, 1.22], [32.9, 1.26]], ease);
    const wx = 200 * easeIn(seg(t, 32.95, TWHIP));                  // whip: pan right, fast (kept inside the plate's margin)
    const sh = t > TCHOMP ? shakeXY(t, 7 * Math.exp(-(t - TCHOMP) * 9)) : [0, 0];
    cam(t, x + wx + sh[0], y + sh[1], z);
  }
  function shotE1(t) {
    camE1(t);
    room(t, { plate: 'stage', bloom: 0 });
    books(t, { bidK: 1, askK: 0, askOp: .35, spread: 0 });
    DE.veil(1);
    const Y = youE1(t), H = themE1(t), seeY = DE.onCanvas(Y.x, Y.y, U), seeH = DE.onCanvas(H.x, H.y, U);
    if (seeY) you(Y.x, Y.y, U, { ...Y.o, boilKey: 'you' });
    if (seeH) them(H.x, H.y, U, { ...H.o, boilKey: 'them' });
    // your half: at your side while you doze, lifted a little on "nothing"
    const hy = DE.heldHalf(t, 'up', Y);
    if (seeY) halfC(hy.x, hy.y, hy.r, 'up', { glow: hy.glow, key: 'upD', rot: lerp(hy.rot, -.25, ease(seg(t, 28.2, 28.6))) });
    // the stranger's half: tilted up to show it off, then bitten
    const hd = DE.heldHalf(t, 'down', H), bite = t < TCHOMP ? 0 : .78 * backOut(seg(t, TCHOMP, TCHOMP + .06));
    const rot = lerp(hd.rot, -.5, ease(seg(t, 28.35, 28.9))), fill = t > TZIP ? Math.exp(-(t - TZIP) * 4) : 0;
    const rD = hd.r * (1 + .15 * spring(t, TZIP, 9, 26)) * (1 - .1 * seg(t, TCHOMP, TCHOMP + .1));
    if (fill > .01) glow(hd.x, hd.y, 200, '#FFF0C0', fill);
    halfC(hd.x, hd.y, rD, 'down', { glow: hd.glow + .6 * fill, key: 'downD', rot, bite });
    // the bite point on the half's top edge (where half()'s bite lands for this tilt)
    const bp = [hd.x + (.33 * Math.cos(rot) + .55 * Math.sin(rot)) * rD, hd.y + (.33 * Math.sin(rot) - .55 * Math.cos(rot)) * rD];
    // the replay: the stranger's chip zips in with speed lines and fills instantly
    if (t > TZIP - .2 && t < TZIP + .08) {
      const k = seg(t, TZIP - .2, TZIP), p0 = [1190, 700], e = easeIn(k), x = lerp(p0[0], hd.x, e), y = lerp(p0[1], hd.y, e);
      boilSeed('zip');
      for (let i = 0; i < 4; i++) {
        const back = (140 + 90 * hash(i)) * Math.min(1, k * 3), dx = (p0[0] - hd.x), dy = (p0[1] - hd.y), L = Math.hypot(dx, dy), off = (i - 1.5) * 16;
        const ux = dx / L, uy = dy / L;
        inkLine([[x + ux * 40 - uy * off, y + uy * 40 + ux * off], [x + ux * (40 + back) - uy * off, y + uy * (40 + back) + ux * off]], .9, C.cream, 'inkfine', 0);
      }
      chip(x, y, '', C.down, { s: 1.05, k: 1 - seg(t, TZIP, TZIP + .08) });
    }
    if (t > TZIP) sparks(hd.x, hd.y, TZIP, t, 8, { v: 420, s: 13, life: .4, key: 'fill', a0: -Math.PI * 1.1, span: Math.PI * 1.2 });
    // the fee jaws: drop in chattering, open wide (anticipation), CHOMP, chew, leave
    if (t > 31.3 && t < 32.8) {
      const s = 84, ang = Math.PI * .3;                                   // lunging down-right onto the half's top
      const hover = [bp[0] - Math.cos(ang) * s * 1.05, bp[1] - Math.sin(ang) * s * 1.05], drop = kf(t, [[31.3, -620], [31.78, 0], [31.84, -8], [31.9, 0]], easeOut);
      const wind = kf(t, [[31.86, 0], [TCHOMP - .07, -30], [TCHOMP, 12], [TCHOMP + .12, 4], [32.42, 0]]);
      const leave = t > 32.42 ? -700 * easeIn(seg(t, 32.42, 32.8)) : 0;
      const open = t < 31.86 ? .25 + .2 * Math.abs(Math.sin(t * 22)) : t < TCHOMP - .07 ? lerp(.3, 1, ease(seg(t, 31.86, TCHOMP - .07))) : t < TCHOMP ? lerp(1, 0, easeIn(seg(t, TCHOMP - .07, TCHOMP))) : t < 32.42 ? .12 * Math.abs(Math.sin((t - TCHOMP) * 18)) : .3;
      const jx = hover[0] + leave * .5 + wind * Math.cos(ang), jy = hover[1] + drop + wind * Math.sin(ang) + leave;
      glow(jx, jy, s * 2.2, '#8C7CC8', .45);
      jaws(jx, jy, s, open, ang, 'fee');
    }
    crumbs(bp[0], bp[1], TCHOMP, t, C.downDk, 'fee');
    // the one term on screen at a time: 0% by you, then 3% by the stranger's bite
    const k0 = seg(t, T.nothing - .16, T.nothing) * (1 - seg(t, 30.52, 30.7));
    pill('0%', 405, 790, 62, { k: k0, key: 'zero' });
    const k3 = seg(t, TCHOMP - .12, TCHOMP + .02);
    pill('3%', 470, 800, 62, { k: k3, key: 'three' });
    camEnd();
    const w = seg(t, 32.95, 33.31);
    if (w > 0) { flushLetters(); whip(w, -1); }
  }

  // ---------- E2: the fee hill (33.128 → 37.255) ----------
  const GATE = { x: 585, beam: 322, rest: 396 };                  // on the summit's shoulder; rest = the portcullis teeth's bottom
  const UY = 27;                                                   // you, on the hill
  const PSTOP = .36;                                               // where you stop, at the top, holding the half into the gate
  const grip = (tip, r) => [tip[0] + .5 * r, tip[1] - .18 * r];   // the hand holds the half by its edge, out in front
  const FL = [35.95, 36.4, 36.78], CH = FL.map(f => f + .12);     // flips, and the gate's bite after each
  const TFALL = 36.93;
  const hillY = x => HILL.y - HILL.h * Math.pow(Math.sin(clamp((x - HILL.x0) / (HILL.x1 - HILL.x0)) * Math.PI), 1.6);
  const youE2Keys = [[TWHIP, 'determined', { lookX: .7, lookY: -.5, emote: 'sweat' }], [34.62, 'surprised', { lookX: .8, lookY: -.8 }],
    [35.4, 'mischief', { lookX: .9, lookY: -.3 }], [CH[0] + .03, 'nervous', { lookX: .9, lookY: -.4 }], [CH[1] + .03, 'dizzy', {}]];
  function youE2(t) {
    const m = actYou(t, youE2Keys, { take: .7 });
    // trudge up the slope, then stand at the gate
    const k = seg(t, TWHIP - .3, 34.62), x0 = 110, x1 = HILL.x0 + (HILL.x1 - HILL.x0) * PSTOP, x = lerp(x0, x1, ease(k));
    const walking = t < 34.62, walk = (x - x0) / (2.6 * UY);
    let o = { ...m, view: 'q', flip: false, walk: walking ? walk : null, rot: walking ? .1 : 0, dy: (m.dy || 0) - (walking ? .35 * Math.abs(Math.sin(walk * Math.PI)) : 0) };
    let aR = walking ? .2 + .1 * Math.sin(walk * TAU) : kf(t, [[34.62, .2], [35.45, .25], [35.8, .4]]);
    for (const f of FL) aR += .3 * Math.exp(-Math.pow((t - f) / .07, 2));                  // the arm pumps each flip
    o.aR = aR;
    o.sq = (o.sq || 0) + FL.reduce((s, f) => s + .12 * spring(t, f - .05, 10, 30), 0) + CH.reduce((s, c) => s + .08 * spring(t, c, 12, 34), 0);
    let X = x, Yy = hillY(x);
    if (t > TFALL) {                                                   // topple back, then tumble down the slope and out
      const a = seg(t, TFALL, TFALL + .09), b = seg(t, TFALL + .05, 37.14), e = b * b;
      X = lerp(x1, -340, e); Yy = hillY(X) - 60 * Math.sin(b * Math.PI);
      o = { ...o, rot: -.7 * ease(a) - TAU * 1.1 * e, smear: .7 * b, smearDir: -1, walk: null, eyes: 'swirl', mouth: 'wobble' };
    }
    return { x: X, y: Yy, o };
  }
  function portcullis(t, biteY) {   // the teeth's bottom edge: rest, a clunk on "most", then a bite after each flip
    let y = GATE.rest;
    const clunk = t - (T.most - .04); if (clunk > 0 && clunk < .4) y += 58 * Math.exp(-clunk * 9) * Math.abs(Math.cos(clunk * 14));
    const d = biteY - GATE.rest;
    for (const c of CH) { const a = t - (c - .05); if (a > 0 && a < .3) y += a < .05 ? d * easeIn(a / .05) : d * Math.exp(-(a - .05) * 14); }
    return y;
  }
  function gate(t, sink, biteY) {
    boilSeed('gate');
    const { x, beam } = GATE, pw = 44, py = portcullis(t, biteY) + sink, b = beam + sink, gy = hillY(x) + 30;
    for (const s of [-1, 1]) paint(rrPts(x + s * (pw + 16) - 13, b + 10, 26, gy - b, 7, 1), { wash: EXCH_DK, ink: C.ink, sw: 1 });   // posts
    paint(rrPts(x - pw, b + 18, pw * 2, py - b - 44, 8, 1), { wash: EXCH, ink: C.ink, sw: 1 });                                    // the portcullis
    for (let i = 0; i < 3; i++) { const tx = x - pw + 2 + i * (pw * 2 - 4) / 3, tw = (pw * 2 - 4) / 3; paint([[tx, py - 28], [tx + tw, py - 28], [tx + tw / 2, py]], { wash: C.cream, ink: C.ink, sw: .6 }); }
    paint(rrPts(x - 104, b - 20, 208, 42, 14, 1), { wash: EXCH, ink: C.ink, sw: 1.2 });                                             // the beam
    const lamp = .5 + .5 * Math.exp(-Math.max(0, t - (T.most - .04)) * 3) + CH.reduce((s, c) => s + (t > c ? .6 * Math.exp(-(t - c) * 6) : 0), 0);
    glow(x, b - 36, 110, '#FFD46A', .55 * lamp);
    paint(ellPts(x, b - 34, 17, 14, 12), { wash: mixCol(C.goldDk, C.gold, clamp(lamp)), ink: C.ink, sw: .8 });
  }
  function camE2(t) {
    const x = kf(t, [[TWHIP, 300], [34.5, 440], [35.3, 452], [35.75, 468], [36.86, 472], [37.13, 470]], ease);
    const y = kf(t, [[TWHIP, 772], [34.5, 610], [35.3, 590], [35.75, 500], [36.86, 494], [37.13, 700]], ease);
    const z = kf(t, [[TWHIP, 1.05], [34.5, 1.08], [35.3, 1.12], [35.75, 1.38], [36.86, 1.42], [37.13, 1]], ease);
    const wx = -110 * (1 - easeOut(seg(t, TWHIP, 33.42)));
    const sh = CH.reduce((s, c) => s + (t > c && t < c + .3 ? 5 * Math.exp(-(t - c) * 12) : 0), 0), d = t > CH[0] ? shakeXY(t, sh) : [0, 0];
    cam(t, x + wx + d[0], y + d[1], z);
  }
  function shotE2(t) {
    camE2(t);
    room(t, { plate: 'stage', bloom: 0 });
    const Y = youE2(t), tip = armTip(Y.x, Y.y, UY, Y.o), gone = t > 37.15 || !DE.onCanvas(Y.x, Y.y, UY);
    // your half: the flips swap it Up↔Down, the gate bites it, it shrinks
    let side = 'up', r = 60, bite = 0, fx = 1, hop = 0;
    FL.forEach((f, i) => {
      const k = seg(t, f - .02, f + .12);
      if (k > 0) { hop = 30 * Math.sin(Math.PI * k); fx = Math.abs(Math.cos(Math.PI * k)); }
      if (k >= .5) { side = i % 2 ? 'up' : 'down'; r = 60 * Math.pow(.8, i); bite = 0; }
      if (t >= CH[i]) { bite = .8 * backOut(seg(t, CH[i], CH[i] + .05)); r = 60 * Math.pow(.8, i) * (1 - .12 * seg(t, CH[i], CH[i] + .1)); }
    });
    const rot = (side === 'up' ? .5 : -.5) + (t > TFALL ? Y.o.rot : 0), hand = grip(tip, r), top = hand[1] - hop - .64 * r;
    const sink = 240 * easeIn(seg(t, 37.0, 37.2));
    if (sink < 235) gate(t, sink, top + 22);
    feeHill(t, 1);
    if (!gone) {
      you(Y.x, Y.y, UY, { ...Y.o, boilKey: 'you' });
      halfC(hand[0], hand[1] - hop, r, side, { rot, fx: Math.max(.04, fx), bite, glow: .35, key: 'hill' });
    }
    if (!gone) CH.forEach((c, i) => crumbs(hand[0], top + 12, c, t, i % 2 ? C.upDk : C.downDk, 'hill' + i));
    // 50/50 over the toll gate
    const k5 = seg(t, T.fifty - .16, T.fifty) * (1 - seg(t, 35.3, 35.46));
    pill('50/50', 470, 228, 62, { k: k5, key: 'fifty' });
    camEnd();
    const w = seg(t, 32.95, 33.31);
    if (w > 0 && w < 1) { flushLetters(); whip(w, -1); }
  }

  function shotE(t, lt, dur) { if (t < TWHIP) shotE1(t); else shotE2(t); }
  shots([[CUT.E, shotE]]);
})();
