# diff_sessione — 2026-07-15 (revisione-fondamenta: audit Fable-5 + pulizia 17 file morti)

> Fotografia dell'ultima sessione. La storia completa sta in git.

## Sessione

Branch: `chore/fondamenta-registro-pulizia` (da main `9cbab56`)
Commit: `bdec279`, `1b03adc`

## File toccati (HEAD~2..HEAD)

### Modificati
- `reports/roadmap.md` — blocco "REVISIONE FONDAMENTA Fable-5" inserito dopo item #6
- `reports/stato_progetto.md` — header aggiornato; F6-history-atomica inserita in Finding aperti; R-crm-diario-rr promosso a fetta; note minori Fable-5 aggiunte; item locale/clone Windows risolti; R-legacy-slice chiuso
- `.gitignore` — aggiunta riga `.venv/` sotto `venv/` (fix F7)
- `CLAUDE.md` sez.2 — cascata e Core Files aggiornati alla realtà del codice
- `brains/router.py` — ridotto da 62 a 18 righe: rimosso get_brain/rispondi/_chiama legacy; mantenuto solo classifica_compito

### Rimossi (17 file)
- `gas`, `router` — junk root (testo)
- `brains/claude_brain.py`, `gemini_brain.py`, `groq_brain.py`, `openrouter_brain.py` — brain legacy non wired
- `self_improve/__init__.py`, `loop.py`, `researcher.py` — modulo non wired
- `modules/marketing/campaign.py`, `funnel_test.py`, `test_postcleanup.py`, `test_finale.py`, `riassunto_canone.md`, `strategy.txt` — marketing husk FASE 4
- `deploy_vps_bozza.txt`, `test_agente.py` — junk root

## Perché

Audit integrale da Fable-5 (SHA 9cbab56) confermava che i file rimossi erano codice morto non collegato al kernel attivo. `claude_brain.py` conteneva anche slicing `messages[-8:]` (violazione §5). La pulizia abbatte il debito di superficie manutenibile senza rischi (delta suite zero, grep residui vuoto, revisore APPROVATO).
