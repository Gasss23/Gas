# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-06-24 — Infra/Doc: handoff autonomo + gh + ci.yml + riserva openrouter

---

## §0 DECISIONI UMANE RICHIESTE

1. **gh CLI non disponibile** (né su Windows né in WSL2 — WSL2 non ha distribuzioni installate).
   Per attivare §6 CI negli handoff futuri, installare gh:
   - Windows nativo: `winget install GitHub.cli`, poi `gh auth login`
   - Oppure: `wsl --install Ubuntu`, poi `sudo apt install gh`, poi `gh auth login`
   Finché gh è assente, §6 CI riporterà "CI NON VERIFICATA (gh assente)".

---

## §1 SCOPE

**Task unico — 4 fette doc/infra:**
- FETTA 1: verificare gh, installarlo se assente, poi estendere il template handoff.md in fine-task.md con 8 sezioni autonome VERBATIM (§0–§7).
- FETTA 2: verificare .claudeignore e CLAUDE.md §11 (coerenza Sonnet default); applicare se mancante/incoerente.
- FETTA 3: in ci.yml righe ~117-118, allineare la dicitura T9a/T9c da "FAIL attesi" a "SKIP in CI se mancano API key".
- FETTA 4: recuperare dal verdetto revisore CI-4 la riserva su OPENROUTER_API_KEY e tracciarla in stato_progetto.md come R-ci-openrouter.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/commands/fine-task.md | 39 ++++++++++++++++++++++++++-------------
 .github/workflows/ci.yml      |  5 ++---
 reports/roadmap.md            |  7 +++++++
 reports/stato_progetto.md     |  1 +
 4 files changed, 36 insertions(+), 16 deletions(-)
```

(reports/roadmap.md era già modificato prima della sessione — non toccato da questo task)

---

## §3 GIT LOG --ONELINE (sessione)

```
2044749 docs(ci-4): verifica task già completato — T9a/T9c skip confermato da suite locale
3d37208 docs(fine-task+config): fix ordine template handoff + diagnostica FETTA 1 già ok
19d25b2 docs(fine-task+vps): invariante git verbatim + VPS 1GB→4GB + CI-4 chiuso
0fbb59a docs(report): CI-4 skip T9a/T9c — verdetto revisore APPROVATO
089b061 test(ci): skip condizionale T9a/T9c su assenza API key live
732bbb1 docs(config): allinea §11 a Sonnet default + crea .claudeignore
ddc33b5 feat(skill): /fine-task esteso — handoff.md + diff_sessione.md + git log grezzo
31df4d9 docs(config): sfoltimento CLAUDE.md + config frugale Claude Code
3ce2062 docs(token): rinomina archivio_stato.md → stato_storico.md, aggiorna riferimenti
86fcf85 docs(token): split stato_progetto.md + disciplina token in CLAUDE.md
```

(Commit di sessione: il commit di questo report — hash disponibile dopo il push)

---

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

Tutti i file toccati sono doc/infra: `.claude/commands/fine-task.md`, `.github/workflows/ci.yml`, `reports/`.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/brains/modules/tests/. Suite invariata: **158 PASS, 7 FAIL** (7 FAIL ambientali Windows pre-esistenti).

---

## §6 STATO CI

CI NON VERIFICATA (gh assente — né su Windows né WSL2; vedi §0 DECISIONI UMANE RICHIESTE).

Ultima run CI nota: CI-4 risolto (2026-06-24, commit 089b061), job verde su runner Linux (BWRAP_OK confermato).

---

## §7 RISERVE APERTE

- **R-ci-openrouter** (da revisore CI-4, 2026-06-24): T9a è fragile se OPENROUTER_API_KEY è presente — il test la poppava prima del turno T9 ma la tolleranza non è garantita formalmente. Tracciata in stato_progetto.md.
- **gh assente su Windows**: finché non installato, §6 CI negli handoff sarà "CI NON VERIFICATA". Decisione umana richiesta per l'installazione.
