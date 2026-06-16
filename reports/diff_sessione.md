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

### 3. DOC
- **`CLAUDE.md`**: §10 FASE 2 voce "Backup della memoria"; §6 nota su pin always-on + tool
  `ricorda` + fail-safe.
- **`reports/stato_progetto.md`**: voci "fetta 2a ATTIVA" e "fetta 2b ATTIVA", decisioni di
  design A/B, riserve R1/R2 (2a) e R1/R2/R3 (2b), conteggi review (#13, #14) e suite (98).

### Processo rispettato
- Gate di review: subagent **revisore** invocato sul diff staged PRIMA di OGNI commit
  motore → **#13 (fetta 2a)** e **#14 (fetta 2b)** entrambi **APPROVATO CON RISERVE**.
  Riserve tracciate in `stato_progetto.md`. Hook deterministico onorato (marcatore
  `.claude/.review_ok` creato per ogni commit motore, rimosso subito dopo).

## File toccati (sintesi)
`gas.py` (+197 nelle due fette) · `tests/test_unit_kernel.py` (+T20a-e, +T21a-h) ·
`CLAUDE.md` (§10 backup, §6 memoria) · `.claude/agents/memoria_revisore.md` (lezioni #13/#14) ·
`reports/ultimo_report.md` · `reports/stato_progetto.md` · `reports/diff_sessione.md` (questo).
Commit motore: `7a75368` (2a) · `f3c5f30` (2b).
