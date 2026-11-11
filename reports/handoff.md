# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 — chat Mani: ascolto più severo di default (zero risposte non richieste)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #371 (https://github.com/Gasss23/Gas/pull/371): review APPROVATO (riserve BASSE); merge secondo CLAUDE.md §10 (verdetto testuale del bot sull'head, CI verde), dopo il via di M1 («#370 dentro»).
2. Al mattino: prova dal vivo di «Hey Jarvis» con 0,7 e 3 blocchi; se non scatta, `GAS_ASCOLTO_SOGLIA=0.6` o `GAS_ASCOLTO_BLOCCHI_PAROLA=2` nel .env.

---

## §1 SCOPE & ESITO FETTE

- **Default più severi dell'ascolto (priorità ALTA dell'operatore via M1)**: `FATTA` — 84481ea, review #757-M1 APPROVATO CON RISERVE (R-757-1-M1 MEDIA chiusa) e #758-M1 APPROVATO.
- **V-1 MEDIA del bot #371 (l'interruzione scattava con un solo blocco)**: `FATTA` — b36c944, review #759-M1 APPROVATO CON RISERVE (R-759-1-M1 BASSA).
- **V-2 MEDIA del bot / V-1 verifica esterna #371 (PR in conflitto con main dopo la #369)**: `FATTA` — 881c4bb, merge di origin/main 51b7d20, conflitti solo nei report; review #760-M1 APPROVATO.
- **Lettura dei log del Mac**: `DEFERITA — l'operatore dorme, ascolto in pausa`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 clients/voice/ascolto.py           |  69 ++++++++++++++++++++++++++++++++++++++++++++++++---------------------
 reports/diff_sessione.md           |  13 +++++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  15 +++++++--------
 scripts/voce/LEGGIMI.md            |  36 +++++++++++++++++++++++-------------
 tests/test_unit_voce_ascolto.py    | 103 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
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

Commit 84481ea: verdetto integrale della review #757-M1 (primo giro) e della re-review #758-M1 (sul diff committato).

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

## §5 DELTA TEST DEL MOTORE

Kernel non toccato. `tests/test_unit_voce_ascolto.py`: da 314 (base 904d9d6) a 319 casi (317 dopo 84481ea, 319 dopo b36c944). Dopo il merge 881c4bb: test_unit_voce_ascolto + test_unit_voice_stt 459 passed. `test_unit_voice_server.py` + `test_unit_manutenzione.py` (-k "not browser"): 233 passed.

```
319 passed in 28.53s
```

Mutanti presi: tetto dell'interruzione = max_turni (1 failed), tetto 9 (2 failed secondo la verifica esterna #371: test_le_interruzioni_restano_sotto_max_turni e test_coi_seguiti_spenti_la_seconda_interruzione_chiude). Su b36c944: interruzione al primo blocco → 2 failed; niente azzeramento su errore → 1 failed; niente azzeramento sotto soglia → 1 failed.

## §6 STATO CI

`gh` non autenticato nel container; lo stato è letto con lo strumento GitHub MCP. Mappatura commit→run:
- b9ad6e7 (testa precedente della PR #371): handoff-check success, smista success, verifica success, verifica-bot FAILURE (V-1 MEDIA interruzione su un blocco, V-2 MEDIA conflitto con main: corrette in b36c944 e 881c4bb); unit-suite in corso alla lettura.
- e1d46fa, 1aa50f0, 84481ea, a164dc8, b36c944: nessuna run conclusa su questo SHA letta qui (commit intermedi o pushati insieme).
- 881c4bb e il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Bot #371 su b9ad6e7: V-1 MEDIA e V-2 MEDIA CHIUSE; V-3 COSMETICA (docstring del modulo) CHIUSA.
- Verifica esterna #371 ([commento](https://github.com/Gasss23/Gas/pull/371#issuecomment-6783011572)): V-1 (conflitto) CHIUSA; V-2 BASSA (LEGGIMI, due rimedi nella stessa frase) CHIUSA; V-3 BASSA (§6 senza stato CI) corretta qui; V-4 BASSA (conteggio del mutante «tetto 9») corretta in §5.
- R-759-1-M1 BASSA: il conto dell'interruzione riparte a ogni frase (parola a cavallo fra due frasi); con 3 blocchi Gas si ferma ~160 ms più tardi.
- Da provare dal vivo: con soglia 0,7 e 3 blocchi la parola vera scatta ancora? (stesso tema di R-736-1). Rimedio documentato nel LEGGIMI.
- La pagina web della voce (`clients/voice/browser_server.py`) resta a 12 s e 5 turni (V-4 verifica esterna #361): prossima fetta voce.
- Le riserve della PR #368 restano in `reports/stato_progetto.md`.
