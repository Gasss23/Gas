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

- **Fetta 4 — Correzioni del 3° verdetto del bot sulla PR #401 (quarto giro, proposta dell'agente approvata dall'operatore «riprendi pure», 24/11) + merge di main**: FATTA. V-1 BASSA: la conferma dei maggiorenni ora sta IN TESTA al messaggio unico del diretto, prima di ogni contenuto commerciale (e resta anche nella riga sotto il campo del nome) — `tasto_collaboratori.md` §3.1 e §4.5 + simulazione. V-2 BASSA: dichiarato che ai lead del diretto il bot non manda MAI promozione (nessun consenso chiesto né registrato; ogni comunicazione la fa l'agente in chat; per promozioni future servirà prima un bottone di consenso registrato) — §3.1, §4.5, regola del consenso di `funnel_v2.md`, simulazione. In più: secondo merge di origin/main nel ramo (erano entrate le PR #399 e #400). Simulazione ripubblicata.

Contesto: PR #396 (trigger solleciti) mergiata oggi col via dell'operatore dopo il 3° verdetto (APPROVATO CON RISERVE senza ALTA/MEDIA); la sua V-1 COSMETICA residua (nome «Fetta unica» accanto a «Fetta 2/3» nei log) è superata dalla riscrittura dei report per questa sessione. `reports/bacheca.md` letta prima del giro: nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = d13d4342fc60eabea8cb9f75232143ad2a177506 (merge-base con origin/main = main dopo il merge della PR #398, aggiornata dal merge di main nel ramo al 3° giro).

```
 .claude/agents/memoria_revisore.md     |   1 +
 reports/diff_sessione.md               |  21 ++++++++++++---------
 reports/funnel/funnel_v2.md            |   7 ++++---
 reports/funnel/simulazione_funnel.html |  54 ++++++++++++++----------------------------------------
 reports/funnel/tasto_collaboratori.md  |  17 +++++++++++------
 reports/handoff.md                     | n/d
 reports/stato_progetto.md              |   2 +-
 reports/ultimo_report.md               |  31 +++++++++++++++++--------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
71dee2da Merge remote-tracking branch 'origin/main' into claude/ritocchi-simulazione
b926745a docs(funnel): corrette le note del 2° verdetto su #401 — riga del rischio nell'ultimo passo del diretto, fase 1 di oggi con la domanda community, Fetta 1
ee275e38 docs(funnel): corrette le note del 1° verdetto su #401 — lingua del diretto dichiarata, handoff coi commit reali, card e rimandi allineati
500cfa39 docs(fine-task): handoff §0 — PR #401 aperta con l'etichetta verifica
fb0f84af docs(funnel): ritocchi dell'operatore dopo la prova — via la domanda community, diretto solo nome e cognome con riga 18 anni, requisito Pannello blu per I miei link
```

NB: il commit di fine-task di QUESTO 3° giro (quello che contiene questo file) non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push. fb0f84af = fetta + fine-task 1° giro; 500cfa39 = §0 dopo l'apertura della PR; ee275e38 = 2° giro (fix 1° verdetto); b926745a = 3° giro (fix 2° verdetto); 71dee2da = merge di origin/main (review #851-MERGE, §4).

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

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura del 3° giro (righe delle sessioni Voce/R7, attive in parallelo):

```
in_progress		fix(voce): 4 fasi sfalsate per «Hey Jarvis», interruzione col filtro, taratura coerente (simulazione end-to-end, M1)	verifica-bot	fix/voce-fasi-interruzione	pull_request_target	45233449449	1m31s	2026-11-23T17:58:58Z
in_progress		docs(fine-task): §2/§3 handoff dopo il merge di main	CI	fix/voce-fasi-interruzione	push	45233443670	1m33s	2026-11-23T17:58:56Z
completed	success	R7 fetta 3: stato dei lavori ricorrenti del giro di notte	verifica-bot	claude/r7-lavori-ricorrenti	pull_request_target	45231777972	3m47s	2026-11-23T17:49:24Z
```

Mappatura commit→run: fb0f84af e 500cfa39 pushati insieme → una sola run CI 45228489192 success (unit-suite 11m39s e handoff-check) sull'albero di 500cfa39; fb0f84af senza run propria (contenuto incluso nell'albero testato); verifica-bot del 1° verdetto su 500cfa39 success. ee275e38 (head del 2° giro): run CI 45231282200 success (unit-suite 10m50s) e verifica-bot del 2° verdetto success. b926745a e 71dee2da: nessuna run su questi SHA alla scrittura (verranno pushati insieme al commit di fine-task di questo 3° giro, che avrà la run del push sull'albero di testa; i due commit intermedi restano senza run propria). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- V-1 COSMETICA del 3° verdetto bot sulla PR #396 (nome «Fetta unica» accanto a «Fetta 2/3» nei log di quella sessione): SUPERATA — i report sono riscritti per questa sessione.
- 1° verdetto del bot su PR #401 (500cfa39, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (lingua del diretto non dichiarata), V-2 BASSA (§3/§6 dell'handoff con «un solo commit»), V-3 COSMETICA (card «niente domande», «in basso a sinistra»), V-4 COSMETICA (eccezione del diretto assente dalla regola del consenso in funnel_v2) — CORRETTE nel 2° giro (Fetta 2); il 2° verdetto le ha date per chiuse.
- 2° verdetto del bot su PR #401 (ee275e38, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (riga del rischio assente dall'ultimo passo del diretto), V-2 COSMETICA (descrizione della fase 1 di oggi senza la domanda della community), V-3 COSMETICA («Fetta unica» accanto a «Fetta 2») — CORRETTE nel 3° giro (Fetta 3).
- 3° verdetto del bot su PR #401 (35ca0faf, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (conferma 18 anni dopo la presentazione commerciale nel diretto), V-2 BASSA (consenso promo del diretto non tracciato) — CORRETTE in questo 4° giro (Fetta 4) con la proposta dell'agente approvata dall'operatore; serve il verdetto del bot sul nuovo head.
- Riserve delle altre chat (CRM #397, Voce): tracciate in `reports/stato_progetto.md`, non toccate qui.
