# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-23 — M1 — Voce: simulazione end-to-end, 4 fasi sfalsate, interruzione col filtro

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questo ramo (fix/voce-fasi-interruzione): con riserve del bot serve il «mergia» dell'operatore; lo esegue l'agente.
2. Dopo il merge, una sola prova sul Mac: `.venv/bin/python scripts/voce/taratura_parola.py --chiamate 6` pronunciando «HEY JARVIS» all'inglese.
3. Se i punteggi restano bassi: decidere sul modello «ehi Jarvis» addestrato apposta (circa 1 giorno + 2-4 ore di GPU in cloud).

---

## §1 SCOPE & ESITO FETTE

- **Sonda — simulazione end-to-end (subagente, 23/11):** voci espeak a −6/−12/−20 dB con riverbero, rumore e TV; codice vero di `registra_voce.main` e `Ascolto.gira` su flussi di 30 minuti. Trovati 3 bug (fasi della griglia, interruzione spenta col filtro, griglia diversa in addestramento) e il limite di pronuncia (hey_jarvis: 0,90 all'inglese, 0,40 all'italiana). Script e risultati in `reports/voce_simulazione_2026-11-23/` (dalla fetta #817).
- **Fetta #815 — 4 fasi, interruzione col filtro, griglia in registra_voce:** FATTA, commit ce04e9c7. Review #815-M1coord APPROVATO CON RISERVE.
- **Fetta #816 — riserve R-815-1..4:** FATTA, commit 8faff652. Review #816-M1coord APPROVATO CON RISERVE (R-816-1 BASSA).
- **Fetta #817 — finding del bot su #400 (b992e1cc, V-1 MEDIA: dati della simulazione fuori dal repo; V-2..V-4):** FATTA, commit 27d33851. Review #817-M1coord APPROVATO CON RISERVE; R-817-1 (sim/ nel .gitignore) chiusa subito nei documenti.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md                                     |  10 ++
 clients/voice/ascolto.py                                               | 119 ++++++++++++++++-----
 reports/diff_sessione.md                                               |  22 ++--
 reports/handoff.md                 | n/d
 reports/stato_progetto.md                                              |   2 +-
 reports/ultimo_report.md                                               |  56 +++++-----
 reports/voce_simulazione_2026-11-23/.gitignore                         |   8 ++
 reports/voce_simulazione_2026-11-23/LEGGIMI.md                         |  57 ++++++++++
 reports/voce_simulazione_2026-11-23/risultati/diff_ascolto.patch       | 161 ++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/risultati/diff_registra.patch      |  23 ++++
 reports/voce_simulazione_2026-11-23/risultati/diff_test_ascolto.patch  | 110 +++++++++++++++++++
 reports/voce_simulazione_2026-11-23/risultati/interr_1fase.txt         |  48 +++++++++
 reports/voce_simulazione_2026-11-23/risultati/interr_f4.txt            |  10 ++
 reports/voce_simulazione_2026-11-23/risultati/sweep1.txt               |  48 +++++++++
 reports/voce_simulazione_2026-11-23/risultati/sweep2.txt               |  44 ++++++++
 reports/voce_simulazione_2026-11-23/risultati/sweep3.txt               |  32 ++++++
 reports/voce_simulazione_2026-11-23/risultati/sweep4.txt               |   8 ++
 reports/voce_simulazione_2026-11-23/risultati/sweep5.txt               |  15 +++
 reports/voce_simulazione_2026-11-23/risultati/val_tr_nover.txt         |   1 +
 reports/voce_simulazione_2026-11-23/risultati/val_tr_ver.txt           |   1 +
 reports/voce_simulazione_2026-11-23/risultati/val_vero_nover.txt       |   1 +
 reports/voce_simulazione_2026-11-23/risultati/val_vero_ver.txt         |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d3_A_chiamate.json |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d3_B_parlato.json  |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d3_C_tv.json       |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d3_D_altri.json    |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d4_A_chiamate.json |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d4_B_parlato.json  |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d4_C_tv.json       |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d4_D_altri.json    |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d5_A_chiamate.json |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d5_B_parlato.json  |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d5_C_tv.json       |   1 +
 reports/voce_simulazione_2026-11-23/risultati/vero4/d5_D_altri.json    |   1 +
 reports/voce_simulazione_2026-11-23/script/analisi_prob.py             |  21 ++++
 reports/voce_simulazione_2026-11-23/script/calib.py                    |  21 ++++
 reports/voce_simulazione_2026-11-23/script/fase.py                     |  16 +++
 reports/voce_simulazione_2026-11-23/script/fase2.py                    |  14 +++
 reports/voce_simulazione_2026-11-23/script/gen_flussi.py               | 128 ++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/script/interr.py                   |  30 ++++++
 reports/voce_simulazione_2026-11-23/script/interr_f4.py                |  42 ++++++++
 reports/voce_simulazione_2026-11-23/script/lib_sim.py                  | 163 ++++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/script/scan2.py                    |  16 +++
 reports/voce_simulazione_2026-11-23/script/scegli_operatore.py         |  34 ++++++
 reports/voce_simulazione_2026-11-23/script/sim_ascolto.py              | 123 +++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/script/sim_registra.py             | 157 +++++++++++++++++++++++++++
 reports/voce_simulazione_2026-11-23/script/sweep.py                    |  43 ++++++++
 reports/voce_simulazione_2026-11-23/script/sweep2.py                   |  83 +++++++++++++++
 reports/voce_simulazione_2026-11-23/script/sweep3.py                   |  83 +++++++++++++++
 reports/voce_simulazione_2026-11-23/script/sweep4.py                   |  83 +++++++++++++++
 reports/voce_simulazione_2026-11-23/script/sweep5.py                   |  28 +++++
 reports/voce_simulazione_2026-11-23/script/traccia.py                  |  36 +++++++
 reports/voce_simulazione_2026-11-23/script/traccia2.py                 |  36 +++++++
 reports/voce_simulazione_2026-11-23/script/traccia_fasi.py             |  30 ++++++
 reports/voce_simulazione_2026-11-23/script/train_varianti.py           |  94 +++++++++++++++++
 scripts/voce/LEGGIMI.md                                                |  17 +--
 scripts/voce/registra_voce.py                                          |  11 +-
 scripts/voce/taratura_parola.py                                        |   7 +-
 tests/test_unit_voce_ascolto.py                                        | 122 ++++++++++++++++++---
```

## §3 GIT LOG --ONELINE (sessione)

```
3ddeefa0 docs(fine-task): verdetti #819/#820 e report aggiornati (soglia 0,6, fasi solo col filtro)
b1cf2c4e fix(voce): col filtro non caricato il ripiego torna a 1 fase (R-819-1) — review #820-M1coord APPROVATO
cbb0feae chore(revisore): memoria review #820 — APPROVATO
8c4728c0 fix(voce): soglia della verifica 0,6 (misurata con le 4 fasi) e 4 fasi solo col filtro della voce (V-1/V-2 bot #400 su 58fc7ed7) — review #819-M1coord APPROVATO CON RISERVE
b9f7ec6e chore(revisore): memoria review #819 — APPROVATO CON RISERVE
58fc7ed7 docs(fine-task): §2/§3 handoff
417eec1a docs(fine-task): verdetto #818, R-818-1 (comando completo per rifare la prova)
b2779464 docs(voce): interruzione misurata con 4 fasi e filtro (V-1 bot #400 su b1ca6dc9), riferimenti alla simulazione nel repo — review #818-M1coord APPROVATO CON RISERVE
8b64a649 chore(revisore): memoria review #818 — APPROVATO CON RISERVE
b1ca6dc9 docs(fine-task): §2/§3 handoff
2e3ba3c5 docs(fine-task): verdetto #817 e note del bot su #400; sim/ nel .gitignore della simulazione (R-817-1)
27d33851 fix(voce): dati della simulazione nel repo, test dell'avviso col filtro, ambiente dei test, docstring (V-1..V-4 bot #400) — review #817-M1coord APPROVATO CON RISERVE
32f25f95 chore(revisore): memoria review #817 — APPROVATO CON RISERVE
b992e1cc docs(fine-task): §2/§3 handoff
90d85369 docs(fine-task): report della simulazione e delle correzioni voce (review #815/#816-M1coord)
8faff652 fix(voce): taratura con le stesse fasi dell'ascolto, avviso dei blocchi d'interruzione col filtro, LEGGIMI e test (R-815-1..4) — review #816-M1coord APPROVATO CON RISERVE
7a70ccb5 chore(revisore): memoria review #816 — APPROVATO CON RISERVE
ce04e9c7 fix(voce): 4 fasi sfalsate per «Hey Jarvis», interruzione che funziona col filtro della voce, griglia coerente in registra_voce — review #815-M1coord APPROVATO CON RISERVE
d8056e2c chore(revisore): memoria review #815 — APPROVATO CON RISERVE
(il commit di fine-task che aggiorna §2/§3 è escluso per costruzione)
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #815-M1coord (commit ce04e9c7)

## VERDETTO: APPROVATO CON RISERVE

Review #815-M1coord. Diff staged sul branch fix/voce-fasi-interruzione: 4 file, +138/−33, sha256 del diff staged 46989ca7…. Letture obbligatorie fatte: CLAUDE.md sez. 5/8/9, stato_progetto e la memoria (lezioni #680/#681 sull'azzeramento tra le fasi, #757/#800 sull'interruzione). `tests/test_unit_voce_ascolto.py` sul working tree, uguale allo staged: **382 passed**.

**Elementi esaminati**

- `clients/voice/ascolto.py:1462` — `coda` è un buffer di 2 blocchi (2560 campioni) inizializzato a zeri; ogni chiamata concatena e tiene gli ultimi 2·BLOCCO (`clients/voice/ascolto.py:1469`). Rischio: discontinuità o ritardi sbagliati. Il ritardo massimo è 3·1280/4 = 960 campioni (60 ms), sempre dentro il buffer. Ogni modello riceve un flusso continuo, solo ritardato (`clients/voice/ascolto.py:1474`). Il test `tests/test_unit_voce_ascolto.py:3921` controlla campione per campione i ritardi 0/320/640/960. Il produttore dei blocchi (`clients/voice/ascolto.py:1331`) legge sempre esattamente BLOCCO campioni, quindi blocchi di lunghezza diversa non arrivano. — **ok**
- `clients/voice/ascolto.py:1484` — `azzera` resetta tutti i modelli e rimette la coda a zeri. Rischio: l'audio di Gas mentre parla che resta nella fase successiva (lezione #680/#681): coperto. Il test controlla però solo i reset dei modelli, non che la coda torni vuota: un mutante che toglie quella riga passerebbe. — **riserva COSMETICA (R-815-4)**
- `clients/voice/ascolto.py:1488` — `rilevatore_con_verifica` passa `fasi` solo se maggiore di 1. Ogni fase crea il suo `Model` con il proprio pickle, dal percorso già controllato da `verifica_della_voce`, letto una volta per fase. Rischio: un errore nel caricamento della 2ª–4ª fase. Esce dalla prima chiamata dentro il try e cade nel ripiego «non caricata», come prima. Il verificatore vede il preprocessore della propria fase: compatibile. — **ok**
- `clients/voice/ascolto.py:1523` — col filtro attivo e il `.env` senza `GAS_ASCOLTO_SOGLIA_INTERRUZIONE`, l'interruzione usa la soglia della parola, mai sotto la base.
  - `GAS_ASCOLTO_INTERRUZIONE=0` resta spento: `soglia_interruzione()` restituisce None e il ramo non scatta.
  - `clients/voice/ascolto.py:1525` porta il predefinito dei blocchi a 1; il valore nel `.env` vince comunque.
  - Senza filtro resta 0,8 su 3 blocchi (test dedicato).
  - Caso limite: una `GAS_ASCOLTO_SOGLIA_INTERRUZIONE=0.8` rimasta nel `.env` (era il default del #757) tiene la soglia a 0,8, ora su 1 blocco. Col filtro, che nelle chiamate arriva al massimo a 0,64–0,83, l'interruzione resta quasi spenta. Anche un valore non numerico conta come «impostato» e lascia 0,8. La tabella di `scripts/voce/LEGGIMI.md:232` dice ancora «0.8» e non nomina il caso col filtro.
  - — **riserva BASSA (R-815-3)**: controllare il `.env` dell'operatore.
- `clients/voice/ascolto.py:1573` — l'avviso «più facile» per i blocchi d'interruzione ora compare solo se il valore viene dal `.env`: niente più falso avviso col nuovo predefinito. Col filtro attivo però confronta ancora con 3: con `BLOCCHI_INTERRUZIONE=1` (che ora è il predefinito) o 2 (più difficile del predefinito) avvisa «predefinito 3», ed è fuorviante. — **riserva BASSA (R-815-2)**
- `clients/voice/ascolto.py:1598` — `GAS_ASCOLTO_FASI` è limitato tra 1 e 4 da `_numero`: un valore non valido torna al predefinito senza crash. Costo: 4 volte il preprocessore (melspec + embedding) e il modello onnx per blocco, più 4 sessioni onnxruntime coi loro thread. Accettabile sul Mac. — **ok**, col rischio escluso più sotto.
- Contesto: `scripts/voce/taratura_parola.py:154` (non toccato) chiama `rilevatore_con_verifica(modello, verifica)` senza `fasi`. La taratura, che dichiara di usare «lo stesso rilevatore dell'ascolto», misura quindi punteggi a 1 fase, mentre l'ascolto ne usa 4 e prende il massimo, che tende ad alzare sia le chiamate prese sia i falsi. Le soglie che consiglia non descrivono più il comportamento in produzione. — **riserva MEDIA (R-815-1)**. Correzione: leggere `GAS_ASCOLTO_FASI` come fa `main` e passarlo.
- `scripts/voce/registra_voce.py:375` — il silenzio davanti ora è `blocchi_per(1,0) · BLOCCO`, lo stesso conteggio di `misura` (`scripts/voce/registra_voce.py:395`): la clip resta sulla stessa griglia. In `scripts/voce/registra_voce.py:382` la prima ripetizione non è spostata e le successive hanno uno spostamento casuale: l'addestramento del verificatore continua a vedere griglie diverse, coerente con le 4 fasi in esecuzione. — **ok**
- Wall of Shame: `[-2 * BLOCCO:]` taglia un buffer audio, non la cronologia dei messaggi, quindi non tocca `_get_window`. Nessuna simulazione di output dei tool. Cap delle 10 iterazioni, cap degli 8k e provider non toccati. §9: nessuna nuova eccezione può arrivare al ciclo. — **ok**

**Rischi esclusi (non verificati)**
- I numeri della simulazione (83–87% di interruzioni, 0 auto-interruzioni, 89→96% da vicino, falsi all'ora più bassi) non li ho rieseguiti: li ho presi dallo scratchpad sim_voce. In particolare non ho controllato che il massimo su 4 verificatori non alzi i falsi con audio reale e il microfono del Mac.
- CPU e latenza reali con 4 fasi sul Mac non sono misurabili qui (nessun microfono né modello onnx eseguito in questa sessione).

**Riserve da tracciare in stato_progetto.md**: R-815-1 MEDIA (taratura a 1 fase, ascolto a 4), R-815-2 BASSA (avviso confrontato con 3 invece di 1), R-815-3 BASSA (0.8 nel `.env` tiene l'interruzione quasi spenta; tabella del LEGGIMI), R-815-4 COSMETICA (il test non verifica la coda svuotata).

**Memoria**: riga #815-M1coord e lezione «quando cambia il calcolo del punteggio, cercare gli altri chiamanti che dichiarano di usare lo stesso rilevatore», committata (d8056e2c); lo staged del motore è rimasto intatto.

### Review #816-M1coord (commit 8faff652)

## VERDETTO: APPROVATO CON RISERVE

Review #816-M1coord sul diff staged (4 file, +19/−5) del branch fix/voce-fasi-interruzione. Prima ho letto CLAUDE.md (sezione 5), stato_progetto.md e la memoria del revisore. Nessun taglio diretto della cronologia e nessuna simulazione dell'output dei tool.

- `scripts/voce/taratura_parola.py:156` — la taratura legge `GAS_ASCOLTO_FASI` con gli stessi limiti (1-4) e lo stesso predefinito di `main` (contesto in `clients/voice/ascolto.py:1600`) e passa `fasi=` a `rilevatore_con_verifica`. Rischio: la taratura misurava punteggi diversi dall'ascolto. Esito: ok, R-815-1 chiusa.
- `tests/test_unit_voce_ascolto.py:3882` — il test controlla `visti[0].get("fasi") == a.FASI_PREDEFINITE`. Se la taratura non passasse `fasi`, `extra` resterebbe vuoto, la chiave mancherebbe e il test fallirebbe. Esito: ok.
- `clients/voice/ascolto.py:1572` — `blocchi_int_pred` vale 1 (`BLOCCHI_INTERRUZIONE_VERIFICA`) col filtro attivo, altrimenti 3, e lo stesso valore va nel confronto e nel testo «predefinito %d». La riga di `_regolazioni` in `clients/voice/ascolto.py:1525` fissa lo stesso predefinito: i due punti sono coerenti. Esito: va bene, ma il ramo col filtro attivo non ha test (R-816-1).
- `scripts/voce/LEGGIMI.md:232` — la tabella dice che col filtro attivo vale la soglia della parola e chiede di togliere una vecchia `=0.8` dal `.env`. Corrisponde a `clients/voice/ascolto.py:1521-1522`. Esito: ok, R-815-3 chiusa.
- `tests/test_unit_voce_ascolto.py:3957` — dopo `azzera` arriva un blocco nuovo e si controlla che le fasi 1-3 vedano zeri nei primi 320/640/960 campioni. Prova a mente con `azzera` che non svuota la coda: le fasi vedrebbero `flusso[2B..3B]`, non zero, e il test fallirebbe. Esito: ok, R-815-4 chiusa.

Esecuzione: `tests/test_unit_voce_ascolto.py` 382 passed; `pytest tests/ -k voce` 538 passed.

Riserve:
- **R-816-1 BASSA**: nessun test copre l'avviso «più facile» col filtro della voce attivo. Il caso mancante è filtro attivo con `GAS_ASCOLTO_BLOCCHI_INTERRUZIONE=1`, dove l'avviso NON deve comparire. L'unico caso nei test è quello senza filtro (`tests/test_unit_voce_ascolto.py:2975`): se si torna al confronto con 3, nessun test se ne accorge.

Non verificato: il comportamento reale col microfono sul Mac (taratura a 4 fasi con openWakeWord vero), non riproducibile qui; controllati solo i test col modello finto.

Memoria aggiornata (#816-M1coord) e committata con `scripts/commit_memoria_revisore.sh` (commit 7a70ccb5).

### Review #817-M1coord (commit 27d33851)

## VERDETTO: APPROVATO CON RISERVE

I quattro finding del bot (V-1..V-4, PR #400) risultano chiusi. Resta una riserva BASSA sul `.gitignore` della simulazione.

**Elementi del diff esaminati**
- `tests/test_unit_voce_ascolto.py:2983` — nuovo test sull'avviso dei blocchi d'interruzione col filtro della voce attivo. Rischio: che il test passi anche senza filtro. Il test controlla «verifica della voce: attiva» e `blocchi_interruzione == 1`, e richiede che nessuna riga di log nomini la variabile. Il confronto di `clients/voice/ascolto.py:1574-1578` usa il predefinito 1 col filtro attivo; rimettendo 3 viene fuori l'avviso «predefinito 3» e il test fallisce. Rilanciati i 15 test mirati: passano. — **ok**
- `tests/test_unit_voce_ascolto.py:158` — `_main_finto` pulisce anche `GAS_ASCOLTO_FASI` (V-3): i test non dipendono più dalle variabili d'ambiente di chi li lancia. — **ok**
- `clients/voice/ascolto.py:54-57` — docstring dei predefiniti con e senza filtro (V-4), coerente col codice di `clients/voice/ascolto.py:1519-1527`: col filtro la soglia d'interruzione è quella della parola (mai sotto la base) e i blocchi sono 1, e la variabile d'ambiente prevale (`clients/voice/ascolto.py:1541`). Il ritorno indietro con `GAS_ASCOLTO_BLOCCHI_INTERRUZIONE=3`, dichiarato in `reports/voce_simulazione_2026-11-23/LEGGIMI.md:36` e in `scripts/voce/LEGGIMI.md:233`, funziona davvero. — **ok**
- `reports/voce_simulazione_2026-11-23/.gitignore:1` — esclude `script/cache`, `runs`, `flussi`, `tracce*`, `varianti`, `vero4` e `__pycache__`. Seguiti tutti i percorsi di scrittura degli script: tracce, cache, flussi, varianti e i wav di `runs/` finiscono in cartelle ignorate. Nel diff staged nessun file audio, modello o pickle; la cartella pesa 244 KB. — **ok**
- `reports/voce_simulazione_2026-11-23/script/sim_registra.py:17` — gli script cercano la copia del repo in `SIM = QUI.parent / "sim"`, cioè `reports/voce_simulazione_2026-11-23/sim/`; lo stesso in `reports/voce_simulazione_2026-11-23/script/sim_ascolto.py:19`, `train_varianti.py` e `fase.py` (`../sim`). Quella cartella **non** è nel `.gitignore` e il LEGGIMI (`reports/voce_simulazione_2026-11-23/LEGGIMI.md:39`) parla di «una copia del repo» senza dire dove metterla: chi rifà la simulazione rischia di committare un'intera copia del repo, col suo `.env` e i dati della voce, al primo `git add -A`. — **riserva**

**Segreti, percorsi personali, dati biometrici**: nessun `/home/`, `/Users/`, token o chiave negli script né nei `.patch`. Voci sintetiche espeak; l'«operatore» è simulato (`reports/voce_simulazione_2026-11-23/script/sim_registra.py:37`). Niente audio vero nel diff. — ok

**Riserva da tracciare**
- **R-817-1 BASSA**: aggiungere `sim/` al `.gitignore` di `reports/voce_simulazione_2026-11-23/` e scrivere nel LEGGIMI che la copia del repo va in `sim/`, accanto a `script/`.

**Rischio escluso**: la simulazione non l'ho rieseguita (servono openwakeword 0.6.0, espeak-ng e alcune ore) e non ho verificato che i numeri in `risultati/` derivino davvero dagli script: presi come dati dichiarati. Interruzione con la voce vera di Gas e CPU con 4 fasi sul Mac non verificabili qui; il LEGGIMI li dichiara correttamente non misurati.

Memoria: riga #817-M1coord e una lezione nuova, committata (32f25f95).

### Review #818-M1coord (commit dopo 27d33851: interruzione misurata con 4 fasi)

## VERDETTO: APPROVATO CON RISERVE

La risposta a V-1 MEDIA del bot (#400) regge. `interr_f4.py` misura davvero la configurazione predefinita: 4 fasi, filtro della voce e il punteggio massimo tra le fasi, con soglia della parola 0,5 su 1 blocco. I numeri del LEGGIMI coincidono riga per riga con i due file di risultati. Nessun antipattern della Wall of Shame. L'unico codice toccato è un commento.

Elementi esaminati:
- `reports/voce_simulazione_2026-11-23/script/interr_f4.py:18` — carica `tracce_f4_ver/<flusso>.npz` per E ed A. Rischio: che misuri le tracce a 1 fase o senza filtro. Esito: ok. Le tracce vengono da `reports/voce_simulazione_2026-11-23/script/traccia_fasi.py:22-27`: punteggio grezzo sotto 0,25, probabilità del filtro sopra, poi il massimo sulle 4 fasi. È la stessa logica della produzione (`clients/voice/ascolto.py:1461` usa `custom_verifier_threshold=soglia_base`; `clients/voice/ascolto.py:1474-1479` prende il massimo sulle fasi). `FASI_PREDEFINITE = 4` è a `clients/voice/ascolto.py:167`.
- `reports/voce_simulazione_2026-11-23/script/interr_f4.py:21` — regolazioni (0,5/1), (0,6/1), (0,8/3), (0,5/2), (0,5/3). Rischio: che quella dichiarata «predefinita» non sia quella reale. Esito: ok. Col filtro attivo e niente nel .env la soglia d'interruzione è quella della parola, 0,5 (`clients/voice/ascolto.py:162`, `clients/voice/ascolto.py:1522-1525`), su 1 blocco (`clients/voice/ascolto.py:172`).
- `reports/voce_simulazione_2026-11-23/script/interr_f4.py:33-38` — conta gli scatti fuori dalle chiamate, una volta per serie di blocchi sopra soglia; ore = blocchi × 0,08 s × 3 filtri. Rischio: metodo diverso da `interr.py`, quindi 1 e 4 fasi non confrontabili. Esito: ok, stesso metodo di `reports/voce_simulazione_2026-11-23/script/interr.py:22-29`; il totale torna (60 chiamate × 3 filtri = 180).
- `reports/voce_simulazione_2026-11-23/LEGGIMI.md:29-32` — numeri confrontati con `risultati/interr_1fase.txt` e `risultati/interr_f4.txt`. Esito: ok. A 1 fase 4/180 e 156/180; a 4 fasi 8/180, 170/180, 158/180 e 99/180; 0 scatti all'ora ovunque; nel flusso E 0/180 prese.
- `reports/voce_simulazione_2026-11-23/LEGGIMI.md:51` — comando per rifare la prova. Esito: riserva R-818-1.
- `clients/voice/ascolto.py:163` — commento che ora punta a `reports/voce_simulazione_2026-11-23/`. Esito: ok (chiude V-2 COSMETICA).

Riserve:
- **R-818-1 BASSA**: il LEGGIMI a riga 51 genera la traccia a 4 fasi solo per `E_sopra_gas`, ma `interr_f4.py` legge anche `tracce_f4_ver/A_chiamate.npz`. Va aggiunto `python traccia_fasi.py A_chiamate 4 varianti/d3_orig.pkl varianti/d4_orig.pkl varianti/d5_orig.pkl`, altrimenti il 170/180 non si può rifare con le istruzioni scritte.

Rischi esclusi:
- `traccia_fasi.py` e `interr_f4.py` non rieseguiti: audio, tracce e modelli non sono in git. Controllata la coerenza tra script, risultati e LEGGIMI, non i numeri in sé.
- In produzione le 4 fasi usano una coda con ritardo all'indietro, la simulazione uno spostamento in avanti: giudicate equivalenti a meno di un blocco, senza prova numerica.
- L'eco reale della voce di Gas dall'altoparlante non è coperta: qui la voce di Gas è simulata.

Memoria: riga #818-M1coord e una lezione, committate (8b64a649).

### Review #819-M1coord (commit 8c4728c0)

## VERDETTO: APPROVATO CON RISERVE

Review #819-M1coord sul diff staged del branch fix/voce-fasi-interruzione (PR #400). Letti CLAUDE.md §5, stato_progetto.md (ricerca mirata) e la memoria. Suite: tests/test_unit_voce_ascolto.py 384 passed.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:166` — `SOGLIA_VERIFICA_PREDEFINITA = 0.6`. Numeri del commento confrontati con i dati: in sweep5.txt la riga 7 (1 fase, 0,5) dà 89%, 28%, 2,0 e 6,0; la riga 14 (4 fasi, 0,6) 96%, 41%, 1,3 e 4,7; la riga 13 (4 fasi, 0,5) 6,6 e 8,7; le righe 2 e 6 danno 33,9 e 45,9. Tutto coincide. Giusto anche il 158/180 dell'interruzione (interr_f4.txt, riga A_chiamate a 0,6 su 1 blocco). Esito: ok.
- `clients/voice/ascolto.py:175` — `fasi_predefinite` è definita prima dell'uso in `main` (`clients/voice/ascolto.py:1613`) e nella taratura (`scripts/voce/taratura_parola.py:156`). Usa `_numero`, definita più in basso (`clients/voice/ascolto.py:307`) ma chiamata solo a runtime: va bene. `"Verifica"` come stringa nell'annotazione è corretta. `GAS_ASCOLTO_FASI` vince sempre. Esito: ok.
- `clients/voice/ascolto.py:1521` (contesto: il ripiego di `rilevatore_con_verifica`, riga non toccata) — **R-819-1 BASSA**. `main` calcola le fasi PRIMA di caricare il filtro: se il file del filtro è rotto lo stato passa a «non caricata», ma il ripiego `rilevatore_openwakeword(modello, **extra)` riusa `fasi=4` e gira 4 fasi SENZA filtro, proprio il caso che V-2 voleva evitare. Riprodotto: chiamate `[{'verificatore':'x', ..., 'fasi':4}, {'fasi':4}]`, stato finale «non caricata».
  - L'affermazione «col filtro non caricato si passa a 1 fase» è quindi **falsa**.
  - Il test `tests/test_unit_voce_ascolto.py:3458` (`rotto`) non registra gli argomenti del ripiego, per questo non se ne accorge.
  - Il `[{}]` di `tests/test_unit_voce_ascolto.py:3472` è corretto, ma copre solo `GAS_ASCOLTO_VERIFICA=0` (filtro spento).
  - Correzione suggerita: nel ripiego ricalcolare le fasi con `fasi_predefinite(verifica)` quando `GAS_ASCOLTO_FASI` non è impostata, oppure far passare a `main` le fasi come `None` = «predefinito»; poi controllare nel test `rotto` il `{}` del ripiego.
- `scripts/voce/registra_voce.py:591` (contesto) — usa `a.SOGLIA_VERIFICA_PREDEFINITA` per il riepilogo: ora mostra 0,6, coerente con l'ascolto. Esito: ok.
- `tests/test_unit_voce_ascolto.py:3427` — portare `GAS_ASCOLTO_SOGLIA` a 0,4 distingue davvero il valore d'ambiente dal predefinito 0,6. Il nuovo caso della taratura (0,55 → «più permissiva») controlla davvero il cambio di soglia. Esito: ok.
- `scripts/voce/taratura_parola.py:35` — la copia 0,6 della soglia è allineata con ascolto.py; un test controlla che i due valori siano uguali. Esito: ok.

**Note cosmetiche, non bloccanti**: dopo `fasi_predefinite` il commento «Con la verifica attiva… interruzione» resta attaccato alla funzione senza riga vuota; prima di `test_taratura_usa_il_rilevatore_con_la_verifica` c'è una sola riga vuota, ne servono due.

Guardrail e antipattern: nessuno slicing della history, nessuna simulazione di tool; gas.py e brains non toccati; §9 rispettato (il ripiego resta senza crash).

**Rischio escluso:** comportamento reale sul Mac (microfono, latenza delle 4 fasi) non verificato, simulazione non rieseguita; controllato solo che i numeri citati corrispondano ai file in risultati/.

Memoria: riga #819-M1coord e una lezione, committata con lo script (b9f7ec6e).

### Review #820-M1coord (commit b1cf2c4e)

## VERDETTO: APPROVATO

La correzione chiude R-819-1.

- `clients/voice/ascolto.py:1523` — nel ripiego (filtro non caricato o assente), se `GAS_ASCOLTO_FASI` non è nel `.env`, `extra` si azzera e il rilevatore gira a 1 fase senza filtro. Rischio: un chiamante che passa `fasi>1` di proposito scavalcato in silenzio. Esito: ok. Gli unici chiamanti sono `clients/voice/ascolto.py:1621` (main) e `scripts/voce/taratura_parola.py:157`, ed entrambi ricavano `fasi` da `fasi_predefinite`: l'override coincide con ciò che darebbe `fasi_predefinite(None)`. Con `GAS_ASCOLTO_FASI` nel `.env` la scelta esplicita è rispettata. Dopo la chiamata `main` non legge più `fasi` (niente log o stato che dica ancora 4 fasi). §9: le eccezioni restano intercettate prima.
- `tests/test_unit_voce_ascolto.py:3469` — controlla che la prima chiamata (col filtro) abbia `fasi == FASI_PREDEFINITE` e che il ripiego sia `{}`. Rischio: un test che non distingue le due chiamate. Esito: ok, `chiamate[0]` e `chiamate[-1]` le separano; l'autore dichiara di averlo visto fallire togliendo la correzione.
- `clients/voice/ascolto.py:179` — due righe vuote prima del commento, PEP8 (cosmetica). Esito: ok.

Suite eseguita: `tests/test_unit_voce_ascolto.py`, 384 passed.

**Rischio escluso:** comportamento reale dell'ascolto sul Mac col filtro rotto non riproducibile qui; non verificato `GAS_ASCOLTO_FASI` non numerico nel `.env` (il ripiego tiene le `fasi` già calcolate, 4 se all'inizio il filtro risultava attivo): marginale, non una riserva.

Memoria: riga #820-M1coord, committata (cbb0feae).

---

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_voce_ascolto.py`:** 379 su main 1b4954e2 → 382 passed (#815) → 382 passed (#816, test rafforzati) → 383 passed (#817) → 384 passed (#819, #820). `pytest tests/ -k voce`: 538 passed (revisore #816).
- **Prova col modello vero** (openWakeWord 0.6.0, venv locale): «Hey Jarvis» di espeak con sfasamento 0/320/640/960 campioni → 4 fasi 0,998 ogni volta.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.

## §6 STATO CI

Run della PR non ancora disponibile alla scrittura dell'handoff: il ramo si pusha col commit di fine-task che contiene questo file.

## §7 RISERVE APERTE

- **Simulazione:** voci sintetiche, valori assoluti non trasferibili alla voce e al microfono veri; CPU con 4 fasi sul Mac da verificare; interruzione mentre la voce di Gas copre la chiamata ancora 0/180 (funziona solo nelle pause).
- **Chiuse:** R-815-1, R-815-2, R-815-3, R-815-4 (#816); R-816-1 e V-1..V-4 del bot su #400 (#817); R-817-1 (documenti); V-1/V-2 del bot su 58fc7ed7 (#819); R-819-1 (#820).
- **Da provare sul Mac:** auto-interruzione con la voce vera di Gas e CPU con 4 fasi (dichiarati non misurati in `reports/voce_simulazione_2026-11-23/LEGGIMI.md`).
- **Aperte da prima:** R-813M1-1, R-810M1-2, note bot #390/#395, #382 V-1/V-2, #383 V-2/V-3 (vedi `reports/stato_progetto.md`).
