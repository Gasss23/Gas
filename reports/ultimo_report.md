# R-crm-1b Fetta 1 — Comando CLI `gas merge-contacts` + fix hint

**Data**: 2026-07-14
**Branch**: feature/crm-dup-detect
**Commit motore**: 9515626

---

## DECISIONI UMANE RICHIESTE

Nessuna.

---

## SCOPE & ESITO FETTE

- **Fetta 1 — comando CLI `gas merge-contacts <da> <verso>`**: `FATTA`
  Implementato con preview, conferma interattiva y/N, rete di sicurezza (snapshot diario atomico), fail-safe §9.
- **Fix hint `check_dups_cmd`**: `FATTA`
  Da `_unisci_contatti` a `gas merge-contacts <da> <verso>`.
- **Fetta 2 — idempotenza diario**: `DEFERITA — fuori scope fetta 1, nessuna modifica`
- **Fetta 3 — telefono**: `DEFERITA — fuori scope fetta 1, nessuna modifica`

---

## SONDA (pre-implementazione)

### `unisci_contatti` in `store.py` (riga 428)
- Transazionale: unico `with self._connect() as con:` — rollback automatico su eccezione. ✓
- Campi fusi via COALESCE: nome, contatto, prossima_azione, note
- Lapide: `da` marcato con `merged_into = canonico_id` (non cancellato)
- NON scrive nel diario: mancava snapshot di `da` e evento merge
- Nessuna preview: eseguiva il merge direttamente
- **Conclusione**: meccanismo corretto, mancava la rete di sicurezza

### Hint in `check_dups_cmd` (riga 2176)
- Stampava `_unisci_contatti` — metodo interno Python, non invocabile da CLI.

---

## IMPLEMENTAZIONE

### `modules/memory/store.py` — `unisci_contatti_con_snapshot()`

Nuovo metodo (NON tocca `unisci_contatti` esistente). Tutto in **un'unica transazione SQLite**:

1. Legge `da` e `verso` (→ None se mancano)
2. Calcola preview: campi da riempire, conflitti (verso vince)
3. **RETE DI SICUREZZA** PRIMA di qualsiasi UPDATE:
   - INSERT `merge_snapshot`: snapshot integrale JSON di `da` nel diario
   - INSERT `merge_evento`: riepilogo campi e conflitti
4. UPDATE COALESCE su `verso`
5. Re-punta lapidi precedenti da `da` a `verso`
6. Marca `da` come lapide
7. COMMIT

Se il diario INSERT fallisce → eccezione → rollback automatico → rubrica invariata → restituisce `None`.

### `gas.py` — `merge_contacts_cmd()`

Comando solo umano (NON tool agente, non in `execute_tool_call`/`tools_schema`):

```
gas merge-contacts <chiave_da> <chiave_verso> [--yes]
```

Preview obbligatoria → conferma y/N (default N) → merge atomico.

### `gas.py` — Fix hint e routing

- `check_dups_cmd`: hint corretto a `gas merge-contacts <da> <verso>`
- `main()`: routing `merge-contacts` aggiunto

---

## TEST REALI — T58 (6/6 PASS, CI verde)

| Test | Scenario | Risultato |
|------|----------|-----------|
| T58a | Merge riuscito: campi vuoti di `verso` riempiti da `da` | PASS |
| T58b | Conflitto: `verso` vince, valore scartato di `da` nel result | PASS |
| T58c | Diario: `merge_snapshot` + `merge_evento` presenti con JSON di `da` | PASS |
| T58d | Chiave inesistente → None, rubrica invariata | PASS |
| T58e | FAIL-SAFE: tabella diario droppata → None, `merged_into` resta NULL | PASS |
| T58f | Fix hint: `check_dups_cmd` output contiene `merge-contacts` | PASS |

---

## VERDETTO REVISORE

**APPROVATO CON RISERVE** — due fix cosmetici applicati prima del commit:
1. f-string mancante in `gas.py:2282` → corretta
2. Variabile `id_carla` inutilizzata in T58c → rimossa

---

## STOP GATE RISPETTATI

- SOLO Fetta 1: non toccata idempotenza diario (fetta 2) né telefono (fetta 3)
- merge NON esposto come tool agente in nessuna forma
- Diario: solo append (INSERT), mai rewrite/delete
- `unisci_contatti` esistente NON modificato
- Branch → PR necessaria per arrivare su main (lucchetto attivo)
