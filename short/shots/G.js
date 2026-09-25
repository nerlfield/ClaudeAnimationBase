// G.js: THE OTHER SCREEN, the hook's answer (42.414 → 51.185). See STORYBOARD.md, shot G.
//   In: F's Up tag filled the frame with green; G opens deep inside the market screen's Up button (63¢, the tag's price)
//   and pulls back fast out of it to the desk: the reverse of A's push. You're watching the card; on "other" your eyes
//   drop to the lower screen and its "?" tag pulses; the camera follows your look and the tag flips to BINANCE on the
//   beat just before "Binance" (you do a take). Held, then the camera opens up to both screens: the ticker jumps on
//   "moves", an arc arrow runs from its live dot up to the card and, a beat later, Up follows (57¢ → 62¢). "Price to
//   Beat": a dashed line draws across the ticker, BTC sitting above it. "The clock": the card's clock swells (3:00 left).
//   "Buy when Up looks cheap": a thought bubble over you fills your odds dial to 75% past the market's 62%, the Up button
//   (62¢) lights, and you leap onto the ticker's bezel and slap Up on the beat of "cheap".
//   Out: a push into the ticker screen, ending on a full-frame C.panel (the G→H contract).
(() => {
  const tBin = wt('G2', 'binance'), tMoves = wt('G2', 'moves');
  const tPrice = wt('G3', 'price'), tClock = wt('G3', 'clock'), tBuy = wt('G3', 'buy');
  const tFlip = 43.446;                 // the beat just before "Binance": the tag's flip lands here
  const tJump = tMoves - .04;           // the ticker lands its jump just before "moves"
  const tFollow = 46.026;               // a beat later, Up follows
  const tTap = 50.6, tPush = CUT.H - .335;

  // ---------- the market, in closed form ----------
  const PTB = 84468, LO = 84340, HI = 84680;
  const btc = tt => btcPath(tt, 84482) - 44 * ease(seg(tt, 44.2, 45.2)) + 165 * easeOut(seg(tt, tJump - .2, tJump));
  const upAt = t => t < 44.4 ? 63 : t < tFollow ? lerp(63, 57, ease(seg(t, 44.4, 45.5))) : lerp(57, 62, easeOut(seg(t, tFollow, tFollow + .28)));
  const clockAt = t => 180.9 - (t - tClock);   // reads 3:00 on "clock"
  const env = (t, a, b, c, d) => Math.min(seg(t, a, b), 1 - seg(t, c, d));
  const kick = (t, t0, k) => t < t0 ? 0 : Math.exp(-(t - t0) * k);

  // ---------- where things are (world = desk coordinates, see sets.js) ----------
  const TAG = [DESK.tx + DESK.tw - 120, DESK.ty + 36];            // the ticker's name tag
  const CLK = [CARD.x + CARD.w - 92, CARD.y + 88];                 // the card's clock
  const HOME = [DESK.youX, DESK.top], LEDGE = [427, DESK.ty - 16]; // you: on the desk, then on the ticker's top bezel
  const HIT = [352, 611];                                           // where your arm meets the Up button
  const BUB = [786, 596];                                           // the thought bubble

  // ---------- camera: pull back out of the Up button, follow your look to the tag, open up, push into the ticker ----------
  // keys: [t, x, y, zoom, ease for the pan, ease for the zoom]
  const CAMK = [
    [CUT.G, UPBTN.cx, UPBTN.cy, 9], [42.85, 470, 640, .97, ease, easeOut], [43.02, 470, 640, 1],
    [43.42, 591, 884, 1.85], [44.35, 588, 878, 1.93], [45.25, 432, 652, 1.04], [46.7, 440, 664, 1.07],
    [47.75, 440, 742, 1.15], [48.72, 446, 736, 1.17], [49.0, 510, 684, 1.08], [tPush, 516, 680, 1.11],
    [CUT.H, DESK.tx + DESK.tw / 2, 850, 9, easeOut, easeIn],
  ];
  function camera(t) {
    let i = 0; while (i + 1 < CAMK.length && t >= CAMK[i + 1][0]) i++;
    const a = CAMK[i], b = CAMK[Math.min(i + 1, CAMK.length - 1)], p = seg(t, a[0], b[0]);
    const ep = (b[4] || ease)(p), ez = (b[5] || ease)(p);
    cam(t, lerp(a[1], b[1], ep), lerp(a[2], b[2], ep), Math.exp(lerp(Math.log(a[3]), Math.log(b[3]), ez)));
  }

  // ---------- you ----------
  const gaze = t => kf(t, [
    [CUT.G, [.6, -.9]], [42.76, [.6, -.9]], [42.86, [.9, .85]],     // "that other screen": down to the "?"
    [45.95, [.9, .8]], [46.07, [.7, -.85]],                         // follow the arrow up to the Up button
    [47.72, [.7, -.85]], [47.82, [.9, .75]],                        // down to the Price to Beat
    [48.92, [.9, .75]], [49.0, [.45, -1]],                          // up to the clock
    [49.56, [.45, -1]], [49.64, [0, -1]],                           // up into the thought
    [49.95, [0, -1]], [50.04, [.9, -.5]],                           // at the Up button: decided
  ], ease);
  const MOOD = [[CUT.G - 1, 'neutral'], [42.8, 'suspicious'], [tFlip + .04, 'surprised'], [44.3, 'smug'],
                [47.75, 'thinking', { emote: null }], [49.97, 'determined'], [tTap + .04, 'happy']];
  const T_CROUCH = 50.08, T_OFF = 50.24, T_LAND = 50.5;
  function trader(t) {
    const m = actYou(t, MOOD, { take: .8 }), [lx, ly] = gaze(t);
    let x = HOME[0], y = HOME[1], o = { ...m, lookX: lx, lookY: ly, view: 'q', flip: true };
    if (t < T_OFF) {   // at the desk; a crouch before the leap
      const c = ease(seg(t, T_CROUCH, T_OFF - .02));
      o = { ...o, ...(t > 50.1 ? turn(t, 50.1, 50.2, -.125, -.25) : {}), sq: (o.sq || 0) + .3 * c, aL: lerp(o.aL ?? .2, -.6, c), aR: lerp(o.aR ?? .2, -.6, c) };
    } else if (t < T_LAND) {   // the leap, on an arc, stretched, arm up
      const k = seg(t, T_OFF, T_LAND);
      [x, y] = arcPt(HOME, LEDGE, 170, k * (.6 + .4 * k));
      o = { ...o, view: 'side', flip: true, noShadow: true, dy: 0, sq: -.18 * Math.sin(Math.PI * k) + .12 * (1 - seg(k, 0, .25)), rot: -.22 * Math.sin(Math.PI * k), aL: 1.7, smear: .35 * Math.sin(Math.PI * k), smearDir: -1 };
    } else {   // landed on the ticker's bezel: the slap, then a happy bounce with the arm on the button
      const age = t - T_LAND, slap = seg(t, T_LAND + .02, tTap);
      [x, y] = LEDGE;
      o = { ...o, view: 'side', flip: true, sq: (o.sq || 0) + .26 * kick(t, T_LAND, 11), dy: t < tTap + .1 ? 0 : o.dy,
            aL: t < tTap + .22 ? lerp(1.7, 1.05, easeIn(slap)) + .1 * spring(t, tTap, 9, 30) : lerp(1.05, o.aL ?? .4, ease(seg(t, tTap + .22, tTap + .45))) };
      if (age < .05) o.smear = 0;
    }
    you(x, y, 21, o);
  }

  // ---------- the thought: your odds dial fills past the market's 62% to 75% ----------
  function bubble(t) {
    const kIn = seg(t, tBuy + .03, tBuy + .2), kOut = seg(t, 50.3, 50.46);
    const tails = [[808, 868, 9, tBuy - .06], [816, 832, 13, tBuy - .02], [808, 786, 19, tBuy + .02]];
    tails.forEach(([x, y, r, t0], i) => {
      const k = Math.min(seg(t, t0, t0 + .12), 1 - seg(t, 50.2 + i * .03, 50.3 + i * .03)); if (k <= 0) return;
      boilSeed('tail' + i); paint(ellPts(x, y, r * backOut(k), r * backOut(k), 12, .6), { wash: C.cream, ink: C.ink, sw: .8 });
    });
    const k = Math.min(kIn, 1 - kOut); if (k <= 0) return;
    const s = backOut(k), R = 122 * s, [bx, by] = BUB, P = [];
    for (let i = 0; i < 44; i++) { const a = i / 44 * TAU, rr = R * (1 + .075 * Math.abs(Math.sin(a * 5 + .4))); P.push([bx + Math.cos(a) * rr, by + Math.sin(a) * rr * .92]); }
    boilSeed('bubble');
    paint(P, { wash: C.cream, ink: C.ink, sw: 1.1 });
    // the dial: a dark UI disc, the market's 62% in dark green, your extra 13% in bright green
    const r = 70 * s, p62 = ease(seg(t, tBuy + .12, tBuy + .3)), p75 = ease(seg(t, tBuy + .32, tBuy + .46));
    boilSeed('dial');
    paint(ellPts(bx, by, r, r, 30, .5), { wash: C.panel, ink: C.ink, sw: .9 });
    const wedge = (a0, a1, col) => { if (a1 - a0 < .002) return; const Q = [[bx, by]], n = Math.max(2, Math.ceil(40 * (a1 - a0))); for (let i = 0; i <= n; i++) { const a = -Math.PI / 2 + TAU * lerp(a0, a1, i / n); Q.push([bx + Math.cos(a) * r * .9, by + Math.sin(a) * r * .9]); } paint(Q, { wash: col, ink: null }); };
    wedge(0, .62 * p62, C.upDk);
    if (p75 > 0) { glow(bx, by, r * 1.6, '#6BE08E', .5 * p75); wedge(.62, .62 + .13 * p75, C.upLt); }
    paint(ellPts(bx, by, r * .56, r * .56, 24, .4), { wash: C.panel, ink: null });
    const ta = -Math.PI / 2 + TAU * .62;   // the market's mark
    if (p62 > .95) inkLine([[bx + Math.cos(ta) * r * .5, by + Math.sin(ta) * r * .5], [bx + Math.cos(ta) * r * 1.02, by + Math.sin(ta) * r * 1.02]], .9, C.cream, 'ink', 0);
    const tk = seg(t, tBuy + .36, tBuy + .5);
    if (tk > 0) txt('75%', bx, by + 2, 34 * s * backOut(tk), C.cream, { ink: false });
  }

  // ---------- the arc arrow: the ticker moves, the Up price follows ----------
  function followArrow(t, tk) {
    const d = easeOut(seg(t, tJump + .03, tFollow + .02)), back = ease(seg(t, 46.55, 46.8));
    if (d <= 0 || back >= 1) return;
    // a curve that rises off the live dot, runs through the gap between the screens and turns up into the Up button
    const B = [[DESK.tx + DESK.tw - 60, tk.Y(btc(Math.min(t, 46.2)))], [780, 700], [420, 700], [300, 626]], n = 22, P = [];
    const bez = k => { const a = 1 - k, w = [a * a * a, 3 * a * a * k, 3 * a * k * k, k * k * k]; return [0, 1].map(c => w.reduce((s, wi, j) => s + wi * B[j][c], 0)); };
    for (let i = 0; i <= n; i++) P.push(bez(lerp(back, d, i / n)));
    boilSeed('farrow');
    inkLine(P, 3.2, C.ink, 'ink', .5);
    inkLine(P, 2, C.tape, 'ink', .5);
    const [hx, hy] = P[n], [qx, qy] = P[n - 1], a = Math.atan2(hy - qy, hx - qx), L = 30;
    paint([[hx + Math.cos(a) * 8, hy + Math.sin(a) * 8], [hx - Math.cos(a - .5) * L, hy - Math.sin(a - .5) * L], [hx - Math.cos(a + .5) * L, hy - Math.sin(a + .5) * L]], { wash: C.tape, ink: C.ink, sw: .8 });
  }

  // ---------- the Price to Beat: a dashed line drawn across the ticker, and its name ----------
  function priceToBeat(t, tk) {
    const d = ease(seg(t, tPrice - .2, tPrice + .06)); if (d <= 0) return;
    const y = tk.Y(PTB), x0 = DESK.tx + 30, x1 = DESK.tx + DESK.tw - 40;
    boilSeed('ptb');
    dashed(x0, y, lerp(x0, x1, d), y, C.cream, .9);
    const pk = env(t, tPrice - .1, tPrice + .08, 48.84, 48.98);
    if (pk > 0) pill('Price to Beat', DESK.tx + 190, y + 42, 42, { k: pk, key: 'ptb', bg: C.bezel });
  }

  // ---------- the clock swells on "clock" ----------
  function clockSwell(t) {
    const k = env(t, tClock - .08, tClock + .1, 49.48, 49.62); if (k <= 0) return;
    glow(CLK[0], CLK[1], 200, '#E9E3D0', .6 * k);
    clock(CLK[0], CLK[1], 62 * (1 + .8 * backOut(k)), clockAt(t));
  }

  function shotG(t, lt, dur) {
    camera(t);
    const up = upAt(t);
    const named = ease(seg(t, 43.3, 43.47));
    const tagPulse = Math.max(.8 * env(t, 42.8, 42.95, 43.28, 43.36) * (1 + .15 * Math.sin(t * 16)), .9 * kick(t, tFlip - .02, 1.1) * (t > tFlip - .02 ? 1 : 0));
    const cardPulse = Math.max(.12 + .05 * Math.sin(t * 5), kick(t, tFollow, 2.2), .7 * env(t, 49.9, 49.98, 50.2, 50.34), kick(t, tTap, 1.8));
    const tk = desk(t, {
      card: { up, clock: clockAt(t), hi: 'up', pulse: cardPulse, example: true },
      fn: btc, lo: LO, hi: HI, named, tagPulse,
      upGlow: Math.max(kick(t, tFollow, 2), kick(t, tTap, 1.6)),
      tickGlow: Math.max(.5 * env(t, 42.85, 43.0, 43.6, 44.4), kick(t, tJump - .05, 2.4)),
      hide: 1,
    });
    priceToBeat(t, tk);
    followArrow(t, tk);
    clockSwell(t);
    trader(t);
    bubble(t);
    if (t > tTap && t < tTap + .45) {   // the buy: a burst off the Up button where your arm lands
      const a = (t - tTap) / .45;
      boilSeed('tapsparks');
      for (let i = 0; i < 8; i++) {
        const ang = Math.PI * .55 + (i - 3.5) * .42, d = 40 + 110 * easeOut(a);
        paint(starPts(HIT[0] + Math.cos(ang) * d, HIT[1] + Math.sin(ang) * d * .85, 15 * (1 - a), .3, 4, ang), { wash: C.upLt, washOp: 255 * (1 - a), ink: null });
      }
    }
    camEnd();
    // in: F's green, now the Up button's face, clears as we pull back out of it
    const open = 1 - seg(lt, 0, .1);
    // out: the ticker's panel fills the frame (H opens on full-frame C.panel)
    const cover = seg(lt, dur - .12, dur);
    if (open > 0 || cover > 0) flushLetters();
    if (open > 0) paint(rectPts(-40, -40, W + 80, H + 80), { wash: C.up, washOp: 255 * open, ink: null });
    if (cover > 0) paint(rectPts(-40, -40, W + 80, H + 80), { wash: C.panel, washOp: 255 * cover, ink: null });
  }
  shots([[CUT.G, shotG]]);
})();
