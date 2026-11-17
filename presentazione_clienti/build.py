#!/usr/bin/env python3
"""Genera presentazione.html (16:9, 1280x720 px per pagina).

Poi: node render.js  ->  Presentazione_Ecosistema.pdf
I dati segnaposto sono marcati con ph(): vanno sostituiti con i dati reali.
"""
from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "presentazione.html"

BRAND = "NOME AZIENDA"
TOTAL = 15

BLUE, TEAL, GOLD, SLATE = "#2F6BFF", "#0E9F8E", "#C7871F", "#64748B"
GRAY_SERIES = "#A6AFBD"


# ---------------------------------------------------------------- helpers
def eur(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".") + " €"


def num(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".")


def ph(txt: str = "da inserire") -> str:
    return f'<span class="ph">{txt}</span>'


def logo(size: int = 22) -> str:
    return (
        f'<svg class="logo" width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true">'
        '<rect x="1" y="1" width="22" height="22" rx="7" fill="url(#g-brand)"/>'
        '<circle cx="11" cy="13" r="4.6" fill="none" stroke="#fff" stroke-width="1.9"/>'
        '<circle cx="17.6" cy="6.6" r="1.8" fill="#fff"/></svg>'
    )


ICONS = {
    "shield": '<path d="M12 3l7 3v5.2c0 4.4-3 8.1-7 9.8-4-1.7-7-5.4-7-9.8V6l7-3z"/><path d="M8.6 12.1l2.4 2.4 4.4-4.7"/>',
    "swap": '<path d="M5 8h13"/><path d="M15 4.5L18.5 8 15 11.5"/><path d="M19 16H6"/><path d="M9 12.5L5.5 16 9 19.5"/>',
    "wave": '<path d="M3 12h3.2l2.3-6 4.4 12 2.6-7.2 1.3 1.2H21"/>',
    "plus": '<circle cx="12" cy="12" r="8.5"/><path d="M12 8.2v7.6M8.2 12h7.6"/>',
    "doc": '<path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20z"/><path d="M14 3.5V8h4"/><path d="M9.5 12.5h5M9.5 16h5"/>',
    "eye": '<path d="M2.8 12s3.4-6.2 9.2-6.2 9.2 6.2 9.2 6.2-3.4 6.2-9.2 6.2S2.8 12 2.8 12z"/><circle cx="12" cy="12" r="2.6"/>',
    "gauge": '<path d="M4.2 16.5a8.5 8.5 0 1 1 15.6 0"/><path d="M12 13.2l3.6-4.4"/><circle cx="12" cy="13.6" r="1.1"/>',
    "grid": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    "cpu": '<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><path d="M10 3.5v3M14 3.5v3M10 17.5v3M14 17.5v3M3.5 10h3M3.5 14h3M17.5 10h3M17.5 14h3"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.4 2.6 3.6 5.4 3.6 8.5s-1.2 5.9-3.6 8.5c-2.4-2.6-3.6-5.4-3.6-8.5S9.6 6.1 12 3.5z"/>',
    "arrows": '<path d="M4 12h16"/><path d="M8 8l-4 4 4 4"/><path d="M16 8l4 4-4 4"/>',
}


def icon(name: str, color: str, size: int = 22) -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


FONT_TITLE = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"
TITLE_CACHE = HERE / "titoli_svg.json"


def _text_to_path(text: str, size: int, tracking_em: float) -> tuple[str, float]:
    """Converte il testo in tracciati vettoriali (serve fonttools + uharfbuzz).

    Il riempimento sfumato su <text> viene reso male da alcuni lettori PDF:
    sui tracciati invece e' affidabile ovunque.
    """
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    data = Path(FONT_TITLE).read_bytes()
    face = hb.Face(data)
    font = hb.Font(face)
    upm = face.upem
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    tt = TTFont(FONT_TITLE)
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upm
    x = 0.0
    pen = SVGPathPen(gs)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, size * 0.86 - pos.y_offset * scale))
        gs[name].draw(tp)
        x += pos.x_advance * scale + tracking_em * size
    return pen.getCommands(), x


def grad_line(text: str, size: int = 62, tracking_em: float = -0.032) -> str:
    """Riga di titolo con riempimento sfumato, come tracciato SVG (nitido nel PDF)."""
    import json

    key = f"{text}|{size}|{tracking_em}"
    cache = json.loads(TITLE_CACHE.read_text()) if TITLE_CACHE.exists() else {}
    try:
        d, w = _text_to_path(text, size, tracking_em)
        cache[key] = [d, w]
        TITLE_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0))
    except ImportError:
        if key not in cache:  # ripiego: testo a tinta unita
            return f'<div class="gline-fallback" style="font-size:{size}px">{text}</div>'
        d, w = cache[key]
    h = round(size * 1.12)
    return (
        f'<svg class="gline" width="{w + 4:.0f}" height="{h}" viewBox="0 0 {w + 4:.0f} {h}" role="img" aria-label="{text}">'
        f'<path d="{d}" fill="url(#g-title)"/></svg>'
    )


def top(eyebrow: str, n: int, color: str | None = None) -> str:
    dot = f'<i class="dot" style="background:{color}"></i>' if color else '<i class="dot dot-grad"></i>'
    return (
        f'<header class="top"><div class="eyebrow">{dot}{eyebrow}</div>'
        f'<div class="top-r"><span class="wm-mini">{logo(16)}{BRAND}</span>'
        f'<span class="pg">{n:02d} <em>/ {TOTAL}</em></span></div></header>'
    )


RISK_LINE = (
    "I risultati passati non sono garanzia di risultati futuri. Ogni investimento comporta il rischio "
    "di perdita, anche totale, del capitale. Leggi le Avvertenze a pag. 14."
)


def foot(risk: bool = True) -> str:
    left = RISK_LINE if risk else "Documento riservato · finalità esclusivamente informative"
    return f'<footer class="foot"><span>{left}</span><span>Documento riservato</span></footer>'


def col_path(x: float, ytop: float, w: float, ybase: float, r: float = 4) -> str:
    """Barra verticale: angoli arrotondati in alto, squadrata sulla base."""
    r = min(r, max(ybase - ytop, 0))
    return (
        f"M{x:.1f},{ybase:.1f} V{ytop + r:.1f} A{r},{r} 0 0 1 {x + r:.1f},{ytop:.1f} "
        f"H{x + w - r:.1f} A{r},{r} 0 0 1 {x + w:.1f},{ytop + r:.1f} V{ybase:.1f} Z"
    )


def hbar_path(x0: float, y: float, xend: float, h: float, r: float = 4) -> str:
    """Barra orizzontale: squadrata sulla base (x0), arrotondata in punta."""
    r = min(r, max(xend - x0, 0))
    return (
        f"M{x0:.1f},{y:.1f} H{xend - r:.1f} A{r},{r} 0 0 1 {xend:.1f},{y + r:.1f} "
        f"V{y + h - r:.1f} A{r},{r} 0 0 1 {xend - r:.1f},{y + h:.1f} H{x0:.1f} Z"
    )


