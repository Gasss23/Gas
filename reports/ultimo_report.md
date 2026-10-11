# ULTIMO REPORT — 2026-10-11

**Task:** (1) Gas carica il `.env` da solo all'avvio; (2) schema a 3 livelli del cancello (decisione 1A); (3) note basse rimaste (V-1/V-2 verifica esterna #179, modifiche dell'agente ai verdetti del revisore, note bot #177). Branch `feat/merge-automatico-z1xjx2`, PR #180.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #180 (https://github.com/Gasss23/Gas/pull/180): tocca la macchina di controllo (gate B, fine-task, revisore.md) → il merge lo decide l'operatore.
2. Fetta di sicurezza (cancello): secondo passaggio indipendente nella chat claude.ai con l'URL dell'handoff.
3. Messaggio Telegram del giro notturno: NON arrivato (confermato dall'operatore). Dopo il merge, sul Mac: `python3 gas.py notte` e leggere la riga «Riepilogo Telegram …» a schermo (o `grep "Riepilogo Telegram" ~/Gas/.gas_notte/launchd.log`).
4. Sul Mac: `git pull`, poi ricopiare il plist (`reports/setup_notte.md` passo 4) per avere la versione senza `source .env` e con `.venv`; facoltativo, il vecchio funziona ancora.
5. Decidere se il codice che applica il cancello (`gas.py`, `bot.py`, `modules/memory/`, `brains/`) e i gate di sviluppo restano al livello 2 o passano al livello 3 (V-2 bot / V-1 verifica esterna #180).
6. Decisione aperta dal limite dichiarato di 1A: permettere a Gas di LEGGERE `gas.py`/`brains/`/`modules/` (oggi vietato) perché il livello 2 serva anche sul codice esistente grande.

## Esito per fetta

- **Fetta 1 — `.env` caricato da Gas**: FATTA. `_carica_dotenv()` come prima riga di `main()` (`gas.py`): non sovrascrive variabili già esportate (shell, plist, systemd vincono), `export`/commenti/virgolette/BOM, nessuna espansione, warning senza valori, `GAS_NO_DOTENV=1` lo spegne (suite pytest e kernel). Plist notturno: tolto `source ./.env`, venv `.venv` poi `venv`. `reports/setup_notte.md` §2a. 10 test in `tests/test_unit_dotenv.py`. Review #260 APPROVATO CON RISERVE (R-260-1/2 chiuse, R-260-3 tracciata) → #261 APPROVATO. Commit `c6a2998`.
- **Fetta 2 — schema a 3 livelli del cancello**: FATTA. `livello_scrittura` in `modules/gate/gate.py`; livello 2 sempre alla firma con diff reale del kernel + pro/contro (max 600), scritto solo se il file risolto è quello mostrato e ha la stessa impronta; livello 3 mai; livello 1 invariato. Review #262 BOCCIATO (symlink con nome libero + finestra contaminata + impronta messa dal modello → scriveva codice senza diff) → corretto → #263 APPROVATO CON RISERVE (R-263-1, poi chiusa in fetta 3). Test T82 (kernel) + test dei livelli (gate). Commit `3e031f2`.
- **Fetta 3 — note basse**: FATTA. V-2 #179 (gate B: percorsi Windows/misti non contano come citazione), V-3 #179 (frase in revisore.md), V-1 #179 e F-verdetto-ritoccato chiuse in `stato_progetto.md` + regola in fine-task (gate B rosso → verdetto riemesso, mai ritoccato), `.gas_history.json.*` in `.gitignore`, righe lunghe in `notte.py`, R-263-1 e R-264-2 (caratteri invisibili nel messaggio di firma). Review #264 BOCCIATO (lookbehind incompleto) → #265 APPROVATO. Commit `0480996`.
- **Fetta 4 — finding del bot di verifica e della verifica esterna #180**: FATTA. verifica-bot su `0f97ba7` = failure (MEDIA: i test del `.env` non giravano in CI); verifica esterna = APPROVATO CON RISERVE. Corretti: step dotenv in CI, write_file negato su file con hard link, altri caratteri invisibili marcati, docstring, limite «codice del cancello firmabile» dichiarato in `reports/design_cancello.md` §5b. Review #266 APPROVATO. Commit `4ad0d46`.
- **Fetta 5 — messaggio Telegram non arrivato + V-6 seconda verifica esterna #180**: FATTA. Causa più probabile del messaggio mancato: `.env` non caricato → token assente (risolto in fetta 1); il motivo finiva solo in `gas_debug.log`. Ora il giro notturno stampa a schermo e in `launchd.log` «Riepilogo Telegram inviato.» / «NON inviato: <motivo>» (stampa che non può far fallire il giro). V-6: un nome di file con a-capo falsava il messaggio di firma → nomi resi su una riga e firma negata. Review #267 APPROVATO CON RISERVE → #268 APPROVATO. Commit `19b1a53`. Il bot su `55a341d`: neutral (approvato con riserve basse, decide l'operatore).
- **E2E con Telegram reale**: SALTATA — nel container non ci sono token né chiavi; resta da provare sul Mac.

## Test

pytest 865 (base) → 947 passed; `python3 tests/test_unit_kernel.py` 715 → 746 PASS, 0 FAIL.

## Anomalie

- Il revisore della #263 dichiara di aver scritto nella sua memoria numeri di riga sbagliati (gas.py:2621/1705/2812 invece di 2620/1704/2813); corretto nel verdetto, non nella memoria.
- I verdetti originali #264/#265 contenevano esempi che il gate B legge come citazioni: riemessi dal revisore e messi nel §4 dell'handoff, originali in §4b (la regola nuova di fine-task va precisata).
- `gh` nel container non è autenticato: PR creata con lo strumento GitHub collegato (`create_pull_request` → `https://github.com/Gasss23/Gas/pull/180`).
