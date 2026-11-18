// Uso: node render.js  ->  Presentazione_Ecosistema.pdf (accanto a presentazione.html)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const html = path.resolve(__dirname, 'presentazione.html');
  const out = path.resolve(__dirname, 'Presentazione_Ecosistema.pdf');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF scritto: ' + out);
})();
