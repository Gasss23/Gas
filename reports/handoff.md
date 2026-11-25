# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-25 — Voce: log più chiari e nome del modello sicuro (PR #407)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #407 (https://github.com/Gasss23/Gas/pull/407): «mergia» dell'operatore dato il 25/11.
   - Con APPROVATO pulito del bot sul nuovo head la mergia l'agente.
   - Altrimenti serve il «mergia» dell'operatore.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Log del primo turno scartato**: FATTA. Un «fine» sul primo turno ora è loggato come richiesta scartata.
- **Fetta 2 — Nome del modello**: FATTA.
  - Un nome non semplice ripiega su hey_jarvis (V-1 bot #405).
  - Il nome è normalizzato in `main` (R-864-1).
- **Fetta 3 — Log di avvio col modello in uso**: FATTA (R-855-1).
- **Fetta 4 — Riserve del bot #407 (eaed5d8a)**: FATTA.
  - V-1 e R-866-1: modelli pronti col nome del file, es. alexa_v0.1.
  - V-2: docstring e LEGGIMI.
  - V-3: il test controlla il nome passato al rilevatore.
  - R-864-2: avviso di ripiego una volta sola.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 ++
 clients/voice/ascolto.py           |  70 +++++++++++++++++++++++----
 reports/diff_sessione.md           |  24 +++++-----
 reports/handoff.md | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  73 +++++++++-------------------
 scripts/voce/LEGGIMI.md            |   2 +-
 tests/test_unit_voce_ascolto.py    |  63 ++++++++++++++++++++++++-
```

NB: regola «n/d»: il conteggio di reports/handoff.md non è misurabile mentre lo si scrive; la riga di totale è tolta.

## §3 GIT LOG --ONELINE (sessione)

```
46dfb8f9 Merge origin/main (PR #410 CRM) nel ramo della PR #407 — report del ramo tenuti, stato e memoria uniti (review #870-MERGE, R-870M-1 chiusa)
dbd0d167 docs(fine-task): report col giro sulle note del bot su 0d433dfc (review #869)
63a28b4a fix(voce): il nostro file del modello resta la prima scelta anche col nome di un modello pronto; avviso col valore rifiutato (V-1/V-2 bot su 0d433dfc)
bb542081 chore(revisore): memoria review #869 — APPROVATO
0d433dfc docs(fine-task): handoff col merge di main (PR #402, review #868-MERGE)
fb60ae2e Merge origin/main (PR #402 R7) nel ramo della PR #407 — report del ramo tenuti, memoria unita (review #868-MERGE)
7cba139c docs(report): riserve aperte della #407 tracciate in stato_progetto con id regolari (V-1 bot su 3d12ee08)
3d12ee08 docs(fine-task): report con le riserve del bot #407 chiuse (review #866/#867)
434e0966 fix(voce): modelli pronti col nome del file (alexa_v0.1), avviso di ripiego una volta sola, docstring e LEGGIMI (V-1/V-2/V-3 bot #407, R-864-2, R-866-1)
94f19a67 chore(revisore): memoria review #867 — APPROVATO CON RISERVE
20e3ded4 chore(revisore): memoria review #866 — APPROVATO CON RISERVE
eaed5d8a docs(fine-task): report della fetta voce log e nome del modello (review #864/#865)
c46b0b86 fix(voce): log chiaro sul primo turno scartato, modello in uso nel log di avvio, nome del modello normalizzato e mai un percorso (V-1 bot #405, R-855-1, R-864-1)
98ec858e chore(revisore): memoria review #865 — APPROVATO CON RISERVE
5586236b chore(revisore): memoria review #864 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

I commit c46b0b86 e 434e0966 toccano `tests/test_unit_voce_ascolto.py`, che è nel perimetro. Sotto ci sono i verdetti INTEGRALI, in ordine:
- #864: primo diff;
- #865: R-864-1 e R-864-2;
- #866: riserve del bot #407;
- #867: R-866-1;
- #869: V-1/V-2 del bot su 0d433dfc (il nostro file resta la prima scelta, avviso col valore).

```
## VERDETTO: APPROVATO CON RISERVE

Review #864 di fix/voce-log-e-modello, `git diff --cached` (2 file, +54/−5). Suite tests/test_unit_voce_ascolto.py rieseguita: 393 passati. Il motore (gas.py, brains/) non è toccato. Non ho usato git stash e l'indice è intatto.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1456` — un nome non semplice (percorso, maiuscole, vuoto) ora ripiega su `hey_jarvis` con un avviso nel log, invece di arrivare a openWakeWord.
   - Rischio: un percorso preso dall'ambiente che arriva a openWakeWord, il quale controlla `os.path.exists(nome)` rispetto alla cartella corrente.
   - Esito: ok, V-1 del bot #405 è chiusa. Il test `tests/test_unit_voce_ascolto.py:3407` lo prova con `../`, un percorso assoluto, maiuscole e la stringa vuota.
   - Effetto collaterale: vedi R-864-1.
2. `clients/voice/ascolto.py:773` — quando il server risponde «fine», il messaggio nel log dipende da `seguito`, il parametro di `turno` (`clients/voice/ascolto.py:749`). Sul primo turno dice «richiesta scartata dal server…». Il comportamento non cambia (`chiudi=True`, svuota, `return False`).
   - Esito: ok. Il test `tests/test_unit_voce_ascolto.py:547` controlla anche che non ci siano bip né audio riprodotto.
3. `clients/voice/ascolto.py:1485` — `descrivi_modello`, usata nel log «ascolto pronto» di `clients/voice/ascolto.py:1706`, distingue tre casi: nome invariato, ripiego, file nostro.
   - Esito: ok, R-855-1 è chiusa. Il test `tests/test_unit_voce_ascolto.py:3377` copre i tre casi. Vedi R-864-2.

**Riserve (da tracciare in stato_progetto.md)**

- **R-864-1 BASSA** (`clients/voice/ascolto.py:1456`):
  - Prima openWakeWord accettava anche nomi di modelli pronti scritti con spazi o con la versione (es. «hey mycroft», «alexa_v0.1»), perché li confrontava per pezzo di nome. Ora ripiegano su hey_jarvis, con l'avviso nel log. Per hey_jarvis il risultato è identico; per gli altri modelli pronti cambia parola in silenzio, salvo il log.
  - `verifica_della_voce` cerca il filtro col nome grezzo: con un nome ripiegato (es. «Hey_Jarvis») un filtro hey_jarvis già addestrato non si carica.
  - Proposta: normalizzare il nome (minuscole, spazio → `_`) prima della regex, oppure documentare che vale solo il nome esatto.
- **R-864-2 COSMETICA** (`clients/voice/ascolto.py:1488`): `descrivi_modello` richiama `modello_della_parola`, quindi all'avvio l'avviso di ripiego compare due volte nel log. Basterebbe passarle il risultato già calcolato.
- **Da prima, ancora aperta** (nota, non nuova): se il file di ehi_jarvis_it manca e si ripiega su hey_jarvis, resta la `GAS_ASCOLTO_SOGLIA=0.5` scritta da installa.sh per il modello italiano.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello nuovo non è misurata.

**Rischi esclusi**

- Ho preso per buona la prova dal vero del 25/11 sul Mac (richiesta di 1,0 s, il server chiude con `X-Gas-Comando: fine`). Il log del server non è nel repo.
- Non ho verificato che il server mandi «fine» solo per trascrizioni vuote o non chiare: modules/voice/ non è nel diff. Il nuovo messaggio dice «di solito», quindi non lo afferma come certo.
- Comportamento con openWakeWord vero: non l'ho riprovato, qui il pacchetto non è installato nell'ambiente dei test.

**Memoria**: aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #864 e una lezione (una funzione che descrive per il log non deve richiamare la funzione che decide e logga, altrimenti gli avvisi si duplicano). Già committate da sole (5586236b).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #865, solo il delta rispetto alla #864 su fix/voce-log-e-modello. L'indice ora vale 2 file, +68/−6. Ho rieseguito la suite tests/test_unit_voce_ascolto.py: 394 passati. Non ho usato git stash e l'indice è intatto.

R-864-1 è chiusa. R-864-2 è chiusa solo in parte: l'avviso di ripiego esce ancora due volte (sotto). Non blocca il commit.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1690` — in `main` il nome preso da `GAS_ASCOLTO_MODELLO` ora si pulisce (spazi ai lati, minuscole, spazi interni → `_`) prima di `verifica_della_voce` e del rilevatore.
   - Rischio: aprire una strada a un percorso.
   - Esito: ok. «/TMP/X.ONNX» diventa «/tmp/x.onnx», che la regex continua a rifiutare, quindi si ripiega comunque. Un filtro hey_jarvis già addestrato ora si carica anche con «Hey Jarvis» nel .env.
   - R-864-1 è chiusa per spazi e maiuscole. I nomi con la versione («alexa_v0.1») restano un ripiego dichiarato nell'avviso: va bene così.
2. `tests/test_unit_voce_ascolto.py:192` — test nuovo: «  Hey  Jarvis » produce «parola «hey_jarvis»» nel log, senza avviso di nome non valido.
   - Esito: ok, il test copre il caso.
   - COSMETICO: la lista `visti`, che raccoglie i nomi passati al rilevatore, non viene mai controllata. Un `assert visti == ["hey_jarvis"]` proverebbe che anche il rilevatore riceve il nome pulito. Ci sono anche 3 righe vuote prima del `@pytest.mark.parametrize` successivo.
3. `clients/voice/ascolto.py:1485` — `descrivi_modello(modello, usato)` ora riceve il risultato già calcolato e non richiama più `modello_della_parola`.
   - Esito: ok nella funzione.
   - Però `main` a `clients/voice/ascolto.py:1709` chiama di nuovo `modello_della_parola(modello)`. La chiama già `rilevatore_openwakeword` a `clients/voice/ascolto.py:1538`. Quindi all'avvio, quando si ripiega, l'avviso esce ancora due volte (vedi R-864-2).

**Riserve (da tracciare in stato_progetto.md)**

- **R-864-2 COSMETICA, ancora aperta**: le chiamate a `modello_della_parola` all'avvio sono ancora due (`clients/voice/ascolto.py:1538` e `clients/voice/ascolto.py:1709`). Correzione semplice: calcolare `usato` una volta in `main` e passarlo al rilevatore, oppure far restituire `usato` a `rilevatore_openwakeword`.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello italiano non è misurata.
- Ancora aperta, da prima: se il file manca, il ripiego su hey_jarvis resta con la `GAS_ASCOLTO_SOGLIA=0.5` scritta da installa.sh.

**Rischi esclusi**

- Il comportamento con openWakeWord vero e sul Mac: qui il pacchetto non c'è nell'ambiente dei test.
- La parte del diff già vista nella #864 (log del «fine» sul primo turno, ripiego per i nomi non semplici): non l'ho riesaminata.

**Memoria**: aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #865, con la lezione «una correzione di una chiamata doppia va verificata contando le chiamate col grep, non leggendo solo la funzione corretta». Già committata da sola (98ec858e).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #866 della PR #407: `git diff --cached`, 3 file (+39/−6). La suite tests/test_unit_voce_ascolto.py passa: 395 test, eseguiti anche in ordine fisso. Non ho usato git stash e l'indice è intatto.

Esito in breve: R-864-2 e la V-3 del bot sono chiuse. La V-1 del bot non è chiusa davvero (R-866-1).

**Elementi esaminati**

1. `clients/voice/ascolto.py:1471` — un nome presente in `_modelli_pronti()` ora passa così com'è, prima della regex.
   - Sicurezza: ok. L'elenco viene dal pacchetto, non dall'ambiente; un modello pronto con lo stesso nome di un nostro file salta il file, che è innocuo.
   - Riserva: la V-1 non è chiusa davvero (R-866-1).
2. `clients/voice/ascolto.py:1455` — `_avvisa_una_volta` scrive ogni avviso al massimo una volta, tramite il set di modulo `_AVVISI_DATI` (`clients/voice/ascolto.py:1452`).
   - Rischi: il testo dell'avviso trattato come formato, e lo stato condiviso tra i test.
   - Esito: ok. Il testo si costruisce prima ed è passato a `log.warning` senza argomenti, quindi un `%` dentro non dà problemi. Il set resta piccolo: pochi testi diversi per processo.
   - Il test `tests/test_unit_voce_ascolto.py:3388` azzera il set con monkeypatch e conta un solo avviso su due chiamate. Nessun altro test dipende da questi avvisi: quello di `tests/test_unit_voce_ascolto.py:3568` riguarda la verifica della voce. R-864-2 è chiusa.
3. `tests/test_unit_voce_ascolto.py:192` — il test ora controlla `visti == ["hey_jarvis"]`, cioè che anche il rilevatore riceve il nome pulito. Righe vuote sistemate.
   - Esito: ok, V-3 del bot chiusa.
4. `scripts/voce/LEGGIMI.md:237` e la docstring di `GAS_ASCOLTO_MODELLO`: descrivono la pulizia del nome e il ripiego.
   - Esito: ok, coerenti col codice. Per i nomi con la versione vale però R-866-1.

**Riserve (da tracciare in stato_progetto.md)**

- **R-866-1 BASSA**, che di fatto è la V-1 del bot ancora aperta (`clients/voice/ascolto.py:1471`):
  - Le chiavi vere di `openwakeword.MODELS`, lette dal pacchetto installato, sono `alexa`, `hey_mycroft`, `hey_jarvis`, `hey_rhasspy`, `timer`, `weather`: nessuna ha la versione. Quindi con openWakeWord vero «alexa_v0.1» non è in `_modelli_pronti()`, non passa la regex (per il punto) e ripiega ancora su hey_jarvis.
  - Il test passa solo perché mette «alexa_v0.1» nell'elenco finto, e il commento «anche con la versione, es. alexa_v0.1» descrive una cosa che non succede.
  - Le chiavi senza versione funzionavano già prima di questa modifica, quindi in pratica non cambia niente.
  - Correzione: aggiungere a `_modelli_pronti()` anche i nomi dei file da `openwakeword.get_pretrained_model_paths()` (es. `alexa_v0.1`), e usare valori veri nel test. In alternativa, togliere il caso e dichiarare che i nomi con la versione ripiegano.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello italiano non è misurata.

**Rischi esclusi**

- Non ho verificato l'elenco dei file restituito da `get_pretrained_model_paths()` sul Mac: dipende da quali modelli ha scaricato `installa.sh` (oggi solo hey_jarvis).
- Comportamento con openWakeWord vero nell'ascolto completo: non riprodotto qui.

**Memoria**: aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #866 e una lezione (un test che finge l'elenco di una libreria esterna deve usare valori presi dalla libreria vera). Già committate da sole (20e3ded4).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #867, solo il delta rispetto alla #866 (PR #407; l'indice ora vale 3 file, +58/−7). R-866-1 è chiusa. Resta una nota BASSA che c'era già prima (sotto). Non ho usato git stash e l'indice è intatto.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1442` — `_modelli_pronti()` ora aggiunge anche i nomi dei file da `openwakeword.get_pretrained_model_paths("onnx")`, cioè il nome senza `.onnx`.
   - Rischi: un'eccezione della libreria che fa crollare l'avvio, e nomi diversi da quelli veri.
   - Esito: ok.
     - L'elenco dei file è in un try suo: se fallisce, restano comunque le chiavi di `MODELS`.
     - Ho chiamato il pacchetto vero del venv di prova: `['alexa_v0.1', 'hey_mycroft_v0.1', 'hey_jarvis_v0.1', 'hey_rhasspy_v0.1', 'timer_v0.1', 'weather_v0.1']`. Quindi «alexa_v0.1» ora passa davvero.
     - L'elenco viene dal pacchetto, non dall'ambiente: nessun percorso arbitrario.
2. `tests/test_unit_voce_ascolto.py:3431` — il test usa un modulo finto con `MODELS` e percorsi in forma reale (`/x/openwakeword/resources/models/alexa_v0.1.onnx`). Chiama la funzione vera, salvata in `tests/test_unit_voce_ascolto.py:3416`, prima di sostituirla con il finto.
   - Rischio: un test che finge valori che la libreria non dà, il difetto trovato nella #866.
   - Esito: ok. I valori del finto coincidono con quelli del pacchetto vero.
   - La suite tests/test_unit_voce_ascolto.py passa: 395 test.

**Riserve (da tracciare in stato_progetto.md)**

- **Nota BASSA, già presente prima di questa fetta**: `get_pretrained_model_paths` elenca anche i modelli non scaricati. Nel venv di prova ne esiste 1 su 6. Con «alexa» o «alexa_v0.1» nel `.env`, senza averlo scaricato:
  - il nome passa come modello pronto;
  - `Model()` fallisce;
  - `main` esce con 1, quindi l'ascolto non parte invece di ripiegare su hey_jarvis.

  Era lo stesso anche prima per «alexa». Correzione possibile: contare come pronti solo i file che esistono davvero (`os.path.exists(p)`).
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello italiano non è misurata.

**Rischi esclusi**

- Gli altri modelli pronti sul Mac: `installa.sh` scarica solo hey_jarvis e non l'ho verificato lì.
- Il giro completo dell'ascolto con openWakeWord vero: non riprodotto qui.

**Memoria**: aggiunta la riga #867 in /home/user/Gas/.claude/agents/memoria_revisore.md, già committata da sola (94f19a67).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO

Review #869 della PR #407, dopo il bot su 0d433dfc: `git diff --cached` (2 file, +14/−5). Le due note del bot sono chiuse. La suite tests/test_unit_voce_ascolto.py passa: 395 test, rieseguiti da me. Non ho usato git stash e l'indice è intatto.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1479` — il controllo dei modelli pronti ora sta dentro il ramo dei nomi non semplici.
   - Rischio controllato: un nostro file `.gas_voce/modelli/<nome>.onnx` ignorato perché ha lo stesso nome di un modello pronto (V-1 del bot).
   - Esito: ok, V-1 chiusa. Per i nomi semplici si cerca di nuovo prima il file, come su main.
   - Se il file manca, il ramo «assente → pronto» di `clients/voice/ascolto.py:1498` torna raggiungibile. «alexa_v0.1», che ha un punto, passa sempre dal ramo dei pronti.
   - L'elenco dei modelli pronti viene dal pacchetto, mai dall'ambiente.
2. `clients/voice/ascolto.py:1488` — l'avviso riporta il valore rifiutato come `%r` di `modello[:60]`.
   - Rischio controllato: un valore con a capo o molto lungo scritto nel log.
   - Esito: ok, V-2 chiusa. `%r` scrive gli a capo come `\n` e il valore è tagliato a 60 caratteri. `main` passa sempre una stringa, quindi tagliarlo è sicuro.
3. `tests/test_unit_voce_ascolto.py:3430` — test nuovo: un nostro `hey_jarvis.onnx` fidato vince sul modello pronto. Il file viene poi rimosso, così le asserzioni che seguono non cambiano.
   - Esito: ok.

**Note aperte (non nuove, già tracciate)**

- **R-854-3 BASSA**: l'interruzione col modello italiano non è misurata.
- **Nota BASSA della #867**: i modelli pronti non scaricati (es. «alexa») fanno fallire l'avvio invece di ripiegare su hey_jarvis.

**Rischi esclusi**

- Non ho provato con openWakeWord vero che un nostro `hey_jarvis.onnx` venga caricato dal percorso. Qui il pacchetto non è installato nell'ambiente dei test; la parte che passa il percorso a `Model()` è già coperta dal test della V-3 (#857).
- Il comportamento sul Mac: non riproducibile qui.

**Memoria**: riga #869 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e già committata da sola (bb542081).

Il commit è consentito.
```

## §4bis VERDETTO DEL REVISORE SUL MERGE DI MAIN (PR #402)

```
## VERDETTO: APPROVATO

Review #868-MERGE: merge di origin/main 86a23f56 (PR #402, R7 fetta 4) nel ramo fix/voce-log-e-modello (PR #407, HEAD 7cba139c). Il merge è in staging e non committato; MERGE_HEAD coincide con origin/main. Non ho usato git stash.

- Nessun conflitto rimasto (`git ls-files -u` vuoto) e `--check` pulito.
- Rispetto a HEAD entrano 4 file (+205/−1).
- I test sottofondo più voce passano: 532 test, rieseguiti da me.

**Elementi esaminati**

1. `modules/sottofondo/__init__.py:17` e `tests/test_unit_sottofondo.py:1`: i file presi da main.
   - Rischio: modifiche non volute nel codice che arriva da main.
   - Esito: ok. `git diff --cached origin/main` su questi file è vuoto, quindi sono identici a main.
2. `clients/voice/ascolto.py:1442`, `tests/test_unit_voce_ascolto.py:3431`, `scripts/voce/LEGGIMI.md:237`, più `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` tenuti col lato del ramo (`--ours`).
   - Rischio: un file nostro perso nel merge.
   - Esito: ok. `git diff --cached HEAD` su questi percorsi è vuoto. Gli unici file cambiati da entrambi i lati sono memoria e stato_progetto, uniti come descritto sotto.
3. `reports/stato_progetto.md:4` e `reports/stato_progetto.md:405`: unione automatica.
   - Rispetto a main cambia solo la riga 393 della voce, cioè la nostra versione (+1/−1).
   - Rispetto a HEAD entrano la riga 4 di main, con la voce R7 del 25/11 in testa, e la voce R7 alla riga 405 (+2/−1).
   - La riga «Ultimo aggiornamento» compare una sola volta.
   - Esito: ok.
4. `.claude/agents/memoria_revisore.md:1`: memoria unita, nessuna riga persa né di HEAD né di main.
   - Esito: ok.

**Nota COSMETICA (viene da main, non da questo merge)**

- `reports/stato_progetto.md:4` dice «PR #402 ancora aperta», ma ora è mergiata. Si può aggiornare nel prossimo giro dei report.

**Rischi esclusi**

- Il contenuto della R7 fetta 4 (tetto di tempo duro del sottofondo): non l'ho rivisto nel merito, perché entra identico a main dopo le review #852-R7 e #853-R7.
- La suite completa: ho eseguito solo i test sottofondo e voce.

**Memoria**: ho aggiunto la riga #868-MERGE in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree (non in staging, non committata). Va messa in staging da te prima del commit del merge.

Il commit del merge è consentito.
```

## §4ter VERDETTO DEL REVISORE SUL MERGE DI MAIN (PR #410)

R-870M-1 chiusa nello stesso commit del merge: entrambe le voci sono ora in stato_progetto.

```
## VERDETTO: APPROVATO CON RISERVE

Review #870-MERGE: merge di origin/main 5a0f9dbc (PR #410, scheda CRM offline) nel ramo fix/voce-log-e-modello (PR #407, HEAD dbd0d167). Il merge è in staging e non committato; MERGE_HEAD coincide con origin/main. Codice e test sono a posto. La fusione di stato_progetto ha perso due finding aperti: vanno rimessi prima di committare (R-870M-1). Non ho usato git stash.

Controlli generali: `git ls-files -u` vuoto e `--check` pulito. Rispetto a HEAD entrano 10 file (+799/−4). Test CRM più voce: 606 passati, rieseguiti da me.

**Elementi esaminati**

1. `requirements.txt:1` e `tests/conftest.py:1`, i due file che toccano tutta la suite.
   - Rischio: una modifica fatta durante il merge che cambia l'ambiente di tutti i test.
   - Esito: ok. `git diff --cached origin/main` è vuoto, quindi sono identici a main. Rispetto a HEAD entrano solo `pypdf>=5.1` (con il suo commento) e `monkeypatch.delenv("GAS_CRM_SCHEDA_PASSWORD", raising=False)`.
2. `modules/crm/scheda.py:1`, `modules/crm/server.py:1`, `modules/crm/__main__.py:1`, `tests/test_unit_crm.py:1`, più `reports/crm/`.
   - Esito: ok, identici a origin/main.
3. I nostri file: `clients/voice/ascolto.py:1479`, `tests/test_unit_voce_ascolto.py:3430`, scripts/, più `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` tenuti col lato del ramo (`--ours`).
   - Esito: ok, `git diff --cached HEAD` su questi percorsi è vuoto. Gli unici file cambiati da entrambi i lati sono memoria e stato_progetto.
4. `.claude/agents/memoria_revisore.md:1`: memoria unita, nessuna riga persa né di HEAD né di main.
   - Esito: ok.
5. `reports/stato_progetto.md:4`: la riga è identica a quella di main e c'è una sola riga «Ultimo aggiornamento».
   - Esito: ok.
6. `reports/stato_progetto.md:394`, voce del modello italiano.
   - Bene: la V-3 della 2ª verifica esterna #405 (manca l'hash del modello valutato in ris/) è riportata, e c'è anche la licenza CC BY-NC-SA come decisione dell'operatore.
   - Esito: riserva, vedi R-870M-1.

**Riserva da sistemare prima del commit del merge**

- **R-870M-1** (`reports/stato_progetto.md:394`): nella versione di main, la stessa voce elenca due finding aperti che nell'indice non ci sono più (controllato con grep su tutto il file: 0 occorrenze).
  - **V-2 BASSA del bot su f51a58c7**: «§6 dell'handoff della #405 con esiti CI non allineati a gh run list».
  - **V-1 BASSA del bot su 05df3ae7**: «ripiego su hey_jarvis che tiene la soglia 0,5 senza filtro». È ancora vera: il ripiego non tocca la soglia.

  La V-1 del bot su f51a58c7 è invece giustamente data per chiusa (nomi non semplici → ripiego). Basta aggiungere le due voci nell'elenco «aperte» della riga 394. Il file è fuori dal perimetro, quindi non serve un'altra review: rimettile, metti in staging e committa.

**Rischi esclusi**

- Il contenuto della PR #410 (scheda PDF cifrata): non l'ho rivisto nel merito. Entra identico a main, revisionato dalla chat CRM.
- Il comportamento di pypdf sul Mac: non verificato qui.
- La suite completa: ho eseguito solo i test CRM e voce. conftest.py cambia per tutti solo con un `delenv`, che ha rischio nullo.

**Memoria**: riga #870-MERGE aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree (non in staging, non committata). Contiene anche la lezione: quando si riscrive a mano una voce di stato durante un merge, confrontare uno per uno i finding aperti delle due versioni. Mettila in staging tu prima del commit del merge.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_voce_ascolto.py`: 391 → 395 passed (4 test nuovi, 2 aggiornati).
- Suite completa: non rilanciata in questo container; la esegue la CI sul push.
- Prova col pacchetto vero (openwakeword 0.6.0 in un venv di prova): `_modelli_pronti()` comprende alexa_v0.1, hey_jarvis_v0.1 e gli altri file; `modello_della_parola("alexa_v0.1")` restituisce "alexa_v0.1".

## §6 STATO CI

- eaed5d8a, primo head della PR:
  - unit-suite e handoff-check: CI propria;
  - verifica-bot: success, verdetto APPROVATO CON RISERVE (V-1 BASSA, V-2 e V-3 COSMETICHE);
  - job «esito» in failure: GitHub ha risposto con un errore quando il bot ha pubblicato la recensione (`gh api … pulls/407/reviews` exit 1), non per un difetto della PR.
- 434e0966, 94f19a67 e 20e3ded4: nessuna run propria, vanno col push di questo commit.
- 3d12ee08: verifica-bot neutral (APPROVATO CON RISERVE, solo V-1 BASSA sui report, corretta in 7cba139c).
- 0d433dfc (merge di main, review #868-MERGE APPROVATO): verifica-bot neutral, APPROVATO CON RISERVE (V-1 BASSA, V-2 COSMETICA), corrette in questo giro.
- dbd0d167: CI verde (unit-suite e handoff-check success), verifica-bot neutral (APPROVATO CON RISERVE, una BASSA e una COSMETICA sul testo dei log, rimandate).
- Merge di main (PR #410) e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-867-1 BASSA preesistente: un modello pronto elencato ma non scaricato (es. alexa) fa uscire l'ascolto invece di ripiegare.
- R-854-3 BASSA: interruzione col modello italiano non misurata.
- Ripiego su hey_jarvis con la soglia 0,5 (bot #405): BASSA, aperta.
- Verifica esterna #407 (https://github.com/Gasss23/Gas/pull/407#issuecomment-7167530017):
  - V-1 (§6): riscritto.
  - V-2 (nomi con la versione): chiusa.
  - V-3 COSMETICA: il log «chiesto «…»» riporta il valore grezzo. Aperta.
- Chiuse anche V-1/V-2 del bot su 0d433dfc (review #869).
- Chiuse: V-1 bot #405, R-855-1, R-864-1, R-864-2, R-866-1, V-1/V-2/V-3 bot #407.
