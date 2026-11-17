/* Gas · CRM — dashboard in tempo reale.
 * Regola di sicurezza: i dati non diventano MAI HTML. Si costruisce il DOM con
 * createElement + textContent (helper `el`), niente innerHTML con dati. */
'use strict';

const S = {
  dati: null, tab: 'panoramica', filtro: 'tutti', cerca: '', ordina: { campo: 'nome', verso: 1 },
  cliente: null, clienteDati: null, grafico: 'commissioni', bozze: {}, live: false,
  rinviato: false, modale: null, eventiVisti: new Set(), stream: null, selezionati: new Set(),
};
const SCHEDE = [
  ['panoramica', 'Panoramica', '◈'], ['clienti', 'Clienti', '◉'],
  ['opportunita', 'Opportunità', '◎'], ['servizi', 'Servizi', '◇'],
];
const TIPI = { cross_sell: 'Nuovo servizio', aumento_capitale: 'Aumento capitale', referral: 'Presenta un amico' };
const STATI_PROP = {
  da_approvare: 'Da approvare', inviata: 'Inviata', accettata: 'Accettata', rifiutata: 'Rifiutata',
  senza_risposta: 'Senza risposta', scartata: 'Scartata', superata: 'Superata',
};
const ICONE_STATO = { accettata: '✓', rifiutata: '✕', senza_risposta: '…', scartata: '–', superata: '↷' };
const TIPI_MOV = { deposito: 'Deposito', prelievo: 'Prelievo', profitto: 'Profitto', perdita: 'Perdita', commissione: 'Commissione' };
const MODELLI = {
  percentuale_profitto: '% sul profitto', percentuale_capitale_annua: '% annua sul capitale', fisso_mensile: 'Fisso al mese',
};

/* ------------------------------------------------------------------ utilità DOM */
function el(tag, props, ...figli) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') e.className = v;
    else if (k === 'testo') e.textContent = v;
    else if (k === 'stile') Object.assign(e.style, v);
    else if (k === 'dataset') Object.assign(e.dataset, v);
    else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2), v);
    else if (k === 'value') e.value = v;
    else if (k === 'checked') e.checked = !!v;
    else e.setAttribute(k, v === true ? '' : String(v));
  }
  for (const f of figli.flat(Infinity)) {
    if (f === null || f === undefined || f === false) continue;
    e.append(f instanceof Node ? f : document.createTextNode(String(f)));
  }
  return e;
}
const NS = 'http://www.w3.org/2000/svg';
function sv(tag, attrs, ...figli) {
  const e = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) if (v !== null && v !== undefined) e.setAttribute(k, String(v));
  for (const f of figli.flat()) if (f) e.append(f instanceof Node ? f : document.createTextNode(String(f)));
  return e;
}
const colore = (slot) => `var(--s${((slot % 8) + 8) % 8})`;

/* ------------------------------------------------------------------ formati */
// useGrouping 'always': in italiano Intl non separa le migliaia sotto i 10.000 («3449 €»)
const fEuro = new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', useGrouping: 'always' });
const fEuro0 = new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0, useGrouping: 'always' });
const euro = (c) => fEuro.format((c || 0) / 100);
const euro0 = (c) => fEuro0.format(Math.round((c || 0) / 100));
const euroSegno = (c) => (c > 0 ? '+' : c < 0 ? '−' : '') + euro0(Math.abs(c || 0));
function compatto(c) {
  const v = Math.abs((c || 0) / 100);
  const s = v >= 1e6 ? (v / 1e6).toLocaleString('it-IT', { maximumFractionDigits: 1 }) + ' M'
    : v >= 1e4 ? (v / 1e3).toLocaleString('it-IT', { maximumFractionDigits: 0 }) + 'K'
      : v >= 1e3 ? (v / 1e3).toLocaleString('it-IT', { maximumFractionDigits: 1 }) + 'K'
        : v.toLocaleString('it-IT', { maximumFractionDigits: 0 });
  return (c < 0 ? '−' : '') + s + ' €';
}
const pct = (bp) => (bp === null || bp === undefined) ? '—'
  : (bp / 100).toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 2 }) + '%';
function dataBreve(iso) {
  if (!iso) return '—';
  const d = new Date(iso.length <= 10 ? iso + 'T12:00:00' : iso);
  return d.toLocaleDateString('it-IT', { day: 'numeric', month: 'short', year: '2-digit' });
}
function ora(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  const oggi = new Date();
  return d.toDateString() === oggi.toDateString()
    ? d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' })
    : d.toLocaleDateString('it-IT', { day: 'numeric', month: 'short' });
}
const oggiIso = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};
function linkSicuro(u) { return typeof u === 'string' && u.startsWith('https://wa.me/') ? u : null; }

/* ------------------------------------------------------------------ rete */
async function api(percorso, corpo) {
  const opz = { credentials: 'same-origin', headers: {} };
  if (corpo !== undefined) {
    opz.method = 'POST';
    opz.headers['Content-Type'] = 'application/json';
    opz.headers['X-Gas-CRM'] = '1';
    opz.body = JSON.stringify(corpo);
  }
  const r = await fetch(percorso, opz);
  let j = null;
  try { j = await r.json(); } catch (_) { j = null; }
  if (r.status === 401 && percorso !== '/api/login') { mostraAccesso(); throw new Error('Accesso richiesto'); }
  if (!r.ok) throw new Error((j && j.errore) || `Errore ${r.status}`);
  return j;
}
function avviso(testo, tipo) {
  const t = el('div', { class: 'toast ' + (tipo || '') , testo });
  document.getElementById('toasts').append(t);
  setTimeout(() => t.remove(), tipo === 'errore' ? 7000 : 3800);
}
async function esegui(fn, ok) {
  try { const r = await fn(); if (ok) avviso(ok, 'ok'); return r; } catch (e) { avviso(e.message, 'errore'); return null; }
}

/* ------------------------------------------------------------------ accesso */
function mostraAccesso(msg) {
  chiudiStream();
  const campo = el('input', { type: 'password', placeholder: 'Token di accesso (GAS_CRM_TOKEN)', autocomplete: 'current-password' });
  const errore = el('div', { class: 'suggerimento', testo: msg || '' });
  const entra = async (ev) => {
    ev.preventDefault();
    try { await api('/api/login', { token: campo.value.trim() }); avvia(); }
    catch (e) { errore.textContent = e.message; campo.select(); }
  };
  const app = document.getElementById('app');
  app.replaceChildren(el('div', { class: 'accesso' },
    el('form', { class: 'carta', onsubmit: entra },
      el('div', { class: 'logo' }, el('div', { class: 'sfera' }), el('div', {}, 'GAS ', el('small', { testo: 'CRM clienti' }))),
      el('p', { class: 'suggerimento', testo: 'Il CRM gira solo su questo computer. Inserisci il token per entrare.' }),
      campo, el('button', { class: 'btn primario', type: 'submit', testo: 'Entra' }), errore)));
  campo.focus();
}

async function avvia() {
  await carica();
  apriStream();
}

/* ------------------------------------------------------------------ dati e tempo reale */
let timerCarica = null;
async function carica() {
  try {
    S.dati = await api('/api/stato');
    if (S.cliente) await caricaCliente(S.cliente, false);
    disegna();
  } catch (e) {
    if (e.message !== 'Accesso richiesto') avviso(e.message, 'errore');
  }
}
function caricaPresto() {
  clearTimeout(timerCarica);
  timerCarica = setTimeout(carica, 250);
}
async function caricaCliente(id, ridisegna = true) {
  try {
    S.clienteDati = await api('/api/cliente?id=' + encodeURIComponent(id));
    S.cliente = id;
  } catch (e) {
    avviso(e.message, 'errore');
    S.cliente = null; S.clienteDati = null;
  }
  if (ridisegna) disegna();
}
function chiudiStream() { if (S.stream) { S.stream.close(); S.stream = null; } }
function apriStream() {
  chiudiStream();
  const es = new EventSource('/api/stream');
  S.stream = es;
  es.addEventListener('pronto', () => { S.live = true; aggiornaVivo(); });
  es.addEventListener('cambio', () => { S.live = true; aggiornaVivo(); caricaPresto(); });
  es.onerror = async () => {
    S.live = false; aggiornaVivo();
    try {
      const s = await fetch('/api/sessione', { credentials: 'same-origin' }).then((r) => r.json());
      if (!s.autenticato) mostraAccesso('Sessione scaduta: rientra.');
    } catch (_) { /* server spento: EventSource ritenta da solo */ }
  };
}
function aggiornaVivo() {
  const v = document.querySelector('.vivo');
  if (!v) return;
  v.classList.toggle('on', S.live);
  v.lastChild.textContent = S.live ? 'LIVE' : 'OFFLINE';
}

