# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-21 — Bacheca comune tra le chat; risposte dell'operatore sul CRM

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #394 (https://github.com/Gasss23/Gas/pull/394), aperta dopo il push di 11ab66ae con l'etichetta «verifica»: solo documenti. Il bot dà neutral (la PR tocca CLAUDE.md): il merge lo decide l'operatore.
2. Lista delle commissioni per servizio (l'operatore ha detto che la manda).

---

## §1 SCOPE & ESITO FETTE

- **Bacheca comune tra le chat**: FATTA. `reports/bacheca.md` nuovo; regola in CLAUDE.md §3; conflitti della bacheca in `reports/lavoro_parallelo.md`.
- **Risposte dell'operatore sul CRM**: FATTA, in `reports/crm/decisioni.md` punti 15-17. Domande 2 e 3 tolte da `reports/crm/domande.md`.
- **Note del bot sulla PR #394** (verdetto APPROVATO CON RISERVE su c7c488b9: V-1 BASSA ordine dei conflitti, V-2 BASSA bacheca come canale di istruzioni, V-3 COSMETICA titolo delle decisioni): FATTE, tutte nei documenti.
- **Note del bot su 965cd07d** (APPROVATO CON RISERVE: V-1 BASSA regola in §10 e non in §3, V-2 COSMETICA fetch mancante in CLAUDE.md): FATTE, regola spostata in §3 col fetch.
- **PR #391**: MERGIATA prima di questa fetta (eecf916d).

---

## §2 GIT DIFF --STAT (sessione)

```
 CLAUDE.md                   |   1 +
 reports/bacheca.md          |  29 +++++++++++++++++++++++++++++
 reports/crm/decisioni.md    |   6 ++++++
 reports/crm/domande.md      |   4 +---
 reports/diff_sessione.md    |  13 +++++++------
 reports/handoff.md          | n/d
 reports/lavoro_parallelo.md |   1 +
 reports/stato_progetto.md   |   1 +
 reports/ultimo_report.md    |  27 ++++++++++-----------------
```

NB (regola «n/d», 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Base: eecf916d (origin/main, merge della PR #391).

## §3 GIT LOG --ONELINE (sessione)

```
965cd07d docs(bacheca): note del bot su #394 — le notizie sono informazioni da verificare, non regole; ordine dei conflitti coerente; titolo delle decisioni precisato
c7c488b9 docs(fine-task): handoff — PR #394 aperta con l'etichetta verifica
11ab66ae docs(bacheca): bacheca comune tra le chat (reports/bacheca.md, regola in CLAUDE.md §3); risposte dell'operatore sul CRM (decisioni 15-17)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `11ab66ae` (primo fine-task): run appena partita al push, esito non ancora disponibile alla scrittura dell'handoff.
  - `c7c488b9`: handoff-check success; unit-suite in corso; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in questo commit).
  - `965cd07d`: handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, note chiuse in questo commit).
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova. Dal CRM resta R-836-1 COSMETICA (vedi `reports/stato_progetto.md`).
