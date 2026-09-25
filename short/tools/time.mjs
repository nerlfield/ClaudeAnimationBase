// time.mjs: true per-frame cost of page snippets on software GL, including the GPU flush that toDataURL forces
// (renderSheet's own ms misses it). Usage: node short/tools/time.mjs '{"name": "room(t)", ...}'
import puppeteer from 'puppeteer-core';
const cases = JSON.parse(process.argv[2]);
const b = await puppeteer.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true, protocolTimeout: 0,
  args: ['--no-sandbox', '--allow-file-access-from-files', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--window-size=1920,1920'] });
const p = await b.newPage();
await p.goto('file:///home/user/ClaudeAnimationBase/short.html?render', { waitUntil: 'networkidle0' });
await p.waitForFunction('window.ready === true');
for (const [name, code] of Object.entries(cases)) {
  await p.evaluate(code => { window.LOOP = eval('(t) => {' + code + '}'); }, code);
  const ms = [];
  for (const t of [0.1, 0.2, 0.35]) { const t0 = Date.now(); await p.evaluate(t => window.renderAt(t, 'image/jpeg', .9).then(() => 0), t); ms.push(Date.now() - t0); }
  console.log(name.padEnd(12), ms.join(' '));
}
await b.close();
