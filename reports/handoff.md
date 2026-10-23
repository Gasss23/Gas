# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-23 — Chat Mani, fetta 14: tempo riservato alla pulizia, grezzi autochiusi conformi (R6)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta 14: solo con verdetto del bot APPROVATO puro sull'head finale e CI verde, oppure con il tuo ok.
2. **R-ve252-2 e R-ve255-1 (BASSE, XHTML malformato)**: estendere «il resto della pagina se ne va» a tutto l'XHTML malformato (più sicuro, si perde testo)? Decidi tu.
3. **R-ve246-5 (MEDIA, già presente)**: canvas/object con elementi speciali; serve un vero costruttore HTML5 (es. lexbor): decidi tu.
4. Rete più corta: i siti lenti ora vanno in timeout a 12 s invece che a 15 (per tenere il totale nei 15 s). Se preferisci 15 s di rete e un totale fino a ~18 s, dimmelo.
5. Decisione aperta dell'altra chat (R2, A/B): vedi `reports/stato_progetto.md` e `reports/r2_regole_abbonamento.md` (V-3 bot #255).
6. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.

---

## §1 SCOPE & ESITO FETTE

- **R-ve235-5** (pulizia fuori dai 15 s): `FATTA`
- **R-496-1, R-496-2** (dalla review #496): `FATTA`
- **R-447-1 parte (b)**: chiusa come conforme
- **V-2 bot #255 bis**: `FATTA`
- **R-ve255-1**: registrata

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 +
 modules/web/leggi.py               |  17 ++-
 reports/diff_sessione.md           |  18 +--
 reports/handoff.md                 | 278 +++++++++++++------------------------
 reports/stato_progetto.md          |   2 +
 reports/ultimo_report.md           |  29 ++--
 tests/test_unit_web_leggi.py       |  54 ++++++-
 7 files changed, 192 insertions(+), 208 deletions(-)
```

NB: preso dall'index con tutti i report in stage, dopo aver scritto questo handoff; solo la riga di `reports/handoff.md` può differire di poche righe, perché lo stat è dentro il file stesso.

---

## §3 GIT LOG --ONELINE (sessione)

```
3bd972f feat(web): fetta 14 — tempo riservato alla pulizia, grezzi autochiusi conformi (R6)
185216f chore(revisore): memoria review #497 — APPROVATO
973a818 chore(revisore): memoria review #496 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Due verdetti, incollati integralmente (chat Mani), tutti e due sul diff della fetta 14 committato in `3bd972f`: #496 (APPROVATO CON RISERVE) sulla prima versione, #497 (APPROVATO) con le sue riserve chiuse. Le righe citate nella #496 si riferiscono al diff di allora.

### Review #496 (chat Mani) — verdetto integrale (fetta 14, prima versione)

## VERDETTO: APPROVATO CON RISERVE

Review #496 (chat Mani), fetta 14 sul ramo feat/mani-web-fetta14 (da main b3f04d9). Il numero #496 era libero: il più alto in memoria era #495.

Le 3 modifiche sono corrette. Restano due riserve piccole: una docstring da aggiornare e un'etichetta d'errore che può ingannare.

**Cosa ho esaminato**
- `modules/web/leggi.py:1398` (costante a `modules/web/leggi.py:55`): la scadenza della rete diventa 15 − min(3, 15/5), cioè 12 s.
  - Rischi esaminati (quelli che chiedevi):
    - **Siti lenti**: ora vanno in timeout a 12 s invece che a 15. È il prezzo dichiarato, accettabile.
    - **Il `min(…, TIMEOUT_TOTALE/5)`**: è corretto. Con 15 s vale 3; con i tempi dei test (0,2–1 s) lascia alla rete l'80%. I test dei server lenti passano tutti (9 su 9).
    - **Il messaggio «tempo massimo superato»**: si basa sulla stessa scadenza, quindi scatta a 12 s e resta coerente.
  - In `gas.py` e `modules/` non c'è nessun chiamante di `leggi_pagina` fuori dal modulo web, quindi non c'è un altro timeout esterno con cui la nuova scadenza possa scontrarsi.
  - La pulizia della pagina (`_componi`) resta senza scadenza. I 3 s sono una tua misura, non un tetto garantito: su una VPS più lenta il totale può superare i 15 s.
- `tests/test_unit_web_leggi.py:405`: test nuovo della scadenza passata a `_scarica`.
  - Rischio esaminato: il mutante «senza riserva» che sopravvive.
  - Esito ok: in una copia isolata dà 1 FAIL. L'indice `argomenti[4]` corrisponde alla scadenza nella chiamata posizionale di `_scarica`.
- `tests/test_unit_web_leggi.py:947`: `<script/>`, `<iframe src=x />` e `<style/>` mai chiusi portano via il resto.
  - Rischio esaminato: che sia una perdita di Gas e non il comportamento dei browser.
  - Esito ok: ho rifatto la prova con lexbor e dà solo «PRIMA» in tutti e 3 i casi. R-447-1 parte b si può chiudere come «conforme».
- `tests/test_unit_web_leggi.py:1284`: le eccezioni dei thread finiscono in una lista che deve restare vuota. Chiude il punto cosmetico della #494. Ok.
- Suite web: 387 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Riserve**
- **R-496-1 COSMETICA**: la docstring del modulo (`modules/web/leggi.py:19`) dice ancora che il tempo massimo copre solo rete e download e che la pulizia viene dopo. Va aggiornata: 12 s alla rete più 3 s di riserva, e la pulizia non ha un tetto rigido.
- **R-496-2 BASSA, preesistente**: se `_componi` solleva un'eccezione dopo la scadenza della rete, il ramo generico (`modules/web/leggi.py:1423`) la riporta come «tempo massimo superato» e non come errore. Con la scadenza a 12 s questo diventa più probabile. Il motivo esatto resta comunque nel log.

**Cosa non ho verificato**
- I tempi di pulizia sulla VPS: non riproducibili qui, mi fido delle tue misure (fino a 2,9 s).
- La suite col parser vecchio (378 passed e 10 skipped).
- La tua mutazione in mut14/run.py: ho rifatto io il mutante «senza riserva».

**Memoria**: aggiunta la riga #496 con R-496-1 e R-496-2, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 973a818). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py

### Review #497 (chat Mani) — verdetto integrale (fetta 14 con le riserve della #496)

## VERDETTO: APPROVATO

Review #497 (chat Mani), fetta 14 con le due riserve della #496 sistemate. Il numero #497 era libero: il più alto in memoria era #496.

**Cosa ho esaminato**
- `modules/web/leggi.py:1414`: il flag `in_rete` si spegne subito prima di `_componi`, cioè dopo l'ultimo download e fuori dal giro dei redirect.
  - Rischio esaminato: un errore di rete o un redirect classificato come errore della pulizia.
  - Esito ok: il flag si spegne solo nel ramo senza redirect, subito prima del `return _componi(...)`. Tutti gli errori di `_scarica` e dei redirect lo trovano ancora acceso.
- `modules/web/leggi.py:1427`: nel ramo generico, a flag spento, il motivo è «errore nella pulizia della pagina (Nome)».
  - Rischi esaminati: testo della pagina o del server che finisce nel motivo, e chiamanti che leggono i testi dei motivi.
  - Esito ok:
    - nel motivo va solo il nome del tipo di eccezione, mai testo della pagina, quindi la regola del modulo («motivo scritto da qui») è rispettata;
    - il warning nel log resta com'era;
    - ho cercato con grep i testi dei motivi nei file .py: nessuno, fuori da modules/web e dai test web, li legge.
- `tests/test_unit_web_leggi.py:421`: test nuovo con `_scarica` che dorme oltre la scadenza e `_componi` che solleva un errore.
  - Rischio esaminato: il mutante «flag mai spento» che sopravvive.
  - Esito ok: in una copia isolata ho tolto lo spegnimento del flag e la suite dà 1 FAIL.
- R-496-1: la docstring del modulo ora dice 12 s su 15 alla rete e 3 s alla pulizia, e che la pulizia non ha un tetto rigido. Corretta.
- Suite web: 388 passed e 1 skipped, sia su 3.13.16 sia su 3.11.17.

**Cosa non ho verificato**
- La suite col parser vecchio (379 passed e 10 skipped).
- I tempi reali di pulizia su VPS: valgono le tue misure. La docstring ora dichiara che sono una stima, non un limite.
- Un caso residuo: un errore dentro `_valida_url` o `urljoin` mentre si seguono i redirect viene ancora chiamato «errore di rete o di protocollo». Era così anche prima e non è cambiato.

**Memoria**: aggiunta la riga #497, nessuna lezione nuova. Committata con `scripts/commit_memoria_revisore.sh` (commit 185216f). Lo stage non è stato toccato.

File:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 383 → 388 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «388 passed, 1 skipped» su Python 3.13 e 3.11; lo skip è il test d'allarme che gira solo in CI). Col html.parser non patchato di CPython 3.12.3 caricato da plugin: 379 passed, 10 skipped.
- Mutazioni in copie isolate (scratchpad/mut14/run.py): «senza riserva» 1 FAIL, «flag della pulizia mai spento» 1 FAIL.
- Tempi misurati di `_componi` su 2 MB: tag 2,6 s, svg annidati 2,9 s, div/li 2,5 s, attributi 1,0 s, XHTML 2,2 s.
- Il diff non tocca `gas.py` né altre suite.

## §6 STATO CI

- `3bd972f` e il commit di fine-task con questo handoff: run non ancora disponibili alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Restano: **R-ve252-2** e **R-ve255-1** BASSE (XHTML malformato, da decidere), **R-ve246-5** MEDIA preesistente (canvas/object, decisione sul costruttore HTML5), R-469-1, R-ve245-2…4, R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-7. Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1…14».
