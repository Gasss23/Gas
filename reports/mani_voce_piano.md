# Mani alla voce — piano (2026-11-25)

> Richiesta dell'operatore (25/11, via M1): con un comando vocale («Hey Jarvis, …») Gas fa partire
> un compito complesso in autonomia e, a fine lavoro, avvisa l'operatore con cosa ha fatto, il
> risultato e gli esiti dei controlli (revisore, CI, bot, verifica esterna), così che lui decida
> se mergiare. Il merge resta suo, salvo la regola di merge autonomo (CLAUDE.md §10).
> Stato: **F2 fatta** (`modules/sviluppo/esiti.py`, PR #409 mergiata il 26/11); **decisioni dell'operatore
> arrivate il 26/11** (§5): F1 rifiutata, compensazioni in §4bis; prossime F2-bis (riserve basse), F3,
> F4, F5 in quest'ordine. Sotto-chat di M1.

## 1. Cosa esiste (verificato nel codice il 25/11)

| Pezzo | Dove | Cosa fa | Limite |
|---|---|---|---|
| `in_sottofondo(compito)` | `gas.py` `_in_sottofondo`, `modules/sottofondo/` | A voce mette il compito in coda e lo lancia in un processo separato (`gas.py sottofondo <id>`), solo col cervello forte, uno alla volta, ripresa dopo un crash. Alla fine avviso Telegram «Ho finito … » con la risposta (max 700 caratteri); al turno a voce successivo Gas legge i compiti finiti (max 250 caratteri ciascuno). | Solo compiti «dentro Gas» (ricerche, CRM, web). Niente sviluppo di codice. |
| `richiedi_sviluppo(titolo, descrizione)` | `gas.py`, `modules/sviluppo/richieste.py` | Apre una issue con l'etichetta `da-gas` nel repo PRIVATO delle richieste (`GAS_RICHIESTE_REPO`), token dedicato solo Issues, tetto 20/giorno, rifiuta se il repo non è privato. | Nessuno la raccoglie da solo: oggi la legge M1 a mano. Al cancello è `UNCERTAIN` → **parte senza firma, anche a voce**. |
| Voce | `modules/voice/server.py`, `clients/voice/ascolto.py` | «Hey Jarvis» dal Mac (PR #405); lettura dei compiti in sottofondo finiti all'inizio del turno. | — |

**Punto 4 (compiti non di sviluppo) — esito della verifica:** il percorso voce → `in_sottofondo` →
processo separato → avviso Telegram con la risposta → lettura a voce al turno dopo **c'è già ed è
coperto dai test** (`tests/test_unit_sottofondo.py` + `tests/test_unit_richieste.py`: 154 passati
in questo container dopo `pip install -r requirements.txt`). Non ho trovato buchi da chiudere nel
codice, quindi **non ho cambiato niente** (e `modules/sottofondo/` è della sotto-chat R7). Manca solo
la prova vera sul Mac, che posso fare solo con l'operatore (vedi §6, punto 1).

## 2. Cosa manca

1. **Esecutore delle richieste di sviluppo**: chi prende le issue `da-gas` nuove e fa il lavoro come
   una chat di sviluppo (branch, revisore, test, PR con `verifica`, verifica esterna, giri finché è
   verde).
2. **Avviso di fine lavoro** con PR, CI, verdetto del bot (con i finding che bloccano il merge), verifica
   esterna e la domanda «vuoi che mergi?».
3. **Risposta dell'operatore** («mergia #N» / «no») da voce o Telegram, che arriva a chi mergia.
4. **Un via libera umano** fra la voce e il lavoro: oggi chiunque parli vicino al microfono (TV,
   ospite, audio riprodotto) può aprire una richiesta, e con l'esecutore la richiesta diventa lavoro
   vero e spesa vera.

## 3. Disegno proposto (il più semplice e sicuro)

Un'unica «cassetta delle lettere»: **la issue nel repo privato delle richieste**. Tutti i messaggi
fra Gas (sul Mac) e l'esecutore (nel cloud) passano da lì, come commenti. Niente segreti nuovi
nel cloud.

```
voce ──▶ Gas (Mac) ──richiedi_sviluppo──▶ issue `da-gas`
                          └──▶ Telegram SUBITO: «accodata #N; se non è tua: annulla richiesta N»
operatore «annulla richiesta N» ──▶ Gas ──▶ issue chiusa con `annullata`
esecutore (cloud, ogni ora 8-22, max 2/giorno) ──issue `da-gas` aperte, senza `annullata`, vecchie ≥30 min──▶ branch, revisore, PR, CI, bot, verifica esterna
esecutore ──commento «ESITO» (formato fisso)──▶ issue
Gas (Mac) ──legge i commenti nuovi──▶ Telegram + voce: «ho fatto X, PR #N, CI verde, bot: …, vuoi che mergi?»
operatore «mergia 412» (Telegram, o voce + firma) ──▶ Gas ──commento «MERGIA #412»──▶ issue
esecutore (scatto dopo) ──ricontrolla §10 (PR aperta, CI, bot, conflitti)──▶ merge ──▶ commento «MERGIATA» ──▶ avviso
```

**Perché il commento sulla issue e non Telegram diretto dal cloud:**
- il token del bot Telegram resterebbe nell'ambiente cloud (condiviso fra le sessioni): un segreto
  in più, fuori dal Mac, che può scrivere all'operatore a nome di Gas;
- con la issue l'esecutore non ha bisogno di NIENTE di nuovo: Gas ha già il token dedicato che
  legge e scrive le issue; l'avviso parte dal Mac col tetto e i filtri che `avvisa_operatore` già
  ha;
- la issue resta come registro: richiesta, via libera, esito, decisione di merge, tutto in un posto.
- Contro: l'avviso arriva solo quando Gas sul Mac è acceso e controlla (ritardo di qualche minuto).

### Le fette, in ordine

| # | Fetta | Tocca | Rischio | Serve il via? |
|---|---|---|---|---|
| F1 | ~~**Via libera a voce**~~ — **RIFIUTATA dall'operatore il 26/11**: a voce `richiedi_sviluppo` resta senza firma; al suo posto le compensazioni di §4bis. | — | — | — |
| F2 | **Formato fisso dei commenti** (`ESITO`, `MERGIA #N`, `NO #N`; `MERGIATA` si aggiunge in F5) e parser stretto in `modules/sviluppo/` (righe con chiave fissa, numero di PR intero, niente testo libero eseguito). Solo codice + test, nessuna credenziale. | `modules/sviluppo/`, `tests/` | basso | no |
| F2-bis | **Riserve basse di F2** chiuse prima di F3: testi liberi solo tra «» dopo le parti fisse (R-864-3), niente domanda di merge con righe RISERVA (finding che bloccano il merge), invisibili Default_Ignorable e testi senza nulla di visibile, «mergia N» solo ASCII. | `modules/sviluppo/`, `tests/` | basso | no |
| F3 | **Gas avvisa e legge gli esiti** (fatta il 26/11, `modules/sviluppo/cassetta.py`): avviso su Telegram APPENA una richiesta viene accodata, con «annulla richiesta N»; «annulla richiesta N» da Telegram (prima del modello, solo da messaggio nuovo) chiude la issue con `annullata`; ogni `GAS_RICHIESTE_CONTROLLO_MIN` minuti (default 5) il bot legge i commenti nuovi, prende solo gli ESITO validi di autori in `GAS_RICHIESTE_AUTORI` (vuoto = niente) su issue `da-gas`, e manda la frase all'operatore; ricorda la PR per cui la domanda di merge è stata fatta davvero (R-873MV-1, per F4). La lettura **a voce** degli esiti è rimandata a F3b. | `modules/sviluppo/`, `modules/telegram/bot.py`, `gas.py`, `.github/workflows/ci.yml` | medio | sì (dato il 26/11) |
| F3b | **Esiti letti a voce e annullo a voce** (fatta il 26/11): al primo turno a voce dopo l'arrivo Gas dice una frase corta con SOLO parti fisse (numero, stato, PR, controlli: niente testo libero dell'esecutore, R-873MV-1), al massimo 2 per turno, ultime 24 ore, segnate dette solo dopo la consegna; «annulla richiesta N» vale anche detto al microfono del Mac (dopo la parola di attivazione, mai nel seguito) e da un vocale Telegram; l'avviso dice «scrivimi o dimmi». | `modules/voice/server.py`, `modules/telegram/bot.py`, `modules/sviluppo/` | basso | no |
| F4 | **Risposta dell'operatore**: comando «mergia N» / «no N» su Telegram (a voce solo con firma) → commento `MERGIA #N`. | `modules/telegram/`, `gas.py` | medio | sì |
| F5 | **Esecutore nel cloud**: scheduled task (una sessione nuova a ogni scatto) con un prompt fisso nel repo (`.claude/esecutore_richieste.md`, lo cambia solo l'operatore). Ogni scatto: legge la bacheca, prende UNA issue `da-gas` aperta, senza `annullata` né esito e creata da almeno 30 minuti, controlla l'autore, lavora come una sotto-chat (tutte le regole di CLAUDE.md), scrive `ESITO`; poi gestisce i `MERGIA #N` rispettando §10. | trigger, ambiente cloud, accesso al repo delle richieste | **alto** (spesa ricorrente, lavoro autonomo) | sì |

Ordine deciso il 26/11: F2-bis, F3, F4, F5 (F1 rifiutata). F5 per ultima: prima si prova il giro a mano
(M1 o io facciamo da esecutore leggendo la issue), poi si automatizza.

## 4. Rischi e difese

**Iniezioni dalla voce.** La descrizione arriva da una trascrizione: chiunque vicino al microfono, o
un audio riprodotto, può dettarla. Difese:
- ~~F1: firma su Telegram~~ (rifiutata il 26/11): al suo posto avviso subito, annullo facile con
  30 minuti di attesa e tetto di 2 al giorno (§4bis);
- l'esecutore tratta la descrizione come richiesta dell'operatore **dentro i vincoli di sempre**:
  CLAUDE.md, perimetro di review, revisore, mai push su main, mai segreti nei file, mai toccare la
  macchina di controllo (hook, gate, bot, CI, `verifica_esterna.md`, `revisore.md`) né le
  credenziali; una richiesta che chiede queste cose → l'esecutore si ferma e scrive `ESITO: ferma` (con il motivo nel
  `RIASSUNTO`) invece di lavorare;
- l'esecutore lavora solo issue aperte con l'etichetta `da-gas`, senza `annullata`, con autore =
  l'account del token di Gas (o l'operatore); ignora le altre.

