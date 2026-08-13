# SONDA FASE 3 — Fetta 0: Endpoint HTTP vocale

**Data**: 2026-08-13
**Branch**: `sonda/voice-endpoint`
**Task**: Sonda fetta 0 — identificazione metodo kernel e libreria HTTP per l'endpoint vocale FASE 3.

---

## DECISIONI UMANE RICHIESTE

1. **Merge della PR `sonda/voice-endpoint`** (o chiusura senza merge — è solo doc/sonda).
2. **Conferma metodo kernel**: `run_turn` generator come descritto nel report — OK?
3. **Conferma libreria HTTP**: stdlib `http.server` + `ThreadingMixIn`, zero nuove dipendenze — OK?
4. **Conferma threadsafety**: Opzione A (lock globale, richieste vocali serializzate) — OK?

Finché i punti 2-4 non sono confermati, la fetta 1 (scrittura dell'endpoint) NON parte.

---

## Esito fette

- **Fetta 0 — Sonda**: `FATTA`
  - Metodo kernel identificato: `GasKernel.run_turn(user_prompt: str) -> Generator` (`gas.py:1424`)
  - Libreria HTTP scelta: stdlib `http.server` + `socketserver.ThreadingMixIn` (zero nuove dipendenze)
  - Threadsafety: lock globale (Opzione A) raccomandato
  - Revisore non invocato (nessuna modifica a gas.py/brains/modules/tests)

- **Fetta 1 — Scrittura endpoint**: `DEFERITA — stop gate attivo, attesa conferma operatore`

---

## Dettagli sonda

### Metodo kernel

`GasKernel.run_turn(user_prompt: str) -> Generator[Dict[str, Any], None, None]` (`gas.py:1424`)

È un **generator**: emette eventi tipizzati durante il loop agentico.

| `type` | Contenuto | Quando |
|--------|-----------|--------|
| `"tool_res"` | `{"type": "tool_res", "output": str}` | Per ogni tool call (loop agentico, max 10 iter) |
| `"final"` | `{"type": "final", "content": str}` | Risposta testuale finale |
| `"error"` | `{"type": "error", "content": str}` | Budget esaurito / pipeline LLM esausta |

L'endpoint HTTP deve iterare il generator e raccogliere l'evento `"final"`. Gli eventi `"tool_res"` intermedi vengono consumati silenziosamente.

Il kernel è stateful (`self.history` mutato in-place): va istanziato UNA VOLTA all'avvio del server, non per ogni richiesta.

### Libreria HTTP

**`requirements.txt`**: openai, requests (client!), numpy, onnxruntime, fastembed — nessun server HTTP.

**Scelta**: stdlib `http.server` + `socketserver.ThreadingMixIn` — zero nuove dipendenze, portabile WSL→VPS, sufficiente per un endpoint singolo.

`ThreadingMixIn` necessario: il loop agentico può durare secondi, il server non deve bloccarsi tra richieste.

### Threadsafety (fuori-scope fetta 0, da confermare)

`GasKernel` non ha lock interni. Con threading, due richieste concorrenti corromperebbero `self.history`.

- **Opzione A** (raccomandata): `threading.Lock` globale — serializza le richieste vocali. Accettabile per uso mono-utente.
- **Opzione B**: istanza kernel per richiesta — nessun lock, overhead disco a ogni chiamata.

`_save_history` usa `os.replace` atomico: safe per accessi concorrenti sul file.

### Anomalie riscontrate

Nessuna anomalia. La sonda ha confermato che la fetta 1 non richiede modifiche al kernel — solo un server wrapper.
