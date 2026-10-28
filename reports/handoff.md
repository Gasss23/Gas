# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — Note basse della PR #287 sul cervello forte: doctor più preciso sul PATH del timer, motivo senza prefisso doppio (chat Motore)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #291 (https://github.com/Gasss23/Gas/pull/291): con verdetto pulito del bot la mergia l'agente (CLAUDE.md §10); con riserve serve il «sì» dell'operatore. Numero e URL dalla risposta JSON di `mcp__github__create_pull_request` (`gh` nel container non è autenticato).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — R-538-1 (GAS_CLAUDE_BIN dalla shell)**: `FATTA` — `_DOTENV_CARICATE` + WARN del doctor.
- **Fetta 2 — R-538-2 + V-2 bot #287 (motivo)**: `FATTA` — niente prefisso doppio, tetto 240.
- **Fetta 3 — V-1 bot #287 (due giri) + V-3 ve #287**: `FATTA` — `_avviso_claude_timer`.
- **Fetta 4 — R-540-1 e R-540-2 (test)**: `FATTA` — review #541 APPROVATO.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  3 +++
 gas.py                             | 58 ++++++++++++++++++++++++++++++++++++++++------------------
 reports/diff_sessione.md           | 14 ++++++--------
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 20 ++++++++++----------
 tests/test_unit_dotenv.py          |  9 +++++++++
 tests/test_unit_kernel.py          | 54 ++++++++++++++++++++++++++++++++++++++++--------------
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d», e la riga di totale è tolta. Conteggi presi con i report già in stage.

## §3 GIT LOG --ONELINE (sessione)

