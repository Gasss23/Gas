# Report — Task: Stima costi token (`gas tokens` + `_PROVIDER_PRICE_PER_MTok`)
**Data:** 2026-06-25
**Review:** #32 — APPROVATO CON RISERVE (R32-1 try/except chiusa pre-commit; R32-2 cosmetic commento corretto)

---

## Obiettivo

Completare il token accounting aggiungendo la stima del costo in USD al comando
`gas tokens`. "Non puoi controllare ciò che non misuri" (CLAUDE.md §11).

---

## Modifiche

### gas.py

**Nuova costante `_PROVIDER_PRICE_PER_MTok`** (aggiunta subito dopo `TOKEN_LOG_FILENAME`):
```python
_PROVIDER_PRICE_PER_MTok: Dict[str, Tuple[float, float]] = {
    "gemini-flash-lite": (0.10,  0.40),   # input USD/MTok / output USD/MTok
    "gemini-flash":      (0.30,  2.50),
    "groq":              (0.59,  0.79),
    "openrouter":        (0.00,  0.00),   # free tier → 0
    "ollama":            (0.00,  0.00),   # locale → 0
}
```
Prezzi approssimati al 2025-06. Chiave = nome provider come registrato da `_log_tokens`.

**`tokens_cmd` aggiornato:**
- Accumula `cost` per bucket: `in_t * p_in / 1_000_000 + out_t * p_out / 1_000_000`
- try/except (TypeError, ValueError) nel loop body: record JSONL malformato → skip silenzioso (§9)
- Aggiunge colonna "Costo (★ USD)" se almeno un provider ha prezzo > 0; altrimenti "Costo" senza simbolo
- Mostra costo per-provider nella sezione "ultimi N giorni"
- Aggiunge riga TOTALE nella sezione "recenti"
- Nota "★ prezzi appross. (2025-06)" visibile solo se `has_costs` è True

### Esempio output `gas tokens` aggiornato:
```
=== GAS — Token Usage ===  (.gas_tokens.jsonl)

Provider                Calls    Tokens In   Tokens Out       Totale  Costo (★ USD)
─────────────────────────────────────────────────────────────────────────────────────
gemini-flash-lite           2        3,000          600        3,600 $      0.0005
groq                        1          500          100          600 $      0.0004
─────────────────────────────────────────────────────────────────────────────────────
TOTALE                      3        3,500          700        4,200 $      0.0009

Ultimi 7 giorni:
  gemini-flash-lite    3,000 in + 600 out = 3,600 tok  $0.0005
  groq                 500 in + 100 out = 600 tok  $0.0004
  TOTALE               3,500 in + 700 out  $0.0009

  ★ prezzi appross. (2025-06) — aggiornare _PROVIDER_PRICE_PER_MTok se cambiano
```

### tests/test_unit_kernel.py

3 nuovi test:
- **T38a** — `_PROVIDER_PRICE_PER_MTok`: 5 provider attesi + tuple (float, float)
- **T38b** — `tokens_cmd`: costo gemini-flash-lite corretto (1000 in + 200 out → "$0.0002") + nota appross visibile
- **T38c** — `tokens_cmd`: provider ignoto → costo 0.0 + nota appross NON visibile

---

## Suite

**171 PASS, 7 FAIL** (7 pre-esistenti Windows/bwrap — invariati).

---

## Riserve review #32

- **R32-1** (MINORE, chiusa): mancanza try/except nel loop aggregazione → aggiunto `try/except (TypeError, ValueError): continue`
- **R32-2** (cosmetica, chiusa): commento T38b impreciso sull'arrotondamento → corretto pre-commit

---

## File modificati

- `gas.py`: `_PROVIDER_PRICE_PER_MTok` + `tokens_cmd` (costo, try/except, TOTALE recenti)
- `tests/test_unit_kernel.py`: T38a, T38b, T38c
- `reports/stato_progetto.md`: review count, suite, CLI gas tokens
- `.claude/agents/memoria_revisore.md`: lezione #32
