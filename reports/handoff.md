# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-05 — chat Mani, fetta 43 parte 2: finestra di 40 s e difese contro il parlato della stanza (PR #341)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #341 (https://github.com/Gasss23/Gas/pull/341). Review #676 APPROVATO CON RISERVE e PR nel perimetro: decide l'operatore tramite M1. Numero e URL dalla risposta dello strumento GitHub `create_pull_request`.

---

## §1 SCOPE & ESITO FETTE

- **PR #340 (fetta 42)**: `FATTA` — mergiata (83f3bcd) col sì dell'operatore, CI verde; riserve nuove di bot e verifica esterna registrate.
- **Fetta 43 parte 2 — finestra di 40 s, turni di seguito con tetto 15 s, X-Gas-Seguito, comandi fine/pausa**: `FATTA` — review #676 APPROVATO CON RISERVE. Il commit di merge su main ha un diff identico a quello rivisto.
- **R-676-1/2 (test di stato e svuota dopo «fine»)**: `DEFERITA — BASSE, registrate, prossima fetta della voce`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 clients/voice/ascolto.py           | 144 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------
 reports/diff_sessione.md           |  14 +++++++-------
 reports/stato_progetto.md          |   6 ++++--
 reports/ultimo_report.md           |  25 +++++++++++--------------
 scripts/voce/LEGGIMI.md            |  28 +++++++++++++++++++++-------
 tests/test_unit_voce_ascolto.py    | 230 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 83f3bcd.

## §3 GIT LOG --ONELINE (sessione)

