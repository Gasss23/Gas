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

- **Fetta 3 — Correzione del 2° verdetto del bot sulla PR #396 (terzo giro, scelta dell'operatore «Sistema prima»)**: FATTA. V-1 BASSA: la mappatura commit→run del §6 attribuiva a 9549d20 «nessuna run propria completata» citando una run di verifica-bot; riscritta con le run reali (CI 45099433261 success; verifica-bot 45099448550 skipped e 45099451611 cancelled), come indicato dal bot.

- **Fetta 2 — Correzioni del 1° verdetto del bot sulla PR #396 (secondo giro)**: FATTA. V-1: `tasto_collaboratori.md` §4.3 ora rimanda esplicitamente ai «2 solleciti del caso B» coi testi, e il caso B di `funnel_v2.md` copre anche il diretto («o, nel percorso diretto, dopo il messaggio unico»). V-2: `reports/stato_progetto.md` aggiornato (trigger deciso, esperto fatto; restano consegna allo sviluppatore e ripristino dello stato dell'operatore nel bot, ora anche in ultimo_report). V-3: §3 con i commit citati e riga dell'esperto senza contraddizione.

Contesto: PR #392 e #393 (funnel) già mergiate nei giorni scorsi; `reports/bacheca.md` (nuova regola della #394) letta prima del giro — nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = bf4284418ba06eafc75e397360dc69dfad5df06f (merge-base con origin/main = main dopo il merge della PR #394).

```
 reports/diff_sessione.md               |  17 ++++++++++-------
 reports/funnel/funnel_v2.md            |  17 ++++++++++-------
 reports/funnel/simulazione_funnel.html |  32 +++++++++++---------------------
 reports/funnel/tasto_collaboratori.md  |   2 +-
 reports/handoff.md                     | n/d
 reports/stato_progetto.md              |   4 ++--
 reports/ultimo_report.md               |  49 ++++++++++++++++++++++++-------------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
6c5dd58 docs(funnel): corretti i finding del 1° verdetto su #396 (V-1 solleciti del diretto in tasto_collaboratori, V-2 stato_progetto aggiornato, V-3 handoff)
30993c2 docs(fine-task): handoff — PR #396 aperta con l'etichetta verifica
9549d20 docs(funnel): trigger dei solleciti deciso — caso A (metà candidatura) e caso B (manca «Scrivi a») con testi propri, in funnel_v2 e nella simulazione
```

NB: il commit di fine-task di QUESTO giro (il quarto del branch, che contiene questo file) non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push. 9549d20 era fetta + fine-task del 1° giro, 30993c2 l'aggiornamento del §0 dopo l'apertura della PR, 6c5dd58 il 2° giro (fix del 1° verdetto).

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto. La sessione tocca solo `reports/funnel/` e i tre report canonici.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura (le righe sono del branch della sessione CRM, attiva in parallelo; le run di QUESTO branch stanno nella mappatura sotto, da `gh run list --branch claude/trigger-solleciti`):

```
completed	success	Gas usa il CRM: comandi da Telegram e voce, con firma e solo Opus	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	45111982842	4m47s	2026-11-23T04:27:44Z
completed	success	docs(fine-task): verifica esterna #397, bot, review #845-#847-CRM; V-…	CI	claude/nifty-galileo-3k7kbm	push	45111980411	11m45s	2026-11-23T04:27:42Z
completed	success	Gas usa il CRM: comandi da Telegram e voce, con firma e solo Opus	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	45109604439	11m4s	2026-11-23T04:04:12Z
```

Run di questo branch (`gh run list --branch claude/trigger-solleciti`, output reale):

```
45100775314 6c5dd58 verifica-bot pull_request_target completed/success
45100772925 6c5dd58 CI push completed/success
45099471823 30993c2 verifica-bot pull_request_target completed/success
45099469058 30993c2 CI push completed/success
45099451611 9549d20 verifica-bot pull_request_target completed/cancelled
45099448550 9549d20 verifica-bot pull_request_target completed/skipped
45099433261 9549d20 CI push completed/success
```

Mappatura commit→run: per 9549d20 run CI 45099433261 success (unit-suite e handoff-check); verifica-bot 45099448550 skipped e 45099451611 cancelled (corregge la V-1 del 2° verdetto: prima era attribuita male). Sull'head del 2° giro (6c5dd58) run CI 45100772925 success (unit-suite 11m53s) e run verifica-bot 45100775314 success (2° verdetto APPROVATO CON RISERVE senza ALTA/MEDIA, una sola V-1 BASSA su questa stessa riga). 30993c2: run CI 45099469058 e verifica-bot 45099471823, entrambe success (1° verdetto). Il commit di fine-task di questo 3° giro: run non ancora disponibile alla scrittura dell'handoff (parte col push). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- Riserve del 5° verdetto bot sulla PR #393 (merge col via dell'operatore): V-1 (registrare la decisione dei solleciti in un posto stabile) CHIUSA da questa fetta (la decisione ora sta in `funnel_v2.md`, fonte canonica); V-2 (citazione precisa delle fonti) assorbita dalla stessa riscrittura; V-3 (ordine delle fette nel vecchio handoff) superata (handoff riscritto).
- Controllo dei testi da parte dell'esperto: CHIUSA (l'operatore il 23/11 ha confermato in chat di averlo fatto).
- 1° verdetto del bot su PR #396 (30993c2, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (frase ambigua in `tasto_collaboratori.md` §4.3 sui solleciti del diretto + definizione del caso B), V-2 BASSA (`stato_progetto.md` non aggiornato: trigger/esperto dati ancora per aperti, voce sul ripristino dello stato nel bot assente dai report), V-3 COSMETICA (§3 «un solo commit», riga dell'esperto contraddittoria) — CORRETTE nel 2° giro (Fetta 2); il 2° verdetto le ha confermate CHIUSE tutte e tre.
- 2° verdetto del bot su PR #396 (6c5dd58, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (mappatura commit→run del §6 sbagliata per 9549d20) — CORRETTA in questo 3° giro (Fetta 3) con le run reali indicate dal bot; serve il verdetto del bot sul nuovo head.
- Riserve delle altre chat (Voce, CRM): tracciate in `reports/stato_progetto.md` (regola 3 di `lavoro_parallelo.md`), non toccate qui.
