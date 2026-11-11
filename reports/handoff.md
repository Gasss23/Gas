# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — Voce: log «parola quasi sentita» per tarare la soglia su dati veri (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (riserve solo BASSE).
2. Dopo una prova di 10-15 minuti sul Mac: se le tue chiamate finiscono tra le «quasi sentite» con punteggi 0,5-0,7, abbassare la soglia a 0,6 (`GAS_ASCOLTO_SOGLIA=0.6` in `.env`). sì/no dopo i dati.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — log «parola quasi sentita» nell'ascolto + sezione nella diagnosi**: FATTA — aafe58b1, review #791-M1coord APPROVATO CON RISERVE. Motivo: dopo l'aggiornamento della sera dell'11/11 (soglia 0,7 per 3 blocchi) l'operatore riferisce «a un certo punto ha smesso di rispondermi» e il log non mostra nessuna attivazione dopo le 23:38: le chiamate scartate non lasciavano traccia.
- **Fetta 2 — bot #377 V-1 BASSA (test della soglia bassa non provava la guardia)**: FATTA — review #792-M1coord APPROVATO.
- **Fetta 3 — bot #377 (7966abf) V-1 BASSA dichiarata, V-2 COSMETICA**: FATTA — review #793-M1coord APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   4 +++
 clients/voice/ascolto.py           |  39 ++++++++++++++++++++++++
 reports/diff_sessione.md           |  18 +++++-------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   1 +
 reports/ultimo_report.md           |  24 ++++++---------
 scripts/voce/LEGGIMI.md            |   4 +++
 scripts/voce/diagnosi_ascolto.py   |  63 +++++++++++++++++++++++++++++++++++++--
 tests/test_unit_voce_ascolto.py    |  92 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
