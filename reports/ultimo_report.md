# Report sessione 2026-06-10 (pomeriggio) — Protezione del budget API

Tre interventi su gas.py: pensionamento flash-lite, retry singolo sul 400
Gemini, cap sull'output dei tool. Tutti verificati end-to-end.

## Intervento A — Pensionamento gemini-2.0-flash-lite → gemini-2.5-flash-lite

Applicata la sostituzione già diagnosticata nel report precedente
(2.0-flash-lite a `limit: 0`, free tier rimosso; 2.5-flash-lite con quota
attiva e tool calling verificato) in entrambi i punti:
- catena "semplice" di `run_turn`;
- lista provider di `doctor`.

**Verifica**: `python gas.py doctor` →
```
[OK   ] Provider   gemini-flash-lite    769 ms
[OK   ] Provider   gemini-flash         444 ms
[OK   ] Provider   groq                 103 ms
VERDETTO: TUTTO OK
```
Primo "TUTTO OK" del progetto: la cascata semplice non paga più un 429 a
vuoto a ogni turno.

## Intervento B — Retry singolo sul 400 transitorio di Gemini

In `run_turn`, la chiamata API è ora avvolta da un try interno: se un
provider Gemini risponde 400 (diagnosi del mattino: stesso payload accettato
5/5 al replay → errore transitorio del layer di compatibilità), viene fatto
**esattamente un** retry con payload identico:
- retry OK → `logging.warning("retry Gemini 400 (<nome>): OK")` e il turno
  prosegue normalmente;
- ancora errore → `logging.warning("...: ancora 400, fallback")` e
  l'eccezione risale al gestore esistente (diagnostica payload + fallback).
Gli errori non-400 e i provider non-Gemini non vengono ritentati.

**Verifica** (simulata con client finto iniettato in `gas.OpenAI`, root
temporanea, zero API reali):
- Scenario "transitorio" (1° tentativo 400, 2° OK): 2 chiamate totali,
  log `retry Gemini 400 (gemini-flash-lite): OK`, risposta finale ottenuta
  senza fallback.
- Scenario "persistente" (Gemini sempre 400): 5 chiamate totali
  (2 lite + 2 flash + 1 groq), un solo retry per provider, log
  `ancora 400, fallback`, diagnostica payload emessa, risposta da Groq.

## Intervento C — Cap a 8.000 caratteri sull'output dei tool (CRITICO)

Nuovo `TOOL_OUTPUT_CAP = 8000` e helper `_cap_tool_output` applicato
all'output di tutti i tool (read_file, run_command, write_file):
1. tronca a 8.000 caratteri;
2. accoda il marker: `[OUTPUT TRONCATO: erano N caratteri totali, mostrati i
   primi 8000. Se serve il resto, leggi il file a pezzi (es. head/tail/sed -n)
   o usa run_command con grep/wc per estrarre solo ciò che serve.]`;
3. logga warning con tool, path/comando e lunghezza originale.

Motivazione (nel codice come commento): senza il cap, un singolo read_file
su un file grosso inietta decine di KB nella storia, che `_get_window` si
trascina a ogni chiamata successiva saturando i limiti TPM (incidente del
mattino: 84 KB letti → richiesta da 23.879 token → Groq 413). Protegge anche
la futura pipeline di apprendimento (trascrizioni Whisper ~80-100 KB/30 min).

**Verifiche**:
1. **Unit**: file da 50.000 caratteri → output ricevuto 8.200 caratteri
   (8.000 + marker), warning loggato con lunghezza originale. ✅
2. **Round-trip sotto il cap**: "leggi CLAUDE.md e dimmi quante sezioni ha"
   → risposta corretta ("10 sezioni"), zero warning di troncamento nel log
   (nessun falso positivo). ✅
3. **Round-trip stressato**: lettura del file da 50 KB → tool result di
   8.200 caratteri con marker, warning nel log, e risposta finale onesta:
   *"contiene una stringa molto lunga composta dalla lettera 'A' ripetuta
   numerose volte. A causa della lunghezza del file, è stato mostrato solo
   un estratto."* — nessuna invenzione del contenuto mancante. ✅

## Stato finale

- `gas doctor`: **VERDETTO: TUTTO OK**, exit 0 — tutti e tre i provider OK.
- Storia integra: zero orfani, finestra valida da `role:user`.
- File di test (`test_grosso.txt`) rimosso.
- Budget API protetto su tre fronti: niente 429 a vuoto (A), niente fallback
  inutili su 400 transitori (B), niente esplosioni TPM da tool result (C).

## Prossimi candidati

- Snapshot preventivo dei file (anti-autodistruzione) — priorità alta da roadmap.
- Modalità dry-run.
- Valutare cap dedicato (più alto) per la futura pipeline Whisper, se 8.000
  caratteri si rivelassero stretti per le trascrizioni.
