# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — Ritocchi finali del funnel dopo la prova dell'operatore (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #401 (https://github.com/Gasss23/Gas/pull/401), aperta con l'etichetta «verifica». Tocca file fuori dalla lista bianca dei log (funnel): serve il verdetto testuale del bot; merge autonomo solo con APPROVATO pulito, altrimenti decide l'operatore (che ha già chiesto di procedere coi ritocchi).
2. Consegnare allo sviluppatore del bot (su main dopo il merge): `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md`, `reports/funnel/simulazione_funnel.html`.
3. Ripristinare nel bot «Inizia Ora · Accesso» lo stato dell'operatore (bottoni «Conto aperto» / «In VIP»).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Tre ritocchi chiesti dall'operatore il 23/11 dopo la prova della simulazione**: FATTA.
  1. Via la domanda «Da quale community arrivi?» dalla fase 1 del percorso completo: si parte dalla lingua (con la conferma dei 18 anni). `funnel_v2.md` (prima regola comune + due rimandi allineati) e simulazione.
  2. Percorso diretto SOLO nome e cognome: messaggio unico (rischio+compenso), campo «Scrivimi nome e cognome» con la riga «Inviando confermi di avere almeno 18 anni e ci autorizzi a risponderti qui», poi [Scrivi a {agente}]. Consenso aggiornamenti non chiesto nel diretto: senza sì niente promozione (lo raccoglie l'agente in chat); i solleciti del caso B non sono promozione (restano indipendenti dal consenso come da regole comuni). `tasto_collaboratori.md` §3.1 e §4.5, simulazione (rimossa `ctaConConsenso`).
  3. Requisito Pannello blu (confermato dall'operatore su screenshot): «I miei link», card e link dell'agente si aprono DENTRO il Pannello esistente (bottone blu «Pannello» della chat del bot), nessuna app o pagina nuova. `tasto_collaboratori.md` §4.6, simulazione (scheda agente).
  La simulazione è stata ripubblicata sulla pagina pubblica claude.ai e PROVATA dal vivo nel browser dopo la ripubblicazione (le tre schede).

- **Fetta 2 — Correzioni del 1° verdetto del bot sulla PR #401 (secondo giro, scelta dell'operatore «Sistema prima»)**: FATTA. V-1 BASSA: dichiarata la lingua del diretto (`language_code` di Telegram, IT/EN, altrimenti italiano; la riga dei 18 anni segue la lingua del lead) in `tasto_collaboratori.md` §3.1 e §4.5 e nella simulazione. V-2 BASSA: §3/§6 di questo handoff aggiornati coi commit reali. V-3 COSMETICA: card del diretto «solo nome e cognome, subito l'ultimo passo» (spec §1 + simulazione) e «in basso nella chat» uniformato nell'intestazione. V-4 COSMETICA: la regola del consenso in `funnel_v2.md` ora rimanda all'eccezione del diretto. Simulazione ripubblicata.

- **Fetta 3 — Correzioni del 2° verdetto del bot sulla PR #401 (terzo giro) + merge di main**: FATTA. V-1 BASSA: la riga sul rischio (e quella «non ti chiede mai soldi») ora sta ANCHE nel messaggio dell'ultimo passo del diretto (`tasto_collaboratori.md` §3.1 + simulazione), come chiede la regola comune V-2 #392. V-2 COSMETICA: in `funnel_v2.md` la descrizione della fase 1 di oggi cita anche la domanda della community. V-3 COSMETICA: «Fetta unica» rinominata «Fetta 1» qui e in ultimo_report. In più: merge di origin/main nel ramo (era entrata la PR #398 della chat Voce; conflitto solo sui 3 report canonici, risolto `--ours`; `stato_progetto.md` auto-mergiato con le voci di entrambi i lati; review #851-MERGE APPROVATO, perimetro byte-identico a main — §4). Simulazione ripubblicata.

- **Fetta 4 — Correzioni del 3° verdetto del bot sulla PR #401 (quarto giro, proposta dell'agente approvata dall'operatore «riprendi pure», 24/11) + merge di main**: FATTA. V-1 BASSA: la conferma dei maggiorenni ora sta IN TESTA al messaggio unico del diretto, prima di ogni contenuto commerciale (e resta anche nella riga sotto il campo del nome) — `tasto_collaboratori.md` §3.1 e §4.5 + simulazione. V-2 BASSA: dichiarato che ai lead del diretto il bot non manda MAI promozione (nessun consenso chiesto né registrato; ogni comunicazione la fa l'agente in chat; per promozioni future servirà prima un bottone di consenso registrato) — §3.1, §4.5, regola del consenso di `funnel_v2.md`, simulazione. In più: secondo merge di origin/main nel ramo (erano entrate le PR #399 e #400; conflitti: 3 report canonici `--ours`, memoria del revisore a unione senza perdite; review #852-MERGE APPROVATO, perimetro byte-identico a main — §4). Simulazione ripubblicata.

Contesto: PR #396 (trigger solleciti) mergiata oggi col via dell'operatore dopo il 3° verdetto (APPROVATO CON RISERVE senza ALTA/MEDIA); la sua V-1 COSMETICA residua (nome «Fetta unica» accanto a «Fetta 2/3» nei log) è superata dalla riscrittura dei report per questa sessione. `reports/bacheca.md` letta prima del giro: nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = af0215de3491c5d6cae4f76183640d2d39063091 (merge-base con origin/main = main dopo il merge della PR #400, aggiornata dal 2° merge di main nel ramo al 4° giro).

```
 .claude/agents/memoria_revisore.md     |   2 ++
 reports/diff_sessione.md               |  22 +++++++++++++---------
 reports/funnel/funnel_v2.md            |   7 ++++---
 reports/funnel/simulazione_funnel.html |  54 ++++++++++++++----------------------------------------
 reports/funnel/tasto_collaboratori.md  |  19 +++++++++++++------
 reports/handoff.md                     | n/d
 reports/stato_progetto.md              |   2 +-
 reports/ultimo_report.md               |  59 +++++++++++++++++++++++++++--------------------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
e8f539a3 Merge remote-tracking branch 'origin/main' into claude/ritocchi-simulazione
05721612 docs(funnel): corrette le note del 3° verdetto su #401 — conferma 18 anni in testa al messaggio del diretto, niente promozioni del bot ai lead del diretto
35ca0faf docs(fine-task): 3° giro PR #401 — fix del 2° verdetto, merge di main (review #851-MERGE), handoff aggiornato
71dee2da Merge remote-tracking branch 'origin/main' into claude/ritocchi-simulazione
b926745a docs(funnel): corrette le note del 2° verdetto su #401 — riga del rischio nell'ultimo passo del diretto, fase 1 di oggi con la domanda community, Fetta 1
ee275e38 docs(funnel): corrette le note del 1° verdetto su #401 — lingua del diretto dichiarata, handoff coi commit reali, card e rimandi allineati
500cfa39 docs(fine-task): handoff §0 — PR #401 aperta con l'etichetta verifica
fb0f84af docs(funnel): ritocchi dell'operatore dopo la prova — via la domanda community, diretto solo nome e cognome con riga 18 anni, requisito Pannello blu per I miei link
```

NB: il commit di fine-task di QUESTO 4° giro (quello che contiene questo file) non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push. fb0f84af = fetta + fine-task 1° giro; 500cfa39 = §0 dopo l'apertura della PR; ee275e38 = 2° giro; b926745a = 3° giro; 71dee2da = 1° merge di main (review #851-MERGE); 35ca0faf = fine-task 3° giro; 05721612 = 4° giro (fix 3° verdetto); e8f539a3 = 2° merge di main (review #852-MERGE).

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore scritto da questa sessione (solo `reports/funnel/` e report canonici). Il commit di merge di origin/main (71dee2da, porta dentro la PR #398) tocca file del perimetro presi IDENTICI da main: review #851-MERGE, verdetto INTEGRALE:

```
## VERDETTO: APPROVATO

Review #851-MERGE: merge di origin/main (d13d4342, con dentro la PR #398 R7) nel ramo claude/ritocchi-simulazione (PR #401).

Ho letto CLAUDE.md §5, reports/stato_progetto.md (solo le parti trovate con grep: R7 e Funnel) e la mia memoria (coda fino a #850-R7).

Comandi eseguiti ed esiti:
1. `git diff --cached origin/main --stat -- gas.py brains/ modules/ tests/ scripts/ .claude/ .github/` non mostra niente: i file del perimetro sono identici byte per byte a origin/main. MERGE_HEAD = origin/main = d13d4342.
2. `git ls-files -u` dà 0 righe (nessun UU). `git diff --cached --check` è pulito. grep dei marcatori di conflitto (`<<<<<<<` e `>>>>>>>`) su reports/*.md: nessuno.
3. `git diff --cached HEAD --stat` su handoff.md, ultimo_report.md, diff_sessione.md e reports/funnel/ non mostra niente: la risoluzione `--ours` è confermata. `git diff` (albero rispetto all'indice) è vuoto.
4. `git diff --cached origin/main --stat` cambia solo file di reports/: 3 report canonici, 3 file del funnel e 1 riga di stato_progetto.md.

Elementi esaminati:
- reports/stato_progetto.md:10 — voce Funnel aggiornata da questa sessione. Rischio esaminato: che il merge automatico perdesse le voci dell'altro lato. Rispetto a origin/main cambia solo questa riga. Esito: ok.
- reports/stato_progetto.md:401 — voce «R7 fetta 2 — ripresa al boot … PR #398» presente, e c'è anche la riga 4 «Ultimo aggiornamento» che cita la #398. Rischio esaminato: decisioni e riserve della #398 perse. Esito: ok.
- reports/funnel/funnel_v2.md:9 — la fase 1 di oggi descritta con la domanda della community, che viene tolta nelle regole comuni (riga 13). Rischio esaminato: contraddizione tra «com'è oggi» e la bozza. È coerente. Esito: ok.
- reports/ultimo_report.md:21 — la Fetta 3 dichiara il merge di origin/main. Rischio esaminato: un report che non racconta il merge. Esito: ok.

Rischio escluso: non ho rivisto il contenuto di reports/funnel/simulazione_funnel.html (54 righe cambiate) né la correttezza di marketing e legale dei testi del funnel. Sono documenti fuori dal perimetro del motore, già passati dal bot sulla #401. Non ho rifatto girare i test della #398: il perimetro è identico a main, già verificato in #849/#850.
```

Secondo merge di origin/main (e8f539a3, porta dentro le PR #399 e #400): review #852-MERGE, verdetto INTEGRALE:

```
## VERDETTO: APPROVATO

Review #852-MERGE: secondo merge di origin/main (af0215de, con le PR #399 R7 fetta 3 e #400 voce) in claude/ritocchi-simulazione (PR #401, solo documenti).

Comandi ed esiti:
1. `git diff --cached origin/main --stat -- gas.py brains/ modules/ tests/ scripts/ .claude/ .github/ clients/` → solo `.claude/agents/memoria_revisore.md | 1 +`. Il resto del perimetro è identico byte per byte a main, compresi modules/notte, clients/voice e i test di #399/#400.
2. `git ls-files -u | wc -l` → 0. Grep dei marcatori su handoff, ultimo_report, diff_sessione, memoria e stato_progetto → nessun risultato.
3. `git show origin/main:.claude/agents/memoria_revisore.md | diff - <(git show :.claude/agents/memoria_revisore.md)` → una sola riga aggiunta (la #851-MERGE), nessuna riga tolta. Le righe di main #848-R7, #851-MERGE-R7 e #822-M1coord ci sono. È un'unione senza perdite.
4. `git diff --cached --quiet HEAD -- reports/{handoff,ultimo_report,diff_sessione}.md` → tutti e tre identici a HEAD (risolti `--ours`, regola 3).
5. `git diff --cached origin/main -- reports/stato_progetto.md` → cambia solo la voce Funnel (1 riga tolta, 1 aggiunta). C'è una sola riga `^> Ultimo aggiornamento`.
6. `git diff --cached --check origin/main` → pulito (gli spazi in coda nei `.patch` di reports/voce_simulazione_2026-11-23/ arrivano da main identici: il merge non li introduce).

Rischio escluso: non ho rilanciato la suite dei test. Il codice del perimetro è identico a origin/main, quindi il risultato dei test è quello di main, già verificato da #848-R7 e #822-M1coord. Non ho riletto nel merito i file della voce né i documenti del funnel: fuori dal perimetro di questa review di merge.
```

NB: dopo il verdetto la riga #852-MERGE della memoria è stata messa in stage col commit di merge: il diff della memoria contro main è di 2 righe (#851-MERGE e #852-MERGE), come annunciato dal revisore.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura del 4° giro (righe di main e della sessione CRM, attiva in parallelo):

```
completed	skipped	CRM: dashboard sempre accesa sul Mac, icona sulla Scrivania	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	45397504753	2s	2026-11-24T12:51:02Z
in_progress		feat(crm): dashboard sempre accesa sul Mac — LaunchAgent com.gas.crm,…	CI	claude/nifty-galileo-3k7kbm	push	45397492179	18s	2026-11-24T12:50:57Z
completed	success	Merge pull request #400 from Gasss23/fix/voce-fasi-interruzione	CI	main	push	45301412525	11m55s	2026-11-24T00:58:18Z
```

Mappatura commit→run: fb0f84af e 500cfa39 pushati insieme → una sola run CI 45228489192 success sull'albero di 500cfa39 (fb0f84af senza run propria, contenuto incluso nell'albero testato); verifica-bot del 1° verdetto su 500cfa39 success. ee275e38 (head 2° giro): run CI 45231282200 success + verifica-bot del 2° verdetto success. b926745a, 71dee2da e 35ca0faf: pushati insieme → run CI 45233853494 success (unit-suite 11m46s) sull'albero di 35ca0faf (head 3° giro; i due commit intermedi senza run propria) + verifica-bot del 3° verdetto success. 05721612 ed e8f539a3: nessuna run su questi SHA alla scrittura (vanno col push del commit di fine-task di questo 4° giro, che avrà la run sull'albero di testa). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- V-1 COSMETICA del 3° verdetto bot sulla PR #396 (nome «Fetta unica» accanto a «Fetta 2/3» nei log di quella sessione): SUPERATA — i report sono riscritti per questa sessione.
- 1° verdetto del bot su PR #401 (500cfa39, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (lingua del diretto non dichiarata), V-2 BASSA (§3/§6 dell'handoff con «un solo commit»), V-3 COSMETICA (card «niente domande», «in basso a sinistra»), V-4 COSMETICA (eccezione del diretto assente dalla regola del consenso in funnel_v2) — CORRETTE nel 2° giro (Fetta 2); il 2° verdetto le ha date per chiuse.
- 2° verdetto del bot su PR #401 (ee275e38, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (riga del rischio assente dall'ultimo passo del diretto), V-2 COSMETICA (descrizione della fase 1 di oggi senza la domanda della community), V-3 COSMETICA («Fetta unica» accanto a «Fetta 2») — CORRETTE nel 3° giro (Fetta 3).
- 3° verdetto del bot su PR #401 (35ca0faf, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (conferma 18 anni dopo la presentazione commerciale nel diretto), V-2 BASSA (consenso promo del diretto non tracciato) — CORRETTE in questo 4° giro (Fetta 4) con la proposta dell'agente approvata dall'operatore; serve il verdetto del bot sul nuovo head.
- Riserve delle altre chat (CRM #397, Voce): tracciate in `reports/stato_progetto.md`, non toccate qui.
