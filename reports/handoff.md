# HANDOFF — Dossier di fine sessione

**Sessione:** 21 novembre 2026 — Simulazione cliccabile del funnel + conteggi vecchi nei report (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #393 (https://github.com/Gasss23/Gas/pull/393), aperta con l'etichetta «verifica». La PR tocca anche un file fuori dalla lista bianca dei log (`simulazione_funnel.html`): serve il verdetto testuale del bot; merge autonomo solo con APPROVATO pulito, altrimenti decide l'operatore.
2. Provare la simulazione `reports/funnel/simulazione_funnel.html` e decidere lì eventuali ritocchi ai testi prima della consegna allo sviluppatore.
3. Consegnare allo sviluppatore del bot: `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md`, più la simulazione come riferimento visivo.
4. Far controllare i testi del funnel a un esperto di promozione finanziaria/privacy prima dell'uso (verifica esterna #392).
5. Ripristinare lo stato dell'operatore nel bot (bottoni «Conto aperto» / «In VIP» sulla scheda).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Simulazione cliccabile del funnel (richiesta dell'operatore)**: FATTA. `reports/funnel/simulazione_funnel.html`, pagina autonoma stile Telegram con tre percorsi: lead completo (fase 1 di oggi invariata + candidatura Bozza B a 3 passaggi, reazioni calde, follow-up +24/+72 h), lead diretto `-vip` (tutele 18+/rischio/compenso/consenso incluse), vista agente del Pannello «I miei link» (2 link, contatori, card da inoltrare). Testi presi dalle fonti (`funnel_v2.md`, `tasto_collaboratori.md` e, per la fase 1 di oggi, `analisi_competitor.md` §1); le poche righe NON fissate dalle specifiche (reazioni calde a capitale/consenso, sollecito del percorso diretto) sono proposte dell'agente, marcate con * nella pagina stessa; l'«ultimo passo» usa il testo della Bozza A di `funnel_v2.md` più la riga sul rischio (V-1/V-2 del 2° verdetto). Provata dal vivo dall'agente nel browser: tutti e tre i percorsi completati, follow-up compresi. Copia privata pubblicata come pagina claude.ai per il test dell'operatore; fonte unica = il file nel repo.
- **Fetta 3 — Correzioni del 1° verdetto del bot sulla PR #393 (secondo giro)**: FATTA. V-1 BASSA: contatore di generazione in `start()`, ogni helper (typing/kb/askText) rifiuta dopo l'await se la generazione è cambiata — niente più percorsi mescolati cambiando scheda a metà «sta scrivendo…»; verificato dal vivo. V-2 BASSA: il claim «testi alla lettera» fu corretto nei report; le righe proposte dall'agente (reazioni calde a capitale/consenso, sollecito del diretto) FURONO marcate con * nella pagina; l'«ultimo passo», allora ricostruito e marcato, dalla Fetta 4 usa il testo della Bozza A di funnel_v2 e non ha più il marcatore (vedi Fetta 4); percorso diretto riallineato alla spec §3.1: [Scrivi a {agente}] attaccato al messaggio, consenso SOTTO, visibili insieme; il sollecito del diretto non parla più di «candidatura». V-3 COSMETICA: messaggi con textContent al posto di innerHTML (input del nome compreso). Pagina ripubblicata e riverificata nel browser.
- **Fetta 5 — Correzioni del 3° verdetto del bot (quarto giro)**: FATTA. V-1 BASSA: `followUp()` ora ramifica anche il sollecito a +72 h su `tipo` — nel diretto niente «candidatura» (testo marcato con *, bottoni Riprendi/Chiudi); verificato dal vivo nel browser. V-2 COSMETICA: testi riallineati alle fonti — tolta la numerazione «1/3-2/3-3/3», tolta l'emoji aggiunta a «Imparare a farlo da solo», «Sei già nella community.» come in `analisi_competitor.md` §1. Pagina ripubblicata.
- **Fetta 6 — Correzioni del 4° verdetto del bot (quinto giro)**: FATTA. V-1 BASSA: l'incoerenza dei solleciti del percorso completo (testo «30 secondi di candidatura» dopo la candidatura già accettata) viene dalle FONTI (funnel_v2 regole comuni: «chi si ferma a metà»; Bozza B: «chi non preme Scrivi a»): nella pagina ora una nota * la dichiara e rimanda alla decisione dell'operatore (`ultimo_report.md` punto 1bis, con proposta: due trigger, due testi); i testi delle fonti restano invariati in attesa della scelta. V-2 COSMETICA: la riga superata della Fetta 3 è riscritta al passato con rimando alla Fetta 4. Pagina ripubblicata.
- **Fetta 2 — Nota bassa del 3° verdetto del bot sulla PR #392 (conteggi vecchi)**: FATTA/SUPERATA. La PR #391 (CRM), mergiata nel frattempo, ha riscritto i report di sessione su main: «7 domande»/«4 domande» su origin/main NON esistono più (grep vuoto, verificato). I report di questa sessione li sostituiscono come fotografia più recente senza riproporli; la descrizione corretta (due fasi) sta in `analisi_competitor.md` §1 e `funnel_v2.md`.
- **Fetta 4 — Correzioni del 2° verdetto del bot + merge di main (terzo giro)**: FATTA. V-1 BASSA (claim «alla lettera» rimasto nella Fetta 1 di questo handoff): allineato al testo di `ultimo_report.md`. V-2 BASSA («ultimo passo» non marcato con * nella pagina): adottata l'opzione suggerita dal bot — il messaggio ora usa il testo della Bozza A (`funnel_v2.md`) più la riga sul rischio, quindi non serve il marcatore. V-3 COSMETICA: la bolla della risposta al consenso nel percorso diretto compare sopra la tastiera (wrap.before) e `nome` si azzera a ogni `start()` (niente nome che trapela tra le schede). In più: merge di origin/main (PR #390 fix voce) nel branch per il conflitto sui report canonici, risolto tenendo la versione del ramo (vedi §4); pagina ripubblicata e riverificata.

