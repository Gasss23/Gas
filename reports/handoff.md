# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-03 — Mani: fetta 39, ascolto H24 a frasi in fila (formato audio+pezzi) e .env letto come Gas (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #329 (https://github.com/Gasss23/Gas/pull/329). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5129534609","url":"https://github.com/Gasss23/Gas/pull/329"}`). **Sì dell'operatore** (via M1, 3 novembre: «mergia #329 e #330»): lo faccio io con la CI verde.
2. La PR #330 di M2 («audio+pezzi») è in main. Dopo il merge, sul Mac: `git pull`, `bash scripts/voce/installa.sh`, «Hey Jarvis» e una domanda: la prima frase deve partire subito.

---

## §1 SCOPE & ESITO FETTE

- **PR #328 (fetta 38)**: `FATTA` — mergiata (e3056fe).
- **Ascolto a frasi in fila (richiesta di M1, l'operatore lo trovava lentissimo)**: `FATTA` — `clients/voice/ascolto.py` chiede `X-Gas-Formato: audio+pezzi` (formato di M2 senza schermo, deciso con M1 dopo che avevo segnalato che «audio+testo+pezzi» dice «c'è uno schermo» e aggiunge «Il resto è a schermo») e suona ogni frase appena arriva; ripieghi su JSON con un audio e audio/mpeg.
- **Lettura del .env in installa.sh (V-1/V-2 bot #328)**: `FATTA` — `valore_env` come `gas._carica_dotenv`, test di confronto su 20 casi.
- **Rilevatore a intermittenza (V-1 ve #328)**: `FATTA` — conto azzerato dopo 125 blocchi buoni di fila.
- **R-625-1 (= V-2 ve #328), R-625-2, R-631-1, R-631-2, V-3 ve #328**: `FATTA`.
- **Formato «audio+pezzi» sul server**: `DEFERITA — è di M2, PR #330 (modules/voice/ non si tocca da qui, istruzione di M1)`.
- **Prova contro la PR #330 di M2 (server vero di #330, ascolto di #329, STT/kernel/ElevenLabs finti)**: `FATTA` — 5 frasi, la prima a 0,3 s e le altre in fila; errore a metà (suona la prima, poi si ferma); «non ho capito» (suona); senza chiave ElevenLabs e testo vuoto (bip d'errore, nessun crash).
- **Bot su 3b92254 (https://github.com/Gasss23/Gas/pull/329#pullrequestreview-5745313709)**: APPROVATO CON RISERVE, check neutral (decide l'operatore). V-1 BASSA (= R-632-2), V-2 BASSA (LEGGIMI prima della #330), V-3 BASSA (formati con lo schermo accettati): `REGISTRATE` in stato_progetto, senza altri giri.
- **Verifica esterna (https://github.com/Gasss23/Gas/pull/329#issuecomment-6592161590)**: APPROVATO CON RISERVE (fuzz di valore_env su 5000 file: 0 differenze; 28 mutanti). V-1/V-2/V-3/V-4/V-5 BASSE, V-6/V-7 COSMETICHE: `REGISTRATE`. V-8 BASSA (conflitto con main dopo la #327): `FATTA` col merge.
- **Merge di main (PR #327 di M2, voce V9)**: `FATTA` in 96f569e — conflitti solo nei report (tenuti i miei), nella memoria (tenute le righe di tutti e due) e nella riga «Ultimo aggiornamento» (unite); file del perimetro entrati da main identici a MERGE_HEAD. **Review #633 (chat Mani)**: APPROVATO.
- **Bot su fc1cab7 (https://github.com/Gasss23/Gas/pull/329#pullrequestreview-5745506029)**: APPROVATO CON RISERVE, neutral. V-1 BASSA (server voce a un solo thread occupato per tutta la riproduzione, perché il client legge la riga dopo a fine frase): `REGISTRATA` in stato_progetto, rimedio nella prossima fetta (righe lette in un thread). V-2 COSMETICA (handoff §6).
- **Merge di main (PR #330 di M2, formato «audio+pezzi»)**: `FATTA` in d32d326 — conflitti solo nei report, nella memoria e nella riga «Ultimo aggiornamento»; file di M2 identici a MERGE_HEAD; prova dal vero sull'albero unito (5 frasi in fila, la prima a 0,3 s; senza chiave bip; «non ho capito» suonato). **Review #634 (chat Mani)**: APPROVATO CON RISERVE (R-634-1/3 BASSE, R-634-2 COSMETICA, registrate).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 clients/voice/ascolto.py           | 196 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------
 reports/diff_sessione.md           |  18 +++++++++++-------
 reports/handoff.md                 | n/d
 reports/roadmap.md                 |   2 +-
 reports/stato_progetto.md          |   5 +++--
 reports/ultimo_report.md           |  32 +++++++++++++++----------------
 scripts/voce/LEGGIMI.md            |  14 ++++++++------
 scripts/voce/installa.sh           |  79 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------
 tests/test_unit_voce_ascolto.py    | 369 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
```

NB: base = merge-base con origin/main = 805c272. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
17d8def chore(revisore): memoria review #634 — APPROVATO CON RISERVE
d32d326 Merge origin/main (PR #330, voce V10 audio+pezzi) in PR #329
fc1cab7 docs(fine-task): merge di main (PR #327) nella PR #329, riserve del bot e della verifica esterna registrate (review #633)
6fd5d16 chore(revisore): memoria review #633 — APPROVATO
96f569e Merge origin/main (PR #327, voce V9) in PR #329
3b92254 docs(fine-task): fetta 39, ascolto a frasi in fila, PR #329
6cb49c9 docs(voce): report della fetta 39 (ascolto a frasi in fila)
c6c7422 chore(revisore): memoria review #632 — APPROVATO CON RISERVE
04d365c feat(voce): ascolto H24 a frasi in fila (formato audio+pezzi, la prima suona subito) e .env letto come Gas in installa.sh; rilevatore a intermittenza (fetta 39, review #632)
```

NB: l'head della PR, cioè il commit che contiene questo file, non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #632 (chat Mani), sul commit 04d365c, verdetto integrale:

```
## VERDETTO: APPROVATO CON RISERVE

Review #632 (chat Mani), fetta 39. Branch claude/peaceful-lovelace-0w2b7q, base origin/main e3056fe. Ho controllato che il diff in staging abbia sha256 a653180cf95883d6… e che contenga 4 file. Prima ho letto CLAUDE.md, le parti utili di reports/stato_progetto.md, la mia memoria e `_do_pezzi_response` della V7b. Ho rilanciato la suite: tests/test_unit_voce_ascolto.py dà **149 passed**.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:481` — `_frasi_ndjson`: `readline(RIGA_MAX + 1)` con controllo della lunghezza, stop su «errore_voce»/«fine», `r.close()` nel finally. Ho controllato memoria illimitata, connessione lasciata aperta e coerenza con la V7b (modules/voice/server.py:491: riga 1 con audio, poi una riga per frase, riga di errore e stop, `fine`). Esito: ok.
- `clients/voice/ascolto.py:401` — `turno` chiude l'iterabile nel finally anche dopo KeyboardInterrupt (l'eccezione non è presa da `except Exception`, il finally gira lo stesso), poi svuota il microfono. Ho controllato §9, la spesa del server dopo Ctrl-C e il doppio svuotamento. Con `suonati == 0` lo svuotamento è doppio (`clients/voice/ascolto.py:410`), ma serve a togliere il bip di errore: innocuo. Esito: ok.
- `clients/voice/ascolto.py:541` — `a_pezzi = True`: di `r` si occupa il generatore, gli altri rami la chiudono nel finally. Esito: ok. Una riserva cosmetica (R-632-3, sotto).
- `clients/voice/ascolto.py:167` — `formato_richiesto` accetta solo `[a-z+]{0,40}`, quindi nessuna iniezione nelle intestazioni HTTP. Il server di oggi non conosce «audio+pezzi»: `_vuole_audio_testo` è falso e la richiesta passa al ramo audio/mpeg (modules/voice/server.py:428), con l'istruzione della voce senza schermo (modules/voice/server.py:398). Oggi quindi nessuna regressione. `_OPENER` resta quello di prima: niente proxy, niente redirect. Esito: ok.
- `clients/voice/ascolto.py:286` — azzeramento dopo `BUONI_PER_AZZERARE` blocchi buoni di fila, riportato a 0 a ogni errore. Ho controllato il log limitato e le pause. Esito: ok, con una riserva bassa (R-632-2).
- `clients/voice/ascolto.py:478` — `b64decode(validate=True)`. Esito: riserva R-632-1.
- `scripts/voce/installa.sh:29` — `valore_env`, confrontata riga per riga con gas.py:635 e gas.py:605:
  - virgolette: si chiude alla prima virgoletta seguita da fine riga o da `\s+#`, come il fullmatch con `.*?`;
  - commento: il primo spazio seguito da `#`, come `re.split(r"\s+#")`;
  - le virgolette non chiuse non fanno contare la chiave, come in Gas;
  - `export ` va scritto con uno spazio solo, come in Gas.
  
  Su `set -e`: la funzione è chiamata solo dentro `$(… || true)` o `if X="$(…)"`, contesti in cui errexit non scatta. Le `&&` con `continue` sono fuori dalla regola, e il corpo del while finisce con `return`. Esito: ok.
- `scripts/voce/installa.sh:34` — `$'\xef\xbb\xbf'` dentro `"${riga#…}"`: su bash 5 funziona anche con `shopt -u extquote` (provato). Su bash 3.2 non l'ho verificato (vedi sotto). Esito: ok.
- `scripts/voce/installa.sh:77` — `TOKEN_VOCE`: mai stampato, usato solo in `[ -n ]` e `[[ != \#* ]]`, poi `unset`. Il test `tests/test_unit_voce_ascolto.py:1012` vale come guardia. Esito: ok.
- `scripts/voce/installa.sh:90` — GAS_CLAUDE_BIN: avvisi per valore vuoto, valore che comincia con `#` e percorso non assoluto. R-625-2 è a `scripts/voce/installa.sh:103`, nell'ordine giusto delle condizioni (assoluto e lista bianca, poi non assoluto, poi caratteri non ammessi). Esito: ok.
- `tests/test_unit_voce_ascolto.py:482` — il server vero aspetta che la prima frase sia suonata prima di mandare la seconda, quindi un client che legge tutto prima di suonare verrebbe preso. `tests/test_unit_voce_ascolto.py:297` copre il rilevatore a intermittenza. `tests/test_unit_voce_ascolto.py:1105` conta gli `sleep 1` (R-631-1 chiusa). Esito: ok.

**Riserve**
- **R-632-1 BASSA**: il controllo `validate=True` (`clients/voice/ascolto.py:478`) non è coperto dai test. Ho provato il mutante senza `validate`: `-k "pezzi or json"` dà 14 passed. Il motivo è che "%%%non-base64" dà errore di padding e "%%%" dà b"" anche senza validate. Serve un caso che senza validate decodifica lo stesso, per esempio `"QUJD!!"` → b"ABC". Non è un rischio di sicurezza: al massimo afplay riceve dati sporchi e fallisce, e l'errore viene loggato.
- **R-632-2 BASSA**: un rilevatore che sbaglia più spesso di una volta ogni 10 s non si azzera mai. Le pause salgono a 60 s per errore, quindi l'ascolto è sordo per gran parte del tempo, e il log scrive solo alla 512ª e alla 1024ª riga di errore (ore di silenzio nel log). È il comportamento chiesto dalla V-1 ve #328 e già presente per il rilevatore sempre rotto. Va dichiarato nel LEGGIMI o nello stato.
- **R-632-3 COSMETICA**: `close()` su un generatore mai avviato non esegue il suo finally. Se l'interruzione cade fra il ritorno di `invia` e il primo `next` (`clients/voice/ascolto.py:401`), `r` resta aperta fino al garbage collector. La finestra è minuscola.

**Rischi esclusi (non verificati)**
- bash 3.2 del Mac: qui c'è solo bash 5.2. Ho ragionato su extquote (attivo di default dalla 3.0), su `for ((…))` e sulle sottostringhe aritmetiche, ma non li ho eseguiti su 3.2.
- Il formato «audio+pezzi» lato server: l'implementazione di M2 non esiste su main né in nessun ramo locale. Ho verificato solo il ripiego sul server di oggi e la compatibilità col tracciato V7b.
- Riproduzione reale con afplay e svuotamento del microfono veri: non riproducibili qui.
- Differenze esotiche fra il parser bash e quello di Gas: separatori di riga Unicode (`splitlines`), UTF-8 non valido (Gas non carica niente, lo script sì), spazi Unicode. Non le ho provate.

**Memoria**: ho aggiunto la riga #632 e una lezione (base64 «quasi valido» nei mutanti) in .claude/agents/memoria_revisore.md, solo nel working tree. Come mi hai chiesto, non ho lanciato commit_memoria_revisore.sh e non ho toccato l'indice: lo sha256 del diff in staging è ancora a653180cf95883d6. Ho provato il mutante e poi ripristinato il file dall'index (`git checkout --`).

File rilevanti: /home/user/Gas/clients/voice/ascolto.py, /home/user/Gas/scripts/voce/installa.sh, /home/user/Gas/tests/test_unit_voce_ascolto.py, /home/user/Gas/.claude/agents/memoria_revisore.md
```

Review #633 (chat Mani), merge di origin/main (PR #327) in 96f569e, verdetto integrale:

```
## VERDETTO: APPROVATO

Review #633 (chat Mani). Si tratta del merge di origin/main b6f3750 (PR #327, voce V9 di M2) dentro claude/peaceful-lovelace-0w2b7q (PR #329, fetta 39, head 3b92254). Ho ricalcolato lo sha256 del diff staged: è 6be0b5ed8e1b6c7b…, coincide col tuo. È rimasto uguale anche dopo che ho scritto la riga #633 nella memoria, perché il working tree è cambiato ma l'indice no. Letture fatte: CLAUDE.md, le parti utili di stato_progetto e la memoria del revisore, con le review #632, #657-M2 e #659-M2.

Elementi del diff che ho esaminato:
- `clients/voice/browser_server.py:88` — /config ora restituisce `agc` accanto a finestra, max_turni e interruzione. Rischio: che il merge abbia rovinato il file di M2. Ho confrontato i blob: indice b0b652dd = MERGE_HEAD, mentre HEAD e la base comune hanno 14ab9cc8. Lo stesso vale per `clients/voice/browser_client.html:650` (4fd3faad = MERGE_HEAD), per `tests/test_unit_voice_server.py:1003` (9bd1fc3f = MERGE_HEAD) e per `reports/prova_voce_mac.md` (eb73c181 = MERGE_HEAD) — ok.
- `clients/voice/browser_server.py:380` — `GAS_VOICE_AGC` viene letta solo qui. Rischio: un'interazione con l'ascolto H24. `grep AGC|browser_server|INTERRUZIONE` su `clients/voice/ascolto.py`, `scripts/voce/installa.sh` e `scripts/voce/LEGGIMI.md` non trova niente. Il lato di main (`git diff e3056fe MERGE_HEAD -- modules/ gas.py brains/`) è vuoto, quindi V9 non tocca modules/voice/ — ok.
- `clients/voice/ascolto.py:158` — ascolto.py parla direttamente col server voce sulla porta 8765, non con browser_server. Rischio: che V9 cambi il contratto del formato. `clients/voice/ascolto.py:523` manda `X-Gas-Formato: audio+pezzi`. La pagina (`clients/voice/browser_client.html:650`) continua a usare `audio+testo+pezzi`. Il server (`modules/voice/server.py:115`, contesto, non toccato dal merge) conosce ancora solo `audio+testo+pezzi`, quindi resta il ripiego su un solo MP3 già registrato nella review #632 — nessuna interazione nuova, ok.
- `git diff --cached MERGE_HEAD --stat` — mostra solo il lavoro di #329: ascolto.py, installa.sh, LEGGIMI, test_unit_voce_ascolto.py, `reports/roadmap.md`, memoria, handoff, ultimo_report, diff_sessione, stato_progetto. Il blob nell'indice è uguale a HEAD per ascolto.py (e454e1ef), installa.sh (dcc04eed), LEGGIMI (7dcebe35), il test dell'ascolto (a474f2cc) e roadmap (4705561b). Roadmap non era nel tuo elenco, ma è lavoro del tuo lato: la base comune ha 481451cd, uguale a MERGE_HEAD — ok.
- Conflitti: handoff, ultimo_report e diff_sessione sono identici a HEAD (presi con --ours) — ok, li aggiorni tu. In `.claude/agents/memoria_revisore.md`, rispetto a HEAD e a MERGE_HEAD, le righe tolte sono 0; ci sono #632 con la sua lezione e #630-M2…#659-M2 con la loro lezione, nessun marcatore — ok.
- `reports/stato_progetto.md:4` — l'ho controllato con uno script Python: il prefisso «(chat Mani: fetta 39, …; PR #328 mergiata) — prima: » è seguito dalla riga 4 di MERGE_HEAD intera (uguaglianza esatta: True). «Voce V9 «rumore»», «Riserve BASSE di #318», «fetta 39 (R8» e «fetta 38 (R8» compaiono una volta ciascuno — ok.
- `git diff --cached --check` è pulito. Test sull'albero unito (working tree = indice): `tests/test_unit_voce_ascolto.py` + `tests/test_unit_voice_server.py` → **249 passed, 0 skipped** in 280 s, compresi i test col browser — ok.

Finding: nessun R-633-N nuovo. Le riserve R-632-1, R-632-2 e R-632-3 restano quelle della review #632, non toccate da questo merge.

Cosa NON ho verificato:
- Il comportamento reale sul Mac (microfono, AGC, launchd), perché non si può riprodurre nel cloud.
- La suite completa del motore: il merge non tocca gas.py, brains/ o modules/.
- Gli altri file del perimetro (hook, gate, CI): non sono nel diff.

Memoria: la riga #633 è stata aggiunta in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md`, solo nel working tree come chiesto. Non ho lanciato `scripts/commit_memoria_revisore.sh`: c'è un merge in corso e non va toccato l'indice. La riga va inclusa nel commit di merge o in quello successivo. Nessuna lezione nuova.
```

Review #634 (chat Mani), merge di origin/main (PR #330) in d32d326, verdetto integrale:

```
## VERDETTO: APPROVATO CON RISERVE

Review #634 (chat Mani). Merge di origin/main 805c272 (PR #330, voce V10 di M2) dentro claude/peaceful-lovelace-0w2b7q (PR #329, head fc1cab7). Lo sha256 del diff staged è 80ccf8177e7651ec…, uguale prima e dopo la review. L'indice non l'ho toccato.

**Elementi del diff esaminati**

- `modules/voice/server.py:506` — con «audio+pezzi» e senza chiave ElevenLabs il server risponde 200 in JSON con `content` ed `errore_voce`, senza `audio` e non in NDJSON. Rischio esaminato: che il client lo legga come voce o vada in crash. Esito: ok. `clients/voice/ascolto.py:545` lo legge come «senza voce», il turno restituisce False e suona il bip d'errore (riprodotto).
- `modules/voice/server.py:641` — nel caso «non ho capito» la risposta passa da `_rispondi_senza_turno`, poi da `_vuole_righe_senza_schermo`, e arriva in NDJSON. Rischio esaminato: un formato diverso da quello atteso dal client. Esito: ok. Il client suona 1 pezzo e il kernel non viene chiamato.
- `modules/voice/server.py:423` — con «audio+pezzi» si usa `ISTRUZIONE_VOCE`, perché `_vuole_audio_testo` resta falso. Rischio esaminato: un'istruzione che parla di schermo. Esito: ok, nell'istruzione catturata dal kernel finto non c'è «schermo».
- `clients/voice/ascolto.py:502` — su una riga con `errore_voce` il client esce e chiude la connessione. Rischio esaminato: che il server continui a sintetizzare frasi che nessuno sente. Esito: ok. Con un errore alla seconda frase le sintesi sono 2, la prima frase suona e poi si ferma. Con l'errore alla prima frase non suona niente e parte il bip.
- `clients/voice/ascolto.py:94` — il tetto di una riga è 8 MB. Rischio esaminato: una riga più lunga del tetto, cioè la prima frase fino a 1500 caratteri in MP3 base64 più il `content` intero. Esito: ok, il margine è ampio.
- `reports/stato_progetto.md:4` — la riga è il prefisso della fetta 39, poi « — prima: », poi la riga 4 di MERGE_HEAD identica carattere per carattere. Verso main il file ha solo 5 righe diverse: la riga 4, il blocco della fetta 39 aggiunto e la riga della fetta 38 aggiornata. I blocchi V10 e fetta 39 compaiono una volta ciascuno. Esito: ok.

**Punto 1 (blob)**: ok. `modules/voice/server.py` e `tests/test_unit_voice_server.py` hanno il blob uguale a MERGE_HEAD. Hanno il blob uguale a HEAD: `clients/voice/ascolto.py`, `scripts/voce/installa.sh`, `scripts/voce/LEGGIMI.md`, `tests/test_unit_voce_ascolto.py`, `reports/roadmap.md`, e anche `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` (presi col tuo lato). `git diff --cached MERGE_HEAD --stat` mostra solo il lavoro di #329: 10 file, nessun file del server.

**Punto 2 (memoria)**: unione esatta. Base 1208 righe, +3 dal tuo lato (#632, la lezione, #633) e +3 da main (#660-M2, #661-M2, #662-M2). Nessuna riga mancante da nessuno dei due lati, nessuna riga «#» doppia, nessun marcatore, nessun file non risolto.

**Punto 3 (contratto)**: l'ho riprodotto da me con server vero e `ascolto.py` vero; STT, kernel ed ElevenLabs finti. Lo script è in /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/prova634.py.
- 5 frasi: suonate tutte e 5 in fila, la prima a 0,05 s col finto.
- Senza chiave: bip d'errore.
- «Non ho capito»: suonato.
- Errore a metà: suona la prima frase, poi si ferma.
- Errore alla prima frase: bip.
- Testo vuoto e testo di soli spazi: bip.
- Testo oltre 1500 caratteri: taglio più l'avviso di resto, 2 pezzi.
- Formato di default del client: «audio+pezzi».

Le suite `tests/test_unit_voce_ascolto.py` e `tests/test_unit_voice_server.py` danno 252 passed, 0 skipped.

**Riserve**
- R-634-1 BASSA: se il TTS si rompe a metà, senza schermo il risultato è silenzio. Il turno risulta riuscito (True), quindi non c'è bip né avviso: l'operatore sente solo la prima frase e non sa che manca il resto. Rimedio possibile: un bip d'errore quando arriva `errore_voce` dopo che almeno un pezzo è già stato suonato.
- R-634-2 COSMETICA: il client scarta il testo di `errore_voce` e nel log scrive «risposta inattesa (senza voce)» sia con la chiave mancante sia con testo vuoto. Sul Mac il log non dice la causa.
- R-634-3 BASSA: nessun test automatico mette insieme il server vero e `ascolto.py`. Ogni suite usa i propri finti e i due lati li scrivono chat diverse (M2 e Mani): se il contratto cambia da una parte, le suite passano lo stesso. La prova dal vero tua e la mia non restano nel repo.

**Rischi esclusi**: il comportamento con ElevenLabs e Groq veri non l'ho verificato (latenza reale, dimensione reale degli MP3, risposte d'errore reali), perché qui ci sono solo finti. Non ho verificato nemmeno l'audio e il microfono veri sul Mac (afplay, openWakeWord), che non si possono riprodurre qui. Lo spazio in coda in `reports/handoff.md:80` c'era già a HEAD; verrà riscritto con l'handoff.

**Memoria**: ho aggiunto la riga #634 più una lezione in coda a .claude/agents/memoria_revisore.md, solo nel working tree. `scripts/commit_memoria_revisore.sh` non l'ho lanciato: col merge in corso concluderebbe il merge, e mi hai chiesto di non toccare l'indice. La riga va portata col commit di merge.
```

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 93 a 149 test (risposta a pezzi con un server vero, ripieghi, chiusura della risposta, rilevatore a intermittenza, confronto di `valore_env` con `gas._carica_dotenv`, lista bianca di GAS_CLAUDE_BIN, attese del giro nc). Suite della voce (ascolto, server, trascrizione): 333 passed. Nessuna modifica a gas.py né a modules/voice/.

## §6 STATO CI

`gh` non autenticato nel cloud.
- 6cb49c9 (report): pushato prima di aprire la PR, handoff non ancora riscritto; verifica-bot cancelled (cambio di head).
- 3b92254 (fine-task): unit-suite success, handoff-check success, verifica-bot neutral (bot APPROVATO CON RISERVE); poi conflitto con main (PR #327).
- I commit di main entrati col merge (fino a b6f3750, PR #327) hanno le run della PR #327.
- 96f569e (merge), 6fd5d16 (memoria #633), fc1cab7 (fine-task): unit-suite success, handoff-check success, verifica-bot neutral (bot APPROVATO CON RISERVE); poi conflitto con main (PR #330).
- I commit di main entrati col merge (fino a 805c272, PR #330) hanno le run della PR #330.
- d32d326 (merge), 17d8def (memoria #634): pushati insieme al commit di fine-task.
- Il commit che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-632-1 BASSA (`validate=True` del base64 senza test), R-632-2 BASSA (rilevatore che sbaglia più di una volta ogni 10 s: mai azzerato, da dire nel LEGGIMI), R-632-3 COSMETICA (Ctrl-C prima della prima frase: connessione chiusa dal garbage collector).
- Da #329: bot V-1 su fc1cab7 BASSA (server a un thread occupato durante la riproduzione), R-634-1 BASSA (= ve V-3), R-634-2 COSMETICA, R-634-3 BASSA (nessun test che unisca server vero e ascolto.py), bot V-3 = ve V-4 BASSA (lista bianca del formato), ve V-1 BASSA (test del ramo R-625-2), ve V-3 BASSA (risposta troncata senza bip), ve V-6/V-7 COSMETICHE.
- Da #324: V-1/V-2 bot su 84b1422 BASSE e V-2 su 7346994 COSMETICA, per la fetta 1 della mail.
- R-615-4 MEDIA (microfono sotto launchd, da provare sul Mac); R-615-5 BASSA (licenza di hey_jarvis); R-623-1, R-623-3, R-622-2/3.
- Bash 3.2 del Mac e launchctl vero: si provano solo sul Mac.
