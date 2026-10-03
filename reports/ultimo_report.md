# ULTIMO REPORT — 2026-10-04 — Il gate protegge se stesso + verifica esterna strutturata

Branch `fix/gate-autoprotezione` · PR #119 · commit `112f8af` · review #138 APPROVATO CON RISERVE → #139 **BOCCIATO** (corretto) → #140 **APPROVATO CON RISERVE**

## DECISIONI UMANE RICHIESTE

1. Merge della PR #119 (variante A: `gasmerge 119`), DOPO aver letto la verifica esterna di questa fetta.
2. R-138-5: allargare il perimetro di review anche a `gas_identity.md`, `knowledge/sources.yaml`, `tools/ingest_knowledge.py`, `clients/voice/`, `requirements*.txt`?

## Esito per step

- **V-1** (il gate non proteggeva se stesso): CHIUSA. Il perimetro di review unico `.claude/perimetro_review.txt` copre motore, hook, settings.json, script dei gate, revisore.md, verifica_esterna.md, fine-task.md e CI.
- **R-138-1** (il perimetro poteva togliersi da solo): CHIUSA. Le voci sono l'unione di voci cablate, working tree, index e HEAD (base per il gate B).
- **V-2** (citazioni non verificate fuori perimetro): CHIUSA.
- **R-136-5** (bastavano citazioni di .md): CHIUSA.
- **R-138-2** (rename e nomi non-ASCII): CHIUSA.
- **R-138-4** (test del gate non in CI): CHIUSA.
- **R-138-6** (promemoria non aggiornato): CHIUSA.
- **V-3** (gate B non bloccante): CHIUSA. `handoff-check` è required in `main-lock`, autorizzato dall'operatore.
- **Blocco #139** (la pipeline con `tr` nascondeva l'exit code di git, regressione della #80): CORRETTO, con test che lo dimostra.
- **R-136-2 / R-138-3 / R-139-1** (formati alternativi del verdetto): MITIGATE con regex allargata, forma canonica del verdetto nullo e divieto del riepilogo "Verdetto finale:".
- **Verifica esterna**: FATTA come istituzione E. Protocollo fisso in `.claude/verifica_esterna.md`; ogni verifica è un agente nuovo su Sonnet (contesto vergine), lanciato da fine-task §4quater. La sessione persistente "Verificatore" è dismessa.
- **R-138-5** (perimetro più largo): DEFERITA, decide l'operatore.

## Test

- `pytest tests --ignore=tests/test_unit_kernel.py`: 247 → **266 passed**.
- Gli handoff reali di C4b-3 (c868bc0) e della #118 (77b5edf) passano anche con le regole nuove (25 e 12 citazioni).
- Kernel non rilanciato: la fetta non tocca gas.py, brains/ o modules/.

## Riserve aperte

R-139-1 (mitigata), R-138-5 (decisione), R-136-3, R-137-1/2/3, residuo basso P4b (target di un symlink già committato). Dettaglio in `reports/stato_progetto.md`.

## Anomalie

- La review #139 ha BOCCIATO il primo diff: il fix `-z` aveva reintrodotto un fail-open già chiuso nella #80. Corretto prima del commit. Il revisore ha fatto il suo lavoro.
