# Ultimo report — 2026-11-11 notte — Blocco esteso dei nomi: dati dei clienti mai ai cervelli gratuiti (M1)

## DECISIONI UMANE RICHIESTE
1. Merge della PR di questa sessione (blocco esteso dei nomi): riserve solo BASSE/COSMETICHE.
2. Effetto voluto della regola da confermare: anche un `ricorda` usato solo per la conoscenza caricata manda il turno al cervello forte (se il forte non c'è, il turno si chiude dichiarato). Va bene così? sì/no

## Esito
- **Finestra con dati di lead → solo il forte** (decisione dell'operatore «blocco esteso sì»): FATTA — anche a metà turno; forte assente → messaggio dichiarato, mai ai gratuiti.
- **Recap e lezioni ai non forti**: FATTA — omessi/filtrati se nominano un lead; contatti illeggibili → omessi.
- **Riflessione di fine task**: FATTA — con dati di lead solo al forte (tetto e uso registrati), altrimenti rimandata.
- **Confronto dei nomi più robusto**: FATTA — accenti (NFKD), lapidi dei lead fusi, telefoni sulle cifre, parole di 3 lettere a parola intera, anche il tipo della riga di diario; ripiego getattr (chiude R-765-1-M1coord).
- **Bot/ve #375 V-1 MEDIA (contatti illeggibili → nomi ai gratuiti)**: FATTA — fail-closed, traslitterazione, avviso del forte (96092c7e; review #767-M1coord BOCCIATO → #768-M1coord APPROVATO CON RISERVE).
- R-753-M1-A: CHIUSA. Review #766-M1coord APPROVATO CON RISERVE (R-766-1..4, BASSE/COSMETICHE).

## Test
Kernel 1135 → 1157 → 1162 PASS / 0 FAIL (T115a-e e round-trip; 18 mutanti uccisi); pytest telegram_voce+notte+sottofondo+gate+manutenzione+voice_server+voce_ascolto (-k "not browser") 1758 passed.

## Anomalie
Nessuna. Non provato: passaggio al `claude -p` vero sul Mac a metà turno.
