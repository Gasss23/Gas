# Ultimo Report — 2026-07-13
## Task: Riserva #44B — prezzi Groq env-overridabili + copertura fallback (T44d)

**Branch:** fix/riserva-44B-groq-prezzi-env
**PR:** #6 — CI SUCCESS, pronta per self-merge

---

## DECISIONI UMANE RICHIESTE

**Nessuna.** Self-merge PR #6 da browser dopo lettura di questo report.

---

## Esito fette

- **Fetta 1 — prezzi Groq env-overridabili**: `FATTA`
  - `brains/model_ids.py`: aggiunte `GROQ_PRICE_IN_USD_PER_1M` / `GROQ_PRICE_OUT_USD_PER_1M` lette da `GAS_GROQ_PRICE_IN`/`GAS_GROQ_PRICE_OUT`, con `try/except` contro valori non numerici (fallback silenzioso ai default 0.15/0.60).
  - `gas.py`: import delle costanti; sostituito il literal `(0.15, 0.60)` in `_PROVIDER_PRICE_PER_MTok["groq"]`.
  - Test T44b (default) + T44c (env-override): entrambi PASS.
  - Gate revisore #46 (due passate): APPROVATO.

- **Fetta 2 — copertura ramo fallback (T44d)**: `FATTA`
  - Aggiunto T44d: setta `GAS_GROQ_PRICE_IN="abc"` e `GAS_GROQ_PRICE_OUT="xyz"`, verifica nessuna eccezione e costanti a default 0.15/0.60.
  - Solo test — gate revisore formale non obbligatorio; suite reale eseguita.

## Suite test finale

```
=== RIEPILOGO: 220 PASS, 0 FAIL ===
[PASS] T44b prezzi Groq default: (0.15, 0.60) da model_ids — prezzi=(0.15, 0.6)
[PASS] T44c prezzi Groq env-override: _daily_cost_usd usa i nuovi prezzi — calcolato=3.0000 atteso=3.0000 p_in=1.0 p_out=2.0
[PASS] T44d env non parsabile (abc/xyz) → no crash, default 0.15/0.60 — p_in=0.15 p_out=0.6
```

## Anomalie

Nessuna.
