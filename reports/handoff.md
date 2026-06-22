# 🤝 HANDOFF — Dossier di fine sessione

> Dossier autocontenuto per la revisione di fine sessione. **NON sostituisce
> `reports/ultimo_report.md`** (che resta la fonte di verità del singolo task):
> l'handoff lo AGGREGA per la revisione e ci aggiunge lo stato della CI.
> Si riscrive a ogni sessione (la storia completa sta in git).

**Sessione:** 2026-06-23 — Infrastruttura di osservabilità di fine sessione (CI + handoff)

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la PRIMA RUN della CI su GitHub Actions** (verde/rosso + conteggio
   PASS/FAIL/SKIP che produce). Non è verificabile in locale: la prova finale è la run
   su Actions DOPO il push. NON è stato scritto "CI verde" senza averla vista girare.
2. **WSL2 non accessibile** (nessuna distro Linux installata su questa macchina) → la
   prima run CI è l'**unica sonda Linux** disponibile. Apre due sotto-decisioni, da
   prendere SOLO dopo aver visto la prima run:
   - **Come si comportano in CI i 6 test bwrap/namespace** (T11c2, T11e, T12a, T12c,
     T12e, T13d2) **senza bubblewrap installato** sul runner: skippano, falliscono o
     passano? In v1 NON installiamo bwrap di proposito.
   - **Come si comportano i 2 test env API/storia** (T9a, T9c) e **T26b** (WinError32,
     Windows-only → atteso PASS su Linux) sul runner Linux.
3. **SE la prima run è ROSSA per FAIL ambientali che persistono su Linux** (bwrap/env):
   decidere come gestirli è un **TASK SEPARATO** che toccherebbe `tests/` (skip-on-CI
   markers, install bubblewrap nel workflow, ecc.) → richiede revisore. In questa
   sessione **NON è stato toccato il motore né la suite** per "far passare" la CI: lo
   scope lo decide l'umano. La CI come infrastruttura è corretta; se la suite è verde o
   rossa è un fatto separato da osservare.

---

## ESITO SONDA (FASE 0)

1. **`requirements.txt`** esiste. Prima della sessione dichiarava `numpy>=1.26` +
   `fastembed>=0.8` ma **NON `onnxruntime` esplicito** (tirato come transitiva di
   fastembed). In sessione aggiunto `onnxruntime>=1.17` esplicito (floor conservativo,
   la risoluzione reale la fissa fastembed) per evitare che i blocchi vettoriali
   T30/T31/T32 si saltino silenziosamente in CI. Cfr. R-reidx-deps in stato_progetto.
2. **Lancio suite + exit code:** `python tests/test_unit_kernel.py`. Coda del runner:
   `sys.exit(1 if FAIL else 0)` → **exit code nativo ≠0 sui FAIL** (CONFERMATO dal vivo:
   `exit=1` con 9 FAIL presenti). La CI può fidarsi dell'exit code SENZA parsare l'output
   → nessuna modifica a `tests/` necessaria.
3. **Run Linux (WSL2):** NON eseguibile — `wsl` è presente ma **nessuna distribuzione
   Linux è installata**. Ci affidiamo alla prima run CI come unica sonda Linux (vedi
   §DECISIONI UMANE). Predizione NON verificata: i FAIL bwrap su Linux dipendono dalla
   presenza di bubblewrap sul runner (non installato in v1); T26b (WinError32) dovrebbe
   sparire su Linux.
4. **Python del venv del progetto:** **3.11.9** → workflow allineato a `3.11`.

**Suite Windows (venv, PYTHONUTF8=1) in sonda:** 158 PASS / 9 FAIL, **exit=1**. I 9 FAIL
sono i noti ambientali Windows (bwrap T11c2/T11e/T12a/T12c/T12e/T13d2, env API/storia
T9a/T9c, WinError32 backup T26b) — non difetti di codice introdotti qui.

---

## GIT DIFF --STAT (sessione, vs `fdbcabc`)

```
 .github/workflows/ci.yml | 38 ++++++++++++++++++++++++++++++++++++++
 requirements.txt         |  6 ++++++
 2 files changed, 44 insertions(+)
```

> NB: snapshot catturato dopo Commit 1, prima dei commit doc/report di questa fetta
> (handoff.md, CLAUDE.md, stato_progetto.md, ultimo_report.md si aggiungono qui sotto al
> momento del Commit 2/3). La storia git completa resta la fonte autorevole.

## GIT LOG (commit della sessione)

```
0eb5322 ci: workflow GitHub Actions per la suite unit a ogni push (zero token LLM)
```
(+ Commit 2 doc/handoff e Commit 3 report, aggiunti a fine sessione — vedi git log vivo.)

---

## DELTA TEST DEL MOTORE

**0.** La CI è infrastruttura: NON aggiunge né modifica test del kernel
(`tests/test_unit_kernel.py` invariato). Dichiarato onestamente, non gonfiato.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Le modifiche toccano solo file di
infrastruttura/documentazione (`.github/workflows/ci.yml`, `requirements.txt`,
`reports/*.md`, `CLAUDE.md`). Il gate di review (CLAUDE.md §3) scatta solo sui diff che
toccano `gas.py`/`brains/`/`modules/`/`tests/`: nessuno di questi è stato toccato.

## STATO CI

**Prima run da verificare su GitHub Actions.** Il numero oggettivo (PASS/FAIL/SKIP e
verde/rosso) lo riempie la run, non l'agente. Vedi §DECISIONI UMANE #1.
