# DIFF SESSIONE — 2026-08-13

**Branch**: `sonda/voice-endpoint`
**Scope**: Sonda fetta 0 — endpoint HTTP vocale FASE 3. Nessuna modifica al motore.

## File toccati

| File | Tipo modifica |
|------|--------------|
| `reports/ultimo_report.md` | Riscritto — report sonda fetta 0 + esito fine-task |
| `reports/handoff.md` | Scritto — dossier fine sessione |
| `reports/diff_sessione.md` | Riscritto (questo file) |
| `reports/stato_progetto.md` | Aggiornato — riga sonda fetta 0 in §FASE 3 |

## Cosa è cambiato e perché

**Sonda fetta 0** (nessun codice di produzione, nessuna modifica motore):
- Letto `gas.py:1424` — identificato `run_turn(user_prompt) -> Generator` come metodo pubblico del kernel. È un generator: emette eventi `{"type": "final"/"error"/"tool_res"}`, non ritorna direttamente una stringa.
- Letto `requirements.txt` / `requirements-dev.txt` — nessun framework server HTTP presente. Scelta: stdlib `http.server` + `socketserver.ThreadingMixIn`, zero nuove dipendenze.
- Identificato punto critico threadsafety: `self.history` mutato in-place senza lock — Opzione A (lock globale) raccomandata.
- Stop gate attivo: nessun codice endpoint scritto, tutto in attesa di conferma operatore.

## Revisore

Non invocato — nessuna modifica a gas.py, brains/, modules/, tests/. Scatterà sulla fetta 1.
