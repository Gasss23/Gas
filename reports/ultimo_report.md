# Ultimo report — sessione revisione-fondamenta (2026-07-15)

Branch: `chore/fondamenta-registro-pulizia`

## Scope

Registrazione dei finding dell'audit Fable-5 (SHA 9cbab56) + pulizia 17 file morti.

## Esito fette

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| 1 — DOC-ONLY | Inserimento blocco revisione fondamenta in roadmap.md + 5 modifiche a stato_progetto.md | FATTA |
| 2 — PULIZIA FILE MORTI | 17 git rm + router.py ridotto + .venv/ in .gitignore + 2 righe CLAUDE.md sez.2 | FATTA |

## Commit della sessione

```
bdec279  docs: registra revisione fondamenta Fable-5 (F1 provato, F6/F7 nuovi, F2-F5) + chiude item allineamento locale
1b03adc  chore: rimuove 17 file morti (brain legacy, self_improve, marketing husk, junk root); router.py ridotto a classifica_compito; .venv/ gitignorato [revisione Fable-5, F3+F7]
```

## diff --stat reale della sessione (HEAD~2..HEAD)

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

## Delta test suite

- PRE-modifica: **231 PASS, 0 FAIL** (suite completa)
- POST-modifica: **231 PASS, 0 FAIL** (delta zero)

## Verifiche Fetta 2

- Residui grep (groq_brain/gemini_brain/openrouter_brain/claude_brain/self_improve/test_agente): **VUOTO** ✅
- `classifica_compito('ciao')` → **semplice** ✅
- `.venv/` gitignore: `.gitignore:2:.venv/ .venv/x` ✅

## Verdetto revisore (Fetta 2 — integrale)

```
## VERDETTO: APPROVATO

La fetta è chirurgica e priva di rischi. Rimuove esclusivamente codice morto confermato,
risolve un finding latente (R-legacy-slice su claude_brain.py) per via radicale,
corregge il gitignore (F7) e allinea CLAUDE.md alla realtà del codebase.
Delta suite: zero. Nessun guardrail indebolito. Nessun antipattern introdotto.

Verifiche revisore:
- 17 file rimossi: tutti confermati non wired (gas.py importa solo brains.model_ids
  e brains.router.classifica_compito)
- brains/router.py: preserva esattamente classifica_compito, import os legacy rimosso
- .gitignore: additivo, nessun effetto collaterale
- CLAUDE.md sez.2: tutte le affermazioni verificate accurate rispetto al codice
- Nessun effetto collaterale inatteso rilevato
```

## Stato CI

PR non ancora aperta al momento della scrittura. CI run atteso su push + PR creation.
Ultima CI su main: run #29031945029 su `87ad26f` ✅ SUCCESS (2026-07-09).

## Finding registrati in questa sessione

- 🔴 **F1 = R-crm-diario-rr** → PROSSIMA FETTA MOTORE (1 riga `_connect()` + test)
- 🟡 **F6 — atomicità .gas_history.json** → fetta piccola dopo F1
- 🟡 **F2 — budget kill-switch** → GATED (primo rung runtime a pagamento)
- ✅ **F3 — pulizia file morti** → ESEGUITA in questa PR
- 🟢 **F4 — messaggi sed -n** → cosmetico, fetta futura
- 🟢 **F5 — single-history Telegram** → vincolo di design
- 🟡 **F7 — .venv/ gitignore** → fix eseguito; residuo: verificare naming venv su VPS (runbook SSH)
- ✅ **R-legacy-slice** → CHIUSO (rimosso con claude_brain.py)
