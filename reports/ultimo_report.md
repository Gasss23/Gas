# Ultimo report — 2026-11-24 — Revisione in più sugli script del CRM e note dei verificatori

## DECISIONI UMANE RICHIESTE
1. Merge della PR #404: tocca il file del perimetro e `scripts/`, quindi il bot dà `neutral` e il merge lo decide l'operatore.
2. Sul Mac, una volta sola dopo il merge: `cd ~/Gas && git pull && bash scripts/crm/installa.sh`; controllare che l'ultima riga dica «Copia cifrata giornaliera fuori dal Mac: ATTIVA».
3. Dalla chat Voce (#400): controllare nel `.env` del Mac che non ci sia una vecchia `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8`.

## Esito
- **Richiesta dell'operatore** («ci sta comunque una revisione in più, dato che comunque sono dati personali dei clienti e non dobbiamo fare assolutamente neanche un errore»): FATTA. `scripts/crm/` è nel perimetro di review, decisione 20 in `reports/crm/decisioni.md`. Commit d54a09ad, review #853.
- **Riserve della #853**: R-853-1 e R-853-2 (parte delle copie) FATTE in 75dbd9d9 (review #854): servizio tolto a ogni STOP dell'installer; copie locali per giorno (30 giorni più le ultime 10).
- **Merge di main (PR #401 del funnel)**: FATTO (1b61ec43), solo report; riserve della #401 in `reports/stato_progetto.md`.
- **Note dei verificatori sulla #404** (verifica esterna: APPROVATO CON RISERVE, https://github.com/Gasss23/Gas/pull/404#issuecomment-7139788043; bot su dfe8fbee: APPROVATO CON RISERVE, neutral): FATTE in 5b75c850 (review #855, #856) e nel commit di correzione delle riserve #856 (review #857).
  - V-1 verifica esterna: la copia appena fatta non si cancella mai, anche con l'orologio del Mac indietro.
  - V-1 bot: le copie fatte a mano con un nome fuori formato non contano e non si toccano.
  - R-854-1: Ctrl+C (o un'uscita qualsiasi) durante l'attesa della dashboard toglie il servizio; un secondo Ctrl+C non interrompe la pulizia; il plist si toglie prima del bootout.
  - R-853-3: test di `installa.sh` e `spegni.sh` con comandi finti (17 test).
- Bacheca: notizia per le altre chat (`scripts/crm/` nel perimetro).

## Test
- `pytest tests/test_unit_crm.py`: 151 → 170 passed. I test nuovi falliscono col codice di prima (provato) e prendono i mutanti dei trap (provati da me e dal revisore).
- `tests/test_unit_hooks.py -k "perimetro or gate"`: 128 passed (review #853). mypy pulito su `modules/crm/store.py`, `bash -n` sugli script.
- CI della PR #404 su dfe8fbee: unit-suite e handoff-check verdi.
- Non provato su un Mac vero (launchctl, Scrivania, bash 3.2).

## Riserve aperte
- R-854-2 BASSA: KeepAlive senza tetto, registro senza rotazione, nessun avviso.
- COSMETICHE #853/#854/#856 (in `reports/stato_progetto.md`).
- Dalla PR #397: R-848-2 BASSA, R-848-3 BASSA, V-3 BASSA della verifica esterna, cosmetiche #848; R-836-1 COSMETICA. R-852M-1 (voce) e riserve della #401 (funnel) in `reports/stato_progetto.md`.
