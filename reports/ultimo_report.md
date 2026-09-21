# Report task: RE-VERIFICA regola lingua italiana

**Data:** 2026-09-21
**Branch:** docs/reverifica-lang-rule
**Tipo:** Re-verifica (task originale già completato in commit 32dd6c2 / PR #92)

---

## DECISIONI UMANE RICHIESTE

Nessuna. Tutto funziona.

---

## PASSO 1 — SONDA (sola lettura)

### Istruzioni lingua attuali

**gas.py:48** (`_GAS_SYSTEM_PROMPT_BASE`):
```
"- LINGUA: Rispondi SEMPRE in italiano, dal primo messaggio, anche se l'utente scrive in un'altra lingua. Sii conciso e diretto.\n"
```

**gas_identity.md:1**:
```
LINGUA: Rispondi SEMPRE in italiano, dal primo messaggio, anche se l'utente scrive in un'altra lingua.
```

### Punto condiviso da tutti i rung

`_GAS_SYSTEM_PROMPT_BASE` in `gas.py` è il prompt base iniettato come `system` in ogni chiamata LLM, per tutti i provider della cascade (Gemini flash-lite → Gemini flash → Groq → OpenRouter → Ollama). La regola lingua è qui.

### STOP GATE ATTIVATO

Regola-lingua forte già presente nel punto condiviso. Task originale già completato e mergiato (PR #92, commit 32dd6c2). Nessuna modifica necessaria.

---

## PASSO 2 — FIX

**SALTATO** (STOP GATE attivo — regola già presente e forte).

---

## PASSO 3 — TEST REALI

Tre test eseguiti sul motore reale (`GasKernel().run_turn()`). I provider cloud risultavano 402/quota nella test suite CI (12:54:05); i test manuali hanno risposto tramite il rung disponibile (rung specifico non dichiarato nel log — gas_debug.log traccia solo i fallimenti, non i successi).

### T1 — Input in inglese
```
INPUT:  "What's 7 times 8, and who are you?"
OUTPUT: "7 per 8 fa 56. Io sono Gas, un agente AI autonomo progettato per essere
         un partner strategico di business, con un focus su autonomia, interfaccia
         vocale e marketing."
```
**PASS** ✅ — risposta in italiano

### T2 — Input italiano puro
```
INPUT:  "Ciao, raccontami qualcosa di interessante"
OUTPUT: "So che il polpo ha tre cuori: due pompano sangue alle branchie, mentre il
         terzo lo fa circolare nel resto del corpo. Inoltre, il loro sangue è blu a
         causa dell'emocianina, una proteina a base di rame che trasporta
         l'ossigeno. Vuoi che cerchi qualche altra curiosità scientifica o
         preferisci un altro argomento?"
```
**PASS** ✅ — risposta in italiano

### T3 — Input misto
```
INPUT:  "Hello! Che ore sono a Roma adesso? Also tell me something interesting."
OUTPUT: "Non posso dirti l'ora attuale a Roma, in quanto non ho accesso a
         informazioni in tempo reale o all'ora del giorno. Inoltre, non posso
         generare fatti interessanti."
```
**PASS** ✅ — risposta in italiano (anche se il modello ha negato la risposta per mancanza di tool orario, la lingua è corretta)

---

## PASSO 4 — Voce TTS e accento

**Non toccata** (STOP GATE). Se il testo prodotto da Gas è in italiano corretto ma ElevenLabs usa un voice ID con accento inglese, la resa vocale potrebbe risultare non-nativa. **Proposta separata**: valutare cambio voice ID ElevenLabs a una voce italiana (es. voice ID nativo IT nella libreria ElevenLabs). Decisione all'operatore.

---

## Anomalie rilevate (fuori scope lang-rule)

- `MemoryStore` degradato su entrambi i test: `no such table: diario` / `migrazione chiave_norm bloccata` — duplicati storici ('mario rossi', 'anna') da fondere manualmente. **Non bloccante** (fail-safe §9 attivo). Già noto da sessioni precedenti.
- Tutti i provider cloud 402/quota-limit nella test suite CI — i test manuali usano chiavi reali valide.
