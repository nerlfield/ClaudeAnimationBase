// A.js: THE JUMP (0 → 5.269). See STORYBOARD.md, shot A.
//   Frame 0 is mid-action: a fresh round (14:59 left, Up 50¢), the camera already pushing in, the ticker below
//   already surging (the cause shows first). Up trembles, dips (anticipation), then rockets 50 → 80¢ with an
//   overshoot, landing on the beat at 2.69 s, just before "eighty". The camera pulls back; you pop up from behind the
//   desk looking at the price, then your eyes drop to the ticker whose name tag is a "?" (the open question).
//   Out: a push through the Up button; its green fills the frame, and B opens from that green.
(() => {
  const tGo = 1.95, tLand = 2.69, tPop = wt('A2', 'buyers') - .1, tLook = wt('A2', 'another'), tPush = 4.93;
  const btc = HOOK0.btc;   // the fast screen moves first
  // Up: holds 50, dips to 49 (anticipation), accelerates like a rocket, lands on 80 at tLand, then a small spring settle
  const upAt = t => t < 1.55 ? 50 : t < tGo ? lerp(50, 49, ease(seg(t, 1.55, tGo))) : t < tLand ? lerp(49, 80, Math.pow(seg(t, tGo, tLand), 1.8))
                  : 80 + 2.4 * spring(t, tLand, 9, 22);
  // camera: push in (already moving at frame 0) → hold → pull back to show you → push through the Up button
  const LZ = Math.log;
  function camera(t) {
    const cx = kf(t, [[0, HOOK0.cam[0]], [2.8, 300], [3.3, 300], [4.3, FRAME.WIDE[0]], [tPush, FRAME.WIDE[0] - 10], [CUT.B, UPBTN.cx]], ease);
    const cy = kf(t, [[0, HOOK0.cam[1]], [2.8, 560], [3.3, 560], [4.3, FRAME.WIDE[1]], [tPush, FRAME.WIDE[1]], [CUT.B, UPBTN.cy]], ease);
    const z = t < tPush ? Math.exp(kf(t, [[0, LZ(HOOK0.cam[2])], [2.8, LZ(1.26)], [3.3, LZ(1.26)], [4.3, LZ(1)]], ease))
                        : Math.exp(lerp(LZ(1), LZ(9), easeIn(seg(t, tPush, CUT.B))));
    // during the push, pan towards the button faster than the zoom so it stays centred
    const k = easeOut(seg(t, tPush, CUT.B));
    // cam() centres on the stage; at the end of the push the button must sit at the FRAME centre to fill it
    const x = t < tPush ? cx : lerp(FRAME.WIDE[0] - 10, UPBTN.cx - (W / 2 - STAGE.x) / z, k), y = t < tPush ? cy : lerp(FRAME.WIDE[1], UPBTN.cy - (H / 2 - STAGE.y) / z, k);
    const land = t > tLand ? shakeXY(t, 5 * Math.exp(-(t - tLand) * 9)) : [0, 0];
    cam(t, x + land[0], y + land[1], z);
  }

  function shotA(t, lt, dur) {
    camera(t);
    const up = upAt(t), rocketing = t >= tGo && t < tLand;
    const pulse = t < tGo ? .12 + .1 * Math.sin(t * 34) : rocketing ? .6 + .4 * seg(t, tGo, tLand) : .25 + .75 * Math.exp(-(t - tLand) * 2.2);
    const tagPulse = t > tLook - .1 ? Math.exp(-(t - tLook) * 1.4) * clamp((t - tLook + .1) / .15) * (1 + .15 * Math.sin((t - tLook) * 16)) : 0;
    const mood = actYou(t, [[0, 'neutral'], [tPop, 'smug', { lookX: .9, lookY: -.9, view: 'q', flip: true }],
                              [tLook, 'suspicious', { lookX: .9, lookY: .85, view: 'q', flip: true }]], { take: .6 });
    const hide = t < tPop ? 1 : 1 - backOut(seg(t, tPop, tPop + .32));
    desk(t, {
      card: { up, clock: 899 - t, hi: 'up', pulse, example: true },
      upGlow: rocketing ? 1 : Math.exp(-Math.max(0, t - tLand) * 1.5),
      tickGlow: .6 * (1 - seg(t, 1.8, 2.6)),
      fn: btc, lo: 84360, hi: 84660, tagPulse,
      hide, you: { ...mood, view: 'q', flip: true },
    });
    // the moment it lands: a burst of sparks off the Up button
    if (t > tLand && t < tLand + .5) {
      const a = (t - tLand) / .5;
      boilSeed('sparks');
      for (let i = 0; i < 9; i++) {
        const ang = -Math.PI / 2 + (i - 4) * .36, d = 90 + 150 * easeOut(a);
        paint(starPts(UPBTN.cx + Math.cos(ang) * d, UPBTN.cy - 40 + Math.sin(ang) * d * .8, 16 * (1 - a), .3, 4, ang), { wash: C.upLt, washOp: 255 * (1 - a), ink: null });
      }
    }
    camEnd();
    // out: the Up button's green fills the frame (B opens from this green)
    const cover = seg(lt, dur - .07, dur - .01);
    if (cover > 0) { flushLetters(); paint(rectPts(-40, -40, W + 80, H + 80), { wash: C.up, washOp: 255 * cover, ink: null }); }
  }
  shots([[CUT.A, shotA]]);
})();
