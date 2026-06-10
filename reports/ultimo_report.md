# Report sessione 2026-06-10 — Guardrail memoria, diagnosi 400 Gemini, pensionamento flash-lite

## Intervento 1 — Guardrail hard contro l'allucinazione "scrivi la memoria"

**Causa accertata**: quando un brain (soprattutto llama-3.3 su Groq, ma anche
gemini-2.5-flash, vedi sotto) vede nella finestra esempi di scritture su
`_gas_history.json`, allucina di dover salvare la memoria da solo via `write_file`.

**Modifiche a `gas.py`**:
1. `execute_tool_call`: ogni `write_file` il cui path normalizzato
   (lowercase, `-`/spazi → `_`) contiene `gas_history` viene rifiutato con:
   *"Operazione negata: la memoria di Gas è gestita automaticamente dal kernel,
   non scriverla mai."*
2. Quinta regola tassativa in `_GAS_SYSTEM_PROMPT_BASE`:
   *"Non scrivere MAI file di memoria o cronologia (gas_history e simili):
   la memoria è gestita automaticamente dal kernel."*

**Verifiche**:
- Test unitario: bloccate tutte le varianti (`_gas_history.json`,
  `.gas_history.json`, `GAS_HISTORY.txt`, `gas-history.json`,
  `backup/gas history.md`); le scritture legittime (`note.md`) passano.
- Turno end-to-end forzato su Groq (GEMINI_API_KEY rimossa) con prompt-esca
  "Salva un riassunto nella tua memoria storica": il modello ha tentato la
  scrittura **3 volte**, ha ricevuto l'errore ogni volta, `_gas_history.json`
  **non si è ricreato** e il loop non è crashato.
- Conferma in produzione: nel test di round-trip finale **anche gemini-2.5-flash**
  ha tentato la scrittura ed è stato bloccato; il turno è proseguito normalmente
  fino alla risposta finale.

**Effetto collaterale scoperto durante il test**: il modello tentato dall'esca ha
letto l'intero `.gas_history.json` via `read_file`, iniettando un tool result da
84 KB nella storia → richiesta successiva da 23.879 token → Groq 413
(limite 12.000 TPM) → pipeline esausta (Gemini era disattivato dal test).
La storia contaminata è stata ripulita (backup in `.gas_history.json.bak`).
**Rischio aperto**: nessun cap sulla dimensione dei tool result; un `read_file`
su file grossi può sfondare i limiti TPM. Candidato per il prossimo intervento
(troncamento tool result oltre N caratteri).

## Intervento 2 — Diagnosi del 400 Gemini flash (fix rimandato, come richiesto)

**Strumentazione aggiunta**: in `run_turn`, ogni 400 da provider Gemini ora logga
la sequenza dei role del payload inviato, con dettaglio per gli assistant
(`tool_calls=N, content=sì/no`).

**Riproduzione**: ricostruita la finestra **esatta** del fallimento delle 18:00
(storia a 68 messaggi, stessa `_get_window`, stesso system prompt, stessi tools,
senza max_tokens) e rinviata a gemini-2.5-flash **5 volte: tutte accettate**.

**Verifica delle tre ipotesi sulla finestra incriminata**:
- (a) assistant con content+tool_calls: **assente** nella finestra del fallimento.
  L'unico messaggio con quella forma (indice 68 della storia) è stato creato
  *dopo* il 400, dalla risposta di Groq nello stesso turno. Testato comunque
  esplicitamente con il payload odierno che lo contiene: accettato.
- (b) tool_calls paralleli con tool result consecutivi: **assenti** (tutti gli
  assistant hanno 1 sola tool call).
- (c) posizione del system message: **esclusa** (stessa posizione in tutte le
  5 riproduzioni riuscite).

**Diagnosi**: la sequenza prodotta da `_get_window` è conforme alle regole di
Gemini; il 400 *INVALID_ARGUMENT* ("function call turn comes immediately
after...") è apparso **una sola volta** nel log e non è riproducibile con la
richiesta identica → errore transitorio/flaky del layer di compatibilità OpenAI
di Gemini, non un bug strutturale nostro.

**Raccomandazione per il fix (da decidere)**: un singolo retry sul 400 Gemini
prima del fallback. La diagnostica ora in gas.py catturerà il payload esatto
alla prossima occorrenza, se il pattern dovesse essere strutturale.

## Intervento 3 — Pensionamento gemini-2.0-flash-lite

**Confermato**: `gemini-2.0-flash-lite` risponde 429 con `limit: 0` su tutte le
metriche free tier → il modello non ha più quota gratuita, non è un limite che
si resetta.

**Sostituto trovato**: `gemini-2.5-flash-lite` —
- ping OK, quota gratuita attiva;
- supporto tool calling verificato (ha invocato correttamente `read_file`).

**PROPOSTA (non applicata, come richiesto)**: sostituire
`gemini-2.0-flash-lite` → `gemini-2.5-flash-lite` in:
- catena "semplice" di `run_turn` (gas.py:143),
- lista provider di `doctor` (gas.py:207).
Fino ad allora la catena semplice paga un 429 a vuoto a ogni turno prima di
passare a flash.

## Stato finale

- `gas doctor`: OPERATIVO CON AVVISI (solo il QUOTA noto di flash-lite), exit 0.
- Round-trip agentico post-modifiche: OK (read_file → guardrail → risposta finale).
- Storia: 77 messaggi, zero orfani, finestra valida da `role:user`.
- File spurio `_gas_history.json`: eliminato e non più ricreabile (guardrail).
