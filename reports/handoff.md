# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-07-27 — Verifica fetta 4 + fix handoff-check CI

---

## §0 DECISIONI UMANE RICHIESTE

1. **Merge della PR** `feature/crm-dup-telefono → main` (CI: job `handoff-check` atteso verde dopo questo commit; `unit-suite` 276 PASS 0 FAIL ✅).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — rileva_duplicati_email**: `CHIUSA` — sessioni precedenti.
- **Fetta 2 — idempotenza diario email**: `CHIUSA` — sessioni precedenti.
- **Fetta 3 — dedup telefono**: `CHIUSA` — commit f6259eb (sessione precedente).
- **Fetta 4 — gas doctor CRM + gas duplicati**: `CHIUSA` — commit 638c894 (sessione precedente). Questa sessione ha solo verificato lo stato: entrambe le feature (sezione CRM in `doctor()` riga 1815 e `duplicati_cmd()` riga 2337) erano già presenti. Nessun nuovo codice scritto.
- **Finding sessione — fix handoff-check**: `FATTO` — §2 precedente ometteva `gas.py`; corretto in questo commit.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 gas.py                             |  67 ++++++++++
 modules/memory/__init__.py         |   2 +
 modules/memory/store.py            | 123 +++++++++++++++++++
 reports/diff_sessione.md           |  29 +++--
 reports/handoff.md                 | 132 ++++++++++----------
 reports/stato_progetto.md          |  10 +-
 reports/ultimo_report.md           |  87 +++++--------
 tests/test_unit_kernel.py          | 242 +++++++++++++++++++++++++++++++++++++
 9 files changed, 561 insertions(+), 133 deletions(-)
```

**VINCOLI VERIFICATI DA CI (job handoff-check):**
Il set di path sopra deve corrispondere esattamente a `git diff --name-only BASE..HEAD`.
`reports/ultima_risposta.md` è escluso dall'allowlist CI (committato dall'hook post fine-task).
I conteggi di righe sono approssimati per costruzione (handoff.md conta se stesso).

---

## §3 GIT LOG --ONELINE (sessione)

```
78b3a76 docs(fine-task): report + stato_progetto R-crm-1b fetta 4 (2026-07-27)
638c894 feat(crm): R-crm-1b fetta 4 — espone duplicati a doctor + CLI gas duplicati
5d9ae20 docs(fine-task): handoff + diff_sessione R-crm-1b fetta 3 (2026-07-27)
c8ab4be docs(fine-task): report + stato_progetto R-crm-1b fetta 3 (2026-07-27)
f6259eb feat(crm): R-crm-1b fetta 3 — dedup telefono (normalizza_telefono + rileva_duplicati_telefono)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun commit motore in questa sessione (zero diff su gas.py/brains/modules/tests/).

Il verdetto per i commit di sessione che toccano il motore (`f6259eb` e `638c894`) è riportato di seguito per completezza (incollato verbatim dai report delle sessioni precedenti):

**Commit f6259eb** — review #67 APPROVATO CON RISERVE

> Elementi esaminati:
> - `modules/memory/store.py:223` — `digits = re.sub(r"[^\d]", "", testo)` — rimozione di tutto il non-numerico (inclusi `+` interni): la lezione #49 della memoria (regex `[^\d+]` conservava i `+` producendo canonici con `+` interni) è stata recepita correttamente. Esito: **ok**.
> - `modules/memory/store.py:938` — `for raw in (r.get("chiave_norm"), r.get("contatto"))` — la lettura doppia cerca il telefono sia nella chiave normalizzata sia nel campo contatto. Il pattern è identico alla versione `rileva_duplicati_email` già revisionata in #57. Esito: **ok**.
> - `tests/test_unit_kernel.py:3472–3500` (T60k) — test fail-open: conforme alla sez. 5 di CLAUDE.md. Esito: **ok**.
> - `tests/test_unit_kernel.py:3438–3451` (T60i) — ramo `chiave_norm` della tupla non esercitato in nessun test T60: riserva R2.
>
> Riserve (non bloccanti):
> - R1 — `int(r["id"])` fuori try/except post-lettura. Non bloccante.
> - R2 — ramo `chiave_norm` non coperto dai test T60. Non bloccante.

