# Report R-crm-1b Fetta 4 — Esposizione duplicati a doctor + CLI

**Data**: 2026-07-27  
**Branch**: feature/crm-dup-telefono  
**Task**: R-crm-1b Fetta 4 — gas doctor sezione CRM + comando `gas duplicati`

---

## § ESITO FETTE

| Fetta | Descrizione | Stato |
|-------|-------------|-------|
| 1 | `rileva_duplicati_email()` in store.py + test T57 | ✅ CHIUSA (sessioni precedenti) |
| 2 | Idempotenza diario `sospetto_duplicato_email` + test T57h/i/j | ✅ CHIUSA (sessioni precedenti) |
| 3 | `normalizza_telefono` + `rileva_duplicati_telefono()` + test T60 | ✅ CHIUSA (sessione precedente) |
| 4 | `gas doctor` sezione CRM + comando `gas duplicati` | ✅ FATTA |

---

## § SCOPE RISPETTATO

**SOLA LETTURA**: le funzioni `rileva_duplicati_email()` e `rileva_duplicati_telefono()` (già esistenti, già revisionate) sono state chiamate senza modificarle. Nessuna chiamata a `unisci_contatti`, `unisci_contatti_con_snapshot` o funzioni che scrivono sul DB.

**VIETATO non violato**: nessun tool aggiunto al loop, nessuna modifica a `run_turn`, `tools_schema` o system prompt.

---

## § MODIFICHE EFFETTUATE

### `gas.py`

**1. `doctor()` — nuova sezione CRM** (dopo TASK B, vector store):
- Chiama `mem.rileva_duplicati_email()` e `mem.rileva_duplicati_telefono()` se `mem` è disponibile
- Conta le coppie: esito `WARN` se > 0 con messaggio `"N email, M telefono — usa: gas duplicati"`, esito `OK` se nessuno
- Se memoria assente/degradata: `OK` con `"non disponibile (memoria assente/degradata)"`
- Wrap in `try/except` → fail-safe §9 completo: mai crash, mai exit 1

**2. Nuova funzione `duplicati_cmd()`**:
- Comando `gas duplicati`: elenca le coppie sospette (email E telefono) in output leggibile
- Output strutturato: `[EMAIL] N coppia/e sospetta/e` + righe dettaglio, poi `[TELEFONO]`
- Fail-safe: memoria non disponibile → messaggio e return 0, mai crash
- Exit 0 sempre (informativo, non un errore)
- Zero token LLM, sola lettura

**3. `main()`**: aggiunto routing `gas duplicati` → `duplicati_cmd()`

---

## § TEST

**Suite eseguita (REALE, non simulata):**

```
276 PASS, 0 FAIL
```

### Nuovi test T61 (4 casi):

| Test | Descrizione | Esito |
|------|-------------|-------|
| T61a | doctor CRM: 1 coppia email + 1 coppia telefono → riga `[WARN]` | PASS |
| T61b | doctor CRM: DB vuoto (nessun duplicato) → riga `[OK] nessuno` | PASS |
| T61c | `duplicati_cmd`: lista email + telefono, exit 0 | PASS |
| T61d | `duplicati_cmd` fail-safe: DB corrotto → exit 0, nessun crash | PASS |

---

## § VERDETTO REVISORE (VERBATIM, review #68)

VERDETTO: APPROVATO CON RISERVE

Il diff è tecnicamente corretto, rispetta la filosofia "robustezza > potenza, zero crash",
non tocca run_turn/tools_schema/system prompt, non espone funzioni di scrittura CRM al
modello, implementa correttamente il fail-safe §9 in entrambi i path (doctor e `duplicati_cmd`),
e i 4 nuovi test T61a–T61d coprono i casi principali.

Riserve da tracciare in `stato_progetto.md` (non bloccanti, commit consentito):

- R1 — gas.py:1815: commento `# 11. CRM` fuori sequenza nel file rispetto a `# 9` (riga 1832)
  e `# 10` (riga 1849). Cosmetico.
- R2 — tests/test_unit_kernel.py:3622: condizione T61d con `or "Duplicati"` sempre vera
  — il test verifica no-crash ed exit 0 ma non asserisce strettamente il messaggio
  "non disponibile".

---

## § DIVIETI RISPETTATI (checklist)

- SOLA LETTURA: nessuna chiamata a `unisci_contatti` / `unisci_contatti_con_snapshot` / funzioni di scrittura
- NESSUN tool aggiunto al loop, `tools_schema` o system prompt non toccati
- `run_turn` non toccato
- Fail-safe §9 in entrambi i path (doctor e CLI)
- Exit code doctor invariato (WARN non causa exit 1)
- Revisore invocato prima del commit, verdetto VERBATIM qui incollato
- Test REALI eseguiti (276 PASS, 0 FAIL)

---

## § RISERVE APERTE (non bloccanti)

- **#68-R1** (cosmetica): commento `# 11. CRM` fuori sequenza rispetto a `# 9`/`# 10` in gas.py
- **#68-R2** (test): condizione T61d con `or "Duplicati"` sempre vera — non asserisce strettamente "non disponibile"
