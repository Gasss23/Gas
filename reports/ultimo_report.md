# Report task: docs/migrazione-mac-2026-09-09

**Data:** 2026-09-09  
**Branch:** docs/migrazione-mac-2026-09-09  
**Tipo:** DOC-ONLY (nessuna modifica al motore)  
**Scope:** Registrazione migrazione Windows/WSL → MacBook Air M2 + 3 finding aperti

---

## Esito

COMPLETATO. Aggiornato `reports/stato_progetto.md` con:
1. Voce datata 2026-09-09 "Migrazione Windows/WSL → MacBook Air M2" nella sezione `DA FARE — sviluppo/processo`.
2. 3 finding aperti (F-mac-1, F-mac-2, F-mac-3) nella sezione `Finding aperti`.
3. Header "Ultimo aggiornamento" aggiornato a 2026-09-09.

Nessun file motore toccato (gas.py, brains/, modules/, tests/ intatti). Gate di stop rispettato.

---

## Dettaglio modifiche

### Voce migrazione aggiunta

```
### Migrazione Windows/WSL → MacBook Air M2 (2026-09-09)

Ambiente ricostruito da GitHub (main allineato a origin) + file solo-locali reimportati
da backup "kit di trasloco": .env, .gas_memory.db (+4 .bak), .gas_history.json,
.claude/settings.local.json.

Verifiche superate:
- gas doctor → GEMINI+GROQ OK (chiamate reali), memoria integra (diario 14 voci), storico 72 msg.
- pytest tests/ → 290 PASS / 5 FAIL.
- I 5 FAIL sono SOLO ambiente (run_command in bwrap): T11c2, T11e, T12a, T12c, T12e —
  su macOS bwrap non esiste, run_command è bloccato fail-closed (corretto; confermato da T13d PASS).
  Su Linux/VPS passano.

Setup: Python 3.14 (Homebrew) in venv .venv; chiavi caricate da ~/.zshrc (GAS legge da
os.environ, niente dotenv); gasmerge symlink R10 ok; Claude Code 2.1.267.

Finding aperti registrati (NON risolti ora): F-mac-1, F-mac-2, F-mac-3 — vedi §Finding aperti.
```

### Finding aperti registrati

**F-mac-1** (test-only): T11c2/T11e/T12a/T12c/T12e FAIL su macOS perché bwrap assente → devono SKIP come T13d.

**F-mac-2** (minore): `modules/memory/store.py:204` SyntaxWarning regex `\+` → usare raw string `r"\+"`.

**F-mac-3** (robustezza): `clients/voice/probe/win_mic_test.py` chiama `sys.exit(1)` all'import se manca `sounddevice` → rompe collection pytest senza target esplicito.

---

## Diff stat

```
reports/stato_progetto.md | 19 ++++++++++++++++++-
 1 file changed, 18 insertions(+), 1 deletion(-)
```

---

## Gate di stop verificato

- ✅ Nessun file motore toccato (gas.py, brains/, modules/, tests/)
- ✅ Nessun finding risolto ora (solo registrati)
- ✅ DOC-ONLY: nessuna review del revisore richiesta
- ✅ Scope rispettato al 100%
