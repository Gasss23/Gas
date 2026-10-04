# ULTIMO REPORT — 2026-10-04 — Promemoria di gasmerge dal perimetro, ref completi (anche gate IP), .gitignore audio

Branch `fix/gasmerge-perimetro-gitignore` · PR #122 · commit `03e01f8` + `27f04b7` · review #145 + #146 + #147 **APPROVATO CON RISERVE** · verifica esterna #122 **APPROVATO CON RISERVE** (V-1/V-2 corretti in `27f04b7`)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #122 (variante A: `gasmerge 122`), dopo la verifica esterna del nuovo handoff.
2. R-147-1 (MEDIA, preesistente): un branch o un path che contiene `gasmerge-ip-ok` aggira il gate IP. Correggerlo in una micro-fetta PRIMA della V-B vera? (consigliato: sì, è piccola)
3. V-3 (verifica #121): vietare nel ruleset i tag `origin/*`? Oggi la difesa sono i ref completi negli script.
4. V-5 (verifica #121): mettere `.gitignore`, `knowledge/` e `CLAUDE.md` nel perimetro di review?
5. Poi la prossima fetta PRIORITARIA, già decisa: V-B "vera" (bot di revisione su GitHub).

## Esito per step

- **V-1 verifica #121** (gasmerge con regex propria): FATTA. Il promemoria legge `.claude/perimetro_review.txt` (main ∪ branch).
- **R-144-1** (ref abbreviati): FATTA in due tempi. `03e01f8` l'aveva dichiarata chiusa, ma la verifica esterna #122 ha trovato il ref abbreviato nel gate IP (`gasmerge.sh:91`, aggirabile con un tag `origin/<branch>`) e in `check_landing.sh:33`. Chiusa davvero in `27f04b7`, con 3 test a tag omonimo.
- **V-2 verifica #121** (R-143-4 parziale): FATTA. `.gitignore`: `*.wav`, `*.mp3`, `clients/**/*_output.{wav,mp3,txt,json}`.
- **R-145-1 / R-145-2**: FATTE nella stessa fetta.
- **Correzioni stato_progetto** (R-143-4 PARZIALE, R-143-1 chiusa dopo il merge di #121): FATTA.
- **Tracciamento V-3 / V-5 (verifica #121) e R-147-1/2/3**: FATTA (stato_progetto, aperte).
- **R-147-1**: DEFERITA — preesistente, tocca anche `fine_task_finale.sh`; decisione operatore (punto 2).
- **V-B vera**: DEFERITA — prossima fetta.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py --ignore=tests/e2e`: 275 → **284 passed**.
- Controprove: i nuovi test falliscono con lo script precedente (perimetro: 5 failed col gasmerge.sh di main; gate IP e check_landing: falliscono con gli script di `4e598e2`; la mutation della riga 144 col ref abbreviato è uccisa).
- CI: `unit-suite` verde su Linux già su `03e01f8` e `4e598e2` (test non-ASCII compreso).
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

- R-147-1 (MEDIA): vedi decisione 2.
- R-147-2 (minore): mutation sopravvissute su `gasmerge.sh:42` e sul perimetro letto da main.
- R-147-3 (minore): `tests/test_unit_gasmerge.py` non gira in ci.yml.
- Minori #146: righe `clients/**/*_output.{wav,mp3}` ridondanti; fixture audio in tests/ con `git add -f`.

## Anomalie

- Il primo fine-task (`4e598e2`) dichiarava R-144-1 chiusa: era falso (gate IP). L'ha scoperto la verifica esterna, non il revisore (#145/#146) né l'agente.
- PR creata con `--title/--body` invece di `--fill` (non interattiva; numero da `gh`).
- Nel primo commit, `segna_review_ok.sh` e `git commit` nello stesso comando: bloccato dal gate (corretto), rifatto in due comandi.
