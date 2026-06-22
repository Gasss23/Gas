# Infrastruttura di osservabilità di fine sessione — CI + handoff

**Data:** 2026-06-23
**Task:** costruire l'infrastruttura di osservabilità di fine sessione in due fette —
FETTA 1 CI (workflow GitHub Actions che gira la suite a ogni push, verde/rosso oggettivo);
FETTA 2 HANDOFF (`reports/handoff.md` + istituzionalizzazione chirurgica in CLAUDE.md/stato).
**Tipo:** infrastruttura/doc NON-motore. **Revisore:** non applicabile (nessun diff su
`gas.py`/`brains/`/`modules/`/`tests/`). **Scope BLOCCATO rispettato:** nessun tocco al motore,
nessun tocco a R26-1/R26-2.

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la PRIMA RUN della CI su GitHub Actions** (verde/rosso + conteggio
   PASS/FAIL/SKIP). Non è verificabile in locale: la prova finale è la run su Actions DOPO
   il push. NON ho scritto "CI verde" senza averla vista girare.
2. **WSL2 NON accessibile** (`wsl` presente ma nessuna distribuzione Linux installata) → la
   prima run CI è l'**unica sonda Linux**. Da decidere DOPO averla vista:
   - comportamento in CI dei 6 test bwrap/namespace (T11c2, T11e, T12a, T12c, T12e, T13d2)
     **senza bubblewrap** sul runner (non installato in v1): skip / fail / pass?
   - comportamento dei 2 test env API/storia (T9a, T9c) e di T26b (WinError32, Windows-only,
     atteso PASS su Linux) sul runner Linux.
3. **SE la prima run è ROSSA per FAIL ambientali che persistono su Linux:** gestirli è un
   **TASK SEPARATO** che toccherebbe `tests/` (skip-on-CI, install bubblewrap, ecc.) →
   richiede revisore. In questa sessione **NON ho toccato motore né suite** per far passare
   la CI: lo scope lo decide l'umano. La CI come infrastruttura è corretta a prescindere dal
   fatto che la suite risulti verde o rossa.

---

## ESITO SONDA (FASE 0)

1. **`requirements.txt`** esiste. Dichiarava `numpy>=1.26` + `fastembed>=0.8`, **NON
   `onnxruntime` esplicito** (transitiva di fastembed). → Aggiunto `onnxruntime>=1.17`
   esplicito (floor conservativo) per non far saltare i blocchi vettoriali T30/T31/T32 in CI
   (R-reidx-deps). Completare requirements era IN SCOPE (presupposto di una CI utile, file
   non-motore).
2. **Lancio suite + exit code:** `python tests/test_unit_kernel.py`; coda del runner
   `sys.exit(1 if FAIL else 0)`. **VERIFICATO dal vivo: `exit=1` con 9 FAIL.** → exit code
   nativo ≠0 sui FAIL: la CI si fida dell'exit code senza parsare l'output, **nessuna
   modifica a `tests/`**.
3. **Run Linux (WSL2):** NON eseguibile (nessuna distro Linux installata). Ci affidiamo alla
   prima run CI come unica sonda Linux.
4. **Python del venv:** **3.11.9** → workflow su `3.11`.

Suite Windows in sonda (PYTHONUTF8=1): **158 PASS / 9 FAIL, exit=1**. I 9 FAIL sono i noti
ambientali Windows (bwrap T11c2/T11e/T12a/T12c/T12e/T13d2, env API/storia T9a/T9c, WinError32
T26b), non difetti introdotti qui.

**La sonda NON ha rivelato necessità di toccare `tests/`/`gas.py`:** l'exit code nativo basta
→ nessuno STOP GATE attivato sulla CI.

---

## COSA È STATO FATTO

### FETTA 1 — CI (Commit `0eb5322`)
- **`.github/workflows/ci.yml`** (NUOVO): `on: push`, runner `ubuntu-latest`,
  `actions/setup-python@v5` a `3.11` con `cache: pip`, `pip install -r requirements.txt`,
  `python tests/test_unit_kernel.py`. Il job è ROSSO se la suite fallisce via exit code
  nativo del runner. **ZERO token LLM:** nessun `env:` di provider, nessun blocco `secrets:`,
  nessun `gas doctor`. `PYTHONUTF8=1` per parità con l'esecuzione del progetto. bubblewrap NON
  installato in v1 (di proposito).
- **`requirements.txt`:** aggiunto `onnxruntime>=1.17` esplicito con commento (vedi sonda).

### FETTA 2 — HANDOFF (Commit `d135bc7`)
- **`reports/handoff.md`** (NUOVO, istituzione D): dossier autocontenuto compilato su QUESTA
  sessione (primo esempio reale). Ordine: §DECISIONI UMANE in cima, esito sonda,
  `git diff --stat` reale, `git log` dei commit, delta test motore (0), verdetto revisore
  (non applicabile), stato CI (prima run da verificare). AGGREGA `ultimo_report.md`, NON lo
  sostituisce.
- **CLAUDE.md §3:** aggiunta l'istituzione **D** (handoff.md) + aggiornato "tre"→"quattro"
  istituzioni di processo.
- **`reports/stato_progetto.md`:** riga "D — reports/handoff.md" nelle Istituzioni di processo
  + entry datata 2026-06-23 in testa (questo commit finale dei report).

---

## DELTA TEST DEL MOTORE

**0.** La CI è infrastruttura: NON aggiunge né modifica test del kernel. `tests/` INVARIATO.
Dichiarato onestamente, non gonfiato.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Diff solo su `.github/workflows/ci.yml`,
`requirements.txt`, `reports/*.md`, `CLAUDE.md`. Il gate di review (CLAUDE.md §3) scatta solo
sui diff che toccano `gas.py`/`brains/`/`modules/`/`tests/`.

## STATO CI

**Prima run da verificare su GitHub Actions** (vedi §DECISIONI UMANE #1). Il numero oggettivo
lo riempie la run, non l'agente.

---

## RISERVE / NOTE NUOVE
- **CI-1:** la suite ha 9 FAIL ambientali noti su Windows; quali persistano su Linux è ignoto
  finché non gira la prima CI (WSL2 non accessibile). Se persistono, la CI resterà ROSSA finché
  non si decide come gestirli (TASK SEPARATO su `tests/`, con revisore). La CI è corretta come
  infrastruttura; la verde/rosso è un fatto da osservare, non da forzare.
- **CI-2:** v1 NON installa bubblewrap nel runner: scelta deliberata per OSSERVARE il
  comportamento reale dei test OS-specifici in CI prima di decidere a priori.
