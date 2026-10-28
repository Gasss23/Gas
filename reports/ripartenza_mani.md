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
1. Controlla lo stato della PR #285 (fetta 22): se è aperta portami il verdetto del bot e della verifica esterna; se è mergiata riparti il branch da main.
2. Leggi in reports/stato_progetto.md i blocchi «Mani — fetta 21» e «Mani — fetta 22» (Grep, non tutto il file) e reports/ultimo_report.md.
Poi portami UNA alla volta le cose aperte, nell'ordine:
   a) FATTA in fetta 22 (riserve «DA SISTEMARE» di #280; R-ve280-1 è della chat Motore, vedi b);
   b) accensione della lettura con lexbor: la fa la chat Motore (selectolax==1.0.2 in requirements-dev.txt e requirements.txt, GAS_WEB_LEXBOR=1 sul VPS); controlla se è già fatta e, se sì, verifica che in CI i test lexbor non siano più saltati;
   c) shadow DOM dichiarativo (figli «light» di un host con <template shadowrootmode>): decisione mia;
   d) cosmetiche aperte (R-ve277-3 con R-529-1, R-ve277-4 controllo di sys.platform in attivo(), R-528-3, R-526-1, R-520-4);
   e) decisioni vecchie: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

Note per chi riparte:
- La lettura con lexbor è nel codice (modules/web/lexbor.py) ma SPENTA: si accende solo con `GAS_WEB_LEXBOR=1`, selectolax installato e su Linux.
- Lo strumento di misura (oracolo html5lib, fuzz, corpus, tempi) è in `reports/strumenti_mani/misura_web.py`: non è un test, non gira in CI; serve `pip install html5lib selectolax==1.0.2`.
