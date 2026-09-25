// F.js: WEIGH THE BOOK (37.255 → 42.414). See STORYBOARD.md, shot F.
//   In: E's fee hill, full, on the stage (the E→F contract). The hill flattens into the beam of a balance scale (with a
//   little sag), a fulcrum grows under it and a pan pops onto each end. The Up book drops in and, on "weigh", pours its
//   bids into the left pan and its asks into the right: the beam rocks with each block and settles level. The formula
//   pill holds while the voice reads it, each pan lighting up as it's named. On "bids" three more bid blocks drop in (the
//   left pan strains), and on "heavier" the scale tips to the bids (a creak first, a heavy settle). On "price" an Up price
//   tag pops over the pivot; a dotted, wobbly arrow draws up out of the scale and the tag drifts 60¢ → 63¢ part of the way
//   up it (a tendency, not a certainty: the arrow runs on past it).
//   Out: a push into the green Up tag; its green fills the frame, and G pulls back out of the market screen's Up button.
(() => {
  const tWeigh = wt('F1', 'weigh'), tBids = wt('F2', 'bids'), tAsks = wt('F2', 'asks'), tOver = wt('F2', 'over'), tBoth = wte('F2', 'both');
  const tMore = wt('F3', 'bids'), tHeavy = wt('F3', 'heavier'), tPrice = wt('F3', 'price'), tTends = wt('F3', 'tends'), tUpW = wt('F3', 'up');
  const tPush = CUT.G - .31;

  // ---------- the scale: the flattened hill's slab is the beam ----------
  const PX = 470, PY = HILL.y + 20;   // pivot: the middle of the slab (HILL.y .. HILL.y + 40)
  const ARM = 270;                    // the pans stand this far out along the beam
  const BH = 24, PITCH = 26, LMAX = 196;
  // the Up book: its bids and asks weigh the same, so the beam first settles level
  const BIDS = [.86, .62, .76, .52], ASKS = [.58, .9, .62, .66], MORE = [.72, .56, .82];
  const FLY = .3, FALL = .24;
  const POUR = [];
  BIDS.forEach((s, i) => POUR.push({ side: 'bid', s, i, j: i, t0: tWeigh + .03 + i * .085 }));
  ASKS.forEach((s, i) => POUR.push({ side: 'ask', s, i, j: 3 - i, t0: tWeigh + .07 + (3 - i) * .085 }));
  MORE.forEach((s, m) => POUR.push({ side: 'bid', s, more: true, j: 4 + m, t0: tMore - FALL + m * .085 }));
  POUR.forEach((b, n) => { b.t1 = b.t0 + (b.more ? FALL : FLY); b.n = n; });

  // the beam's angle (negative = the left, bid side, down)
  function ang(t) {
    let a = .006 * wob(t, .31);                                           // never still: a slow sway
    for (const b of POUR) a += (b.side === 'bid' ? -1 : 1) * (b.more ? .045 : .032) * spring(t, b.t1, 6, 15);
    for (const b of POUR) if (b.more) a -= .014 * ease(seg(t, b.t1, b.t1 + .12));   // the extra bids strain it
    a += .014 * Math.sin(Math.PI * seg(t, tHeavy - .2, tHeavy - .02));   // a creak: it lifts a hair first
    a -= .15 * ease(seg(t, tHeavy - .04, tHeavy + .3));                  // then tips, heavily
    a -= .03 * spring(t, tHeavy + .26, 4.5, 11);                          // a small overshoot, no bounce
    return a;
  }
  // a point on the beam's top edge, d px out from the pivot
  const onBeam = (t, d) => { const a = ang(t), c = Math.cos(a), s = Math.sin(a); return [PX + d * c + 20 * s, PY + d * s - 20 * c]; };
  const panAt = (t, side) => onBeam(t, side === 'bid' ? -ARM : ARM);
  // where block j of a pan sits (its centre), with a little stable offset so the stack looks piled, not ruled
  const slot = (t, side, j) => { const [ax, ay] = panAt(t, side); return [ax + (hash(j * 3 + (side === 'bid' ? 1 : 7)) - .5) * 26, ay - 70 - j * PITCH]; };

  function fulcrum(k) {
    const s = backOut(k); if (s < .02) return;
    boilSeed('fulcrum');
    const base = 1088, top = lerp(base, PY, s);
    paint([[PX - 15, top], [PX + 15, top], [PX + 76, base], [PX - 76, base]], { wash: mixCol(C.panelHi, C.grid, .45), ink: C.ink, sw: 1 });
    paint(rrPts(PX - 150 * s, base - 4, 300 * s, 26, 10, 1), { wash: C.panelHi, ink: C.ink, sw: 1 });
  }
  function panBack(ax, ay, k, key) {
    const s = backOut(k); if (s < .02) return;
    boilSeed('panB' + key);
    paint(rrPts(ax - 9 * s, ay - 36 * s, 18 * s, 38 * s, 5, .6), { wash: C.grid, ink: C.ink, sw: .8 });
    paint(ellPts(ax, ay - 66 * s, 118 * s, 13 * s, 24, .6), { wash: C.bezel, ink: C.ink, sw: .8 });
  }
  function panFront(ax, ay, k, key) {
    const s = backOut(k); if (s < .02) return;
    boilSeed('panF' + key);
    const P = []; for (let i = 0; i <= 16; i++) { const th = Math.PI * i / 16; P.push([ax + 118 * s * Math.cos(th), ay - 66 * s + 40 * s * Math.sin(th)]); }
    paint(P, { wash: C.panelHi, ink: C.ink, sw: 1 });
  }
  // a depth bar, in the look of book(): bids solid Up green, asks dim and hollow
  function bar(x, y, len, h, side, key, rot = 0, sq = 0) {
    boilSeed('blk' + key);
    const bid = side === 'bid';
    push(); translate(x, y); rotate(rot); scale(1 + sq * .5, 1 - sq);
    paint(rrPts(-len / 2, -h / 2, len, h, 8, .8), bid ? { wash: C.up, ink: C.ink, sw: .6 } : { wash: mixCol(C.upDk, C.panel, .35), ink: mixCol(C.up, C.panel, .3), sw: .6 });
    pop();
  }

  // ---------- the Up book (a small copy of C's ladder) ----------
  const BK = { x: 320, w: 300, h: 324 };
  const bookRow = (by, b) => b.side === 'ask' ? by + 86 + b.i * 28 : by + 214 + b.i * 28;
  const inBook = (by, b) => { const len = (BK.w - 60) * b.s; return [b.side === 'ask' ? BK.x + BK.w - 30 - len / 2 : BK.x + 30 + len / 2, bookRow(by, b), len]; };
  function bookY(t) {
    const drop = lerp(-420, 238, backOut(seg(t, 37.3, 37.6)));
    return drop + 12 * spring(t, tWeigh - .02, 8, 20) - 780 * easeIn(seg(t, 38.12, 38.42));
  }
  function upBook(t, by) {
    if (by < -380) return;
    boilSeed('fbook');
    paint(rrPts(BK.x, by, BK.w, BK.h, 24, 1.5), { wash: C.panel, ink: C.ink, sw: 1.1 });
    const cx = BK.x + BK.w / 2, cy = by + 40, hw = BK.w - 32, ht = 54, a = 19;
    paint(rrPts(cx - hw / 2, cy - ht / 2, hw, ht, 18, 1), { wash: C.up, ink: null });
    paint([[cx, cy - a], [cx + a * .9, cy + a * .1], [cx + a * .33, cy + a * .1], [cx + a * .33, cy + a], [cx - a * .33, cy + a], [cx - a * .33, cy + a * .1], [cx - a * .9, cy + a * .1]], { wash: C.cream, ink: null });
    inkLine([[BK.x + 30, by + 200], [BK.x + BK.w - 30, by + 200]], .5, C.grid, 'inkfine', 0);   // the spread
  }

  // ---------- the Up price tag and the dotted arrow it drifts up ----------
  const AR = { y0: 872, y1: 292 };
  const pathX = y => PX + 20 * Math.sin((AR.y0 - y) / 68);
  const TAG = { w: 196, h: 172, y0: 612, y1: 414 };
  const tagK = t => seg(t, tPrice - .04, tPrice + .16);
  const tagDrift = t => ease(seg(t, tTends + .08, tUpW));
  const tagPos = t => { const y = lerp(TAG.y0, TAG.y1, tagDrift(t)) - 3 * wob(t, .9); return [pathX(y), y]; };
  function dottedArrow(t) {
    const d = ease(seg(t, tTends - .16, tTends + .16)); if (d <= 0) return;
    boilSeed('farrow');
    const n = 26;
    for (let i = 0; i < n; i++) {
      const q = i / (n - 1); if (q > d) break;
      const y = lerp(AR.y0, AR.y1 + 30, q), r = 5.5 * clamp((d - q) * 12);
      paint(ellPts(pathX(y) + jit(1.5), y, r, r, 8), { wash: C.cream, washOp: 200, ink: null });
    }
    const hk = seg(d, .85, 1);
    if (hk > 0) {
      const s = backOut(hk), hx = pathX(AR.y1 + 20), hy = AR.y1;
      paint([[hx, hy - 30 * s], [hx + 24 * s, hy + 12 * s], [hx - 24 * s, hy + 12 * s]], { wash: C.cream, washOp: 220, ink: C.ink, sw: .7 });
    }
  }
  function upTag(t) {
    const k = tagK(t); if (k <= 0) return;
    const s = backOut(k), [x, y] = tagPos(t), w = TAG.w * s, h = TAG.h * s;
    const cents = Math.round(lerp(60, 63, tagDrift(t)));
    const pulse = t < tTends ? .25 : t < tUpW ? .25 + .45 * seg(t, tTends, tTends + .3) : .35 + .65 * Math.exp(-(t - tUpW) * 3);
    button(x - w / 2, y - h / 2, w, h, 'Up', cents, C.up, C.upDk, pulse, 'ftag');
  }

  // ---------- camera: settle, a slow push, tilt up with the tag, then push into it ----------
  function camera(t) {
    const y = kf(t, [[CUT.F, 700], [38.15, 700], [38.95, 772], [40.9, 766], [tUpW, 738]], ease) + 5 * spring(t, tHeavy + .28, 6, 13);
    const z = kf(t, [[CUT.F, 1], [38.15, 1.0], [38.95, 1.1], [40.9, 1.12], [tUpW, 1.15]], ease);
    const p = seg(t, tPush, CUT.G);
    if (p <= 0) return cam(t, 470, y, z);
    const [tx, ty] = tagPos(t), k = easeOut(p);
    cam(t, lerp(470, tx, k), lerp(y, ty + TAG.h * .06, k), Math.exp(lerp(Math.log(z), Math.log(9), easeIn(p))));
  }

  function shotF(t, lt, dur) {
    room(t, { plate: 'stage', bloom: 0 });
    camera(t);
    // light: the pans glow as the formula names them (bids, asks, then both)
    const env = (a, b, c, d) => Math.min(seg(t, a, b), 1 - seg(t, c, d));
    const gBoth = env(tOver - .05, tOver + .12, tBoth + .05, tBoth + .3);
    const gBid = Math.max(env(tBids - .05, tBids + .1, tAsks - .12, tAsks + .05), gBoth, .8 * env(tMore - .1, tMore + .05, tHeavy + .4, tHeavy + .9));
    const gAsk = Math.max(env(tAsks - .08, tAsks + .08, tOver - .12, tOver), gBoth);
    const [lx, ly] = panAt(t, 'bid'), [rx, ry] = panAt(t, 'ask');
    if (gBid > 0) glow(lx, ly - 110, 250, '#6BE08E', .75 * gBid);
    if (gAsk > 0) glow(rx, ry - 110, 250, '#E9E3D0', .5 * gAsk);
    glow(PX, 560, 520, '#1F6B45', .35 + .1 * wob(t, .2));   // the stage's own breathing light

    // the hill flattens into the beam (with a sag), a fulcrum grows under it, the pans pop onto its ends
    const k = 1 - ease(seg(t, CUT.F, 37.6)) - .07 * Math.sin(Math.PI * seg(t, 37.45, 37.78));
    const kFul = seg(t, 37.4, 37.62), kPan = [seg(t, 37.48, 37.68), seg(t, 37.53, 37.73)];
    fulcrum(kFul);
    push(); translate(PX, PY); rotate(ang(t)); translate(-PX, -PY);
    feeHill(t, k);
    pop();
    if (kFul > .5) { boilSeed('bolt'); paint(ellPts(PX, PY, 13, 13, 12, .4), { wash: C.creamDim, ink: C.ink, sw: .8 }); }

    // the book, then its blocks: in the book, in flight, or in a pan
    const by = bookY(t);
    upBook(t, by);
    const landed = { bid: [], ask: [] }, flying = [];
    for (const b of POUR) {
      if (t < b.t0) { if (!b.more && by > -380) { const [x, y, len] = inBook(by, b); bar(x, y, len, 20, b.side, b.n); } continue; }
      if (t >= b.t1) landed[b.side].push(b); else flying.push(b);
    }
    for (const side of ['bid', 'ask']) {
      const [ax, ay] = panAt(t, side), pk = kPan[side === 'bid' ? 0 : 1];
      panBack(ax, ay, pk, side);
      for (const b of landed[side]) {
        const [x, y] = slot(t, side, b.j), age = t - b.t1;
        bar(x, y, LMAX * b.s, BH, side, b.n, 0, .32 * Math.exp(-age * 13) * Math.cos(age * 26));
      }
      panFront(ax, ay, pk, side);
    }
    for (const b of flying) {
      const q = seg(t, b.t0, b.t1), [x1, y1] = slot(t, b.side, b.j);
      if (b.more) {   // dropped from above: falls, stretched
        const y = lerp(-180, y1, easeIn(q)), x = x1 + (1 - q) * 30 * (hash(b.n) - .5);
        bar(x, y, LMAX * b.s, BH, b.side, b.n, .12 * (1 - q) * (hash(b.n + 4) - .5), -.28 * q);
      } else {        // poured out of the book on an arc, tumbling a little
        const [x0, y0, l0] = inBook(by, b), kk = q * (.55 + .45 * q), [x, y] = arcPt([x0, y0], [x1, y1], 110, kk);
        bar(x, y, lerp(l0, LMAX * b.s, kk), lerp(20, BH, kk), b.side, b.n, (b.side === 'bid' ? -1 : 1) * .5 * Math.sin(Math.PI * kk), -.12 * Math.sin(Math.PI * q));
      }
    }

    // the formula, while the voice reads it
    const fk = Math.min(seg(t, tBids - .04, tBids + .14), 1 - seg(t, 39.96, 40.1));
    if (fk > 0) pill('(bids − asks) ÷ (bids + asks)', PX, 600, 56, { k: fk, key: 'formula', w: 760 });

    // price tends to drift up: a dotted arrow out of the scale, and the Up tag partway up it
    dottedArrow(t);
    upTag(t);
    camEnd();

    // out: the Up tag's green fills the frame (G opens on this green and pulls back out of the Up button)
    const cover = seg(lt, dur - .12, dur);
    if (cover > 0) { flushLetters(); paint(rectPts(-40, -40, W + 80, H + 80), { wash: C.up, washOp: 255 * cover, ink: null }); }
  }
  shots([[CUT.F, shotF]]);
})();
