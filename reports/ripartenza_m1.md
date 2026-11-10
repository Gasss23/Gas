# Ripartenza M1 (coordinamento): stato al 7 novembre 2026

## STATO AL 10/11 (dopo /clear leggi prima questo)
- **REGOLA N.1 dell'operatore (arrabbiato, 10/11):** risposte di MASSIMO 5 righe. Scrivergli solo per decisioni o risultati da provare. Niente papiri, niente cronaca.
- **Operatore 10/11: NO all'obiettivo unico.** Si lavora in parallelo su tutto, con più chat. Nuove chat: **M3** `session_01NNEhCpcBJbujHFoDPBQLgM` (R7 direttore v2, branch feat/r7-direttore-m3); **M4** `session_01NNEhCt7spryW9nfRfuFnME` (R1 giro notturno dal vero, branch feat/r1-notte-m4). Mani: voce/ascolto (#361). M2: terminale A + server voce.
- Mergiate il 9/11: #356, #357, #358 (sicurezza server voce), #359 (voce Telegram in thread), #360 se M2 l'ha chiusa (verificare).
- In corso: Mani → fetta correttiva ascolto (finestra 15 s, max 2 seguiti, eco ignorata, parola confermata su 2 frame, soglia più alta). M2 → PR terminale A (sicurezza, attende sì).
- Sul Mac (.env): GAS_VOICE_MAX_TURNI=1, GAS_ASCOLTO_SOGLIA=0.6 (mitigazione falsi «Hey Jarvis» e seguiti, 9/11 sera).
- Log dell'ascolto: ~/Gas/.gas_voce/ascolto.log (NON gas_debug.log).
- Remote Control del Mac: ancora bloccato lato prodotto.

