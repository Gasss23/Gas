# Ultimo report — 2026-11-02 — Mani, fetta 36 (R6): strumento avvisa_operatore

## DECISIONI UMANE RICHIESTE
1. Merge della PR #319 (https://github.com/Gasss23/Gas/pull/319): tocca `.github/workflows/ci.yml` (macchina del bot), quindi decide l'operatore anche con un verdetto pulito.
2. Per usare lo strumento sul VPS: `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_IDS` (già usati dal bot) e, se si vuole un tetto diverso da 5, `GAS_NOTIFICHE_GIORNO` (0 = spento).

## Esito
- **PR #317 (fetta 35)**: `FATTA` — mergiata (b472fe1) col sì dell'operatore.
- **Piano a M1** (max 10 righe): `FATTA` — approvato, con le aggiunte di M1 (UNCERTAIN nel cancello, test del cancello, gas_identity.md e prompt di riserva, conto in tutti gli elenchi e in .gitignore, passo CI).
- **Strumento `avvisa_operatore`**: `FATTA` — `modules/telegram/avviso.py` + gas.py + cancello; solo la chat dell'operatore, prefisso fisso, max 1000 caratteri, invisibili resi visibili, una per turno, tetto al giorno su file prenotato prima dell'invio, fail-closed.
- **Conto sul diario** (punto 3 del primo piano): `SALTATA — il diario in degrado restituisce [] (= zero notifiche, tetto aperto): si usa un file come per le richieste di sviluppo, con l'ok di M1`.
- **Review #611**: APPROVATO CON RISERVE; R-611-1..5 `FATTA`. **Review #612**: APPROVATO CON RISERVE; R-612-1 COSMETICA e R-612-2 BASSA `DEFERITA — registrate`.
- **Bot e verifica esterna su 3db59c2**: APPROVATO CON RISERVE (bot neutral per ci.yml). V-1 (una per turno anche alla firma), V-2 ve (testo non stringa), V-3 ve (0 = spento): `FATTA` in b1d1e45. V-2 bot COSMETICA (emoji espanse) e V-5 ve BASSA (righe finte dopo il prefisso): `DEFERITA — registrate`.
- **Review #613**: APPROVATO CON RISERVE; R-613-1..3 `FATTA`. **Review #614**: APPROVATO CON RISERVE; R-614-1 COSMETICA e R-614-2 BASSA (preesistente) `DEFERITA — registrate`.
- **Voce H24 (R8)**: codice e test scritti (43 test, 7 mutanti presi) in uno stash locale; `DEFERITA — revisione e PR dopo il merge della #319, per non mescolare le fette`.
- **Riserve basse del browser**: `DEFERITA — si chiudono quando si toccano di nuovo quei file (indicazione di M1)`.

## Anomalie
- T31g (vector store con GAS_VECTORS=1) fallisce in questo container anche su main pulito (1066 PASS, 1 FAIL): ambiente, non questa fetta.
