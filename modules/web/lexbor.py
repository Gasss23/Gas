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
# Namespace come nel parser del browser (lexbor non lo dice): da HTML «svg» e «math» aprono il
# loro; nello straniero si resta nel namespace del padre, tranne dentro i punti d'integrazione
# del namespace giusto (foreignObject, desc, title di svg; mi, mo, mn, ms, mtext di math, dove
# mglyph e malignmark restano math; annotation-xml con encoding HTML), dove si torna a HTML; un
# svg dentro annotation-xml è svg (R-520-4, R-540-1, B-547-1).
def ns_figli(padre, ns):
    tag = padre.tag.lower()
    if ns == "svg" and tag in ("foreignobject", "desc", "title"):
        return "html"
    if ns == "math" and tag in ("mi", "mo", "mn", "ms", "mtext"):
        return "testo"
    if ns == "math" and tag == "annotation-xml":
        codifica = (padre.attrs.get("encoding") or "").lower()
        return "html" if codifica in ("text/html", "application/xhtml+xml") else "annotazione"
    return ns

def ns_di(nodo, ns):
    # Namespace di un elemento i cui fratelli stanno in `ns` (risultato di ns_figli).
    tag = nodo.tag.lower()
    if ns in ("html", "testo", "annotazione") and tag in ("svg", "math"):
        return tag
    if ns == "testo":
        return "math" if tag in ("mglyph", "malignmark") else "html"
    return "math" if ns == "annotazione" else ns

def elementi(radice, ns="html"):
    # (elemento, namespace) sotto radice, in ordine d'albero, scendendo una volta sola.
    pila = [(radice.iter(include_text=False), ns)]
    while pila:
        figli, ns = pila[-1]
        nodo = next(figli, None)
        if nodo is None:
            pila.pop()
        elif nodo.is_element_node:
            proprio = ns_di(nodo, ns)
            yield nodo, proprio
            pila.append((nodo.iter(include_text=False), ns_figli(nodo, proprio)))

# Il titolo è il primo title HTML in ordine d'albero (un title in foreignObject vale, quello di
# svg no). Senza svg né math basta il primo title.
titolo = ""
if albero.css_first("svg, math") is None:
    primo = albero.css_first("title")
    titolo = primo.text(deep=True) if primo is not None else ""
elif albero.root is not None:
    for nodo, ns in elementi(albero.root):
        if nodo.tag == "title" and ns == "html":
            titolo = nodo.text(deep=True)
            break
def nascosto(nodo):
    attributi = nodo.attrs
    return "hidden" in attributi or (nodo.tag == "dialog" and "open" not in attributi)

def opzioni_visibili(select):
    # La «list of options» dello standard, scendendo dall'alto una volta sola (lineare,
    # R-527-2): solo le opzioni HTML (anche dentro un foreignObject); non si entra in select,
    # hr, option, datalist né in un optgroup dentro un altro optgroup. Per ogni opzione
    # (opzione, visibile, disabilitata): visibile se fuori dai sotto-alberi nascosti;
    # disabilitata con «disabled» o con l'optgroup più vicino «disabled» (R-ve277-3, R-529-1).
    trovate = []
    pila = [(select.iter(include_text=False), "html", True, False, False)]
    while pila:
        figli, ns, visibile, in_gruppo, gruppo_spento = pila[-1]
        nodo = next(figli, None)
        if nodo is None:
            pila.pop()
            continue
        if not nodo.is_element_node:
            continue  # commenti: iter(include_text=False) li restituisce lo stesso
        proprio = ns_di(nodo, ns)
        html = proprio == "html"
        if html and nodo.tag == "option":
            trovate.append((nodo, visibile and not nascosto(nodo), gruppo_spento or "disabled" in nodo.attrs))
        elif html and (nodo.tag in ("select", "hr", "datalist") or (nodo.tag == "optgroup" and in_gruppo)):
            continue
        else:
            sotto = visibile and nodo.tag not in nascosti and not nascosto(nodo)
            gruppo = html and nodo.tag == "optgroup"
            pila.append((nodo.iter(include_text=False), ns_figli(nodo, proprio), sotto, in_gruppo or gruppo,
                         ("disabled" in nodo.attrs) if gruppo else gruppo_spento))
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

