# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-11 — chiavi private e credenziali vietate (V-1 verifica esterna #184)

---

## §0 DECISIONI UMANE RICHIESTE

1. Nessuna: l'operatore ha già chiesto il merge della PR #188 dopo la correzione delle varianti.

---

## §1 SCOPE & ESITO

- **Varianti dei nomi** (scelta dell'operatore «chiudi le varianti e poi mergia», finding BASSI di bot e verifica esterna #188): `FATTO` — copie, prefissi/suffissi, `.kube`, `.docker`, `.npmrc`, service-account, token(s).json, wallet.dat. Review #291.
- **Chiavi private e credenziali vietate**: `FATTO` — decisione dell'operatore («sì, vietale»). `_CHIAVE_PRIVATA_RE` in `_nome_da_segreto`; `livello_scrittura` → 3 per i nomi da segreto.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   5 +++++
 modules/gate/gate.py               |  28 +++++++++++++++++++++++++++-
 reports/diff_sessione.md           |   8 +++++---
 reports/handoff.md                 | 150 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------------------
 reports/stato_progetto.md          |   2 +-
 reports/ultimo_report.md           |  15 ++++++---------
 tests/test_unit_gate.py            |  34 +++++++++++++++++++++++++++++++++-
 tests/test_unit_kernel.py          |  35 +++++++++++++++++++++++++++++++++++
 8 files changed, 240 insertions(+), 37 deletions(-)
```

## §3 GIT LOG --ONELINE (sessione)

```
bcde62f fix(cancello): varianti dei nomi di credenziali (V-1/V-2 bot e verifica esterna #188)
8337f55 chore(revisore): memoria review #291 — APPROVATO CON RISERVE
a0614e7 docs(fine-task): report e handoff — chiavi private e credenziali vietate
17df75b feat(cancello): chiavi private e credenziali illeggibili e mai scritte (V-1 verifica esterna #184)
df1ff26 chore(revisore): memoria review #290 — APPROVATO
a51e73d chore(revisore): memoria review #289 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE

### Review #289

## VERDETTO: APPROVATO CON RISERVE

Ho letto CLAUDE.md (sezioni 5, 8, 9 e 10), `reports/stato_progetto.md` (V-1 della verifica esterna #184, R-277-1) e `.claude/agents/memoria_revisore.md`. Il diff staged ha 3 file, +80/-1. È la decisione presa dall'operatore il 2026-10-11 e chiude il finding V-1 #184 (2° giro).

**Elementi esaminati:**
- `modules/gate/gate.py:278`: nuova regex `_CHIAVE_PRIVATA_RE` con due rami. Il primo è ancorato all'inizio (`^`) e copre `id_*` ssh, `secret(s)`, `credential(s)` e le cartelle/file `.ssh`, `.gnupg`, `.aws`, `.netrc` e simili. Il secondo è ancorato alla fine (`$`) e copre i suffissi `.pem`, `.key`, `.p12`, `.pfx`, `.ppk`, `.jks`, `.keystore`, `.kdbx`.
  - Rischio esaminato: falsi positivi su file legittimi e falsi negativi su maiuscole e punti/spazi finali.
  - Provato a mano: `ID_RSA`, `server.KEY`, `x.pem.` e `x.pem ` sono negati. `monkey.py`, `secrets_manager.py`, `keys/x.txt` e `secretary.md` restano leggibili.
  - Ho passato in `_nome_da_segreto` tutti i file tracciati del repo (`git ls-files`): nessuno viene colpito, quindi nessun file del progetto diventa illeggibile per Gas.
  - Esito: riserva (R-289-1, sotto).
- `modules/gate/gate.py:297`: `_nome_da_segreto` applica entrambe le regex a ogni pezzo del percorso ripulito.
  - Rischio esaminato: un'eccezione che faccia crashare il gate.
  - Gira dentro i `try` che rispondono "negato" in caso di errore, sia in `lettura_consentita` (`modules/gate/gate.py:302`) sia in `livello_scrittura`.
  - Esito: ok.
- `modules/gate/gate.py:337`: i nomi da segreto passano a livello 3 in scrittura, con il controllo messo prima di quelli di livello 2.
  - Rischio esaminato: si indebolisce qualche guardrail? No, lo rafforza. Una conseguenza voluta: `prod.env` passa da livello 1 a 3, e così Gas non può più scrivere un file che poi non potrebbe rileggere.
  - Esito: ok.
- `tests/test_unit_kernel.py:8088`: T86 fa un round-trip agentico vero con `run_turn_scriptato`. `read_file` su `id_rsa` viene negato e il loop arriva comunque alla risposta finale (sezione 7 rispettata). Il test copre anche `conta_file` e `cerca_testo` sulla root (salta 9 voci e trova solo `secretary.md`), più `write_file` verso `nuovo.pem` (negato, il file non viene creato).
  - Nessuna simulazione dell'output dei tool: passa da `execute_tool_call`, cioè dai tool reali.
  - Esito: ok.
- `tests/test_unit_gate.py:566`: due test parametrici, uno sui nomi negati in lettura e scrittura (25 casi), uno sui nomi simili che restano leggibili (9 casi).
  - Esito: ok.

**Risultati che ho riprodotto:** `pytest tests/test_unit_gate.py` 317 passed; `tests/test_unit_kernel.py` 810 PASS / 0 FAIL, T86a–d PASS. Nessuno slicing della history e nessun tocco a `_get_window`, al limite di 10 iterazioni o al limite di 8k di output.

**Riserve:**
- **R-289-1 (BASSA): le copie dei file con suffisso restano leggibili.** `x.pem~`, `x.key.bak` e `server.pem.old` restano leggibili (verificato: `lettura_consentita` restituisce True, livello di scrittura 1).
  - Motivo: il ramo dei suffissi è ancorato alla fine del nome, quindi il suffisso aggiunto dalla copia lo fa saltare.
  - Le altre famiglie le copie le coprono già: `prod.env~` e `id_rsa.bak` sono negati.
  - Correzione possibile: sostituire l'ancora finale con un lookahead che escluda solo le lettere, come fa già `_SEGRETO_RE`. Va però controllato che non colpisca nomi legittimi (es. `x.keyboard`).
- **R-289-2 (COSMETICA): vengono bloccati anche file innocui con quei nomi.** `secret.py`, `credentials.py` e qualunque cartella `secrets/` diventano illeggibili e non scrivibili. È un blocco in eccesso che ritengo accettabile: oggi nel repo nessun file è colpito e va nella direzione "robustezza > potenza".

**Rischio escluso:** non ho verificato il comportamento sui link simbolici (symlink) verso chiavi fuori dalla root di Gas, né su un filesystem reale della VPS non sensibile alle maiuscole. Mi affido al controllo già esistente sul percorso risolto in `lettura_consentita`, che questo diff non tocca e che non ho rieseguito con symlink reali. Resta anche il limite già dichiarato: il divieto è per nome, quindi un file di segreti con un nome qualunque non è coperto.

**Memoria:** ho aggiunto in `/home/user/Gas/.claude/agents/memoria_revisore.md` la riga #289 e una lezione (provare le copie `~`/`.bak`/`.old` di ogni famiglia di nomi). È committata con lo script (a51e73d).

### Review #290 (dopo la correzione di R-289-1)

## VERDETTO: APPROVATO

Rivisto il diff staged attuale, delta compreso (3 file, +83/-1). La correzione chiude R-289-1.

**Elementi esaminati:**
- `modules/gate/gate.py:286`: il ramo dei suffissi (`.pem`, `.key`, `.p12`, `.pfx`, `.ppk`, `.jks`, `.keystore`, `.kdbx`) ora usa `(?![a-z])` al posto di `$`, come `_SEGRETO_RE`.
  - Rischio esaminato: le copie dei file di chiavi che passano ancora, e nomi legittimi bloccati per errore.
  - Prove a mano:
    - Negati in lettura e a livello 3 in scrittura: `x.pem~`, `x.key.bak`, `server.pem.old`, `y.pfx1`, `x.key_old`, `x.key-old`, `a.ppk2`, `x.pem.`.
    - Restano leggibili: `x.keyboard`, `a.keys.md`, `b.pemmican`, `monkey.py`.
    - Nessuno dei file tracciati del repo è colpito: `git ls-files` passato in `_nome_da_segreto` dà lista vuota.
  - Esito: ok.
- `modules/gate/gate.py:297`: `_nome_da_segreto` non cambia rispetto alla #289. Gira sempre dentro i `try` che, in caso di errore, negano (lettura) o mettono il livello 3 (scrittura).
  - Esito: ok.
- `tests/test_unit_gate.py:569`: aggiunti i casi negati `x.pem~`, `x.key.bak`, `server.pem.old`, `y.pfx1`, che dimostrano la chiusura di R-289-1.
  - Esito: ok.
- `tests/test_unit_gate.py:583`: aggiunti i casi che restano leggibili `dati/x.keyboard`, `dati/a.keys.md`, `dati/b.pemmican`, che fissano il confine del lookahead.
  - Esito: ok.
- `tests/test_unit_kernel.py:8088`: T86 non cambia. Il round-trip agentico resta vero, con i tool reali e senza simulazione.
  - Esito: ok.

**Risultati riprodotti:** pytest `tests/test_unit_gate.py` 324 passed; kernel 810 PASS / 0 FAIL. Nessuno slicing della history. Nessun tocco a `_get_window`, al limite di 10 iterazioni né al limite di 8k di output.

**Nota, non bloccante:** il lookahead allarga un po' il blocco per eccesso. Ora sono negati anche nomi come `api.key.json` o `note.key.md`. È lo stesso tipo di compromesso di R-289-2 (prudenza invece di potenza) e per me è accettabile.

**Rischio escluso:** non ho verificato i link simbolici verso chiavi fuori dalla root, né filesystem che ignorano le maiuscole sulla VPS. Il controllo sul percorso risolto in `lettura_consentita` non è toccato da questo diff e non l'ho riprovato con symlink reali. Resta anche il limite già noto: il divieto vale per nome, quindi un file di segreti con un nome qualsiasi non è coperto.

**Memoria:** aggiunta la riga #290 in `/home/user/Gas/.claude/agents/memoria_revisore.md`, committata con lo script (df1ff26). Nessuna lezione nuova.

### Review #291 (varianti: V-1/V-2 bot e verifica esterna #188)

## VERDETTO: APPROVATO CON RISERVE

Prima della review ho letto CLAUDE.md, le voci R-289 di reports/stato_progetto.md e la coda di .claude/agents/memoria_revisore.md. Nel diff staged non c'è slicing della history, nessun output di tool simulato e nessun cambio ai limiti fissi (10 iterazioni, 8k di output, `_get_window`). Le due funzioni di controllo restano "fail-closed": in caso di errore negano invece di lasciar passare.

**Elementi esaminati**
1. `modules/gate/gate.py:283`: `_CHIAVE_PRIVATA_RE` ora usa come bordo «niente lettera prima e dopo» (`(?<![a-z])…(?![a-z])`) per chiavi ssh, secret(s), credential(s), service-account, token(s) con estensione json, txt o yaml, e wallet.dat.
   - Rischio: falsi negativi sulle copie e sui nomi con prefisso o suffisso; falsi positivi su nomi innocui.
   - Prove dirette (lettura / livello di scrittura):
     - `backup_id_rsa`, `token.json.bak`, `access_token.json`, `Token.JSON`, `Secret.TXT`: negati in lettura, livello 3 in scrittura.
     - `valid_rsa`, `idx_rsa`, `tokenizer.json`, `secretary.md`: leggibili.
   - Esito: ok.
2. `modules/gate/gate.py:287`: i dotfile sono ancorati a `^` con `(?![a-z])`, e si aggiungono kube, docker e npmrc.
   - Rischio: colpire file di progetto legittimi.
   - Prove: `.dockerignore` resta leggibile (livello 1) e `Dockerfile` resta a livello 2. `.Docker/config.json`, `x/.npmrc~` e `.NPMRC` sono negati (il percorso viene portato in minuscolo da `_normalize_path` prima del controllo). `.aws-sam/x` e `.ssh-agent` sono bloccati per eccesso, accettabile.
   - Esito: ok.
3. `modules/gate/gate.py:302` (contesto, `_nome_da_segreto`): il controllo per pezzo di percorso, con punti e spazi finali tolti, è invariato. Su tutti i file di `git ls-files` → HIT [] (nessun file del repo colpito).
   - Esito: ok.
4. `tests/test_unit_gate.py:428`: `.npmrc` è tolto dai casi che richiedono firma (livello 2) perché ora è livello 3. Il test `tests/test_unit_gate.py:569` lo copre come illeggibile e mai scrivibile.
   - Rischio: un test tolto per far passare la suite.
   - Esito: ok, il caso è spostato e non perso.
5. `tests/test_unit_gate.py:588`: i casi «nomi simili restano leggibili» perdono `credentials_guide.md` e `secret_sauce.md`, ora bloccati per eccesso come previsto da R-289-2, e guadagnano valid_rsa, tokenizer.py, tokens.md e kubectl.md.
   - Esito: ok.

Ho rieseguito `pytest tests/test_unit_gate.py`: 344 passed.

**Riserve**
- R-291-1 (BASSA): `kubeconfig` senza punto iniziale (es. `dati/KUBECONFIG` → leggibile, livello 1) e `mywallet.dat` (una lettera prima di «wallet») restano leggibili. È lo stesso limite dichiarato del divieto per nomi (R-223-2). Va tracciata in stato_progetto.md, oppure chiusa aggiungendo `kubeconfig` all'elenco se l'operatore lo vuole.

**Rischio escluso**
- La suite kernel (810 PASS / 0 FAIL dichiarati) non l'ho rieseguita: ho rieseguito solo la suite del gate. Il diff non tocca gas.py, ma il kernel richiama `lettura_consentita` sul percorso risolto dei symlink, e quel percorso non l'ho provato end-to-end.
- Non ho verificato i nomi con lettere non ASCII (es. «é» prima di «secret»): il bordo `[a-z]` è solo ASCII e potrebbe bloccare per eccesso. Non è un rischio di fuga.

Memoria aggiornata (riga #291 più una lezione) e committata con lo script: commit 8337f55.

## §5 DELTA TEST DEL MOTORE

Kernel 806 → 810 PASS / 0 FAIL in locale (T86a–d). pytest completo 1032 passed (`tests/test_unit_gate.py` 344).

## §6 STATO CI

`a0614e7`: unit-suite e handoff-check success; verifica-bot neutral (APPROVATO CON RISERVE, tocca la memoria del revisore). Run del commit di questa correzione non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

R-289-2 (COSMETICA, accettata): blocco per eccesso su nomi innocui (`secret.py`, `credentials_guide.md`, `note.key.md`). R-291-1 (BASSA): `kubeconfig` senza punto e `mywallet.dat` leggibili. Divieto per nomi (R-223-2).
