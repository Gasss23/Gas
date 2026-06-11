# 📊 STATO PROGETTO GAS

> Fotografia viva dello stato del progetto. Aggiornata a fine di ogni task.
> Ultimo aggiornamento: **2026-06-11** (pomeriggio — fix T10 + battesimo revisore)

## Stato del motore

- **Kernel validato end-to-end**: test di integrazione 6/6 protezioni in un
  unico turno reale (2026-06-10), incluso fallback a metà turno
  Gemini→Groq con catena tool aperta.
- **Suite unit test a zero token** (`tests/test_unit_kernel.py`):
  **25 PASS, 0 FAIL** (2026-06-11). Copre `_get_window`, cap output 8k,
  guardrail anti-memoria, errori tool senza crash, storia corrotta, cap 10
  iterazioni per provider, e da oggi **5 check bloccanti anti-traversal**.
- **Fix `_get_window`** (ricerca all'indietro senza cap): revisionato
  retroattivamente dal revisore (review #1, battesimo) → **APPROVATO CON
  RISERVE**. Il vecchio cap n*2 cedeva esattamente al worst case dei
  guardrail ufficiali (10 iterazioni × 1 tool = 21 messaggi → finestra
  vuota a metà turno): rimozione giustificata e necessaria.
- **Fix T10 — path traversal BLOCCATO** (2026-06-11): nuovo helper
  `_safe_path` (`.resolve()` + `is_relative_to(self.root)`) applicato a
  `write_file` (anti-autodistruzione) e `read_file` (anti-esfiltrazione
  API key). Nega `../`, path assoluti esterni e symlink che puntano fuori
  root; rifiuto con messaggio chiaro, `logging.warning` in scatola nera,
  loop che non crasha. Review #2 pre-commit → **APPROVATO CON RISERVE**.

## Pipeline provider (paracadute)

1. `gemini-2.5-flash-lite` → 2. `gemini-2.5-flash` → 3. `groq/llama-3.3-70b-versatile`
- Gemini free tier: 20 req/giorno. Fallback mid-turn verificato funzionante.

## Finding aperti

- 🟠 **run_command bypassa il guardrail filesystem** (emerso in review #2):
  `cat <file fuori root>` esfiltra ancora; il blocco anti-traversal copre
  solo read_file/write_file. Da affrontare con sandbox/dry-run di roadmap.
- 🟡 **Nessun cap rigido sulla finestra** (emerso in review #1): dopo la
  rimozione del cap n*2, il limite è solo strutturale (ancora = ultimo
  user + cap 8k + 10 iterazioni); tool call parallele lo aggirano.
  Rimedio proposto dal revisore: `WINDOW_CHAR_CAP` a granularità di
  messaggio (compattare i content dei tool vecchi, struttura e
  tool_call_id intatti — mai slicing).
- ✅ ~~T10 path traversal~~ — **CHIUSO** il 2026-06-11 (vedi sopra).

## Istituzioni di processo (attive dal 2026-06-11)

- **A — `reports/stato_progetto.md`**: questo file, aggiornato a fine task.
- **B — `reports/diff_sessione.md`**: riepilogo del diff a fine sessione.
- **C — Subagent revisore** (`.claude/agents/revisore.md`): **operativo, 2
  review ufficiali completate**, 6 lezioni accumulate in
  `.claude/agents/memoria_revisore.md`. Nota tecnica: il tipo `revisore`
  non è ancora registrato dall'harness (creato a sessione in corso, serve
  riavvio); finché non lo è, si invoca via agente general-purpose che
  carica e segue revisore.md — protocollo identico.

## Prossimi passi (in ordine di priorità)

1. **Snapshot preventivo dei file** (anti-autodistruzione) — roadmap alta.
2. **Modalità dry-run / sandbox per run_command** — copre anche il finding
   🟠 del bypass shell.
3. **WINDOW_CHAR_CAP** sulla finestra (rimedio proposto in review #1).
4. Valutare cap output dedicato (più alto) per la futura pipeline Whisper.
