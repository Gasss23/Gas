# Ultimo report — 2026-11-12 notte — Voce: perché «Hey Jarvis» non risponde (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (riserve solo BASSE).
2. Compromesso: con 1 blocco i falsi sui quasi-omofoni salgono da 3 a 9 su 120 frasi; le chiamate vere prese da 19 a 35 su 81. sì/no

## Esito
- **Causa trovata** (misura col modello vero hey_jarvis su voci sintetiche, reports/voce_taratura_2026-11-12.md): i 3 blocchi di fila sopra 0,7 della #371 dimezzavano le chiamate prese; la pronuncia italiana resta sopra soglia 1-2 blocchi. La soglia 0,5→0,7 non cambiava quasi nulla. Frasi comuni ~0: i falsi dei giorni scorsi venivano dalla soglia 0,35 nel .env.
- **Correzione**: predefinito 0,7 e 1 blocco; riga «quasi sentita» con i blocchi di fila sopra soglia; `scripts/voce/taratura_parola.py` per tarare sulla voce vera (nessun audio salvato).
- Review #795/#796/#797/#798-M1coord APPROVATO CON RISERVE (R-795-1 MEDIA chiusa; aperte R-795-3, R-798-1 BASSE).

## Test
tests/test_unit_voce_ascolto.py 332 → 343 passed; con voice_server 568 passed.

## Anomalie
Nessuna. Non provato sulla voce vera.
