# Ultimo Report — 2026-06-27 — Build telemetria fallthrough per-provider

## DECISIONI UMANE RICHIESTE

Nessuna. Opzione A (stesso `.gas_tokens.jsonl` con campo `event`) implementata e approvata dal revisore.

---

## FETTE

- **FETTA UNICA — Build telemetria (gas.py)**: `FATTA`
  4 punti implementati, revisore #33 APPROVATO CON RISERVE (R-tel-1 cosmetica, tracciata).

---

## DETTAGLIO MODIFICHE

### 1. `_log_tokens` (gas.py:407-430)
Estesa con parametri opzionali `event: str = "call"` e `reason: Optional[str] = None`.
- `event="call"` (default) → comportamento invariato, record JSONL retrocompatibili
- `event="fallthrough"` → in/out=0, reason=motivo classificato
- Campo `event` ora sempre presente nel record; `reason` solo se non-None

### 2. Aggancio fallthrough in `run_turn` (gas.py:1397-1400)
Nell'`except` del loop provider, dopo il `logging.warning`:
```python
_, _ft_reason = _classify_provider_error(
    getattr(e, "status_code", None), str(e), True)
self._log_tokens(name, model, 0, 0, event="fallthrough", reason=_ft_reason)
```
`_classify_provider_error` è il classificatore già usato in `doctor()` — ora collegato anche al loop runtime (prima era "morto" per il loop).

### 3. `tokens_cmd` (gas.py:1815-1891)
- Aggregazione separata: `totali`/`recenti` per call, `ft_totali`/`ft_recenti` per fallthrough
- I record fallthrough (in/out=0) non entrano nel calcolo costo USD
- Nuova sezione di output "Fallthrough" mostrata solo se ft_totali non vuoto: Provider, Tot, UltimiNgg, Ultimo motivo

### 4. `doctor()` sez.10 Telemetria (gas.py:1655-1698)
Lettura locale `.gas_tokens.jsonl` — zero token LLM, zero ping.
- Log assente → `[OK] assente (si popola dal primo run agentico)`
- Log presente → per provider: `calls=N, fallthrough=M` + ultimo motivo se M>0
- Esito: OK se nessun fallthrough, WARN se almeno uno
- Fail-safe triplo: file assente, record malformati, eccezione generica

### Riserva R-tel-1 (tracciata in stato_progetto.md)
`obbligatoria=True` hardcoded per tutti i provider nel loop: la 402 di openrouter/ollama riceve `"KO"` invece di `"WARN"` nel campo `reason`. Puramente cosmetico, nessun impatto funzionale.

---

## ESITO TEST

172 PASS, 6 FAIL pre-esistenti (bwrap, WinError32 T26b). La sezione Telemetria è già visibile nell'output di T37e.

## ANOMALIE

Nessuna.
