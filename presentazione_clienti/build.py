#!/usr/bin/env python3
"""Genera presentazione.html (16:9, 1280x720 px per pagina, stile HUD scuro).

Poi: node render.js  ->  «PDF servizi ecosistema.pdf»
Versione corta (9 pagine) per chi investe per la prima volta: per ogni servizio prima
«cos'è» e «come funziona» in parole semplici, poi i numeri.
Niente ombre/bagliori CSS (text-shadow, box-shadow): nel PDF diventano immagini che alcuni
lettori disegnano come riquadri sopra il testo (operatore, 19/11). Restano immagini interne per
sfumature e trasparenze (sfondi, pannelli): pdfimages -list non le mostra, ma ci sono.
Versione del repo (predefinita, senza contatti):  python3 build.py && node render.js
Versione completa (fuori da git):  python3 build.py --con-contatti && node render.js
(con i contatti render.js scrive solo in privato/ e rifiuta il PDF tracciato)
"""
from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "presentazione.html"

BRAND = "GasTradeFx"
TOTAL = 9

# colori HUD: identità dei servizi (sempre accanto a numero e nome del servizio)
CYAN, GREEN, GOLD, VIOLET = "#4FD8FF", "#5BE38A", "#FFB547", "#C79BFF"

# ---------------------------------------------------------------- dati reali
# Copy trading Forex: numeri del conto di riferimento (Myfxbook), dal catalogo
# "The Source Finance - Catalogo servizi pre-lancio" (TSF-CAT-2026-0001, 11.11.2026),
# servizio 01 "TSF Forex Algo". Vanno tenuti tutti come sono (operatore, 2026-11-17).
FX = {
    "rendimento": "+165,12%", "max_dd": "17,92%", "media_mensile": "+4,31%", "win_rate": "75,5%",
    "profit_factor": "2,18", "rend_dd": "9,2x", "operazioni": "1.230", "durata_media": "11h 45m",
}
FX_MENSILI = {
    2025: [2.45, 7.47, 8.21, -0.08, 15.80, 5.37, 4.75, 5.69, 1.98, 2.48, 1.37, 0.00],
    2026: [7.56, 9.63, 5.84, 5.90, 3.39, 1.32, 0.45, 1.68, 2.07, 4.70, 2.96],
}
FX_ANNO = {2025: "+70,35%", 2026: "+55,59%"}
FX_FONTE = ("Fonte: Myfxbook, conto reale USD (Darwinex, leva 1:200, deposito 100.000 $, nessun prelievo), "
            "16.12.2024 – 09.11.2026, track record verificato; valori 2025 per mese ricavati dalla curva "
            "Myfxbook. Il conto dei dati è al livello di rischio 3 su 10 (stop 30%); il copy dei clienti "
            "opera al livello 1 (stop 10%), broker TMGM. Condizioni: accesso gratuito, profit share 35% "
            "sui profitti netti con high-water mark (si paga solo sui nuovi massimi), calcolo settimanale.")


# ---------------------------------------------------------------- helpers
def eur(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".") + " €"


def dec(v: float, d: int = 2) -> str:
    return f"{v:.{d}f}".replace(".", ",")



def logo(size: int = 22) -> str:
    return (
        f'<svg class="logo" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10.5" fill="none" stroke="#4FD8FF" stroke-width="1.3"/>'
        '<circle cx="12" cy="12" r="5" fill="none" stroke="#4FD8FF" stroke-width="1.6"/>'
        '<circle cx="12" cy="12" r="1.8" fill="#BFF3FF"/>'
        '<path d="M12 0.5v3M12 20.5v3M0.5 12h3M20.5 12h3" stroke="#4FD8FF" stroke-width="1.3"/></svg>'
    )


# Contatti della pagina finale: SOLO da un file locale ignorato da git (il repo è pubblico,
# operatore 19/11). Formato: {"Referente": "...", "Telefono": "...", "Email": "..."}.
# Predefinito SENZA contatti (versione del repo): entrano solo con --con-contatti, e allora
# render.js scrive solo in privato/ (bot #384 V-1: un rendering «normale» non deve poterli
# ripubblicare nel PDF tracciato).
CONTATTI_FILE = HERE / "contatti.local.json"
CON_CONTATTI = "--con-contatti" in sys.argv


def contatti() -> list:
    if not CON_CONTATTI:
        return []
    try:
        dati = json.loads(CONTATTI_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [(str(k), str(v)) for k, v in dati.items() if v]


FONT_TITLE = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
TITLE_CACHE = HERE / "titoli_svg.json"


def _text_to_path(text: str, size: int, tracking_em: float) -> tuple[str, float]:
    """Testo -> tracciati vettoriali (serve fonttools + uharfbuzz). Il riempimento sfumato su
    <text> o con background-clip:text viene reso male nel PDF; sui tracciati è affidabile."""
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    face = hb.Face(Path(FONT_TITLE).read_bytes())
    font = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    tt = TTFont(FONT_TITLE)
    gs, order = tt.getGlyphSet(), tt.getGlyphOrder()
    scale = size / face.upem
    x = 0.0
    pen = SVGPathPen(gs)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, size * 0.86 - pos.y_offset * scale))
        gs[order[info.codepoint]].draw(tp)
        x += pos.x_advance * scale + tracking_em * size
    return pen.getCommands(), x


def grad_line(text: str, size: int = 60, tracking_em: float = -0.03) -> str:
    """Riga di titolo con riempimento sfumato (tracciato SVG); ripiego: testo a tinta unita."""
    key = f"{text}|{size}|{tracking_em}"
    cache = json.loads(TITLE_CACHE.read_text()) if TITLE_CACHE.exists() else {}
    try:
        d, w = _text_to_path(text, size, tracking_em)
        cache[key] = [d, w]
        TITLE_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0))
    except ImportError:
        if key not in cache:
            return f'<div class="gline-fb" style="font-size:{size}px">{text}</div>'
        d, w = cache[key]
    h = round(size * 1.12)
    return (f'<svg class="gline" width="{w + 4:.0f}" height="{h}" viewBox="0 0 {w + 4:.0f} {h}" role="img" '
            f'aria-label="{text}"><path d="{d}" fill="url(#g-title)"/></svg>')


def top(label: str, n: int, color: str = CYAN) -> str:
    return (f'<header class="top"><div class="k top-l"><i class="pulse" style="--c:{color}"></i>{label}</div>'
            f'<div class="top-r"><span class="pg">{n:02d}<em>/{TOTAL:02d}</em></span></div></header><div class="rule"></div>')


def foot() -> str:
    return ('<footer class="foot"><span>Il trading con leva comporta il rischio di perdere il capitale. I risultati '
            'passati non sono indicativi di quelli futuri. Avvertenze complete a pag. 8.</span>'
            '<span class="k">Documento riservato</span></footer>')


def frame() -> str:
    return '<div class="frame"></div>'


