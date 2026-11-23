# ULTIMO REPORT — R7 fetta 2: ripresa al boot del compito in sottofondo

**Data:** 23 novembre 2026
**Branch:** claude/r7-ripresa-al-boot (sotto-chat di M1)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #398** (il bot dà «neutral»: tocca la macchina del bot, decide l'operatore) (vedi handoff §0): tocca il motore; merge autonomo solo con verdetto del bot APPROVATO pulito, altrimenti decide l'operatore. Il 1° verdetto del bot era BOCCIATO (V-1 MEDIA), corretto in questo giro.
2. **(Facoltativo) Installare il servizio di ripresa al boot sul Mac**: sostituire `TUO_UTENTE` in `scripts/sottofondo/com.gas.sottofondo.plist`, poi `cp ~/Gas/scripts/sottofondo/com.gas.sottofondo.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.gas.sottofondo.plist`. Serve `~/Gas/.venv`.

## Esito fette

- **Fetta 2 R7 — ripresa al boot**: FATTA. `riprendi_al_boot` in `modules/sottofondo/__init__.py` (riusa `controlla`: stessi guardrail della fetta 1; nel terminale solo id e stato), comando `python gas.py sottofondo-riprendi`, plist launchd (solo RunAtLoad, AbandonProcessGroup, pretende `.venv`), `scripts/sottofondo/` nel perimetro di review, 8 test nuovi (121 in `tests/test_unit_sottofondo.py`). Review #839 e #840 APPROVATO CON RISERVE; chiuse R-839-1 e R-839-2.
- **Correzioni del 1° verdetto del bot (eafdb49a, BOCCIATO)**: FATTA. V-1 MEDIA: al boot `riprendi_al_boot` aspetta la rete (tetto 120 s, `GAS_SOTTOFONDO_ATTESA_RETE`) e senza rete non tocca la coda, così il compito riparte al primo turno invece di finire «ko» per sempre; V-2 documentata; V-3 exit 1 se il riavvio non parte; commento del plist allineato. 5 test nuovi (126). Review #841 APPROVATO CON RISERVE (R-841-1 BASSA: il controllo della rete ignora il proxy; R-841-2 COSMETICA).
- **Merge di main (PR #397) nel ramo**: FATTO (4114b631), review #849-MERGE-R7 APPROVATO CON RISERVE (R-849-1 BASSA: con «Sempre Opus» serve `GAS_CLAUDE_BIN` nel `.env` se launchd non trova `claude`).
- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: FATTA nella PR #399.
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — dopo la 3.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

## Anomalie / cose da sapere

- La suite completa `pytest tests/` in locale non è arrivata in fondo (fermata dopo ~5 minuti); la CI esegue le suite per file. Eseguite in locale: `tests/test_unit_sottofondo.py` (121 passati) e `tests/test_unit_kernel.py` (esito nel §5 dell'handoff).
- Launchd non provato dal vero (ambiente Linux): solo plist valido e comando simulato in bash.
- Letta `reports/bacheca.md`: niente che blocchi questa fetta, niente da aggiungere.
