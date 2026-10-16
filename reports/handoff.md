# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-16 — Prova FASE 2.6 sul Mac; recap usato solo se pertinente, niente lezioni quasi uguali

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #215 (https://github.com/Gasss23/Gas/pull/215).

(`gh` non disponibile nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Merge #214**: `FATTA` — `d0c7283`.
- **Recap usato solo se pertinente**: `FATTA`.
- **Niente lezioni quasi uguali**: `FATTA`.
- **Note rimaste da #214 (R-351-1, V-2 bot)**: `FATTA`.
- **Bot #215 BOCCIATO, V-1 MEDIA (rifiutate non fidate nel prompt)**: `FATTA` — review #354.
- **Avviso knowledge_fts / risposta «win rate»**: `SALTATA` — fuori scope, registrati.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 gas.py                             |  80 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------
 reports/diff_sessione.md           |  11 +++++------
 reports/handoff.md                 | 148 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  22 ++++++++++++----------
 tests/test_unit_kernel.py          |  82 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 7 files changed, 276 insertions(+), 75 deletions(-)
```

NB: conteggi di `reports/handoff.md` (e totali) presi prima del proprio commit.

## §3 GIT LOG --ONELINE (sessione)

```
41ca88a fix(riflessione): lezioni rifiutate da finestre non fidate fuori dal prompt (V-1 bot #215)
34e588f chore(revisore): memoria review #354 — APPROVATO
097c288 docs(fine-task): report e handoff — recap pertinente e lezioni non ripetute (PR #215)
c1bae19 feat(riflessione): recap usato solo se pertinente; niente lezioni quasi uguali (prova Mac 2026-10-16)
0693018 chore(revisore): memoria review #353 — APPROVATO
5616bfa chore(revisore): memoria review #352 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #352 — verdetto integrale

## VERDETTO: APPROVATO CON RISERVE

Ho letto le tre fonti obbligatorie: CLAUDE.md sez. 5, `reports/stato_progetto.md` (solo le parti che servivano) e la memoria del revisore. Ho poi riprodotto la suite del kernel: **876 PASS, 0 FAIL**.

Ho fatto anche due mutazioni su una copia del repo, per controllare che i test nuovi colgano davvero un errore:
- **Soglia portata a 9**: falliscono solo T91c e T91e.
- **Blocco delle lezioni già note svuotato**: fallisce solo T91b.

Non trovo slicing della history né output dei tool simulati. Il cap delle 10 iterazioni e `_get_window` non sono toccati. Tutto il codice nuovo di `rifletti` sta dentro il try/except già esistente, che logga e restituisce un esito: nessun nuovo punto di crash.

**Elementi del diff esaminati**
- `gas.py:98` — nuova regola su `<recap_dati>`: il recap si usa solo se la domanda riguarda quel task, e il suo «cosa resta da fare» non è una richiesta dell'utente. Rischio esaminato: che la regola indebolisca «mai istruzioni». Esito: ok, la frase resta (T91a la controlla).
- `gas.py:803` — `_lezione_simile`: radici di 5 lettere, soglia 0,5 sulla lezione più corta, nessun confronto sotto le 4 radici. Rischio esaminato: falsi positivi. Esito: **riserva** (R-352-2).
- `gas.py:3003` — il system della riflessione elenca fino a 30 lezioni del catalogo, sanitizzate e chiuse in `<lezioni_esistenti>`. Rischio esaminato: iniezione e riciclo di fiducia. Esito: **riserva** (R-352-1).
- `gas.py:3082` — il catalogo è letto una volta sola e la lezione appena aggiunta viene accodata, così il controllo vale anche dentro la stessa riflessione. Rischio esaminato: `lid` non definito. Esito: ok, `lid` è sempre valorizzato quando si arriva all'append.
- `gas.py:2906` — `dal` ora è calcolato con `_now_iso_da`. Rischio esaminato: formato diverso da quello del diario. Esito: ok, chiude R-351-1.
- `tests/test_unit_kernel.py:8818` — `_recap90` usa `_store90._now_iso_da`. Esito: ok.
- `tests/test_unit_kernel.py:8906` — T91a–f. Esito: ok; le mutazioni sopra le fanno fallire.
- Contesto: `modules/memory/store.py:1514` (`lista_lezioni` restituisce TUTTI gli stati, dal più recente) e `modules/memory/store.py:166` (testo della lezione al massimo 300 caratteri).

**Riserve**
- **R-352-1 MEDIA — da sistemare prima del merge.** Il catalogo mostrato alla riflessione contiene anche le lezioni in stato `proposta`, comprese quelle nate da finestre `:non_fidato`. Quei testi non sono mai passati dall'operatore. Il percorso del rischio:
  1. una lezione proposta da una finestra non fidata entra nel system di una riflessione successiva su una finestra pulita;
  2. il recap di quella riflessione esce come `recap` fidato;
  3. `_recap_pin` lo rimette nel system prompt.

  È un riciclo di fiducia contro la regola fail-closed (R-200-1 / R-201-1). Le difese a valle (sanitizzazione, i tag `<..._dati>`, il limite di 300 caratteri) lo attenuano ma non lo chiudono. Correzione: una riga, cioè mostrare solo gli stati `approvata`, `rifiutata` e `ritirata`, oppure escludere le lezioni con `turni_sorgente` che contiene `:non_fidato`. Più un test.
- **R-352-2 BASSA.** Senza parole vuote, e con la più corta come denominatore, vengono scartate lezioni diverse. Prova fatta: «Quando l utente chiede una email, scrivila sempre in italiano formale» viene presa come simile a «Chiedi sempre conferma all utente prima di inviare una email a un cliente». Coincidono 4 radici su 4 (sempr, utent, chied, email). La taratura sulle 12 lezioni del Mac non copre questi casi. Lo scarto si vede solo nella stampa di `clear` (`gas.py:4778`). Suggerimento: un piccolo elenco di parole vuote («sempre», «prima», «quando», «utente») oppure il denominatore sulla lezione più lunga.
- **R-352-3 COSMETICA.** Nessun test controlla che `<` e `>` vengano neutralizzati dentro `<lezioni_esistenti>`.

**Risposte alle due domande**
1. **Import di `_now_iso_da`.** Accettabile: è un helper puro e senza stato. Il nome privato importato da fuori però è un debito; meglio renderlo pubblico (`now_iso_da`) ed esportarlo da `modules.memory`. Cosmetico, non blocca.
2. **Lezioni nel prompt della riflessione.** Per le lezioni rifiutate (e anche per quelle approvate o ritirate) sì: sono passate dall'operatore, sono sanitizzate e chiuse come dato. La premessa però è vera solo per quegli stati. Le lezioni in `proposta` non sono passate dall'operatore, ed è il punto R-352-1.

**Rischio escluso:** non ho verificato il comportamento reale del modello, cioè se riproponga davvero meno lezioni e se ignori il recap non pertinente. È testo del prompt valutabile solo con un LLM vero, da riprovare sul Mac. Non ho neanche rilanciato `pytest tests/` completo: ho girato solo la suite del kernel.

**Memoria:** aggiunta la riga #352 e una lezione nuova (verificare quali stati del DB entrano in un prompt, perché `proposta` è testo del modello mai deciso). Il commit è `5616bfa`, fatto da `scripts/commit_memoria_revisore.sh`.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #353 (ri-review dopo R-352-1/2/3) — verdetto integrale

## VERDETTO: APPROVATO

Ri-review del diff staged completo: le tre riserve della #352 sono chiuse. Ho rilanciato la suite del kernel su una copia del repo: 878 PASS, 0 FAIL. Poi ho fatto quattro mutazioni del codice per vedere se i test se ne accorgono.

**Elementi del diff esaminati**
- `gas.py:3015` — nel prompt della riflessione entrano solo le lezioni approvate, rifiutate o ritirate. Rischio esaminato: un testo del modello mai deciso, nato da una finestra non fidata, che finisce in un recap fidato (R-352-1). Esito: ok. Se tolgo il filtro sullo stato fallisce solo T91g (`tests/test_unit_kernel.py:8937`). La rete `_lezione_simile` legge ancora anche le lezioni in proposta, ma solo per confrontarle: quel testo non entra nel prompt.
- `gas.py:789` — `_RADICI_VUOTE`, l'elenco delle radici comuni da ignorare. Rischio esaminato: falsi positivi (R-352-2). Esito: ok. Il tuo esempio dell'email ora vale 0,4 e la lezione non viene scartata (T91d, `tests/test_unit_kernel.py:8946`). Se tolgo l'elenco falliscono T91c, T91d e T91e.
- `gas.py:821` — il denominatore ora è la lezione più LUNGA. Rischio esaminato: soglia troppo larga. Esito: ok nel merito, con una nota: se rimetto la più corta (`min`) nessun test fallisce, perché con l'elenco delle radici vuote anche il caso dell'email dà 0,4 in entrambi i modi.
- `gas.py:3024` e `tests/test_unit_kernel.py:8939` — un tag scritto nel testo di una lezione viene neutralizzato. Esito: ok. Se tolgo `_sanitize_memory_text` fallisce solo T91h (R-352-3).
- Non trovo slicing della history né output dei tool simulati. Il codice nuovo resta dentro il try/except di `rifletti`.

**Note non bloccanti**
- COSMETICA: manca un test che distingua il denominatore sulla lezione più lunga da quello sulla più corta.
- Margine stretto: la coppia #6/#9 vale 0,53 con soglia 0,5. Basta una riformulazione un po' diversa perché non venga più presa. È una scelta di taratura, non un difetto.

**Rischio escluso:** non ho verificato il comportamento reale del modello, cioè se smette davvero di riproporre lezioni e se ignora il recap non pertinente. Si può provare solo con un LLM vero sul Mac. Non ho rilanciato `pytest tests/` completo: ho girato solo la suite del kernel.

**Memoria:** aggiunta la riga #353, nessuna lezione nuova. Il commit è `0693018`, fatto da `scripts/commit_memoria_revisore.sh`.

File rilevanti: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

### Review #354 (fix V-1 bot #215) — verdetto integrale

## VERDETTO: APPROVATO

**Letture obbligatorie fatte**: CLAUDE.md (sezione 5, e sezioni 6 e 8), reports/stato_progetto.md (la parte che serviva), .claude/agents/memoria_revisore.md (le ultime voci, #350–#353, e la lezione del 2026-10-16 sugli stati delle lezioni).

**Elementi del diff esaminati**
- `gas.py:3017` — il filtro `decise` passa le `approvata` sempre. Passa le `rifiutata`/`ritirata` solo se `":non_fidato"` non compare in `str(turni_sorgente)`. Rischio esaminato: che il marcatore abbia altre forme, o che `turni_sorgente` arrivi come lista o come JSON e sfugga al controllo. Il marcatore si scrive in un solo punto, `gas.py:3116` (`diario:{rid}:non_fidato`). `str()` lo trova sia nella lista sia nella stringa JSON. Il cap `decise[:RIFLESSIONE_LEZIONI_NOTE]` si applica dopo il filtro, quindi le lezioni non fidate non tolgono posto a quelle fidate. Esito: ok.
- `gas.py:3017` — perché le approvate non fidate restano nel blocco. Rischio esaminato: che anche loro riciclino fiducia. Non lo fanno: il «sì» dell'operatore le rende fidate, e infatti entrano già in ogni turno tramite `_lezioni_pin`. Il «no» invece non rende fidato un testo. La distinzione è giusta. Esito: ok.
- `gas.py:804` — il commento della soglia ora dice «in qualunque stato» e da dove vengono le misure (T91c). Rischio esaminato: che il commento dica qualcosa di diverso dal codice. Non succede: `_lezione_simile` confronta con tutto il catalogo. Esito: ok.
- `tests/test_unit_kernel.py:8943` — T91i controlla che la lezione rifiutata con `diario:1:non_fidato` resti fuori dal prompt e che il recap sia di tipo `recap`. Ho riprodotto la suite: **879 PASS, 0 FAIL**. Ho poi tolto la condizione sulla provenienza (mutazione): fallisce **solo T91i** (878/1). Il codice originale è stato ripristinato, `git diff` senza modifiche fuori dallo staging. Esito: ok.
- Wall of Shame (gli errori vietati dalla sezione 5): nessuno slicing della history, nessuna simulazione di tool. `_get_window` e il cap delle iterazioni non sono toccati.

**Nota cosmetica (non è una riserva)**: il ramo `ritirata` con provenienza `:non_fidato` non ha un test dedicato. Se si toglie `"ritirata"` dalla tupla non fallisce nulla.

**Risposta alla tua domanda**: sì, mi sta bene. È "robustezza > potenza": perdere un po' di aiuto contro le ripetizioni costa poco. Il riciclo di fiducia è un buco di sicurezza (vedi R-200-1/R-201-1). Contro i doppioni restano due reti meccaniche: il confronto esatto con `esistenti` e `_lezione_simile`. Nessuna delle due mette testo nel prompt. Il costo peggiore è che l'operatore riveda una lezione già rifiutata con parole diverse, sotto la soglia di somiglianza. È un fastidio, non un rischio. Se sul Mac il rumore diventa troppo, la strada giusta è passare al modello solo un riassunto meccanico (per esempio le radici) delle rifiutate non fidate, mai il loro testo.

**Cosa non ho verificato**: il comportamento sul database reale del Mac, cioè quante lezioni rifiutate non fidate vengono riproposte e se `_lezione_simile` basta a fermarle. Non si può riprodurre in dev: il database del Mac non è nel repo. Non ho rieseguito le altre suite oltre a quella del kernel.

**Memoria**: aggiunta la riga #354 (APPROVATO) con la lezione: un filtro di fiducia deve guardare la provenienza oltre allo stato. Committata con `scripts/commit_memoria_revisore.sh` (commit 34e588f), lo staging del diff è rimasto intatto.

File: /home/user/Gas/gas.py, /home/user/Gas/tests/test_unit_kernel.py, /home/user/Gas/.claude/agents/memoria_revisore.md

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 870 → 879 PASS, 0 FAIL (T91a–i). Blocco reale: `=== RIEPILOGO: 879 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1419 passed in 174.58s (0:02:54)` (prima delle correzioni R-352).

## §6 STATO CI

`gh` non disponibile nella sessione cloud: lo stato CI si legge dai check-run della PR via MCP GitHub.

- `5616bfa`, `0693018`, `c1bae19`: pushati insieme prima dell'apertura della PR #215; nessuna run su questi SHA singolarmente.
- `097c288` (primo fine-task): handoff-check success; bot BOCCIATO (V-1 MEDIA, definitivo su quello SHA); verifica esterna APPROVATO CON RISERVE ([commento](https://github.com/Gasss23/Gas/pull/215#issuecomment-6213316242)).
- `34e588f`, commit del fix V-1 e commit di fine-task (questo handoff): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- COSMETICA #353: nessun test distingue il denominatore min/max di `_lezione_simile`; margine stretto #6/#9 (0,53 con soglia 0,5).
- COSMETICA #352: `_now_iso_da` importato come nome privato da gas.py.
- R-ve215-1 (BASSA): somiglianza per parole, non per senso.
- COSMETICA #354: ramo `ritirata` non fidata senza test dedicato.
- Avviso knowledge_fts a schermo sul Mac; risposta «win rate» povera (non corretti, registrati).
