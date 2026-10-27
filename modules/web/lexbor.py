"""Lettura del testo visibile con lexbor (selectolax), in prova (R-ve246-5, fetta 19 chat Mani).

leggi.py imita a mano le regole del browser per sapere quale testo si vede, e ogni giro di
verifiche ne trova un caso nuovo (canvas/object: R-ve246-5). lexbor costruisce l'albero come
il browser, con gli script attivi come nel modello di Gas, ed è già l'oracolo con cui Gas si
controlla. Qui si legge il testo da quell'albero, con gli stessi contenitori nascosti di
leggi.py. È SPENTO per default: si accende con GAS_WEB_LEXBOR=1 e serve a misurare, non a
sostituire.

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
from typing import Optional

logger = logging.getLogger("gas.web")

TEMPO_MAX = 4.0              # secondi per pagina nel processo figlio
MEMORIA_MAX = 1 << 30        # byte di memoria virtuale del figlio

_DISPONIBILE = importlib.util.find_spec("selectolax") is not None
_FIGLIO_OK: Optional[bool] = None  # esito della sonda del figlio, una volta sola (R-520-3)

# Codice del figlio: legge la pagina da stdin, scrive {"testo", "titolo"} su stdout. Il titolo
# è quello della scheda come nel browser, il primo «title» HTML del documento (non di svg o
# math); il body si visita senza ricorsione (una pagina annidata a fondo non esaurisce la pila)
# saltando i contenitori nascosti e il titolo, con un a capo per i blocchi come in leggi.py.
_FIGLIO = r"""
import json, resource, sys
resource.setrlimit(resource.RLIMIT_AS, (int(sys.argv[1]), int(sys.argv[1])))
from selectolax.lexbor import LexborHTMLParser
nascosti = frozenset(json.loads(sys.argv[2])) | {"title"}
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
pezzi = []
corpo = albero.body
pila = [(corpo.tag, corpo.iter(include_text=True))] if corpo is not None else []
while pila:
    tag, figli = pila[-1]
    nodo = next(figli, None)
    if nodo is None:
        pila.pop()
        if tag in blocchi:
            pezzi.append("\n")
        continue
    if nodo.is_text_node:
        pezzi.append(nodo.text_content or "")
    elif nodo.is_element_node and nodo.tag not in nascosti:
        if nodo.tag in blocchi:
            pezzi.append("\n")
        pila.append((nodo.tag, nodo.iter(include_text=True)))
sys.stdout.write(json.dumps({"testo": "".join(pezzi), "titolo": titolo}))
"""


def attivo() -> bool:
    """La lettura con lexbor è accesa (GAS_WEB_LEXBOR=1), la libreria c'è e il figlio la trova:
    con «-I» e l'ambiente vuoto il figlio non vede PYTHONPATH, quindi la libreria trovata qui
    può mancargli; lo dice una sonda, una volta sola (R-520-3)."""
    global _FIGLIO_OK
    if not _DISPONIBILE or os.environ.get("GAS_WEB_LEXBOR", "").strip() != "1":
        return False
    if _FIGLIO_OK is None:
        _FIGLIO_OK = _esegui("<title>t</title><p>x</p>", frozenset(), frozenset()) == ("x", "t")
        if not _FIGLIO_OK:
            logger.warning("leggi_pagina: GAS_WEB_LEXBOR=1 ma il processo figlio non legge con lexbor, "
                           "si usa la lettura di sempre")
    return _FIGLIO_OK


def testo_visibile(html: str, nascosti: frozenset, blocchi: frozenset) -> Optional[tuple[str, str]]:
    """(testo, titolo) di una pagina text/html come la mostra il browser con gli script
    attivi, o None se lexbor non c'è, supera TEMPO_MAX o MEMORIA_MAX o fallisce. Il contenuto
    dei tag in `nascosti` (script, svg, canvas, object…) non si legge; i tag in `blocchi` vanno
    a capo. Una pagina a frame (senza body) dà testo vuoto, come nel browser."""
    if not _DISPONIBILE:
        return None
    return _esegui(html, nascosti, blocchi)


def _esegui(html: str, nascosti: frozenset, blocchi: frozenset) -> Optional[tuple[str, str]]:
    """Il lavoro di testo_visibile, nel processo figlio; None su ogni errore."""
    try:
        dati = html.encode("utf-8")
        esito = subprocess.run(
            [sys.executable, "-I", "-c", _FIGLIO, str(MEMORIA_MAX),
             json.dumps(sorted(nascosti)), json.dumps(sorted(blocchi))],
            input=dati, capture_output=True, timeout=TEMPO_MAX, env={}, check=False)
        if esito.returncode != 0:
            logger.warning("leggi_pagina: lettura con lexbor fallita (uscita %s), si usa quella di sempre",
                           esito.returncode)
            return None
        letto = json.loads(esito.stdout)
        return letto["testo"], letto["titolo"]
    except subprocess.TimeoutExpired:
        logger.warning("leggi_pagina: lettura con lexbor oltre %.0f s, si usa quella di sempre", TEMPO_MAX)
        return None
    except Exception as e:
        logger.warning("leggi_pagina: lettura con lexbor fallita (%s), si usa quella di sempre", type(e).__name__)
        return None
