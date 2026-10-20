# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-20 (dopo il merge di #228) — avviso sui file nuovi delicati, fonti di studio solo dentro knowledge/

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR: l'agente mergia da solo solo con un APPROVATO pulito del bot (CLAUDE.md §10); altrimenti decide l'operatore.
2. Togliere dal progetto claude.ai le copie di `briefing_architettura_voce.md` e `recinto_autonomia.md` (l'agente non vi ha accesso).

---

## §1 SCOPE & ESITO FETTE

- **R-223-2 (avviso sui file nuovi delicati)**: `FATTA` — review #386 BOCCIATO → #387 APPROVATO CON RISERVE.
- **V-1 bot #228 (fonti solo dentro knowledge/)**: `FATTA` — review #387.

---

## §2 GIT DIFF --STAT (sessione)

```
 .claude/agents/memoria_revisore.md |   2 ++
 .github/workflows/ci.yml           |   7 +++++++
 gas.py                             |  43 +++++++++++++++++++++++++++++++++++++++++--
 modules/gate/gate.py               |  40 ++++++++++++++++++++++++++++++++++++++++
 reports/diff_sessione.md           |  17 ++++++++---------
 reports/handoff.md                 | 127 +++++++++++++++++++++++++++++++++++++++++++++++++++++--------------------------------------------------------------------------
 reports/stato_progetto.md          |   2 ++
 reports/ultimo_report.md           |  11 +++++------
 tests/test_unit_gate.py            |  17 +++++++++++++++++
 tests/test_unit_ingest_fonti.py    |  42 ++++++++++++++++++++++++++++++++++++++++++
 tests/test_unit_kernel.py          |  38 ++++++++++++++++++++++++++++++++++++++
 tools/ingest_knowledge.py          |   9 +++++++++
 12 files changed, 264 insertions(+), 91 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
1ea5346 Merge remote-tracking branch 'origin/main' into feat/merge-automatico-z1xjx2
ec83cf7 Merge remote-tracking branch 'origin/feat/merge-automatico-z1xjx2' into feat/merge-automatico-z1xjx2
2074c27 feat(avvisi): avviso per i file nuovi che sembrano delicati (R-223-2); fonti di studio solo dentro knowledge/
83b68e6 chore(revisore): memoria review #387 — APPROVATO CON RISERVE
f1754e3 chore(revisore): memoria review #386 — BOCCIATO
```

---

## §4 VERDETTO DEL REVISORE (per commit motore)

### Review #386

## VERDETTO: BOCCIATO

Ho letto le tre fonti obbligatorie: CLAUDE.md (sez. 5, 8 e 9), reports/stato_progetto.md (le voci su R-223-2 e la decisione 12 del 19-20 ottobre) e la mia memoria (lezione #382 sul limite Telegram).

Elementi del diff esaminati:
1. `modules/gate/gate.py:516`: `sembra_delicato` classifica il nome del file (minuscolo grazie al casefold di `_normalize_path`). Se qualcosa va storto restituisce True, e il test `test_sembra_delicato` passa (18 casi, riprodotto). Rischio esaminato: falsi positivi su documenti normali. Sondato: `dati/cronologia.md`, `dati/sessione_marketing.md`, `dati/credito_clienti.csv` e `dati/monkey.md` danno tutti True, perché le parole «cron», «session», «cred» e «key» vengono cercate come pezzi dentro il nome. Esito: **riserva R-386-2 BASSA**. La regola dell'operatore dice che i documenti normali passano in silenzio. Proposta: confrontare le parole del nome divise su `_`, `-`, `.` e spazio, oppure fare il controllo per nome solo sulle estensioni che non sono documenti.
2. `gas.py:2643`: `_invia_avvisi_file` manda un solo messaggio con al massimo 10 percorsi, ognuno tagliato a 200 caratteri con `tronca_visibile`, ma il testo intero non ha un tetto di lunghezza. Rischio esaminato: il caso peggiore contro i 4096 caratteri di Telegram (è la lezione #382). Sondato: 10 percorsi `.json` di livello 1 con cartelle di emoji (975 byte, livello 1 confermato da `livello_scrittura`). Ogni emoji vale 2 unità per Telegram, quindi 200 caratteri diventano 400 unità; il totale fa 4098 unità. `invia_notifica` (`modules/telegram/bot.py:271`) rifiuta il messaggio intero e resta solo un warning nel log. Così chi scrive i file (anche un modello manipolato da un testo letto) può spegnere proprio l'avviso pensato per lui. Esito: **BLOCCO R-386-1 MEDIA**, lo stesso difetto di R-382-1. Correzione: riusare il ciclo di riduzione di `_invia_avvisi_lead` (`gas.py:2634`): togliere percorsi finché `lunghezza_telegram` sta sotto `TELEGRAM_MAX_CHARS` e contare quelli tolti. In alternativa un helper comune. Serve un test con percorsi di emoji.
3. `gas.py:3793`: `_nuovo` viene calcolato prima della scrittura e il controllo sta in un try/except separato dopo `write_text`. Rischio esaminato: che l'avviso cambi l'esito della scrittura (§9), o che un file esistente o di livello 2 o 3 venga segnalato. Esito: ok. `.py` e `.sh` sono già di livello 2 e restano fuori, come previsto.
4. `gas.py:3845` e `gas.py:4125`: la lista viene azzerata a inizio turno e svuotata nel finally, dopo l'avviso dei lead. Rischio esaminato: avvisi che passano da un turno all'altro, eccezioni nel finally. Esito: ok, il metodo non lancia eccezioni.
5. `tests/test_unit_kernel.py:5967`: T74b5 R-223-2 copre file nuovo, file esistente, documento e lista svuotata. Esito: ok, ma manca il caso della lunghezza (vedi punto 2).

Nessuna violazione del Wall of Shame: niente slicing della history, `_get_window` non è toccata, il tetto delle 10 iterazioni resta, nessuna simulazione dei tool.

Rischi esclusi:
- Suite kernel completa e `pytest tests/` non rieseguiti da me: mi baso sui numeri dichiarati (946/0 e 715) più i 18 casi nuovi che ho riprodotto.
- Nessun test di mutazione.
- I file creati da `run_command` (shell) non fanno scattare l'avviso. È fuori dall'ambito della fetta, che parla solo di `write_file`, ma va dichiarato come limite.
- Invio reale su Telegram non verificato: in sviluppo non c'è un token vero.

Memoria: aggiunta la riga #386 in /home/user/Gas/.claude/agents/memoria_revisore.md con la lezione «ogni nuovo messaggio accorpato va ricontrollato contro i 4096 caratteri di Telegram; `tronca_visibile` a n caratteri vale fino a 2n unità». Lanciato `scripts/commit_memoria_revisore.sh`: è terminato senza output, quindi non ho la conferma esplicita che il commit sia avvenuto.

### Review #387

## VERDETTO: APPROVATO CON RISERVE

Ho rivisto di nuovo il diff staged che avevo bocciato nella review #386. Le tre correzioni funzionano e i test le coprono; resta una sola riserva BASSA (R-387-1, sotto).

**Letture fatte prima della review**: CLAUDE.md (sez. 5, 8, 9), `reports/stato_progetto.md` (voci R-223-2 e R-386), coda di `.claude/agents/memoria_revisore.md` (#382–#386, compresa la lezione sul limite di 4096 unità di Telegram per i messaggi accorpati).

**Elementi del diff esaminati**
- `gas.py:2662` — ciclo che riduce `k` finché `lunghezza_telegram(_componi(k))` sta sotto `TELEGRAM_MAX_CHARS`, come per i lead. Rischio esaminato: testo esterno che spegne l'avviso (R-386-1). **Esito: ok.** Con il loop spento (mutazione in un worktree temporaneo, ora rimosso) T74b5 R-386-1 fallisce; col codice staged passa con 1 messaggio da 1986 caratteri. Con `k=0` restano l'intestazione e «… e altri N». Tutto è dentro un try/except che fa solo warning, come chiede il §9.
- `gas.py:3795` — `_nuovo = not path.exists()` calcolato prima della scrittura; l'aggiunta alla lista avviene solo con `livello == LIVELLO_LIBERO`, dentro un try a parte. Rischio esaminato: l'avviso cambia l'esito della scrittura, o usa variabili fuori portata. **Esito: ok.** `livello` e `rel_root` sono quelli già ricalcolati sul percorso risolto (`gas.py:3765`, `gas.py:3752`). La lista si azzera a inizio turno e nel `finally` (`gas.py:4133`).
- `modules/gate/gate.py:530` — `sembra_delicato` ora confronta parole intere con `_NOMI_DELICATI`. Rischio esaminato: falsi allarmi su documenti normali (R-386-2). **Esito: riserva BASSA (R-387-1).** I quattro documenti citati ora tornano False. Però le parole si cercano solo prima del PRIMO punto: `nome.split(".")[0]` taglia via il resto, quindi il `.` nella regex non serve e il commento dice il falso. Ho sondato:
  - `x.secret.md`, `id_rsa.txt`, `accesstoken.md` → False;
  - `.fish` (livello 1) non è segnalato.

  È un avviso solo informativo e non tocca il cancello, quindi non blocca. `.sh` e `.py` non c'entrano: sono già di livello 2.
- `tools/ingest_knowledge.py:153` — `abs_path.resolve().relative_to((REPO_ROOT/"knowledge").resolve())`. Rischio esaminato: fonti fuori da knowledge/ via «..», symlink o percorso assoluto (V-1 bot #228). **Esito: ok.** I 4 casi da rifiutare falliscono col controllo spento e passano col codice staged; il caso accettato passa. Anche `REPO_ROOT / "/etc/hostname"` (assoluto) viene rifiutato. L'unica fonte di `knowledge/sources.yaml` (`knowledge/test_source.txt`) resta valida.
- `.github/workflows/ci.yml:157` — nuovo step `if: always()` con pipefail. Rischio esaminato: test nuovo che la CI non lancia mai. **Esito: ok.** Il YAML è valido e non c'è nessun `paths-ignore`.
- `tests/test_unit_ingest_fonti.py:31` — test parametrico; il fixture fa monkeypatch di `REPO_ROOT` su tmp_path. **Esito: ok.**

**Wall of Shame**: nel diff non c'è slicing della storia né simulazione dell'output dei tool. Il tetto di 10 iterazioni e `_get_window` non sono toccati.

**Esiti riprodotti**: kernel 947 PASS / 0 FAIL; gate (`test_sembra_delicato`) + ingest 34 passed; YAML ok. Con la mutazione il kernel dà 945/2: T74b5 R-386-1 e T74b6 R-382-1, perché la stessa sostituzione ha spento anche il loop dei lead. Entrambi i FAIL sono mirati.

**Riserva da tracciare in `reports/stato_progetto.md`**
- **R-387-1 (BASSA)**: in `sembra_delicato` le parole delicate si cercano solo prima del primo punto del nome. Correzione proposta: `re.split` su tutto il nome senza l'ultima estensione. Valutare `.fish` tra le estensioni delicate.

**Rischi esplicitamente esclusi**
- Invio reale su Telegram: non l'ho verificato; ho usato solo `_TgFinto`, quindi l'invio vero lo vedrà l'operatore.
- Esecuzione dello step nuovo sulla CI di GitHub: non verificata, posso solo validare il YAML in locale.
- Suite pytest completa da 1558: non rilanciata, ho eseguito solo le parti toccate.
- Symlink nei test di ingest su Windows: non verificato, Windows non è una piattaforma di Gas.

**Memoria**: ho aggiunto la riga #387 in `/home/user/Gas/.claude/agents/memoria_revisore.md` e lanciato `scripts/commit_memoria_revisore.sh`, che non ha stampato errori. Nessuna lezione nuova.

---

## §5 DELTA TEST DEL MOTORE

tests/test_unit_kernel.py in locale: 944 → 947 PASS, 0 FAIL. Blocco reale: `=== RIEPILOGO: 947 PASS, 0 FAIL ===`. In CI i conteggi sono +2 (test del profilo sandbox saltati in locale).
pytest `tests/`: `1558 passed in 184.08s (0:03:04)` (+24 gate, +5 ingest).

## §6 STATO CI

- Run sui commit di questo handoff: non ancora disponibile alla scrittura dell'handoff. §2/§3 non possono contenere il commit dell'handoff stesso.

## §7 RISERVE APERTE

- R-387-1 (BASSA): in `sembra_delicato` le parole delicate si cercano solo prima del primo punto; `.fish` non segnalato.
- Limite dichiarato: i file creati da `run_command` non fanno scattare l'avviso.
- R-384-1 (COSMETICA), R-380-1/2, R-378-1, R-379-1, R-ve224-2 e quelle di #222: vedi stato_progetto.md.
