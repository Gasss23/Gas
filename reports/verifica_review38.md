# VERIFICA READ-ONLY — commit a8c6d53 (review #38)

**Data verifica**: 2026-06-28
**Scope**: lettura pura. Zero modifiche al working tree.

---

## 1 DIFF STAT

```
commit a8c6d534dde49f5d9f181bdbf4ac4301d34ee0fc
Author: gqual <gqualantoni23@gmail.com>
Date:   Sat Jun 27 22:01:09 2026 +0200

    feat(kernel): chiusura item aperti roadmap — budget cap + Telegram bridge + calibrate/eval-vectors (review #38)

 gas.py                       | 155 +++++++++++++++++++++++++++++++++
 modules/telegram/__init__.py |   0
 modules/telegram/bot.py      | 198 +++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py    |  93 ++++++++++++++++++++
 4 files changed, 446 insertions(+)
```

File toccati: `gas.py`, `modules/telegram/__init__.py` (file vuoto), `modules/telegram/bot.py`, `tests/test_unit_kernel.py`.
**Nessun file motore esistente è stato modificato**: tutte inserzioni, zero cancellazioni.
`requirements.txt`: nessun diff (zero nuove dipendenze).

---

## 1b DIFF GAS.PY (integrale)

```diff
diff --git a/gas.py b/gas.py
index 461c962..b3793c6 100755
--- a/gas.py
+++ b/gas.py
@@ -428,6 +428,44 @@ class GasKernel:
         except Exception as e:
             logging.warning("_log_tokens: scrittura fallita (%s) — ignorato", e)
 
+    def _daily_cost_usd(self) -> float:
+        """Somma i costi (USD stimati) degli ultimi 86400 secondi dal log token.
+        FAIL-SAFE: log assente/corrotto → 0.0 (mai bloccare il turno per log
+        mancante, §9). Zero token LLM: sola lettura file locale."""
+        try:
+            log_path = self.root / TOKEN_LOG_FILENAME
+            if not log_path.exists():
+                return 0.0
+            from datetime import timedelta
+            # Stesso formato di _log_tokens ("ts": strftime("%Y-%m-%dT%H:%M:%S")) →
+            # il confronto stringa lessicografico è corretto (ISO 8601 senza "Z").
+            cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
+            total = 0.0
+            with open(log_path, "r", encoding="utf-8") as f:
+                for line in f:
+                    line = line.strip()
+                    if not line:
+                        continue
+                    try:
+                        r = json.loads(line)
+                    except Exception:
+                        continue
+                    if r.get("event", "call") == "fallthrough":
+                        continue
+                    if r.get("ts", "") < cutoff:
+                        continue
+                    prov = r.get("provider", "?")
+                    p_in, p_out = _PROVIDER_PRICE_PER_MTok.get(prov, (0.0, 0.0))
+                    try:
+                        total += int(r.get("in", 0)) * p_in / 1_000_000
+                        total += int(r.get("out", 0)) * p_out / 1_000_000
+                    except (TypeError, ValueError):
+                        continue
+            return total
+        except Exception as e:
+            logging.warning("_daily_cost_usd fallita (%s) — budget non applicato", e)
+            return 0.0
+
     def _add_to_history(self, role: str, content: Optional[str] = None, tool_calls: Optional[List[Any]] = None, tool_call_id: Optional[str] = None, name: Optional[str] = None):
         """Costruisce un dizionario puro, evitando oggetti complessi."""
         entry = {"role": role}
@@ -1293,6 +1331,19 @@ class GasKernel:
         # loop dei provider. No-op se GAS_VECTORS è spento o il layer è degradato.
         self._vettori_catchup()
 
+        # Budget giornaliero kill-switch (§11, GAS_DAILY_TOKEN_BUDGET in USD):
+        # se configurato, somma i costi 24h dal log locale e blocca se superato.
+        # Fail-safe §9: errore nella lettura → 0.0, il turno PROSEGUE comunque.
+        _budget = _env_float("GAS_DAILY_TOKEN_BUDGET", 0.0, min_val=0.0, max_val=100_000.0)
+        if _budget > 0.0:
+            _spent = self._daily_cost_usd()
+            if _spent >= _budget:
+                yield {"type": "error",
+                       "content": (f"Budget giornaliero esaurito: ${_spent:.4f} spesi "
+                                   f"(limite ${_budget:.2f} USD). "
+                                   "Riprova domani o aumenta GAS_DAILY_TOKEN_BUDGET.")}
+                return
+
         # Endpoint/modelli dalle costanti di modulo (punto unico, condiviso con doctor).
         # Pavimento offline Ollama: NON gira nel Codespace. Sul PC/VPS si esporta

@@ -1898,6 +1949,94 @@ def tokens_cmd(root_dir: Optional[str] = None, days: Optional[int] = None) -> int:
     return 0
 
+def calibrate_vectors_cmd(root_dir: Optional[str] = None, n_sample: int = 20) -> int:
+    ...  # [vedi diff integrale in sezione 4]
+
+def eval_vectors_cmd(root_dir: Optional[str] = None, query: Optional[str] = None,
+                     k: int = 10) -> int:
+    ...  # [vedi diff integrale in sezione 4]
+
 def main():
     ...
+    if len(sys.argv) > 1 and sys.argv[1] == "calibrate-vectors":
+        ...
+    if len(sys.argv) > 1 and sys.argv[1] == "eval-vectors":
+        ...
+    if len(sys.argv) > 1 and sys.argv[1] == "telegram":
+        from modules.telegram.bot import run_bot
+        sys.exit(run_bot())
```

