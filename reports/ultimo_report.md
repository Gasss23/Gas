# ULTIMO REPORT — 2026-10-06 — TradeGasFX, oggetto 3D sempre visibile

## Decisioni umane richieste

1. Rivedere la preview aggiornata prima di pubblicare; per modificare il sito live servono i sorgenti o l'accesso al progetto.
2. Sostituire gli esempi di testimonianza, dichiarati fittizi, con esperienze autentiche e autorizzate.
3. Verificare documenti e formulazione del servizio “fondo con garanzia”.

## Esito

- Corretto il motivo per cui l'oggetto poteva sparire: l'attributo WebGL del materiale veniva letto con tre componenti invece di una. Ora il buffer ha la dimensione corretta e il primo frame verifica che la canvas abbia disegnato pixel visibili.
- Il modello WebGL mantiene lo stile precedente: tre globi scuri lucidi, anime luminose e fasce metalliche dorate intrecciate, ricostruiti come mesh volumetriche.
- La scultura originale resta visibile fin dal caricamento come fallback: i tre render front/left/right sfumano tra loro seguendo lo scroll e una rotazione lenta; se il primo frame WebGL è vuoto, la canvas viene nascosta e il fallback continua a muoversi.
- Conservate rotazione fluida allo scroll, lieve inclinazione al puntatore e rispetto di `prefers-reduced-motion`.
- Nessuna libreria esterna. Restano invariati sfondo continuo, tre servizi, CTA WhatsApp e copy essenziale.
- La skill `.agents/skills/website-service-showcase/SKILL.md` contiene una sola nota sintetica a favore della geometria 3D reale.
- Nessun uso di Claude. Nessuna modifica al sito live; sorgenti/accesso non disponibili.
- Preview: `/Users/gas/.codex/visualizations/2026/10/04/01a10831-3402-73f0-99fd-af978a026433/tradegasfx-immersive-preview.html`.
- Non ho potuto renderizzare la preview aggiornata nel browser perché l'accesso a file locali è bloccato. La correzione è verificata per ispezione del codice; nessun test automatico eseguito.

## Anomalie

PR e CI non verificabili con GitHub CLI non autenticata e API non raggiungibile.
