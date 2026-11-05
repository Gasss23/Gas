# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 41: la parola di attivazione interrompe Gas mentre parla

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #336 (https://github.com/Gasss23/Gas/pull/336). Review #669 APPROVATO CON RISERVE e PR nel perimetro: decide l'operatore tramite M1. Numero e URL dalla risposta dello strumento GitHub `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **PR #333 (fetta 40)**: `FATTA` — mergiata (830c5bf) col sì dell'operatore, CI verde.
- **Fetta 41 — interruzione con la parola**: `FATTA`
  Solo la parola fa da grilletto mentre Gas parla (soglia 0.7). Frase fermata, frasi in fila scartate, bip, nuova richiesta sotto max_turni. Review #668 (con R-668-1 MEDIA, corretta) e #669 APPROVATO CON RISERVE. Diff identico a quello rivisto (stesso SHA del diff staged), riportato su main dopo il merge della #333.
- **Fetta 42 — «Sì, signore?»**: `DEFERITA — aspetta il merge della PR #335 di M2 (GET /voce/conferma)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 clients/voice/ascolto.py           | 151 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------
 reports/diff_sessione.md           |  15 +++++++--------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  29 ++++++++++++++---------------
 scripts/voce/LEGGIMI.md            |   8 ++++++++
 tests/test_unit_voce_ascolto.py    | 270 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 830c5bf.

## §3 GIT LOG --ONELINE (sessione)

```
e619103 docs(fine-task): fetta 41 chat Mani — interruzione con la parola, review #668–#669, PR #336; PR #333 mergiata
ef65e42 feat(voce): fetta 41 — la parola di attivazione interrompe Gas mentre parla
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit ef65e42 — review #668 (primo giro), verdetto integrale. Le citazioni si riferiscono al diff di allora; le righe sono cambiate di poco con le correzioni della #669. Gli hash 808993d e 91f74aa citati nei verdetti sono commit del branch locale `mani/voce-interruzione`, mai pubblicato (V-1 della verifica esterna): sul branch remoto le righe #668/#669 della memoria sono nel commit di fine-task.

## VERDETTO: APPROVATO CON RISERVE

Review #668 (chat Mani). Ho letto lo staged di `mani/voce-interruzione` (base 2c8cd2a, 3 file). Ho esportato l'indice in scratch con `checkout-index`: niente stash e nessuna modifica al repo vero. Lo SHA-256 del diff staged è `f10e532e…9258`, uguale prima e dopo il commit della memoria.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:645` — `RiproduzioneAfplay`: avvia afplay con Popen. Il file temporaneo è 0600 in una cartella sua; se afplay non parte, la cartella si cancella (anche con BaseException). C'è un tetto `RIPRODUZIONE_MAX_S`. Rischi esaminati: afplay che resta acceso, file che resta su disco. Esito: ok. Tre mutanti uccisi: senza `terminate`, senza `rmtree` in `ferma`, senza pulizia nell'init. Il mutante che ignora il tetto è ucciso anche lui.
- `clients/voice/ascolto.py:488` — `_ascolta_mentre_suona` chiama sempre `ferma()` nel finally, anche con KeyboardInterrupt; il rilevatore viene usato solo con `soglia_interruzione`. Rischi esaminati: eccezioni che escono, il volume che fa da grilletto. Esito: ok. Il mutante «soglia normale» è ucciso dal test di `tests/test_unit_voce_ascolto.py:266`. Riserva R-668-2 sulle guardie di finita/ferma, vedi sotto.
- `clients/voice/ascolto.py:433` — su interruzione, `turno` esce col break e il finally chiude `pezzi`, cioè la risposta: il server smette di sintetizzare. Esito: ok. Il test di `tests/test_unit_voce_ascolto.py:246` verifica la frase fermata a metà, la B scartata e la risposta chiusa. Il mutante che non rimette `interrotto` a False è ucciso.
- `clients/voice/ascolto.py:527` — ramo `interrotto` di `conversazione`: azzera, bip, svuota, `turni = 0`, poi registra. Esito: riserva (R-668-1, R-668-3).
- `clients/voice/ascolto.py:196` — `soglia_interruzione()`: «0» la spegne, la soglia va da 0.05 a 1.0, un valore non numerico ripiega su 0.7. Esito: ok, coperto dal test parametrico. La tabella di `scripts/voce/LEGGIMI.md:91` è allineata al codice e un test la controlla.

**Esecuzione**: sull'indice esportato 147 passed e 20 failed. I 20 falliti mancano anche sulla base e non dipendono dal diff: `openai` e `installa` non ci sono nel container. Ho provato 12 mutanti contro l'insieme dei falliti della base: 7 uccisi, 5 vivi.

