# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 40: soglia della voce predefinita 200 invece di 500

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #333 (https://github.com/Gasss23/Gas/pull/333). Review #667 APPROVATO CON RISERVE e PR nel perimetro: l'operatore ha detto sì (via M1, 5 novembre); dopo il merge di main (review #670) la mergio io con la CI verde. Numero e URL letti dallo strumento GitHub (`list_pull_requests` con head `claude/peaceful-lovelace-0w2b7q`: la PR esisteva già, aperta il 4 novembre per b7f2c23).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 40 — soglia della voce 200**: `FATTA`
  `GAS_ASCOLTO_VOCE_RMS` predefinito da 500 a 200 (costante `VOCE_RMS_PREDEFINITO`), LEGGIMI aggiornato, 3 test nuovi (5 casi) con mutanti uccisi. Motivo: prova dell'operatore sul MacBook Air del 5 novembre.
- **Ripartenza della chat Mani (b7f2c23)**: `FATTA` (sessione precedente) — unita con un merge perché non era ancora in main.
- **Riserve basse della fetta 39**: `DEFERITA — M1 ha chiesto solo la soglia`.
- **Merge di main (PR #334, voce V13) in b00c506**: `FATTA` — conflitti solo nei report, review #670 APPROVATO, suite voce 358 passed.
- **Registrazione dei verdetti di bot e verifica esterna su 2c8cd2a**: `FATTA` — entrambi APPROVATO CON RISERVE, nessuna ALTA o MEDIA; riserve in stato_progetto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 clients/voice/ascolto.py           |  10 +-
 reports/diff_sessione.md           |  16 +--
 reports/handoff.md                 | n/d
 reports/ripartenza_mani.md         | 122 +++++++++++++++++------
 reports/stato_progetto.md          |   4 +-
 reports/ultimo_report.md           |  33 ++++++++++++++++++---------------
 scripts/voce/LEGGIMI.md            |   2 +-
 tests/test_unit_voce_ascolto.py    |  49 +++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 7bdaa8f (dopo il merge della PR #334).

## §3 GIT LOG --ONELINE (sessione)

```
b00c506 Merge origin/main (PR #334, voce V13) nella PR #333 — review #670 APPROVATO
51088d9 docs(fine-task): fetta 40 — riserve di bot e verifica esterna su 2c8cd2a registrate (PR #333)
2c8cd2a docs(fine-task): fetta 40 chat Mani — soglia della voce 200, review #667, PR #333
4f80d9d Merge remote-tracking branch 'origin/claude/peaceful-lovelace-0w2b7q' into claude/peaceful-lovelace-0w2b7q
20d2972 fix(voce): soglia della voce predefinita 200 invece di 500 (prova sul MacBook Air del 5 novembre)
27afc8f chore(revisore): memoria review #667 — APPROVATO CON RISERVE
b7f2c23 docs(mani): ripartenza aggiornata — stato al 4 novembre, riserve aperte, prossima fetta della voce e regole
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 20d2972 (review #667, chat Mani) — verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #667 (chat Mani). Diff staged su claude/peaceful-lovelace-0w2b7q rispetto alla base origin/main 8b8012d: 3 file, +57/-4. Ho letto CLAUDE.md (sezione 5), reports/stato_progetto.md e la mia memoria.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:85` — nuova costante `VOCE_RMS_PREDEFINITO = 200.0`, con il commento che spiega perché è stata cambiata. Rischio: due default diversi tra la classe e `main`. Esito: ok, la stessa costante è usata in entrambi i punti.
- `clients/voice/ascolto.py:239` — il default di `Ascolto(voce_rms=...)` ora usa la costante. Rischio: una soglia più bassa cambia `registra`, che inizia a registrare dopo 0,24 s di suono sopra soglia (INIZIO_VOCE_S) e si ferma a 30 s (REGISTRAZIONE_MAX_S), e cambia `aspetta_voce`, la finestra di 12 s dopo la risposta. Esito: riserva R-667-1.
- `clients/voice/ascolto.py:655` — `main` passa `_numero("GAS_ASCOLTO_VOCE_RMS", VOCE_RMS_PREDEFINITO, 10, 30000)`. Rischio: env ignorata o valore non valido. Esito: ok. «abc» torna a 200, i limiti 10–30000 restano, un valore non finito torna al default.
- `scripts/voce/LEGGIMI.md:82` — tabella aggiornata a 200, con l'indicazione di alzarlo a 300–500 in una stanza rumorosa. Esito: ok, la allinea `test_leggimi_riporta_il_default_della_voce`.
- `tests/test_unit_voce_ascolto.py:134` e `tests/test_unit_voce_ascolto.py:141` — test con voce a RMS 300 e test di `main` parametrizzato (None, «350», «abc»). Esito: ok, salvo R-667-2 e R-667-3.

**Verifiche eseguite**
- Suite in una copia dell'index in scratch: 133 passed, 21 failed. Sulla base origin/main: 128 passed, 21 failed, gli stessi test. Sono fallimenti dell'ambiente del container: modulo `openai` assente per `test_dotenv_usa_il_caricatore_di_gas` e i 20 casi di `test_installa_legge_il_env_come_gas`. Il diff aggiunge 5 test, tutti verdi. Il conteggio di 154 passed dichiarato da voi non l'ho riprodotto per questo motivo.
- Quattro mutanti in copia scratch, tutti uccisi:
  - costante a 500: 4 test falliti;
  - solo il default di Ascolto a 500: 1 fallito;
  - solo `main` a 500: 2 falliti;
  - `main` che ignora la variabile d'ambiente: 1 fallito.
- Effetti collaterali:
  - Eco della risposta: `turno` chiama `_svuota()` nel finally dopo la riproduzione (`clients/voice/ascolto.py:409`), quindi l'audio della risposta catturato dal microfono non apre turni. La soglia più bassa non cambia questo comportamento.
  - INIZIO_VOCE_S: resta l'unica difesa contro i rumori brevi (3 blocchi di fila sopra soglia). Un clic resta escluso; un rumore continuo tra 200 e 500 ora apre il turno.
- Wall of Shame: non applicabile. Il diff è un client, senza history né tool. §9 non toccato.

**Riserve**
- **R-667-1 BASSA**: con soglia 200 un rumore di fondo continuo sopra 200 (ventola, TV, tastiera) può:
  - aprire turni da solo nella finestra di 12 s, mandando rumore al server e consumando trascrizione e sintesi;
  - non far scattare mai la chiusura per silenzio, così la richiesta arriva a 30 s.

  È mitigato da `max_turni` (5), dall'uscita del ciclo quando un turno non riesce, dal tetto orario lato server (V12) e dalla nota nel LEGGIMI. La scelta si basa su una sola prova su un Mac: va riverificata in ambiente rumoroso. Non blocca, perché si regola dal .env.
- **R-667-2 BASSA**: nessun test fissa il limite basso. Il rumore dei test (SILENZIO) vale 10, quindi un default sceso per errore a 50 sopravvive a tutti i test. Proposta: un test in cui un rumore continuo a RMS ~150 non apre la finestra o chiude la richiesta.
- **R-667-3 COSMETICA**: `test_main_passa_la_soglia_della_voce` (`tests/test_unit_voce_ascolto.py:141`) non toglie `GAS_VOICE_URL` e `GAS_VOICE_PORT` dall'ambiente. Il test preesistente vicino alla riga 741 lo fa: se l'ambiente di CI avesse un URL non valido, `main` restituirebbe 1 e il test fallirebbe senza motivo.

**Cosa NON ho verificato**
- Il comportamento reale sul MacBook Air (guadagno del microfono, rumore di fondo reale, coda di riverbero dopo `afplay` e dopo `svuota`): non riproducibile nel container Linux, senza microfono né macOS.
- I 21 test che falliscono per l'ambiente: non li ho fatti girare con le dipendenze complete. Che siano identici sulla base esclude una regressione introdotta dal diff, ma non dimostra che passino.

**Incidente di processo**
Per confrontare con la base ho lanciato per errore `git stash --keep-index` sul repo vero. Ho verificato subito che lo stash conteneva solo una copia dello staged (nessuna modifica fuori dallo staging) e che l'index era intatto: stesso `--cached --stat`, 3 file. Poi ho rimosso lo stash e ho fatto il confronto su copie in scratch. Stato finale: index invariato, nessuno stash residuo.

**Memoria**
In `.claude/agents/memoria_revisore.md` ho aggiunto la riga contatore `#667 (chat Mani) — 2026-11-05 — APPROVATO CON RISERVE — …` e la lezione di non usare `git stash` sul repo vero per i confronti. Committata con `scripts/commit_memoria_revisore.sh` (commit 27afc8f, solo quel file; lo staged del diff è rimasto intatto).

Merge b00c506 (main con la PR #334 dentro la PR #333) — review #670, verdetto integrale:

## VERDETTO: APPROVATO

Review #670 (chat Mani). Ho controllato il merge di origin/main 7bdaa8f (PR #334, voce V13) nel branch claude/peaceful-lovelace-0w2b7q (PR #333, fetta 40). Il merge è in corso e staged; ho guardato `git diff --cached HEAD` e `git diff --cached MERGE_HEAD`.

**Cosa ho esaminato nel diff**
- `modules/voice/server.py:453`: è il filtro V13 `_SOLO_ATTIVAZIONE`, che risponde «Dimmi.» passando da `_rispondi_senza_turno`. Ho controllato se interagisce con la fetta 40: no. È tutto lato server e usa la stessa strada di risposta senza turno già gestita da ascolto.py nel formato audio+pezzi. Il contenuto del file nell'index è identico a quello di MERGE_HEAD, cioè quello già rivisto in #667-M2, #668-M2 e #668-M2 bis. Esito: ok.
- `tests/test_unit_voice_server.py:1666`: è il test V13 sull'orologio locale, e anche questo file nell'index è identico a MERGE_HEAD. Ho controllato se si perdeva qualche test V13: non se ne perde nessuno. Vale lo stesso per `tests/test_unit_voice_stt.py` e per `reports/ripartenza_m2.md`, tutti identici a MERGE_HEAD. Esito: ok.
- `reports/stato_progetto.md:4`: ho controllato se il conflitto era risolto male. La riga è il prefisso della fetta 40, poi « — prima: », poi la riga 4 di main senza modifiche (prefisso e suffisso controllati con uno script). Ho rifatto il merge in automatico con `git merge-file` nello scratch: l'unico punto in conflitto era quella riga. Il resto, cioè la voce V13 aggiunta da main e il paragrafo della fetta 40 dal tuo lato, coincide con l'index. Esito: ok.
- Contesto: `clients/voice/ascolto.py:85` (`VOCE_RMS_PREDEFINITO = 200.0`). ascolto.py, LEGGIMI, test di ascolto, ripartenza_mani, handoff, ultimo_report e diff_sessione nell'index sono identici a HEAD, quindi resta la tua versione. Esito: ok.
- Memoria del revisore: contiene tutte le righe di HEAD e tutte quelle di MAIN, senza doppioni. L'unica riga ripetuta è una riga vuota, che c'era già su entrambi i lati.
- Marcatori e conflitti: nessun marcatore di conflitto, `git diff --cached HEAD --check` pulito, `git ls-files -u` vuoto.
- Test: copia dell'index nello scratch con `git checkout-index`, senza toccare il repo vero. Suite ascolto, server e stt: 334 passed e 24 failed, 358 in totale come i tuoi. I 24 fallimenti dipendono tutti dall'ambiente: 23 per `ModuleNotFoundError: openai`, più il test di collection dell'intero repo che si ferma per lo stesso motivo. Sono gli stessi già segnalati come preesistenti in #667 (21) e #667-M2 (3).

**Cosa non ho verificato**
- Non ho rieseguito le suite in un ambiente con openai installato: nel container manca. I tuoi 358 passed li prendo per buoni, ma la mia prova li conferma solo per i 334 test che non dipendono da openai.
- Non ho rifatto la review del contenuto della V13: è già stata rivista da M2 e qui entra senza modifiche.
- Non ho controllato come si comporta il sistema dal vero sul Mac.

**Riserve:** nessuna (nessuna R-670-n).

**Memoria:** ho aggiunto la riga `#670 (chat Mani) — 2026-11-05 — APPROVATO — …` in coda a `.claude/agents/memoria_revisore.md`. È solo nel working tree, NON staged e NON committata: aggiungila tu al commit del merge con `git add`. Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 149 a 154 casi (+3 test, 5 casi). Riepilogo reale nel venv con requirements e requirements-dev:

```
........................................................................ [ 93%]
..........                                                               [100%]
154 passed in 16.16s
```

Mutanti: costante a 500 → 4 FAILED (`test_voce_piana_passa_col_default`, `test_main_passa_la_soglia_della_voce[None-200.0]`, `[abc-200.0]`, `test_leggimi_riporta_il_default_della_voce`); solo `main` a 500 → 2 FAILED. Nessun FAIL fuori scope nel mio ambiente (i 21 del revisore erano per `openai` assente nel suo).

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Ultime run CI lette prima del merge di main:

```
42076739905 CI  push  2c8cd2a  (handoff-check success; unit-suite in corso alla lettura)
verifica-bot su 2c8cd2a: neutral (APPROVATO CON RISERVE, PR nel perimetro)
```

Mappatura commit → run:
- b00c506 (merge di main) e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (si pushano insieme: la run del push testa la testa).
- 51088d9: run del suo push, non riletta qui.
- 2c8cd2a: CI run 42076739905.
- 4f80d9d: CI run 42076547829.
- 20d2972, 27afc8f: nessuna run su questo SHA (pushati insieme a 4f80d9d).
- b7f2c23: nessuna run CI su questo SHA tra quelle lette.

Suite voce in locale dopo il merge (ascolto, server, stt): 358 passed.

## §7 RISERVE APERTE

- R-667-1 BASSA: con soglia 200 un rumore continuo (ventola, TV) può aprire turni da solo nella finestra di 12 s e non chiudere la richiesta prima dei 30 s. Da riprovare in una stanza rumorosa; si regola dal .env.
- R-667-2 BASSA: nessun test fissa il limite basso (un default sceso per errore a 50 passerebbe).
- R-667-3 COSMETICA: `test_main_passa_la_soglia_della_voce` non toglie GAS_VOICE_URL/GAS_VOICE_PORT dall'ambiente.
- Bot su 2c8cd2a, V-1 BASSA: rumore continuo sopra 200 → fino a ~150 s di audio della stanza inviati alla trascrizione per attivazione (rimedio: soglia adattiva come nel client browser V9). V-2 COSMETICA: base della PR su GitHub vecchia (9cd1ad5).
- Verifica esterna (https://github.com/Gasss23/Gas/pull/333#issuecomment-6665009996): V-1 BASSA (R-667-2 sovrastimata: un default a 50 fa fallire 3 test; resta scoperto solo il rumore continuo a ~150), V-2 BASSA (= bot V-2), V-3 BASSA (= R-667-1), V-4 COSMETICA (§6 citava la CI di 4f80d9d).
- Restano le riserve della fetta 39 e precedenti, elencate in `reports/stato_progetto.md`.