# ---------------------------------------------------------------- charts
def chart_growth() -> str:
    """Servizio 01: 10.000 EUR al 20% annuo, incassando vs reinvestendo."""
    W, H = 690, 396
    ml, mr, mt, mb = 66, 92, 18, 40
    pw, phh = W - ml - mr, H - mt - mb
    ymax = 30000
    xs = list(range(0, 6))
    simple = [10000 + 2000 * t for t in xs]
    comp = [10000 * 1.2**t for t in xs]

    def X(i: int) -> float:
        return ml + pw * i / 5

    def Y(v: float) -> float:
        return mt + phh * (1 - v / ymax)

    o: list[str] = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
                    'aria-label="Crescita di 10.000 euro al 20% annuo in 5 anni">']
    for t in range(0, ymax + 1, 5000):
        o.append(f'<line class="{"base" if t == 0 else "grid"}" x1="{ml}" x2="{W - mr + 20}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>')
        o.append(f'<text class="tick" x="{ml - 12}" y="{Y(t) + 4:.1f}" text-anchor="end">{num(t)}</text>')
    for i in xs:
        lab = "Oggi" if i == 0 else f"Anno {i}"
        o.append(f'<text class="tick" x="{X(i):.1f}" y="{H - mb + 24}" text-anchor="middle">{lab}</text>')
    # area wash under the story series
    pts_c = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in zip(xs, comp))
    o.append(f'<polygon points="{X(0):.1f},{Y(0):.1f} {pts_c} {X(5):.1f},{Y(0):.1f}" fill="{GOLD}" opacity="0.10"/>')
    pts_s = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in zip(xs, simple))
    o.append(f'<polyline points="{pts_s}" fill="none" stroke="{GRAY_SERIES}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<polyline points="{pts_c}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i in xs:
        o.append(f'<circle cx="{X(i):.1f}" cy="{Y(simple[i]):.1f}" r="4.5" fill="{GRAY_SERIES}" stroke="#fff" stroke-width="2"/>')
        o.append(f'<circle cx="{X(i):.1f}" cy="{Y(comp[i]):.1f}" r="4.5" fill="{GOLD}" stroke="#fff" stroke-width="2"/>')
    # end labels
    o.append(f'<text class="endv" x="{X(5) + 12:.1f}" y="{Y(comp[5]) + 5:.1f}">{eur(comp[5])}</text>')
    o.append(f'<text class="endv" x="{X(5) + 12:.1f}" y="{Y(simple[5]) + 5:.1f}">{eur(simple[5])}</text>')
    o.append("</svg>")
    return "".join(o)


def chart_tranches() -> str:
    """Servizio 02: scaglioni da 3.000 EUR -> risultato medio per ciclo."""
    W, H = 640, 390
    ml, mr, mt, mb = 120, 76, 6, 34
    pw = W - ml - mr
    caps = [3000, 6000, 9000, 12000, 15000]
    res = [c / 3000 * 500 for c in caps]
    xmax = 3000
    bh, step = 26, 70

    def X(v: float) -> float:
        return ml + pw * v / xmax

    o = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Risultato medio per ciclo in base allo scaglione di capitale">']
    plot_bottom = mt + step * len(caps)
    for t in range(0, xmax + 1, 500):
        o.append(f'<line class="{"base" if t == 0 else "grid"}" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{mt}" y2="{plot_bottom:.1f}"/>')
        if t % 1000 == 0:
            o.append(f'<text class="tick" x="{X(t):.1f}" y="{plot_bottom + 22:.1f}" text-anchor="middle">{num(t)} €</text>')
    for i, (c, r) in enumerate(zip(caps, res)):
        y = mt + step * i + (step - bh) / 2
        o.append(f'<text class="cat" x="{ml - 16}" y="{y + bh / 2 + 5:.1f}" text-anchor="end">{eur(c)}</text>')
        o.append(f'<path d="{hbar_path(X(0), y, X(r), bh)}" fill="{TEAL}"/>')
        o.append(f'<text class="endv" x="{X(r) + 10:.1f}" y="{y + bh / 2 + 5:.1f}">+{eur(r)}</text>')
    o.append("</svg>")
    return "".join(o)


def chart_mean_reversion() -> str:
    """Servizio 03: schema illustrativo (NON dati reali) della mean reversion."""
    W, H = 720, 392
    ml, mr, mt, mb = 14, 14, 30, 14
    pw, phh = W - ml - mr, H - mt - mb
    N = 420
    mean, price = [], []
    for i in range(N):
        t = i / (N - 1)
        m = 50 + 5.0 * math.sin(2 * math.pi * (0.65 * t + 0.08))
        amp = 0.70 + 0.40 * math.sin(2 * math.pi * (1.0 * t + 0.15))
        d = 9.0 * amp * math.sin(2 * math.pi * (3.3 * t + 0.02))
        d += 0.9 * math.sin(2 * math.pi * 19 * t) + 0.5 * math.sin(2 * math.pi * 33 * t + 1.3)
        mean.append(m)
        price.append(m + d)
    k = 6.0
    lo = min(min(price), min(mean) - k) - 4
    hi = max(max(price), max(mean) + k) + 4

    def X(i: int) -> float:
        return ml + pw * i / (N - 1)

    def Y(v: float) -> float:
        return mt + phh * (1 - (v - lo) / (hi - lo))

    # apertura quando |scarto| esce dalla fascia, chiusura quando lo scarto torna a zero
    entries, exits = [], []
    open_side = 0
    for i in range(1, N):
        dev, pdev = price[i] - mean[i], price[i - 1] - mean[i - 1]
        if open_side == 0 and abs(dev) > k >= abs(pdev):
            open_side = 1 if dev > 0 else -1
            entries.append(i)
        elif open_side != 0 and (dev * open_side) <= 0:
            exits.append(i)
            open_side = 0
    entries = entries[: len(exits)]

    line = lambda arr: " ".join(f"{X(i):.1f},{Y(arr[i]):.1f}" for i in range(N))
    up = [m + k for m in mean]
    dn = [m - k for m in mean]
    band = line(up) + " " + " ".join(f"{X(i):.1f},{Y(dn[i]):.1f}" for i in reversed(range(N)))
    o = [f'<svg class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         'aria-label="Schema illustrativo della strategia di ritorno alla media">']
    o.append(f'<polygon points="{band}" fill="{BLUE}" opacity="0.07"/>')
    o.append(f'<polyline points="{line(up)}" fill="none" stroke="#C9D7FF" stroke-width="1"/>')
    o.append(f'<polyline points="{line(dn)}" fill="none" stroke="#C9D7FF" stroke-width="1"/>')
    o.append(f'<polyline points="{line(mean)}" fill="none" stroke="#7C8494" stroke-width="1.8"/>')
    o.append(f'<polyline points="{line(price)}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round"/>')
    for e, x in zip(entries, exits):
        o.append(f'<line x1="{X(e):.1f}" y1="{Y(price[e]):.1f}" x2="{X(x):.1f}" y2="{Y(price[x]):.1f}" stroke="{TEAL}" stroke-width="1.4" stroke-opacity="0.75"/>')
    for e in entries:
        o.append(f'<circle cx="{X(e):.1f}" cy="{Y(price[e]):.1f}" r="5.5" fill="#0B1220" stroke="#fff" stroke-width="2"/>')
    for x in exits:
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(price[x]):.1f}" r="5.5" fill="{TEAL}" stroke="#fff" stroke-width="2"/>')
    # annotazioni con linea guida, posizionate fuori dalla fascia
    if entries:
        j = 1 if len(entries) > 2 else 0
        e, x = entries[j], exits[j]
        above = price[e] > mean[e]
        ey = Y(price[e])
        ly = Y(max(price[e - 25:e + 25]) if above else min(price[e - 25:e + 25])) + (-26 if above else 30)
        o.append(f'<line x1="{X(e):.1f}" y1="{ey + (-8 if above else 8):.1f}" x2="{X(e):.1f}" y2="{ly + (6 if above else -16):.1f}" stroke="#0B1220" stroke-width="1"/>')
        o.append(f'<text class="ann" x="{X(e):.1f}" y="{ly:.1f}" text-anchor="middle">Lontano dalla media → apertura</text>')
        xy = Y(price[x])
        ly2 = Y(dn[x] if above else up[x]) + (40 if above else -34)
        o.append(f'<line x1="{X(x):.1f}" y1="{xy + (8 if above else -8):.1f}" x2="{X(x):.1f}" y2="{ly2 + (-16 if above else 6):.1f}" stroke="{TEAL}" stroke-width="1"/>')
        o.append(f'<text class="ann ann-teal" x="{X(x):.1f}" y="{ly2:.1f}" text-anchor="middle">Ritorno alla media → chiusura</text>')
    o.append(f'<text class="tag" x="{W - mr}" y="12" text-anchor="end">SCHEMA ILLUSTRATIVO · NON SONO DATI REALI</text>')
    o.append("</svg>")
    return "".join(o)


def risk_ruler() -> str:
    """Servizio 03: righello della perdita, 0-100% del capitale."""
    seg = [(17, "17%", "#2F6BFF", "#fff"), (13, "", "#A9C0FF", "#0B1220"), (70, "Area esclusa: oltre il 30% la copia si interrompe", "#EEF1F6", "#475467")]
    parts, x = [], 0
    for w, lab, fill, ink in seg:
        parts.append(
            f'<div class="seg" style="left:{x}%;width:calc({w}% - 3px);background:{fill};color:{ink}">{lab}</div>'
        )
        x += w
    return (
        '<div class="ruler">'
        + "".join(parts)
        + '<div class="stop" style="left:calc(30% - 2.5px)"><span>EQUITY STOP · 30%</span></div>'
        + '<div class="ruler-axis"><span>0%</span><span style="left:17%">17%</span><span style="left:30%">30%</span>'
          '<span style="left:100%">100% del capitale</span></div>'
        + "</div>"
    )


def rings() -> str:
    S, c = 640, 320
    o = [f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" aria-hidden="true"><circle cx="{c}" cy="{c}" r="300" fill="url(#g-glow)"/>']
    for r, a in ((120, 0.14), (200, 0.10), (280, 0.07)):
        o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{a}"/>')
    o.append(f'<path d="M{c + 200 * math.cos(-2.4):.1f},{c + 200 * math.sin(-2.4):.1f} A200,200 0 0 1 {c + 200 * math.cos(-0.3):.1f},{c + 200 * math.sin(-0.3):.1f}" fill="none" stroke="url(#g-brand-h)" stroke-width="2" stroke-linecap="round"/>')
    for deg, col, r in ((-150, "#E0A43C", 200), (-62, "#22C2AE", 280), (38, "#5B8CFF", 200), (128, "#94A3B8", 280)):
        a = math.radians(deg)
        o.append(f'<circle cx="{c + r * math.cos(a):.1f}" cy="{c + r * math.sin(a):.1f}" r="6" fill="#0B1222" stroke="{col}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="44" fill="#0F1729" stroke="url(#g-brand)" stroke-width="1.5"/>')
    o.append("</svg>")
    return "".join(o)


def cover_orbit() -> str:
    S = 560
    c = S / 2
    o = [f'<svg width="{S}" height="{S}" viewBox="0 0 {S} {S}" aria-hidden="true">']
    o.append(f'<circle cx="{c}" cy="{c}" r="250" fill="url(#g-glow)"/>')
    for r, a in ((110, 0.16), (178, 0.12), (246, 0.08)):
        o.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{a}" stroke-width="1"/>')
    # tick marks on the outer ring
    for i in range(72):
        ang = 2 * math.pi * i / 72
        r1, r2 = 246, 246 + (7 if i % 6 == 0 else 3)
        o.append(
            f'<line x1="{c + r1 * math.cos(ang):.1f}" y1="{c + r1 * math.sin(ang):.1f}" '
            f'x2="{c + r2 * math.cos(ang):.1f}" y2="{c + r2 * math.sin(ang):.1f}" stroke="#fff" stroke-opacity="0.18" stroke-width="1"/>'
        )
    # faint "data" arc
    o.append(f'<path d="M{c + 178 * math.cos(-2.6):.1f},{c + 178 * math.sin(-2.6):.1f} A178,178 0 0 1 {c + 178 * math.cos(-0.5):.1f},{c + 178 * math.sin(-0.5):.1f}" '
             'fill="none" stroke="url(#g-brand-h)" stroke-width="2" stroke-linecap="round"/>')
    o.append(f'<circle cx="{c}" cy="{c}" r="62" fill="#0F1729" stroke="url(#g-brand)" stroke-width="1.5"/>')
    o.append(f'<text x="{c}" y="{c - 4}" text-anchor="middle" class="orb-c1">IL TUO</text>')
    o.append(f'<text x="{c}" y="{c + 16}" text-anchor="middle" class="orb-c2">capitale</text>')
    nodes = [(-150, "01", "Rendimento", "contrattuale", "#E0A43C", 178),
             (-62, "02", "Matched", "trading", "#22C2AE", 246),
             (38, "03", "Copy trading", "algoritmico", "#5B8CFF", 178),
             (128, "04", "Nuovo", "servizio", "#94A3B8", 246)]
    for deg, n, l1, l2, col, r in nodes:
        a = math.radians(deg)
        x, y = c + r * math.cos(a), c + r * math.sin(a)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{col}" fill-opacity="0.10"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="21" fill="#0B1222" stroke="{col}" stroke-width="1.6"/>')
        o.append(f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" class="orb-n">{n}</text>')
        right = math.cos(a) >= 0
        tx = x + (36 if right else -36)
        anchor = "start" if right else "end"
        o.append(f'<text x="{tx:.1f}" y="{y - 2:.1f}" text-anchor="{anchor}" class="orb-l1">{l1}</text>')
        o.append(f'<text x="{tx:.1f}" y="{y + 15:.1f}" text-anchor="{anchor}" class="orb-l2">{l2}</text>')
    # scattered particles
    import random
    rnd = random.Random(7)
    for _ in range(46):
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(70, 275)
        o.append(f'<circle cx="{c + r * math.cos(a):.1f}" cy="{c + r * math.sin(a):.1f}" r="{rnd.choice([0.8, 1, 1.3])}" fill="#fff" fill-opacity="{rnd.uniform(0.15, 0.45):.2f}"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- slides
def s_cover() -> str:
    return f'''
<section class="slide dark cover">
  <div class="cover-grid"></div>
  <div class="cover-l">
    <div class="wm">{logo(30)}<span>{BRAND}</span></div>
    <div class="eyebrow light"><i class="dot dot-grad"></i>Ecosistema di investimento · Edizione 2026</div>
    <h1 class="display">Un ecosistema,<br>quattro strade per</h1>{grad_line("far crescere il capitale.")}
    <p class="cover-sub">Rendimento contrattuale, matched trading, copy trading algoritmico e un nuovo servizio in arrivo: soluzioni diverse, unite da metodo, numeri verificabili e controllo del rischio.</p>
    <div class="cover-meta"><span>Presentazione riservata ai clienti</span><span class="sep"></span><span>Referente: {ph("nome e cognome")}</span></div>
  </div>
  <div class="cover-r">{cover_orbit()}</div>
</section>'''


def s_about() -> str:
    pill = lambda ic, t, d: (f'<div class="card pillar"><div class="ic-box">{icon(ic, BLUE)}</div>'
                             f'<h3>{t}</h3><p>{d}</p></div>')
    return f'''
<section class="slide">
  {top("Chi siamo", 2)}
  <div class="about">
    <div class="about-l">
      <h2>Facciamo lavorare il capitale con <span class="grad-text">metodo, matematica</span> e regole chiare.</h2>
      <p class="lead">{BRAND} riunisce in un unico ecosistema quattro soluzioni diverse per natura, rischio e orizzonte. Ognuna risponde a un obiettivo preciso: dalla rendita definita per contratto alla crescita dinamica guidata da un algoritmo.</p>
      <div class="pillars">
        {pill("gauge", "Metodo", "Ogni strategia segue regole stabilite in anticipo. Niente improvvisazione, niente emozioni.")}
        {pill("eye", "Trasparenza", "Condizioni scritte, report periodici e un referente sempre raggiungibile.")}
        {pill("shield", "Rischio misurato", "Limiti di perdita, scaglioni e contratti: sai sempre fin dove ci si può spingere.")}
      </div>
    </div>
    <div class="about-r card">
      <div class="stat"><div class="stat-v">4</div><div class="stat-l">soluzioni in un unico ecosistema</div></div>
      <div class="stat"><div class="stat-v">4+ <small>anni</small></div><div class="stat-l">di storico operativo sul copy trading</div></div>
      <div class="stat"><div class="stat-v ph-v">{ph("00")}</div><div class="stat-l">clienti seguiti</div></div>
      <div class="stat"><div class="stat-v ph-v">{ph("0,0 M€")}</div><div class="stat-l">capitale complessivo seguito</div></div>
    </div>
  </div>
  {foot(risk=False)}
</section>'''


def svc_card(n: str, ic: str, color: str, tint: str, name: str, tag: str, fig: str, figcap: str, prof: str, ghost: bool = False) -> str:
    cls = "card svc ghost" if ghost else "card svc"
    return f'''<div class="{cls}" style="--c:{color};--t:{tint}">
  <div class="svc-h"><div class="ic-box" style="background:{tint}">{icon(ic, color)}</div><span class="svc-n">{n}</span></div>
  <h3>{name}</h3><p class="svc-tag">{tag}</p>
  <div class="svc-fig">{fig}</div><div class="svc-cap">{figcap}</div>
  <div class="svc-prof"><i style="background:{color}"></i>{prof}</div>
</div>'''


def s_ecosystem() -> str:
    cards = "".join([
        svc_card("01", "shield", GOLD, "#FBF3E6", "Rendimento Contrattuale", "Capitale affidato con un contratto che fissa rendimento, durata e garanzie.", "20%", "rendimento annuo da contratto", "Profilo: stabilità"),
        svc_card("02", "swap", TEAL, "#E6F6F4", "Matched Trading", "Due conti con posizioni opposte: il risultato è calcolato prima di entrare.", "≈ 500 €", "medi ogni 3.000 € per ciclo", "Profilo: matematico"),
        svc_card("03", "wave", BLUE, "#EAF0FF", "Copy Trading Algoritmico", "Un algoritmo non direzionale sul Forex che punta sul ritorno alla media.", "≈ 4%", "medio mensile (dato storico)", "Profilo: dinamico"),
        svc_card("04", "plus", SLATE, "#F1F4F8", "Nuovo servizio", "Il quarto pilastro dell'ecosistema. Dettagli in arrivo.", ph("—"), "dato chiave da inserire", "Profilo: da definire", ghost=True),
    ])
    return f'''
<section class="slide">
  {top("L'ecosistema", 3)}
  <h2 class="mt">Quattro soluzioni. <span class="grad-text">Un'unica regia.</span></h2>
  <p class="lead narrow">Puoi scegliere un singolo servizio o combinarli: ognuno lavora con una logica diversa, così il capitale non dipende da un solo motore.</p>
  <div class="svc-row">{cards}</div>
  <div class="spectrum"><span>Più stabilità</span><div class="spec-line"></div><span>Più dinamismo</span></div>
  {foot()}
</section>'''


def s_compare() -> str:
    rows = [
        ("Come funziona", "Capitale affidato in gestione con contratto", "Due conti collegati, prop firm + broker, con posizioni opposte", "Copia automatica di un algoritmo sulle coppie valutarie", ph()),
        ("Rendimento indicativo", "<b>20% annuo</b>, fissato dal contratto", "<b>≈ 500 €</b> ogni 3.000 € per ciclo (media)", "<b>≈ 4% mensile</b> medio (dato storico)", ph()),
        ("Protezione", "Garanzia prevista dal contratto", "Copertura matematica tra i due conti", "Equity stop al 30%, max drawdown storico 17%", ph()),
        ("Capitale d'ingresso", ph(), "Scaglioni da 3.000 €", ph(), ph()),
        ("Orizzonte", ph("durata contratto"), ph("durata media del ciclo"), ph("orizzonte consigliato"), ph()),
    ]
    head = "".join(
        f'<th style="--c:{c}"><span class="th-n">{n}</span>{t}</th>'
        for n, t, c in (("01", "Rendimento Contrattuale", GOLD), ("02", "Matched Trading", TEAL), ("03", "Copy Trading", BLUE), ("04", "Nuovo servizio", SLATE))
    )
    body = "".join(
        "<tr><td class='rl'>" + r[0] + "</td>" + "".join(f"<td>{v}</td>" for v in r[1:]) + "</tr>" for r in rows
    )
    return f'''
<section class="slide">
  {top("Confronto rapido", 4)}
  <h2 class="mt">Tutto a colpo d'occhio.</h2>
  <div class="card tbl-wrap"><table class="cmp"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>
  {foot()}
</section>'''


def step(n: str, t: str, d: str, color: str) -> str:
    return f'<div class="vstep"><div class="vnum" style="--c:{color}">{n}</div><div><h4>{t}</h4><p>{d}</p></div></div>'


def s_svc1_a() -> str:
    return f'''
<section class="slide">
  {top("Servizio 01 · Rendimento Contrattuale", 5, GOLD)}
  <div class="split">
    <div class="split-l">
      <h2>Un rendimento del 20% annuo, <span class="gold-text">scritto nero su bianco.</span></h2>
      <p class="lead">Pensato per chi cerca stabilità e prevedibilità. Il capitale viene affidato in gestione con un contratto che stabilisce in modo chiaro rendimento, durata, tempi di pagamento e garanzie.</p>
      <div class="vsteps">
        {step("1", "Definiamo importo e durata", "Una call per capire obiettivi e orizzonte, poi la proposta su misura.", GOLD)}
        {step("2", "Firmi il contratto", "Rendimento, garanzie e condizioni di uscita sono messi per iscritto.", GOLD)}
        {step("3", "Ricevi il rendimento", "Secondo il calendario concordato, con rendiconto a ogni scadenza.", GOLD)}
      </div>
    </div>
    <div class="split-r">
      <div class="card hero-card gold">
        <div class="hero-k">RENDIMENTO ANNUO</div>
        <div class="hero-v">20<span>%</span></div>
        <div class="hero-c">definito dal contratto, con garanzia prevista dalle condizioni contrattuali</div>
      </div>
      <div class="mini-row">
        <div class="card mini"><div class="mini-k">Durata</div><div class="mini-v">{ph()}</div></div>
        <div class="card mini"><div class="mini-k">Pagamenti</div><div class="mini-v">{ph("mensili / trimestrali")}</div></div>
        <div class="card mini"><div class="mini-k">Ingresso minimo</div><div class="mini-v">{ph()}</div></div>
      </div>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc1_b() -> str:
    return f'''
<section class="slide">
  {top("Servizio 01 · Simulazione", 6, GOLD)}
  <div class="chart-split">
    <div class="card chart-card">
      <div class="chart-h">
        <div><h3>10.000 € al 20% annuo</h3><p>Valore complessivo nei primi 5 anni · euro</p></div>
        <div class="legend"><span><i style="background:{GOLD}"></i>Reinvestendo il rendimento</span><span><i style="background:{GRAY_SERIES}"></i>Incassando il rendimento</span></div>
      </div>
      {chart_growth()}
    </div>
    <div class="side">
      <h2 class="sm">Quanto può diventare il tuo capitale.</h2>
      <div class="kv"><div class="kv-v">+14.883 €</div><div class="kv-l">dopo 5 anni reinvestendo ogni anno il rendimento (interesse composto)</div></div>
      <div class="kv"><div class="kv-v">+2.000 €</div><div class="kv-l">all'anno se scegli di incassare il rendimento e lasciare investito il capitale</div></div>
      <p class="note">Simulazione illustrativa su 10.000 € al 20% annuo, al lordo di costi e imposte. Fanno fede esclusivamente le condizioni del contratto.</p>
    </div>
  </div>
  {foot()}
</section>'''


def flow_matched() -> str:
    return f'''
<div class="flow">
  <div class="fbox fcap"><div class="fk">CAPITALE</div><div class="fv">3.000 €</div><div class="fc">per ogni scaglione</div></div>
  <svg class="flines" width="130" height="250" viewBox="0 0 130 250" aria-hidden="true">
    <path d="M0,125 C65,125 55,48 130,48" fill="none" stroke="#B9C3D1" stroke-width="1.5"/>
    <path d="M0,125 C65,125 55,202 130,202" fill="none" stroke="#B9C3D1" stroke-width="1.5"/>
    <circle cx="130" cy="48" r="3.5" fill="{TEAL}"/><circle cx="130" cy="202" r="3.5" fill="{TEAL}"/>
  </svg>
  <div class="fcol">
    <div class="fbox"><div class="fk">CONTO A · PROP FIRM</div><div class="ft">Posizione su un conto finanziato</div><div class="fc">es. acquisto su una coppia valutaria</div></div>
    <div class="fbox"><div class="fk">CONTO B · BROKER</div><div class="ft">Posizione opposta di copertura</div><div class="fc">es. vendita, dimensionata con calcolo</div></div>
  </div>
  <svg class="flines" width="130" height="250" viewBox="0 0 130 250" aria-hidden="true">
    <path d="M0,48 C75,48 55,125 130,125" fill="none" stroke="#B9C3D1" stroke-width="1.5"/>
    <path d="M0,202 C75,202 55,125 130,125" fill="none" stroke="#B9C3D1" stroke-width="1.5"/>
    <circle cx="130" cy="125" r="3.5" fill="{TEAL}"/>
  </svg>
  <div class="fbox fres"><div class="fk">RISULTATO NETTO MEDIO</div><div class="fv teal-text">≈ +500 €</div><div class="fc">qualunque direzione prenda il mercato</div></div>
</div>'''


def s_svc2_a() -> str:
    return f'''
<section class="slide">
  {top("Servizio 02 · Matched Trading", 7, TEAL)}
  <h2 class="mt">Due conti, <span class="teal-text">una sola equazione.</span></h2>
  <p class="lead narrow">Il matched trading sfrutta la matematica, non le previsioni. Lavoriamo con due conti collegati e posizioni opposte, dimensionate in modo che il risultato complessivo sia calcolato prima di entrare a mercato.</p>
  {flow_matched()}
  <div class="scen-row">
    <div class="card scen"><span class="scen-k">SCENARIO A</span><p><b>Il conto prop raggiunge l'obiettivo.</b> I pagamenti della prop firm superano la perdita sul conto di copertura.</p></div>
    <div class="card scen"><span class="scen-k">SCENARIO B</span><p><b>Il conto prop non raggiunge l'obiettivo.</b> Il guadagno sul conto broker copre il costo della prop e genera il margine.</p></div>
    <div class="card scen def"><span class="scen-k">COS'È UNA PROP FIRM</span><p>Una società che mette il proprio capitale a disposizione dei trader che superano una prova di valutazione.</p></div>
  </div>
  {foot()}
</section>'''


def s_svc2_b() -> str:
    return f'''
<section class="slide">
  {top("Servizio 02 · I numeri", 8, TEAL)}
  <div class="chart-split">
    <div class="card chart-card">
      <div class="chart-h"><div><h3>Si cresce per scaglioni</h3><p>Risultato medio per ciclo in base al capitale impiegato · euro</p></div></div>
      {chart_tranches()}
    </div>
    <div class="side">
      <div class="kv"><div class="kv-v teal-text">≈ 16,7%</div><div class="kv-l">risultato medio per ciclo sul capitale impiegato (500 € su 3.000 €)</div></div>
      <div class="kv"><div class="kv-v">3.000 €</div><div class="kv-l">taglio di ogni scaglione: si aggiungono scaglioni per scalare</div></div>
      <div class="kv"><div class="kv-v ph-v">{ph("00 giorni")}</div><div class="kv-l">durata media di un ciclo</div></div>
      <div class="card warn"><b>Da sapere.</b> Il risultato è una media, non è garantito: dipende dalle regole delle prop firm (che possono cambiarle o negare un pagamento), dai costi di esecuzione e dalla corretta gestione dei due conti.</div>
    </div>
  </div>
  {foot()}
</section>'''


def feat(ic: str, t: str, d: str) -> str:
    return f'<div class="feat"><div class="ic-box" style="background:#EAF0FF">{icon(ic, BLUE)}</div><div><h4>{t}</h4><p>{d}</p></div></div>'


def s_svc3_a() -> str:
    return f'''
<section class="slide">
  {top("Servizio 03 · Copy Trading Algoritmico", 9, BLUE)}
  <div class="s3">
    <div class="s3-l">
      <h2 class="md">Quando il prezzo si allontana dalla media, <span class="blue-text">l'algoritmo punta sul ritorno.</span></h2>
      <p class="lead">Una strategia non direzionale sulle principali coppie valutarie del Forex. Non deve indovinare se il mercato salirà o scenderà: misura quanto il prezzo si è allontanato dalla sua media storica e apre un'operazione scommettendo sul rientro.</p>
      <div class="feats">
        {feat("arrows", "Non direzionale", "Lavora sia al rialzo sia al ribasso: conta la distanza dalla media.")}
        {feat("cpu", "100% algoritmico", "Regole fisse, eseguite in automatico, senza emozioni.")}
        {feat("globe", "Forex", "Il mercato più liquido al mondo, aperto 24 ore su 5 giorni.")}
      </div>
    </div>
    <div class="card s3-chart">
      <div class="legend sm"><span><i style="background:{BLUE}"></i>Prezzo</span><span><i style="background:#7C8494"></i>Media storica</span><span><i class="sq" style="background:#DCE6FF"></i>Fascia normale</span><span><i class="dotk" style="background:#0B1220"></i>Apertura</span><span><i class="dotk" style="background:{TEAL}"></i>Chiusura</span></div>
      {chart_mean_reversion()}
    </div>
  </div>
  {foot()}
</section>'''


def s_svc3_b() -> str:
    tile = lambda v, l, extra="": f'<div class="card tile">{extra}<div class="tile-v">{v}</div><div class="tile-l">{l}</div></div>'
    return f'''
<section class="slide">
  {top("Servizio 03 · Numeri e gestione del rischio", 10, BLUE)}
  <h2 class="mt">Numeri solidi, <span class="blue-text">rischio con un limite preciso.</span></h2>
  <div class="tiles">
    {tile('≈ 4<span>%</span>', "rendimento medio mensile, dato storico")}
    {tile('17<span>%</span>', "drawdown massimo registrato negli ultimi ~4 anni")}
    {tile('30<span>%</span>', "equity stop: soglia di interruzione automatica")}
    {tile(ph("dal 20XX"), "operativo con continuità da anni")}
  </div>
  <div class="card ruler-card">
    <div class="ruler-h"><h3>Fin dove può scendere il conto</h3><p>Perdita rispetto al capitale investito</p></div>
    {risk_ruler()}
    <div class="ruler-legend"><span><i style="background:{BLUE}"></i>Discesa massima registrata nello storico</span><span><i style="background:#A9C0FF"></i>Margine fino all'equity stop</span><span><i style="background:#E3E8EF"></i>Zona esclusa: la copia si ferma prima</span></div>
  </div>
  <div class="defs">
    <p><b>Drawdown</b> · la discesa massima del conto dal suo punto più alto prima di risalire.</p>
    <p><b>Equity stop</b> · il limite che chiude le operazioni se il conto perde il 30%. In condizioni estreme di mercato la perdita effettiva può superare la soglia.</p>
  </div>
  {foot()}
</section>'''


def s_svc3_track() -> str:
    months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic", "Anno"]
    head = "<div class='hm-c hm-h'></div>" + "".join(f"<div class='hm-c hm-h'>{m}</div>" for m in months)
    rows = "".join(
        f"<div class='hm-c hm-y'>20XX</div>" + "".join("<div class='hm-c hm-e'>—</div>" for _ in months)
        for _ in range(4)
    )
    return f'''
<section class="slide">
  {top("Servizio 03 · Lo storico", 11, BLUE)}
  <h2 class="mt">Anni di risultati, <span class="blue-text">mese per mese.</span></h2>
  <p class="lead narrow">In questa pagina inseriremo il track record reale del servizio: la curva del conto e il rendimento di ogni singolo mese, così puoi verificare i numeri con i tuoi occhi.</p>
  <div class="track">
    <div class="card track-eq">
      <div class="chart-h"><div><h3>Curva del conto</h3><p>Andamento del capitale dall'avvio · %</p></div></div>
      <div class="eq-ghost"><svg width="100%" height="100%" viewBox="0 0 400 220" preserveAspectRatio="none" aria-hidden="true">
        <line x1="0" y1="55" x2="400" y2="55" class="gl"/><line x1="0" y1="110" x2="400" y2="110" class="gl"/><line x1="0" y1="165" x2="400" y2="165" class="gl"/><line x1="0" y1="219" x2="400" y2="219" class="bl"/>
      </svg><div class="eq-lab">{ph("dati reali in arrivo")}</div></div>
    </div>
    <div class="card track-hm">
      <div class="chart-h"><div><h3>Rendimenti mensili</h3><p>Rendimento netto di ogni mese e totale annuo · %</p></div></div>
      <div class="hm">{head}{rows}</div>
      <p class="hm-src">Fonte dei dati: {ph("piattaforma / broker")} · Storico verificabile su richiesta.</p>
    </div>
  </div>
  {foot()}
</section>'''


def s_svc4() -> str:
    return f'''
<section class="slide">
  {top("Servizio 04 · In arrivo", 12, SLATE)}
  <div class="split">
    <div class="split-l">
      <h2>{ph("Nome del quarto servizio")}</h2>
      <p class="lead">Spazio riservato al quarto pilastro dell'ecosistema. Qui descriveremo in due righe che cosa fa, per chi è pensato e perché completa gli altri tre servizi.</p>
      <div class="vsteps">
        {step("1", "Come funziona", ph("descrizione del meccanismo"), SLATE)}
        {step("2", "Cosa ti aspetti", ph("rendimento indicativo e orizzonte"), SLATE)}
        {step("3", "Come è protetto", ph("limiti di rischio e garanzie"), SLATE)}
      </div>
    </div>
    <div class="split-r">
      <div class="card hero-card ghost-card">
        <div class="hero-k">DATO CHIAVE</div>
        <div class="hero-v slate">—</div>
        <div class="hero-c">il numero che racconta il servizio</div>
      </div>
      <div class="card ghost-chart"><div>{icon("grid", "#98A2B3", 26)}<span>Qui andrà il grafico del servizio</span></div></div>
    </div>
  </div>
  {foot()}
</section>'''


def s_start() -> str:
    steps = [
        ("01", "Call conoscitiva", "30 minuti per capire obiettivi, orizzonte e tolleranza al rischio."),
        ("02", "Proposta su misura", "Ti indichiamo il servizio, o la combinazione, più adatta al tuo profilo."),
        ("03", "Attivazione", "Firma dei documenti, apertura o collegamento dei conti, avvio operativo."),
        ("04", "Monitoraggio", "Report periodici, accesso ai risultati e un referente dedicato."),
    ]
    cells = "".join(
        f'<div class="hstep"><div class="hnum">{n}</div><div class="hdot"></div><h4>{t}</h4><p>{d}</p></div>'
        for n, t, d in steps
    )
    return f'''
<section class="slide">
  {top("Come iniziare", 13)}
  <h2 class="mt">Dal primo contatto all'operatività <span class="grad-text">in quattro passi.</span></h2>
  <p class="lead narrow">Un percorso semplice e accompagnato: in ogni fase sai cosa succede, chi se ne occupa e quali sono i numeri.</p>
  <div class="hsteps"><div class="hline"></div>{cells}</div>
  <div class="card mix"><div class="ic-box">{icon("grid", BLUE, 24)}</div><p>Puoi attivare un solo servizio o combinarne più di uno. <span>Costruiamo insieme il mix più adatto ai tuoi obiettivi e al tuo orizzonte.</span></p></div>
  {foot(risk=False)}
</section>'''


def s_legal() -> str:
    items = [
        ("Rischio di perdita del capitale", "Ogni investimento comporta rischi: il valore del capitale può diminuire e si può perdere, in tutto o in parte, quanto investito."),
        ("Risultati passati", "Rendimenti storici e medie indicate non sono una garanzia né un'indicazione affidabile dei risultati futuri."),
        ("Forex e leva finanziaria", "Il trading su valute e CFD con leva comporta un rischio elevato e può amplificare sia i guadagni sia le perdite."),
        ("Simulazioni ed esempi", "Grafici ed esempi numerici sono illustrativi, calcolati al lordo di costi, commissioni e imposte."),
        ("Contratti e garanzie", "Rendimenti, garanzie e condizioni di ogni servizio sono regolati esclusivamente dal relativo contratto, che prevale su questo documento."),
        ("Soggetti terzi", "Prop firm e broker sono soggetti terzi: regole, costi e condizioni possono cambiare e influire sui risultati."),
    ]
    cells = "".join(f'<div class="li"><span class="li-n">{i + 1:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>' for i, (t, d) in enumerate(items))
    return f'''
<section class="slide">
  {top("Avvertenze importanti", 14)}
  <h2 class="mt">La trasparenza fa parte del metodo.</h2>
  <p class="lead narrow">Prima di scegliere è giusto conoscere i rischi. Ecco, in parole semplici, cosa tenere presente.</p>
  <div class="card legal">{cells}</div>
  <p class="legal-foot">Questo documento ha finalità esclusivamente informative e non costituisce offerta al pubblico, sollecitazione all'investimento né consulenza finanziaria personalizzata. Valuta con attenzione la tua situazione e, se necessario, rivolgiti a un consulente indipendente.</p>
  {foot(risk=False)}
</section>'''


def s_close() -> str:
    c = lambda k, v: f'<div class="ct"><div class="ct-k">{k}</div><div class="ct-v">{v}</div></div>'
    return f'''
<section class="slide dark close">
  <div class="cover-grid"></div>
  <div class="close-r">{rings()}</div>
  <div class="close-in">
    <div class="wm">{logo(30)}<span>{BRAND}</span></div>
    <h1 class="display">Il prossimo passo è</h1>{grad_line("una conversazione.")}
    <p class="cover-sub">Prenota una call conoscitiva di 30 minuti: analizziamo insieme obiettivi e orizzonte e ti mostriamo i numeri reali di ogni servizio.</p>
    <div class="cts">
      {c("Referente", ph("nome e cognome"))}
      {c("Telefono", ph("+39 000 000 0000"))}
      {c("Email", ph("nome@azienda.it"))}
      {c("Sito", ph("www.azienda.it"))}
    </div>
  </div>
  <p class="close-legal">Documento riservato, a scopo informativo. Non costituisce offerta né consulenza. Investire comporta il rischio di perdita del capitale: leggi le Avvertenze a pag. 14.</p>
</section>'''


# ---------------------------------------------------------------- page
CSS = r"""
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --ink:#0B1220; --ink2:#475467; --muted:#8B95A7; --line:#E6E9EE; --page:#F5F6F8; --card:#FFFFFF;
  --blue:#2F6BFF; --teal:#0E9F8E; --gold:#C7871F; --slate:#64748B;
}
html, body { background:#DDE1E7; }
body { font-family:'Inter', system-ui, sans-serif; color:var(--ink); -webkit-font-smoothing:antialiased;
       font-feature-settings:"cv11","ss01"; }
@media screen { body { display:flex; flex-direction:column; align-items:center; gap:28px; padding:28px 0; } }
.slide { width:1280px; height:720px; position:relative; overflow:hidden; background:var(--page);
         padding:44px 72px 0; break-after:page; page-break-after:always; isolation:isolate; }
.slide:last-child { break-after:auto; page-break-after:auto; }
.slide:not(.dark)::before { content:""; position:absolute; inset:0; z-index:-1;
  background-image:radial-gradient(circle at 1px 1px, rgba(11,18,32,.10) 1px, transparent 0);
  background-size:22px 22px;
  -webkit-mask-image:radial-gradient(ellipse 46% 60% at 100% 0%, #000 0%, transparent 70%);
          mask-image:radial-gradient(ellipse 46% 60% at 100% 0%, #000 0%, transparent 70%); }
.slide:not(.dark)::after { content:""; position:absolute; z-index:-2; width:720px; height:720px; right:-260px; top:-380px;
  background:radial-gradient(closest-side, rgba(47,107,255,.10), rgba(14,159,142,.05) 55%, transparent 100%); }

/* header / footer */
.top { display:flex; justify-content:space-between; align-items:center; height:24px; }
.eyebrow { font-family:'JetBrains Mono', monospace; font-size:11.5px; letter-spacing:.16em; text-transform:uppercase;
           color:var(--ink2); display:flex; align-items:center; gap:10px; font-weight:500; }
.eyebrow.light { color:#A7B0C0; }
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
.dot-grad { background:linear-gradient(135deg, var(--blue), var(--teal)); }
.top-r { display:flex; align-items:center; gap:22px; }
.wm-mini { display:flex; align-items:center; gap:8px; font-size:11px; letter-spacing:.18em; font-weight:600; color:var(--ink); }
.pg { font-family:'JetBrains Mono', monospace; font-size:11.5px; color:var(--ink); font-weight:500; }
.pg em { font-style:normal; color:var(--muted); }
.foot { position:absolute; left:72px; right:72px; bottom:22px; border-top:1px solid var(--line); padding-top:11px;
        display:flex; justify-content:space-between; gap:40px; font-size:10px; color:var(--muted); line-height:1.4; }
.foot span:last-child { white-space:nowrap; font-family:'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; font-size:9.5px; }

/* type */
h1.display { font-family:'Inter Display','Inter',sans-serif; font-weight:600; font-size:62px; line-height:1.03; letter-spacing:-.032em; }
h2 { font-family:'Inter Display','Inter',sans-serif; font-weight:600; font-size:44px; line-height:1.07; letter-spacing:-.028em; max-width:900px; }
h2.mt { margin-top:34px; }
h2.md { font-size:38px; }
h2.sm { font-size:30px; line-height:1.12; }
h3 { font-size:19px; font-weight:600; letter-spacing:-.012em; }
h4 { font-size:16px; font-weight:600; letter-spacing:-.01em; }
.lead { font-size:17px; line-height:1.55; color:var(--ink2); margin-top:16px; max-width:720px; }
.lead.narrow { max-width:780px; }
p { color:var(--ink2); }
.grad-text { color:var(--blue); }
.gold-text { color:#B07415; } .teal-text { color:var(--teal); } .blue-text { color:var(--blue); }

.card { background:var(--card); border:1px solid rgba(11,18,32,.06); border-radius:20px;
        box-shadow:0 1px 2px rgba(11,18,32,.04), 0 14px 34px -16px rgba(11,18,32,.12); }
.ic-box { width:44px; height:44px; border-radius:12px; display:grid; place-items:center; background:#EEF3FF; flex:none; }
.ph { display:inline-block; font-family:'JetBrains Mono', monospace; font-size:.78em; font-weight:500; letter-spacing:.02em;
      color:#7A8597; background:repeating-linear-gradient(135deg, #F3F5F8 0 6px, #EBEEF3 6px 12px);
      border:1px dashed #C3CAD5; border-radius:6px; padding:.12em .55em; line-height:1.35; vertical-align:middle; }
.dark .ph { color:#9AA6B8; background:rgba(255,255,255,.04); border-color:rgba(255,255,255,.22); }

/* cover + close */
.dark { background:#0A0F1A; color:#F2F4F7; }
.dark p { color:#A7B0C0; }
.cover-grid { position:absolute; inset:0; z-index:-1;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
  background-size:48px 48px;
  -webkit-mask-image:radial-gradient(ellipse 70% 80% at 75% 50%, #000 0%, transparent 75%);
          mask-image:radial-gradient(ellipse 70% 80% at 75% 50%, #000 0%, transparent 75%); }
.cover { display:flex; padding:56px 0 0 80px; }
.cover-l { width:640px; display:flex; flex-direction:column; padding-top:6px; position:relative; z-index:2; }
.wm { display:flex; align-items:center; gap:12px; font-size:14px; letter-spacing:.22em; font-weight:600; color:#F2F4F7; }
.cover .eyebrow { margin-top:92px; }
.cover h1 { margin-top:22px; }
.close h1 + .gline, .cover h1 + .gline { margin-top:0; }
.cover-sub { font-size:17px; line-height:1.6; margin-top:24px; max-width:540px; }
.cover-meta { margin-top:auto; margin-bottom:46px; display:flex; align-items:center; gap:16px; font-size:12.5px; color:#8A94A6; }
.cover-meta .sep { width:24px; height:1px; background:#3A4458; }
.cover-r { position:absolute; right:6px; top:80px; }
.close-r { position:absolute; right:-150px; top:40px; opacity:.9; }
.gline { display:block; overflow:visible; margin-top:2px; }
.gline-fallback { font-family:'Inter Display','Inter',sans-serif; font-weight:600; letter-spacing:-.032em; line-height:1.12; color:#6E9BFF; }
.orb-c1 { font-family:'JetBrains Mono', monospace; font-size:9.5px; letter-spacing:.2em; fill:#8A94A6; }
.orb-c2 { font-family:'Inter Display','Inter'; font-size:17px; font-weight:600; fill:#F2F4F7; }
.orb-n { font-family:'JetBrains Mono', monospace; font-size:12px; font-weight:600; fill:#F2F4F7; }
.orb-l1 { font-size:13px; font-weight:600; fill:#E6EAF0; }
.orb-l2 { font-size:12px; fill:#8A94A6; }
.close { padding:56px 80px 0; }
.close-in { display:flex; flex-direction:column; height:100%; }
.close h1 { margin-top:110px; }
.cts { display:grid; grid-template-columns:repeat(4, 1fr); gap:0; margin-top:56px; border-top:1px solid rgba(255,255,255,.1); max-width:1060px; }
.ct { padding:20px 24px 0 0; }
.ct-k { font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.16em; text-transform:uppercase; color:#8A94A6; }
.ct-v { margin-top:10px; font-size:16px; color:#F2F4F7; }
.close-legal { position:absolute; left:80px; right:80px; bottom:28px; font-size:10px; color:#6B7587 !important; }

/* about */
.about { display:flex; gap:44px; margin-top:44px; height:560px; }
.about-l { display:flex; flex-direction:column; }
.about-l { flex:1; }
.about-l h2 { font-size:42px; }
.about-l .lead { font-size:18px; }
.pillars { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:auto; margin-bottom:34px; }
.pillar { padding:26px 24px 30px; min-height:212px; }
.pillar h3 { margin-top:16px; font-size:17px; }
.pillar p { margin-top:8px; font-size:14px; line-height:1.55; }
.about-r { width:300px; flex:none; padding:14px 28px; align-self:stretch; margin-bottom:34px; display:flex; flex-direction:column; justify-content:space-around; }
.stat { padding:14px 0; border-bottom:1px solid var(--line); }
.stat:last-child { border-bottom:0; }
.stat-v { font-family:'Inter Display','Inter'; font-size:40px; font-weight:600; letter-spacing:-.03em; line-height:1; }
.stat-v small { font-size:18px; letter-spacing:-.01em; color:var(--ink2); font-weight:500; }
.stat-v.ph-v .ph { font-size:20px; }
.stat-l { font-size:13px; color:var(--ink2); margin-top:6px; }

/* ecosystem */
.svc-row { display:grid; grid-template-columns:repeat(4,1fr); gap:18px; margin-top:30px; }
.svc { padding:22px 22px 20px; position:relative; overflow:hidden; display:flex; flex-direction:column; height:350px; }
.svc::before { content:""; position:absolute; left:0; right:0; top:0; height:3px; background:var(--c); }
.svc.ghost { background:rgba(255,255,255,.55); border:1px dashed #C3CAD5; box-shadow:none; }
.svc.ghost::before { display:none; }
.svc-h { display:flex; justify-content:space-between; align-items:center; }
.svc-n { font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--muted); font-weight:500; }
.svc h3 { margin-top:18px; font-size:18px; }
.svc-tag { font-size:13.5px; line-height:1.5; margin-top:8px; min-height:60px; }
.svc-fig { margin-top:auto; font-family:'Inter Display','Inter'; font-size:40px; font-weight:600; letter-spacing:-.03em; color:var(--ink); }
.svc-fig .ph { font-size:22px; }
.svc-cap { font-size:12.5px; color:var(--muted); margin-top:4px; }
.svc-prof { margin-top:16px; padding-top:14px; border-top:1px solid var(--line); font-size:12px; font-weight:500; color:var(--ink2); display:flex; align-items:center; gap:8px; }
.svc-prof i { width:7px; height:7px; border-radius:50%; }
.spectrum { display:flex; align-items:center; gap:14px; margin-top:20px; font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); width:calc(75% - 4px); }
.spec-line { flex:1; height:2px; border-radius:2px; background:linear-gradient(90deg, var(--gold), var(--teal), var(--blue)); position:relative; opacity:.75; }
.spec-line::after { content:""; position:absolute; right:-2px; top:-4px; border-left:7px solid var(--blue); border-top:5px solid transparent; border-bottom:5px solid transparent; }

/* table */
.tbl-wrap { margin-top:28px; padding:8px 28px 6px; }
.cmp { width:100%; border-collapse:collapse; table-layout:fixed; }
.cmp th { text-align:left; font-size:14.5px; font-weight:600; padding:18px 16px 16px; vertical-align:bottom; position:relative; letter-spacing:-.01em; }
.cmp th:first-child { width:170px; }
.cmp th::after { content:""; position:absolute; left:16px; right:16px; bottom:0; height:2px; background:var(--c); border-radius:2px; }
.cmp th:first-child::after { display:none; }
.th-n { display:block; font-family:'JetBrains Mono', monospace; font-size:11px; color:var(--muted); font-weight:500; margin-bottom:6px; }
.cmp td { padding:15px 16px; font-size:13.5px; line-height:1.45; color:var(--ink2); border-bottom:1px solid var(--line); vertical-align:top; }
.cmp tr:last-child td { border-bottom:0; }
.cmp td b { color:var(--ink); font-weight:600; }
.cmp td.rl { font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); padding-top:17px; }
.cmp td .ph { font-size:11px; }

/* split layouts */
.split { display:flex; gap:56px; margin-top:38px; height:540px; }
.split-l { flex:1; display:flex; flex-direction:column; }
.split-r { width:430px; flex:none; display:flex; flex-direction:column; gap:16px; padding-bottom:40px; }
.split-r .hero-card { flex:1; display:flex; flex-direction:column; justify-content:center; }
.vsteps { margin-top:auto; margin-bottom:40px; display:flex; flex-direction:column; gap:22px; position:relative; }
.vstep { display:flex; gap:18px; align-items:flex-start; }
.vnum { width:38px; height:38px; border-radius:50%; flex:none; display:grid; place-items:center; font-family:'JetBrains Mono', monospace;
        font-size:13px; font-weight:600; color:var(--c); background:#fff; border:1.5px solid var(--c); box-shadow:0 0 0 5px color-mix(in srgb, var(--c) 10%, transparent); }
.vstep h4 { margin-top:3px; font-size:17px; }
.vstep p { font-size:14.5px; margin-top:4px; line-height:1.45; }
.hero-card { padding:30px 32px; position:relative; overflow:hidden; }
.hero-card.gold { background:linear-gradient(160deg, #FFFFFF 0%, #FFF8EC 100%); }
.hero-card.gold::after { content:""; position:absolute; right:-80px; top:-80px; width:240px; height:240px; border-radius:50%;
        border:1px solid rgba(199,135,31,.25); box-shadow:0 0 0 30px rgba(199,135,31,.04), 0 0 0 60px rgba(199,135,31,.03); }
.hero-k { font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:.16em; color:var(--muted); }
.hero-v { font-family:'Inter Display','Inter'; font-size:132px; font-weight:600; letter-spacing:-.05em; line-height:1; margin-top:14px; color:#B07415; }
.hero-v span { font-size:64px; letter-spacing:-.02em; margin-left:4px; }
.hero-v.slate { color:#B5BDC9; }
.hero-c { font-size:14px; color:var(--ink2); margin-top:12px; line-height:1.45; max-width:330px; }
.mini-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
.mini { padding:16px 16px 18px; }
.mini-k { font-size:11.5px; color:var(--muted); }
.mini-v { margin-top:8px; font-size:14px; font-weight:600; }
.mini-v .ph { font-size:10.5px; }
.ghost-card { background:rgba(255,255,255,.55); border:1px dashed #C3CAD5; box-shadow:none; }
.ghost-chart { height:170px; background:rgba(255,255,255,.55); border:1px dashed #C3CAD5; box-shadow:none; display:grid; place-items:center; }
.ghost-chart div { display:flex; align-items:center; gap:12px; color:var(--muted); font-size:13.5px; }

/* charts */
.chart-split { display:flex; gap:40px; margin-top:38px; align-items:stretch; height:540px; padding-bottom:40px; }
.chart-card { display:flex; flex-direction:column; justify-content:space-between; }
.chart-card { padding:24px 26px 18px; flex:none; }
.chart-h { display:flex; justify-content:space-between; align-items:flex-start; gap:20px; margin-bottom:16px; }
.chart-h h3 { font-size:18px; }
.chart-h p { font-size:12.5px; color:var(--muted); margin-top:4px; }
.legend { display:flex; gap:16px; flex-wrap:wrap; font-size:12px; color:var(--ink2); }
.legend span { display:flex; align-items:center; gap:7px; white-space:nowrap; }
.legend i { width:14px; height:3px; border-radius:2px; display:inline-block; }
.legend i.sq { width:12px; height:12px; border-radius:3px; }
.legend i.dotk { width:9px; height:9px; border-radius:50%; }
.legend.sm { font-size:11.5px; gap:14px; margin-bottom:6px; }
.chart text { font-family:'Inter', sans-serif; }
.chart .grid { stroke:#ECEEF2; stroke-width:1; }
.chart .base { stroke:#C9CFD8; stroke-width:1; }
.chart .tick { font-size:11.5px; fill:#8B95A7; font-variant-numeric:tabular-nums; }
.chart .cat { font-size:13px; fill:#0B1220; font-weight:500; font-variant-numeric:tabular-nums; }
.chart .endv { font-size:13px; fill:#0B1220; font-weight:600; }
.chart .ann { font-size:11.5px; fill:#0B1220; font-weight:500; }
.chart .ann-teal { fill:#0B6E63; }
.chart .tag { font-family:'JetBrains Mono', monospace; font-size:9.5px; letter-spacing:.12em; fill:#98A2B3; }
.side { flex:1; padding-top:4px; display:flex; flex-direction:column; }
.side .warn { margin-top:auto; }
.side h2.sm { margin-bottom:22px; }
.kv { padding:14px 0 16px; border-bottom:1px solid var(--line); }
.kv:first-of-type { padding-top:0; }
.kv-v { font-family:'Inter Display','Inter'; font-size:32px; font-weight:600; letter-spacing:-.025em; }
.kv-v.ph-v .ph { font-size:16px; }
.kv-l { font-size:13.5px; color:var(--ink2); margin-top:4px; line-height:1.45; }
.note { font-size:11.5px; color:var(--muted) !important; margin-top:16px; line-height:1.5; }
.warn { margin-top:18px; padding:14px 16px; font-size:12.5px; line-height:1.5; color:var(--ink2); background:#FBFAF6; border-color:#EFE6D2; box-shadow:none; border-radius:14px; }
.warn b { color:var(--ink); }

/* matched flow */
.flow { display:flex; align-items:center; margin-top:18px; height:250px; }
.fbox { background:#fff; border:1px solid rgba(11,18,32,.07); border-radius:16px; padding:16px 18px; box-shadow:0 1px 2px rgba(11,18,32,.04), 0 10px 26px -14px rgba(11,18,32,.12); }
.fcap, .fres { width:240px; }
.fres { border-color:rgba(14,159,142,.35); background:linear-gradient(160deg,#fff 0%,#F0FAF8 100%); }
.fcol { display:flex; flex-direction:column; justify-content:space-between; height:250px; width:396px; }
.fcol .fbox { height:96px; }
.fk { font-family:'JetBrains Mono', monospace; font-size:10.5px; letter-spacing:.14em; color:var(--muted); }
.fv { font-family:'Inter Display','Inter'; font-size:34px; font-weight:600; letter-spacing:-.025em; margin-top:6px; }
.ft { font-size:15px; font-weight:600; margin-top:6px; }
.fc { font-size:12.5px; color:var(--ink2); margin-top:3px; }
.flines { flex:none; }
.scen-row { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; margin-top:14px; }
.scen { padding:16px 18px; }
.scen-k { font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:.14em; color:var(--teal); font-weight:600; }
.scen p { font-size:13px; line-height:1.5; margin-top:6px; }
.scen p b { color:var(--ink); font-weight:600; }
.scen.def { background:#F8F9FB; box-shadow:none; }
.scen.def .scen-k { color:var(--muted); }

/* service 3 */
.s3 { display:flex; gap:36px; margin-top:30px; }
.s3-l { width:380px; flex:none; }
.s3-l .lead { font-size:15.5px; }
.feats { display:flex; flex-direction:column; gap:14px; margin-top:22px; }
.feat { display:flex; gap:14px; align-items:flex-start; }
.feat .ic-box { width:38px; height:38px; border-radius:10px; }
.feat h4 { font-size:14.5px; }
.feat p { font-size:13px; line-height:1.45; margin-top:2px; }
.s3-chart { flex:1; padding:18px 20px 12px; align-self:flex-start; margin-top:4px; }
.tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:30px; }
.tile { padding:26px 24px 28px; }
.tile-v { font-family:'Inter Display','Inter'; font-size:50px; font-weight:600; letter-spacing:-.035em; line-height:1.05; }
.tile-v span { font-size:26px; margin-left:2px; color:var(--ink2); }
.tile-v .ph { font-size:20px; }
.tile-l { font-size:13px; color:var(--ink2); margin-top:6px; line-height:1.4; }
.ruler-card { margin-top:20px; padding:24px 30px 22px; }
.ruler-h { display:flex; align-items:baseline; gap:14px; }
.ruler-h h3 { font-size:16px; }
.ruler-h p { font-size:12.5px; color:var(--muted); }
.ruler { position:relative; height:88px; margin-top:16px; }
.seg { position:absolute; top:24px; height:28px; border-radius:4px; font-size:12px; font-weight:600; display:flex; align-items:center; padding-left:10px; white-space:nowrap; overflow:visible; }
.stop { position:absolute; top:6px; height:52px; width:2px; background:#0B1220; }
.stop span { position:absolute; left:8px; top:-6px; font-family:'JetBrains Mono', monospace; font-size:10px; letter-spacing:.12em; font-weight:600; color:#0B1220; white-space:nowrap; }
.ruler-axis { position:absolute; left:0; right:0; top:60px; font-size:11px; color:var(--muted); font-variant-numeric:tabular-nums; }
.ruler-axis span { position:absolute; transform:translateX(-50%); white-space:nowrap; }
.ruler-axis span:first-child { transform:none; }
.ruler-axis span:last-child { transform:translateX(-100%); }
.ruler-legend { display:flex; gap:22px; font-size:12px; color:var(--ink2); }
.ruler-legend span { display:flex; align-items:center; gap:7px; }
.ruler-legend i { width:12px; height:12px; border-radius:3px; }
.defs { display:grid; grid-template-columns:1fr 1fr; gap:36px; margin-top:24px; }
.defs p { font-size:13.5px; line-height:1.55; }
.defs b { color:var(--ink); font-weight:600; }


/* track record */
.track { display:grid; grid-template-columns:400px 1fr; gap:18px; margin-top:28px; height:372px; }
.track .card { padding:22px 24px 20px; display:flex; flex-direction:column; }
.eq-ghost { position:relative; flex:1; margin-top:4px; }
.eq-ghost svg { position:absolute; inset:0; }
.eq-ghost .gl { stroke:#ECEEF2; stroke-width:1; vector-effect:non-scaling-stroke; }
.eq-ghost .bl { stroke:#C9CFD8; stroke-width:1; vector-effect:non-scaling-stroke; }
.eq-lab { position:absolute; inset:0; display:grid; place-items:center; }
.eq-ghost .ph { font-size:12px; }
.hm { display:grid; grid-template-columns:48px repeat(13, 1fr); gap:4px; margin-top:6px; }
.hm-c { height:44px; border-radius:6px; display:grid; place-items:center; font-size:11.5px; font-variant-numeric:tabular-nums; }
.hm-h { height:22px; color:var(--muted); font-size:11px; }
.hm-y { color:var(--ink2); font-weight:500; font-size:12px; justify-content:start; }
.hm-e { background:#F4F6F9; border:1px dashed #D5DBE4; color:#B5BDC9; }
.hm-c.hm-e:nth-child(14n) { background:#EEF3FF; border-color:#C9D7FF; }
.hm-src { font-size:12px; color:var(--muted) !important; margin-top:auto; }
.hm-src .ph { font-size:10.5px; }

/* start */
.hsteps { position:relative; display:grid; grid-template-columns:repeat(4,1fr); gap:28px; margin-top:58px; }
.hline { position:absolute; left:0; right:0; top:58px; height:2px; background:linear-gradient(90deg, var(--blue), var(--teal)); opacity:.35; border-radius:2px; }
.hnum { font-family:'Inter Display','Inter'; font-size:44px; font-weight:600; letter-spacing:-.03em; color:#C9D2E0; line-height:1; }
.hdot { width:14px; height:14px; border-radius:50%; background:#fff; border:3px solid var(--blue); margin-top:12px; position:relative; z-index:1; box-shadow:0 0 0 6px rgba(47,107,255,.10); }
.hstep:nth-child(3) .hdot { border-color:#1F86C8; } .hstep:nth-child(4) .hdot { border-color:#15959F; } .hstep:nth-child(5) .hdot { border-color:var(--teal); box-shadow:0 0 0 6px rgba(14,159,142,.12); }
.hstep h4 { margin-top:26px; font-size:18px; }
.hstep p { font-size:14.5px; line-height:1.55; margin-top:8px; max-width:250px; }
.mix { margin-top:46px; padding:22px 28px; display:flex; align-items:center; gap:20px; }
.mix p { font-size:15px; color:var(--ink); }
.mix p span { color:var(--ink2); }
.mix .ic-box { width:46px; height:46px; }

/* legal */
.legal { margin-top:26px; padding:10px 30px; display:grid; grid-template-columns:1fr 1fr; column-gap:48px; }
.li { display:flex; gap:16px; padding:19px 0; border-bottom:1px solid var(--line); }
.li:nth-last-child(-n+2) { border-bottom:0; }
.li-n { font-family:'JetBrains Mono', monospace; font-size:11px; color:var(--muted); padding-top:3px; }
.li h4 { font-size:14.5px; }
.li p { font-size:12.8px; line-height:1.5; margin-top:3px; }
.legal-foot { margin-top:18px; font-size:12px; line-height:1.55; color:var(--muted) !important; max-width:1050px; }
"""

DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="g-brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2F6BFF"/><stop offset="1" stop-color="#0E9F8E"/></linearGradient>
<linearGradient id="g-brand-h" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5B8CFF" stop-opacity="0"/><stop offset=".5" stop-color="#5B8CFF"/><stop offset="1" stop-color="#22C2AE"/></linearGradient>
<linearGradient id="g-title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6E9BFF"/><stop offset="1" stop-color="#2CD3BC"/></linearGradient>
<radialGradient id="g-glow"><stop offset="0" stop-color="#2F6BFF" stop-opacity=".28"/><stop offset=".55" stop-color="#0E9F8E" stop-opacity=".07"/><stop offset="1" stop-color="#0A0F1A" stop-opacity="0"/></radialGradient>
</defs></svg>"""


def build() -> None:
    slides = [s_cover(), s_about(), s_ecosystem(), s_compare(), s_svc1_a(), s_svc1_b(), s_svc2_a(), s_svc2_b(),
              s_svc3_a(), s_svc3_b(), s_svc3_track(), s_svc4(), s_start(), s_legal(), s_close()]
    assert len(slides) == TOTAL, len(slides)
    html = (
        '<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">'
        f'<title>{BRAND} · Ecosistema di investimento</title><style>{CSS}</style></head>'
        f'<body>{DEFS}{"".join(slides)}</body></html>'
    )
    OUT.write_text(html, encoding="utf-8")
    print(f"scritto {OUT} ({len(html) // 1024} KB, {len(slides)} pagine)")


if __name__ == "__main__":
    build()
