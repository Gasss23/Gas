# Diff Sessione — K3-bis FTS5

**Data:** 2026-09-29  
**Branch:** feat/autonomia-k3-bis (basato su feat/autonomia-k3-k4 via merge)

## File toccati (diff da main)

| File | Tipo | Motivo |
|------|------|--------|
| `gas.py` | modifica | `_knowledge_fts_match()` + `_knowledge_search` FTS5 al posto di LIKE |
| `tools/ingest_knowledge.py` | modifica | `_init_fts()`: FTS5 table + trigger + backfill |
| `gas_identity.md` | modifica | Regola ricorda con parole chiave semplici |
| `tests/test_unit_kernel.py` | modifica | `_make_knowledge_root()` FTS5 + T69-fts-a/b/c/d/e |
| `tests/e2e/e2e_k3k4_llm.py` | riscrittura | R-e2e-2 fix + injection innocua + criterio ≥2/3 |
| `reports/ultimo_report.md` | aggiornamento | risultati K3-bis |
| `reports/stato_progetto.md` | aggiornamento | stato corrente + nota storica "K3 era 0/3" |

## Cosa è cambiato e perché

**FTS5 su knowledge (FETTA 1)**: la ricerca LIKE falliva quando il modello passava frasi intere o
query multi-parola con parole diverse da quelle nel chunk. FTS5 con tokenizzazione OR
(ogni token ≥3 char) trova i chunk per parole chiave indipendenti.

**Guida al modello (FETTA 2)**: senza una regola esplicita in gas_identity.md, il modello
non chiamava ricorda per D1/D2 (rispondeva dal proprio training). La regola porta D2+D3
a usare ricorda con parole chiave semplici, che FTS5 matcha correttamente.

**E2E reale**: 2/3 ≥ criterio. D1 ("iterazioni" parola singola ambigua) ancora non chiama
ricorda — comportamento atteso perché il termine è generico. Iniezione NULLO: la domanda
sulle ricette non è Gas-specifica, il modello (correttamente) non consulta la knowledge base.

## Commit di sessione

- `b76c120` — feat(autonomia): K3-bis — FTS5 su knowledge + regola ricorda in gas_identity (review #111)
