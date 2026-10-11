# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — FETTA 1 PR B: nessun binario offerto al modello (PR #185), secondo giro dopo bot e verifica esterna

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #185 (https://github.com/Gasss23/Gas/pull/185). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/185"}`): `gh` nel container non è autenticato. **FERMO all'operatore**: dopo 2 giri il bot dà APPROVATO CON RISERVE (neutral, tocca `scripts/`), non il verdetto testuale APPROVATO richiesto dalla condizione d) dell'autorizzazione dell'operatore. Nessun finding ALTA/MEDIA; CI verde.
2. Chiavi private/file di credenziali leggibili e cercabili: nomi da segreto o compromesso (V-1 verifica esterna #184, 2° giro).
3. FETTA 4: `claude/roadmap_completa.md` non leggibile, allegato non arrivato.

---

## §1 SCOPE & ESITO FETTE

- **FETTA 1 PR A**: `FATTA` — PR #184 mergiata (`5725131`) in una sessione precedente di oggi.
- **FETTA 1 PR B — nessun binario offerto al modello**: `FATTA` — review #286 APPROVATO CON RISERVE; bot e verifica esterna APPROVATO CON RISERVE (neutral) → note corrette in `1d19bba` (review #287, #288 APPROVATO).
- **FETTA 2**: `DEFERITA` — dopo il merge della PR B.
- **FETTA 3**: `DEFERITA`.
- **FETTA 4**: `SALTATA — documento non leggibile`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md  |   5 +++++
 README.md                           |   7 ++++++-
 gas.py                              |  42 ++++++++++++++++++++++++++++++++----------
 gas_identity.md                     |   3 +--
 reports/diff_sessione.md            |  16 +++++++++-------
 reports/handoff.md                  | 220 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------------------------------------------------------------------
 reports/setup_notte.md              |  16 ++++++++++++----
 reports/stato_progetto.md           |  28 +++++++++++++++++++++-------
 reports/ultimo_report.md            |  25 ++++++++++---------------
 scripts/notte/catalogo_esempio.yaml |   5 ++---
 tests/test_unit_kernel.py           |  73 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 11 files changed (conteggi approssimati per reports/handoff.md)
```

Nota: i conteggi di righe di `reports/handoff.md` sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
c9f3f9c docs(stato): note del secondo giro su #185, merge all'operatore
ec701ec docs(fine-task): report PR #185 aggiornati (note di bot e verifica esterna, review #287-#288)
1d19bba fix(recinto): note di bot e verifica esterna #185 (messaggio, doctor, test firma)
94a9a90 docs(fine-task): report PR #185 (nessun binario offerto al modello, review #286)
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

### Review #287 (primo diff di 1d19bba)

## VERDETTO: APPROVATO CON RISERVE

Review #287 (seconda review della PR #185) sul nuovo diff in staging di gas.py e tests/test_unit_kernel.py. Prima avevo chiuso la review #286 (APPROVATO CON RISERVE, aperte R-286-1 e R-286-2), che è riassunta in coda. Ho rilanciato i test: kernel **806 PASS 0 FAIL**, pytest **971 passed**.

**Elementi del diff esaminati**
- `gas.py:3387` — il flag `_run_command_spento` (run_command con allowlist vuota) forza DENY e cambia il messaggio in «Gas non ha comandi di sistema. Usa elenca_cartella, …». Rischio esaminato: il flag poteva cambiare il messaggio di altri dinieghi o valere per altri tool. Vale solo per run_command; gli altri DENY restano col messaggio generico, e il controllo symlink di write_file che segue non viene toccato. — ok
- `gas.py:3576` — nel doctor, se manca la sandbox OS e l'allowlist è vuota, ora esce OK «non usato: run_command non offerto» invece di FAIL. Rischio esaminato: nascondere un FAIL reale quando run_command è offerto. L'ho provato rendendo finta la sonda della sandbox. Con la lista vuota esce OK. Con la lista del recinto esce `[FAIL ] … mode=os_strict (run_command bloccato)`, cioè il comportamento di prima. Chiude R-286-1. — ok
- `tests/test_unit_kernel.py:8072` — T85i accoda un run_command, lo firma e chiama applica_firma. Risultato: `eseguita: False` e output «Operazione negata» dal recinto. Rischio esaminato: un'asserzione sempre vera. La chiave `eseguita` esiste sempre, vale False di default e diventa True solo se il comando parte davvero, quindi l'asserzione regge. Chiude R-286-2. — ok
- `tests/test_unit_kernel.py:8065` — T85h lancia il doctor con os_strict e controlla che la riga «Sandbox OS» non contenga FAIL. Rischio esaminato: un test che non prova il ramo nuovo. Qui bwrap c'è, quindi il doctor passa dal ramo OK che esisteva già e il test resta verde anche se si toglie il ramo nuovo. — riserva

**Riserve**
- **R-287-1 (BASSA)**: T85h non forza l'assenza della sandbox. Dove bwrap è installato, come qui (e forse nella CI), il test non prova il ramo `gas.py:3576`. Correzione: dentro T85h sostituire `gas._probe_os_sandbox` con una versione finta che risponde `(False, "...")`, e rimettere l'originale nel `finally`.

**Rischio escluso**: non ho verificato se la CI su Ubuntu abbia bwrap, cioè se lì T85h prova il ramo nuovo; non ho accesso ai log dei runner. README.md e reports/setup_notte.md sono fuori perimetro e non li ho rivisti.

**Review #286**
- `## VERDETTO: APPROVATO CON RISERVE`
- Elementi esaminati: `gas.py:837`, `gas.py:1415`, `gas.py:3387`, `tests/test_unit_kernel.py:21`, `tests/test_unit_kernel.py:8023`.
- Riserve: R-286-1 e R-286-2 (entrambe BASSE), più una nota cosmetica su setup_notte.md.
- Il testo integrale è nella consegna precedente.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md le righe #286 e #287, ciascuna con una lezione. Non ho committato, come richiesto.

### Review #288 (diff finale di 1d19bba, correzione R-287-1)

## VERDETTO: APPROVATO

Review #288: seconda review della #287 sul diff staged di tests/test_unit_kernel.py. Ho rilanciato la suite del kernel: 806 PASS, 0 FAIL, con T85h verde e la riga «bwrap assente (finto, T85h) — non usato: run_command non offerto».

**Elementi esaminati**
- `tests/test_unit_kernel.py:8057` — T85h sostituisce `gas._probe_os_sandbox` con una sonda finta che risponde `(False, …)`, così il ramo «sandbox assente» viene provato anche dove bwrap c'è. Il rischio esaminato era che il doctor non usasse la sonda sostituita. Il doctor la chiama per nome dal modulo, quindi prende la finta. — ok
- `tests/test_unit_kernel.py:8062` — il blocco finally rimette la sonda vera e la variabile d'ambiente `GAS_SANDBOX_MODE`. Il rischio esaminato era che la finta restasse attiva e falsasse i test successivi. Il ripristino avviene anche se il doctor solleva un'eccezione. — ok
- `tests/test_unit_kernel.py:8068` — l'asserzione ora richiede «non usato» nella riga «Sandbox OS». Il rischio esaminato era un test sempre vero. Senza il ramo di `gas.py:3576` il doctor stamperebbe FAIL: l'ho verificato con la sonda finta e la lista del recinto nella review #287, quindi il test fallirebbe. — ok

R-287-1 è chiusa.

**Rischio escluso**: non ho rifatto la prova di mutazione sul file staged per non toccare l'index; il risultato FAIL senza il ramo è quello già osservato nella #287. Non ho rilanciato pytest perché questo diff tocca solo lo script, che pytest esclude.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga #288. Non ho committato.

## §5 DELTA TEST DEL MOTORE

Kernel 797 → 806 PASS (T85a–i); pytest 971 passed.

```
=== RIEPILOGO: 806 PASS, 0 FAIL ===
```

```
971 passed in 116.03s (0:01:56)
```

## §6 STATO CI

```
completed	success	feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)	verifica-bot	feat/via-binari-run-command	pull_request_target	38166016472	2m57s	2026-10-11T18:57:59Z
completed	success	docs(fine-task): report PR #185 aggiornati (note di bot e verifica es…	CI	feat/via-binari-run-command	push	38166015352	1m42s	2026-10-11T18:57:58Z
completed	success	feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)	verifica-bot	feat/via-binari-run-command	pull_request_target	38164927800	2m26s	2026-10-11T18:42:18Z
completed	skipped	feat(recinto): nessun binario offerto al modello (FETTA 1, PR B)	verifica-bot	feat/via-binari-run-command	pull_request_target	38164924546	1s	2026-10-11T18:42:16Z
```

Mappatura commit→run:
- `ec701ec` (testa del secondo push): CI success (unit-suite, handoff-check); verifica-bot neutral (APPROVATO CON RISERVE).
- `94a9a90` (testa del primo push): CI success; verifica-bot neutral.
- `aec9c6c`, `1d19bba`: nessuna run propria (pushati insieme alle teste sopra).
- commit di fine-task attuale: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Bot #185 (2° giro): V-1/V-2 COSMETICHE. Verifica esterna #185 (2° giro): V-1/V-2 BASSE, V-3 COSMETICA (vedi stato_progetto).
- Note dei verificatori di #184 (2° giro): V-1 bot (esito del diario dal prefisso), V-1 verifica esterna (credenziali cercabili, decisione dell'operatore), cosmetiche.
- R-284-2, R-283-1, R-283-2, R-277-1 (BASSE) e cosmetiche R-283-3/#284.
