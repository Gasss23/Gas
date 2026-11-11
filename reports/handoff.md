# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-11 notte — Voce: log «parola quasi sentita» per tarare la soglia su dati veri (M1)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR di questa sessione (riserve solo BASSE).
2. Dopo una prova di 10-15 minuti sul Mac: se le tue chiamate finiscono tra le «quasi sentite» con punteggi 0,5-0,7, abbassare la soglia a 0,6 (`GAS_ASCOLTO_SOGLIA=0.6` in `.env`). sì/no dopo i dati.

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — log «parola quasi sentita» nell'ascolto + sezione nella diagnosi**: FATTA — aafe58b1, review #791-M1coord APPROVATO CON RISERVE. Motivo: dopo l'aggiornamento della sera dell'11/11 (soglia 0,7 per 3 blocchi) l'operatore riferisce «a un certo punto ha smesso di rispondermi» e il log non mostra nessuna attivazione dopo le 23:38: le chiamate scartate non lasciavano traccia.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 clients/voice/ascolto.py           | 39 +++++++++++++++++++++++++++++++++++++++
 scripts/voce/LEGGIMI.md            |  4 ++++
 scripts/voce/diagnosi_ascolto.py   | 63 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_voce_ascolto.py    | 91 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: regola «n/d» — il conteggio di reports/handoff.md non è misurabile al momento della scrittura; riga di totale tolta.

## §3 GIT LOG --ONELINE (sessione)

```
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

## §5 DELTA TEST DEL MOTORE

- `python -m pytest -q tests/test_unit_voce_ascolto.py` → 326 passed (main e196964) → 332 passed (aafe58b1; 6 test nuovi).
- Kernel non toccato (gas.py, brains/, modules/ invariati).

```
332 passed
```

## §6 STATO CI

CI NON VERIFICATA (gh assente): run della PR non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-791-1 BASSA — conteggio delle «taciute» è una stima (ultimo gruppo perso a fine flusso/riavvio, mezzanotte sommata al giorno dopo).
- R-791-2 BASSA — la diagnosi legge tutto il log in memoria (il log dell'ascolto non ruota).
- Non provato: rumore reale di casa (TV) → quante righe «quasi» al giorno.