**Commit 638c894** — review #68 APPROVATO CON RISERVE

> VERDETTO: APPROVATO CON RISERVE
>
> Il diff è tecnicamente corretto, rispetta la filosofia "robustezza > potenza, zero crash",
> non tocca run_turn/tools_schema/system prompt, non espone funzioni di scrittura CRM al
> modello, implementa correttamente il fail-safe §9 in entrambi i path (doctor e `duplicati_cmd`),
> e i 4 nuovi test T61a–T61d coprono i casi principali.
>
> Riserve da tracciare in `stato_progetto.md` (non bloccanti, commit consentito):
> - R1 — gas.py:1815: commento `# 11. CRM` fuori sequenza nel file rispetto a `# 9` e `# 10`. Cosmetico.
> - R2 — tests/test_unit_kernel.py:3622: condizione T61d con `or "Duplicati"` sempre vera — il test verifica no-crash ed exit 0 ma non asserisce strettamente il messaggio "non disponibile".

---

## §5 DELTA TEST DEL MOTORE

**Prima (main):** 250 PASS.
**Dopo (HEAD):** 276 PASS, 0 FAIL.
**Delta:** +26 test (T60a–T60m: 22 su dedup telefono; T61a–T61d: 4 su doctor CRM + duplicati_cmd).

Output riepilogo reale (run CI `30247532892`, unit-suite):
```
=== RIEPILOGO: 276 PASS, 0 FAIL ===
```

---

## §6 STATO CI

Output `gh run list -L 3`:
```
completed	failure	docs(fine-task): report + stato_progetto R-crm-1b fetta 4 (2026-07-27)	CI	feature/crm-dup-telefono	push	30247532892	45s	2026-07-27T07:49:18Z
completed	success	docs(fine-task): handoff + diff_sessione R-crm-1b fetta 3 (2026-07-27)	CI	feature/crm-dup-telefono	push	30242319126	39s	2026-07-27T06:18:41Z
completed	success	docs(fine-task): report + stato_progetto R-crm-1b fetta 3 (2026-07-27)	CI	feature/crm-dup-telefono	push	30241988037	51s	2026-07-27T06:12:31Z
```

**Mappatura commit → run:**

- `78b3a76` (docs fine-task fetta 4) → run `30247532892` ❌ FAILURE. Job `handoff-check` fallito: `gas.py` omesso da §2. Job `unit-suite`: 276 PASS, 0 FAIL ✅.
- `638c894` (feat motore fetta 4) → **nessuna run propria su questo SHA** (pushato nello stesso push di `78b3a76`). Contenuto incluso nell'albero testato dalla run `30247532892`.
- `5d9ae20` (docs handoff fetta 3) → run `30242319126` ✅ SUCCESS.
- `c8ab4be` (docs fine-task fetta 3) → run `30241988037` ✅ SUCCESS.
- `f6259eb` (feat motore fetta 3) → nessuna run propria. Contenuto incluso nell'albero testato da run `30241988037`.

**Commit di questa sessione** (docs fix handoff): run non ancora disponibile alla scrittura dell'handoff.

---

## §7 RISERVE APERTE

Da review #67 (f6259eb):
- **R1** — `int(r["id"])` fuori try/except in `rileva_duplicati_telefono` (non critico: SQLite garantisce INTEGER PK).
- **R2** — ramo `chiave_norm` non coperto da T60: nessun test con telefono come chiave primaria in coppia con telefono nel campo `contatto`.

Da review #68 (638c894):
- **R3** (ex #68-R1) — commento `# 11. CRM` in `doctor()` fuori sequenza rispetto a `# 9` / `# 10`. Cosmetico.
- **R4** (ex #68-R2) — condizione T61d con `or "Duplicati"` sempre vera: non asserisce strettamente "non disponibile".

Tutte tracciate in `reports/stato_progetto.md`.
