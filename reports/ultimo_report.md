# Report — Infra/Doc: handoff autonomo + gh + ci.yml + riserva openrouter
**Data:** 2026-06-24

## DECISIONI UMANE RICHIESTE

1. **gh CLI non disponibile** (né su Windows né in WSL2 — WSL2 non ha distribuzioni installate).
   Per attivare il §6 CI nell'handoff, installare gh manualmente:
   - Windows nativo: `winget install GitHub.cli`, poi `gh auth login`
   - Oppure installare WSL2 (`wsl --install Ubuntu`) e poi `sudo apt install gh` + `gh auth login`
   Finché gh è assente, il §6 CI nei futuri handoff riporterà "CI NON VERIFICATA (gh assente)".

## Fette eseguite

### FETTA 1 — gh + template handoff.md/fine-task.md
- **gh check**: assente su Windows e in WSL2 (WSL2 non installato). Decisione umana tracciata sopra.
- **.claude/commands/fine-task.md**: aggiornato template handoff.md da 6 sezioni generiche a 8 sezioni numerate (§0–§7), tutte VERBATIM. Aggiunto nel §0 la raccolta di `gh run list -L 3`. Nessun ESITO / CONTESTO libero — sostituito da §1 SCOPE (cosa chiedeva ogni prompt) + §7 RISERVE APERTE.

### FETTA 2 — .claudeignore e CLAUDE.md §11
- **.claudeignore**: già presente e completo (venv/ .venv/ __pycache__/ *.pyc *.db .gas_memory.db .gas_vectors.db *.log gas_debug.log). **SKIP**.
- **CLAUDE.md §11**: già allineato ("default Sonnet 4.6, Opus on-demand via /model opus"). **SKIP**.

### FETTA 3 — ci.yml T9a/T9c FAIL → SKIP
- Righe 117-118: rimosso "FAIL sono T9a/T9c (env API / storia su root temp) il sandbox è OK" + "renderli verdi tocca tests/ → micro-task con revisore". Sostituito con: "T9a/T9c sono SKIP in CI su assenza GEMINI/GROQ API key — non FAIL attesi."
- Riga 125 (commento Gate step): aggiornato "rosso da T9a/T9c (atteso)" → "T9a/T9c SKIP in CI (assenza API key)".
- Grep di verifica: nessun'altra occorrenza T9a/T9c con dicitura FAIL nel file.

### FETTA 4 — R-ci-openrouter in stato_progetto.md
- Aggiunta riserva 🟡 **R-ci-openrouter** in Finding aperti: "T9a fragile se OPENROUTER_API_KEY è presente: il test la poppava prima del turno T9 ma la tolleranza alla presenza di OPENROUTER non è garantita formalmente (revisore CI-4, 2026-06-24)."
- Testo esatto del revisore: "T9a è fragile se OPENROUTER_API_KEY è presente (ma il test già la poppava prima del turno T9)."

## File toccati
- `.claude/commands/fine-task.md` (template handoff §0–§7)
- `.github/workflows/ci.yml` (T9a/T9c FAIL → SKIP)
- `reports/stato_progetto.md` (R-ci-openrouter aggiunta)
- `reports/ultimo_report.md` (questo file)
- `reports/handoff.md` (dossier sessione)
- `reports/diff_sessione.md` (diff sessione)
