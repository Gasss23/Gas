# SONDA R-crm-1b — Fetta 0: anatomia del CRM attuale

**Sessione:** feature/crm-dup-detect — 2026-07-14
**Scope:** sonda di lettura del codice reale. NESSUN codice scritto.

---

## Domanda 1 — Come si costruisce `chiave_norm` in `upsert_contatto`?

Il tool `salva_contatto` del loop chiama `gas.py:1221` → `_salva_contatto` → `memory.upsert_contatto`.

In `store.py:376`:

```python
chiave_norm = normalizza_chiave(chiave)
```

dove `chiave` è il **primo argomento** di `upsert_contatto` (l'identificatore dichiarato dal modello:
es. `'anna@ex.com'`, `'Anna Rossi'`, `'+39 333 000'`).

`normalizza_chiave` (`store.py:148-186`) è **pura e lessicale**:

```python
testo = unicodedata.normalize("NFKC", str(chiave))
return " ".join(testo.split()).lower()
```

Step in ordine: str → NFKC (unifica varianti tipografiche) → collasso whitespace via `split()` → `lower()`.

**NON** estrae la parte locale dell'email, **NON** toglie il `+` del telefono, **NON** usa il
campo `nome`. La docstring lo dice esplicitamente (store.py:164-165):

> v1: NESSUNA logica speciale per telefono/email (es. strip del '+' iniziale o del dominio):
> è solo canonicalizzazione LESSICALE.

`chiave_norm` **deriva unicamente dal valore passato come `chiave`**, non da email/nome/telefono
in campi separati.

---

## Domanda 2 — Due contatti con la STESSA email: collidono o sono due record?

**Dipende da come viene usato il campo `chiave`.**

Caso A — l'email è la `chiave` (uso corretto):

```python
salva_contatto(chiave='anna@ex.com', nome='Anna')
salva_contatto(chiave='anna@ex.com', nome='Anna Rossi')   # seconda chiamata
```

`chiave_norm = 'anna@ex.com'` in entrambi → `ON CONFLICT(chiave_norm) DO UPDATE` (store.py:387).
**Un solo record**: la seconda chiamata aggiorna il primo (nessun duplicato).

Caso B — il modello usa chiavi diverse per la stessa persona (es. nome vs email):

```python
salva_contatto(chiave='anna rossi', contatto='anna@ex.com')
salva_contatto(chiave='anna@ex.com')
```

`chiave_norm('anna rossi') = 'anna rossi'` ≠ `chiave_norm('anna@ex.com') = 'anna@ex.com'`
→ **DUE record distinti**. Questo è il duplicato cross-formato che R-crm-1b deve rilevare.

Il campo `contatto` (TEXT libero, store.py:108) può contenere email/telefono/handle ma
**non è la chiave** e non partecipa all'indice UNIQUE. L'unica identità è `chiave_norm`.

**Conclusione: il caso "stessa email = due contatti" ESISTE** ogni volta che lo stesso recapito
appare come `chiave` per un salvataggio e in `contatto` per un altro (o in `chiave` con forme
diverse). Lo scope di R-crm-1b è reale.

---

## Domanda 3 — Esiste un campo telefono normalizzato?

No. Schema tabella `contatti` (store.py:95-121):

| campo | tipo | ruolo |
|---|---|---|
| `chiave` | TEXT NOT NULL | grafia originale dell'identità (as-entered) |
| `chiave_norm` | TEXT NOT NULL | forma canonica (UNIQUE, deriva da `chiave`) |
| `nome` | TEXT | nome leggibile |
| `contatto` | TEXT | **campo libero**: email/telefono/handle — non normalizzato |
| `stato` | TEXT | stato funnel |
| `note` | TEXT | testo libero |

`normalizza_chiave` si applica **solo** al campo `chiave` al momento dell'upsert.
Il campo `contatto` entra nel DB esattamente come passato dal modello, senza alcuna
canonicalizzazione. Non esiste un campo separato per email o telefono.

Implicazione: due schede della stessa persona potrebbero avere
`contatto='anna@ex.com'` l'una e `chiave='anna@ex.com'` l'altra —
il rilevatore deve confrontare i due campi cross-record.

---

## Domanda 4 — Com'è fatto `unisci_contatti` oggi?

**Store** (`store.py:428`):

```python
def unisci_contatti(self, chiave_da: str, chiave_verso: str) -> Optional[int]:
```

Firma: due chiavi (non ID). Risolve entrambe al canonico via `_risolvi_canonico`
(segue `merged_into` se è già una lapide). Poi:

1. **COALESCE anagrafica**: completa i campi NULL del canonico (`chiave_verso`) dai dati
   del doppione (`chiave_da`) — solo i campi assenti, non sovrascrive mai.
2. **Ri-punta lapidi**: UPDATE su `contatti.merged_into` dai vecchi puntatori a `da`
   verso il canonico (invariante: catena profonda max 1).
3. **Marca lapide**: `da.merged_into = canonico_id` — il doppione diventa lapide.

Nessun UPDATE/DELETE sul diario (immutabile). Stato funnel non toccato. Idempotente.
Ritorna `id` del canonico, o `None` in degrado.

**Dispatcher `gas.py` (righe 1383-1387)**:

```python
# unisci_contatti NON è più un tool autopilot: il merge di lead è
# mutante e irreversibile (lossy), quindi è MANUTENZIONE UMANA e non
# passa più di qui (vedi _unisci_contatti). Il meccanismo di merge
# in MemoryStore resta intatto. Tool ignoto → diniego pulito.
return "Tool non trovato."
```

`unisci_contatti` **non è esposto come tool nel loop**: il branch nel dispatcher non esiste.
Il wrapper `_unisci_contatti` (gas.py:1254) esiste ma è helper per uso manuale futuro.
Il modello non può invocare merge da sé — in linea col DIVIETO dello scope.

---

## Sintesi e implicazioni per lo scope

| Punto | Stato attuale |
|---|---|
| Chiave di identità | `chiave_norm = normalizza_chiave(chiave)` — lessicale, no semantica |
| Collisione stessa email | Solo se email usata come `chiave` in entrambi i salvataggi |
| Duplicati cross-formato | Esistono: stesso lead, `chiave` diversa (nome vs email vs tel) |
| Normalizzazione telefono | Assente — `contatto` è TEXT libero |
| `unisci_contatti` | Implementato in store.py (merge a lapide), NON autopilot |
| Fusione umana | Confermata: `_unisci_contatti` è helper manuale, non tool LLM |

**Lo scope R-crm-1b è valido.** I duplicati cross-formato esistono. Il rilevatore deve:
- confrontare il campo `contatto` tra record diversi (match email-email o tel-tel)
- eventualmente somiglianza di `nome` (con soglia alta per evitare falsi-merge)
- NON fondere mai: solo segnalare i candidati all'operatore.

---

*Sonda completata. Attendo via dell'operatore per le fette successive.*
