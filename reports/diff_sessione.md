# 🔀 DIFF DI SESSIONE — 2026-06-16 (Memoria FASE 2 fette 2a + 2b)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni
> sessione.

## Cosa è cambiato e perché

### 1. Fetta 2a — aggancio diario a run_turn, SOLO scrittura (commit `7a75368`)
- **`gas.py`** (+65): import memoria; `self.memory = MemoryStore(...)` in `__init__` con
  doppia cintura fail-safe; helper `_riassumi_args`/`_esito_sintetico`/`_diario_log`; nel
  loop di `run_turn`, per OGNI tool call DOPO l'esecuzione, una riga di diario in-process
  (esito negativo incluso).
- **`tests/`** (+T20a-e): round-trip REALE zero token.
- **Perché**: dare a GAS un diario che ricorda DA SOLO ogni azione, senza toccare la
  blindatura del loop. La memoria che non scrive non ferma mai il turno.

### 2. Fetta 2b — lettura/iniezione memoria (commit `f3c5f30`)
- **`gas.py`** (+132, −3):
  - `_memoria_pin()`: blocco compatto ALWAYS-ON (lead ATTIVI non chiusi + poche azioni
    "significative", escluso il rumore di lettura `read_file`/`run_command`/`ricorda`),
    appeso AL MESSAGGIO SYSTEM in `run_turn` (`self.system_prompt + mem_pin`), calcolato
    UNA volta per turno. Vive nel system message, FUORI dalla finestra → `_get_window`/
    `_cap_window_chars` INVARIATI (unica modifica alla finestra: la riga del payload). Cap
    dedicato `MEMORY_PIN_CHAR_CAP=3000` che tronca il TESTO con marker (no slicing, §5).
  - Tool **`ricorda()`** di SOLA LETTURA in `tools_schema` + ramo in `execute_tool_call`:
    pesca diario/contatti on-demand in-process (codice fidato → niente FS/rete, niente
    sandbox, niente snapshot); output capato da `_cap_tool_output`.
  - Fail-safe §9: memoria None/degradata → pin "" e turno prosegue; `_ricorda` gentile.
- **`tests/`** (+T21a-h): pin filtra attivi/rumore, pin vuoto, `ricorda` per
  contatto/query/default, **T21f cattura il payload reale** (1 solo system, finestra che
  parte da user → no Gemini 400), fail-safe, cap del pin.
- **Perché**: far sì che GAS *usi* la memoria — vede sempre i lead attivi e le ultime
  azioni (pin), e può approfondire on-demand col tool `ricorda`. Senza toccare la finestra
  blindata: il pin sta nel system message, non nella conversazione.

### 3. CRM autopilot — scrittura contatti dal loop + chiusura riserve 2b (commit `a70cbb1`)
- **`modules/memory/store.py`** (+14): aggiunto il SOLO lookup `get_contatto_per_chiave`
  (esatto su indice UNIQUE); schema/trigger/diario/upsert/update della fetta 1 invariati.
- **`gas.py`** (+133, −13): tool `salva_contatto` (upsert anagrafica, non tocca lo stato) e
  `imposta_stato_contatto` (transizione, match esatto + validazione stato) + handler
  `_salva_contatto`/`_imposta_stato_contatto`; `_trova_contatto` (R1: match esatto + nota
  ambiguità); helper `_env_int` + override env `GAS_MEMORY_PIN_*` (R2); `MEMORY_PIN_SCAN=200`
  (R3); `_riassumi_args` con casi dedicati.
- **`tests/`** (+T22a-h): salva/aggiorna, dinieghi, lookup, R1/R2/R3, round-trip CRM completo.
- **Perché**: completare il ciclo della memoria — GAS popola la rubrica lead DA SOLO durante
  il lavoro, per via controllata (no SQL grezzo dal modello). Suite 98 → 106.

### 4. DOC
- **`CLAUDE.md`**: §10 FASE 2 voce "Backup della memoria"; §6 nota su pin always-on + tool
  `ricorda` + tool di scrittura contatti + override env + fail-safe.
- **`reports/stato_progetto.md`**: voci "fetta 2a ATTIVA", "fetta 2b ATTIVA", "CRM autopilot
  ATTIVA + R1/R2/R3 chiuse"; decisioni di design A/B; riserve R1/R2 (2a), R-crm (CRM);
  conteggi review (#13, #14, #15) e suite (106).

### Processo rispettato
- Gate di review: subagent **revisore** invocato sul diff staged PRIMA di OGNI commit
  motore → **#13 (fetta 2a)**, **#14 (fetta 2b)** e **#15 (CRM + riserve)** tutti
  **APPROVATO CON RISERVE**. Riserve tracciate in `stato_progetto.md`. Hook deterministico
  onorato (marcatore `.claude/.review_ok` creato per ogni commit motore, rimosso subito dopo).

## File toccati (sintesi)
`gas.py` (+~330 nella sessione) · `modules/memory/store.py` (+lookup) ·
`tests/test_unit_kernel.py` (+T20a-e, +T21a-h, +T22a-h) · `CLAUDE.md` (§10 backup, §6 memoria) ·
`.claude/agents/memoria_revisore.md` (lezioni #13/#14/#15) · `reports/ultimo_report.md` ·
`reports/stato_progetto.md` · `reports/diff_sessione.md` (questo).
Commit motore: `7a75368` (2a) · `f3c5f30` (2b) · `a70cbb1` (CRM + riserve).
