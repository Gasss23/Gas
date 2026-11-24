# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Voce: modello «ehi jarvis» con accento italiano (ehi_jarvis_it)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #405 (https://github.com/Gasss23/Gas/pull/405). Il revisore ha dato APPROVATO CON RISERVE: serve il «mergia» dell'operatore, salvo verdetto pulito del bot.
2. R-854-1: col modello italiano il filtro della voce dell'operatore, legato a hey_jarvis, resta spento. `installa.sh` avvisa. Per tornare indietro: `GAS_ASCOLTO_MODELLO=hey_jarvis` nel `.env`.
3. Prova sul Mac con la voce vera, dopo `git pull` e `bash scripts/voce/installa.sh`.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Addestramento del modello **: FATTA. Lavoro nello scratchpad; nel repo vanno il modello, gli script e i risultati.
  Risultati della simulazione (1 fase, prese a vicino / −6 / −12 / −20 dB):

  | | voci della simulazione | voci mai viste | falsi/ora, parlato italiano | falsi/ora, audio generico |
  |---|---|---|---|---|
  | ehi_jarvis_it | 100 / 100 / 87 / 47% | 90 / 75 / 70 / 58% | 0,35 | 0 |
  | hey_jarvis | 23 / 33 / 3 / 0% | 50 / 40 / 40 / 20% | 1,06 | 0,47 |

- **Fetta 2 — Integrazione**: FATTA.
  - Modello da file fidato in `clients/voice/ascolto.py`, con ripiego su hey_jarvis.
  - Passo 3b in `scripts/voce/installa.sh`.
  - Nuovi test.
  - Prova con openWakeWord vero: 1,00 su «ehi jarvis» (hey_jarvis 0,49), 0,00 su una frase neutra.
- **Fetta 3 — Prova sul Mac con la voce dell'operatore**: DEFERITA. Il Mac non è raggiungibile da questa sessione.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md                                                             |   4 +++
 clients/voice/ascolto.py                                                                       |  37 ++++++++++++++++++--
 clients/voice/modelli/LEGGIMI.md                                                               |  26 ++++++++++++++
 clients/voice/modelli/ehi_jarvis_it.onnx                                                       | Bin 0 -> 856178 bytes
 reports/diff_sessione.md                                                                       |  26 ++++++--------
 reports/handoff.md | n/d
 reports/stato_progetto.md                                                                      |   3 +-
 reports/ultimo_report.md                                                                       |  70 ++++++++++++++++++++++---------------
 reports/voce_simulazione_2026-11-23/modello_italiano/LEGGIMI.md                                |  63 +++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/ehi_jarvis_it.addestramento.json          | 574 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_ens67_f1.json                 |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_hey_jarvis_H_f1.json          |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_hey_jarvis_H_f4.json          |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_hey_jarvis_f1.json            |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_hey_jarvis_f4.json            |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v4_G.json                     |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v4_d128_ami_f1.json           |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v6_d128_nomi_H_f1.json        |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v6_d128_nomi_f1.json          |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v7_d128_nomi_neg384_H_f1.json |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v7_d128_nomi_neg384_f1.json   |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/griglia_v7_d128_nomi_neg384_f4.json   |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/quasi_v4.txt                          |  10 ++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/quasi_v6.txt                          |   5 +++
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/quasi_v7.txt                          |   5 +++
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/ris_validazione_heyjarvis.txt         |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/validazione_v4.txt                    |   1 +
 reports/voce_simulazione_2026-11-23/modello_italiano/ris/validazione_v6_v7.txt                 |   3 ++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/addestra.py                        | 272 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/feature.py                         | 193 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/flussi_nuovi.py                    | 102 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/frasi_test.py                      |  25 +++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/genera.py                          | 146 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/lib_sim.py                         | 163 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/mls.py                             |  30 ++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/quasi_test.py                      |  64 ++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/rifai_tutto.sh                     |  51 +++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/scarica.sh                         |  46 ++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/tabella.py                         |  24 +++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/testi.py                           | 160 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/valuta.py                          | 139 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/LEGGIMI.md                                                                        |   2 +-
 scripts/voce/installa.sh                                                                       |  20 +++++++++++
 tests/test_unit_voce_ascolto.py                                                                |  66 ++++++++++++++++++++++++++++++++---
