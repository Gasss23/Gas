# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — chat Mani: ascolto più severo di default, misure per tarare, diagnosi delle attivazioni (PR #371)

---

## §0 DECISIONI UMANE RICHIESTE

1. **Togliere `GAS_ASCOLTO_SOGLIA=0.6` dal `.env` del Mac prima della prova** (V-1 bot #371 su 5b27586): il .env vince sul predefinito 0,7. Al riavvio il log scrive «regolazioni in uso» e avvisa.
2. Merge della PR #371 (https://github.com/Gasss23/Gas/pull/371): riserve BASSE/COSMETICHE, serve il sì dell'operatore (CLAUDE.md §10); riallineare a main subito prima se è avanzato.
3. Licenza di «hey_jarvis» (CC BY-NC-SA, non commerciale) e verifica del parlante: `reports/proposta_verifica_parlante.md`.

---

## §1 SCOPE & ESITO FETTE

- **Default più severi (priorità ALTA dell'operatore)**: `FATTA` — 84481ea, review #757-M1 (R-757-1-M1 MEDIA chiusa) e #758-M1 APPROVATO.
- **V-1 MEDIA bot #371 su b9ad6e7 (interruzione su un solo blocco)**: `FATTA` — b36c944, review #759-M1 APPROVATO CON RISERVE.
- **V-2 MEDIA bot #371 (conflitto dopo #369)**: `FATTA` — 881c4bb, review #760-M1 APPROVATO.
- **Misure per tarare e diagnosi delle attivazioni (richiesta di M1)**: `FATTA` — df3e650, review #761-M1 (R-761-1/2 chiuse) e #762-M1 APPROVATO.
- **V-1 MEDIA bot #371 su 5b27586 (.env del Mac con soglia 0.6)**: `FATTA` — 4db776c, review #763-M1 APPROVATO CON RISERVE (solo COSMETICHE).
- **Conflitto dopo #370**: `FATTA` — 175289c, review #764-M1 APPROVATO.
- **Proposta verifica del parlante**: `FATTA` come documento in reports/.
- **Difesa adattiva da eco/TV**: `DEFERITA — prima i dati delle nuove misure dal Mac`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md    |  10 +++++++++
 clients/voice/ascolto.py              | 160 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------------------------
 reports/diff_sessione.md              |  17 ++++++++-------
 reports/handoff.md                    | n/d
 reports/proposta_verifica_parlante.md |  71 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md             |   4 +++-
 reports/ultimo_report.md              |  26 +++++++++++++----------
 scripts/voce/LEGGIMI.md               |  51 ++++++++++++++++++++++++++++++++-------------
 scripts/voce/diagnosi_ascolto.py      | 165 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_voce_ascolto.py       | 244 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
175289c merge: origin/main (PR #370) in claude/peaceful-lovelace-0w2b7q — conflitti solo nei report, review #764-M1
4db776c fix(voce): all'avvio il log dice le regolazioni in uso e avvisa se il .env rende la parola più facile — V-1 bot #371 su 5b27586, review #763-M1
9b148c5 chore(revisore): memoria review #763 — APPROVATO CON RISERVE
df3e650 feat(voce): misure per tarare l'ascolto e comando di diagnosi delle attivazioni — review #761-M1/#762-M1
5bdead4 chore(revisore): memoria review #762 — APPROVATO
bd5a717 chore(revisore): memoria review #761 — APPROVATO CON RISERVE
8de3ae0 chore(revisore): memoria review #761 — APPROVATO CON RISERVE
5b27586 docs(fine-task): V-1/V-2 del bot #371 chiuse, merge di main dopo la #369 — PR #371
881c4bb merge: origin/main (PR #369) in claude/peaceful-lovelace-0w2b7q — conflitti solo nei report, review #760-M1
b36c944 fix(voce): anche l'interruzione vuole la parola su più blocchi di fila — V-1 bot #371, review #759-M1
a164dc8 chore(revisore): memoria review #759 — APPROVATO CON RISERVE
b9ad6e7 docs(fine-task): ascolto più severo di default — PR #371
84481ea fix(voce): ascolto più severo di default — zero risposte non richieste — review #757-M1/#758-M1
1aa50f0 chore(revisore): memoria review #758 — APPROVATO
e1d46fa chore(revisore): memoria review #757 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 84481ea: verdetti integrali delle review #757-M1 e #758-M1.

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md, la voce di stato_progetto.md sull'ascolto H24 (riga 694) e la coda di memoria_revisore.md. Il diff non tocca kernel, provider, `_get_window` o il cap di 10 iterazioni. Non c'è slicing della history e non c'è simulazione di tool.

**Elementi esaminati**
- clients/voice/ascolto.py:118 — `MAX_TURNI_PREDEFINITO = 1`. Rischio controllato: che la finestra si apra comunque. **Esito: ok.** In `conversazione` il controllo `turni >= self.max_turni` (clients/voice/ascolto.py:844) fa `break` prima di `aspetta_voce` (clients/voice/ascolto.py:850). Lo conferma anche il nuovo test `test_col_predefinito_di_main_niente_turni_di_seguito`.
- clients/voice/ascolto.py:836 — il ramo dell'interruzione con la parola, con max_turni=1. Rischio controllato: l'interruzione resta utilizzabile? **Esito: riserva MEDIA (R-757-1-M1).** L'ho provato con lo stesso scenario di `test_la_parola_interrompe_gas_e_apre_una_nuova_richiesta`:
  - con max_turni=3: suona A poi C, 2 invii, due bip;
  - con max_turni=1: suona solo A, 1 invio, un bip.
  Quindi «Hey Jarvis» detto mentre Gas parla lo ferma, ma la nuova domanda non viene registrata e non c'è il bip: va ripetuta la parola una seconda volta. scripts/voce/LEGGIMI.md:47 promette invece «fa il bip e ascolta la nuova domanda». Va contro l'obiettivo «zero risposte non richieste»? No, è più prudente. Però una funzione documentata (fetta 41) si spegne in silenzio. Due rimedi possibili, a scelta vostra o dell'operatore:
  1. dare all'interruzione un tetto suo, per esempio permettere almeno 1 interruzione anche con max_turni=1, tenendo il tetto di R-668-1 contro l'eco;
  2. documentare nel LEGGIMI che, con il default, interrompere = solo «fermati».
  Nessun test copre interruzione + max_turni=1: aggiungerne uno.
- clients/voice/ascolto.py:125-126 — soglia 0,7 e 3 blocchi di fila. Rischio: la parola vera non scatta più (R-736-1). **Esito: ok.** Il rimedio è scritto sia nel commento (clients/voice/ascolto.py:123-124) sia nel LEGGIMI (scripts/voce/LEGGIMI.md:129-131: `GAS_ASCOLTO_SOGLIA=0.6` / `GAS_ASCOLTO_BLOCCHI_PAROLA=2`). La tabella è verificata dai nuovi test.
- clients/voice/ascolto.py:346-349 — il costruttore ora ha default letterali (15 / 3 / 0,7). Rischio: qualcuno usa ancora i default del costruttore. **Esito: ok.** L'unico `Ascolto(` fuori dai test è in main (clients/voice/ascolto.py:1235), che passa sempre soglia, blocchi_parola, finestra_s, max_turni e soglia_interruzione. `MAX_TURNI_PREDEFINITO`, `FINESTRA_PREDEFINITA_S` e `SOGLIA_INTERRUZIONE_PREDEFINITA` non compaiono in nessun altro file .py.
- clients/voice/ascolto.py:154 — interruzione a 0,8, sopra la soglia normale di 0,7. **Esito: ok**, c'è anche un assert nel test di main.

**Riserve BASSE**
- scripts/voce/LEGGIMI.md:50 dice ancora «soglia 0.7 invece di 0.5»: ora è 0.8 contro 0.7.
- I commenti a clients/voice/ascolto.py:153 («quella normale (0.5)») e clients/voice/ascolto.py:846 («soglia 0,7 … 0,6») sono rimasti con i valori vecchi.
- Il test si chiama `test_finestra_di_15_secondi` ma verifica `FINESTRA_PREDEFINITA_S == 10.0`. Il nome è difendibile, perché la prova usa i 15 s del costruttore, ma confonde.

**Cosa NON ho verificato**
- Il comportamento dal vivo sul Mac (falsi positivi e mancate attivazioni con 0,7 e 3 blocchi): non si può riprodurre senza microfono e openWakeWord. Va provato dall'operatore col nuovo log.
- browser_server.py: non è toccato, quindi non l'ho esaminato.
- La suite completa del motore: ho rilanciato solo tests/test_unit_voce_ascolto.py (315 passed).

Memoria: riga #757-M1 e una lezione aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, committate con lo script (e1d46fa). La lezione: quando si abbassa a 1 un tetto condiviso come max_turni, va provato ogni ramo che lo usa.

## VERDETTO: APPROVATO

Re-review #758-M1: approvato. La riserva MEDIA della #757 è risolta e le riserve BASSE pure. 317 test passano.

**Elementi esaminati**
- clients/voice/ascolto.py:157 — la nuova costante `TURNI_CON_INTERRUZIONE = 2`, col commento che la lega a R-757-1-M1. Rischio controllato: che allarghi i turni di seguito senza parola. **Esito: ok.** Si usa solo nel ramo dell'interruzione.
- clients/voice/ascolto.py:842 — il tetto `max(self.max_turni, TURNI_CON_INTERRUZIONE)` nel ramo `if self.interrotto`. **Esito: ok.**
  - Rischio 1, che dopo la domanda nata da un'interruzione si apra la finestra con i seguiti spenti. Il controllo di clients/voice/ascolto.py:850 usa ancora `self.max_turni` puro. Al secondo turno turni=2 ≥ 1, quindi `break` prima di `aspetta_voce`.
  - Prova fatta: parola, interruzione con nuova domanda, poi voce senza parola, con finestra 10 e max_turni=1. Risultato: si sentono A e B, 2 invii, la voce che segue NON viene inviata.
  - Rischio 2, cioè R-668-1 (la voce di Gas che si interrompe da sola all'infinito). Resta limitato: la seconda interruzione chiude la conversazione. Lo verifica `test_coi_seguiti_spenti_la_seconda_interruzione_chiude` (tests/test_unit_voce_ascolto.py:2763).
  - Con max_turni ≥ 2 il comportamento non cambia, perché il max vale quanto max_turni.
- tests/test_unit_voce_ascolto.py:2752 — `test_coi_seguiti_spenti_l_interruzione_apre_ancora_la_nuova_domanda`. Copre esattamente il caso che la sonda della #757 aveva trovato rotto. **Esito: ok.** I mutanti dichiarati («tetto = max_turni» e «tetto 9») fanno fallire un test ciascuno, coerente con i due test nuovi.
- scripts/voce/LEGGIMI.md:51 — ora dice «0.8 invece di 0.7» e spiega l'interruzione coi seguiti spenti: la prima apre la nuova domanda, la seconda ferma Gas. **Esito: ok**, coerente col codice. Anche le altre BASSE della #757 sono chiuse (commenti con i numeri vecchi, nome del test sulla finestra).

**Cosa NON ho verificato**
- Il comportamento dal vivo sul Mac: se 0,8 durante la risposta di Gas sente ancora la parola vera e se 0,7 con 3 blocchi riduce davvero le attivazioni per sbaglio. Senza microfono e openWakeWord non si può riprodurre: va provato dall'operatore col log.
- La suite completa del motore: ho rilanciato solo tests/test_unit_voce_ascolto.py (317 passed).

Memoria: riga #758-M1 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script (1aa50f0).

Commit b36c944: verdetto integrale della review #759-M1.

## VERDETTO: APPROVATO CON RISERVE

Review #759-M1: diff staged sul branch claude/peaceful-lovelace-0w2b7q (PR #371). Corregge la V-1 MEDIA del bot: un solo picco forte non basta più a fermare Gas mentre parla.

**Cosa ho controllato nel diff**
- `clients/voice/ascolto.py:735` — Il conteggio `sopra` sale solo con blocchi di fila sopra `soglia_interruzione`. Gas si ferma quando `sopra >= self.blocchi_parola` e il conto si azzera appena un blocco scende sotto soglia (riga 740). Rischio cercato: un comportamento diverso dal ciclo della parola normale, cioè quello in cui Gas aspetta senza parlare (clients/voice/ascolto.py:434-439). Esito: ok, la logica è la stessa. `blocchi_parola` vale almeno 1 grazie a clients/voice/ascolto.py:372, quindi il conto non può restare bloccato per sempre.
- `clients/voice/ascolto.py:730` — Il conto si azzera anche quando il rilevatore va in errore. Rischio cercato: due blocchi forti separati da un errore contati come «di fila». Esito: ok. Ho provato a togliere l'azzeramento (mutante): `test_errore_del_rilevatore_mentre_gas_parla_azzera_il_conto` fallisce (1 failed). Il file è stato poi ripristinato.
- `clients/voice/ascolto.py:724` — Con `interrompibile=False` (la conferma, chiamata a clients/voice/ascolto.py:787) e con PAROLA_NEL_TESTO (riga 661) si salta via con `continue` prima di leggere il rilevatore. Il conto non viene toccato, quindi lì non cambia nulla. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2773` — Il test con `blocchi_parola=3` copre tre casi: un picco isolato, due picchi non di fila, tre di fila che interrompono. Il test dell'errore sta a riga 2789. Esito: ok. Risultato: 319 passed, confermato.
- `scripts/voce/LEGGIMI.md:51` e `:131-134` — L'interruzione ora dice «per `GAS_ASCOLTO_BLOCCHI_PAROLA` blocchi di fila» e i due rimedi opposti sono in due voci separate (V-2 della verifica esterna). Esito: ok.

**Riserve**
- **R-759-1-M1 (BASSA)** — `sopra` riparte da zero a ogni chiamata, cioè a ogni frase. Se l'operatore dice la parola a cavallo fra due frasi, il conto ricomincia. Al bordo questo dà più ritardo o un'interruzione che non scatta.
- **Latenza non documentata** — Con 3 blocchi Gas si ferma circa 160 ms dopo rispetto a un blocco solo: sono 2 blocchi in più da 80 ms. Il brief dice 240 ms, ma quello è il tempo totale dei 3 blocchi. Il LEGGIMI non lo dice; è una nota, non un blocco.

**Cosa non ho verificato**
- Il comportamento reale con microfono e casse del Mac: non si può riprodurre qui in dev. Resta da capire se 3 blocchi sopra 0,8 sulla voce vera dell'operatore scattano in modo affidabile.
- Il merge con origin/main che farai dopo: è fuori da questo diff e va rivisto se tocca il motore.

Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. Le eccezioni restano intercettate e loggate.

Memoria: riga #759-M1 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script dedicato (commit a164dc8). L'index staged non è stato toccato.

Commit 881c4bb (merge di origin/main 51b7d20): verdetto integrale della review #760-M1.

## VERDETTO: APPROVATO

Review #760-M1. È il merge di origin/main 51b7d20 (PR #369 di M2) nel branch claude/peaceful-lovelace-0w2b7q. Il merge è in corso e le modifiche sono in staging. Prima della review ho letto CLAUDE.md §5, reports/stato_progetto.md (in testa) e la coda della memoria del revisore.

Elementi esaminati:
- `clients/voice/ascolto.py:735` — conta i blocchi di fila sopra `soglia_interruzione` e restituisce True quando arrivano a `blocchi_parola`. Rischio: che il merge abbia alterato la fetta V-1 bot #371. Il file staged è identico a HEAD (`git diff --cached HEAD --quiet`). Esito: ok.
- `clients/voice/ascolto.py:730` — azzera `sopra` quando il rilevatore va in errore (§9). Rischio: regressione dovuta al merge. Il file è identico a HEAD. Esito: ok.
- `clients/voice/ascolto.py:981` — `invia_al_server`. Rischio: il filtro allucinazioni di M2 cambia il contratto del server (su allucinazione risponde silenzio o «fine»). Ho controllato: le nostre modifiche rispetto alla base 904d9d6 non toccano questa funzione né la lettura di X-Gas-Comando (`clients/voice/ascolto.py:973`). Il comando «fine» era già in COMANDI (`clients/voice/ascolto.py:137`). `clients/voice/ascolto.py` non importa `modules.voice`, quindi il filtro di M2 non tocca l'ascolto. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2533` — test «errore del rilevatore azzera i blocchi di fila». Il file è identico a HEAD. Ho lanciato test_unit_voce_ascolto + test_unit_voice_stt: 459 passed, come avevi indicato. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2520` — test «parola valida solo con due blocchi di fila». È presente e passa. Esito: ok.
- Contesto: `modules/voice/stt.py`, `modules/voice/server.py`, `tests/test_unit_voice_stt.py` e `reports/ripartenza_m2.md` sono identici a MERGE_HEAD (`git diff --cached MERGE_HEAD --quiet`). Esito: ok.

Controlli sul merge:
- `ls-files -u` è vuoto.
- Nessun marcatore di conflitto nel diff staged, in stato_progetto.md o in memoria_revisore.md.
- memoria_revisore.md è un'unione: +4/-0 rispetto a main e +4/-0 rispetto a HEAD. Sono presenti sia #757–#759-M1 sia #761–#763-M2, senza doppioni.
- handoff.md, ultimo_report.md, diff_sessione.md e scripts/voce/LEGGIMI.md sono identici a HEAD.
- stato_progetto.md: l'auto-merge ha aggiunto solo la voce «Allucinazioni di Whisper» (da main) e la voce R8 della PR #371 (nostra).
- Rispetto a main restano solo clients/voice/ascolto.py e tests/test_unit_voce_ascolto.py tra i file in modules/tests/clients.
- Nessuno slicing della history e nessuna simulazione di tool. Il motore (gas.py, brains) non è toccato.

Cosa non ho verificato:
- Il comportamento dal vivo sul Mac (microfono, Whisper reale): non è riproducibile qui.
- La suite completa (server voce, Telegram): ho lanciato solo ascolto + stt. I file di M2 sono byte-identici a main, dove li ha già revisionati la review #763-M2.

Memoria: ho aggiunto la riga #760-M1 in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho messa in staging con `git add` (+5/-0 rispetto a HEAD). Come richiesto, non ho lanciato commit_memoria_revisore.sh perché il merge è in corso. Nessuna lezione nuova.

Commit df3e650: verdetti integrali delle review #761-M1 e #762-M1.

## VERDETTO: APPROVATO CON RISERVE

Review #761-M1 sul diff in staging (`git diff --cached`) di claude/peaceful-lovelace-0w2b7q, sopra la PR #371. Prima della review ho letto CLAUDE.md, reports/stato_progetto.md (le parti sulla voce) e la mia memoria. Il diff tocca 4 file, con 303 righe aggiunte e 8 tolte. Ho lanciato la suite dei test dell'ascolto: 324 passed.

**Elementi del diff esaminati**
- clients/voice/ascolto.py:432 — se il rilevatore va in errore durante una corsa sopra soglia, la conta in `picchi_scartati` e poi azzera `sopra` e `massimo`. Rischio esaminato: conteggio doppio o stato sporco tra una chiamata e l'altra. `picchi_scartati` si azzera all'inizio di ogni `aspetta_parola`, e un errore senza corsa in atto non conta niente. Esito: ok.
- clients/voice/ascolto.py:454 — stessa conta quando un blocco scende sotto soglia. clients/voice/ascolto.py:450 salva il massimo della corsa solo quando la parola scatta. Rischio esaminato: punteggio vecchio nel log o interazione con la finestra e con l'interruzione. `conversazione()` parte solo dal ciclo `while self.aspetta_parola()` di clients/voice/ascolto.py:914, quindi il valore nel log è sempre quello appena misurato. La finestra e l'interruzione non toccano questi campi, e i loro messaggi («… nella finestra: richiesta normale», «interrotto: parola di attivazione…») non hanno il formato che il parser riconosce come nuova attivazione. Esito: ok.
- clients/voice/ascolto.py:858 — il volume medio dei blocchi forti, scritto nel log come multiplo di `voce_rms`, con protezione da divisione per zero. Rischio esaminato: privacy. Nel log finiscono solo durata, secondi e rapporti, niente audio, testo o valori grezzi. Esito: ok.
- scripts/voce/diagnosi_ascolto.py:35 — la regex `_RIGA` è allineata al basicConfig di clients/voice/ascolto.py:1242 (`%(asctime)s %(levelname)s %(message)s`). L'ho provata con un log costruito apposta: una riga httpx «HTTP Request», una riga «Traceback» senza data, un «punteggio nan» e il formato vecchio senza punteggio. Le prime tre vengono saltate senza errori, il formato vecchio viene letto con «punteggio —». Con il file mancante esce con codice 1. Le regex dei numeri `[\d.]+` sono coerenti con `%.1f`/`%.2f`, che usano sempre il punto e non dipendono dalla lingua. Esito: ok.
- scripts/voce/diagnosi_ascolto.py:55 — classificazione. La prima «richiesta registrata» dopo la parola è sempre quella diretta, perché `seguito` parte da False, oppure non c'è affatto (registra → None, e allora l'esito è «nessuna richiesta»). Una conversazione si chiude alla riga «torno ad aspettare» (scripts/voce/diagnosi_ascolto.py:104). Esito: ok.
- scripts/voce/diagnosi_ascolto.py:139 — `scelte[-ultime:]`. Esito: riserva R-761-1-M1.

**Riserve**
- R-761-1-M1 BASSA: con `--ultime 0` lo script stampa «Ultime 0:» e poi elenca TUTTE le attivazioni, perché `lista[-0:]` restituisce la lista intera. L'ho riprodotto con la sonda. Correzione: `scelte[len(scelte)-ultime:]`, oppure un `if ultime`.
- R-761-2-M1 COSMETICA: nel riassunto per giorno «N con richiesta» non conta le sospette, che una richiesta però l'hanno inviata. Esempio dalla sonda: «0 con richiesta, … 1 sospette». Con un numero pari di punteggi la mediana prende l'elemento più alto dei due centrali.

**Rischio escluso**
- Non ho verificato il comportamento sul Mac con il microfono vero, cioè se i punteggi e i picchi scartati servono davvero a tarare la soglia: non si può riprodurre qui.
- Non ho ripetuto i mutanti dichiarati: mi fido del resoconto dell'agente.
- Non ho controllato il nome reale del file di log che produce il servizio sul Mac (`.gas_voce/ascolto.log`): mi baso su quanto scritto nel LEGGIMI.

**Memoria**
- Ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md la riga contatore #761-M1 (APPROVATO CON RISERVE).
- Ho aggiunto una lezione nuova: `lista[-n:]` con n=0 restituisce tutta la lista.
- Il file è committato con lo script dedicato. L'ultimo commit è bd5a717: nel primo (8de3ae0) avevo scritto un numero di riga sbagliato, :455 invece di :454.
- Il diff in staging dell'agente è intatto: 4 file.

File rilevanti:
- /home/user/Gas/clients/voice/ascolto.py
- /home/user/Gas/scripts/voce/diagnosi_ascolto.py
- /home/user/Gas/scripts/voce/LEGGIMI.md
- /home/user/Gas/tests/test_unit_voce_ascolto.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## VERDETTO: APPROVATO

Re-review #762-M1 del diff in staging aggiornato su claude/peaceful-lovelace-0w2b7q (4 file, +311/-8). Le due riserve della #761-M1 sono chiuse: R-761-1-M1 e R-761-2-M1. Ho rilanciato i test: 324 passed.

**Elementi del diff esaminati**
- scripts/voce/diagnosi_ascolto.py:140 — `ultime` ora resta tra 0 e il numero di attivazioni, e la lista si taglia con `scelte[len(scelte) - ultime:]` (scripts/voce/diagnosi_ascolto.py:142). Rischio esaminato: con 0 o un numero negativo lo script stampava tutte le attivazioni. Ho provato con lo stesso log di prova della #761:
  - `--ultime 0` e `--ultime -3`: «Ultime 0:» e nessuna riga;
  - `--ultime 1`: solo l'ultima attivazione;
  - `--ultime 99`: «Ultime 2:» e tutte e due.
  - Esito: ok, R-761-1-M1 chiusa.
- scripts/voce/diagnosi_ascolto.py:130 — il riassunto per giorno ora dice «N con richiesta (di cui M sospette)», dove N somma inviate e sospette. Rischio esaminato: conti incoerenti. Nella prova esce «2 attivazioni — 1 con richiesta (di cui 1 sospette), 1 senza richiesta», e il totale torna. Esito: ok, R-761-2-M1 chiusa (la mia COSMETICA su «con richiesta»).
- scripts/voce/diagnosi_ascolto.py:137 — mediana vera: con un numero pari di punteggi fa la media dei due centrali. Rischio esaminato: indici sbagliati, perché si arriva a questa riga solo se c'è almeno un punteggio. Con n=1 e con n pari gli indici sono validi. Esito: ok.
- clients/voice/ascolto.py:432 e clients/voice/ascolto.py:454 — la parte dell'ascolto è invariata rispetto alla #761 (stesse 34 righe cambiate, stesse righe che contano i picchi scartati). Esito: ok, vale l'analisi della #761.

**Cosa non ho verificato**
- Il comportamento sul Mac con il log vero: non si può riprodurre qui.
- I test cambiati li ho solo eseguiti, non li ho riletti riga per riga, quindi non ho controllato che il valore 0.82 sia scritto a mano e non ricavato dal codice.

**Memoria**
- Riga #762-M1 — APPROVATO — aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script dedicato (commit 5bdead4).
- Nessuna lezione nuova.
- Il diff in staging non l'ho toccato.

**Review precedente (#761-M1), da conservare nel report**
- Esito: APPROVATO CON RISERVE.
- Riserve, ora chiuse: R-761-1-M1 BASSA (`--ultime 0` stampava tutte le attivazioni) e R-761-2-M1 COSMETICA («con richiesta» senza le sospette, mediana con n pari).
- Commit della memoria: bd5a717.

File:
- /home/user/Gas/scripts/voce/diagnosi_ascolto.py
- /home/user/Gas/clients/voice/ascolto.py
- /home/user/Gas/tests/test_unit_voce_ascolto.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

Commit 4db776c: verdetto integrale della review #763-M1.

## VERDETTO: APPROVATO CON RISERVE

Review #763-M1: diff staged sul branch claude/peaceful-lovelace-0w2b7q. Correzione della V-1 MEDIA del bot: la soglia `GAS_ASCOLTO_SOGLIA=0.6` rimasta nel .env del Mac vince sul nuovo predefinito 0,7.

Letture obbligatorie fatte: CLAUDE.md (sezioni 5, 8, 9 e 10), reports/stato_progetto.md (letto in modo mirato, con la riga 13 di reports/ripartenza_m1.md come contesto), .claude/agents/memoria_revisore.md.

Elementi del diff esaminati:
- `clients/voice/ascolto.py:1241` — `_regolazioni()` raccoglie le 8 regolazioni con gli stessi `_numero`, predefiniti e limiti di prima. Rischio esaminato: un'eccezione che, ora fuori dal `try`, farebbe crashare main invece di riprovare. `_numero` intercetta ValueError e i valori non finiti, e `soglia_interruzione`/`_finestra_dall_ambiente` non sollevano eccezioni. Effetto positivo: l'avviso su `GAS_VOICE_FINESTRA` fuori dai limiti ora compare una volta sola e non a ogni riprova del microfono. Esito: ok.
- `clients/voice/ascolto.py:1319` — `**regolazioni` passato ad `Ascolto`. Rischio esaminato: un argomento perso o passato due volte, che darebbe un TypeError intercettato dal ciclo di riprova, quindi un ciclo infinito silenzioso. Ho confrontato le chiavi con `Ascolto.__init__` (`clients/voice/ascolto.py:344`). soglia, blocchi_parola, voce_rms, silenzio_s, finestra_s, seguito_max_s, max_turni e soglia_interruzione coincidono tutte. Restano espliciti svuota, azzera_rilevatore, coda_eco_s=CODA_ECO_S, subito_s=SUBITO_S, invia_seguito e conferma. È lo stesso insieme di 14 argomenti di prima, senza doppioni. Esito: ok.
- `clients/voice/ascolto.py:1264` — riga di log «regolazioni in uso». Rischi esaminati: valori segreti nel log e interruzione spenta. Il log contiene solo numeri, nessun token né URL. Con `soglia_interruzione` a None scrive «spenta» (coperto dal test con `GAS_ASCOLTO_INTERRUZIONE=0`). Esito: ok.
- `clients/voice/ascolto.py:1265` — elenco `piu_facile` per l'avviso. Confronti: soglia minore di 0.7, blocchi minori di 3, turni maggiori di 1. Il valore 0.7 scritto nel .env non fa scattare l'avviso, perché il float è uguale. Esito: riserva cosmetica (manca il type hint `List[str]`).
- `tests/test_unit_voce_ascolto.py:155` — `_main_finto` ora pulisce anche SOGLIA, BLOCCHI_PAROLA e MAX_TURNI. Senza questa pulizia un ambiente del runner con queste variabili renderebbe instabile il test «nessun avviso». Esito: ok.
- `tests/test_unit_voce_ascolto.py:2926` — test dell'avviso: controlla un solo WARNING con i tre pezzi e anche il valore passato davvero ad Ascolto (`k.get("soglia") == 0.6`). Esito: ok. Le 3 righe vuote prima di `tests/test_unit_voce_ascolto.py:2917` sono una riserva cosmetica.

Suite rieseguita da me: `tests/test_unit_voce_ascolto.py`, 326 passed. Wall of Shame: nessuno slicing della history e nessuna simulazione di tool. Il diff non tocca il motore LLM né `_get_window`, il cap di 10 iterazioni o il cap di 8k.

Riserve (tutte COSMETICHE, da tracciare in stato_progetto.md):
- R-763-1-M1: `piu_facile = []` senza type hint `List[str]` (`clients/voice/ascolto.py:1265`).
- R-763-2-M1: tre righe vuote prima del primo test nuovo (`tests/test_unit_voce_ascolto.py:2914`).

Rischi esplicitamente esclusi:
- Comportamento reale sul Mac (che il .env contenga davvero 0.6 e che la riga finisca in .gas_voce/ascolto.log tramite il lanciatore): non riproducibile qui.
- Non ho rifatto i mutanti dichiarati (1 failed ciascuno).
- Scelta di progetto non contestata: l'avviso non copre `GAS_ASCOLTO_SOGLIA_INTERRUZIONE`, `GAS_ASCOLTO_VOCE_RMS` e `GAS_VOICE_FINESTRA`, che pure possono rendere Gas più reattivo. La V-1 riguardava solo la parola.

Memoria: aggiunta la riga #763-M1 in /home/user/Gas/.claude/agents/memoria_revisore.md e committata con lo script dedicato (commit 9b148c5). Il diff staged è intatto (3 file, +79/-14). Nessuna lezione nuova.

Commit 175289c (merge di origin/main e3eb542): verdetto integrale della review #764-M1.

## VERDETTO: APPROVATO

Il merge di origin/main e3eb542 (PR #370) dentro claude/peaceful-lovelace-0w2b7q (HEAD 4db776c, PR #371) è pulito. Non ci sono conflitti nel codice e non si perde niente in nessuno dei due lati.

Elementi del diff esaminati:
- `clients/voice/ascolto.py:1241` — `_regolazioni()` legge una volta i valori dal .env, entro i limiti, e li passa ad Ascolto. Rischio esaminato: che il merge lo modifichi o lo faccia interagire con il kernel di #370. Il file è identico a HEAD (`git diff --cached HEAD`: 0 righe). Il file importa solo librerie standard, niente da gas, telegram o modules, quindi le modifiche di #370 (pin anonimo, tetto delle chiamate, avviso di ripiego) non lo toccano. — ok
- `tests/test_unit_voce_ascolto.py:2917` — `test_main_scrive_le_regolazioni_in_uso`, il test della V-1 del bot su #371. Rischio esaminato: che il merge lo perda o lo alteri. Il file è identico a HEAD. Ho rieseguito test_unit_voce_ascolto più test_unit_notte: 525 passed. — ok
- `reports/stato_progetto.md:697` — riga di #368. Rischio esaminato: che l'unione automatica abbia perso testo di main (il conteggio rispetto a main dà 3 righe aggiunte e 1 tolta). La riga tolta è la versione di main della riga #368, sostituita dalla nostra identica più «✅ #368 MERGIATA». In più c'è la voce nuova di #371. La voce R-765-1-M1coord di main è presente a :378. — ok
- `.claude/agents/memoria_revisore.md` — unione dei due lati. Rischio esaminato: righe perse o doppioni introdotti. Ho cercato le righe di HEAD e di MERGE_HEAD che non sono nel file finale: 0 per entrambi. #764-M1coord e #765-M1coord restano distinte dalle righe -M1. I 3 doppioni esatti (#746, #747, una lezione) c'erano già su entrambi i lati: il merge non li ha introdotti, quindi non li ho toccati. — ok

Controlli meccanici:
- I 4 file di #370 (gas.py, modules/telegram/bot.py, tests/test_unit_kernel.py, tests/test_unit_notte.py) sono identici a MERGE_HEAD.
- Sono identici a HEAD i file nostri: scripts/voce/diagnosi_ascolto.py, scripts/voce/LEGGIMI.md, handoff, ultimo_report e diff_sessione.
- Dopo il merge, rispetto a main nel perimetro restano solo clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py e scripts/voce/diagnosi_ascolto.py.
- `git ls-files -u` è vuoto, non ci sono marcatori di conflitto e `--check` è pulito.
- Merge-base 51b7d20: i file di codice cambiati sui due lati non si sovrappongono.
- Nessun antipattern del Wall of Shame: il merge non porta codice nuovo.

Cose che non ho verificato:
- tests/test_unit_kernel.py non l'ho lanciato: il file è identico a MERGE_HEAD e quella suite è già stata verificata nella review #765-M1coord (1135 PASS).
- Il comportamento reale sul Mac (microfono, log dell'ascolto) non è riproducibile qui.
- La CI della PR dopo il merge non è ancora disponibile.

Memoria: ho aggiunto la riga `#764-M1 — 2026-11-11 — APPROVATO — … Nessuna lezione nuova.` in coda a /home/user/Gas/.claude/agents/memoria_revisore.md e l'ho messa in stage con `git add`; rispetto a HEAD il file ha ora 8 righe aggiunte e 0 tolte. Come richiesto non ho lanciato commit_memoria_revisore.sh: la riga entra nel commit di merge.

## §5 DELTA TEST DEL MOTORE

Kernel non toccato da questa PR (gas.py e i test del kernel arrivano identici da main). `tests/test_unit_voce_ascolto.py`: da 314 (main prima della PR) a 326 casi. Dopo il merge 175289c: test_unit_voce_ascolto + test_unit_notte 525 passed.

```
326 passed in 27.00s
```

Mutanti presi (riprodotti dall'agente): tetto dell'interruzione = max_turni; interruzione al primo blocco; niente azzeramento del conto dell'interruzione su errore / sotto soglia; niente conteggio dei picchi scartati su errore / sotto soglia; massimo della corsa non azzerato; ciascun controllo dell'avviso sulle regolazioni.

## §6 STATO CI

`gh` non autenticato nel container; stato letto con lo strumento GitHub MCP. Mappatura commit→run:
- 5b27586 (testa precedente della PR #371): unit-suite success, handoff-check success, verifica success, verifica-bot FAILURE (V-1 MEDIA .env con soglia 0.6, corretta in 4db776c).
- b9ad6e7: verifica-bot FAILURE (2 MEDIA, corrette in b36c944 e 881c4bb); handoff-check success.
- e1d46fa, 1aa50f0, 84481ea, a164dc8, b36c944, 881c4bb, 8de3ae0, bd5a717, 5bdead4, df3e650, 9b148c5, 4db776c: nessuna run conclusa su questo SHA (commit intermedi o mai pushati da soli).
- 175289c e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-759-1-M1 BASSA (= V-2 bot su 5b27586): il conto dell'interruzione riparte a ogni frase; con 3 blocchi Gas si ferma ~160 ms più tardi.
- V-3 BASSA bot su 5b27586: `GAS_ASCOLTO_BLOCCHI_PAROLA` vale anche per l'interruzione: abbassarlo per la parola abbassa anche quella difesa.
- R-763-1-M1, R-763-2-M1 COSMETICHE (type hint, righe vuote nel test).
- Da provare dal vivo: la parola vera con 0,7 + 3 blocchi e l'interruzione con 0,8 + 3 blocchi.
- Pagina web della voce (`clients/voice/browser_server.py`) ancora a 12 s e 5 turni (V-4 verifica esterna #361).
- Licenza CC BY-NC-SA di hey_jarvis (vedi proposta).
