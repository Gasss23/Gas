# Ultimo report — 2026-11-02 — Mani, fetta 37 (R8): voce H24, Gas sempre in ascolto sul Mac

## DECISIONI UMANE RICHIESTE
1. Merge della PR #323 (https://github.com/Gasss23/Gas/pull/323): tocca `.github/workflows/ci.yml` (macchina del bot), quindi decide l'operatore.
2. Licenza dei modelli pronti di openWakeWord («hey_jarvis»): CC BY-NC-SA, non commerciale. Va bene per le prove, oppure si aspetta «Ehi Gas» addestrata da noi?
3. Prova sul Mac: `bash scripts/voce/installa.sh`, poi «Hey Jarvis». Se il log `.gas_voce/ascolto.log` dice «solo silenzio assoluto», il permesso del microfono sotto launchd non è passato (vedi `scripts/voce/LEGGIMI.md`).

## Esito
- **PR #319 (fetta 36, avvisa_operatore)**: `FATTA` — mergiata (ceaa4aa) col sì dell'operatore, dopo tre merge di main (PR #318, #321, #320; review #619 e #620).
- **Voce H24**: `FATTA` — `clients/voice/ascolto.py`, `scripts/voce/` (plist launchd, installa.sh, spegni.sh, LEGGIMI.md), dipendenze solo Mac, passo CI, 73 test.
- **Review #615**: BOCCIATO (installa.sh si fermava in silenzio); R-615-1/2/3/6/7 `FATTA`. **#616**: R-616-1/2/3 `FATTA`. **#618**: R-618-1/2 `FATTA` in questa PR. **#621**: APPROVATO CON RISERVE (R-621-1: memoria #615/#616/#618 portata dal branch locale, `FATTA` in 5876b7e).
- **Bot su c5e7321**: APPROVATO CON RISERVE (neutral per ci.yml). V-1 BASSA (parser del .env diverso dal server), V-2 BASSA (porta: ultima riga invece della prima; URL remoto non avvisato), V-3 COSMETICA (microfono non svuotato dopo un errore): `FATTA` in 7de4eeb. **Review #622**: APPROVATO CON RISERVE; R-622-1 BASSA, R-622-2/3 COSMETICHE `DEFERITA — registrate`.
- **Verifica esterna su c5e7321**: APPROVATO CON RISERVE (https://github.com/Gasss23/Gas/pull/323#issuecomment-6583089402). V-1/V-2/V-5 = bot (`FATTA` in 7de4eeb); V-3 BASSA (Python 3.11 e attesa del server) e V-4 BASSA (log del server): `FATTA` nel commit dopo la review #623, con R-622-1. **Bot su 1127f5c**: APPROVATO CON RISERVE (V-1 registrare V-3/V-4 ve, V-2 conteggio dei test: `FATTA`). **Review #623**: APPROVATO CON RISERVE; R-623-1 BASSA, R-623-2/3 COSMETICHE `DEFERITA — registrate`.
- **Riserve di #319 in stato_progetto**: `FATTA` (V-1 bot e V-1/V-2 ve su 9c44686).
- **R-615-4** (microfono sotto launchd) e **R-615-5** (licenza): `DEFERITA — da provare sul Mac / decide l'operatore`.
- **Piano mail**: `DEFERITA — PR doc-only subito dopo la #323 (un solo branch remoto)`.

## Anomalie
- T31g (vector store con GAS_VECTORS=1) fallisce in questo container anche su main: ambiente, non questa fetta (la suite kernel non è toccata).
