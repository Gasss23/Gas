# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-27 — R-crm-1b Fetta 3: dedup telefono

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge della PR** `feature/crm-dup-telefono → main` (CI verde run `30241988037` ✅ su `c8ab4be`).
2. **Decidere se esporre** `normalizza_telefono` / `rileva_duplicati_telefono` in `gas doctor`, CLI `check-dups`, o tool `ricorda` — non fatto per stop gate esplicito del prompt; proposto nel report come prossimo passo.

---

## §1 SCOPE & ESITO FETTE

- **Fetta UNICA — R-crm-1b fetta 3 (dedup telefono)**: `FATTA`
  `normalizza_telefono` + `rileva_duplicati_telefono` in `modules/memory/store.py`. Export in `__init__.py`. 22 test T60a–T60m. 272 PASS 0 FAIL. Revisore #67 APPROVATO CON RISERVE.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   1 +
 modules/memory/__init__.py         |   2 +
 modules/memory/store.py            | 123 +++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  19 +++--
 reports/handoff.md                 | 116 ++++++++++++++----------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           | 130 +++++++++++++++++++--------------
 tests/test_unit_kernel.py          | 143 +++++++++++++++++++++++++++++++++++++
 8 files changed, 407 insertions(+), 129 deletions(-)
```

**VINCOLI VERIFICATI DA CI (job handoff-check):**
Il set di path sopra deve corrispondere esattamente a `git diff --name-only BASE..HEAD`.
`reports/ultima_risposta.md` è escluso dall'allowlist CI (committato dall'hook post fine-task).
I conteggi di righe sono approssimati per costruzione (handoff.md conta se stesso).

---

## §3 GIT LOG --ONELINE (sessione)

```
c8ab4be docs(fine-task): report + stato_progetto R-crm-1b fetta 3 (2026-07-27)
f6259eb feat(crm): R-crm-1b fetta 3 — dedup telefono (normalizza_telefono + rileva_duplicati_telefono)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

**Commit f6259eb** — tocca `modules/memory/store.py`, `modules/memory/__init__.py`, `tests/test_unit_kernel.py`.

**Review #67 — APPROVATO CON RISERVE**

Elementi esaminati:
- `modules/memory/store.py:223` — `digits = re.sub(r"[^\d]", "", testo)` — rimozione di tutto il non-numerico (inclusi `+` interni): la lezione #49 della memoria (regex `[^\d+]` conservava i `+` producendo canonici con `+` interni) è stata recepita correttamente. Regex verificata: `"+39+333"` → `digits = "39333"` (5 cifre) → gate `^\+\d{8,15}$` fallisce → `""`. Esito: **ok**.
- `modules/memory/store.py:938` — `for raw in (r.get("chiave_norm"), r.get("contatto"))` — la lettura doppia cerca il telefono sia nella chiave normalizzata sia nel campo contatto. `_rows` restituisce `List[Dict]` (riga 388: `[dict(r) for r in cur.fetchall()]`), quindi `.get()` è sicuro e restituisce `None` su campo assente/NULL; `normalizza_telefono(None) → ""` fa da gate. Il pattern è identico alla versione `rileva_duplicati_email` già revisionata in #57. Esito: **ok**.
- `tests/test_unit_kernel.py:3472–3500` (T60k) — test fail-open: il `diario` viene DROP-pato fisicamente, poi si verifica che `rileva_duplicati_telefono` non crashi, restituisca la coppia E tenti il `append_diario` (FAIL-OPEN §9). Il pattern di mock (`_tracked_append_60k`) è in-process, senza simulazione di output — conforme alla sez. 5 di CLAUDE.md. Esito: **ok**.
- `tests/test_unit_kernel.py:3438–3451` (T60i) — usa `chiave_norm` via campo `contatto` per entrambe le schede. Il ramo `chiave_norm` della tupla `(r.get("chiave_norm"), r.get("contatto"))` non viene esercitato in nessun test della serie T60: scheda con telefono nella chiave primaria e scheda con telefono in contatto non compaiono in coppia. Il percorso è logicamente simmetrico ma la copertura è incompleta. Esito: **riserva R2**.

Riserve (non bloccanti):
- **R1** — `int(r["id"])` fuori dal try/except post-lettura. In produzione non causa crash perché SQLite garantisce che `INTEGER PRIMARY KEY` sia sempre un intero e una corruzione che alterasse quel campo causerebbe già un `sqlite3.Error` alla query. Non bloccante, ma non blindato esplicitamente.
- **R2** — ramo `chiave_norm` non coperto dai test: T60i–T60m usano sempre il telefono nel campo `contatto`. Un test in cui la scheda A ha il telefono come chiave normalizzata e la scheda B lo ha in `contatto` eserciterebbe il ramo separatamente. Non bloccante (la logica è simmetrica e usata identicamente in `rileva_duplicati_email`), ma da tenere a mente per la copertura futura.

Rischio esplicitamente escluso: correttezza del gate su numeri di altri paesi non testata end-to-end (fuori perimetro dichiarato).

Guardrail verificati: nessun slicing history ✓, nessuna simulazione output tool ✓, loop cap §8 non toccato ✓, `_get_window` non toccato ✓, eccezioni intercettate con `logging.warning` ✓, FAIL-OPEN §9 ✓, `normalizza_telefono` mai solleva ✓.

---

## §5 DELTA TEST DEL MOTORE

**Prima:** 250 PASS (suite pre-sessione su main).
**Dopo:** 272 PASS, 0 FAIL.
**Delta:** +22 test (T60a–T60m: 12 su `normalizza_telefono` + 10 su `rileva_duplicati_telefono`).

Output riepilogo reale (da run in sessione):
```
=== RIEPILOGO: 272 PASS, 0 FAIL ===
```

---

## §6 STATO CI

Output `gh run list -L 3`:
```
completed	success	docs(fine-task): report + stato_progetto R-crm-1b fetta 3 (2026-07-27)	CI	feature/crm-dup-telefono	push	30241988037	51s	2026-07-27T06:12:31Z
completed	success	Merge pull request #46 from Gasss23/fix/gasmerge-failopen	CI	main	push	30223085074	51s	2026-07-26T22:24:53Z
completed	success	docs: fix frase riga 21 + sync contatore #65->#66 riga 138	CI	fix/gasmerge-failopen	push	30222975736	40s	2026-07-26T22:21:35Z
```

**Mappatura commit → run:**
- `c8ab4be` (docs fine-task) → run `30241988037` ✅ SUCCESS. Questa run testa l'albero dell'HEAD al momento del push, che include anche `f6259eb`.
- `f6259eb` (feat motore) → **nessuna run propria su questo SHA** (pushato nello stesso push di `c8ab4be`; GitHub Actions crea una run per push, non per commit). Il contenuto di `f6259eb` è incluso e testato nell'albero di `c8ab4be` (run `30241988037` ✅).

---

## §7 RISERVE APERTE

Dalla review #67 (questo commit):
- **R1** — `int(r["id"])` fuori try/except in `rileva_duplicati_telefono` post-lettura (non critico: SQLite garantisce INTEGER PK; non blindato esplicitamente).
- **R2** — Ramo `chiave_norm` non coperto da T60: nessun test con telefono come chiave primaria di una scheda in coppia con telefono nel campo `contatto` dell'altra (logica simmetrica, copertura futura).

Entrambe tracciate in `reports/stato_progetto.md`.