```
ed2c430 fix(forte): note basse della #287 — doctor più preciso sul PATH del timer, motivo senza prefisso doppio
4b6538e chore(revisore): memoria review #541 — APPROVATO
de5cf2b chore(revisore): memoria review #540 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #540 (chat Motore) — sul diff di ed2c430 (prima dei test aggiunti per R-540-1/R-540-2)

## VERDETTO: APPROVATO CON RISERVE

Review #540 (chat Motore) del diff già pronto per il commit sul branch fix/note-forte-doctor. File toccati: gas.py e tests/test_unit_kernel.py. Prima ho letto CLAUDE.md, la parte di stato_progetto che serviva e la mia memoria.

**Cosa ho esaminato nel diff**
- `gas.py:449` — `_avviso_claude_timer` restituisce un motivo, oppure None se il timer trova `claude`. Ho cercato falsi OK nuovi: non ce ne sono.
  - GAS_CLAUDE_BIN relativo → WARN.
  - GAS_CLAUDE_BIN assoluto ma non preso dal .env → WARN.
  - Conta solo il primo venv che ha `bin/activate`, come fa scripts/notte/com.gas.notte.plist:15.
  - /usr/local/bin conta solo su Linux, quindi niente falso OK sul Mac con Homebrew Intel.
  - Se il percorso indicato non esiste, `shutil.which` dà None e il doctor dà già WARN prima di arrivare qui.
  - Esito: ok.
- `gas.py:627` — `_DOTENV_CARICATE.update(caricate)` contiene solo i nomi scritti davvero dal .env. Se la variabile c'è sia nella shell sia nel .env, vince la shell, il nome non entra nell'insieme e il doctor dà WARN: falso allarme, nel verso prudente.
  - Effetti collaterali: la variabile globale si aggiorna solo all'avvio della CLI (`gas.py:6066`). In pytest c'è GAS_NO_DOTENV, quindi l'insieme resta vuoto. tests/test_unit_dotenv.py ci lascia dentro nomi GAS_T_*, che non danno fastidio.
  - Il test fa add e discard dentro un `finally` (`tests/test_unit_kernel.py:11210`).
  - Esito: ok, con la riserva R-540-1.
- `gas.py:439` — `_motivo_forte` toglie il prefisso «claude-cli: », tiene «429 » e taglia a 240 caratteri.
  - Fughe di dati: tutti i raise di brains/claude_cli.py sono testi fissi. L'unica parte variabile è il timeout (un numero). `_prefisso_limite` restituisce solo «429 » oppure "". Il messaggio del login entra intero.
  - Esito: ok.
- `gas.py:466` — il confronto con realpath: vedi la riserva R-540-2.
- `tests/test_unit_kernel.py:11209` — T99s copre tre casi: solo PATH → WARN, assoluto dalla shell → WARN, assoluto dal .env → OK. Esito: ok.
- `tests/test_unit_kernel.py:11233` — T99t: col secondo venv dà l'avviso, col link simbolico no, /usr/local/bin vale solo con linux=True. Esito: ok.

**Prove eseguite**
- Suite del kernel rifatta: 1057 PASS, 0 FAIL.
- Mutanti (gas.py ripristinato, zero differenze):
  - con «da_dotenv» ignorato → T99s e T99t FAIL;
  - con «qualsiasi venv» invece del primo → T99t FAIL;
  - senza realpath sul binario → T99t FAIL;
  - senza realpath sulle cartelle → il mutante sopravvive.

**Finding**
- **R-540-1 BASSA**: nessun test collega `_carica_dotenv` a `_DOTENV_CARICATE`. T99s aggiunge il nome a mano, quindi togliendo `gas.py:627` non fallisce nulla e potrebbe tornare il WARN sempre acceso o la regressione inversa senza che nessun test se ne accorga. Rimedio: in tests/test_unit_dotenv.py controllare che il nome caricato finisca in `gas._DOTENV_CARICATE`, e che non ci finisca quando la shell vince.
- **R-540-2 BASSA**: il mutante con realpath tolto alle cartelle (`gas.py:466`) sopravvive. L'effetto sarebbe solo un falso WARN, per esempio con la radice del repo sotto un collegamento simbolico come /tmp → /private/tmp sul Mac.
- **R-540-3 BASSA (c'era già prima)**: su Linux il venv è contato come «visto dal timer» per analogia col plist, ma nel repo non c'è un'unità systemd che lo attivi. Lanciare `venv/bin/python` non mette `venv/bin` nel PATH, quindi potrebbe esserci un falso OK sulla VPS.

**Cosa non ho verificato**: il comportamento reale di launchd e systemd e del PATH di ~/.zshenv sul Mac e sulla VPS, perché qui non si possono riprodurre. Non ho rifatto pytest completo (2282 passed è un dato dichiarato dall'agente); ho rifatto solo la suite del kernel.

**Memoria**: riga #540 (chat Motore) e una lezione nuova (uno stato simulato a mano nel test va collegato da un altro test alla funzione vera) aggiunte in /home/user/Gas/.claude/agents/memoria_revisore.md, commit de5cf2b. Il diff in revisione resta intatto e pronto per il commit.

### Review #541 (chat Motore) — sul diff finale di ed2c430

## VERDETTO: APPROVATO

Review #541 (chat Motore): rifatta la review sul diff pronto per il commit (gas.py, tests/test_unit_dotenv.py, tests/test_unit_kernel.py). gas.py è identico, byte per byte, a quello approvato con riserve nella #540.

**Cosa ho esaminato**
- `tests/test_unit_dotenv.py:127` — il nuovo test collega `_carica_dotenv` a `_DOTENV_CARICATE`. Il nome letto dal file entra, quello già impostato nella shell no. Ho controllato due rischi:
  - lo stato globale sporcato tra un test e l'altro: no, il test sostituisce l'insieme con `monkeypatch.setattr` e lo ripristina da solo;
  - il caricamento del .env spento da GAS_NO_DOTENV: no, la fixture `env` toglie quella variabile.
  - Esito: ok, R-540-1 chiusa.
- `tests/test_unit_kernel.py:11236` — T99t ora prova anche una radice raggiunta da un collegamento simbolico (`linkroot99`). Esito: ok, R-540-2 chiusa.
- `gas.py:627` e `gas.py:466` — le due righe di codice che i test nuovi proteggono. Esito: ok.

**Prove rifatte da me** (gas.py ripristinato, zero differenze)
- `gas.py:627` tolta (il loader non registra più i nomi caricati) → il test dotenv nuovo FALLISCE.
- `gas.py:466` con `vedute = set(cartelle)`, cioè senza risolvere i collegamenti simbolici delle cartelle → T99t FALLISCE.
- Suite senza modifiche: kernel 1057 PASS, 0 FAIL; test_unit_dotenv 11 passed.

**Finding**
- **R-541-1 COSMETICA**: `linkroot99` punta alla radice stessa, quindi crea un ciclo, e resta nella cartella temporanea del test. Oggi non fa danni (la suite passa e la pulizia non segue i collegamenti). Un futuro test che scorre quella cartella seguendo i collegamenti ci girerebbe dentro all'infinito: meglio cancellarlo subito dopo l'uso.
- R-540-3 (venv su Linux senza unità systemd) l'agente dichiara di tracciarla in stato_progetto come aperta. Non è nel diff e non l'ho verificata.

**Cosa non ho verificato**: il comportamento reale di launchd e systemd, perché qui non si può riprodurre. Non ho rifatto pytest completo, solo test_unit_dotenv e la suite del kernel.

**Memoria**: riga #541 aggiunta in /home/user/Gas/.claude/agents/memoria_revisore.md, commit 4b6538e. Nella #540 c'era già il commit de5cf2b con la riga #540 e la lezione. Il diff in revisione resta intatto e pronto per il commit.

## §5 DELTA TEST DEL MOTORE

Kernel: 1057 → 1057 PASS (nessun check nuovo: T99s, T99t, T99u e T99v hanno più casi dentro). Conteggi del container locale: la CI ne conta di più (es. 1063 su #287, V-2 bot #287).

```
=== RIEPILOGO: 1057 PASS, 0 FAIL ===
```

pytest (`python3 -m pytest -q tests`, prima dei test aggiunti per la #541): `2282 passed, 61 skipped in 192.48s (0:03:12)`. Dopo: `python3 -m pytest -q tests/test_unit_dotenv.py` → `11 passed in 6.00s`. Nessun FAIL.

## §6 STATO CI

`gh` nel container non è autenticato: run lette con lo strumento GitHub della sessione (`actions_list`, branch fix/note-forte-doctor).

Mappatura commit→run:
- de5cf2b, 4b6538e → nessuna run su questi SHA (pushati insieme a ed2c430).
- ed2c430 → run non ancora disponibile alla scrittura dell'handoff (handoff-check rosso atteso: l'handoff arriva col commit dopo).
- commit di fine-task → run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- **R-540-3** (BASSA, review #540): su Linux il venv conta come visto dal timer, ma nessuna unità systemd lo attiva (falso OK possibile sulla VPS).
- **R-541-1** (COSMETICA, review #541): `linkroot99` in T99t è un collegamento ciclico lasciato nella cartella temporanea.
