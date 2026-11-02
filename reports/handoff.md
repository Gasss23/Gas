# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Mani, fetta 37 (R8): voce H24, Gas sempre in ascolto sul Mac (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #323 (https://github.com/Gasss23/Gas/pull/323). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5123976401","url":"https://github.com/Gasss23/Gas/pull/323"}`), perché `gh` nel cloud non è autenticato. La PR tocca `.github/workflows/ci.yml` (macchina del bot): il merge lo decide l'operatore.
2. Licenza dei modelli pronti di openWakeWord («hey_jarvis», CC BY-NC-SA, non commerciale): va bene per le prove, oppure si aspetta «Ehi Gas» nostra? (R-615-5)
3. Prova sul Mac: `bash scripts/voce/installa.sh`, poi «Hey Jarvis»; se `.gas_voce/ascolto.log` dice «solo silenzio assoluto», il permesso del microfono sotto launchd non è passato (R-615-4, `scripts/voce/LEGGIMI.md`).

---

## §1 SCOPE & ESITO FETTE

- **PR #319 (fetta 36, avvisa_operatore)**: `FATTA` — mergiata (ceaa4aa) col sì dell'operatore, dopo i merge di main delle PR #318, #321 e #320 (review #619, #620).
- **Voce H24 (piano approvato da M1, con installa.sh, spegni.sh e LEGGIMI.md chiesti da M1)**: `FATTA` — `clients/voice/ascolto.py`, `scripts/voce/`, `clients/voice/requirements-ascolto.txt`, `.gitignore`, un passo in ci.yml (ok di M1), 73 test. Scritta su un branch locale mentre la #319 aspettava, poi portata su main come un unico diff (review #621).
- **Review #615 (chat Mani)**: BOCCIATO. R-615-1 MEDIA (installa.sh usciva in silenzio senza GAS_VOICE_PORT), R-615-2 BASSA (redirect e proxy di sistema col Bearer), R-615-3 BASSA (cartella con `$()`), R-615-6 BASSA (un clic apriva la richiesta; privacy dichiarata incompleta), R-615-7 BASSA (grep -q con pipefail, reset ridondante, log senza rotazione): `FATTA`. R-615-4 MEDIA (microfono sotto launchd) e R-615-5 BASSA (licenza): `DEFERITA — da provare sul Mac / decide l'operatore`.
- **Review #616**: APPROVATO CON RISERVE. R-616-1 BASSA (porta del client), R-616-2 BASSA (attesa dopo la parola), R-616-3 COSMETICA (log): `FATTA`.
- **Review #618**: APPROVATO CON RISERVE. R-618-1 BASSA (`main` senza test sull'URL) e R-618-2 COSMETICA: `FATTA` in questa PR.
- **Review #621**: APPROVATO CON RISERVE. R-621-1 BASSA (memoria #615/#616/#618 dal branch locale): `FATTA` in 5876b7e.
- **Bot su c5e7321 (https://github.com/Gasss23/Gas/pull/323#pullrequestreview-5740118682)**: APPROVATO CON RISERVE, check verifica-bot neutral (la PR tocca ci.yml). V-1 BASSA (il client leggeva il .env con un parser suo: con un commento in linea il token era diverso dal server), V-2 BASSA (installa.sh prendeva l'ultima GAS_VOICE_PORT; con GAS_VOICE_URL il controllo finale guardava solo il Mac), V-3 COSMETICA (microfono non svuotato dopo un invio fallito): `FATTA` in 7de4eeb.
- **Review #622 (chat Mani)**: APPROVATO CON RISERVE. R-622-1 BASSA (installa.sh fonde nella porta le cifre di un commento in linea: falso STOP, fail-closed), R-622-2 COSMETICA, R-622-3 COSMETICA: `DEFERITA — registrate`.
- **Verifica esterna su c5e7321 (https://github.com/Gasss23/Gas/pull/323#issuecomment-6583089402)**: APPROVATO CON RISERVE. V-1/V-2/V-5 coincidono con V-1/V-2/V-3 del bot (`FATTA` in 7de4eeb). V-3 BASSA (installa.sh senza controllo di Python ≥ 3.11 e con un solo controllo dopo `sleep 5`) e V-4 BASSA (la frase «nei log mai la conversazione» non vale per voce.server.log): `FATTA` nel commit dopo la review #623, insieme a R-622-1 (porta con commento in linea).
- **Bot su 1127f5c (https://github.com/Gasss23/Gas/pull/323#pullrequestreview-5740245924)**: APPROVATO CON RISERVE, check neutral. V-1 BASSA (V-3/V-4 della verifica esterna non registrate) e V-2 COSMETICA («62 test» in §1 e in ultimo_report): `FATTA` in questo commit.
- **Review #623 (chat Mani)**: APPROVATO CON RISERVE. R-623-1 BASSA (il ricontrollo dei servizi dopo l'attesa non ha un test), R-623-2 COSMETICA (finto sleep muto), R-623-3 COSMETICA (messaggio sul python3 del PATH): `DEFERITA — registrate`.
- **Riserve aperte di #319 in stato_progetto (richiesta di M1)**: `FATTA` — V-1 bot e V-1/V-2 ve su 9c44686.
- **Piano mail**: `DEFERITA — PR doc-only subito dopo questa (un solo branch remoto)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md     |  12 +++++++
 .github/workflows/ci.yml               |   8 +++++
 .gitignore                             |   1 +
 clients/voice/ascolto.py               | 512 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 clients/voice/requirements-ascolto.txt |   4 +++
 reports/diff_sessione.md               |  24 ++++++--------
 reports/handoff.md                     | n/d
 reports/ripartenza_mani.md             |   2 +-
 reports/roadmap.md                     |   4 +--
 reports/stato_progetto.md              |   5 +--
 reports/ultimo_report.md               |  30 ++++++++---------
 scripts/voce/LEGGIMI.md                |  97 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/com.gas.ascolto.plist     |  28 ++++++++++++++++
 scripts/voce/com.gas.voce.server.plist |  28 ++++++++++++++++
 scripts/voce/installa.sh               | 110 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/spegni.sh                 |  13 ++++++++
 tests/test_unit_voce_ascolto.py        | 638 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: base = merge-base con origin/main = ceaa4aa. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
3b322ef fix(voce): installa.sh controlla Python 3.11, aspetta il server fino a 30 s, porta senza commento in linea; log del server da trattare come privato (V-3/V-4 ve #323, R-622-1, review #623)
57f12dc chore(revisore): memoria review #623 — APPROVATO CON RISERVE
1127f5c docs(fine-task): fetta 37, PR #323, correzioni bot su c5e7321, review #622
7de4eeb fix(voce): il client legge il .env come il server (gas._carica_dotenv), porta: vale la prima riga, svuota dopo un errore (V-1/V-2/V-3 bot #323, review #622)
4fc2378 chore(revisore): memoria review #622 — APPROVATO CON RISERVE
c5e7321 docs(fine-task): fetta 37, PR #323, voce H24, review #615-#621
5876b7e chore(revisore): memoria review #615, #616, #618 (voce H24, dal branch locale)
234f41c feat(voce): Gas sempre in ascolto sul Mac — parola di attivazione locale, launchd, installa in un colpo (R8, fetta 37, chat Mani)
31b8ec1 chore(revisore): memoria review #621 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 234f41c (clients/voice/ascolto.py, scripts/voce/, tests/test_unit_voce_ascolto.py, .github/workflows/ci.yml, .gitignore). È il diff del branch locale voce-h24 (commit 8e69ab6 e 52c26bf, rivisti in #615/#616/#618) portato su main con le correzioni di R-618-1/2 (rivisto in #621). Verdetto integrale della review #615 (chat Mani), sulla prima versione:

```
## VERDETTO: BOCCIATO

Review #615 (chat Mani), R8 «voce H24». Ho rivisto il diff staged (sha256 7839f0f01edadc59..., verificato), sul branch voce-h24 con base b472fe1. Prima ho letto CLAUDE.md, reports/stato_progetto.md e la mia memoria. Il blocco è uno solo (R-615-1): è un bug vero, l'ho riprodotto e si corregge con una riga. Il resto sono riserve.

**Elementi del diff esaminati**

1. `scripts/voce/installa.sh:76` — legge la porta dal `.env` con `PORTA="$(grep … | tail -1 | sed …)"`, sotto `set -euo pipefail`. Rischio: un'assegnazione la cui sostituzione fallisce ferma lo script. — **BLOCCO (R-615-1, MEDIA)**. Riprodotto nella cartella di lavoro: con un `.env` senza `GAS_VOICE_PORT` (il caso normale, porta di default 8765) lo script esce con 1 senza nessun messaggio, subito dopo «5/6 servizi caricati: OK». Il controllo della porta e il messaggio finale non arrivano mai: l'operatore pensa che sia fallito, mentre i servizi girano. Con `GAS_VOICE_PORT=9000` invece arriva in fondo.
   - Correzione: `PORTA="$( { grep -E '…' .env || true; } | tail -1 | sed …)"`.
   - Va aggiunto un test che esegue installa.sh con comandi finti nel PATH (uname che risponde Darwin, launchctl, plutil, nc, python). Deve fallire sul codice di oggi. Oggi lo script è provato solo con `bash -n` e col rifiuto fuori dal Mac.
2. `clients/voice/ascolto.py:333` — POST /voice con urllib, header Bearer. Rischio: il token esce verso un host diverso. — **riserva R-615-2 BASSA**. Riprodotto: se il server risponde 302 verso un altro host, urllib rifà la richiesta in GET, ricopia `Authorization: Bearer SEGRETO-TOKEN` e il client accetta come buona la risposta audio. Il controllo di `clients/voice/ascolto.py:115` (`url_valido`, «fuori dal Mac solo https») si aggira così, anche verso http. In più su macOS urllib usa i proxy di sistema anche per 127.0.0.1: le eccezioni di default sono «*.local, 169.254/16» e il codice di urllib non salta di suo gli indirizzi locali. Correzione: un opener con `ProxyHandler({})` e un gestore che rifiuta i redirect.
3. `scripts/voce/installa.sh:24` — il `case` che rifiuta i caratteri pericolosi nella cartella di Gas. Rischio: iniezione dalla cartella dentro il sed (riga 55) e dentro la shell del plist (`scripts/voce/com.gas.ascolto.plist:15`, `cd "CARTELLA_GAS"` tra virgolette doppie). — **riserva R-615-3 BASSA**. Riprodotto: una cartella chiamata `Gas$(touch PWNED)` passa il controllo e la shell esegue il comando. Rifiuta & < > " # ma non `$`, il backtick, `\` e l'a capo. La cartella è dell'operatore, quindi il rischio reale è basso, ma la riga si presenta come una protezione. Meglio una lista bianca `[A-Za-z0-9/._ -]`.
4. `clients/voice/ascolto.py:356` — `riproduci_afplay`: cartella da mkdtemp (0700), file con O_EXCL 0600, `rmtree` nel finally, timeout di 600 s. Il timeout è intercettato da `turno`. — **ok**. Sulla privacy prima della parola: `aspetta_parola` passa i blocchi solo al rilevatore e non li tiene in memoria. Fino alla parola non c'è niente su disco né in rete — **ok**.
5. `clients/voice/ascolto.py:302` — l'ordine azzera → bip → svuota, e lo svuotamento dopo la risposta in `turno`. Rischio: Gas che si attiva da solo con la sua voce. — **ok**. Durante afplay il microfono non viene letto e poi si butta il buffer. Il rilevatore non gira né nella conversazione né nella finestra. Tre mutanti miei, ciascuno preso con 1 failed (test_parola_bip_registrazione_e_risposta): senza svuota dopo il bip, senza svuota dopo la risposta, senza azzera finale. Nota BASSA dentro R-615-7: il reset iniziale misurato costa 0,21 s, ed è ridondante perché c'è già quello finale. Con bip e svuota butta circa mezzo secondo di parlato, quindi chi non aspetta il bip perde le prime parole.
6. `clients/voice/ascolto.py:221` — `registra`, e la soglia a numeri interi (`blocchi_per`). — **ok**: 0,8 s = 10 blocchi, 12 s = 150, 30 s = 375, 0,24 s = 3. Il minimo di 0,2 s diventa 0,16 s, trascurabile. Riserva in R-615-6: dopo la parola basta un solo blocco da 80 ms sopra la soglia (un clic) per aprire la richiesta, mentre nella finestra ne servono 3. È incoerente, e un clic produce una clip di rumore mandata a Whisper.
7. `scripts/voce/installa.sh:73` — `launchctl print … | grep -q` con pipefail. — **riserva BASSA (R-615-7)**: se launchctl scrive dopo che grep ha già chiuso, arriva un SIGPIPE (codice 141) e lo script dice per sbaglio «non gira». Meglio salvare prima l'output in una variabile.
8. Contesto, file non toccato: `modules/voice/server.py:220` — risponde audio/mpeg solo se l'header Accept lo chiede. Con testo vuoto risponde 200 in JSON e con un errore TTS 502: il client fa il bip di errore — ok. Nota: dopo un 502 l'azione del kernel può essere già avvenuta. Il bip non lo distingue e l'operatore potrebbe ripetere la richiesta (dentro R-615-6).

**Altre riserve**

- **R-615-4 MEDIA, da provare sul Mac**: il permesso del microfono sotto launchd. Python avviato da launchd, senza un'app che lo «possieda», potrebbe essere negato in silenzio senza nessuna richiesta. Il pannello Microfono non ha il «+», quindi l'istruzione del LEGGIMI («accendi Python», `scripts/voce/LEGGIMI.md:28`) potrebbe non essere eseguibile. L'avviso sul microfono che dà solo zeri dà il segnale giusto. R8 non va dichiarata funzionante prima della prova sul Mac. Va tracciata in stato_progetto.md.
- **R-615-5 BASSA, decide l'operatore**: i modelli pronti di openWakeWord sono sotto licenza CC BY-NC-SA 4.0, cioè non commerciale. Verificato nel METADATA del wheel 0.6.0. Usare «hey_jarvis» in Gas, che è un partner di business, è una zona grigia. Va scritto nel LEGGIMI; il modello «Ehi Gas» addestrato chiude la questione.
- **R-615-6 BASSA, privacy dichiarata incompleta**: una falsa attivazione (TV, un'altra persona) o qualsiasi voce di almeno 240 ms nella finestra di 12 s manda a Groq l'audio della stanza e fa partire un turno del kernel. Nel caso peggiore 5 turni da 30 s: è limitato, ma va detto nel LEGGIMI accanto a `scripts/voce/LEGGIMI.md:46`.
- **R-615-7 BASSA, varie**: oltre al grep -q e al reset iniziale, i log in `.gas_voce/` non hanno rotazione (con il microfono staccato si aggiunge una riga ogni 5 s). Con KeepAlive, un'uscita 1 per configurazione mancante riparte ogni 10 s: costa poco perché il token si controlla prima di importare openWakeWord, quindi è accettabile. Se un passo fallisce restano a metà dei plist in ~/Library/LaunchAgents: `spegni.sh` li toglie.

**Coerenza col progetto**: va nella direzione di D-voce-3 del briefing (parola di attivazione in locale sul dispositivo, prima il giro, poi l'orecchio) e della voce R8 della roadmap («openWakeWord; prima il modello pronto, poi la parola nostra»). La roadmap segna R8 «🔒 R5»: questa parte gira sul Mac e non dipende dal server, con il piano approvato da M1. Va aggiornata `reports/roadmap.md`, che non è nel diff. Il server voce e la pagina del browser non sono toccati. Il passo nuovo in ci.yml non aggiunge `paths-ignore`. Il motore (gas.py, `_get_window`, tetti) non è toccato.

**Prove riprodotte**: 43 passed da root. Ho installato openWakeWord 0.6.0 vero (con `--no-deps`, perché tflite-runtime manca su Linux con Python 3.13; sul Mac non serve), con numpy 2.4.6 e onnxruntime 1.27.0. `download_models(["hey_jarvis_v0.1"])` scarica anche la versione onnx, `Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")` carica, `predict` su un blocco da 1280 (anche ricavato da una colonna come in `Microfono.blocchi`) dà 0.0, `reset` azzera anche i buffer interni dell'audio, 10 s di audio si elaborano in 0,31 s. `source .venv/bin/activate` sotto `set -u` funziona.

**Cosa NON ho verificato**: il comportamento vero sul Mac: permessi del microfono sotto launchd, launchctl bootstrap/print, plutil, afplay, sounddevice con CoreAudio, quanto PortAudio tiene nel buffer durante una risposta lunga, bash 3.2 di macOS. Qui non si può riprodurre: ambiente Linux, senza audio e senza launchd. Non ho misurato quante false attivazioni dà hey_jarvis con la voce italiana o con la TV, né quanto è adatta la soglia di volume 500 con il microfono vero.

**Per la ri-review**: correggere R-615-1 con il test sugli script (che deve fallire sul codice di oggi). R-615-2 e R-615-3 sono correzioni da poche righe, consigliate nello stesso giro. Le altre riserve vanno in reports/stato_progetto.md.

Memoria aggiornata: riga #615 più 2 lezioni (le assegnazioni con pipefail; urllib che ricopia il Bearer sui redirect e usa i proxy di sistema). Commit 3900afb, poi 6213ea4 (corretto un numero di riga). Il diff staged è intatto (sha256 sempre 7839f0f01edadc59...).
```

Verdetto integrale della review #616 (chat Mani), sul diff del commit locale 8e69ab6:

```
## VERDETTO: APPROVATO CON RISERVE

Review #616 (chat Mani), ri-review della #615. Fetta R8, voce H24 sul Mac. Diff staged con sha256 che inizia per 350d51c7f4af73e0: l'ho verificato prima e dopo la review, è invariato. Branch locale voce-h24, base b472fe1.

Letture obbligatorie fatte: CLAUDE.md (sez. 5, 8, 9, 10), stato_progetto.md (letto con Grep), memoria del revisore.

**Elementi del diff esaminati**
- `scripts/voce/installa.sh:84` — legge la porta con `{ grep … .env || true; }`. Rischio esaminato: con `set -euo pipefail` lo script usciva in silenzio quando la porta non è nel `.env` (era R-615-1). Esito: ok. I test portano lo script fino in fondo con i comandi del Mac finti: «6/6» e `nc -z 127.0.0.1 8765`; con la porta 9001 nel `.env`, `nc` va sulla 9001. Il mutante «grep senza `|| true`» dà 1 failed.
- `scripts/voce/installa.sh:26` — lista bianca `^[A-Za-z0-9/._ -]+$` controllata con `[[ =~ ]]`. Rischio esaminato: caratteri che finiscono nel sed e nella shell zsh del plist (`$( )`, backtick, `\`, `&`, `"`, `#`, `;`). Esito: ok. I 7 casi del test vengono rifiutati con STOP prima di toccare qualcosa. Il mutante con la lista bianca `.*` dà 7 failed.
- `clients/voice/ascolto.py:344` — l'opener usa `ProxyHandler({})` e `_NienteRedirect`. Rischio esaminato: il token Bearer che segue un redirect o passa da un proxy di sistema (era R-615-2). Esito: ok. `build_opener` scarta i gestori predefiniti quando gli si passa una loro sottoclasse, quindi un 302 diventa un errore «HTTP 302» con una sola richiesta. Mutanti: senza `_NienteRedirect` 1 failed, senza `ProxyHandler({})` 1 failed.
- `clients/voice/ascolto.py:234` — dopo la parola la voce comincia solo con 3 blocchi forti di fila (era R-615-6). Rischio esaminato: un clic che apre una richiesta, oppure l'inizio della voce che si perde. Esito: ok. Il mutante «blocchi forti tenuti anche non di fila» dà 2 failed. Lo stesso punto produce però la riserva R-616-2.
- `clients/voice/ascolto.py:323` — l'azzeramento del rilevatore resta solo a fine conversazione (era R-615-7). Esito: ok, il test pretende 1 azzeramento. Anche le eccezioni nel ciclo restano intercettate (§9).
- `scripts/voce/installa.sh:76` — l'output di `launchctl print` è salvato in una variabile, con `|| true` e un `case`. Esito: ok, non c'è più il falso «non gira» da SIGPIPE.
- Contesto: `modules/voice/server.py:473` — il server legge `GAS_VOICE_PORT` dal `.env`. Da qui nasce la riserva R-616-1.

**Prove riprodotte**
- `tests/test_unit_voce_ascolto.py`: 57 passed.
- Mutanti provati su una copia dell'indice in scratch, senza toccare il working tree: risultati come sopra (1, 1, 1, 7 e 2 failed).
- Nessun antipattern della sez. 5 (né slicing della history né output dei tool simulato). `gas.py`, cap di 10 iterazioni e `_get_window` non sono toccati.
- `ci.yml`: il nuovo passo ha `if: always()` e `pipefail` come gli altri, e nessun `paths-ignore`.

**Riserve (da mettere in stato_progetto.md al fine-task, insieme a R-615-4 e R-615-5 che restano aperte: microfono da provare sul Mac, licenza da decidere per l'operatore)**
- **R-616-1 BASSA**: con `GAS_VOICE_PORT` nel `.env`, il server e il controllo finale di installa.sh usano quella porta. `clients/voice/ascolto.py:440` invece, se manca `GAS_VOICE_URL`, resta su `http://127.0.0.1:8765`. Risultato: installa.sh dice «tutto acceso» e poi ogni turno finisce col bip di errore. L'ho provato: con `GAS_VOICE_PORT=9001` l'URL resta `:8765`. Correzione suggerita: costruire l'URL di default da `GAS_VOICE_PORT`, oppure far controllare a installa.sh la stessa porta che usa il client.
- **R-616-2 BASSA**: `clients/voice/ascolto.py:238` conta l'attesa dopo la parola solo sui blocchi deboli. Con un rumore forte-forte-debole l'attesa dura 14,9 s invece dei 5 dichiarati (misurato: 186 blocchi). Non viene inviato niente, quindi la privacy è salva, ma il docstring di `registra` non è esatto.
- **R-616-3 COSMETICA**: alla riga 92 il LEGGIMI dice «cancellali (i servizi li ricreano)». In realtà launchd apre il file di log solo quando avvia il servizio: dopo un `rm` il processo continua a scrivere sul file cancellato, che non si ricrea e non libera spazio fino al riavvio. Meglio consigliare di svuotarlo con `: > .gas_voce/ascolto.log`.

**Rischi esplicitamente esclusi**
- Comportamento reale sul Mac non verificato perché qui non si riproduce: bash 3.2 di `/bin/bash`, sed/grep BSD, `launchctl bootstrap`/`print` veri, permesso del microfono sotto launchd, `activate` di un venv vero con `set -u`. Ho controllato solo per lettura che i costrutti usati esistano in bash 3.2 e in BSD.
- openWakeWord vero non rieseguito: era stato provato nella #615 e quella parte non è cambiata.
- Le suite voce di M2 (server/stt/tts) non le ho rilanciate: quei file non sono nel diff.

**Memoria**: riga #616 più una lezione, committate con `scripts/commit_memoria_revisore.sh` (commit cc6f953, solo `.claude/agents/memoria_revisore.md`). Il diff staged sotto review è intatto.
```

Verdetto integrale della review #618 (chat Mani), sul diff del commit locale 52c26bf:

```
## VERDETTO: APPROVATO CON RISERVE

Review #618 (chat Mani). Diff staged con sha256 c5fdc9c85c13e5b4… (l'ho ricalcolato e coincide), su voce-h24 sopra 8e69ab6. File: clients/voice/ascolto.py, scripts/voce/LEGGIMI.md, tests/test_unit_voce_ascolto.py. Letture obbligatorie fatte: CLAUDE.md (sezione 5), reports/stato_progetto.md (letto per Grep sulla sezione voce), la coda di .claude/agents/memoria_revisore.md con le review #615 e #616.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:116` — `url_del_server()`: usa GAS_VOICE_URL se c'è (senza la `/` finale), altrimenti `http://127.0.0.1:<cifre di GAS_VOICE_PORT o 8765>`. Rischio: che il client e il server leggano la porta in modi diversi. Il filtro «solo cifre» è lo stesso di scripts/voce/installa.sh:84. Il server (modules/voice/server.py:473) e il client caricano lo stesso .env. Se il valore è sporco (es. «9001 # nota»), il server non parte e il controllo finale di installa.sh si ferma, quindi niente falso «tutto acceso». Esito: ok.
- `clients/voice/ascolto.py:249` — in `registra`, prima della voce, l'attesa conta ogni blocco, anche i rumori. Quando la voce si apre si passa oltre con `continue`, come faceva il codice vecchio. Rischio: tagliare una voce vera vicino alla scadenza. L'ho provato direttamente: con voce che parte dopo 55 o 59 blocchi di silenzio la richiesta passa (22 blocchi), dopo 60 blocchi (4,8 s) no. Quindi la scadenza vera è 5 s meno l'inizio della voce (0,24 s), ed è accettabile. Il caso «riprendi a parlare dopo la risposta» non cambia, perché lì la voce è già aperta. Esito: ok.
- `clients/voice/ascolto.py:451` — `main` ora chiama `url_del_server()`. Rischio: che il collegamento non sia coperto da nessun test. Ho rimesso la vecchia espressione `GAS_VOICE_URL or 8765` e i test restano verdi (61 passed). Esito: riserva (R-618-1).
- `tests/test_unit_voce_ascolto.py:108` — test forte-forte-debole ripetuto oltre i 5 s, poi voce vera: non si invia niente. Mutante con la logica vecchia: 1 failed (riprodotto). Esito: ok.
- `tests/test_unit_voce_ascolto.py:376` — test con 3 casi su `url_del_server`. Mutante «sempre 8765»: 1 failed. Mutante senza la pulizia della `/` finale: 1 failed. Esito: ok.
- `scripts/voce/LEGGIMI.md:92` — «svuotali senza cancellarli» con `: > .gas_voce/ascolto.log`. Chiude R-616-3. Esito: ok, salvo la nota cosmetica R-618-2.

**Prove riprodotte**: 61 passed su una copia esatta dell'indice. Il diff è pulito (`git diff --cached --check`). clients/voice/ascolto.py lo importa solo il suo test, quindi nessun altro test è toccato.

**Riserve chiuse**: R-616-1, R-616-2 e R-616-3, tutte chiuse.

**Riserve nuove**
- R-618-1 BASSA — nessun test controlla che `main` usi davvero `url_del_server()` (clients/voice/ascolto.py:451). Rimettendo la vecchia espressione, il bug di R-616-1 tornerebbe con la suite verde. Basta un test su `main` con GAS_VOICE_PORT=9001 e senza GAS_VOICE_URL che legga l'URL passato a `invia_al_server` (o il log «server …»).
- R-618-2 COSMETICA — il LEGGIMI dà il comando per svuotare solo `ascolto.log`, ma anche `voce.server.log` cresce allo stesso modo. Inoltre il test di clients/voice/ascolto.py:108 riceve `monkeypatch` senza usarlo.

**Restano aperte** R-615-4 (permesso del microfono sotto launchd, da provare sul Mac) e R-615-5 (licenza dei modelli di openWakeWord, decide l'operatore).

**Cosa NON ho verificato**
- Il funzionamento vero sul Mac (launchd, microfono, afplay, porta diversa da 8765 col server vero acceso): non si può riprodurre su Linux.
- Le suite del server voce, dell'STT e del TTS: le ho lanciate ma non hanno finito entro i 110 s. Il diff non le tocca, perché il modulo modificato lo importa solo il suo test.

**Memoria**: aggiunte la riga contatore #618 e una lezione (dopo aver estratto una funzione, provare anche il mutante che lascia il chiamante sulla vecchia espressione). Committate da sole con scripts/commit_memoria_revisore.sh (commit 158a61d). Il diff staged sotto review non è stato toccato (sempre 3 file).
```

Verdetto integrale della review #621 (chat Mani), sul diff finale del commit 234f41c su main:

```
## VERDETTO: APPROVATO CON RISERVE

Review #621 (chat Mani): R8 voce H24 portata su main. Diff staged: sha256 63b0523b90b704c1, che corrisponde a quello dichiarato e non è cambiato dopo il commit della memoria. Base ceaa4aa.

Letture fatte: CLAUDE.md (sez. 5, 8, 9, 10), reports/stato_progetto.md (le parti sulla voce), la memoria del revisore. In questo branch la memoria non contiene le righe #615, #616 e #618: le ho lette nella copia del commit 52c26bf.

**Elementi esaminati**
- `clients/voice/ascolto.py:451` — `main` prende l'URL da `url_del_server()` (`clients/voice/ascolto.py:116`). Rischio: che il collegamento che chiude R-616-1 non sia fissato da nessun test (era R-618-1). Esito: ok. Il mutante con la vecchia espressione (`GAS_VOICE_URL or "http://127.0.0.1:8765"`) dà 1 failed su 62, cioè `test_main_usa_la_porta_del_server`.
- `tests/test_unit_voce_ascolto.py:386` — il test nuovo. Rilevatore, invio e Microfono sono finti, `_GAS_ROOT` punta a tmp_path (quindi nessun .env vero), e pretende `["http://127.0.0.1:9001"]`. Rischi: che dipenda dall'ambiente della shell e che tocchi hardware o rete. Esito: ok. Resta verde anche con `GAS_VOICE_URL=http://example.com GAS_VOICE_PORT=1` esportati, perché delenv e setenv li coprono. Non apre il microfono: KeyboardInterrupt fa `return 0` e `mic` resta None. Il parametro monkeypatch inutilizzato è stato tolto dalla riga `tests/test_unit_voce_ascolto.py:108`, quindi R-618-2 è chiusa per la parte del test.
- `.github/workflows/ci.yml:128` — passo «voce H24» subito dopo il passo voce di main, che ha già `test_unit_voice_contesto.py`. Rischio: un'unione che perda o raddoppi passi di main. Esito: ok. Il diff verso main è di sole +8 righe, lo YAML si carica e il passo avvisa_operatore di main è intatto. Il test usa solo la libreria standard (numpy si importa solo dentro il rilevatore vero), quindi in CI non mancano dipendenze.
- `.gitignore:23` — `.gas_voce/`. Esito: ok, `git check-ignore -v` sui log lo conferma.
- `scripts/voce/LEGGIMI.md:93` — dice di svuotare anche `voce.server.log`. Esito: ok, R-618-2 chiusa.
- Confronto completo con 52c26bf: `ascolto.py`, i due plist, `installa.sh`, `spegni.sh` e `requirements-ascolto.txt` sono identici byte per byte. Le uniche differenze sono le novità dichiarate e il contenuto già presente in main.
- Antipattern: il diff non tocca gas.py, brains/ né la history, quindi niente slicing né output dei tool simulati.

**Prove riprodotte** (su una copia dell'indice): `tests/test_unit_voce_ascolto.py` → 62 passed.

**Riserve**
- R-621-1 BASSA (processo): le righe #615, #616 e #618 vanno ancora riportate nella memoria, come avete previsto. Finiranno dopo la #621, fuori dall'ordine dei numeri; va bene, ma va fatto prima di chiudere la fetta.
- Restano aperte, e vanno in stato_progetto.md:
  - R-615-4 MEDIA: permesso del microfono sotto launchd, da provare sul Mac.
  - R-615-5 BASSA: licenza CC BY-NC-SA di hey_jarvis, decide l'operatore.

**Rischio escluso**: non ho rieseguito `installa.sh` coi comandi finti, né il resto della CI (suite kernel, voice server/stt/tts/contesto, avvisa_operatore). Quei file sono identici a quelli già provati in #616 e #618, o sono quelli di main senza modifiche. Il comportamento vero sul Mac (launchd, permesso del microfono, openWakeWord con audio reale) non è verificabile qui.

Il merge spetta all'operatore perché la PR tocca ci.yml.

Memoria: riga #621 aggiunta in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e committata da sola (31b8ec1).
```

Commit 7de4eeb (clients/voice/ascolto.py, scripts/voce/installa.sh, tests/test_unit_voce_ascolto.py: V-1/V-2/V-3 bot su c5e7321). Verdetto integrale della review #622 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #622 (chat Mani). Diff staged (sha256 e95595c8f16e9dad, ricontrollato dopo il commit della memoria e invariato) su claude/peaceful-lovelace-0w2b7q, base c5e7321, PR #323. Prima della review ho letto CLAUDE.md (sez. 5, 8, 9, 10), le voci R8 e voce H24 di reports/stato_progetto.md e la memoria del revisore (#615-#621 e lezioni).

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:85` — `_carica_dotenv` importa `gas._carica_dotenv` e gli passa `root/.env`. Se l'import fallisce, ripiega e scrive un warning con il solo nome dell'eccezione (§9).
  - Rischio esaminato: effetti collaterali dell'import di gas.py nel processo che resta acceso sempre.
  - Prova: ho importato davvero gas dal client in un processo pulito. Ci mette 0,5 s. Il `logging.basicConfig` di gas.py non ha effetto, perché `main` configura il logging prima (clients/voice/ascolto.py:469): il livello resta INFO, l'handler resta lo StreamHandler e il logger gas.ascolto resta a 20. Il token letto è 'abc' e l'URL è http://127.0.0.1:9001.
  - Esito: ok.
- `clients/voice/ascolto.py:102` — il ripiego ora gestisce il commento in linea, le virgolette seguite da commento (stessa regex di `_DOTENV_VIRGOLETTE` a gas.py:605), il BOM e GAS_NO_DOTENV. Vince la prima riga, come in gas.
  - Rischio esaminato: il ripiego dà valori diversi dal server.
  - Ho fatto tre mutanti: parser vecchio, senza GAS_NO_DOTENV, utf-8 senza BOM. Ognuno dà 1 failed.
  - Esito: ok. Resta una differenza minore: con virgolette non chiuse gas scarta la riga, il ripiego tiene il valore. Non la rilevo come finding.
- `clients/voice/ascolto.py:312` — `_svuota()` dopo il bip di errore. Il test è a tests/test_unit_voce_ascolto.py:179 (`svuotati == 2`).
  - Mutante senza svuotamento: 1 failed.
  - Esito: ok.
- `scripts/voce/installa.sh:85` — legge la porta con `head -1` invece di `tail -1`.
  - Mutante `tail -1`: 1 failed (tests/test_unit_voce_ascolto.py:577).
  - Esito: riserva (R-622-1).
- `scripts/voce/installa.sh:88` — AVVISO se nel .env c'è GAS_VOICE_URL.
  - Rischio esaminato: `set -e` con grep che non trova la riga. È dentro un `if`, quindi non ferma lo script, e il .env esiste di sicuro (lo garantisce lo STOP a scripts/voce/installa.sh:30).
  - Mutante senza AVVISO: 1 failed.
  - Esito: riserva cosmetica (R-622-2).
- `tests/test_unit_voce_ascolto.py:431` — test parametrizzato con gas e col ripiego; `_senza_gas` (tests/test_unit_voce_ascolto.py:418) rende l'import di gas impossibile. Il mutante «ImportError sempre» dà 1 failed.
  - Esito: ok.

**Prove**: su un export dell'indice 69 passed. Tutti i 7 mutanti danno 1 failed ciascuno; ripristinato il codice, di nuovo 69 passed.

**Finding**
- **R-622-1 BASSA**: con `GAS_VOICE_PORT=9001 # era 8765` client e server usano 9001, ma installa.sh (`scripts/voce/installa.sh:85`) toglie i caratteri non numerici e fonde le cifre del commento: «90018765». Risultato: falso STOP «il server voce non risponde». È fail-closed, non un falso «tutto acceso», ma è la stessa disparità di V-2 rimasta nello script shell. Correzione: togliere ` #…` prima di `s/[^0-9]//g`, ad esempio `sed 's/[[:space:]]#.*//; s/.*=//; s/[^0-9]//g'`, e aggiungere un test.
- **R-622-2 COSMETICA**: l'AVVISO compare anche con `GAS_VOICE_URL=""` o `GAS_VOICE_URL= # vuoto`, perché `.+` li accetta. In quei casi il client usa comunque il Mac, quindi l'avviso è sbagliato ma innocuo.
- **R-622-3 COSMETICA**: `clients/voice/ascolto.py:92` aggiunge la cartella a `sys.path` e non la toglie più. In produzione è la root di Gas, quindi va bene. Nei test invece ogni `tmp_path` resta in `sys.path` per il resto della suite: meglio `monkeypatch.syspath_prepend` nei test, oppure togliere la voce dopo l'import.

Restano aperte R-615-4 MEDIA (permesso del microfono sotto launchd, da provare sul Mac) e R-615-5 BASSA (licenza dei modelli hey_jarvis, decide l'operatore).

**Rischio escluso**: non ho verificato l'avvio reale sotto launchd su macOS (permesso del microfono, venv del Mac con requirements.txt completo), perché in dev non si riproduce. Il ramo «gas importabile» l'ho provato solo in Linux, dove fastembed manca e stampa due warning all'avvio. Nemmeno l'effetto di un handle in più su gas_debug.log, aperto dal client che resta acceso sempre, è verificato sul Mac.

Memoria: riga #622 e una lezione nuova aggiunte in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, committate da sole (4fc2378). La lezione: quando si allinea il parser del client a quello del server, ricontrollare anche gli script shell che rileggono la stessa chiave con grep e sed.
```

Commit successivo a 57f12dc (scripts/voce/installa.sh, scripts/voce/LEGGIMI.md, clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py: V-3/V-4 ve su c5e7321 e R-622-1). Verdetto integrale della review #623 (chat Mani):

```
## VERDETTO: APPROVATO CON RISERVE

Review #623 (chat Mani). Ho esaminato il diff staged su claude/peaceful-lovelace-0w2b7q, sopra 1127f5c. Lo sha256 inizia per 2bad1f4ebc9780b3 ed è lo stesso prima e dopo il commit della memoria. Ho fatto le tre letture obbligatorie: CLAUDE.md (sez. 5, 8, 9), reports/stato_progetto.md (in modo mirato) e la memoria del revisore.

**Elementi del diff esaminati**
- `scripts/voce/installa.sh:43` — controlla che il Python del .venv sia almeno 3.11 prima di pip. Rischi esaminati: che `set -e` scatti sulla sostituzione `$(python --version)` dentro l'argomento di stop (non scatta) e che lo snippet funzioni con un Python vero (rc=0 su 3.13). Il mutante senza controllo dà 1 FAIL. Esito: ok.
- `scripts/voce/installa.sh:89` — il sed toglie ` #…` prima di tenere le cifre. Ho provato «9001 # era 8765», il commento dopo un tab, `"9001" # 8765` e `export … 9001   #x 1`: danno tutti 9001. È equivalente allo split `\s+#` di `gas._carica_dotenv` (gas.py:653). Il mutante col sed vecchio dà 1 FAIL. Esito: ok.
- `scripts/voce/installa.sh:92-97` — la porta viene riprovata fino a 30 volte con `sleep 1`, poi STOP. Il mutante con `seq 1 5` dà 1 FAIL. Esito: ok.
- `scripts/voce/installa.sh:99-105` — dopo l'attesa ricontrolla che i servizi siano ancora accesi. Rischio: nessun test fissa questo controllo. Esito: riserva R-623-1.
- `tests/test_unit_voce_ascolto.py:519` — il finto nc conta i tentativi in `$REGISTRO.nc`. Ho verificato la logica: con NC_FALLISCE=3 fa 4 tentativi, con 999 ne fa 30. Le asserzioni sulla porta ora confrontano riga per riga (`registro.splitlines()`), quindi «90018765» non passa più. Esito: ok.
- `scripts/voce/LEGGIMI.md:71-74` e `clients/voice/ascolto.py:23` — il testo ora dice che voce.server.log va trattato come privato. È corretto: gas.py:48 ha uno StreamHandler sullo stderr, e il plist manda stderr in voce.server.log. Esito: ok.

**Prove**: 73 passed su un export dell'indice (scratchpad r623). Nel diff non c'è slicing della history. Il diff non tocca il codice dei provider, il cap di 10 iterazioni né `_get_window`.

**Riserve**
- R-623-1 BASSA: il ricontrollo dopo l'attesa (scripts/voce/installa.sh:99-105) non è fissato da nessun test. Ho provato due mutanti: tolgo il blocco, oppure cambio `stop` in `echo`. Con entrambi la suite dà 18 passed su 18, perché il finto launchctl risponde sempre «running». Serve un finto che alla seconda chiamata di `print` risponda in un altro modo.
- R-623-2 COSMETICA: il finto `sleep` non scrive nel registro, quindi il mutante senza `sleep 1` nel giro sopravvive. Sul Mac quel giro farebbe 30 tentativi di nc in meno di un secondo e darebbe un falso STOP. Basta far registrare anche il finto sleep e contare le chiamate.
- R-623-3 COSMETICA: il messaggio dice «cancella .venv e riprova», ma lo script ricrea .venv con il `python3` del PATH. Sul Mac `/usr/bin/python3` è 3.9, quindi l'operatore ricadrebbe nello stesso STOP. Il messaggio dovrebbe dire di mettere prima nel PATH un python3 3.11 o più recente.
- Restano aperte R-615-4 MEDIA (microfono sotto launchd, da provare sul Mac) e R-615-5 BASSA (licenza di hey_jarvis, decide l'operatore).

**Rischi esplicitamente esclusi (non verificati)**
- Il comportamento reale su macOS non è verificato: launchd, `nc -z` senza timeout e il tempo di avvio del server non sono riproducibili in un ambiente Linux. I test usano comandi finti.
- Non ho provato la suite con `pytest -s` da un terminale vero. Il finto python fa `cat > /dev/null` sullo stdin ereditato e senza la cattura di pytest potrebbe restare in attesa. Il problema c'era già prima di questo diff, che lo estende solo al ramo `--version`.
- Divergenza fuori dal diff: se il valore è tra virgolette e contiene ` #` (es. `GAS_VOICE_PORT="9001 # x"`), installa.sh legge 9001 mentre il server va in errore. Il caso è raro e il server lo segnala da solo.

**Memoria**: ho aggiunto la riga #623 e una lezione in /home/user/Gas/.claude/agents/memoria_revisore.md. La lezione: quando il test usa uno `sleep` finto muto, o un ricontrollo con un finto che risponde sempre uguale, i mutanti che li tolgono sopravvivono. La memoria è committata a parte in 57f12dc con `scripts/commit_memoria_revisore.sh`, e l'indice del diff sotto review è rimasto intatto.
```

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py, brains/ o modules/. Test nuovi: `tests/test_unit_voce_ascolto.py` (`python -m pytest tests/test_unit_voce_ascolto.py`, da root): 73 passed. Con le suite voce di M2 (server/stt/tts), prima delle ultime correzioni: 181 passed. Mutanti presi (1 failed o più ciascuno): soglia ignorata, niente svuotamento dopo la risposta, file temporaneo non cancellato, http remoto accettato, massimo dei turni ignorato, silenzio prima della voce incluso, file 0644, senza `_NienteRedirect`, senza `ProxyHandler({})`, blocchi forti non di fila, attesa sulla logica vecchia, URL sempre 8765, `main` con la vecchia espressione, caricatore di gas mai usato, niente svuotamento dopo un errore, niente controllo di Python, niente attesa del server, sed della porta senza togliere il commento; per gli script: `grep` senza `|| true` (installa fermo dopo «5/6», riprodotto sul codice vecchio), lista bianca `.*`.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 31b8ec1 (memoria #621), 234f41c (fetta 37), 5876b7e (memoria #615/#616/#618): pushati insieme prima dell'apertura della PR #323. Run non ancora disponibile alla scrittura dell’handoff.
- c5e7321 (fine-task): run 41485162729 su c5e7321 (unit-suite e handoff-check: vedi la PR); verifica-bot neutral (bot APPROVATO CON RISERVE).
- 4fc2378 (memoria #622), 7de4eeb (correzioni), 1127f5c (fine-task): run 41486699260 su 1127f5c (vedi la PR); verifica-bot neutral (bot APPROVATO CON RISERVE).
- 57f12dc (memoria #623), il commit delle correzioni e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-615-4 (chat Mani) MEDIA: permesso del microfono sotto launchd, da provare sul Mac; la voce H24 non è dichiarata funzionante prima.
- R-615-5 (chat Mani) BASSA: licenza CC BY-NC-SA dei modelli pronti di openWakeWord, decide l'operatore.
- R-623-1 (chat Mani) BASSA: il ricontrollo dei servizi dopo l'attesa non ha un test (il finto launchctl risponde sempre «running»).
- R-623-2 (chat Mani) COSMETICA: finto sleep muto. R-623-3 (chat Mani) COSMETICA: il messaggio sul Python vecchio non dice di mettere un python3 ≥ 3.11 nel PATH.
- R-622-2 (chat Mani) COSMETICA: AVVISO anche con GAS_VOICE_URL vuoto. R-622-3 (chat Mani) COSMETICA: la root resta in sys.path.
- V-2 COSMETICA del bot su c5e7321: il passo CI nuovo non compare nel «Job summary».
- Log in `.gas_voce/` senza rotazione (dichiarato nel LEGGIMI).
- Da #319 (mergiata): V-1 bot su 9c44686 BASSA (limite dichiarato), V-1/V-2 ve su 9c44686 COSMETICHE, R-612-1/2, R-614-1/2, R-617-1/2/3, V-2 bot, V-5 ve.
