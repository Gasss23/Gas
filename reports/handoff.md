# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-20 — M1 — Voce: `registra_voce.py` tiene solo «Hey Jarvis» riconosciuti dal modello

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questo ramo (fix/voce-registra-solo-parola): con riserve del bot serve il «mergia» dell'operatore; lo esegue l'agente.
2. Dopo il merge, sul Mac: `git pull`, poi rifare la registrazione (`bash scripts/voce/pausa.sh`, `.venv/bin/python scripts/voce/registra_voce.py`, `bash scripts/voce/riprendi.sh`) e incollare il riepilogo.

---

## §1 SCOPE & ESITO FETTE

- **Sonda (operatore, 20-11):** le tre clip «altra stanza / camminando / di spalle» ascoltate con `afplay` erano rumori della lavastoviglie e delle pentole, non «Hey Jarvis». Il controllo era solo sul volume.
- **Fetta #810 — controllo della parola nella registrazione:** FATTA, commit 992cef9b. Review #810-M1coord APPROVATO CON RISERVE (R-810M1-1, R-810M1-2 BASSE).
- **Fetta #811 — parola tagliata all'inizio della finestra:** FATTA, commit e27c655a. Review #811-M1coord APPROVATO (R-810M1-1 chiusa).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +++
 reports/diff_sessione.md           |  22 +++++++--------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  38 ++++++++++----------------
 scripts/voce/LEGGIMI.md            |   4 +++
 scripts/voce/registra_voce.py      |  79 +++++++++++++++++++++++++++++++++++++++++++++--------
 tests/test_unit_voce_ascolto.py    |  70 ++++++++++++++++++++++++++++++++++++++++++++---
