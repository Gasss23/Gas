# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-08-06 — Sanare stato_progetto.md: sonda F0, scope-creep #59, decisioni aperte

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR `docs/stato-fase3-sonda` su main.
2. **🔴 Ruotare subito la chiave ElevenLabs** esposta in chat di sessione. Verificare che non sia hardcoded in nessun file sotto `clients/`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Annotare sonda F0 in "Prossimi passi" §4**: `FATTA`
  Riga aggiunta sotto FASE 3: sonda atterrata (PR #59, merge 5323b9b, 2026-08-02), 6 script in `clients/voice/probe/`; sonda ≠ pipeline; FASE 3 DA COSTRUIRE.

- **Fetta 2 — Note datate 2026-08-02**: `FATTA`
  (a) Scope-creep PR #59: sonda voce + allowlist gasmerge-ip in un unico branch; recidiva classe 2026-07-08.
  (b) Esito "6/6 verde" dichiarato solo nel subject di commit 4056c97, NON nel §1 del handoff: da riconfermare.

- **Fetta 3 — Decisioni aperte D1-ter / D2-audio / SICUREZZA**: `FATTA`
  Tre voci registrate in stato_progetto.md prima delle righe di archivio finali.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  | 28 +++++++-------------
 reports/handoff.md        | 65 ++++++++++++++---------------------------------
 reports/stato_progetto.md |  9 ++++++-
 reports/ultimo_report.md  | 43 +++++++++++++++----------------
 4 files changed, 56 insertions(+), 89 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
4c41b6b docs(stato): sonda F0 atterrata su main, scope-creep #59, decisioni aperte D1-ter/D2-audio/sicurezza
```

NB: il commit di fine-task (con i report) non compare ancora — viene creato dopo questo blocco.

---

## §4 VERDETTO DEL REVISORE

nessun diff motore, revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

---

## §6 STATO CI

```
in_progress  docs(stato): sonda F0 atterrata su main, scope-creep #59, decisioni a…  CI  docs/stato-fase3-sonda  push  31119916342  2m28s  2026-08-06T16:27:53Z
completed    success  Merge pull request #59 from Gasss23/feature/voice-probe  CI  main  push  30760725254  53s  2026-08-02T18:15:54Z
completed    success  docs(voice-probe): allowlist IP su meta-righe handoff/ultimo_report (…  CI  feature/voice-probe  push  30760658988  45s  2026-08-02T18:14:07Z
```

Mappatura commit→run:
- `4c41b6b` (commit motore sessione precedente): run CI `31119916342` in_progress al momento della scrittura dell'handoff — run su branch `docs/stato-fase3-sonda`, push del commit `4c41b6b`. Il commit dei report (questo handoff) non ha ancora una run al momento della scrittura.

La copertura pre-merge è garantita da `gasmerge` (`gh pr checks --watch`).

---

## §7 RISERVE APERTE

Nessuna (sessione doc-only, nessun diff motore).
