# ULTIMO REPORT — 2026-10-22 — Chat Mani, fetta 9: nodo corrente dentro svg/math come i browser (R6)

Ramo `feat/mani-web-fetta9`, partito dalla fetta 8 (PR #245, non ancora mergiata: su GitHub la PR è rimasta ferma al vecchio head dopo i push del secondo giro). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. Fetta di sicurezza.

## DECISIONI UMANE RICHIESTE

1. Merge della PR #245 (chiesto dall'operatore): aspetta che GitHub sincronizzi la PR sul nuovo head e che il bot riporti; questa PR contiene anche i commit della fetta 8 finché la #245 non è mergiata.
2. Merge di questa PR: vale CLAUDE.md §10 (merge autonomo solo con APPROVATO pieno del bot), salvo richiesta esplicita dell'operatore.
3. Sul Mac e sulla VPS: `.venv/bin/python -c "import modules.web.leggi as w; print(w._PARSER_AGGIORNATO)"` (dalla cartella di Gas) deve dire True.
4. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

## Esito

- **R-463-1 (MEDIA, CDATA nei punti di integrazione)**: `FATTA` — `_Contesto` tiene il nodo corrente come il browser; CDATA vero solo se è svg/math.
- **R-450-1, V-2 ve #243 (uscita da svg/math con `<p>`, `<div>`…)**: `FATTA`.
- **R-ve245-1 (MEDIA, XHTML con prefissi)**: `FATTA` — in XHTML conta il nome locale.
- **R-456-1 (`<svg><noembed/></svg>VIS`)**: `FATTA`.
- **B-467-1, B-467-2 (ALTE, regressioni trovate dal revisore)**, **R-467-1, R-468-1 (test)**, **R-468-2 (MEDIA preesistente)**: `FATTA`.
- **R-467-2, R-469-1 (BASSE), tabelle**: `DEFERITA — registrate in stato_progetto`.
- **Test**: web suite 239 → 264 (Python 3.13 e 3.11). Fuzz con oracolo html5lib contro l'head della fetta 8: 0 fughe del ripiego, 0 casi in cui il nuovo mostra di più, salvo 2 casi con `</template>` dove html5lib sbaglia (per lo standard il template si chiude; revisore d'accordo).
- **Review**: #467 BOCCIATO, #468 e #469 (chat Mani) APPROVATO CON RISERVE.

## Anomalie

- Durante la fetta ho dovuto mettere da parte (stash) il lavoro per pushare un commit di soli report sul ramo della fetta 8: il gate di review guarda il repo principale anche per i commit fatti da un worktree. Il revisore l'ha notato nel verdetto #467; il contenuto revisionato è rimasto identico (cmp).
- Alcuni vecchi test codificavano la semantica di html.parser invece di quella dei browser: portati alla semantica dei browser (verificata con html5lib).

## RICHIESTE ALLA CHAT MOTORE

Invariate (vedi `reports/stato_progetto.md`, blocchi «Mani — fetta 1…9»): aggancio di `leggi_pagina` con al modello solo `testo`, firma a finestra contaminata, tetto di chiamate, diario senza il testo della pagina, fiducia solo nei marcatori con il codice di quella chiamata; richiesta su `scripts/bot_esito.py` (MEDIA preesistenti citate come V-x contate come nuove, blocco «Mani — fetta 7»).
