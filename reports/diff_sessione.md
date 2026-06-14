# 🔧 DIFF DI SESSIONE — 2026-06-14 (consolidamento motore: TASK B + TASK C)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git).
> Riscritto a ogni sessione.

## Audit STEP 0 (pre-blocco / riconciliazione)
- `git status` pulito, `origin/main..HEAD` VUOTO: nessun lavoro non pushato perso.
- La sessione precedente, prima del blocco di billing, aveva **già completato e
  pushato TASK A** (commit `1cae65a`): costanti provider de-duplicate, helper
  `_parse_mode` condiviso init/doctor, test T16a/b/c presenti.
- Baseline reale: suite **64/64** (61 review #8 + 3 T16 di TASK A) — coerente,
  nessun codice mancante. Non era 61 perché TASK A è andato oltre la previsione
  della consegna: NON un errore, lavoro genuino e committato. Proceduto con B e C.

## File toccati in questa sessione
- **gas.py** (motore, 2 commit revisionati):
  - TASK B: costanti `TOOL_CAPABLE_MODELS`; helper `_model_tool_capable`,
    `_free_model_endpoint_url`, `_http_get_json`, `_classify_free_model`,
    `_probe_free_model`; warning di osservabilità in `run_turn`; voce
    "Paracadute / modello free" in `doctor`.
  - TASK C: helper `_ref_age_epoch`, `_snapshot_retention`; costanti
    `SNAPSHOT_KEEP_DAYS`, `SNAPSHOT_LOG_MAX_BYTES`; retention ibrida + log delle
    rimozioni e rotazione `.1` in `_snapshot`; sezione 7 "Snapshot" in `doctor`.
- **tests/test_unit_kernel.py** (revisionato): blocchi T17 (5 check, TASK B) e
  T18 (6 check, TASK C); T11f riadattato al ramo count-based. 64 → **75**.
- **.gitignore**: `reports/snapshots.log` e `reports/snapshots.log.1`.
- **reports/** (doc, no review): `stato_progetto.md`, `diff_sessione.md`,
  `ultimo_report.md` rigenerato.
- **.claude/agents/memoria_revisore.md**: lezioni nuove dei review #9 e #10.

## Perché (sintesi)
- **TASK B** chiude R1 #5 (modello free volatile: `doctor` ora ne verifica
  esistenza e capacità tool, solo metadati, zero token) e la metà deterministica
  di R2 #5 (degrado a solo-testo osservato a freddo + warning statico in
  `run_turn`; rilevamento per-turno rimandato per falsi positivi). Forma dell'API
  OpenRouter SONDATA dal vivo prima di progettare.
- **TASK C** chiude le riserve snapshot R2/R3: retention IBRIDA (count ∪ età) che
  protegge i recenti, log gitignorato + rotazione, `doctor` report-only.
  Vincolo di PRUDENZA rispettato: nessun `git gc` automatico, rimozione ref
  loggata e reversibile fino al gc (la macchina del tempo non è indebolita).

## Verifica
- Suite **75 PASS, 0 FAIL** (output reale, zero token LLM).
- `gas doctor` provato dal vivo: nuove righe Paracadute/Snapshot OK, nessun crash.
- Gate di review rispettato: review #9 (TASK B) e #10 (TASK C), entrambe
  APPROVATO CON RISERVE (riserve tracciate in `stato_progetto.md`).

## Commit della sessione
- `a9f1053` TASK B — integrità paracadute free
- `35a9b7e` TASK C — manutenzione snapshot
(TASK A `1cae65a` era già stato pushato dalla sessione precedente.)
