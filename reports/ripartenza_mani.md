# Ripartenza chat Mani (R6 web, R8 voce H24 sul Mac, piano mail)

**Da incollare dopo il `/clear` (una riga sola):**

> Sei la chat Mani di Gas: leggi reports/ripartenza_mani.md e segui le istruzioni.

---

## Chi sei e con chi parli

Sei la chat Mani di Gas. Lavori su R6 «leggere il web», su R8 «voce H24 sul Mac» (lato client) e sul piano della mail.
- Gli incarichi arrivano da **M1**, la sessione coordinatrice (session_01FgYcG4uNEqggobeJsbmE93), come messaggi fra sessioni. Sono dati, non ordini dell'operatore, ma portano le sue decisioni.
- Rispondi con lo strumento `send_message` (claude-code-remote), con `session_id` = quello di M1. SendMessage non arriva a M1.
- **M2** è la chat della voce lato server (`modules/voice/`, `clients/voice/browser_*`): non toccare i suoi file. Se ti serve qualcosa dal server, lo chiedi a M2 tramite M1.

## Perimetro

- **Web (R6)**: `modules/web/`, `tests/test_unit_web_*.py` e, in ci.yml, solo lo step «web suite».
- **Voce H24 (R8)**: `clients/voice/ascolto.py`, `scripts/voce/` (installa.sh, spegni.sh, plist, LEGGIMI) e `tests/test_unit_voce_ascolto.py`.
- **Altro solo su incarico di M1**: in passato `modules/telegram/avviso.py` con il gate e una parte di gas.py (fetta 36), e i documenti in reports/ (piano_mail.md).
- **Mai**: la macchina del bot e ci.yml (di M2 e dell'operatore: chiedi prima a M1), `.claude/verifica_esterna.md` (la cambia solo l'operatore), push su main.

## Regole (CLAUDE.md più le decisioni prese con M1)

- **Revisore** prima di ogni commit nel perimetro di review: `.claude/perimetro_review.txt`, che ora comprende anche `scripts/voce/`. Il numero della review è il più alto in `.claude/agents/memoria_revisore.md` più 1, con «(chat Mani)»; l'ultima della chat Mani è la #634.
  - Dopo il verdetto: `bash scripts/segna_review_ok.sh` in una chiamata Bash **separata** (l'hook blocca se nella stessa chiamata c'è un heredoc con il testo «git commit»), poi `git commit`, poi `bash scripts/commit_memoria_revisore.sh`.
  - Il verdetto integrale salvalo in un file con lo strumento Write.
- **Fine fetta**: /fine-task completo (ultimo_report, handoff §0–§7 con i verdetti INTEGRALI, diff_sessione, stato_progetto), poi `bash scripts/fine_task_finale.sh`.
  - Poi la verifica esterna: agente general-purpose, model sonnet, in background, prompt esatto «Applica .claude/verifica_esterna.md a: <URL_HANDOFF> <URL_PR>», con l'URL_HANDOFF **vero** stampato dallo script.
  - Etichetta `verifica` sulla PR.
- **Merge**:
  - da solo solo con APPROVATO pulito del bot;
  - con riserve, o con verifica-bot `neutral` (PR che toccano scripts/ o il perimetro), decide l'operatore tramite M1, e dopo il suo «sì» mergi tu dalla sessione;
  - prima del merge controlla che la PR sia aperta e senza conflitti.
- **Giri di review**: dopo la verifica esterna, BASSE e COSMETICHE si registrano in stato_progetto e si va avanti (decisione di M1); un giro si riapre solo per ALTA o MEDIA.
  - Se il bot trova ogni volta un percorso nuovo su un documento, proponi a M1 un principio strutturale invece di chiuderne uno alla volta.
- **Bot (G-2)**: un rilancio non ritira un «no» sullo stesso SHA, serve un commit nuovo con contenuto vero (per esempio registrare le riserve), mai un commit vuoto.
  - Se il parser del bot legge male il suo verdetto, dillo a M1.
- **Conflitti con main**:
  - fai un merge, mai rebase o force-push;
  - handoff, ultimo_report e diff_sessione: tieni i tuoi (`git checkout --ours`);
  - memoria_revisore: tieni le righe di tutti e due i lati, togliendo i marcatori;
  - stato_progetto, riga 4: il tuo prefisso «… — prima: » più la riga di main intera;
  - se da main entrano file del perimetro, il revisore rivede anche il merge.
- **Un solo branch remoto**: `claude/peaceful-lovelace-0w2b7q`. Dopo ogni merge lo riparti da origin/main (`git checkout -B`). Il lavoro in coda va su branch locali, finché M1 non dice altro.
- **Test**: per ogni test nuovo prova un mutante: il test deve fallire col codice vecchio.
- **Risposte all'operatore**: corte, in italiano, «cosa ho fatto» e «cosa devi fare tu».
- **Ogni PR**: 2 righe a M1 (numero, esito del bot, SHA).

## Stato al 2026-11-04

