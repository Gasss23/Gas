# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Prima notte del cervello forte: `claude` non trovato (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #283 (https://github.com/Gasss23/Gas/pull/283, numero dalla risposta di `create_pull_request`; `gh` nel cloud non è autenticato), dall'agente da qui secondo CLAUDE.md §10.
2. Verificare il giro del 29 ottobre sul Mac.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Diagnosi della notte fallita**: `FATTA` — «comando `claude` non trovato» nel log del 27 e del 28.
- **Fetta 2 — Correzione sul Mac e stato del progetto**: `FATTA` — `GAS_CLAUDE_BIN` nel `.env`, G-3 aggiornata.
- **Fetta 2b — Nota COSMETICA del bot #283 (frase in G-3)**: `FATTA`.
- **Fetta 2c — Merge di main (conflitto solo nei log)**: `FATTA` — nessun file del perimetro.
- **Fetta 3 — Motivo vero nel report della notte e avviso nel doctor**: `DEFERITA — prossima fetta del motore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  5 ++---
 reports/handoff.md        | n/d
 reports/stato_progetto.md |  6 +++---
 reports/ultimo_report.md  | 14 +++++++++-----
```

NB: regola «n/d» — conteggio di `reports/handoff.md` non misurabile, riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1e5e47e Merge origin/main in feat/merge-automatico-z1xjx2 (PR #283)
a42cac6 docs: nota del bot #283 — frase del 28 ottobre al suo posto in G-3
dbfcf7c docs(stato): prima notte del forte fallita per «claude non trovato», GAS_CLAUDE_BIN sul Mac
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` nel cloud non è autenticato. Commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Da #279 (bot, BASSE/COSMETICHE): riga «merge da browser» nel Lucchetto main di CLAUDE.md; `gas fida-contatto <chiave>` con rubrica illeggibile dice «chiave non trovata»; docstring di `_ricorda`.
- Nuova: il report della notte mostra solo «RuntimeError» per gli errori del forte.
