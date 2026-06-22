# 🤝 HANDOFF — Dossier di fine sessione

> Dossier autocontenuto per la revisione di fine sessione. **NON sostituisce
> `reports/ultimo_report.md`** (che resta la fonte di verità del singolo task):
> l'handoff lo AGGREGA per la revisione e ci aggiunge lo stato della CI.
> Si riscrive a ogni sessione (la storia completa sta in git).

**Sessione:** 2026-06-23 — CI auto-verificabile (job summary + gate sandbox)

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la run post-push** (commit più recente su GitHub Actions). Ora SENZA
   scaricare il log: la pagina della run mostra un **Job Summary** con esito bwrap
   (`BWRAP_OK`/`BWRAP_FAIL` pre e post sysctl), riga `RIEPILOGO: N PASS, M FAIL`, conteggio
   `SKIP` e lista FAIL; e lo step **"Gate — sandbox OS attivo"** è verde/rosso a sé:
   - **verde** = sandbox attivo (5 bwrap + 4 T13 hanno esercitato il profilo reale);
   - **rosso** = `BWRAP_FAIL` → STOP GATE → micro-task skip-on-CI (tocca `tests/`, revisore).
2. CI verde piena = micro-task su `tests/` (T9a/T9c + eventuale skip bwrap), fuori scope
   solo-workflow.

---

## ESITO SONDA / CONTESTO

Follow-up della verifica della run `4f8d014`: job failure, step sandbox "success", step
suite "failure" — MA "failure" è atteso anche col sandbox attivo (T9a/T9c restano), lo step
sandbox era "success" per costruzione (`|| echo BWRAP_FAIL`), e il log dettagliato è dietro
auth (HTTP 403, `gh` assente). → non si poteva distinguere il caso buono dallo STOP GATE
senza lo zip. Lacuna chiusa rendendo la run auto-verificabile.

---

## GIT DIFF --STAT (sessione, vs `4f8d014`)

```
 .github/workflows/ci.yml | 89 ++++++++++++++++++++++++++++++++++++++++++------
 1 file changed, 78 insertions(+), 11 deletions(-)
```

> Snapshot dopo il commit del workflow, prima del commit dei report. Storia git = fonte.

## GIT LOG (commit della sessione)

```
5dab394 ci: run auto-verificabile (job summary + gate sandbox) senza scaricare il log
```
(+ commit finale dei report — vedi git log vivo.)

---

## DELTA TEST DEL MOTORE

**0.** `tests/` e `gas.py` INVARIATI. Solo workflow.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Diff solo su `.github/workflows/ci.yml` (+ report).
Il gate di review (CLAUDE.md §3) scatta solo sui diff che toccano
`gas.py`/`brains/`/`modules/`/`tests/`: nessuno toccato.

## STATO CI

**Run post-push da verificare**, ora a colpo d'occhio dalla pagina della run (Job Summary +
step "Gate — sandbox OS attivo"), senza zip né auth. Il verdetto del job NON è mascherato:
resta rosso finché esistono FAIL (oggi attesi T9a/T9c), ma il *perché* è leggibile. Verde
pieno = micro-task su `tests/` (fuori scope solo-workflow).
