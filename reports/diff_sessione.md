# 🔀 DIFF DI SESSIONE — 2026-06-18 (vector store fetta 1: storage + embedding)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni sessione.

## Tema
FASE 2 — retrieval semantico, **fetta 1**: SOLO storage + embedding come modulo
STANDALONE. Nessun aggancio a `ricorda`/`run_turn`/loop (wiring = fetta successiva,
solo PROPOSTA nel report §FINALE).

## File toccati
- **`modules/memory/vectors.py`** (NUOVO): `VectorStore`. Sidecar `.gas_vectors.db`
  separato dal `.db` sacro (cache derivata/ricostruibile, fuori dal backup). Schema
  multi-source `(id, source, source_ref, testo, ts, vettore BLOB, dim, model)`, v1 solo
  `source='diario'`. Embedding LOCALE fastembed (MiniLM-L12-v2 384-dim), prefissi e5
  per-modello nel codice. Brute-force cosine in numpy su vettori float32 normalizzati
  (dot product), top-k + soglia; niente sqlite-vec, niente ANN. `ricostruisci_da_diario`
  (embed-prima-di-svuotare, transazione). Fail-safe §9: import protetti,
  `available=False`→degrado, BLOB corrotto→`search` [] (R-vec-1).
- **`modules/memory/store.py`**: nuovo `diario_tutto()` SOLA LETTURA (per il rebuild
  dell'indice; immutabilità del diario intatta).
- **`modules/memory/__init__.py`**: esporta `VectorStore` & co (import fail-safe).
- **`requirements.txt`** (NUOVO): `openai`, `numpy`, `fastembed` (il deploy bozza lo
  assumeva già ma non esisteva).
- **`.gitignore`**: `.gas_vectors.db*` + cache pesi (`local_cache/`, `.fastembed_cache/`).
- **`tests/test_unit_kernel.py`**: T30a-f. Suite **139→145**, 0 FAIL.

## Decisione umana presa in sessione
Modello della spec `intfloat/multilingual-e5-small` assente da fastembed 0.8.0 →
STOP GATE → l'utente ha scelto ESPLICITAMENTE `paraphrase-multilingual-MiniLM-L12-v2`
(384-dim). Prefissi e5 non applicati (mappa per-modello, MiniLM → `("","")`), meccanismo
del prefisso comunque mantenuto nel codice.

## Processo
- Verifica DAL VIVO di fastembed: 384-dim, norma vettore grezzo ~4.2 (→ normalizzo io),
  download ~504MB, cold embed ~0.11s, similarità IT 0.876 vs 0.113.
- Review #23 (revisore) sul diff staged → **APPROVATO CON RISERVE**. R-vec-1 (fail-safe
  `search` su BLOB corrotto) CHIUSA in sessione su sua prescrizione (+T30f); R-vec-2
  (env-config) e R-vec-3 (ARM/RAM VPS) tracciate in `stato_progetto.md`.
- `gas.py` INVARIATO. Arch dev x86_64; VPS ARM/1GB RAM da validare al deploy (R-vec-3).
