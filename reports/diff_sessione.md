# 🔀 DIFF DI SESSIONE — 2026-06-16 (Memoria FASE 2 fetta 2a — aggancio scrittura)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché

### 1. DOC (no motore)
- **`CLAUDE.md` §10 FASE 2**: nuova voce **"Backup della memoria"**. Il DB di memoria
  (file SQLite singolo, fuori da git) è il dato più prezioso e meno rimpiazzabile; la
  macchina del tempo snapshot NON lo copre (solo repo git). `MemoryStore.backup()` =
  copia `.bak` LOCALE (protegge da auto-corruzione, NON dalla morte del disco); il
  backup OFF-MACHINE è da FASE 5/deploy VPS, banale perché DB = file singolo.
- **`reports/stato_progetto.md`**: voce **"fetta 2a ATTIVA"** + decisioni di design
  **A** (diario logga OGNI tool call, esito incluso; filtro del rumore è scelta del
  lato LETTURA; contatti NON scritti dal loop) e **B** (iniezione always-on PROPOSTA =
  contatti attivi + pochi eventi recenti filtrati, budget ~3000 char dentro
  `WINDOW_CHAR_CAP`, diario profondo via tool `ricorda()`). Riserve R1/R2 della
  review #13 tracciate. Conteggi review (#13) e suite (90) aggiornati.

### 2. BUILD fetta 2a — motore, SOLO lato scrittura (commit `7a75368`)
- **`gas.py`** (+65, 0 cancellazioni):
  - import `from modules.memory import MemoryStore, default_db_path`.
  - `GasKernel.__init__`: `self.memory = MemoryStore(default_db_path(self.root))` con
    **doppia cintura fail-safe** (`MemoryStore` degrada da sé con `available=False`; un
    errore remoto all'avvio mette `self.memory=None`) → il kernel non crasha MAI.
  - Helper `_riassumi_args` (sintesi argomenti per tool), `_esito_sintetico`
    (`[OK]`/`[KO]` dal prefisso dell'output) e `_diario_log` (fail-safe §9: memoria
    None/degradata → warning nella scatola nera, il turno CONTINUA).
  - Nel loop di `run_turn`, per OGNI tool call, DOPO l'esecuzione (esito negativo
    incluso): una riga di diario in-process via `append_diario`. Scrittura
    **IN-PROCESS** (codice fidato → bypassa correttamente il sandbox bwrap).
- **`tests/test_unit_kernel.py`** (+102): T20a-e (round-trip REALE zero token: multi-tool
  in ordine, esiti `[OK]`, tool fallito → `[KO]` + turno non interrotto, memoria corrotta
  → round-trip OK, memoria None → nessun crash). Suite **85 → 90**, 0 FAIL.
- **Perché**: dare a GAS un diario che ricorda DA SOLO tutto ciò che fa, agganciandolo al
  loop senza toccarne la blindatura. Robustezza > potenza: la memoria che non scrive non
  ferma mai il turno.

### Vincoli rispettati (prova-di-scope)
- `for _ in range(10)` (§8) INVARIATO, ordine delle fasi pure.
- CONTATTI non toccati dal loop (solo diario). Nessuna iniezione nel contesto:
  `_get_window`/`_cap_window_chars`/finestra INVARIATI. Schema memoria fetta 1
  (`store.py`) INVARIATO. **Lato lettura/iniezione (fetta 2b) NON implementato: solo
  PROPOSTO** nel report §FINALE.

### Processo rispettato
- Gate di review: subagent **revisore** invocato sul diff staged PRIMA del commit →
  **review #13 APPROVATO CON RISERVE** (R1 etichetta esito da prefisso testuale, R2
  verbosità diario). Riserve tracciate in `stato_progetto.md`. Hook deterministico
  onorato (marcatore `.claude/.review_ok` creato per il commit, rimosso subito dopo).

## File toccati (sintesi)
`gas.py` (+65) · `tests/test_unit_kernel.py` (+T20a-e) · `CLAUDE.md` (§10 backup memoria) ·
`reports/ultimo_report.md` · `reports/stato_progetto.md` · `reports/diff_sessione.md` (questo).
Commit motore: `7a75368`.
