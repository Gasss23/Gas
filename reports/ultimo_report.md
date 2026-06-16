# 📄 REPORT — Memoria FASE 2: scrittura CONTATTI dal loop (CRM autopilot) + chiusura riserve 2b

**Data:** 2026-06-16 · **Commit motore:** `a70cbb1` · **Suite:** 106/106, 0 FAIL (era 98)
**Review:** #15 — **APPROVATO CON RISERVE** (R-crm-1, R-crm-2 tracciate in `stato_progetto.md`)

> Sessione autonoma su mandato esplicito dell'utente ("prossimi passi: fai pure tutto in
> autonomia, senza checkpoint"). Tutto committato e pushato. Recap per il revisore in fondo.

---

## Esito in breve

**Il ciclo della memoria di GAS è ora COMPLETO.** Prima GAS sapeva: scrivere il diario
(2a), leggere/iniettare la memoria (2b), e *leggere* i contatti. Ma la **rubrica lead** si
poteva popolare solo a mano. Ora GAS la **costruisce da solo durante il lavoro**, per via
controllata: due nuovi tool (`salva_contatto`, `imposta_stato_contatto`) che scrivono nel
DB via SQL parametrizzato (il modello non scrive mai SQL grezzo).

In più ho **chiuso le tre riserve** lasciate aperte dalla review #14 (R1 match contatto
ambiguo, R2 costanti hardcoded, R3 euristica filtro rumore).

---

## Cosa è stato costruito

