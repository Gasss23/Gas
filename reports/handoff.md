# HANDOFF — Dossier di fine sessione

**Sessione:** 23 novembre 2026 — Ritocchi finali del funnel dopo la prova dell'operatore (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #401 (https://github.com/Gasss23/Gas/pull/401), aperta con l'etichetta «verifica». Tocca file fuori dalla lista bianca dei log (funnel): serve il verdetto testuale del bot; merge autonomo solo con APPROVATO pulito, altrimenti decide l'operatore (che ha già chiesto di procedere coi ritocchi).
2. Consegnare allo sviluppatore del bot (su main dopo il merge): `reports/funnel/tasto_collaboratori.md`, `reports/funnel/funnel_v2.md`, `reports/funnel/simulazione_funnel.html`.
3. Ripristinare nel bot «Inizia Ora · Accesso» lo stato dell'operatore (bottoni «Conto aperto» / «In VIP»).

---

## §1 SCOPE & ESITO FETTE

- **Fetta unica — Tre ritocchi chiesti dall'operatore il 23/11 dopo la prova della simulazione**: FATTA.
  1. Via la domanda «Da quale community arrivi?» dalla fase 1 del percorso completo: si parte dalla lingua (con la conferma dei 18 anni). `funnel_v2.md` (prima regola comune + due rimandi allineati) e simulazione.
  2. Percorso diretto SOLO nome e cognome: messaggio unico (rischio+compenso), campo «Scrivimi nome e cognome» con la riga «Inviando confermi di avere almeno 18 anni e ci autorizzi a risponderti qui», poi [Scrivi a {agente}]. Consenso aggiornamenti non chiesto nel diretto: senza sì niente promozione (lo raccoglie l'agente in chat); i solleciti del caso B non sono promozione (restano indipendenti dal consenso come da regole comuni). `tasto_collaboratori.md` §3.1 e §4.5, simulazione (rimossa `ctaConConsenso`).
  3. Requisito Pannello blu (confermato dall'operatore su screenshot): «I miei link», card e link dell'agente si aprono DENTRO il Pannello esistente (bottone blu «Pannello» della chat del bot), nessuna app o pagina nuova. `tasto_collaboratori.md` §4.6, simulazione (scheda agente).
  La simulazione è stata ripubblicata sulla pagina pubblica claude.ai e PROVATA dal vivo nel browser dopo la ripubblicazione (le tre schede).

- **Fetta 2 — Correzioni del 1° verdetto del bot sulla PR #401 (secondo giro, scelta dell'operatore «Sistema prima»)**: FATTA. V-1 BASSA: dichiarata la lingua del diretto (`language_code` di Telegram, IT/EN, altrimenti italiano; la riga dei 18 anni segue la lingua del lead) in `tasto_collaboratori.md` §3.1 e §4.5 e nella simulazione. V-2 BASSA: §3/§6 di questo handoff aggiornati coi commit reali. V-3 COSMETICA: card del diretto «solo nome e cognome, subito l'ultimo passo» (spec §1 + simulazione) e «in basso nella chat» uniformato nell'intestazione. V-4 COSMETICA: la regola del consenso in `funnel_v2.md` ora rimanda all'eccezione del diretto. Simulazione ripubblicata.

Contesto: PR #396 (trigger solleciti) mergiata oggi col via dell'operatore dopo il 3° verdetto (APPROVATO CON RISERVE senza ALTA/MEDIA); la sua V-1 COSMETICA residua (nome «Fetta unica» accanto a «Fetta 2/3» nei log) è superata dalla riscrittura dei report per questa sessione. `reports/bacheca.md` letta prima del giro: nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = 1b4954e2a16d665998fe315a4ea009fc0b8e1ced (merge-base con origin/main = main dopo i merge delle PR #396 e #397).

```
 reports/diff_sessione.md               |  24 +++++++-------
 reports/funnel/funnel_v2.md            |   7 +++--
 reports/funnel/simulazione_funnel.html |  54 +++++++++----------------------
 reports/funnel/tasto_collaboratori.md  |  17 ++++++----
 reports/handoff.md                     | n/d
 reports/stato_progetto.md              |   2 +-
 reports/ultimo_report.md               |  61 +++++++++++++++--------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
500cfa39 docs(fine-task): handoff §0 — PR #401 aperta con l'etichetta verifica
fb0f84af docs(funnel): ritocchi dell'operatore dopo la prova — via la domanda community, diretto solo nome e cognome con riga 18 anni, requisito Pannello blu per I miei link
```

NB: il commit di fine-task di QUESTO 2° giro (il terzo del branch, che contiene questo file) non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push. fb0f84af era fetta + fine-task del 1° giro, 500cfa39 l'aggiornamento del §0 dopo l'apertura della PR (corregge la V-2 del 1° verdetto: prima il §3 diceva «un solo commit»).

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto. La sessione tocca solo `reports/funnel/` e i report canonici.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura del 2° giro (righe di main e della sessione Voce, attive in parallelo):

```
in_progress		Merge pull request #398 from Gasss23/claude/r7-ripresa-al-boot	CI	main	push	45230996568	1m2s	2026-11-23T17:45:03Z
in_progress		fix(voce): 4 fasi sfalsate per «Hey Jarvis», interruzione col filtro, taratura coerente (simulazione end-to-end, M1)	verifica-bot	fix/voce-fasi-interruzione	pull_request_target	45230485553	3m59s	2026-11-23T17:42:06Z
in_progress		docs(fine-task): §2/§3 handoff	CI	fix/voce-fasi-interruzione	push	45230478544	4m2s	2026-11-23T17:42:03Z
```

Mappatura commit→run: fb0f84af e 500cfa39 sono stati pushati insieme → una sola run CI 45228489192 success (unit-suite 11m39s e handoff-check) sull'albero di 500cfa39 (head del 1° giro); fb0f84af senza run propria (contenuto incluso nell'albero testato); run verifica-bot del 1° verdetto sull'head 500cfa39: success (APPROVATO CON RISERVE senza ALTA/MEDIA). Il commit di fine-task di questo 2° giro: run non ancora disponibile alla scrittura dell'handoff (parte col push). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- V-1 COSMETICA del 3° verdetto bot sulla PR #396 (nome «Fetta unica» accanto a «Fetta 2/3» nei log di quella sessione): SUPERATA — i report sono riscritti per questa sessione.
- 1° verdetto del bot su PR #401 (500cfa39, APPROVATO CON RISERVE senza ALTA/MEDIA): V-1 BASSA (lingua del diretto non dichiarata), V-2 BASSA (§3/§6 dell'handoff con «un solo commit»), V-3 COSMETICA (card «niente domande», «in basso a sinistra»), V-4 COSMETICA (eccezione del diretto assente dalla regola del consenso in funnel_v2) — CORRETTE in questo 2° giro (Fetta 2); serve il verdetto del bot sul nuovo head.
- Riserve delle altre chat (CRM #397, Voce): tracciate in `reports/stato_progetto.md`, non toccate qui.
