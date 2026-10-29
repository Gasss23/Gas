# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani: decisioni dell'operatore su R-ve235-7 e tempo di rete 12 s (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #301 (https://github.com/Gasss23/Gas/pull/301). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5072015865","url":"https://github.com/Gasss23/Gas/pull/301"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore.
2. Prossimi argomenti della chat Mani: da scegliere.
3. Proposta di coordinamento della chat Motore 1 (scritta in stato_progetto, blocco «Mani — fetta 26»): da confermare.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #300**: `FATTA` — richiesta dell'operatore («mergia 300»), merge ed777ef. Bot su 69fd75e APPROVATO CON RISERVE: V-1 COSMETICA (la correzione dei «sei casi» della verifica esterna #298 stava solo in `reports/ultimo_report.md`, non anche in stato_progetto come diceva l'handoff della #300): `FATTA` — corretta qui.
- **R-ve235-7**: `FATTA` — chiusa come accettata (decisione dell'operatore).
- **Tempo di rete 12 s**: `FATTA` — confermato (decisione dell'operatore).
- **Ripartenza e stato della chat Mani**: `FATTA`.
- **Bot su 251b0c2 (PR #301)**: APPROVATO CON RISERVE. V-1 BASSA (riserve aperte non elencate): `FATTA` — in ripartenza_mani, stato_progetto e §7. V-2 COSMETICA (proposta di coordinamento fuori dal repo): `FATTA` — scritta in stato_progetto.
- **Bot su 604edcb (PR #301)**: APPROVATO CON RISERVE. V-1 BASSA (descrizione della PR vecchia): `FATTA` — descrizione aggiornata. V-2 COSMETICA (lista delle aperte incompleta): `FATTA` — aggiunte V-1 ve/bot #288 e R-546-1.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md   | 10 +++++-----
 reports/handoff.md         | n/d
 reports/ripartenza_mani.md |  3 ++-
 reports/stato_progetto.md  |  4 ++--
 reports/ultimo_report.md   | 19 ++++++++++---------
```

NB: base = merge-base con origin/main = ed777ef. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
604edcb docs(fine-task): Mani, riserve ancora aperte e proposta di coordinamento nel repo (V-1/V-2 bot #301)
251b0c2 docs(fine-task): Mani, decisioni su R-ve235-7 e tempo di rete, handoff (PR #301)
3430de8 docs(mani): R-ve235-7 chiusa come accettata, tempo di rete 12 s confermato (decisioni dell'operatore)
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 3430de8: pushato prima dell'apertura della PR #301; nessuna run su questo SHA come PR.
- 251b0c2: run 40914680818, `handoff-check` success; `verifica-bot` success, APPROVATO CON RISERVE (V-1/V-2 chiuse qui).
- 604edcb: run 40915228383; `verifica-bot` success, APPROVATO CON RISERVE (V-1/V-2 chiuse qui).
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- R-518-1 (chat Mani) BASSA: guardia `_nascosti_html` nelle chiusure in scope; per canvas fa perdere testo che il browser mostra (da decidere con l'oracolo).
- R-516-1 (chat Mani) BASSA: titolo perso sulle pagine a frame (verso sicuro).
- R-ve277-5 BASSA PREESISTENTE, parte leggi.py: con la lettura di sempre escono riserva di video/audio, testo di meter/progress, figli «light» di un host shadow.
- V-1 ve/bot #288 BASSA: adoption agency che sposta il template dichiarativo (dichiarata in `shadow()`).
- Ripartenza b): dopo l'accensione di lexbor, controllare che in CI i test lexbor non siano più saltati.
- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441), scelta: entità non dichiarata con DOCTYPE esterno non XHTML, Gas taglia come Firefox.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 fuori dal DTD XHTML 1.0 accettate, come whatwg.
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
- Chat Motore: libexpat ≥ 2.4 sul VPS e controllo nel doctor; `scripts/bot_esito.py` boccia i verdetti del bot con caratteri Cf scritti dal bot stesso.