---

## 2 — BUDGET CAP: codice e analisi

### Codice verbatim

```python
def _daily_cost_usd(self) -> float:
    """Somma i costi (USD stimati) degli ultimi 86400 secondi dal log token.
    FAIL-SAFE: log assente/corrotto → 0.0 (mai bloccare il turno per log
    mancante, §9). Zero token LLM: sola lettura file locale."""
    try:
        log_path = self.root / TOKEN_LOG_FILENAME
        if not log_path.exists():
            return 0.0
        from datetime import timedelta
        cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        total = 0.0
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("event", "call") == "fallthrough":
                    continue
                if r.get("ts", "") < cutoff:
                    continue
                prov = r.get("provider", "?")
                p_in, p_out = _PROVIDER_PRICE_PER_MTok.get(prov, (0.0, 0.0))
                try:
                    total += int(r.get("in", 0)) * p_in / 1_000_000
                    total += int(r.get("out", 0)) * p_out / 1_000_000
                except (TypeError, ValueError):
                    continue
        return total
    except Exception as e:
        logging.warning("_daily_cost_usd fallita (%s) — budget non applicato", e)
        return 0.0
```

```python
# Kill-switch in run_turn() (gas.py ~riga 1331):
_budget = _env_float("GAS_DAILY_TOKEN_BUDGET", 0.0, min_val=0.0, max_val=100_000.0)
if _budget > 0.0:
    _spent = self._daily_cost_usd()
    if _spent >= _budget:
        yield {"type": "error",
               "content": (f"Budget giornaliero esaurito: ${_spent:.4f} spesi "
                           f"(limite ${_budget:.2f} USD). "
                           "Riprova domani o aumenta GAS_DAILY_TOKEN_BUDGET.")}
        return
```

### Risposte secche

- **Agisce sul RUNTIME GAS (provider gemini/groq/etc) o sul dev (Anthropic)?**
  RUNTIME GAS. Legge `.gas_tokens.jsonl` e usa `_PROVIDER_PRICE_PER_MTok` che mappa provider del runtime (gemini-flash, gemini-flash-lite, groq, openrouter, ollama). Non tocca costi Anthropic/Claude Code.

- **Cosa fa al raggiungimento del cap?**
  Blocca il turno: `yield {"type": "error", ...}` + `return`. Zero token AI consumati per quel turno.

- **Valore di default?**
  `0.0` (disabilitato). Configurabile via env `GAS_DAILY_TOKEN_BUDGET` (USD float).

- **Su quale spesa interviene, concretamente?**
  Sui costi dei provider del RUNTIME GAS. Il runtime gira su free tier (Gemini gratis, Groq gratis) → costo runtime ~0€. Il budget cap non tocca la spesa di sviluppo Claude Code (che è separata e incide sul conto Anthropic). Se il runtime è 0€, il cap è inerte salvo configurarlo intenzionalmente.

---

## 3 — TELEGRAM BRIDGE: codice e analisi

### Funzione principale verbatim (`modules/telegram/bot.py`)

