# Report — Fix gate di review inerte (jq 1.7 + input oggetto)

**Branch:** fix/gate-review-jq (nuovo da main `9e848d0`; tutta la sessione su questo branch)
**Data:** 2026-10-03
**Review:** #129 — APPROVATO CON RISERVE
**Commit:** `b991a99` (fix hook + test), `f7af312` (memoria revisore)
**PR:** https://github.com/Gasss23/Gas/pull/114 — merge all'operatore (gasmerge)

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #114 (https://github.com/Gasss23/Gas/pull/114) con gasmerge.
2. Opzionale: prova di controllo da terminale. Con `claude` da terminale, su questo branch o dopo il merge, ripetere il commit di prova (riga di commento in `gas.py`, stage, `git commit` senza marcatore). Atteso: "BLOCCATO (gate review)".

---

## STATO ONESTO

| Passo | Esito |
|---|---|
| Prova del gate nell'app (prima del fix) | FATTA — commit di `gas.py` senza review **PASSATO**: gate inerte |
| Diagnosi | FATTA — causa nello script, non nell'app (riprodotto lanciando l'hook a mano) |
| Fix parser + fail-closed | FATTA |
| Test con input oggetto | FATTA — T-gate-E..I |
| Prova del gate nell'app (dopo il fix) | FATTA — stesso commit **BLOCCATO** |
| Prova da terminale | NON fatta — superflua per la diagnosi (lo script si comporta allo stesso modo fuori dall'app); resta opzionale per l'operatore |
| R-c4b1-1 (suite non ermetica) | DEFERITA — prossima fetta, come concordato |

---

## PROVA E DIAGNOSI

Prova nell'app, su branch usa-e-getta `test/gate-app-probe` (mai pushato, poi cancellato): riga di commento aggiunta in `gas.py`, stage, `.claude/.review_ok` assente, `git commit` → **commit creato** (`7c38537`, poi annullato). Il gate non è scattato.

- L'hook è registrato correttamente: `.claude/settings.json`, PreToolUse, matcher "Bash".
- Lanciato a mano fuori dall'app, con input `{"tool_name":"Bash","tool_input":{"command":"git commit -m ..."}}` → exit 0.
- Causa: `.claude/hooks/review_gate.sh` leggeva il comando con jq `(.[0] // .) | .tool_input.command // empty`. Con `/usr/bin/jq` (jq-1.7.1-apple), `.[0]` su un oggetto è un ERRORE ("Cannot index object with number", rc 5), e `//` non lo sopprime. Risultato: comando vuoto → `exit 0` → fail-open.
- La CI non se ne accorgeva perché i test T-gate-A..D (`tests/test_unit_hooks.py:517`) passavano l'input solo come array `[{...}]`, che la vecchia espressione leggeva bene.
- Conseguenza: su questo Mac il gate deterministico non ha mai bloccato nulla da quando c'è jq. Le review sono state fatte comunque per procedura (barriera primaria). Da quando: non misurato, presumibilmente dalla migrazione al Mac (2026-09-09).

## FIX

- jq: `if type == "array" then .[0] else . end | .tool_input.command // empty` → gestisce oggetto e array.
- Se il parser fallisce (rc ≠ 0), il controllo "è un git commit?" si fa sul testo grezzo dell'input (fail-closed). I comandi non-commit restano liberi.
- Rami python/perl invariati: gestivano già oggetto e array (il revisore ha eseguito il ramo python togliendo jq dal PATH; il ramo perl l'ha solo letto).

## TEST

- Nuovi T-gate-E..I (classe `TestReviewGateInputOggetto`, riusa gli helper senza ereditare per non far girare due volte A-D): oggetto+motore senza marcatore → 2; oggetto+motore+marcatore → 0; oggetto+solo doc → 0; oggetto non-commit → 0; JSON illeggibile con commit+motore → 2.
- Test esistente modificato: `TestReviewGateFailClosed._run` ha un parametro opzionale `stdin` (default invariato). Motivo: passare l'input oggetto ai nuovi test. T-gate-A..D invariati e verdi.
- Discriminanza: con l'hook VECCHIO cadono T-gate-E e T-gate-I (2 failed, 7 passed); col fix 9 passed. Il revisore l'ha riprodotto in modo indipendente.
- Suite hook: **51 → 56 passed**. pytest totale (escluso test_unit_kernel.py ed e2e): **227 → 232 passed**. La suite del kernel non è toccata (nessuna modifica a gas.py/modules/).
- Prova reale nell'app dopo il fix (l'hook gira dal working tree): stesso commit di prova → `PreToolUse:Bash hook error: ... BLOCCATO (gate review) ...`, nessun commit creato; riga di prova rimossa.
- Effetto osservato subito dopo: il mio primo comando di commit di questa fetta (`touch .claude/.review_ok && git commit ...` nello stesso comando) è stato **BLOCCATO**, perché l'hook gira prima del comando, quando il marcatore non esiste ancora. Ho rifatto con il `touch` in un comando separato. Nella sessione C4b-1 quel comando unico era passato solo perché il gate era inerte.

## RISERVE (review #129)

- **R-gjq-1** (operativa): il matcher `git[[:space:]].*commit` ora blocca qualsiasi comando che contiene quel testo mentre c'è codice del motore in stage senza marcatore. Inoltre il marcatore va creato con un comando separato prima del commit.
- **R-gjq-2** (copertura): i rami python/perl con input oggetto non sono testati in CI.
- **R-gjq-3** (minore, pre-esistente): grep assente → `|| exit 0` (fail-open).

## ANOMALIE

- Il gate inerte stesso è l'anomalia principale. È registrato in stato_progetto.md come F-gate-inerte (chiuso dalla PR #114).