/* ------------------------------------------------------------------ disegno principale */
function staScrivendo() {
  const a = document.activeElement;
  return a && (a.tagName === 'TEXTAREA' || (a.tagName === 'INPUT' && a.type !== 'checkbox') || a.tagName === 'SELECT')
    && document.getElementById('app').contains(a);
}
document.addEventListener('focusout', () => {
  setTimeout(() => { if (S.rinviato && !staScrivendo()) { S.rinviato = false; disegna(); } }, 50);
});

function disegna() {
  if (!S.dati) return;
  if (staScrivendo()) { S.rinviato = true; return; }
  const scorri = window.scrollY;
  const cassettoScorri = document.querySelector('.cassetto')?.scrollTop || 0;
  const d = S.dati;
  const corpo = { panoramica: vistaPanoramica, clienti: vistaClienti, opportunita: vistaOpportunita, servizi: vistaServizi }[S.tab](d);
  const app = document.getElementById('app');
  const figli = [barra(d), el('main', { class: 'contenuto' }, corpo)];
  if (S.cliente && S.clienteDati) figli.push(...cassetto(S.clienteDati));
  if (S.modale) figli.push(S.modale());
  app.replaceChildren(...figli);
  window.scrollTo(0, scorri);
  const c = document.querySelector('.cassetto');
  if (c) c.scrollTop = cassettoScorri;
  S.eventiVisti = new Set((d.eventi || []).map((e) => e.id));
}

function barra(d) {
  const k = d.kpi;
  return el('header', { class: 'barra' },
    el('div', { class: 'logo' }, el('div', { class: 'sfera' }), el('div', {}, 'GAS', el('small', { testo: 'CRM clienti' }))),
    el('nav', { class: 'schede', role: 'tablist' }, SCHEDE.map(([id, nome, icona]) => el('button', {
      role: 'tab', 'aria-selected': S.tab === id ? 'true' : 'false',
      onclick: () => { S.tab = id; disegna(); window.scrollTo(0, 0); },
    }, el('span', { 'aria-hidden': 'true', testo: icona }), el('span', { class: 'testo-scheda', testo: nome }),
    id === 'opportunita' && k.opportunita_da_approvare ? el('span', { class: 'contatore', testo: String(k.opportunita_da_approvare) }) : null))),
    el('div', { class: 'spazio' }),
    d.server.demo ? el('span', { class: 'etichetta-demo', title: 'Dati inventati, nessun messaggio arriva a persone vere', testo: 'DEMO' }) : null,
    el('div', { class: 'vivo' + (S.live ? ' on' : ''), title: 'Aggiornamento in tempo reale' }, el('span', { class: 'punto' }), el('span', { testo: S.live ? 'LIVE' : 'OFFLINE' })),
    el('button', { class: 'btn piccolo', title: 'Il motore rilegge tutti i dati e cerca nuove opportunità', onclick: scansiona }, '⟳ Scansiona'),
    el('button', { class: 'btn primario piccolo', onclick: () => apriModale(modaleNuovoCliente) }, '+ Cliente'),
    el('button', { class: 'btn fantasma piccolo', title: 'Esci', onclick: esci }, '⏻'));
}
async function scansiona() {
  const r = await esegui(() => api('/api/scansiona', {}));
  if (r) {
    const n = r.risultato.create.length;
    avviso(n ? `Trovate ${n} nuove opportunità (~${euro0(r.risultato.valore_nuovo_cents)}/mese)` : 'Nessuna nuova opportunità: il motore ha controllato tutti i clienti.', 'ok');
    carica();
  }
}
async function esci() { await esegui(() => api('/api/logout', {})); mostraAccesso(); }

