# Diff della sessione — 2026-11-02 — Voce V7b, voce frase per frase (chat M2)

- `modules/voice/server.py` — formato «audio+testo+pezzi»: risposta NDJSON con una sintesi per frase e riga «fine» coi tempi; stop su errore della voce o pagina chiusa; guardia sul tipo di `t_cervello`.
- `clients/voice/browser_server.py` — il proxy inoltra le righe appena arrivano; thread di guardia che chiude la connessione verso il server se la pagina chiude.
- `clients/voice/browser_client.html` — lettore di righe, frasi suonate in fila, interruzione/pausa/errore fermano le frasi in arrivo, riascolto di tutta la parte parlata.
- `tests/test_unit_voice_server.py` — test del formato a pezzi (server, proxy, pagina nel browser con «pezzi», «pezzi_interrotti» e «guasto»).
- `.claude/agents/memoria_revisore.md` — review #618–#622-M2, #651–#653-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
