"""Lettura del testo visibile con lexbor (selectolax) (R-ve246-5, fette 19-20 chat Mani).

leggi.py imita a mano le regole del browser per sapere quale testo si vede, e ogni giro di
verifiche ne trova un caso nuovo (canvas/object: R-ve246-5). lexbor costruisce l'albero come
il browser, con gli script attivi come nel modello di Gas, ed è già l'oracolo con cui Gas si
controlla. Qui si legge il testo da quell'albero, con gli stessi contenitori nascosti di
leggi.py, più quello che il browser nasconde sempre e leggi.py non vede (attributo «hidden»,
anche su html e body, dialog chiuso, details chiuso tranne il summary, datalist, rp; del
select solo l'opzione scelta, o tutte con multiple/size). È SPENTO per default: si accende con GAS_WEB_LEXBOR=1,
per decisione dell'operatore (fetta 20: pronto per l'accensione). Solo su Linux: il tetto di
memoria del figlio (RLIMIT_AS) altrove non vale, e lì la lettura resta quella di sempre.

lexbor gira in un processo figlio, con un tempo massimo e un tetto di memoria: su alcune
pagine costa il quadrato (decine di migliaia di «<div>» annidati, migliaia di attributi in un
tag: 6-8 s per 50 mila, misurato in prova) e una chiamata in C non si interrompe; un errore
nel codice C ucciderebbe il processo. Così muore il figlio, non Gas. Senza selectolax, oltre
il tempo o se qualcosa va storto, testo_visibile restituisce None e leggi.py usa la sua
lettura di sempre (FAIL-SAFE §9).
"""
from __future__ import annotations

import importlib.util
import json
import logging
import os
import subprocess
import sys
import threading
import time
from typing import Optional

logger = logging.getLogger("gas.web")

TEMPO_MAX = 4.0              # secondi per pagina nel processo figlio
MEMORIA_MAX = 1 << 30        # byte di memoria virtuale del figlio

_DISPONIBILE = importlib.util.find_spec("selectolax") is not None
RIPROVA_SONDA = 600.0       # secondi prima di riprovare una sonda fallita
MAX_SONDE = 3               # sonde fallite dopo le quali la lettura con lexbor si spegne

_FIGLIO_OK: Optional[bool] = None  # esito della sonda del figlio (R-520-3)
_RIPROVA_DOPO = 0.0                # time.monotonic() prima del quale non si risonda (R-521-2)
_SONDE_FALLITE = 0
_SONDA = threading.Lock()          # una sonda alla volta (R-521-1)

