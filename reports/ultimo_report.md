# Report task — doctor visibility layer memoria SQLite
**Data:** 2026-06-29
**Scope:** Sonda (FASE 1) + verdetto GATE STOP #1

---

## Esito: GATE STOP #1 — già coperto, niente da fare

### Sonda (read-only)

Letta la funzione `doctor()` in `gas.py` righe 1538–1808 e il modulo
`modules/memory/store.py` righe 1–805.

La **Sezione 8** di `doctor` (commento "# 8. Memoria di lungo periodo",
righe 1695–1775) apre già il layer SQLite e ne dichiara lo stato in modo
speculare a `disable_reason` del vector store.

#### Check già presenti

| Ramo di degrado | Variabile | Righe doctor | Esito emesso |
|---|---|---|---|
| DB assente | `mem_path.exists()` == False | 1701–1703 | WARN "assente (verrà creato al primo run)" |
| Init fallita — collisione `chiave_norm` | `mem.collisione_chiave_norm` | 1708–1710 | FAIL + dettaglio collisione |
| Init fallita — corruzione/permessi | `mem.available == False` (else) | 1711–1713 | FAIL "DB non apribile..." |
| DB aperto ma corrotto | `mem.integrity_check()` → `PRAGMA quick_check` | 1715–1717 | OK/FAIL |
| FTS5 assente | `mem.fts_available` | 1718–1720 | OK/WARN |
| Nessun backup locale | `mem.ultimo_backup()` | 1720–1728 | WARN |
| Backup stantio | età backup > 0 h | 1725–1728 | OK con età |

#### Paragone con `disable_reason` (vector store, righe 1758–1775)

Il pattern è identico:
- Vector store: `_vs_probe.available` + `_vs_probe.disable_reason`
- Memoria SQLite: `mem.available` + `mem.collisione_chiave_norm`

Entrambi emettono un singolo FAIL o WARN con motivo esplicito.
La memoria SQLite espone addirittura più granularità (integrity_check, FTS5, backup).

### Rami di degrado — silenzioso o visibile?

Tutti i rami identificati nel brief sono **visibili a freddo** tramite doctor:

- `MemoryStore.__init__` fallisce → `available = False` → doctor FAIL con motivo
- `_memoria_pin()` → ricade su pin vuoto quando `available = False`: il per-turno
  è silenzioso PER DESIGN (finding rimandato, FUORI SCOPE), ma il degrado a freddo
  è visibile via doctor.
- `ricorda`, `salva_contatto`, `imposta_stato_contatto` → degradano su `available = False`
  oppure su eccezioni SQLite/OSError catturate: già coperto dal check `available`.

### Conclusione

Nessun gap. Nessun codice da scrivere.

Il gate di ingresso GATE STOP #1 è soddisfatto: il layer memoria SQLite è già
dichiarato da `doctor` in modo equivalente (e più dettagliato) al `disable_reason`
del vector store.

---

## Finding residuo (FUORI SCOPE — da decidere)

Il degrado **per-turno** (quando il layer si degrada DOPO l'avvio, durante un
turno agentico) resta SILENZIOSO: il fail-safe §9 logga un warning nel
`gas_debug.log` ma non lo propaga al runtime della sessione. Questo finding è
esplicitamente rimandato nel brief ("Degrado a solo-testo per-turno, rimandato
APPOSTA per falsi positivi"). Se in futuro si vuole affrontarlo, il punto di
intervento corretto è in `_memoria_pin()` (aggiunge un token nel contesto quando
`available` diventa False a runtime), non in `doctor`.

---

*Nessun file modificato. Nessun commit necessario.*
