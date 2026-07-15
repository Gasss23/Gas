# diff_sessione — 2026-07-15 (revisione-fondamenta: audit Fable-5 + pulizia 17 file morti)

> Fotografia dell'ultima sessione. La storia completa sta in git.

## Sessione

Branch: `chore/fondamenta-registro-pulizia` (da main `9cbab56`)
Commit: `bdec279`, `1b03adc`, `942c5c8`

## File toccati (BASE=9cbab56..HEAD)

### Aggiunti / modificati — motore e config
- `.gitignore` — aggiunta riga `.venv/` sotto `venv/` (fix F7: snapshot non assorbe più il virtualenv)
- `CLAUDE.md` sez.2 — cascata e Core Files aggiornati alla realtà del codice attivo
- `brains/router.py` — ridotto da 62 a 18 righe: rimossi get_brain/rispondi/_chiama legacy; mantenuto solo classifica_compito

### Rimossi — 17 file morti
- `gas`, `router` — junk root (testo, non Python)
- `brains/claude_brain.py` — brain legacy non wired; conteneva messages[-8:] (violazione §5)
- `brains/gemini_brain.py` — brain legacy non wired
- `brains/groq_brain.py` — brain legacy non wired
- `brains/openrouter_brain.py` — brain legacy non wired
- `self_improve/__init__.py`, `self_improve/loop.py`, `self_improve/researcher.py` — modulo non wired, non testato
- `modules/marketing/campaign.py`, `funnel_test.py`, `test_postcleanup.py`, `test_finale.py`, `riassunto_canone.md`, `strategy.txt` — marketing husk FASE 4 (da costruire)
- `deploy_vps_bozza.txt`, `test_agente.py` — junk root

### Modificati — reports
- `reports/roadmap.md` — blocco "REVISIONE FONDAMENTA Fable-5" inserito dopo item #6 della lista PROSSIMI PASSI
- `reports/stato_progetto.md` — header aggiornato; F6-history-atomica in Finding aperti; R-crm-diario-rr promosso a fetta; note minori Fable-5; item locale/clone Windows chiusi; R-legacy-slice marcato chiuso
- `reports/ultimo_report.md` — report di fine task (questa sessione)
- `reports/handoff.md` — dossier di fine sessione (questa sessione)
- `reports/diff_sessione.md` — questo file

## Perché

Audit integrale da Fable-5 (SHA 9cbab56) confermava fondamenta SOLIDE e 17 file morti non connessi al kernel. `claude_brain.py` conteneva anche `messages[-8:]` (slicing raw §5). Pulizia abbatte il debito di superficie manutenibile senza rischi (delta suite zero, grep residui vuoto, revisore APPROVATO).