# Codice del figlio: legge la pagina da stdin, scrive {"testo", "titolo"} su stdout. Il titolo
# è quello della scheda come nel browser, il primo «title» HTML del documento (non di svg o
# math); il body si visita senza ricorsione (una pagina annidata a fondo non esaurisce la pila)
# saltando i contenitori nascosti e il titolo, con un a capo per i blocchi come in leggi.py.
# Si salta anche quello che il browser non mostra mai: l'attributo «hidden» (anche su html e
# body: allora niente testo), i dialog chiusi, i details chiusi tranne il primo summary,
# datalist, rp, il contenuto di riserva di video e audio, l'interno di meter e progress. Del
# select (lexbor segue il select nuovo, che accetta altri tag dentro) si legge solo quello
# che il browser mostra: l'opzione scelta (l'ultima con «selected», se no la prima), o tutte
# le opzioni con «multiple» o «size» > 1 (V-1 bot / V-4 ve #277).
# Shadow DOM dichiarativo (decisione dell'operatore 2026-10-28, scelta 3): un host con
# `<template shadowrootmode>` si legge come lo disegna il browser, cioè lo shadow, con al
# posto di ogni slot i figli dell'host assegnati a quello slot; i figli non assegnati non si
# vedono. La lettura di sempre di leggi.py resta com'è.
# Fuori da Linux il figlio si rifiuta (uscita 3).
_FIGLIO = r"""
import json, resource, sys
if sys.platform != "linux":
    sys.stderr.write("solo Linux: il tetto di memoria (RLIMIT_AS) qui non vale\n")
    sys.exit(3)
resource.setrlimit(resource.RLIMIT_AS, (int(sys.argv[1]), int(sys.argv[1])))
from selectolax.lexbor import LexborHTMLParser
# In più di quelli di leggi.py, quello che il browser non disegna mai: il contenuto di
# riserva di video e audio, l'interno di meter e progress (R-ve277-5).
nascosti = frozenset(json.loads(sys.argv[2])) | {"title", "datalist", "rp", "video", "audio", "meter", "progress"}
blocchi = frozenset(json.loads(sys.argv[3]))
albero = LexborHTMLParser(sys.stdin.buffer.read().decode("utf-8"), scripting=True)
titolo = ""
for nodo in albero.css("title"):
    sopra = nodo.parent
    while sopra is not None and sopra.tag not in ("svg", "math"):
        sopra = sopra.parent
    if sopra is None:
        titolo = nodo.text(deep=True)
        break
def nascosto(nodo):
    attributi = nodo.attrs
    return "hidden" in attributi or (nodo.tag == "dialog" and "open" not in attributi)

def opzioni_visibili(select):
    # Le opzioni del select scendendo dall'alto, una volta sola (lineare, R-527-2): si salta
    # ogni sotto-albero nascosto e non si scende dentro le opzioni né dentro altri select.
    trovate = []
    pila = [select.iter(include_text=False)]
    while pila:
        nodo = next(pila[-1], None)
        if nodo is None:
            pila.pop()
        elif not nodo.is_element_node:
            continue  # commenti: iter(include_text=False) li restituisce lo stesso
        elif nodo.tag == "option":
            trovate.append(nodo)
        elif nodo.tag not in nascosti and nodo.tag != "select" and not nascosto(nodo):
            pila.append(nodo.iter(include_text=False))
    return trovate

def intero(valore):
    # Come il browser legge gli interi non negativi: spazi, un segno + o - facoltativo, poi le
    # cifre ASCII in testa; oltre 2**31-1 il valore non vale (V-1 ve #277 ter: con migliaia di
    # cifre int() cadeva; V-2 ve #285).
    testo = (valore or "").lstrip(" \t\n\f\r")
    meno = testo.startswith("-")
    cifre, letto = "", False
    for c in testo[1:] if testo.startswith(("+", "-")) else testo:
        if c not in "0123456789" or len(cifre) > 10:
            break
        letto = True
        if cifre or c != "0":  # gli zeri in testa non contano
            cifre += c
    # «0», «000» e «-0» valgono 0, non «senza valore»; un negativo non vale (R-bot280-1, R-536-1)
    numero = int(cifre or "0")
    return numero if letto and numero < 1 << 31 and not (meno and numero) else None

def opzioni(select, giro=None):
    attributi = select.attrs
    tutte = opzioni_visibili(select)
    if "multiple" in attributi or (intero(attributi.get("size")) or 1) > 1:
        # Lista aperta: si vedono tutte le opzioni, tranne quelle con «hidden».
        tutte = [o for o in tutte if not nascosto(o)]
    else:
        # Tendina chiusa: si vede l'opzione scelta, l'ultima con «selected» (anche se ha
        # «hidden», come il segnaposto «Scegli»), se no la prima non disabilitata, anche se
        # ha «hidden»: è la selezione automatica dello standard (R-527-3, R-528-2).
        scelte = [o for o in tutte if "selected" in o.attrs]
        libere = [o for o in tutte if "disabled" not in o.attrs]
        tutte = scelte[-1:] or libere[:1]
    # Il testo dell'opzione passa dalla stessa visita del body: nel select nuovo un'opzione
    # può contenere altri tag, anche script o elementi nascosti (V-1 ve #277 bis).
    return [o.attrs.get("label") or visita(o, True, giro) for o in tutte]

def primo_summary(details):
    for figlio in details.iter(include_text=False):
        if figlio.tag == "summary":
            yield figlio
            return

# Gli elementi che possono avere uno shadow, oltre ai nomi con il trattino (custom element),
# tranne quelli riservati di svg e math (R-539-2).
HOST = frozenset({"article", "aside", "blockquote", "body", "div", "footer", "h1", "h2", "h3",
                  "h4", "h5", "h6", "header", "main", "nav", "p", "section", "span"})
RISERVATI = frozenset({"annotation-xml", "color-profile", "font-face", "font-face-src",
                       "font-face-uri", "font-face-format", "font-face-name", "missing-glyph"})

def primi_slot(frammento):
    # Ogni nome va al primo slot che lo porta, nell'ordine dello shadow, anche se quello slot
    # è nascosto; non contano gli slot dentro svg e math (non sono slot HTML, R-539-2). iter()
    # non entra nel contenuto dei template: gli shadow annidati hanno i loro. Discesa lineare.
    primi = {}
    pila = [frammento.iter(include_text=False)]
    while pila:
        nodo = next(pila[-1], None)
        if nodo is None:
            pila.pop()
        elif nodo.is_element_node and nodo.tag not in ("svg", "math"):
            if nodo.tag == "slot":
                primi.setdefault(nodo.attrs.get("name") or "", nodo.mem_id)
            pila.append(nodo.iter(include_text=False))
    return primi

# Senza template shadowrootmode fuori dai template non ce ne sono nemmeno dentro: le pagine
# normali non pagano la ricerca degli shadow tra i figli.
CON_SHADOW = albero.css_first("template[shadowrootmode]") is not None

def shadow(nodo):
    # (frammento, slot) dello shadow dichiarativo dell'host, o None. Vale il primo template
    # figlio con shadowrootmode open o closed, come nel parser del browser; gli altri restano
    # template normali, cioè nascosti.
    tag = nodo.tag
    if not CON_SHADOW or tag in RISERVATI or tag not in HOST and not ("-" in tag and "a" <= tag[:1] <= "z"):
        return None
    for figlio in nodo.iter(include_text=False):
        modo = figlio.attrs.get("shadowrootmode") if figlio.tag == "template" else None
        if modo is not None and modo.lower() in ("open", "closed"):
            frammenti = figlio.template_fragments()
            if not frammenti:
                continue  # template di svg o math: nessun contenuto HTML (R-539-1)
            frammento = frammenti[0]
            primi = primi_slot(frammento)
            # I figli dell'host vanno allo slot col loro nome (attributo «slot»); il testo
            # solo allo slot senza nome. Il template dello shadow non è un figlio.
            assegnati = {}
            for luce in nodo.iter(include_text=True):
                if luce.is_text_node:
                    assegnati.setdefault("", []).append(luce)
                elif luce.is_element_node and luce.mem_id != figlio.mem_id:
                    assegnati.setdefault(luce.attrs.get("slot") or "", []).append(luce)
            return frammento, (primi, assegnati)
    return None

# Testo visibile sotto radice, senza ricorsione sulla profondità della pagina. Dentro
# un'opzione un select non si legge: lexbor non annida mai i select, è solo una difesa
# contro catene di ricorsione (R-527-4). Ogni livello della pila porta gli slot dello
# shadow in cui si trova (None fuori dagli shadow) e quelli del livello fuori dall'host.
def visita(radice, dentro_opzione=False, giro=None):
    pezzi = []
    pila = []
    def scendi(nodo, giro):
        trovato = shadow(nodo)
        if trovato is None:
            pila.append((nodo.tag, nodo.iter(include_text=True), giro))
        else:
            pila.append((nodo.tag, trovato[0].iter(include_text=True), (trovato[1], giro)))
    scendi(radice, giro)
    while pila:
        tag, figli, giro = pila[-1]
        nodo = next(figli, None)
        if nodo is None:
            pila.pop()
            if tag in blocchi:
                pezzi.append("\n")
            continue
        if nodo.is_text_node:
            pezzi.append(nodo.text_content or "")
        elif nodo.is_element_node and nodo.tag not in nascosti and not nascosto(nodo):
            if nodo.tag == "select":
                if not dentro_opzione:
                    pezzi.append("\n" + "\n".join(opzioni(nodo, giro)) + "\n")
                continue
            if nodo.tag in blocchi:
                pezzi.append("\n")
            if nodo.tag == "details" and "open" not in nodo.attrs:
                pila.append((nodo.tag, primo_summary(nodo), giro))
            elif nodo.tag == "slot" and giro is not None:
                # Slot dello shadow: i figli dell'host assegnati, che si leggono col livello
                # fuori dall'host; senza assegnati, il suo contenuto di riserva.
                (primi, assegnati), fuori = giro
                nome = nodo.attrs.get("name") or ""
                if primi.get(nome) == nodo.mem_id and assegnati.get(nome):
                    pila.append((nodo.tag, iter(assegnati[nome]), fuori))
                else:
                    pila.append((nodo.tag, nodo.iter(include_text=True), giro))
            else:
                scendi(nodo, giro)
    return "".join(pezzi)

corpo = albero.body
radice = corpo.parent if corpo is not None else None
nascosta = corpo is None or nascosto(corpo) or (radice is not None and nascosto(radice))
pezzi = [] if nascosta else [visita(corpo)]
sys.stdout.write(json.dumps({"testo": "".join(pezzi), "titolo": titolo}))
"""


