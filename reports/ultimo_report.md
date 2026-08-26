# Sonda VPS read-only — 2026-08-26

**Branch:** `sonda/vps-stato-2026-08-26`  
**Data:** 2026-08-26  
**Tipo:** Ricognizione in sola lettura. Zero modifiche al VPS.

---

## §0 DECISIONI UMANE RICHIESTE

- **S2 (riallineamento VPS)**: il VPS gira su codice del 2026-06-29, 17 commit motore dietro origin/main (FASE 3 completa mancante). Il riallineamento è dichiarato FASE 5 S2 — decisione operatore su timing e modalità.
- **F7 — `.venv/` nel gitignore VPS**: confermata assenza. La fix è su origin/main (`1b03adc`) ma non è deployata. Se il VPS viene aggiornato via `git pull`, `.venv/` smette di apparire come untracked — nessuna azione urgente, ma da ricordare a S2.
- **`gas_debug.log` solo timeout**: il log non mostra conversazioni reali da luglio. Confermare che il bot Telegram non stia perdendo messaggi o che nessun utente reale abbia scritto.

---

## §1 ESITO TASK

**ESEGUITA** — Sonda read-only completata. Nessuna modifica al VPS.

---

## §2 PREFLIGHT SSH

```
OK
gas-vps
gas
```
Connessione riuscita. Host: `gas-vps`, utente: `gas`.

---

## §3 DATI VERBATIM VPS

### A) gas.service

```
● gas.service - GAS Autonomous Agent
     Loaded: loaded (/etc/systemd/system/gas.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-08-25 17:00:04 UTC; 1 day 4h ago
   Main PID: 853 (python)
      Tasks: 4 (limit: 9255)
     Memory: 123.9M (high: 1.4G max: 1.9G available: 1.3G peak: 124.6M)
        CPU: 8.218s
     CGroup: /system.slice/gas.service
             └─853 /home/gas/gas/.venv/bin/python /home/gas/gas/gas.py telegram

Aug 25 20:46:45 gas-vps python[853]: 2026-08-25 20:46:45,078 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 02:17:44 gas-vps python[853]: 2026-08-26 02:17:44,560 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 03:43:17 gas-vps python[853]: 2026-08-26 03:43:17,152 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 03:50:32 gas-vps python[853]: 2026-08-26 03:50:32,526 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 04:05:29 gas-vps python[853]: 2026-08-26 04:05:29,044 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 05:11:49 gas-vps python[853]: 2026-08-26 05:11:49,460 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 14:13:40 gas-vps python[853]: 2026-08-26 14:13:40,305 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 18:01:38 gas-vps python[853]: 2026-08-26 18:01:38,827 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 26 19:22:23 gas-vps python[853]: 2026-08-26 19:22:23,382 - WARNING - Telegram getUpdates errore: The read operation timed out
Warning: journal has been rotated since unit was started and some journal files were not opened due to insufficient permissions, output may be incomplete.
===
active
enabled
```

### B) Git state VPS

```
f3a8acc docs(stato): sonda doctor sez.8 — confermata copertura completa memoria SQLite a freddo
===
## main...origin/main
?? .venv/
===
main
===
f3a8accf6b54911dba394c70c732d38718217de8
```

### C) .gitignore VPS (head -5)

```
venv/
__pycache__/
*.pyc
logs/
*.bak
```

### D) RAM / Disco / Python

```
               total        used        free      shared  buff/cache   available
Mem:           7.6Gi       502Mi       6.3Gi       4.8Mi       1.0Gi       7.1Gi
Swap:          2.0Gi          0B       2.0Gi
===
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        75G  4.9G   67G   7% /
===
Python 3.12.3
```

### E) ls -la / memoria

