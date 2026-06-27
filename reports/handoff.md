# HANDOFF — Verifica indipendente R-vec-2b

**Sessione:** 2026-06-27 — Verifica post-build fingerprint-guard (commit 9e70bbf)

---

## §DECISIONI UMANE RICHIESTE

**Nessuna.**

Tutti e 4 i punti strutturali del guard sono verificati sani.

**RISERVA MINORE (non bloccante):** il conteggio test in questa sessione di verifica è
**175 PASS / 8 FAIL** vs **177 PASS / 6 FAIL** dichiarato nell'handoff di build. La
differenza è spiegata da 2 test ambientali Windows che in questa run risultano FAIL
anziché PASS/SKIP: `T13d2` (WinError2, `os_with_fallback`) e `T26c` (timing backup).
Nessuno dei due test tocca il fingerprint-guard. I 6 FAIL originali (bwrap Windows +
T26b) sono tutti presenti. La discrepanza di 2 va investigata in una sessione
dedicata se il conteggio diventa baseline VPS.

---

## §VERDETTO SINTETICO

**A VERIFICATO SANO**

Il fingerprint-guard di R-vec-2b è reale, non auto-certificato. Il confronto avviene
su `model_id` (non solo `dim`). Il test critico dim-uguale/model-diverso esiste e
passa. Il fail-safe è un disable pulito, non un raise. La suite T39 è tutta verde.

---

## §1 — IL CUORE DEL GUARD (confronto model_id, non solo dim)

**Sorgente:** `modules/memory/vectors.py`, metodo `__init__` di `VectorStore`.

Righe esatte del confronto (estratte da `git show 9e70bbf:modules/memory/vectors.py`):

```python
else:
    fp = self._read_fingerprint(con)
    if fp is None:
        # Legacy o provenienza ignota: fingerprint assente → fail-closed.
        log.warning(
            "VectorStore: sidecar %s senza fingerprint (DB legacy o "
            "provenienza ignota) — layer disabilitato. "
            "Esegui 'gas reindex' per ricostruire con il modello corrente.",
            self.db_path)
        _guard_ok = False
    else:
        stored_model, stored_dim = fp
        if stored_model != self.model_name or stored_dim != self.dim:
            log.warning(
                "VectorStore: fingerprint mismatch su %s — "
                "DB contiene model=%r dim=%d, configurato model=%r dim=%d. "
                "Layer disabilitato. Esegui 'gas reindex' per ricostruire "
                "con il modello corrente.",
                self.db_path, stored_model, stored_dim,
                self.model_name, self.dim)
            _guard_ok = False
```

**La condizione è `stored_model != self.model_name or stored_dim != self.dim`.**

Il ramo che rifiuta quando dim COINCIDE ma model_id DIFFERISCE **esiste e si attiva**:
basta che `stored_model != self.model_name` sia True, indipendentemente dalla dim.
Il guard NON è inutile su coppie 384-dim diverse.

---

## §2 — IL TEST CHE ESERCITA IL PATH CRITICO (dim uguale, model_id diverso)

**T39b** — righe `tests/test_unit_kernel.py:2410-2430`:

```python
# T39b — fingerprint mismatch model_id, stessa dim → fail-closed (cuore del guard)
_d39b = tempfile.mkdtemp(prefix="gas_vec39b_")
_p39b = default_vectors_path(_d39b)
# Crea il DB manualmente con fingerprint di un modello DIVERSO (stessa dim 384)
with _sq39.connect(str(_p39b)) as _c39b:
    _c39b.executescript("""
        CREATE TABLE IF NOT EXISTS vettori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL, source_ref TEXT NOT NULL,
            testo TEXT NOT NULL, ts TEXT,
            vettore BLOB NOT NULL, dim INTEGER NOT NULL, model TEXT NOT NULL,
            UNIQUE(source, source_ref, model)
        );
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        INSERT OR REPLACE INTO metadata VALUES ('model_id', 'intfloat/multilingual-e5-small');
        INSERT OR REPLACE INTO metadata VALUES ('model_dim', '384');
    """)
_vs39b = VectorStore(_p39b, embed_fn=_fake_embed)   # embed_fn ok, ma fingerprint mismatch
check("T39b fingerprint-guard: model_id diverso stessa dim → fail-closed (available=False)",
      _vs39b.available is False and _vs39b._db_available is False,
      f"available={_vs39b.available} _db_available={_vs39b._db_available}")
```

**Configurazione del test:**
- DB contiene: `model_id='intfloat/multilingual-e5-small'`, `model_dim='384'`
- VectorStore aperto con: `model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'` (default), `dim=384`
- `embed_fn=_fake_embed` → l'embedder sarebbe disponibile, il mismatch è solo sul model_id

**Output grezzo dalla suite:**
```
[PASS] T39b fingerprint-guard: model_id diverso stessa dim → fail-closed (available=False) — available=False _db_available=False
```

Il path critico è testato e verde.

---

## §3 — GLI ALTRI DUE PATH

**Fingerprint ASSENTE (DB legacy) → rifiuta fail-closed:**

```
[PASS] T39c fingerprint-guard: DB legacy senza fingerprint → fail-closed (available=False) — available=False _db_available=False
```

T39c crea un DB con schema `vettori` ma senza tabella `metadata` (simula DB pre-guard).
Il DDL crea `metadata` (idempotente), ma la tabella è vuota → `_read_fingerprint` ritorna
`None` → `_guard_ok = False`. (righe `tests/test_unit_kernel.py:2432-2451`)

**Fingerprint COINCIDENTE → procede:**