def attivo() -> bool:
    """La lettura con lexbor è accesa (GAS_WEB_LEXBOR=1), la libreria c'è e il figlio la trova:
    con «-I» e l'ambiente vuoto il figlio non vede PYTHONPATH, quindi la libreria trovata qui
    può mancargli; lo dice una sonda (R-520-3). Una sonda alla volta: chi arriva mentre gira
    usa la lettura di sempre (R-521-1). Una sonda fallita (oltre il tempo all'avvio a freddo,
    un fork negato con poca memoria…) si riprova dopo RIPROVA_SONDA secondi; dopo MAX_SONDE
    sonde fallite la lettura con lexbor si spegne (R-521-2, V-3 bot e ve #277)."""
    global _FIGLIO_OK, _RIPROVA_DOPO, _SONDE_FALLITE
    if not _DISPONIBILE or os.environ.get("GAS_WEB_LEXBOR", "").strip() != "1":
        return False
    if _FIGLIO_OK is not None:
        return _FIGLIO_OK
    if time.monotonic() < _RIPROVA_DOPO or not _SONDA.acquire(blocking=False):
        return False
    try:
        if _FIGLIO_OK is None and time.monotonic() >= _RIPROVA_DOPO:
            letto, motivo = _esegui("<title>t</title><p>x</p>", frozenset(), frozenset())
            if letto == ("x", "t"):
                _FIGLIO_OK = True
            else:
                _SONDE_FALLITE += 1
                if _SONDE_FALLITE >= MAX_SONDE:
                    _FIGLIO_OK = False
                    logger.warning("leggi_pagina: GAS_WEB_LEXBOR=1 ma il processo figlio non legge con lexbor "
                                   "(%d sonde fallite), si usa la lettura di sempre", _SONDE_FALLITE)
                else:
                    _RIPROVA_DOPO = time.monotonic() + RIPROVA_SONDA
                    logger.warning("leggi_pagina: sonda di lexbor fallita (%s), si riprova fra %.0f s",
                                   motivo, RIPROVA_SONDA)
        return bool(_FIGLIO_OK)
    finally:
        _SONDA.release()


