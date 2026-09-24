# Diff sessione — 2026-09-25

## File toccati

| File | Cosa è cambiato e perché |
|------|--------------------------|
| `gas.py` | Fetta A: `import re`, costanti `_MEMORIA_DATI_OPEN/_CLOSE`, `_sanitize_memory_text` (sanitizzazione memoria anti-injection), aggiornamento `_GAS_SYSTEM_PROMPT_BASE` (regola dato storico), `_memoria_pin` (sanitize campi + wrapper), `_ricorda` (sanitize + wrapper). Fetta B: `_turno_tentati` tracking, `_turno_provider` spostato al ramo successo, `tentati=` aggiunto a `_chiudi_turno`. |
| `modules/memory/store.py` | Fetta C: `FONTI_AMMESSE = frozenset{...}` + guard in `append_diario` (valore non ammesso → WARN + NULL, fail-safe §9). |
| `modules/memory/__init__.py` | Export di `FONTI_AMMESSE` aggiunto all'import e a `__all__`. |
| `tests/test_unit_kernel.py` | +21 test: T65a-f (Fetta A: sanitizzazione, wrapper, regola system prompt), T66a-c (Fetta B: provider onesto, tentati), T67a-e (Fetta C: guard fonte). |
| `.claude/agents/memoria_revisore.md` | Riga #104 aggiunta dal revisore (2026-09-25, APPROVATO). |
| `reports/stato_progetto.md` | Aggiornato: header data/review, counter review (103→104), numeri suite (318→339 PASS). |
| `reports/ultimo_report.md` | Riscritto per fetta 2: obiettivo, modifiche, test, E2E reale, review #104. |

## Note

- Fetta A etichetta MITIGATO (non CHIUSO): i delimitatori riducono la prompt injection, non la eliminano.
- Fette B e C: CHIUSO — dati deterministici, test coprono tutti i rami.
- Suite: 339 PASS, 5 FAIL (bwrap macOS F-mac-1, invariati).
