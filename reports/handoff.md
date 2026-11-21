# HANDOFF — Dossier di fine sessione

**Sessione:** 21 novembre 2026 — Funnel community: analisi competitor, funnel v2, tasto collaboratori (solo doc)

---

## §0 DECISIONI UMANE RICHIESTE

(da completare dopo il push)

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Mappatura funnel attuale del bot «Inizia Ora · Accesso»**: FATTA. Ricostruito dalla cronologia del test del 18/11: presentazione, 7 domande a risposta multipla, «ultimo passo» con messaggio precompilato all'agente, scheda lead, guida agenti, /pannello. La mini app «Pannello» non si apre dall'automazione (non bloccante).
- **Fetta 2 — Analisi competitor Telegram**: FATTA. 9 canali della cartella «Competitor» analizzati (canali pubblici, bot di ingresso, cronologie esistenti). Risultato: `reports/funnel/analisi_competitor.md`.
- **Fetta 3 — Funnel v2 in due bozze (vocale vs messaggi)**: FATTA. Copy completo e confronto in `reports/funnel/funnel_v2.md`.
- **Fetta 4 — Tasto 2 link per i collaboratori**: FATTA COME SPECIFICA (`reports/funnel/tasto_collaboratori.md`): il codice del bot non è nel repo Gas né altrove sul Mac/GitHub dell'account; implementazione a carico di chi mantiene il bot.
- **Fetta 5 — Scrivere ai competitor fingendosi clienti**: SALTATA — limite di sicurezza dell'agente (niente messaggi a persone reali sotto falsa identità). Compensata leggendo i bot automatici e la cronologia già esistente (chat «LEO SUPPORTO» = loro intero processo di vendita). Nessun messaggio inviato ai competitor.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md              |  21 +++++++++------------
 reports/funnel/analisi_competitor.md  |  44 ++++++++++++++++++++++++++++++++++++++++++++
 reports/funnel/funnel_v2.md           |  66 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/funnel/tasto_collaboratori.md |  45 +++++++++++++++++++++++++++++++++++++++++++++
 reports/handoff.md                    | n/d
 reports/stato_progetto.md             |   2 +-
 reports/ultimo_report.md              |  46 +++++++++++++++++++---------------------------
```

NB: il conteggio righe di `reports/handoff.md` è `n/d` e la riga di totale è tolta (regola del 2026-10-24): il file conta se stesso e il suo conteggio finale non è misurabile alla scrittura. La CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
```

NB: la sessione è doc-only e produce UN solo commit, quello di fine-task che contiene questo file: per costruzione non compare nel range `${BASE}..HEAD` calcolato prima del commit. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Output reale di `gh run list -L 3` alla scrittura (nessuna run ancora per questo branch, mai pushato prima d'ora):

```
in_progress		fix(crm): note minori — resti in chiaro tolti anche dopo un riavvio, messaggi più chiari nel ripristino e negli avvisi	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	44937070857	1m41s	2026-11-21T18:43:29Z
in_progress		docs(fine-task): handoff — PR #391 aperta con l'etichetta verifica	CI	claude/nifty-galileo-3k7kbm	push	44937068923	1m43s	2026-11-21T18:43:27Z
completed	cancelled	fix(crm): note minori — resti in chiaro tolti anche dopo un riavvio, messaggi più chiari nel ripristino e negli avvisi	verifica-bot	claude/nifty-galileo-3k7kbm	pull_request_target	44937062360	30s	2026-11-21T18:43:23Z
```

Mappatura commit→run: l'unico commit della sessione è quello di fine-task; run non ancora disponibile alla scrittura dell'handoff (esito reale aggiornato dopo il push, vedi sotto). La copertura pre-merge è garantita da `gasmerge` (gh pr checks --watch).

## §7 RISERVE APERTE

Nessuna.
