# Ultimo Report — 2026-06-27 — D1/D2: fix probe vector doctor + disable_reason

## DECISIONI UMANE RICHIESTE

Nessuna. D1 e D2 approvate dall'umano dopo la sonda read-only della sessione.

## Task eseguito

Fix di due gap di observability rilevati dalla sonda probe_telemetria (sessione 2026-06-27):

**D1 — gas doctor: path vector store ora rispetta GAS_VECTORS_DB**  
`gas.py:1628` usava `default_vectors_path(root)` hardcoded, ignorando `GAS_VECTORS_DB` env.
Fix: stesso pattern di `GasKernel.__init__` (gas.py:368-369) — legge `GAS_VECTORS_DB`, risolve
il path configurato, fallback al default solo se non settato. Ora probe e runtime guardano
sempre lo stesso DB.

**D2 — VectorStore.disable_reason: motivo specifico del disable ora visibile in doctor**  
Aggiunto attributo pubblico `disable_reason: str = ""` a `VectorStore.__init__`. Valorizzato
in ciascun ramo di fallimento del fingerprint-guard:
- fingerprint assente (DB legacy) → `"DB legacy: fingerprint assente — esegui 'gas reindex'"`
- fingerprint mismatch → `"fingerprint mismatch: DB 'X' != configurato 'Y' — esegui 'gas reindex'"`
- `sqlite3.Error` / `OSError` → `"init sidecar fallita: <errore[:80]>"`
- db ok ma embedder assente → `"deps embedding assenti (numpy o fastembed mancanti)"`

Doctor lo legge con `getattr(_vs_probe, "disable_reason", "")` (retrocompatibile) e lo
include nel WARN al posto del vecchio messaggio generico `"deps assenti o sidecar corrotto"`.

## Commit

- `29188f9` — fix(doctor): D1 path GAS_VECTORS_DB + D2 disable_reason visibile — review #35

## Review

Review #35 — **APPROVATO CON RISERVE** (revisore subagent).  
Riserve: T39b/c non assertiscono il valore di `disable_reason`; mancano test per rami
`sqlite3.Error` ed embedder-unavailable. Non bloccanti — tracciate in stato_progetto.md.

## File toccati

```
gas.py                    | +9 -2  (doctor: path fix D1 + lettura disable_reason D2)
modules/memory/vectors.py | +9     (disable_reason attribute + valorizzazione in 4 rami)
reports/stato_progetto.md | +1     (riserve review #35)
```