```
51c4aa0 Merge branch 'mani/finestra' into claude/peaceful-lovelace-0w2b7q
4cd7b97 feat(voce): fetta 43 parte 2 — finestra di 40 s e difese contro il parlato della stanza
da24b2c chore(revisore): memoria review #676 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 4cd7b97 — review #676, verdetto integrale. Il commit 51c4aa0 (merge su main dopo la #340) ha un diff identico, verificato confrontando i diff:

## VERDETTO: APPROVATO CON RISERVE

Review #676 (chat Mani). Riguarda la fetta 43 parte 2, cioè le difese contro il parlato della stanza nel client di ascolto. Ho lavorato nel worktree /tmp/claude-0/wt43b sul diff staged (3 file: ascolto.py, LEGGIMI, test).

**Cosa ho controllato**
- Ho letto prima CLAUDE.md, stato_progetto.md e la mia memoria.
- Ho letto il server della #339 da origin/feat/voce-v12-m2:modules/voice/server.py.
- Ho fatto girare i test su una copia dell'index (non sul worktree): **248 passed**.
- Ho provato 4 mutanti miei sulla copia: 1 preso dai test, 3 no.
- Il codice del diff non contiene slicing della history né simulazione di tool.

**Citazioni**
- `clients/voice/ascolto.py:735` — se il server manda `X-Gas-Comando: fine`, l'invio restituisce `(True, None, "", "fine")` prima di guardare il Content-Type. Rischio: un JSON vuoto preso per un errore, con bip. Esito: ok. Torna col server della #339 (`_chiudi_seguito` risponde 200 con `{"content":"","fine":true}`, e `end_headers` mette l'intestazione in ogni formato). `_comando()` (riga 692) accetta solo «fine» e «pausa», e un'eccezione nella lettura diventa "".
- `clients/voice/ascolto.py:462` e `clients/voice/ascolto.py:508` — un errore o una risposta senza voce in un turno di seguito, o con «pausa», chiude senza bip. Dopo la parola il bip d'errore resta. Rischio: bip a ripetizione col forte spento (il server risponde 500 ai turni di seguito). Esito: ok. Anche i fake a 3 valori e gli esiti malformati vanno bene: l'IndexError o il TypeError finiscono nell'`except` (§9).
- `clients/voice/ascolto.py:627` — una registrazione di seguito che arriva al tetto (`registra(..., max_s=seguito_max_s)`) non si invia e chiude la conversazione. Rischio: soglia sbagliata di uno. Esito: ok, il mutante con `>` al posto di `>=` è preso dai test. Nota: il tetto conta anche gli 0,8 s di silenzio finale, quindi il parlato massimo che passa è circa 14,2 s. Va bene, nessuna azione.
- `clients/voice/ascolto.py:444` — `self.chiudi = False` all'inizio di ogni turno. Rischio: se l'azzeramento manca, la conversazione dopo un «fine» o una «pausa» si chiude dopo il primo turno, senza finestra. Esito: **riserva**. Il codice è giusto, ma il mutante «riga tolta» passa tutti i 248 test.
- `clients/voice/ascolto.py:458` — una «pausa» dopo la parola, con audio, deve chiudere. Esito: **riserva**. Il mutante `if comando == "pausa" and seguito` sopravvive: `tests/test_unit_voce_ascolto.py:520` prova solo la pausa di seguito e `tests/test_unit_voce_ascolto.py:527` solo quella senza audio. Con quel mutante «Hey Jarvis, pausa» suonerebbe «Va bene.» e lascerebbe la finestra aperta 40 s.
- Contesto, interruzione: dopo una parola che interrompe si torna a `seguito = False` e la registrazione torna a 30 s. Coperto dai due test sull'interruzione. Ok.
- `scripts/voce/LEGGIMI.md` — tabella e privacy aggiornate (40 s, 15 s, «pausa», chiusura in silenzio, audio a Groq dichiarato). Ok. «40 secondi senza che nessuno parli» è un'approssimazione: in realtà sono 40 s in cui non arrivano 0,24 s di voce continua. Non serve correggerlo.

**Riserve**
- **R-676-1 BASSA** — Due mutanti sulla gestione dello stato passano tutti i test:
  - `self.chiudi` non azzerato in `turno`;
  - «pausa» che chiude solo nei turni di seguito.

  Da aggiungere:
  - un test con due conversazioni di fila: «fine» nella prima, poi la seconda deve ancora aprire un turno di seguito;
  - un test «parola + pausa con audio»: tipi == ["parola"], niente seguito.
- **R-676-2 BASSA** — Il `self._svuota()` dopo «fine» (ascolto.py:461) non è coperto: il mutante che lo toglie passa. Asserire una chiamata a svuota in più nel test di «fine».
- **R-676-3 BASSA**, per M2, fuori da questo diff — Nel server della #339, una trascrizione incerta in un turno di seguito risponde a voce «Non ho capito» (`_rispondi_senza_turno(_NON_HO_CAPITO)` in `_do_stt`) e non chiude. Il rumore della stanza nella finestra può quindi produrre fino a 5 «Non ho capito» parlati. Il caso è da girare a M2: con `_seguito()` attivo il server dovrebbe chiudere con «fine».

**Privacy**: la finestra passa da 12 a 40 s, quindi la stanza è ascoltata più a lungo. In cambio ogni turno di seguito porta al massimo circa 15 s di audio invece di 30, il parlato lungo non parte, e il server usa solo il cervello forte e chiude se il parlato non era per Gas. Il saldo è a favore della privacy, ma ogni turno di seguito arriva comunque a Groq per la trascrizione prima che il cervello decida. È scritto nel LEGGIMI ed è una scelta dell'operatore.

**Cosa non ho verificato**
- Il comportamento vero sul Mac (microfono, openWakeWord, rumore reale della stanza): non si può riprodurre qui. I tempi sono provati solo con blocchi sintetici.
- L'integrazione end-to-end client ↔ server della #339: non l'ho fatta girare. Il contratto l'ho controllato leggendo il codice; il server finto dei test copre solo intestazioni e codici.
- flake8: non è installato nell'ambiente, quindi lo stile (E30x) non è controllato.

**Memoria**: aggiunta la riga #676 (chat Mani) e una lezione nuova (un flag di stato per turno va provato su due conversazioni di fila) in .claude/agents/memoria_revisore.md. Committata con lo script: commit da24b2c, solo quel file. Lo staged è identico a prima. Il marcatore non l'ho toccato.

## §5 DELTA TEST DEL MOTORE

`tests/test_unit_voce_ascolto.py`: da 220 (main dopo la #340) a 248 casi. Riepilogo reale nel venv con requirements e requirements-dev:

```
248 passed in 28.02s
```

Mutanti presi (15):
- «fine» ignorato;
- pausa che non chiude;
- errore di seguito con bip;
- `chiudi` ignorato;
- parlato lungo inviato;
- tetto di seguito a 30 s;
- `seguito` sempre False;
- intestazione mancante;
- interruzione che resta di seguito;
- finestra a 12 s;
- comando sconosciuto accettato;
- risposta senza voce di seguito con bip;
- più 3 rinforzati dopo il primo giro.

I due mutanti di stato trovati dal revisore sono nella riserva R-676-1.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP).

Mappatura commit → run:
- 51c4aa0, 4cd7b97, da24b2c: pushati insieme prima di aprire la PR #341; run del push non letta alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-676-1 BASSA: due mutanti di stato sopravvivono (`self.chiudi` non azzerato; «pausa» che chiude solo nei turni di seguito).
- R-676-2 BASSA: lo svuota dopo «fine» non è coperto da test.
- R-676-3 BASSA, per M2 (girata a M1): trascrizione incerta di seguito → «Non ho capito» a voce invece di «fine».
- Dalla #340: bot V-1 BASSA (conferma non suonabile = silenzio), verifica esterna V-4 BASSA (eco dopo la conferma), R-675-1 BASSA.
- Restano le riserve delle fette 40, 41 e 43 parte 1, in `reports/stato_progetto.md`.
