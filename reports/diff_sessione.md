# DIFF SESSIONE — 2026-10-06 — TradeGasFX, oggetto 3D sempre visibile

| File | Cosa è cambiato e perché |
|---|---|
| .agents/skills/website-service-showcase/SKILL.md | Skill del branch: prescrive geometria WebGL reale con profondità e luce, rilevante per questa rifinitura. |
| reports/ultimo_report.md | Esito e limiti della correzione di visibilità. |
| reports/stato_progetto.md | Fotografia aggiornata; motore GAS invariato. |
| reports/handoff.md | Dossier aggiornato con diff, log, test, review e CI. |
| reports/diff_sessione.md | Fotografia delle modifiche di questa sessione. |

La preview standalone `/Users/gas/.codex/visualizations/2026/10/04/01a10831-3402-73f0-99fd-af978a026433/tradegasfx-immersive-preview.html` corregge l'attributo buffer WebGL del materiale e controlla che il primo frame produca pixel. Il modello originale resta visibile subito come fallback: sfuma tra tre render con scroll e movimento lento. Il sito live non è stato modificato; la preview non è stata renderizzata nel browser.
