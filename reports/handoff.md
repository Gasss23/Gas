# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-11-10 — chat Mani: «Hey Jarvis, …» detto d'un fiato non finisce più sotto «Sì, signore?»

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #368 (https://github.com/Gasss23/Gas/pull/368): riserve solo BASSE; il merge lo esegue M1 col sì dell'operatore.
2. Lanciare sul Mac i 3 comandi di lettura del log mandati a M1 e incollarne l'output (falsi «Hey Jarvis» o turni di seguito?): servono per i default più severi.

---

## §1 SCOPE & ESITO FETTE

- **Richiesta d'un fiato (prova dal vivo 10/11, 6 attivazioni su 8 senza richiesta)**: `FATTA` — 0664325, review #753-M1 e #754-M1 APPROVATO CON RISERVE (MEDIA/BASSA chiuse, restano BASSE).
- **Scarto delle trascrizioni allucinate di Whisper**: `SALTATA — sta in modules/voice/stt.py (chat M2); scartare «grazie» toglierebbe anche quelli veri`.
- **Default più severi contro le risposte non richieste**: `DEFERITA — prima i log del Mac richiesti all'operatore via M1`.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   3 +++
 clients/voice/ascolto.py           |  62 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++------
 reports/diff_sessione.md           |  19 ++++++++-----------
 reports/handoff.md                 | n/d
 reports/stato_progetto.md          |   4 +++-
 reports/ultimo_report.md           |  29 ++++++++++-------------------
 scripts/voce/LEGGIMI.md            |   6 ++++++
 tests/test_unit_voce_ascolto.py    |  72 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

NB: per la regola «n/d» dell'operatore (2026-10-24) la riga di `reports/handoff.md` dice `n/d` e manca la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
0664325 fix(voce): «Hey Jarvis, …» detto d'un fiato non finisce più sotto «Sì, signore?» — review #753-M1/#754-M1
fa7f9f8 chore(revisore): memoria review #754 — APPROVATO CON RISERVE
8599767 chore(revisore): memoria review #753 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

Commit 0664325: verdetto integrale della review #753-M1 (primo giro) e della re-review #754-M1 (sul diff committato).

## VERDETTO: APPROVATO CON RISERVE