## Chi sono e come lavoro
- Sono **M1**: l'operatore parla solo con me. Coordino le altre chat, decido con lui e gli riporto riassunti **brevissimi**.
- **Stile (richiesto più volte, con rabbia, dall'operatore):** risposte CORTE. Per le decisioni: una riga di spiegazione, poi «rispondi sì/no» oppure «A/B». Niente papiri. Comandi sempre in riquadri ``` da copiare.
- Chat attive (si raggiungono con `send_message`):
  - **M2**, «sviluppo voce»: `session_01NNEhCqH77rouMxjiz51336`. Lavora su server voce, gas.py/brains per la voce, macchina del bot (`scripts/bot_esito.py`, verifica-bot.yml). Branch: feat/voce-v12-m2.
  - **Mani**, «ascolto»: `session_01NNEhCp31GsAtPmtpTkGGRf`. Lavora su `clients/voice/ascolto*` e `scripts/voce/`. Branch: claude/peaceful-lovelace-0w2b7q (può usare un solo branch remoto).
  - La mia sessione (M1) resta la stessa anche dopo un /clear.
- **Regole di merge:**
  - APPROVATO pulito del bot → merge senza chiedere;
  - riserve BASSE/COSMETICHE → serve il sì dell'operatore, poi mergio io o la chat proprietaria;
  - ALTA/MEDIA → si corregge prima;
  - niente giri infiniti sulle BASSE: si registrano e si va avanti.
- Il «sì bot» dell'operatore copre le correzioni al lettore del bot (falsi FAILURE).
- Accesso al Mac (Remote Control): bloccato. Si lavora con comandi da copiare.

## PR del 5-7 novembre (tutte mergiate salvo dove indicato)
- #333 soglia della voce 200 · #334 ora nel prompt e voce corta · #335 «Sì, signore?» lato server · #336 interruzione con «Hey Jarvis» · #337 bot riparato (verdetto compresso) · #338 pausa.sh/riprendi.sh · #339 pausa a voce e turni di seguito · #340 «Sì, signore?» lato Mac · #342 lettore del bot (citazioni) · #343 voce rapida (finestra 6, effort low, «rispondi solo all'ultima») · #344 rifiuto di --effort più stretto.
- **#341** (Mani, finestra di 40 s e difese): SÌ dell'operatore il 7/11, rischio di ~2 s accettato. Al /clear era in fase di merge: verificare che sia mergiata.
- **#345** (M2, compiti lunghi in sottofondo con avviso Telegram): SÌ dell'operatore il 7/11. Al /clear era in fase di merge: verificare.

## Decisioni dell'operatore (valide)
- 9/11 ~10:30 UTC: sì a #356 e #357; thread voce Telegram opzione b (Mani); sicurezza server voce «scegli la sicurezza migliore» → R8 fetta 1 fail-closed, opzioni più sicure, merge se niente ALTA/MEDIA (M2); terminale opzione A sì (azioni fisse con firma a bottoni, M2 dopo R8).
- 9/11 02:10 UTC (M1): la regola notturna di merge con riserve è SOSPESA. Verifica esterna #357 V-1 MEDIA: non è scritta dall'operatore nel repo e CLAUDE.md §10 dice il contrario; il permission check di Mani ha bloccato un agente che se la scriveva. Stanotte si mergia solo APPROVATO pulito; le PR con riserve restano per l'operatore.
- 9/11 notte: sì a #355 (ElevenLabs accettato). M2 → B: server voce sicuro (sicurezza: PR aperta per l'operatore). Notte: lavoro continuo sulla voce (Jarvis completo, intelligente, veloce), poi roadmap, poi terminale/autonomia se avanza tempo. REGOLA DI MERGE NOTTURNA: solo BASSE/COSMETICHE e niente sicurezza → merge senza chiedere; sicurezza → resta per l'operatore. Test del mattino: reports/test_voce_mattina.md.
- 8/11 sera: sì a #352 (M2) e #353 (Mani, vocali Telegram fetta 1). Fetta 2 Telegram: risposta vocale SOLO se l'operatore manda un vocale. V-2 #353: chiesto all'operatore di confermare la scelta A con un suo commento sulla PR.
- 9/11: Remote Control: la cartella Gas sul MacBook-Air-di-gaspare è nella lista ma NON offerta alle sessioni cloud (not_available: app Claude da aggiornare o funzione non ancora disponibile).
- 7/11 sera: sì a #350 (M2, compiti finiti detti a voce; V-5 accettata) e #351 (Mani, fetta 45). Vocali Telegram senza «forte»: opzione A (regole dei testi Telegram, anche ai gratuiti; GAS_VOCE_FORTE vale anche lì; tetto 30/ora). Ordine merge: #350 poi #351, poi PR fetta 1 Telegram (Mani).
- 7/11 ~16:00 UTC: sì al merge di #349 (M2) e #348 (Mani); sì alla voce via Telegram, opzione B in due fette (vocale→testo, poi anche voce). Ordine merge: #349 poi #348. In coda: PR fetta 3.2 (M2, compiti finiti detti a voce) e fetta 45 (Mani, d711cc6 in locale).
- 7/11: sì al merge di #346 (M2) e #347 (Mani, se niente ALTE/MEDIE). «Hey Gas» NO: si resta con «Hey Jarvis».
- 7/11: voce «simile al film» = voce generica british/maggiordomo (NON clone dell'attore). Proposta: Daniel (premade ElevenLabs, onwK4e9ZLuTAKqWW03F9) da confrontare con George (attuale) su /voci.
- Voce: sempre in ascolto. «Hey Jarvis» attiva. Dopo una risposta la finestra dura 40 s di silenzio, poi torna in attesa. «Jarvis, pausa» chiude la conversazione. `pausa.sh` = standby profondo, `riprendi.sh` per riaccendere.
- Turni di seguito (senza parola): solo cervello forte, nessuno strumento. Il cervello decide se il parlato è rivolto a Gas; se no, silenzio e niente memoria. I seguiti rivolti a Gas vanno in memoria, e finché sono nella finestra si usa solo il forte (mai i gratuiti).
- Rischi accettati: la trascrizione Groq riceve tutto l'audio della voce; circa 2 s di stanza dopo un falso «Hey Jarvis» nella finestra.
- Niente Haiku per la voce. Niente cronologia separata: voce, Telegram e resto sono UNA sola Gas.
- Voce di Gas: NON il JARVIS del film (attore reale). L'operatore sceglierà sulla pagina /voci una voce british/calma/maggiordomo, che io metterò in ELEVENLABS_VOICE_ID.
- Accesso al terminale del Mac: per ora SOLO M1; Gas più avanti, quando sarà pronto.

## Sul Mac (.env dell'operatore)
- `GAS_ASCOLTO_VOCE_RMS=200` (ora anche di default).
- `GAS_ASCOLTO_SOGLIA=0.35` consigliata (non confermato che l'abbia messa).

## PROSSIMI PASSI
1. Verificare il merge di #341 e #345. Poi dare all'operatore il comando per aggiornare il Mac:
   `cd ~/Gas && git pull origin main && bash scripts/voce/installa.sh`
   Da provare: «Sì, signore?», la pausa a voce, la finestra di 40 s, la voce più veloce, un compito lungo con l'avviso Telegram.
2. Sul Mac, dopo l'aggiornamento: tempi `grep "tempi voce" ~/Gas/gas_debug.log | tail -10` e `claude --help | grep effort`.
3. M2: fetta piccola con le BASSE della #345 (pid riusato, «creato» non numerico, avviso al crash, ultimo avviso del giorno, «fermato», pulizia dei file, inf/nan).
4. Mani: fetta 44 (riserve dell'ascolto e `reports/proposta_parola_gas.md`), poi le BASSE della #341.
5. Parola nostra «Hey Gas» / «Jarvis»: la proposta di Mani dice Colab, circa 1 ora; licenza dei dati negativi da verificare; l'italiano non è supportato ufficialmente. Da far decidere all'operatore.

## PROMEMORIA DELL'OPERATORE (da ricordargli)
1. A fine lavoro sulla voce: provare a completare un compito della roadmap interamente a voce.
2. Accesso al terminale del Mac: problema aperto. Solo M1 per ora.
3. Scegliere la voce sulla pagina /voci.
