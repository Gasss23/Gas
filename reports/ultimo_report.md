# Report task: fix/ci-summary-openrouter — 2026-07-23

## Esito per fetta

| Fetta | Esito | Note |
|---|---|---|
| FETTA 1 — R-ci-summary | **FATTA** | commit `70d1b0d` |
| FETTA 2 — R-ci-openrouter (T9a) | **DEFERITA** | suite kernel non eseguibile in locale (dipendenze assenti) |

---

## FETTA 1 — R-ci-summary

### Problema risolto
Lo step "Run hook suite" in ci.yml non catturava l'output verso un file,
quindi la hook suite (pytest tests/test_unit_hooks.py) non compariva nel
Job Summary della run CI.

### Modifica apportata
Solo `.github/workflows/ci.yml`. Nient'altro.

1. **Step "Run hook suite"**: aggiunto `set -o pipefail` e `tee "$RUNNER_TEMP/hooks_output.txt"`
   per catturare l'output mantenendo l'exit code nativo di pytest.
2. **Step "Job summary"**: aggiunta lettura di `$RUNNER_TEMP/hooks_output.txt`,
   riga nella tabella per "Hook suite", sezione "### FAIL hook suite".
   Rinominate le righe esistenti da "Suite"/"SKIP" a "Suite kernel"/"SKIP kernel"
   per distinguerle visivamente.

### diff --stat (rigenerato live)

```
 .github/workflows/ci.yml | 25 ++++++++++++++++++++-----
 1 file changed, 20 insertions(+), 5 deletions(-)
```

### Hash commit FETTA 1
`70d1b0d` — `ci(summary): aggiungi hook suite al Job Summary con pipefail`

---

## PROVE OBBLIGATORIE (FETTA 1)

### (a) Meccanismo pipefail — comando e output reali

```bash
$ set -o pipefail; false | tee /dev/null; echo "exit code: $?"
exit code: 1
```

`set -o pipefail` propaga l'exit code del comando sinistro della pipe
(qui `false`, exit 1) anche quando `tee` termina con 0.
Senza pipefail il risultato sarebbe `exit code: 0` — gate CI silenziosamente cieco.

### (b) pytest tests/test_unit_hooks.py — output reale locale

```
platform linux -- Python 3.12.3, pytest-9.1.1
collected 10 items

tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_a_main_no_commit PASSED
tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_b_feature_branch_commits PASSED
tests/test_unit_hooks.py::TestSessionEndGuard::test_hook_c_detached_head_no_commit PASSED
tests/test_unit_hooks.py::TestSessionEndPush::test_hook_d_push_to_feature_branch_not_main PASSED
tests/test_unit_hooks.py::TestSessionEndPush::test_hook_e_push_failure_warns_and_exits_zero PASSED
tests/test_unit_hooks.py::TestSessionEndAddRobust::test_hook_f_add_without_gas_history PASSED
tests/test_unit_hooks.py::TestScriviRepPush::test_hook_g_push_to_feature_branch_not_main PASSED
tests/test_unit_hooks.py::TestScriviRepPush::test_hook_h_main_no_commit PASSED
tests/test_unit_hooks.py::TestScriviRepJq::test_hook_i_no_jq_warns_and_exits_zero PASSED
tests/test_unit_hooks.py::TestScriviRepJq::test_hook_j_detached_head_no_commit PASSED

10 passed in 2.18s
```

**10 PASS, 0 FAIL, 0 SKIP.**

---

## VERDETTO REVISORE FETTA 1 (verbatim, copia-incolla)

```
File aggiornato: /home/gqual/Gas/.claude/agents/memoria_revisore.md (riga #58 aggiunta in coda).

Riepilogo: Il diff è approvato senza riserve. Il meccanismo `set -o pipefail` è il
solo intervento necessario e sufficiente per preservare l'exit code di pytest attraverso
la pipe `tee`, ed è già usato in modo identico per la suite kernel. Il passo summary
rimane puramente informativo con `set +e` e guardie `[ -f ... ]` su tutti i file prodotti.
Nessun guardrail indebolito, nessun antipattern del Wall of Shame.
```

**Verdetto: APPROVATO senza riserve.**

---

## FETTA 2 — R-ci-openrouter (T9a) — DEFERITA

### Motivo
La suite kernel (`tests/test_unit_kernel.py`) non è eseguibile in locale:

```
$ python tests/test_unit_kernel.py
Traceback (most recent call last):
  File "tests/test_unit_kernel.py", line 16, in <module>
    import gas
  File "gas.py", line 11, in <module>
    from openai import OpenAI
ModuleNotFoundError: No module named 'openai'
```

Il venv contiene solo pytest e le dipendenze degli hook; le dipendenze del
motore (openai, ecc.) non sono installate.

### Analisi della fix necessaria (non implementata)
T9a è gated su `_has_live_keys = bool(GEMINI_API_KEY and GROQ_API_KEY)`,
ovvero viene eseguito SOLO se le chiavi reali sono presenti. In CI non lo
sono, quindi T9a è SEMPRE SKIP in CI. La fix corretta sarebbe:
- Aggiungere chiavi fake per GEMINI e GROQ prima del run (come già fatto
  per OPENROUTER con `os.environ.pop`)
- Rimuovere il gate `_has_live_keys` per T9a (lasciandolo solo per T9c se
  T9c richiede verifica su disco — da valutare)
- Così T9a girerebbe sempre, deterministicamente, con FakeOpenAI

### Come procedere
Installare `pip install -r requirements.txt` nel venv di sviluppo locale,
eseguire la suite kernel (`python tests/test_unit_kernel.py`), validare le
due condizioni (OPENROUTER assente / iniettata fake), poi committare la fetta
in un PR separato con revisore.

La fetta 2 NON è stata committata. La PR attuale contiene solo FETTA 1.

---

## PR

URL: https://github.com/Gasss23/Gas/pull/41
NON mergiare — il merge è azione umana da browser.
