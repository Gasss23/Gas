# Handoff — sessione 2026-07-09 (migrazione modello Groq + doc roadmap)

## §DECISIONI UMANE RICHIESTE
1. **🔴 Validazione a caldo migrazione Groq (R-groq41-2/3)** — NON eseguibile in questo ambiente cloud (manca `GROQ_API_KEY` + rete verso Groq). Da fare in ambiente con chiave: round-trip agentico reale su `openai/gpt-oss-120b` e conferma che il modello reasoning restituisca ancora `tool_calls` in formato OpenAI in `groq_brain.py` (unico brain che passa `tools_schema`). Worst case: quel rung degrada a solo-testo, fail-safe §9, nessun crash. Decisione/azione umana.
2. **📱 Sonda Claude Dispatch pendente** — validare pairing QR telefono↔desktop + un task doc-only da telefono; verificare ambiente Windows vs WSL, hook `review_gate`/`session_end` scattati, modello usato. Se OK, l'item "accesso dev da telefono" (item 2) si chiude senza bridge custom. Decisione/azione umana.
3. **🔴 BLOCCANTE FASE 5** (invariata): postazione locale assente (no clone, no WSL sul PC). S1 hardening VPS non eseguibile finché non c'è una postazione canonica. Vedi `stato_progetto.md` § Note operative VPS #4.
4. **Repo pubblico → privato prima di FASE 5** (invariata, registrata in `reports/raccomandazioni_aperte.md`). Decisione umana.
5. **Branch**: lavorato su `claude/phone-gas-development-10svqc` (dedicato, non main) per la regola harness "no push su branch diversi".

