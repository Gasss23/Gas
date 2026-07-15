# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-15 — revisione fondamenta Fable-5: audit integrale + pulizia 17 file morti

---

## § DECISIONI UMANE RICHIESTE

1. **Merge PR** `chore/fondamenta-registro-pulizia` → main: revisiona diff (22 file, 694 delete, 27 insert) e approva il merge se soddisfatto. CI deve essere verde prima del merge.
2. **Residuo F7 — venv su VPS**: verificare via SSH il naming del venv di produzione (`ls -a /home/gas/gas/`) per sapere se il buco snapshot era vivo in h24 sul VPS. Se è `.venv` → era un problema attivo; se è `venv` → era già coperto. Runbook SSH, non task Claude Code.
3. **Prossima fetta motore (F1)**: confermare priorità relativa di `R-crm-diario-rr` (1 riga `_connect()` + test) vs altri task in coda (R-crm-1b fette 2-3, FASE 3 vocale).

---

## Sonda

Nessuna sonda live eseguita in questa sessione (sessione doc+pulizia). Suite: 231 PASS, 0 FAIL pre e post.

---

## git diff --stat reale della sessione (HEAD~2..HEAD)

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
 reports/roadmap.md                    |  13 ++++
 reports/stato_progetto.md             |   9 ++-
 router                                |   4 --
 self_improve/__init__.py              |   0
 self_improve/loop.py                  |  93 -------------------------
 self_improve/researcher.py            |  85 -----------------------
 test_agente.py                        |  16 -----
 22 files changed, 27 insertions(+), 694 deletions(-)
```

---

## git log commit della sessione

```
1b03adc  chore: rimuove 17 file morti (brain legacy, self_improve, marketing husk, junk root); router.py ridotto a classifica_compito; .venv/ gitignorato [revisione Fable-5, F3+F7]
bdec279  docs: registra revisione fondamenta Fable-5 (F1 provato, F6/F7 nuovi, F2-F5) + chiude item allineamento locale
```

---

## Delta test suite

| Momento | PASS | FAIL |
|---------|------|------|
| PRE-Fetta 2 | 231 | 0 |
| POST-Fetta 2 | 231 | 0 |

Delta zero ✅

---

## Verdetto revisore INTEGRALE (Fetta 2)

```
## REVIEW PRE-COMMIT — Fetta 2 "pulizia file morti" (2026-07-15)

Verifica 1 — I 17 file rimossi sono davvero non wired: CONFERMATO.
  gas.py importa solo brains.model_ids e brains.router.classifica_compito.

Verifica 2 — brains/router.py ridotto: CORRETTO.
  Preserva esattamente classifica_compito. import os legacy rimosso correttamente.
  Default mutable (memoria=[]) rimosso con le funzioni legacy.

Verifica 3 — .gitignore: CORRETTO.
  .venv/ posizionata sotto venv/, additiva, nessun effetto collaterale.

Verifica 4 — CLAUDE.md sez.2: ACCURATO.
  Cascata, brains/model_ids.py, Claude non rung runtime, modules/memory/ e /telegram/
  tutti confermati rispetto al codice reale.

Verifica 5 — Effetti collaterali inattesi: Nessuno rilevato.
  Guardrail intatti. R-legacy-slice (messages[-8:]) chiuso alla radice.

## VERDETTO: APPROVATO

La fetta è chirurgica e priva di rischi. Rimuove esclusivamente codice morto confermato,
risolve un finding latente (R-legacy-slice su claude_brain.py) per via radicale,
corregge il gitignore (F7) e allinea CLAUDE.md alla realtà del codebase.
Delta suite: zero. Nessun guardrail indebolito. Nessun antipattern introdotto.
```

---

## Stato CI (FETTA 1 — .github/workflows/ci.yml)

- Ultima run su main: #29031945029 su `87ad26f` ✅ SUCCESS (2026-07-09)
- Run su questa PR: attesa dopo push. La PR non è ancora aperta al momento della scrittura di questo handoff.
- CI check `unit-suite` required per merge (ruleset `main-lock`).
