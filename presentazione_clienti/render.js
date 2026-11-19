// Uso: node render.js
// Senza contatti nell'HTML scrive «PDF servizi ecosistema.pdf» (il file tracciato nel repo, che è
// pubblico); con i contatti (build.py --con-contatti) scrive SOLO in privato/, ignorato da git, e
// rifiuta qualsiasi altro percorso (bot #384 V-1).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const html = path.resolve(__dirname, 'presentazione.html');
  const conContatti = fs.readFileSync(html, 'utf8').includes('class="cts"');
  const nome = 'PDF servizi ecosistema.pdf';
  const out = path.resolve(__dirname, conContatti ? path.join('privato', nome) : nome);
  if (conContatti && !out.startsWith(path.resolve(__dirname, 'privato') + path.sep)) {
    console.error('STOP: PDF con contatti personali fuori da privato/');
    process.exit(1);
  }
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF scritto: ' + out);
})();
