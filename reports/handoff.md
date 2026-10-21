# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-21 — Chat Mani, fetta 3: note della PR #237 (R6, PR #238)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #238 (https://github.com/Gasss23/Gas/pull/238): l'operatore ha chiesto in chat «mergia quando il bot approva»; l'agente la mergia con `verifica-bot` success, CI verde e nessuna riserva ALTA/MEDIA.
2. Fetta di sicurezza: secondo passaggio nella chat claude.ai con il link della PR.
3. Porte verso host pubblici ancora libere (R6 della review #391, chat Mani).

(`gh` non autenticato nella sessione cloud: numero/URL della PR presi dall'esito reale di `create_pull_request` via MCP GitHub.)

---

## §1 SCOPE & ESITO FETTE

- **Finti marcatori con separatori lunghi (R-410-1)**: `FATTA`
- **Ripiego senza parser senza script/stili (V-2 bot #237, R-429-1)**: `FATTA`
- **Motivo del DNS saturo (V-3 bot #237)**: `FATTA`
- **Test a tempo in sottoprocesso (R-410-2, R-429-2)**: `FATTA`
- **Test dei rami difensivi, server_close (V-1 verifica esterna #237, V-4 bot #237)**: `FATTA`
- **R-ve235-5**: `DEFERITA` — limite dichiarato, non chiuso.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 modules/web/leggi.py               |  58 ++++++++++++++++++++++++++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  10 +++++-----
 reports/handoff.md                 | 222 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-------------------------------------------------------------------------------------------------------------------------------
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  29 ++++++++++++++---------------
 tests/test_unit_web_leggi.py       | 105 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------
 7 files changed, 266 insertions(+), 164 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
9cf0df0 fix(web): fetta 3 chat Mani — finti marcatori lunghi, ripiego senza script, DNS saturo, test a tempo veri
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione; anche i numeri del §2 sono presi prima di quel commit, quindi le righe di `reports/handoff.md` possono differire di poco (l'elenco dei file è esatto).

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Due verdetti, incollati integralmente: #429 (chat Mani), #430 (chat Mani).

### Review #429 (chat Mani)

## VERDETTO: APPROVATO CON RISERVE

Review #429 (chat Mani). Ho esaminato il diff staged su feat/mani-web-fetta3 (2 file: modules/web/leggi.py e tests/test_unit_web_leggi.py) dopo aver letto CLAUDE.md, reports/stato_progetto.md (sezione Mani) e la memoria del revisore. Il motore resta lineare e fail-safe. Due chiusure dichiarate però non reggono alla misura: una è un difetto nuovo, l'altra è R-410-2, che risulta ancora aperta.

**Elementi del diff esaminati**

1. `modules/web/leggi.py:77`: in `_FINTO_MARCATORE` il tetto `{0,3}` resta solo sul prefisso, dopo le parole fisse ci sono di nuovo `+` e `*`.
   - Rischio esaminato: che il ReDoS si riapra.
   - Misure su 2 MB, tutte sotto 0,66 s: «fine» seguito da 2 MB di «-»; «fine del» seguito da «_»; «contenuto web» seguito da « -»; «contenuto web non» seguito da «-»; «fine del » ripetuto; «fine-del-contenuto-web-non-» ripetuto; («fine» + 1000 «_») ripetuto; («contenuto» + 1000 «-») ripetuto; «[ -» ripetuto; spazi Unicode U+2003.
   - Le 5 forme lunghe del test sono neutralizzate.
   - Esito: ok.
2. `modules/web/leggi.py:451`: `_togli_blocchi_nascosti`.
   - Rischio esaminato: che sia quadratica.
   - Tutti i casi sotto 0,14 s: 100k blocchi `<script>x</script>`, 200k «<script» senza chiusura, 1M «<», tag maiuscoli, `<scriptx>`, `</script` senza «>», i 4 tag aperti mescolati, `<style>` + 2 MB, 250k «</scrip», 1M «<s».
   - Esito: lineare, ok.
3. `modules/web/leggi.py:456`: `basso = testo.lower()`, poi gli indici di `basso` sono usati per tagliare `testo`.
   - Esito: **riserva R-429-1 (chat Mani), BASSA.**
   - `str.lower()` non conserva la lunghezza: «İ» (U+0130) diventa 2 caratteri.
   - Riprodotto: «İ»×10 + `<p>vis</p><script>SEGRETO_JS</script>DOPO_VISIBILE` dà `'İİİİİİİİİİ vis  SE ILE'`. Parte del JS passa nel testo e il testo visibile che segue si perde. Con «İ»×40 passa tutto il contenuto dello script.
   - Non è un'escalation di sicurezza (la pagina è tutta dell'attaccante e finisce comunque dentro i marcatori NON FIDATO) e riguarda solo il ripiego. Però la garanzia scritta nella docstring («toglie script e stili») è falsa sulle pagine in turco.
   - Correzione: minuscole solo ASCII (`testo.translate(str.maketrans(string.ascii_uppercase, string.ascii_lowercase))`) più un test con «İ».
4. `modules/web/leggi.py:483`: `html_unescape` dentro il try.
   - Rischio esaminato: che sollevi o esploda.
   - Con «&#» + 5000 cifre solleva ValueError: il try lo prende e la pagina resta senza riferimenti interpretati. Comunque `modules/web/leggi.py:496` toglie già prima i riferimenti enormi.
   - «&amp;»×400k: 0,13 s. «&»+31 lettere ripetuto: 0,24 s. «&#»+4300 cifre ripetuto: 0,05 s.
   - L'ordine è giusto: `_pulisci` viene dopo l'unescape (`modules/web/leggi.py:505`), quindi «&#91;CONTENUTO WEB NON FIDATO» viene neutralizzato.
   - Esito: ok.
5. `modules/web/leggi.py:166`: il motivo «troppe risoluzioni DNS in corso: tempo massimo superato».
   - Il test lo controlla a `tests/test_unit_web_leggi.py:679`. È deterministico: il DNS lento dura 3 s, il ciclo circa 2 s.
   - Esito: ok.
6. `tests/test_unit_web_leggi.py:685`: `_entro` (un thread con `join(secondi)`).
   - Esito: **riserva R-429-2 (chat Mani), BASSA. R-410-2 NON è chiusa.**
   - Il motore delle regex di Python (`re`) tiene il blocco dell'interprete (GIL) per tutta la ricerca, quindi `join` non può tornare prima che la ricerca finisca. Misurato: `join(1)` torna dopo 15,3 s su 30k «-» con la regex quadratica.
   - Mutazione `[\s_-]*` in testa: `test_pulizia_lineare_con_tanti_trattini` (`tests/test_unit_web_leggi.py:694`) viene ucciso a 300 s. Blocca la suite esattamente come prima.
   - Correzione: un sottoprocesso con `timeout` (`subprocess` e `sys` sono già importati), oppure un input dimensionato perché la versione quadratica finisca ma superi la soglia (30k «-»: 0,005 s se lineare, circa 15 s se quadratica).
   - Lo stesso limite vale per `test_ripiego_lineare` (`tests/test_unit_web_leggi.py:700`), che passa da `re.sub`.
7. `tests/test_unit_web_leggi.py:717` e `tests/test_unit_web_leggi.py:740`: i test dei due rami difensivi.
   - Rischio esaminato: stato globale lasciato dai test.
   - I monkeypatch di `threading.Thread` e `socket.socket` sono globali ma vengono annullati (`tests/test_unit_web_leggi.py:752`, più il teardown).
   - Il semaforo è un BoundedSemaphore e i permessi vengono presi e restituiti tutti.
   - Gli ordini «dns lento → non parte» e «non parte, dns, descrittori» passano. Il DNS lento dura 3 s, meno del `join(5)`, quindi non restano permessi occupati.
   - Le mutazioni dichiarate le ho rifatte: release nell'except, `os.close`, blocchi nascosti tolti, unescape tolto. Ognuna fa fallire un test.
   - Esito: ok.
8. `tests/test_unit_web_leggi.py:168` e `tests/test_unit_web_leggi.py:789`: `server_close()` dopo `shutdown()`. Esito: ok.

**Note cosmetiche**: `<scriptx>`, `<stylesheet>` e `<template-x>` vengono trattati come blocchi, quindi si toglie troppo; senza una chiusura corrispondente si perde il resto della pagina. È la direzione innocua e vale solo nel ripiego. Al parametro `funzione` di `_entro` manca il type hint (CLAUDE.md §4).

**Test**: 104 passed su Python 3.13 (`python3 -m pytest tests/test_unit_web_leggi.py`).

**Rischi esclusi**:
- Non ho rieseguito la suite su 3.11 né con rete e DNS veri bloccati: mi baso sulla tua esecuzione.
- Non ho cercato input che oggi facciano ancora sollevare ValueError a html.parser (cioè quanto spesso si arriva davvero al ripiego): richiede uno studio della stdlib versione per versione, fuori da questo diff.
- Il comportamento su VPS non è verificato: in sviluppo non si riproduce.

**Raccomandazione**: R-429-1 e R-429-2 sono correzioni di poche righe. Conviene chiuderle in questa stessa fetta, che è di sicurezza, con una nuova review. Altrimenti vanno tracciate in reports/stato_progetto.md. In ogni caso il report non deve dire «R-410-2 chiusa».

**Memoria**: ho aggiunto la riga «#429 (chat Mani) — 2026-10-21 — APPROVATO CON RISERVE — …» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md. Contiene due lezioni: un thread con `join` non limita il tempo di una regex, quindi i test a tempo vanno in un sottoprocesso; `str.lower()` non conserva la lunghezza, quindi non si usano i suoi indici sul testo originale. Su tua istruzione NON ho committato e NON ho lanciato `scripts/commit_memoria_revisore.sh`: il file è modificato e non è in staging.

File rilevanti:
- /home/user/Gas/modules/web/leggi.py
- /home/user/Gas/tests/test_unit_web_leggi.py
- /home/user/Gas/.claude/agents/memoria_revisore.md
- sonda usata: /tmp/claude-0/-home-user-Gas/5f4d2b04-ac60-5f96-b899-73c2097e5216/scratchpad/sonda429.py

### Review #430 (chat Mani)

## VERDETTO: APPROVATO

Ri-review #430 (chat Mani) del diff STAGED sul ramo feat/mani-web-fetta3. Ho letto prima CLAUDE.md, reports/stato_progetto.md (le parti Mani/web) e la memoria del revisore (fino alla #429 compresa).

Elementi del diff esaminati:
- `modules/web/leggi.py:457`: `basso = testo.translate(_MINUSCOLE_ASCII)`. Rischio: che gli indici di `basso`, usati su `testo`, si sfasino come succedeva con `lower()` e «İ». La tabella a `modules/web/leggi.py:81` trasforma un carattere in un carattere e tocca solo A-Z, quindi la lunghezza resta uguale. Abbassare solo l'ASCII è anche il comportamento dei browser sui nomi dei tag. Ho misurato «İ»×1M più 50k blocchi: 0,30 s, quindi resta lineare. Esito: ok, **R-429-1 chiusa**.
- `tests/test_unit_web_leggi.py:712`: test con «İ»×40. Ho rifatto la mutazione «lower()» in una copia isolata: 1 FAIL. Esito: ok, il test morde.
- `tests/test_unit_web_leggi.py:688-698`: `_entro` gira in un sottoprocesso.
  1. Uccisione al timeout: in una copia isolata ho messo `[\s_-]*` in testa. Il test fallisce in 10,5 s (prima la suite si bloccava) e dopo `pgrep` non trova nessun sottoprocesso rimasto vivo. Al timeout `subprocess.run` uccide il figlio e lo aspetta.
  2. Iniezione di codice: l'f-string a `tests/test_unit_web_leggi.py:692` riceve solo costanti dei test (`repr` di stringhe letterali e interi). Nessun input esterno, nessun rischio.
  3. Modulo importato: la mutazione fallisce nella copia anche se il repo vero era intatto. Quindi il figlio importa il modulo della copia, cioè del ramo: `cwd` è la radice ricavata dal file di test e la cartella corrente viene prima di PYTHONPATH. Se in CI fosse attivo PYTHONSAFEPATH l'import fallirebbe con CalledProcessError: test rosso, mai un falso verde.
  4. CI lenta: ho misurato i carichi dei figli tra 0,09 e 0,43 s (solo l'import 0,07 s), contro una soglia di 10 s. Il margine è di circa 23 volte.

  Esito: ok, **R-429-2 chiusa e con lei R-410-2**.
- `tests/test_unit_web_leggi.py:701-709`: nuovi riempitivi («fine-», «contenuto-», «non»+50 «-») e il ripiego lineare, entrambi passati in `_entro`. Esito: ok.

Nota cosmetica (non è una riserva): `capture_output=True` a `tests/test_unit_web_leggi.py:694` nasconde lo stderr del figlio se crasha. Il test resta rosso, ma la diagnosi è più povera.

Suite: 105 passed su 3.13 in 15,3 s.

Cosa NON ho verificato: la suite su Python 3.11, perché qui `python3.11` non ha pytest (mi fido della vostra esecuzione). Non ho rifatto la prova con rete e DNS bloccati via sitecustomize. Non ho misurato i tempi su un runner CI reale: ho solo stimato il margine dai tempi in locale.

Memoria: ho aggiunto la riga «#430 (chat Mani) — 2026-10-21 — APPROVATO — …» in coda a /home/user/Gas/.claude/agents/memoria_revisore.md (ora 678 righe), senza nessuna lezione nuova. NON l'ho messa in staging né committata, come richiesto. La riga #429 era già nello staging, quindi il file ora ha una modifica non in staging da aggiungere.

---

## §5 DELTA TEST DEL MOTORE

- Web suite: 96 → 105 PASS (`python3 -m pytest tests/test_unit_web_leggi.py -q`: «105 passed», Python 3.13.16 e 3.11.17; 105 passed anche con rete e DNS veri bloccati via sitecustomize).
- Mutazioni eseguite: release nell'except tolto 1 FAIL; os.close tolto 1 FAIL; regex col tetto vecchio 1 FAIL; blocchi nascosti tolti 1 FAIL; unescape tolto 1 FAIL; motivo vecchio 1 FAIL; `[\s_-]*` in testa 1 FAIL in ~10 s; `lower()` 1 FAIL.
- Nessun altro file del motore toccato.

## §6 STATO CI

- `9cf0df0`: pushato da solo prima dell'apertura della PR; run di push non verificata in questa sessione. Sui commit intermedi `handoff-check` può essere rosso per costruzione (l'handoff si aggiorna solo nel commit di fine-task).
- Commit di fine-task con questo handoff: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Di questa fetta: nessuna nuova (R-429-1/2 chiuse nello stesso giro).
- Restano: R6 porte, R7 riepilogo CI, R-408-1, R-ve235-1 (per l'aggancio), R-392-3, R-ve235-5 e R-ve235-7 (limiti dichiarati). Dettaglio in `reports/stato_progetto.md`, blocchi «Mani — fetta 1/2/3».
