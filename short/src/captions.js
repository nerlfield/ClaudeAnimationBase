// captions.js: burned-in captions, 1–3 words at a time, timed to the narration's word timestamps (WORDS in
// short/voice/words.js). Each chunk is [display text, how many spoken words it covers]. *word* marks the one key word
// in lime (C.neon). Numbers are spoken as words and shown as digits. Drawn over the paper grain (window.overlayLayer), so
// they stay crisp, in the band y 1130..1250 (SAFE.capY), clear of YouTube's buttons.
const CAPS = [
  // A1–A2
  ['This 15-minute', 2], ['Bitcoin bet', 2], ['just jumped', 2], ['from *50¢*', 3], ['to *80¢*', 2],
  ['The first buyers', 3], ['were watching', 2], ['another *screen*', 2],
  // B
  ['*Up* wins', 2], ['if Bitcoin ends', 3], ['at or *above*', 3], ['where it started', 3],
  ['One Up', 2], ['plus one Down', 3], ['is backed by', 3], ['*$1*', 2], ['and the winner', 3], ['takes it', 2],
  ['So *62¢*', 3], ['means a', 2], ['*62%* chance', 3],
  // C
  ['Each side has', 3], ['an *order book*', 3], ['*Bids* to buy', 3], ['*asks* to sell', 3], ['and a *spread*', 3], ['between', 1],
  // D
  ['You bid', 2], ['*60¢* on Up', 4], ['A stranger', 2], ['bids *40¢*', 2], ['on Down', 2], ['Nobody\'s *selling*', 2],
  ['But 60 + 40', 4], ['is *$1*', 3], ['so the exchange', 3], ['*mints*', 1], ['a fresh pair', 3], ['and fills', 2], ['you both', 2],
  // E
  ['You waited', 2], ['in the book', 3], ['so you pay', 3], ['*nothing*', 1],
  ['The stranger', 2], ['filled instantly', 2], ['so they pay', 3], ['up to *3%*', 4],
  ['And selling', 2], ['costs most', 2], ['at *50/50*', 2], ['Limitless says', 2], ['that discourages', 2], ['*flip-flopping*', 1],
  // F
  ['Now *weigh*', 2], ['the book', 2], ['Bids minus asks', 3], ['over both', 2], ['When bids', 2], ['are *heavier*', 2], ['price tends', 2], ['to drift up', 3],
  // G
  ['That other *screen?*', 3], ['*Binance*', 1], ['one of the fastest', 4], ['places Bitcoin', 2], ['moves show up', 3],
  ['Traders check it', 3], ['against the', 2], ['*Price to Beat*', 3], ['and the *clock*', 3], ['and buy', 2], ['when Up', 2], ['looks *cheap*', 2],
  // H
  ['But this market', 3], ['settles on', 2], ['Chainlink\'s', 1], ['*60-second* average', 2],
  ['A last-second', 2], ['spike', 1], ['*barely* moves it', 3], ['so chasing', 2], ['that candle', 2], ['can *burn* you', 3],
  // I
  ['Add fees', 2], ['and a half-second', 3], ['delay', 1], ['and you can', 3], ['lose your', 2], ['*whole stake*', 2],
  ['Then the close', 3], ['becomes the', 2], ['next round\'s', 2], ['*Price to Beat*', 3],
];
// Resolve each chunk to a time span: it appears with its first word (a hair early) and holds until the next one starts,
// or 0.35 s after its last word if a pause follows.
const CAPTIONS = (() => {
  const out = []; let i = 0;
  for (const [s, n] of CAPS) { out.push({ s, a: WORDS[i].start - .04, b: WORDS[i + n - 1].end }); i += n; }
  if (i !== WORDS.length) console.error(`captions cover ${i} words, narration has ${WORDS.length}`);
  for (let k = 0; k < out.length; k++) out[k].b = Math.min(out[k].b + .35, k + 1 < out.length ? out[k + 1].a : Infinity);
  return out;
})();

// Draw the caption at time t on the 2D compositor. Two-colour runs: plain words cream, *key* words lime.
function drawCaption(c, t) {
  const cap = CAPTIONS.find(x => t >= x.a && t < x.b); if (!cap) return;
  const age = t - cap.a, k = backOut(clamp(age / .1)), size = 86;
  const runs = cap.s.split('*').map((s, j) => ({ s, hi: j % 2 === 1 })).filter(r => r.s);
  c.save(); c.font = `${size}px ${FONT}`; c.textBaseline = 'middle'; c.lineJoin = 'round';
  const widths = runs.map(r => c.measureText(r.s).width), total = widths.reduce((a, b) => a + b, 0);
  const fit = Math.min(1, 820 / total);   // never wider than the safe band
  c.translate(W / 2, SAFE.capY); c.scale(k * fit, k * fit);
  let x = -total / 2;
  runs.forEach((r, j) => {
    c.shadowColor = 'rgba(20,18,24,.55)'; c.shadowOffsetY = 7; c.shadowBlur = 10;
    c.lineWidth = 15; c.strokeStyle = C.ink; c.strokeText(r.s, x, 0);
    c.shadowColor = 'transparent'; c.fillStyle = r.hi ? C.neon : C.cream; c.fillText(r.s, x, 0);
    x += widths[j];
  });
  c.restore();
}
// Small top pills for the required disclaimers, below the top 10% of the frame.
function drawTag(c, s, alpha) {
  if (alpha <= 0) return;
  c.save(); c.globalAlpha = clamp(alpha); c.font = `34px ${FONT}`; c.textBaseline = 'middle';
  const w = c.measureText(s).width + 44, x = W / 2 - w / 2, y = 1330;   // under the captions, above YouTube's UI
  c.fillStyle = 'rgba(20,18,24,.72)'; c.beginPath(); c.roundRect(x, y - 27, w, 54, 27); c.fill();
  c.fillStyle = C.cream; c.fillText(s, x + 22, y + 2);
  c.restore();
}
const TAGS = [
  { s: 'Not financial advice', a: 58.95, b: 61.2 },
  { s: 'Unofficial explainer · not affiliated with Limitless', a: 62.9, b: 99 },
];
window.overlayLayer = (c, t) => {
  if (window.LOOP && !window.LOOP.captions) return;
  const tt = window.LOOP ? window.LOOP.captions(t) : t;
  for (const g of TAGS) drawTag(c, g.s, Math.min(seg(tt, g.a, g.a + .2), 1 - seg(tt, g.b - .2, g.b)));
  drawCaption(c, tt);
};
