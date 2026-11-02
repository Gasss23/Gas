# Diff della sessione — 2026-11-02 — Voce V8, «prova voci» e libreria (chat M2)

- `modules/voice/prova_voci.py` — frasi fisse, categorie ammesse, tetti orari delle prove e delle aggiunte.
- `modules/voice/tts.py` — elenco voci, voce scelta per la prova, ricerca e aggiunta dalla libreria condivisa.
- `modules/voice/server.py` — pagina `/voci`, `GET /voci/elenco` e `/voci/libreria`, `POST /voci/prova` e `/voci/aggiungi`; convive coi tempi della V7a e col formato a pezzi della V7b.
- `clients/voice/prova_voci.html` — pagina per ascoltare e scegliere la voce.
- `clients/voice/browser_server.py` — il proxy inoltra `/voci/*` con le guardie host locale e stessa origine; gli elenchi solo se vengono dalla pagina.
- `.github/workflows/ci.yml` — test di «prova voci» nel passo della suite voce.
- `tests/test_unit_voice_prova_voci.py` — test di server, proxy e pagina.
- `reports/prova_voce_mac.md` — guida Mac per la pagina e la libreria.
- `.claude/agents/memoria_revisore.md` — review #624–#629-M2, #655–#656-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
