# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — Trigger dei solleciti deciso (caso A / caso B) in funnel_v2 e nella simulazione (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #396 (https://github.com/Gasss23/Gas/pull/396), aperta con l'etichetta «verifica». Tocca file fuori dalla lista bianca dei log (funnel_v2, simulazione): serve il verdetto testuale del bot; merge autonomo solo con APPROVATO pulito, altrimenti decide l'operatore.
2. Consegnare allo sviluppatore del bot (su main dopo il merge): `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md` (regola dei solleciti ora completa), `reports/funnel/simulazione_funnel.html`.
3. Decisioni aperte di altre sessioni: elencate in `reports/ultimo_report.md` (fonte #394 e `stato_progetto.md`).

---

## §1 SCOPE & ESITO FETTE

- **Fetta unica — Trigger dei solleciti (decisione dell'operatore, 23/11, «ok vai» alla proposta)**: FATTA. `funnel_v2.md`, regole comuni: DUE trigger con testi propri — caso A (lead fermo a metà dei passaggi: testi di prima) e caso B (candidatura accettata ma «Scrivi a {agente}» non premuto, unico caso del percorso diretto: «Ti manca solo l'ultimo passo…» / «Vuoi fare l'ultimo passo o chiudo qui?»). Per entrambi: max 2 solleciti poi silenzio, solo per chi ha iniziato il percorso, niente promozione a freddo, indipendenti dal consenso aggiornamenti. Rimandi aggiornati (regola del consenso, Bozza B «ultimo passo», percorso diretto). Chiude l'incoerenza del 4° verdetto del bot sulla PR #393 (le fonti davano un testo solo per due momenti diversi). Simulazione: `followUp()` unificato sui testi del caso B senza più note di proposta, con la riga che spiega dove vale il caso A; provata dal vivo nel browser (percorso diretto fino al 2° sollecito) e ripubblicata sulla pagina claude.ai, che dal 22/11 è PUBBLICA (condivisa dall'operatore per i collaboratori).

Contesto: PR #392 e #393 (funnel) già mergiate nei giorni scorsi; `reports/bacheca.md` (nuova regola della #394) letta prima del giro — nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = bf4284418ba06eafc75e397360dc69dfad5df06f (merge-base con origin/main = main dopo il merge della PR #394).

```
 reports/diff_sessione.md               |  15 ++---
 reports/funnel/funnel_v2.md            |  17 ++---
 reports/funnel/simulazione_funnel.html |  32 +++---
 reports/handoff.md                     | n/d
 reports/ultimo_report.md               |  43 +++---
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
(nessun commit prima del commit di fine-task: il branch riparte da main bf42844 e questa fetta produce un solo commit)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto. La sessione tocca solo `reports/funnel/` e i tre report canonici.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura:

```
completed	success	Merge pull request #394 from Gasss23/claude/nifty-galileo-3k7kbm — ba…	CI	claude/nifty-galileo-3k7kbm	push	44968847316	11m18s	2026-11-22T00:53:51Z
completed	success	Merge pull request #394 from Gasss23/claude/nifty-galileo-3k7kbm — ba…	CI	main	push	44968832490	12m53s	2026-11-22T00:53:39Z
completed	success	docs: bacheca comune tra le chat; risposte dell'operatore sul CRM	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	44967870295	2m21s	2026-11-22T00:41:43Z
```

Mappatura commit→run: il commit di fine-task di questa fetta è l'unico del branch; run non ancora disponibile alla scrittura dell'handoff (parte col push). Le run elencate sopra sono della PR #394 (altra chat). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- Riserve del 5° verdetto bot sulla PR #393 (merge col via dell'operatore): V-1 (registrare la decisione dei solleciti in un posto stabile) CHIUSA da questa fetta (la decisione ora sta in `funnel_v2.md`, fonte canonica); V-2 (citazione precisa delle fonti) assorbita dalla stessa riscrittura; V-3 (ordine delle fette nel vecchio handoff) superata (handoff riscritto).
- RESTA APERTA: far controllare i testi del funnel all'esperto — l'operatore il 23/11 ha detto di averlo FATTO (punto 4): da considerare chiusa salvo esito contrario dell'esperto.
- Riserve delle altre chat (Voce, CRM): tracciate in `reports/stato_progetto.md` (regola 3 di `lavoro_parallelo.md`), non toccate qui.
