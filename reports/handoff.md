# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — Bacheca comune tra le chat; risposte dell'operatore sul CRM

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (numero dopo il push): solo documenti.
2. Lista delle commissioni per servizio (l'operatore ha detto che la manda).

---

## §1 SCOPE & ESITO FETTE

- **Bacheca comune tra le chat**: FATTA. `reports/bacheca.md` nuovo; regola in CLAUDE.md §3; conflitti della bacheca in `reports/lavoro_parallelo.md`.
- **Risposte dell'operatore sul CRM**: FATTA, in `reports/crm/decisioni.md` punti 15-17. Domande 2 e 3 tolte da `reports/crm/domande.md`.
- **PR #391**: MERGIATA prima di questa fetta (eecf916d).

---

## §2 GIT DIFF --STAT (sessione)

```
 CLAUDE.md                   |   1 +
 reports/bacheca.md          |  27 +++++++++++++++++++++++++++
 reports/crm/decisioni.md    |   6 ++++++
 reports/crm/domande.md      |   4 +---
 reports/diff_sessione.md    |  13 +++++++------
 reports/handoff.md          | n/d
 reports/lavoro_parallelo.md |   1 +
 reports/stato_progetto.md   |   1 +
 reports/ultimo_report.md    |  25 ++++++++-----------------
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: eecf916d (origin/main, merge della PR #391).

## §3 GIT LOG --ONELINE (sessione)

```
(nessun commit di sessione prima del fine-task)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - Commit di fine-task che contiene questo file (unico commit della sessione): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova. Dal CRM resta R-836-1 COSMETICA (vedi `reports/stato_progetto.md`).
