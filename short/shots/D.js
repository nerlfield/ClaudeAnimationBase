// D.js: THE MINT (18.683 → 27.969). See STORYBOARD.md, shot D.
//   Opens exactly on C's last frame (the stage plate, BOOK.cam, both books, nothing else). You slide in from the left
//   and slap a 60¢ chip on the Up book's top bid; the stranger sneaks in from the right and slaps 40¢ on the Down
//   book's top bid. "Nobody's selling": every ask greys and slides away, a tumbleweed rolls through the empty asks, the
//   two glance at each other. The chips lift, arc together and fuse into the gold $1; the exchange's stamp lowers,
//   winds up and SLAMS down on "mints" (flash, sparks, shake, punch-in); a fresh Up half and Down half pop out and
//   fly to their bidders. Out: continuous into E (both holding their halves).
// window.DE: the cast, geometry and helpers E.js shares, so the D→E seam agrees frame for frame.
(() => {
  // ---------- the cast and the geometry (world px) ----------
  const U = 30, YX = 95, TX = 815, FY = 1180;                       // you (left) and the stranger (right): ground points
  const BU = BOOK.U, RH = (BU[3] - 150) / 10, ROW = BU[1] + 110 + 5 * RH + 34 + RH / 2;   // the top bid row's centre
  const CHIP_U = [300, ROW], CHIP_D = [618, ROW];
  const MX = BOOK.mint[0], MY = BOOK.mint[1], CR = 88, HR = 56;     // the mint: coin centre and radius; held-half radius
  const T = {
    in: CUT.D + .2, sixty: wt('D1', 'sixty'), stranger: wt('D2', 'stranger'), forty: wt('D2', 'forty'),
    nobody: wt('D3', "Nobody's"), selling: wt('D3', 'selling'), sixty2: wt('D4', 'sixty'), forty2: wt('D4', 'forty'),
    dollar: wt('D4', 'dollar'), mints: wt('D4', 'mints'), fresh: wt('D4', 'fresh'), both: wt('D4', 'both'),
  };
  const TS1 = T.sixty - .05, TS2 = T.forty - .06;                  // the two slaps (chip on the row)
  const TI = 25.83;                                                // stamp impact (frame 775, on "mints")
  const TCU = 27.0, TCD = 27.25;                                   // the halves are caught (you, then the stranger)

  // ---------- helpers shared with E ----------
  // Where a character's arm tip is, in world px, for the same options passed to clawd() (mirrors clawd's transforms).
  function armTip(x, y, u, o, which = 'R') {
    const V = VIEWS[o.view] || VIEWS.front, arm = V.arms.find(a => a[2] === which) || V.arms[0];
    const [px, dir] = arm, a = which === 'L' ? (o.aL ?? .2) : (o.aR ?? .2);
    const sq = (o.sq || 0) + (o.take || 0), sm = clamp(o.smear || 0);
    const Sx = (o.flip ? -1 : 1) * (o.sx ?? 1) * (1 + sq * .6) * (1 + sm * .35), Sy = (o.sy ?? 1) * (1 - sq);
    let bx = (px + dir * .55 * clamp((Math.abs(a) - .7) / .9)) * u, by = -4.5 * u;
    if (dir === 0) { const th = .7 - a; by += .3 * u; bx += 2.1 * u * Math.cos(th); by += 2.1 * u * Math.sin(th); }
    else { const th = dir < 0 ? a : -a; bx += dir * 2.2 * u * Math.cos(th); by += dir * 2.2 * u * Math.sin(th); }
    const lx = bx * Sx, ly = by * Sy, r = o.rot || 0, c = Math.cos(r), s = Math.sin(r);
    return [x + (o.dx || 0) * u + lx * c - ly * s, y + (o.dy || 0) * u + lx * s + ly * c];
  }
  // A half positioned by its visual centre (not the coin's), so it can flip in place: o.fx squeezes it (a card flip).
  function halfC(cx, cy, r, side, o = {}) {
    const s = side === 'up' ? -1 : 1;
    push(); translate(cx, cy); rotate(o.rot || 0); scale(o.fx ?? 1, o.fy ?? 1);
    half(-s * .42 * r, 0, r, side, { ...o, rot: 0 });
    pop();
  }
  // A half held in a hand: the hand grips its bottom edge.
  const heldAt = (tip, r, dir = 1) => [tip[0] + dir * r * .45, tip[1] - r * .3];
  // Gold sparks off an impact: n stars on ballistic arcs, fading. Pure in t.
  function sparks(x, y, t0, t, n, o = {}) {
    const a = t - t0, life = o.life || .6; if (a < 0 || a > life) return;
    boilSeed('sparks' + (o.key || ''));
    for (let i = 0; i < n; i++) {
      const ang = (o.a0 ?? -Math.PI) + (o.span ?? Math.PI) * (i + .5 * hash(i + 3)) / n, v = (o.v || 700) * (.55 + .6 * hash(i + 11));
      const q = a / (life * (.6 + .4 * hash(i + 5))); if (q >= 1) continue;
      const px = x + Math.cos(ang) * v * a, py = y + Math.sin(ang) * v * a * .8 + 900 * a * a;
      paint(starPts(px, py, (o.s || 18) * (1 - q) * (.7 + .6 * hash(i + 2)), .28, 4, ang + a * 6), { wash: i % 3 ? C.goldLt : C.cream, washOp: 255 * (1 - q * q), ink: null });
    }
  }
  // After the fill the books step back: a panel-coloured veil over each ladder, so the held halves read against it.
  function veil(k) {
    if (k <= .01) return;
    boilSeed('veil');
    for (const [x, y, w, h] of [BOOK.U, BOOK.D]) paint(rrPts(x + 12, y + 100, w - 24, h - 112, 18, .8), { wash: C.panel, washOp: 170 * k, ink: null });
  }
  // Is a character (ground point x, y, unit u) anywhere on the canvas? p5.brush strokes just off-canvas are slow, so
  // shots skip a character that the camera has left entirely.
  function onCanvas(x, y, u, pad = 10, l = 8, r = 8) {   // l, r: how far it reaches left and right, in u
    const a = toScreen(x - l * u, y - 13 * u), b = toScreen(x + r * u, y + 2 * u);
    return Math.max(a[0], b[0]) > -pad && Math.min(a[0], b[0]) < W + pad && Math.max(a[1], b[1]) > -pad && Math.min(a[1], b[1]) < H + pad;
  }
  window.DE = { U, YX, TX, FY, ROW, CHIP_U, CHIP_D, HR, TCU, TCD, armTip, halfC, heldAt, sparks, veil, onCanvas };

  // ---------- acting ----------
  // You: slide in (fast, leaning), slap 60¢ on "sixty", watch the stranger, glance, look up, flinch at the stamp, catch.
  const youKeys = [[CUT.D, 'determined', { lookX: .6, lookY: -.6 }], [TS1 + .03, 'happy', { lookX: .5, lookY: -.7 }],
    [T.stranger + .05, 'neutral', { lookX: 1, lookY: -.1 }], [22.52, 'confused', { lookX: 1, lookY: -.1 }],
    [23.2, 'hopeful', { lookX: .5, lookY: -1 }], [TI + .02, 'surprised', { lookX: .6, lookY: -1 }],
    [26.3, 'hopeful', { lookX: .6, lookY: -.9 }], [TCU, 'happy', { lookX: .6, lookY: -.3 }]];
  const themKeys = [[T.stranger - .1, 'mischief', { lookX: .6, lookY: -.5 }], [TS2 + .03, 'smug', { lookX: .4, lookY: -.6 }],
    [22.66, 'suspicious', { lookX: 1, lookY: -.1 }], [23.75, 'hopeful', { lookX: .6, lookY: -1 }],
    [TI + .06, 'surprised', { lookX: .4, lookY: -1, emote: null }], [26.45, 'hopeful', { lookX: .7, lookY: -.8 }], [TCD, 'excited', { lookX: .5, lookY: -.3 }]];
  window.DE.youKeys = youKeys; window.DE.themKeys = themKeys;

  function youPose(t) {
    const m = actYou(t, youKeys, { take: .8 });
    const kIn = seg(t, T.in, T.in + .14), x = lerp(-230, YX, backOut(kIn));
    let rot = (m.rot || 0) + .2 * (1 - ease(kIn)) + .08 * spring(t, T.in + .14, 7, 16), sq = m.sq || 0, dy = m.dy || 0, aR = m.aR;
    const smear = t < T.in + .14 ? .6 * Math.sin(kIn * Math.PI) : 0;
    if (t < TS1 + .45) {                                           // the slap: arm up, crouch, stretch, slap, settle
      aR = kf(t, [[T.in, 1.15], [TS1 - .09, 1.2], [TS1 - .04, .95], [TS1, 1.55], [TS1 + .1, 1.4], [TS1 + .45, m.aR]]);
      sq += kf(t, [[TS1 - .09, 0], [TS1 - .04, .14], [TS1, -.24], [TS1 + .08, .1], [TS1 + .2, 0]]);
      dy += kf(t, [[TS1 - .04, 0], [TS1, -.7], [TS1 + .12, 0]]);
      rot += kf(t, [[TS1 - .04, 0], [TS1, .08], [TS1 + .2, 0]]);
    }
    if (t > 26.5 && t < TCU) aR = lerp(m.aR, 1.25, ease(seg(t, 26.5, 26.85)));           // reach up for the half
    if (t >= TCU) aR = 1.0 + .08 * Math.sin((t - TCU) * 5) - .25 * spring(t, TCU, 7, 20);  // hold it up
    return { x, y: FY, o: { ...m, view: 'q', flip: false, rot, sq, dy, aR, smear, smearDir: 1 } };
  }
  function themPose(t) {
    const m = actThem(t, themKeys, { take: .8 });
    const kIn = seg(t, T.stranger - .1, T.stranger + .3), x = lerp(1190, TX, ease(kIn));
    let rot = (m.rot || 0) - .1 * Math.sin(kIn * Math.PI) - .06 * spring(t, T.stranger + .3, 6, 14), sq = m.sq || 0, dy = m.dy || 0, aR = m.aR;
    if (t < TS2 + .5) {                                            // sneak in holding the chip low, wind up, slap
      aR = kf(t, [[T.stranger - .1, .35], [TS2 - .35, .35], [TS2 - .12, 1.25], [TS2 - .05, 1.05], [TS2, 1.55], [TS2 + .12, 1.4], [TS2 + .5, m.aR]]);
      sq += kf(t, [[TS2 - .12, 0], [TS2 - .05, .14], [TS2, -.22], [TS2 + .08, .1], [TS2 + .22, 0]]);
      dy += kf(t, [[TS2 - .05, 0], [TS2, -.6], [TS2 + .12, 0]]);
    }
    if (t > 26.6 && t < TCD) aR = lerp(m.aR, 1.25, ease(seg(t, 26.6, 27.05)));
    if (t >= TCD) aR = 1.0 + .08 * Math.sin((t - TCD) * 4.3 + 1) - .25 * spring(t, TCD, 7, 20);
    return { x, y: FY, o: { ...m, view: 'q', flip: true, rot, sq, dy, aR } };
  }

  // A caught half, held up in the hand (E continues from this).
  function heldHalf(t, side, P) {
    const up = side === 'up', tc = up ? TCU : TCD, hand = heldAt(armTip(P.x, P.y, U, P.o), HR, up ? 1 : -1);
    return { x: hand[0], y: hand[1], r: HR * (1 + .12 * spring(t, tc, 8, 24)), rot: (up ? -.1 : .1) + .06 * Math.sin((t - tc) * 4), glow: .5 + .3 * Math.exp(-(t - tc) * 3) };
  }
  Object.assign(window.DE, { youPose, themPose, heldHalf, camEnd: [460, 812, .95] });

  // ---------- props ----------
  // The two chips: held, slapped onto the top bid row, lifted and flown up together to the mint.
  function chipState(t, side, P) {
    const up = side === 'up', ts = up ? TS1 : TS2, lift = up ? 23.26 : 23.87, fly = up ? .6 : .57, meet = [MX + (up ? -54 : 54), MY + 8];
    const tip = armTip(P.x, P.y, U, P.o);
    if (t < ts - .04) return { x: tip[0], y: tip[1] - 30, s: 1.05 };
    if (t < ts) { const k = ease(seg(t, ts - .04, ts)); return { x: lerp(tip[0], (up ? CHIP_U : CHIP_D)[0], k), y: lerp(tip[1] - 30, ROW, k), s: 1.1 }; }
    const home = up ? CHIP_U : CHIP_D;
    if (t < lift - .08) return { x: home[0], y: home[1], s: 1.2 * (1 + .18 * spring(t, ts, 9, 26)), land: t - ts };
    if (t < lift) { const k = seg(t, lift - .08, lift); return { x: home[0], y: home[1] + 7 * Math.sin(k * Math.PI / 2), s: 1.2 * (1 - .06 * k) }; }
    if (t < lift + fly) { const k = seg(t, lift, lift + fly), p = arcPt(home, meet, 150, ease(k)); return { x: p[0], y: p[1], s: 1.2 * (1 + .08 * Math.sin(k * Math.PI)), rot: (up ? 1 : -1) * .5 * Math.sin(k * Math.PI) }; }
    const hov = t - lift - fly, bob = 6 * Math.sin(hov * 7) * (1 - seg(t, 24.3, 24.4)), clink = kf(t, [[24.3, 0], [24.38, 1], [24.43, .8], [24.47, 1]]);
    if (t < 24.57) return { x: lerp(meet[0], MX + (up ? -47 : 47), clink) + (up ? 1 : -1) * 30 * ease(seg(t, 24.46, 24.57)), y: meet[1] + bob, s: 1.2 * (1 - ease(seg(t, 24.46, 24.57))) };
    return null;
  }
  // The exchange's stamp: out of frame → lowers into view → winds up (rises) → slams → holds → lifts away.
  const CONTACT = MY - CR;                                        // the coin's top
  function dieBottom(t) {
    if (t < 25.72) return kf(t, [[24.95, -320], [25.35, CONTACT - 100], [25.4, CONTACT - 94], [25.72, CONTACT - 172]], ease);
    if (t < TI) return lerp(CONTACT - 172, CONTACT, easeIn(seg(t, 25.72, TI)));      // the slam: accelerating
    if (t < 25.96) return CONTACT + 64;                                               // held down on the squashed coin
    return lerp(CONTACT + 64, -380, easeIn(seg(t, 25.96, 26.36)));                    // lifts away
  }
  const coinSquash = t => t < TI ? 0 : t < 25.96 ? .36 : .36 * Math.exp(-(t - 25.96) * 9) * Math.cos((t - 25.96) * 30);
  function tumbleweed(t) {
    const k = seg(t, 22.26, 23.15); if (k <= 0 || k >= 1) return;
    const r = 66, x = lerp(-170, 1130, k), ph = k * Math.PI * 3.4 + .35, hop = Math.abs(Math.sin(ph)) * 64 * (1 - .35 * k), y = 850 - r - hop;
    boilSeed('tumble');
    paint(ellPts(x, 852, r * (1 - hop / 220), 9, 14), { wash: C.ink, washOp: 80, ink: null });
    const land = Math.abs(Math.cos(ph)) > .9 ? 1 : 0;   // a puff of dust where it touches down
    if (land) for (const d of [-1, 1]) paint(ellPts(x + d * r * .8, 846, 16, 9, 10), { wash: '#6E6650', washOp: 90, ink: null });
    push(); translate(x, y); rotate((x + 170) / r); scale(1 + .06 * (1 - hop / 64), 1 - .06 * (1 - hop / 64));
    for (let i = 0; i < 9; i++) {   // loops of dry twigs, each tilted a different way
      const a = i * .7 + hash(i) * .5, rr = r * (.55 + .45 * hash(i + 20)), P = [];
      for (let j = 0; j <= 12; j++) { const b = j / 12 * TAU; P.push([Math.cos(b) * rr * Math.cos(a) - Math.sin(b) * rr * .55 * Math.sin(a), Math.cos(b) * rr * Math.sin(a) + Math.sin(b) * rr * .55 * Math.cos(a)]); }
      inkLine(P, i % 3 ? .9 : 1.3, ['#C9AE72', '#8C7447', '#B09058'][i % 3], 'dry', .7);
    }
    for (let i = 0; i < 7; i++) { const a = hash(i + 40) * TAU, a2 = a + .4 * (hash(i + 50) - .5); inkLine([[Math.cos(a) * r * .5, Math.sin(a) * r * .5], [Math.cos(a2) * r * 1.12, Math.sin(a2) * r * 1.1]], .7, '#9C8250', 'inkfine', .3); }
    pop();
  }

  // ---------- camera ----------
  function camera(t) {
    const x = kf(t, [[CUT.D, BOOK.cam[0]], [19.5, 456], [23.2, 462], [24.4, 463], [25.7, 464], [TI, 465], [26.3, 465], [27.35, 460]], ease);
    const y = kf(t, [[CUT.D, BOOK.cam[1]], [19.5, 778], [23.2, 790], [24.4, 610], [25.7, 575], [TI, 562], [26.3, 572], [27.35, 806], [CUT.E, 812]], ease);
    const z = kf(t, [[CUT.D, BOOK.cam[2]], [23.2, 1], [24.4, .92], [25.7, .92], [TI, .957], [26.3, .95], [27.35, .95]], ease);   // +4% on the slam
    const sh = t > TI ? shakeXY(t, 18 * Math.exp(-(t - TI) * 7)) : [0, 0];
    cam(t, x + sh[0], y + sh[1], z);
  }

  function shotD(t, lt, dur) {
    camera(t);
    room(t, { plate: 'stage', bloom: 0 });
    // the books: asks grey, then slide away ("Nobody's selling"); the spread goes with them
    const gU = seg(t, 21.96, 22.16), gD = seg(t, 22.04, 22.24), sU = seg(t, 22.1, 22.42), sD = seg(t, 22.18, 22.5);
    const spread = .6 * (1 - seg(t, 22.0, 22.3));
    const bk = books(t, { bidK: 1, spread,
      U: { askK: 1 - ease(sU), askOp: 1 - .65 * gU },
      D: { askK: 1 - ease(sD), askOp: 1 - .65 * gD } });
    // the filled rows flash as each half lands
    for (const [tc, x, col] of [[TCU, 222, '#6BE08E'], [TCD, 632, '#FF8A5C']]) if (t > tc) glow(x, ROW, 230, col, .9 * Math.exp(-(t - tc) * 3.5));
    veil(ease(seg(t, TCD + .15, CUT.E)));
    tumbleweed(t);
    // the cast
    const Y = t >= T.in ? youPose(t) : null, H = t >= T.stranger - .1 ? themPose(t) : null;
    // the chips: in a hand they're in front of the cast; placed on the board (or flying off it) they're behind it
    const chips = front => { for (const [side, P, col, label] of [['up', Y, C.up, '60¢'], ['down', H, C.down, '40¢']]) {
      if (!P || (t < (side === 'up' ? TS1 : TS2) + .5) !== front) continue;   // in front until the slapper has settled
      const c = chipState(t, side, P); if (!c) continue;
      if (c.land != null && c.land < .4) glow(c.x, c.y, 120, side === 'up' ? '#6BE08E' : '#FF8A5C', .8 * (1 - c.land / .4));
      if (c.s < .05) continue;
      push(); translate(c.x, c.y); rotate(c.rot || 0); translate(-c.x, -c.y);
      chip(c.x, c.y, label, col, { s: c.s });
      pop();
    } };
    chips(false);
    if (t > TS1 + .5 && t < 24.6) flushLetters();   // placed chips' labels go behind the cast too (letters otherwise sit on top)
    if (Y) you(Y.x, Y.y, U, { ...Y.o, boilKey: 'you' });
    if (H) them(H.x, H.y, U, { ...H.o, boilKey: 'them' });
    chips(true);
    // the fuse: a gold flash where the chips meet, and the $1 coin pops out of it
    if (t > 24.4 && t < 24.9) glow(MX, MY, 280, '#FFD46A', 1.3 * Math.sin(seg(t, 24.4, 24.9) * Math.PI));
    const q = coinSquash(t);
    if (t > 24.4 && t < 24.6) flushLetters();   // the coin grows over the chips' labels
    if (t > 24.48 && t < 26.14) {
      const bob = t < TI ? 5 * Math.sin((t - 24.5) * 6) : 0, ringRot = .1 * spring(t, 24.62, 5, 22) + .08 * spring(t, 25.96, 6, 34);
      push(); translate(MX, MY + CR + bob); scale(1 + .45 * q, 1 - q);
      coin(0, -CR, CR, { k: seg(t, 24.48, 24.66), glow: .45 + .15 * Math.sin(t * 5), rot: ringRot, label: null, key: 'mint' });
      pop();
      const lk = backOut(seg(t, 24.48, 24.66));
      if (lk > .02) txt('$1', MX, MY + CR + bob - CR * (1 - q) + 4, CR * .82 * lk * (1 - .5 * q), C.goldDk, { ink: false, rot: ringRot });
    }
    // the stamp
    const db = dieBottom(t);
    if (db > -300) {
      flushLetters();   // so the stamp covers the coin's lettering
      const fall = t > 25.72 && t < TI ? seg(t, 25.72, TI) : 0, imp = t >= TI ? Math.exp(-(t - TI) * 12) : 0;
      if (fall > .3) { boilSeed('slam'); for (let i = 0; i < 5; i++) { const sx = MX + (i - 2) * 70 + 10 * hash(i), L = 160 * fall; inkLine([[sx, db - 150 - L - 40 * hash(i + 4)], [sx, db - 140]], 1.1, C.cream, 'inkfine', 0); } }
      push(); translate(MX, db); scale(1 - .05 * fall + .08 * imp, 1 + .1 * fall - .1 * imp);
      press(0, 10, 0);
      pop();
    }
    // impact: light, impact lines, a shock ring and sparks
    if (t >= TI && t < TI + .7) {
      const a = t - TI, cy = CONTACT + 64;
      glow(MX, cy, 760, '#FFD98A', .9 * Math.exp(-a * 6));
      glow(MX, cy, 260, '#FFF4D6', Math.exp(-a * 9));
      boilSeed('impact');
      if (a < .22) for (let i = 0; i < 12; i++) {
        const ang = Math.PI * (i / 11) - Math.PI, r0 = 200 + 260 * easeOut(a / .22), r1 = r0 + 90 * (1 - a / .22);
        if (i === 0 || i === 11) continue;
        inkLine([[MX + Math.cos(ang + Math.PI) * r0, cy + Math.sin(ang + Math.PI) * r0 * .45], [MX + Math.cos(ang + Math.PI) * r1, cy + Math.sin(ang + Math.PI) * r1 * .45]], 1.4, C.goldLt, 'ink', 0);
      }
      if (a < .35) {   // a flat shock ring spreading along the stamp's floor (one painted polygon: cheap)
        const k = easeOut(a / .35), rr = 150 + 400 * k, th = 14 * (1 - k) + 3, O = ellPts(MX, cy + 22, rr, rr * .26, 32), I = ellPts(MX, cy + 22, rr - th, (rr - th) * .26, 32).reverse();
        paint([...O, O[0], I[I.length - 1], ...I], { wash: C.goldLt, washOp: 230 * (1 - k), ink: null });
      }
      sparks(MX, cy, TI, t, 16, { v: 900, s: 20, key: 'mint' });
    }
    // the fresh pair: pops out of the coin on "fresh", then each half flies to its bidder
    if (t >= 26.12) {
      if (t < 26.3) glow(MX, MY, 320, '#FFF0C0', 1.2 * (1 - seg(t, 26.12, 26.3)));
      for (const [side, P, t0, t1, tc] of [['up', Y, 26.34, TCU, TCU], ['down', H, 26.5, TCD, TCD]]) {
        const up = side === 'up', s = up ? -1 : 1, pop = backOut(seg(t, 26.12, 26.3));
        const start = [MX + s * .42 * CR + s * 22 * pop, MY - 6 * pop];
        const tip = armTip(P.x, P.y, U, P.o), hand = heldAt(tip, HR, up ? 1 : -1);
        let x, y, r, rot;
        if (t < t0) { x = start[0]; y = start[1] + 4 * Math.sin((t - 26.12) * 9); r = CR; rot = s * .12 * pop; }
        else if (t < t1) { const k = ease(seg(t, t0, t1)), p = arcPt(start, hand, 110, k); x = p[0]; y = p[1]; r = lerp(CR, HR, k); rot = s * .12 + s * TAU * easeOut(seg(t, t0, t1)); }
        else { const h = heldHalf(t, side, P); x = h.x; y = h.y; r = h.r; rot = h.rot; }
        halfC(x, y, r, side, { glow: .5 + .3 * Math.exp(-Math.max(0, t - t1) * 3), key: side + 'D', rot });
      }
    }
    camEnd();
  }
  shots([[CUT.D, shotD]]);
})();
