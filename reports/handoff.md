# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-28 — chat Motore: riserve del punto 3 della RIPARTENZA (cervello forte e doctor)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #290 (https://github.com/Gasss23/Gas/pull/290): review #540 APPROVATO CON RISERVE, quindi decide l'operatore (CLAUDE.md §10). Numero e URL dalla risposta JSON dello strumento GitHub `create_pull_request` (`gh` non autenticato in questo ambiente).

---

## §1 SCOPE & ESITO FETTE

- **Fetta 1 — R-538-1, WARN se GAS_CLAUDE_BIN sta solo nella shell**: `FATTA` — `_chiavi_dotenv` (solo i nomi) e WARN col rimedio.
- **Fetta 2 — R-538-2 e V-2 bot #287, motivo del forte**: `FATTA` — senza «claude-cli: » ripetuto, tetto 300.
- **Fetta 3 — V-1 bot #287, falsi WARN del doctor**: `FATTA` per `/usr/local` su Linux e i collegamenti; `DEFERITA — ~/.zshenv`: sbaglia nel verso prudente (WARN in più, mai un OK sbagliato).

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |  2 ++
 gas.py                             | 45 ++++++++++++++++++++++++++++++++++++++++-----
 reports/diff_sessione.md           |  7 +++++--
 reports/stato_progetto.md          |  4 ++--
 reports/ultimo_report.md           | 15 ++++++++++-----
 tests/test_unit_kernel.py          | 50 ++++++++++++++++++++++++++++++++++++++++++++------
 reports/handoff.md                 | n/d (commit finale)
```

NB: per `reports/handoff.md` il conteggio non è misurabile al momento della scrittura (il file sta nel commit finale), quindi «n/d» e niente riga di totale. Conteggi presi con i report in stage.

## §3 GIT LOG --ONELINE (sessione)

```
cceadcc fix(forte): riserve del punto 3 — WARN se GAS_CLAUDE_BIN sta solo nella shell, motivo senza prefisso ripetuto e non troncato, /usr/local su Linux
e6604cb chore(revisore): memoria review #540 — APPROVATO CON RISERVE
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione. Il suo hash è nel `git log` del branch dopo il push.

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #540 (chat Motore) — sul diff di cceadcc

## VERDETTO: APPROVATO CON RISERVE

Il diff in stage tocca gas.py e tests/test_unit_kernel.py. Ho ripetuto la suite del kernel: 1064 PASS, 0 FAIL. Ho provato tre mutanti e alla fine ho ripristinato gas.py: lo stage è invariato e non ci sono modifiche fuori stage.

Elementi esaminati:
- gas.py:434 — `_motivo_forte` toglie il prefisso «claude-cli: » e conserva «429 », con un tetto di 300 caratteri — rischio esaminato: che cambi la classificazione QUOTA o che lasci uscire dati personali — ok. La classificazione resta su `str(e)` in `_classify_provider_error` (gas.py:4935); il motivo è solo testo mostrato. Resta valida solo la prima riga e il controllo «solo RuntimeError con prefisso fisso» è invariato. Prova diretta: «429 claude-cli: limite» diventa «429 limite». Il messaggio del login arriva intero (lo verifica T99u).
- gas.py:463 — `_chiavi_dotenv` — rischio esaminato: che esponga valori — ok. Restituisce solo i nomi delle chiavi (prova con `SEGRETO=abc123`: esce solo la chiave), non fa log e non carica niente in os.environ. Se il file manca o non si legge restituisce None, senza crash (fail-safe §9).
- gas.py:5022 — WARN «impostata solo nella shell» — rischio esaminato: che scatti a torto — ok. Il mutante che toglie il ramo fa fallire T99w. Il template scripts/notte/com.gas.notte.plist non ha EnvironmentVariables, quindi il caso «.env assente ma GAS_CLAUDE_BIN dal plist» non esiste nel repo. Con un plist personalizzato, oppure con un export in ~/.zshenv (il plist lancia `zsh -c`, che legge ~/.zshenv), il WARN sarebbe falso. È però un falso WARN e non un falso OK, quindi va nel verso prudente e l'exit code resta 0.
- gas.py:455 — /usr/local/bin e /usr/local/sbin contano solo su Linux, con confronto anche a percorsi risolti — ok. Il mutante «sempre Linux» fa fallire T99x.
- tests/test_unit_kernel.py:11216 — ripristino dell'ambiente dopo il test — ok. GAS_NO_DOTENV torna a "1", come lo imposta globalmente tests/test_unit_kernel.py:53. Il `.env` di prova viene cancellato, PATH e GAS_CLAUDE_BIN vengono ripristinati. `gas.sys.platform` torna al valore originale nel `finally` di T99x.

Riserve:
- R-540-1 BASSA — gas.py:460: il mutante che toglie `{os.path.realpath(v) for v in vedute}` sopravvive con la suite verde. T99x mette il collegamento solo dalla parte del binario (lnk99 → /usr/bin); manca un caso col collegamento dalla parte delle cartelle note, per esempio `.venv` collegato altrove.
- R-540-2 BASSA — gas.py:478: `_chiavi_dotenv` conta anche righe che `_carica_dotenv` scarta (virgolette non chiuse). Conta anche `GAS_CLAUDE_BIN=` con valore vuoto. In questi casi rari il doctor dà un falso OK.
- Nota, non bloccante e già presente prima: il doctor cerca il `.env` nella cartella da cui lo lanci (gas.py:4963), mentre `_carica_dotenv` lo legge accanto a gas.py. Se lanci il doctor da un'altra cartella, il WARN può essere falso, sempre nel verso prudente.

Antipattern di CLAUDE.md sez. 5: niente slicing della cronologia (gli slicing nel diff sono solo su stringhe), niente simulazione di tool. Il tetto delle 10 iterazioni e `_get_window` non sono toccati.

Rischio escluso: non ho verificato il comportamento reale su macOS (launchd con `zsh -c` e ~/.zshenv, /bin non collegato): non è riproducibile in questo ambiente Linux. Il caso Mac l'ho visto solo simulando `sys.platform="darwin"` in T99x.

Riga contatore #540 scritta e committata: e6604cb, solo /home/user/Gas/.claude/agents/memoria_revisore.md. Lezione nuova aggiunta: un confronto a collegamenti risolti va provato con un collegamento da ciascuna delle due parti.

## §5 DELTA TEST DEL MOTORE

Suite kernel: 1061 → 1064 PASS (T99w, T99x, T99y nuovi; T99s e T99u aggiornati), 0 FAIL. Il valore di main è stato misurato in un worktree a `094eb57`.

```
=== RIEPILOGO: 1064 PASS, 0 FAIL ===
```

pytest (tutti i file tranne la suite kernel): `2282 passed, 61 skipped in 214.81s (0:03:34)`.

## §6 STATO CI

CI letta con lo strumento GitHub della sessione: `gh run list` non è disponibile (`gh` non autenticato).

Mappatura commit→run:
- `e6604cb`: nessuna run su questo SHA (pushato insieme a `cceadcc`).
- `cceadcc`: pushato prima dell'apertura della PR #290; la run CI del push sul branch non l'ho letta alla scrittura dell'handoff, quindi l'esito non è dichiarato.
- commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-540-1 BASSA: manca un test col collegamento dalla parte delle cartelle note (`.venv` collegato altrove).
- R-540-2 BASSA: `_chiavi_dotenv` conta righe che il caricamento scarta (virgolette non chiuse, valore vuoto), quindi un falso OK in casi rari.
- Il PATH di `~/.zshenv` non è considerato (falso WARN, verso prudente).