def opzioni(select):
    attributi = select.attrs
    tutte = opzioni_visibili(select)
    if "multiple" in attributi or (intero(attributi.get("size")) or 1) > 1:
        # Lista aperta: si vedono le opzioni fuori dai sotto-alberi nascosti e senza «hidden».
        tutte = [o for o, visibile, _ in tutte if visibile]
    else:
        # Tendina chiusa: si vede l'opzione scelta, l'ultima con «selected» (anche se è
        # nascosta, come il segnaposto «Scegli»), se no la prima non disabilitata, anche se
        # nascosta: è la selezione automatica dello standard (R-527-3, R-528-2, R-ve277-3).
        scelte = [o for o, _, _ in tutte if "selected" in o.attrs]
        libere = [o for o, _, spenta in tutte if not spenta]
        tutte = scelte[-1:] or libere[:1]
    # Il testo dell'opzione passa dalla stessa visita del body: nel select nuovo un'opzione
    # può contenere altri tag, anche script o elementi nascosti (V-1 ve #277 bis).
    # Il testo dell'opzione è quello dei suoi discendenti (option.text): uno slot lì dentro
    # mostra la sua riserva, mai i figli dell'host assegnati (V-1 bot #288 su 300e1aa).
    return [o.attrs.get("label") or visita(o, True) for o in tutte]

def primo_summary(details):
    for figlio in details.iter(include_text=False):
        if figlio.tag == "summary":
            yield figlio
            return

# Gli elementi che possono avere uno shadow, oltre ai nomi con il trattino (custom element),
# tranne quelli riservati di svg e math (R-539-2). Per lo standard di oggi («valid custom
# element name» di HTML, «valid element local name» di DOM) basta iniziale a-z, trattino e
# niente maiuscole A-Z, spazi, NUL, «/» o «>» (R-543-1): il tag che dà lexbor è già così,
# anche «x-a!» (V-2 ve #288 riletta alla fonte dal revisore #542).
HOST = frozenset({"article", "aside", "blockquote", "body", "div", "footer", "h1", "h2", "h3",
                  "h4", "h5", "h6", "header", "main", "nav", "p", "section", "span"})
RISERVATI = frozenset({"annotation-xml", "color-profile", "font-face", "font-face-src",
                       "font-face-uri", "font-face-format", "font-face-name", "missing-glyph"})

def primi_slot(frammento):
    # Ogni nome va al primo slot che lo porta, nell'ordine dello shadow, anche se quello slot
    # è nascosto; contano solo gli slot HTML: non quelli di svg e math (R-539-2), sì quelli in
    # un punto d'integrazione come foreignObject (R-540-1, B-547-1). iter() non entra nel
    # contenuto dei template: gli shadow annidati hanno i loro. Discesa lineare.
    primi = {}
    for nodo, ns in elementi(frammento):
        if nodo.tag == "slot" and ns == "html":
            primi.setdefault(nodo.attrs.get("name") or "", nodo.mem_id)
    return primi

# Senza template shadowrootmode fuori dai template non ce ne sono nemmeno dentro: le pagine
# normali non pagano la ricerca degli shadow tra i figli.
CON_SHADOW = albero.css_first("template[shadowrootmode]") is not None

def shadow(nodo):
    # (frammento, slot) dello shadow dichiarativo dell'host, o None. Vale il primo template
    # figlio con shadowrootmode open o closed, come nel parser del browser; gli altri restano
    # template normali, cioè nascosti. Limite: lo shadow si cerca sull'albero finale. Il
    # browser lo attacca mentre legge la pagina; se poi l'adoption agency sposta il template
    # (tag di formattazione chiusi in ordine sbagliato) qui l'host non ha più lo shadow e si
    # leggono i suoi figli (V-1 bot e ve #288 su 6627250).
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
            # solo allo slot senza nome. Il template dello shadow non è un figlio: con un
            # attributo «slot» toglierebbe la riserva a quello slot (V-3 ve #288).
            # Con shadowrootslotassignment=manual nessun figlio va agli slot da sé: si vedono le
            # riserve (V-3 ve #288 su 300e1aa).
            assegnati = {}
            manuale = (figlio.attrs.get("shadowrootslotassignment") or "").lower() == "manual"
            for luce in ([] if manuale else nodo.iter(include_text=True)):
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
        # Dentro un'opzione si legge il suo testo (i discendenti): niente shadow (R-544-1).
        trovato = None if dentro_opzione else shadow(nodo)
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
                    pezzi.append("\n" + "\n".join(opzioni(nodo)) + "\n")
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
    sonde fallite la lettura con lexbor si spegne (R-521-2, V-3 bot e ve #277). Fuori da
    Linux è spenta subito, senza sonde: il figlio lì si rifiuta (R-ve277-4)."""
    global _FIGLIO_OK, _RIPROVA_DOPO, _SONDE_FALLITE
    if not _DISPONIBILE or sys.platform != "linux" or os.environ.get("GAS_WEB_LEXBOR", "").strip() != "1":
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