**Commenti falsi.** `MERGIA #N` vale solo se l'autore è l'account di Gas o l'operatore, e solo per una
PR che l'esecutore stesso ha aperto per quella issue. Il merge lo decide comunque §10: verdetto
testuale del bot sull'head, CI verde, nessun conflitto, PR ancora aperta. `MERGIA` su una PR con
riserve = il «sì» esplicito dell'operatore richiesto da §10 (va registrato nella PR).

**Spesa.** Ogni scatto della scheduled task è una sessione cloud che consuma l'uso dell'abbonamento
dell'operatore, anche quando non c'è niente da fare (lettura della bacheca + una chiamata). Il tetto
minimo di frequenza è di norma un'ora. Proposta: uno scatto all'ora solo nelle ore di lavoro
dell'operatore, e la sessione chiude subito se non c'è una issue col via libera. Un lavoro vero
costa quanto una sotto-chat di sviluppo. Tetto: al massimo N richieste lavorate al giorno.

**Accesso.** Questa sessione vede solo `gasss23/gas`; il repo delle richieste va aggiunto con
`add_repo`. Da verificare prima di F5: che le sessioni nate dalla scheduled task abbiano accesso a
tutti e due i repo e i permessi per aprire PR ed etichettarle `verifica`.

**Avvisi persi.** Se Gas sul Mac è spento, l'esito resta nella issue e arriva alla riaccensione.
Gli avvisi di esito hanno un tetto loro (F3): 5 per controllo e `GAS_RICHIESTE_ESITI_GIORNO` al
giorno (default 20), separato da quello di `avvisa_operatore`. Un ESITO è sempre un commento nuovo
(un commento modificato non si rilegge).

