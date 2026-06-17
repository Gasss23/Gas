# 🔀 DIFF DI SESSIONE — 2026-06-17 (Memoria FASE 2: onestà R-crm-1 + blindatura test)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché

### 1. TEST — blindatura interazione substring↔normalizzazione (commit `f4b2321`)
- **`tests/test_unit_kernel.py`** (+28): due nuovi test, `gas.py` INVARIATO.
  - **T23e**: lead salvato con chiave NON normalizzata (`"  Anna   Rossi "`, storata
    `"anna rossi"`) → cercato via tool `ricorda` con varianti `"anna rossi"` (risolve
    via match esatto normalizzato) e `"ANNA"` (risolve via substring case-insensitive)
    → TROVATO. Prova che la scrittura-normalizzata e la lettura-substring (non toccata)
    restano coerenti.
  - **T23f**: `"anna@ex.com"` e `"Anna"` salvati come due `salva_contatto` distinti →
    restano DUE record (la normalizzazione lessicale NON fonde identità cross-formato).
    Test che incarna ONESTAMENTE il limite APERTO R-crm-1b, così nessun futuro
    intervento lo "aggiusta" per sbaglio (no verde fittizio, §5).
- **Perché**: dopo la normalizzazione in scrittura (cdf764a) mancava la prova che la
  lettura substring trovasse ancora i lead. T23e la fornisce (e NON fallisce → nessun
  gap di read-path). T23f fissa il confine tra ciò che la normalizzazione fa e ciò che
  NON deve fare. Suite **110 → 112**, 0 FAIL.

### 2. DOC (commit doc separato)
- **`reports/stato_progetto.md`**: la voce "R-crm-1 CHIUSA" SPACCATA in due — **R-crm-1
  (case/whitespace) ✅ CHIUSA** e **R-crm-1b (identità cross-formato) 🟡 APERTA** (stesso
  lead con chiavi semanticamente diverse, es. email vs nome; non è migrazione, esiste a
  runtime; difesa da progettare: chiave canonica o tool merge-lead, nessun impegno).
  Aggiornati conteggio suite (112) e voce dei nuovi test.
- **`reports/ultimo_report.md`**: report canonico del task.

### Processo rispettato
- Gate di review §3: il commit dei test tocca `tests/` → subagent **revisore** invocato
  sul diff staged PRIMA del commit → **APPROVATO** (verificato dal vivo + mutation
  testing: mutando il `.lower()` del needle T23e cade → il test morde davvero; gas.py e
  store.py ripristinati bit-identici). Hook deterministico onorato (`.claude/.review_ok`
  creato per il commit test, rimosso subito dopo). Il PUNTO 1 è doc-only → nessuna review.
- Scope BLOCCANTE rispettato: SOLO i due punti del mandato. `_trova_contatto`/read-path
  NON toccati; nessun env override, fix echo, Vector DB, merge tool — solo registrati/
  proposti nel §FINALE del report.

## File toccati (sintesi)
`tests/test_unit_kernel.py` (+T23e/f) · `reports/stato_progetto.md` (split R-crm-1/1b) ·
`reports/ultimo_report.md` · `reports/diff_sessione.md` (questo) ·
`.claude/agents/memoria_revisore.md` (lezione 2026-06-17).
Commit test: `f4b2321` (T23e/f — review APPROVATO). gas.py INVARIATO.
