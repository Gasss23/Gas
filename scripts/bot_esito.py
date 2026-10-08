#!/usr/bin/env python3
"""Bot di verifica esterna (V-B vera) — logica deterministica del workflow verifica-bot.yml.

Due comandi, entrambi eseguiti dal workflow nella versione di MAIN (pull_request_target):

  smista  — legge i file della PR e decide se serve la verifica LLM (dosaggio dei costi):
            una PR che tocca SOLO reports/ si approva senza chiamare Claude; una PR che
            tocca la macchina del bot stesso non si approva MAI (merge all'operatore).
  esito   — legge il verdetto strutturato del bot, ricontrolla la head della PR e pubblica
            il CHECK RUN `verifica-bot` dell'App sullo SHA verificato (G-1 verifica chat
            #130: il ruleset richiede quel check, l'approvazione di un'App senza Contents
            write non conterebbe): success solo se il verdetto non è BOCCIATO e non c'è
            nessun finding ALTA/MEDIA; il verdetto integrale va anche in una review COMMENT.

La decisione sta qui e non nel modello: il modello produce un verdetto, questo script
decide. Esiti (evento → conclusione del check):
  APPROVE   → success    il sì del bot;
  COMMENT   → failure    NO nel merito (anche testo ambiguo o incoerente): DEFINITIVO per
                         quello SHA (G-2), un rilancio non lo ritira, serve un commit nuovo;
  RIPROVA   → cancelled  verifica non conclusa (head cambiata, verdetto assente, storico
                         del check illeggibile, strumenti_ok non true — R-196-1): nessun
                         giudizio, si può rilanciare;
  OPERATORE → neutral    macchina del bot con un sì del bot: decide l'operatore (neutral
                         non blocca il ruleset; `gasmerge --auto` vuole solo success).
                         R-163-1: si valuta PRIMA il verdetto; solo un APPROVE della
                         macchina del bot diventa OPERATORE, un NO resta NO.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata

VERDETTI = ("APPROVATO", "APPROVATO CON RISERVE", "BOCCIATO")
GRAVITA_BLOCCANTI = ("ALTA", "MEDIA")
GRAVITA = ("ALTA", "MEDIA", "BASSA", "COSMETICA")
NOME_CHECK = "verifica-bot"
CONCLUSIONE = {"APPROVE": "success", "COMMENT": "failure", "RIPROVA": "cancelled",
               "OPERATORE": "neutral"}
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
# G-4 verifica chat #130: senza verifica LLM passano SOLO i log di sessione (lista
# BIANCA). Stato, roadmap, raccomandazioni, setup e design contengono criteri e
# istruzioni: passano dal bot anche se sono .md (assorbe V-6 #130 bis).
LOG_DI_SESSIONE = ("reports/handoff.md", "reports/ultimo_report.md",
                   "reports/diff_sessione.md", "reports/ultima_risposta.md")
# Nomi base che contano in QUALSIASI cartella: un CLAUDE.md annidato diventa istruzioni;
# G-5 #130: un .gitattributes può nascondere file dal diff (`-diff`, `linguist-generated`).
NOMI_MACCHINA_BOT = ("CLAUDE.md", "CLAUDE.local.md", ".gitattributes")
# R-159-2: il repo è pubblico e la review anche. Un testo con forme di credenziali non si
# pubblica (prompt injection che fa leggere al bot il proprio ambiente).
_SEGRETO = re.compile(r"sk-ant-|gh[pousr]_[A-Za-z0-9]|github_pat_|-----BEGIN")

# R-158-2: la riga del verdetto è una riga che INIZIA con "VERIFICA ESTERNA" (un preambolo
# che la cita a metà frase non conta); tutte le righe così devono dire la stessa cosa.
# V-2 seconda verifica #130 + R-161-1: ogni riga che inizia con "VERIFICA ESTERNA" deve
# essere ESATTAMENTE nel formato del protocollo ("VERIFICA ESTERNA #N — ESITO", markdown a
# parte). Una lista di negazioni non finisce mai ("NON-APPROVATO", "NON È APPROVATO",
# "NEGATO / APPROVATO", "APPROVATO (ma io lo boccerei)"): fuori formato = COMMENT.
_RIGA_TITOLO = re.compile(r"^\W*VERIFICA ESTERNA\b[^\n]*$", re.M | re.I)
_TITOLO_CANONICO = re.compile(
    r"VERIFICA ESTERNA(?:\s+(?:PR\s*)?#?\d+)?\s*[—–:-]\s*"
    r"(APPROVATO CON RISERVE|APPROVATO|BOCCIATO)\.?", re.I)
_FINDING_GRAVITA = re.compile(r"\b[A-Za-z]+-\d+\b[^\n(]*\(([^)\n]*)\)")
# Gravità bloccanti, anche in inglese o a parole (V-2 seconda verifica #130: CRITICAL,
# HIGH, blocker, importante passavano).
_GRAVI = (r"alta|media|grave|gravi|critic\w*|high|medium|severe|severa|major|blocker"
          r"|bloccant\w*|important\w*")
_PAROLA_BLOCCANTE = re.compile(r"\b(ALTA|MEDIA|HIGH|MEDIUM|CRITICAL|CRITICA|BLOCKER|BLOCCANTE)\b")
# Riga di finding nel formato del protocollo ("V-1 ...", anche F-/R-/G-) con una gravità
# bloccante scritta in minuscolo o a parole ("V-1 — grave: ...", "F-1 HIGH").
_FINDING_GRAVE_A_PAROLE = re.compile(
    r"^\W*[VFRG]-\d+\b.*\b(" + _GRAVI + r")\b", re.M | re.I)
_APRE_GRAVE = re.compile(r"\s*(" + _GRAVI + r")\b", re.I)


def solo_reports(files: list[str]) -> bool:
    """True se OGNI path (compresi i vecchi nomi dei rename) è un log di sessione della
    lista bianca LOG_DI_SESSIONE (G-4 #130). Tutto il resto passa dal bot."""
    if not files or len(files) >= MAX_FILE_API:
        return False
    return all(f in LOG_DI_SESSIONE for f in files)


def stato_elenco(files: list[str]) -> str:
    """R-163-1: "ok" se l'elenco dei file è verificabile, "vuoto" (API illeggibile: si può
    rilanciare) o "troncato" (oltre il limite dell'API: un rilancio non cambia nulla).
    R-164-3: il conto include i vecchi nomi dei rename, quindi "troncato" può scattare
    poco prima dei 3000 file reali: errore dal lato prudente (NO, mai un sì)."""
    if not files:
        return "vuoto"
    if len(files) >= MAX_FILE_API:
        return "troncato"
    return "ok"


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


# R-161-1 (PR #149, due falsi NO): una riserva GIÀ registrata nel repo, citata col suo id
# di revisione e la gravità tra parentesi ("R-203-1 (ALTA, preesistente)"), non è un
# finding di questa PR. Si toglie SOLO la parentesi della citazione e l'id resta (#205
# B-1: con l'id le regex delle righe di finding vedono ancora il resto della riga);
# niente parentesi annidate (#205 B-2: "R-1-1 (x, V-2 (ALTA))" resta intera e blocca).
_RISERVA_REGISTRATA = re.compile(r"\b(R-\d+-\d+)\b\s*\([^()\n]*\)")


def _gravita_nel_testo(testo: str) -> set[str]:
    """Gravità citate nel testo libero: "V-1 (media)", "F-2 (MEDIA-BASSA)" e ogni parola
    ALTA/MEDIA maiuscola dopo FINDING ("V-1 — MEDIA — x"). Le citazioni di riserve già
    registrate ("R-203-1 (ALTA, ...)") non contano (R-161-1)."""
    sezione = _RISERVA_REGISTRATA.sub(r"\1", _dopo_finding(testo))
    # HIGH, CRITICAL, BLOCKER... contano come MEDIA (bloccanti) anche se fuori vocabolario.
    trovate: set[str] = {p if p in GRAVITA_BLOCCANTI else "MEDIA"
                         for p in _PAROLA_BLOCCANTE.findall(sezione)}
    if _FINDING_GRAVE_A_PAROLE.search(sezione):
        trovate.add("MEDIA")
    # R-159-3: tra parentesi conta la gravità che APRE la parentesi ("(alta)", "(MEDIA-BASSA)"),
    # non una parola qualsiasi ("(test saltati)", "(in media 3 ms)", "(parte multimediale)").
    for gruppo in _FINDING_GRAVITA.findall(sezione):
        m = re.match(r"\s*(ALTA|MEDIA|BASSA|COSMETICA)\b", gruppo, re.I)
        if m:
            trovate.add(m.group(1).upper())
        elif _APRE_GRAVE.match(gruppo):
            trovate.add("MEDIA")
    return trovate


def _caratteri_invisibili(testo: str) -> bool:
    """V-2 seconda verifica #130: "ME\u200bDIA" sfuggiva a ogni regex. Un carattere di
    formato (categoria Unicode Cf: spazi a larghezza zero, controlli bidi) = ambiguo."""
    return any(unicodedata.category(c) == "Cf" for c in testo)


def con_storico(evento: str, motivo: str, precedenti: list[str] | None) -> tuple[str, str]:
    """G-2 verifica chat #130: un NO sullo stesso SHA resta NO. `precedenti` sono le
    conclusioni dei check `verifica-bot` già pubblicati dall'App su quello SHA (None =
    storico illeggibile: niente sì alla cieca)."""
    # R-163-1: anche il sì sulla macchina del bot (OPERATORE) cede a un NO precedente.
    if evento not in ("APPROVE", "OPERATORE"):
        return evento, motivo
    if precedenti is None:
        return "RIPROVA", "storico del check verifica-bot non leggibile: niente sì alla cieca"
    if "failure" in precedenti:
        return "COMMENT", ("su questo SHA il bot ha già detto NO: un rilancio non ritira il"
                           " verdetto (G-2), serve un commit nuovo")
    return evento, motivo


def contiene_segreti(verdetto: object) -> bool:
    """V-2 #130: forme di credenziali in QUALSIASI campo del verdetto (testo, id e
    descrizioni dei finding finiscono tutti nella review pubblica)."""
    try:
        grezzo = json.dumps(verdetto, ensure_ascii=False)
    except (TypeError, ValueError):
        return True
    return bool(_SEGRETO.search(grezzo))


def decidi(verdetto: dict | None, head_analizzata: str, head_attuale: str,
           doc_only: bool = False, macchina_bot: bool | None = False,
           elenco: str = "ok") -> tuple[str, str]:
    """Ritorna (evento, motivo). evento ∈ CONCLUSIONE (vedi docstring del modulo).
    macchina_bot None = informazione mancante; elenco = stato_elenco() dei file della PR.
    R-163-1: "non verificabile" (elenco, macchina_bot mancante) non è mai neutral, e la
    macchina del bot trasforma in OPERATORE solo un APPROVE."""
    if not head_analizzata or not head_attuale:
        return "RIPROVA", "head della PR non verificabile"
    # R-164-1: un NO definitivo (troncato) solo sullo SHA ancora in testa alla PR.
    if head_analizzata != head_attuale:
        return "RIPROVA", (f"head cambiata durante la verifica ({head_analizzata[:12]} → "
                           f"{head_attuale[:12]}): serve una nuova verifica")
    if elenco == "troncato":
        return "COMMENT", (f"elenco dei file troncato dall'API (≥{MAX_FILE_API}): PR non"
                           " verificabile, va spezzata")
    if elenco != "ok":
        return "RIPROVA", "elenco dei file della PR non leggibile: serve una nuova verifica"
    if macchina_bot is None:
        return "RIPROVA", "non si sa se la PR tocca la macchina del bot: serve una nuova verifica"
    evento, motivo = _decidi_verdetto(verdetto, head_analizzata, head_attuale, doc_only)
    if macchina_bot and evento == "APPROVE":
        return "OPERATORE", ("la PR tocca la macchina del bot (workflow, decisione, protocollo):"
                             f" il merge lo decide l'operatore ({motivo})")
    return evento, motivo


def _decidi_verdetto(verdetto: dict | None, head_analizzata: str, head_attuale: str,
                     doc_only: bool) -> tuple[str, str]:
    """Il giudizio sul verdetto, senza la macchina del bot."""
    if not head_analizzata or not head_attuale:
        return "RIPROVA", "head della PR non verificabile"
    if head_analizzata != head_attuale:
        return "RIPROVA", (f"head cambiata durante la verifica ({head_analizzata[:12]} → "
                           f"{head_attuale[:12]}): serve una nuova verifica")
    if doc_only:
        return "APPROVE", "solo log di sessione: approvata senza verifica LLM (dosaggio)"
    if not isinstance(verdetto, dict):
        return "RIPROVA", "verifica non eseguita o verdetto illeggibile"
    # R-196-1: un verdetto dato senza aver letto diff e CI (Bash/gh rotti, terza prova #142)
    # non è un giudizio: né sì né NO definitivo. Campo assente o non True = alla cieca.
    if verdetto.get("strumenti_ok") is not True:
        return "RIPROVA", ("il bot non ha potuto leggere diff e CI della PR (strumenti non"
                           " disponibili): verifica non conclusa, nessun giudizio alla cieca")
    esito = verdetto.get("verdetto")
    testo = verdetto.get("testo")
    finding = verdetto.get("finding")
    if esito not in VERDETTI or not isinstance(testo, str) or not testo.strip() \
            or not isinstance(finding, list):
        return "COMMENT", "verdetto strutturato incompleto"
    if contiene_segreti(verdetto):
        return "COMMENT", "il verdetto contiene forme di credenziali: non pubblicato"
    if _caratteri_invisibili(testo):
        return "COMMENT", "caratteri invisibili (Unicode Cf) nel testo: verdetto ambiguo"
    righe = []
    for riga in _RIGA_TITOLO.findall(testo):
        m = _TITOLO_CANONICO.fullmatch(riga.strip().strip("*_>`# ").strip())
        if not m:
            return "COMMENT", "riga del verdetto fuori dal formato del protocollo: verdetto ambiguo"
        righe.append(m.group(1).upper())
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


ETICHETTE = {"APPROVE": "APPROVATA (check verifica-bot: success)",
             "COMMENT": "NON approvata (check verifica-bot: failure, definitivo su questo SHA)",
             "RIPROVA": "verifica NON conclusa (check verifica-bot: cancelled, si può rilanciare)",
             "OPERATORE": "sì del bot sulla macchina del bot: decide l'operatore"
                          " (check verifica-bot: neutral)"}


def componi_corpo(evento: str, motivo: str, verdetto: dict | None, modello: str,
                  falliti: str) -> str:
    righe = ["## 🤖 Verifica esterna automatica (V-B)", ""]
    righe.append(f"**Esito:** {ETICHETTE.get(evento, 'NON approvata')} — {motivo}")
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
            macchina_bot="true" if tocca_macchina_bot(files) else "false",
            elenco=stato_elenco(files))
    return 0


_SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,99}")


def _conclusioni_precedenti(repo: str, sha: str, slug: str) -> list[str] | None:
    """Conclusioni dei check `verifica-bot` già pubblicati dalla NOSTRA App su `sha`
    (filter=all: anche quelli superati da un rilancio). None = non leggibile."""
    if not _SLUG.fullmatch(slug) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        return None
    try:
        grezzo = _gh("api", "--paginate",
                     f"repos/{repo}/commits/{sha}/check-runs"
                     f"?check_name={NOME_CHECK}&filter=all&per_page=100",
                     "--jq", f'.check_runs[] | select(.app.slug == "{slug}")'
                             ' | (.conclusion // "")')
    except subprocess.CalledProcessError:
        return None
    return [r for r in grezzo.split("\n") if r]


def cmd_esito() -> int:
    repo, pr = os.environ["REPO"], os.environ["PR"]
    head_analizzata = os.environ.get("HEAD_ANALIZZATA", "")
    doc_only = os.environ.get("SOLO_REPORTS") == "true"
    # R-163-1: solo "true"/"false" esatti; tutto il resto = non verificabile (RIPROVA).
    macchina_bot = {"true": True, "false": False}.get(os.environ.get("MACCHINA_BOT", ""))
    elenco = os.environ.get("ELENCO_FILE", "")
    grezzo = os.environ.get("VERDETTO_JSON", "")
    try:
        verdetto = json.loads(grezzo) if grezzo.strip() else None
    except json.JSONDecodeError:
        verdetto = None
    try:
        head_attuale = _gh("api", f"repos/{repo}/pulls/{pr}", "--jq", ".head.sha").strip()
    except subprocess.CalledProcessError:
        head_attuale = ""
    evento, motivo = decidi(verdetto, head_analizzata, head_attuale, doc_only, macchina_bot,
                            elenco)
    if evento in ("APPROVE", "OPERATORE"):
        evento, motivo = con_storico(evento, motivo, _conclusioni_precedenti(
            repo, head_analizzata, os.environ.get("APP_SLUG", "")))
    corpo = componi_corpo(evento, motivo, verdetto, os.environ.get("MODELLO", ""),
                          os.environ.get("MODELLI_FALLITI", ""))
    if not head_analizzata:
        print(f"nessuno SHA analizzato: check non pubblicabile ({motivo})", file=sys.stderr)
        return 1
    # G-1: il check run è il sì/no che il ruleset richiede; va pubblicato PRIMA della
    # review (se la review fallisce, il gate è comunque al suo posto).
    check = {"name": NOME_CHECK, "head_sha": head_analizzata, "status": "completed",
             "conclusion": CONCLUSIONE[evento],
             "output": {"title": ETICHETTE[evento][:200], "summary": corpo}}
    _gh("api", "-X", "POST", f"repos/{repo}/check-runs", "--input", "-",
        input_text=json.dumps(check))
    # La review resta un COMMENTO legato al commit verificato (testo per l'operatore).
    richiesta = {"event": "COMMENT", "body": corpo, "commit_id": head_analizzata}
    _gh("api", "-X", "POST", f"repos/{repo}/pulls/{pr}/reviews", "--input", "-",
        input_text=json.dumps(richiesta))
    print(f"check {NOME_CHECK} {CONCLUSIONE[evento]}: {motivo}")
    return 0


def main(argv: list[str]) -> int:
    comandi = {"smista": cmd_smista, "esito": cmd_esito}
    if len(argv) != 2 or argv[1] not in comandi:
        print("uso: bot_esito.py smista|esito", file=sys.stderr)
        return 2
    return comandi[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
