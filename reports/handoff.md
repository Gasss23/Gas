# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — FETTA 1 PR B: nessun binario offerto al modello (PR #185)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #185 (https://github.com/Gasss23/Gas/pull/185). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/185"}`): `gh` nel container non è autenticato. Merge autonomo autorizzato dall'operatore in chat (2026-10-11, condizioni a–e; la prova è la conversazione); tocca `scripts/`, quindi serve il verdetto testuale APPROVATO del bot.
2. Chiavi private/file di credenziali leggibili e cercabili: nomi da segreto o compromesso (V-1 verifica esterna #184, 2° giro).
3. FETTA 4: `claude/roadmap_completa.md` non leggibile, allegato non arrivato.

---

## §1 SCOPE & ESITO FETTE

- **FETTA 1 PR A**: `FATTA` — PR #184 mergiata (`5725131`) in una sessione precedente di oggi.
- **FETTA 1 PR B — nessun binario offerto al modello**: `FATTA` — review #286 APPROVATO CON RISERVE.
- **FETTA 2**: `DEFERITA` — dopo il merge della PR B.
- **FETTA 3**: `DEFERITA`.
- **FETTA 4**: `SALTATA — documento non leggibile`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |  2 ++
 gas.py                              | 31 +++++++++++++++++++++----------
 gas_identity.md                     |  3 +--
 reports/diff_sessione.md            | 15 ++++++++-------
 reports/handoff.md                  |  1 +
 reports/setup_notte.md              | 11 +++++++----
 reports/stato_progetto.md           | 24 +++++++++++++++++-------
 reports/ultimo_report.md            | 25 ++++++++++---------------
 scripts/notte/catalogo_esempio.yaml |  5 ++---
 tests/test_unit_kernel.py           | 46 +++++++++++++++++++++++++++++++++++++++++++++-
 10 files changed (conteggi approssimati per reports/handoff.md)
```

Nota: i conteggi di righe di `reports/handoff.md` sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
aec9c6c feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #286 (diff di aec9c6c)

## VERDETTO: APPROVATO CON RISERVE

Review #286, sul diff STAGED del ramo feat/via-binari-run-command (base 5725131). Ho letto CLAUDE.md, la sezione attiva di reports/stato_progetto.md e la mia memoria. Ho rilanciato i test: suite kernel **804 PASS 0 FAIL**, pytest **971 passed**. I numeri dichiarati sono confermati.

**Elementi del diff esaminati**
- `gas.py:837` — se SHELL_ALLOWLIST è vuota, run_command viene tolto da tools_schema. Rischio esaminato: il filtro deve valere anche per i kernel costruiti da notte e dal bot. Lo schema viene creato in `__init__` a partire dall'attributo di classe, quindi ogni kernel di produzione nasce senza run_command. — ok
- `gas.py:1415` — `SHELL_ALLOWLIST: frozenset = frozenset()`; la lista storica sopravvive come `_SHELL_ALLOWLIST_RECINTO`, ma nessun codice di produzione la legge: l'unico che la usa è `tests/test_unit_kernel.py`. Rischio esaminato: un percorso che riapra il recinto. `_vet_command` (`gas.py:1485`) controlla solo SHELL_ALLOWLIST, quindi ogni binario viene negato. — ok
- `gas.py:3387` — se arriva una run_command e la lista è vuota, il risultato diventa `GateClass.DENY` prima del ramo del cancello. Rischio esaminato: una firma su Telegram inutile, e l'interazione con il controllo symlink di write_file che segue. Il blocco agisce solo su run_command, write_file non è toccato e modules/gate non è modificato. Mutazione ragionata: senza questo blocco "ls" sarebbe UNCERTAIN, verrebbe eseguito e negato da `_vet_command` con un altro messaggio, quindi T85d fallirebbe. — ok
- `tests/test_unit_kernel.py:21` — patch di classe all'import (`GasKernel.SHELL_ALLOWLIST = _SHELL_ALLOWLIST_RECINTO`). Rischio esaminato: che la patch nasconda la configurazione reale altrove. `tests/conftest.py:6` contiene `collect_ignore = ["test_unit_kernel.py"]`, quindi pytest non importa lo script. `tests/test_unit_notte.py` (che costruisce GasKernel) e gli altri moduli vedono la lista vuota di produzione. La CI lancia lo script in un processo separato. — ok
- `tests/test_unit_kernel.py:8023` — T85 prova la configurazione reale:
  - a: la lista è vuota;
  - b: run_command è fuori dallo schema;
  - c: prompt e gas_identity.md non lo citano;
  - d: una run_command inventata dal modello viene negata e non parte nessuna chiamata a Telegram;
  - e: chiamata diretta, negata;
  - f: il codice del recinto c'è ancora;
  - g: catalogo.

  Ripristina la lista del recinto nel `finally`. — ok
- `gas.py:2437`, codice di contesto non toccato (applica_firma) — una run_command parcheggiata prima della PR, se firmata, passa a `execute_tool_call` (`gas.py:3105`), poi a `_vet_command`, ed è negata. `_run_command_meta` resta None, quindi l'esito nel diario è negativo. Nessuna riapertura. — ok, ma senza test (vedi R-286-2)
- `scripts/notte/catalogo_esempio.yaml:13` — salute_sistema ora usa elenca_cartella. — ok

Il recinto resta testato: i test di vetting, bwrap e snapshot continuano a girare con la lista storica. Nel diff non c'è slicing della history né simulazione dell'output dei tool. Il tetto di 10 iterazioni non è toccato.

**Riserve**
- **R-286-1 (BASSA)**: `gas.py:3566`, il controllo "Sandbox OS" del doctor (codice di contesto), in modalità os_strict senza bwrap dà ancora FAIL con exit 1 e la scritta "(run_command bloccato)", ma run_command non viene più offerto. È un falso allarme. Suggerimento: con la lista vuota declassarlo a OK/WARN "non usato". Il doctor non viene usato da notte o da altri script, quindi non blocca nulla.
- **R-286-2 (BASSA)**: nessun test prova applica_firma su una run_command parcheggiata prima della PR. Il percorso è sicuro per costruzione (vedi sopra) ma non c'è una prova meccanica.
- **Cosmetica**: reports/setup_notte.md (modificato ma NON in staging: ricordati di committarlo con i report) cita ancora «comandi in modalità non protetta» tra le azioni che vanno alla firma.

**Rischio escluso**: non ho verificato bwrap reale né il comportamento su VPS, perché non è riproducibile qui. Non ho fatto girare una sessione E2E reale (provider o Telegram veri) per vedere se un modello invoca comunque run_command: la copertura è solo T85d, con il modello scriptato.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #286 e una lezione, senza committare come richiesto. La lezione: una patch di classe all'import in uno script di test è accettabile solo se il file è escluso dalla collection di pytest.

## §5 DELTA TEST DEL MOTORE

Kernel 797 → 804 PASS (T85, 7 check nuovi); pytest 971 passed.

```
=== RIEPILOGO: 804 PASS, 0 FAIL ===
```

```
971 passed in 116.03s (0:01:56)
```

## §6 STATO CI

```
completed	skipped	feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)	verifica-bot	feat/via-binari-run-command	pull_request_target	38164870475	10s	2026-10-11T18:41:28Z
in_progress		feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)	CI	feat/via-binari-run-command	push	38164856927	53s	2026-10-11T18:41:16Z
completed	success	Merge pull request #184 from Gasss23/feat/strumenti-lettura-nativi	CI	main	push	38164275410	1m27s	2026-10-11T18:32:55Z
```

Mappatura commit→run:
- `aec9c6c` (primo push del ramo): run CI del push, se presente nell'elenco sopra; altrimenti run non ancora disponibile alla scrittura dell'handoff.
- commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-286-1 (BASSA): falso FAIL del doctor in os_strict senza bwrap.
- R-286-2 (BASSA): applica_firma su run_command vecchio senza test.
- Note dei verificatori di #184 (2° giro): V-1 bot (esito del diario dal prefisso), V-1 verifica esterna (credenziali cercabili, decisione dell'operatore), cosmetiche.
- R-284-2, R-283-1, R-283-2, R-277-1 (BASSE) e cosmetiche R-283-3/#284.
