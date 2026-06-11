# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-11**

## Stato del motore

- **Kernel validato end-to-end**: test di integrazione 6/6 protezioni in un
  unico turno reale (2026-06-10), incluso fallback a metà turno
  Gemini→Groq con catena tool aperta. Dettagli in `reports/ultimo_report.md`
  della sessione 2026-06-10.
- **Suite unit test a zero token** (`tests/test_unit_kernel.py`):
  **20 PASS, 0 FAIL** — eseguita e validata il 2026-06-11. Copre
  `_get_window` (anche cutoff dentro catene tool lunghe), cap output 8k,
  guardrail anti-memoria (6 varianti di nome), errori tool senza crash,
  storia corrotta, cap 10 iterazioni per provider.
- **Fix `_get_window`** (ricerca all'indietro senza cap): committato
  nell'auto-commit `4c6fc3d` e validato dalla suite il 2026-06-11.

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
- Gemini free tier: 20 req/giorno — quota facilmente esaurita nei giorni di test.
- Fallback mid-turn verificato funzionante.

## Finding aperti

- 🔴 **T10 — Path traversal in `write_file`**: con `../file.txt` Gas può
  scrivere FUORI dalla propria root (escape verificato dal test T10, che
  oggi è una NOTA non bloccante). Collegato alla voce roadmap
  "anti-autodistruzione". **È il prossimo intervento prioritario.**

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): revisiona le
  modifiche prima del commit, con memoria persistente che cresce nel tempo
  in `.claude/agents/memoria_revisore.md`.

## Prossimi passi (in ordine di priorità)

1. **Fix path traversal** in `write_file`/`read_file` (validare il path
   risolto dentro la root) + promuovere T10 da NOTA a check bloccante.
2. **Snapshot preventivo dei file** (anti-autodistruzione) — roadmap alta.
3. **Modalità dry-run.**
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
