# Memoria FASE 2 — Normalizzazione chiavi lead (R-crm-1) + chiusura doc di due riserve

**Data:** 2026-06-17
**Commit motore:** `cdf764a` (review #16 APPROVATO)
**Suite:** **110/110, 0 FAIL** (era 106)
**Scope:** UNA fetta di motore (PUNTO 1) + due aggiornamenti doc (PUNTI 2-3). Gate di
scope rispettato: nessun lavoro fuori mandato (Vector DB / retention / merge-lead solo
registrati, NON implementati).

---

## PUNTO 1 — MOTORE: normalizzazione chiavi lead (chiude R-crm-1)

**Problema.** La rubrica deduplica solo a chiave ESATTA (vincolo UNIQUE), quindi
`'anna@ex.com'` e `'Anna '` diventavano due lead distinti. Con il CRM autopilot (GAS
popola la rubrica da solo) col volume questo genera doppioni silenziosi: la memoria che
dovrebbe impedire di reinseguire i lead inizia a mentire.

**Soluzione.** Funzione PURA e testabile in `modules/memory/store.py`:

```python
def normalizza_chiave(chiave: Optional[str]) -> str:
    if chiave is None:
        return ""
    try:
        testo = str(chiave)
    except Exception:
        return ""
    return " ".join(testo.split()).lower()
```

- **Deterministica, NIENTE aggressività**: solo coercizione a `str`, collasso di ogni
  whitespace (anche tab/newline) via `str.split()` + `lower()`. Nessun fuzzy match,
  nessun merge euristico — solo canonicalizzazione prevedibile.
- **Applicata in UN unico punto logico** (la funzione) nei DUE punti di confronto-esatto:
  - **scrittura** → `upsert_contatto` (prima di INSERT e SELECT);
  - **lettura/match esatto** → `get_contatto_per_chiave`.
  Così la stessa chiave logica risolve SEMPRE allo stesso record.
- `update_stato_contatto` lavora per **id** (già risolto a monte via
  `get_contatto_per_chiave` dentro `_imposta_stato_contatto`) → coperto, non serve
  normalizzare lì.
- **Asimmetria preservata**: il substring di lettura (`_trova_contatto`) NON è toccato;
  la normalizzazione si applica al CONFRONTO esatto, non trasforma il substring in altro.
- **Type hints** (§4): `Optional[str] -> str`.
- **Fail-safe** (§9): chiave None/non-stringa → `""` (mai crash); la chiave vuota è poi
  rifiutata a monte da `_salva_contatto`.
- Esportata da `modules/memory/__init__.py`.

**CASO MIGRAZIONE.** DB di sviluppo VUOTO (`.gas_memory.db` ASSENTE, verificato dal vivo
prima di toccare il codice) → **nessuna migrazione necessaria, nessun rischio di record
irraggiungibili**. Se in futuro esistessero chiavi non normalizzate da test/demo:
strategia PROPOSTA (NON eseguita) = script idempotente una-tantum che, per ogni contatto,
calcola `normalizza_chiave(chiave)` e fonde i record collidenti tenendo il più recente —
decisione umana, MAI distruttiva in autonomia.

---

## PUNTO 2 — DOC: riserve di 2b nei finding aperti

**Nota di onestà (riconciliazione con review #15).** Il mandato chiedeva di aggiungere
come finding 🟡 le riserve R2/R3 di 2b "che oggi compaiono solo nel verdetto review #14".
Verificato nel codice: la review **#15 (già in repo)** le aveva GIÀ chiuse —
`MEMORY_PIN_CHARS/CONTACTS/EVENTS` resi overridabili via env (`GAS_MEMORY_PIN_*`), e
l'euristica `MEMORY_PIN_EVENTS*5` SOSTITUITA da `MEMORY_PIN_SCAN=200`. Per non scrivere un
finding falso (riaprire qualcosa di già risolto), ho tracciato il **residuo REALE** che
incarna lo stesso intento — non perdere queste classi di rischio:

- 🟡 **R2-residuo**: `MEMORY_PIN_SCAN=200` resta HARDCODED senza override env (le tre
  costanti principali del pin sono già overridabili). Stessa classe di
  `WINDOW_CHAR_CAP`/`SNAPSHOT_KEEP`; valutare `GAS_MEMORY_PIN_SCAN` (via `_env_int`,
  fail-safe) al deploy VPS. (`DIARIO_NOISE_TIPI` resta hardcoded di proposito.)
- 🟡 **R3-residuo**: `MEMORY_PIN_SCAN=200` è un **numero magico** scelto a priori, da
  tarare con dati reali quando il diario avrà volume.

Entrambi non bloccanti, ora in "Finding aperti" di `stato_progetto.md`.

---

## PUNTO 3 — DOC: stato del Vector DB

Registrato in `reports/stato_progetto.md` → "Prossimi passi" voce **0**: il **Vector DB
per i ricordi semantici** è il prossimo passo GROSSO di FASE 2, **NON ancora avviato per
scelta** (dipendenze nuove, possibili costi di embedding, filosofia "robustezza prima
della potenza"), **da PROGETTARE prima di implementare** (libreria locale vs. servizio,
modello di embedding, dove vive il file, fail-safe §9, composizione col pin always-on e
col tool `ricorda`). Nessun impegno preso: stato esplicito così non evapora.

---

## VERIFICHE (eseguite e dimostrate)

### A. Suite completa
`python tests/test_unit_kernel.py` → **`=== RIEPILOGO: 110 PASS, 0 FAIL ===`**
(era 106; +4 con i T23). Zero token, tutto locale.

### B. I 4 test del PUNTO 1 (tutti PASS)
- **T23a** (R-crm-1) chiavi equivalenti = stesso record, nessun doppione —
  `id_a==id_b`, `lista_contatti()==1`, chiave salvata `"anna"`. **PASS**
- **T23b** `imposta_stato_contatto` trova il lead con chiave non normalizzata in input
  (`"  bob   white "` → record `"bob white"`), stato aggiornato, 1 solo record. **PASS**
- **T23c** fail-safe: `normalizza_chiave(None)==""`, `("   ")==""`, `(12345)=="12345"`,
  `get_contatto_per_chiave(None)` → `None`, nessun crash. **PASS**
- **T23d** idempotenza: `normalizza(normalizza(x))==normalizza(x)` su 6 campioni
  (spazi/tab/newline/unicode/vuoto) + esiti attesi. **PASS**

### C. Diff del commit motore + invarianti
`git diff --cached --stat` del commit `cdf764a`:
```
 modules/memory/__init__.py |  2 ++
 modules/memory/store.py    | 35 ++++++++++++++++++++++++++++++++-
 tests/test_unit_kernel.py  | 49 ++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 85 insertions(+), 1 deletion(-)
```
**`gas.py` NON è tra i file modificati (INVARIATO).** Confermato esplicitamente, sui diff
reali: `_get_window`, `_cap_window_chars`, `for _ in range(10)`, sandbox/bwrap, snapshot,
i trigger di immutabilità del diario e lo schema della fetta 1 sono **INVARIATI** (grep
sul diff di `store.py` → nessuna di queste invarianti compare). L'unico tocco è la
funzione `normalizza_chiave` + le due righe che la applicano in `upsert_contatto` e
`get_contatto_per_chiave` + una riga di docstring.

### D. Migrazione
DB di sviluppo **VUOTO** (`.gas_memory.db` assente) → nessuna chiave non normalizzata,
**nessuna migrazione eseguita né necessaria**. Strategia proposta documentata sopra
(PUNTO 1) per il caso futuro, lasciata alla decisione umana.

---

## PROCESSO

- **Gate di review §3**: subagent **revisore** invocato sul diff staged PRIMA del commit
  motore → **review #16 APPROVATO**. Unica riserva minore (cosmetica) **R-crm-norm-1**:
  l'eco testuale della chiave nei messaggi di successo dei tool (`gas.py`) mostra l'input
  RAW e non la forma canonica salvata (il dato nel DB è corretto) → tracciata in
  `stato_progetto.md`, chiudibile al prossimo intervento su `gas.py`, fuori scope qui.
- Hook deterministico onorato (`.claude/.review_ok` creato per il commit motore, rimosso
  subito dopo).
- `stato_progetto.md` e `diff_sessione.md` aggiornati.

---

## §FINALE — Proposte FUORI da questo mandato (NON committate, scope deciso dall'umano)

Il GATE imponeva SOLO i tre punti. Emerse durante il lavoro, NON eseguite:

1. **Tool di merge-lead / migrazione idempotente delle chiavi**: utile se mai si
   accumulassero chiavi non normalizzate (oggi DB vuoto → non serve). Strategia bozzata
   in PUNTO 1, da approvare separatamente.
2. **`GAS_MEMORY_PIN_SCAN` env override** (chiude il R2-residuo qui tracciato): coerente
   con `_env_int` già esistente, un'aggiunta minima — ma tocca `gas.py`, fetta a sé.
3. **R-crm-norm-1**: normalizzare anche l'eco della chiave nei messaggi di successo dei
   tool (`gas.py`), così schermo e DB coincidono. Cosmetico, fuori scope.
4. **Vector DB** (PUNTO 3): solo registrato come stato, da progettare prima di implementare.

Nessuna di queste è stata toccata: lo scope lo decide l'umano, non il revisore.
