# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-19 — Regola in CLAUDE.md: documenti di progetto, fonte unica = il repo (PR #219)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #219 (https://github.com/Gasss23/Gas/pull/219): tocca `CLAUDE.md`, l'agente la mergia solo con APPROVATO pulito del bot.
2. Testo di `claude/roadmap_completa.md` (sta solo nel progetto claude.ai, invisibile all'agente): incollarlo per l'aggiornamento della roadmap con le decisioni del 19 ott.
3. Collegare il repo GitHub al progetto Gas su claude.ai (`reports/`, `CLAUDE.md`).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Regola «documenti di progetto: fonte unica = il repo» in CLAUDE.md**: `FATTA` — PR #219.
- **Aggiornamento della roadmap con le decisioni del 19 ott**: `BLOCCATA` — il file sorgente sta solo nel progetto claude.ai (nessuno strumento per leggerlo da questa sessione).
- **Regola delle risposte brevi**: già presente in CLAUDE.md (§3, punto 4), non duplicata.

---

## §2 GIT DIFF --STAT (sessione)

```
 CLAUDE.md                |  1 +
 reports/diff_sessione.md |  6 +++---
 reports/handoff.md       | 23 +++++++++++------------
 reports/ultimo_report.md | 18 ++++++++----------
 4 files changed, 23 insertions(+), 25 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
cb0a937 docs(CLAUDE.md): documenti di progetto, fonte unica = il repo (decisione operatore 2026-10-19)
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit motore: solo `CLAUDE.md` e `reports/` (fuori dal perimetro di review).

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica al motore: delta zero. Ultimo dato su main `e4edf7d`: kernel 895 PASS in CI, pytest `tests/` 1450 passed.

## §6 STATO CI

- PR #219 (`cb0a937`): run in corso all'apertura; il commit di questo handoff la fa ripartire.

## §7 RISERVE APERTE

- Invariate rispetto alla #217: R-bot217-1, R-bot217-2, R-ve217-1 (BASSE), dettaglio in `reports/stato_progetto.md`.
