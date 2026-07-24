# Report — 2026-07-24 (p2): blocchi git rigenerati, registrazioni, sanare F7

**Data:** 2026-07-24  
**Branch:** docs/fine-task-git-blocks  
**Revisore:** NON invocato — sessione doc-only, nessun file di motore nel diff (gas.py, brains/, modules/, tests/ assenti dal diff).

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## Esito per fetta

- **FETTA A — .claude/commands/fine-task.md: blocchi git rigenerati per ultimi**: FATTA
  - A1: §0 rinominato "Calcola BASE"; intro aggiornata; blocchi §2/§3/§6 rimossi da §0.
  - A2: nuovo step "4bis — RIGENERA I BLOCCHI GIT" con `git diff --cached --stat ${BASE}`, `git log`, `gh run list`; spiegazione `--cached` vs `${BASE}..HEAD`; update handoff poi commit.
  - A3: NB obbligatorio in §3 del template handoff (commit fine-task non compare nel log per costruzione).
  - A4: regola §6 — commit senza run CI: scrivere "run non ancora disponibile alla scrittura dell'handoff"; vietato omettere o attribuire run di commit precedente.
  - A5: GATE POST-FINE-TASK in maiuscolo a fine file — rieseguire /fine-task se si committa dopo.

- **FETTA B — reports/stato_progetto.md: registrazioni 2026-07-24**: FATTA
  - B1: recidiva handoff §2/§3/§6 non rigenerati (PR #43) — numeri misurati, causa strutturale distinta dal micro-finding 2026-07-13.
  - B2: PR #43 mergiata da browser invece di gasmerge — gate aggirato per canale, nessun danno.
  - B3: ~/bin/gasmerge non era symlink — risolto con ln -sfn; azione senza traccia in git.
  - B4: deviazione gate PR #43 review #60/#61 da general-purpose.
  - B5: R-gasmerge-failopen punto (6) — nit messaggio d'uso parametro posizionale.
  - B6: riga CI di testa aggiornata (PR #43 b3379b7 CI 30099181638 ✅); head origin = 5.

- **FETTA C — reports/stato_progetto.md: sanare contraddizione F7**: FATTA
  - C1: righe 2026-07-21 (🔴 F7 CONFERMATO APERTO, 🟡 F7 APERTA e FATTIBILE) marcate ℹ️ SUPERATE — storia mantenuta, prefisso aggiunto.
  - C2: riserva di evidenza sotto ✅ F7 CHIUSO; stessa verifica come 🟡 nella coda DEPLOY VPS.
  - C3: 🟡 Copia VPS stantia vs origin/main NON toccata — finding separato, resta aperto.

---

## Diff reale per file

- `.claude/commands/fine-task.md` — 41 inserzioni, 12 delezioni (FETTA A: step 4bis, regole §3/§6, gate)
- `reports/stato_progetto.md` — 22 inserzioni, 4 delezioni (FETTE B e C: nuova sezione p2, F7 sanato, coda VPS)

---

## Dichiarazione

Revisore NON invocato — sessione doc-only, nessun file di motore nel diff.
