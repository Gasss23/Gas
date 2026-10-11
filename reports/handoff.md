# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — FETTA 1 PR A: strumenti nativi di sola lettura (PR #184), secondo giro dopo il BOCCIATO del bot

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #184 (https://github.com/Gasss23/Gas/pull/184). Numero e URL dall'output reale dello strumento GitHub collegato (`create_pull_request` → `{"url":"https://github.com/Gasss23/Gas/pull/184"}`): `gh` nel container non è autenticato. Autorizzazione al merge autonomo della FETTA 1 data dall'operatore in chat il 2026-10-11 (condizioni a–e): non è nel repo, la prova è la conversazione della sessione.
2. FETTA 4: `claude/roadmap_completa.md` non leggibile da questa sessione, allegato non arrivato: incollarne il testo in chat.

---

## §1 SCOPE & ESITO FETTE

- **Passo 0 — sola lettura**: `FATTA` — nessuna PR aperta, main `ea4a368`.
- **FETTA 1 PR A — strumenti nativi di sola lettura**: `FATTA` — review #282 → #283; bot e verifica esterna BOCCIATO sul primo SHA (V-1 MEDIA); correzioni in `00d5d08`, review #284 → #285 APPROVATO CON RISERVE.
- **FETTA 1 PR B — riduzione di run_command**: `DEFERITA` — dopo il merge della PR A.
- **FETTA 2 — prova del turno di notte**: `DEFERITA` — dopo la FETTA 1.
- **FETTA 3 — proposta cervello forte**: `DEFERITA` — PR a parte.
- **FETTA 4 — roadmap nel repo**: `SALTATA — documento non leggibile`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   7 ++++++
 gas.py                             | 438 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------------
 gas_identity.md                    |   9 ++++++--
 modules/gate/gate.py               |  23 +++++++++++++++++--
 reports/diff_sessione.md           |  12 +++++-----
 reports/handoff.md                 | 167 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++------------------------------------------------
 reports/stato_progetto.md          |  13 ++++++++++-
 reports/ultimo_report.md           |  22 ++++++++++++------
 tests/test_unit_kernel.py          | 307 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 9 files changed (conteggi approssimati per reports/handoff.md)
```

Nota: i conteggi di righe di `reports/handoff.md` sono approssimati per costruzione. Il set di file è esatto; la CI confronta solo i path.

## §3 GIT LOG --ONELINE (sessione)

```
00d5d08 fix(lettura): finding V-1/V-4/V-5 bot e verifica esterna #184, R-284-1
3dfd06c docs(fine-task): report PR #184 (strumenti nativi di sola lettura, review #282-#283)
1615e32 feat(lettura): strumenti nativi di sola lettura (FETTA 1, PR A)
f29b888 chore(revisore): memoria review #282 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