## Esito sonda / STOP-gate
- Nessuno STOP effettivo. A inizio sessione erano presenti 3 file motore modificati e non committati (`brains/*.py`) di origine ignota nel contesto: verificati via `git diff` — si sono rivelati una migrazione coerente del rung Groq (non un residuo spurio). Passati per il gate revisore e committati.
- Aggiunte roadmap fatte in modalità **add-only** su richiesta umana (nessuna sostituzione; eventuale duplicazione accettata e da riconciliare all'esecuzione della task). Mirage già presente → non duplicato.

## git diff --stat (sessione, `c67137e..fa212a6`)
```
 .claude/agents/memoria_revisore.md | 1 +
 brains/claude_brain.py             | 4 ++--
 brains/gemini_brain.py             | 7 ++++---
 brains/groq_brain.py               | 5 +++--
 reports/roadmap.md                 | 3 +++
 reports/stato_progetto.md          | 9 +++++----
 6 files changed, 18 insertions(+), 11 deletions(-)
```
Motore toccato: `brains/claude_brain.py`, `brains/gemini_brain.py`, `brains/groq_brain.py`.

## git log (commit della sessione)
```
fa212a6 docs(roadmap): Dispatch candidato accesso dev telefono, Telegram ridimensionato, PARK Cowork
cec8e9f chore(revisore): lezione #41 in memoria persistente (migrazione modello rung)
4137921 feat(brains): migra rung Groq a openai/gpt-oss-120b con reasoning_effort low
```

## Delta test motore
- **Suite non eseguita in questo ambiente cloud**: `bwrap` assente → i test sandbox/`run_command`/snapshot sono strutturalmente rossi qui (confine noto, `stato_progetto.md` § Note operative VPS #3); nessuna `GROQ_API_KEY` → il round-trip agentico live su Groq non è verificabile localmente. Validazione delegata a CI + ambiente con chiave (vedi §DECISIONI UMANE #1).
- Il diff motore è un cambio di sola stringa-modello + parametro `reasoning_effort` nel payload JSON, logica di controllo invariata (endpoint/headers/timeout/try-except identici). CI verde su `4137921` (vedi §CI).

## Revisore — verdetto INTEGRALE (review #41, incollato, non riassunto)

> ## Verdetto: APPROVATO CON RISERVE
>
> ### Cosa fa il diff
> Migrazione del rung Groq della cascata: `llama-3.3-70b-versatile` → `openai/gpt-oss-120b`, con aggiunta di `"reasoning_effort": "low"` al payload JSON, in `brains/claude_brain.py`, `brains/gemini_brain.py`, `brains/groq_brain.py`. In `claude_brain.py` aggiornata anche la label di stampa (cosmetica). Nessun'altra logica toccata.
>
> ### Correttezza tecnica — OK
> 1. **Model-id valido**: `openai/gpt-oss-120b` è effettivamente servito da GroqCloud (famiglia GPT-OSS 120B/20B). `reasoning_effort` (`low`/`medium`/`high`) è un parametro documentato e accettato dall'endpoint OpenAI-compatible di Groq per i modelli reasoning gpt-oss.
> 2. **Endpoint/headers/timeout invariati**: verificato bit-per-bit. URL `api.groq.com/openai/v1/chat/completions`, header Authorization/Content-Type, timeout (12s in groq_brain, 15s negli altri due) tutti immutati.
> 3. **Fail-safe §9 integro**: tutte e tre le chiamate restano dentro `try/except`:
>    - `groq_brain.py` (righe 35-47): except globale → `FakeMsg` d'errore; il non-200 (riga 37-38) ritorna `FakeMsg`, mai crash.
>    - `gemini_brain.py` (righe 62-73) e `claude_brain.py` (righe 75-81): blocco Groq in `try/except: pass` con fallback a valle.
>
>    Corollario importante: anche nel worst case in cui Groq rifiutasse `reasoning_effort` con un 400, il flusso degrada a non-200/except → fallback sul rung successivo, senza crash. Il rischio del nuovo parametro è quindi coperto dalla cintura §9.
>
> ### Riserve (non bloccanti, da tracciare)
> 1. **Doc-sync — §8 Model Awareness**: `reports/stato_progetto.md` riga 41 ("Pipeline provider") cita ancora `3. groq/llama-3.3-70b-versatile`. La sezione 8 CLAUDE.md impone di dichiarare i cambi di modello: aggiornare quella riga al nuovo `openai/gpt-oss-120b`. La label di stampa aggiornata in `claude_brain.py` è corretta ma non sostituisce l'aggiornamento del documento di stato. (roadmap.md non cita il model-id specifico → nessuna modifica lì.)
> 2. **Validazione dal vivo §7 non eseguibile in review**: manca `GROQ_API_KEY` e rete, quindi il round-trip agentico reale (specie il tool-calling) non è verificabile qui. L'esecuzione reale va delegata all'ambiente con chiave.
> 3. **Tool-calling su modello reasoning**: `brains/groq_brain.py` è l'unico che passa `tools_schema` (righe 31-33) e si aspetta `tool_calls` in formato OpenAI (riga 42). Con un modello reasoning + `reasoning_effort:low` va confermato a caldo che gpt-oss-120b restituisca ancora `tool_calls` nel formato atteso, altrimenti il ciclo agentico su quel rung degrada a solo-testo (comunque fail-safe, non crash).
>
> ### Osservazione fuori scope (pre-esistente, NON introdotta da questo diff)
> `groq_brain.py` riga 17 (`messages[:2] + messages[-6:]`) e `claude_brain.py` riga 36 (`messages[-8:]`) sono raw-slicing della history dentro i brain. Non violano direttamente §5 (che riguarda il `_get_window` del kernel) e non sono toccati da questa modifica, ma restano un debito da tenere a mente.
>
> Commit consentito (APPROVATO CON RISERVE): tracciare le riserve 1-3 in `stato_progetto.md`.

**Stato riserve**: R-groq41-1 (doc-sync) → ✅ chiusa in `4137921` (pipeline provider aggiornata). R-groq41-2/3 → aperte, tracciate in `stato_progetto.md`, delegate all'ambiente con chiave (§DECISIONI UMANE #1).

## CI (FETTA 1, `.github/workflows/ci.yml`)
- **run#92 su `4137921`** (commit motore, migrazione Groq): **SUCCESS** ✅ — la modifica al motore passa la CI.
- **run#93 su `cec8e9f`** (memoria revisore): **SUCCESS** ✅.
- **run#94 su `fa212a6`** (doc roadmap, HEAD): **queued/pending** al momento dell'handoff (doc-only, basso rischio).
