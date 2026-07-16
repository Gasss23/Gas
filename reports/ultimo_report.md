# Report fine task — F6 atomicità .gas_history.json (2026-07-16)

## DECISIONI UMANE RICHIESTE

1. **Merge PR #19** (`feature/f6-history-atomica` → main): CI verde ✅ — revisiona diff e approva il merge.
2. **Recupero review #49 in memoria_revisore.md**: la lezione di review #49 è nel commit locale `92a08ba` (non pushato — main-lock bloccante). Proposta: aggiungere la riga nel prossimo commit doc o fare cherry-pick su un branch.

## Scope

F6 — atomicità `.gas_history.json` (finding aperto dal 2026-07-15, revisione Fable-5).
STOP gate: SOLO `_save_history` e `_load_history` in `gas.py` + test T59a/b/c in `tests/test_unit_kernel.py`. Nessun altro file del motore.

## Esito fette

| Fetta | Descrizione | Esito |
|-------|-------------|-------|
| 1 — MOTORE | `_save_history` atomico + `_load_history` quarantena + T59a/b/c | FATTA |
| 2 — DOC | `stato_progetto.md`: counter review, F6 chiuso, micro-finding | FATTA |

## Modifiche applicate

### 1. `gas.py` — `_save_history`

- Serializza in stringa in memoria
- Scrive su `.gas_history.json.tmp.<pid>` (stessa directory)
- `f.flush()` + `os.fsync(f.fileno())`
- `os.replace(tmp, db_path)` — atomico su POSIX
- fsync directory in try/except best-effort (FS che non lo supportano: ignora)
- Su eccezione: `logging.warning` + `tmp.unlink()` (fail-safe §9) — file originale intatto

### 2. `gas.py` — `_load_history`

- JSON invalido/corrotto → `logging.warning` + rename a `.gas_history.json.corrupt.<YYYYmmdd-HHMMSS>`
- Collisione timestamp → suffisso con microseconds (MAI overwrite di `.corrupt` esistente)
- Quarantena fallita → `logging.warning` + ritorna `[]` (mai crash)
- Nessuna eccezione propagata al chiamante

### 3. `tests/test_unit_kernel.py` — T59a/b/c

- **T59a**: round-trip save→load corretto + nessun `*.tmp*` residuo
- **T59b**: file corrotto → storia vuota + zero eccezioni + esattamente 1 `.corrupt.*` + contenuto originale preservato (byte-a-byte)
- **T59c**: `os.replace` monkeypatched a sollevare → no crash + file originale intatto (byte-a-byte) + tmp rimosso

### 4. `reports/stato_progetto.md`

- Aggiornato contatore review: 48→50 (ultima #50, F6 atomicità)
- F6 finding: 🟡→✅ chiuso (PR #19, CI verde)
- Aggiunta discrepanza contatore + micro-finding processo (c)(f)
- R-crm-diario-rr: confermato CHIUSO (PR #18 su origin/main)

## Verdetto revisore (review #50) — VERBATIM

> **APPROVATO**
>
> Il fix implementa esattamente ciò che il finding F6 richiedeva, con pattern di atomicità POSIX corretti, fail-safe §9 completo su tutti i path di eccezione, e tre test che mordono in modo mirato (round-trip, corruzione+quarantena, fallimento atomico). Nessuna violazione di scope, nessun antipattern del Wall of Shame, nessun guardrail indebolito.
>
> (Revisore review #50, 2026-07-16 — nessuna riserva, nessuna lezione nuova aggiunta a memoria_revisore.md)

## git diff --stat (BASE=origin/main)

```
 gas.py                    | 46 +++++++++++++++++++++++++++-----
 tests/test_unit_kernel.py | 67 +++++++++++++++++++++++++++++++++++++++++++++++
 reports/stato_progetto.md | ~20 righe modificate (doc-only, commit separato)
 reports/ultimo_report.md  | questo file (commit separato)
```

Motore: `gas.py` + `tests/test_unit_kernel.py` in commit `e9ffee0`.
Doc: `stato_progetto.md` + `ultimo_report.md` in commit separato (questa fetta 2).

## Delta test suite

- PRE-fetta: 231 PASS (run 29336713885, 2026-07-14)
- POST-fetta: **241 PASS, 0 FAIL** (run `29482410951`, 2026-07-16, feature/f6-history-atomica) — +10 test (T59a×2, T59b×2, T59c×3 + conversione T59a/b check split)
- Nota: T59 eseguiti anche in isolamento pre-commit: 7 PASS, 0 FAIL

## CI

- Run ID `29482410951` — **completed SUCCESS** su `feature/f6-history-atomica` (commit `e9ffee0`, 2026-07-16)

## Commit e PR

- Commit motore: `e9ffee0` (`fix(kernel): F6 atomicità .gas_history.json — write tmp+rename, quarantena corrotto`)
- Commit doc: questo commit (fetta 2 separata)
- Branch: `feature/f6-history-atomica`
- PR: https://github.com/Gasss23/Gas/pull/19

## Chiude

- **F6-history-atomica** (finding da revisione Fable-5, 2026-07-15) ✅

## Analisi discrepanza contatore review (fetta 2b)

- **stato_progetto.md** precedente: diceva #48 (R-crm-1b, 2026-07-14)
- **ultimo_report.md** (PR #18): diceva review #49 (R-crm-diario-rr, 2026-07-16)
- **memoria_revisore.md** su origin/main: termina a #47 (2026-07-14)
- **Dangling commit `92a08ba`** (solo local/main, bloccato da main-lock): aggiungeva la lezione di review #49

**Verità ricostruita**: review #48 (R-crm-1b merge umano) + review #49 (R-crm-diario-rr) non hanno aggiunto lezioni al file canonical (eccetto #49 nel commit locale non pushato). Review #50 (questa sessione, F6) non aggiunge lezioni.
**Contatore corretto**: 50. Stato aggiornato a 50/#50.

## Analisi gate review #49 vs test modificato (fetta 2f)

**Evidenza git**: un solo commit fix `894eb06` che include ENTRAMBI la fix `store.py` e il test finale `m._connect()`.

**Evidenza handoff PR #18**: un solo verdetto — review #49 "APPROVATO CON RISERVE" sulla versione raw del test; poi "Riserva risolta in-session: il test è stato aggiornato a usare `m._connect()`"; poi "Il revisore ha verificato anche:" (3 bullet in discorso indiretto).

**Conclusione**: il test fu modificato DOPO il verdetto #49. Non risulta un secondo verdetto esplicito del revisore sul test aggiornato. Il gate non è stato formalmente chiuso sull'aggiornamento. Registrato come micro-finding di processo in stato_progetto.md.

## Proposte fuori scope

- **Cherry-pick `92a08ba`** (lezione review #49 su memoria_revisore.md) sul prossimo branch doc: proposta da valutare in sessione futura.
- **F2 — budget kill-switch**: GATED, nessun impegno.
- **F7 — .venv gitignorato su VPS**: runbook SSH, nessun impegno.
