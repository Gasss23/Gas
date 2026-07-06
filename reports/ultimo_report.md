# Report — Aggiunta sezione "Deprecazioni provider" in roadmap.md

**Data:** 2026-07-06  
**Task:** Aggiungere nuova sotto-sezione `### Deprecazioni provider` in `reports/roadmap.md`

---

## Modifica effettuata

**File:** `reports/roadmap.md`  
**Posizione:** in coda alla sezione `### 🟡 PROSSIMI PASSI`, prima di `### 🗂️ FASE 2.5`

**Righe aggiunte (verbatim):**

```
### Deprecazioni provider

- 2026-08-16 — Groq llama-3.3-70b-versatile (rung 3) in pensione: migrare a groq/qwen3-27b (o nome modello Groq ufficiale da verificare al momento della migrazione). Trigger: comunicazione ufficiale Groq. Azione: aggiornare RUNG_3_MODEL in configurazione + test round-trip.
```

## Motivazione posizionamento
La sezione PROSSIMI PASSI conteneva già l'item Groq come priorità #1 — sezione più pertinente. Nessuna sezione "Deprecazioni" preesistente → creata come nuova sotto-sezione.

## Esito
- ✅ `reports/roadmap.md` aggiornato
- ✅ Nessun altro file toccato