## 4bis. Al posto di F1: compensazioni (decisione dell'operatore del 26/11)

L'operatore ha scelto che a voce `richiedi_sviluppo` NON passi dalla firma su Telegram. Il rischio
resta: chiunque parli al microfono (o un audio riprodotto) può accodare lavoro e spesa. Al posto della
firma, tre difese, nessuna delle quali chiede un passo in più all'operatore quando la richiesta è sua:

1. **Avviso subito (F3).** Appena la issue è creata, Gas manda su Telegram: «Ho accodato la richiesta
   #N «titolo» (arrivata a voce). Se non è tua, rispondi «annulla richiesta N»». Così una richiesta non
   sua l'operatore la vede in pochi secondi, non a lavoro finito.
2. **Annullare è facile (F3) e c'è il tempo per farlo (F5).** «annulla richiesta N» su Telegram →
   Gas chiude la issue con l'etichetta `annullata`. L'esecutore non tocca issue chiuse né `annullata`,
   e non parte su una issue creata da meno di **30 minuti** (finestra per annullare).
3. **Tetto duro (F5).** L'esecutore lavora al massimo **2 richieste al giorno**; le altre restano in
   coda per i giorni dopo. Il tetto lato Gas (`GAS_RICHIESTE_MAX_GIORNO`, oggi 20 issue al giorno)
   resta come limite alle issue create.

