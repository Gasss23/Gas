#!/usr/bin/env python3
"""Bot di verifica esterna (V-B vera) — logica deterministica del workflow verifica-bot.yml.

Due comandi, entrambi eseguiti dal workflow nella versione di MAIN (pull_request_target):

  smista  — legge i file della PR e decide se serve la verifica LLM (dosaggio dei costi):
            una PR che tocca SOLO reports/ si approva senza chiamare Claude; una PR che
            tocca la macchina del bot stesso non si approva MAI (merge all'operatore).
  esito   — legge il verdetto strutturato del bot, ricontrolla la head della PR e pubblica
            una review LEGATA ALLO SHA verificato: APPROVE solo se il verdetto non è
            BOCCIATO e non c'è nessun finding ALTA/MEDIA; altrimenti COMMENT (niente
            approvazione = niente merge, l'agente aggiusta e ripusha).

La decisione sta qui e non nel modello: il modello produce un verdetto, questo script
decide se approvare. Ogni dubbio (JSON rotto, testo incoerente, head cambiata) = COMMENT.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

VERDETTI = ("APPROVATO", "APPROVATO CON RISERVE", "BOCCIATO")
GRAVITA_BLOCCANTI = ("ALTA", "MEDIA")
GRAVITA = ("ALTA", "MEDIA", "BASSA", "COSMETICA")
# Limite GitHub sul corpo di una review: 65536 caratteri. Margine per intestazione.
MAX_TESTO = 60000
MAX_CORPO = 65000
# L'API dei file di una PR restituisce al massimo 3000 file: oltre, l'elenco è parziale.
MAX_FILE_API = 3000

# R-158-1: file che definiscono il bot (workflow, decisione, protocollo, configurazione
# di Claude caricata dal bot). Un'approvazione sbagliata qui si autoalimenterebbe (es. un
# workflow `on: push` con environment verifica-bot riceverebbe la chiave dell'App):
# queste PR le mergia solo l'operatore. Riga con "/" finale = cartella.
MACCHINA_BOT = (
    ".github/",
    ".claude/verifica_esterna.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
    # R-159-1: gli hook sono bash arbitrario (il bot gira con --setting-sources user e non
    # li carica, ma un domani basterebbe un flag per riattivarli col token nell'env).
    ".claude/hooks/",
    ".mcp.json",
    ".claude.json",
    # V-5 verifica esterna #130: la macchina che decide i merge (gate, gasmerge, perimetro,
    # revisore, fine-task) e i test che la proteggono. Per queste PR decide l'operatore.
    "scripts/",
    ".claude/perimetro_review.txt",
    ".claude/agents/revisore.md",
    ".claude/commands/fine-task.md",
    "tests/test_unit_verifica_bot.py",
    "tests/test_unit_gasmerge.py",
    "tests/test_unit_gate.py",
    "tests/test_unit_hooks.py",
    "tests/test_unit_handoff_check.py",
)
# V-6 verifica esterna #130 bis: report che contengono istruzioni operative o criteri
# (setup dei segreti, design dei gate) passano dalla verifica LLM anche se sono .md.
DOC_DA_VERIFICARE = ("reports/setup_", "reports/design_")
# Istruzioni per Claude in QUALSIASI cartella (un CLAUDE.md annidato diventa istruzioni).
NOMI_MACCHINA_BOT = ("CLAUDE.md", "CLAUDE.local.md")
# R-159-2: il repo è pubblico e la review anche. Un testo con forme di credenziali non si
# pubblica (prompt injection che fa leggere al bot il proprio ambiente).
_SEGRETO = re.compile(r"sk-ant-|gh[pousr]_[A-Za-z0-9]|github_pat_|-----BEGIN")

# R-158-2: la riga del verdetto è una riga che INIZIA con "VERIFICA ESTERNA" (un preambolo
# che la cita a metà frase non conta); tutte le righe così devono dire la stessa cosa.
_RIGA_VERDETTO = re.compile(
    r"^\W*VERIFICA ESTERNA\b[^\n]*?(APPROVATO CON RISERVE|APPROVATO|BOCCIATO)", re.M | re.I)
_FINDING_GRAVITA = re.compile(r"\b[A-Za-z]+-\d+\b[^\n(]*\(([^)\n]*)\)")
_PAROLA_BLOCCANTE = re.compile(r"\b(ALTA|MEDIA)\b")
# V-4 verifica esterna #130: "NON APPROVATO", "DISAPPROVATO", "non bocciato" sulla riga
# del verdetto la rendono ambigua.
_NEGAZIONE = re.compile(r"(\bNON\s+|DIS)(APPROVATO|BOCCIATO)", re.I)
_RIGA_TITOLO = re.compile(r"^\W*VERIFICA ESTERNA\b[^\n]*$", re.M | re.I)
# Riga di finding nel formato del protocollo ("V-1 ...") con una gravità bloccante scritta
# in minuscolo o a parole ("V-1 — grave: ...", "V-2 — media — ...").
_FINDING_GRAVE_A_PAROLE = re.compile(
    r"^\W*V-\d+\b.*\b(alta|media|grave|gravi|critic[aoi]|critiche)\b", re.M | re.I)


def solo_reports(files: list[str]) -> bool:
    """True se OGNI path (compresi i vecchi nomi dei rename) è un .md sotto reports/
    (V-5 #130: output di sonde .txt/.json non passano senza verifica)."""
    if not files or len(files) >= MAX_FILE_API:
        return False
    return all(f.startswith("reports/") and f.endswith(".md") and ".." not in f.split("/")
               and not f.startswith(DOC_DA_VERIFICARE) for f in files)


def tocca_macchina_bot(files: list[str]) -> bool:
    """True se un path (anche vecchio nome di un rename) cade in MACCHINA_BOT. Elenco
    vuoto o troncato dall'API = non verificabile = sì (prudenza)."""
    if not files or len(files) >= MAX_FILE_API:
        return True
    for f in files:
        if f.rsplit("/", 1)[-1] in NOMI_MACCHINA_BOT:
            return True
        for voce in MACCHINA_BOT:
            if (f.startswith(voce) if voce.endswith("/") else f == voce):
                return True
    return False


def _dopo_finding(testo: str) -> str:
    """Testo da "FINDING:" in poi (FINDING, NON VERIFICATO, RACCOMANDAZIONE): le citazioni
    di verifiche passate in Metodo/CLAIM non contano. Senza la sezione: tutto il testo."""
    m = re.search(r"^\W*FINDING:", testo, re.M)
    return testo[m.end():] if m else testo


def _gravita_nel_testo(testo: str) -> set[str]:
    """Gravità citate nel testo libero: "V-1 (media)", "F-2 (MEDIA-BASSA)" e ogni parola
    ALTA/MEDIA maiuscola dopo FINDING ("V-1 — MEDIA — x")."""
    sezione = _dopo_finding(testo)
    trovate: set[str] = set(_PAROLA_BLOCCANTE.findall(sezione))
    if _FINDING_GRAVE_A_PAROLE.search(sezione):
        trovate.add("MEDIA")
    # R-159-3: tra parentesi conta la gravità che APRE la parentesi ("(alta)", "(MEDIA-BASSA)"),
    # non una parola qualsiasi ("(test saltati)", "(in media 3 ms)", "(parte multimediale)").
    for gruppo in _FINDING_GRAVITA.findall(sezione):
        m = re.match(r"\s*(ALTA|MEDIA|BASSA|COSMETICA)\b", gruppo, re.I)
        if m:
            trovate.add(m.group(1).upper())
    return trovate


def contiene_segreti(verdetto: object) -> bool:
    """V-2 #130: forme di credenziali in QUALSIASI campo del verdetto (testo, id e
    descrizioni dei finding finiscono tutti nella review pubblica)."""
    try:
        grezzo = json.dumps(verdetto, ensure_ascii=False)
    except (TypeError, ValueError):
        return True
    return bool(_SEGRETO.search(grezzo))


def decidi(verdetto: dict | None, head_analizzata: str, head_attuale: str,
           doc_only: bool = False, macchina_bot: bool = False) -> tuple[str, str]:
    """Ritorna (evento, motivo). evento ∈ {"APPROVE", "COMMENT"}."""
    if macchina_bot:
        return "COMMENT", ("la PR tocca la macchina del bot (workflow, decisione, protocollo):"
                           " il merge lo decide l'operatore")
    if not head_analizzata or not head_attuale:
        return "COMMENT", "head della PR non verificabile"
    if head_analizzata != head_attuale:
        return "COMMENT", (f"head cambiata durante la verifica ({head_analizzata[:12]} → "
                           f"{head_attuale[:12]}): serve una nuova verifica")
    if doc_only:
        return "APPROVE", "solo file in reports/: approvata senza verifica LLM (dosaggio)"
    if not isinstance(verdetto, dict):
        return "COMMENT", "verifica non eseguita o verdetto illeggibile"
    esito = verdetto.get("verdetto")
    testo = verdetto.get("testo")
    finding = verdetto.get("finding")
    if esito not in VERDETTI or not isinstance(testo, str) or not testo.strip() \
            or not isinstance(finding, list):
        return "COMMENT", "verdetto strutturato incompleto"
    if contiene_segreti(verdetto):
        return "COMMENT", "il verdetto contiene forme di credenziali: non pubblicato"
    if any(_NEGAZIONE.search(r) for r in _RIGA_TITOLO.findall(testo)):
        return "COMMENT", "riga del verdetto con negazione (NON/DIS): verdetto ambiguo"
    righe = [r.upper() for r in _RIGA_VERDETTO.findall(testo)]
    if not righe or any(r != esito for r in righe):
        return "COMMENT", "il testo del verdetto non coincide con il campo verdetto"
    gravita_strutturate: set[str] = set()
    for f in finding:
        if not isinstance(f, dict) or f.get("gravita") not in GRAVITA:
            return "COMMENT", "finding con gravità mancante o non valida"
        gravita_strutturate.add(f["gravita"])
    if esito == "BOCCIATO":
        return "COMMENT", "verdetto BOCCIATO"
    if esito == "APPROVATO CON RISERVE" and not finding:
        return "COMMENT", "APPROVATO CON RISERVE senza finding elencati: verdetto incoerente"
    bloccanti = (gravita_strutturate | _gravita_nel_testo(testo)) & set(GRAVITA_BLOCCANTI)
    if bloccanti:
        return "COMMENT", ("finding " + "/".join(sorted(bloccanti))
                           + ": da aggiustare (con test) prima del merge")
    return "APPROVE", f"verdetto {esito} senza finding ALTA/MEDIA"


def componi_corpo(evento: str, motivo: str, verdetto: dict | None, modello: str,
                  falliti: str) -> str:
    righe = ["## 🤖 Verifica esterna automatica (V-B)", ""]
    righe.append(f"**Esito:** {'APPROVATA' if evento == 'APPROVE' else 'NON approvata'} — {motivo}")
    if modello:
        righe.append(f"**Modello:** `{modello}`")
    if falliti:
        righe.append(f"**Cambio modello:** falliti prima `{falliti}` (cascata dichiarata)")
    if isinstance(verdetto, dict) and contiene_segreti(verdetto):
        righe += ["", "[verdetto NON pubblicato: contiene forme di credenziali — V-2 #130]"]
    elif isinstance(verdetto, dict):
        elenco = verdetto.get("finding")
        minori = [f for f in (elenco if isinstance(elenco, list) else [])
                  if isinstance(f, dict) and f.get("gravita") in ("BASSA", "COSMETICA")]
        if evento == "APPROVE" and minori:
            righe += ["", "**Riserve minori da aggiustare dopo il merge:**"]
            righe += [f"- {f.get('id', '?')} ({f.get('gravita')}): {f.get('descrizione', '')}"
                      for f in minori]
        testo = verdetto.get("testo")
        if isinstance(testo, str) and testo.strip():
            if len(testo) > MAX_TESTO:
                testo = testo[:MAX_TESTO] + "\n…[TRONCATO: verdetto oltre il limite di GitHub]"
            righe += ["", "<details><summary>Verdetto integrale</summary>", "", "```",
                      testo.replace("```", "ʼʼʼ"), "```", "</details>"]
    corpo = "\n".join(righe)
    if len(corpo) > MAX_CORPO:
        corpo = corpo[:MAX_CORPO] + "\n…[TRONCATO: corpo oltre il limite di GitHub]"
    return corpo


def _gh(*args: str, input_text: str | None = None) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True,
                          input=input_text).stdout