Nota (V-2 verifica esterna #184): le frasi «il file NON è committato» nei verdetti erano vere quando sono state scritte; la memoria del revisore viene poi committata nel commit di fine-task (es. `3dfd06c` per #283). Il testo dei verdetti resta integrale e non ritoccato.

### Review #282 (primo diff di 1615e32)

## VERDETTO: APPROVATO CON RISERVE

Review #282 sul diff staged di feat/strumenti-lettura-nativi: gas.py, modules/gate/gate.py, gas_identity.md, tests/test_unit_kernel.py. Prima ho letto CLAUDE.md, reports/stato_progetto.md e la mia memoria. Ho rilanciato la suite del kernel: 793 PASS, 0 FAIL, come dichiarato. I tool li ho provati davvero, sia su una root temporanea sia sul repo vero.

**Elementi del diff esaminati**
- `gas.py:1812`: `_risolvi_lettura` è l'unico punto di controllo dei percorsi. Rischio esaminato: che il comportamento di read_file cambi. Esito: ok. I messaggi sono identici. Un `relative_path` che non è una stringa dava già lo stesso diniego "esce dalla root", perché `_safe_path` andava in eccezione e negava. Cambia solo il testo del log ("lettura negata …").
- `gas.py:3145`: read_file ora passa da `_risolvi_lettura`. Rischio esaminato: regressione. Esito: ok; la chiave mancante resta gestita come prima.
- `gas.py:1858`: `_visita_cartella`, cioè la visita delle cartelle. Rischi esaminati: symlink, nomi da segreto nelle sottocartelle, hard link, cartelle speciali. Esito: ok. Ho provato questi casi:
  - un symlink a `.git`, usato con leggi_righe, elenca_cartella e cerca_testo, viene negato;
  - un symlink a una cartella interna viene elencato come "link" ma non visitato;
  - `sub/x.env`, `sub/.git/` e `sub/venv/` vengono omessi;
  - un hard link verso `.env` dentro una cartella viene omesso (T84d).
  Gli hard link su cartelle non esistono su Linux.
- `gas.py:1839`: `_righe_testo`. Rischi esaminati: righe enormi, binari, UTF-8 spezzato. Esito: ok. `readline(budget+1)` limita la memoria. Un file da 6 MB su una sola riga viene negato. Una riga da 100k caratteri viene tagliata da `_cap_tool_output`, con il nuovo messaggio che suggerisce leggi_righe. Un carattere multibyte non può spezzarsi al confine di riga.
- FIFO: ok. leggi_righe e conta_file la negano con `is_file`. La ricerca in una cartella la esclude grazie al filtro `v.is_file()` di `_cerca_testo` (`gas.py:1997`). Nessun blocco riprodotto.
- `modules/gate/gate.py:384`: i tool di lettura usano lo stesso controllo per nome di read_file, e "." è il default per elenca/cerca. Rischio esaminato: discrepanze tra gate e kernel. Esito: ok. `{}` passa per elenca (SAFE) ma è negato per leggi_righe; `None` e `sub/x.env` sono negati da entrambi; `modules/gate` resta leggibile.
- `modules/gate/gate.py:85`: i 4 tool di lettura sono in UNTRUSTED_INPUT_TOOLS. `gas.py:545`: data_ora è in `_TOOL_OUTPUT_FIDATO`. Esito: ok, è corretto. data_ora ignora gli argomenti e il suo output dipende solo dall'orologio del kernel.
- `gas.py:1680` e `gas.py:1721`: il diario registra del testo cercato solo la lunghezza e, come esito, solo conteggi (F-diario-eco). Esito: ok.
- `tests/test_unit_kernel.py:7807`: T84d copre il caso in cui cerca_testo sulla root non legge i file protetti né l'hard link. Esito: ok.

**Riserve (da tracciare in stato_progetto.md)**
- **R-282-1 (MEDIA)**: in `_cerca_testo` (`gas.py:2037`), un solo file più grande del budget di byte ancora disponibile ferma tutta la ricerca. L'ho riprodotto sul repo vero: `cerca_testo {"testo":"def gate_classify"}` dà "0 righe trovate in 4 file … RICERCA INCOMPLETA: tetto di byte letti". Il motivo è che `gas_debug.log` (4,9 MB, nella root, log rotante fino a 5 MB) viene letto prima delle sottocartelle. La stessa ricerca su `modules` trova invece `modules/gate/gate.py:346`. Così la ricerca sulla root, che è quella di default, oggi è quasi inutile. Fix: saltare i file con `st_size` maggiore del budget residuo, contarli come "troppo grandi" e proseguire. In alternativa un tetto per singolo file.
- **R-282-2 (BASSA)**: resta una finestra TOCTOU. Se tra `is_file()` e `open()` un file normale viene sostituito da una FIFO, `open` si blocca senza tetto di tempo. Serve però un processo esterno che scriva nel repo: Gas non può creare FIFO. Fix possibile: `os.open(..., O_RDONLY|O_NONBLOCK)` e poi controllo `S_ISREG` su `fstat`. Due difetti di messaggio: elenca_cartella mostra la FIFO come "file", e cerca_testo su una FIFO risponde "il percorso non esiste".
- **R-282-3 (BASSA)**: `sorted(os.scandir(...))` in `_visita_cartella` carica tutta la cartella prima che scattino i tetti di voci e di tempo. Con una cartella enorme si spendono memoria e tempo oltre `LETTURA_MAX_SECONDI`.
- **R-282-4 (BASSA)**: ogni voce protetta incontrata nella visita scrive un WARNING in `gas_debug.log` (6 righe per ogni ricerca sulla root). Il log cresce, ed è proprio il file che esaurisce il budget di R-282-1.

**Vincoli dell'operatore**
- 1–9: rispettati. run_command è intatto: T84m verifica che resti nello schema dei tool.
- R-277-1 resta un compromesso aperto e dichiarato: `prod.environment` è ancora leggibile.

**Rischi esplicitamente esclusi**
- Il comportamento su VPS e Mac non è verificato: ho provato solo nel container Linux da root.
- La TOCTOU con un processo concorrente non l'ho riprodotta: andrebbe sostituito un file durante la visita.
- pytest 971 non l'ho rilanciato; ho rilanciato solo la suite del kernel.

**Memoria**
- Ho aggiunto la riga #282 e una lezione nuova in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committate da sole (`f29b888`).
- Lezione: un tetto di byte condiviso tra più file va provato sul repo vero, perché un solo log grande può esaurirlo.

### Review #283 (diff finale di 1615e32, correzioni R-282-1…4)

## VERDETTO: APPROVATO CON RISERVE

Review #283: ho rivisto solo le correzioni alle riserve della #282, sul diff staged aggiornato. Tutte e 4 sono chiuse; restano 2 note basse e 1 cosmetica. Ho rilanciato la suite del kernel: 795 PASS, 0 FAIL, come dichiarato. pytest non l'ho rilanciato.

**Correzioni esaminate**
- `gas.py:2062` (R-282-1, chiusa). In `_cerca_testo` i file più grandi del budget di byte rimasto vengono contati e saltati, e la ricerca prosegue. Rischio esaminato: che la ricerca dalla root resti inutile. Esito: ok. Sul repo vero, cerca_testo "def gate_classify" dalla root ora legge 98 file, ne salta 1 troppo grande e trova `modules/gate/gate.py:346`. Su una root temporanea con un file da 5,5 MB trova i match in `z.txt` e `d/x.txt`. Se un file cresce tra il controllo della dimensione e la lettura, il tetto di byte scatta comunque e la ricerca viene dichiarata incompleta (fail-closed).
- `gas.py:1850` (R-282-2, chiusa). `_righe_testo` apre il file in modo non bloccante e controlla che sia un file normale sul descrittore già aperto; se l'apertura fallisce chiude il descrittore. Rischio esaminato: una FIFO messa al posto del file dopo i controlli. Esito: ok. Chiamato direttamente su una FIFO senza scrittore, solleva subito `_NonRegolare`, senza bloccarsi. cerca_testo su una FIFO risponde "non è un file normale né una cartella".
- `gas.py:1978`: elenca_cartella mostra le FIFO come "speciale". Provato su `d/f2`. Esito: ok.
- `gas.py:1894` (R-282-3, chiusa). La lettura della cartella si ferma al tetto di voci più 1, con controllo del tempo. Rischio esaminato: un errore di conteggio che lascerebbe il tetto non dichiarato. Esito: ok. Con 3000 file vengono 500 voci e "ELENCO INCOMPLETO" in 0,09 s.
- `gas.py:1913` (R-282-4, chiusa). Durante la visita delle cartelle il controllo dei percorsi gira con `avvisa=False`. Rischio esaminato: perdere i WARNING di read_file e delle chiamate dirette. Esito: ok. Il default resta True; `_safe_path` cambia solo nei due rami che scrivono il log, i dinieghi sono identici.
- `tests/test_unit_kernel.py:7826`: T84f prova i tetti, incluso il salto del file troppo grande. Esito: ok.

**Riserve**
- **R-283-1 (BASSA)**: il messaggio "N file oltre il tetto di byte saltati (usa leggi_righe su quei file)" non dice quali sono quei file. Il modello non sa su cosa usare leggi_righe. Basta aggiungere i primi nomi.
- **R-283-2 (BASSA, preesistente, riprodotta)**: read_file su una FIFO si blocca. Ho dovuto interrompere la prova per timeout dopo 10 s. read_file legge ancora con `path.read_text` e non ha il nuovo controllo "è un file normale". Il controllo dei percorsi ora è in un punto solo, ma l'apertura dei file no. Si può sistemare in questa PR o tracciarla. Per arrivarci serve una FIFO nel repo, e Gas non può crearne.
- **R-283-3 (COSMETICA)**: quando si supera il tetto di voci, elenca_cartella mostra un sottoinsieme preso nell'ordine del disco (es. f1000, f1007…), non i primi in ordine alfabetico. L'elenco è comunque dichiarato incompleto.

**Rischi esplicitamente esclusi**
- Non ho riprodotto lo scambio file→symlink dopo i controlli: `os.open` segue i symlink e non c'è `O_NOFOLLOW`. Serve un processo esterno che scriva nel repo; è un rischio preesistente, uguale per read_file.
- Il comportamento di `O_NONBLOCK` su macOS/BSD non è verificato: ho provato solo nel container Linux.

**Memoria**
- Ho aggiunto in coda a `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #283 e una lezione nuova: quando un fix protegge il percorso nuovo, controllare anche il percorso vecchio gemello (qui read_file).
- Come chiesto, il file NON è committato: resta modificato nel working tree.

### Review #284 (primo diff di 00d5d08, correzioni V-1/V-4/V-5 di bot e verifica esterna)

## VERDETTO: APPROVATO CON RISERVE

Review #284 sul diff staged della PR #184 (gas.py e tests/test_unit_kernel.py), dopo il BOCCIATO del bot e della verifica esterna. Le correzioni V-1, V-4 e V-5 funzionano. Restano 2 riserve basse e una nota cosmetica. Ho rilanciato la suite del kernel: 797 PASS, 0 FAIL. pytest non l'ho rilanciato.

**Elementi del diff esaminati**
- `gas.py:1926` (V-1): nella visita delle cartelle, le cartelle vere oltre la profondità massima vengono contate in `stato["profonde"]`. Rischio esaminato: contare anche cartelle protette o symlink. Esito: ok. Il conteggio avviene solo dopo il controllo di lettura e solo per cartelle vere. Una cartella vuota al limite viene dichiarata incompleta lo stesso: è un falso allarme, non un silenzio.
- `gas.py:2106` (V-1): cerca_testo dichiara «RICERCA INCOMPLETA: N cartelle oltre la profondità massima». Esito: ok, provato. Con `a/b/c/d/x.txt`, la ricerca dalla root dice «1 cartelle oltre la profondità massima (3) non visitate»; cercando da `a/b` il file viene trovato.
- `gas.py:2001`: elenca_cartella dice «N sottocartelle non aperte». Esito: ok.
- `gas.py:1976` e `gas.py:2068` (V-4): in elenca_cartella e cerca_testo i nomi passano da `rendi_visibili(a_capo=False)`. Rischio esaminato: un nome che inventa righe finte. Esito: ok, provato. Il file `evil\nfake.txt:1: alfa FALSO` esce come `evil<U+000A>fake…` e la cartella `strano
x` come `strano<U+2028>x/`.
- `gas.py:1942` (V-5): il dispatcher nega gli argomenti che non sono un dizionario, come fa il gate. Esito: ok. `elenca_cartella "[1,2]"` e `data_ora "[]"` danno «Operazione negata: argomenti non validi.» e il diario li registra come KO. Il chiamante (`gas.py:3214`) ora passa gli argomenti senza convertirli.
- `tests/test_unit_kernel.py:7831` (T84f V-1) e `tests/test_unit_kernel.py:7914` (T84g V-4): i test coprono le due correzioni. Esito: ok.

**Riserve**
- **R-284-1 (BASSA)**: le intestazioni non passano da `rendi_visibili`. Succede in leggi_righe («[rel, righe …]»), conta_file («rel: …») ed elenca_cartella («Cartella 'rel'»). Il percorso mostrato è quello risolto, quindi un symlink dal nome normale può portare a un nome con a-capo o U+2028. Provato: leggi_righe su `ok/k.txt` mostra `[strano
x/k.txt, …]` senza renderlo visibile. È lo stesso difetto V-4, ma nelle intestazioni.
- **R-284-2 (BASSA)**: il contenuto della riga trovata da cerca_testo non viene reso visibile. Un U+2028 dentro il file imita una riga finta «fake.txt:9: alfa» dopo quella vera. Provato. È contenuto già non fidato, come per read_file (lo strumento è in UNTRUSTED_INPUT_TOOLS), quindi non blocca.
- **Cosmetica**: con la profondità di default 1, elenca_cartella dice sempre «N sottocartelle non aperte» quando ci sono sottocartelle. È corretto ma rumoroso.

**Rischi esplicitamente esclusi**
- Non ho verificato come il modello interpreta U+2028 nella finestra: dipende dal tokenizer di ciascun provider.
- V-2, V-3 e la parte "" di V-5 riguardano solo i testi dei report: non li ho rivisti, come indicato.

**Memoria**
- Ho aggiunto la riga #284 e una lezione nuova in `/home/user/Gas/.claude/agents/memoria_revisore.md`.
- Come chiesto, il file NON è committato: resta modificato nel working tree.

### Review #285 (diff finale di 00d5d08, correzione R-284-1)

## VERDETTO: APPROVATO CON RISERVE

Review #285: R-284-1 è chiusa. Restano aperte, già registrate, R-284-2 (BASSA) e la nota cosmetica. Ho rilanciato la suite del kernel: 797 PASS, 0 FAIL.

**Elementi del diff esaminati**
- `gas.py:1850`: `_rel_root` ora restituisce il percorso con a-capo e caratteri di controllo resi visibili. Rischio esaminato: che il percorso trasformato finisca nei controlli di sicurezza. Esito: ok. `_rel_root` serve solo a mostrare i percorsi; i controlli usano `_file_rel_root` (`gas.py:1827`), che non cambia.
- `gas.py:2037` (leggi_righe), `gas.py:2136` (conta_file), `gas.py:1997` (elenca_cartella) e `gas.py:2071` (cerca_testo, senza più il doppio wrap): rischio esaminato, un nome che inventa righe nelle intestazioni. Esito: ok. L'ho provato con un symlink `ok` verso la cartella `strano
x`: tutti e 4 i tool mostrano `strano<U+2028>x/…`.
- `tests/test_unit_kernel.py:7924`: T84g ora copre anche leggi_righe e conta_file. Esito: ok.

**Riserve ancora aperte**
- **R-284-2 (BASSA)**: il contenuto della riga trovata da cerca_testo non viene reso visibile. Nel mio test la riga mostra ancora `riga alfa
fake.txt:9: alfa`, cioè una finta riga «fake.txt:9:».
- **Cosmetica**: con la profondità di default 1, elenca_cartella dice sempre «N sottocartelle non aperte».

**Rischio escluso**: pytest (971) non l'ho rilanciato; ho rilanciato solo la suite del kernel.

**Memoria**: ho aggiunto la riga #285 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, senza lezioni nuove. Come chiesto, il file NON è committato.

## §5 DELTA TEST DEL MOTORE

Kernel 763 → 797 PASS (T84, 34 check nuovi); pytest 971 passed (nessun test pytest nuovo). La CI conta 765 → 797+ per differenze d'ambiente (verifica esterna #184).

```
=== RIEPILOGO: 797 PASS, 0 FAIL ===
```

```
971 passed in 117.35s (0:01:57)
```

## §6 STATO CI

```
completed	success	feat(lettura): strumenti nativi di sola lettura (FETTA 1, PR A)	verifica-bot	feat/strumenti-lettura-nativi	pull_request_target	38162811892	3m45s	2026-10-11T18:12:04Z
completed	skipped	feat(lettura): strumenti nativi di sola lettura (FETTA 1, PR A)	verifica-bot	feat/strumenti-lettura-nativi	pull_request_target	38162803562	11s	2026-10-11T18:11:57Z
completed	success	docs(fine-task): report PR #184 (strumenti nativi di sola lettura, re…	CI	feat/strumenti-lettura-nativi	push	38162802071	1m59s	2026-10-11T18:11:56Z
completed	skipped	feat(lettura): strumenti nativi di sola lettura (FETTA 1, PR A)	verifica-bot	feat/strumenti-lettura-nativi	pull_request_target	38162706684	1s	2026-10-11T18:10:33Z
```

Mappatura commit→run:
- `3dfd06c` (testa del secondo push): CI `38162802071` success; verifica-bot `38162811892` (check `verifica-bot` failure: verdetto BOCCIATO).
- `1615e32`: CI `38162691707` (primo push).
- `f29b888`: nessuna run su questo SHA (pushato insieme a `1615e32`).
- `00d5d08` e commit di fine-task: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-284-2 (BASSA): contenuto delle righe di `cerca_testo` non reso visibile.
- R-283-1 (BASSA): `cerca_testo` non nomina i file saltati perché troppo grandi.
- R-283-2 (BASSA, preesistente): `read_file` su una FIFO si blocca.
- R-283-3 e nota #284 (COSMETICHE).
- V-5 parte "" (COSMETICA).
- R-277-1 (BASSA, aperta): `prod.environment` leggibile (T84l).
