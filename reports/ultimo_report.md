# R-crm-1b Fetta 1 — Comando CLI `gas merge-contacts` + fix hint

**Branch**: feature/crm-dup-detect
**Commit**: 9515626
**Data**: 2026-07-14

---

## SONDA

### (a) `unisci_contatti` in `store.py` (riga 428)
- **Transazionale**: un unico `with self._connect() as con:` — tutti e 3 gli UPDATE nella stessa transazione SQLite con rollback automatico su eccezione. ✓
- **Campi fusi via COALESCE**: nome, contatto, prossima_azione, note
- **Lapide**: `da` marcato con `merged_into = canonico_id` (non cancellato mai)
- **NON scrive nel diario**: nessun snapshot di `da`, nessun evento merge
- **Nessuna preview**: esegue il merge direttamente
- **Conclusione**: meccanismo corretto, mancava la rete di sicurezza (snapshot diario atomico)

### (b) Hint in `check_dups_cmd` (riga 2176)
- Stampava `_unisci_contatti` con underscore — metodo interno Python, non invocabile da CLI. Sbagliato.

---

## IMPLEMENTATO

### 1. `modules/memory/store.py` — `unisci_contatti_con_snapshot()`

Nuovo metodo (NON tocca `unisci_contatti` esistente) che fa tutto in **UN'unica transazione SQLite**:

1. Legge `da` e `verso` (entrambi devono esistere → None se mancano)
2. Calcola preview: campi da riempire e conflitti (verso vince su entrambi valorizzati e diversi)
3. **RETE DI SICUREZZA** (PRIMA di qualsiasi UPDATE):
   - INSERT `merge_snapshot`: snapshot integrale JSON di `da` nel diario
   - INSERT `merge_evento`: riepilogo campi riempiti e conflitti
4. UPDATE COALESCE su `verso` (riempie i NULL da `da`)
5. Re-punta le lapidi precedenti da `da` a `verso`
6. Marca `da` come lapide (`merged_into = canonico_id`)
7. COMMIT

**Garanzia FAIL-SAFE**: se il diario INSERT fallisce → eccezione SQLite → rollback automatico → rubrica invariata → restituisce `None`.

Ritorna `dict {canonico_id, campi_riempiti, conflitti, no_op}` oppure `None` in degrado.

### 2. `gas.py` — `merge_contacts_cmd()`

Comando **solo umano** (NON tool agente, non in `execute_tool_call`, non in `tools_schema`):

```
gas merge-contacts <chiave_da> <chiave_verso> [--yes]
```

Flow:
1. Verifica esistenza di entrambe le chiavi (errore chiaro se mancante)
2. **Preview** obbligatoria: mostra entrambi i record, campi che verranno riempiti, conflitti con valore scartato esplicitato
3. Conferma interattiva `y/N` (default N; `--yes` per saltare)
4. Chiama `mem.unisci_contatti_con_snapshot()` — atomico con rete di sicurezza
5. Stampa SUCCESSO con dettaglio valori scartati (se conflitti)

### 3. `gas.py` — Fix hint `check_dups_cmd`

Prima: `Fondere con: _unisci_contatti.`
Dopo: `Fondere con: gas merge-contacts <da> <verso>.`

### 4. `gas.py` — Routing in `main()`

```python
if len(sys.argv) > 1 and sys.argv[1] == "merge-contacts":
    sys.exit(merge_contacts_cmd())
```

---

## TEST REALI — T58 (6/6 PASS)

| Test | Scenario | Risultato |
|------|----------|-----------|
| T58a | Merge riuscito: campi vuoti di `verso` riempiti da `da`, `verso` sopravvive | PASS |
| T58b | Conflitto: `verso` vince su `nome`, valore scartato di `da` nel result | PASS |
| T58c | Diario: `merge_snapshot` e `merge_evento` presenti, snapshot contiene JSON di `da` | PASS |
| T58d | Chiave inesistente → None, rubrica invariata | PASS |
| T58e | FAIL-SAFE: tabella diario droppata → None, `merged_into` resta NULL per entrambi | PASS |
| T58f | Fix hint: output di `check_dups_cmd` contiene `merge-contacts`, non `_unisci_contatti` | PASS |

---

## VERDETTO REVISORE

**APPROVATO CON RISERVE** — due fix cosmetici applicati prima del commit:
1. f-string mancante in `gas.py:2282` (stampava nome variabile letterale) → corretta
2. Variabile `id_carla` non usata in T58c → rimossa

---

## STOP GATE RISPETTATI

- SOLO Fetta 1: non toccata idempotenza diario (fetta 2) né telefono (fetta 3)
- merge NON esposto come tool dell'agente in nessuna forma
- Diario: solo append (INSERT), mai rewrite/delete
- `unisci_contatti` esistente NON modificato (aggiunto `unisci_contatti_con_snapshot` separato)
- Branch → PR prevista; mai push diretto su main
