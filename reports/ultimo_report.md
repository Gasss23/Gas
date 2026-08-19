# REPORT TASK — 2026-08-19
## fix/quotepath-non-ascii — core.quotePath=false per path non-ASCII in git diff --name-only

Branch: `fix/quotepath-non-ascii`
Commit: `1a45930`

---

## DECISIONI UMANE RICHIESTE

Nessuna. Nessun trade-off aperto: il fix è localizzato, i test sono reali, il revisore ha approvato.

---

## §1 — SCOPE & ESITO FETTE

- **Sonda call site git path-parsing nel motore**: FATTA — vedi §2.
- **Fix core.quotePath=false**: FATTA — 2 call site, sotto soglia ~3.
- **Test reale con file non-ASCII**: FATTA — 2 test nuovi, 11 PASS totali.
- **Commit**: FATTA — `1a45930` — review #85 APPROVATO.

---

## §2 — SONDA: invocazioni git che parsano path nel motore

Sonda su: `gas.py`, `brains/`, `modules/`, `scripts/`.

### gas.py — NESSUN call site path-parsing

Le invocazioni git in `gas.py` sono:
- `gas.py:802` — wrapper `git()` in `_take_snapshot`: usa `rev-parse`, `add -A`, `write-tree`, `commit-tree`, `update-ref` — nessuna parsa path dall'output.
- `gas.py:850` — `for-each-ref --format=%(refname)`: parsa ref names (non file path).
- `gas.py:1699` — `for-each-ref` in `doctor`: conta ref, non file path.
- `gas.py:1711` — `count-objects -v`: parsa coppie chiave:valore numerici, non file path.

**Conclusione**: `gas.py` non ha call site vulnerabili.

### brains/, modules/ — NESSUN call site git

Confermato da grep: nessuna invocazione git in questi directory.

### scripts/ — 2 CALL SITE (unici nel motore)

| File | Funzione | Riga | Comando |
|------|----------|------|---------|
| `scripts/check_handoff.py` | `_diff_names` | 48 | `git diff --name-only {base}..HEAD` |
| `scripts/check_verdetto.py` | `_session_files` | 67 | `git diff --name-only {base}..HEAD` |

Ogni script ha il proprio wrapper `_git()` (non condiviso). Non esiste un chokepoint unico tra i due file. Con soli 2 call site (sotto la soglia ~3), il fix viene applicato direttamente alle chiamate path-parsing, non al wrapper generico (che gestisce anche `rev-parse`, `merge-base`, `show` — non path-parsing).

---

## §3 — FIX APPLICATO

### check_handoff.py:48 (`_diff_names`)

```python
# PRIMA
r = _git(["git", "diff", "--name-only", f"{base}..HEAD"], repo)
# DOPO
r = _git(["git", "-c", "core.quotePath=false", "diff", "--name-only", f"{base}..HEAD"], repo)
```

### check_verdetto.py:67 (`_session_files`)

```python
# PRIMA
r = _git(["git", "diff", "--name-only", f"{base}..HEAD"], repo)
# DOPO
r = _git(["git", "-c", "core.quotePath=false", "diff", "--name-only", f"{base}..HEAD"], repo)
```

Il flag `-c` è **per-invocazione**: non modifica `.gitconfig` utente/globale e non ha effetti collaterali su altri comandi git.

---

## §4 — TEST REALE (verificato)

### Verifica before/after (subprocess reale, non simulato)

```
SENZA fix: '"caff\303\250.txt"'   ← stringa con virgolette letterali
CON fix:   'caffè.txt'            ← UTF-8 corretto

Set SENZA fix: {'"caff\\303\\250.txt"'}
Set CON fix:   {'caffè.txt'}

'caffè.txt' in SENZA fix set: False   ← test fallisce senza fix
'caffè.txt' in CON fix set:   True    ← test passa con fix
```

### Suite completa

```
tests/test_unit_handoff_check.py::TestCheckHandoff::test_omits_file_exits_1 PASSED
tests/test_unit_handoff_check.py::TestCheckHandoff::test_correct_handoff_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckHandoff::test_allowlist_ultima_risposta_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckHandoff::test_handoff_not_in_diff_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckHandoff::test_on_main_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckHandoff::test_nonascii_filename_check_handoff PASSED
tests/test_unit_handoff_check.py::TestCheckVerdetto::test_invalid_path_line_ref_exits_1 PASSED
tests/test_unit_handoff_check.py::TestCheckVerdetto::test_valid_ref_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckVerdetto::test_no_diff_motore_exits_0 PASSED
tests/test_unit_handoff_check.py::TestCheckVerdetto::test_nota_mitigated_not_closed PASSED
tests/test_unit_handoff_check.py::TestCheckVerdetto::test_nonascii_filename_check_verdetto PASSED

11 passed in 3.68s
```

---

## §5 — VERDETTO REVISORE (INTEGRALE)

Review #85 — APPROVATO — 2026-08-19

Elementi concreti esaminati nel diff:

- `scripts/check_handoff.py:48` — aggiunta `-c core.quotePath=false` alla lista argomenti git — rischio effetti persistenti su gitconfig o regressioni su path ASCII — esito: ok (flag per-invocazione, path ASCII invariati).
- `tests/test_unit_handoff_check.py:267-271` — cattura `merge-base` prima di `_commit_all` — rischio che la sequenza invertita renderebbe il diff BASE..HEAD vuoto e il test non mordace — esito: ok, sequenza corretta.

Rischio esplicitamente escluso: compatibilità git < 2.x per il flag `-c` — non verificata, ritenuta fuori scope per gli ambienti target del progetto (WSL Ubuntu recente, GitHub Actions).

---

## §6 — NOTE DI PROCESSO

Il commit atomico del revisore (`chore(revisore): memoria review #85`) ha incluso per errore anche i file staged del motore (scenario R2-vaglio B2: `git add memoria_revisore.md && git commit` quando altri file sono in staging committa tutto). Risolto con `git reset --soft HEAD~1` e recommit separato con messaggio corretto. Il contenuto era già corretto; solo il messaggio era sbagliato. Nessuna perdita di dati.
