# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-15 — revisione fondamenta Fable-5: audit integrale + pulizia 17 file morti

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge PR #17** (`chore/fondamenta-registro-pulizia` → main): CI verde ✅ — revisiona diff e approva il merge se soddisfatto.
2. **Residuo F7 — venv su VPS**: verificare via SSH il naming del venv di produzione (`ls -a /home/gas/gas/`) — se è `.venv` il buco snapshot era vivo in h24; se è `venv` era già coperto. Runbook SSH, non task Claude Code.
3. **Priorità prossima fetta motore (F1)**: confermare se procedere con `R-crm-diario-rr` (1 riga `_connect()` + test) oppure un'altra fetta (R-crm-1b fette 2-3, FASE 3 vocale).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — DOC-ONLY (reports/roadmap.md + reports/stato_progetto.md)**: `FATTA`
  Inserito blocco "REVISIONE FONDAMENTA Fable-5" in roadmap.md; 5 modifiche a testo esatto in stato_progetto.md (header, F6 in Finding aperti, R-crm-diario-rr promosso a fetta, note minori Fable-5, item locale/clone Windows chiusi).
  Il revisore NON è stato invocato per questa fetta: modifica esclusiva di reports/*.md, doc-only, nessun codice motore.

- **Fetta 2 — PULIZIA FILE MORTI (brains/ + modules/ + root + .gitignore + CLAUDE.md)**: `FATTA`
  17 file rimossi con git rm; brains/router.py ridotto al solo classifica_compito; riga .venv/ aggiunta a .gitignore; 2 righe CLAUDE.md sez.2 aggiornate. Gate revisore invocato e APPROVATO prima del commit.

---

## §2 GIT DIFF --STAT (sessione)

```
 .gitignore                            |   1 +
 CLAUDE.md                             |   4 +-
 brains/claude_brain.py                | 125 ----------------------------------
 brains/gemini_brain.py                |  78 ---------------------
 brains/groq_brain.py                  |  52 --------------
 brains/openrouter_brain.py            |  73 --------------------
 brains/router.py                      |  53 ++------------
 deploy_vps_bozza.txt                  |  82 ----------------------
 gas                                   |  11 ---
 modules/marketing/campaign.py         |   1 -
 modules/marketing/funnel_test.py      |   1 -
 modules/marketing/riassunto_canone.md |   5 --
 modules/marketing/strategy.txt        |   1 -
 modules/marketing/test_finale.py      |  13 ----
 modules/marketing/test_postcleanup.py |   1 -
 reports/diff_sessione.md              |  30 ++++++--
 reports/handoff.md                    | 102 ++++++++++++++++++---------
 reports/roadmap.md                    |  13 ++++
 reports/stato_progetto.md             |  11 +--
 reports/ultimo_report.md              |  98 +++++++++++++++++++++-----
 router                                |   4 --
 self_improve/__init__.py              |   0
 self_improve/loop.py                  |  93 -------------------------
 self_improve/researcher.py            |  85 -----------------------
 test_agente.py                        |  16 -----
 25 files changed, 200 insertions(+), 753 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
942c5c8 docs(report): fine sessione revisione-fondamenta — ultimo_report, handoff, diff_sessione, stato_progetto (chiude R-legacy-slice)
1b03adc chore: rimuove 17 file morti (brain legacy, self_improve, marketing husk, junk root); router.py ridotto a classifica_compito; .venv/ gitignorato [revisione Fable-5, F3+F7]
bdec279 docs: registra revisione fondamenta Fable-5 (F1 provato, F6/F7 nuovi, F2-F5) + chiude item allineamento locale
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit motore: `1b03adc` (tocca brains/ e modules/).

Verdetto integrale del revisore (invocato prima del commit `1b03adc`):

```
## REVIEW PRE-COMMIT — Fetta 2 "pulizia file morti" (2026-07-15)

### Verifica 1 — I 17 file rimossi sono davvero non wired

CONFERMATO. Il grep su gas.py e tests/ non produce alcun residuo di import verso i
file rimossi. Gli unici due simboli importati da brains/ nel kernel attivo sono:
- from brains.model_ids import (...) — riga 14 di gas.py, file intatto
- from brains.router import classifica_compito — riga 1398 di gas.py, import lazy,
  file ridotto correttamente

### Verifica 2 — brains/router.py ridotto

CORRETTO. Il file preserva esattamente e soltanto KEYWORDS_COMPLESSO e
classifica_compito — l'unico simbolo usato dal kernel. L'import os legacy (non usato
dalla funzione preservata) è stato rimosso correttamente. Il tipo di ritorno str è
presente nel type hint.
Nota positiva: le funzioni get_brain/_chiama/rispondi rimosse contenevano importazioni
lazy dei brain legacy e un default mutable (memoria=[]) — anti-pattern Python classico.
Rimozione giusta.

### Verifica 3 — .gitignore

CORRETTO. La riga .venv/ è posizionata immediatamente sotto venv/, coprendo entrambe
le convenzioni di naming del virtualenv. Risolve F7. Nessun effetto collaterale: la
riga è additiva e non altera alcuna regola esistente.

### Verifica 4 — CLAUDE.md sez.2

ACCURATO. Confronto con la realtà del codice:
- Cascata Gemini→Groq→OpenRouter free→Ollama: confermata da stato_progetto.md
- fonte unica ID brains/model_ids.py: confermata (review #43)
- Claude NON è un rung runtime: confermato (gas.py non importa anthropic nel loop)
- modules/memory/ (Memoria): attivo, confermato
- modules/telegram/ (Bridge): attivo, confermato
- Funnel marketing FASE 4: confermato (directory rimossa perché husk non wired)

### Verifica 5 — Effetti collaterali inattesi

Nessuno rilevato. Guardrail intatti: cap 10 iterazioni, _get_window(),
_cap_window_chars, memoria SQLite — nessuno dei file rimossi li toccava.
Wall of Shame §5: brains/claude_brain.py conteneva messages[-8:] (R-legacy-slice).
La rimozione lo chiude alla radice. Nessun slicing raw residuo.

Nota minore (non bloccante): stato_progetto.md conservava la voce R-legacy-slice
sotto "Debito latente" — marcata chiusa nell'aggiornamento di fine sessione.

## VERDETTO: APPROVATO

La fetta è chirurgica e priva di rischi. Rimuove esclusivamente codice morto
confermato, risolve un finding latente (R-legacy-slice su claude_brain.py) per via
radicale, corregge il gitignore (F7) e allinea CLAUDE.md alla realtà del codebase.
Delta suite: zero. Nessun guardrail indebolito. Nessun antipattern introdotto.
```

---

## §5 DELTA TEST DEL MOTORE

Suite `tests/test_unit_kernel.py`:

```
=== RIEPILOGO: 231 PASS, 0 FAIL ===   ← PRE-Fetta 2
=== RIEPILOGO: 231 PASS, 0 FAIL ===   ← POST-Fetta 2
```

Delta zero. Nessun nuovo test aggiunto in questa sessione (fetta doc+pulizia).

---

## §6 STATO CI

```
completed	success	docs(report): fine sessione revisione-fondamenta — ultimo_report, han…	CI	chore/fondamenta-registro-pulizia	push	29452996720	43s	2026-07-15T21:44:25Z
completed	success	Merge pull request #16 from Gasss23/chore/stato-microfinding-pr14	CI	main	push	29402943465	36s	2026-07-15T09:01:36Z
completed	success	docs(handoff): fine sessione stato-microfinding-pr14	CI	chore/stato-microfinding-pr14	push	29402791860	37s	2026-07-15T08:59:19Z
```

Run sul branch di sessione: **29452996720** — `completed SUCCESS` su `chore/fondamenta-registro-pulizia` (2026-07-15T21:44:25Z, 43s).

---

## §7 RISERVE APERTE

Da questa sessione (nuove):
- 🔴 **F1 = R-crm-diario-rr → PROSSIMA FETTA MOTORE**: `INSERT OR REPLACE` sulla PK del diario aggira i trigger di immutabilità con `recursive_triggers` OFF (dimostrato su DB di test). Fix: `PRAGMA recursive_triggers=ON` in `MemoryStore._connect()` (1 riga) + test ABORT su INSERT OR REPLACE.
- 🟡 **F6 — atomicità .gas_history.json**: `_save_history` non atomico (niente tmp+rename), `_load_history` ingoia corruzione silenziosamente. Fix pianificato dopo F1.
- 🟡 **F7 — residuo VPS**: fix .gitignore eseguito; naming venv su VPS da verificare via SSH.
- 🟡 **F2 — budget kill-switch**: check solo a inizio run_turn; inerte sul free tier. Gated al primo rung a pagamento.

Chiuse in questa sessione:
- ✅ **R-legacy-slice**: rimosso con claude_brain.py (messages[-8:] eliminato alla radice).
- ✅ **F3 — pulizia file morti**: 17 file rimossi.

PR: https://github.com/Gasss23/Gas/pull/17
