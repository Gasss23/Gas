# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Dashboard del CRM sempre accesa sul Mac

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #403 (https://github.com/Gasss23/Gas/pull/403). Solo script per il Mac e guida: nessun codice del motore.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`.

---

## §1 SCOPE & ESITO FETTE

- **Dashboard del CRM sempre accesa** (richiesta dell'operatore: «vorrei mettere da qualche parte questa dashboard… che non dipenda da Claude o dall'IA… accessibile anche offline e in modo facile»): FATTA. LaunchAgent `com.gas.crm`, `scripts/crm/installa.sh` e `spegni.sh`, icona «CRM Gas» sulla Scrivania (il token non finisce in nessun file), guida aggiornata.
- **Prova su un Mac vero** (launchctl, Scrivania): SALTATA — il Mac non è raggiungibile da qui; provati la sintassi degli script, il plist e il controllo di token e porta col codice vero del CRM.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/crm/guida.md          |  2 ++
 reports/diff_sessione.md      | 20 +++++++-------------
 reports/handoff.md            | n/d
 reports/stato_progetto.md     |  3 ++-
 reports/ultimo_report.md      | 39 +++++++++------------------------------
 scripts/crm/com.gas.crm.plist | 29 +++++++++++++++++++++++++++++
 scripts/crm/installa.sh       | 78 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/crm/spegni.sh         |  9 +++++++++
```

NB: regola «n/d» — il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
5d5911b4 feat(crm): dashboard sempre accesa sul Mac — LaunchAgent com.gas.crm, installa/spegni e icona sulla Scrivania
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh run list` non usato: GitHub si interroga con `gh api` REST.
- Mappatura commit→run:
  - `5d5911b4`: run partita al push, esito non ancora disponibile alla scrittura dell'handoff.
  - Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Nessuna nuova. Script non provati su un Mac vero.
- Dalla PR #397: R-848-2 BASSA (doctor senza avviso col forte spento), R-848-3 BASSA («Sempre Opus» provato solo nel kernel), V-3 BASSA della verifica esterna (commento di `importi_nel_testo` impreciso), cosmetiche #848; R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`).
