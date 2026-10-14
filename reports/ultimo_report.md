# ULTIMO REPORT — 2026-10-14 — riserva R-gate-nomi-1 (nomi BASSI dopo D3)

## DECISIONI UMANE RICHIESTE

1. Merge della PR di questa fetta (solo `reports/`): se il bot non dà un APPROVATO pulito, decide l'operatore.

## Esito

- **Controllo D3** — FATTA. D3 è già in main (PR #202). Sonda sul cancello di main (7ed2d18): chiusi bot/auth/telegram/slack token, `.config/gh/hosts.yml`, password con suffisso o copia, separatore ripetuto; restano leggibili i residui già tracciati in R-329-2 / R-bot201-2.
- **Riserva R-gate-nomi-1** — FATTA (decisione operatore: solo riserva, nessuna fetta per questi nomi). In `reports/stato_progetto.md`: `.bash_history`, `.zsh_history`, `.mylogin.cnf`, `login.keychain-db`, `gshadow`, `htpasswd` senza punto, `.jceks`, `.bks`, `putty.reg`, `.kdb` restano leggibili.
- **Note del bot su #203** — FATTA: V-1 (BASSA) nomi aggiunti alla riserva e lista dichiarata non esaustiva; V-2 (COSMETICA) riga spostata dopo il blocco R-329, id `R-gate-nomi-1` tenuto (riserva nata da decisione dell'operatore, non da una review).
- **Fetta per questi nomi** — SALTATA — l'operatore ha scelto solo la riserva (la D4 mergiata in #204 riguarda la scrittura in keys/, tokens/, passwd/, shadow/).

## Anomalie

- PR #203 in conflitto dopo il merge di #204 in main: il merge di main nel branch era bloccato dal gate di review (il diff in stage conteneva `gate.py` di #204), quindi rebase dei 3 commit di soli report su main e push con `--force-with-lease`.
- Note COSMETICHE del bot sul secondo passaggio #203: §6 dell'handoff riscritto con gli esiti reali; la riserva ora dice che la misura è una sonda manuale non registrata.
