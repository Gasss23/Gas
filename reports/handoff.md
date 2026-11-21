# HANDOFF — Dossier di fine sessione

**Sessione:** 21 novembre 2026 — Funnel community: analisi competitor, funnel v2, tasto collaboratori (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #392 (https://github.com/Gasss23/Gas/pull/392).
2. Consegnare `reports/funnel/funnel_v2.md` (Bozza B, scelta dall'operatore il 21/11 in chat) e `reports/funnel/tasto_collaboratori.md` a chi mantiene il bot «Inizia Ora · Accesso» (non è nel repo Gas).
3. Far controllare i testi del funnel a un esperto di promozione finanziaria/privacy prima dell'uso (raccomandazione della verifica esterna #392).
4. Il repo è PUBBLICO e `reports/funnel/analisi_competitor.md` cita testi della chat privata con «LEO SUPPORTO» e nomi di canali/persone (nota della verifica esterna #392): decidere se va bene così o se l'analisi va anonimizzata/spostata fuori dal repo pubblico.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Mappatura funnel attuale del bot «Inizia Ora · Accesso»**: FATTA. Ricostruito dalla cronologia del test del 18/11: presentazione, 7 domande a risposta multipla, «ultimo passo» con messaggio precompilato all'agente, scheda lead, guida agenti, /pannello. La mini app «Pannello» non si apre dall'automazione (non bloccante).
- **Fetta 2 — Analisi competitor Telegram**: FATTA. 9 canali della cartella «Competitor» analizzati (canali pubblici, bot di ingresso, cronologie esistenti). Risultato: `reports/funnel/analisi_competitor.md`.
- **Fetta 3 — Funnel v2 in due bozze (vocale vs messaggi)**: FATTA. Copy completo e confronto in `reports/funnel/funnel_v2.md`.
- **Fetta 4 — Tasto 2 link per i collaboratori**: FATTA COME SPECIFICA (`reports/funnel/tasto_collaboratori.md`): il codice del bot non è nel repo Gas né altrove sul Mac/GitHub dell'account; implementazione a carico di chi mantiene il bot.
- **Fetta 5 — Scrivere ai competitor fingendosi clienti**: SALTATA — limite di sicurezza dell'agente (niente messaggi a persone reali sotto falsa identità). Compensata leggendo i bot automatici e la cronologia già esistente (chat «LEO SUPPORTO» = loro intero processo di vendita). Nessun messaggio inviato ai competitor. L'unica bozza cancellata nei composer è quella auto-generata dal clic sul link «ENTRA ORA» di Luke World (mai inviata); la bozza preesistente in «LEO SUPPORTO» è rimasta com'era (V-6 bot).
- **Fetta 7 — Secondo passaggio su Telegram (richiesta dell'operatore in corsa)**: FATTA. Funnel nostro rifatto dal vivo (/cancellami + /start): due fasi, tutte le opzioni di risposta catturate («Li avrò a breve» e consenso esplicito GIÀ presenti nel bot); bozze/analisi corrette. Altri competitor: Gold Signals, LTD-CAPITAL, CNS VIP, Shmek, Invest360; bot ALE STARK provato fino al passaggio all'umano (vocale 1:08), lì fermato. Il vecchio bot «welcome REF» non risponde a /links e /stats. Stato dell'operatore nel bot dopo il test: «Candidato — pronto per la VIP» (si rimette con Conto aperto / In VIP sulla scheda).
- **Fetta 6 — Scelta Bozza B + correzioni del bot (secondo giro)**: FATTA. Operatore: Bozza B (messaggi). Corretti V-1 (scarsità finta tolta dal sollecito +72 h), V-2 (avviso rischio + trasparenza sul compenso in presentazione, ultimo passo e card collaboratori), V-3 (consenso esplicito con bottoni Sì/No), V-4 (merge di origin/main f75e09a2 nel branch, conflitti risolti sui soli report canonici tenendo la versione del ramo; review #834-MERGE APPROVATO), V-5/V-6/V-7 (handoff e ultimo_report corretti).

---

## §2 GIT DIFF --STAT (sessione)

BASE = f75e09a238835e7c2b7430ca6a71856af50962c6 (merge-base con origin/main dopo il merge di main nel branch).

```
 .claude/agents/memoria_revisore.md    |   1 +
 reports/diff_sessione.md              |  23 +++++++++----------
 reports/funnel/analisi_competitor.md  |  62 +++++++++++++++++++++++++++++++++++++++++++++++++
 reports/funnel/funnel_v2.md           |  80 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/funnel/tasto_collaboratori.md |  46 +++++++++++++++++++++++++++++++++++++
 reports/handoff.md                    | n/d
 reports/stato_progetto.md             |   2 +-
 reports/ultimo_report.md              |  53 ++++++++++++++++++------------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path. `.claude/agents/memoria_revisore.md` è la riga #834-MERGE aggiunta dal revisore.

## §3 GIT LOG --ONELINE (sessione)

```
1188739 Merge remote-tracking branch 'origin/main' into claude/funnel-community
e8c67c5 docs(fine-task): handoff — PR #392 aperta con l'etichetta verifica
f40f2b3 docs(funnel): analisi competitor Telegram, funnel v2 in due bozze (vocale/messaggi) e specifica tasto /linkmiei per i collaboratori
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore scritto in sessione. Il merge di origin/main (commit 1188739) porta nello staged file del perimetro byte-identici a main: revisionato comunque dal revisore, verdetto integrale:

```
## VERDETTO: APPROVATO

Review #834-MERGE. Oggetto: il merge in preparazione di origin/main (f75e09a2) nel ramo claude/funnel-community (HEAD e8c67c55, PR #392, sessione solo documenti).

**Cosa ho controllato**
- Nessun conflitto rimasto: `git ls-files -u` è vuoto, nessun marcatore `<<<<<<<`/`=======`/`>>>>>>>` nei file di reports/, `git diff --cached --check` è pulito. L'albero di lavoro è uguale all'indice.
- Ho rieseguito io il comando `git diff --cached origin/main -- gas.py brains/ modules/ tests/ scripts/ .claude/ .github/`: è VUOTO. Contro main cambiano solo 7 file sotto reports/: i 3 file di reports/funnel/, ultimo_report, handoff, diff_sessione e stato_progetto.

**Elementi del diff esaminati**
- `modules/crm/server.py:273` — firma di `_segna_copia` con il nuovo parametro `locale` e il testo dell'avviso che cambia a seconda del caso. Rischio esaminato: codice del motore entrato con il merge senza review. Esito: ok. Il file è identico byte per byte a origin/main, dove è già stato revisionato (#822–#823).
- `modules/crm/copia_cifrata.py:57` — modifiche a `cartella()` e alla gestione dei permessi sulla cartella delle copie, arrivate dalla PR #387. Rischio esaminato: differenze rispetto alla versione revisionata. Esito: ok, il contenuto coincide con main.
- `scripts/bot_esito.py:180` — `_GRAVITA_NEGATA` con `\b[Nn]on` (PR #389). Rischio esaminato: la regola del bot che fa da check required cambiata di nascosto. Esito: ok, identica a main (review #831–#833).
- `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento». Rischio esaminato: un'unione automatica che perde righe. Esito: ok. Contro main cambia solo l'intestazione del 21/11 presa dal ramo. Contro HEAD entrano solo la riga del bot «Non bloccante» e la riga CRM aggiornata da main.
- Report canonici `reports/ultimo_report.md:1`, `reports/handoff.md:1`, `reports/diff_sessione.md:1` — risoluzione dei conflitti. Esito: ok. I blob nell'indice sono identici a quelli di HEAD (versione del ramo), il che è coerente: si riscrivono a ogni sessione e questa è la più recente. Anche `reports/funnel/funnel_v2.md` è identico a HEAD.

**Rischi esclusi**
- Non ho rieseguito i test (crm e verifica_bot). Il codice è identico a main, quindi la verifica resta alla CI del ramo dopo il push.
- Non ho controllato nel merito i contenuti del funnel (reports/funnel/*). Sono fuori dal perimetro di review e non toccano il motore.
- Wall of Shame (tagliare la cronologia con `[-10:]` o simili, inventare l'output dei tool): non si applica, il merge non porta codice nuovo.

**Nota fuori dal diff:** stato_progetto.md è a 974 righe, contro le ~100 indicate da CLAUDE.md §11. È un problema che c'era già, non introdotto da questo merge.
```

NB: le correzioni ai testi del funnel COMMITTATE DOPO il merge (V-1/V-2/V-3 e report) toccano solo reports/: fuori dal perimetro, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 4` alla scrittura:

```
completed	success	docs(funnel): analisi competitor, funnel v2 e tasto collaboratori	verifica-bot	claude/funnel-community	pull_request_target	44937326141	2m46s	2026-11-21T18:46:18Z
completed	success	docs(fine-task): handoff — PR #392 aperta con l'etichetta verifica	CI	claude/funnel-community	push	44937323388	13m6s	2026-11-21T18:46:16Z
completed	cancelled	docs(funnel): analisi competitor, funnel v2 e tasto collaboratori	verifica-bot	claude/funnel-community	pull_request_target	44937305362	24s	2026-11-21T18:46:03Z
completed	cancelled	docs(funnel): analisi competitor, funnel v2 e tasto collaboratori	verifica-bot	claude/funnel-community	pull_request_target	44937303663	52s	2026-11-21T18:46:02Z
```

Mappatura commit→run: f40f2b3 ed e8c67c5 pushati insieme → run CI 44937323388 (success) sull'albero di e8c67c5; f40f2b3 non ha una run propria. La run verifica-bot 44937326141 (success come run; esito del CHECK: failure = finding MEDIE, verdetto nel commento sulla PR) è su e8c67c5. Il merge 1188739 e il commit di fine-task di questo giro: run non ancora disponibile alla scrittura dell'handoff (partono col push). La copertura pre-merge è garantita da `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

Dal verdetto del bot (verifica esterna #392, commento sulla PR) su e8c67c5:
- V-1 (MEDIA, scarsità finta), V-2 (MEDIA, rischio/compenso), V-3 (MEDIA, consenso), V-4 (MEDIA, conflitto con main), V-5/V-6 (BASSE, §3 e bozze Telegram), V-7 (COSMETICA, §6): CORRETTE in questo giro; serve il nuovo verdetto del bot sul nuovo head.
- RESTANO APERTE: (a) far controllare i testi del funnel a un esperto di promozione finanziaria/privacy prima dell'uso; (b) il repo è pubblico e `analisi_competitor.md` cita testi di chat private e nomi: decisione dell'operatore (§0 punto 4).