Ho controllato il diff in staging (`git diff --cached`) sul branch claude/peaceful-lovelace-0w2b7q, 3 file. Prima ho letto CLAUDE.md, stato_progetto.md (solo le parti che servivano) e la mia memoria. Ho fatto girare tests/test_unit_voce_ascolto.py: **308 passed**. Con uno script mio nella cartella temporanea ho provato due casi limite.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:708` — `_voce_subito`: legge al massimo `blocchi_per(subito_s)` blocchi (5 nel main) e restituisce i blocchi solo con 3 blocchi forti di fila (INIZIO_VOCE_S). Rischi controllati:
  - fine del flusso: restituisce None, e il chiamante suona la conferma; la conferma poi non legge più nulla, quindi nessun crash;
  - il conto «di fila» si azzera su un blocco debole;
  - con `subito_s<=0` esce subito: i test vecchi non cambiano.
  - Esito: ok.
- `clients/voice/ascolto.py:773` — `registra(subito)`. Ho controllato che `registra` (`clients/voice/ascolto.py:471`) riceva `iniziali` già validi: ci sono almeno 3 blocchi, quindi voce=True; nessuno svuotamento, quindi l'audio non si perde; in quel ramo non suona niente, quindi niente eco. Non può restituire None (voce=True), e il tetto max_s conta anche i blocchi iniziali (al massimo 5 su 187), quindi non cambia nulla. Esito: ok. Le due sonde però hanno trovato due problemi:
  - **R-753-1-M1 (MEDIA)**: la sonda è PAROLA → 3 blocchi di voce (la coda di «…vis» se il rilevatore scatta prima della fine della parola) → pausa → richiesta. La conferma viene saltata a vuoto. Con una pausa più corta di silenzio_s (0,8 s) la richiesta si attacca e va bene (provato: un solo invio di 31 blocchi). Ma chi aspetta il «Sì, signore?» (che non arriva) per più di 0,8 s si vede chiudere la richiesta sul solo «…vis». Whisper riceve circa 0,3 s di audio, quindi è probabile un'allucinazione tipo «grazie». Nessun crash, ma è un caso d'uso rovinato. Prima di decidere una correzione va provato dal vivo. Il nuovo log aiuta a riconoscerlo: «voce subito…» seguito da «voce 0.2–0.3 s». Correzione possibile: nel ramo «subito», dare a `registra` la stessa tolleranza fino ad ATTESA_VOCE_S che ha già `dopo_parola`, finché non arrivano altri 3 blocchi forti.
  - **R-753-2-M1 (BASSA)**: con voce che parte al 4° blocco (cioè dopo circa 0,16 s dalla rilevazione) la finestra finisce con di_fila=1-2. Risultato: la conferma suona sopra l'inizio della frase e quell'audio si butta (sonda: riprodotti [SI, A], inizio perso), cioè il difetto di prima, ristretto ma non chiuso. Correzione suggerita: se la finestra finisce con di_fila>0, continuare a leggere fino a INIZIO_VOCE_S (al massimo 2 blocchi in più).
- `clients/voice/ascolto.py:785` — riga di log con voce e volume massimo espresso come multiplo della soglia. Rischi controllati:
  - divisione per zero: protetta;
  - nessun valore dell'audio nel log (test_log_senza_audio_ne_token passa);
  - il «×» fuori ASCII su stderr non crea problemi: in Python stderr usa sempre backslashreplace.
  - Costo: rms viene calcolato su ogni blocco della richiesta (fino a circa 187×1280 campioni in Python puro), cioè decine di ms prima dell'invio.
  - Esito: ok, con una nota BASSA sul costo.
- `clients/voice/ascolto.py:1202` — main passa `subito_s=SUBITO_S`; il test di main lo controlla. Esito: ok.
- `tests/test_unit_voce_ascolto.py:2614` e `tests/test_unit_voce_ascolto.py:2632` — coprono: voce d'un fiato, pausa, blocchi forti non di fila, default 0, fine del flusso. Il controllo sulla lunghezza totale uccide il mutante `letti[-1:]`. Esito: ok. Manca un test sul bordo della finestra (R-753-2-M1).

**Costo di 0,4 s**: si paga solo quando dopo la parola c'è silenzio (la conferma arriva 0,4 s più tardi). È accettabile per l'obiettivo, e il valore è una costante facile da regolare.

**Guardrail**: il diff non tocca kernel, `_get_window`, il tetto di 10 iterazioni né i provider. Nessun antipattern del Wall of Shame (è una lista di blocchi audio, non la cronologia). Le eccezioni restano gestite (§9).

**Rischio escluso**: comportamento con microfono e rilevatore openWakeWord veri sul Mac (quando scatta il rilevatore rispetto alla fine di «Jarvis», RMS reale della coda «-vis»). Non si può riprodurre in questo ambiente: R-753-1-M1 si può confermare o smentire solo con una prova dal vivo e il nuovo log.

**Riserve da tracciare in stato_progetto.md**: R-753-1-M1 (MEDIA), R-753-2-M1 (BASSA), più la nota BASSA sul costo del calcolo rms nel log.

Riga contatore #753-M1 e una lezione nuova scritte in /home/user/Gas/.claude/agents/memoria_revisore.md e committate (8599767, solo quel file). Il diff in staging è intatto (3 file).

## VERDETTO: APPROVATO CON RISERVE

Re-review #754-M1 del diff in staging aggiornato (branch claude/peaceful-lovelace-0w2b7q, 3 file, +134/−6). Ho rifatto le due sonde di #753-M1 più quattro casi nuovi con uno script mio nella cartella temporanea; tests/test_unit_voce_ascolto.py: **310 passed**. Le due riserve di #753-M1 sono chiuse; restano solo note BASSE.

**Elementi del diff esaminati**
- `clients/voice/ascolto.py:127` — SUBITO_S=0,6 s (8 blocchi) e SUBITO_VOCE_S=0,4 s (5 blocchi). **R-753-1-M1 chiusa.** Sonde con coda di 3 e di 4 blocchi forti seguita da una pausa di 1,2 s: la conferma suona e la richiesta vera arriva intera (20 blocchi inviati). Esito: ok.
- `clients/voice/ascolto.py:711` — `_voce_subito`. Il ciclo ha un tetto finestra+servono (12 blocchi, circa 0,96 s): non può girare all'infinito. Rischi controllati:
  - fine del flusso dentro l'allungamento: restituisce None, suona la conferma, nessun crash;
  - un blocco debole durante l'allungamento azzera il conto e fa uscire dal ciclo;
  - i blocchi restituiti sono almeno 5, più dei 3 di INIZIO_VOCE_S, quindi `registra` (`clients/voice/ascolto.py:780`) parte con voce=True.
  - **R-753-2-M1 chiusa**: con voce che parte all'ultimo blocco della finestra non suona la conferma e la richiesta è intera (27 blocchi).
  - Esito: ok.
- `clients/voice/ascolto.py:792` — riga di log con voce e volume: invariata rispetto a #753. Esito: riserva BASSA (vedi sotto).
- `tests/test_unit_voce_ascolto.py:2662` e `tests/test_unit_voce_ascolto.py:2672` — i due test nuovi coprono proprio le due riserve chiuse; per l'agente ognuno dei due mutanti fa fallire un test. Esito: ok.
- `clients/voice/ascolto.py:1209` — main passa `subito_s=SUBITO_S`. Esito: ok.

**Riserve (tutte BASSE)**
1. Costo del calcolo rms nel log della richiesta: decine di ms prima dell'invio. Già tracciata dall'agente.
2. Limite di progetto, non da correggere: la voce che parte DOPO la finestra perde ancora l'inizio sotto la conferma. Sonda: 17 blocchi inviati su 20 attesi. Vale anche per la voce a singhiozzo sul bordo (2 blocchi forti, 1 debole, poi voce): il conto torna a 0 e la conferma suona. Una finestra deve pur finire. Chi fa una pausa dopo «Hey Jarvis» paga ora 0,6 s di attesa in più prima della conferma (prima erano 0,4 s).

**Guardrail**: kernel, `_get_window`, tetto di 10 iterazioni e provider non sono toccati; nessun antipattern del Wall of Shame; eccezioni gestite (§9).

**Rischio escluso**: con microfono e rilevatore openWakeWord veri non ho potuto verificare che la coda reale di «…vis» resti sotto i 5 blocchi forti, né la durata reale delle pause tra «Hey Jarvis» e la richiesta. Non si può riprodurre qui: lo dirà la prova dal vivo, aiutata dal nuovo log.

Riga contatore #754-M1 scritta in /home/user/Gas/.claude/agents/memoria_revisore.md e committata (fa7f9f8, solo quel file). Il diff in staging è intatto.

## §5 DELTA TEST DEL MOTORE

Kernel non toccato. `tests/test_unit_voce_ascolto.py`: da 303 (base a0c200c) a 310 casi.

```
310 passed in 26.94s
```

Mutanti presi: ramo «subito» tolto, conto di fila senza azzeramento, `return letti[-1:]`, `servono = INIZIO_VOCE_S` (coda di «…vis»), niente allungamento al bordo della finestra. Equivalente: `return None` → `break` su fine flusso.

## §6 STATO CI

`gh` non autenticato nel container (GitHub passa dallo strumento MCP). Mappatura commit→run:
- 8599767, fa7f9f8 (memoria del revisore): nessuna run su questo SHA (pushati insieme a 0664325).
- 0664325: run del push del branch non letta alla scrittura; la PR #368 è stata aperta dopo.
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- #754-M1 BASSA: costo del calcolo rms su ogni blocco per il log della richiesta (decine di ms prima dell'invio).
- #754-M1 BASSA (limite di progetto): voce che parte dopo la finestra di 0,6 s perde ancora l'inizio sotto la conferma; chi fa una pausa dopo «Hey Jarvis» sente la conferma 0,6 s più tardi.
- Da provare dal vivo: che la coda reale di «…vis» resti sotto 0,4 s di voce continua.
- Aperto (priorità ALTA dell'operatore): risposte non richieste — attesa dei log del Mac.
- Le altre riserve sono in `reports/stato_progetto.md`.
