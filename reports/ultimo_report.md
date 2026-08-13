# SONDA FASE 3 — Fetta 0: Endpoint HTTP vocale

**Data**: 2026-08-13
**Branch**: `sonda/voice-endpoint`
**Scope**: SOLO sonda (fetta 0). Nessuna modifica al motore → revisore NON invocato (dichiarato esplicitamente).
**Stato**: In attesa di conferma operatore prima di procedere con la fetta 1 (endpoint).

---

## 1. Metodo pubblico del kernel

### Metodo individuato

```
GasKernel.run_turn(user_prompt: str) -> Generator[Dict[str, Any], None, None]
```

**Definizione**: `gas.py:1424`

### Comportamento del generator

`run_turn` è un **generator**, non un metodo che ritorna direttamente una stringa.
Yield intermedi e finali:

| `type` | Contenuto | Quando |
|--------|-----------|--------|
| `"tool_res"` | `{"type": "tool_res", "output": str}` | Per ogni tool call durante il loop agentico (fino a 10 iterazioni) |
| `"final"` | `{"type": "final", "content": str}` | Risposta testuale finale al prompt utente |
| `"error"` | `{"type": "error", "content": str}` | Budget giornaliero esaurito / pipeline LLM esausta |

### Come l'endpoint HTTP deve consumarlo

L'endpoint non può invocare `run_turn` come una funzione normale. Deve iterare il generator e raccogliere l'evento `"final"`:

```python
response_text = None
error_text = None
for event in kernel.run_turn(user_text):
    if event["type"] == "final":
        response_text = event["content"]
        break
    elif event["type"] == "error":
        error_text = event["content"]
        break
# se response_text è None e error_text è None → pipeline esausta (nessun provider disponibile)
```

Gli eventi `"tool_res"` intermedi vengono silenziosamente consumati (non trasmessi al client vocale).

### Istanziazione

```python
from gas import GasKernel
kernel = GasKernel()       # usa os.getcwd() come root; rilegge .gas_history.json
```

Il kernel è stateful (mantiene `self.history`): va istanziato UNA VOLTA alla partenza del server e riusato tra le richieste — non re-istanziato per ogni chiamata HTTP.

---

## 2. Libreria HTTP disponibile

### Inventario dipendenze

**`requirements.txt`** (deploy core):
```
openai==2.43.0
requests==2.34.2      ← client HTTP, non server
numpy==2.4.6
onnxruntime==1.27.0
fastembed==0.8.0
```

**`requirements-dev.txt`**: solo `pytest==9.1.1`

**Nessun framework server HTTP presente** (no Flask, no FastAPI, no aiohttp, no uvicorn).

### Scelta raccomandata: stdlib `http.server` + `socketserver.ThreadingMixIn`

**Motivazione**:
- **Zero nuove dipendenze** — moduli puri stdlib (`http.server`, `socketserver`, `hmac`, `json`), già presenti su qualsiasi Python 3.11+.
- **Sufficiente per una superficie minima**: un solo endpoint, traffico locale/VPN, nessuna concorrenza pesante.
- **Portabilità garantita**: identico su WSL locale e VPS — l'unica differenza al deploy è `.env` (bind/porta/token).
- `ThreadingMixIn` gestisce le richieste in thread separati → il server non si blocca mentre il kernel elabora (il loop agentico può richiedere svariati secondi).

Sketch della struttura (NON codice definitivo, solo riferimento):

```python
import socketserver, http.server

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class VoiceHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self): ...  # unico verbo accettato
```

**Alternativa stdlib valutata**: `wsgiref.simple_server` — scartata perché single-threaded (una richiesta blocca le successive durante il loop agentico).

**Alternativa con framework** (Flask/FastAPI): NON raccomandata per questa fetta. Richiederebbe una nuova dipendenza e un ASGI/WSGI runner. Il guadagno (routing dichiarativo, middleware) non giustifica la complessità per UN endpoint singolo. Proposta se l'operatore vede altri endpoint futuri in scope.

---

## 3. Osservazioni fuori-scope (da confermare prima di procedere)

### 3a. Threadsafety del kernel

`GasKernel` non ha lock interni: la storia (`self.history`) è mutata in-place durante ogni `run_turn`. Con `ThreadingMixIn`, due richieste concorrenti corromperebbe la history.

**Soluzione proposta** (da discutere con operatore):
- Opzione A — **Lock globale** (`threading.Lock` attorno all'invocazione di `run_turn`): il server serializza le richieste vocali. Accettabile per uso personale (una voce alla volta).
- Opzione B — **Istanza kernel per richiesta**: ogni chiamata HTTP istanzia un `GasKernel` fresco, rilegge la history dal file, poi la salva. Overhead accettabile, nessun lock, ma la history viene letta dal disco a ogni richiesta.

**Raccomandazione**: Opzione A (lock globale) — più semplice e coerente col modello "un utente, una sessione".

### 3b. Thread safety `_save_history`

`_save_history` usa `os.replace` atomico (già in gas.py:422): safe anche con accessi concorrenti sul file — il kernel CLI e il server non si corrompono a vicenda sul .json.

### 3c. Timeout per richieste lente

Il loop agentico può durare secondi in caso di cascata (tutti i provider lenti). Il client Windows deve avere un timeout generoso (es. 60s). Da documentare nella risposta al client, non in scope del server.

---

## STOP GATE — in attesa dell'operatore

La sonda è completa. **Non si scrive nessun codice dell'endpoint finché l'operatore non conferma**:

1. **Metodo kernel OK?** — `run_turn` (generator) come descritto sopra.
2. **Libreria HTTP OK?** — stdlib `http.server` + `ThreadingMixIn`, zero nuove dipendenze.
3. **Threadsafety** — Opzione A (lock globale) raccomandata. Confermare?
4. **Fuori-scope rilevati** — nessuna modifica al kernel necessaria per la fetta 1. Nessuna nuova dipendenza. Tutto risolvibile nel solo server wrapper.

**Revisore**: non invocato in questa fetta (nessuna modifica a gas.py, brains/, modules/, tests/).
Il revisore scatterà sul commit dell'endpoint (prossima sessione, fetta 1).
