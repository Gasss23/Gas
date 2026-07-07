# REPORT — 2026-07-07 — Migrazione Groq gpt-oss-120b: fetta unica (4 punti)

## DECISIONI UMANE RICHIESTE

1. **GROQ_API_KEY mancante** — `GROQ_API_KEY` non trovata nell'ambiente (né .env nel progetto, né variabile Windows persistente). Fornirla per completare il PUNTO 2 (round-trip live) e sbloccare il revisore + commit motore.
2. **R-groq-dup architettura** — `"openai/gpt-oss-120b"` hardcoded in 3 file (`groq_brain.py`, `claude_brain.py`, `gemini_brain.py`). Fonte unica richiesta: `env GAS_GROQ_MODEL` con default o `config.py` dedicato. Decisione: dove definire il default? (NON importare da gas.py per rischio circular import.) Deferito a fetta separata, nessun impegno attuale.

---

## Esito per fetta

**FETTA UNICA — 4 punti**

### PUNTO 1 — `reasoning_effort: "low"` nei 3 brain
`FATTA` — aggiunto a tutti e tre i payload Groq:
- `brains/groq_brain.py`: payload principale `chat()`
- `brains/claude_brain.py`: payload Groq fallback (rung 2)
- `brains/gemini_brain.py`: payload Groq fallback (rung 3)
Nessun altro parametro toccato (temperature, timeout invariati).
**STATO**: uncommitted, in working tree. Attende round-trip live + revisore.

### PUNTO 2 — Round-trip reale con tool call
`SALTATA — GROQ_API_KEY non disponibile nell'ambiente al momento dell'esecuzione`
Nessun .env nel progetto. Variabile non presente né come env di sessione né come env Windows persistente. Round-trip NON eseguito. Conseguenza: R-groq-slash resta APERTO, doc marcate PENDING, revisore non ancora invocabile sul diff motore.

### PUNTO 3 — Doc oneste (roadmap.md, stato_progetto.md)
`FATTA` — rimosso "✅ CHIUSA (review #43)" da entrambi i file (non esisteva ancora nessun verdetto del revisore). Sostituito con stato reale:
- `roadmap.md` riga PROSSIMI PASSI: `🟡 migrazione codice fatta 2026-07-07; validazione live: PENDING`
- `roadmap.md` sezione Deprecazioni: `🟡 2026-07-07 — [...] validazione live [...] PENDING; review revisore PENDING`
- `stato_progetto.md`: header `Ultimo aggiornamento: 2026-07-07 (migrazione Groq gpt-oss-120b: codice ✅, validazione live PENDING)`
Grep su "review #43" → zero match nei doc.
**STATO**: uncommitted, incluso in questo commit di report.

### PUNTO 4 — Finding in stato_progetto.md
`FATTA` — tre operazioni:
- (a) **R-groq-slash** lasciato `🟡 APERTO PENDING` (punto 2 non completato; chiusura condizionale rispettata)
- (b) **R-groq-dup** aperto: `"openai/gpt-oss-120b"` triplicato hardcoded; fonte unica deferita a fetta separata, decisione umana richiesta
- (c) Nota TPM aggiunta: burst TPM 8K (< 12K llama) → fallthrough a OpenRouter più frequente = comportamento atteso, non regressione
**STATO**: uncommitted, incluso in questo commit di report.

---

## Anomalie

- **Nessun .env nel progetto**: il task assumeva `GROQ_API_KEY dal .env locale` ma non esiste né un .env né una variabile persistente Windows. Sviluppo possibilmente eseguito con keys impostate manualmente in sessione PowerShell (non persistenti). Suggerisco di documentare la procedura di setup keys per future sessioni.
- **Diff staged pre-esistente**: il diff delle brains e gas.py era già presente come working tree change prima di questa sessione (migrazione modello già fatta da una sessione precedente su branch separato, poi mergiata in main alle 14:41 di oggi via commit "Merge branch 'refactor/model-ids-fonte-unica'"). I `reasoning_effort` aggiunti ora si sommano a quel diff pre-esistente.
- **reports/verifica_fase25.md** untracked — non toccato in questa sessione, lasciato intatto.
