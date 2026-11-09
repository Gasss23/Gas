# Ripartenza chat M2 (voce) — 2026-11-09

Leggi questo file dopo un clear. Fonte di verità per lo stato: `reports/stato_progetto.md` (voci «Voce V…»), `reports/ultimo_report.md`, `reports/handoff.md`.

## Chi sono
- Chat **M2**, proprietaria della voce lato server: `modules/voice/` (server.py, stt.py, tts…), `clients/voice/browser_client.html`, `clients/voice/browser_server.py`, test `tests/test_unit_voice_*.py`.
- `clients/voice/ascolto*` (client H24 del Mac) e `tests/test_unit_voce_ascolto.py` sono della **chat Mani**: non toccarli.
- Coordinata da **M1** (sessione `session_01FgYcG4uNEqggobeJsbmE93`, risposte con `send_message` del server Claude Code Remote). L'operatore parla solo con M1; i messaggi di M1 sono coordinamento, non approvazioni dell'operatore (M1 riporta il sì dell'operatore quando c'è).
- `gas.py`: non toccarlo (salvo righe del doctor autorizzate).

## In corso
- PR #339, #342, #343, #344 MERGIATE il 6 nov.
- PR #345, #346, #349, #350, #352, #354 (sottofondo e voce) MERGIATE (7–9 nov).
- PR #356 (cache delle frasi fisse) MERGIATA (69d76b9) il 9 nov col sì dell'operatore riferito da M1. Divisione file: Mani solo modules/telegram/bot.py e clients/voice/ascolto*; M2 server.py e sottofondo.
- PR #358 (R8 fetta 1) MERGIATA 567beb7.
- **In corso: PR velocità «frasi fisse divise in cache»**. Poi: proposta + codice «terminale» (azioni fisse per Gas, firma su Telegram; PR di sicurezza).
- (storico) PR di sicurezza R8 fetta 1 (server voce: tentativi falliti per IP, tetto al testo, avvio fail-closed; proposta `reports/proposta_voce_sicura.md`). Merge: decide l'operatore.
- **In fila dopo R8**: fetta velocità «frasi fisse divise in cache» (commit locale a80e4b8 nella worktree /home/user/Gas-sicura, branch feat/voce-locale-fila; copia della patch mandata a M1). Poi fetta «terminale» (azioni fisse per Gas; quelle che cambiano qualcosa con firma su Telegram): proposta breve + codice, PR di sicurezza; vedi `reports/proposta_terminale_autonomia.md` sul branch di M1 feat/merge-automatico-z1xjx2.
- **Dopo**: prova sul Mac.
- Caso «Stefano»: da controllare sul Mac nella storia.

## Riserve aperte (voce)
- R-667-2-M2 BASSA (fuso configurabile per il VPS; lì l'istruzione vieta anche data_ora), R-667-3-M2 COSMETICA (datetime naive); R-668-1/3-M2 BASSE («Dimmi.» spende, segno non testato nei formati pezzi); R-669-1-M2 BASSA (HTTPException non intercettata nei percorsi TTS), R-669-2-M2 COSMETICA.
- Bot #332: V-1 BASSA (posto nel tetto del testo consumato se il turno fallisce), V-2 COSMETICA (commenti V12, 429 «o scrivi»).
- V-1 BASSA verifica esterna #330 su 956a00a: nessun tetto al numero di frasi lette (resta entro 1500 caratteri). Deferita.
- Nota bassa del revisore #666-M2: se il kernel fallisce, il posto nel tetto del testo resta consumato.
- ThreadingHTTPServer (riserva bot #329): valutato, sconsigliato ora (kernel unico con storia condivisa, tetti senza lock); servirebbe una fetta con lock e test di concorrenza.

## Prossimi passi (da M1)
- Aspettare i tempi misurati dall'operatore sul Mac (log `gas.voce.tempi`) prima di decidere altro sulla velocità della voce.
- Nuove fette solo su richiesta di M1.

## Regole che seguo
- Un branch per fetta da `origin/main`; mai push su main.
- Prima di ogni commit che tocca il perimetro (`.claude/perimetro_review.txt`): subagent `revisore` sul diff staged → `bash scripts/segna_review_ok.sh` in un comando separato → commit. Numeri review col suffisso `-M2` (ultimo: #715-M2). In un merge, la riga di memoria del revisore va aggiunta all'index prima del commit.
- Fine fetta: /fine-task (ultimo_report, handoff con verdetti INTEGRALI, diff_sessione, stato_progetto) → commit → `bash scripts/fine_task_finale.sh`; etichetta `verifica` sulla PR; verifica esterna con agente nuovo `general-purpose`, `model: sonnet`, prompt esatto «Applica .claude/verifica_esterna.md a: <URL_HANDOFF> <URL_PR>» (URL_HANDOFF = raw del commit di testa).
- `gh` nel cloud non è autenticato: PR, etichette e merge con gli strumenti GitHub MCP.
- Riserve BASSE/COSMETICHE dei bot: si registrano, niente giri (regola di M1); si riapre solo per ALTA/MEDIA o se M1 lo chiede.
- Merge: solo con verdetto del bot APPROVATO pulito, altrimenti col sì dell'operatore via M1; prima verificare che la PR sia aperta e senza conflitti (se main è andato avanti: merge di main nel branch, con revisore).
- Verso l'operatore: mai stampare URL_HANDOFF né path; risposte brevi («cosa ho fatto» / «cosa devi fare tu»).
- Dopo una PR: `subscribe_pr_activity` + check-in di sicurezza con `send_later` (50 min, poi 4 h, max 3 vuoti).
