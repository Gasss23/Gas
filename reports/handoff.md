# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-10-29 — Mani: chiusura fetta 26, note cosmetiche della verifica esterna #298, ripartenza (chat Mani)

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #300 (https://github.com/Gasss23/Gas/pull/300). Numero e URL dalla risposta JSON dell'integrazione GitHub (`create_pull_request`: `{"id":"5071930147","url":"https://github.com/Gasss23/Gas/pull/300"}`); `gh` nel cloud non è autenticato. Merge da solo SOLO con verdetto del bot APPROVATO pulito; con riserve serve l'OK dell'operatore.
2. Due decisioni rimaste della chat Mani, una alla volta: «tempo di rete 12 s» e R-ve235-7 (proposta: chiuderla come accettata).
3. Accensione della lettura con lexbor: la chat Motore mette `selectolax==1.0.2` in `requirements-dev.txt` e `requirements.txt` (R-ve280-1); poi `GAS_WEB_LEXBOR=1` sul VPS.

---

## §1 SCOPE & ESITO FETTE

- **Merge della PR #298 (fetta 26)**: `FATTA` — richiesta dell'operatore («mergia 298»), merge 7cc2112. Bot su d3b489f APPROVATO CON RISERVE: V-1 COSMETICA (descrizione della PR): `FATTA`.
- **Note della verifica esterna #298 su d3b489f** (https://github.com/Gasss23/Gas/pull/298#issuecomment-6499903630):
  - V-1 COSMETICA (i casi di non regressione sono sei, non tre): `FATTA` — corretto in `reports/ultimo_report.md` e in stato_progetto.
  - V-2 COSMETICA («`valore is not None` tolto» non è un mutante equivalente): `FATTA` — corretto in `reports/ultimo_report.md` e in stato_progetto.
  - V-3 informativa: `SALTATA — già dichiarata`.
- **Ripartenza della chat Mani**: `FATTA`.
- **Tempo di rete 12 s, R-ve235-7**: `DEFERITA — decisioni dell'operatore`.

---

## §2 GIT DIFF --STAT (sessione)

```
 reports/diff_sessione.md   |  13 +++++--------
 reports/handoff.md         | n/d
 reports/ripartenza_mani.md |   4 ++--
 reports/stato_progetto.md  |   4 ++--
 reports/ultimo_report.md   |  35 +++++++++++------------------------
```

NB: base = merge-base con origin/main = 7cc2112. Regola «n/d»: il conteggio di `reports/handoff.md` non è misurabile mentre lo si scrive; tolta la riga di totale.

## §3 GIT LOG --ONELINE (sessione)

```
09cbb69 docs(mani): ripartenza e stato dopo il merge della #298, note cosmetiche della verifica esterna #298
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

## §4 VERDETTO DEL REVISORE (per commit motore)

nessun diff motore, revisore non richiesto.

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/.

## §6 STATO CI

`gh` non autenticato nel cloud: check run lette dall'integrazione GitHub.
- 09cbb69: pushato prima dell'apertura della PR #300; nessuna run su questo SHA come PR (la run della PR testerà il commit di testa).
- Il commit di fine-task che contiene questo file: run non ancora disponibile alla scrittura dell'handoff.

## §7 RISERVE APERTE

- Decisioni dell'operatore: tempo di rete 12 s; R-ve235-7 (il DNS di sistema non si interrompe).
- V-2 BASSA della verifica esterna #296 su 336e67c (https://github.com/Gasss23/Gas/pull/296#issuecomment-6485248441), scelta: entità non dichiarata con DOCTYPE esterno non XHTML, Gas taglia come Firefox.
- V-3 BASSA della verifica esterna #296 su 06bc98e (https://github.com/Gasss23/Gas/pull/296#issuecomment-6498712956), scelta: entità HTML5 fuori dal DTD XHTML 1.0 accettate, come whatwg.
- R-ve280-1 BASSA: i test lexbor con selectolax non girano nei check required. Chat Motore.
- R-546-1 BASSA: numeri delle review doppi tra le chat.
- Chat Motore: libexpat ≥ 2.4 sul VPS e controllo nel doctor; `scripts/bot_esito.py` boccia i verdetti del bot con caratteri Cf scritti dal bot stesso.
