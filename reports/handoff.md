# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-25 — Chat Mani: riserve rimaste dopo il merge di #261 salvate prima del /clear

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #267 (https://github.com/Gasss23/Gas/pull/267): solo `reports/`. La chat Mani la mergia da sola solo con APPROVATO pulito del bot (CLAUDE.md §10); altrimenti serve l'OK dell'operatore.
2. PR #263 (chat Notte, `/clear` da Telegram): check verdi, bot APPROVATO CON RISERVE (solo BASSE) → merge solo con OK esplicito dell'operatore.
3. Decisioni aperte dell'area web (in `reports/stato_progetto.md`): R-ve261-2 MEDIA, R-ve252-2 / R-ve255-1, R-ve246-5 MEDIA, tempo di rete 12 s, R-ve235-7.

Numero e URL della PR presi dall'output reale dello strumento GitHub (create_pull_request → 267), non inventati.

---

## §1 SCOPE & ESITO FETTE

- **Salvare nel repo le riserve finali del bot #261 (commit 5e704c0)**: `FATTA` — blocco nuovo in `reports/stato_progetto.md` con R-ve261-3 (test NOSCRIPT maiuscolo), R-ve261-4 (frameset), R-ve261-5 (frasi imprecise), R-ve261-6 (con_noscript in feed, docstring, test doppio).
- **Chiudere quelle riserve**: `DEFERITA — prossima fetta Mani, quando l'operatore la chiede`.
- **Merge della PR #263**: `SALTATA — non è della chat Mani e ha riserve: decide l'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  | 16 ++++++++--------
 reports/handoff.md        | n/d
 reports/stato_progetto.md |  2 ++
 reports/ultimo_report.md  | 17 ++++++++---------
```

NB: regola «n/d» (decisione dell'operatore, 2026-10-24): il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive, quindi la sua riga dice `n/d` e la riga di totale è tolta. Gli altri conteggi sono presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
17016ba docs(stato): riserve rimaste dopo il merge di #261 (chat Mani)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

Letto dai check della PR #267 (strumento GitHub; `gh` non autenticato in questo ambiente):

- `17016ba`: run 40217924262 — handoff-check success, unit-suite in_progress alla scrittura; run 40217937814 (bot di verifica) — smista success, verifica in_progress.
- commit di fine-task (questo file): run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-ve261-3 (chat Mani) BASSA — test con `<NOSCRIPT>`/`<NoScript>` maiuscolo mancante.
- R-ve261-4 (chat Mani) BASSA preesistente — testo delle pagine con `<frameset>`.
- R-ve261-5 (chat Mani) COSMETICA — frasi imprecise in ultimo_report/PR #261.
- R-ve261-6 (chat Mani) COSMETICA — `con_noscript` da calcolare in `_componi`, docstring di `_Contesto`, test doppio.
- Preesistenti, decisione dell'operatore: R-ve261-2 MEDIA, R-ve252-2, R-ve255-1, R-ve246-5 MEDIA, R-ve235-7.