```python
def run_bot(root_dir: Optional[str] = None) -> int:
    """Loop principale del bridge bot. Blocca fino a KeyboardInterrupt (Ctrl-C).
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("✗ gas telegram: TELEGRAM_BOT_TOKEN non configurato.")
        return 1

    raw_ids = os.environ.get("TELEGRAM_ALLOWED_IDS", "").strip()
    if not raw_ids:
        print("✗ gas telegram: TELEGRAM_ALLOWED_IDS non configurato (fail-closed).")
        return 1

    allowed: Set[int] = set()
    for chunk in raw_ids.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            allowed.add(int(chunk))
        except ValueError:
            print(f"  WARN: '{chunk}' in TELEGRAM_ALLOWED_IDS non è un intero — ignorato")
    if not allowed:
        print("✗ gas telegram: nessun ID autorizzato valido in TELEGRAM_ALLOWED_IDS.")
        return 1

    base_url = f"{_TELEGRAM_API}{token}"

    me = _tg_post(base_url, "getMe")
    if not me or not me.get("ok"):
        print("✗ gas telegram: impossibile connettersi all'API Telegram.")
        return 1

    root = Path(root_dir or os.getcwd()).resolve()
    import sys as _sys
    _sys.path.insert(0, str(root if (root / "gas.py").exists() else root.parent))
    from gas import GasKernel
    kernel = GasKernel(root_dir=str(root))

    offset = 0
    while True:
        try:
            resp = _tg_post(base_url, "getUpdates",
                            {"offset": offset, "timeout": 60}, timeout=70)
            if resp is None or not resp.get("ok"):
                time.sleep(5)
                continue
            updates: List[Dict[str, Any]] = resp.get("result", [])
            for upd in updates:
                offset = max(offset, int(upd.get("update_id", 0)) + 1)
                _handle_update(base_url, upd, allowed, kernel)
        except KeyboardInterrupt:
            print("\n✓ gas telegram: interruzione ricevuta, uscita.")
            return 0
        except Exception as e:
            log.warning("Errore nel loop di polling: %s — riprendo tra 5s", e)
            time.sleep(5)
```

### Risposte secche

- **È un'interfaccia per il RUNTIME di GAS o un canale per il DEV TOOLING?**
  RUNTIME DI GAS. L'utente manda messaggi al bot Telegram → il bot chiama `kernel.run_turn(text)` → GAS risponde. È GAS che parla con l'utente via Telegram, non uno strumento di controllo di Claude Code / del repo.

- **Apre un endpoint/bot in ascolto? Riceve comandi?**
  Sì, apre un long-polling `getUpdates` verso l'API Telegram (nessuna porta IN INGRESSO aperta localmente). Riceve messaggi di testo liberi dall'utente autorizzato. Non ha comandi speciali: tutto il testo va direttamente a `run_turn()`.

- **Tocca o bypassa hook `.claude/hooks/`?**
  NO. Il modulo non tocca `.claude/hooks/` in alcun punto del codice.

- **Tocca o bypassa il gate revisore?**
  NO. Il gate revisore è un gate di sviluppo (pre-commit). `bot.py` è runtime, non ha alcun riferimento al gate.

- **Tocca o bypassa sandbox bwrap?**
  NO direttamente. Il bot chiama `kernel.run_turn()` che usa il kernel intero, inclusa la sandbox bwrap per `run_command`. Nessun bypass.

- **Dipendenze nuove in requirements.txt?**
  ZERO. `git show a8c6d53 -- requirements.txt` → nessun output (file non toccato). Il modulo usa solo `urllib.request` (stdlib Python).

---

## 4 — CALIBRATE / EVAL-VECTORS: codice e analisi

### Codice verbatim `calibrate_vectors_cmd`

