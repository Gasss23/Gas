# DIFF SESSIONE — 2026-09-28 (K3+K4 knowledge base in ricorda)

> Fotografia dell'ultima sessione. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

| File | Tipo | Cosa è cambiato e perché |
|------|------|--------------------------|
| `gas.py` | modificato | K3: aggiunto `_knowledge_search()` + wiring in `_ricorda()`; K4: costanti `_CONOSCENZA_DATI_OPEN/CLOSE`, class constants `KNOWLEDGE_MAX_RESULTS/CHARS`, env init `knowledge_db_path`, esteso `_MEM_FILE_PREFIXES` con `.gas_knowledge`, aggiornata descrizione tool `ricorda`. |
| `tests/test_unit_kernel.py` | modificato | +17 test T69a-T69h per i 6 punti K4 + round-trip agentico. |
| `.claude/agents/memoria_revisore.md` | modificato | Review #108 aggiunta (APPROVATO CON RISERVE, commit `6a0a2f7`). |

## Commit di sessione

```
6249e16 feat(autonomia): K3+K4 — ricorda() pesca .gas_knowledge.db + 6 protezioni
6a0a2f7 chore(revisore): memoria review #108 — APPROVATO CON RISERVE
```

## Note

- File NON toccati: `brains/`, `modules/`, `tools/ingest_knowledge.py`, `knowledge/`.
- `.gas_memory.db` e `.gas_knowledge.db` della repo principale non toccati (E2E su copia temporanea).
- Suite: 383 PASS, 5 FAIL (invariati F-mac-1 bwrap macOS).
