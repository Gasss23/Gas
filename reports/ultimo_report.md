# Sonda auto-apprendimento — ricognizione stato attuale
**Data:** 2026-09-23  
**Branch:** sonda/auto-apprendimento-recon

---

## Fetta unica — Ricognizione e mappatura del sistema di memoria

**FATTA**

Eseguita ricognizione completa del codice reale (senza modifiche). Output: `reports/sonda_auto_apprendimento.md`.

### Cosa è stato mappato

1. **Schema DB** verificato su copia di `.gas_memory.db`: tabelle `diario`, `contatti`, `diario_fts`, `vettori` (in `.gas_vectors.db`). Confermati trigger di immutabilità sul diario.
2. **Formato diario** verificato su dati reali: 20 righe, tutte `tipo="calcola"`, formato `"args | [OK/KO] output[:160]"`.
3. **Compressione history** (FASE 2.5): documentata la perdita di contenuto oltre 300 char e la struttura delle sequenze tool_use.
4. **Recupero** — due canali: `_memoria_pin()` always-on (3000 char nel system prompt) + tool `ricorda` con cascata FTS5 → semantico (opt-in) → substring.
5. **Telemetria** — `.gas_tokens.jsonl` esiste (24 righe), traccia fallthrough provider con classificazione `KO/QUOTA/WARN`.
6. **Tool di scrittura** — `salva_contatto` e `imposta_stato_contatto` accessibili all'agente; `unisci_contatti` solo per uso umano manuale.
7. **7 rischi identificati** per un sistema di auto-apprendimento.
8. **3 opzioni design** proposte per il capitolo auto-apprendimento.

### Anomalie riscontrate

- **R2 (prompt injection)**: nessuna sanitizzazione del testo estratto dalla memoria prima dell'iniezione nel pin (verificato `gas.py:1221-1222`).
- **Caveat immutabilità**: con `recursive_triggers = OFF` (default SQLite pre-`_connect`), `INSERT OR REPLACE` sulla PK aggirava i trigger. Risolto in `_connect()` con `PRAGMA recursive_triggers = ON` (`store.py:278`).
- Il `.gas_vectors.db` non esiste: il vector store è opt-in via `GAS_VECTORS` e non ancora abilitato.
