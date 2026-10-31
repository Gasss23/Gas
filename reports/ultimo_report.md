# Ultimo report — 2026-10-31 — Voce V5: tetto che conta ogni richiesta parlata, guida di prova sul Mac (chat M2) — PR #314

## DECISIONI UMANE RICHIESTE

1. Merge della PR #314 (https://github.com/Gasss23/Gas/pull/314): la mergia M1 se il bot dà APPROVATO pulito; con riserve M1 chiede il sì all'operatore.
2. Prova sul Mac seguendo `reports/prova_voce_mac.md` (eco, «sì» a voce normale, TV accesa).

## Esito delle fette

- **V5.1 — R-581-2-M2** («uso» e trascrizioni vuote spendevano Groq senza contare per il tetto orario): `FATTA` — `modules/voice/server.py`: il tetto conta ogni chiamata a Groq (registrata subito prima della trascrizione); i rifiuti locali (chiave assente, audio vuoto o non valido) non contano (R-585-1-M2); oltre `GAS_VOICE_MAX_TURNI_ORA` → 429 senza Groq. Review #585-M2 APPROVATO CON RISERVE, #586-M2 APPROVATO. Test: «Forte.» → 200, trascrizione vuota → 400, terza → 429, Groq chiamato 2 volte, nessun turno; fallisce sul codice di main.
- **V5.2 — guida di prova sul Mac**: `FATTA` — `reports/prova_voce_mac.md`, una pagina in parole semplici: `.env`, avvio di server e pagina, i 3 test, cosa fare se qualcosa va storto.
- **gas.py / brains/ / ci.yml**: non toccati.

## Anomalie

- `gh` non autenticato nel cloud: PR con l'integrazione GitHub.
