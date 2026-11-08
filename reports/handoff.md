# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-08 — Voce: riserve BASSE della PR #350 (compiti finiti detti a voce) (chat M2, coordinata da M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta: con riserve BASSE serve il sì dell'operatore via M1 (CLAUDE.md §10).
2. Prova sul Mac: compito lungo a voce → avviso Telegram → alla prossima attivazione (anche solo «Gas») Gas lo dice per primo.

---

## §1 SCOPE & ESITO FETTE

- **PR #350** (fetta 3.2): `MERGIATA` (9b6b2fa) col sì dell'operatore via M1 (8 nov); Mani avvisato per la #351.
- **Fetta BASSE della #350**: `FATTA` — segno di lettura dei compiti solo dopo la consegna (ve #350 V-1, bot V-1); con risposta vuota la frase dei compiti si dice lo stesso (R-710-1-M2); la sola parola di attivazione («Dimmi.») dice i compiti, mai nel seguito (bot #350 V-5); file temporanei con nome unico fra thread (ve #350 V-3); test dei rami audio+testo e audio/mpeg (bot #350 V-1 su 40c5b30). Review #711-M2 APPROVATO CON RISERVE (R-711-1/2-M2 BASSE, R-711-3-M2 COSMETICA).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 modules/sottofondo/__init__.py     |   3 +-
 modules/voice/server.py            |  55 +++++++++++++++----
 reports/diff_sessione.md                        | n/d
 reports/handoff.md                              | n/d
 reports/ripartenza_m2.md                        | n/d
 reports/stato_progetto.md                       | n/d
 reports/ultimo_report.md                        | n/d
 tests/test_unit_sottofondo.py      |  14 +++++
 tests/test_unit_voice_server.py    | 108 +++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — i report si scrivono in questo stesso commit di fine task; riga di totale tolta. Base: origin/main 9b6b2fa (merge della #350).

## §3 GIT LOG --ONELINE (sessione)

```
19167e0 fix(voce): riserve BASSE della #350 — compiti segnati letti solo dopo la consegna, «Dimmi.» dice i compiti, risposta vuota, file temporanei unici, test dei rami mancanti (sì dell'operatore via M1)
beee8ae chore(revisore): memoria review #711 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Review #711-M2 sul commit 19167e0 (verdetto integrale):

## VERDETTO: APPROVATO CON RISERVE

Review #711-M2. Diff staged su feat/voce-v12-m2, base 9b6b2fa: 4 file, +168/−12. Prima di revisionare ho letto CLAUDE.md (§5, §8, §9), reports/stato_progetto.md (righe 615 e seguenti, riserve aperte della fetta 3) e .claude/agents/memoria_revisore.md (lezioni #709/#710-M2). Nessuno slicing della history, nessuna simulazione di tool, guardrail intatti. git stash non usato: ho copiato l'index nello scratchpad con checkout-index.

**Elementi esaminati**
- modules/voice/server.py:691 — `_compiti_finiti` ora salva solo `self._finiti_jobs` e non segna più. Rischio: compiti segnati prima della consegna (ve #350 V-1). Esito: ok.
- modules/voice/server.py:697 — `_segna_finiti_letti`: legge `_finiti_jobs`, lo azzera PRIMA di scrivere e intercetta ogni eccezione con `log.warning` (§9). Rischio: segno doppio o crash. Esito: ok. Un secondo richiamo trova None ed esce.
- modules/voice/server.py:853 — formato a pezzi: il segno parte quando `i + 1 == n_prefisso`, dopo che `riga()` è riuscita. Se la sintesi fallisce o il client chiude prima, si esce dal ciclo e non si segna nulla. Esito: ok. Il mutante «segno prima di riga()» viene preso da tests/test_unit_voice_server.py:1815.
- modules/voice/server.py:889 — `_do_tts_response`: il segno parte dopo `_send_audio`. `wfile.write` su un client chiuso solleva l'eccezione prima del segno, e con i 502 si esce prima. Esito: ok. Coperto da tests/test_unit_voice_server.py:1880 per il caso riuscito.
- modules/voice/server.py:774 — la guardia `not (text.strip() or prefisso)` e la lambda `resto` (:783) escludono le frasi della risposta quando è vuota, e il prefisso si dice lo stesso. Chiude R-710-1-M2. Esito: ok, test a tests/test_unit_voice_server.py:1843.
- modules/voice/server.py:539 — la sola parola di attivazione legge i compiti solo se non siamo nel seguito. `prefisso` arriva in tutti e tre i rami di `_rispondi_senza_turno`, e il ramo a testo (:721) segna. Rischio privacy (lettura nel seguito): escluso, test a tests/test_unit_voice_server.py:1862. Esito: ok.
- modules/sottofondo/__init__.py:47 — il nome temporaneo diventa `.tmp.<pid>.<token_hex(4)>`. `secrets` è già importato e `_pulisci_vecchi` (modules/sottofondo/__init__.py:248) riconosce ancora «.tmp.». Esito: ok.
- modules/voice/server.py:797 — ramo MP3 unico: il segno parte dopo la sintesi ma PRIMA di `_send_json` (:806). Esito: riserva R-711-2-M2.

**Istanza del handler per richiesta**: protocol_version non è impostato, quindi resta HTTP/1.0: una connessione per richiesta, un'istanza per richiesta. `_finiti_jobs` non può arrivare da un'altra richiesta.

**Test (rieseguiti su una copia dell'index)**: tests/test_unit_voice_server.py + tests/test_unit_sottofondo.py: 200 passed. Mutanti provati:
- segno prima di riga() nel formato a pezzi: PRESO.
- segno prima della sintesi nel ramo MP3 unico: SOPRAVVIVE (16/16 f32 verdi).

**Riserve**
- R-711-1-M2 BASSA: manca un test con sintesi fallita nei rami audio+testo (MP3 unico) e audio/mpeg (502). Il mutante che anticipa il segno a modules/voice/server.py:797 passa inosservato.
- R-711-2-M2 BASSA: nei rami JSON il segno precede la scrittura (`_send_json`), cioè ramo a testo :669/:721, MP3 unico :797 e senza chiave a schermo :779. Se il client chiude durante la scrittura, i compiti risultano letti ma non sono arrivati. Nei pezzi e in audio/mpeg invece il segno segue l'invio. Correzione di una riga per ramo: spostare il segno dopo `_send_json`.
- R-711-3-M2 COSMETICA: `_finiti_jobs` non viene azzerato in do_POST come `_capito` (:476). Oggi è innocuo per via di HTTP/1.0. In più c'è la lambda `resto` con `noqa: E731`.

**Cosa non ho verificato**
- Comportamento reale col client sul Mac e con ElevenLabs vero: non riproducibile in dev, tutto è mockato.
- Concorrenza vera fra thread su `segna_letti`/`_scrivi_privato`: c'è solo il test sui nomi, nessuno stress test.
- Una scrittura TCP riuscita non prova che il client abbia riprodotto l'audio. È un limite accettato, non verificabile lato server.

Memoria aggiornata con la riga #711-M2 più una lezione, committata (beee8ae) in /home/user/Gas/.claude/agents/memoria_revisore.md. Il diff staged non è stato toccato (4 file, +168/−12).

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voice_server.py`: 126 passed (prima 118), 8 nuovi f32b — sintesi fallita non segna letti; senza schermo segnati appena dette le frasi dei compiti; risposta vuota dice comunque i compiti; sola parola di attivazione («Gas.», «Hey Jarvis!») dice i compiti prima di «Dimmi.»; nel seguito no; ramo audio+testo (MP3 unico); ramo audio/mpeg diretto (round-trip del server voce col kernel finto). Col server di main 4 di questi falliscono. `tests/test_unit_sottofondo.py`: 74 passed (+1: nomi temporanei unici). `gas.py` non toccato.

## §6 STATO CI

`gh` non autenticato nel cloud. I commit sono pushati insieme a questo report: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-711-1-M2 BASSA: nessun test con sintesi fallita nei rami MP3 unico e audio/mpeg.
- R-711-2-M2 BASSA: nei rami JSON il segno di lettura precede la scrittura della risposta (client chiuso durante l'invio → compiti letti ma non arrivati).
- R-711-3-M2 COSMETICA: `_finiti_jobs` non azzerato a inizio richiesta (innocuo con HTTP/1.0); lambda con noqa.
- Dalla fetta 3.2: R-709-1-M2 (pulizia dei 7 giorni dalla lettura), R-709-2-M2 (frase non nella storia); doppia lettura con due richieste contemporanee.
- Dal sottofondo: R-708-1-M2, R-707-1-M2, R-706-1-M2, R-701-3-M2, R-703-2-M2, R-696-1-M2, bot #349 (a9a17a5) V-1/V-2.
- Non verificato in dev: client vero sul Mac, ElevenLabs vero.
