# REPORT — 2026-07-07 — Migrazione Groq gpt-oss-120b: fetta unica (4 punti)

## DECISIONI UMANE RICHIESTE

1. **GROQ_API_KEY mancante** — Non trovata nell'ambiente (né .env nel progetto, né variabile Windows persistente). Richiesta per completare il PUNTO 2 (round-trip live con tool call reale) e sbloccare il gate revisore + commit motore. Fornire con `$env:GROQ_API_KEY = "gsk_..."` in sessione oppure creare un `.env` nel progetto o impostarla come variabile Windows persistente.
2. **R-groq-dup architettura (decisione rimandabile)** — `"openai/gpt-oss-120b"` è ancora hardcoded nei brain fallback di `claude_brain.py` e `gemini_brain.py` (i payload Groq). Il refactor `model-ids-fonte-unica` ha già introdotto `MODEL_GROQ` in `brains/model_ids.py` — import banale, ma richiede decisione umana sullo scope della fetta. Deferito, nessun impegno attuale.

---

## Esito per fetta

**FETTA UNICA — 4 punti**

### PUNTO 1 — `reasoning_effort: "low"` nei 3 brain
`FATTA` — aggiunto a tutti e tre i payload Groq:
- `brains/groq_brain.py`: payload principale `chat()`
- `brains/claude_brain.py`: payload Groq fallback (rung 2)
- `brains/gemini_brain.py`: payload Groq fallback (rung 3)
Nessun altro parametro toccato (temperature, timeout invariati). I brain usano ora `MODEL_GROQ` dalla costante `brains/model_ids.py` (post-merge refactor).
**STATO**: uncommitted, in working tree. Attende round-trip live + revisore.

### PUNTO 2 — Round-trip reale con tool call
`SALTATA — GROQ_API_KEY non disponibile nell'ambiente al momento dell'esecuzione`
Nessun .env nel progetto. Variabile non presente né come env di sessione né come env Windows persistente. Round-trip NON eseguito. Conseguenza: R-groq-slash resta APERTO, doc marcate PENDING, revisore non ancora invocabile sul diff motore.

### PUNTO 3 — Doc oneste (roadmap.md, stato_progetto.md)
`FATTA` — rimosso "✅ CHIUSA (review #43)" da entrambi i file (verdetto non ancora esistente). Sostituito con stato reale: "migrazione codice fatta 2026-07-07; validazione live: PENDING". Grep "review #43" → zero match. Committato e pushato (`a1f503b`).

### PUNTO 4 — Finding in stato_progetto.md
`FATTA` — tre operazioni:
- (a) R-groq-slash lasciato `🟡 APERTO PENDING` (punto 2 non completato; chiusura condizionale rispettata)
- (b) R-groq-dup aperto: hardcoded triplicato nei brain fallback; deferito a fetta separata, decisione umana richiesta
- (c) Nota TPM aggiunta: burst TPM 8K (< 12K llama) → fallthrough a OpenRouter più frequente = comportamento atteso, non regressione
Committato e pushato (`a1f503b`).

---

## Anomalie

- **Nessun .env nel progetto**: il task assumeva `GROQ_API_KEY dal .env locale` ma non esiste né un .env né una variabile persistente Windows. Suggerisco di creare un `.env` o impostare la chiave come variabile Windows persistente per le sessioni future.
- **Merge remoto durante sessione**: il refactor `model-ids-fonte-unica` era già stato mergiato in main (commit `eb0509f`, ore 14:41) mentre questa sessione era in corso. Il merge ha introdotto `brains/model_ids.py` e cambiato i brain in modo significativo. Lo stash pop ha prodotto conflitti risolti mantenendo la struttura upstream (MODEL_GROQ costante) con aggiunta di `reasoning_effort`.
- **Latenza GAS** (segnalata dall'utente durante la sessione) — risposte ~5s più lente del solito. Registrata in roadmap.md come item non urgente (`2700f1f`).
- **reports/verifica_fase25.md** untracked — non toccato in questa sessione, lasciato intatto.