f99e1eda docs(fine-task): handoff #377 dopo il fix di bot V-1
6072471f test(voce): la guardia della soglia bassa ora è provata davvero (bot #377 V-1) — review #792-M1coord
7504f44a chore(revisore): memoria review #792 — APPROVATO
278f7595 docs(fine-task): §2/§3 dell'handoff con i report
dee51752 docs(fine-task): voce — log «parola quasi sentita» (review #791-M1coord)
aafe58b1 feat(voce): log «parola quasi sentita» per tarare la soglia su dati veri + diagnosi — review #791-M1coord
6c11f0e8 chore(revisore): memoria review #791 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #791-M1coord (commit aafe58b1)

## VERDETTO: APPROVATO CON RISERVE

Review #791-M1coord sul diff staged del branch fix/voce-quasi-parola. Letti prima CLAUDE.md §5, la parte voce di stato_progetto e la coda della memoria del revisore.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:452` — per ogni blocco con punteggio da 0,3 in su aggiorna il massimo e il numero di blocchi della salita; quando il punteggio scende sotto 0,3 chiama `_segnala_quasi`. Rischio: un cambio nell'attivazione. Il ramo `punteggio >= self.soglia` (sopra, massimo, `blocchi_parola`, `return True`) è identico a prima; quasi e quasi_blocchi sono locali e non entrano nella condizione di attivazione; se la salita attiva, `return True` arriva prima di qualsiasi segnalazione. Costo per blocco: un confronto e un max. Esito: **ok**.
- `clients/voice/ascolto.py:480` — `_segnala_quasi`: nulla se la soglia è ≤ 0,3; al massimo una riga ogni `blocchi_per(5.0)` = 62 blocchi, con `_blocchi_letti` contato in `_prossimo` (`clients/voice/ascolto.py:416`); le righe in più vanno in `_quasi_taciuti`. Rischio: crescita del log e privacy. La riga contiene solo float e int (%.2f/%d), niente audio né testo. Caso peggiore (TV h24): circa 17.280 righe/giorno, ~2,5 MB/giorno su un log che non ruota. Esito: **ok** come limite, con R2.
- `clients/voice/ascolto.py:447` — un errore del rilevatore azzera anche la salita in corso: nessuna «quasi» a metà. Esito: **ok**, coperto da un test.
- `scripts/voce/diagnosi_ascolto.py:40` — regex `_QUASI`, provata su una riga nel formato reale del log (`basicConfig` a `clients/voice/ascolto.py:1320`, «asctime levelname message»): dà ('0.65','4','2'); il `.*?` assorbe «da 0.30 in su, soglia … per … blocchi;». Esito: **ok**.
- `scripts/voce/diagnosi_ascolto.py:217` — `main` ora legge l'intero log con `readlines()` invece di scorrerlo riga per riga. Esito: **riserva** (R2).

**Riserve (tutte BASSE)**
- **R1**: le taciute dell'ultimo gruppo, se nessuna riga le segue (fine flusso o riavvio), si perdono; quelle che passano la mezzanotte si sommano al giorno della riga successiva in `riassunto_quasi`; una salita in corso a fine flusso non viene scritta. Il conteggio delle taciute è una stima: va dichiarato.
- **R2**: la diagnosi carica in memoria tutto il log, che non ruota; nel caso peggiore (~2,5 MB/giorno) dopo mesi centinaia di MB. Meglio due letture in streaming o un solo passaggio che alimenti entrambi i parser.

**Rischi esclusi (non verificati)**: comportamento reale sul Mac con openWakeWord e la TV (non riproducibile qui; la crescita del log è un tetto teorico); LEGGIMI non riletto riga per riga.

**Test**: tests/test_unit_voce_ascolto.py rieseguito, 332 passed; 6 test nuovi (riga scritta, pausa con taciute, salita che attiva, soglia bassa, errore del rilevatore, diagnosi).

Memoria: riga #791-M1coord e una lezione in .claude/agents/memoria_revisore.md (commit 6c11f0e8).

### Review #792-M1coord (fix bot #377 V-1 BASSA, test della soglia bassa)

## VERDETTO: APPROVATO

Review #792-M1coord: modifica sopra la #791-M1coord sul branch fix/voce-quasi-parola, diff staged (solo il file di test, 2 righe aggiunte e 1 tolta), chiude V-1 BASSA del bot #377.

**Elementi esaminati**
- `tests/test_unit_voce_ascolto.py:2992` — `test_quasi_sentita_spenta_con_soglia_bassa` ora usa [0.35, 0.4, 0.0] con soglia 0.3 e blocchi_parola=5. Rischio: test che non tocca il ramo protetto (prima i valori erano sotto 0,3). Ora la salita supera 0,3 per 2 blocchi, ne servono 5 per attivare, scende a 0.0 e arriva a `_segnala_quasi`; prova anche il caso limite soglia = SOGLIA_QUASI (il `<=`). Esito: **ok**.
- `clients/voice/ascolto.py:485` — guardia `if self.soglia <= SOGLIA_QUASI: return`, non toccata. Rischio: test che passa anche senza la guardia. Mutante provato (guardia → `if False:`): `-k soglia_bassa` → «1 failed»; file ripristinato, `git diff` vuoto su ascolto.py, suite intera 332 passed. Esito: **ok**.

**Rischio escluso**: comportamento sul Mac col rilevatore vero non verificato. Restano aperte le riserve BASSE della #791 (R1 taciute residue; R2 `readlines()` su un log che non ruota).

**Memoria**: riga #792-M1coord e una lezione in .claude/agents/memoria_revisore.md (commit 7504f44a).

### Review #793-M1coord (bot #377 V-1 BASSA dichiarata, V-2 COSMETICA)

## VERDETTO: APPROVATO

Review #793-M1coord. Diff staged del branch fix/voce-quasi-parola (PR #377): 3 file, 8 righe aggiunte e 4 tolte. Solo commenti, docstring e documentazione: le righe cambiate in clients/voice/ascolto.py sono tutte in un commento `#` o nel docstring; nessuna riga eseguibile cambia.

Elementi esaminati:
- clients/voice/ascolto.py:128 — il commento sopra SOGLIA_QUASI dice che la riga «parola quasi sentita» si scrive solo nell'attesa della parola. Rischio: dire più di quanto fa il codice. Esito: ok. L'unico punto che chiama `_segnala_quasi` è clients/voice/ascolto.py:457, dentro `aspetta_parola` (clients/voice/ascolto.py:429); `_ascolta_mentre_suona` (clients/voice/ascolto.py:759, confronto a :794) e `aspetta_voce` (clients/voice/ascolto.py:627) non lo chiamano.
- clients/voice/ascolto.py:481 — docstring di `_segnala_quasi`: «uguale o sotto» SOGLIA_QUASI e «solo in `aspetta_parola`». Esito: ok, la guardia a clients/voice/ascolto.py:487 è `if self.soglia <= SOGLIA_QUASI: return`; V-2 chiusa.
- scripts/voce/LEGGIMI.md:181 — «il conteggio è una stima» (R-791-1) e «vale solo nell'attesa di Hey Jarvis». Esito: ok.
- reports/stato_progetto.md:380 — V-1 del bot #377 registrata come «dichiarato». Esito: ok, scelta legittima per una BASSA.

Wall of Shame: nessun taglio della cronologia, nessun output inventato; guardrail non toccati.

Non verificato: suite non rieseguita (332 passed dichiarato; il delta non cambia il bytecode); uso del rilevatore nella finestra dopo un turno non controllato (la frase vale comunque: lì `_segnala_quasi` non è chiamato). Restano aperte R-791-1 e R-791-2.

Memoria: riga #793-M1coord in .claude/agents/memoria_revisore.md (commit 07c65023).

## §5 DELTA TEST DEL MOTORE

- `python -m pytest -q tests/test_unit_voce_ascolto.py` → 326 passed (main e196964) → 332 passed (aafe58b1; 6 test nuovi).
- Kernel non toccato (gas.py, brains/, modules/ invariati).

```
332 passed
```

## §6 STATO CI

CI letta con lo strumento GitHub sulla PR #377: 278f7595 handoff-check success, unit-suite in corso; verifica-bot neutral (APPROVATO CON RISERVE, V-1 BASSA chiusa qui). Run del commit finale non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-791-1 BASSA — conteggio delle «taciute» è una stima (ultimo gruppo perso a fine flusso/riavvio, mezzanotte sommata al giorno dopo).
- R-791-2 BASSA — la diagnosi legge tutto il log in memoria (il log dell'ascolto non ruota).
- Bot #377 V-1 BASSA (dichiarata): la riga «quasi» c'è solo nell'attesa della parola, non nella finestra dopo un turno né mentre Gas parla.
- Non provato: rumore reale di casa (TV) → quante righe «quasi» al giorno.