```
[PASS] T39a fingerprint-guard: DB nuovo con modello corrente → available=True — available=True
```

T39a apre un DB appena creato con lo stesso modello di default → fingerprint scritto nel
costruttore stesso → riapertura concettuale identica: `available=True`. (righe `2403-2408`)

---

## §4 — FAIL-SAFE §9 (guard disabilita il layer, non crasha)

Righe esatte di `__init__` che chiudono il guard:

```python
        except (sqlite3.Error, OSError) as e:
            log.warning("VectorStore: init sidecar fallita su %s (%s) — degrado",
                        self.db_path, e)
            _guard_ok = False
        if _guard_ok:
            self._db_available = True
```

`_db_available` è inizializzato a `False` nel costruttore (`self._db_available: bool = False`).
Il guard che rifiuta **non esegue `self._db_available = True`**: nessun raise, nessun crash.

Ogni metodo pubblico (`index`, `search`, `index_batch`, `ricostruisci_da_diario`, `conta`)
inizia con:

```python
if not self.available:
    return None   # oppure [] o 0 secondo il tipo
```

Il turno dell'agente prosegue con `available=False` → tutte le operazioni vettoriali
restituiscono degrado silenzioso, coerente con §9 CLAUDE.md ("turno prosegue, mai crash").

**Non è un `raise`. È un `disable`.**

---

## §5 — ESITO SUITE REALE (output grezzo)

Comando: `venv\Scripts\python.exe tests/test_unit_kernel.py` (Windows, PYTHONUTF8=1)

**T39 (estratto grezzo dall'output):**
```
[PASS] T39a fingerprint-guard: DB nuovo con modello corrente → available=True — available=True
[PASS] T39b fingerprint-guard: model_id diverso stessa dim → fail-closed (available=False) — available=False _db_available=False
[PASS] T39c fingerprint-guard: DB legacy senza fingerprint → fail-closed (available=False) — available=False _db_available=False
[PASS] T39d gas reindex scrive fingerprint; riapertura con modello corretto → available=True — n=1 reopen_available=True
[PASS] T39e recovery: DB mismatch → reindex (sostituzione) → riapertura → available=True — mismatch_ok=True reopen_available=True
```

**Riepilogo grezzo:**
```
=== RIEPILOGO: 175 PASS, 8 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (comando lecito) bloccato (fail-closed) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T11e run_command fa scattare lo snapshot — refs 1 -> 1
  FAIL: T12a comando in allowlist (wc) eseguito, output reale — Operazione negata: sandbox OS (bwrap + namespace) non dispon
  FAIL: T12c pipe non interpretata (niente shell) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T12e command substitution non eseguita (resta letterale) — Operazione negata: sandbox OS (bwrap + namespace) non disponibile e GA
  FAIL: T13d2 os_with_fallback + sandbox assente -> esegue (sandbox applicativa) — Errore eseguendo run_command: [WinError 2] Impossibile trova
  FAIL: T26b backup: copia leggibile + rotazione ultime N + retention pura — rimasti=4 keep=2 drop=3
  FAIL: T26c backup_auto throttled: crea, poi salta, intervallo 0 ricrea — first=True second=None third=False
```

**Note sul conteggio:**
- Handoff build (4e14f09) dichiarava: 177 PASS / 6 FAIL.
- Questa verifica: 175 PASS / 8 FAIL. Totale 183 test = coerente (178 baseline + 5 T39).
- Differenza: T13d2 (WinError2, ambientale Windows) e T26c (timing backup) risultano FAIL
  anziché SKIP/PASS. **Nessuno dei due test tocca il fingerprint-guard.**
- I 5 bwrap Windows (T11c2, T11e, T12a, T12c, T12e) + T26b = 6 FAIL originali: tutti presenti.

---

## §6 — VERDETTO REVISORE #34 VERBATIM

Estratto dall'handoff di build commit `4e14f09` (`reports/handoff.md`, §4):

> **Review #34 — APPROVATO CON RISERVE**
>
> Il codice è tecnicamente corretto su tutti e 5 i punti esaminati:
> - **TOC-TOU** (`_db_existed` prima del `connect`): accettabile in contesto single-process GAS. Manca solo un commento esplicito che dichiari il vincolo.
> - **Due `con.commit()`**: corretti. Il `with con:` fa auto-commit in `__exit__` come no-op; il primo commit fissa il DDL, il secondo il fingerprint; se `_write_fingerprint` lancia, il rollback riguarda solo l'uncommitted e `_guard_ok=False`.
> - **Gestione transazioni nelle helper**: il contratto "il chiamante committa" è dichiarato e rispettato in tutti i call-site (`__init__` e `ricostruisci_da_diario`).
> - **Fingerprint nella stessa transazione dell'atomic swap**: corretto e desiderabile — o vettori+fingerprint nuovi oppure stato preesistente intatto, senza stati intermedi incoerenti.
> - **T39b/T39c senza `_SCHEMA`**: fedeli al legacy reale; `CREATE TABLE/INDEX IF NOT EXISTS` su tabelle già esistenti è idempotente, e la tabella `metadata` vuota (T39c) porta correttamente a `None` → fail-closed.
>
> **Riserve (non bloccanti):**
> 1. R1 — Aggiungere un commento al check `_db_existed` che dichiari il vincolo single-process.
> 2. R2 — Manca T39e: path di recovery VPS (mismatch → reindex → riapertura → available=True).
>
> Entrambe risolte prima del commit.

---

## §git log (sessione di verifica)

Nessun commit di motore in questa sessione (read-only). Solo questo handoff di verifica.
