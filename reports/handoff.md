# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-25 — Auto-apprendimento Fetta 2 (memoria DATO + provider onesto + guard fonte)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #99 (https://github.com/Gasss23/Gas/pull/99).

---

## §1 SCOPE & ESITO FETTE

- **Fetta A — R2: memoria entra nel prompt come DATO**: `FATTA`  
  `_sanitize_memory_text` (entità HTML per tag delimitatori + rimozione C0 ctrl-chars);
  `_memoria_pin` e `_ricorda` avvolgono output in `<memoria_dati>…</memoria_dati>`;
  regola anti-injection aggiunta a `_GAS_SYSTEM_PROMPT_BASE`. Etichetta: **MITIGATO**.

- **Fetta B — provider onesto in turno_fine**: `FATTA`  
  `_turno_provider` settato SOLO quando la risposta è prodotta; `_turno_tentati` traccia
  tutti i provider tentati in ordine; `turno_fine` include `tentati=<lista>`.

- **Fetta C — guard su `fonte`**: `FATTA`  
  `FONTI_AMMESSE = frozenset{"kernel","utente","modello"}`; guard in `append_diario`:
  valore non ammesso → WARN + NULL, fail-safe §9.

---

## §2 GIT DIFF --STAT (sessione)

```
.claude/agents/memoria_revisore.md |   1 +
 gas.py                             |  57 ++++++++++---
 modules/memory/__init__.py         |   2 +
 modules/memory/store.py            |   7 ++
 reports/diff_sessione.md           |  28 ++++---
 reports/handoff.md                 | 144 +++++++++++++++-----------------
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           | 163 +++++++++++++++++++++++++-----------
 tests/test_unit_kernel.py          | 167 +++++++++++++++++++++++++++++++++++++
 9 files changed, 424 insertions(+), 149 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
457dd2b docs(fine-task): report auto-apprendimento fetta 2 — memoria DATO + provider onesto + guard fonte
644ff09 feat(apprendimento-f2): memoria come dato + provider onesto + guard fonte
0b9c509 chore(revisore): memoria review #104 — APPROVATO
```

---

## §4 VERDETTO DEL REVISORE

**Commit 644ff09** tocca `gas.py`, `modules/memory/store.py`, `modules/memory/__init__.py`,
`tests/test_unit_kernel.py` — verdetto integrale review #104:

> **APPROVATO**
>
> 1. `gas.py:47-56` — `_sanitize_memory_text`: sostituzione HTML entities non contiene il
>    tag originale come sottostringa; regex C0 charset corretto; gap C1 (0x80-0x9F)
>    accettabile per il contesto.
> 2. `gas.py:1585-1586` + `gas.py:1682` + `gas.py:1747` — separazione `_turno_provider` /
>    `_turno_tentati`: `_turno_provider` settato SOLO nel ramo `_turno_final = True`,
>    `_turno_tentati` accumula ogni provider tentato. Semantica corretta. `descr` cresce
>    ma è testo libero, nessuna migrazione schema SQLite.
> 3. `modules/memory/store.py:59` + `modules/memory/store.py:412-414` — `FONTI_AMMESSE` + guard in
>    `append_diario`: conforme fail-safe §9, valore non ammesso → WARN + NULL, zero crash.
> 4. `gas.py:79` — regola anti-injection nel system prompt: conforme.
> 5. Wall of Shame §5: conforme. Cap 10 iterazioni (§8): intatto. `_get_window()`:
>    non toccato. `_memoria_pin` resta FUORI dalla finestra.
>
> Riserva cosmetica non bloccante: `List[str]` (typing legacy) vs `list[str]` (Python 3.10+).

---

## §5 DELTA TEST DEL MOTORE

**Prima (fetta 1):** 318 PASS, 5 FAIL  
**Dopo (fetta 2):** 339 PASS, 5 FAIL

```
=== RIEPILOGO: 339 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile...
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS...
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS...
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS...
```

I 5 FAIL sono T11c2/T11e/T12a/T12c/T12e — bwrap macOS (F-mac-1, noto, fuori scope).
Nessun FAIL nuovo. Nuovi PASS: +21 (T65a-f, T66a-c, T67a-e).

---

## §6 STATO CI

```
completed	success	docs(fine-task): report auto-apprendimento fetta 2 — memoria DATO + p…	CI	feat/apprendimento-f2	push	36054178310	53s	2026-09-24T20:20:15Z
completed	success	Merge pull request #98 from Gasss23/feat/apprendimento-f1-esiti	CI	main	push	36051566338	1m1s	2026-09-24T19:56:53Z
completed	success	docs(fine-task): handoff 2026-09-24 auto-apprendimento fetta 1	CI	feat/apprendimento-f1-esiti	push	36050616546	53s	2026-09-24T19:48:21Z
```

**Mappatura commit→run:**
- `457dd2b` (docs fine-task) — run `36054178310` su `feat/apprendimento-f2`, **completed success**
- `644ff09` (feat fetta 2) — push bundled con `457dd2b`, testato dall'albero della stessa run `36054178310`; SHA intermedio mai testato in isolamento
- `0b9c509` (chore revisore) — nessuna run su questo SHA in isolamento; incluso nell'albero di `36054178310`

---

## §7 RISERVE APERTE

- **Riserva cosmetica non bloccante (review #104)**: `List[str]` in `gas.py:1586` è
  typing legacy — `list[str]` è lo style Python 3.10+. Non bloccante.
- **Fetta A etichetta MITIGATO**: i delimitatori `<memoria_dati>` riducono la prompt
  injection, non la eliminano. Un solo giro E2E non è una prova formale; l'efficacia
  dipende dal modello che riceve il blocco. Da re-testare con provider reali al deploy VPS.
- **Gap C1 controls (0x80-0x9F)**: `_sanitize_memory_text` non copre i caratteri C1
  (0x80-0x9F). Accettabile per il contesto corrente; da valutare in hardening futuro.
