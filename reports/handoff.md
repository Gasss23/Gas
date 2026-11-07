# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-07 — chat Mani: «Hey Gas» NO e riserve della PR #347 registrate (solo documenti)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #348 (https://github.com/Gasss23/Gas/pull/348). Il numero e l'URL vengono dalla risposta dello strumento GitHub `create_pull_request`, perché `gh` non è usato in questa sessione. La PR è di soli documenti: la mergio da solo se il bot dà APPROVATO senza finding, altrimenti serve il sì dell'operatore via M1.

---

## §1 SCOPE & ESITO FETTE

- **PR #347 (fetta 44)**: `FATTA` — mergiata (4a0b113) col sì dell'operatore. CI verde; bot e verifica esterna APPROVATO CON RISERVE, senza ALTA/MEDIA.
- **Decisione «Hey Gas» registrata**: `FATTA` — NO, si resta con «Hey Jarvis».
- **Riserve nuove della #347 in stato_progetto**: `FATTA`.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md       |  18 +++++-------------
 reports/proposta_parola_gas.md |   4 ++++
 reports/stato_progetto.md      |   4 ++--
 reports/ultimo_report.md       |  23 ++++++++---------------
 reports/handoff.md                 | n/d
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; riga di totale tolta. Base: main 4a0b113 (dopo il merge della PR #347).

## §3 GIT LOG --ONELINE (sessione)

```
021f68d docs(voce): «Hey Gas» NO (decisione dell'operatore), riserve della PR #347 registrate (chat Mani)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` non usato: GitHub passa dallo strumento MCP.
- 021f68d: pushato all'apertura della PR #348; run non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.
- PR #347 su 54ed685 (sessione precedente): unit-suite e handoff-check success, poi mergiata.

## §7 RISERVE APERTE

- Verifica esterna #347 (https://github.com/Gasss23/Gas/pull/347#issuecomment-6706499378):
  - V-1 BASSA: con la parola sentita in aspetta_voce la tolleranza dopo la parola non parte. Da provare sul Mac insieme a R-702-2 e R-694-2.
  - V-2 COSMETICA: controllo dell'eco solo con risposte NDJSON.
- Bot #347:
  - V-1 BASSA: eco non coperta con audio/mpeg e JSON V3.
  - V-2 BASSA: casi limite di riprendi.sh (servizio che si riavvia di continuo; errore dopo più di 3 s).
  - V-3 COSMETICA: finestra oltre 120 riportata a 120 senza avviso.
- Restano le riserve della fetta 44 e delle precedenti in `reports/stato_progetto.md`.
