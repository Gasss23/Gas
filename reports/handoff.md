# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-23 — FIX promemoria_end.sh (blocco JSON Stop hook con logica handoff fresco)

---

## §0 DECISIONI UMANE RICHIESTE

_[da completare dopo git push — vedi procedura §0]_

---

## §1 SCOPE & ESITO FETTE

- **Passo 0 — Pre-check settings.local.json**: `FATTO` — nessuna chiave `hooks`/`disableAllHooks`, procede.
- **Verifica formato hook Stop**: `FATTO` — `stop_hook_active` + `{"decision":"block","reason":"..."}` confermati dal binario Claude Code 2.1.280.
- **Fetta 1a — Riscrittura `.claude/hooks/promemoria_end.sh`**: `FATTA` — soft-warning stderr → blocco JSON stdout; logica handoff fresco (ultimo commit non-chore); filtro chore(scrivi-rep):; anti-loop; fail-open totale.
- **Fetta 1b — Test `tests/test_unit_hooks.py`**: `FATTA` — 9 test (T-prom-1..7+3b+3c), repo git reali, 34/34 green.
- **Test e2e manuale**: `FATTO` — blocco JSON confermato su branch temporaneo mai pushato.
- **Revisore (gate obbligatorio)**: `FATTO` — Review #101 APPROVATO.
- **F2, F3 (fuori scope)**: `SALTATE — fuori scope dichiarato`.

---

## §2 GIT DIFF --STAT (sessione)

_[da completare al passo 4bis con `git diff --cached --stat ${BASE}`]_

---

## §3 GIT LOG --ONELINE (sessione)

_[da completare al passo 4bis]_

---

## §4 VERDETTO DEL REVISORE

**Review #101 — APPROVATO** (diff: `.claude/hooks/promemoria_end.sh` + `tests/test_unit_hooks.py`)

Testo integrale del verdetto:

> ## VERDETTO REVIEW #101 — APPROVATO
>
> **File revisionati:** `.claude/hooks/promemoria_end.sh` + `tests/test_unit_hooks.py`
> **Scope:** riscrittura soft-warning → blocco JSON con logica "handoff fresco"
>
> ### Elementi verificati sul diff/file reale
>
> 1. **`.claude/hooks/promemoria_end.sh:33-34`** — `SESSION_COMMITS=$(git ... | grep -cv '^chore(scrivi-rep):') || SESSION_COMMITS=0` — rischio: grep -cv su input vuoto. Per POSIX, grep -c con zero righe emette "0" ed esce rc=1; il `||` cattura rc=1 → SESSION_COMMITS=0; la guard regex a riga 36 copre output non numerici; riga 38 (`-le 0 && exit 0`) porta all'uscita silenziosa. **Esito: ok.**
>
> 2. **`.claude/hooks/promemoria_end.sh:41-42`** — pipeline LAST_NON_CHORE: `log --format="%H %s" | grep -v ' chore(scrivi-rep):' | head -1 | awk '{print $1}'` — rischio: affidabilità del pattern. `%H` è hex puro senza spazi, lo spazio separatore è garantito; le parentesi `()` nel pattern sono BRE-letterali (nessun flag `-E`), nessun rischio regex. **Esito: ok.**
>
> 3. **`.claude/hooks/promemoria_end.sh:16-19`** — anti-loop `stop_hook_active` via python3 JSON parse: in caso di stdin non-JSON o python3 assente, `_SHA` resta vuoto, lo script continua normalmente. Fail-open preservato. **Esito: ok.**
>
> 4. **`.claude/hooks/promemoria_end.sh:44+50-52`** — `HANDOFF_IN_LAST=0` inizializzato prima del blocco condizionale; formato `{"decision":"block","reason":"..."}` su stdout corretto per Stop hook; `exit 0` finale garantisce fail-open. **Esito: ok.**
>
> ### Coerenza con CLAUDE.md
>
> - Sez.5 Wall of Shame: nessun raw history slicing di `.gas_history.json`, nessuna simulazione output tool. ✓
> - Sez.9: tutte le eccezioni bash sono fail-open (exit 0), log su `gas_debug.log` solo su merge-base fallita. ✓
> - Sez.3 Gate: il diff tocca `tests/` → gate correttamente invocato. ✓
> - Guardrail `gas.py` (cap 10 iterazioni, `_get_window`) non toccati. ✓
>
> ### Rischio escluso
>
> Il comportamento effettivo di Claude Code alla ricezione del payload `{"decision":"block","reason":"..."}` su stdout da uno Stop hook non è verificabile in locale (richiede sessione Claude Code attiva con hook scattante). L'analisi è basata sullo schema documentato.
>
> **VERDETTO: APPROVATO**
>
> La riscrittura è tecnicamente corretta, fail-open in tutti i percorsi, anti-loop su `stop_hook_active`, e coerente con la filosofia "robustezza > potenza, zero crash". La logica "handoff fresco" è implementata correttamente con tutte le guard per gli edge case.

---

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_hooks.py` modificato (non gas.py/brains/modules/).

**Prima:** 25 test in `TestPromemoriaEnd` (5 test, alcuni ormai obsoleti con stderr semantics).
**Dopo:** 34 test totali — 9 test in `TestPromemoriaEnd`, tutti green.

```
============================= test session starts ==============================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
collected 34 items

tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_1_no_commits_since_base_no_block PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_2_commits_no_handoff_blocks PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_3_handoff_as_last_commit_no_block PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_3b_commits_after_handoff_blocks PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_3c_only_chore_after_handoff_no_block PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_4_no_origin_warns_log_exit_0 PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_5_head_on_main_silent_exit_0 PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_6_stop_hook_active_true_no_block PASSED
tests/test_unit_hooks.py::TestPromemoriaEnd::test_prom_7_non_git_dir_exit_0 PASSED

============================== 34 passed in 5.40s ==============================
```

---

## §6 STATO CI

_[da completare al passo 4bis]_

---

## §7 RISERVE APERTE

Nessuna riserva dal revisore #101.

**Finding F3 (partenza su main) non in scope**: se si vuole affrontare, richiede sessione dedicata con decisione umana su strategia.
