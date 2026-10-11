# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — merge #177 + decisioni dell'operatore 2a, 3, 4C (PR #178, con correzione dopo il bot)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #178 (https://github.com/Gasss23/Gas/pull/178). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/178"}`): `gh` nel container non è autenticato. Tocca la macchina di controllo: il merge lo decide l'operatore.
2. Punto 5 (V-2 bot #163): (a)/(b)/(c), proposta (c).
3. Punto 1A: elenco delle cartelle scrivibili da Gas (proposta `dati/`, `knowledge/`, `output/`).
4. Prova reale sul Mac (7B): esito del primo `python3 gas.py notte`.

---

## §1 SCOPE & ESITO FETTE

- **Merge di #177**: `FATTA` — su richiesta esplicita dell'operatore, merge commit `63e9fec` (= BASE di questa sessione).
- **Fetta 1 — 4C (Opus 5.5 per primo nel bot)**: `FATTA`.
- **Fetta 2 — 2a (verdetto della verifica esterna sulla PR)**: `FATTA`.
- **Fetta 3 — 3 (roadmap)**: `FATTA`.
- **Fetta 4 — V-1 bot #178 (pubblicazione solo per l'agente di sessione)**: `FATTA`.
- **Punti 5 e 1A**: `DEFERITA` — in attesa dell'operatore.
- **Note basse del bot su #177**: `DEFERITA` — prossima fetta motore.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 ++++
 .claude/commands/fine-task.md      |   8 +++++---
 .claude/verifica_esterna.md        |  20 ++++++++++++++++++++
 .github/workflows/verifica-bot.yml |  24 +++++++++++++-----------
 CLAUDE.md                          |   2 +-
 reports/diff_sessione.md           |  17 ++++++++++-------
 reports/handoff.md                 | 173 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------
 reports/roadmap.md                 |   6 +++---
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  28 ++++++++++++++++++----------
 reports/verifiche_esterne.md       |  99 ---------------------------------------------------------------------------------------------------
 tests/test_unit_verifica_bot.py    |   3 ++-
 12 files changed, 195 insertions(+), 193 deletions(-)
```

Nota: i conteggi di righe dei report scritti dopo lo stat (`reports/handoff.md`) sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
ba77d93 docs(fine-task): report PR #178 secondo giro (pubblicazione solo per l'agente di sessione)
5ab30b3 fix(controllo): la pubblicazione del verdetto vale solo per l'agente di sessione, non per il bot
475a84f chore(revisore): memoria review #257 — APPROVATO
f61d789 docs(fine-task): report PR #178 (decisioni dell'operatore 2a, 3, 4C)
0c21c6a chore(controllo): bot di verifica con Opus 5.5 per primo; verdetto della verifica esterna pubblicato sulla PR; roadmap aggiornata
1308eaa chore(revisore): memoria review #256 — APPROVATO
f67a5ea chore(revisore): memoria review #255 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. `f61d789` è il commit di fine-task del primo giro; `ba77d93` è un commit di fine-task fermato dal gate B (non pushato da solo) e superato da questo.

## §4 VERDETTO DEL REVISORE

### Review #255 (prima versione del diff di 0c21c6a)

## VERDETTO: APPROVATO CON RISERVE

Ho seguito le letture obbligatorie: CLAUDE.md, le sezioni pertinenti di reports/stato_progetto.md (cercate con grep) e la coda di memoria_revisore.md. Ho letto tutto il diff staged, compreso il file eliminato a HEAD. Ho cercato con grep "fable" e "verifiche_esterne" in tutto il repo e ho rilanciato `tests/test_unit_verifica_bot.py`: 297 passed.

**Elementi del diff esaminati**

- `.github/workflows/verifica-bot.yml:199` (m1 = Opus 5.5), `:214` (m2 = Opus 4.8), `:230` (m3 = Fable 5.1). Ho controllato che nomi dei passi e `--model` restino allineati e che l'ordine non conti per le condizioni. Gli `if` di m2/m3 (`:216`, `:232`) dipendono solo da `structured_output == ''` dei passi precedenti, non dal nome del modello. **Esito: ok.**
- `.github/workflows/verifica-bot.yml:255-258`: «Raccogli il verdetto». Ho controllato che ogni S1/S2/S3 sia associato al suo modello e che l'elenco dei modelli falliti segua il nuovo ordine. È coerente in tutti e quattro i rami. `MODELLO` serve solo al corpo del messaggio (`scripts/bot_esito.py:392`) e non entra nella decisione APPROVE/COMMENT. **Esito: ok.** I test a `tests/test_unit_verifica_bot.py:701/726` usano ancora il vecchio ordine come dati d'esempio, senza conseguenze per la logica.
- `tests/test_unit_verifica_bot.py:1005`: controlla l'ordine della cascata. Ho verificato che l'asserzione segua davvero l'ordine del workflow: è un confronto esatto della lista. **Esito: ok.**
- `.claude/verifica_esterna.md:52-61`: nuova sezione «Pubblicazione del verdetto». Ho controllato che non contraddica la regola 4 («il repo reale non va toccato») e che non apra un percorso verso il bot. Il commento è una scrittura su GitHub, non nel repo, quindi la regola regge. Il workflow non parte su `issue_comment` (`:39-41`) e il bot tratta i commenti della PR come dati (`:133`). **Esito: riserva (R-255-2).**
- `.claude/commands/fine-task.md:293-297` e `CLAUDE.md:25` (istituzione E): allineati alla nuova regola. **Esito: ok.**
- Eliminazione di `reports/verifiche_esterne.md`. Ho cercato i riferimenti rimasti: `reports/stato_progetto.md:358` cita ancora quell'archivio come rimedio che chiudeva V-1 bot #172. **Esito: riserva (R-255-1).**
- `reports/roadmap.md:38/81/82`: italiano, F1 e F6 segnati FATTI. Ho controllato nel codice che lo siano davvero:
  - F1: `PRAGMA recursive_triggers = ON` a `modules/memory/store.py:527`;
  - F6: quarantena `.corrupt` a `gas.py:773-777` e `os.replace` a `gas.py:791`;
  - italiano: regola a `gas.py:74`.

  **Esito: ok nel merito, riserva cosmetica (R-255-3).**

**Questi cambi indeboliscono un gate?**

- **Cascata dei modelli: no.** Cambia solo l'ordine dei tentativi; come il bot decide e quali strumenti ha restano invariati. Opus 5.5 era già il modello che rispondeva di fatto, perché Fable falliva sempre (stato_progetto:126/128).
- **Archivio sostituito dai commenti sulla PR: no nel complesso, ma qualcosa si perde.**
  - Si guadagna: il verdetto lo scrive l'agente di verifica, quindi l'agente principale non lo ricopia più a mano.
  - Si perde: la prova non sta più nel clone del repo e un commento cancellato non lascia traccia.
  - I verdetti archiviati per #171-#176 restano consultabili nella storia git (es. `git show 63e9fec:reports/verifiche_esterne.md`).

  È una scelta esplicita dell'operatore (2a). La giudico accettabile.

**Riserve**

- **R-255-1 (BASSA):** `reports/stato_progetto.md:358` dice ancora «verdetti integrali … archiviati in `reports/verifiche_esterne.md` (V-1 bot #172 …)». Il file non esiste più. Va riscritta così: «archivio sostituito dai commenti dell'agente sulla PR (decisione 2a, 2026-10-11); verdetti #171-#176 nella storia git a `63e9fec`».
- **R-255-2 (BASSA):** il testo di `verifica_esterna.md` non dice nulla di falso: non promette che il commento sia immodificabile e parla di «cronologia delle modifiche». Però «scritta da te» non è verificabile, perché il commento esce con l'identità GitHub dell'operatore. Le modifiche si vedono nella cronologia, ma una cancellazione seguita da una nuova pubblicazione non lascia traccia. Va aggiunta una frase che lo dica in modo esplicito. Manca anche cosa fare se il commento non viene pubblicato («COMMENTO NON PUBBLICATO»). La soluzione proposta è che l'agente principale pubblichi il verdetto ricevuto, dichiarando che è una copia, oppure lo incolli nell'handoff.
- **R-255-3 (COSMETICA):** `reports/roadmap.md:81-82` hanno la spunta ✅ ma conservano «**PROSSIMA FETTA MOTORE**: fix 1 riga…» e «Fetta piccola dopo F1…». È una contraddizione nella stessa riga.

**Cosa non ho verificato**

- Il comportamento reale del bot con la nuova cascata su GitHub Actions non l'ho visto: serve una PR etichettata `verifica`, che in sviluppo non posso riprodurre.
- Non so se il subagente di verifica esterna abbia davvero uno strumento GitHub in scrittura per pubblicare il commento. Non esiste una definizione dell'agente in `.claude/agents/` e dipende dall'ambiente MCP della sessione: si vedrà alla prima verifica.
- Non ho controllato il comportamento di cancellazione dei commenti lato GitHub: è un'affermazione basata su come funziona di norma GitHub, non su una sonda.

**Memoria aggiornata:** ho aggiunto la riga #255 e una lezione in `.claude/agents/memoria_revisore.md`, committata come `f67a5ea` solo su quel file. Il diff staged è rimasto intatto (8 file).

### Review #256 (delta R-255-1/2/3, diff finale di 0c21c6a)

## VERDETTO: APPROVATO

Ho riletto tutto il diff staged (8 file, 42 righe aggiunte e 119 tolte) e rilanciato `tests/test_unit_verifica_bot.py`: 297 passed. Le tre riserve della review #255 sono chiuse.

**Elementi del diff esaminati**

- **`reports/stato_progetto.md:358`** (R-255-1): la voce dice ora che l'archivio è stato sostituito dai commenti dell'agente sulla PR (decisione 2a). Rimanda a `git show 63e9fec:reports/verifiche_esterne.md` per i verdetti #171-#172.
  - Rischio esaminato: un rimando che indica verdetti che a quel commit non ci sono. Ho elencato i titoli dell'archivio a `63e9fec`: contiene solo PR #171 e PR #172, quindi «#171-#172» è esatto. Nella review #255 avevo scritto «#171-#176»: era un mio errore, e la correzione dell'agente è giusta.
  - Il grep su `verifiche_esterne` trova solo questa riga e la :349, entrambe coerenti.
  - **Esito: ok.**
- **`.claude/verifica_esterna.md:58-65`** (R-255-2): «scritta da te» è diventato «pubblicata da te». Il testo ora dichiara il limite: il commento esce con la stessa identità GitHub dell'operatore, e una cancellazione seguita da una nuova pubblicazione non lascia traccia. Aggiunge anche il ripiego se compare `COMMENTO NON PUBBLICATO`: l'agente principale pubblica il verdetto dichiarando in testa che è una sua copia, e lo incolla nell'handoff successivo.
  - Rischio esaminato: un testo che promette più di quanto GitHub garantisca davvero. Il testo non lo fa più, e il ripiego rende visibile che si tratta di una copia.
  - **Esito: ok.**
- **`reports/roadmap.md:81-82`** (R-255-3): le frasi superate ora compaiono come «(Era: …)».
  - Rischio esaminato: una contraddizione rimasta dentro una voce già spuntata ✅. Non ce n'è più. Nella F6 la parentesi «(Era: fetta piccola dopo F1:)» seguita dal testo fuori parentesi si legge un po' male, ma non induce in errore.
  - **Esito: ok.**
- **`.github/workflows/verifica-bot.yml:199-258`** e **`tests/test_unit_verifica_bot.py:1005`**: le righe cambiate sono le stesse 29 già esaminate nella review #255. Cascata, condizioni `if` dei passi m2/m3 e mappatura in «Raccogli il verdetto» restano coerenti tra loro.
  - **Esito: ok.**

**Gate indeboliti:** nessuno, oltre alla perdita già accettata nella review #255 con la decisione 2a: la prova non sta più nel clone del repo.

**Cosa non ho verificato:**
- La nuova cascata del bot non l'ho vista girare su GitHub Actions, perché in sviluppo non è riproducibile.
- Non so se l'agente di verifica esterna abbia davvero uno strumento GitHub in scrittura: dipende dall'ambiente MCP della sessione e si vedrà alla prima verifica.
- La cancellazione dei commenti senza traccia è un'affermazione su come funziona GitHub, non l'ho provata con una sonda.

**Memoria:** ho aggiunto la riga #256 in `.claude/agents/memoria_revisore.md` e l'ho committata come `1308eaa`, solo quel file. Il diff staged è rimasto intatto.

### Review #257 (delta V-1 bot #178, diff di 5ab30b3) — riemissione con riferimenti completi

## VERDETTO: APPROVATO

Questa è una riemissione del verdetto della review #257: stesso esito e stessi contenuti. Ogni riferimento a un file ora ha il percorso completo e una sola riga, senza intervalli. La memoria non va aggiornata: la riga #257 è già nel commit `475a84f`.

Ho letto le tre fonti obbligatorie: CLAUDE.md (in contesto), `reports/stato_progetto.md` (cercando le parti che servivano) e la coda di `.claude/agents/memoria_revisore.md` (ultima voce: #256).

**Cosa ho controllato nel diff** (5 righe aggiunte a un solo file):

1. `.claude/verifica_esterna.md:54` — limita la sezione «Pubblicazione del verdetto» all'agente lanciato dalla sessione di sviluppo con il prompt `Applica .claude/verifica_esterna.md a: <URL_HANDOFF> <URL_PR>`. Rischio esaminato: che il bot possa scambiarsi per quell'agente. Il prompt che il bot riceve davvero (`.github/workflows/verifica-bot.yml:123`) è «Applica il protocollo .claude/verifica_esterna.md … alla PR #N, commit …»: non ha la forma «a: <URL_HANDOFF> <URL_PR>» e si apre con «Sei il bot di verifica esterna». Il prompt di sessione in `.claude/commands/fine-task.md:279` coincide invece carattere per carattere con quello citato. La distinzione è quindi univoca, e il testo nomina anche il file del workflow. — ok
2. `.claude/verifica_esterna.md:56` — dice che il bot salta la sezione perché il workflow pubblica già il suo verdetto come review. Rischio esaminato: che sia una giustificazione di comodo. È coerente con i fatti: gli strumenti del bot (`.github/workflows/verifica-bot.yml:118`, voce `STRUMENTI`) sono Read/Grep/Glob più `gh pr view`, `gh pr diff`, `gh pr checks`, `gh run view` e `gh run list`, quindi non può commentare. Senza questa esclusione, dopo il merge ogni giro del bot avrebbe tentato una scrittura impossibile e anteposto «COMMENTO NON PUBBLICATO» al verdetto. È esattamente la V-1 (il primo finding del bot sulla PR #178), che così è chiusa. — ok
3. `.claude/verifica_esterna.md:68` (riga non toccata, stesso file) — il ripiego «COMMENTO NON PUBBLICATO» e la copia dichiarata dall'agente principale restano invariati per l'agente di sessione. Rischio esaminato: perdere il ripiego introdotto con R-255-2. Non si perde. — ok
4. Contesto: `scripts/bot_esito.py:93` (regex `_RIGA_TITOLO`) e `scripts/bot_esito.py:256` (lettura del campo `testo`) — il gate del bot lavora sulla risposta strutturata (`verdetto`, `finding`, `testo`) e sulla riga di titolo. Il testo del protocollo non finisce mai nel verdetto, quindi le righe aggiunte non toccano né lo schema né la regex. — ok
5. Contesto: su main (`63e9fec`) la sezione «Pubblicazione» non esiste ancora (cercata con grep, nessun risultato). Il bot legge il protocollo da main, quindi il suo giro sulla PR #178 non ne è toccato; l'esclusione vale dal merge in poi, cioè proprio quando serve. — ok

Il file è nel perimetro di review (`.claude/perimetro_review.txt:16`), quindi questa review era dovuta. I guardrail del motore (`_get_window`, il tetto di 10 iterazioni, la gestione degli errori dei provider) non vengono toccati.

**Cosa NON ho verificato**:
- Il comportamento reale di un giro del bot dopo il merge: richiede GitHub Actions con la GitHub App e non si riproduce in locale. La garanzia viene dalla lettura del testo e dalla lista degli strumenti, non da un'esecuzione.
- Non ho eseguito la suite di test: il diff tocca solo un protocollo in prosa che nessun test né script analizza.

(Modifiche dell'agente al testo dei verdetti #255/#256/#257: path assoluti della memoria scritti relativi; elenco «File rilevanti» finale omesso; `&lt;`/`&gt;` della riemissione #257 riportati a `<`/`>`. Il #257 è stato riemesso dal revisore con riferimenti completi perché il gate B non contava le forme abbreviate «:56».)

## §5 DELTA TEST DEL MOTORE

Motore non toccato. Suite del bot di verifica 297 passed (invariata nel numero, test della cascata aggiornato); `pytest tests/` 865 passed.

```
865 passed in 145.91s (0:02:25)
```

## §6 STATO CI

`gh` non autenticato nel container; stato letto con lo strumento GitHub collegato.

Per costruzione i commit intermedi sono ROSSI su `handoff-check`: fa fede la run sul commit di fine-task.

- `f67a5ea`, `1308eaa`, `0c21c6a`: pushati insieme; run su `0c21c6a` rossa su `handoff-check` per costruzione.
- `f61d789` (fine-task del primo giro): `unit-suite` success, `handoff-check` success; `verifica-bot` neutral (macchina del bot), con V-1 corretta in questo giro.
- `475a84f`, `5ab30b3`: pushati insieme al commit di fine-task di questo giro; nessuna run propria.
- Commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova dal revisore.
- Da vedere alla prima verifica: se l'agente esterno riesce davvero a pubblicare il commento sulla PR.
- Note basse del bot su #177 (`.gitignore` per `.gas_history.json.*`, riga lunga in `notte.py`): prossima fetta motore.
