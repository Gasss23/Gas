# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-22 — Sonda bug "phantom PR" in /fine-task

---

## §0 DECISIONI UMANE RICHIESTE

1. Creare PR per il branch `sonda/phantom-pr-bug` e mergiare su main (nessuna PR aperta al momento della scrittura — `gh pr list --head sonda/phantom-pr-bug` ritorna `[]`).
2. Approvare il fix proposto in `reports/ultimo_report.md §Punto 4` e autorizzare implementazione in fetta successiva.

*Nota meta: questo §0 dimostra il bug trovato — il template attuale richiederebbe di scrivere "Merge della PR #<numero>" ma siccome nessuna PR esiste, il numero sarebbe phantom. Scritto invece il fatto reale: "crea PR e mergia".*

---

## §1 SCOPE & ESITO FETTE

- **Punto 1 — Localizzare /fine-task**: `FATTA` — `.claude/commands/fine-task.md` (238 righe), unica definizione.
- **Punto 2 — Logica esatta "Merge PR #NN"**: `FATTA` — riga 65, REGOLA §0; root cause: assenza di `gh pr list` prima di scrivere il numero.
- **Punto 3 — Sonda ambiente**: `FATTA` — `gh` 2.96.0, autenticato, `gh pr list` ritorna `[]` (corretto).
- **Punto 4 — Fix proposto**: `FATTA` — snippet bash + riscrittura REGOLA §0 proposti, NON implementati.
- **Modifica codice**: `SALTATA — GATE DI STOP BLOCCANTE` (scope = sonda zero-modifica).

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  16 ++---
 reports/handoff.md        |  72 +++++--------------
 reports/stato_progetto.md |   3 +-
 reports/ultimo_report.md  | 176 +++++++++++++++++++++-------------------------
 4 files changed, 106 insertions(+), 161 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
00465bb docs(sonda): phantom PR bug — root cause isolata in fine-task.md REGOLA §0
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è stampato al passo 5.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

---

## §6 STATO CI

```
completed	success	docs(sonda): phantom PR bug — root cause isolata in fine-task.md REGO…	CI	sonda/phantom-pr-bug	push	32539819289	54s	2026-08-22T00:17:01Z
completed	success	Merge pull request #73 from Gasss23/feat/voice-client-4a	CI	main	push	32500841097	51s	2026-08-21T16:02:28Z
completed	success	docs(fine-task): handoff + diff_sessione Fetta 4a — probe_client_4a E…	CI	feat/voice-client-4a	push	32495474900	1m8s	2026-08-21T15:03:00Z
```

**Mappatura commit→run:**
- `00465bb` (docs(sonda): phantom PR bug…) → run `32539819289` — **SUCCESS** ✅
- Commit di fine-task (questo handoff) → nessuna run su questo SHA al momento della scrittura (run disponibile dopo il push).

---

## §7 RISERVE APERTE

- 🟡 **R-phantom-pr-1** (nuova, 2026-08-22): `.claude/commands/fine-task.md:65` — REGOLA §0 non ordina `gh pr list` prima di scrivere il numero PR → allucinazione phantom PR (3 occorrenze 2026-08-21). Fix proposto in `reports/ultimo_report.md §Punto 4`, non implementato. Attende decisione operatore.
