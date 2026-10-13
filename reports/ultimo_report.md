# ULTIMO REPORT — 2026-10-13 — Chiusura dei problemi aperti post #193 (lista #197)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #198** (https://github.com/Gasss23/Gas/pull/198). Tocca la macchina del bot (`scripts/bot_esito.py`, B1): per CLAUDE.md il merge lo decide l'operatore. I verdetti sono tutti APPROVATO CON RISERVE (nessun APPROVATO secco su ogni fetta), quindi niente merge autonomo.
2. **D1 è una fetta di sicurezza**: secondo passaggio nella chat claude.ai col link della PR #198.
3. **E3**: sostituire il token `gh` che amministra il repo con quello senza Administration (`reports/setup_agente_non_admin.md`).
4. **E4**: confermare che i quattro commit «di autore ignoto» di #193 vengono dalla tua sessione cloud claude.ai/code: il loro trailer `session_01FgYcG4uNEqggobeJsbmE93` è lo stesso di questa sessione.
5. **C3** (proposta): limitare a monte la lunghezza di un record di log, così `_LOG_SFORO_MAX` diventa una conseguenza e non una scommessa. Fetta a sé, se la vuoi.
6. **C4** (decisione): derivare la cartella del log da `handler.baseFilename` invece di assumere `cwd == root`, oppure lasciare com'è.

## Decisioni prese dall'operatore in sessione

- C1: il salto dei log resta; si corregge solo il testo (V-4).
- E2: niente rinumerazione delle review duplicate, resta la NOTA DI MERGE.
- E1: `AGENTS.md` in `.gitignore`.
- A2 e B1: «sì a entrambi» per rendere meno severi i due controlli, a condizione che nel dubbio blocchino.
- PR #197: era già mergiata a inizio sessione (main `04635d5`).

## Esito per voce

| Voce | Esito | Dettaglio |
|---|---|---|
| A1 promemoria_end cieco al worktree | FATTA | `cwd` del payload → repo del turno; contatore nel git-dir del worktree, una riga per `session_id`; test T-prom-wt-1..6. Review #314, #315 APPROVATO CON RISERVE. Non provato con il payload reale di una sessione in worktree. |
| A2 R-gate-matcher-1 | FATTA | `.claude/hooks/gate_matcher.py` + 6 righe in `review_gate.sh`. Review #318, #319, #320, #321 BOCCIATO (quattro bypass reali: git riconfigurato, `rg --pre`, commenti `#`, `printf "-v"`+`${x@P}`, `test -v`); taglio radicale; #322 APPROVATO CON RISERVE, #323 conferma. |
| B1 falsi rossi di verifica-bot | FATTA | Test con gli estratti reali di #196 (1761eb5) e #193 (7e4609b, bd3770f). Review #316 APPROVATO CON RISERVE (R-316-1 MEDIA chiusa), #317 APPROVATO. Merge: operatore. |
| C1 R-297-3 + V-4 | FATTA (solo testo) | Il messaggio non dice più «usa leggi_righe su quei file». |
| C2 R-301-3 | FATTA | `letti` conta solo i file davvero letti; R-326-1 (testo poi byte NUL) chiusa. |
| C3 V-2 `_LOG_SFORO_MAX` | DEFERITA — fetta a sé (tocca la scrittura del log) |
| C4 V-5 cwd == root | DEFERITA — decisione operatore |
| C5a, C5c | SALTATA — il revisore sconsigliava di toccarle |
| C5b commento ~200 KB | FATTA |
| D1 nove buchi denylist | FATTA | + token.pickle/.bin/.db, *.pgp, pezzo > 255 caratteri negato (costo lineare). Review #324, #325 APPROVATO CON RISERVE. |
| E1 AGENTS.md | FATTA |
| E2 numeri duplicati | CHIUSA senza modifiche (decisione operatore) |
| E3 token admin | DEFERITA — azione dell'operatore |
| E4 commit di autore ignoto | DEFERITA — conferma dell'operatore (vedi decisione 4) |
| Igiene stato_progetto.md | FATTA | La lista di 145 righe è spostata in `reports/stato_storico.md`; nell'attivo resta l'esito. |

## Test

- Kernel (`python tests/test_unit_kernel.py`): base 843 PASS / 0 FAIL → **846 PASS / 0 FAIL**.
- pytest completo dopo D1 (prima di C, che tocca solo la suite kernel): **1171 passed**.
- `tests/test_unit_hooks.py` 211 passed, `tests/test_unit_verifica_bot.py` 311 passed, `tests/test_unit_gate.py` 370 passed.

## Anomalie

- Il gate di review ha bloccato più volte comandi miei che non facevano commit (proprio A2): il nome `e_commit.py` lo faceva scattare su `git add`/`git diff`. Rinominato in `gate_matcher.py`.
- Disco della sessione pieno durante la review #327: liberato (cache pytest, tmp). Il revisore non ha potuto rieseguire la suite kernel; l'ho rieseguita io dopo la pulizia: 846/0.
- Il commit doc-only `40ee9b5` (promemoria #192/#193) che stava solo sul branch remoto è stato sostituito: il branch è ripartito da main aggiornato (push con `--force-with-lease`).
