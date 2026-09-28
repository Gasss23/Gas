# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-28 — Fetta 3a + 3a-bis (lezioni quarantena + fix pre-merge)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge PR #101** (`feat/fetta3a-lezioni-quarantena`): dopo review, eseguire `gasmerge 101`.
2. **Fetta 3b**: decidere se/quando implementare il generatore LLM di lezioni (proposte automatiche). Fuori scope.
3. **R-lez-bis-1** (cosmetica, non bloccante): `_MEM_FILE_PREFIXES` definita inline — spostare a costante di modulo in sessione futura se si desidera.
4. **R-lez-2** (non bloccante, ereditata): nessun blocco architetturale `lezioni_*` in `execute_tool_call`. Mitigata da T68n.

---

## §1 SCOPE & ESITO FETTE

**Fetta 3a** — lezioni in quarantena: tabella DB, CLI umana (`gas lezioni lista/approva/elimina`), iniezione prompt. 15/15 test PASS (T68a-T68n).

**Fetta 3a-bis** — fix pre-merge: lista testo completo+autore, rifiuto `\n`/`\r`, guard JSON R-lez-3, `write_file` guardrail esteso. 5/5 test PASS (T68o-T68s). 0 nuovi FAIL.

**Verifica DB E2E** (`gas lezioni lista` su `.gas_memory.db` reale):

```
Nessuna lezione trovata.
```

DB di produzione pulito. Le lezioni dell'E2E Fetta 3a erano su DB temporaneo in-process (`kernel_tmp()`).

**Delta test motore:**

- Baseline (2026-09-27, main): 346 PASS, 5 FAIL (F-mac-1 bwrap)
- Fetta 3a (0c816a9): 361 PASS, 5 FAIL (+15 PASS T68a-T68n)
- Fetta 3a-bis (427fcf0): **366 PASS, 5 FAIL** (+5 PASS T68o-T68s, 0 nuovi FAIL)

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 gas.py                             | 145 +++++++++++++++++++++++-
 modules/memory/store.py            | 149 +++++++++++++++++++++++++
 reports/diff_sessione.md           |  36 +++---
 reports/handoff.md                 | 137 +++++++++++------------
 reports/stato_progetto.md          |   6 +-
 reports/ultimo_report.md           | 218 ++++++++++++++-----------------------
 tests/test_unit_kernel.py          | 201 ++++++++++++++++++++++++++++++++++
 8 files changed, 666 insertions(+), 228 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
6dfbcfd docs(fetta3a-bis): report + handoff + stato_progetto aggiornati
427fcf0 fix(fetta3a-bis): lista testo completo+autore, \n rifiutato, R-lez-3, write_file esteso
f88e081 chore(revisore): memoria review #107 — APPROVATO CON RISERVE
715af86 fix(fetta3a): concordanza grammaticale R-lez-1 + verdetto revisore verbatim
8dfdf08 chore(revisore): memoria review #106 — APPROVATO CON RISERVE
625e34d docs(fine-task): handoff 2026-09-28 Fetta 3a lezioni quarantena
0c816a9 feat(fetta3a): lezioni in quarantena — tabella + CLI umana + iniezione prompt
```

---

## §4 VERDETTO DEL REVISORE

### Review #107 — Fetta 3a-bis (INTEGRALE)

**APPROVATO CON RISERVE**

**1. `gas.py:1552` — `_MEM_FILE_PREFIXES` e guardrail write_file esteso**: Introduce tupla locale e sostituisce il singolo check con `any(p in normalized for p in _MEM_FILE_PREFIXES)`. La normalizzazione `lower().replace("-","_").replace(" ","_")` già applicata garantisce: `.gas_memory.db-wal` → bloccato; `.GAS_MEMORY.db` → bloccato. T68s verifica 6 varianti. Rischio falsi positivi: trascurabile. **ok.** Riserva cosmetica: `_MEM_FILE_PREFIXES` inline — meglio come costante di modulo (R-lez-bis-1), non bloccante.

**2. `modules/memory/store.py:1186` — rifiuto `\n`/`\r`**: Check DOPO strip() e PRIMA del len-check. Interazione con strip() corretta. T68q verifica rifiuto + assenza scrittura DB. **ok.**

**3. `gas.py:2677-2686` — guard JSON, testo completo, autore**: `try/except (json.JSONDecodeError, TypeError)` chiude R-lez-3. Fallback `"<illeggibile>"`. Rimozione `[:80]` corretta. T68r inietta JSON malformato via sqlite3 → verifica `rc==0 AND "<illeggibile>"`. **ok.**

**4. T68o-T68s**: 5/5 PASS. `_run_lezioni_cmd` in-process con `redirect_stdout` + `sys.argv` patch — corretto. Nessun antipattern Wall of Shame. **ok.**

**Verifica guardrail**: cap 10 iterazioni non toccato. `_get_window()` non toccato. Wall of Shame pulito. Fail-safe §9 rispettato.

**Riserve non bloccanti:**
- R-lez-bis-1 (cosmetica): `_MEM_FILE_PREFIXES` inline
- R-lez-2 (ereditata da #106): nessun blocco architetturale `lezioni_*`

---

### Review #106 — Fetta 3a (INTEGRALE)

**APPROVATO CON RISERVE**

**`gas.py:1282-1300` — `_lezioni_pin()`**: calcolato una volta per turno, fuori dal loop per-provider. Fail-safe su due livelli. Escape via `_sanitize_memory_text`. E2E reale conferma escape funzionante. **ok.**

**`gas.py:1718` — payload con `lezioni_pin`**: copre TUTTI i provider. `_get_window()` non toccato. Cap 10 iterazioni non toccato. **ok.**

**`gas.py:2607-2706` — `lezioni_cmd()` CLI SOLO UMANA**: try/except ValueError su int(argv[3]). Guard `mem.available`. Docstring "VIETATO". T68n asserisce assenza tool "lezione". **ok.**

**`modules/memory/store.py:1174-1278`**: CHECK DDL + validazione applicativa. `_transiziona_lezione` legge prima di scrivere. `get_lezioni_approvate` bounded. **ok.**

**T68a-T68n**: 15/15 PASS. **ok.**

**Riserve:** R-lez-1 (cosmetic, già fixata); R-lez-2 (minore, nessun blocco architetturale); R-lez-3 (json.loads — chiusa da questa fetta 3a-bis).

---

## §5 STATO CI

PR #101 aperta (`feat/fetta3a-lezioni-quarantena`). CI `.github/workflows/ci.yml` — stato da verificare su GitHub prima del merge.
