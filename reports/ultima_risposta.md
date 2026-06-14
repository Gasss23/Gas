Task completato. Riepilogo finale.

## ✅ FASE 2 / FASE 1 punto 1 — Sandbox OS (bwrap) per `run_command`

**Report:** `reports/ultimo_report.md` · **Commit:** `8b42f9791aef2e9c8cb28e292677f955d66c91fd` (pushato su `main`) · **Suite:** 52 PASS, 0 FAIL · **Review #6:** APPROVATO CON RISERVE

### Risposte ai chiarimenti (P0)
- **SessionEnd in `5cc609b`** = **add SELETTIVO non-motore** (`git add reports/ '*.md' .gas_history.json`, mai `-A`). `gas.py`/`brains/`/`modules/`/`tests/` **non possono** essere auto-committati. Verificato.
- **Riserve revisore #5** (R1 modello free volatile, R2 degrado solo-testo non rilevato, R3 duplicazione costanti) tracciate in `stato_progetto.md`.

### Implementato (decisioni §6)
- **§6.1** profilo bwrap con mascheramento tmpfs di `/home`,`/root`,`/run` e re-bind RO della project root **per ultimo** — chiude R2 **anche in lettura**. `/tmp` lasciato RO (deviazione consapevole, più severo).
- **§6.2** `GAS_SANDBOX_MODE` (`os_strict` default fail-closed / `os_with_fallback`), fail-safe su `os_strict`; doctor FAIL/WARN per mode.
- **§6.3** ortogonale a `GAS_SHELL_MODE`; ordine `vetting→dry_run→snapshot→check sandbox→exec`; doctor sonda SEMPRE.

### Sonda ambiente (fatta PRIMA di progettare, come da roadmap)
Codespace: bwrap 0.9.0, namespace concessi. 4 barriere validate empiricamente.

### Test che mordono (reali)
T13a rete chiusa (rc=2) · T13b fs RO · **T13c esca segreta sotto /home mascherata** · T13d/d2 fallback per mode · T13e lecito dentro bwrap + snapshot.

### Verdetto revisore #6
APPROVATO CON RISERVE. **Declassamento condizionato** (os_strict + sandbox disponibile) dei finding esfiltrazione e R2 #4. Le tre riserve #6 (R1 snapshot-prima-del-check per decisione §6.3, R2 caveat `--chdir`/cwd, R3 duplicazione mode in doctor) sono tracciate in `stato_progetto.md` — **nessuna indebolisce i guardrail**.

Nota su R1 #6: il revisore suggeriva di anticipare il check sandbox prima dello snapshot, ma l'ordine `snapshot→check` è una tua **decisione esplicita §6.3**, quindi l'ho rispettato e tracciato come riserva (candidato per i prossimi passi) invece di modificarlo unilateralmente.
