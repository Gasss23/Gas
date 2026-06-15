# 🗄️ FINDING ARCHIVIATI (chiusi)

> Cimitero dei finding già CHIUSI/RISOLTI/RIDOTTI, compressi a una riga datata.
> Nessuna informazione distrutta: il dettaglio integrale resta nella history git
> (commit citati) e nei report di sessione. I finding APERTI (🟡/🟠/🔴) restano
> invece in `reports/stato_progetto.md`.
> Creato il 2026-06-15 (TASK 2 — sfoltimento `stato_progetto.md`).

- **2026-06-11** — T10 path traversal su `write_file`/`read_file` BLOCCATO via `_safe_path` (`.resolve()` + `is_relative_to`). CHIUSO. (review #2)
- **2026-06-11** — Snapshot preventivo dei file: `_snapshot` via indice git temporaneo + ref `refs/gas/snapshots/*`, fail-closed. CHIUSO. (review #3, R1 in #3-bis)
- **2026-06-12** — Sandbox/dry-run per `run_command` (shlex no-shell + allowlist read-only + env sanificata): finding esfiltrazione RIDOTTO 🟠→🟡 (chiusura piena rinviata al sandbox OS). (review #4)
- **2026-06-14** — Snapshot sprecato in os_strict quando il sandbox manca (R1 #6): check sandbox OS anticipato PRIMA dello snapshot nel ramo `run_command`. RISOLTO. (review #7)
- **2026-06-14** — Manca test permanente per `_cap_window_chars` (R1 #7): aggiunto blocco T14 (9 check), mordacità verificata per mutazione. RISOLTO. (review #8)
- **2026-06-14** — Nessun cap rigido sulla finestra (review #1): `WINDOW_CHAR_CAP = 24000` a granularità di messaggio (`_cap_window_chars`), mai slicing. CHIUSO. (review #7)
- **2026-06-14** — Modello free hardcoded e volatile (R1 #5): `gas doctor` verifica esistenza (404→WARN) e capacità tool del modello free via GET di metadati. CHIUSO. (TASK B, review #9)
- **2026-06-14** — Duplicazione costanti provider (R3 #5): URL/slug provider estratti in costanti di modulo, punto unico per `run_turn`/`doctor`, cascata bit-identica. CHIUSO. (TASK A)
- **2026-06-14** — Duplicazione del parse di `GAS_SANDBOX_MODE` in doctor (R3 #6): estratto helper `_parse_mode`, init e doctor risolvono lo STESSO mode (T16c). CHIUSO. (TASK A)
- **2026-06-14** — Retention snapshot count-based (R2): passata a IBRIDA = UNIONE di (ultimi `SNAPSHOT_KEEP=100`) e (più giovani di `SNAPSHOT_KEEP_DAYS=7`), certificata dai T18. CHIUSO. (TASK C, review #10)
- **2026-06-14** — Manutenzione snapshot residua (R3): `doctor` sez.7 REPORTA ref/loose/log (gc resta opt-in manuale) + `snapshots.log` gitignorato e ruotato `.1`. CHIUSO/MITIGATO. (TASK C)
- **2026-06-15** — Rumore log + amplificazione sovrascrittura via hook SessionEnd: hook reso additivo+condizionale (script testabile, niente commit vuoti, motore mai committato) + regola "commit esplicito dei report" dell'agente; bug sovrascrittura (7005517→412714f) chiuso, verifica reale 8/8. CHIUSO. (TASK 1, revisore APPROVATO)
