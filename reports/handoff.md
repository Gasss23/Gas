# Handoff — feat/cancello-c4a — 2026-10-03

---

## §DECISIONI UMANE RICHIESTE

1. **Merge PR feat/cancello-c4a**: Fare PR e merge quando ritenuto opportuno. `gasmerge` (no push diretto su main).
2. **R-c4a-1 dedup**: Decidere se e quando implementare dedup coda prima del deploy autonomo.
3. **C4b priorità**: Confermare che C4b (Telegram + read-back + esecuzione post-approvazione) sia il prossimo passo del cancello.

---

## §1 — Esito sonda (PASSO 0)

Nessun conflitto §4 vs prompt C4a. §4b descrive il flusso completo (incluso Telegram); C4a implementa solo la prima metà (parking nel DB + esito fisso). Il prompt era esplicito e coerente. Nessun blocco, nessuna riserva di scope rilevata.

---

## §2 — git diff --stat (main → feat/cancello-c4a)

```
.claude/agents/memoria_revisore.md |   2 +
gas.py                             |  48 +++++--
modules/memory/store.py            |  19 ++-
tests/test_unit_kernel.py          | 267 ++++++++++++++++++++++++++++++++++---
4 files changed, 304 insertions(+), 32 deletions(-)
```

---

## §3 — git log (commit sessione)

```
766c0ee fix(cancello-c4a): R-c3-1b + collegamento coda al loop — review #127 APPROVATO CON RISERVE
cce2211 chore(revisore): memoria review #127 — APPROVATO CON RISERVE
```

---

## §4 — Verdetto revisore INTEGRALE (review #127)

## VERDETTO REVIEW #127 — feat/cancello-c4a

**APPROVATO CON RISERVE**

---

### Letture obbligatorie eseguite

CLAUDE.md §5 (antipatterns), §8 (guardrail API), §10 (roadmap) — letti dalla system prompt. `reports/stato_progetto.md` — letto integralmente. `.claude/agents/memoria_revisore.md` — letto integralmente (ultima entry #126, prossimo #127).

---

### Elementi del diff esaminati

**1. `gas.py:1942` — inizializzazione `_gate_pending_id`**
Cosa fa: `_gate_pending_id: Optional[str] = None` dichiarato PRIMA del blocco if/elif/else.
Rischio esaminato: riferimento a variabile non definita nel ternario del diario (riga 1994) se fosse dentro il ramo elif.
Esito: **OK** — inizializzazione corretta, sempre valutabile.

**2. `gas.py:1950–1966` — try/except attorno a `enqueue_approval` + catena FAIL-CLOSED**
Cosa fa: chiama `enqueue_approval` o ritorna None se `self.memory is None`; su eccezione `_gate_pending_id = None`; guardia `if _gate_pending_id is None` (riga 1967) chiude con diniego.
Rischio esaminato: (a) tool eseguito su eccezione enqueue — impossibile, `execute_tool_call` è nel ramo `else` separato; (b) memory=None non gestita — gestita nell'espressione condizionale; (c) eccezione propagante — catturata dall'except generico.
Esito: **OK** — catena fail-closed a tre livelli verificata da T74e (enqueue lancia) e T74f (memory=None).

**3. `store.py:1611–1629` — due UPDATE in transazione + trigger analysis**
Cosa fa: primo UPDATE scade righe con `typeof(ts_expiry) NOT IN ('real', 'integer')`; secondo scade righe con `ts_expiry <= now`; `con.commit()` unico dopo entrambi.
Rischio esaminato: (a) `approvals_stato_immutabile` (WHEN OLD.stato != 'pending') — entrambi i WHERE matchano solo 'pending' → non scatta; (b) `approvals_payload_immutabile` (WHEN payload columns cambiano) — i due UPDATE cambiano solo stato/ts_resolved/risolto_da, nessun campo trigger → non scatta; (c) atomicità: context manager `with con:` rollback su eccezione; (d) doppio conteggio: return `int(cur.rowcount) + n_bad` corretto, le righe scadute dal primo UPDATE non sono più 'pending' e il secondo non le ri-tocca.
Esito: **OK**

**4. `tests/test_unit_kernel.py` (area T74a) — spy + check diario F-diario-eco/args**
Cosa fa: verifica che send_email NON sia nella lista calls, che il diario contenga "pending id=" ma non "@example.com".
Rischio esaminato: se `_riassumi_args` fosse invocato per il pending branch (regressione), l'indirizzo email apparirebbe nel diario e il check cadrebbe.
Esito: **OK** — il test è mordace sulla regola F-diario-eco/args.

**5. `tests/test_unit_kernel.py` — T74g (grep stub C2)**
Cosa fa: `"C2 stub" not in _src74g and "GATE-C2-STUB" not in _src74g` — verifica assenza residui stub.
Esito: **OK** — confermato leggendo gas.py:1949.

---

### Antipattern Wall of Shame — nessuna violazione

- Nessun raw history slicing nel diff.
- Nessuna simulazione di tool output.
- `_get_window()` non toccato.
- `for _ in range(10)` invariato.
- FUORI SCOPE rispettato: nessuna modifica a Telegram, read-back, firma/hash, esecuzione post-approvazione.

---

### RISERVE APERTE

**R-c4a-1** (minore): F-c4a-dedup non corretto in C4a. Un modello che ripete la stessa chiamata IRREVERSIBLE nelle 10 iterazioni di un turno può creare fino a 9 righe pending identiche. Il finding è misurato da F-c4a-dedup (3 enqueue identici → 3 UUID distinti). Correzione esplicitamente fuori scope C4a. Da tracciare in `reports/stato_progetto.md` come finding aperto.

**R-c4a-2** (cosmetica): UUID duplicato nel diario per il path pending — la riga diventa `pending id=<uuid> | [OK] Azione in attesa di approvazione umana (ID: <uuid>)`. Nessun impatto funzionale.

---

### Rischio esplicitamente escluso

Comportamento dei trigger su DB legacy (schema senza trigger pre-C3): non verificabile senza snapshot del DB di produzione. Non è un rischio introdotto da questa fetta.

---

### Verifica risultati test

501 PASS, 5 FAIL solo F-mac-1 (bwrap macOS, già documentato): coerente con la traiettoria C3 (472 PASS) + delta ~29 nuovi check. Pytest 227/227 PASS confermato.

---

**VERDETTO FINALE: APPROVATO CON RISERVE**

Le riserve R-c4a-1 e R-c4a-2 sono NON bloccanti. Il commit è consentito. Tracciare R-c4a-1 in `reports/stato_progetto.md` come finding aperto prima del deploy autonomo.

---

## §5 — Delta test motore

| Suite | Prima | Dopo | Delta |
|-------|-------|------|-------|
| python3 test_unit_kernel.py | 472 PASS, 5 FAIL | 501 PASS, 5 FAIL | +29 PASS |
| pytest (escluso kernel) | 227 PASS | 227 PASS | 0 |

---

## §6 — Stato CI

CI non ancora lanciata (branch non pushato). La pipeline `ci.yml` (`unit-suite`) girerà su PR. Gli unici FAIL attesi sono i 5 di F-mac-1 (bwrap non disponibile su GitHub Actions macOS runner) — già documentati e invariati.

---

## §7 — Prossimi passi consigliati

1. PR feat/cancello-c4a → merge su main (via gasmerge)
2. C4b: bridge Telegram per le approvazioni (turno suddiviso lato bot)
3. Eventuale fix R-c4a-1 dedup prima del deploy autonomo