/* ------------------------------------------------------------------ PANORAMICA */
function confrontoParziale(prec) {
  // il mese in corso non è finito: niente percentuali rosse/verdi, solo il riferimento
  return el('span', { class: 'delta piatto', testo: `mese in corso · mese prima ${euroSegno(prec).replace(/^\+/, '')}` });
}
function delta(att, prec, bassoBene) {
  if (!prec) return el('span', { class: 'delta piatto', testo: '— vs mese prima' });
  const diff = att - prec;
  const p = Math.round((diff / Math.abs(prec)) * 100);
  const su = diff >= 0;
  const bene = bassoBene ? !su : su;
  return el('span', { class: 'delta ' + (diff === 0 ? 'piatto' : bene ? 'su' : 'giu') },
    diff === 0 ? '=' : su ? '▲' : '▼', ` ${Math.abs(p)}% vs mese prima`);
}
function sparkline(valori, w = 90, h = 30, blocco = false) {
  const max = Math.max(...valori, 1), min = Math.min(...valori, 0);
  const x = (i) => (i / Math.max(valori.length - 1, 1)) * (w - 6) + 3;
  const y = (v) => h - 4 - ((v - min) / (max - min || 1)) * (h - 8);
  const punti = valori.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
  const ultimo = valori.length - 1;
  return sv('svg', { class: blocco ? 'spark-blocco' : 'spark', width: blocco ? null : w, height: h, viewBox: `0 0 ${w} ${h}`, preserveAspectRatio: blocco ? 'none' : null, 'aria-hidden': 'true' },
    sv('polyline', { points: punti, fill: 'none', stroke: blocco ? '#3987e5' : '#5c6a90', 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', 'vector-effect': 'non-scaling-stroke' }),
    blocco ? null : sv('circle', { cx: x(ultimo), cy: y(valori[ultimo]), r: 4, fill: '#4ee1ff', stroke: '#0d1424', 'stroke-width': 2 }));
}
function tessera(etichetta, valore, nota, extra) {
  const e = el('section', { class: 'carta kpi' + (extra?.classe ? ' ' + extra.classe : ''), onclick: extra?.clic },
    el('div', { class: 'etichetta', testo: etichetta }), el('div', { class: 'valore num', testo: valore }), nota);
  if (extra?.spark) e.append(extra.spark);
  if (extra?.clic) e.classList.add('cliccabile');
  return e;
}
function vistaPanoramica(d) {
  const k = d.kpi;
  const mese = d.mese_label.split(' ')[0];
  const nServizi = Math.max(k.servizi_attivi, 1);
  return [
    el('div', { class: 'titolo-sezione' }, el('h1', { testo: 'Plancia' }),
      el('p', { testo: `${d.mese_label} · aggiornata in tempo reale · ${k.clienti_attivi} clienti attivi` })),
    el('div', { class: 'griglia-kpi' },
      tessera(`Commissioni di ${mese}`, euro0(k.commissioni_mese_cents), confrontoParziale(k.commissioni_mese_prec_cents),
        { spark: sparkline(d.serie.commissioni_cents, 200, 28, true) }),
      tessera(`Profitto clienti di ${mese}`, euroSegno(k.profitto_clienti_mese_cents), confrontoParziale(k.profitto_clienti_mese_prec_cents),
        { spark: sparkline(d.serie.profitto_clienti_cents, 200, 28, true) }),
      tessera('Capitale gestito', compatto(k.capitale_totale_cents), el('span', { class: 'nota', testo: `commissioni totali ${euro0(k.commissioni_totali_cents)}` })),
      tessera('Clienti paganti', `${k.clienti_paganti} / ${k.clienti_attivi}`, el('span', { class: 'nota', testo: `${k.clienti_totali - k.clienti_attivi} non attivi` })),
      tessera('Servizi per cliente', (k.servizi_per_cliente_x100 / 100).toLocaleString('it-IT', { minimumFractionDigits: 2 }),
        el('div', {}, el('span', { class: 'nota', testo: `${k.clienti_multi_servizio} con 2+ servizi · su ${nServizi}` }),
          el('div', { class: 'metro', title: 'Diversificazione media' }, el('div', { stile: { width: Math.min(100, (k.servizi_per_cliente_x100 / nServizi)) + '%' } })))),
      tessera('Opportunità aperte', String(k.opportunita_aperte),
        el('span', { class: 'nota', testo: `~${euro0(k.valore_opportunita_cents)}/mese di commissioni in più` }),
        { classe: k.opportunita_da_approvare ? 'in-evidenza' : '', clic: () => { S.tab = 'opportunita'; disegna(); } })),
    el('div', { class: 'griglia-2' }, cartaGrafico(d), cartaServizi(d)),
    el('div', { class: 'griglia-3' }, cartaImbuto(d), cartaTopOpportunita(d), cartaAttivita(d)),
  ];
}

function cartaGrafico(d) {
  const tipo = S.grafico;
  const valori = tipo === 'commissioni' ? d.serie.commissioni_cents : d.serie.profitto_clienti_cents;
  const contenitore = el('div', { class: 'grafico' });
  requestAnimationFrame(() => graficoColonne(contenitore, d.serie.etichette, valori, tipo === 'commissioni' ? 'Commissioni' : 'Profitto clienti'));
  const bottone = (id, testo) => el('button', { 'aria-pressed': tipo === id ? 'true' : 'false', onclick: () => { S.grafico = id; disegna(); }, testo });
  const totale = valori.reduce((a, b) => a + b, 0);
  return el('section', { class: 'carta' },
    el('div', { class: 'intestazione-carta' },
      el('div', {}, el('h2', { testo: tipo === 'commissioni' ? 'Le nostre commissioni, ultimi 12 mesi' : 'Profitto dei clienti, ultimi 12 mesi' }),
        el('p', { class: 'sotto', testo: `Totale 12 mesi ${euro0(totale)} · il mese in corso è parziale` })),
      el('div', { class: 'interruttore' }, bottone('commissioni', 'Commissioni'), bottone('profitto', 'Profitto clienti'))),
    contenitore);
}

function tickPuliti(min, max, n = 4) {
  const span = (max - min) || 1;
  const grezzo = span / n;
  const mag = Math.pow(10, Math.floor(Math.log10(grezzo)));
  const passo = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((p) => p >= grezzo) || 10 * mag;
  const out = [];
  for (let v = Math.floor(min / passo) * passo; v <= max + passo * 0.001; v += passo) out.push(Math.round(v));
  return out;
}
function graficoColonne(box, etichette, centesimi, nome) {
  const W = Math.max(box.clientWidth, 320), H = 300, sx = 52, dx = 8, su = 18, giu = 26;
  const euroV = centesimi.map((c) => c / 100);
  const ticks = tickPuliti(Math.min(0, ...euroV), Math.max(0, ...euroV));
  const minV = ticks[0], maxV = ticks[ticks.length - 1];
  const y = (v) => su + (1 - (v - minV) / ((maxV - minV) || 1)) * (H - su - giu);
  const banda = (W - sx - dx) / euroV.length;
  const larg = Math.min(24, banda * 0.62);
  const s = sv('svg', { viewBox: `0 0 ${W} ${H}`, height: H, role: 'img', 'aria-label': `${nome} per mese` });
  for (const t of ticks) {
    s.append(sv('line', { x1: sx, x2: W - dx, y1: y(t), y2: y(t), stroke: t === 0 ? '#2b3858' : '#1c2742', 'stroke-width': 1 }));
    s.append(sv('text', { x: sx - 8, y: y(t) + 4, 'text-anchor': 'end', class: 'tick' }, compatto(t * 100)));
  }
  const tip = el('div', { class: 'tooltip' });
  euroV.forEach((v, i) => {
    const cx = sx + banda * i + banda / 2;
    const y0 = y(0), y1 = y(v);
    const alto = Math.abs(y0 - y1);
    const r = Math.min(4, alto);
    const x0 = cx - larg / 2;
    const colore0 = i === euroV.length - 1 ? '#4ee1ff' : '#3987e5';
    let path;
    if (v >= 0) path = `M${x0},${y0} V${y1 + r} Q${x0},${y1} ${x0 + r},${y1} H${x0 + larg - r} Q${x0 + larg},${y1} ${x0 + larg},${y1 + r} V${y0} Z`;
    else path = `M${x0},${y0} V${y1 - r} Q${x0},${y1} ${x0 + r},${y1} H${x0 + larg - r} Q${x0 + larg},${y1} ${x0 + larg},${y1 - r} V${y0} Z`;
    if (alto >= 0.5) s.append(sv('path', { d: path, fill: v < 0 ? '#e66767' : colore0 }));
    const lab = etichette[i].split(' ');
    if (euroV.length <= 12 || i % 2 === 0) s.append(sv('text', { x: cx, y: H - 8, 'text-anchor': 'middle', class: 'tick' }, lab[0].slice(0, 3)));
    if (i === euroV.length - 1) s.append(sv('text', { x: cx, y: v >= 0 ? y1 - 6 : y1 + 14, 'text-anchor': 'middle', class: 'valore-barra' }, compatto(centesimi[i])));
    const area = sv('rect', { x: sx + banda * i, y: su, width: banda, height: H - su - giu, fill: 'transparent' });
    area.addEventListener('mouseenter', () => {
      tip.replaceChildren(el('b', { testo: euro(centesimi[i]) }), el('span', { testo: `${nome} · ${etichette[i]}${i === euroV.length - 1 ? ' (in corso)' : ''}` }));
      tip.style.left = (cx / W * 100) + '%'; tip.style.top = Math.min(y1, y0) + 'px'; tip.classList.add('on');
    });
    area.addEventListener('mouseleave', () => tip.classList.remove('on'));
    s.append(area);
  });
  box.replaceChildren(s, tip);
}

function cartaServizi(d) {
  const max = Math.max(...d.servizi.map((s) => s.penetrazione_bp), 1);
  return el('section', { class: 'carta' },
    el('h2', { testo: 'Servizi: quanti clienti ci sono dentro' }),
    el('p', { class: 'sotto', testo: 'Barra = quota dei clienti attivi nel servizio. Lo spazio vuoto è la tua prossima vendita.' }),
    el('div', { class: 'barre-servizi' }, d.servizi.length ? d.servizi.map((s) => el('div', { class: 'barra-servizio' },
      el('div', { class: 'testa' }, el('span', { class: 'nome' }, el('span', { class: 'pallino', stile: { background: colore(s.slot) } }), s.nome),
        el('span', { class: 'num', testo: `${s.clienti_attivi} clienti · ${pct(s.penetrazione_bp)}` })),
      el('div', { class: 'traccia' }, el('div', { class: 'riempi', stile: { width: (s.penetrazione_bp / Math.max(max, 10000) * 100) + '%', background: colore(s.slot) } })),
      el('div', { class: 'dati' }, el('span', { testo: s.capitale_cents ? `capitale ${compatto(s.capitale_cents)}` : MODELLI[s.modello_commissione] }),
        el('span', { testo: `commissioni ${euro0(s.commissioni_mese_cents)} nel mese` }),
        s.roi_osservato_bp !== null ? el('span', { testo: `rende ${pct(s.roi_osservato_bp)}/mese` }) : null))) : el('div', { class: 'vuoto', testo: 'Nessun servizio: aggiungilo nella scheda Servizi.' })));
}

function cartaImbuto(d) {
  const passi = [['da_approvare', 'Da approvare'], ['inviata', 'Inviate'], ['senza_risposta', 'Senza risposta'], ['accettata', 'Accettate'], ['rifiutata', 'Rifiutate']];
  const max = Math.max(...passi.map(([k]) => d.imbuto[k] || 0), 1);
  const tasso = d.kpi.tasso_accettazione_bp;
  return el('section', { class: 'carta' },
    el('h2', { testo: 'Proposte ai clienti' }),
    el('p', { class: 'sotto', testo: tasso === null ? 'Ancora nessun esito registrato' : `Tasso di sì: ${pct(tasso)} delle risposte` }),
    el('div', { class: 'imbuto' }, passi.map(([k, nome]) => el('div', { class: 'passo' },
      el('span', { testo: nome }),
      el('div', { class: 'traccia' }, el('div', { class: 'riempi', stile: { width: ((d.imbuto[k] || 0) / max * 100) + '%' } })),
      el('span', { class: 'n num', testo: String(d.imbuto[k] || 0) })))));
}

function cartaTopOpportunita(d) {
  const top = d.proposte_aperte.filter((p) => p.stato === 'da_approvare').slice(0, 4);
  return el('section', { class: 'carta' },
    el('h2', { testo: 'Le migliori opportunità adesso' }),
    el('p', { class: 'sotto', testo: 'Il motore le trova da solo leggendo i dati. Tu approvi l’invio.' }),
    top.length ? el('div', { class: 'feed' }, top.map((p) => el('div', { class: 'voce', stile: { gridTemplateColumns: '1fr auto', cursor: 'pointer' }, onclick: () => { S.tab = 'opportunita'; disegna(); } },
      el('div', {}, el('b', { testo: p.cliente_nome }), el('div', { class: 'chi', testo: TIPI[p.tipo] + (p.servizio_nome ? ' · ' + p.servizio_nome : '') })),
      el('b', { class: 'num', testo: `+${euro0(p.valore_stimato_cents)}/m` })))) : el('div', { class: 'vuoto', testo: 'Nessuna opportunità da approvare.' }));
}

function cartaAttivita(d) {
  return el('section', { class: 'carta' },
    el('h2', { testo: 'Attività in tempo reale' }),
    el('p', { class: 'sotto', testo: 'Tutto quello che succede nel CRM (registro che non si può riscrivere).' }),
    el('div', { class: 'feed' }, (d.eventi || []).map((e) => el('div', { class: 'voce' + (S.eventiVisti.size && !S.eventiVisti.has(e.id) ? ' nuova' : '') },
      el('span', { class: 'ora', testo: ora(e.ts) }),
      el('div', {}, el('div', { testo: e.descrizione }), el('div', { class: 'chi', testo: e.autore + (e.cliente_id ? ' · ' + nomeCliente(e.cliente_id) : '') }))))));
}
function nomeCliente(id) {
  const c = S.dati && S.dati.clienti.find((x) => x.id === id);
  return c ? c.nome : 'cliente #' + id;
}

/* ------------------------------------------------------------------ CLIENTI */
const FILTRI = [
  ['tutti', 'Tutti'], ['paganti', 'Paganti'], ['mono', 'Un solo servizio'], ['opportunita', 'Con opportunità'],
  ['nuovi', 'Senza pagamenti'], ['bloccati', 'Senza consenso / STOP'],
];
function filtraClienti(d) {
  const q = S.cerca.trim().toLowerCase();
  let righe = d.clienti.filter((c) => {
    if (q && !(`${c.nome} ${c.telefono || ''} ${c.email || ''}`.toLowerCase().includes(q))) return false;
    switch (S.filtro) {
      case 'paganti': return c.pagante && c.stato === 'attivo';
      case 'mono': return c.servizi_attivi.length === 1;
      case 'opportunita': return !!c.proposta_aperta;
      case 'nuovi': return !c.pagante;
      case 'bloccati': return !c.consenso_marketing || c.opt_out;
      default: return true;
    }
  });
  const { campo, verso } = S.ordina;
  const val = (c) => campo === 'nome' ? c.nome.toLowerCase() : campo.startsWith('srv:') ? (c.celle[campo.slice(4)]?.capitale_cents ?? -1) : c[campo];
  righe = righe.slice().sort((a, b) => (val(a) > val(b) ? 1 : val(a) < val(b) ? -1 : 0) * verso);
  return righe;
}
function ordinaPer(campo) {
  S.ordina = S.ordina.campo === campo ? { campo, verso: -S.ordina.verso } : { campo, verso: campo === 'nome' ? 1 : -1 };
  disegna();
}
function vistaClienti(d) {
  const righe = filtraClienti(d);
  const cerca = el('input', { type: 'search', placeholder: 'Cerca nome, telefono, email…', value: S.cerca });
  cerca.addEventListener('input', () => { S.cerca = cerca.value; const t = document.querySelector('.tabella-scorri'); if (t) t.replaceWith(tabellaClienti(S.dati, filtraClienti(S.dati))); });
  cerca.addEventListener('keydown', (e) => { if (e.key === 'Escape') { cerca.value = ''; S.cerca = ''; cerca.blur(); disegna(); } });
  return [
    el('div', { class: 'titolo-sezione' }, el('h1', { testo: 'Clienti × Servizi' }),
      el('p', { testo: `${righe.length} di ${d.clienti.length} clienti · ogni casella vuota è un servizio che il cliente non ha ancora` })),
    el('div', { class: 'strumenti' }, cerca,
      el('div', { class: 'chips' }, FILTRI.map(([id, nome]) => el('button', { class: 'chip', 'aria-pressed': S.filtro === id ? 'true' : 'false', onclick: () => { S.filtro = id; disegna(); }, testo: nome })))),
    barraSelezione(d, righe),
    leadPronti(d),
    tabellaClienti(d, righe),
  ];
}
function barraSelezione(d, righe) {
  // scelta dell'operatore (decisione 17-11): un messaggio a cliente singolo, con le spunte
  // per tutti / nessuno / alcuni. Regole dure e ritmo mensile restano anche qui.
  const vivi = new Set(d.clienti.map((c) => c.id));
  for (const id of [...S.selezionati]) if (!vivi.has(id)) S.selezionati.delete(id);
  const n = S.selezionati.size;
  const prepara = async () => {
    const r = await esegui(() => api('/api/proposte/selezionati', { clienti: [...S.selezionati] }));
    if (!r) return;
    const es = r.risultato, esclusi = Object.entries(es.esclusi || {});
    avviso(`Messaggi pronti da approvare: ${es.create.length}` + (esclusi.length ? ` · saltati ${esclusi.length}` : ''), 'ok');
    if (esclusi.length) apriModale(() => modaleEsclusi(esclusi));
    S.selezionati.clear();
    S.tab = 'opportunita';
    carica();
  };
  return el('div', { class: 'strumenti selezione' },
    el('span', { class: 'suggerimento', testo: n ? `${n} selezionati` : 'Spunta i clienti a cui scrivere' }),
    el('button', { class: 'btn piccolo', onclick: () => { righe.forEach((c) => S.selezionati.add(c.id)); disegna(); } }, '☑ Tutti quelli in lista'),
    el('button', { class: 'btn piccolo', disabled: !n, onclick: () => { S.selezionati.clear(); disegna(); } }, '☐ Nessuno'),
    el('button', { class: 'btn primario piccolo', disabled: !n, onclick: prepara, title: 'Prepara un messaggio per ogni cliente spuntato: li approvi uno per uno' }, `✉ Prepara messaggio (${n})`));
}
function modaleEsclusi(esclusi) {
  const nome = (id) => nomeCliente(Number(id));
  return el('div', { class: 'modale-velo', onclick: (e) => { if (e.target === e.currentTarget) chiudiModale(); } },
    el('div', { class: 'carta modale' },
      el('h2', { testo: 'Clienti saltati' }),
      el('p', { class: 'sotto', testo: 'Le regole valgono anche a mano: consenso, STOP, un messaggio al mese, una proposta alla volta.' }),
      el('div', { class: 'feed' }, esclusi.map(([id, motivo]) => el('div', { class: 'voce', stile: { gridTemplateColumns: '1fr' } },
        el('div', {}, el('b', { testo: nome(id) }), el('div', { class: 'chi', testo: motivo }))))),
      el('div', {}, el('button', { class: 'btn', onclick: chiudiModale, testo: 'Chiudi' }))));
}
function leadPronti(d) {
  if (!d.lead_pronti || !d.lead_pronti.length) return null;
  return el('section', { class: 'carta' },
    el('h2', { testo: `Lead pronti a diventare clienti (${d.lead_pronti.length})` }),
    el('p', { class: 'sotto', testo: 'Dalla rubrica di Gas, stato «interessato». Convertendoli entrano nel CRM (il consenso ai messaggi va raccolto a parte).' }),
    el('div', { class: 'feed' }, d.lead_pronti.map((l) => el('div', { class: 'voce', stile: { gridTemplateColumns: '1fr auto' } },
      el('div', {}, el('b', { testo: l.nome || l.chiave }), el('div', { class: 'chi', testo: (l.contatto || '') + (l.non_fidato ? ' · ⚠ scritto dopo una lettura esterna: verifica' : '') })),
      el('button', { class: 'btn piccolo', onclick: () => esegui(() => api('/api/lead/converti', { contatto_id: l.id }), 'Lead convertito in cliente').then(carica), testo: 'Converti' })))));
}
function tabellaClienti(d, righe) {
  const freccia = (campo) => S.ordina.campo === campo ? (S.ordina.verso > 0 ? ' ↑' : ' ↓') : '';
  const th = (testo, campo, extra) => el('th', { class: extra?.classe, onclick: () => ordinaPer(campo), scope: 'col' }, extra?.pallino, testo + freccia(campo));
  const tutti = righe.length > 0 && righe.every((c) => S.selezionati.has(c.id));
  const spuntaTutti = el('input', { type: 'checkbox', checked: tutti, 'aria-label': 'Seleziona tutti quelli in lista',
    onclick: (e) => e.stopPropagation(),
    onchange: (e) => { righe.forEach((c) => (e.target.checked ? S.selezionati.add(c.id) : S.selezionati.delete(c.id))); disegna(); } });
  const testa = el('tr', {}, el('th', { class: 'spunta' }, spuntaTutti), th('Cliente', 'nome'),
    d.servizi.map((s) => th(s.nome, 'srv:' + s.id, { pallino: el('span', { class: 'pallino', stile: { background: colore(s.slot) } }) })),
    th('Profitto mese', 'profitto_mese_cents', { classe: 'destra' }), th('Profitto totale', 'profitto_totale_cents', { classe: 'destra' }),
    th('Ci ha pagato', 'commissioni_totali_cents', { classe: 'destra' }));
  const maxCap = {};
  for (const s of d.servizi) maxCap[s.id] = Math.max(1, ...d.clienti.map((c) => c.celle[s.id]?.capitale_cents || 0));
  const corpo = righe.map((c) => {
    const obiettivo = c.proposta_aperta;
    const celle = d.servizi.map((s) => {
      const x = c.celle[s.id];
      if (!x) {
        const mira = obiettivo && obiettivo.tipo === 'cross_sell' && S.dati.proposte_aperte.some((p) => p.id === obiettivo.id && p.servizio_id === s.id);
        return el('td', {}, mira ? el('div', { class: 'cella obiettivo', title: 'Il motore ha una proposta pronta per questo servizio', testo: '◎ da proporre' }) : el('div', { class: 'cella vuota', 'aria-label': 'non attivo', testo: '·' }));
      }
      const m = x.profitto_mese_cents;
      return el('td', {}, el('div', { class: 'cella' + (x.stato === 'chiusa' ? ' chiusa' : ''), title: `${s.nome}: ${x.stato}${x.roi_bp !== null ? ' · rende ' + pct(x.roi_bp) + '/mese' : ''}` },
        el('span', { class: 'cap', testo: x.capitale_cents ? compatto(x.capitale_cents) : (x.stato === 'attiva' ? 'abbonato' : x.stato) }),
        x.capitale_cents ? el('div', { class: 'traccia' }, el('div', { class: 'riempi', stile: { width: (x.capitale_cents / maxCap[s.id] * 100) + '%', background: colore(s.slot) } })) : null,
        m ? el('span', { class: 'mese ' + (m > 0 ? 'su' : 'giu'), testo: (m > 0 ? '▲ ' : '▼ ') + euroSegno(m) }) : null));
    });
    const badge = [];
    if (c.opt_out) badge.push(el('span', { class: 'badge stop', testo: 'STOP' }));
    else if (!c.consenso_marketing) badge.push(el('span', { class: 'badge', testo: 'no consenso' }));
    if (c.stato !== 'attivo') badge.push(el('span', { class: 'badge', testo: c.stato.replace('_', ' ') }));
    if (!c.pagante) badge.push(el('span', { class: 'badge', testo: 'nessun pagamento' }));
    if (obiettivo) badge.push(el('span', { class: 'badge tipo-' + obiettivo.tipo, testo: '◎ ' + TIPI[obiettivo.tipo] }));
    const spunta = el('input', { type: 'checkbox', checked: S.selezionati.has(c.id), 'aria-label': 'Seleziona ' + c.nome,
      onclick: (e) => e.stopPropagation(),
      onchange: (e) => { if (e.target.checked) S.selezionati.add(c.id); else S.selezionati.delete(c.id); disegna(); } });
    if (!c.followup_attivo) badge.push(el('span', { class: 'badge', testo: 'follow-up spento' }));
    return el('tr', { class: S.selezionati.has(c.id) ? 'scelta' : '', onclick: () => apriCliente(c.id), tabindex: '0', onkeydown: (e) => { if (e.key === 'Enter') apriCliente(c.id); } },
      el('td', { class: 'spunta', onclick: (e) => e.stopPropagation() }, spunta),
      el('td', { class: 'cliente' }, el('div', { class: 'nome', testo: c.nome }), el('div', { class: 'sub' }, el('span', { testo: c.telefono || 'senza telefono' }), badge)),
      celle,
      el('td', { class: 'destra num ' + (c.profitto_mese_cents > 0 ? 'su' : c.profitto_mese_cents < 0 ? 'giu' : ''), testo: euroSegno(c.profitto_mese_cents) }),
      el('td', { class: 'destra num', testo: euroSegno(c.profitto_totale_cents) }),
      el('td', { class: 'destra num', testo: euro0(c.commissioni_totali_cents) }));
  });
  return el('div', { class: 'tabella-scorri' }, el('table', { class: 'matrice' }, el('thead', {}, testa),
    el('tbody', {}, corpo.length ? corpo : el('tr', {}, el('td', { colspan: String(d.servizi.length + 5) }, el('div', { class: 'vuoto', testo: 'Nessun cliente con questi filtri.' }))))));
}

/* ------------------------------------------------------------------ OPPORTUNITÀ */
function livello(n) { return el('span', { class: 'livello', title: `Insistenza ${n} su 3` }, [1, 2, 3].map((i) => el('i', { class: i <= n ? 'on' : '' }))); }
function cartaProposta(p) {
  const testa = el('div', { class: 'testa' },
    el('div', {}, el('div', { class: 'chi', onclick: () => apriCliente(p.cliente_id), testo: p.cliente_nome }),
      el('div', { class: 'sub', stile: { display: 'flex', gap: '6px', marginTop: '6px', flexWrap: 'wrap' } },
        el('span', { class: 'badge tipo-' + p.tipo, testo: TIPI[p.tipo] + (p.servizio_nome ? ' · ' + p.servizio_nome : '') }), livello(p.livello))),
    el('div', { class: 'valore num' }, `+${euro0(p.valore_stimato_cents)}`, el('small', { testo: '/mese' })));
  const parti = [testa, el('div', { class: 'motivo', testo: p.motivo })];
  if (p.stato === 'da_approvare') {
    const area = el('textarea', { 'aria-label': 'Messaggio da inviare', rows: '7' });
    area.value = S.bozze[p.id] ?? p.messaggio;
    area.addEventListener('input', () => { S.bozze[p.id] = area.value; });
    const invia = async () => {
      const finestra = window.open('about:blank', '_blank');
      const r = await esegui(() => api('/api/proposte/azione', { id: p.id, azione: 'invia', messaggio: area.value }));
      const link = r && linkSicuro(r.risultato.link_whatsapp);
      if (link && finestra) { finestra.opener = null; finestra.location.href = link; avviso('WhatsApp aperto col messaggio pronto: premi invio. Proposta segnata come inviata.', 'ok'); }
      else { if (finestra) finestra.close(); if (r) avviso('Proposta segnata come inviata (link WhatsApp non disponibile).', 'ok'); }
      delete S.bozze[p.id];
      carica();
    };
    const opus = S.dati.server.opus || {};
    const riscrivi = async (ev) => {
      const b = ev.currentTarget;
      b.disabled = true; b.textContent = '✨ Opus sta scrivendo…';
      const r = await esegui(() => api('/api/proposte/riscrivi', { id: p.id }), 'Testo riscritto da Claude Opus');
      if (r) { delete S.bozze[p.id]; }
      carica();
    };
    const invii = S.dati.server.invii || {};
    const fermo = invii.max && invii.fatti >= invii.max;
    parti.push(area, el('div', { class: 'azioni' },
      el('button', { class: 'btn primario', onclick: invia, disabled: fermo,
        title: fermo ? `Pausa anti-blocco: ${invii.fatti}/${invii.max} invii negli ultimi ${invii.minuti} min` : 'Apre WhatsApp col messaggio già scritto: tu premi invio' }, '✓ Approva e apri WhatsApp'),
      el('button', { class: 'btn', onclick: riscrivi, disabled: !!opus.motivo,
        title: opus.motivo || `Riscrive il testo con ${opus.modello} (mai modelli gratuiti)` }, '✨ Riscrivi con Opus'),
      el('button', { class: 'btn', onclick: () => navigator.clipboard?.writeText(area.value).then(() => avviso('Messaggio copiato', 'ok')) }, 'Copia'),
      el('button', { class: 'btn rosso', onclick: () => azioneProposta(p.id, 'scarta', 'Proposta scartata') }, 'Scarta')));
  } else if (p.stato === 'inviata' || p.stato === 'senza_risposta') {
    parti.push(el('div', { class: 'suggerimento', testo: `${p.stato === 'inviata' ? 'Inviata' : 'Nessuna risposta dal'} ${dataBreve(p.inviata_il)}. Com’è andata?` }),
      el('div', { class: 'azioni' },
        el('button', { class: 'btn verde', onclick: () => azioneProposta(p.id, 'accettata', 'Ottimo! Ricorda di aprire il servizio nella scheda del cliente.') }, '✓ Ha detto sì'),
        el('button', { class: 'btn', onclick: () => azioneProposta(p.id, 'rifiutata', 'Registrato. Il motore proverà un’altra strada più avanti.') }, '✕ Ha detto no'),
        el('button', { class: 'btn rosso', title: 'Il cliente non vuole più messaggi: non verrà più contattato', onclick: () => azioneProposta(p.id, 'stop', 'STOP registrato: nessun altro messaggio a questo cliente.') }, 'STOP')));
  } else {
    parti.push(el('div', {}, el('span', { class: 'badge stato-' + p.stato, testo: `${ICONE_STATO[p.stato] || ''} ${STATI_PROP[p.stato]} · ${dataBreve(p.esito_il)}` })));
  }
  return el('article', { class: 'carta opp' + (p.stato === 'da_approvare' ? ' calda' : '') }, parti);
}
async function azioneProposta(id, azione, ok) {
  await esegui(() => api('/api/proposte/azione', { id, azione }), ok);
  carica();
}
function indicatoreInvii(inv) {
  if (!inv || !inv.max) return null;
  const pieno = inv.fatti >= inv.max;
  const minuti = Math.ceil((inv.libero_tra_s || 0) / 60);
  return el('span', { class: 'badge ' + (pieno ? 'stato-senza_risposta' : 'ok'),
    title: 'Invio a scaglioni per non farsi bloccare da WhatsApp',
    testo: pieno ? `⏸ ${inv.fatti}/${inv.max} invii in ${inv.minuti} min · prossimo tra ${minuti} min` : `Invii ${inv.fatti}/${inv.max} negli ultimi ${inv.minuti} min` });
}
function vistaOpportunita(d) {
  const da = d.proposte_aperte.filter((p) => p.stato === 'da_approvare');
  const inviate = d.proposte_aperte.filter((p) => p.stato === 'inviata').concat(d.proposte_recenti.filter((p) => p.stato === 'senza_risposta'));
  const esiti = d.proposte_recenti.filter((p) => p.stato !== 'senza_risposta');
  const r = d.server.regole;
  const ultima = d.server.ultima_scansione;
  const colonna = (titolo, voci, vuoto, classe) => el('div', { class: 'colonna-opp' + (classe ? ' ' + classe : '') },
    el('h3', {}, titolo, el('span', { class: 'contatore', testo: String(voci.length) })),
    voci.length ? el('div', { class: 'pila-opp' }, voci.map(cartaProposta)) : el('div', { class: 'vuoto', testo: vuoto }));
  return [
    el('div', { class: 'titolo-sezione' }, el('h1', { testo: 'Opportunità' }),
      el('p', { testo: `Il motore legge i dati da solo: un follow-up al mese a chi è cliente da almeno ${r.anzianita_min_giorni} giorni, ha pagato almeno ${r.pagamenti_min} commissione e ha fatto almeno ${euro0(r.soglia_cents)} nel mese. Mai dopo una perdita, mai a chi ha detto STOP o ha il follow-up spento. Invii a scaglioni: al massimo ${r.invii_per_lotto} ogni ${r.lotto_minuti} minuti.` })),
    el('div', { class: 'strumenti' },
      el('button', { class: 'btn primario', onclick: scansiona }, '⟳ Scansiona ora'),
      indicatoreInvii(d.server.invii),
      ultima ? el('span', { class: 'suggerimento', testo: `Ultima scansione ${ora(new Date(d.server.ultima_scansione_ts * 1000).toISOString())}: ${ultima.create.length} nuove, ${Object.keys(ultima.esclusi).length} clienti esclusi (il perché è nella scheda di ognuno).` }) : null),
    el('div', { class: 'colonne-opp' },
      colonna('Da approvare', da, 'Niente da approvare: il motore riprova da solo quando cambiano i dati.', 'principale'),
      el('div', { class: 'colonna-opp' },
        colonna('In attesa di risposta', inviate, 'Nessun messaggio in attesa.'),
        colonna('Esiti recenti', esiti, 'Ancora nessun esito.'))),
  ];
}

/* ------------------------------------------------------------------ SERVIZI */
function vistaServizi(d) {
  const r = d.server.regole;
  return [
    el('div', { class: 'titolo-sezione' }, el('h1', { testo: 'Servizi' }),
      el('p', { testo: 'Il catalogo che il motore usa per proporre. Le stime di rendimento sono interne: non vengono mai scritte ai clienti.' })),
    el('div', { class: 'carte-servizi' }, d.servizi.map((s) => cartaServizio(s)), cartaNuovoServizio()),
    el('section', { class: 'carta' },
      el('h2', { testo: 'Regole del motore' }),
      el('p', { class: 'sotto', testo: 'Si cambiano dal file delle chiavi (.env) e valgono al riavvio del CRM.' }),
      el('div', { class: 'regole' },
        regola(euro0(r.soglia_cents), 'profitto nel mese per far scattare una proposta', 'GAS_CRM_SOGLIA_EURO'),
        regola(String(r.pagamenti_min), 'commissioni già pagate prima di proporre altro', 'GAS_CRM_PAGAMENTI_MIN'),
        regola(`${r.pausa_giorni} giorni`, 'pausa minima tra due messaggi', 'GAS_CRM_PAUSA_GIORNI'),
        regola(String(r.max_messaggi_30g), 'messaggi al massimo in 30 giorni', 'GAS_CRM_MAX_MESSAGGI_30G'),
        regola(`${r.pausa_dopo_no_giorni} giorni`, 'prima di riproporre ciò a cui ha detto no', 'GAS_CRM_PAUSA_DOPO_NO_GIORNI'),
        regola(`+${r.aumento_pct}%`, 'aumento di capitale suggerito', 'GAS_CRM_AUMENTO_PCT'),
        regola(`${r.anzianita_min_giorni} giorni`, 'da cliente prima della prima proposta', 'GAS_CRM_ANZIANITA_GIORNI'),
        regola(`${r.invii_per_lotto} / ${r.lotto_minuti} min`, 'invii a scaglioni (anti-blocco WhatsApp)', 'GAS_CRM_INVII_PER_LOTTO · GAS_CRM_LOTTO_MINUTI'))),
  ];
}
function regola(valore, testo, env) { return el('div', { class: 'regola' }, el('b', { class: 'num', testo: valore }), el('span', { testo }), el('div', {}, el('code', { testo: env }))); }
function descriviCommissione(s) {
  if (s.modello_commissione === 'fisso_mensile') return `${euro(s.commissione_fissa_cents)} al mese`;
  if (s.modello_commissione === 'percentuale_capitale_annua') return `${pct(s.commissione_bp)} all’anno sul capitale`;
  return `${pct(s.commissione_bp)} sul profitto`;
}
function cartaServizio(s) {
  let aperto = false;
  const corpo = el('div');
  const modulo = moduloServizio(s);
  modulo.hidden = true;
  const carta = el('section', { class: 'carta servizio' },
    el('span', { class: 'striscia', stile: { background: colore(s.slot) } }),
    el('div', { class: 'intestazione-carta' }, el('div', {}, el('h2', { testo: s.nome }), el('p', { class: 'sotto', testo: `${s.codice} · ${descriviCommissione(s)}` })),
      el('div', { stile: { display: 'flex', gap: '6px', flexWrap: 'wrap', justifyContent: 'flex-end' } },
        s.consigliato ? el('span', { class: 'badge tipo-cross_sell', testo: '★ da consigliare' }) : null,
        el('span', { class: 'badge ' + (s.attivo ? 'ok' : ''), testo: s.attivo ? 'attivo' : 'spento' }))),
    s.descrizione ? el('p', { class: 'suggerimento', testo: s.descrizione }) : null,
    el('div', { class: 'metriche' },
      el('div', {}, el('span', { testo: 'Clienti' }), el('b', { testo: `${s.clienti_attivi} · ${pct(s.penetrazione_bp)}` })),
      el('div', {}, el('span', { testo: 'Capitale' }), el('b', { testo: s.capitale_cents ? compatto(s.capitale_cents) : '—' })),
      el('div', {}, el('span', { testo: 'Commissioni mese' }), el('b', { testo: euro0(s.commissioni_mese_cents) })),
      el('div', {}, el('span', { testo: 'Rendimento osservato' }), el('b', { testo: s.roi_osservato_bp === null ? '—' : pct(s.roi_osservato_bp) + '/m' }))),
    el('button', { class: 'btn piccolo', onclick: () => { aperto = !aperto; modulo.hidden = !aperto; } }, '✎ Modifica'), modulo, corpo);
  return carta;
}
function moduloServizio(s) {
  const nuovo = !s;
  const v = (k, def) => (s ? s[k] : def);
  const campi = {
    codice: el('input', { type: 'text', value: v('codice', ''), placeholder: 'es. copy-oro', disabled: !nuovo }),
    nome: el('input', { type: 'text', value: v('nome', ''), placeholder: 'Nome del servizio' }),
    modello: el('select', {}, Object.entries(MODELLI).map(([k, n]) => el('option', { value: k, testo: n }))),
    commissione: el('input', { type: 'text', inputmode: 'decimal', value: s ? String(s.commissione_bp / 100).replace('.', ',') : '', placeholder: 'es. 25' }),
    fissa: el('input', { type: 'text', inputmode: 'decimal', value: s && s.commissione_fissa_cents ? (s.commissione_fissa_cents / 100).toFixed(2).replace('.', ',') : '', placeholder: 'es. 99' }),
    minimo: el('input', { type: 'text', inputmode: 'decimal', value: s && s.capitale_minimo_cents ? String(s.capitale_minimo_cents / 100) : '', placeholder: 'es. 1000' }),
    rendimento: el('input', { type: 'text', inputmode: 'decimal', value: s ? String(s.rendimento_stimato_bp / 100).replace('.', ',') : '', placeholder: 'es. 3' }),
    priorita: el('input', { type: 'text', inputmode: 'numeric', value: String(v('priorita', 100)) }),
    descrizione: el('input', { type: 'text', value: v('descrizione', '') || '', placeholder: 'Una riga per te' }),
    attivo: el('input', { type: 'checkbox', checked: v('attivo', true) }),
    consigliato: el('input', { type: 'checkbox', checked: v('consigliato', false) }),
  };
  campi.modello.value = v('modello_commissione', 'percentuale_profitto');
  const salva = async (ev) => {
    ev.preventDefault();
    const corpo = {
      nome: campi.nome.value, modello_commissione: campi.modello.value, commissione_pct: campi.commissione.value,
      commissione_fissa: campi.fissa.value, capitale_minimo: campi.minimo.value, rendimento_stimato_pct: campi.rendimento.value,
      priorita: campi.priorita.value, descrizione: campi.descrizione.value, attivo: campi.attivo.checked,
      consigliato: campi.consigliato.checked,
    };
    if (nuovo) corpo.codice = campi.codice.value; else corpo.id = s.id;
    const r = await esegui(() => api(nuovo ? '/api/servizi' : '/api/servizi/aggiorna', corpo), nuovo ? 'Servizio creato' : 'Servizio aggiornato');
    if (r) carica();
  };
  return el('form', { class: 'modulo', onsubmit: salva, stile: { marginTop: '12px' } },
    nuovo ? el('label', { class: 'campo' }, 'Codice (fisso, senza spazi)', campi.codice) : null,
    el('label', { class: 'campo' }, 'Nome', campi.nome),
    el('label', { class: 'campo' }, 'Come guadagniamo', campi.modello),
    el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Commissione %', campi.commissione), el('label', { class: 'campo' }, 'Fisso € al mese', campi.fissa)),
    el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Capitale minimo €', campi.minimo), el('label', { class: 'campo' }, 'Rendimento stimato %/mese', campi.rendimento)),
    el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Priorità (più bassa = prima)', campi.priorita), el('label', { class: 'campo' }, 'Descrizione', campi.descrizione)),
    el('label', { class: 'check' }, campi.attivo, 'Servizio attivo'),
    el('label', { class: 'check' }, campi.consigliato, 'Da consigliare nei follow-up (se ne segni almeno uno, il motore propone solo quelli)'),
    el('button', { class: 'btn primario', type: 'submit', testo: nuovo ? 'Crea servizio' : 'Salva' }));
}
function cartaNuovoServizio() {
  return el('section', { class: 'carta servizio' }, el('h2', { testo: '+ Nuovo servizio' }),
    el('p', { class: 'sotto', testo: 'Aggiungi i 4-5 servizi veri: nome, come guadagniamo, capitale minimo.' }), moduloServizio(null));
}

/* ------------------------------------------------------------------ SCHEDA CLIENTE */
function apriCliente(id) { S.cliente = id; caricaCliente(id); }
function chiudiCliente() { S.cliente = null; S.clienteDati = null; disegna(); }
function cassetto(x) {
  const c = x.cliente, m = x.metriche;
  const d = S.dati;
  const servizioPer = Object.fromEntries(d.servizi.map((s) => [s.id, s]));
  const aggiorna = (campi, ok) => esegui(() => api('/api/clienti/aggiorna', Object.assign({ id: c.id }, campi)), ok).then(carica);
  const consenso = el('input', { type: 'checkbox', checked: !!c.consenso_marketing, onchange: (e) => aggiorna({ consenso_marketing: e.target.checked }, 'Consenso aggiornato') });
  const stop = el('input', { type: 'checkbox', checked: !!c.opt_out, onchange: (e) => aggiorna({ opt_out: e.target.checked }, 'Preferenza aggiornata') });
  const followup = el('input', { type: 'checkbox', checked: c.followup_attivo !== 0, onchange: (e) => aggiorna({ followup_attivo: e.target.checked }, 'Follow-up aggiornato') });
  const statoSel = el('select', { onchange: (e) => aggiorna({ stato: e.target.value }, 'Stato aggiornato'), stile: { width: 'auto' } },
    ['attivo', 'in_pausa', 'perso'].map((s) => el('option', { value: s, testo: s.replace('_', ' ') })));
  statoSel.value = c.stato;

  const posizioni = x.posizioni.map((p) => {
    const s = servizioPer[p.servizio_id];
    const sel = el('select', { onchange: (e) => esegui(() => api('/api/posizioni/stato', { id: p.id, stato: e.target.value }), 'Servizio aggiornato').then(carica) },
      ['attiva', 'in_pausa', 'chiusa'].map((v) => el('option', { value: v, testo: v.replace('_', ' ') })));
    sel.value = p.stato;
    return el('div', { class: 'posizione' },
      el('div', {}, el('div', { class: 'nome' }, el('span', { class: 'pallino', stile: { background: colore(s ? s.slot : 0) } }), p.servizio_nome),
        el('div', { class: 'numeri' },
          el('span', {}, 'capitale ', el('b', { testo: euro0(p.capitale_cents) })),
          el('span', {}, 'mese ', el('b', { class: p.profitto_mese_cents >= 0 ? 'su' : 'giu', testo: euroSegno(p.profitto_mese_cents) })),
          el('span', {}, 'totale ', el('b', { testo: euroSegno(p.profitto_totale_cents) })),
          el('span', {}, 'rende ', el('b', { testo: pct(p.roi_bp) + '/m' })),
          el('span', {}, 'dal ', dataApertura(p)))),
      el('div', { stile: { display: 'grid', gap: '6px', justifyItems: 'end' } }, sparkline(p.serie_profitto_cents, 110, 32), sel));
  });

  const nonPosseduti = d.servizi.filter((s) => s.attivo && !x.posizioni.some((p) => p.servizio_id === s.id));
  const proposte = x.proposte.map((p) => el('div', { class: 'voce', stile: { gridTemplateColumns: '90px 1fr auto' } },
    el('span', { class: 'ora', testo: dataBreve(p.creata_il) }),
    el('div', {}, el('b', { testo: TIPI[p.tipo] + (p.servizio_nome ? ' · ' + p.servizio_nome : '') }), el('div', { class: 'chi', testo: p.motivo })),
    el('span', { class: 'badge stato-' + p.stato, testo: STATI_PROP[p.stato] })));

  return [
    el('div', { class: 'velo', onclick: chiudiCliente }),
    el('aside', { class: 'cassetto', role: 'dialog', 'aria-label': 'Scheda cliente ' + c.nome },
      el('div', { class: 'testa' },
        el('div', { stile: { flex: '1' } }, el('h2', { testo: c.nome }),
          el('div', { class: 'sub' }, el('span', { testo: c.telefono || 'senza telefono' }), c.email ? el('span', { testo: '· ' + c.email }) : null,
            m.pagamenti ? el('span', { class: 'badge ok', testo: `${m.pagamenti} pagamenti` }) : el('span', { class: 'badge', testo: 'nessun pagamento' }),
            c.presentato_da ? el('span', { class: 'badge', testo: 'presentato da #' + c.presentato_da }) : null)),
        el('button', { class: 'btn fantasma', 'aria-label': 'Chiudi', onclick: chiudiCliente }, '✕')),
      el('div', { class: 'mini-kpi' },
        el('div', {}, el('span', { testo: 'Capitale' }), el('b', { testo: euro0(m.capitale_cents) })),
        el('div', {}, el('span', { testo: 'Profitto mese' }), el('b', { class: m.profitto_mese_cents >= 0 ? 'su' : 'giu', testo: euroSegno(m.profitto_mese_cents) })),
        el('div', {}, el('span', { testo: 'Profitto totale' }), el('b', { testo: euroSegno(m.profitto_totale_cents) })),
        el('div', {}, el('span', { testo: 'Ci ha pagato' }), el('b', { testo: euro0(m.commissioni_totali_cents) }))),
      el('div', { class: 'motore' }, el('b', { testo: 'Cosa farebbe il motore adesso' }), x.spiegazione),
      el('div', { class: 'blocco' }, el('h3', { testo: 'Permessi e stato' }),
        el('div', { class: 'modulo' },
          el('label', { class: 'check' }, consenso, 'Ha dato il consenso a ricevere proposte su WhatsApp (serve per qualsiasi messaggio promozionale)'),
          el('label', { class: 'check' }, stop, 'Ha chiesto STOP: non contattarlo mai più'),
          el('label', { class: 'check' }, followup, 'Follow-up mensile automatico (toglilo per escludere questo cliente dalle proposte del motore)'),
          el('label', { class: 'campo', stile: { maxWidth: '220px' } }, 'Stato del cliente', statoSel))),
      el('div', { class: 'blocco' }, el('h3', { testo: `Servizi (${x.posizioni.length})` }),
        el('div', { class: 'modulo' }, posizioni.length ? posizioni : el('div', { class: 'vuoto', testo: 'Non è ancora in nessun servizio.' }))),
      moduloMovimento(x),
      nonPosseduti.length ? moduloNuovaPosizione(c, nonPosseduti) : null,
      x.proposte.length ? el('div', { class: 'blocco' }, el('h3', { testo: 'Proposte' }), el('div', { class: 'feed' }, proposte)) : null,
      registroMovimenti(x),
      moduloNota(c),
      el('div', { class: 'blocco' }, el('h3', { testo: 'Storia' }),
        el('div', { class: 'linea-tempo' }, x.eventi.map((e) => el('div', { class: 'voce' }, el('span', { class: 'ora', testo: new Date(e.ts).toLocaleString('it-IT', { dateStyle: 'short', timeStyle: 'short' }) }), el('span', { testo: e.descrizione })))))),
  ];
}
function dataApertura(p) {
  // la data di apertura si può solo anticipare, per caricare lo storico (R-806-2)
  const campo = el('input', { type: 'date', value: p.aperta_il, max: p.aperta_il, title: 'Anticipa la data di apertura per caricare movimenti più vecchi' });
  campo.style.width = 'auto';
  campo.style.padding = '2px 6px';
  campo.addEventListener('change', () => {
    if (!campo.value || campo.value === p.aperta_il) return;
    esegui(() => api('/api/posizioni/apertura', { id: p.id, data: campo.value }), 'Data di apertura aggiornata').then(carica);
  });
  return campo;
}
function moduloMovimento(x) {
  if (!x.posizioni.length) return null;
  const pos = el('select', {}, x.posizioni.map((p) => el('option', { value: String(p.id), testo: p.servizio_nome })));
  const tipo = el('select', {}, Object.entries(TIPI_MOV).map(([k, n]) => el('option', { value: k, testo: n })));
  tipo.value = 'profitto';
  const importo = el('input', { type: 'text', inputmode: 'decimal', placeholder: 'es. 1.234,56' });
  const data = el('input', { type: 'date', value: oggiIso(), max: oggiIso() });
  const nota = el('input', { type: 'text', placeholder: 'Nota (facoltativa)' });
  const invia = async (ev) => {
    ev.preventDefault();
    const r = await esegui(() => api('/api/movimenti', { posizione_id: Number(pos.value), tipo: tipo.value, importo: importo.value, data: data.value, nota: nota.value }), 'Movimento registrato');
    if (r) { importo.value = ''; nota.value = ''; importo.blur(); carica(); }
  };
  return el('div', { class: 'blocco' }, el('h3', { testo: 'Registra un movimento' }),
    el('form', { class: 'modulo', onsubmit: invia },
      el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Servizio', pos), el('label', { class: 'campo' }, 'Tipo', tipo)),
      el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Importo €', importo), el('label', { class: 'campo' }, 'Data', data)),
      el('label', { class: 'campo' }, 'Nota', nota),
      el('div', { class: 'suggerimento', testo: 'Profitto e perdita del cliente, versamenti (deposito), prelievi, e le commissioni che ci ha pagato. Un errore si corregge con «Storna», non si cancella.' }),
      el('div', {}, el('button', { class: 'btn primario', type: 'submit', testo: 'Registra' }))));
}
function moduloNuovaPosizione(c, servizi) {
  const srv = el('select', {}, servizi.map((s) => el('option', { value: String(s.id), testo: s.nome })));
  const capitale = el('input', { type: 'text', inputmode: 'decimal', placeholder: 'es. 10.000 (vuoto se abbonamento)' });
  const data = el('input', { type: 'date', value: oggiIso(), max: oggiIso() });
  const invia = async (ev) => {
    ev.preventDefault();
    const r = await esegui(() => api('/api/posizioni', { cliente_id: c.id, servizio_id: Number(srv.value), capitale_iniziale: capitale.value, data: data.value }), 'Cliente aggiunto al servizio');
    if (r) carica();
  };
  return el('div', { class: 'blocco' }, el('h3', { testo: 'Aggiungi a un servizio' }),
    el('form', { class: 'modulo', onsubmit: invia },
      el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Servizio', srv), el('label', { class: 'campo' }, 'Capitale iniziale €', capitale), el('label', { class: 'campo' }, 'Dal', data)),
      el('div', {}, el('button', { class: 'btn', type: 'submit', testo: '+ Aggiungi' }))));
}
function registroMovimenti(x) {
  if (!x.movimenti.length) return null;
  const segno = { deposito: '+', prelievo: '−', profitto: '+', perdita: '−', commissione: '' };
  return el('div', { class: 'blocco' }, el('h3', { testo: 'Registro movimenti' }),
    el('div', { stile: { maxHeight: '320px', overflow: 'auto' } }, el('table', { class: 'registro' },
      el('thead', {}, el('tr', {}, ['Data', 'Servizio', 'Tipo', 'Importo', 'Fonte', ''].map((t) => el('th', { testo: t })))),
      el('tbody', {}, x.movimenti.map((mv) => el('tr', { class: mv.stornato || mv.storno_di ? 'stornato' : '' },
        el('td', { testo: dataBreve(mv.data) }), el('td', { testo: mv.servizio_nome || '' }),
        el('td', { testo: (mv.storno_di ? 'storno · ' : '') + TIPI_MOV[mv.tipo] }),
        el('td', { class: 'destra', testo: segno[mv.tipo] + euro(mv.importo_cents) }),
        el('td', { testo: mv.fonte }),
        el('td', {}, !mv.stornato && !mv.storno_di ? el('button', { class: 'btn piccolo fantasma', title: 'Annulla questo movimento con uno storno', onclick: () => {
          if (confirm(`Stornare ${TIPI_MOV[mv.tipo].toLowerCase()} di ${euro(mv.importo_cents)} del ${dataBreve(mv.data)}?`)) esegui(() => api('/api/movimenti/storno', { id: mv.id }), 'Movimento stornato').then(carica);
        } }, 'Storna') : null)))))));
}
function moduloNota(c) {
  const testo = el('textarea', { rows: '2', placeholder: 'Annota una telefonata, una richiesta, un dettaglio…' });
  testo.style.minHeight = '60px';
  const invia = async (ev) => { ev.preventDefault(); const r = await esegui(() => api('/api/note', { cliente_id: c.id, testo: testo.value }), 'Nota salvata'); if (r) { testo.value = ''; testo.blur(); carica(); } };
  return el('div', { class: 'blocco' }, el('h3', { testo: 'Nota' }), el('form', { class: 'modulo', onsubmit: invia }, testo, el('div', {}, el('button', { class: 'btn', type: 'submit', testo: 'Salva nota' }))));
}

/* ------------------------------------------------------------------ MODALI */
function apriModale(fn) { S.modale = fn; disegna(); setTimeout(() => document.querySelector('.modale input')?.focus(), 30); }
function chiudiModale() { S.modale = null; disegna(); }
function modaleNuovoCliente() {
  const d = S.dati;
  const f = {
    nome: el('input', { type: 'text', placeholder: 'Nome e cognome', required: true }),
    telefono: el('input', { type: 'text', placeholder: '+39 333 1234567', inputmode: 'tel' }),
    email: el('input', { type: 'text', placeholder: 'nome@esempio.it', inputmode: 'email' }),
    consenso: el('input', { type: 'checkbox' }),
    presentato: el('select', {}, el('option', { value: '', testo: '— nessuno —' }), d.clienti.map((c) => el('option', { value: String(c.id), testo: c.nome }))),
    note: el('input', { type: 'text', placeholder: 'Facoltative' }),
  };
  const salva = async (ev) => {
    ev.preventDefault();
    const r = await esegui(() => api('/api/clienti', { nome: f.nome.value, telefono: f.telefono.value, email: f.email.value, consenso_marketing: f.consenso.checked, presentato_da: f.presentato.value, note: f.note.value }), 'Cliente creato');
    if (r) { S.modale = null; S.cliente = r.risultato.id; await caricaCliente(r.risultato.id, false); carica(); }
  };
  return el('div', { class: 'modale-velo', onclick: (e) => { if (e.target === e.currentTarget) chiudiModale(); } },
    el('form', { class: 'carta modale modulo', onsubmit: salva },
      el('h2', { testo: 'Nuovo cliente' }),
      el('label', { class: 'campo' }, 'Nome', f.nome),
      el('div', { class: 'riga' }, el('label', { class: 'campo' }, 'Telefono WhatsApp', f.telefono), el('label', { class: 'campo' }, 'Email', f.email)),
      el('label', { class: 'campo' }, 'Presentato da (referral)', f.presentato),
      el('label', { class: 'campo' }, 'Note', f.note),
      el('label', { class: 'check' }, f.consenso, 'Ha dato il consenso a ricevere proposte (spuntalo solo se l’ha dato davvero, meglio per iscritto)'),
      el('div', { stile: { display: 'flex', gap: '10px' } }, el('button', { class: 'btn primario', type: 'submit', testo: 'Crea cliente' }), el('button', { class: 'btn', type: 'button', onclick: chiudiModale, testo: 'Annulla' }))));
}
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (S.modale) chiudiModale(); else if (S.cliente) chiudiCliente();
});
window.addEventListener('resize', () => { clearTimeout(window.__r); window.__r = setTimeout(() => { if (!staScrivendo()) disegna(); }, 200); });

/* ------------------------------------------------------------------ avvio */
(async function inizio() {
  const m = /[#&]t=([^&]+)/.exec(location.hash);
  if (m) {
    history.replaceState(null, '', location.pathname);
    try { await api('/api/login', { token: decodeURIComponent(m[1]) }); } catch (_) { /* si mostra l'accesso */ }
  }
  try {
    const s = await fetch('/api/sessione', { credentials: 'same-origin' }).then((r) => r.json());
    if (s.autenticato) avvia(); else mostraAccesso();
  } catch (_) { mostraAccesso('Server non raggiungibile.'); }
}());