```

## §3 GIT LOG --ONELINE (sessione)

```
520e6ca4 docs(fine-task): report della correzione di registra_voce (review #810/#811-M1coord)
e27c655a fix(voce): parola tagliata all'inizio della finestra si rifà (R-810M1-1) — review #811-M1coord APPROVATO
0dad979f chore(revisore): memoria review #811 — APPROVATO
992cef9b fix(voce): registra_voce tiene solo «Hey Jarvis» riconosciuti dal modello; da lontano finestra di 6 s — review #810-M1coord APPROVATO CON RISERVE
c49d271c chore(revisore): memoria review #810 — APPROVATO CON RISERVE
(il commit di fine-task che aggiorna §2/§3 è escluso per costruzione)
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #810-M1coord (commit 992cef9b)

## VERDETTO: APPROVATO CON RISERVE

Review #810-M1coord — diff staged su fix/voce-registra-solo-parola (3 file, +118/−15). Suite `tests/test_unit_voce_ascolto.py` rieseguita: **375 passed**.

**Elementi del diff esaminati**
- `scripts/voce/registra_voce.py:371` — `MotoreOWW.misura`: `oww.reset()` a ogni clip, poi 12 blocchi di silenzio prima della clip. Rischio: punteggio sporcato dalla clip precedente o dal ciclo degli esempi (`addestra` usa poi lo stesso modello). Esito ok: anche `blocchi()` fa reset a ogni ripetizione (`scripts/voce/registra_voce.py:358`); l'indice restituito non conta il silenzio, quindi è corretto; i blocchi del microfono sono liste di int, quindi `np.asarray(..., int16)` funziona. Differenza trascurabile: in `blocchi` il silenzio davanti è di 12,5 blocchi, qui di 12.
- `scripts/voce/registra_voce.py:295` — taglio sul picco: `fine = min(len, i+1+6)`, `inizio = max(0, fine-38)`. Rischio: picco agli estremi della finestra. Esito: riserva.
  - Picco a fine finestra: ok, si tengono gli ultimi 3 s.
  - Picco nei primi blocchi: clip cortissima, fino a 7 blocchi (0,56 s) → R-810M1-1.
  - Gruppi vicini (finestra di 3 s): ora anche lì la clip si accorcia, finendo 0,5 s dopo il picco. Innocuo: in addestramento la clip viene allungata con silenzio e il punteggio ricalcolato.
- `scripts/voce/registra_voce.py:265` — ciclo delle prove. Esito: ok.
  - Un bip per prova: il conteggio torna (4 bip e 4 svuotamenti nel test esistente, `tests/test_unit_voce_ascolto.py:3534`).
  - `dorme(SEC_FRA_CLIP)` (`scripts/voce/registra_voce.py:268`) dopo ogni prova, riuscita o no, prima del bip successivo.
  - `n` aumenta solo quando si salva (`scripts/voce/registra_voce.py:271`): nomi dei file consecutivi e senza buchi; «✓ n di totale» non arriva a 15 se si salta qualcosa, ed è giusto.
  - Il `for/else` stampa «dopo 3 prove la salto» solo se nessuna prova va a segno. Cosmetico: variabile `prova` non usata.
- `scripts/voce/registra_voce.py:593` — main passa `misura=getattr(m, "misura", None)` e `soglia_parola=soglia_base`. Rischio: soglia diversa da quella dell'addestramento. Esito ok: è la stessa soglia con cui `addestra` già scartava i blocchi, quindi una clip rifiutata qui non sarebbe servita comunque. Un'eccezione di onnx dentro `misura` finisce nel `except Exception` di main: messaggio, nessun traceback né crash, ma la registrazione si chiude tutta (le clip già salvate restano).
- `tests/test_unit_voce_ascolto.py:3544` e `tests/test_unit_voce_ascolto.py:3563` — i due test nuovi (rumore scartato e saltato dopo 3 prove; finestra di 6 s e taglio sul picco) hanno verifiche precise. Esito: ok. Manca il caso del picco vicino all'inizio.

**Riserve (BASSE, da segnare in stato_progetto.md)**
- **R-810M1-1 BASSA**: picco nei primi blocchi della finestra lunga (parola cominciata prima che si aprisse) → clip di 0,56 s o poco più. In addestramento verrebbe scartata «sotto soglia», ma intanto conta come «✓» e consuma una delle 15 prese. Correzione: rifiutare con «rifallo» se il picco è troppo presto, con un test.
- **R-810M1-2 BASSA**: il messaggio dice «ogni 7,5 s», ma il ciclo vero dura di più (bip, tempo di `misura`, svuotamento). Dall'altra stanza, senza bip, la parola può cadere nella pausa e quell'audio si butta. Le 3 prove attenuano; da verificare nella prova sul Mac.

**Coerenza col progetto**: va nella direzione giusta (niente rumori addestrati come «Hey Jarvis»). Non tocca kernel, cronologia né provider. Nessuna voce del Wall of Shame: il taglio `blocchi[inizio:fine]` lavora su campioni audio, non sulla cronologia. Nota: «camminando» e «di spalle» (attesa 5 s) restano sulla finestra di 3 s, che va bene solo perché lì il bip si sente; il controllo della parola vale comunque anche per loro.

**Rischio escluso**: microfono vero e modello onnx sul Mac (tempo di `misura` per clip, punteggi reali della voce da 3 metri e dall'altra stanza rispetto alla soglia 0,25) non verificati: qui non ci sono né il microfono né openWakeWord. Mi fido della prova dichiarata con espeak (0,996 contro 0,07), senza averla rieseguita.

Memoria aggiornata con la riga #810-M1coord e una lezione nuova (ritaglio attorno a un picco: controllare anche il picco vicino all'inizio), poi `scripts/commit_memoria_revisore.sh`.

### Review #811-M1coord (commit e27c655a)

## VERDETTO: APPROVATO

Review #811-M1coord — diff staged su fix/voce-registra-solo-parola (2 file, +22/−2).

**Elementi del diff esaminati**
1. `scripts/voce/registra_voce.py:296` — picco prima di `blocchi_per(SEC_PICCO_MINIMO)` (6 blocchi): clip scartata, «tagliato all'inizio», nuova prova.
   - Rischio: indice contato sulla finestra registrata, non sul secondo di silenzio messo davanti da `misura`. In `scripts/voce/registra_voce.py:373` il silenzio passa prima di `enumerate(blocchi)`, quindi `i` parte da 0 sulla finestra.
   - Rischio: confine stretto (`<`), l'indice 6 viene accettato; il test lo copre.
   - 0,5 s invece di 32 blocchi è giusto per la finestra di 3 s dei gruppi vicini.
   - Esito: ok, R-810M1-1 chiusa.
2. `scripts/voce/registra_voce.py:266` — `prova` diventa `_prova` con `range(TENTATIVI_PAROLA)`: sempre 3 prove; «dopo %d prove la salto» usa la costante. Esito: ok.
3. `tests/test_unit_voce_ascolto.py:3590` — test nuovo: indice 1 alla prima prova (scartata), 6 alla seconda (salvata); controlla il messaggio e una sola clip salvata. Esito: ok. Rieseguito sul sorgente senza la correzione (aggiungendo solo la costante): fallisce; con la correzione passa.
4. `tests/test_unit_voce_ascolto.py:3555` — il test sul rumore usa l'indice 20 (prima 0, che con la regola nuova verrebbe scartato). Esito: ok.

**Prove eseguite**: suite voce 376 passed (rieseguita). Nessuno slicing della storia, nessun output di tool simulato; `gas.py`/`brains` non toccati.

**Cosa non ho verificato**: con una voce vera il modello potrebbe dare il picco prima di 0,5 s a chi parla subito dopo il bip (rifiuti inutili, non clip sbagliate; le 3 prove attenuano). Serve il microfono del Mac. R-810M1-2 resta aperta.

**Incidente di procedura, già sistemato**: durante la prova ho usato `git stash` / `stash pop`, che ha rimesso le modifiche come non staged; le ho rimesse in stage con `git add` sui 2 file. Lo staged è identico (2 file, +22/−2, niente non staged).

**Memoria**: aggiunta la riga #811-M1coord e una lezione (niente `stash pop` senza `--index` per provare un test sullo staged); poi `bash scripts/commit_memoria_revisore.sh`.

---

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_voce_ascolto.py`:** 373 su main d03e5bf2 → 375 (#810) → 376 passed (#811). Il test di #811 fallisce sul codice di 992cef9b (rieseguito dal revisore).
- **Prova col modello vero** (openWakeWord 0.6.0 in un venv locale): `MotoreOWW.misura` su «Hey Jarvis» di espeak → (0,996, blocco 38); su rumore casuale → 0,07.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.

## §6 STATO CI

Run della PR non ancora disponibile alla scrittura dell'handoff: il ramo si pusha col commit di fine-task che contiene questo file, e una sola run testerà l'albero di testa.

## §7 RISERVE APERTE

- **R-810M1-2 BASSA:** tempi del messaggio «ogni N secondi» quando il bip non si sente: da verificare sul Mac.
- **Non verificabile qui:** punteggi reali della voce dell'operatore da lontano col microfono del MacBook.
- **Chiusa in questa sessione:** R-810M1-1 (#811).
- **Dalle PR #382/#383 (note basse del bot):** ripiego del filtro durante l'ascolto e controllo delle cartelle sopra (#382 V-1/V-2); varianti di «Jarvis» in tutti i punti e «Dimmi.» su una variante nel seguito (#383 V-2/V-3).
