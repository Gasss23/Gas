# ULTIMO REPORT — 2026-10-14 — D3: altri nomi di credenziali vietati (gate)

## DECISIONI UMANE RICHIESTE

1. Merge della PR #202 (tocca il cancello: il bot darà riserve o neutral → decide l'operatore).
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai col link della PR #202.

## Esito

- **Fornitori senza estensione** — FATTA: bot_token, auth_token, telegram_token, slack_token, mistral_key, cohere_key, oauth_token negati (lettura e scrittura, livello 3).
- **`.config/gh`** — FATTA: la cartella della CLI GitHub (hosts.yml col token) è negata confrontando i pezzi puliti del percorso (anche «.config./gh», «gh /»).
- **Password con suffisso** — FATTA (R-ve201-1, R-bot201-1): passwords_backup.txt, password_list.txt, password-prod.csv, «passwords copy.txt», «password (1).txt», password_2024.txt negati; password_reset.md, password_policy.md, passwordless.md restano leggibili.
- **Separatore ripetibile** — FATTA (R-ve201-2): `api  key`, `api__key`, `seed  phrase` negati. Anche mnemonic.json.
- **Nome intero solo sull'ultimo pezzo** — FATTA (R-bot201-3): shadow/readme.md torna leggibile; dentro keys/ e tokens/ (anche keys.bak/, keys~/) è negato tutto tranne .md/.rst/.py, quindi keys/prod.txt resta negato e keys/readme.md leggibile; .ssh/ e secrets/ restano negati.
- **R-bot201-2** (composti incollati, myapikey.txt) — SALTATA: limite del bordo sinistro, resta riserva aperta.
- **Misura su file reali** — nessun cambio di esito rispetto a origin/main (179 voci fra `git ls-files` e albero di lavoro).
- **Test** — tests/test_unit_gate.py 520 passed dopo V-1 (514 prima; con il gate di main 22 failed); pytest tests/ 1320 passed.
- **Review** — #331 APPROVATO CON RISERVE: R-331-1 (BASSA) eccesso su password_new.md, password_dev.md, slack_tokens_docs.md, accodata a R-329-3.
- **Verifica esterna #202** — APPROVATO CON RISERVE, nessuna ALTA/MEDIA ([commento](https://github.com/Gasss23/Gas/pull/202#issuecomment-6167193706)). V-1 (bot.token, telegram.token col punto) chiusa in fetta: review #332 APPROVATO CON RISERVE (R-332-1 BASSA, eccesso su auth.keys.md, bot.token.md). V-2 (suffissi password fuori lista) e V-3 (solo macOS/Windows) tracciate in stato_progetto.md.
- **Bot #202** (sullo SHA f6b3ed9) — APPROVATO CON RISERVE, tre BASSE tutte chiuse in fetta: fornitori usati da Gas (openrouter, elevenlabs, voice, claude e altri); in keys/ e tokens/ negato tutto tranne .md/.rst/.py; `.config/gh` confrontato sui pezzi puliti. Review #333 APPROVATO CON RISERVE (R-333-1 chiusa, R-333-2 BASSA eccessi), #334 APPROVATO. Test gate 540 passed, pytest tests/ 1346 passed.
- **Bot #202 sullo SHA 9f5446b** — APPROVATO CON RISERVE (neutral): V-1 (copie della cartella: keys.bak/openai) CHIUSA, con anche `daily_token` (GAS_DAILY_TOKEN, nota del bot su 2da725a); V-2 (report non allineati) corretta qui. Review #335 APPROVATO. Test gate 547 passed.
- **Riserve di #200** (bot e verifica esterna) — tracciate in stato_progetto.md come promesso.
