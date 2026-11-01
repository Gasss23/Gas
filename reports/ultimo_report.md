# ULTIMO REPORT — 2026-11-01 — Mani: browser senza schermo dentro bwrap (R6, fetta 34, chat Mani)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #316 (numero nell'handoff §0): solo con verdetto del bot APPROVATO pulito la faccio io; con riserve serve il sì dell'operatore (anche tramite M1).
2. Fetta di SICUREZZA: secondo passaggio indipendente nella chat claude.ai col link della PR.
3. Il browser resta SPENTO (`GAS_WEB_BROWSER` non impostato). Accenderlo sul VPS è una decisione dell'operatore, dopo una prova dal vero (bwrap e AppArmor del VPS, node, Playwright). Sul Mac non si accende comunque: bwrap non c'è.

## Esito
- **PR #315 (browser senza schermo)**: MERGIATA (0f02868) col sì dell'operatore.
- **Punto 4 del piano (bwrap)**: FATTA (PR #316) — namespace nuovi, nessuna capability, cartelle sensibili nascoste, proxy su socket Unix con ponte dentro il sandbox, fail-closed senza bwrap.
- **V-1 ve/bot #315 (WebSocket nei worker)**: FATTA — Worker spenti, routeWebSocket obbligatorio, test con wss sulla 443 da un worker.
- **R-594-2, R-595-1, R-595-2, R-598-1**: FATTE.
- **iframe about:blank (bot su 25ce2ef)**: FATTA — non riprodotto, ora fissato da un test.
- **Review #599 (chat Mani)**: APPROVATO CON RISERVE. R-599-1 MEDIA (socket Unix di altri raggiungibili), R-599-2 MEDIA (node in ~/bin scopriva la home), R-599-3 e R-599-4 BASSE: FATTE.
- **Review #600**: APPROVATO CON RISERVE. R-600-1/2/3 BASSE: FATTE.
- **Review #601**: APPROVATO CON RISERVE. R-601-1 e R-601-2 BASSE: DEFERITA — registrate.
- **CI su fc318cf**: ROSSA (3 test del sandbox validi solo da root); **bot**: BOCCIATO per la CI rossa. FATTA la correzione (9b6b83e). **Review #602**: BOCCIATO (saltare i collegamenti riapriva R-600-1): FATTA. **Review #603**: APPROVATO CON RISERVE; R-603-1/2/3 BASSE: DEFERITA — registrate.
- **Bot su e3a59ee**: APPROVATO CON RISERVE, CI verde. V-1 BASSA (discendenti della home ri-esposti interi): DEFERITA — prossima fetta. V-2/V-3 COSMETICHE: FATTE.
- **Verifica esterna su fc318cf**: BOCCIATO. V-1 ALTA e V-2 MEDIA (CI rossa): FATTE. V-3 MEDIA (mutanti del sandbox senza test) e V-4 BASSA (scrittura senza tetto sul disco): FATTE in 366a0d5. V-6 BASSA (/etc e /usr leggibili): DEFERITA — limite dichiarato. **Review #604**: BOCCIATO (corsa in un test): FATTA. **Review #605**: APPROVATO CON RISERVE; R-605-1/2: DEFERITA — registrate.
- **Bot su 30cd0a8**: APPROVATO CON RISERVE (V-1 descrizione: FATTA; V-2 cartelle fuori dall'elenco: DEFERITA — prossima fetta, condizione in roadmap). **Verifica esterna su 30cd0a8**: APPROVATO CON RISERVE; V-1 MEDIA a/b: FATTA (test, review #606); c/d: SALTATA — dichiarati. R-605-2: FATTA.
- **ci.yml**: SALTATA — non serviva (bwrap è già abilitato in CI prima del passo web).

## Prove
- Browser 43 test (anche da utente nobody, come il runner), proxy 72 test. Web (`python -m pytest tests/test_unit_web_*.py`): 751 passed, 2 skipped.
- Mutanti presi: 21 (vedi handoff §5).

## Anomalie
- La verifica esterna ha lasciato due cartelle di prova fuori dalla scratchpad (/home/runnerx, /data/gashome) nel container di sviluppo; la rimozione l'ha bloccata un controllo di sicurezza: restano nel container, che è temporaneo.
- Le prime prove erano da root: in CI (non root) tre test del sandbox fallivano. D'ora in poi i test del sandbox si provano anche da utente nobody.
- bwrap non era installato in questo container: installato con apt (bubblewrap 0.9.0) per le prove.
- `gh` nel cloud non è autenticato: PR, etichetta e stato della CI passano dall'integrazione GitHub.