def _output(**kv: str) -> None:
    percorso = os.environ.get("GITHUB_OUTPUT")
    righe = "".join(f"{k}={v}\n" for k, v in kv.items())
    if percorso:
        with open(percorso, "a", encoding="utf-8") as fh:
            fh.write(righe)
    print(righe, end="")


def cmd_smista() -> int:
    repo, pr = os.environ["REPO"], os.environ["PR"]
    head = _gh("api", f"repos/{repo}/pulls/{pr}", "--jq", ".head.sha").strip()
    elenco = _gh("api", "--paginate", f"repos/{repo}/pulls/{pr}/files",
                 "--jq", ".[] | .filename, (.previous_filename // empty)")
    files = [r for r in elenco.split("\n") if r]
    _output(head=head, solo_reports="true" if solo_reports(files) else "false",
            macchina_bot="true" if tocca_macchina_bot(files) else "false")
    return 0


def cmd_esito() -> int:
    repo, pr = os.environ["REPO"], os.environ["PR"]
    head_analizzata = os.environ.get("HEAD_ANALIZZATA", "")
    doc_only = os.environ.get("SOLO_REPORTS") == "true"
    # Prudenza: tutto ciò che non è esattamente "false" conta come macchina del bot.
    macchina_bot = os.environ.get("MACCHINA_BOT") != "false"
    grezzo = os.environ.get("VERDETTO_JSON", "")
    try:
        verdetto = json.loads(grezzo) if grezzo.strip() else None
    except json.JSONDecodeError:
        verdetto = None
    try:
        head_attuale = _gh("api", f"repos/{repo}/pulls/{pr}", "--jq", ".head.sha").strip()
    except subprocess.CalledProcessError:
        head_attuale = ""
    evento, motivo = decidi(verdetto, head_analizzata, head_attuale, doc_only, macchina_bot)
    corpo = componi_corpo(evento, motivo, verdetto, os.environ.get("MODELLO", ""),
                          os.environ.get("MODELLI_FALLITI", ""))
    richiesta = {"event": evento, "body": corpo}
    if head_analizzata:
        # La review resta legata al commit verificato: con "dismiss stale reviews" nel
        # ruleset, un push successivo la invalida.
        richiesta["commit_id"] = head_analizzata
    _gh("api", "-X", "POST", f"repos/{repo}/pulls/{pr}/reviews", "--input", "-",
        input_text=json.dumps(richiesta))
    print(f"review {evento}: {motivo}")
    return 0


def main(argv: list[str]) -> int:
    comandi = {"smista": cmd_smista, "esito": cmd_esito}
    if len(argv) != 2 or argv[1] not in comandi:
        print("uso: bot_esito.py smista|esito", file=sys.stderr)
        return 2
    return comandi[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
