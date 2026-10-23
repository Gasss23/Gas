# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-23 — Chat Motore: regole d'uso dell'abbonamento per R2 riverificate; stato del turno di notte

---

## §0 DECISIONI UMANE RICHIESTE

1. R2: via A (API key con i crediti inclusi nel Max 5x) o via B (`claude -p` col login) — `reports/r2_regole_abbonamento.md`.
2. Merge della PR PLACEHOLDER_PR (solo documenti).

---

## §1 SCOPE & ESITO FETTE

- **Verifica delle regole R2**: `FATTA`.
- **Riserve bot #253 V-1/V-2**: `FATTA`.
- **Costruzione R2**: `DEFERITA — decisione dell'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
PLACEHOLDER_STAT
```

## §3 GIT LOG --ONELINE (sessione)

```
PLACEHOLDER_LOG
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; per lo stesso motivo la riga di `reports/handoff.md` nel §2 non conta il commit finale.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

- Commit della sessione: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Bot #253 V-2 (BASSA): «prima notte» riconosciuta dall'assenza di rami `notte/*` invece che di PR mergiate — si chiude cambiando il testo dell'attività dalla sessione fissa.
- Bot #253 V-3 (BASSA): la sessione fissa accumula contesto tra le notti (contaminazione) — stessa chiusura, o tornare a una sessione nuova per notte col repo.
- R2 via B: uso automatico col login ambiguo per le Consumer Terms §3.7.
