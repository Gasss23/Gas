# Report sessione 2026-06-10 (sera) — Verifica puntuale Intervento C: il cap agisce a monte della history

Domanda della sessione: il troncamento di `_cap_tool_output` avviene PRIMA che
l'output del tool venga salvato nella history (`_add_to_history`), o solo su
ciò che viene mostrato, mentre `.gas_history.json` salva l'originale intero?

**Risposta: il cap agisce a monte. La history salva l'output già troncato.
Nessuna correzione necessaria.**

## Evidenza statica (gas.py)

Il flusso è lineare e non esiste un percorso che salvi l'output non troncato:

1. `execute_tool_call` (riga ~160) termina con
   `return self._cap_tool_output(name, args, out)` — il valore non troncato
   `out` non esce mai dalla funzione;
2. in `run_turn` (righe ~217-218) lo stesso valore di ritorno viene usato sia
   per la history sia per lo yield all'utente:
   ```python
   out = self.execute_tool_call(tc.function.name, tc.function.arguments)
   self._add_to_history("tool", content=out, tool_call_id=tc.id, name=tc.function.name)
   yield {"type": "tool_res", "output": out}
   ```

## Evidenza empirica (round-trip reale)

Test eseguito: file `test_cap_50k.txt` da **50.000 caratteri esatti**, prompt
a Gas che forza un `read_file` su quel file, poi ispezione diretta di
`.gas_history.json` con uno script Python esterno al kernel.

Risultati:
- Warning in `gas_debug.log`:
  `Output tool troncato: read_file su 'test_cap_50k.txt', 50000 caratteri originali` ✅
- Evento `tool_res` emesso dal generatore: **8.200 caratteri** (8.000 + marker) ✅
- **Campo `content` dell'ultimo messaggio `role:tool` in `.gas_history.json`:
  8.200 caratteri, NON 50.000** ✅
- Coda del content salvato: termina con il marker
  `[OUTPUT TRONCATO: ... usa run_command con grep/wc per estrarre solo ciò che serve.]` ✅
- Risposta finale di Gas coerente e onesta sul contenuto parziale. ✅

Nota di contorno: durante il test gemini-2.5-flash era a quota esaurita
(429 free tier, 20 req/giorno); il paracadute ha portato il turno su Groq
senza crash né interruzione del ciclo agentico — il round-trip ha anche
ri-validato il fallback a cascata.

## Stato finale

- Intervento C confermato corretto end-to-end: il cap protegge la history su
  disco, non solo la visualizzazione. Nessuna modifica al codice.
- File di test `test_cap_50k.txt` rimosso.

## Prossimi candidati (invariati)

- Snapshot preventivo dei file (anti-autodistruzione) — priorità alta da roadmap.
- Modalità dry-run.
- Valutare cap dedicato (più alto) per la futura pipeline Whisper, se 8.000
  caratteri si rivelassero stretti per le trascrizioni.