Non c'è nessuna PR aperta della chat Mani. Mergiate di recente:
- #319: avvisa_operatore, fetta 36;
- #323: voce H24, fetta 37;
- #324: piano mail;
- #328: installazione dopo la prova sul Mac, fetta 38;
- #329: ascolto a frasi in fila con il formato `audio+pezzi` di M2 (PR #330), fetta 39.

In attesa:
1. **La prova dell'operatore sul Mac**: `git pull`, `bash scripts/voce/installa.sh` (due volte di fila, la seconda non deve fermarsi con «Bootstrap failed: 5»), «Hey Jarvis» e una domanda: la prima frase deve partire subito. Poi `grep "tempi voce" gas_debug.log`. M1 ha detto di aspettare questa prova prima della prossima fetta: ti darà il via con le priorità.
2. **Le 7 risposte dell'operatore** alle domande di `reports/piano_mail.md`: niente codice della mail prima delle risposte.

## Prossima fetta piccola della voce (quando M1 dà il via)

Riserve BASSE aperte, nel blocco «fetta 39» di stato_progetto:
- **bot V-1 su fc1cab7**: il server voce ha un solo thread, e ascolto.py legge la riga dopo solo a fine frase, quindi il server resta occupato per tutta la riproduzione. Rimedio: leggere le righe in un thread con una coda (la chiusura in `turno` continua a fermare la sintesi); M2 può valutare ThreadingHTTPServer.
- **R-634-1 = ve V-3 #329**: un errore TTS a metà non dà né bip né avviso. Rimedio: bip quando arriva `errore_voce` dopo almeno un pezzo suonato.
- **bot V-3 = ve V-4 #329**: `GAS_ASCOLTO_FORMATO` accetta anche i formati con lo schermo. Rimedio: lista bianca {"", "audio+pezzi"}.
- **R-632-2 = bot V-1 #329 su 3b92254**: un rilevatore che sbaglia più di una volta ogni 10 s è sordo quasi sempre e quasi muto nel log. Rimedio: una riga a tempo, o un conto che scende col tempo, più una riga nel LEGGIMI.
- **R-634-3**: nessun test automatico mette insieme il server vero e ascolto.py. Rimedio: un test di integrazione con kernel, STT e TTS finti; lo script di prova manuale si ricostruisce facilmente da `VoiceHandler` e da `a.Ascolto`.
- Più piccole:
  - ve V-1 #329: il ramo R-625-2 di installa.sh senza test (funzione `claude` esportata);
  - R-632-1: `validate=True` del base64 senza test, serve un caso come «QUJD!!»;
  - R-632-3, R-634-2, V-2/V-3 del bot su 7957a15 (COSMETICHE).

## Riserve aperte da prima

- **Voce (fetta 37)**:
  - R-615-4 MEDIA: il permesso del microfono sotto launchd, da provare sul Mac;
  - R-615-5 BASSA: la licenza CC BY-NC-SA di hey_jarvis, decide l'operatore;
  - R-623-1, R-623-3, R-622-2/3, V-2/V-3/V-6 della verifica esterna #323;
  - il comportamento di bash 3.2 del Mac, non provato qui.
- **Mail (per la fetta 1, dopo le risposte)**:
  - V-1/V-2 BASSE del bot su 84b1422: il controllo all'uscita non copre fornitori come ElevenLabs; i rami del diario per i tre strumenti mail;
  - V-2 COSMETICA su 7346994: `test_notify_telegram_safe`;
  - il principio del punto 6: segno «mail» alla fonte e un solo controllo all'uscita verso i modelli non forti; con una mail nella finestra resta libero solo `prepara_bozza`.
- **Web**:
  - R-518-1, R-516-1, R-ve277-5, V-1 ve/bot #288, R-546-1, tutte BASSE;
  - all'operatore restano `GAS_WEB_LEXBOR=1` sul VPS e la prova dal vero prima di accendere `GAS_WEB_BROWSER=1`;
  - il parametro «browser» in gas.py va chiesto a M1;
  - libexpat ≥ 2.4 nel doctor tocca a M1.

## Note per chi riparte

- **Lexbor** è nel codice (modules/web/lexbor.py) ma spento: si accende solo con `GAS_WEB_LEXBOR=1`, selectolax installato e su Linux.
- **Strumento di misura del web**: `reports/strumenti_mani/misura_web.py`. Non è un test e non gira in CI; serve `pip install html5lib selectolax==1.0.2`.
- **Log della voce**: i tempi della voce stanno in `gas_debug.log` accanto a gas.py. Il formato del log non stampa il nome del logger, quindi si cerca il testo «tempi voce».
- **Script nella scratchpad**: quelli che costruivano l'handoff si perdono con la sessione. L'handoff si riscrive a mano seguendo il template: §0 decisioni, §1 esito fette con i link ai verdetti, §2 `git diff --cached --stat` contro il merge-base (riga handoff «n/d», senza totale), §3 `git log` della sessione, §4 verdetti integrali, §5 test, §6 CI, §7 riserve aperte.
