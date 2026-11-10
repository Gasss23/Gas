# Ultimo report — 2026-11-10 — chat M4: R1 «Giro notturno provato dal vero», procedura di prova

## DECISIONI UMANE RICHIESTE

1. Merge della PR #362 (solo documentazione): la mergio io se il bot dà APPROVATO pulito con CI verde; altrimenti serve il sì dell'operatore via M1.
2. Archivio della conoscenza (voce R1 «avviso knowledge_fts»): tolto dalla prova perché l'unica fonte è quella di prova, superata (V-2 bot #362 terzo giro). Va creato quando c'è una fonte vera: decide l'operatore quale.
3. L'operatore sceglie una notte e segue `reports/prova_r1_notte.md` (sera + mattina), poi manda a M1 gli output dei punti B, C, E, F.

## Esito

- **Analisi di cosa manca a R1**: `FATTA` — già provati in ottobre messaggio del mattino, bottoni di giorno, timer e giro col forte. Mancano: partenza alle 03:00 da solo, firma nata di notte approvata al mattino (24 ore), riga «Riflessione», archivio `knowledge_fts` (poi tolto dalla prova, vedi sotto).
- **Procedura `reports/prova_r1_notte.md`**: `FATTA` — comandi in riquadri per sera e mattina, tabella dei guasti. Verificato qui: il catalogo col compito `prova_firma_r1` si carica senza avvisi (`carica_catalogo`), `prove_r1/buongiorno.sh` è di livello 2 (sempre alla firma, `livello_scrittura`).
- **Correzioni al codice**: `SALTATA — non servono`: il codice per la prova c'è già.
- **Messaggio a M1**: `FATTA` — consegnato.
- **PR #362**: aperta, etichetta `verifica` messa. Bot sul commit 1bd7939: APPROVATO CON RISERVE (nessuna ALTA/MEDIA).
- **Riserve del bot #362 (V-1, V-2 BASSE; V-3, V-4 COSMETICHE)**: `FATTA` — V-1 controllo vero del forte nel doctor (non basta OK, «spento» è OK), V-2 pulizia con `rm -rf …; mv …` che rimette sempre il catalogo, V-3 mappatura CI corretta nell'handoff, V-4 chiavi di `plutil` tra virgolette.
- **Riserve del bot #362, secondo giro su 1eb30cb (V-1, V-2 BASSE)**: `FATTA` in bae139c — controllo esplicito dell'archivio `knowledge_fts` (conteggio > 0) e output atteso dell'ingest; cosa fare se il controllo del catalogo non passa. 

- **Riserve del bot #362, terzo giro su e4191a2 (V-1, V-2 BASSE; V-3 COSMETICA)**: `FATTA` — controllo B con l'ora del giro nel log del timer; archivio della conoscenza tolto dalla prova (diventa decisione dell'operatore); WARN «spento nella shell ma il .env lo accende» accettato.

## Anomalie

- `gh` nel container non è autenticato (token rifiutato): stato CI letto con gli strumenti GitHub della sessione.
