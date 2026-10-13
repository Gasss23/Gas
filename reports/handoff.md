# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-13 — raccolta dei problemi aperti dalla fetta `cerca_testo` (PR #193)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR — numero e URL compilati al passo 4bis dopo il push (solo da `gh`).
2. **Non mergio io**: `reports/stato_progetto.md` non e' nella lista bianca `LOG_DI_SESSIONE` di
   `scripts/bot_esito.py`, quindi questa PR non ricade nell'eccezione di merge autonomo per i soli log di
   sessione.
3. **Due voci della lista sono decisioni tue, non lavoro**: `C1`/`R-297-3` (il salto dei log non dipende
   dalla dimensione; l'alternativa condizionata e' provata e perde la protezione sul tetto dei risultati) e
   `E2` (numerazione univoca delle review: otto duplicati, da decidere sul ramo di integrazione).
4. **`E4`**: resta da chiarire se hai una sessione viva altrove. Quattro commit di autore ignoto
   (`Co-Authored-By: Claude Opus 5.5`, trailer `session_01FgYcG4uNEqggobeJsbmE93`) sono entrati nella PR #193
   da fuori questa macchina. Non e' un problema di codice: e' sapere chi scrive sul repo.

---

## §1 SCOPE & ESITO FETTE

- **Task unico — raccogliere i problemi aperti in un posto solo**: `FATTA`.
  Scritta in `reports/stato_progetto.md` la sezione «Problemi aperti dalla fetta `cerca_testo` (PR #193) —
  da chiudere in UNA sessione»: 13 voci in 5 gruppi (A hook, B bot, C `cerca_testo`, D sicurezza,
  E igiene/processo). **Ogni voce riverificata su `origin/main` `a9fd74d`**, non ricopiata: due risultavano
  gia' chiuse dal merge (marcate «non rifarle»), una chiusa solo a metà, nove aperte.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md  |  59 +++++++++++++-------------------------------------
 reports/handoff.md        | 437 +++++++++++++++++++++++++++++++++++++++++++++++++++---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md | 145 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/ultimo_report.md  | 204 ++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------
 4 files changed, 272 insertions(+), 573 deletions(-)
```

Base = `a9fd74de346e`, il merge-base con `origin/main` ricalcolato adesso (`a9fd74d`, dopo il merge di #193,
#195 e #196).

## §3 GIT LOG --ONELINE (sessione)

```
(nessun commit: il commit di fine-task e' quello che contiene questo file)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; il suo hash
e' nel log del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore, revisore non richiesto. Il diff tocca **solo `reports/`**, che e' fuori dal perimetro di
review (`.claude/perimetro_review.txt`: `gas.py`, `brains/`, `modules/`, `tests/` piu' la macchina di
controllo), e CLAUDE.md sez. 3 dice esplicitamente che i commit di soli `reports/` o doc fuori dal perimetro
non richiedono review.

I verdetti del revisore sulla fetta `cerca_testo` — dieci giri, #297-#310 — sono nella storia git
nell'handoff al merge della PR #193 (`ceb9d90e`).

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a `gas.py` ne' a `tests/`: nessun delta da dichiarare.

Per riferimento, misurato da me su un worktree di `origin/main` (`a9fd74d`) all'inizio di questo task, per
stabilire che la base da cui si parte e' sana: suite kernel **840 PASS, 0 FAIL**; pytest **1067 passed,
1 skipped**. Il FAIL T80u5, trascinato per mezza sessione di ieri come preesistente, non esiste piu' (lo ha
chiuso la PR #195).

## §6 STATO CI

Nessuna run disponibile alla scrittura: questo e' il primo push del branch, quindi la run viene creata dal
push che segue questa scrittura. **Mappatura commit→run**: il solo commit di sessione e' quello di fine-task
che contiene questo file — **run non ancora disponibile alla scrittura dell'handoff**. L'esito va letto sulla
PR, non qui.

Nota su un check *required*: `verifica-bot` ha un falso rosso provato su due PR (voce `B1` della lista), e la
PR non e' immergeabile finche' non riporta success. Se arriva rosso senza un finding ALTA/MEDIA corrispondente
nel verdetto, la prima cosa da sospettare e' quel bug e non una riserva vera.

## §7 RISERVE APERTE

Questo task non apre riserve proprie: il suo scopo e' **elencare** quelle esistenti. La lista completa e
verificata e' in `reports/stato_progetto.md`, sezione «Problemi aperti dalla fetta `cerca_testo` (PR #193)»:

- **A1** (ALTA) `promemoria_end.sh` cieco al worktree — la meta' non corretta di `R-gate-worktree-1`.
- **A2** (BASSA) `R-gate-matcher-1`: il gate blocca comandi che non committano (sei occorrenze, tre inneschi).
- **B1** (ALTA come impatto) `verifica-bot`: falsi rossi su un check required, provati su #193 e #196.
- **C1** (BASSA, decisione dell'operatore) `R-297-3` + `V-4`.
- **C2** (semantica) `R-301-3`: `letti` conta anche il file dichiarato «non letto».
- **C3** (BASSA) `V-2`: `_LOG_SFORO_MAX` e' un numero, non un limite dimostrato.
- **C4** (BASSA, non provata raggiungibile) `V-5`: «solo nella root» assume `cwd == root`.
- **C5** (COSMETICHE) attribuzione del log dopo il primo tetto; commento «~200 KB» falso; due test da non
  unificare nelle asserzioni.
- **D1** (ALTA) nove buchi della denylist credenziali, tutti ancora leggibili su `a9fd74d`.
- **E1** `AGENTS.md` non tracciata e non ignorata; **E2** otto numeri di review duplicati; **E3** il token
  `gh` amministra il repo; **E4** autore ignoto dei quattro commit nella PR #193.
- Gia' chiuse e da non rifare: `R-300-2`, `R-301-4`, `R-gate-worktree-1` (per `review_gate.sh`),
  T80u5. `R-299-1` chiusa nel codice ma non coperta da test (dichiarato).
