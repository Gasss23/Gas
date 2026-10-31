# Ripartenza chat Mani (R6, «leggere il web»)

**Da incollare dopo il `/clear` (una riga sola):**

> Sei la chat Mani di Gas: leggi reports/ripartenza_mani.md e segui le istruzioni.

---

## Istruzioni per la chat Mani

Sei la chat Mani di Gas (roadmap R6, «leggere il web»).

Perimetro: lavori SOLO in modules/web/, tests/test_unit_web_*.py e, in ci.yml, solo nello step «web suite». Non toccare gas.py, brains/, gli altri modules/, clients/, scripts/, .claude/ né gli altri step di ci.yml: se serve, scrivilo in «RICHIESTE ALLA CHAT MOTORE» dentro ultimo_report.

Regole:
- Revisore prima di ogni commit nel perimetro; poi `bash scripts/segna_review_ok.sh` in una chiamata Bash separata, poi `git commit`. Numero della review = il più alto in .claude/agents/memoria_revisore.md + 1, con «(chat Mani)».
- A fine fetta /fine-task completo. Poi la verifica esterna: agente general-purpose, model sonnet, in background, prompt esatto «Applica .claude/verifica_esterna.md a: <URL_HANDOFF> <URL_PR>». Etichetta `verifica` sulla PR.
- Merge da solo SOLO con APPROVATO pulito del bot; con riserve aspetti il mio OK.
- Conflitti con main: tieni i tuoi handoff/ultimo_report/diff_sessione, unisci a mano stato_progetto, tieni le righe di tutti e due i lati in memoria_revisore. Se entrano file del perimetro da main, fai rivedere il merge al revisore.
- Gate B: almeno 2 citazioni path:riga valide per verdetto (reports/ e memoria_revisore non contano). Mai ritoccare un verdetto: chiedi al revisore di riemetterlo.
- Mai commit vuoti, rebase o force-push.
- Guidami passo passo: una cosa alla volta, risposte corte.

Prima di tutto:
1. Controlla lo stato della PR aperta della chat Mani (numero in reports/handoff.md §0): se è aperta portami il verdetto del bot; se è mergiata riparti il branch da main. Le PR #296 (fetta 25) e #298 (fetta 26) sono mergiate.
2. Leggi in reports/stato_progetto.md i blocchi «Mani — fetta 25» e «Mani — fetta 26» (Grep, non tutto il file) e reports/ultimo_report.md.
Poi portami UNA alla volta le cose aperte, nell'ordine:
   a) FATTA in fetta 22 (riserve «DA SISTEMARE» di #280; R-ve280-1 è della chat Motore, vedi b);
   b) FATTA in fetta 27 (PR #303) la parte selectolax: `selectolax==1.0.2` in requirements.txt e allarme in CI (`test_selectolax_in_ci`); resta all'operatore `GAS_WEB_LEXBOR=1` sul VPS. In CI i test lexbor non si saltano più (run 40926576413 su 67fea3d: web 622 passed, 0 skipped);
   c) FATTA in fetta 23 (scelta 3 dell'operatore) — shadow DOM dichiarativo (figli «light» di un host con <template shadowrootmode>): decisione mia;
   d) FATTA in fetta 24 — cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4 controllo di sys.platform in attivo(), R-528-3, R-526-1, R-520-4);
   e) FATTE: R-ve252-2 e R-ve255-1 (XHTML malformato) in fetta 25, le riserve rimaste in fetta 26; R-ve235-7 chiusa come accettata e tempo di rete 12 s confermato (decisioni dell'operatore del 2026-10-29). Fuori dalle decisioni non resta niente da fare da soli: chiedi all'operatore i prossimi argomenti.
   f) riserve BASSE ancora aperte della chat Mani (V-1 bot #301): R-518-1 (chat Mani) BASSA: la guardia `_nascosti_html` nelle chiusure in scope, per canvas fa perdere testo che il browser mostra (da decidere con l'oracolo); R-516-1 (chat Mani) BASSA: su una pagina a frame il titolo si perde (verso sicuro); R-ve277-5 BASSA PREESISTENTE, parte leggi.py: con la lettura di sempre escono il contenuto di riserva di video/audio, il testo di meter/progress e i figli «light» di un host shadow (con lexbor già chiusa); V-1 ve/bot #288 BASSA (adoption agency che sposta il template dichiarativo, dichiarata in `shadow()`); R-546-1 BASSA (numeri delle review doppi tra le chat). Del punto b) resta solo, all'operatore, l'accensione di lexbor sul VPS; V-3 ve #303 (selectolax 1.0.2 uscita il 2026-10-22) è da decidere dall'operatore.
   g) Dalla sessione coordinatrice M1 (2026-10-29): (c) `scripts/bot_esito.py` coi caratteri invisibili FATTA in fetta 28 (PR #305 mergiata), test dopo la terza verifica esterna in fetta 29 (PR #306 mergiata), invisibili citati dal bot come <U+XXXX> in fetta 30 (PR #309 mergiata); porte 80 e 443 in fetta 31 (PR #310 mergiata); proxy filtrante in fetta 32 (PR #312, sicurezza); dopo: la fetta del browser senza schermo (con R-585-4 e R-585-5); (b) libexpat ≥ 2.4 nel doctor resta a M1 finché il suo ponte voce non è mergiato. Ogni PR: 2 righe a M1 (numero, esito del bot) con send_message.

Note per chi riparte:
- La lettura con lexbor è nel codice (modules/web/lexbor.py) ma SPENTA: si accende solo con `GAS_WEB_LEXBOR=1`, selectolax installato e su Linux.
- Lo strumento di misura (oracolo html5lib, fuzz, corpus, tempi) è in `reports/strumenti_mani/misura_web.py`: non è un test, non gira in CI; serve `pip install html5lib selectolax==1.0.2`.
