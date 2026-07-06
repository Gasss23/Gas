# Report — Sez. 10 CLAUDE.md convertita in puntatore a roadmap.md

**Data:** 2026-07-06
**Scope:** doc-only, sez. 10 CLAUDE.md. Nessuna modifica al motore. Niente revisore, niente test.
**Branch:** `docs/sez10-puntatore-roadmap`

---

## Esito sonda (obbligatoria)

Confronto sez. 10 CLAUDE.md vs `reports/roadmap.md`:

| Elemento in sez. 10 | Presente in roadmap.md |
|---|---|
| FASE 1 ✅ CHIUSA | ✅ sez. FASE 1, dettagliata |
| FASE 2 ✅ CHIUSA | ✅ sez. FASE 2, dettagliata |
| FASE 2.5 ✅ CHIUSA | ✅ sez. FASE 2.5 con review #39 / commit 65c4c7b |
| FASE 3 futura | ✅ sez. FASE 3 |
| FASE 4 futura | ✅ sez. FASE 4 |
| FASE 5 🟡 IN CORSO S1+S1b | ✅ sez. FASE 5 con S1 ✅ / S1b ✅ / prossimo S2 |
| Item 1 — Spesa token | ✅ ITEM APERTI CHIUSI + dettaglio cap giornaliero |
| Item 2 — Telegram dual-control | ✅ sezione "Idee da valutare" |
| Item 3 — R-wire-1 VEC_MIN_SIM | ✅ PROSSIMI PASSI / FASE 5 entry |
| Item 4 — Task scheduler autonomo | ✅ sez. FASE 4.5 dettagliata |
| Item 5 — Video learning | ✅ sezione "Idee da valutare" |

**Verdetto:** `reports/roadmap.md` è il superset completo. Nessuna informazione unica in sez. 10. Condizione necessaria soddisfatta — sostituzione eseguita.

**Nota struttura CLAUDE.md:** sez. 11 (DISCIPLINA TOKEN) si trova alle righe 51-59, PRIMA della sez. 10 (righe 61-77, ultima del file). La sostituzione ha toccato solo righe 61-77, nessun rischio di tagliare materiale di altre sezioni.

---

## Modifica applicata

**Header:** `## 10. ROADMAP — SOMMARIO` → `## 10. ROADMAP`

**Contenuto sostituito (rimosso):**
- Lista 6 fasi con stato
- "Item aperti TOP" con 5 voci
- Riga "Dettaglio completo, completati storici e priorità: reports/roadmap.md"

**Contenuto nuovo (stub):**
```
## 10. ROADMAP

La roadmap completa — fasi e loro stato, item aperti, priorità, completati storici —
vive in `reports/roadmap.md` (fonte unica autorevole).
Questa sezione NON riporta stato per-fase di proposito: un sommario duplicato va fuori
sync con la fonte. Per lo stato del giorno: `reports/roadmap.md` + `reports/stato_progetto.md`.
```

---

## Derive rilevate FUORI SCOPE (non corrette — decisione all'umano)

**A. Stato inconsistente negli "Item aperti TOP" rimossi**
Alcuni item avevano etichette di stato obsolete rispetto a `roadmap.md`:
- Item 1 (Spesa token): marcato 🔴 in sez. 10, ma ✅ chiuso in roadmap.md (runtime cap implementato; il problema residuo è disciplina dev, non una feature mancante).
- Item 3 (R-wire-1): marcato come residuo aperto in sez. 10, ma il tool `gas calibrate-vectors` è ✅ chiuso in roadmap.md (resta solo taratura al deploy VPS).

Questi item spariscono con la conversione; la loro fonte autorevole resta `roadmap.md`.

**B. Riga 1 di `reports/roadmap.md` fa ancora riferimento a CLAUDE.md come co-fonte**
Il file apre con: `"Sommario e stato corrente in CLAUDE.md e reports/stato_progetto.md."` — dopo questa modifica, CLAUDE.md non ha più un sommario, solo un puntatore. La riga andrebbe aggiornata in `roadmap.md` per riflettere il nuovo ruolo di CLAUDE.md sez. 10.

---

## Verifica finale

Righe toccate in CLAUDE.md: **17 rimosse + 5 nuove** — solo sez. 10.
Sez. 11 e tutte le altre sezioni: **non toccate**.
`reports/roadmap.md`: **non toccato**.