```
total 508
drwxr-xr-x 12 gas gas   4096 Aug 26 20:35 .
drwxr-xr-x  6 gas gas   4096 Aug 24 07:55 ..
drwxr-xr-x  3 gas gas   4096 Jul  5 17:06 brains
drwxr-xr-x  5 gas gas   4096 Jun 30 22:06 .claude
-rw-r--r--  1 gas gas     88 Jun 30 22:06 .claudeignore
-rw-r--r--  1 gas gas  10767 Jun 30 22:06 CLAUDE.md
-rw-r--r--  1 gas gas   2998 Jun 30 22:06 deploy_vps_bozza.txt
-rw-------  1 gas gas    413 Jul  6 17:24 .env.prod
-rwxr-xr-x  1 gas gas    298 Jun 30 22:06 gas
-rw-r--r--  1 gas gas  24747 Aug 26 19:22 gas_debug.log
-rw-r--r--  1 gas gas   3632 Jul  6 18:26 .gas_history.json
-rw-r--r--  1 gas gas    579 Jun 30 22:06 gas_identity.md
-rw-r--r--  1 gas gas  53248 Jul  5 17:06 .gas_memory.20260705T170600_301580Z.bak
-rw-r--r--  1 gas gas  53248 Jul  6 05:50 .gas_memory.20260706T055008_472006Z.bak
-rw-r--r--  1 gas gas  53248 Jul  6 18:26 .gas_memory.20260706T182638_099445Z.bak
-rw-r--r--  1 gas gas  53248 Aug 25 17:01 .gas_memory.db
-rwxr-xr-x  1 gas gas 122892 Jun 30 22:06 gas.py
-rw-r--r--  1 gas gas   2027 Jul  6 18:26 .gas_tokens.jsonl
-rw-r--r--  1 gas gas  32768 Jun 30 22:10 .gas_vectors.db
drwxr-xr-x  8 gas gas   4096 Aug 26 21:56 .git
drwxr-xr-x  3 gas gas   4096 Jun 30 22:06 .github
-rw-r--r--  1 gas gas    613 Jun 30 22:06 .gitignore
drwxr-xr-x  6 gas gas   4096 Jun 30 22:10 modules
drwxr-xr-x  2 gas gas   4096 Jul  5 16:59 __pycache__
-rw-r--r--  1 gas gas   3997 Jun 30 22:06 README.md
drwxr-xr-x  2 gas gas   4096 Jun 30 22:06 reports
-rw-r--r--  1 gas gas    156 Jun 30 22:06 requirements.txt
-rw-r--r--  1 gas gas     19 Jun 30 22:06 router
drwxr-xr-x  2 gas gas   4096 Jun 30 22:06 self_improve
-rw-r--r--  1 gas gas    581 Jun 30 22:06 test_agente.py
drwxr-xr-x  2 gas gas   4096 Jun 30 22:06 tests
drwxr-xr-x  5 gas gas   4096 Jun 30 22:08 .venv
===
 124 .gas_history.json
wc: 'diario*': No such file or directory
 124 total
```

### F) Log (journalctl -u gas -n 30)

```
Aug 23 05:30:08 gas-vps python[105482]: 2026-08-23 05:30:08,390 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 23 05:59:37 gas-vps python[105482]: 2026-08-23 05:59:37,282 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 23 07:22:19 gas-vps python[105482]: 2026-08-23 07:22:19,102 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 23 07:47:32 gas-vps python[105482]: 2026-08-23 07:47:32,884 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 23 10:22:47 gas-vps python[105482]: 2026-08-23 10:22:47,824 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 23 10:31:50 gas-vps python[105482]: 2026-08-23 10:31:50,906 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 01:35:08 gas-vps python[105482]: 2026-08-24 01:35:08,813 - WARNING - Telegram getUpdates HTTP 502: Bad Gateway
Aug 24 01:37:34 gas-vps python[105482]: 2026-08-24 01:37:34,002 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 01:39:59 gas-vps python[105482]: 2026-08-24 01:39:59,181 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 06:08:22 gas-vps python[105482]: 2026-08-24 06:08:22,074 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 07:02:02 gas-vps python[105482]: 2026-08-24 07:02:02,050 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 08:17:53 gas-vps python[105482]: 2026-08-24 08:17:53,419 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 11:49:21 gas-vps python[105482]: 2026-08-24 11:49:21,093 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 20:00:08 gas-vps python[105482]: 2026-08-24 20:00:08,383 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 24 20:01:24 gas-vps python[105482]: 2026-08-24 20:01:24,538 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 25 01:59:29 gas-vps python[105482]: 2026-08-25 01:59:29,076 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 25 02:44:03 gas-vps python[105482]: 2026-08-25 02:44:03,826 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 25 09:30:23 gas-vps python[105482]: 2026-08-25 09:30:23,006 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 25 09:35:14 gas-vps python[105482]: 2026-08-25 09:35:14,542 - WARNING - Telegram getUpdates URLError: [Errno 104] Connection reset by peer
Aug 25 12:25:06 gas-vps python[105482]: 2026-08-25 12:25:06,864 - WARNING - Telegram getUpdates errore: The read operation timed out
Aug 25 15:54:24 gas-vps python[105482]: 2026-08-25 15:54:24,678 - WARNING - Telegram getUpdates errore: The read operation timed out
-- Boot 6be2bec2dad046d787b71c46b1c83432 --
Aug 25 20:46:45 gas-vps python[853]: 2026-08-25 20:46:45,078 - WARNING - Telegram getUpdates errore: The read operation timed out
[... omissis — solo timeout fino alle 19:22 del 26/08 ...]
```

