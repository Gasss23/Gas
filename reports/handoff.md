# HANDOFF — Dossier di fine sessione

**Sessione:** 2026-09-22/23 — Autonomia #1 "Studia/Comprendi" — K0+K1+K2

---

## §0 DECISIONI UMANE RICHIESTE

1. Merge della PR #94 (https://github.com/Gasss23/Gas/pull/94).
2. **Prima fonte reale**: approvare una fonte reale in `knowledge/sources.yaml` (richiede commit umano esplicito con slug, URI e `approvata_il`). Solo dopo si può testare l'ingest su contenuto non-test.
3. **K3** (wiring `ricorda` in gas.py): decidere se affrontarlo nella prossima sessione o rimandarlo. È l'unica fetta che tocca il motore e richiede gate revisore.

---

## §1 SCOPE & ESITO FETTE

- **K0 — `knowledge/sources.yaml`**: FATTA — catalogo fonti YAML versionato in git, una fonte test locale (`test_local`, tipo=file, chunk_max=10)
- **K1 — schema `.gas_knowledge.db`**: FATTA — DB SQLite separato da `.gas_memory.db`, tabella `knowledge` con partial unique index versioning su `stato='active'`
- **K2 — `tools/ingest_knowledge.py`**: FATTA — CLI off-loop, chunking a capoversi (~1800 char ≈ 500 token), idempotenza SHA-256, versioning (vecchio → `stato='superseded'`, mai cancellato)
- **K3 — wiring `ricorda` in gas.py**: DEFERITA — VIETATA in questo scope (tocca il motore, richiede revisore)
- **K4 — protezioni anti-prompt-injection**: DEFERITA — fuori scope esplicito

**Test reali eseguiti:**
1. Primo ingest: 2 chunk ingeriti (chunk_0000: 1505 chars, chunk_0001: 314 chars), ingested=2 skipped=0
2. Secondo ingest identico: ingested=0 skipped=2 (idempotenza confermata)
3. `.gas_memory.db` mtime invariato (1789992259 prima e dopo), 20 righe diario invariate

**Anomalie:**
- CI failure su commit `d46868c`: il `reports/handoff.md` in quel commit era il residuo della sessione sonda e dichiarava solo 4 file in §2 invece dei 9 reali. Corretto dal presente handoff.

---

## §2 GIT DIFF --STAT (sessione)

```
 .gitignore                |   4 +
 knowledge/sources.yaml    |  21 ++++
 knowledge/test_source.txt |  38 +++++++
 reports/diff_sessione.md  |  29 ++---
 reports/handoff.md        |  86 +++++++--------
 reports/stato_progetto.md |   3 +
 reports/ultimo_report.md  | 219 ++++++++++++++++++++++++++-----------
 requirements.txt          |   1 +
 tools/ingest_knowledge.py | 268 ++++++++++++++++++++++++++++++++++++++++++++++
 9 files changed, 543 insertions(+), 126 deletions(-)
```

---

## §3 GIT LOG --ONELINE (sessione)

```
d46868c feat(knowledge): K0+K1+K2 — knowledge store + CLI ingest off-loop
afabf03 docs(fine-task): handoff sonda autonomia cap#1 studia/comprendi 2026-09-21
f8f45b3 docs(sonda): autonomia cap#1 studia/comprendi — sonda architetturale + piano a fette
```

NB: il commit di fine-task che contiene questo file non compare in questo log, per costruzione.

---

## §4 VERDETTO DEL REVISORE (per commit motore)

Nessun diff motore (nessun commit tocca gas.py/brains/modules/tests/) — revisore non richiesto.

---

## §5 DELTA TEST DEL MOTORE

Nessuna modifica a gas.py/tests/ in questa sessione.

Suite di riferimento pre-sessione (macOS, 2026-09-21):
- `python tests/test_unit_kernel.py`: 294 PASS, 5 FAIL (F-mac-1, bwrap macOS)
- pytest altri test: 132 PASS, 0 FAIL

Nessuna variazione attesa.

---

## §6 STATO CI

```
completed	failure	feat(knowledge): K0+K1+K2 — knowledge store + CLI ingest off-loop	CI	sonda/autonomia-studia-cap1	push	35759608797	1m11s	2026-09-22T17:16:32Z
completed	success	docs(fine-task): handoff sonda autonomia cap#1 studia/comprendi 2026-…	CI	sonda/autonomia-studia-cap1	push	35620436911	51s	2026-09-21T15:39:35Z
completed	success	docs(sonda): autonomia cap#1 studia/comprendi — sonda architetturale …	CI	sonda/autonomia-studia-cap1	push	35618104536	1m2s	2026-09-21T15:19:03Z
```

**Mappatura commit→run:**
- `d46868c` → run 35759608797 — **FAILURE** (handoff-check: §2 dichiarava 4 file, diff reale 9 file). Corretto dal presente fine-task.
- `afabf03` → run 35620436911 — success
- `f8f45b3` → run 35618104536 — success

**Nota:** il push di questo fine-task produrrà una nuova run CI che testerà l'handoff corretto.

---

## §7 RISERVE APERTE

- **F-K2-1** (minore): il campo opzionale `chunk_chars` per fonte in `sources.yaml` non è documentato nel template del file. Da aggiungere come commento facoltativo prima di usare fonti reali.
- **R-K5** (N/A per ora): pesi MiniLM non ancora scaricati su questo Mac (K2 non usa ancora `.gas_vectors.db`). Diventa rilevante a K3.
- **CI failure `d46868c`**: documentato in §2 anomalie, corretto da questo commit.
