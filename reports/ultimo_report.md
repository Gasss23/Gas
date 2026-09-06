# REPORT — Ricognizione audit F1..F6 (2026-08-29) — verifica stato reale su main

**Data:** 2026-09-07
**Scope:** Sessione READ-ONLY. Nessuna modifica a gas.py, brains/, modules/, tests/. Solo reports/.

---

## DECISIONI UMANE RICHIESTE

1. **F5 CHIUSO implicitamente — gap documentale da sanare**: il finding F5 (doppia auto-presentazione) era già risolto da commit `62af5ee` (2026-08-29). Il commit message recita esplicitamente "self-intro unificata (rimossa da `_GAS_SYSTEM_PROMPT_BASE`, sola in `gas_identity.md`)". I report non lo avevano mai marcato ✅. Questa sessione aggiunge la riga nel §Finding — sanzione puramente documentale. Se l'operatore ritiene la chiusura prematura, reverire la modifica a stato_progetto.md.

2. **F4 MEDIO e F6 MINORE restano aperti**: scope del fix a decisione operatore. F4 = tensione strutturale gas.py:45-47; F6 = echo in SHELL_ALLOWLIST:993 (innocuo).

3. **Merge della PR** (numero da §0 handoff).

---

## Esito fette

- **Fetta 1 — git fetch + checkout main aggiornato**: `FATTA` — main già aggiornato, branch sessione `sonda/audit-f1-f6-verifica-2026-09-07` creato da HEAD `3b80e33`.

- **Fetta 2 — localizzazione definizione F1..F6 nei report**: `FATTA` — definizioni estratte da `reports/stato_progetto.md:289-294`, `reports/handoff.md:77-78`, `reports/ultimo_report.md` sessione precedente.

- **Fetta 3 — verifica F1 sul codice attuale**: `FATTA` — CHIUSO confermato. `gas.py:55-56` ordina `calcola()` per aritmetica; `gas.py:992-993` SHELL_ALLOWLIST senza bc/python/expr/awk. Commit `62af5ee` (F1 fix principale) + branch `fix/chiusura-f1-calcola-2026-09-01` (review #95).

- **Fetta 4 — verifica F2 sul codice attuale**: `FATTA` — CHIUSO confermato. `gas_identity.md` lista 7 tool con ruolo ciascuno. Commit `62af5ee`.

- **Fetta 5 — verifica F3 sul codice attuale**: `FATTA` — CHIUSO confermato. `gas.py:42` "_GAS_SYSTEM_PROMPT_BASE" ora recita "Hai 7 tool nativi: read_file, write_file, run_command, calcola, ricorda, salva_contatto, imposta_stato_contatto." Commit `62af5ee`.

- **Fetta 6 — verifica F4 sul codice attuale**: `FATTA` — APERTO confermato, con sfumatura. Pre-fix mancava un path d'uscita generico; post-62af5ee `gas.py:45-46` aggiunge "DICHIARA esplicitamente" per qualsiasi tool failure. Tuttavia la TENSIONE STRUTTURALE tra `gas.py:45` ("DICHIARA che non puoi") e `gas.py:47` ("gestisci l'errore senza bloccarti") persiste — non è definito cosa fare DOPO la dichiarazione. F4 rimane APERTO.

- **Fetta 7 — verifica F5 sul codice attuale**: `FATTA` — trovato GAP DOCUMENTALE. Commit `62af5ee` aveva rimosso "Sei Gas, un agente AI autonomo e personale che gira su VPS." da `_GAS_SYSTEM_PROMPT_BASE` (evidenza: `git show 62af5ee -- gas.py` + commit message "self-intro unificata"). Codice attuale: `gas.py:183` = identity("Sono Gas...") + "REGOLE TASSATIVE:" senza seconda intro → F5 era già chiuso. Marcato ✅ con nota gap doc in `stato_progetto.md`.

- **Fetta 8 — verifica F6 sul codice attuale**: `FATTA` — APERTO confermato. `gas.py:993`: `"ls", "cat", "head", "tail", "wc", "grep", "echo", "pwd", "date",` — echo presente. Dichiarato innocuo (sandbox blocca redirezioni; nessun fix pianificato).

- **Fetta 9 — tabella evidenza in stato_progetto.md**: `FATTA` — tabella markdown F1..F6 inserita in `reports/stato_progetto.md:289-306` con stato, definizione originale, evidenza file:riga.

---

## Anomalie

- **F5 era già chiuso da agosto**: commit `62af5ee` (2026-08-29 16:26) aveva risolto F5 insieme a F2, F3. Il commit message lo documenta esplicitamente. I report non avevano registrato la chiusura. Questa sessione chiude il gap puramente documentale (zero modifica al motore).
- **Doppia nomenclatura F5/F6**: nel repo esistono due serie di finding con label F5/F6 — quella della roadmap (F5=Telegram single-history, F6=atomicità history, entrambi CHIUSI) e quella dell'audit 2026-08-29 (F5=doppia autopresentazione, F6=echo). Nessuna ambiguità nel codice ma leggendo i report va tenuta presente la distinzione.
