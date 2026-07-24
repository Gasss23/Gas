# Diff sessione — chore/hardening-processo (2026-07-24)

> Riscritto a ogni sessione. La storia completa sta in git.
> Range: 1ebea40..HEAD (fork da origin/main, PR #42 mergiata)

## File toccati

| File | Cosa è cambiato e perché |
|---|---|
| `tests/test_unit_kernel.py` | Gate di iniezione chiavi fittizie T9 (GEMINI/GROQ) cambiato da `is None` a falsy con sentinel `_MISSING`; il `finally` ripristina il valore ORIGINALE esatto invece di cancellare la chiave — chiudeva un falso-rosso ambientale con chiavi presenti-ma-vuote |
| `.claude/agents/revisore.md` | Nuova sezione "FORMATO OBBLIGATORIO DEL VERDETTO": vieta verdetti degeneri (sola riga di esito), richiede ≥2 elementi concreti del diff + un rischio escluso, dopo 3 recidive (#56, #59, PR #14/#18) |
| `.claude/agents/memoria_revisore.md` | Aggiunte righe #60 (APPROVATO, lezione sentinel simmetrico) e #61 (APPROVATO CON RISERVE, lezioni fail-open grep/diff + fetch-stantio) |
| `scripts/gasmerge.sh` | Nuovo file, versionato da `~/bin/gasmerge`: wrapper `main()` anti-corruzione mid-pull, fix CI (`--watch --fail-fast` + timeout 900 + verifica JSON indipendente su bucket), regex file sensibili estesa a `scripts/`/`.claude/`, stampa di provenienza pre-conferma |
| `.claude/commands/fine-task.md` | §6: nuova clausola "Mappatura commit→run OBBLIGATORIA" — vieta le formule collettive "tutti i commit hanno CI verde" |
| `reports/stato_progetto.md` | 5 correzioni: micro-finding CI PR #42 (3 commit su 2 run, f6b6caa mai testato da run propria); declassata attribuzione "247 PASS" da CI/Codespace a non verificata; recidiva Flag #3 (review #59) accanto a Flag #2; nuovo finding R-verdetto-evidenza; registrazione porting gasmerge |
| `reports/ultimo_report.md` | Report della sessione: esito per fetta, verdetti revisore integrali, output test grezzi, mappatura commit→run applicata a se stessa |
| `reports/handoff.md` | Dossier fine sessione con §0–§7 completi |
| `reports/diff_sessione.md` | Questo file |

## Azioni senza traccia in git

Nessuna in questa sessione. Tutte le modifiche sono passate da commit tracciati (`1551312`, `fd07a6d`, `81933c9`, `6f5ba71`, `4fd0d31`). Le esecuzioni di test locali (venv WSL, varie combinazioni di env vars) non producono per costruzione artefatti da tracciare.