def ring(frac: float, color: str, value: str, sub: str, size: int = 190) -> str:
    """Anello HUD: l'arco colorato è la quota frac (0-1) del cerchio."""
    c, r = size / 2, size / 2 - 22
    circ = 2 * math.pi * r
    o = [f'<svg class="ring" width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-hidden="true">']
    for i in range(60):
        a = 2 * math.pi * i / 60 - math.pi / 2
        r1, r2 = r + 12, r + (18 if i % 5 == 0 else 15)
        o.append(f'<line x1="{c + r1 * math.cos(a):.1f}" y1="{c + r1 * math.sin(a):.1f}" '
                 f'x2="{c + r2 * math.cos(a):.1f}" y2="{c + r2 * math.sin(a):.1f}" stroke="#9FDFFF" '
                 f'stroke-opacity="{0.45 if i % 5 == 0 else 0.18}" stroke-width="1"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#FFFFFF" stroke-opacity=".07" stroke-width="7"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{color}" stroke-opacity=".18" stroke-width="15" '
             f'stroke-dasharray="{circ * frac:.1f} {circ:.1f}" transform="rotate(-90 {c} {c})"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" '
             f'stroke-dasharray="{circ * frac:.1f} {circ:.1f}" transform="rotate(-90 {c} {c})"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="{r - 16}" fill="none" stroke="{color}" stroke-opacity=".25" stroke-width="1"/>')
    o.append("</svg>")
    return (f'<div class="ring-w" style="width:{size}px;height:{size}px">{"".join(o)}'
            f'<div class="ring-t"><div class="ring-v">{value}</div><div class="k ring-s">{sub}</div></div></div>')


# ---------------------------------------------------------------- grafici
def chart_equity() -> str:
    """Crescita cumulata a fine mese, calcolata dai rendimenti mensili reali (Myfxbook)."""
    W, H = 600, 236
    ml, mr, mt, mb = 44, 66, 12, 26
    pw, phh = W - ml - mr, H - mt - mb
    vals, g = [0.0], 1.0
    for anno in (2025, 2026):
        for r in FX_MENSILI[anno]:
            g *= 1 + r / 100
            vals.append((g - 1) * 100)
    n, ymax = len(vals) - 1, 200

    def X(i: int) -> float:
        return ml + pw * i / n

    def Y(v: float) -> float:
        return mt + phh * (1 - v / ymax)

    o = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Crescita cumulata del conto di riferimento, a fine mese">']
    for t in range(0, ymax + 1, 50):
        o.append(f'<line class="{"base" if t == 0 else "grid"}" x1="{ml}" x2="{W - mr + 8}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>')
        o.append(f'<text class="tick" x="{ml - 10}" y="{Y(t) + 4:.1f}" text-anchor="end">{t}%</text>')
    for i, lab in {0: "12.2024", 12: "12.2025", n: "11.2026"}.items():
        o.append(f'<text class="tick" x="{X(i):.1f}" y="{H - 6}" text-anchor="middle">{lab}</text>')
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    o.append(f'<polygon points="{X(0):.1f},{Y(0):.1f} {pts} {X(n):.1f},{Y(0):.1f}" fill="url(#g-area)"/>')
    o.append(f'<polyline points="{pts}" fill="none" stroke="{CYAN}" stroke-opacity=".18" stroke-width="8" stroke-linejoin="round"/>')
    o.append(f'<polyline points="{pts}" fill="none" stroke="{CYAN}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<circle cx="{X(n):.1f}" cy="{Y(vals[-1]):.1f}" r="9" fill="{CYAN}" fill-opacity=".2"/>')
    o.append(f'<circle cx="{X(n):.1f}" cy="{Y(vals[-1]):.1f}" r="4.5" fill="#E8FAFF" stroke="{CYAN}" stroke-width="2"/>')
    o.append(f'<text class="endv" x="{X(n) + 12:.1f}" y="{Y(vals[-1]) + 5:.1f}">+{dec(vals[-1], 1)}%</text>')
    o.append("</svg>")
    return "".join(o)


def heat_cell(v: float | None) -> str:
    """Rendimento del mese: più chiaro il ciano, migliore il mese; negativo in rosso spento."""
    if v is None:
        return "<div class='hm-c hm-na'></div>"
    if v < 0:
        bg, ink = "#3A1A26", "#FFA7B5"
    elif v == 0:
        bg, ink = "#15212F", "#8DA2B8"
    else:
        steps = [(2, "#0F3048", "#CDEFFF"), (4, "#124B69", "#E6F7FF"), (6, "#176A8F", "#FFFFFF"),
                 (8, "#1D8BB6", "#FFFFFF"), (12, "#33B3E0", "#03121D"), (99, "#7FE3FF", "#03121D")]
        bg, ink = next((b, i) for lim, b, i in steps if v < lim)
    return f"<div class='hm-c' style='background:{bg};color:{ink}'>{dec(v)}</div>"


def heatmap() -> str:
    mesi = ["G", "F", "M", "A", "M", "G", "L", "A", "S", "O", "N", "D"]
    head = "<div class='hm-c hm-h'></div>" + "".join(f"<div class='hm-c hm-h'>{m}</div>" for m in mesi) + \
        "<div class='hm-c hm-h'>ANNO</div>"
    rows = ""
    for anno, vals in FX_MENSILI.items():
        rows += f"<div class='hm-c hm-y'>{anno}</div>"
        rows += "".join(heat_cell(vals[i] if i < len(vals) else None) for i in range(12))
        rows += f"<div class='hm-c hm-tot'>{FX_ANNO[anno]}</div>"
    return f"<div class='hm'>{head}{rows}</div>"


def chart_elastico() -> str:
    """Schema (non dati reali): due valute che si muovono insieme, si allontanano, tornano."""
    W, H = 560, 150
    ml, mr, mt, mb = 8, 16, 16, 14
    pw, phh = W - ml - mr, H - mt - mb
    N = 260
    a_vals, b_vals, gap = [], [], []
    for i in range(N):
        t = i / (N - 1)
        base = 50 + 7 * math.sin(2 * math.pi * (0.55 * t + 0.05)) + 1.2 * math.sin(2 * math.pi * 6 * t)
        s = 0.9 * math.sin(2 * math.pi * 9 * t) + 9.5 * math.exp(-((t - 0.5) / 0.085) ** 2)
        a_vals.append(base + s / 2 + 0.5 * math.sin(2 * math.pi * 17 * t))
        b_vals.append(base - s / 2 - 0.4 * math.sin(2 * math.pi * 13 * t + 1))
        gap.append(a_vals[-1] - b_vals[-1])
    lo, hi = min(b_vals) - 3, max(a_vals) + 3

    def X(i: int) -> float:
        return ml + pw * i / (N - 1)

    def Y(v: float) -> float:
        return mt + phh * (1 - (v - lo) / (hi - lo))

    picco = max(range(N), key=lambda i: gap[i])
    apre = next(i for i in range(N) if gap[i] > 6.5)
    chiude = next(i for i in range(picco, N) if gap[i] < 1.2)
    o = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Schema: due valute si allontanano e poi tornano vicine">']
    area = " ".join(f"{X(i):.1f},{Y(a_vals[i]):.1f}" for i in range(apre, chiude + 1)) + " " + \
        " ".join(f"{X(i):.1f},{Y(b_vals[i]):.1f}" for i in range(chiude, apre - 1, -1))
    o.append(f'<polygon points="{area}" fill="{CYAN}" fill-opacity=".14"/>')
    for vals, col, lab in ((a_vals, CYAN, "Valuta A"), (b_vals, "#C8D6E6", "Valuta B")):
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>')
    for i, testo, col in ((apre, "SI ALLONTANANO → APRE", "#E8FAFF"), (chiude, "TORNANO VICINE → CHIUDE", GREEN)):
        o.append(f'<line x1="{X(i):.1f}" y1="{mt:.1f}" x2="{X(i):.1f}" y2="{H - mb:.1f}" stroke="{col}" stroke-opacity=".35" stroke-width="1"/>')
        o.append(f'<circle cx="{X(i):.1f}" cy="{Y((a_vals[i] + b_vals[i]) / 2):.1f}" r="5" fill="{col}" stroke="#08111D" stroke-width="2"/>')
        anchor, dx = ("end", -8) if i == apre else ("start", 8)
        o.append(f'<text class="ann" x="{X(i) + dx:.1f}" y="{mt + 10:.1f}" text-anchor="{anchor}" fill="{col}">{testo}</text>')
    o.append(f'<text class="tag" x="{W - mr}" y="{H - 4}" text-anchor="end">SCHEMA ILLUSTRATIVO</text>')
    o.append("</svg>")
    return "".join(o)