**Privacy**: ok. Mentre Gas parla, i blocchi del microfono vanno solo al rilevatore locale, e dopo l'interruzione si svuota due volte (nel finally di `turno` e dopo il bip). L'unico file su disco è l'MP3 della voce di Gas (0600, cancellato), mai l'audio dell'operatore. Prima della parola nessun audio va in rete.

**Finding**
- **R-668-1 MEDIA** — A ogni interruzione `turni = 0` (`clients/voice/ascolto.py:527`), quindi le interruzioni azzerano il tetto `max_turni`. Una catena è possibile senza l'operatore: Gas dice «Jarvis» dalle casse, l'eco supera 0.7, poi un rumore sopra 200 di volume apre una richiesta, e così via: turni pagati senza tetto. Il mutante che toglie l'azzeramento sopravvive, cioè nessun test fissa la scelta. Rimedio: non azzerare (o mettere un tetto a parte alle interruzioni di fila), e aggiungere un test. Non blocca: serve che la parola scatti per eco, e il server ha già il tetto orario V12.
- **R-668-2 BASSA** — Le guardie §9 di `finita()` e di `ferma()` (`clients/voice/ascolto.py:466`, `clients/voice/ascolto.py:488`) non hanno test: i due mutanti che le tolgono sopravvivono. Se mancassero, l'eccezione arriverebbe a `gira`, che la ferma: la conversazione finisce, ma nessun crash.
- **R-668-3 BASSA** — Lo svuotamento dopo il bip d'interruzione (`clients/voice/ascolto.py:526`) non ha test: i test finti non mettono il bip nel microfono, quindi il mutante sopravvive.
- **R-668-4 COSMETICA** — L'annotazione `riproduci: Callable[[bytes], None]` (`clients/voice/ascolto.py:255`) è superata: ora la funzione restituisce un oggetto con `finita()`/`ferma()`, oppure None. Serve `Optional[...]` o un Protocol.
- Nota, non è un finding: il mutante «continue tolto dopo una riproduzione fallita» si comporta in modo identico all'originale (`in_corso=None` restituisce False). Resta aperta, come dichiarato, la riserva V-1 del bot su fc1cab7: fra una frase e l'altra il microfono non viene letto, quindi la parola detta in quel momento si coglie solo se è ancora nel buffer.

**Rischio escluso**: non ho verificato il comportamento reale sul Mac, cioè afplay e `terminate` veri, l'eco delle casse del MacBook contro la soglia 0.7 di openWakeWord, e il buffer di sounddevice fra una frase e l'altra. Qui non si possono riprodurre: niente macOS, niente microfono, niente modello.

