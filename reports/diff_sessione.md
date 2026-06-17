# 🔀 DIFF DI SESSIONE — 2026-06-17 (CHIUSURA FASE 2 memoria: declassamento unisci_contatti)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché
Chiusura di FASE 2 memoria: il merge di lead è mutante e IRREVERSIBILE, quindi non deve
essere un tool che il modello invoca in autopilot. Declassato a **manutenzione umana**
(meccanismo intatto) + igiene di lettura e cosmetica.

## File toccati (commit motore `0240161`, +89 / -25; SOLO gas.py + tests)
- **`gas.py`**:
  - PUNTO 1: rimossa l'entry `unisci_contatti` da `tools_schema` e il ramo dal dispatcher
    `execute_tool_call` (→ "Tool non trovato."); handler `_unisci_contatti` resta
    richiamabile a mano (docstring: manutenzione umana, perché). `_riassumi_args`
    invariato. **store.py NON toccato** (meccanismo di merge intatto).
  - PUNTO 2: `_trova_contatto` collassa il whitespace su ENTRAMBI i lati del substring
    (riuso `normalizza_chiave` solo per il confronto); ramo match-esatto invariato.
  - PUNTO 3: messaggi di successo di `_salva_contatto`/`_imposta_stato_contatto` con
    chiave canonica (chiude R-crm-norm-1).
  - import `normalizza_chiave` da `modules.memory`.
- **`tests/test_unit_kernel.py`**: T28a-c nuovi; T24a/c/d migrati da `execute_tool_call`
  all'handler `_unisci_contatti`. Suite **132→135, 0 FAIL**.

## Doc (commit separato, no review)
`stato_progetto.md`: R-crm-1b ✅→🟡 MITIGATA; voce motore "Fusione lead" riscritta;
R-crm-norm-1 CHIUSA; paragrafo Istituzioni C ripulito (ultima review #21); Strato B
Vector DB CONGELATO; un-merge non necessario col merge manuale.

## Processo
Gate §3: revisore **#21 APPROVATO** (1 nota cosmetica chiusa in sessione). Report
`ultimo_report.md` riscritto.

## Invarianti
`_get_window` / `_cap_window_chars` / `for _ in range(10)` / sandbox bwrap / snapshot /
FTS5 / meccanismo merge nello store INVARIATI.
