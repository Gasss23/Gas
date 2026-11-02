# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-02 — Mani: piano della mail di Gas (R6), PR doc-only; riserve di #323 registrate (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #324 (https://github.com/Gasss23/Gas/pull/324). Numero e URL vengono dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5125431345","url":"https://github.com/Gasss23/Gas/pull/324"}`), perché `gh` nel cloud non è autenticato. Solo documenti: il merge segue la regola di CLAUDE.md §10 (verdetto del bot).
2. Rispondere alle 7 domande in fondo a `reports/piano_mail.md`: niente codice della mail prima delle risposte.

---

## §1 SCOPE & ESITO FETTE

- **PR #323 (fetta 37, voce H24)**: `FATTA` — mergiata (9718e0c) col sì dell'operatore; la parola resta «hey_jarvis» per ora («Hey Gas» in una fetta a parte, decisione di M1).
- **Piano mail (chiesto da M1)**: `FATTA` — `reports/piano_mail.md`: lettura non fidata, bozze in Gas, invio solo con firma, credenziali separate, tetti, solo cervello forte, 7 domande per l'operatore.
- **Riserve di #323 in stato_progetto (richiesta di M1)**: `FATTA` — V-1 del bot su 3672964 e V-1…V-6 della seconda verifica esterna (https://github.com/Gasss23/Gas/pull/323#issuecomment-6583621078), registrate senza altri giri.
- **Fetta piccola sulla voce (V-1 ve, V-1 bot, V-4 ve di #323)**: `DEFERITA — subito dopo questa PR (un solo branch remoto)`.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md   |  17 ++++++-----------
 reports/handoff.md         | n/d
 reports/piano_mail.md      |  74 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ripartenza_mani.md |   2 +-
 reports/roadmap.md         |   4 ++--
 reports/stato_progetto.md  |   5 +++--
 reports/ultimo_report.md   |  21 ++++++---------------
```

NB: base = merge-base con origin/main = 9718e0c. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
ec1fdbb docs(mail): stato, roadmap e ripartenza col piano mail; riserve di #323 registrate
6af999b docs(mail): piano della mail di Gas (R6) con le domande per l'operatore, senza codice
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` non autenticato nel cloud.
- 6af999b (piano mail), ec1fdbb (report): pushati insieme prima dell'apertura della PR #324; run non ancora disponibile alla scrittura dell'handoff.
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Da #323 (mergiata): V-1 bot su 3672964 BASSA (GAS_CLAUDE_BIN sotto launchd); V-1 ve BASSA (rilevatore sempre in errore); V-2/V-3 ve BASSE (igiene dei test); V-4 ve BASSA (scripts/voce/ fuori dal perimetro); V-5 ve BASSA (spegni.sh e due garanzie senza test); V-6 ve COSMETICA; R-623-1/2/3; R-615-4 MEDIA (microfono sotto launchd, da provare sul Mac); R-615-5 BASSA (licenza).
- Da #319: V-1 bot su 9c44686 BASSA (limite dichiarato) e le altre registrate in stato_progetto.
