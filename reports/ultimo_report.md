# ULTIMO REPORT — R7 fetta 2: ripresa al boot del compito in sottofondo

**Data:** 23 novembre 2026
**Branch:** claude/r7-ripresa-al-boot (sotto-chat di M1)

## DECISIONI UMANE RICHIESTE

1. **Merge della PR #398** (vedi handoff §0): tocca il motore; merge autonomo solo con verdetto del bot APPROVATO pulito, altrimenti decide l'operatore.
2. **(Facoltativo) Installare il servizio di ripresa al boot sul Mac**: sostituire `TUO_UTENTE` in `scripts/sottofondo/com.gas.sottofondo.plist`, poi `cp ~/Gas/scripts/sottofondo/com.gas.sottofondo.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.gas.sottofondo.plist`. Serve `~/Gas/.venv`.

## Esito fette

- **Fetta 2 R7 — ripresa al boot**: FATTA. `riprendi_al_boot` in `modules/sottofondo/__init__.py` (riusa `controlla`: stessi guardrail della fetta 1; nel terminale solo id e stato), comando `python gas.py sottofondo-riprendi`, plist launchd (solo RunAtLoad, AbandonProcessGroup, pretende `.venv`), `scripts/sottofondo/` nel perimetro di review, 8 test nuovi (121 in `tests/test_unit_sottofondo.py`). Review #839 e #840 APPROVATO CON RISERVE; chiuse R-839-1 e R-839-2.
- **Fetta 3 R7 — lista dei lavori ricorrenti con stato**: DEFERITA — prossima PR.
- **Fetta 4 R7 — tetti di tempo duri**: DEFERITA — dopo la 3.
- **Fetta 5 R7 — piano scritto dal modello**: DEFERITA — dopo la 4.

## Anomalie / cose da sapere

- La suite completa `pytest tests/` in locale non è arrivata in fondo (fermata dopo ~5 minuti); la CI esegue le suite per file. Eseguite in locale: `tests/test_unit_sottofondo.py` (121 passati) e `tests/test_unit_kernel.py` (esito nel §5 dell'handoff).
- Launchd non provato dal vero (ambiente Linux): solo plist valido e comando simulato in bash.
- Letta `reports/bacheca.md`: niente che blocchi questa fetta, niente da aggiungere.
