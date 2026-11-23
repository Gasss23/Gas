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

Contesto: PR #396 (trigger solleciti) mergiata oggi col via dell'operatore dopo il 3° verdetto (APPROVATO CON RISERVE senza ALTA/MEDIA); la sua V-1 COSMETICA residua (nome «Fetta unica» accanto a «Fetta 2/3» nei log) è superata dalla riscrittura dei report per questa sessione. `reports/bacheca.md` letta prima del giro: nessuna notizia bloccante, niente da aggiungere.

---

## §2 GIT DIFF --STAT (sessione)

BASE = 1b4954e2a16d665998fe315a4ea009fc0b8e1ced (merge-base con origin/main = main dopo i merge delle PR #396 e #397).

```
 reports/diff_sessione.md               |  23 ++++++--------
 reports/funnel/funnel_v2.md            |   5 +--
 reports/funnel/simulazione_funnel.html |  50 ++++++++----------------------
 reports/funnel/tasto_collaboratori.md  |  13 +++++---
 reports/handoff.md                     | n/d
 reports/stato_progetto.md              |   2 +-
 reports/ultimo_report.md               |  60 +++++++++++++++---------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
(vuoto: la sessione ha UN solo commit, quello di fine-task che contiene questo file)
```

Output reale di `git log --oneline ${BASE}..HEAD` alla scrittura: vuoto. Il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto. La sessione tocca solo `reports/funnel/` e i report canonici.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura (le righe sono del branch della sessione Voce, attiva in parallelo; questo branch non ha ancora run):

```
completed	success	fix(voce): 4 fasi sfalsate per «Hey Jarvis», interruzione col filtro, taratura coerente (simulazione end-to-end, M1)	verifica-bot	fix/voce-fasi-interruzione	pull_request_target	45227473463	2m57s	2026-11-23T17:25:16Z
in_progress		docs(fine-task): §2/§3 handoff	CI	fix/voce-fasi-interruzione	push	45227465740	4m46s	2026-11-23T17:25:13Z
completed	cancelled	fix(voce): 4 fasi sfalsate per «Hey Jarvis», interruzione col filtro, taratura coerente (simulazione end-to-end, M1)	verifica-bot	fix/voce-fasi-interruzione	pull_request_target	45226247559	26s	2026-11-23T17:18:35Z
```

Mappatura commit→run: la sessione ha UN solo commit (quello di fine-task): run non ancora disponibile alla scrittura dell'handoff (parte col push). La copertura pre-merge è garantita da `gh pr checks` prima del merge.

## §7 RISERVE APERTE

- V-1 COSMETICA del 3° verdetto bot sulla PR #396 (nome «Fetta unica» accanto a «Fetta 2/3» nei log di quella sessione): SUPERATA — i report sono riscritti per questa sessione.
- Riserve delle altre chat (CRM #397, Voce): tracciate in `reports/stato_progetto.md`, non toccate qui.
