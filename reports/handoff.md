# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — Voce, fetta 3.2: compiti in sottofondo finiti detti a voce alla prossima attivazione (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: con riserve BASSE serve il sì dell'operatore via M1 (CLAUDE.md §10).
2. Prova sul Mac: a voce un compito lungo → «ci lavoro», avviso su Telegram, poi alla prossima attivazione a voce Gas dice per primo che il compito è finito.

---

## §1 SCOPE & ESITO FETTE

- **PR #349** (seconda fetta BASSE del sottofondo): `MERGIATA` (f4ece4e) col sì dell'operatore via M1; Mani avvisato per la sua #348.
- **Fetta 3.2** (proposta `reports/proposta_fetta3_sottofondo.md`, «lettura della coda dei finiti alla prossima attivazione»): `FATTA` — `sottofondo.da_leggere` / `frase_finiti` / `segna_letti`; `VoiceHandler._con_compiti_finiti` solo nei turni a voce di attivazione (mai nel seguito, cioè parlato della stanza; mai a testo), al massimo 2 compiti finiti nelle ultime 24 ore, titolo e riassunto corto, segnati letti. Review #709-M2 APPROVATO CON RISERVE (R-709-1/2-M2 BASSE).
- **Correzioni dopo bot e verifica esterna #350** (commit 5b83fb2): `FATTE` — la frase dei compiti si dice per prima FUORI dal limite di 3 frasi/400 caratteri della parte parlata (bot V-1: prima poteva togliere tutto lo spazio alla risposta), test per due compiti lunghi, client senza schermo e senza chiave TTS (bot V-2); niente «:» con risposta vuota (ve V-2). Review #710-M2 APPROVATO CON RISERVE. Bot #350 su 382eab3 APPROVATA, verifica esterna APPROVATO CON RISERVE (BASSE).
- **Fetta 3.3** (passaggio automatico al sottofondo oltre N giri): `DEFERITA — opzionale`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +
 modules/sottofondo/__init__.py     |  67 +++++++++++++++
 modules/voice/server.py            |  48 +++++++++--
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_sottofondo.py      |  51 ++++++++++++
 tests/test_unit_voice_server.py    | 108 +++++++++++++++++++++++-
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main f4ece4e (merge della #349).

## §3 GIT LOG --ONELINE (sessione)

```
5b83fb2 fix(voce): fetta 3.2 — frase dei compiti finiti fuori dal limite della parte parlata (bot #350 V-1/V-2); niente «:» con risposta vuota (ve #350 V-2)
50de38d chore(revisore): memoria review #710 — APPROVATO CON RISERVE
382eab3 docs(voce): report di fine task — fetta 3.2 (compiti finiti detti a voce); PR #349 mergiata (chat M2)
cf5caf0 feat(voce): fetta 3.2 — alla prossima attivazione a voce Gas dice i compiti in sottofondo finiti (sì dell'operatore via M1) (chat M2)
5896e04 chore(revisore): memoria review #709 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #709-M2 sul commit cf5caf0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #709-M2. Diff staged su feat/voce-v12-m2 (base f4ece4e): 4 file, +201/−2. Prima della review ho letto CLAUDE.md, le parti di reports/stato_progetto.md che riguardano il sottofondo, la mia memoria e le parti della proposta che servivano. Ho rilanciato io i test: tests/test_unit_sottofondo.py 72 passed; tests/test_unit_voice_server.py -k f32 5 passed. La suite completa del server voce non l'ho rilanciata, perché supera il tempo limite del comando.

**Elementi del diff esaminati**
- `modules/voice/server.py:656` — chiama `_con_compiti_finiti` solo se `is_audio and not self._seguito()`, dopo i rami del seguito (serve_attivazione, «non per me», registra_seguito) e prima di tutte e tre le uscite (audio+testo/righe, tts, json). Rischi esaminati: lettura nel seguito, cioè parlato della stanza senza parola di attivazione, e lettura nei turni a testo. Esito: ok. `_seguito()` (`modules/voice/server.py:712`) vale solo per il parlato. I test f32 «testo non legge» e «seguito non legge» coprono entrambi i casi, e i compiti non letti restano in coda.
- `modules/voice/server.py:669` — `_con_compiti_finiti`: import pigro, `kernel.root` assente porta alla risposta invariata, un unico try/except con `log.warning`. Rischio esaminato: un'eccezione della coda che rompe la risposta, contro il §9. Esito: ok, coperto dal test con `da_leggere` che solleva. Il segno di lettura viene scritto prima dell'invio: se la sintesi vocale fallisce, il compito non si ripete. È accettabile perché la risposta è già arrivata su Telegram.
- `modules/sottofondo/__init__.py:478` — `_ore_lettura`: `_numero_env` porta nan/inf al default, `max(1.0, …)`, e `isfinite(ore*3600)` gestisce un valore enorme (1e308). Rischio esaminato: un limite di tempo infinito o nan che legge tutti i compiti, o nessuno. Esito: ok.
- `modules/sottofondo/__init__.py:483` — `da_leggere`: salta `attivo.json`, i file illeggibili, gli stati diversi da ok/ko, quelli già letti, quelli con id non stringa o nome diverso dall'id, e i `fine` non numerici o non finiti. Ordina dal più vecchio e ne prende al massimo 2. I file temporanei (`.tmp.<pid>`) non passano il glob `*.json`. Rischio esaminato: file estranei o corrotti nella cartella. Esito: ok.
- `modules/sottofondo/__init__.py:525` — `segna_letti`: rilegge il file, aggiorna solo gli stati ok/ko, ricava il percorso con `Path(id).name` (contiene `../../fuori`, come prova il test) e scrive in modo atomico con permessi 0600. Rischio esaminato: una scrittura fuori dalla cartella o la sovrascrittura di un compito ancora aperto. Esito: ok. Una riserva sulla durata dei dati (R-709-1-M2, sotto).
- `modules/sottofondo/__init__.py:512` — `frase_finiti`: titolo fino a 80 caratteri e risposta fino a 250, passati da `_breve` (`modules/sottofondo/__init__.py:384`, che usa `str()` ed è robusto ai tipi strani). Per i ko dice solo «non è riuscito», senza leggere l'errore. Rischio esaminato: privacy dei dati dell'operatore detti ad alta voce. Esito: riserva BASSA (R-709-2-M2). Il rischio è coerente con il modello voce attuale: `in_sottofondo` si può avviare solo a voce (contesto: `gas.py:4594`), quindi la persona attivata con la parola di Gas è chi ha chiesto il compito.

**Riserve (da tracciare in stato_progetto.md)**
- **R-709-1-M2 BASSA**: `segna_letti` riscrive il file e ne rinnova la data di modifica. `_pulisci_vecchi` (`modules/sottofondo/__init__.py:229`) cancella i finiti in base a quella data, quindi i dati del compito restano 7 giorni dalla lettura invece che dalla fine. Lo sforamento è al massimo di 24 ore, perché la lettura avviene entro 24 ore dalla fine.
- **R-709-2-M2 BASSA**: la frase sui compiti detta a voce non entra nella storia, dove è registrata solo la risposta del modello. Se l'operatore chiede «cosa hai detto?», il modello non sa del compito appena letto. Sul fronte privacy, chiunque attivi Gas nella stanza sente il risultato del compito: è lo stesso rischio di oggi per qualsiasi domanda a voce, non uno nuovo.

**Coerenza col progetto**: le modifiche toccano solo il server voce (competenza di M2) e il modulo del sottofondo. Il client dell'ascolto e `bot.py` di Mani non sono toccati. Nessuna simulazione dell'output dei tool, nessun taglio diretto della storia, e il cap di 10 iterazioni e `_get_window` non sono toccati. La fetta rispetta la proposta (`reports/proposta_fetta3_sottofondo.md`, punto «lettura della coda dei finiti alla prossima attivazione»).

**Rischio escluso**: non ho verificato due richieste a voce contemporanee, che potrebbero leggere lo stesso compito due volte (non riprodotto in dev; finestra trascurabile, senza lock). Non ho verificato nemmeno la resa della sintesi vocale sul Mac o sulla VPS con testo lungo fino a circa 760 caratteri: in dev la sintesi è finta. Non ho fatto prove con mutanti: mi sono basato su quella dichiarata dall'agente («legge anche nel seguito», 1 failed).

**Memoria**: aggiunta la riga #709-M2 e una lezione (la pulizia che si basa sulla data di modifica sposta la durata dei dati quando un segno di lettura riscrive il file) in /home/user/Gas/.claude/agents/memoria_revisore.md, già committata con 5896e04.

Review #710-M2 sul commit 5b83fb2 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #710-M2: branch feat/voce-v12-m2, base HEAD 382eab3, diff staged di 4 file (+75/−20). Ho letto CLAUDE.md (sez. 5), stato_progetto.md (letto in parte) e la mia memoria. Nel diff non c'è slicing della history, nessun output di tool simulato e non viene toccato nessun guardrail del kernel (cap delle iterazioni, `_get_window`).

**Cosa ho esaminato nel diff**
- `modules/voice/server.py:657` — `finiti` viene calcolato solo se `is_audio and not self._seguito()`. Rischio esaminato: che i compiti vengano letti nel seguito (cioè nel parlato della stanza). Esito: ok, la condizione è la stessa di prima.
- `modules/voice/server.py:746` — a schermo `content` è prefisso + riga vuota + testo; `extra` resta dopo. Rischio esaminato: che i chiamanti esistenti si rompano (`_rispondi_senza_turno`, `modules/voice/server.py:695`, non passa `prefisso`). Esito: ok, il default "" lascia il comportamento identico.
- `modules/voice/server.py:757` e `modules/voice/server.py:766` — le frasi del prefisso stanno davanti a `frasi_parlate`, a `frasi_voce` o a `parte_parlata`, fuori dal loro limite. Rischio esaminato: un parlato senza tetto. Esito: ok, il prefisso è già limitato (al massimo 2 compiti, titolo di 80 caratteri, riassunto di 250 per `LETTURA_RISPOSTA_MAX`).
- `modules/voice/server.py:751` — `if not text.strip(): pass` resta legato al solo testo del modello. Rischio esaminato: risposta vuota con prefisso presente. Esito: **riserva** (R-710-1-M2, sotto).
- `modules/voice/server.py:662` — nel ramo audio/mpeg il testo diventa prefisso + spazio + testo. Rischio esaminato: un limite che taglia la risposta. Esito: ok, `_do_tts_response` (`modules/voice/server.py:827`) sintetizza il testo intero, senza `parte_parlata`.
- `modules/sottofondo/__init__.py:521` — con risposta vuota, None o solo spazi la frase si chiude con «.» invece di «:». Rischio esaminato: un None che finisce nella f-string. Esito: ok, `_breve` lo normalizza con `str(testo or "")`.
- `tests/test_unit_voice_server.py:1774` e `tests/test_unit_voice_server.py:1799`, più `tests/test_unit_sottofondo.py:776` — test nuovi. Esito: ok. Ho rieseguito: sottofondo 73 passed, f32 8 passed. In un worktree a HEAD 382eab3 con i test nuovi falliscono 3 test: i 2 f32 citati qui e `test_frase_finiti_risposta_vuota`. Il test del client H24 passa anche a HEAD: blocca il comportamento ma non prova la correzione, ed è dichiarato così.

**Riserve**
- **R-710-1-M2 (BASSA)**: se la risposta del modello è vuota o fatta solo di spazi, il ramo `if not text.strip(): pass` (`modules/voice/server.py:751`) salta del tutto la sintesi, quindi il prefisso non viene detto. Intanto `_compiti_finiti` ha già segnato i compiti come letti. Sul client senza schermo (audio+pezzi) quei compiti si perdono. Prima di questa modifica la frase era fusa nel testo, che quindi non era vuoto, e veniva detta. È un piccolo passo indietro, in un caso raro. Rimedio: guardia `if not (text.strip() or prefisso)`, più un test.
- **R-710-2-M2 (COSMETICA)**: tre righe vuote prima di `tests/test_unit_sottofondo.py:776` (PEP8 E303). È lo stesso difetto di R-707-2-M2.
- Restano aperte e non toccate da questo diff: ve #350 V-1 (segno di lettura scritto prima dell'invio, che peggiora R-710-1) e V-3 (`.tmp.<pid>`).

**Cosa NON ho verificato**
- Il comportamento reale con ElevenLabs e sul client H24 del Mac: non riproducibile in dev, i test usano un TTS finto.
- Non ho rieseguito l'intero `test_unit_voice_server.py` (270 s): solo il sottoinsieme f32. Mi fido del 118 passed dichiarato.
- Non ho verificato lato client il rendering di `\n\n` nella pagina.

- Memoria aggiornata con la riga #710-M2 e una lezione: quando un contenuto diventa un parametro separato, vanno ricontrollate le guardie sul testo vuoto. Commit 50de38d, fatto con `scripts/commit_memoria_revisore.sh`, solo `/home/user/Gas/.claude/agents/memoria_revisore.md`.

File di riferimento:
- /home/user/Gas/modules/voice/server.py
- /home/user/Gas/modules/sottofondo/__init__.py
- /home/user/Gas/tests/test_unit_voice_server.py
- /home/user/Gas/tests/test_unit_sottofondo.py
- /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_sottofondo.py`: 73 passed (prima 70; +1 in 5b83fb2: risposta vuota): `da_leggere` filtra (stato, già letti, oltre 24 ore, «fine» non numerico, nome ≠ id), ordina e limita a 2; `frase_finiti` corta; `segna_letti` non scrive fuori dalla cartella. `tests/test_unit_voice_server.py`: 5 nuovi f32 (lettura alla prossima attivazione e niente ripetizione — round-trip del server voce col kernel finto; testo non legge e non segna; compito fallito e compito vecchio; errore della coda non rompe la risposta; seguito non legge), 3 nuovi f32 in 5b83fb2 (due compiti lunghi in audio+testo+pezzi, client audio+pezzi, senza chiave TTS); suite intera 118 passed. Mutante «legge anche nel seguito» → 1 failed. `gas.py` non toccato: suite kernel non rilanciata.

## §6 STATO CI

`gh` non autenticato nel cloud. Su 382eab3: handoff-check e verifica-bot verdi (bot APPROVATA), unit-suite in corso alla verifica esterna. I commit nuovi sono pushati insieme a questo report: run non ancora disponibile alla scrittura.

## §7 RISERVE APERTE

- R-709-1-M2 BASSA: `segna_letti` rinnova la data del file, quindi la pulizia dei 7 giorni parte dalla lettura (al massimo +24 ore).
- R-709-2-M2 BASSA: la frase sui compiti detta a voce non entra nella storia; chiunque attivi Gas nella stanza sente il risultato (stesso rischio di ogni risposta a voce).
- R-710-1-M2 BASSA: con risposta del modello vuota la sintesi salta e la frase dei compiti (già segnati letti) non viene detta. R-710-2-M2 COSMETICA: righe vuote in più nel test.
- Ve #350 V-1 BASSA: il segno di lettura si scrive prima dell'invio a voce (se la sintesi fallisce il compito non si ridice). Ve #350 V-3 BASSA: `.tmp.<pid>` uguale per due thread dello stesso processo.
- Due richieste a voce contemporanee possono leggere lo stesso compito due volte (non riprodotto, finestra minima).
- Dal sottofondo restano aperte: R-706-1-M2, R-707-1-M2, R-708-1-M2, R-701-3-M2, R-703-2-M2, R-696-1-M2, bot #349 (a9a17a5) V-1/V-2 (compito «in_corso» mai cancellato dalla pulizia; `_ultima_pulizia` con l'orologio di sistema).
- Non verificato in dev: sintesi vera di una frase lunga (~760 caratteri) sul Mac, processo vero con `claude -p`, avviso Telegram vero.
