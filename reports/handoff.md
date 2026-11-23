# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-23 — M1 — Voce: simulazione end-to-end, 4 fasi sfalsate, interruzione col filtro

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questo ramo (fix/voce-fasi-interruzione): con riserve del bot serve il «mergia» dell'operatore; lo esegue l'agente.
2. Dopo il merge, una sola prova sul Mac: `.venv/bin/python scripts/voce/taratura_parola.py --chiamate 6` pronunciando «HEY JARVIS» all'inglese.
3. Se i punteggi restano bassi: decidere sul modello «ehi Jarvis» addestrato apposta (circa 1 giorno + 2-4 ore di GPU in cloud).

---

## §1 SCOPE & ESITO FETTE

- **Sonda — simulazione end-to-end (subagente, 23/11):** voci espeak a −6/−12/−20 dB con riverbero, rumore e TV; codice vero di `registra_voce.main` e `Ascolto.gira` su flussi di 30 minuti. Trovati 3 bug (fasi della griglia, interruzione spenta col filtro, griglia diversa in addestramento) e il limite di pronuncia (hey_jarvis: 0,90 all'inglese, 0,40 all'italiana). Script e risultati nello scratchpad `sim_voce`.
- **Fetta #815 — 4 fasi, interruzione col filtro, griglia in registra_voce:** FATTA, commit ce04e9c7. Review #815-M1coord APPROVATO CON RISERVE.
- **Fetta #816 — riserve R-815-1..4:** FATTA, commit 8faff652. Review #816-M1coord APPROVATO CON RISERVE (R-816-1 BASSA).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +
 clients/voice/ascolto.py           |  90 +++++++++++++++++------
 reports/diff_sessione.md           |  21 +++---
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  50 ++++++-------
 scripts/voce/LEGGIMI.md            |  13 ++--
 scripts/voce/registra_voce.py      |  11 ++-
 scripts/voce/taratura_parola.py    |   5 +-
 tests/test_unit_voce_ascolto.py    |  74 +++++++++++++++++--
```

## §3 GIT LOG --ONELINE (sessione)

```
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

---

## §5 DELTA TEST DEL MOTORE

- **`tests/test_unit_voce_ascolto.py`:** 379 su main 1b4954e2 → 382 passed (#815) → 382 passed (#816, test rafforzati). `pytest tests/ -k voce`: 538 passed (revisore #816).
- **Prova col modello vero** (openWakeWord 0.6.0, venv locale): «Hey Jarvis» di espeak con sfasamento 0/320/640/960 campioni → 4 fasi 0,998 ogni volta.
- **Kernel** (`gas.py`, `tests/test_unit_kernel.py`): non toccato.

## §6 STATO CI

Run della PR non ancora disponibile alla scrittura dell'handoff: il ramo si pusha col commit di fine-task che contiene questo file.

## §7 RISERVE APERTE

- **R-816-1 BASSA:** test mancante sull'avviso dei blocchi d'interruzione col filtro attivo.
- **Simulazione:** voci sintetiche, valori assoluti non trasferibili alla voce e al microfono veri; CPU con 4 fasi sul Mac da verificare; interruzione mentre la voce di Gas copre la chiamata ancora 0/180 (funziona solo nelle pause).
- **Chiuse:** R-815-1, R-815-2, R-815-3, R-815-4 (#816).
- **Aperte da prima:** R-813M1-1, R-810M1-2, note bot #390/#395, #382 V-1/V-2, #383 V-2/V-3 (vedi `reports/stato_progetto.md`).