def schema_matched() -> str:
    """Schema semplice: 3.000 € → due conti con scommesse opposte → in media ≈ +500 € (non garantito)."""
    W, H = 560, 206
    g = GREEN
    box = 'fill="#0C1E2C" stroke="{c}" stroke-opacity="{o}" stroke-width="1.3" rx="6"'
    o = [f'<svg class="chart schema" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Schema del matched trading: due conti con scommesse opposte, in media il vincente guadagna più di quanto perde l\'altro">']
    # collegamenti
    for d in ("M104,103 C130,103 126,42 152,42", "M104,103 C130,103 126,164 152,164",
              "M398,42 C424,42 420,103 448,103", "M398,164 C424,164 420,103 448,103"):
        o.append(f'<path d="{d}" fill="none" stroke="{g}" stroke-opacity=".55" stroke-width="1.5"/>')
    for x, y in ((152, 42), (152, 164), (448, 103)):
        o.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{g}"/>')
    # capitale
    o.append(f'<rect x="1" y="74" width="103" height="58" {box.format(c=g, o=".7")}/>')
    o.append('<text x="52" y="101" text-anchor="middle" class="sm-v">3.000 €</text>')
    o.append('<text x="52" y="119" text-anchor="middle" class="sm-k">IL CAPITALE</text>')
    # i due conti
    for y, nome, freccia, punta, esito in ((4, "CONTO A · PROP FIRM", "▲", "punta sul rialzo", "se supera la prova, paga la prop firm"),
                                           (126, "CONTO B · BROKER", "▼", "punta sul ribasso", "se A non la supera, guadagna B")):
        o.append(f'<rect x="152" y="{y}" width="246" height="76" {box.format(c=g, o=".45")}/>')
        o.append(f'<text x="168" y="{y + 22}" class="sm-k" fill="{g}">{nome}</text>')
        o.append(f'<text x="168" y="{y + 45}" class="sm-t"><tspan fill="{g}">{freccia}</tspan> {punta}</text>')
        o.append(f'<text x="168" y="{y + 64}" class="sm-s">{esito}</text>')
    # risultato
    o.append(f'<rect x="448" y="70" width="111" height="66" fill="rgba(91,227,138,.10)" stroke="{g}" stroke-width="1.5" rx="6"/>')
    o.append(f'<text x="503" y="101" text-anchor="middle" class="sm-r" fill="{g}">≈ +500 €</text>')
    o.append('<text x="503" y="121" text-anchor="middle" class="sm-k">IN MEDIA</text>')
    o.append("</svg>")
    return "".join(o)


