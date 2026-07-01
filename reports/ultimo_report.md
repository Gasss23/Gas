# Report — Correttivo DOC-ONLY post-a15ff61 (FASE 5, 2026-07-02)

> Scope: DOC-ONLY sopra a15ff61. Zero modifiche a gas.py, brains/, modules/, tests/.
> Nessuna review revisore (nessun file motore toccato).

## §1 SCOPE & ESITO FETTE

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| 0 | git pull + lettura stato_progetto.md corrente (post-a15ff61) | **FATTA** |
| 1 | Verifica conteggio 208 test su CI run #28539899123 | **FATTA** |
| 2 | Chiusura R-vec-3 su evidenza sonda S0 + aggiornamento stato_progetto.md | **FATTA** |
| 3 | Fatti macchina reali (sonda 2026-07-02) + FINDING no-swap in stato_progetto.md | **FATTA** |
| 4 | Requisito non-root specifico (VECTORS_DB /root/gas/.gas_vectors.db) in stato_progetto.md | **FATTA** |
| 5 | Verifica lezione #40 dangling in memoria_revisore.md | **FATTA** — già committata, nessun diff pendente |

---

## §2 FETTA 1 — Verifica conteggio 208 (CI run #28539899123)

### Riga grezza dal log CI (evidenza)

```
unit-suite  UNKNOWN STEP  2026-07-01T18:43:45.9338850Z  === RIEPILOGO: 208 PASS, 0 FAIL ===
```

### 2 SKIP confermati da log

```
[SKIP] T9a ogni provider cappato a 10 iterazioni — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI
[SKIP] T9c storia salvata su disco nella root temporanea — richiede API key live (GEMINI_API_KEY, GROQ_API_KEY), skip in CI
```

### Verdetto

Il log conferma **208 PASS, 0 FAIL**. Il "2 SKIP" in stato_progetto.md è ricavato dai `[SKIP]` T9a/T9c (il RIEPILOGO custom non li conta separatamente). Il numero 208 è corretto — **nessuna correzione** a stato_progetto.md necessaria per il conteggio.

---

## §3 FETTA 2 — Chiusura R-vec-3

### Stato precedente
`🟡 RIDOTTO` — wheels installabili confermate, embedding a runtime NON ancora provato su CX33.

### Evidenza sonda S0 (2026-06-30, box CX33)
```
[OK] BAAI/bge-small-en-v1.5: dims=384 load=3.5s embed=0.01s
[OK] sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2: dims=384 load=5.0s embed=0.02s (UserWarning: mean pooling invece di CLS)
PICCO_RSS_MB 697
```

### Azioni in stato_progetto.md
- R-vec-3: da `🟡 RIDOTTO` a `✅ CHIUSO`.
- Boundary esplicito registrato: prova che l'embedder importa e produce vettori di dim corretta sul box reale; NON prova qualità semantica (→ R-wire-2) né comportamento sotto carico RAM concorrente.
- Rimossa nota "chiusura R-vec-3 rinviata a S1b" (ora chiuso; a S1b resta solo la misura RAM a regime del singolo modello).
- Caveat RSS: picco 697MB misurato a DUE modelli residenti; produzione carica UN SOLO modello → footprint reale < 697MB; 697 = ceiling conservativo.
- Prossimi passi item 6: rimosso R-vec-3 dalla checklist, aggiunta nota "R-vec-3 ✅ chiuso".

---

## §4 FETTA 3 — Fatti macchina (sonda 2026-07-02, box CX33)

### Dati rilevati
```
uname -m = x86_64
nproc = 4
Mem total 7.6Gi, available 7.1Gi (a vuoto)
Disco / 75G, 70G liberi (4% usato)
SWAP = 0B (NESSUNO swap configurato)
```

### Azioni in stato_progetto.md
- Hardware aggiornato con specifiche reali: x86_64, 4 core, 7.6Gi RAM usabile (7.1Gi a vuoto), 70Gi disco liberi.
- 🔴 FINDING no-swap registrato con le tre conseguenze:
  - (a) Unit systemd S1b: MemoryHigh ~1.5Gi / MemoryMax ~2Gi su GAS.
  - (b) Ollama 3B always-on: rivalutare → on-demand o 1-1.5B; decisione rinviata a S3.
  - (c) OPZIONE S1a (non decisa): swap file 2-4Gi come cuscinetto h24.

---

## §5 FETTA 4 — Requisito non-root specifico

### Evidenza sonda S0
```
VECTORS_DB /root/gas/.gas_vectors.db
```
Runtime + cache/db girano sotto `/root` come root.

### Azione in stato_progetto.md
Aggiunta clausola (c) a nota #3 "Contesto sicurezza OBBLIGATORIO per S1":
> Requisito esplicito S1: creare utente runtime dedicato non-root e spostare working dir + model cache + `.gas_*.db` fuori da `/root`, di proprietà di quell'utente.

Il giro precedente aveva il contesto generico non-root; questa è la fotografia specifica del fatto.

---

## §6 FETTA 5 — Lezione #40 dangling

`git diff HEAD -- .claude/agents/memoria_revisore.md` → output vuoto. Nessuna modifica pendente. Già committata nel giro precedente. **Nessuna azione necessaria.**

---

## §7 NOTE SULLO SCOPE

- Zero modifiche a file motore (gas.py, brains/, modules/, tests/). Gate revisore non attivato.
- `reports/verifica_fase25.md` era già presente come untracked pre-sessione — non appartiene a questo task, lasciata invariata.
- S1 non iniziata. Proposta di prima riga S1 da fare in sessione dedicata.
