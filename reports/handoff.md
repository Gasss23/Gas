# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — Presentazione clienti: prima bozza del PDF dell'ecosistema

---

## §0 DECISIONI UMANE RICHIESTE

1. PR #380 (https://github.com/Gasss23/Gas/pull/380): NON mergiare finché la presentazione non ha i dati reali, salvo decisione dell'operatore. Numero e URL dalla risposta reale dello strumento GitHub (create_pull_request), non da `gh`: in questo ambiente cloud `gh` è riservato alla ricerca.
2. Prima di usare il PDF con i clienti, farlo vedere a un legale: proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Mandare all'agente i dati reali (PDF d'esempio, brand e contatti, dati dei servizi 1-3, servizio 4).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — prima bozza del PDF (15 pagine, 16:9)**: FATTA — 83511a47. Sorgente `presentazione_clienti/build.py` + `render.js`, PDF `presentazione_clienti/Presentazione_Ecosistema.pdf`; dati mancanti come segnaposto tratteggiati.
- **Fetta 2 — dati reali nel PDF**: DEFERITA — l'operatore deve ancora mandarli.
- **Fetta 3 — revisore e verifica esterna**: SALTATA — nessun file nel perimetro di review né di sicurezza.

---

## §2 GIT DIFF --STAT (sessione)

```
 presentazione_clienti/.gitignore                   |    1 +
 presentazione_clienti/Presentazione_Ecosistema.pdf |  Bin 0 -> 2578700 bytes
 presentazione_clienti/build.py                     | 1096 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 presentazione_clienti/render.js                    |   15 +++++
 presentazione_clienti/titoli_svg.json              |   10 ++++
 reports/diff_sessione.md                           |   16 +++--
 reports/handoff.md                                 | n/d
 reports/ultimo_report.md                           |   20 ++++---
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
83511a47 presentazione clienti: prima bozza del PDF dell'ecosistema (15 pagine)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/

## §6 STATO CI

`gh run list` non usato (in questo ambiente cloud `gh` è riservato alla ricerca). Output reale dello strumento GitHub `actions_list` (list_workflow_runs, branch claude/practical-tesla-ea9a9g) alla scrittura:

```
CI            run 44155605928  #1938  push                 in_progress  sha 83511a47  https://github.com/Gasss23/Gas/actions/runs/44155605928
verifica-bot  run 44155820797  #1173  pull_request_target  completed/skipped  sha 83511a47  https://github.com/Gasss23/Gas/actions/runs/44155820797
```

Mappatura commit→run:
- 83511a47 → CI run 44155605928 (in corso alla scrittura, esito non ancora disponibile); verifica-bot run 44155820797 skipped (manca l'etichetta `verifica` sulla PR).
- commit di fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

Nessuna.