Restano valide le difese di §4 sui contenuti: l'esecutore non tocca mai macchina di controllo e
credenziali, e una richiesta che lo chiede finisce con `ESITO: ferma`.

## 5. Decisioni dell'operatore (26/11, via M1: «ok tutto tranne punto 1»)

1. F1: **NO** (compensazioni in §4bis).
2. Canale: **issue + Gas sul Mac** che legge i commenti e li gira su Telegram e voce; niente token
   Telegram nel cloud.
3. F5: **ogni ora dalle 8 alle 22**, **max 2 richieste al giorno** (le altre in coda), **sempre
   cervello forte**.
4. Con `MERGIA #N` **mergia l'esecutore stesso**, rispettando CLAUDE.md §10 (verdetto letto davvero,
   CI verde, nessun conflitto).

### Proposte originali (25/11), per memoria



1. **F1:** a voce, `richiedi_sviluppo` passa dalla firma su Telegram? (proposta: sì).
2. **Canale dell'avviso:** commento sulla issue letto da Gas sul Mac (proposta) oppure Telegram
   diretto dal cloud col token del bot come segreto dell'ambiente.
3. **F5 — scheduled task:** frequenza e ore (proposta: ogni ora, 8–20, giorni feriali), tetto di
   richieste lavorate al giorno (proposta: 2), modello (proposta: quello delle sotto-chat).
4. **Cosa l'esecutore NON può fare mai**, oltre a quanto sopra (proposta: niente macchina di
   controllo, niente credenziali, niente dipendenze nuove senza dirlo nell'esito).
5. **Merge:** con `MERGIA #N` mergia l'esecutore allo scatto successivo (proposta), oppure resta M1.

## 6. Cosa serve dall'operatore (quando si arriva lì)

1. Prova del punto 4 sul Mac: dire «Hey Jarvis, fai in sottofondo una ricerca su …», aspettare
   l'avviso su Telegram e controllare che contenga il risultato.
2. Per F5: aggiungere il repo delle richieste alla sessione/ambiente (lo chiedo io con `add_repo`,
   lui approva) e approvare la scheduled task.
