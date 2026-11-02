# Diff della sessione — 2026-11-02 — Mani, fetta 37 (PR #323)

Si riscrive a ogni sessione; la storia completa sta in git.

- `clients/voice/ascolto.py` (nuovo): ascolto sempre attivo, parola di attivazione locale, .env letto come il server (gas._carica_dotenv), registrazione in memoria, invio al server voce senza proxy né redirect, risposta riprodotta e cancellata, finestra di 12 s, fail-safe.
- `clients/voice/requirements-ascolto.txt` (nuovo): dipendenze solo per il Mac.
- `scripts/voce/com.gas.voce.server.plist`, `scripts/voce/com.gas.ascolto.plist` (nuovi): servizi launchd con KeepAlive.
- `scripts/voce/installa.sh`, `scripts/voce/spegni.sh` (nuovi): accendere tutto in un colpo, spegnere tutto.
- `scripts/voce/LEGGIMI.md` (nuovo): istruzioni, privacy, licenza, permesso del microfono, regolazioni.
- `tests/test_unit_voce_ascolto.py` (nuovo): 69 test.
- `.github/workflows/ci.yml`: passo che lancia i test nuovi.
- `.gitignore`: `.gas_voce/`.
- `.claude/agents/memoria_revisore.md`: righe #615, #616, #618, #621, #622.
- `reports/`: report di fine task, stato_progetto (blocco fetta 37, riserve aperte di #319), roadmap (R8 e notifica), ripartenza_mani.
