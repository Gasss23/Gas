# Diff sessione — 2026-07-30

Task: hardening scripts/gasmerge.sh + suite test (PR #56, branch fix/gasmerge-hardening)

## File toccati

```
 .claude/agents/memoria_revisore.md |  1 +
 scripts/gasmerge.sh                | 12 +++---
 tests/test_unit_gasmerge.py        | 76 ++++++++++++++++++++++++++++++-
 3 files changed, 79 insertions(+), 10 deletions(-)
```

## Cosa è cambiato e perché

**scripts/gasmerge.sh** (+12/-4):
- FIX 3: mktemp per-run (`GASPR_JSON=$(mktemp /tmp/gaspr.XXXXXX.json)`) + export + trap EXIT. Sostituisce il path fisso `/tmp/gaspr.json` condiviso fra test → thread-safe con pytest-xdist.
- FIX 1: guard `[ -n "$NEW_HEAD" ]` post-conferma. Il guard per HEAD_SHA era già a riga 158; il caso NEW_HEAD (ri-lettura dopo il prompt) mancava.

**tests/test_unit_gasmerge.py** (+76/-6):
- FIX 2: `shutil.which("git")` in Python risolve il git reale PRIMA che fake_bin sia preposta a PATH → nessuna ricorsione nell'`exec` del body dello stub.
- FIX 3: stub `_make_stub_gh` e stub inline TOCTOU: `> /tmp/gaspr.json` → `> "$GASPR_JSON"` (ereditato via export da gasmerge.sh).
- FIX 1 mordacità: nuovo test `test_new_head_empty_blocks_with_explicit_message` — stub stateful (1ª headRefOid → SHA valido, 2ª → "") verifica che il BLOCCO citi "vuoto" e NON "head cambiata".

**memoria_revisore.md**: riga review #69 aggiunta dal revisore.

## Suite

- Gasmerge: 12/12 PASS (era 11/11)
- Hooks+handoff: 19/19 PASS
- Kernel: INTERNALERROR pre-esistente (sys.exit a livello modulo), non regressionato
