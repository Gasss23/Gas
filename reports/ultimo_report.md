# Report — Aggiornamento roadmap.md al 2026-09-21

**Data:** 2026-09-21  
**Tipo task:** doc-only (nessuna modifica a motore/codice/test)  
**Branch:** main (doc-only, PR obbligatoria da main-lock)

---

## Esito

✅ **FATTO** — `reports/roadmap.md` aggiornato allo stato reale di oggi.

---

## Fatti applicati (confermati dall'operatore)

1. **FASE 3 VOCE = ✅ COMPLETATA** — pipeline mic→STT Groq Whisper→kernel→TTS ElevenLabs→audio; fette 1+2+3+4a+4b tutte su main; attestazione voce umana reale (2026-08-22); client browser HTML5 fetta 4b mergiato su main (PR #90, 2026-09-15). La sezione era ancora marcata come "futura" — corretta.

2. **FASE 5 = 🔴 RESET** — VPS Hetzner PERSO il 2026-09-14 per mancato pagamento. Dati `.gas_memory.db` / `.gas_history.json` / `.env.prod` cancellati irrevocabilmente. S1/S1b eseguiti sul vecchio VPS non più validi. Sezione aggiornata da "IN CORSO" a "RESET". Aggiunta lezione VPS in §Trasversali OBBLIGATORI (backup off-server + pagamento blindato + 2FA, obbligatori dal giorno 1 del prossimo deploy).

3. **FASE 4.5 = prossimo grande lavoro** — Primo mattone dell'"Orchestratore / Direttore". Nota architetturale aggiunta: dipendeva da "FASE 5 + systemd"; con VPS perso va ripensato IN LOCALE sul Mac (launchd/cron).

4. **Ordine operatore (2026-09-14, aggiornato 2026-09-21)** — registrato in cima a §PROSSIMI PASSI sia in roadmap.md sia in stato_progetto.md:
   1. voce 4b ✅
   2. GAS risponde SEMPRE in italiano ← **PROSSIMO IMMEDIATO**
   3. auto-apprendimento / auto-sviluppo
   4. motore marketing (tra gli ultimi)
   VPS rimandato.

5. **Trasversali OBBLIGATORI pre-deploy** — nuova sezione in roadmap.md §PROSSIMI PASSI: backup off-server automatico + pagamento server blindato + rotazione ElevenLabs + privatizzare repo + disciplina spesa token.

6. **Header** — aggiunta riga `> Fonte unica autorevole della roadmap. Ultimo aggiornamento: 2026-09-21.` in cima al file.

---

## File modificati

| File | Tipo modifica |
|---|---|
| `reports/roadmap.md` | Aggiornamento contenuto (fatti operatore 2026-09-21) |
| `reports/stato_progetto.md` | Aggiornamento riga "Ultimo aggiornamento" + sezione §Prossimi passi |
| `reports/ultimo_report.md` | Questo file |

**Nessuna modifica a:** `gas.py`, `brains/`, `modules/`, `tests/`, hook, CI.

---

## Note per sessioni future

- Il **prossimo task immediato** per il motore è: far rispondere GAS sempre in italiano (fetta piccola, system prompt / gas_identity.md).
- FASE 4.5 va riprogettata per Mac locale prima di qualsiasi implementazione.
- Il prossimo VPS andrà blindato dal giorno 1: backup off-server + pagamento attivo sono prerequisiti non negoziabili (lezione perdita 2026-09-14).
