# Report task — Allineamento canonici pre-S1 (FASE 5)
**Data:** 2026-07-02
**Scope:** DOC-ONLY. Allineare i canonici del repo allo stato reale della sonda S0 (eseguita 2026-06-30, mai committata). Zero modifiche al motore (gas.py, brains/, modules/, tests/). Nessuna review revisore necessaria.

---

## §1 SCOPE & ESITO FETTE

| Fetta | Titolo | Esito |
|-------|--------|-------|
| Fetta 0 | git pull + lettura stato_progetto.md corrente | **FATTA** |
| Fetta 1 | R-vec-pool: analisi fingerprint vector store | **FATTA** |
| Fetta 2 | Allineamento canonici (CX33, review #41, R-vec-pool, sicurezza, systemd) | **FATTA** |

---

## §2 FETTA 0 — STATO A TERRA

- `git pull` → Already up to date. Repo locale già allineato.
- `reports/stato_progetto.md` letto: riferiva CX22/4GB (ERRATO), review #40, CI run #28307518983 su cde4d94, suite 196 PASS 7 FAIL.
- `.claude/agents/memoria_revisore.md`: ultima lezione #40 (2026-06-28). Aveva una modifica locale non committata (aggiunta lezione #40 già scritta ma non staggiata).
- `reports/handoff.md` (sessione gas version): evidenza esplicita di review #41 APPROVATO, nessuna lezione nuova.
- CI `gh run list --branch main --limit 5`: ultima run reale = **#28539899123** (success, "Merge branch 'main'", 2026-07-01, commit `76cd3bb`).

---

## §3 FETTA 1 — REFERTO R-VEC-POOL

**File esaminato:** `modules/memory/vectors.py`

**Funzione che scrive il fingerprint** (`_write_fingerprint`, riga 226):
```python
con.execute("INSERT OR REPLACE INTO metadata VALUES ('model_id', ?)", (self.model_name,))
con.execute("INSERT OR REPLACE INTO metadata VALUES ('model_dim', ?)", (str(self.dim),))
```

**Funzione che lo legge e confronta** (`_read_fingerprint` + confronto in `__init__`, righe 214-197):
```python
stored_model, stored_dim = fp
if stored_model != self.model_name or stored_dim != self.dim:
    # mismatch → layer disabilitato
```

**Risposta alla domanda netta:**
Il fingerprint include **SOLO il nome/id del modello** (`model_id`) e la **dimensione** (`model_dim` = 384, costante hardcoded `EMBED_DIM`). **NON include** la versione di fastembed né il tipo di pooling (mean/CLS).

**Rischio — drift SILENZIOSO:**
Un bump di fastembed che cambia la strategia di pooling per lo stesso nome modello (es. mean→CLS sullo stesso `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) NON verrebbe rilevato dal guard:
- `stored_model` = `self.model_name` → match ✓
- `stored_dim` = 384 → match ✓ (la dim non cambia)
- Guard passa → layer ABILITATO
- Ma i vettori in DB sono stati computati con pooling A, le nuove query usano pooling B → le dot product restituiscono similarity sbagliate **senza alcun warning**

**Mitigazione attuale:** `requirements.txt` ha `fastembed==0.8.0` pinnato (revisione 2026-06-29). Il rischio è latente ma non attivo finché fastembed non viene aggiornato manualmente.

**Raccomandazione (senza toccare codice ora):**
1. Al deploy VPS: documentare `gas reindex` come prassi obbligatoria dopo ogni upgrade di fastembed (→ già aggiunto nelle Note operative VPS di stato_progetto.md).
2. In una review futura (bassa priorità, non S1): valutare di includere `fastembed.__version__` nel fingerprint → mismatch esplicito invece di drift silenzioso. Patch minimale: aggiungere una terza riga `('fastembed_ver', fastembed.__version__)` in `_write_fingerprint` e confrontarla in `__init__`.

**Finding aperto:** 🟡 **R-vec-pool** aggiunto a stato_progetto.md.

---

## §4 FETTA 2 — MODIFICHE APPORTATE

Tutte DOC-ONLY. File toccati: `reports/stato_progetto.md`, `reports/roadmap.md`.

### 4.1 CX22/4GB → CX33/8GB
- `stato_progetto.md` riga R-reidx-3: "Su CX22 4GB" → "Su CX33 8GB"
- `stato_progetto.md` riga R-vec-3: "sul CX22" → "sul CX33"
- `roadmap.md` (2 occorrenze): "CX22 4GB" e "sul CX22" → corretti
- `stato_storico.md`: nessuna occorrenza (verificato)

### 4.2 Conteggio review e suite (evidenza da CI + handoff)
- Review #41: APPROVATO (gas version 0.2.0, 2026-07-01) — evidenza da `reports/handoff.md` (§4 integrale). Nessuna lezione nuova → memoria_revisore.md correttamente ferma a #40.
- Suite CI (run #28539899123, Ubuntu runner, bwrap attivo): **208 PASS, 0 FAIL, 2 SKIP** (T9a/T9c skip su assenza API key live). Suite Windows locale (cloud sandbox gas version): 198 PASS, 5 FAIL (bwrap).
- CI reference aggiornato: run #28539899123 su `76cd3bb` — SUCCESS ✅

### 4.3 R-vec-3 aggiornamento
Aggiunta nota esplicita: "Chiusura R-vec-3 + misura RAM rinviate a **S1b** (primo embedding reale + pre-scald cache di proprietà utente runtime; NON lanciare embedding usa-e-getta root)."

### 4.4 R-vec-pool aperto
Aggiunto come finding 🟡 in stato_progetto.md (vedi §3 per dettaglio).

### 4.5 Note operative VPS — hardware corretto
Hardware VPS aggiornato a **CX33 / 8 GB Helsinki** (errore CX22 rimosso ovunque).

### 4.6 Nota ollama pavimento 3B
Aggiunta in Note operative VPS: ollama sul VPS deve usare modello 3B (es. qwen2.5:3b-instruct), NON 7B — gli 8 GB sono condivisi da GAS + embedder fastembed (~500 MB cache) + bot trading demo coabitante.

### 4.7 Contesto sicurezza S1 (bot trading coabitante)
Registrato in Note operative VPS:
- (a) `os_strict` OBBLIGATORIO finché il bot trading coabita
- (b) utente runtime non-root = requisito RAFFORZATO (chiavi exchange sulla stessa macchina di AI che esegue codice = superficie di esfiltrazione)

### 4.8 Decisione systemd ratificata
Registrata in Note operative VPS: `gas doctor` NON gatea l'avvio systemd (esce 1 anche su sole API key assenti). Comportamento corretto: `Restart=always` + notifica Telegram al primo turno se degradato.

---

## §5 VERIFICA FINALE

Grep CX22 post-edit su `reports/`:
- stato_progetto.md: 0 occorrenze ✅
- roadmap.md: 0 occorrenze ✅
- stato_storico.md: 0 (non c'era) ✅

Nessuna modifica a gas.py, brains/, modules/, tests/ — scope DOC-ONLY rispettato.

---

## §6 NOTE PER S1

S1 NON è stata avviata (scope di questo task = allineamento canonici). Azioni per S1:
- Aprire con checklist di sicurezza aggiornata (os_strict, non-root, bot trading context)
- S1b per chiusura R-vec-3: primo embedding reale + misura RSS → NON prima (cache root anti-pattern)
- Confermare VEC_MIN_SIM con diario reale (R-wire-1)
- `gas doctor` come verifica post-avvio (non gate), via notifica Telegram
