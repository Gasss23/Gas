# ULTIMO REPORT — 2026-10-21 — Chat Mani, fetta 2: `leggi_pagina` più robusta (R6, PR #237)

Ramo `feat/mani-web-fetta2` (da main dopo il merge di #235, poi merge di main). Area della chat Mani: `modules/web/`, `tests/test_unit_web_*.py`. PR #237 (https://github.com/Gasss23/Gas/pull/237). Fetta di sicurezza. Operatore: «procedi con la prossima fetta Mani», «mergia quando il bot approva».

## DECISIONI UMANE RICHIESTE

1. Merge della PR #237: su richiesta dell'operatore l'agente la mergia quando il bot approva (check `verifica-bot` success, nessuna riserva ALTA/MEDIA); la PR non tocca `ci.yml`.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani): decisione dell'operatore.

## Esito

- **Riferimenti numerici enormi (R-ve235-4)**: `FATTA` — `&#` + migliaia di cifre diventano U+FFFD (zeri iniziali tolti prima); se html.parser solleva comunque, ripiego senza parser con una regex lineare.
- **Thread del DNS (R-ve235-7)**: `FATTA` — al massimo 4 risoluzioni vive (semaforo rilasciato solo quando la risoluzione finisce davvero).
- **Cane da guardia (R-393-1, R-393-2)**: `FATTA` — la copia del descrittore si chiude sempre, anche se il costruttore fallisce a metà; test.
- **Finti marcatori (R-392-3)**: `FATTA` in parte — anche con trattini e trattini bassi; separatori a tetto dopo la B-409-1. La difesa vera resta il codice casuale.
- **Test mancanti (R-ve235-6)**: `FATTA` — certificato autofirmato rifiutato sul percorso vero (`_tls=None`) e accettato con la sua CA, tetto redirect, timeout di connessione, primo IP.
- **Docstring (R-408-2, R-ve235-5)**: `FATTA` — divieto di downgrade e limiti dichiarati.
- **Test**: web suite 85 → 96 passed (Python 3.13 e 3.11, anche con rete e DNS veri bloccati); mutazioni sui test nuovi tutte prese.
- **Review**: #409 (chat Mani) BOCCIATO (B-409-1 ALTA: la regex nuova dei finti marcatori era quadratica, 40k trattini = 27 s, 2 MB = ore; R-409-2 MEDIA: tre test che non mordevano; R-409-3 BASSA) → corretti; #410 (chat Mani) APPROVATO CON RISERVE (R-410-1 BASSA, R-410-2 COSMETICA); #428 (chat Mani, merge di main) APPROVATO.
- **Allineamenti chiesti dalla verifica esterna #235 (V-3/V-4)**: `FATTA` per lo stato (85/96 test); l'handoff di questa fetta dichiara i commit intermedi.

## Anomalie

- Nessuna. I numeri delle review #409/#410 coincidono con quelli della chat Motore: distinti dal suffisso «(chat Mani)».

## RICHIESTE ALLA CHAT MOTORE

Invariate dalla fetta 1 (PR #235): aggancio di `leggi_pagina` come strumento (al modello solo `testo`; a finestra contaminata `leggi_pagina` va alla firma; tetto di chiamate per turno e per notte; diario con URL ed esito, mai il testo; il modello si fida solo dei marcatori con il codice di quella chiamata). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1» e «Mani — fetta 2».
