# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-12 notte — Voce: la prima frase parte appena pronta (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (riserve solo BASSE).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — prima frase subito** (sul Mac dei tempi dell'11/11: prima frase pronta ~3,7 s dopo la richiesta ma arrivata al client a ~6,2 s, a turno finito): FATTA — 59478461, review #799-M1coord BOCCIATO → #801-M1coord APPROVATO CON RISERVE. Solo client senza schermo (audio+pezzi), mai nei seguiti, mai con compiti finiti da annunciare, mai se la prima frase contiene la parola di attivazione.
- **Fetta 2 — merge di main (#378) nella #379**: FATTA — review #802-M1coord APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 clients/voice/ascolto.py           |  11 ++++++++-
 modules/voice/server.py            | 118 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------
 reports/diff_sessione.md           |  13 +++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  15 ++++++-------
 tests/test_unit_voce_ascolto.py    |  25 +++++++++++++++++++++
 tests/test_unit_voice_server.py    | 135 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
37e729b8 docs(fine-task): handoff #379 dopo il merge di main
9a0fb748 Merge origin/main (#378) nella #379 — review #802-M1coord APPROVATO
e2766972 docs(fine-task): §2/§3 handoff
f7053b3d docs(fine-task): voce — prima frase subito (review #799/#801-M1coord)
59478461 perf(voce): la prima frase parte appena pronta, senza aspettare la fine del turno (~2 s prima) — review #799/#801-M1coord
37654b0f chore(revisore): memoria review #801 — APPROVATO CON RISERVE
382aae45 chore(revisore): memoria review #799 — BOCCIATO
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #799-M1coord (1° giro, diff staged poi corretto)

## VERDETTO: BOCCIATO

Review #799-M1coord: modifica staged su perf/voce-prima-frase-subito, base origin/main 3756c97. Letti prima CLAUDE.md (sezione 5), reports/stato_progetto.md e la memoria del revisore.

**Motivo del blocco (MEDIA, verificato con una prova)**
Con compiti finiti da annunciare (prefisso, fetta 3.2) la prima frase della risposta si sente due volte e l'annuncio finisce in mezzo alla risposta.
- In `_do_pezzi_response` la prima frase si toglie solo se `frasi[0]` è uguale alla frase anticipata (modules/voice/server.py:1274). Con il prefisso `frasi` è prefisso + risposta (modules/voice/server.py:1238-1242), quindi `frasi[0]` è la frase del prefisso: il confronto fallisce.
- I compiti finiti si leggono solo dopo il turno (modules/voice/server.py:1105), quando la prima frase è già partita.
- Prova (spazio temporaneo, `_voce_subito` con `_compiti_finiti` = "Ho finito il compito."): audio `['Uno.', 'Ho finito il compito.', 'Uno.', 'Due.']`; la riga del testo dice `pezzi: 3`, gli audio sono 4.
- Correzione suggerita: calcolare `_compiti_finiti()` prima di `run_turn` e passare `pronto=None` se ci sono compiti da annunciare; test col prefisso.

**Elementi del diff esaminati**
- modules/voice/server.py:691 — `_invia_anticipo`: blocca la frase con la parola di attivazione; sotto `_risposta_lock` scrive intestazioni e riga solo se lo stato è «attesa»; lo stato passa a «chiusa» prima della scrittura. Rischio: due fili sulla stessa connessione. Esito: ok (HTTP/1.0, una richiesta per gestore; errore di scrittura catturato in `_sintetizza`, modules/voice/server.py:467-471).
- modules/voice/server.py:714 — `_prendi_risposta`. Rischio: una via di risposta che non passa da qui. Esito: ok con riserva: `_send_json` (modules/voice/server.py:726) e `_do_pezzi_response` (modules/voice/server.py:1271) ci passano; `_send_audio` (modules/voice/server.py:753) no, oggi irraggiungibile con l'anticipo acceso.
- modules/voice/server.py:726-742 — errore dopo l'anticipo: riga `errore_voce` + `fine`, stato HTTP già 200. Esito: riserva R2.
- modules/voice/server.py:1044-1047 — invio immediato solo con `_vuole_righe_senza_schermo()` e fuori dai seguiti (modules/voice/server.py:1041). Rischio: privacy. Esito: ok.
- clients/voice/ascolto.py:727 (contesto) — controllo della parola a ogni pezzo; la frase anticipata per costruzione non contiene la parola; `test_regola_della_parola_uguale_al_client` (tests/test_unit_voice_server.py:2804). Esito: ok.

**Riserve**
- R1 (BASSA): se la risposta finale cambia rispetto alla frase anticipata si sente una frase in più (es. "Ecco\n\nIl resto."): da dichiarare.
- R2 (MEDIA, esperienza): errore del turno dopo l'anticipo → nessun bip (prima, col 500, `_bip("errore")`); l'utente sente solo la prima frase e poi silenzio.
- R3 (COSMETICA): `_send_audio` non passa da `_prendi_risposta`.

**Test**: voice_server + voce_ascolto 567 passed (rieseguiti). Kernel non rieseguito (gas.py non toccato).

**Non verificato**: tempi reali sul Mac, `claude -p` vero, ElevenLabs vero; scrittura lenta con client bloccato (lucchetto fino al timeout di 60 s del socket, ragionato).

**Memoria**: riga #799-M1coord e una lezione (commit 382aae45).

### Review #801-M1coord (2° giro, commit 59478461)

## VERDETTO: APPROVATO CON RISERVE

Review #801-M1coord, secondo giro della #799. Diff staged riletto: 4 file, +277/-12. Il blocco della #799 è risolto: con un compito finito già pronto prima del turno la prova dà `['Ho finito il compito.', 'Uno.', 'Due.']` (prima `['Uno.', 'Ho finito il compito.', 'Uno.', 'Due.']`).

**Elementi del diff esaminati**
- modules/voice/server.py:1052 — con compiti da annunciare l'invio anticipato si spegne (`pronto=None`); solo senza schermo e mai nei seguiti (dentro `not self._seguito()`). Rischio: effetti della lettura prima del turno. Esito: ok — `_compiti_finiti` (modules/voice/server.py:1131) non solleva e scrive solo `_finiti_jobs`; la lettura dopo il turno (modules/voice/server.py:1115) lo sovrascrive; se i compiti spariscono `_segna_finiti_letti` non è chiamato (`n_prefisso` 0): innocuo.
- modules/voice/server.py:1285 — dopo un anticipo la frase si cerca in `frasi[n_prefisso]` e si toglie solo quella; prefisso e `n_prefisso` invariati. Rischio: segno dei compiti letti, ripetizioni. Esito: ok; riserva sull'ordine (R-801-1).
- modules/voice/server.py:754-759 — `_send_audio` passa da `_prendi_risposta`; dopo un anticipo `_send_json(500)` scrive la riga d'errore. Esito: ok (chiude R3).
- modules/voice/server.py:726-737 — errore del turno dopo un anticipo con `"errore_turno": true`; clients/voice/ascolto.py:1035 lo registra; clients/voice/ascolto.py:754 suona `_bip("errore")` se almeno una frase è stata detta; errore della sola sintesi senza bip come prima; con 0 frasi resta il ramo vecchio (niente doppio bip). Esito: ok (chiude R2).
- Sicurezza fra i due fili (`_invia_anticipo` modules/voice/server.py:691, `_prendi_risposta` modules/voice/server.py:717) invariata rispetto alla #799.

**Test**: voice_server + voce_ascolto 570 passed (236 + 334); i 9 test della prima frase subito e i 2 nuovi del client passano anche da soli.

**Riserve (da segnare in stato_progetto.md)**
- R-801-1 (BASSA): un compito che finisce durante il turno si annuncia dopo la prima frase della risposta, non prima (ordine diverso da quello della fetta 3.2), senza ripetizioni.
- R-799-1 (BASSA): una frase in più se la risposta finale cambia rispetto alla frase anticipata.

**Non verificato**: tempi reali sul Mac, `claude -p`, ElevenLabs e casse veri; suite del kernel (gas.py non toccato).

**Memoria**: riga #801-M1coord (commit 37654b0f).

### Review #802-M1coord (merge di origin/main cb9ae3c, PR #378, nella #379)

## VERDETTO: APPROVATO

Review #802-M1coord: merge di origin/main cb9ae3c (PR #378) nella PR #379, branch perf/voce-prima-frase-subito. Letti CLAUDE.md §5, stato_progetto.md e la memoria del revisore.

**Nessun lato ha perso modifiche.** Confrontate le righe +/- di `git diff base..MERGE_HEAD` con `git diff HEAD --cached`, e di `git diff base..HEAD` con `git diff MERGE_HEAD --cached`: su `clients/voice/ascolto.py` e `tests/test_unit_voce_ascolto.py` coincidono in entrambe le direzioni. Il file in staging si analizza senza errori; cartella di lavoro = staging.

Elementi del diff esaminati:
- `clients/voice/ascolto.py:829` — l'interruzione mentre Gas parla usa `self.blocchi_interruzione` (#378). Rischio: ritorno a `blocchi_parola` (1 blocco, eco delle casse). Esito: ok; contatore azzerato su errore e sotto soglia.
- `clients/voice/ascolto.py:777` — bip d'errore se la prima frase è già detta e il turno fallisce (#379), dopo il `finally` del ciclo, fuori da `_ascolta_mentre_suona`. Rischio: interferenza con l'interruzione. Esito: ok — punti diversi; interrotto → `break`, il bip parte solo con `errore_turno` (impostato in `clients/voice/ascolto.py:1059`); con `suonati == 0` resta il bip esistente, niente doppio bip.
- `clients/voice/ascolto.py:1336` — `_regolazioni()` legge `GAS_ASCOLTO_BLOCCHI_INTERRUZIONE` (1-5, default 3) e lo passa al costruttore (`clients/voice/ascolto.py:378`) via `**regolazioni`. Esito: ok.
- `tests/test_unit_voce_ascolto.py:836` (test #379 su `errore_turno=True`) e `tests/test_unit_voce_ascolto.py:3224` (test #378 parola=1, interruzione=3) presenti. Esito: ok.
- Wall of Shame: nessuno slicing della history, nessuna simulazione dei tool; motore non toccato.

Test: `tests/test_unit_voce_ascolto.py` 346 passed (rilanciato dal revisore).

Rischi esclusi: `tests/test_unit_voice_server.py` non rieseguito (timeout dell'ambiente; il merge non tocca il server: valgono i 236 passed del coordinatore); comportamento reale sul Mac non verificato. R-800-1 ancora aperta, ereditata.

Memoria: riga #802-M1coord in .claude/agents/memoria_revisore.md, entrata nel commit di merge.

## §5 DELTA TEST DEL MOTORE

- `python -B -m pytest -q tests/test_unit_voice_server.py` → 227 passed (main 3756c97) → 236 passed (59478461; 9 test nuovi, uno prova che la prima riga arriva a turno ancora aperto).
- `tests/test_unit_voce_ascolto.py` → 332 → 334 passed → 346 passed dopo il merge di main (#378); voice_server 236 passed dopo il merge.
- Kernel (`python -B tests/test_unit_kernel.py`): 1167 PASS, 0 FAIL (gas.py non toccato).

```
236 passed
```

## §6 STATO CI

CI letta con lo strumento GitHub sulla PR #379: e2766972 tutti i check success, verifica-bot success (APPROVATO CON RISERVE, solo BASSE/COSMETICHE). Run del merge non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-801-1 BASSA — un compito finito arrivato durante il turno si annuncia dopo la prima frase, non prima.
- R-799-1 BASSA — una frase in più se la risposta finale cambia rispetto a quella anticipata.
- Non provato: tempi reali sul Mac (atteso circa 2 s in meno alla prima frase), `claude -p` ed ElevenLabs veri.