**Memoria**: ho aggiunto la riga `#668` e una lezione nuova (un azzeramento del contatore dentro un ciclo con tetto va mutato, chiedendosi se l'evento che lo attiva può ripetersi da solo). Commit 808993d con `scripts/commit_memoria_revisore.sh`; lo staged non cambia (stesso SHA prima e dopo). Nota: il commit sposta HEAD da 2c8cd2a a 808993d.

Commit ef65e42 — review #669 (ri-review con le correzioni), verdetto integrale:

## VERDETTO: APPROVATO CON RISERVE

Review #669 (chat Mani). Riguarda la fetta 41, l'interruzione di Gas con la parola mentre parla. Branch mani/voce-interruzione: 3 file in staging, base 808993d. Prima della review ho letto CLAUDE.md, la testata di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:525` — nel ramo dell'interruzione il codice esce se `turni >= max_turni`; `turni` non viene più azzerato. Rischio: l'eco di Gas fa scattare la parola e parte una catena di turni pagati senza limite. Ho provato in una copia, ognuno da solo, 3 mutanti: azzeramento rimesso, `>` al posto di `>=`, uscita tolta. Esito: tutti presi (22 failed contro i 21 di partenza). **R-668-1 chiusa.**
- `tests/test_unit_voce_ascolto.py:303` — test sul tetto con `max_turni=2` e due interruzioni di fila: escono 2 invii e solo A e B suonate. Rischio: il test non distingue il mutante. Esito: ok, il mutante con l'azzeramento viene preso.
- `tests/test_unit_voce_ascolto.py:347` — test parametrico con `finita()` rotta, `ferma()` rotta, ed entrambe. Controlla che `ferma` venga chiamata una volta per frase, che le frasi in fila vengano chiuse e che le righe di log ci siano. Rischio: con le guardie tolte l'eccezione uscirebbe dal turno. Esito: ok, l'eccezione salirebbe fuori da `turno` e il test la prende (ho controllato il percorso; i mutanti li ha provati l'agente). **R-668-2 chiusa.**
- `tests/test_unit_voce_ascolto.py:315` — conta gli svuotamenti del microfono al momento del secondo bip (2) e alla fine (+2). Rischio: il bip finisce nella nuova richiesta. Esito: ok. **R-668-3 chiusa.**
- `clients/voice/ascolto.py:255` — l'annotazione ora è `riproduci: Callable[[bytes], Optional[object]]` ed è coerente con `_ascolta_mentre_suona`, che accetta None (riproduzione già finita). Esito: ok. **R-668-4 chiusa.**
- `clients/voice/ascolto.py:415` — `_azzera()` all'inizio della risposta. Ho tolto la chiamata: mutante preso. Ho anche tolto `self.interrotto = False` a inizio turno: mutante preso (23 failed). Esito: ok.

**Prove eseguite**
- Suite voce sulla copia dell'indice: 152 passed e 21 failed. I 21 sono `test_installa_legge_il_env_come_gas` (20 casi) e `test_dotenv_usa_il_caricatore_di_gas`. Falliscono perché nel container manca il modulo openai, e lo stesso test dotenv fallisce anche sulla base 2c8cd2a.
- 152 passed qui contro i 173 dell'agente: la differenza sono questi stessi 21 test.
- 147 passed alla #668 + 5 test nuovi = 152.
- 6 mutanti: 5 presi e 1 sopravvissuto (vedi R-669-2), che non cambia il comportamento.

**Riserve**
- **R-669-1 BASSA** — Quando si arriva al tetto, l'interruzione ferma Gas ma non c'è né bip né nuova richiesta: si torna ad aspettare la parola in silenzio. Con `GAS_VOICE_MAX_TURNI=1` la parola detta mentre Gas parla non apre mai una domanda. Il comportamento è corretto per R-668-1, ma `scripts/voce/LEGGIMI.md:8` promette «fa il bip e ascolta la nuova domanda». Basta una riga nel LEGGIMI, oppure un bip di errore al tetto.
- **R-669-2 COSMETICA** — Il mutante sopravvissuto è il `_azzera()` nel ramo dell'interruzione (`clients/voice/ascolto.py:527`). È ridondante: `registra` non usa il rilevatore, e il turno successivo, come la fine della conversazione, lo azzera già.
- **R-669-3 COSMETICA** — Prima di `tests/test_unit_voce_ascolto.py:369` c'è una sola riga vuota dopo la funzione precedente (regola di stile PEP8 E302).

**Cosa non ho verificato**
- Il comportamento vero sul Mac (afplay con Popen, eco delle casse, punteggi reali di openWakeWord con la soglia 0.7): non si può riprodurre nel container, che non ha afplay né microfono. Vale la prova dell'operatore.
- I 21 test di installa/dotenv: qui manca il modulo openai.

**Memoria**
- Riga #669 aggiunta in `.claude/agents/memoria_revisore.md` e salvata da sola nel commit 91f74aa con `scripts/commit_memoria_revisore.sh`.
- Lo staging non è cambiato (3 file, 398+/31-).
- Nessun `git stash`: le copie sono in scratchpad.
- Nessuna lezione nuova.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 154 a 173 casi. Riepilogo reale nel venv con requirements e requirements-dev:

```
173 passed in 20.06s
```

Mutanti, tutti presi: soglia normale al posto di quella dell'interruzione (1 FAILED), niente ferma (5), niente break (1), interrotto ignorato in conversazione (1), volume al posto della parola (1), azzeramento dei turni rimesso (1), svuota dopo il bip tolto (1), guardia di finita tolta (2), guardia di ferma tolta (2). Nessun FAIL fuori scope nel mio ambiente.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Check della PR #336 su e619103, letti con `pull_request_read`:

```
handoff-check  success
unit-suite     in_progress (run 42085956774)
verifica-bot   failure (verdetto testuale APPROVATO CON RISERVE, parser che legge un MEDIA inesistente)
```

Mappatura commit → run:
- e619103: CI run 42085956774 — handoff-check success, unit-suite in corso alla scrittura.
- ef65e42: run del suo push non letta (pushato da solo prima di aprire la PR).
- Commit di fine-task che registra i verdetti: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-669-1 BASSA: al tetto dei turni la parola ferma Gas ma non fa né bip né nuova domanda; il LEGGIMI promette il bip.
- R-669-2 COSMETICA: `_azzera()` ridondante nel ramo dell'interruzione.
- R-669-3 COSMETICA: una riga vuota mancante in un test (PEP8 E302).
- Bot V-1 su fc1cab7 (ancora aperta): fra una frase e l'altra il microfono non si legge.
- Da provare sul Mac: eco delle casse contro la soglia 0.7, afplay fermato davvero.
- PR #333: bot V-2 su 83b0975 COSMETICA (§3/§6 dell'handoff di allora), in stato_progetto.
- Restano le riserve della fetta 40 e precedenti, elencate in `reports/stato_progetto.md`.
