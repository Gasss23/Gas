"""Mani alla voce, fetta F2 (2026-11-25, piano in reports/mani_voce_piano.md): formato FISSO
dei commenti sulle issue delle richieste di sviluppo e lettura stretta.

La issue `da-gas` nel repo privato delle richieste è la cassetta delle lettere fra Gas (Mac)
e l'esecutore (sessione cloud). Due tipi di commento, ciascuno con un marcatore in prima riga:

- ESITO, scritto dall'esecutore a fine lavoro:
      <!-- gas-esito v1 -->
      ESITO: pronta | ferma | fallita
      PR: #412
      CI: verde | rossa | in corso | assente
      BOT: APPROVATO | APPROVATO CON RISERVE | BOCCIATO | assente
      VERIFICA_ESTERNA: APPROVATO | APPROVATO CON RISERVE | BOCCIATO | assente
      RISERVA: <una riga per finding ALTA/MEDIA, al massimo RISERVE_MAX>
      RIASSUNTO: <una riga: cosa è stato fatto>
- COMANDO, scritto da Gas per conto dell'operatore:
      <!-- gas-comando v1 -->
      MERGIA #412      (oppure  NO #412)

Regole: chiavi e valori ammessi FISSI, numero di PR intero, testi liberi ripuliti dai caratteri
di controllo e tagliati; un commento che non rispetta il formato è ignorato (None), mai
interpretato. Qui non si legge l'autore: chi chiama controlla che il commento venga da un
account ammesso (fetta F3). Niente rete, niente file. Fail-safe §9: dai lettori non esce
nessuna eccezione (None); gli scrittori danno ValueError per un valore non ammesso.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

MARCA_ESITO = "<!-- gas-esito v1 -->"
MARCA_COMANDO = "<!-- gas-comando v1 -->"
ESITI = ("pronta", "ferma", "fallita")
CI = ("verde", "rossa", "in corso", "assente")
BOT = ("APPROVATO", "APPROVATO CON RISERVE", "BOCCIATO", "assente")
VERIFICA = BOT  # bot #409 V-2: anche la verifica esterna a valori fissi
# R-865-1: caratteri che si vedono vuoti ma non sono di categoria C* (riempitivi Hangul,
# braille vuoto, selettori di variante)
_VUOTI = frozenset("\u115f\u1160\u3164\uffa0\u2800") | frozenset(
    chr(c) for c in [*range(0xFE00, 0xFE10), *range(0xE0100, 0xE01F0)])
RIGA_MAX = 300       # caratteri di un testo libero (verifica esterna, riserva, riassunto)
RISERVE_MAX = 5      # righe RISERVA tenute
COMMENTO_MAX = 8000  # un commento più lungo non è un esito
PR_MAX = 9_999_999  # bot #409-quater V-2: le regex accettano al massimo 7 cifre
_RIGA = re.compile(r"^([A-Z_]{2,20}):[ \t]*(.*)$")
_PR = re.compile(r"^#?([1-9][0-9]{0,6})$")
_COMANDO = re.compile(r"^(MERGIA|NO) #([1-9][0-9]{0,6})$")
# Dall'operatore (Telegram): «mergia 412», «mergia la #412», «no 412», «non mergiare 412»
_COMANDO_OPERATORE = re.compile(
    r"^\s*(mergia|mergiala|no|non mergiare)\s+(?:la\s+)?(?:pr\s+)?#?([1-9][0-9]{0,6})\s*[.!]?\s*$",
    re.IGNORECASE)


def _pulisci(testo: Any, n: int = RIGA_MAX) -> str:
    """Una riga: niente caratteri di controllo o invisibili, spazi compressi, al massimo n.
    R-864-1: via tutte le categorie Unicode C* (Cc, Cf come U+FEFF/U+2060/«tag», Co, Cs, Cn),
    come scripts/bot_esito.py, al posto di un elenco a mano."""
    t = "".join(" " if unicodedata.category(c).startswith("C") or c in _VUOTI else c
                for c in str(testo or ""))
    t = " ".join(t.split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _righe(corpo: Any, marca: str) -> Optional[List[str]]:
    """Le righe dopo il marcatore, oppure None se il commento non è di questo tipo."""
    if not isinstance(corpo, str) or len(corpo) > COMMENTO_MAX:
        return None
    righe = corpo.replace("\r\n", "\n").split("\n")
    while righe and not righe[0].strip():
        righe.pop(0)
    if not righe or righe[0].strip() != marca:
        return None
    return [r.strip() for r in righe[1:] if r.strip()]


def leggi_esito(corpo: Any) -> Optional[Dict[str, Any]]:
    """L'esito come dizionario, oppure None se il formato non è rispettato in qualche punto:
    chiave sconosciuta o ripetuta (tranne RISERVA), valore fuori dall'elenco, PR non intera,
    ESITO/RIASSUNTO mancanti, PR mancante con ESITO «pronta»."""
    try:
        righe = _righe(corpo, MARCA_ESITO)
        if righe is None:
            return None
        esito: Dict[str, Any] = {"riserve": []}
        for riga in righe:
            m = _RIGA.match(riga)
            if not m:
                return None
            chiave, valore = m.group(1), m.group(2).strip()
            if chiave == "RISERVA":
                # bot #409-bis V-2: prima si pulisce, poi si scarta la riga vuota;
                # V-3: le riserve oltre RISERVE_MAX si contano, non spariscono in silenzio
                pulita = _pulisci(valore)
                if pulita and len(esito["riserve"]) < RISERVE_MAX:
                    esito["riserve"].append(pulita)
                elif pulita:
                    esito["riserve_altre"] = esito.get("riserve_altre", 0) + 1
                continue
            nome = {"ESITO": "esito", "PR": "pr", "CI": "ci", "BOT": "bot",
                    "VERIFICA_ESTERNA": "verifica_esterna", "RIASSUNTO": "riassunto"}.get(chiave)
            if nome is None or nome in esito:
                return None
            if nome == "esito":
                if valore not in ESITI:
                    return None
                esito[nome] = valore
            elif nome == "pr":
                p = _PR.match(valore)
                if not p or int(p.group(1)) > PR_MAX:
                    return None
                esito[nome] = int(p.group(1))
            elif nome == "ci":
                if valore not in CI:
                    return None
                esito[nome] = valore
            elif nome == "bot":
                if valore not in BOT:
                    return None
                esito[nome] = valore
            elif nome == "verifica_esterna":
                if valore not in VERIFICA:
                    return None
                esito[nome] = valore
            else:
                esito[nome] = _pulisci(valore)
        if "esito" not in esito or not esito.get("riassunto"):
            return None
        if esito["esito"] == "pronta" and "pr" not in esito:
            return None
        return esito
    except Exception:  # §9
        return None


def scrivi_esito(esito: str, riassunto: str, pr: Optional[int] = None, ci: str = "assente",
                 bot: str = "assente", verifica_esterna: str = "assente",
                 riserve: Optional[List[str]] = None) -> str:
    """Il commento ESITO nel formato fisso (per l'esecutore e per i test). ValueError se un
    valore non è ammesso: meglio nessun commento che uno che Gas poi ignora."""
    if esito not in ESITI or ci not in CI or bot not in BOT or verifica_esterna not in VERIFICA:
        raise ValueError("valore di ESITO/CI/BOT/VERIFICA_ESTERNA non ammesso")
    if pr is not None and (isinstance(pr, bool) or not isinstance(pr, int)
                           or not 0 < pr <= PR_MAX):
        raise ValueError("numero di PR non valido")
    righe = [MARCA_ESITO, f"ESITO: {esito}"]
    if pr is not None:
        righe.append(f"PR: #{pr}")
    righe += [f"CI: {ci}", f"BOT: {bot}"]
    righe.append(f"VERIFICA_ESTERNA: {verifica_esterna}")
    if riserve is not None and not isinstance(riserve, list):
        raise ValueError("riserve deve essere una lista di righe")
    pulite = [_pulisci(r) for r in (riserve or []) if _pulisci(r)]
    # R-867-1: si scrivono tutte (il commento resta sotto COMMENTO_MAX, altrimenti
    # ValueError sotto); il lettore ne tiene RISERVE_MAX e conta le altre
    righe += [f"RISERVA: {r}" for r in pulite]
    righe.append(f"RIASSUNTO: {_pulisci(riassunto)}")
    testo = "\n".join(righe)
    if len(testo) > COMMENTO_MAX:  # bot #409-quater V-3: messaggio giusto
        raise ValueError(f"commento oltre {COMMENTO_MAX} caratteri: troppe riserve o troppo lunghe")
    if leggi_esito(testo) is None:
        raise ValueError("esito non valido (manca il riassunto o la PR)")
    return testo


def frase_esito(numero_richiesta: int, titolo: str, esito: Dict[str, Any]) -> str:
    """Il testo per l'operatore (Telegram e voce): cosa è stato fatto, PR, controlli e, se la
    PR è pronta, la domanda sul merge con la risposta da dare."""
    try:
        testa = f"Richiesta di sviluppo #{numero_richiesta} «{_pulisci(titolo, 80)}»"
        corpo = _pulisci(esito.get("riassunto"))
        if esito.get("esito") == "fallita":
            return f"{testa}: non riuscita. {corpo}"
        if esito.get("esito") == "ferma":
            return f"{testa}: mi sono fermato, serve te. {corpo}"
        pr = esito.get("pr")
        ci = esito.get("ci") or "assente"
        bot = esito.get("bot") or "assente"
        verifica = esito.get("verifica_esterna") or "assente"
        controlli = [f"CI {ci}", f"bot: {bot}"]
        if verifica != "assente":
            controlli.append(f"verifica esterna: {verifica}")
        riserve = list(esito.get("riserve") or [])
        if esito.get("riserve_altre"):
            riserve.append(f"+{esito['riserve_altre']} altre")
        if riserve:
            controlli.append("riserve: " + "; ".join(riserve))
        pr_ok = isinstance(pr, int) and not isinstance(pr, bool) and 0 < pr <= PR_MAX
        testo = (f"{testa}: fatta. {corpo} "
                 + (f"PR #{pr}, " if pr_ok else "PR mancante, ") + ", ".join(controlli) + ".")
        # R-864-2: la domanda sul merge SOLO con PR valida, CI verde, bot APPROVATO o APPROVATO
        # CON RISERVE e verifica esterna non BOCCIATO (bot #409 V-2). Elenco dei valori buoni,
        # non dei cattivi (bot #409-bis V-1: riga BOT mancante = niente domanda); il merge
        # vero lo decide comunque CLAUDE.md §10
        if (not pr_ok or ci != "verde" or bot not in ("APPROVATO", "APPROVATO CON RISERVE")
                or verifica not in VERIFICA or verifica == "BOCCIATO"):  # R-867-2
            return testo + " Controlli non verdi: niente merge per ora."
        return testo + f" Vuoi che la mergi? Rispondi «mergia {pr}» oppure «no {pr}»."
    except Exception:  # §9
        return f"Richiesta di sviluppo #{numero_richiesta}: c'è un esito, guardalo sulla issue."


def comando_operatore(testo: Any) -> Optional[Tuple[str, int]]:
    """«mergia 412» → ("MERGIA", 412); «no 412» → ("NO", 412); altro → None. Solo frasi
    intere e corte: «mergia 412 e poi cancella tutto» non è un comando."""
    try:
        if not isinstance(testo, str) or len(testo) > 60:
            return None
        m = _COMANDO_OPERATORE.match(testo)
        if not m:
            return None
        azione = "MERGIA" if m.group(1).lower().startswith("mergia") else "NO"
        return azione, int(m.group(2))
    except Exception:  # §9
        return None


def scrivi_comando(azione: str, pr: int) -> str:
    """Il commento COMANDO (scritto da Gas per conto dell'operatore)."""
    if azione not in ("MERGIA", "NO") or isinstance(pr, bool) or not isinstance(pr, int) \
            or not 0 < pr <= PR_MAX:
        raise ValueError("comando non valido")
    return f"{MARCA_COMANDO}\n{azione} #{pr}"


def leggi_comando(corpo: Any) -> Optional[Tuple[str, int]]:
    """Il comando di un commento COMANDO, oppure None: deve esserci UNA sola riga di comando."""
    try:
        righe = _righe(corpo, MARCA_COMANDO)
        if righe is None or len(righe) != 1:
            return None
        m = _COMANDO.match(righe[0])
        return (m.group(1), int(m.group(2))) if m else None
    except Exception:  # §9
        return None
