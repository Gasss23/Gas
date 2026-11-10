# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — chat Mani: ascolto H24, meno attivazioni per sbaglio (Jarvis rispondeva senza essere chiamato)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #361 (https://github.com/Gasss23/Gas/pull/361): l'operatore ha già detto sì via M1 se le riserve sono solo BASSE. Dopo il merge va provato dal vivo sul Mac che «Hey Jarvis» scatti ancora (R-736-1); se non scatta, aggiungere `GAS_ASCOLTO_BLOCCHI_PAROLA=1` nel .env.

---

## §1 SCOPE & ESITO FETTE

- **PR #359 (voce di Telegram in un thread)**: `FATTA` — mergiata (695b759) col sì esplicito dell'operatore.
- **Ascolto H24, meno attivazioni per sbaglio**: `FATTA` — review #736 APPROVATO CON RISERVE (solo BASSE/COSMETICHE).
- **V-1 della verifica esterna #359 (log degli errori del thread della voce)**: `DEFERITA — prossima fetta voce, come deciso dall'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 clients/voice/ascolto.py           |  52 +++++++++++++++++++++++++++--------
 reports/diff_sessione.md           |  14 ++++------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 ++-
 reports/ultimo_report.md           |  21 +++++++-------
 scripts/voce/LEGGIMI.md            |  15 +++++-----
 tests/test_unit_voce_ascolto.py    |  80 +++++++++++++++++++++++++++++++++++++++++++++--------
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
3835a14 docs(fine-task): ascolto H24 meno attivazioni per sbaglio — PR #361
1a031ae fix(voce): l'ascolto risponde meno senza essere chiamato — finestra 15 s, al massimo 2 seguiti, parola su 2 blocchi di fila, soglia 0,6, coda dell'eco ignorata — review #736
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 1a031ae: verdetto integrale della review #736.

## VERDETTO: APPROVATO CON RISERVE

Review #736 (chat Mani). Ho letto il diff staged (`git diff --cached`, 3 file: clients/voice/ascolto.py, tests/test_unit_voce_ascolto.py, scripts/voce/LEGGIMI.md) e l'ho verificato su una copia dell'index fatta con `git checkout-index -a --prefix=` nello scratchpad, senza stash. Prima ho letto CLAUDE.md sez. 5, reports/stato_progetto.md (voci voce/H24) e la coda della mia memoria.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:387` — `aspetta_parola` conta i blocchi di fila sopra soglia (`sopra`). Rischio: il conto non si azzera su un ramo e due picchi isolati sommati fanno scattare la parola. Ho guardato tutti i rami: eccezione → `sopra = 0` (:395), sotto soglia → `sopra = 0` (:412), NaN → `nan >= soglia` è False, quindi azzera. Il ramo dei «buoni di fila» dopo gli errori non tocca `sopra`. Esito: **ok**.
- `clients/voice/ascolto.py:409` — `return True` solo con `sopra >= self.blocchi_parola`. Il valore viene da `max(1, int(...))` (:349) e in main da `_numero(...,1,5)` (:1145): il valore 0 o negativo è impossibile, e inf/nan/abc tornano al default 2. Esito: **ok**.
- `clients/voice/ascolto.py:524` — `aspetta_voce` scarta prima `blocchi_per(0.5)` = 6 blocchi, poi parte la finestra. A fine flusso esce con None, senza crash. Questi blocchi NON passano a `_parola_nel_blocco`, ma il rilevatore è appena stato azzerato (`_azzera`, :756), quindi non perde stato utile. La finestra reale diventa 15,5 s. Il percorso dell'interruzione (:741-749) non passa da `aspetta_voce`, quindi lì la coda dell'eco non si applica, come dichiarato. Il microfono viene comunque svuotato a fine riproduzione (:636): la coda vale 0,5 s in tempo reale dopo la fine della voce di Gas. Esito: **ok**, con riserva R-736-2.
- `clients/voice/ascolto.py:328` e `clients/voice/ascolto.py:1154` — `MAX_TURNI_PREDEFINITO=3` è usato sia dal costruttore sia da main. Le interruzioni contano nei turni (R-668-1 resta valida) e una parola ripetuta nella finestra azzera il conto come prima. Esito: **ok**.
- `clients/voice/ascolto.py:1144` — la soglia predefinita in main passa a 0,6 e la finestra usa la stessa soglia (`_parola_nel_blocco`). L'interruzione resta a 0,7 e su un blocco solo. Esito: **ok**.
- `tests/test_unit_voce_ascolto.py:2513` e `tests/test_unit_voce_ascolto.py:2541` — test nuovi su: parola isolata contro 2 blocchi di fila, errore che azzera il conto, coda dell'eco e massimo 2 turni di seguito. Rischio: test che passano anche col codice rotto. Ho rifatto io due mutanti sulla copia dell'index: senza `sopra = 0` nel ramo sotto soglia → 1 test fallito; coda dell'eco a 0 → 1 test fallito. Suite completa: **300 passed**. Esito: **ok**.
- `scripts/voce/LEGGIMI.md:135` — tabella aggiornata (0.6, nuova riga BLOCCHI_PAROLA, 15, 3), coerente con il docstring di ascolto.py. Esito: **ok**.
- Contesto: `clients/voice/browser_server.py:73` — la pagina web tiene il suo default di 12 s e il diff non la tocca. Esito: **ok**.