Contesto: la PR #392 (funnel community) è stata mergiata in main (7cf5235) col sì dell'operatore in chat («Lascia e mergia», verdetto bot APPROVATO CON RISERVE senza ALTA/MEDIA). Questo branch riparte da main eecf916 (post #391); al terzo giro, merge di origin/main nel branch (019c6c8, per il conflitto creato dalla #390 sui report canonici — vedi Fetta 4 e §4). Le decisioni ancora aperte della sessione CRM (#391) sono riportate in `ultimo_report.md`.

---

## §2 GIT DIFF --STAT (sessione)

BASE = dcedea6a7a9432940fe0591f5a89133ef8b48f10 (merge-base con origin/main = main dopo il merge della PR #390, aggiornato dal merge 019c6c8 nel branch).

```
 .claude/agents/memoria_revisore.md     |   1 +
 reports/diff_sessione.md               |  21 +++++++++----------
 reports/funnel/simulazione_funnel.html | 276 ++++++++++++++++++++++++++++++++
 reports/handoff.md                     | n/d
 reports/ultimo_report.md               |  51 ++++++++++++++++++++++----------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path. `.claude/agents/memoria_revisore.md` è la riga #837-MERGE aggiunta dal revisore.

## §3 GIT LOG --ONELINE (sessione)

```
9fe5132 docs(funnel): simulazione — corretti i finding del 3° verdetto del bot (V-1 sollecito +72h del diretto, V-2 testi riallineati alle fonti)
444d08a docs(funnel): simulazione — corretti i finding del 2° verdetto del bot (V-1 handoff, V-2 ultimo passo da funnel_v2, V-3 bolla consenso e nome); merge di main nel branch
019c6c8 Merge remote-tracking branch 'origin/main' into claude/simulazione-funnel
6185f33 docs(funnel): simulazione — corretti i finding del 1° verdetto del bot sulla #393 (V-1 generazioni, V-2 testi marcati e ordine del diretto, V-3 textContent)
0de4046 docs(fine-task): handoff — PR #393 aperta con l'etichetta verifica
55bab38 docs(funnel): simulazione cliccabile del funnel (Bozza B, link diretto, Pannello «I miei link»); nota bassa del bot sulla #392 superata
```

NB: il commit di fine-task di QUESTO giro (il settimo del branch, che contiene questo file) non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push. Dei commit sopra, 0de4046, 6185f33, 444d08a e 9fe5132 erano i commit di fine-task dei giri precedenti; 019c6c8 è il merge di main (review #837-MERGE, §4).

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore SCRITTO in sessione (solo `reports/`: tre report canonici + una pagina HTML statica di simulazione, senza dipendenze esterne e senza dati inviati). Il merge di origin/main (commit 019c6c8, terzo giro) porta nello staged file del perimetro byte-identici a main: revisionato comunque dal revisore, verdetto integrale:

```
## VERDETTO: APPROVATO

Il merge in corso di origin/main dcedea6a (PR #390, correzione della voce) nel ramo claude/simulazione-funnel è stato verificato. HEAD è 6185f337, la PR è la #393, la base comune è eecf916d. I tre punti richiesti sono tutti a posto.

**Elementi esaminati**
- `scripts/voce/registra_voce.py:108` — è codice della voce che arriva da main (`def cartella`). Rischio: che il file del perimetro entri diverso dalla versione già revisionata sulla #390. Il blob nell'indice è 0cad38f6, uguale a origin/main. Esito: ok.
- `tests/test_unit_voce_ascolto.py:1` — è il test della voce che arriva da main. Rischio: un test diverso da quello che la CI di main ha già fatto passare. Il blob nell'indice è b5d9b376, uguale a origin/main. Esito: ok.
- `reports/stato_progetto.md:7` — preso da main (blob acc6d437). Rischio: perdere righe scritte sul ramo. Il diff base..HEAD non tocca questo file, quindi non si perde niente. Esito: ok.
- `reports/handoff.md:1` — tenuto dal ramo (blob ad775498 = HEAD). Rischio: che il ramo cancelli un contenuto di main che serve. È uno dei report che si riscrivono a ogni sessione e questa è la sessione più recente; vale lo stesso per `reports/ultimo_report.md:1` (blob = HEAD) e `reports/diff_sessione.md:1` (blob = HEAD). Esito: ok.
- `.claude/agents/memoria_revisore.md:1` — nell'indice c'è la versione di main (ff788f56). Il diff base..HEAD non tocca questo file, quindi non si perde niente. Esito: ok.

**Controlli meccanici**
1. `git ls-files -u` è vuoto, non ci sono marcatori di conflitto in reports/ e `git diff --cached --check` è pulito. L'albero di lavoro è uguale all'indice.
2. `git diff --cached origin/main` su gas.py, brains/, modules/, tests/, scripts/, .claude/ e .github/ è vuoto: il perimetro entra identico byte per byte a main.
3. Contro origin/main cambiano solo 4 file, tutti sotto reports/: `reports/diff_sessione.md`, `reports/handoff.md`, `reports/ultimo_report.md` e `reports/funnel/simulazione_funnel.html`. Quest'ultimo è nuovo, con blob 033dac14 uguale a HEAD.

Nessun antipattern della sez. 5 di CLAUDE.md: il merge non porta codice del motore nuovo.

**Rischi esclusi**
- I test non li ho rieseguiti: il codice è identico a main, già passato dalla CI della #390.
- Non ho controllato che `reports/funnel/simulazione_funnel.html` sia corretto: è del ramo, già revisionato sulla #393, e il merge non lo cambia.

**Memoria**
- Ho aggiunto in coda a `/Users/gas/Gas/.claude/agents/memoria_revisore.md` la riga contatore `#837-MERGE — 2026-11-21 — APPROVATO — … Nessuna lezione nuova.`. L'ultimo numero era 836.
- `scripts/commit_memoria_revisore.sh` non l'ho lanciato, come nella #834: un commit di un solo file durante un merge in corso sarebbe un commit parziale. La riga è solo nell'albero di lavoro, quindi la devi mettere tu in staging (`git add .claude/agents/memoria_revisore.md`) prima di chiudere il merge.
- Dopo questo add l'indice non è più quello che ho revisionato: lancia `bash scripts/segna_review_ok.sh` solo dopo l'add.
```

NB: le correzioni del terzo giro (V-1/V-2/V-3 del 2° verdetto) toccano solo reports/: fuori dal perimetro, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	success	docs(funnel): simulazione cliccabile del funnel (Bozza B, link diretto, Pannello «I miei link»); nota bassa del bot sulla #392 superata	verifica-bot	claude/simulazione-funnel	pull_request_target	44957676510	2m40s	2026-11-21T22:37:02Z
completed	success	docs(funnel): simulazione — corretti i finding del 3° verdetto del bo…	CI	claude/simulazione-funnel	push	44957674167	13m18s	2026-11-21T22:37:00Z
completed	success	docs: bacheca comune tra le chat; risposte dell'operatore sul CRM	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	44954979298	2m10s	2026-11-21T22:06:22Z
```

Mappatura commit→run: sull'head del 1° giro (0de4046) run CI 44951186868 e verifica-bot 44951189268, entrambe success (unit-suite 12m14s pass; 1° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA); 55bab38 senza run propria completata (push superato pochi secondi dopo). Sull'head del 2° giro (6185f33) run CI 44952713972 e verifica-bot 44952716514, entrambe success (unit-suite 14m14s pass; 2° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA). Sull'head del 3° giro (444d08a) run CI 44954281947 e verifica-bot 44954284114, entrambe success (unit-suite 11m55s pass; 3° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA); 019c6c8 (merge di main) senza run propria (pushato insieme a 444d08a, testato nel suo albero). Sull'head del 4° giro (9fe5132) run CI 44957674167 e verifica-bot 44957676510, entrambe success (unit-suite 13m14s pass; 4° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA) — sono le prime due run del blocco qui sopra. Il commit di fine-task di questo 5° giro: run non ancora disponibile alla scrittura dell'handoff (parte col push). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- 1° verdetto del bot su PR #393 (0de4046): V-1/V-2/V-3 CORRETTE (Fetta 3); il 2° verdetto (su 6185f33) le dà chiuse (V-1 e V-3 «CHIUSA», V-2 «parzialmente», completata nel terzo giro).
- 2° verdetto del bot su PR #393 (6185f33, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1/V-2/V-3 CORRETTE (Fetta 4); il 3° verdetto (su 444d08a) le dà chiuse.
- 3° verdetto del bot su PR #393 (444d08a, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1/V-2 CORRETTE (Fetta 5); il 4° verdetto (su 9fe5132) le dà chiuse. L'operatore ha scelto in chat «Prima i fix».
- 4° verdetto del bot su PR #393 (9fe5132, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (solleciti del completo incoerenti dopo la candidatura accettata — incoerenza che sta nelle FONTI: funnel_v2 regole comuni vs Bozza B) → nota * nella pagina + decisione per l'operatore in ultimo_report punto 1bis (trigger unico da fissare in funnel_v2 dopo il merge); V-2 COSMETICA (riga superata in Fetta 3) → riscritta. Entrambe trattate in questo giro (Fetta 6); serve il verdetto del bot sul nuovo head.
- Nota bassa del 3° verdetto bot su PR #392 (conteggi vecchi nei report): SUPERATA — vedi Fetta 2 (già assenti su main dopo la #391; non riproposti qui).
- RESTA APERTA: far controllare i testi del funnel a un esperto di promozione finanziaria/privacy prima dell'uso.
- R-836-1 COSMETICA (sessione CRM #391, fuori da questa sessione): messaggio d'errore del test sysctl meno chiaro se manca un parametro.
