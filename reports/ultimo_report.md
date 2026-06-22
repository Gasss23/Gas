# CI — abilitazione del sandbox OS (bubblewrap) nel runner

**Data:** 2026-06-23
**Task:** SOLO-WORKFLOW. Mettere il runner GitHub Actions in condizione di ESERCITARE il
sandbox OS (bwrap), così i 5 test bwrap-FAIL si chiudono e i 4 test del profilo sandbox
(oggi [SKIP]) si accendono → prima verifica CONTINUA del sandbox OS (meccanismo che rende
sicuro l'h24 sul VPS).
**Tipo:** infrastruttura CI (`.github/workflows/`) NON-motore. **Revisore:** non applicabile
(nessun diff su `gas.py`/`brains/`/`modules/`/`tests/`).

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la run post-push su GitHub Actions** (https://github.com/Gasss23/Gas/actions),
   leggendo nel log:
   - **lo smoke-test bwrap**: `BWRAP_OK` o `BWRAP_FAIL` (sia smoke-test 1 post-install, sia
     smoke-test 2 post-sysctl) — è il risultato della sonda runtime sui namespace;
   - **i 5 test bwrap** (T11c2, T11e, T12a, T12c, T12e) col sandbox attivo → attesi PASS;
   - **i 4 test T13** (T13a rete-isolata, T13b fs-read-only, T13c segreto-mascherato,
     T13e comando-in-bwrap) → attesi GIRARE (non più [SKIP]) e PASS;
   - **conteggio PASS/FAIL/SKIP finale**.
2. **STOP GATE — se lo smoke-test resta `BWRAP_FAIL` anche dopo il sysctl** (GitHub nega del
   tutto gli unprivileged userns): `os_strict` NON è esercitabile sul runner. In tal caso la
   CI resta ROSSA sui 5 bwrap-FAIL e va aperto il **micro-task 2** (skip-on-CI dei test
   bwrap, che tocca `tests/` → CON REVISORE). NON ho skippato test né committato workaround
   su `tests/` da solo.
3. **Restano fuori scope T9a/T9c** (env API / storia su root temp): toccano `tests/` →
   micro-task 2, NON trattati qui.

---

## ESITO SONDA (FASE 0, sola lettura)

Letto `tests/test_unit_kernel.py`. Determinato COME ogni test ottiene lo stato del sandbox:

1. **T13a/b/c/e (oggi SKIP):** gated da `OS_SB = gas._probe_os_sandbox()[0]` (riga 380); ogni
   test è dentro `if OS_SB: ... else: skip(...)` (righe 391/401/416/452). Reagiscono alla
   disponibilità **REALE** del sandbox → con bwrap installato e namespace concessi GIREREBBERO.
   **Confermato sì.**
2. **T11c2/T11e/T12a/T12c/T12e (oggi FAIL):** dipendono dall'ESECUZIONE di `run_command`. Oggi,
   su runner senza bwrap + `os_strict`, `run_command` è negato fail-closed → i test che si
   aspettano output/effetto falliscono. Con sandbox presente `run_command` esegue → tornano
   PASS. Caso particolare **T11c2** (riga 248): forza il fallimento dello snapshot usando una
   dir **non-git** (`k_nogit`) con comando lecito `ls -la`; il check sandbox è ortogonale —
   oggi corto-circuita PRIMA con un diniego "sandbox OS"; col sandbox presente il flusso
   prosegue fino allo snapshot che fallisce come da disegno → messaggio "snapshot" atteso → PASS.
3. **PIVOT — T13d/T13d2 (oggi PASS):** **FORZANO l'assenza in modo deterministico** —
   `k_strict.os_sandbox_available = False` (riga 434) e `k_fb.os_sandbox_available = False`
   (riga 443) sull'ISTANZA, NON leggono `_probe_os_sandbox()`. Il commento del test lo dichiara:
   *"deterministico, NON richiede bwrap: si forza os_sandbox_available=False"*. → Installare
   bwrap **NON li flippa** PASS→FAIL.

**DECISIONE:** T13d/T13d2 forzano l'assenza (deterministici) e T13a-e + i 5 bwrap-FAIL
reagiscono alla presenza reale; nessun test attualmente-PASS dipende dall'assenza reale del
sandbox. → Installare bwrap nel workflow è **PULITO e SOLO-WORKFLOW** → VIA LIBERA per FETTA 1.

---

## COSA È STATO FATTO — FETTA 1 (Commit `919f677`)

`.github/workflows/ci.yml`, nuovo step **prima** della suite ("Enable OS sandbox (bubblewrap)"):
1. `sudo apt-get update && sudo apt-get install -y bubblewrap`.
2. **Smoke-test 1** esplicito (output nel log): `bwrap --unshare-all --ro-bind / / /bin/true
   && echo BWRAP_OK || echo BWRAP_FAIL`.
3. **Rilassamento unprivileged userns** (ubuntu-24.04 li restringe via AppArmor), guardato
   sull'esistenza delle chiavi: `kernel.apparmor_restrict_unprivileged_userns=0` e
   `kernel.unprivileged_userns_clone=1` (best-effort, `|| true`). Benigno sul runner
   EFFIMERO della CI; **NON tocca `os_strict` del VPS** (lì il sandbox resta fail-closed).
4. **Smoke-test 2** post-sysctl (output nel log).
5. Step suite **INVARIATO** (`PYTHONUTF8=1`, `python tests/test_unit_kernel.py`), ora DOPO lo
   step sandbox.

ZERO token LLM: nessun provider, nessun secrets, nessuna API key. Nessun altro cambiamento.

---

## DELTA TEST DEL MOTORE

**0.** `tests/` e `gas.py` INVARIATI. La sonda ha confermato che non serve toccarli (il pivot
T13d/T13d2 è deterministico) → nessuno STOP GATE attivato.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Diff solo su `.github/workflows/ci.yml` (+ report).

## STATO CI

**Prima run COL SANDBOX da verificare su GitHub Actions** (vedi §DECISIONI UMANE #1). La
prova è la run post-push: smoke-test BWRAP_OK/FAIL + conteggio PASS/FAIL/SKIP. NON scrivo
"CI verde" senza averla vista girare.

## RISERVE / NOTE
- **CI-3 (NUOVA):** la chiusura dei 5 bwrap-FAIL dipende dal fatto che il runner GitHub
  conceda gli unprivileged userns dopo il sysctl. Se `BWRAP_FAIL` persiste → micro-task 2
  (skip-on-CI, tocca `tests/`, con revisore). Non forzato qui.
- **CI-1/CI-2** (sessione precedente) superate da questo step: bwrap ora è installato e
  abilitato di proposito.