```python
def calibrate_vectors_cmd(root_dir: Optional[str] = None, n_sample: int = 20) -> int:
    """Comando `gas calibrate-vectors`: campiona N righe del diario come query,
    cerca ciascuna nel vector store, mostra la distribuzione degli score coseno
    e suggerisce un valore per GAS_VECTORS_MIN_SIM sul diario reale.
    Zero token LLM — solo embedding locali + lettura DB."""
    import random
    root = Path(root_dir or os.getcwd()).resolve()
    from modules.memory import MemoryStore, default_db_path
    mem = MemoryStore(default_db_path(root))
    if not mem.available:
        print("✗ calibrate-vectors: memoria non disponibile — niente da campionare.")
        return 1
    vs = VectorStore(default_vectors_path(root))
    if not vs.available:
        dr = getattr(vs, "disable_reason", "") or "dipendenze assenti"
        print(f"✗ calibrate-vectors: vector store non disponibile ({dr}).")
        return 1
    righe = mem.diario_recente(500)
    if len(righe) < 5:
        print(f"✗ calibrate-vectors: diario troppo piccolo ({len(righe)} righe, minimo 5).")
        return 1
    sample = random.sample(righe, min(n_sample, len(righe)))
    scores: List[float] = []
    for r in sample:
        query = str(r.get("descrizione", ""))
        hits = vs.search(query, k=6, min_sim=0.0, source="diario")
        for h in hits:
            if str(h.get("source_ref")) != str(r.get("id")):
                scores.append(float(h["score"]))
    if not scores:
        print("Nessun risultato: esegui 'gas reindex' per popolare l'indice, poi riprova.")
        return 1
    scores.sort(reverse=True)
    n = len(scores)
    p25 = scores[n * 3 // 4]
    p50 = scores[n // 2]
    p75 = scores[n // 4]
    mean_ = sum(scores) / n
    cur_sim = _env_float("GAS_VECTORS_MIN_SIM", 0.30)
    suggested = max(0.10, min(0.80, round(p25 - 0.05, 2)))
    print(f"Suggerimento:    GAS_VECTORS_MIN_SIM={suggested:.2f}  (p25 - 0.05, conservativo)")
    return 0
```

### Codice verbatim `eval_vectors_cmd`

```python
def eval_vectors_cmd(root_dir: Optional[str] = None, query: Optional[str] = None,
                     k: int = 10) -> int:
    """Comando `gas eval-vectors [query]`: ricerca semantica di test per valutare
    qualità del retrieval e confrontare modelli (cambia GAS_EMBED_MODEL + gas reindex).
    Senza query mostra le statistiche del vector store. Zero token LLM."""
    root = Path(root_dir or os.getcwd()).resolve()
    vs = VectorStore(default_vectors_path(root))
    if not vs.available:
        dr = getattr(vs, "disable_reason", "") or "dipendenze assenti"
        print(f"✗ eval-vectors: vector store non disponibile ({dr}).")
        return 1
    n_vettori = vs.conta("diario")
    cur_sim = _env_float("GAS_VECTORS_MIN_SIM", 0.30)
    print(f"  Modello:   {vs.model_name}")
    print(f"  Alt. mod.: intfloat/multilingual-e5-small  (384-dim, stessa infra)")
    print(f"             → per valutare: GAS_EMBED_MODEL=intfloat/multilingual-e5-small gas reindex")
    if not query:
        print("\nUso: gas eval-vectors \"la tua query\"  [k=10]")
        return 0
    hits = vs.search(query, k=k, min_sim=0.0, source="diario")
    for i, h in enumerate(hits):
        score = float(h["score"])
        marker = "✓" if score >= cur_sim else "✗"
        print(f"  {marker} [{i+1:2}] score={score:.3f}")
    return 0
```

### Risposte secche

- **Ha MODIFICATO il valore di default di VEC_MIN_SIM (o GAS_EMBED_MODEL, o altri parametri) nel codice?**
  **NO.** Entrambe le funzioni leggono `_env_float("GAS_VECTORS_MIN_SIM", 0.30)` ma non modificano il valore. Sono strumenti di sola lettura/misura. Nessuna costante modificata nel diff.

- **È SOLO uno strumento di misura che stampa numeri senza cambiare default?**
  **SÌ.** `calibrate_vectors_cmd` stampa la distribuzione score e il valore suggerito ma non lo scrive da nessuna parte. La riga `suggested = max(0.10, min(0.80, round(p25 - 0.05, 2)))` calcola il suggerimento in memoria e lo stampa; non tocca nessun file di configurazione né variabile globale.

- **Su quali DATI calibra/valuta: diario reale o esempi SINTETICI?**
  **DIARIO REALE.** La riga chiave è:
  ```python
  righe = mem.diario_recente(500)   # legge dal DB SQLite locale
  sample = random.sample(righe, min(n_sample, len(righe)))
  ```
  Prende le ultime 500 righe del diario SQLite reale. Su Windows/dev il diario è vuoto o piccolo → esce con "diario troppo piccolo". Utile sul VPS dove il diario è reale.

