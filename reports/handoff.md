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
- **Fetta 3.3** (passaggio automatico al sottofondo oltre N giri): `DEFERITA — opzionale`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 modules/sottofondo/__init__.py     | 65 +++++++++++++++++++++++++++++++++
 modules/voice/server.py            | 22 ++++++++++++
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_sottofondo.py      | 43 ++++++++++++++++++++++
 tests/test_unit_voice_server.py    | 73 ++++++++++++++++++++++++++++++++++++--
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main f4ece4e (merge della #349).

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_sottofondo.py`: 72 passed (prima 70): `da_leggere` filtra (stato, già letti, oltre 24 ore, «fine» non numerico, nome ≠ id), ordina e limita a 2; `frase_finiti` corta; `segna_letti` non scrive fuori dalla cartella. `tests/test_unit_voice_server.py`: 5 nuovi f32 (lettura alla prossima attivazione e niente ripetizione — round-trip del server voce col kernel finto; testo non legge e non segna; compito fallito e compito vecchio; errore della coda non rompe la risposta; seguito non legge), suite 115 passed prima del cambio di base (i file del server e dei test sono identici su main da allora). Mutante «legge anche nel seguito» → 1 failed. `gas.py` non toccato: suite kernel non rilanciata.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-709-1-M2 BASSA: `segna_letti` rinnova la data del file, quindi la pulizia dei 7 giorni parte dalla lettura (al massimo +24 ore).
- R-709-2-M2 BASSA: la frase sui compiti detta a voce non entra nella storia; chiunque attivi Gas nella stanza sente il risultato (stesso rischio di ogni risposta a voce).
- Due richieste a voce contemporanee possono leggere lo stesso compito due volte (non riprodotto, finestra minima).
- Dal sottofondo restano aperte: R-706-1-M2, R-707-1-M2, R-708-1-M2, R-701-3-M2, R-703-2-M2, R-696-1-M2, bot #349 (a9a17a5) V-1/V-2 (compito «in_corso» mai cancellato dalla pulizia; `_ultima_pulizia` con l'orologio di sistema).
- Non verificato in dev: sintesi vera di una frase lunga (~760 caratteri) sul Mac, processo vero con `claude -p`, avviso Telegram vero.
