# ULTIMO REPORT — 2026-10-06 — TradeGasFX, ombre e resa 3D

## Decisioni umane richieste

1. Rivedere la preview aggiornata prima di qualsiasi pubblicazione; il sito live è invariato.
2. Sostituire gli esempi di testimonianza fittizi con esperienze autentiche e autorizzate.
3. Verificare documenti e formulazione del servizio “fondo con garanzia”.

## Esito

- Mantenuti i tre globi e le fasce metalliche; la rotazione e il passaggio laterale restano guidati dallo scroll. Rimossa la rotazione simulata con viste statiche.
- Aggiunta una shadow map WebGL che proietta sul fondale l'ombra aggiornata con la rotazione, con filtro PCF 3×3. Il codice prevede il fallback senza ombre se il dispositivo non supporta il framebuffer.
- Conservati i riflessi da studio, lo shading metallico GGX e Fresnel/trasmissione per il vetro. La skill `.agents/skills/website-service-showcase/SKILL.md` ora ricorda di aggiungere un'ombra proiettata per dare profondità.
- Nessun uso di Claude. Nessuna modifica al sito live e nessuna libreria esterna.
- Preview: `/Users/gas/.codex/visualizations/2026/10/04/01a10831-3402-73f0-99fd-af978a026433/tradegasfx-immersive-preview.html`.
- Verifica: controllo sintattico Node dello script inline superato. La preview locale non è stata renderizzata nel browser disponibile, quindi la nuova resa visiva non è verificata; nessun test automatico eseguito.

## Limiti aperti

Prima della pubblicazione servono una revisione visiva della preview, testimonianze reali autorizzate e verifica documentale delle condizioni del fondo.
