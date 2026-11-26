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
      RISERVA: <una riga per finding che blocca il merge; il lettore ne tiene RISERVE_MAX e conta
               le altre>
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
# Bot #409 su 0b039727 e 20fddc0c V-1: anche gli invisibili «Default_Ignorable» di categoria Mn
# (U+034F, U+17B4, U+17B5, U+180B-U+180D, U+180F; U+180E è Cf e lo toglie già il filtro C*); in più un testo libero senza nessuna lettera,
# cifra, punteggiatura o simbolo conta come vuoto (_pulisci), qualunque cosa contenga.
_VUOTI = frozenset("\u115f\u1160\u3164\uffa0\u2800\u034f\u17b4\u17b5") | frozenset(
    chr(c) for c in [*range(0x180B, 0x1810), *range(0xFE00, 0xFE10),
                     *range(0xE0100, 0xE01F0)])
_VISIBILI = ("L", "N", "P", "S")
RIGA_MAX = 300       # caratteri di un testo libero (riserva, riassunto, titolo)
RISERVE_MAX = 5      # righe RISERVA tenute
COMMENTO_MAX = 8000  # un commento più lungo non è un esito
PR_MAX = 9_999_999  # bot #409-quater V-2: le regex accettano al massimo 7 cifre
_RIGA = re.compile(r"^([A-Z_]{2,20}):[ \t]*(.*)$")
_PR = re.compile(r"^#?([1-9][0-9]{0,6})$")
_COMANDO = re.compile(r"^(MERGIA|NO) #([1-9][0-9]{0,6})$")
# Dall'operatore (Telegram): «mergia 412», «mergia la #412», «no 412», «non mergiare 412»
_COMANDO_OPERATORE = re.compile(
    r"^\s*(mergia|mergiala|no|non mergiare)\s+(?:la\s+)?(?:pr\s+)?#?([1-9][0-9]{0,6})\s*[.!]?\s*$",
    re.IGNORECASE | re.ASCII)  # ve #409 V-1: niente «ı» turca né spazi Unicode (U+00A0)


def _pulisci(testo: Any, n: int = RIGA_MAX) -> str:
    """Una riga: niente caratteri di controllo o invisibili, spazi compressi, al massimo n.
    R-864-1: via tutte le categorie Unicode C* (Cc, Cf come U+FEFF/U+2060/«tag», Co, Cs, Cn),
    come scripts/bot_esito.py, al posto di un elenco a mano."""
    t = "".join(" " if unicodedata.category(c).startswith("C") or c in _VUOTI else c
                for c in str(testo or ""))
    t = " ".join(t.split())
    if not any(unicodedata.category(c)[0] in _VISIBILI for c in t):
        return ""  # solo spazi o segni senza base: a schermo sembra vuoto
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


# Bot #411 V-2: anche le virgolette che a schermo somigliano a «» (≪≫, 《》, 〈〉, ‹›, ⟨⟩, ⟪⟫,
# e, R-880MV-1 della review #880-MV e ve #411, ︽︾ ⸨⸩ ❮❯ ❬❭ 「」 『』 〝〞〟)
_SIMILI_A_CAPORALI = str.maketrans({c: '"' for c in
                                    "\u00ab\u00bb\u226a\u226b\u300a\u300b\u3008\u3009"
                                    "\u2039\u203a\u2329\u232a\u27e8\u27e9\u27ea\u27eb\uff02"
                                    "\ufe3d\ufe3e\u2e28\u2e29\u276e\u276f\u276c\u276d"
                                    "\u300c\u300d\u300e\u300f\ufe41\ufe42\ufe43\ufe44"
                                    "\u301d\u301e\u301f\uff62\uff63"})


def _virgolette_simili(testo: str) -> str:
    """Ve #411 (5af3680e) V-1: oltre all'elenco, ogni virgoletta d'apertura o chiusura
    (categorie Unicode Pi/Pf) diventa una virgoletta dritta, e le parentesi angolari o doppie
    dell'elenco anche: nessun carattere che a schermo somiglia a «» resta nella citazione."""
    # R-880MV-2: gli apostrofi tipografici singoli (frequenti dal telefono) diventano «'», e le
    # parentesi restano parentesi (non somigliano a «»: le angolari sono nell'elenco sopra)
    return "".join("'" if c in "\u2018\u2019\u201a\u201b"
                   else '"' if unicodedata.category(c) in ("Pi", "Pf") else c
                   for c in testo.translate(_SIMILI_A_CAPORALI))


