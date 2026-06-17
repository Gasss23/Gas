Tutto raccolto. Ecco l'esito completo, punto per punto.

---

## 1. `reports/ultimo_report.md` (canonico, integrale)

Stampato sopra per intero. Intestazione: **"Memoria FASE 2: scrittura CONTATTI dal loop (CRM autopilot) + chiusura riserve 2b"** — Data 2026-06-16, commit motore `a70cbb1`, suite **106/106 0 FAIL** (era 98), review **#15 APPROVATO CON RISERVE**.

## 2. `git log --oneline -8` + `git show --stat`

Log (dal più recente):
```
2add5e9 chore(scrivi-rep): ultima risposta salvata
937bcac docs(memory): report CRM autopilot ...
a70cbb1 feat(memory): scrittura CONTATTI dal loop (CRM autopilot) ...
bea0670 docs(memory): report FASE 2 fetta 2b ...
f3c5f30 feat(memory): FASE 2 fetta 2b — lettura/iniezione memoria ...
7cacde3 docs(memory): report FASE 2 fetta 2a ...
7a75368 feat(memory): FASE 2 fetta 2a — aggancio diario a run_turn ...
9d96f0d chore(scrivi-rep): ultima risposta salvata
```

Stat dei tre commit:

| Commit | File toccati | Δ |
|---|---|---|
| **7a75368** (2a) | `gas.py`, `tests/test_unit_kernel.py` | +167, −0 |
| **f3c5f30** (2b) | `gas.py`, `tests/test_unit_kernel.py` | +261, −3 |
| **a70cbb1** (CRM) | `gas.py`, `modules/memory/store.py`, `tests/test_unit_kernel.py` | +228, −13 |

## 3. Conferma secca — invarianti del motore

Verificato **sui diff reali** (`git show ... | grep '^[-+]'`), non sui messaggi di commit.

**`f3c5f30` (2b): essenzialmente NO**, con **UNA sola eccezione documentata e attesa** su `_get_window`.
- `_get_window` → **toccato in 1 riga sola**, e solo per appendere il pin al system:
  ```
  - payload = [{"role": "system", "content": self.system_prompt}] + self._get_window()
  + payload = [{"role": "system", "content": self.system_prompt + mem_pin}] + self._get_window()
  ```
  La chiamata `self._get_window()` è **identica**; cambia solo il `content` del messaggio system. Le altre occorrenze di `_get_window`/`_cap_window_chars` nel diff sono **commenti** (righe 58, 79, 198).
- `_cap_window_chars` → **NO** (solo commenti).
- `for _ in range(10)` → **NO** (nessuna riga +/−).
- sandbox / `_bwrap_prefix` / `_snapshot` / snapshot → **NO** (unica occorrenza è un commento: *"dal sandbox di run_command. Nessuno snapshot (non muta nulla)"*).

**`a70cbb1` (CRM): NO su tutto.**
- `_get_window` → **NO** · `_cap_window_chars` → **NO** · `for _ in range(10)` → **NO** · `_bwrap_prefix`/`_snapshot` → **NO**.
- sandbox/snapshot → **NO**: unica occorrenza è un commento (*"...rete, niente sandbox/snapshot. La riga viene comunque tracciata..."*). Nessuna riga di codice modificata.

➡️ **In sintesi:** l'unica modifica funzionale agli invarianti è quella riga del payload in 2b (`system_prompt + mem_pin`). Il loop a 10 iterazioni, il cap della finestra, sandbox e snapshot sono **intatti** in entrambi i commit.

## 4. Verdetto integrale del revisore

### Fetta 2b — Review #14 → **APPROVATO CON RISERVE**
Riserve aperte (poi chiuse in #15):
- **R1** — match contatto via substring case-insensitive con `next(...)` prende il PRIMO → query corte/comuni possono colpire il lead sbagliato senza avviso di match multipli (UX di lettura, non sicurezza).
- **R2** — costanti hardcoded (cap del pin).
- **R3** — euristica filtro rumore (`MEMORY_PIN_EVENTS*5`).

Lezione registrata (memoria revisore, 2026-06-16): *"Iniezione di memoria always-on nel SYSTEM message (`system_prompt + pin`) è il vettore CORRETTO per non destabilizzare la finestra: il pin sta FUORI da `_get_window`/`_cap_window_chars`, la finestra parte sempre da role:user → nessun rischio Gemini 400. Pretendere: (a) cap dedicato che tronca il TESTO con marker — MAI slicing (§5); (b) pin calcolato UNA volta prima del loop, non dentro `for _ in range(10)`; (c) test che cattura il payload reale e asserisce 1 solo system + finestra che parte da user. Verificato che l'UNICA riga toccata della finestra sia il content del system."*

### CRM autopilot — Review #15 → **APPROVATO CON RISERVE**
Chiude R1/R2/R3 della 2b e lascia due riserve minori, **non bloccanti**:
- **R-crm-1** — *qualità del dato della rubrica*: il modello può registrare lo stesso lead con chiavi incoerenti (`anna@ex.com` vs `Anna`) come contatti distinti; l'UNIQUE deduplica solo a parità di chiave esatta. Nessuna normalizzazione lato kernel. Rischio di **QUALITÀ, non di sicurezza** (recuperabile, mai crash). Difesa candidata: normalizzare la chiave (lower/trim) prima dell'upsert, o un tool di merge lead.
- **R-crm-2** — `int(c["id"])` in `_imposta_stato_contatto` assume id convertibile (sempre vero con PK INTEGER SQLite, protetto dal try/except globale) — **cosmetico**.

Lezione registrata (2026-06-16): *"Tool di SCRITTURA della memoria: asimmetria di risoluzione del contatto CORRETTA — la scrittura/transizione mutante usa SOLO match ESATTO sulla chiave (UNIQUE), perché spostare il lead sbagliato in silenzio è un effetto collaterale; la sola LETTURA può tollerare il substring con nota di ambiguità (mai scelta muta). Verificare separazione identità/ciclo-di-vita: `salva_contatto`→`upsert_contatto` NON passa mai `stato`, la transizione passa SOLO da `update_stato_contatto`; e che si validi lo stato contro STATI_CONTATTO PRIMA di toccare il DB (diniego, non ValueError). Rischio residuo = QUALITÀ del dato, non sicurezza."*

---

### 📌 Recap (semplice)
- **Punto 1**: il report canonico l'ho stampato per intero — parla del completamento della memoria (GAS ora riempie la rubrica lead da solo durante il lavoro), 106 test passati.
- **Punto 2**: i tre commit toccano solo `gas.py`, lo storage della memoria e i test — niente di sparso altrove.
- **Punto 3 (la domanda chiave)**: i pezzi delicati del motore (finestra, loop a 10 giri, sandbox, macchina del tempo) **non sono stati toccati**. L'unica vera modifica è **una riga** in 2b che aggiunge il "promemoria" al messaggio di sistema — tutto il resto identico. Il CRM non tocca nessuno di questi.
- **Punto 4**: entrambe le revisioni sono **APPROVATE CON RISERVE**, e le riserve sono migliorie di qualità (es. evitare lead doppi scritti con nomi diversi), **non bug né rischi di sicurezza**.

Tutto in sola lettura: nessuna modifica e nessun commit, come richiesto.