**Wall of Shame**: nessuno slicing di cronologia, il diff è solo nel client voce e non tocca il kernel. Nessuna simulazione di tool. §9: le eccezioni del rilevatore restano intercettate e il loop di `gira` non cambia. I guardrail del kernel (10 iterazioni, `_get_window`) non sono toccati.

**Riserve (tutte BASSE)**
- **R-736-1**: non sappiamo se con 2 blocchi di fila la parola vera scatta ancora. Con un blocco da 1280 campioni openWakeWord dà un solo punteggio (:1104), e i rilevamenti veri di solito restano sopra soglia per più frame: la libreria stessa ha un parametro «patience» con la stessa logica. Ma qui non si può provare. Rimedio pronto: `GAS_ASCOLTO_BLOCCHI_PAROLA=1`. Va confermato dal vivo sul Mac.
- **R-736-2**: se l'operatore parla entro 0,5 s dalla fine della risposta, quel primo mezzo secondo non entra nella richiesta (può mancare la prima sillaba) e non viene ascoltato dal rilevatore. È un costo accettabile rispetto all'eco, ma non è scritto nel LEGGIMI.
- **R-736-3 (cosmetica)**: il default del costruttore resta `soglia=0.5`, quello di main è `SOGLIA_PREDEFINITA=0.6`. È voluto per i test e lo dichiari, ma chi crea `Ascolto` fuori da main riceve la soglia vecchia.

**Rischio escluso**: non ho verificato il comportamento reale col microfono e openWakeWord sul Mac (falsi positivi e negativi con TV o stanza): fuori dal Mac non si riproduce. Non ho verificato nemmeno la pagina web (browser_server.py), che non è nel diff.

**Memoria**: ho aggiunto in coda a /home/user/Gas/.claude/agents/memoria_revisore.md, solo nel working tree e NON in index, la riga `#736 (chat Mani) — 2026-11-10 — APPROVATO CON RISERVE — …` e una lezione: «un conto N blocchi di fila va azzerato su ogni ramo che non conferma; mutante per ramo». Come mi hai chiesto non ho lanciato `scripts/commit_memoria_revisore.sh`: il file resta da committare nel tuo fine-task. L'index è intatto (staged solo i 3 file sotto review).

## §5 DELTA TEST DEL MOTORE

Kernel non toccato. `tests/test_unit_voce_ascolto.py`: da 296 a 300 casi.

```
300 passed in 27.85s
```

Mutanti presi:
- conto dei blocchi ignorato;
- coda dell'eco tolta;
- nessun azzeramento su errore;
- nessun azzeramento sotto soglia.

## §6 STATO CI

`gh` non usato (GitHub passa dallo strumento MCP). Per 1a031ae e per il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff (nessuna run su 1a031ae, pushato solo insieme all'apertura della PR). La PR #359 su 8e29c36 aveva unit-suite, handoff-check e verifica-bot success ed è stata mergiata.

## §7 RISERVE APERTE

- R-736-1 BASSA: con 2 blocchi di fila la parola vera scatta ancora? Da provare dal vivo; rimedio `GAS_ASCOLTO_BLOCCHI_PAROLA=1`.
- R-736-2 BASSA: chi parla entro 0,5 s dalla fine della risposta perde la prima sillaba.
- R-736-3 COSMETICA: il costruttore tiene soglia 0,5, main usa 0,6.
- Verifica esterna #359: V-1 BASSA, prossima fetta voce.
- R-733-1/2 e V-3 della verifica esterna #359: accettati dall'operatore come limite della guardia statica.
- Le altre riserve sono in `reports/stato_progetto.md`.