```

NB: regola «n/d»: il conteggio di reports/handoff.md non è misurabile mentre lo si scrive; la riga di totale è tolta.

## §3 GIT LOG --ONELINE (sessione)

```
21a68a4f docs(fine-task): handoff modello ehi_jarvis_it, review #854/#855
d6a980a5 feat(voce): modello «ehi jarvis» con accento italiano (ehi_jarvis_it)
b650558a chore(revisore): memoria review #855 — APPROVATO CON RISERVE
5291bca4 chore(revisore): memoria review #854 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Il commit d6a980a5 tocca  (perimetro). Sotto ci sono i due verdetti INTEGRALI: #854 sul primo diff e #855 sul delta con le correzioni R-854-1/R-854-2.

```
## VERDETTO: APPROVATO CON RISERVE

Review #854. Diff staged su feat/voce-modello-italiano: 39 file, +2214/−8. Ho letto CLAUDE.md, la memoria del revisore e le voci sulla voce in stato_progetto.md (letto con grep mirato). I 73 test `-k "modello or installa"` di tests/test_unit_voce_ascolto.py passano. `git diff --cached --check` è pulito. Lo sha256 del file .onnx corrisponde a quello scritto nel LEGGIMI. I `__pycache__` sotto reports/ non sono nell'indice. Nessun antipattern del Wall of Shame: nessun taglio diretto della history e nessun output dei tool simulato. Il motore (gas.py, brains/) non è toccato.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1431` — `modello_della_parola`
   - Cosa fa: con un nome semplice (regex `[a-z0-9_]{1,40}` di `clients/voice/ascolto.py:194`) costruisce il percorso solo dentro `.gas_voce/modelli` sotto `_GAS_ROOT`. `exists()` e `is_symlink()` stanno dentro un try su OSError. Il file passa da `_file_fidato` (`clients/voice/ascolto.py:1402`): niente symlink, proprietario l'utente, file e cartella non scrivibili da altri.
   - Rischio: percorso preso dall'ambiente, symlink, permessi deboli.
   - Esito: ok. Il nome non entra mai nel percorso se contiene `/` o `..`, e lo copre `tests/test_unit_voce_ascolto.py:3327`.

2. `clients/voice/ascolto.py:1494` — `sorgente` passata a `Model(wakeword_models=[sorgente])`, mentre `custom_verifier_models={modello: ...}` resta sotto il nome.
   - Rischio: chiave delle previsioni diversa dal nome.
   - Esito: ok. openWakeWord, in openwakeword/model.py righe 91-92 del pacchetto installato, chiama il modello con `splitext(basename(percorso))[0]`, cioè `ehi_jarvis_it`, uguale al nome.

3. `clients/voice/ascolto.py:1644` — effetti di contesto con `GAS_ASCOLTO_MODELLO=ehi_jarvis_it`.
   - `verifica_della_voce` cerca `ehi_jarvis_it_verifier.pkl`, non lo trova e dà «assente». Quindi 1 fase (`clients/voice/ascolto.py:177`), soglia `GAS_ASCOLTO_SOGLIA` 0,7 e interruzione a 0,8 su 3 blocchi (`clients/voice/ascolto.py:198`).
   - Esito: ok, coerente con quanto dichiarato. Vedi però R-854-1 e R-854-3.

