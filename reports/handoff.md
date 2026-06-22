# 🤝 HANDOFF — Dossier di fine sessione

> Dossier autocontenuto per la revisione di fine sessione. **NON sostituisce
> `reports/ultimo_report.md`** (che resta la fonte di verità del singolo task):
> l'handoff lo AGGREGA per la revisione e ci aggiunge lo stato della CI.
> Si riscrive a ogni sessione (la storia completa sta in git).

**Sessione:** 2026-06-23 — CI: abilitazione del sandbox OS (bubblewrap) nel runner

---

## §DECISIONI UMANE RICHIESTE

1. **Verificare la run post-push su GitHub Actions** leggendo nel log:
   - smoke-test bwrap: **BWRAP_OK / BWRAP_FAIL** (smoke-test 1 post-install + smoke-test 2
     post-sysctl);
   - i 5 test bwrap (T11c2, T11e, T12a, T12c, T12e) col sandbox attivo → attesi PASS;
   - i 4 test T13 (a rete-isolata, b fs-read-only, c segreto-mascherato, e comando-in-bwrap)
     → attesi GIRARE (non più [SKIP]) e PASS;
   - conteggio PASS/FAIL/SKIP finale.
2. **STOP GATE:** se lo smoke-test resta `BWRAP_FAIL` anche dopo il sysctl → `os_strict` NON
   esercitabile sul runner GitHub → aprire **micro-task 2** (skip-on-CI dei test bwrap, tocca
   `tests/` → CON REVISORE). NON skippato/committato workaround su `tests/` in autonomia.
3. **T9a/T9c** (env API / storia su root temp) restano fuori scope → micro-task 2.

---

## ESITO SONDA (FASE 0, sola lettura)

1. **T13a/b/c/e (oggi SKIP):** gated da `OS_SB = gas._probe_os_sandbox()[0]` (riga 380) +
   `if OS_SB: ... else skip`. Reagiscono alla disponibilità REALE → con bwrap GIRANO. ✓
2. **T11c2/T11e/T12a/T12c/T12e (oggi FAIL):** dipendono dall'esecuzione di `run_command`
   (oggi negato fail-closed senza bwrap). Col sandbox presente eseguono → PASS. T11c2 forza il
   fallimento snapshot via dir non-git (ortogonale al sandbox): col sandbox attivo il flusso
   arriva allo snapshot-fail → messaggio "snapshot" atteso → PASS. ✓
3. **PIVOT T13d/T13d2 (oggi PASS):** FORZANO l'assenza in modo deterministico
   (`os_sandbox_available = False` sull'istanza, righe 434/443) — NON dipendono dall'ambiente
   reale. Installare bwrap NON li flippa. ✓ → VIA LIBERA, installare bwrap è solo-workflow.

Nessun test attualmente-PASS dipende dall'assenza reale del sandbox.

---

## GIT DIFF --STAT (sessione, vs `6f3793a`)

```
 .github/workflows/ci.yml | 32 ++++++++++++++++++++++++++++++--
 1 file changed, 30 insertions(+), 2 deletions(-)
```

> Snapshot dopo il commit di FETTA 1, prima del commit dei report (questo handoff +
> ultimo_report + stato_progetto si aggiungono al commit finale). Storia git = fonte.

## GIT LOG (commit della sessione)

```
919f677 ci: abilita il sandbox OS (bubblewrap) nel runner prima della suite
```
(+ commit finale dei report — vedi git log vivo.)

---

## DELTA TEST DEL MOTORE

**0.** `tests/` e `gas.py` INVARIATI. La sonda ha confermato che non serve toccarli (pivot
T13d/T13d2 deterministico). Dichiarato onestamente, non gonfiato.

## VERDETTO DEL REVISORE

**Non applicabile — task non-motore.** Diff solo su `.github/workflows/ci.yml` (+ report).
Il gate di review (CLAUDE.md §3) scatta solo sui diff che toccano
`gas.py`/`brains/`/`modules/`/`tests/`: nessuno toccato.

## STATO CI

**Prima run COL SANDBOX da verificare su GitHub Actions.** Contesto: la run precedente
(prima del sandbox) era 160 PASS / 7 FAIL / 4 SKIP su Linux. Atteso col sandbox attivo: i 5
bwrap-FAIL → PASS, i 4 T13-SKIP → PASS, restano i 2 env-FAIL (T9a/T9c, fuori scope). Il
numero OGGETTIVO lo riempie la run, non l'agente. Vedi §DECISIONI UMANE #1.
