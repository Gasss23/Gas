# ULTIMO REPORT — 2026-10-08 — R-203-1: la compressione non "lava" più l'input esterno

## Riassunto

Chiuso l'ultimo buco grave noto del cancello: quando Gas comprimeva una conversazione lunga,
il testo letto da file o comandi finiva nel riassunto come se l'avesse scritto l'operatore, e il
cancello non lo vedeva più come esterno. Ora la prima riga del riassunto lo dichiara e il
cancello la legge; nel dubbio considera il riassunto esterno.

## Cosa ho fatto

1. `gas.py`: la compressione marca la prima riga del riepilogo `[CONTIENE INPUT ESTERNO]` o `[SOLO INTERNO]` (si propaga alle compressioni successive; un tool senza nome conta come esterno).
2. `gas.py`: `_finestra_e_contaminata` considera contaminato ogni riepilogo che non si dichiara `[SOLO INTERNO]` (anche quelli vecchi).
3. Test T72g: marcatori, propagazione, falsi marcatori, round-trip (scrittura in attesa di conferma dopo un riassunto esterno, eseguita dopo uno interno). Kernel 699 PASS / 0 FAIL.
4. `reports/design_cancello.md` §3a corretto.
5. Review #208 APPROVATO CON RISERVE (R-208-1/2 chiuse nella stessa PR) → #209 APPROVATO.

## Cosa NON ho fatto da solo

- Prova di `gas rifletti` con un modello vero: qui non ci sono chiavi API → la fa l'operatore sul Mac.

## Cosa devi fare tu

1. Niente per questa PR: se il bot dice sì la mergio.
2. Sul Mac: `git checkout main && git pull`, un piccolo task, `python gas.py rifletti`, poi `python gas.py lezioni approva|rifiuta <id>`; mandami l'output.