4. `scripts/voce/installa.sh:138` — passo 3b.
   - Cosa fa: `mkdir -p`, chmod 700 sulle due cartelle, `install -m 600` (che sostituisce il file, anche un symlink, invece di scriverci dentro), `stop` se la copia fallisce. Il `.env` si aggiorna solo se `valore_env` non trova la chiave; una chiave presente anche vuota resta intatta.
   - Rischio: idempotenza, doppioni nel `.env`, `.env` senza a capo finale (il printf inizia con `\n`).
   - Esito: ok. Lo provano `tests/test_unit_voce_ascolto.py:1945` (seconda esecuzione senza doppioni) e `tests/test_unit_voce_ascolto.py:1961` (modello già scelto lasciato com'è).

5. `tests/test_unit_voce_ascolto.py:2221` — i test del `.env` «byte per byte» ora partono con `GAS_ASCOLTO_MODELLO` già presente.
   - Rischio: test indeboliti.
   - Esito: ok. Verificano ancora che il `.env` resti identico; il caso «chiave assente» è coperto dal test nuovo.

**Riserve (da tracciare in stato_progetto.md)**

- **R-854-1 MEDIA** (`scripts/voce/installa.sh:142`): rieseguire installa.sh su un `.env` senza `GAS_ASCOLTO_MODELLO` (probabile sul Mac dell'operatore) passa a `ehi_jarvis_it` e spegne in silenzio il filtro della voce già addestrato. Quel filtro è il file `.gas_voce/verifica/hey_jarvis_verifier.pkl`, legato al nome hey_jarvis. Inoltre `registra_voce.py` accetta solo modelli pronti, quindi oggi il filtro non si può rifare per ehi_jarvis_it. Il LEGGIMI lo dice, l'installer no. Proposta: se il filtro hey_jarvis esiste, non cambiare modello (o almeno avvisare a terminale) e lasciare la scelta all'operatore. La decisione «modello italiano senza filtro» contro «hey_jarvis col filtro» spetta all'operatore.
- **R-854-2 BASSA** (`clients/voice/ascolto.py:1446`): se il file del modello c'è ma non è fidato, la funzione restituisce il nome nudo. openWakeWord non trova un modello pronto con quel nome e alza ValueError. `main` scrive «openWakeWord non pronto… installa» ed esce con 1, e launchd lo riavvia ogni 10 s. Non va in crash, ma l'ascolto resta fermo e il messaggio porta fuori strada. Ripiegare su hey_jarvis con un avviso nel log terrebbe l'ascolto acceso (§9).
- **R-854-3 BASSA**: l'interruzione col modello nuovo (0,8 per 3 blocchi di fila, voce di Gas in sottofondo) non è stata misurata. Il LEGGIMI riporta solo attivazioni e falsi.
- **Nota (già prima, nessun peggioramento)**: openWakeWord prova `os.path.exists(nome)` rispetto alla cartella corrente. Un `GAS_ASCOLTO_MODELLO` con un percorso, che non passa la regex, arriva com'è a `Model()` e carica quel file ONNX, come prima della modifica.

**Rischi esclusi (non verificati)**

- Qualità reale del modello sulla voce dell'operatore e sul microfono del Mac: in questo container non si può riprodurre. Fa fede la prova del chiamante con openWakeWord vero.
- Contenuto del file .onnx: non l'ho ispezionato. È ONNX, non pickle, quindi non esegue codice al caricamento.
- Script di addestramento in reports/: letti solo per cercare percorsi o segreti, nessuno trovato.
- Licenza CC BY-NC-SA in un repo pubblico: rilevante, ma è una scelta dell'operatore e non un controllo tecnico.
- Comportamento di `install` BSD su macOS: dato per buono senza prova sul Mac.
- I fallimenti della suite completa (34 in tests/test_unit_web_browser.py e 1 in tests/test_unit_voice_server.py, per bwrap assente) riguardano file fuori dal diff: non li ho riverificati, come mi hai indicato.

**Memoria**: riga #854 e 2 lezioni aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, già committate da sole (5291bca4). L'indice staged è intatto (39 file); git stash non usato.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #855: ho ricontrollato solo il delta rispetto alla #854. L'indice è come lo hai descritto: 39 file, +2232/−8. Rieseguiti i test `-k "modello or installa"` di tests/test_unit_voce_ascolto.py: 74 passati. Non ho usato git stash.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1452` — se il file del modello c'è ma non è fidato, ora la funzione restituisce `MODELLO_DI_RISERVA` (`clients/voice/ascolto.py:194`, vale "hey_jarvis") e scrive un avviso nel log.
   - Rischio: il nome del modello caricato diventa diverso da `modello`, la chiave del verificatore.
   - Esito: ok. Il verificatore si cerca per `ehi_jarvis_it_verifier.pkl`, che non esiste, quindi va col nome giusto. Se ci fosse un verificatore con la chiave sbagliata, l'errore lo prende il try di `rilevatore_con_verifica`. Il punteggio è il massimo dei valori, quindi la chiave non conta. R-854-2 è chiusa: l'ascolto non si ferma più.
2. `clients/voice/ascolto.py:1498` — la sorgente si calcola una volta sola, prima di creare i modelli.
   - Esito: ok.
3. `scripts/voce/installa.sh:149` — l'avviso compare solo quando lo script scrive `GAS_ASCOLTO_MODELLO=ehi_jarvis_it` e `.gas_voce/verifica/hey_jarvis_verifier.pkl` esiste. Dice che il filtro della voce resta spento e come riaverlo.
   - Esito: ok. R-854-1 è risolta con un avviso. La scelta (modello italiano senza filtro) è dell'operatore e va registrata come sua decisione in stato_progetto.md.
4. `tests/test_unit_voce_ascolto.py:1961` — test nuovo dell'avviso.
   - Esito: ok, ma controlla solo che l'avviso ci sia. Manca il controllo opposto: nessun avviso senza il file del filtro, o quando la chiave era già nel `.env`. Lacuna di copertura BASSA, non blocca.
5. `tests/test_unit_voce_ascolto.py:3351` — col file non fidato il test ora si aspetta "hey_jarvis".
   - Esito: ok.

**Riserve (da tracciare in stato_progetto.md)**

- **R-854-1, decisione dell'operatore**: col modello italiano il filtro della sua voce resta spento. L'installer lo avvisa, ma la scelta va registrata come sua.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello nuovo non è misurata (soglia 0,8 su 3 blocchi di fila, con la voce di Gas in sottofondo).
- **R-855-1 COSMETICA**: dopo il ripiego su hey_jarvis, la riga di log «ascolto pronto: parola «ehi_jarvis_it»» (`clients/voice/ascolto.py:1663`) indica ancora il nome chiesto, non il modello usato. L'avviso del ripiego compare prima nel log, quindi la cosa si capisce.

**Rischi esclusi (non verificati)**

- Il comportamento sul Mac: la qualità del modello, l'avviso letto dall'operatore, `install` di macOS. Non si può riprodurre in questo container.
- I fallimenti di tests/test_unit_web_browser.py: non li ho riverificati. Li dai come identici su origin/main per bwrap assente, e sono fuori dal diff.

**Memoria**: aggiunta la riga #855 in /home/user/Gas/.claude/agents/memoria_revisore.md, già committata da sola (b650558a). L'indice staged è rimasto intatto.

Il commit è consentito.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_voce_ascolto.py`: 384 → 388 passed (4 test nuovi; 3 test esistenti adattati).
- Suite completa su questo container: 35 failed, 4285 passed, 2 skipped (riepilogo reale: «35 failed, 4285 passed, 2 skipped in 579.99s», prima delle correzioni R-854).
  - I FAIL sono fuori scope: 34 in `tests/test_unit_web_browser.py` e 1 in `tests/test_unit_voice_server.py`, per bwrap assente nel container (`FileNotFoundError: ... 'bwrap'`).
  - Su origin/main `tests/test_unit_web_browser.py` fallisce allo stesso modo (verificato con -x). Il test di `tests/test_unit_voice_server.py` non l'ho riprovato su main.
  - Nessuno dei due file è nel diff.

## §6 STATO CI

Output reale delle ultime 3 run (via API, alla scrittura):

```
in_progress		Voce: «ehi Jarvis» con accento italiano (modello ehi_jarvis_it)	verifica-bot	feat/voce-modello-italiano	pull_request_target	45513021640	5s	2026-11-24T23:48:26Z
in_progress		feat(voce): modello «ehi jarvis» con accento italiano (ehi_jarvis_it)	CI	feat/voce-modello-italiano	push	45513013196	8s	2026-11-24T23:48:23Z
completed	success	Merge pull request #404 from Gasss23/claude/nifty-galileo-3k7kbm	CI	main	push	45511193577	11m54s	2026-11-24T23:35:00Z
```

Mappatura commit→run:
- d6a980a5: run CI 45513013196 (push), in corso alla scrittura.
- 5291bca4 e b650558a: pushati insieme a d6a980a5, quindi nessuna run su questi SHA; il loro contenuto è nell'albero testato.
- 21a68a4f (primo commit di fine-task, con l'handoff rovinato dalla shell e corretto in questo commit): run CI partita col suo push; esito non ancora disponibile alla scrittura dell'handoff.
- Commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-854-1: decisione dell'operatore (modello italiano senza filtro della voce). Avviso aggiunto in `installa.sh`.
- R-854-2: CHIUSA con il ripiego su hey_jarvis (review #855).
- R-854-3 BASSA: interruzione col modello nuovo non misurata.
- R-855-1 COSMETICA: dopo il ripiego, il log «ascolto pronto» mostra il nome chiesto.
- Lacuna di copertura BASSA (#855): manca il test «nessun avviso» senza filtro.
- Riserve delle altre chat: in `reports/stato_progetto.md`, non toccate qui.