def reticle(size: int = 600, labels: bool = True) -> str:
    """Mirino HUD della copertina, con i quattro servizi."""
    c = size / 2
    o = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" aria-hidden="true">']
    o.append(f'<circle cx="{c}" cy="{c}" r="{c - 10}" fill="url(#g-glow)"/>')
    for r, a, w in ((92, .5, 1.2), (150, .22, 1), (212, .14, 1), (262, .10, 1)):
        o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{CYAN}" stroke-opacity="{a}" stroke-width="{w}"/>')
    for i in range(120):
        a = 2 * math.pi * i / 120
        r1, r2 = 262, 262 + (10 if i % 10 == 0 else 4)
        o.append(f'<line x1="{c + r1 * math.cos(a):.1f}" y1="{c + r1 * math.sin(a):.1f}" x2="{c + r2 * math.cos(a):.1f}" '
                 f'y2="{c + r2 * math.sin(a):.1f}" stroke="{CYAN}" stroke-opacity="{.5 if i % 10 == 0 else .2}" stroke-width="1"/>')
    circ = 2 * math.pi * 236
    o.append(f'<circle cx="{c}" cy="{c}" r="236" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-width="3" '
             f'stroke-dasharray="{circ * .12:.0f} {circ * .05:.0f} {circ * .03:.0f} {circ * .08:.0f}"/>')
    circ2 = 2 * math.pi * 120
    o.append(f'<circle cx="{c}" cy="{c}" r="120" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="2" '
             f'stroke-dasharray="{circ2 * .2:.0f} {circ2 * .3:.0f}" transform="rotate(-30 {c} {c})"/>')
    for x1, y1, x2, y2 in ((c - 300, c, c - 100, c), (c + 100, c, c + 300, c), (c, c - 300, c, c - 100), (c, c + 100, c, c + 300)):
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity=".18" stroke-width="1"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="66" fill="#071422" stroke="{CYAN}" stroke-width="1.5"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="74" fill="none" stroke="{CYAN}" stroke-opacity=".3" stroke-width="6"/>')
    if labels:
        o.append(f'<text x="{c}" y="{c - 6}" text-anchor="middle" class="orb-c1">IL TUO</text>')
        o.append(f'<text x="{c}" y="{c + 16}" text-anchor="middle" class="orb-c2">capitale</text>')
    nodes = [(-148, "01", "Rendimento", "contrattuale", GOLD, 150), (-58, "02", "Matched", "trading", GREEN, 212),
             (32, "03", "Copy", "trading", CYAN, 150), (122, "04", "Gruppo", "privato", VIOLET, 212)]
    for deg, n, l1, l2, col, r in nodes:
        a = math.radians(deg)
        x, y = c + r * math.cos(a), c + r * math.sin(a)
        o.append(f'<line x1="{c + 74 * math.cos(a):.1f}" y1="{c + 74 * math.sin(a):.1f}" x2="{x - 24 * math.cos(a):.1f}" '
                 f'y2="{y - 24 * math.sin(a):.1f}" stroke="{col}" stroke-opacity=".35" stroke-width="1"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{col}" fill-opacity=".10"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="21" fill="#061220" stroke="{col}" stroke-width="1.6"/>')
        o.append(f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" class="orb-n" fill="{col}">{n}</text>')
        if labels:
            right = math.cos(a) >= 0
            tx = x + (34 if right else -34)
            anchor = "start" if right else "end"
            o.append(f'<text x="{tx:.1f}" y="{y - 2:.1f}" text-anchor="{anchor}" class="orb-l1">{l1}</text>')
            o.append(f'<text x="{tx:.1f}" y="{y + 14:.1f}" text-anchor="{anchor}" class="orb-l2">{l2}</text>')
    rnd = random.Random(11)
    for _ in range(40):
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(80, 280)
        o.append(f'<circle cx="{c + r * math.cos(a):.1f}" cy="{c + r * math.sin(a):.1f}" r="{rnd.choice([0.8, 1.1])}" '
                 f'fill="#BFF3FF" fill-opacity="{rnd.uniform(.15, .5):.2f}"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- pagine
def s_cover() -> str:
    return f'''
<section class="slide cover">{frame()}
  <div class="cover-l">
    <div class="k cov-k"><i class="pulse"></i>Ecosistema di investimento · 2026</div>
    <h1>Il tuo capitale,</h1>{grad_line("quattro motori.", 66)}
    <p class="cov-sub">Quattro modi semplici per far lavorare i tuoi soldi. Per ognuno: cos'è, come funziona e cosa aspettarti.</p>
    <div class="k cov-st"><span>● 4 servizi</span><span>● spiegati in modo semplice</span><span>● documento riservato</span></div>
  </div>
  <div class="cover-r">{reticle()}</div>
</section>'''


def card(n: str, color: str, name: str, cosa: str, fig: str, cap: str, per: str) -> str:
    return f'''<div class="hud svc" style="--c:{color}">
  <div class="svc-h"><span class="k" style="color:{color}">Servizio {n}</span><span class="svc-dot" style="background:{color};color:{color}"></span></div>
  <h3>{name}</h3><p class="svc-p">{cosa}</p>
  <div class="svc-fig">{fig}</div><div class="svc-cap">{cap}</div>
  <div class="svc-per"><span class="k">Per chi</span>{per}</div>
</div>'''


def s_overview() -> str:
    cards = "".join([
        card("01", GOLD, "Rendimento Contrattuale", "Affidi un capitale. Il contratto dice quanto ricevi e quando.",
             "20%", "all'anno, scritto nel contratto", "cerca stabilità"),
        card("02", GREEN, "Matched Trading", "Due conti che si coprono a vicenda. Il risultato è un calcolo.",
             "≈ 500 €", "in media ogni 3.000 €", "vuole un metodo matematico"),
        card("03", CYAN, "Copy Trading", "Il tuo conto copia in automatico un algoritmo sulle valute.",
             FX["media_mensile"], "al mese in media, su 23 mesi", "punta alla crescita"),
        card("04", VIOLET, "Gruppo Privato", "Ti scriviamo noi cosa fare. Tu lo copi sul tuo conto.",
             "30 s", "per copiare un'operazione", "vuole gestire da solo i suoi soldi"),
    ])
    return f'''
<section class="slide">{frame()}
  {top("Panoramica · in 30 secondi", 2)}
  <h2>Quattro servizi, <span class="hl">in parole semplici.</span></h2>
  <div class="svc-row">{cards}</div>
  <div class="spectrum"><span class="k">Puoi scegliere un solo servizio o combinarli</span><div class="spec-line"></div></div>
  <p class="fine">I servizi sono diversi per natura, conto, broker e periodo dei dati: i numeri non vanno confrontati tra loro senza leggere le note di ogni pagina.</p>
  {foot()}
</section>'''


def svc_head(n: str, color: str, name: str, tag: str, num: int) -> str:
    return f'''{top(f"Servizio {n} · {name}", num, color)}
  <div class="sv-title"><span class="sv-n" style="color:{color}">{n}</span><div><h2 class="sv-h2">{name}</h2><p class="sv-tag">{tag}</p></div></div>'''


def s_svc1() -> str:
    steps = "".join(f'<div class="st"><div class="st-n" style="--c:{GOLD}">{i}</div><div class="st-t">{t}</div></div>'
                    for i, t in ((1, "Scegli quanto investire e per quanto tempo"), (2, "Firmi il contratto: rendimento e garanzie sono scritti"),
                                 (3, "Ricevi il 20% all'anno alle scadenze concordate")))
    return f'''
<section class="slide">{frame()}
  {svc_head("01", GOLD, "Rendimento Contrattuale", "Un rendimento fisso, scritto nel contratto.", 3)}
  <div class="cols">
    <div class="col-l">
      <div class="hud pan" style="--c:{GOLD}"><div class="k pk">01 · Cos'è</div>
        <p class="big-p">Affidi un capitale per un periodo stabilito. Il contratto dice in anticipo quanto ricevi, quando lo ricevi e quali garanzie hai.</p></div>
      <div class="hud pan" style="--c:{GOLD}"><div class="k pk">02 · Come funziona</div><div class="steps">{steps}</div></div>
    </div>
    <div class="hud pan col-r" style="--c:{GOLD}"><div class="k pk">03 · I numeri</div>
      <div class="num-row">{ring(0.20, GOLD, "20%", "all'anno")}
        <div class="ex"><div class="k">Esempio</div><div class="ex-v">10.000 €</div><div class="ex-l">investiti</div>
          <div class="ex-arrow">↓</div><div class="ex-v gold">+2.000 €</div><div class="ex-l">ogni anno</div></div></div>
      <div class="facts"><div><span class="k">Reinvestendo, in 5 anni</span><b>24.883 €</b></div>
        <div><span class="k">Pagamenti</span>alle scadenze del contratto</div><div><span class="k">Garanzie</span>scritte nel contratto</div></div>
      <p class="note">Esempio al lordo di costi e imposte. Fanno fede rendimento e garanzie scritti nel contratto.</p>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc2() -> str:
    bars = "".join(
        f'<div class="br"><span class="br-k">{eur(c)}</span><div class="br-t"><div class="br-f" style="width:{c / 12000 * 100:.0f}%"></div></div>'
        f'<span class="br-v">+{eur(c / 6)}</span></div>' for c in (3000, 6000, 9000, 12000))
    return f'''
<section class="slide">{frame()}
  {svc_head("02", GREEN, "Matched Trading", "Il metodo matematico.", 4)}
  <div class="cols">
    <div class="col-l">
      <div class="hud pan" style="--c:{GREEN}"><div class="k pk">01 · Cos'è</div>
        <p class="big-p">Due conti collegati fanno scommesse opposte sullo stesso mercato: quando uno perde, l'altro guadagna. Uno è presso una prop firm (presta capitale a chi supera una prova), l'altro presso un broker.</p></div>
      <div class="hud pan" style="--c:{GREEN}"><div class="k pk">02 · Come funziona</div>
        {schema_matched()}
        <p class="mid-p mt-foot">Il calcolo punta a far guadagnare il conto vincente più di quanto perde l'altro. Non è garantito: in alcuni casi possono perdere entrambi (regole della prop firm, salti di prezzo).</p>
      </div>
    </div>
    <div class="hud pan col-r" style="--c:{GREEN}"><div class="k pk">03 · I numeri</div>
      <div class="num-row">{ring(500 / 3000, GREEN, "≈ 16,7%", "per ciclo")}
        <div class="ex"><div class="k">In media</div><div class="ex-v green">+500 €</div><div class="ex-l">ogni 3.000 € impiegati</div>
</div></div>
      <div class="k sub-k">Si cresce a scaglioni da 3.000 €</div>
      <div class="bars">{bars}</div>
      <p class="note">Media statistica, non garantita: dipende dalle regole delle prop firm e dai costi di esecuzione.</p>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc3() -> str:
    facts = "".join(f'<div class="fx"><div class="fx-v">{v}</div><div class="fx-l">{l}</div></div>' for v, l in (
        ("10", "coppie di valute seguite dall'algoritmo"),
        ("24/5", "lavora in automatico, 24 ore su 24 nei giorni di mercato"),
        ("10%", "stop automatico: si ferma tutto se il conto perde il 10%"),
    ))
    return f'''
<section class="slide">{frame()}
  {svc_head("03", CYAN, "Copy Trading Algoritmico", "Il tuo conto copia un algoritmo, in automatico.", 5)}
  <div class="cols">
    <div class="col-l">
      <div class="hud pan" style="--c:{CYAN}"><div class="k pk">01 · Cos'è</div>
        <p class="big-p">Il tuo conto, a tuo nome, copia in automatico le operazioni di un algoritmo che lavora sul Forex, il mercato delle valute. Non devi fare niente: le operazioni si replicano da sole.</p></div>
      <div class="hud pan" style="--c:{CYAN}"><div class="k pk">02 · Come funziona</div>
        <p class="mid-p">Alcune valute si muovono quasi sempre insieme. Quando si allontanano più del normale, l'algoritmo scommette che torneranno vicine, come un elastico. Non deve indovinare se il mercato sale o scende.</p>
        <div class="legend"><span><i style="background:{CYAN}"></i>Valuta A</span><span><i style="background:#C8D6E6"></i>Valuta B</span><span><i class="sq"></i>distanza tra le due</span></div>
        {chart_elastico()}</div>
    </div>
    <div class="hud pan col-r" style="--c:{CYAN}"><div class="k pk">03 · In breve</div>
      <div class="fxs">{facts}</div>
      <div class="teaser"><div class="k">Risultato del conto di riferimento</div><div class="teaser-v">{FX["rendimento"]}</div>
        <div class="ex-l">in 23 mesi · {FX["media_mensile"]} al mese in media · i numeri alla pagina seguente</div></div>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc4() -> str:
    steps = "".join(f'<div class="st"><div class="st-n" style="--c:{VIOLET}">{i}</div><div class="st-t">{t}</div></div>'
                    for i, t in ((1, "Ti arriva un messaggio nel gruppo privato"),
                                 (2, "Copi l'operazione sul tuo conto: bastano 30 secondi"),
                                 (3, "Ripeti ogni volta che arriva un nuovo messaggio")))
    msg = "".join(f'<div class="msg-r"><span class="k">{k}</span><span>{v}</span></div>' for k, v in (
        ("Cosa", "EUR/USD"), ("Come", "compra"), ("Quando", "adesso")))
    return f'''
<section class="slide">{frame()}
  {svc_head("04", VIOLET, "Gruppo Privato", "Ti diciamo noi cosa fare. Tu copi e incolli.", 7)}
  <div class="cols">
    <div class="col-l">
      <div class="hud pan" style="--c:{VIOLET}"><div class="k pk">01 · Cos'è</div>
        <p class="big-p">Entri in un gruppo privatissimo. Lì ti scriviamo noi cosa fare, quando farlo e come. Tu lo ripeti sul tuo conto, in autonomia: i soldi restano tuoi.</p></div>
      <div class="hud pan" style="--c:{VIOLET}"><div class="k pk">02 · Come funziona</div><div class="steps">{steps}</div></div>
    </div>
    <div class="hud pan col-r" style="--c:{VIOLET}"><div class="k pk">03 · In breve</div>
      <div class="num-row">{ring(0.5, VIOLET, "30 s", "per operazione", 176)}
        <div class="ex"><div class="k">Si parte da zero</div><div class="ex-v violet">Guida PDF</div><div class="ex-l">inclusa, passo passo</div>
          <div class="ex-l2">Basta il telefono e un po' di attenzione ai messaggi durante il giorno.</div></div></div>
      <div class="msg"><div class="msg-h"><i class="pulse" style="--c:{VIOLET}"></i><span class="k">Esempio di messaggio</span></div>{msg}</div>
      <p class="note">Le indicazioni sono uguali per tutti e non sono una consulenza personalizzata: sei tu a scegliere se copiarle. Ogni operazione può andare in perdita.</p>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc3_numeri() -> str:
    stats = "".join(f'<div class="sr"><div class="sr-v">{v}</div><div class="sr-l"><b>{t}</b>{d}</div></div>' for v, t, d in (
        (FX["media_mensile"], "Guadagno medio al mese", ""),
        (FX["max_dd"], "Discesa massima", " · il primo numero da leggere: il calo più grande dal punto più alto (max drawdown)"),
        (FX["win_rate"], "Operazioni in guadagno", " · su 100 operazioni, 75 chiuse in positivo (win rate)"),
        (FX["profit_factor"], "Profit factor", " · per ogni 1 € perso, 2,18 € guadagnati"),
        (FX["rend_dd"], "Rendimento / discesa", " · guadagno totale diviso la discesa massima"),
        (FX["operazioni"], "Operazioni", f" · durata media {FX['durata_media']}"),
    ))
    return f'''
<section class="slide">{frame()}
  {top("Servizio 03 · I numeri reali", 6, CYAN)}
  <div class="n-title"><h2>I numeri reali: <span class="hl">{FX["rendimento"]} in 23 mesi.</span></h2><span class="k chip">Track record verificato · Myfxbook</span></div>
  <div class="n-row">
    <div class="hud pan n-chart" style="--c:{CYAN}"><div class="k pk">Crescita del conto</div>{chart_equity()}</div>
    <div class="hud pan n-stats" style="--c:{CYAN}"><div class="k pk">Cosa dicono i numeri</div>{stats}</div>
  </div>
  <div class="hud pan n-hm" style="--c:{CYAN}"><div class="k pk">Rendimento di ogni mese, %</div>{heatmap()}</div>
  <p class="fine">{FX_FONTE}</p>
  {foot()}
</section>'''


def s_legal() -> str:
    items = [("Perdita del capitale", "Il trading su Forex, oro, criptovalute e CFD con leva comporta un rischio elevato: si può perdere una parte o tutto il capitale investito."),
             ("Solo quello che puoi perdere", "Investi solo somme di cui puoi sostenere la perdita totale."),
             ("Risultati passati", "I numeri vengono da conti reali di riferimento in periodi specifici: non sono indicativi dei risultati futuri, che possono essere peggiori."),
             ("La leva amplifica", "La leva aumenta sia i guadagni sia le perdite, anche in poco tempo."),
             ("Differenze tra conti", "Broker, spread, commissioni, swap, latenza, leva e dimensione del conto possono dare risultati diversi dal conto di riferimento."),
             ("Natura del servizio", "Copy trading e gruppo privato non sono consulenza finanziaria personalizzata né gestione di patrimoni per conto terzi: il conto resta intestato al cliente."),
             ("Conta il contratto", "Rendimenti e garanzie del servizio 01 sono solo quelli scritti nel contratto. Gli esempi sono al lordo di costi e imposte."),
             ("Soggetti terzi", "Prop firm e broker hanno regole e costi propri, che possono cambiare in ogni momento."),
             ("Fonti", "Copy trading: Myfxbook, conto reale indicato a pagina 6, aggiornato alle date riportate lì.")]
    cells = "".join(f'<div class="hud lg" style="--c:{GOLD}"><div class="lg-n k">{i + 1:02d}</div><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(items))
    return f'''
<section class="slide">{frame()}
  {top("Avvertenze", 8, GOLD)}
  <h2>Il rischio, <span class="hl gold">per intero.</span></h2>
  <div class="lgs">{cells}</div>
  <p class="fine wide">Documento informativo e riservato: non è un'offerta al pubblico né una sollecitazione all'investimento. Nel copy trading le operazioni della strategia sono replicate sul conto del cliente; le indicazioni del gruppo privato sono uguali per tutti, e ogni decisione e operazione restano del cliente.</p>
  {foot()}
</section>'''


def s_close() -> str:
    steps = "".join(f'<div class="hud cs" style="--c:{CYAN}"><div class="cs-n">{n}</div><h4>{t}</h4><p>{d}</p></div>' for n, t, d in (
        ("01", "Una call di 30 minuti", "Capiamo obiettivi, tempi e quanto rischio sei disposto a prendere."),
        ("02", "Scegliamo insieme", "Uno o più servizi, con i numeri reali davanti."),
        ("03", "Attivazione e report", "Si parte, e ricevi aggiornamenti periodici sui risultati.")))
    ct = "".join(f'<div class="ct"><div class="k">{k}</div><div class="ct-v">{v}</div></div>' for k, v in contatti())
    return f'''
<section class="slide close">{frame()}
  <div class="close-r">{reticle(560, labels=False)}</div>
  <div class="close-in">
    <div class="wm">{logo(28)}<span>{BRAND}</span></div>
    <h1>Iniziare è</h1>{grad_line("semplice.", 66)}
    <div class="css">{steps}</div>
    {f'<div class="cts">{ct}</div>' if ct else ''}
  </div>
  <p class="close-legal">Il trading con leva comporta il rischio di perdere il capitale. I risultati passati non sono indicativi di quelli futuri. Avvertenze complete a pag. 8. Documento riservato.</p>
</section>'''


# ---------------------------------------------------------------- stile
CSS = r"""
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --cyan:#4FD8FF; --green:#5BE38A; --gold:#FFB547; --violet:#C79BFF;
        --txt:#E9F3FB; --txt2:#A3B6CA; --muted:#61768E; --line:rgba(120,200,255,.14); }
html, body { background:#02050A; }
body { font-family:'Inter', system-ui, sans-serif; color:var(--txt); -webkit-font-smoothing:antialiased; }
@media screen { body { display:flex; flex-direction:column; align-items:center; gap:24px; padding:24px 0; } }
.slide { width:1280px; height:720px; position:relative; overflow:hidden; padding:38px 64px 0; isolation:isolate;
  background:radial-gradient(1100px 680px at 80% 12%, #0E2238 0%, #08111D 48%, #04070D 100%);
  break-after:page; page-break-after:always; }
.slide:last-child { break-after:auto; page-break-after:auto; }
.slide::before { content:""; position:absolute; inset:0; z-index:-1;
  background-image:linear-gradient(rgba(79,216,255,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(79,216,255,.045) 1px, transparent 1px);
  background-size:40px 40px;
  -webkit-mask-image:radial-gradient(ellipse 75% 85% at 70% 35%, #000 0%, transparent 80%);
          mask-image:radial-gradient(ellipse 75% 85% at 70% 35%, #000 0%, transparent 80%); }
.frame { position:absolute; inset:16px; pointer-events:none; z-index:0; --b:rgba(79,216,255,.55);
  background:
    linear-gradient(var(--b),var(--b)) top left/22px 1.5px no-repeat, linear-gradient(var(--b),var(--b)) top left/1.5px 22px no-repeat,
    linear-gradient(var(--b),var(--b)) top right/22px 1.5px no-repeat, linear-gradient(var(--b),var(--b)) top right/1.5px 22px no-repeat,
    linear-gradient(var(--b),var(--b)) bottom left/22px 1.5px no-repeat, linear-gradient(var(--b),var(--b)) bottom left/1.5px 22px no-repeat,
    linear-gradient(var(--b),var(--b)) bottom right/22px 1.5px no-repeat, linear-gradient(var(--b),var(--b)) bottom right/1.5px 22px no-repeat; }
.k { font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.2em; text-transform:uppercase; color:#73CDEB; font-weight:500; }
.pulse { width:8px; height:8px; border-radius:50%; display:inline-block; background:var(--c, var(--cyan)); }
.top { position:relative; z-index:1; display:flex; justify-content:space-between; align-items:center; height:22px; }
.top-l { display:flex; align-items:center; gap:12px; }
.top-r { display:flex; align-items:center; gap:22px; }
.pg { font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--cyan); font-weight:600; }
.pg em { font-style:normal; color:var(--muted); }
.rule { position:relative; height:1px; margin-top:12px; background:linear-gradient(90deg, rgba(79,216,255,.45), rgba(79,216,255,.08) 60%, transparent); }
.rule::before { content:""; position:absolute; left:0; top:-1px; width:64px; height:3px; background:var(--cyan); }
.foot { position:absolute; left:64px; right:64px; bottom:24px; display:flex; justify-content:space-between; gap:30px;
  font-size:10px; color:var(--muted); border-top:1px solid rgba(120,200,255,.10); padding-top:10px; }
.foot .k { font-size:9.5px; color:var(--muted); white-space:nowrap; }

h1 { font-family:'Inter Display','Inter',sans-serif; font-weight:600; font-size:66px; line-height:1.04; letter-spacing:-.03em; color:#F4FAFF; }
h2 { font-family:'Inter Display','Inter',sans-serif; font-weight:600; font-size:38px; line-height:1.1; letter-spacing:-.025em; color:#F4FAFF; margin-top:24px; }
h3 { font-size:19px; font-weight:600; letter-spacing:-.01em; color:#F4FAFF; }
h4 { font-size:15px; font-weight:600; color:#F4FAFF; }
p { color:var(--txt2); }
b { color:#F4FAFF; font-weight:600; }
.hl { color:var(--cyan); } .hl.gold { color:var(--gold); }
.gline { display:block; overflow:visible; }
.gline-fb { font-family:'Inter Display','Inter',sans-serif; font-weight:600; color:var(--cyan); line-height:1.12; letter-spacing:-.03em; }

/* pannelli HUD con angoli a staffa */
.hud { position:relative; background:linear-gradient(180deg, rgba(20,40,64,.50), rgba(9,20,34,.55));
  border:1px solid var(--line); border-radius:6px; }
.hud::before { content:""; position:absolute; inset:-1px; pointer-events:none; --b:var(--c, #4FD8FF);
  background:
    linear-gradient(var(--b),var(--b)) top left/14px 2px no-repeat, linear-gradient(var(--b),var(--b)) top left/2px 14px no-repeat,
    linear-gradient(var(--b),var(--b)) top right/14px 2px no-repeat, linear-gradient(var(--b),var(--b)) top right/2px 14px no-repeat,
    linear-gradient(var(--b),var(--b)) bottom left/14px 2px no-repeat, linear-gradient(var(--b),var(--b)) bottom left/2px 14px no-repeat,
    linear-gradient(var(--b),var(--b)) bottom right/14px 2px no-repeat, linear-gradient(var(--b),var(--b)) bottom right/2px 14px no-repeat; }
.pan { padding:16px 22px 18px; }
.pk { margin-bottom:10px; color:var(--c, var(--cyan)); }

/* copertina */
.cover { display:flex; padding:56px 0 0 84px; }
.cover-l { width:640px; position:relative; z-index:2; display:flex; flex-direction:column; }
.wm { display:flex; align-items:center; gap:12px; font-size:14px; letter-spacing:.26em; font-weight:600; color:#F4FAFF; }
.cov-k { display:flex; align-items:center; gap:14px; margin-top:150px; }
.cover h1 { margin-top:22px; }
.cov-sub { font-size:18px; line-height:1.6; margin-top:22px; max-width:520px; }
.cov-st { margin-top:auto; margin-bottom:52px; display:flex; gap:26px; color:var(--muted); }
.cover-r { position:absolute; right:-20px; top:60px; }
.orb-c1 { font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:.24em; fill:#73CDEB; }
.orb-c2 { font-family:'Inter Display','Inter'; font-size:19px; font-weight:600; fill:#F4FAFF; }
.orb-n { font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:600; }
.orb-l1 { font-size:13.5px; font-weight:600; fill:#E9F3FB; }
.orb-l2 { font-size:12px; fill:#7F93AA; }

/* panoramica */
.svc-row { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:28px; }
.svc { padding:20px 20px 18px; height:398px; display:flex; flex-direction:column; }
.svc::after { content:""; position:absolute; left:20px; right:20px; top:0; height:2px; background:var(--c); opacity:.8; }
.svc-h { display:flex; justify-content:space-between; align-items:center; }
.svc-dot { width:8px; height:8px; border-radius:50%; }
.svc h3 { margin-top:16px; }
.svc-p { font-size:14.5px; line-height:1.5; margin-top:10px; }
.svc-fig { margin-top:auto; font-family:'Inter Display','Inter'; font-size:46px; font-weight:600; letter-spacing:-.03em; color:#F4FAFF; }
.svc-cap { font-size:12.5px; color:var(--txt2); margin-top:2px; }
.svc-per { margin-top:16px; padding-top:12px; border-top:1px solid var(--line); font-size:13px; color:#F4FAFF; display:flex; flex-direction:column; gap:4px; }
.svc-per .k { font-size:9.5px; color:var(--muted); }
.spectrum { display:flex; align-items:center; gap:14px; margin-top:18px; }
.spectrum .k { color:var(--muted); font-size:10px; }
.spec-line { flex:1; height:2px; background:linear-gradient(90deg, var(--gold), var(--green), var(--cyan), var(--violet)); position:relative; opacity:.8; }
.spec-line::after { content:""; position:absolute; right:-2px; top:-4px; border-left:7px solid var(--violet); border-top:5px solid transparent; border-bottom:5px solid transparent; }

/* pagine servizio */
.sv-title { display:flex; align-items:center; gap:20px; margin-top:20px; }
.sv-n { font-family:'Inter Display','Inter'; font-size:64px; font-weight:600; letter-spacing:-.04em; line-height:1; opacity:.9; }
.sv-h2 { margin-top:0; font-size:34px; }
.sv-tag { font-size:16px; color:var(--txt2); margin-top:2px; }
.cols { display:flex; gap:18px; margin-top:20px; height:470px; }
.col-l { flex:1; display:flex; flex-direction:column; gap:14px; margin-bottom:48px; }
.col-l .pan:last-child { flex:1; }
.col-r { width:470px; flex:none; display:flex; flex-direction:column; margin-bottom:48px; }
.big-p { font-size:17px; line-height:1.55; }
.mid-p { font-size:14px; line-height:1.45; margin-bottom:6px; }
.steps { display:flex; flex-direction:column; justify-content:space-evenly; gap:16px; height:calc(100% - 26px); }
.col-l .pan:last-child { display:flex; flex-direction:column; }
.st { display:flex; align-items:center; gap:16px; }
.st-n { width:38px; height:38px; flex:none; border-radius:50%; display:grid; place-items:center; font-family:'JetBrains Mono', monospace;
  font-weight:600; color:var(--c); border:1.5px solid var(--c); }
.st-t { font-size:17px; color:#F4FAFF; }
.num-row { display:flex; align-items:center; gap:22px; }
.ring-w { position:relative; flex:none; }
.ring-w svg { position:absolute; inset:0; }
.ring-t { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.ring-v { font-family:'Inter Display','Inter'; font-size:36px; font-weight:600; letter-spacing:-.03em; color:#F4FAFF; }
.ring-s { font-size:9.5px; margin-top:2px; color:var(--txt2); }
.ex { display:flex; flex-direction:column; }
.ex-v { font-family:'Inter Display','Inter'; font-size:30px; font-weight:600; letter-spacing:-.02em; color:#F4FAFF; margin-top:4px; }
.ex-v.gold { color:var(--gold); }
.ex-v.green { color:var(--green); font-size:40px; }
.ex-l { font-size:13px; color:var(--txt2); }
.ex-l2 { font-size:12.5px; color:var(--txt2); margin-top:12px; }
.ex-arrow { color:var(--muted); font-size:18px; margin:4px 0 -2px; }
.facts { margin-top:16px; border-top:1px solid var(--line); }
.facts div { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid var(--line); font-size:15px; }
.facts .k { color:var(--txt2); font-size:10px; }
.note { font-size:11.5px; color:var(--muted); margin-top:auto; line-height:1.5; }
.sub-k { margin-top:14px; color:var(--txt2); font-size:10px; }
.bars { display:flex; flex-direction:column; gap:9px; margin-top:10px; }
.br { display:grid; grid-template-columns:76px 1fr 78px; align-items:center; gap:10px; font-size:13px; font-variant-numeric:tabular-nums; }
.br-k { color:var(--txt2); text-align:right; }
.br-t { height:12px; background:rgba(255,255,255,.05); border-radius:3px; }
.br-f { height:100%; background:var(--green); border-radius:0 3px 3px 0; }
.br-v { color:#F4FAFF; font-weight:600; }
.schema { display:block; margin-top:4px; }
.schema .sm-v { font-family:'Inter Display','Inter'; font-size:21px; font-weight:600; fill:#F4FAFF; }
.schema .sm-r { font-family:'Inter Display','Inter'; font-size:23px; font-weight:600; }
.schema .sm-k { font-family:'JetBrains Mono', monospace; font-size:9.5px; letter-spacing:.16em; fill:#73CDEB; }
.schema .sm-t { font-size:15px; font-weight:600; fill:#F4FAFF; }
.schema .sm-s { font-size:12.5px; fill:#A3B6CA; }
.mt-foot { margin-top:10px; margin-bottom:0; }
.legend { display:flex; gap:16px; font-size:11.5px; color:var(--txt2); margin-top:4px; }
.legend span { display:flex; align-items:center; gap:7px; }
.legend i { width:14px; height:3px; border-radius:2px; display:inline-block; }
.legend i.sq { width:12px; height:10px; border-radius:2px; background:rgba(79,216,255,.25); }
.ex-v.violet { color:var(--violet); font-size:32px; }
.msg { margin-top:16px; border:1px solid rgba(199,155,255,.35); border-radius:10px 10px 10px 2px; background:rgba(199,155,255,.06); padding:12px 16px; }
.msg-h { display:flex; align-items:center; gap:10px; margin-bottom:6px; }
.msg-h .k { color:var(--violet); }
.msg-r { display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(199,155,255,.15); font-size:14px; color:#F4FAFF; }
.msg-r:last-child { border-bottom:0; }
.msg-r .k { color:var(--txt2); font-size:10px; }
.fxs { display:flex; flex-direction:column; gap:14px; }
.fx { display:flex; align-items:center; gap:18px; padding-bottom:14px; border-bottom:1px solid var(--line); }
.fx-v { font-family:'Inter Display','Inter'; font-size:38px; font-weight:600; letter-spacing:-.03em; color:#F4FAFF; width:92px; flex:none; }
.fx-l { font-size:14px; line-height:1.45; color:var(--txt2); }
.teaser { margin-top:auto; padding:16px 18px; border:1px solid rgba(79,216,255,.35); border-radius:6px; background:rgba(79,216,255,.06); }
.teaser-v { font-family:'Inter Display','Inter'; font-size:46px; font-weight:600; letter-spacing:-.03em; color:var(--cyan); margin-top:4px; }

/* numeri reali */
.n-title { display:flex; justify-content:space-between; align-items:flex-end; }
.n-title h2 { font-size:34px; }
.chip { color:var(--txt2); font-size:10px; border:1px solid var(--line); border-radius:4px; padding:5px 10px; margin-bottom:4px; }
.n-row { display:flex; gap:16px; margin-top:16px; }
.n-chart { width:650px; flex:none; padding-bottom:10px; }
.n-stats { flex:1; padding-bottom:8px; }
.sr { display:flex; align-items:baseline; gap:14px; padding:6px 0; border-bottom:1px solid var(--line); }
.sr:last-child { border-bottom:0; }
.sr-v { font-family:'Inter Display','Inter'; font-size:22px; font-weight:600; color:#F4FAFF; width:92px; flex:none; letter-spacing:-.02em; }
.sr:nth-child(3) .sr-v { color:var(--gold); }
.sr-l { font-size:12px; line-height:1.4; color:var(--txt2); }
.sr-l b { font-size:12.5px; }
.n-hm { margin-top:14px; padding:12px 22px 14px; }
.n-hm .pk { margin-bottom:8px; }
.hm { display:grid; grid-template-columns:48px repeat(12, 1fr) 80px; gap:4px; }
.hm-c { height:28px; border-radius:3px; display:grid; place-items:center; font-size:12px; font-weight:500; font-variant-numeric:tabular-nums; }
.hm-h { height:16px; color:var(--muted); font-family:'JetBrains Mono', monospace; font-size:10px; }
.hm-y { color:var(--txt2); font-size:12px; }
.hm-tot { color:#F4FAFF; font-weight:700; background:rgba(79,216,255,.10); border:1px solid rgba(79,216,255,.35); }
.hm-na { border:1px dashed rgba(127,147,170,.25); }
.fine { font-size:9.5px; line-height:1.45; color:var(--muted); margin-top:8px; }
.fine.wide { font-size:12px; margin-top:18px; max-width:1100px; }
.chart text { font-family:'Inter', sans-serif; }
.chart .grid { stroke:rgba(160,200,240,.08); stroke-width:1; }
.chart .base { stroke:rgba(160,200,240,.25); stroke-width:1; }
.chart .tick { font-size:11px; fill:#6F849C; font-variant-numeric:tabular-nums; }
.chart .endv { font-size:14px; fill:#F4FAFF; font-weight:700; }
.chart .lab { font-size:12px; fill:#A3B6CA; font-weight:500; }
.chart .ann { font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:.08em; font-weight:600; }
.chart .tag { font-family:'JetBrains Mono', monospace; font-size:9px; letter-spacing:.14em; fill:#61768E; }

/* avvertenze */
.lgs { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:20px; }
.lg { padding:14px 18px 15px; min-height:126px; }
.lg-n { color:var(--gold); }
.lg h4 { margin-top:10px; font-size:16px; }
.lg p { font-size:13px; line-height:1.45; margin-top:5px; }
.lg h4 { font-size:15px !important; }

/* chiusura */
.close { padding:56px 84px 0; }
.close-r { position:absolute; right:-150px; top:60px; opacity:.85; }
.close-in { position:relative; z-index:2; }
.close h1 { margin-top:70px; }
.close .wm { letter-spacing:.02em; font-size:19px; }
.css { display:grid; grid-template-columns:repeat(3, 250px); gap:14px; margin-top:34px; }
.cs { padding:16px 18px 18px; }
.cs-n { font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--cyan); font-weight:600; }
.cs h4 { margin-top:8px; }
.cs p { font-size:13px; line-height:1.45; margin-top:6px; }
.cts { display:grid; grid-template-columns:repeat(3, auto); justify-content:start; column-gap:56px; margin-top:30px; }
.ct-v { margin-top:8px; font-size:15px; }
.close-legal { position:absolute; left:84px; right:84px; bottom:30px; font-size:10px; color:var(--muted); }
"""

DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g-title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8FE6FF"/><stop offset=".45" stop-color="#6FDFFF"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="g-area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".32"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<radialGradient id="g-glow"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset=".5" stop-color="#1A6E9A" stop-opacity=".08"/><stop offset="1" stop-color="#04070D" stop-opacity="0"/></radialGradient>
</defs></svg>"""


def build() -> None:
    slides = [s_cover(), s_overview(), s_svc1(), s_svc2(), s_svc3(), s_svc3_numeri(), s_svc4(), s_legal(), s_close()]
    assert len(slides) == TOTAL, len(slides)
    html = ('<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
            f'<title>Ecosistema di investimento</title><style>{CSS}</style></head>'
            f'<body>{DEFS}{"".join(slides)}</body></html>')
    OUT.write_text(html, encoding="utf-8")
    print(f"scritto {OUT} ({len(html) // 1024} KB, {len(slides)} pagine)")


if __name__ == "__main__":
    build()
