# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-24 — Voce: modello «ehi jarvis» con accento italiano (ehi_jarvis_it), PR #405

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #405 (https://github.com/Gasss23/Gas/pull/405).
   - Revisore: APPROVATO CON RISERVE.
   - Bot sul giro 05df3ae7: APPROVATO CON RISERVE senza ALTA/MEDIA, check neutral: decide l'operatore.
   - Verifica esterna su 3b407738: APPROVATO CON RISERVE, con V-1 MEDIA (conflitto con main), risolta col merge c85490e5.
   - L'operatore ha dato il «mergia» il 25/11, prima del 2° merge di main (PR #406, solo report in conflitto, review #863-MERGE APPROVATO).
2. R-854-1, scelta dell'operatore:
   - modello italiano: più chiamate prese, ma risponde a chiunque dica «ehi Jarvis» e fa più falsi sui quasi-omofoni (flusso B 49,8/h contro 33,9). Si sceglie con `bash scripts/voce/installa.sh --italiano`;
   - hey_jarvis col filtro della voce: resta tale lanciando `installa.sh` senza opzione.
   - Senza il file del filtro (`.gas_voce/verifica/hey_jarvis_verifier.pkl`), `installa.sh` sceglie da solo il modello italiano, se il `.env` non ne sceglie già uno (V-2 della 2ª verifica esterna).
3. Licenza del modello CC BY-NC-SA (uso personale) in un repo pubblico (V-3 della verifica esterna). È la stessa di hey_jarvis; la decisione è dell'operatore.
4. Prova sul Mac con la voce vera.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — Addestramento del modello `ehi_jarvis_it`**: FATTA.
  - Lavoro nello scratchpad; nel repo vanno il modello, gli script e i risultati.
  - Simulazione a soglia 0,5, 1 fase, prese a vicino / −6 / −12 / −20 dB:

    | | voci della simulazione | voci mai viste | falsi/ora, parlato letto | falsi/ora, audio generico | falsi/ora, flusso B con quasi-omofoni |
    |---|---|---|---|---|---|
    | ehi_jarvis_it | 100 / 100 / 87 / 47% | 90 / 75 / 70 / 58% | 0,35 | 0 | 49,8 |
    | hey_jarvis | 23 / 33 / 3 / 0% | 50 / 40 / 40 / 20% | 1,06 | 0,47 | 33,9 |

- **Fetta 2 — Integrazione**: FATTA.
  - Modello da file fidato in `clients/voice/ascolto.py`.
  - Passo 3b in `scripts/voce/installa.sh`.
  - Prova con openWakeWord vero: 1,00 su «ehi jarvis» (hey_jarvis 0,49), 0,00 su una frase neutra.
- **Fetta 3 — Riserve di verifica esterna e bot su #405**: FATTA (908f430b, review #856/#857).
  - Soglia 0,5 scritta insieme al modello.
  - Ripiego su hey_jarvis col file assente.
  - Opzione `--italiano` quando c'è il filtro hey_jarvis.
  - Test del collegamento rilevatore→file.
  - Documenti con i limiti.