### A. Scrittura contatti dal loop (CRM autopilot)
- **`modules/memory/store.py`**: aggiunto il SOLO metodo di lettura
  `get_contatto_per_chiave(chiave)` (lookup esatto sull'indice UNIQUE). Schema, trigger,
  diario, `upsert_contatto`, `update_stato_contatto`, `lista_contatti` della fetta 1
  **INVARIATI** (il revisore ha verificato che il lato `-` del diff è vuoto).
- **`gas.py`** — due tool in `tools_schema` + rami in `execute_tool_call`:
  - **`salva_contatto(chiave, nome?, contatto?, prossima_azione?, note?)`** →
    `_salva_contatto` → `MemoryStore.upsert_contatto`. Aggiorna l'anagrafica; **NON** tocca
    lo stato del funnel (separazione identità ↔ ciclo di vita, come upsert).
  - **`imposta_stato_contatto(chiave, stato, prossima_azione?)`** → `_imposta_stato_contatto`
    → match **ESATTO** sulla chiave (una transizione non può essere ambigua) + valida lo
    stato contro `STATI_CONTATTO` **prima** di toccare il DB. Lead inesistente / stato
    invalido → messaggio di diniego, mai crash.
  - Scrittura **IN-PROCESS** (codice fidato → niente filesystem/rete, quindi niente sandbox
    e niente snapshot). Ogni tool call è comunque **tracciata nel diario** dal loop (fetta
    2a); `_riassumi_args` ha ora casi dedicati per salva/imposta/ricorda.
  - **Fail-safe §9** ovunque: memoria None/degradata → messaggi, mai crash.

### B. Chiusura riserve 2b (review #14)
- **R1** (match contatto ambiguo): nuovo `_trova_contatto(termine)` → **priorità al match
  esatto** sulla chiave; se il fallback substring trova PIÙ lead, prende il più recente ma
  **restituisce una nota di ambiguità** invece di scegliere in silenzio. Usato da `ricorda`.
- **R2** (costanti hardcoded): helper `_env_int(name, default, min_val)` fail-safe + override
  via env **`GAS_MEMORY_PIN_CHARS/CONTACTS/EVENTS`** (attributi d'istanza che shadowano i
  default di classe). Valore sporco → default; sotto il minimo → clamp.
- **R3** (euristica `*5`): sostituita con **`MEMORY_PIN_SCAN=200`** (finestra ampia e
  bounded): anche con rumore di lettura denso, le azioni vere poco più indietro emergono.

---

## VERIFICHE (eseguite dal vivo, output integrale)

### A. Suite completa — 106 PASS, 0 FAIL (era 98 → +8 T22)

```
[PASS] T22a salva_contatto crea+aggiorna senza duplicare — o1=Successo: contatto 'anna@ex.com' salvato c=Anna
[PASS] T22b salva_contatto: chiave mancante negata, memoria None gestita
[PASS] T22c imposta_stato: ok + inesistente/stato-invalido negati
[PASS] T22d get_contatto_per_chiave: esatto + None
[PASS] T22e (R1) match esatto prioritario + ambiguità segnalata — nota_amb=⚠ 2 lead corrispondono a 'mario' (Mario Bianchi, Mario Rossi…); mostro il più recente. Usa la chiave esatta per disambiguare.
[PASS] T22f (R2) override env dei tetti memoria + fail-safe valore sporco — chars=5000 events=6
[PASS] T22g (R3) azione vera emerge sotto 40 eventi di rumore (scan ampio) — scan=200
[PASS] T22h round-trip: rubrica popolata dal loop + diario + pin riflette — stato=interessato diario=['imposta_stato_contatto', 'salva_contatto']

=== RIEPILOGO: 106 PASS, 0 FAIL ===
```

### B. Compile check
`python -m py_compile gas.py modules/memory/store.py` → **OK**.

### C. Prova-di-scope (commit motore `a70cbb1`)

```
 gas.py                    | 133 +++++++++++++++++++++++++++++++++++++++++-----
 modules/memory/store.py   |  14 +++++
 tests/test_unit_kernel.py |  94 ++++++++++++++++++++++++++++++++
 3 files changed, 228 insertions(+), 13 deletions(-)
```

- **NESSUNA** ridefinizione di `_get_window`, `_cap_window_chars`, `_msg_chars`,
  `_bwrap_prefix`, `_snapshot`, `_vet_command`, `providers`, `payload = [...]`,
  `for _ in range(10)`.
- `store.py`: **solo aggiunta** di `get_contatto_per_chiave` — NESSUNA modifica a
  schema/trigger/diario/upsert/update (verificato anche dal revisore: lato `-` vuoto).

### D. Prova dal vivo (round-trip reale: l'agente popola la rubrica DA SOLO)

`run_turn` in cui il modello finto chiama `salva_contatto` + `imposta_stato_contatto`:

```
ESITI TOOL: ["Successo: contatto 'giulia@studio.it' salvato (id=1).",
             "Successo: lead 'giulia@studio.it' ora in stato 'interessato'."]
RUBRICA: {'nome': 'Giulia', 'stato': 'interessato', 'prossima_azione': 'mandare preventivo'}
DIARIO: [('imposta_stato_contatto', "chiave='giulia@studio.it' stato='interessato' | [OK] Su"),
         ('salva_contatto',        "contatto chiave='giulia@studio.it' | [OK] Successo: con")]

PIN che GAS vedrà al PROSSIMO turno:
# MEMORIA (sola lettura — usa il tool 'ricorda' per approfondire il diario o un lead)
## Lead attivi
- Giulia [interessato] → prossima: mandare preventivo (ultimo: 2026-06-16)
## Ultime azioni
- [imposta_stato_contatto] chiave='giulia@studio.it' stato='interessato' | [OK] Successo...
- [salva_contatto] contatto chiave='giulia@studio.it' | [OK] Successo: contatto...
```

Il lead è salvato e portato a "interessato", l'azione è nel diario, e il pin lo mostra al
turno successivo. Ciclo completo: scrivi → ricorda → agisci.

---

## Riserve (review #15, minori, non bloccanti — in `stato_progetto.md`)
- **R-crm-1**: qualità del dato della rubrica — il modello può registrare lo stesso lead con
  chiavi incoerenti (`anna@ex.com` vs `Anna`) come contatti distinti; l'UNIQUE deduplica
  solo a parità di chiave esatta. È rischio di QUALITÀ, non di sicurezza (recuperabile, mai
  crash). Difesa candidata: normalizzare la chiave (lower/trim) prima dell'upsert o un tool
  di merge lead. Non urgente.
- **R-crm-2**: `int(c["id"])` in `_imposta_stato_contatto` assume id convertibile (sempre
  vero con PK INTEGER SQLite, comunque protetto dal try/except globale). Cosmetico.

---

## Stato complessivo della Memoria (FASE 2)
| Pezzo | Stato | Commit |
|---|---|---|
| Fetta 1 — fondamenta storage (DB, diario immutabile, rubrica) | ATTIVA | `8de2b0c` |
| Fetta 2a — aggancio diario a run_turn (scrittura) | ATTIVA | `7a75368` |
| Fetta 2b — lettura/iniezione (pin always-on + tool `ricorda`) | ATTIVA | `f3c5f30` |
| CRM autopilot — scrittura contatti dal loop + chiusura R1/R2/R3 | ATTIVA | `a70cbb1` |

**Suite 106/106, 0 FAIL.** Tutte le review APPROVATE CON RISERVE (riserve tracciate, nessuna
bloccante).

## Prossimi passi possibili (NON fatti — da decidere)
1. **Normalizzazione chiave lead** (chiude R-crm-1): lower/trim della chiave prima
   dell'upsert, o un tool `unisci_contatti` per deduplicare lead doppi.
2. **Retention del diario** (nota PARK): il diario cresce per sempre; quando il volume lo
   richiederà, archiviazione/export + rotazione del file storico, MAI `DELETE` (immutabilità).
3. **Vector DB** (FASE 2 roadmap): ricordi a lungo termine semantici (richiede design su
   dipendenze/costi prima di toccare il motore — è il passo grosso, da pianificare).
4. **Backup OFF-MACHINE** del DB memoria (FASE 5/VPS): oggi `backup()` è solo locale.

---

## 📌 RECAP per il revisore (Claude web) — leggi qui se hai poco tempo
- **Cosa ho fatto in questa sessione**: (1) chiuso DOC + costruito la **fetta 2a** (il
  kernel scrive nel diario una riga per ogni tool call, fail-safe); (2) costruito la **fetta
  2b** (pin di memoria always-on nel system message + tool `ricorda` di sola lettura, SENZA
  toccare la finestra blindata); (3) su mandato autonomo, aggiunto il **CRM autopilot** (tool
  `salva_contatto`/`imposta_stato_contatto`) e **chiuso le 3 riserve** della 2b.
- **Dove guardare**: motore in `gas.py` (cerca `_memoria_pin`, `_ricorda`, `_trova_contatto`,
  `_salva_contatto`, `_imposta_stato_contatto`, `_diario_log`); storage in
  `modules/memory/store.py`; test `T19`–`T22` in `tests/test_unit_kernel.py`.
- **Garanzie chiave**: la finestra conversazionale (`_get_window`/`_cap_window_chars`) e il
  loop a 10 iterazioni sono **INVARIATI**; l'unica modifica alla finestra è
  `system_prompt → system_prompt + mem_pin`. Tutta la memoria è **fail-safe**: se il DB
  manca/è corrotto, GAS lavora lo stesso. Scrittura memoria = **in-process**, codice fidato,
  bypassa correttamente il sandbox bwrap (che protegge solo `run_command`).
- **Commit di questa sessione**: `7a75368` (2a), `f3c5f30` (2b), `a70cbb1` (CRM+riserve), più
  i commit doc. Suite **106/106**. 4 review revisore, tutte APPROVATE CON RISERVE.
- **Non c'è nulla in sospeso che blocchi**: le riserve aperte (R-crm-1 qualità chiavi,
  retention diario, ecc.) sono migliorie future, non bug. Vedi "Prossimi passi possibili".
