# REPORT TASK — R-crm-1b Fette 2+3

**Data:** 2026-07-14  
**Branch:** feature/crm-dup-detect  
**Task:** R-crm-1b — Fetta 2 (idempotenza diario) + Fetta 3 (telefono)  

---

## ESITO

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| Fetta 2 | Idempotenza diario `rileva_duplicati_email` | ✅ FATTA |
| Fetta 3 | Normalizzazione telefono + `rileva_duplicati_telefono` | ✅ FATTA |

---

## SONDA PREVENTIVA (pre-codice)

**Fetta 2 — idempotenza:**
- `rileva_duplicati_email` (store.py) chiamava `self.append_diario(...)` direttamente per ogni coppia trovata, senza verificare se la coppia era già nel diario. Ogni run ri-appendeva gli stessi sospetti.
- Finding R1 (INSERT OR REPLACE aggirava trigger): confermato latente ma SEPARATO dall'idempotenza. Non toccato (scope STOP GATE 2).

**Fetta 3 — telefono:**
- Campo `contatto` è TEXT unstructured (confermato: `contatto TEXT,` nel DDL). Nessun campo phone/email separato.
- Schema `_is_email` / `rileva_duplicati_email` è il modello da replicare.

---

## MODIFICHE EFFETTUATE

### `modules/memory/store.py`

1. **`normalizza_telefono(valore)` (funzione modulo, pura, idempotente):**
   - Strip separatori (spazi/trattini/punti/parentesi)
   - Equivalenza `+` e `00` iniziali (ITU-T)
   - Aggiunta automatica prefisso Italia (`39`) per numeri locali a 9-10 cifre che iniziano con `0` o `3`
   - Strip difensivo `re.sub(r"\D", "", digits)` per `+` interni da input patologici (riserva R1 revisore)
   - Range valido: 9-15 cifre (E.164). Fail-safe §9: `None`/fuori range → `""`

2. **`_is_phone(valore)` (metodo statico MemoryStore):**
   - Delegato a `normalizza_telefono` (non vuoto → valido). Puro, fail-safe.

3. **`_append_sospetto(tipo, descrizione_base, id_a, id_b)` (metodo privato MemoryStore):**
   - Helper condiviso da `rileva_duplicati_email` e `rileva_duplicati_telefono`
   - Tag `[ids:X,Y]` (X < Y) nella descrizione: permette check idempotente via `LIKE '%[ids:X,Y]%'`
   - `[`, `]`, `,` NON sono wildcard in SQLite LIKE → nessun falso positivo
   - SELECT + INSERT in connessione unica (atomico)
   - FAIL-SAFE: errore nel check → `log.warning` + skip (no duplicato, no crash)

4. **`rileva_duplicati_email` (modificata):**
   - Usa `_append_sospetto` invece di `append_diario` diretto
   - Stesso sospetto già nel diario → zero nuove righe (idempotente)
   - Logica di rilevamento invariata

5. **`rileva_duplicati_telefono` (nuovo):**
   - Speculare a `rileva_duplicati_email`
   - Usa `normalizza_telefono` sul campo `chiave_norm` e `contatto`
   - Tipo diario: `sospetto_duplicato_telefono`
   - Idempotente (via `_append_sospetto`)
   - Fail-safe §9: lapidi escluse, memoria degradata → `[]`

### `modules/memory/__init__.py`

- Aggiunto `normalizza_telefono` agli export pubblici

### `gas.py` — `check_dups_cmd`

- Chiama ora sia `rileva_duplicati_email` che `rileva_duplicati_telefono`
- Output separato per email e telefono con sezioni WARN distinte
- Messaggio OK aggiornato: "nessun sospetto duplicato trovato (email né telefono)"

### `tests/test_unit_kernel.py`

**T59 — Idempotenza diario (Fetta 2):**
- T59a: stesso sospetto email 2 volte → 1 sola riga diario
- T59b: sospetti email diversi → righe distinte nel diario
- T59c: tag `[ids:X,Y]` presente nella descrizione del sospetto

**T60 — Telefono (Fetta 3):**
- T60a: `normalizza_telefono` — 5 forme diverse → stesso canonico
- T60b: due contatti stesso numero normalizzato → coppia segnalata + riga diario
- T60c: numeri diversi → nessun falso positivo
- T60d: contatti senza numero → nessun falso positivo
- T60e: idempotenza diario telefono — stesso sospetto 2 volte → 1 sola riga
- T60f: `check_dups_cmd` include risultati telefono nel report CLI

---

## RISULTATO SUITE

```
CI run 29342632131: 240 PASS, 0 FAIL
```

Delta: +9 test (T59a/b/c + T60a-f). Locale Codespace conta 242 per T9a/T9c con API keys — CI è la fonte autorevole.

---

## VERDETTI REVISORE (review #49)

### Fetta 2 — APPROVATO CON RISERVE

> Il meccanismo `_append_sospetto` è tecnicamente corretto: tag normalizzato (min,max), LIKE letterale sicuro su SQLite, SELECT+INSERT in connessione unica, exception handler completo. I test T59a/b/c coprono correttamente i tre casi. Riserva: errore di documentazione nel docstring ("LIKE ... sul tipo" invece di "sulla descrizione") — non bloccante.

Riserva applicata prima del commit.

### Fetta 3 — APPROVATO CON RISERVE

> `normalizza_telefono` è fail-safe e idempotente; `rileva_duplicati_telefono` è strutturalmente speculare a quella email. T60a-f coprono normalizzazione, detection, falsi positivi, idempotenza. Riserve: (R1) regex `[^\d+]` lascia `+` interni su input patologici — aggiungere `re.sub(r"\D", "", digits)` dopo gestione prefisso; (R2) import ridondanti T60 — cosmetico.

Riserva R1 applicata. R2 non applicata (cosmetica).

---

## INVARIANTI RISPETTATE

- Diario APPEND-ONLY e IMMUTABILE: idempotenza = NON scrivere il duplicato, mai riscrivere/cancellare (§6). ✅
- FAIL-SAFE §9: errore nel check → log + skip, mai crash. ✅
- STOP GATE 2 rispettato: R1/hardening diario NON toccato, sonda Dispatch telefono NON toccata. ✅
- main-lock: modifiche su feature/crm-dup-detect. ✅
