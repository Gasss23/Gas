# ULTIMO REPORT — 2026-10-30 — Mani: gli invisibili citati dal bot come <U+XXXX> (fetta 30, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #309 (numero nell'handoff §0). Tocca la macchina del bot (workflow e suo test): il check `verifica-bot` sarà neutral e il merge lo decide l'operatore (anche tramite M1).

## Esito
- **PR #306**: MERGIATA (95be7b1) dopo due merge di main (#307 di M1, #308 di M2), review #578 e #579 APPROVATO.
- **Invisibili citati dal bot come <U+XXXX>** (via libera dell'operatore tramite M1): FATTA (PR #309). Nuova regola nel PROMPT di `.github/workflows/verifica-bot.yml`; il controllo di `bot_esito.py` resta severo.
- **Review #580 (chat Mani)**: APPROVATO CON RISERVE. R-580-1 BASSA (nessun test sulla regola): FATTA — assert in `test_schema_coerente_con_lo_script`. R-580-2 BASSA (una gravità maiuscola nuda citata nella sezione FINDING dà ancora NO): DEFERITA — limite dichiarato. **Review #581**: APPROVATO.

- **Bot su 7d57b26 (PR #309)**: APPROVATO CON RISERVE, check neutral. V-1 BASSA (l'assert non fissava «in qualunque campo»): FATTA in 0b7782a. V-2 COSMETICA («di controllo» comprende a capo e tab): FATTA — «a capo e tab restano normali».
- **Verifica esterna su 7d57b26 (https://github.com/Gasss23/Gas/pull/309#issuecomment-6523271160)**: APPROVATO CON RISERVE. V-1 BASSA (una credenziale spezzata da una citazione «<U+200B>» non era riconosciuta, e il PROMPT spinge proprio verso quella forma): FATTA in 0b7782a — _senza_citazioni in contiene_segreti. V-2 COSMETICA (R-580-2 senza test): SALTATA — limite dichiarato. V-3 COSMETICA (test del gate con -I): SALTATA — già registrata (V-2 #306).
- **Review #582 (chat Mani)**: APPROVATO CON RISERVE (R-582-1 BASSA: citazione annidata o lettera visibile citata non riconosciute; R-582-2 COSMETICA: l'assert del PROMPT a pezzi separati). Registrate in stato_progetto.

## Prove
- YAML del workflow valido, 0 caratteri Cf nel file.
- `tests/test_unit_verifica_bot.py`: 514 passed. Mutanti: regola cambiata in <U+YYYY> 1 failed; senza `_senza_citazioni` 4 failed.
- Suite completa non rilanciata: il diff tocca solo il PROMPT e un assert del test del bot.

## Anomalie
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