def _citato(testo: Any, n: int = RIGA_MAX) -> str:
    """Un testo libero da mostrare all'operatore tra «»: senza «» (né virgolette che le
    somigliano) dentro, così non può chiudere la citazione e sembrare una frase di Gas
    (R-864-3, bot #409 V-1, bot #411 V-2)."""
    return _pulisci(_virgolette_simili(str(testo or "")), n)


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
                else:
                    # ve #411 V-1, R-875MV-1: OGNI riga RISERVA è un finding dichiarato, anche se
                    # illeggibile o vuota (scrivi_esito non ne scrive mai di vuote): si conta, così
                    # blocca la domanda di merge (fail-closed)
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
    """Il testo per l'operatore (Telegram e voce). Prima le parti FISSE scritte da Gas (stato,
    PR, controlli a valori fissi), poi i testi liberi dell'esecutore tra «» con un'etichetta
    (R-864-3, bot #409 V-1: un riassunto non può imitare i controlli né la domanda). La domanda
    sul merge solo con PR valida, CI verde, bot APPROVATO o APPROVATO CON RISERVE, verifica
    esterna non BOCCIATO e NESSUNA riga RISERVA (ve #409 V-2: le RISERVA sono i finding che
    bloccano il merge): la regola è in propone_merge. Il merge vero lo decide comunque
    CLAUDE.md §10."""
    try:
        try:
            n = int(numero_richiesta)
        except (TypeError, ValueError):
            n = 0
        testa = f"Richiesta di sviluppo #{n} «{_citato(titolo, 80)}»"
        stato = esito.get("esito")
        pr = esito.get("pr")
        pr_ok = isinstance(pr, int) and not isinstance(pr, bool) and 0 < pr <= PR_MAX
        # ve #409-ter V-1: un dizionario fatto a mano non porta valori fuori elenco
        ci = esito.get("ci") if esito.get("ci") in CI else "assente"
        bot = esito.get("bot") if esito.get("bot") in BOT else "assente"
        verifica_ok = esito.get("verifica_esterna", "assente") in VERIFICA  # R-867-2
        verifica = esito.get("verifica_esterna", "assente") if verifica_ok else "assente"
        grezze = esito.get("riserve") or []
        grezze = grezze if isinstance(grezze, list) else [grezze]
        riserve = [_citato(x) for x in grezze if _citato(x)]
        altre = esito.get("riserve_altre")
        altre = altre if isinstance(altre, int) and not isinstance(altre, bool) and altre > 0 else 0
        # bot #411 V-1: ogni elemento conta, anche se illeggibile (come nel lettore)
        n_riserve = len(grezze) + altre
        stato_txt = {"pronta": "fatta", "fallita": "non riuscita",
                     "ferma": "mi sono fermato, serve te"}.get(stato, "esito non chiaro")
        fissi = [f"PR #{pr}" if pr_ok else "nessuna PR", f"CI {ci}", f"bot {bot}"]
        if verifica != "assente":
            fissi.append(f"verifica esterna {verifica}")
        if n_riserve:
            fissi.append(f"riserve aperte: {n_riserve}")
        testo = f"{testa}: {stato_txt}. " + ", ".join(fissi) + "."
        riassunto = _citato(esito.get("riassunto"))
        if riassunto:
            testo += f" Dice l'esecutore: «{riassunto}»."
        if riserve:
            testo += " Riserve: " + "; ".join(f"«{x}»" for x in riserve)
            testo += (f" (+{altre} altre)." if altre else ".")
        if stato != "pronta":
            return testo
        if not propone_merge(esito):
            return testo + " Niente merge per ora."
        return testo + f" Vuoi che la mergi? Rispondi «mergia {pr}» oppure «no {pr}»."
    except Exception:  # §9
        # R-873MV-2: niente valore grezzo nel ripiego
        n = numero_richiesta if isinstance(numero_richiesta, int) else 0
        return f"Richiesta di sviluppo #{n}: c'è un esito, guardalo sulla issue."


def propone_merge(esito: Any) -> bool:
    """True SOLO se la frase per l'operatore chiede il merge: esito «pronta», PR valida, CI
    verde, bot APPROVATO o APPROVATO CON RISERVE, verifica esterna in elenco e non BOCCIATO,
    nessuna riga RISERVA. Fail-closed anche su un dizionario fatto a mano (bot #411 V-1): un
    elemento di riserve conta anche se illeggibile, un riserve_altre presente ma non intero
    toglie la domanda. F3 ricorda la PR per cui la domanda è stata fatta (R-873MV-1). Mai
    eccezioni: nel dubbio False."""
    try:
        if not isinstance(esito, dict) or esito.get("esito") != "pronta":
            return False
        pr = esito.get("pr")
        if not (isinstance(pr, int) and not isinstance(pr, bool) and 0 < pr <= PR_MAX):
            return False
        if esito.get("ci") != "verde" or esito.get("bot") not in ("APPROVATO",
                                                                 "APPROVATO CON RISERVE"):
            return False
        verifica = esito.get("verifica_esterna", "assente")
        if verifica not in VERIFICA or verifica == "BOCCIATO":
            return False
        if esito.get("riserve") not in (None, []):
            return False
        altre = esito.get("riserve_altre", 0)
        return isinstance(altre, int) and not isinstance(altre, bool) and altre == 0
    except Exception:  # §9
        return False


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
