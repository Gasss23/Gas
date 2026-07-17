# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-17 — docs/sanitize-post-pr21: F0 verifica merge + F1-bis sonda CI + F2-bis stato_progetto
**Branch:** docs/sanitize-post-pr21
**BASE (merge-base origin/main):** 8f9cf7bddbd7d584b4a588558cdd52acd9b31a34

---

## §0 DECISIONI UMANE RICHIESTE

1. **R-ci-hooks — task separato (fuori scope questa sessione)**: `tests/test_unit_hooks.py` (T-hook-a/b/c/d/e/f/g) non è eseguito da CI. Decidere se aggiungere `python tests/test_unit_hooks.py` al job `unit-suite` in `ci.yml`. Tocca `ci.yml` → task separato, non committato qui.
2. **Merge PR docs/sanitize-post-pr21 → main** — solo doc/report, CI run 29570876259 ✅ SUCCESS, self-merge consentito.

---

## §1 SCOPE & ESITO FETTE

- **F0 — Verifica hash merge (PR #21 e PR #19)**: `FATTA` — hash confermati dall'operatore. PR #21 → `8f9cf7b`, PR #19 → `9a9278e`. Output verbatim di `git log origin/main --merges --oneline -5` nel report iniziale.
- **F1-bis — Sonda CI unit-suite (SOLA LETTURA)**: `FATTA` — vedi §F1-bis sotto. Gap scoperto: `tests/test_unit_hooks.py` non eseguito da CI.
- **F2-bis — Completamento reports/stato_progetto.md**: `FATTA` — 5 punti: (a)(b) da fetta precedente; (c) blocco discrepanza contatore rimosso; (d) finding R-ci-hooks aggiunto; (e) header aggiornato.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  57 +++------
 reports/handoff.md        | 156 ++++++------------------
 reports/stato_progetto.md |  13 +-
 reports/ultimo_report.md  | 296 +++++++++++++++++++++++++++++-----------------
 4 files changed, 248 insertions(+), 274 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
8301cb7 docs(fine-task): F1-bis sonda CI + F2-bis stato_progetto — sanitize-post-pr21
407ef9f docs(fine-task): ultimo_report + handoff + diff_sessione — sanitize-post-pr21
e6447af docs(sanitize-post-pr21): stato_progetto + ultimo_report post-merge PR #21 e PR #19
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Il revisore NON è stato invocato. Motivo: nessun commit di questa sessione tocca `gas.py`, `brains/`, `modules/`, o `tests/`. La sessione è doc-only (reports/) + sonda read-only (F1-bis legge ci.yml e tests/ senza modificare nulla). Il gate di review si attiva solo su diff motore.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py` o `tests/` in questa sessione.

---

## §6 STATO CI

Output di `gh run list -L 3`:

```
completed	success	docs(fine-task): F1-bis sonda CI + F2-bis stato_progetto — sanitize-p…	CI	docs/sanitize-post-pr21	push	29570876259	40s	2026-07-17T09:41:36Z
completed	success	docs(fine-task): ultimo_report + handoff + diff_sessione — sanitize-p…	CI	docs/sanitize-post-pr21	push	29569357111	35s	2026-07-17T09:16:12Z
completed	success	docs(sanitize-post-pr21): stato_progetto + ultimo_report post-merge P…	CI	docs/sanitize-post-pr21	push	29569065912	55s	2026-07-17T09:11:18Z
```

Run dell'ultimo commit di sessione (`8301cb7`): **29570876259** su `docs/sanitize-post-pr21` — ✅ SUCCESS.

---

## §7 RISERVE APERTE

**Finding nuovo da F1-bis:**
- 🟡 **R-ci-hooks**: `tests/test_unit_hooks.py` non eseguito da CI (sonda 2026-07-17). Registrato in `stato_progetto.md` "Finding aperti". Task separato richiesto (modifica `ci.yml`).

**Ereditate attive (da review #52–#54, non chiuse in questa sessione):**
- Pattern `_cur_branch="$(...)"; if [ $? -ne 0 ]` fragile in `scrivi_rep.sh` — da allineare alla forma atomica (lezione #51).
- Manca test esplicito guard main-lock su `scrivi_rep.sh` (coperto per analogia da T-hook-a, asimmetria nella copertura).
- Backfill `memoria_revisore.md` #48–#50 PENDENTE — richiede sessione WSL locale, non eseguibile da Codespace.

---

## §F1-bis — Sonda CI: cosa esegue DAVVERO unit-suite

### cat .github/workflows/ci.yml (VERBATIM)

```yaml
name: CI

# Osservabilità di fine sessione — verde/rosso OGGETTIVO della suite unit a ogni push.
# Gira a ZERO token LLM: NESSUNA API key, NESSUN secrets.*, NESSUN provider LLM,
# NESSUN `gas doctor` con ping reali. Solo la suite pure-Python + le sue dipendenze.
# Il job è ROSSO se la suite fallisce: il runner tests/test_unit_kernel.py termina
# con `sys.exit(1 if FAIL else 0)` (exit code nativo ≠0 sui FAIL, verificato in sonda),
# quindi il fail dello step propaga senza parsing dell'output.
#
# Dal 2026-06-23 il runner installa e ABILITA il sandbox OS (bubblewrap) PRIMA della
# suite: così i 5 test bwrap (T11c2/T11e/T12a/T12c/T12e) eseguono run_command e i 4
# test del profilo sandbox (T13a/b/c/e, prima [SKIP]) GIRANO davvero → prima verifica
# CONTINUA del meccanismo che rende sicuro l'h24 sul VPS.
#
# AUTO-VERIFICABILE senza scaricare il log (2026-06-23): lo smoke-test bwrap e il
# conteggio PASS/FAIL/SKIP della suite finiscono nel JOB SUMMARY (visibile nella pagina
# della run, senza auth/zip); uno step-gate finale diventa rosso in modo inequivocabile
# SOLO se il sandbox non si attiva → "rosso da sandbox" si distingue da "rosso da test".
# Il verdetto della suite NON viene mai mascherato: l'exit code nativo resta la verità.

on: push

jobs:
  unit-suite:
    runs-on: ubuntu-latest
    # Nessun `env:` di provider e nessun blocco `secrets:` — di proposito.
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"   # combacia col venv del progetto (3.11.9)
          cache: pip

      - name: Install dependencies
        # numpy + fastembed + onnxruntime devono installarsi qui, altrimenti i
        # blocchi vettoriali T30/T31/T32 si saltano e la CI non prova metà del sistema.
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Enable OS sandbox (bubblewrap)
        id: sandbox
        # Installa bwrap e VERIFICA che possa creare gli unprivileged user namespace.
        # ubuntu-24.04 (ubuntu-latest) di default li RESTRINGE via AppArmor → senza
        # rilassamento bwrap fallisce ANCHE da installato. Lo smoke-test ESPLICITO
        # (BWRAP_OK/BWRAP_FAIL) finisce nel log E come output dello step (riusato dal
        # summary e dallo step-gate). NB: rilassare gli userns QUI è benigno — è il runner
        # EFFIMERO della CI, NON tocca GAS_SANDBOX_MODE=os_strict del VPS (lì fail-closed).
        # Questo step NON fallisce mai su BWRAP_FAIL: lascia girare la suite per avere il
        # quadro completo; la distinzione "rosso da sandbox" la fa lo step-gate finale.
        run: |
          sudo apt-get update
          sudo apt-get install -y bubblewrap
          smoke() { bwrap --unshare-all --ro-bind / / /bin/true >/dev/null 2>&1 && echo OK || echo FAIL; }
          r1="$(smoke)"
          echo "smoke-test 1 (post-install, pre-sysctl): BWRAP_${r1}"
          # ubuntu-24.04 restringe gli unprivileged userns via AppArmor: rilasso se la chiave esiste.
          if sysctl -n kernel.apparmor_restrict_unprivileged_userns >/dev/null 2>&1; then
            sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 || true
          fi
          if sysctl -n kernel.unprivileged_userns_clone >/dev/null 2>&1; then
            sudo sysctl -w kernel.unprivileged_userns_clone=1 || true
          fi
          r2="$(smoke)"
          echo "smoke-test 2 (post-sysctl): BWRAP_${r2}"
          {
            echo "smoke1=BWRAP_${r1}"
            echo "smoke2=BWRAP_${r2}"
          } >> "$GITHUB_OUTPUT"

      - name: Run unit suite (zero token LLM)
        # Eseguito DOPO l'abilitazione del sandbox: _probe_os_sandbox() deve vedere
        # bwrap + namespace disponibili (vedi smoke-test sopra). L'output è copiato in un
        # file (tee) per il summary; `pipefail` fa propagare l'exit code NATIVO della
        # suite → il verdetto verde/rosso non viene mai mascherato.
        env:
          PYTHONUTF8: "1"   # parità con l'esecuzione del progetto su Windows
        run: |
          set -o pipefail
          python tests/test_unit_kernel.py 2>&1 | tee "$RUNNER_TEMP/suite_output.txt"

      - name: Job summary (esito a colpo d'occhio)
        if: always()
        # Scrive nel JOB SUMMARY (pagina della run, niente zip/auth): esito bwrap +
        # conteggio della suite + lista dei FAIL. Puramente informativo: non cambia il
        # verdetto del job.
        run: |
          set +e   # step puramente informativo: un grep senza match non deve abortirlo
          out="$RUNNER_TEMP/suite_output.txt"
          {
            echo "## ⛽ GAS CI — esito osservabilità"
            echo ""
            echo "| Segnale | Valore |"
            echo "|---|---|"
            echo "| Sandbox OS post-install  | ${{ steps.sandbox.outputs.smoke1 }} |"
            echo "| Sandbox OS post-sysctl   | ${{ steps.sandbox.outputs.smoke2 }} |"
            if [ -f "$out" ]; then
              riep="$(grep -E 'RIEPILOGO:' "$out" | tail -1 | sed -E 's/=+//g; s/^[[:space:]]+//; s/[[:space:]]+$//')"
              nskip="$(grep -c '\[SKIP\]' "$out" || true)"
              echo "| Suite | ${riep:-non disponibile} |"
              echo "| SKIP  | ${nskip} |"
            else
              echo "| Suite | output non disponibile (la suite non è partita) |"
            fi
            echo ""
            if [ -f "$out" ]; then
              echo "### FAIL"
              echo '```'
              grep -E 'FAIL: ' "$out" || echo "(nessun FAIL)"
              echo '```'
            fi
            echo ""
            echo "> _Nota: il job resta ROSSO finché esiste un solo FAIL (exit code nativo della suite)._"
            echo "> _T9a/T9c sono SKIP in CI su assenza GEMINI/GROQ API key — non FAIL attesi._"
          } >> "$GITHUB_STEP_SUMMARY"

      - name: Gate — sandbox OS attivo
        if: always()
        # Rosso INEQUIVOCABILE e nominato se bwrap non crea i namespace nemmeno dopo il
        # sysctl: distingue lo STOP GATE ("rosso da sandbox" → micro-task skip-on-CI dei
        # test bwrap, tocca tests/, con revisore) da "T9a/T9c SKIP in CI" (assenza API key). Eseguito
        # per ULTIMO così il summary è già stato scritto.
        run: |
          if [ "${{ steps.sandbox.outputs.smoke2 }}" != "BWRAP_OK" ]; then
            echo "::error::Sandbox OS NON attivabile sul runner (smoke-test=${{ steps.sandbox.outputs.smoke2 }})."
            echo "::error::I 5 test bwrap restano rossi: STOP GATE → micro-task skip-on-CI (tocca tests/, con revisore)."
            exit 1
          fi
          echo "Sandbox OS attivo (BWRAP_OK): i test bwrap/T13 hanno potuto esercitare il profilo reale."
```

### ls -la tests/ (VERBATIM)

```
total 196
drwxrwxrwx+  3 codespace codespace   4096 Jul 17 09:05 .
drwxrwxrwx+ 15 codespace root        4096 Jul 16 09:35 ..
drwxrwxrwx+  2 codespace codespace   4096 Jul 16 13:43 __pycache__
-rw-rw-rw-   1 codespace codespace  13974 Jul 17 09:05 test_unit_hooks.py
-rw-rw-rw-   1 codespace codespace 170810 Jul 16 09:35 test_unit_kernel.py
```

### Risposte puntuali F1-bis

**1. Comando esatto eseguito dal job unit-suite?**

```
python tests/test_unit_kernel.py 2>&1 | tee "$RUNNER_TEMP/suite_output.txt"
```

Riga che lo prova: step "Run unit suite (zero token LLM)", blocco `run:`, riga con `python tests/test_unit_kernel.py`. La riga precedente `set -o pipefail` garantisce che l'exit code di `python` (non di `tee`) piloti il risultato dello step.

**2. Quali file di test esegue? Elenco esplicito.**

Solo `tests/test_unit_kernel.py`. Non esistono altri comandi nel workflow che referenzino file in `tests/`.

**3. tests/test_unit_hooks.py è eseguito da CI? SÌ/NO + riga che lo prova.**

**NO.** La stringa `test_unit_hooks` non compare in nessuna riga del workflow. Il file esiste in `tests/` (confermato da `ls -la tests/`) ma non è referenziato da alcun comando CI.

**4. tests/test_unit_kernel.py è eseguito da CI? SÌ/NO + come.**

**SÌ**, come script Python diretto: `python tests/test_unit_kernel.py` — NON pytest. Questo spiega l'assenza di INTERNALERROR: pytest importa il modulo e urta il `sys.exit` a livello modulo durante l'import; `python tests/test_unit_kernel.py` lo esegue come script e `sys.exit` è il normale punto di uscita.

**5. File in tests/ non eseguiti da nessun comando del workflow.**

`tests/test_unit_hooks.py` — presente in `ls -la tests/`, assente da tutto il workflow.

**6. Il check fallisce davvero se un test fallisce? Grep su `|| true` / `continue-on-error` / `set +e`.**

Output di `grep -n "|| true\|continue-on-error\|set +e" .github/workflows/ci.yml`:

```
62:            sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 || true
65:            sudo sysctl -w kernel.unprivileged_userns_clone=1 || true
91:          set +e   # step puramente informativo: un grep senza match non deve abortirlo
102:              nskip="$(grep -c '\[SKIP\]' "$out" || true)"
```

Analisi:
- Righe 62 e 65: `|| true` sui comandi `sysctl` dello step "Enable OS sandbox" — best-effort sulla chiave kernel, non toccano il run della suite.
- Riga 91: `set +e` nello step "Job summary" (`if: always()`) — dichiarato puramente informativo, non cambia il verdetto del job.
- Riga 102: `grep -c ... || true` nello stesso step informativo — evita che un grep senza match abortisca lo step di summary.

**Nessuno di questi pattern tocca lo step "Run unit suite".** Quello step usa solo `set -o pipefail` e nessun `set +e`. Il verde è reale.

### grep -n "sys.exit" tests/test_unit_kernel.py (VERBATIM)

```
3302:sys.exit(1 if FAIL else 0)
```

Contesto: riga 3302 è l'ultima riga eseguibile del file, dopo il blocco `print(RIEPILOGO)`. `grep -n "__main__" tests/test_unit_kernel.py` restituisce nessun output — il `sys.exit` è a livello modulo (non sotto `if __name__ == "__main__"`). Quando Python esegue il file come script, è il normale punto di uscita. Exit code: 1 se FAIL non vuoto, 0 altrimenti.

### Conclusione F1-bis

**Il verde di `unit-suite` copre tutti i test in `tests/test_unit_kernel.py` (T1–T59, motore + sandbox + memoria + vettori) e NON copre `tests/test_unit_hooks.py` (T-hook-a/b/c/d/e/f/g — hook bash).**