---

## 5 REVIEW 38 — Verdetto integrale (da reports/handoff.md del commit 932f17c)

**APPROVATO CON RISERVE**

Le quattro feature (budget cap kill-switch, Telegram bridge, `gas calibrate-vectors`, `gas eval-vectors`) sono corrette, fail-safe §9 rispettato, zero token LLM sui comandi CLI. Suite 190 PASS, 7 FAIL Windows pre-esistenti, T41-T48 tutti PASS.

**Riserve da tracciare (non bloccanti):**

1. **R-budget-ts** — Verificare che `_log_tokens` scriva `ts` nello stesso formato `%Y-%m-%dT%H:%M:%S` usato dal cutoff in `_daily_cost_usd()` — senza suffisso "Z". Se c'è discrepanza il budget viene sottostimato silenziosamente e il kill-switch non blocca mai. → **CHIUSA**: formato verificato identico; aggiunto commento esplicito in codice.

2. **R-tel-2** — In `run_bot()`, la condizione `sys.path.insert` era invertita: aggiungeva `root.parent` quando `gas.py` è in `root`. Inerte in produzione (avviato via `gas telegram`, `gas` è già in `sys.modules`), ma da correggere per correttezza. → **CHIUSA**: condizione corretta prima del commit.

3. **R-tel-budget-perf** (cosmetico) — `_daily_cost_usd()` scansiona l'intero JSONL ad ogni turno. Su VPS h24 con log grande, futuro ottimizzazione: leggere dal fondo. → APERTA, non bloccante.

4. **R-tel-tool_res** (cosmetico) — Output dei tool (troncato 200 char) incluso nel reply Telegram: accettabile con whitelist fail-closed, ma va dichiarato nel docstring del modulo. → APERTA, non bloccante.

---

## 6 — RISERVE / OSSERVAZIONI (solo testo, nessuna azione)

### 6a — Budget cap: agisce sul runtime ~0€, non sulla spesa reale

Il kill-switch legge `.gas_tokens.jsonl` che traccia i provider del RUNTIME GAS (Gemini, Groq, OpenRouter). Questi giratori su free tier hanno costo ~0€. La spesa reale (20€ in 2 giorni, sez. 11 CLAUDE.md) è 100% costo di sviluppo Claude Code su Opus 4.8, che non viene loggato in `.gas_tokens.jsonl` e non viene intercettato dal cap. Il budget cap è quindi oggi inerte rispetto alla spesa problematica. Senza azione.

### 6b — Telegram bridge: storia condivisa tra sessioni

Il kernel condiviso (`kernel = GasKernel(root_dir=str(root))`) inizializzato una sola volta al lancio del bot usa `.gas_history.json` condiviso con la sessione CLI. Se il bot e la CLI girano in parallelo sullo stesso working directory, le due istanze leggono e scrivono lo stesso file di storia → potenziale race condition / corruzione atomica. Il docstring lo segnala ("storia condivisa: adatto all'uso personale single-user") ma non menziona il caso CLI-parallela. Senza azione.

### 6c — R-tel-budget-perf: già nota, aperta

Il revisore #38 l'ha già identificata e lasciata aperta come non bloccante. Su VPS con log h24 potrebbe diventare significativa. Senza azione.

### 6d — `calibrate-vectors` non ha test automatici (T45-T48 testano solo Telegram)

I test T41-T48 coprono budget cap e Telegram. `calibrate_vectors_cmd` e `eval_vectors_cmd` non hanno test dedicati nel diff — plausibile perché richiedono un diario SQLite + vector store popolati, difficili da mockare. Il revisore #38 ha approvato comunque. Senza azione.

### 6e — `eval-vectors` nota e5-small ma non cambia il default

La riga `print(f"  Alt. mod.: intfloat/multilingual-e5-small (384-dim, stessa infra)")` documenta l'alternativa e5-small (già in `_MODEL_PREFIXES`). Nessun cambio di default. La voce roadmap R-wire-1 (ri-taratura sul diario reale VPS) rimane aperta e richiede esecuzione manuale su VPS. Senza azione.
