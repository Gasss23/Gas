# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 12: script a doppio escape, DOCTYPE e PI in XHTML, parser vecchi (R6)

Ramo `feat/mani-web-fetta12` da main 7af0c48 (dopo il merge di #250). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #252: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; chiuderla bene richiede un vero costruttore HTML5 (es. lexbor): decidi tu.
3. Sul Mac e sulla VPS, dalla cartella di Gas: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` deve dire True (se dice False Gas lo scrive ora anche in gas_debug.log).
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-454-2 (doppio escape negli script)**: `FATTA`.
- **R-453-2 (chat Mani) (PI e DOCTYPE in XHTML)**: `FATTA`, con **B-482-1** e **B-483-1** (ALTE, trovate dal revisore nelle prime due versioni del DOCTYPE): `FATTA`.
- **V-2 ve #242 (commenti vuoti su 3.11)**: `FATTA`.
- **R-466-1, R-466-2, R-ve245b-4 (parser vecchi: rilevatore provato, avviso nel log, test saltati invece che rossi)**: `FATTA`.
- **R-482-1 (test della posizione dalla fine)**: `FATTA`.
- **Bot #252 e verifica esterna #252 su 3cea14e: BOCCIATO.** V-1 MEDIA (testo dopo un DOCTYPE con `<script>` in un letterale): `FATTA`. V-2 bot / V-5 ve COSMETICA (avviso non atomico): `FATTA`. V-3 ve BASSA (test per 5 mutanti) e R-485-1: `FATTA`. V-4 ve (conflitto con main): merge di main `FATTA`. V-6 ve COSMETICA: `FATTA`. V-2 ve BASSA preesistente (XHTML malformato letto come HTML): registrata come **R-ve252-2**, da decidere.
- **Bot #252 su 3c0be94: APPROVATO CON RISERVE** (solo COSMETICHE: descrizione della PR aggiornata; Event+Lock, nota aperta). **Seconda verifica esterna #252: APPROVATO CON RISERVE**: V-1 BASSA (PI senza nome XML in XHTML non valido faceva uscire testo): `FATTA`, con B-488-1 dal revisore; V-2 BASSA (test di `<scripts>`): `FATTA`; V-3 COSMETICA: tenuta.
- **Test**: web suite 321 → 375 (Python 3.13 e 3.11; col parser vecchio 367 passati e 9 saltati apposta). Fuzz e enumerazione con oracolo lexbor: 0 regressioni; mutazioni elencate tutte prese.
- **Review**: #482 BOCCIATO, #483 BOCCIATO, #484 APPROVATO, #485 APPROVATO CON RISERVE, #486 APPROVATO, #487 APPROVATO (merge di main), #488 BOCCIATO, #489 APPROVATO (chat Mani): verdetti integrali nell'handoff.

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…12»).
