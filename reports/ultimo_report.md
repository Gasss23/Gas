# R-crm-1b Fetta 1 — Rilevamento duplicati email

**Sessione:** feature/crm-dup-detect — 2026-07-14
**Scope:** implementazione rilevatore duplicati email cross-campo. NESSUNA fusione automatica.
**Review:** #47 — APPROVATO CON RISERVE (riserve minori tracciate in stato_progetto.md)

---

## Cosa è stato fatto

### 1. `modules/memory/store.py` — rilevatore sola lettura

**`_is_email(valore)`** (staticmethod, puro, fail-safe):
- Pattern minimale: almeno 1 char prima di `@`, dominio con punto e TLD non vuoto
- Mai solleva, ritorna `False` su qualsiasi input malformato

**`rileva_duplicati_email() → List[Dict]`**:
- Legge tutti i contatti VIVI (`merged_into IS NULL`)
- Estrae email da `chiave_norm` e da `contatto` per ogni scheda, normalizzate con `normalizza_chiave`
- Costruisce indice `email → {id: scheda}` (dedup per id all'interno della stessa email)
- Per ogni email con ≥2 contatti distinti → coppia sospetta
- Per ogni coppia: `append_diario("sospetto_duplicato_email", "sospetto duplicato: ... (email ...)")`
- Ritorna lista `[{chiave_a, id_a, chiave_b, id_b, email}]`
- Fail-safe §9: `[] in degrado`, never raises

### 2. `gas.py` — comando CLI

**`check_dups_cmd(root_dir)`**:
- `gas check-dups` dalla shell
- Instanzia MemoryStore, chiama `rileva_duplicati_email()`, stampa rapporto
- Exit 0 in entrambi i casi (OK: nessun duplicato; WARN: coppie trovate)
- Exit 1 solo se memoria non disponibile
- NON esposto al loop LLM (non in `tools_schema`, non in `execute_tool_call`)

### 3. `tests/test_unit_kernel.py` — T57 (7 test)

| Test | Caso | Esito |
|---|---|---|
| T57a | match cross-campo `chiave↔contatto` + segnalazione nel diario | PASS |
| T57b | stessa email come chiave → già fusi → nessun falso segnale | PASS |
| T57c | nomi identici senza email → nessun segnale | PASS |
| T57d | fail-safe DB corrotto → `[]` senza crash | PASS |
| T57e | lapidi escluse → nessuna falsa coppia | PASS |
| T57f | match cross-`contatto` (stessa email in campo libero) | PASS |
| T57g | CLI `check_dups_cmd`: OK e WARN stampati correttamente | PASS |

---

## Verdetto revisore #47

**APPROVATO CON RISERVE**

Riserva bloccante (corretta prima del commit): `nota` → `note` in T57b.

Riserve minori tracciate in `stato_progetto.md`:
- Re-entry diario su invocazioni ripetute (accettabile per audit log)
- Messaggio CLI `_unisci_contatti` → da correggere in `unisci_contatti` (cosmetic, fetta successiva)

---

## Vincoli rispettati

- GAS NON fonde mai autonomamente (zero merge in questo diff)
- Diario immutabile: solo `append_diario`, zero UPDATE/DELETE
- `unisci_contatti` non esposto al loop (confermato: dispatcher invariato)
- Fail-safe §9: `[]` in degrado su DB corrotto/assente

---

## Cosa resta aperto

- Fetta 2 (telefono): normalizzazione numero telefonico + match cross-campo
- Fetta 3 (nome): somiglianza fuzzy (da decidere con l'operatore prima di implementare)
- Riserva cosmetic: messaggio CLI `_unisci_contatti` → `unisci_contatti`

---

*La sonda (Fetta 0) è in git come commit `b99c1f1`. Questo report sovrascrive il precedente.*
