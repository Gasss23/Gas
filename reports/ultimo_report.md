# Report task — 2026-06-24

## Scope
Task doc/config puro. Nessuna modifica a gas.py, brains/, modules/, tests/. Nessuna review revisore richiesta.

## Modifiche effettuate

### 1. CLAUDE.md §11 — allineamento modello default
**Prima:** `default opusplan (Opus solo in plan mode, Sonnet per l'esecuzione)`
**Dopo:** `default Sonnet 4.6 (esecuzione). Opus SOLO on-demand via /model opus per strategia/architettura — mai automatico.`

Motivazione: settings.json forza già `claude-sonnet-4-6`. La doc era disallineata menzionando `opusplan` come default, che non esiste più come modalità operativa.

### 2. .claudeignore — creato ex novo
File creato in root con rumore puro (binari/cache/log). Nessun file .md/.py/config escluso.
Contenuto:
```
venv/
.venv/
__pycache__/
*.pyc
*.db
.gas_memory.db
.gas_vectors.db
*.log
gas_debug.log
```

## DECISIONI UMANE RICHIESTE
Nessuna. Task completamente entro scope.

## File toccati
- `CLAUDE.md` (1 riga modificata, §11)
- `.claudeignore` (creato)
- `reports/ultimo_report.md` (questo file)
