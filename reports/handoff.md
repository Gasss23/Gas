# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-17 — Presentazione clienti: PDF dell'ecosistema con i dati reali del copy trading Forex

---

## §0 DECISIONI UMANE RICHIESTE

1. PR #380 (https://github.com/Gasss23/Gas/pull/380): NON mergiare finché la presentazione non è completa, salvo decisione dell'operatore; oggi comunque la CI è rossa per l'ambiente (§6). Numero e URL dalla risposta reale dello strumento GitHub (create_pull_request; list_pull_requests sul branch), non da `gh`: in questo ambiente cloud `gh` è riservato alla ricerca.
2. Prima di usare il PDF con i clienti, farlo vedere a un legale: proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
3. Confermare: storico verificato del copy trading = 23 mesi (non 4 anni); stop sull'equity 10% al livello del copy e 30% al livello 3 del conto dati. Nel PDF ci sono i dati del catalogo.
4. Decidere se citare nel PDF il fornitore della strategia («The Source Finance» / «TSF Forex Algo»).
5. Far sistemare la CI (attività separata proposta in sessione: test bwrap della suite web rossi sul runner).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — prima bozza del PDF (15 pagine, 16:9)**: FATTA — 83511a47.
- **Fetta 2 — dati reali del copy trading Forex (catalogo TSF, servizio 01)**: FATTA — 03466aae. Tutti i numeri del catalogo tenuti; 16 pagine.
- **Fetta 3 — dati dei servizi 1, 2 e 4**: DEFERITA — l'operatore deve ancora mandarli.
- **Fetta 4 — revisore e verifica esterna**: SALTATA — nessun file nel perimetro di review né di sicurezza.

---

## §2 GIT DIFF --STAT (sessione)

```
 presentazione_clienti/.gitignore                   |    1 +
 presentazione_clienti/Presentazione_Ecosistema.pdf |  Bin 0 -> 2721708 bytes
 presentazione_clienti/build.py                     | 1251 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 presentazione_clienti/render.js                    |   15 +++++
 presentazione_clienti/titoli_svg.json              |   10 +++
 reports/diff_sessione.md                           |   16 +++--
 reports/handoff.md                                 | n/d
 reports/ultimo_report.md                           |   23 ++++---
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
03466aae presentazione clienti: dati reali del copy trading Forex (catalogo TSF)
adb0e188 docs(fine-task): report della bozza della presentazione clienti
83511a47 presentazione clienti: prima bozza del PDF dell'ecosistema (15 pagine)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/

## §6 STATO CI

`gh run list` non usato (in questo ambiente cloud `gh` è riservato alla ricerca). Output reale dello strumento GitHub `actions_list` (list_workflow_runs, branch claude/practical-tesla-ea9a9g, event push) alla scrittura:

```
CI  run 44155950606  #1939  push  completed/failure  sha adb0e188  https://github.com/Gasss23/Gas/actions/runs/44155950606
CI  run 44155605928  #1938  push  completed/failure  sha 83511a47  https://github.com/Gasss23/Gas/actions/runs/44155605928
```

Job della run 44155950606: `handoff-check` success; `unit-suite` failure allo step «Run web suite»: «7 failed, 747 passed», tutti in tests/test_unit_web_browser.py (test del sandbox bwrap, es. «bwrap: execvp sleep: No such file or directory»). Tutte le altre suite del job passano. Il branch non tocca codice: guasto dell'ambiente del runner (ultima CI verde su main: run 43312735169 del 12/11 su 01eb9f50).

Mappatura commit→run:
- 83511a47 → CI run 44155605928: failure (stessa causa, web suite).
- adb0e188 → CI run 44155950606: failure (web suite, 7 test bwrap).
- 03466aae → run non ancora disponibile alla scrittura dell'handoff (pushato insieme al commit di fine-task: una sola run testerà la testa).
- commit di fine-task (questo file) → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- CI rossa per l'ambiente (test bwrap della suite web): blocca il merge di ogni PR finché non viene sistemata; attività separata proposta all'operatore.