- **Fetta 3b — CI rossa su d6a980a5**: FATTA. Rinominati gli script `*_test.py` della simulazione, che pytest prendeva per test.
- **Fetta 3c — Conflitto con main (PR #404 CRM)**: FATTA. Merge c85490e5: report del ramo tenuti, stato e memoria uniti, file di main identici (review #860-MERGE APPROVATO).
- **Fetta 3d — 2° conflitto con main (PR #406 CRM)**: FATTA (review #863-MERGE APPROVATO).
- **Fetta 4 — Prova sul Mac con la voce dell'operatore**: DEFERITA. Il Mac non è raggiungibile da questa sessione.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md                                                             |   9 +++++
 clients/voice/ascolto.py                                                                       |  54 ++++++++++++++++++++++++++--
 clients/voice/modelli/LEGGIMI.md                                                               |  27 ++++++++++++++
 clients/voice/modelli/ehi_jarvis_it.onnx                                                       | Bin 0 -> 856178 bytes
 reports/diff_sessione.md                                                                       |  21 +++++------
 reports/handoff.md | n/d
 reports/stato_progetto.md                                                                      |   3 +-
 reports/ultimo_report.md                                                                       |  72 +++++++++++++++++++++++++++-----------
 reports/voce_simulazione_2026-11-23/modello_italiano/LEGGIMI.md                                |  61 ++++++++++++++++++++++++++++++++
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
 reports/voce_simulazione_2026-11-23/modello_italiano/script/frasi_prova.py                     |  25 +++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/genera.py                          | 146 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/lib_sim.py                         | 163 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/mls.py                             |  30 ++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/quasi_prova.py                     |  64 ++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/rifai_tutto.sh                     |  51 +++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/scarica.sh                         |  46 ++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/tabella.py                         |  24 +++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/testi.py                           | 160 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/modello_italiano/script/valuta.py                          | 139 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 scripts/voce/LEGGIMI.md                                                                        |   2 +-
 scripts/voce/installa.sh                                                                       |  45 +++++++++++++++++++++++-
 tests/test_unit_voce_ascolto.py                                                                | 119 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----
```

NB: regola «n/d»: il conteggio di reports/handoff.md non è misurabile mentre lo si scrive; la riga di totale è tolta.

## §3 GIT LOG --ONELINE (sessione)

```
1068914b Merge origin/main (PR #406 CRM) nel ramo della PR #405 — report del ramo tenuti, stato e memoria uniti (review #863-MERGE)
ad58e167 docs(fine-task): handoff dopo il merge di main (review #860-MERGE) e i verdetti del 2° giro sulla #405
c85490e5 Merge origin/main (PR #404 CRM) nel ramo della PR #405 — report del ramo tenuti, stato e memoria uniti (review #860-MERGE)
05df3ae7 fix(report): script della simulazione rinominati *_prova.py (pytest li raccoglieva: unit-suite rosso); handoff corretto
3b407738 docs(fine-task): handoff con le correzioni di verifica esterna e bot #405 (review #856/#857)
908f430b fix(voce): installa.sh sceglie il modello italiano col filtro solo con --italiano; soglia 0.5; ripiego col file assente
dcee5f24 chore(revisore): memoria review #857 — APPROVATO CON RISERVE
c0c30f2f chore(revisore): memoria review #856 — APPROVATO CON RISERVE
d63cb6f5 docs(fine-task): handoff ripulito (testo perso nella shell)
21a68a4f docs(fine-task): handoff modello ehi_jarvis_it, review #854/#855
d6a980a5 feat(voce): modello «ehi jarvis» con accento italiano (ehi_jarvis_it)
b650558a chore(revisore): memoria review #855 — APPROVATO CON RISERVE
5291bca4 chore(revisore): memoria review #854 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

I commit d6a980a5 e 908f430b toccano `tests/test_unit_voce_ascolto.py` (perimetro). Sotto ci sono i quattro verdetti INTEGRALI, in ordine:
- #854: primo diff;
- #855: correzioni R-854-1 e R-854-2;
- #856: correzioni della verifica esterna;
- #857: delta finale, con le correzioni del bot.

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

```
## VERDETTO: APPROVATO CON RISERVE

Review #856: ho ricontrollato solo il delta staged dopo la verifica esterna della PR #405 (4 file, +53/−9). Rieseguita tutta tests/test_unit_voce_ascolto.py: 389 passati. Non ho usato git stash; l'indice è intatto.

**Elementi esaminati**

1. `clients/voice/ascolto.py:1432` — `_modelli_pronti()` legge i nomi da `openwakeword.MODELS`. Ho controllato nel pacchetto installato: le chiavi sono `alexa`, `hey_mycroft`, `hey_jarvis`, `hey_rhasspy`…. Restituisce un insieme vuoto se c'è un'eccezione.
   - Rischio: insieme vuoto che fa ripiegare anche un modello pronto.
   - Esito: ok. `rilevatore_openwakeword` importa `openwakeword.model` prima di chiamare `modello_della_parola`, quindi a runtime il pacchetto c'è sempre. Nota cosmetica: il tipo di ritorno è `set` nudo invece di `Set[str]`.
2. `clients/voice/ascolto.py:1458` — se il file manca e il nome non è un modello pronto (né `hey_jarvis`), ripiega su `hey_jarvis` con un warning; un modello pronto passa col suo nome.
   - Rischio: un nome nudo che openWakeWord non trova e che ferma l'ascolto.
   - Esito: ok, V-4 della verifica esterna è chiusa. L'unico effetto collaterale è voluto: un nome parziale come `jarvis`, che prima openWakeWord accettava confrontando un pezzo del nome, ora finisce su hey_jarvis, che è comunque il modello giusto.
3. `scripts/voce/installa.sh:149` — `GAS_ASCOLTO_SOGLIA=0.5` si scrive solo nel ramo che scrive anche `ehi_jarvis_it`, e solo se `valore_env` non trova già una soglia. Una chiave presente anche vuota resta intatta.
   - Esito: ok, V-1 della verifica esterna è chiusa ed è coerente con `clients/voice/modelli/LEGGIMI.md:8`. Una seconda esecuzione non scrive di nuovo, perché la chiave del modello c'è già.
4. `tests/test_unit_voce_ascolto.py:1962` — test nuovo: una soglia già scelta (0.6) resta intatta, il modello viene scritto e l'avviso sul filtro non compare se il file del filtro manca.
   - Esito: ok, chiude la lacuna di copertura segnalata nella #855.
5. `tests/test_unit_voce_ascolto.py:3351` — il ripiego col file assente è provato con `_modelli_pronti` finto (`ehi_jarvis_it` → `hey_jarvis`, `alexa` → `alexa`).
   - Esito: ok.

**Riserve (da tracciare in stato_progetto.md)**

- **R-856-1 BASSA** (`scripts/voce/installa.sh:157`): l'AVVISO dice di tornare indietro con `GAS_ASCOLTO_MODELLO=hey_jarvis`, ma non nomina la `GAS_ASCOLTO_SOGLIA=0.5` scritta insieme. Chi torna a hey_jarvis senza filtro resta a 0,5 invece di 0,7, quindi con più attivazioni per sbaglio. Con il filtro attivo la soglia che conta è un'altra (`GAS_ASCOLTO_SOGLIA_VERIFICA`), quindi l'effetto c'è solo senza filtro. Correzione: aggiungere all'avviso «e togli GAS_ASCOLTO_SOGLIA=0.5», e fare lo stesso nella riga «tornare indietro» del LEGGIMI.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello nuovo non è misurata.
- **R-855-1 COSMETICA**, ancora aperta: dopo il ripiego, il log «ascolto pronto» mostra il nome chiesto e non quello usato.

**Rischi esclusi (non verificati)**

- La prova con openWakeWord vero (1,00 contro 0,49 di hey_jarvis): non l'ho ripetuta, mi fido della tua.
- Il comportamento sul Mac: in questo container non si può riprodurre.
- Il resto della PR, fuori da questo delta: era già coperto dalle review #854 e #855.

**Memoria**: aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md la riga #856 e una lezione (quando l'installer scrive due chiavi legate nel .env, le istruzioni per tornare indietro devono nominarle entrambe). Già committate da sole (c0c30f2f).

Il commit è consentito.
```

```
## VERDETTO: APPROVATO CON RISERVE

Review #857: ho riletto tutto il `git diff --cached` (6 file, +114/−26). Rieseguita tests/test_unit_voce_ascolto.py: 391 passati. Non ho usato git stash; l'indice è intatto.

**Elementi esaminati**

1. `scripts/voce/installa.sh:28` — lettura delle opzioni: `--italiano` accende la scelta, qualunque altra opzione chiama `stop`.
   - Rischio: uno stop arrivato dopo aver già scritto qualcosa.
   - Esito: ok. Il ciclo gira prima del passo 1, quindi niente è stato ancora toccato. `tests/test_unit_voce_ascolto.py:1994` controlla l'uscita con 1 e il `.env` senza `GAS_ASCOLTO`. Nessun altro script chiama installa.sh con opzioni.
2. `scripts/voce/installa.sh:158` — se esiste il filtro della voce per hey_jarvis e manca `--italiano`, il `.env` non viene toccato e lo script spiega come scegliere. Il file del modello viene copiato lo stesso.
   - Rischio: filtro spento in silenzio (V-1 MEDIA del bot).
   - Esito: ok, V-1 è chiusa. La scelta passa all'operatore. `tests/test_unit_voce_ascolto.py:1976` prova prima la versione senza opzione (nessuna scrittura) e poi quella con `--italiano` (modello, soglia e avviso scritti).
3. `scripts/voce/installa.sh:172` — l'avviso spiega di tornare a `GAS_ASCOLTO_MODELLO=hey_jarvis` e di togliere anche `GAS_ASCOLTO_SOGLIA=0.5`.
   - Esito: ok, R-856-1 è chiusa. Lo stesso testo è in `clients/voice/modelli/LEGGIMI.md`.
4. `tests/test_unit_voce_ascolto.py:3475` — test nuovo: con openWakeWord finto e il file fidato, `Model()` riceve `wakeword_models=[str(f)]`.
   - Esito: ok, V-3 è chiusa. È il collegamento che mancava tra `rilevatore_openwakeword` e il file.
5. `clients/voice/ascolto.py:1458` — ripiego su hey_jarvis se il file manca e il nome non è un modello pronto (`_modelli_pronti` in `clients/voice/ascolto.py:1432`). Era già esaminato nella #856; nel diff contro HEAD non è cambiato.
   - Esito: ok.

**Riserve (da tracciare in stato_progetto.md)**

- **R-857-1 COSMETICA**: con `GAS_ASCOLTO_MODELLO` già nel `.env`, `--italiano` non cambia niente. Il messaggio dice «lo lascio com'è», ma non dice che l'opzione è stata ignorata.
- **R-854-3 BASSA**, ancora aperta: l'interruzione col modello nuovo non è misurata.
- **R-855-1 COSMETICA**, ancora aperta: dopo il ripiego, il log «ascolto pronto» mostra il nome chiesto e non quello usato.
- **Numeri peggiori** (V-2 del bot): il LEGGIMI ora dichiara più falsi di hey_jarvis sui flussi pieni di parole simili (49,8 contro 33,9 all'ora) e più chiamate prese da altre voci (75% contro 40%). È un compromesso dichiarato, non un difetto del codice. La scelta resta dell'operatore, ed è il motivo per cui `--italiano` è giusto.

**Rischi esclusi (non verificati)**

- Il comportamento sul Mac (installer vero, voce dell'operatore): in questo container non si può riprodurre.
- La correttezza dei numeri riscritti nei LEGGIMI: non li ho ricalcolati dai file grezzi in `reports/voce_simulazione_2026-11-23/modello_italiano/ris/`. Ho controllato solo che i documenti siano coerenti tra loro.
- I fallimenti di tests/test_unit_web_browser.py: fuori dal diff e, secondo te, identici su main.

**Memoria**: aggiunta la riga #857 in /home/user/Gas/.claude/agents/memoria_revisore.md, già committata da sola (dcee5f24).

Il commit è consentito.
```

## §4bis VERDETTO DEL REVISORE SUL MERGE DI MAIN (c85490e5)

```
## VERDETTO: APPROVATO

Review #860-MERGE: merge di origin/main b100f8d4 (PR #404 CRM) in feat/voce-modello-italiano (PR #405, HEAD 05df3ae7). Il merge è in staging e non ancora committato; MERGE_HEAD è uguale a origin/main. Non ho usato git stash.

Controlli generali:
- `git ls-files -u` è vuoto: nessun conflitto lasciato aperto.
- `git diff --cached --check HEAD` è pulito e non ci sono marcatori di conflitto.
- Rispetto a HEAD entrano 10 file (+510/−23).
- I test CRM più quelli della voce passano: 564 passati.

**Elementi esaminati**

1. `modules/crm/store.py:1`, `modules/crm/copia_cifrata.py:1`, `tests/test_unit_crm.py:1`, `scripts/crm/installa.sh:1`, `.claude/perimetro_review.txt:1`, oltre a `reports/bacheca.md` e `reports/crm/`: questi sono i file del perimetro presi da main.
   - Rischio: un file di main modificato o incompleto.
   - Esito: ok. `git diff --cached origin/main` su questi percorsi è vuoto, quindi sono uguali a main byte per byte.
2. `scripts/voce/installa.sh:158`, `clients/voice/ascolto.py:1458`, `tests/test_unit_voce_ascolto.py:3475`, oltre a `reports/voce_simulazione_2026-11-23/`: questi sono i file nostri.
   - Rischio: un file del ramo perso nel merge.
   - Esito: ok. `git diff --cached HEAD` su questi percorsi è vuoto. I soli file cambiati sia dal ramo sia da main sono memoria e stato_progetto, entrambi uniti e controllati sotto.
3. `reports/handoff.md:1`, `reports/ultimo_report.md:1`, `reports/diff_sessione.md:1`: tenuti uguali a HEAD (`--ours`).
   - Esito: ok, come vuole la regola per i report di sessione del ramo.
4. `reports/stato_progetto.md:4` — la riga «Ultimo aggiornamento» ha in testa la nostra voce e in coda la riga di main intera (verificato confrontando le stringhe). Nell'indice c'è una sola riga di questo tipo. `reports/stato_progetto.md:392` aggiunge la voce del modello italiano. Rispetto a main cambiano solo queste 2 righe (+2/−1).
   - Esito: ok.
5. `.claude/agents/memoria_revisore.md:1` — unione delle due parti: rispetto a HEAD entrano le righe della chat CRM (#858/#859 e le loro lezioni), rispetto a main entrano le nostre (#854–#857 e 3 lezioni). Nessuna riga persa né di HEAD né di main.
   - Esito: ok.

**Note COSMETICHE (contenuto del ramo, non del merge)**

- `reports/stato_progetto.md:4` cita le review «#854/#855» e dà R-854-1 come decisione dell'operatore. Dopo la #857 è già gestita con `--italiano`. R-857-1 non è tracciata in stato_progetto.md; la riga 392 dice correttamente #854–#857.

**Rischi esclusi**

- La suite completa: ho eseguito solo i test CRM e voce. Gli altri file di test non sono toccati dal merge, e i fallimenti di tests/test_unit_web_browser.py dovuti a bwrap assente sono noti.
- Il comportamento sul Mac di scripts/crm/installa.sh: non si può riprodurre qui. È già stato revisionato dalla chat CRM (#858/#859).

**Memoria**: aggiunta la riga #860-MERGE in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree. Non l'ho messa in staging né committata, perché un commit del solo file chiuderebbe il merge. Fai tu `git add .claude/agents/memoria_revisore.md` prima di committare il merge.

Il commit del merge è consentito.
```

## §4ter VERDETTO DEL REVISORE SUL 2° MERGE DI MAIN

```
## VERDETTO: APPROVATO

Review #863-MERGE: merge di origin/main 3b624d77 (PR #406, CRM dal telefono) in feat/voce-modello-italiano (PR #405, HEAD ad58e167). Il merge è in staging e non ancora committato; MERGE_HEAD è uguale a origin/main. Non ho usato git stash.

Controlli generali:
- `git ls-files -u` è vuoto: nessun conflitto lasciato aperto.
- Rispetto a HEAD entrano 9 file (+669/−7).
- I test CRM più voce passano: 586 passati (rieseguiti da me).

**Elementi esaminati**

1. `modules/crm/server.py:71`, `modules/crm/__main__.py:1`, `scripts/crm/telefono.sh:1`, `scripts/crm/spegni.sh:1`, `tests/test_unit_crm.py:1`, oltre a `reports/crm/`: sono i file presi da main.
   - Rischio: un file di main modificato nel merge.
   - Esito: ok. `git diff --cached origin/main` su questi percorsi è vuoto, quindi sono identici a main.
   - L'unica nota di `--check` (riga vuota a fine file, `tests/test_unit_crm.py:3286`) arriva già così da main, non dal merge.
2. `scripts/voce/installa.sh:158`, `clients/voice/ascolto.py:1458`, `tests/test_unit_voce_ascolto.py:3475`, `reports/voce_simulazione_2026-11-23/`, più `reports/handoff.md`, `reports/ultimo_report.md` e `reports/diff_sessione.md` (tenuti `--ours`).
   - Rischio: un file del ramo perso nel merge.
   - Esito: ok. `git diff --cached HEAD` su questi percorsi è vuoto. I soli file cambiati sia dal ramo sia da main sono memoria e stato_progetto, entrambi uniti e controllati sotto.
3. `reports/stato_progetto.md:4` — riga «Ultimo aggiornamento».
   - Ho verificato confrontando le stringhe che la riga nell'indice è esattamente così: la prima voce di main (25/11), poi la nostra voce del 24/11, poi il resto della riga di main.
   - Nell'indice c'è una sola riga di questo tipo. Rispetto a main cambia solo, in più, la voce del modello italiano.
   - Esito: ok.
4. `.claude/agents/memoria_revisore.md:1752` — memoria unita: nessuna riga persa né di HEAD né di main.
   - `#860-MERGE` (nostra) e `#860` della chat CRM sono righe distinte che convivono.
   - Esito: ok.

**Rischi esclusi**

- Il contenuto della PR #406 (dashboard del CRM dal telefono via Tailscale): non l'ho revisionato nel merito, perché entra identico a main ed è già passato dalle review #860–#862 della chat CRM.
- Il comportamento sul Mac e su Tailscale: non si può riprodurre qui.
- La suite completa: ho eseguito solo i test CRM e voce.

**Memoria**: ho aggiunto la riga #863-MERGE in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree, non in staging e non committata. Va messa in staging da te prima di committare il merge.

Il commit del merge è consentito.
```

## §5 DELTA TEST DEL MOTORE

- `tests/test_unit_voce_ascolto.py`: 384 → 391 passed (7 test nuovi; 3 test esistenti adattati).
- Dopo il merge di main: `tests/test_unit_crm.py`, `tests/test_unit_voce_ascolto.py` e `test_collection_dell_intero_repo_non_esplode` danno 565 passed.
- Suite completa su questo container, prima delle correzioni: 35 failed, 4285 passed, 2 skipped. Riepilogo reale: «35 failed, 4285 passed, 2 skipped in 579.99s».
- Correzione: non tutti i FAIL erano fuori scope.
  - 34 in `tests/test_unit_web_browser.py` dipendono da bwrap, assente nel container (`FileNotFoundError: ... 'bwrap'`); su origin/main falliscono allo stesso modo. Il file non è nel diff.
  - 1 in `tests/test_unit_voice_server.py` (`test_collection_dell_intero_repo_non_esplode`) era invece di questa PR, e la CI l'ha trovato: lo `unit-suite` di d6a980a5 è rosso. Due script della simulazione si chiamavano `frasi_test.py` e `quasi_test.py`, pytest li prendeva per test e cadeva su `import openwakeword`.
  - Rinominati in `frasi_prova.py` e `quasi_prova.py`, con il riferimento corretto in `rifai_tutto.sh`. Dopo la correzione il test passa in locale («1 passed»).

## §6 STATO CI

Output reale (API, run del branch) alla scrittura:

```
completed	success	verifica-bot	feat/voce-modello-italiano	pull_request_target	45515477257	ad58e167	2026-11-25T00:06:45Z
completed	success	CI	feat/voce-modello-italiano	push	45515470801	ad58e167	2026-11-25T00:06:42Z
completed	success	verifica-bot	feat/voce-modello-italiano	pull_request_target	45514562040	05df3ae7	2026-11-25T00:00:05Z
completed	success	CI	feat/voce-modello-italiano	push	45514556378	05df3ae7	2026-11-25T00:00:03Z
```

Mappatura commit→run:
- d6a980a5: run CI propria del push.
- 21a68a4f: run propria.
- d63cb6f5: run CI propria; unit-suite in corso al momento della verifica esterna; verifica-bot failure (V-1 MEDIA, corretta in 908f430b).
- 5291bca4, b650558a, c0c30f2f, dcee5f24, 908f430b: nessuna run su questi SHA (pushati insieme ad altri commit, o non ancora pushati); il loro contenuto è nell'albero testato dal commit di testa.
- 05df3ae7: CI e bot propri (bot APPROVATO CON RISERVE, neutral).
- ad58e167: CI verde (unit-suite, handoff-check success), verifica-bot neutral.
- c85490e5: nessuna run propria (pushato insieme ad ad58e167).
- Commit del 2° merge di main e commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-854-1: decisione dell'operatore (modello italiano senza filtro o hey_jarvis col filtro), ora esplicita con `--italiano`.
- V-3 della verifica esterna: licenza CC BY-NC-SA, decisione dell'operatore.
- R-854-3 BASSA: interruzione col modello nuovo non misurata.
- R-855-1 COSMETICA: dopo il ripiego, il log «ascolto pronto» mostra il nome chiesto.
- R-857-1 COSMETICA: `--italiano` ignorato in silenzio se il modello è già scelto nel `.env`.
- Chiuse in questa sessione:
  - R-854-2, R-856-1;
  - verifica esterna #405: V-1, V-2 (documenti), V-4, V-5 (test «nessun avviso»), V-6 (handoff riscritto);
  - bot #405: V-1, V-2, V-3, V-4.
- Bot su 05df3ae7, V-1 BASSA: nel ripiego su hey_jarvis restano la soglia 0,5 e niente filtro. Aperta; c'è il warning nel log.
- 2ª verifica esterna (commento https://github.com/Gasss23/Gas/pull/405#issuecomment-7148094095):
  - V-1 MEDIA (conflitto con main): chiusa col merge c85490e5.
  - V-2 BASSA (scelta automatica senza filtro): dichiarata in §0.
  - V-3 BASSA: manca l'hash del modello valutato in `ris/`, quindi il legame tra il `.onnx` e le griglie non si prova dal repo. Aperta.
  - V-4 COSMETICA (§6 vecchio): riscritto.
- Riserve delle altre chat: in `reports/stato_progetto.md`, non toccate qui.