def testo_visibile(html: str, nascosti: frozenset, blocchi: frozenset) -> Optional[tuple[str, str]]:
    """(testo, titolo) di una pagina text/html come la mostra il browser con gli script
    attivi, o None se lexbor non c'è, supera TEMPO_MAX o MEMORIA_MAX o fallisce. Il contenuto
    dei tag in `nascosti` (script, svg, canvas, object…) non si legge; i tag in `blocchi` vanno
    a capo. Una pagina a frame (senza body) dà testo vuoto, come nel browser."""
    if not _DISPONIBILE:
        return None
    return _esegui(html, nascosti, blocchi)[0]


def _ultima_riga(errore: bytes) -> str:
    """L'ultima riga dello stderr del figlio, per la scatola nera: corta e solo stampabile."""
    righe = errore.decode("utf-8", "replace").strip().splitlines()
    return "".join(c if c.isprintable() else "?" for c in (righe[-1] if righe else ""))[:200]


def _esegui(html: str, nascosti: frozenset, blocchi: frozenset) -> tuple[Optional[tuple[str, str]], str]:
    """Il lavoro di testo_visibile, nel processo figlio: (risultato o None, motivo), con
    motivo «ok», «tempo» (oltre TEMPO_MAX) o «errore»."""
    try:
        dati = html.encode("utf-8")
        esito = subprocess.run(
            [sys.executable, "-I", "-c", _FIGLIO, str(MEMORIA_MAX),
             json.dumps(sorted(nascosti)), json.dumps(sorted(blocchi))],
            input=dati, capture_output=True, timeout=TEMPO_MAX, env={}, check=False)
        if esito.returncode != 0:
            logger.warning("leggi_pagina: lettura con lexbor fallita (uscita %s: %r), si usa quella di sempre",
                           esito.returncode, _ultima_riga(esito.stderr))
            return None, "errore"
        letto = json.loads(esito.stdout)
        return (letto["testo"], letto["titolo"]), "ok"
    except subprocess.TimeoutExpired:
        logger.warning("leggi_pagina: lettura con lexbor oltre %.0f s, si usa quella di sempre", TEMPO_MAX)
        return None, "tempo"
    except Exception as e:
        logger.warning("leggi_pagina: lettura con lexbor fallita (%s), si usa quella di sempre", type(e).__name__)
        return None, "errore"