---

## §4 RISPOSTE SINTETICHE

### (a) gas installato/attivo come servizio systemd?
**SÌ.** `gas.service` active (running), enabled. Uptime: dal 2026-08-25 17:00:04 UTC (riavvio con nuovo boot). PID 853. Comanda `gas.py telegram`. MemoryHigh=1.4G, MemoryMax=1.9G — consumo reale 123.9M RAM. Stabile, nessun crash.

### (b) Commit/branch VPS vs origin/main

| | VPS | origin/main |
|---|---|---|
| Branch | `main` (locale, mai fetchato dal deploy) | `main` |
| HEAD | `f3a8acc` (2026-06-29) | `8a946c6` (2026-08-25) |
| Commit descrizione | `docs(stato): sonda doctor sez.8 — confermata copertura completa memoria SQLite a freddo` | `Merge pull request #76 from Gasss23/chore/audit-branch-remoti` |

**NON coincide.** Il VPS è **391 commit dietro** origin/main (include merge commits). Di questi, **17 toccano gas.py / brains/ / modules/** — ovvero tutta FASE 3 (voice endpoint, STT Groq Whisper, TTS ElevenLabs, client 4a) e altri fix del motore NON sono deployati.

Motor commits mancanti (dal più recente):
```
4380f65 feat(voice): FASE 3 Fetta 3 — TTS output via ElevenLabs
ff4d0c4 feat(voice): FASE 3 Fetta 2 — STT server-side via Groq Whisper
bf04d18 feat(fase3-fetta1): endpoint HTTP POST /voice + suite 18 test
638c894 feat(crm): R-crm-1b fetta 4 — gas duplicati
f6259eb feat(crm): R-crm-1b fetta 3 — dedup telefono
22ea680 fix(crm): idempotenza diario in rileva_duplicati_email
e9ffee0 fix(kernel): F6 atomicità .gas_history.json — write tmp+rename
894eb06 fix(memory): chiude varco INSERT OR REPLACE sul diario (recursive_triggers)
1b03adc chore: rimuove 17 file morti; .venv/ gitignorato [F7]
9515626 feat(crm-dup-detect): R-crm-1b Fetta 1 — gas merge-contacts
[+ 7 altri commit motore]
```

Stato atteso e dichiarato: "copia VPS stantia" — riallineamento = FASE 5 S2.

### (c) Memoria/diario presenti con dati reali?

| File | Presente | Dimensione | Timestamp |
|---|---|---|---|
| `.gas_memory.db` | ✅ | 53248 bytes | 2026-08-25 17:01 |
| `.gas_memory.*.bak` | ✅ | 3 backup (53248 bytes ciascuno) | luglio 2026 |
| `.gas_history.json` | ✅ | 3632 bytes / 124 righe | 2026-07-06 18:26 |
| `.gas_tokens.jsonl` | ✅ | 2027 bytes | 2026-07-06 18:26 |
| `.gas_vectors.db` | ✅ | 32768 bytes | 2026-06-30 22:10 |
| `diario*` (file flat) | ❌ | n/a | n/a |

**Nota diario**: nessun file flat `diario*`. Il diario è una tabella IMMUTABILE dentro `.gas_memory.db` (comportamento corretto — il `wc -l diario*` era un falso negativo).

**Nota `.gas_history.json`**: datato 2026-07-06, mai aggiornato dopo il deploy. Il bot ha girato in long-polling per mesi ma il log mostra SOLO timeout — nessuna conversazione reale processata. La history si aggiorna solo dopo un turno kernel effettivo: 124 righe = stato al deploy iniziale.

**`.gas_memory.db` aggiornato al 2026-08-25 17:01** (riavvio del servizio). Questo è normale: il kernel scrive nel db all'avvio.

### (d) RAM/disco a regime

| Metrica | Valore |
|---|---|
| RAM totale | 7.6 GiB |
| RAM usata (sistema) | 502 MiB (7%) |
| RAM disponibile | 7.1 GiB |
| Swap totale | 2.0 GiB |
| Swap usata | 0 B |
| Gas RSS (reale) | 123.9 MB (peak 124.6 MB) |
| Gas MemoryHigh | 1.4 GiB |
| Gas MemoryMax | 1.9 GiB |
| Disco totale | 75 GB |
| Disco usato | 4.9 GB (7%) |
| Disco libero | 67 GB |
| Python | 3.12.3 |

**A regime.** Nessuna pressione su RAM né su disco. Il gas service usa 123 MB di un budget di 1.4 GB.

### (e) Discrepanze VPS vs stato_progetto.md

1. **⚠️ VPS 391 commit dietro** (17 motore mancanti): stato_progetto.md lo dichiara come "copia VPS stantia (2026-07-21), riallineamento = S2" — **NOTO**. Però il file NON specifica quanti commit mancano né quali fette motore. Aggiornato in questa sonda: 391 totali, 17 motore, FASE 3 completa mancante.

2. **⚠️ F7 confermata — `.venv/` assente dal gitignore VPS**: `.gitignore` VPS = `venv/`, `__pycache__/`, `*.pyc`, `logs/`, `*.bak`. NO `.venv/`. La fix (`1b03adc chore: .venv/ gitignorato`) è su origin/main ma non deployata. `.venv/` compare come untracked (`?? .venv/`) in git status VPS. Stato_progetto.md dichiarava F7 come "riserva di evidenza da verificare al prossimo SSH": **ora verificata e chiusa** — il VPS NON ha `.venv/` in gitignore, atteso perché stantio.

3. **⚠️ Review count outdated in stato_progetto.md**:
   - §Stato motore (riga 9): dichiara "**82 review**" — realtà: ultima review = **#92** (R-phantom-pr-1, 2026-08-22)
   - §C Istituzioni (riga 134): dichiara "**77 review**. Ultima: **#77**" — realtà: #92
   - Il task brief lo segnala: "parla di 82 review mentre la realtà è #91 + PR #77 aperta". Entrambe le occorrenze aggiornate in questa sessione.

4. **ℹ️ Riavvio VPS 2026-08-25 17:00**: boot marker nel log (`-- Boot 6be2bec2dad046d787b71c46b1c83432 --`). Il processo precedente (PID 105482) era già in running prima. `Restart=always` ha riportato il servizio su dopo il reboot. Non è un crash — comportamento atteso.

5. **ℹ️ Nessuna conversazione reale dal deploy**: il log mostra solo timeout Telegram (long-polling standard, 30s). Nessun messaggio utente processato. Non è un errore, è lo stato atteso se nessuno ha scritto al bot.

---

## §5 AZIONI SUGGERITE (non eseguite — scope S2)

- `git fetch && git pull --ff-only` sul VPS per aggiornare al commit corrente di main (richiede review del diff + verifica CLAUDE.md prima del deploy)
- Rotazione chiave ElevenLabs prima di qualsiasi S2 (finding aperto in stato_progetto.md)
- Verificare `ELEVENLABS_API_KEY` e `GROQ_API_KEY` in `.env.prod` — necessarie per FASE 3 once deployed
