# Ultimo Report — 2026-06-28 (fix R-comp-1 boundary compressione)

**Data**: 2026-06-28
**Review gate**: #40 — APPROVATO
**Commit motore**: `cde4d94`

---

## Task: Fix R-comp-1 — boundary al confine piegato nel summary

Chiusura della riserva R-comp-1 aperta in review #39 (FASE 2.5):
i messaggi di `recent` che precedevano il primo `user` venivano scartati
silenziosamente. Fix applicato + 2 test aggiunti (T53, T54).

---

## Parte A — Fix `_compress_history_if_needed` (gas.py)

**Problema**: nella vecchia logica, dopo aver separato `old` e `recent`, il codice
trovava il primo `user` in `recent` e faceva `recent = recent[start:]`, scartando
silenziosamente `recent[:start]` (0..keep_msgs-1 messaggi: assistant/tool orfani
al confine).

**Fix**:
```python
# Prima: start detection + recent = recent[start:]  (drop silenzioso)
# Dopo:
boundary = recent[:start]
recent = recent[start:]
to_compress = old + boundary   # old + eventuali boundary piegati
lines = [f"[RIEPILOGO SESSIONI PRECEDENTI — {len(to_compress)} messaggi compressi]"]
for msg in to_compress:        # stesso loop/formato di prima, ora su old+boundary
    ...
summary = "\n".join(lines)
```

- Zero drop silenzioso: tutti i messaggi al confine finiscono nel riepilogo.
- Formato identico a `old`: stesso troncamento `content[:300]`, stessa notazione tool call.
- Header aggiornato: `len(to_compress) = len(old) + len(boundary)`.
- Caso degenere (no user in `recent`): `boundary=[]`, comportamento invariato.
- `logging.info` aggiornato: `"… (%d old + %d boundary → riepilogo)"`.
- Docstring aggiornato: rimuove il vecchio testo "scartati … accettabile".

---

## Parte B — Test T53 e T54

**T53 — R-comp-1 (il fix)**:
- History: 12 old (alternating) + 3 boundary assistant con `MARCATORE_COMP1_XK9` + 7 recent starting user (tot 22 msg).
- `GAS_HISTORY_KEEP_MSGS=10`, `GAS_HISTORY_MAX_MSGS=20` → `recent=history[-10:]` inizia con i 3 boundary.
- `start=3`, `boundary=[asst(M),asst(M),asst(M)]`, `to_compress=old(12)+boundary(3)=15`.
- Assert: (a) marker in `history[0]["content"]`; (b) `history[0]["role"]=="user"`; (c) `"15 messaggi compressi"` in summary. **PASS**.

**T54 — caso degenere no-user**:
- History: 30 messaggi `assistant` (nessun user).
- `start=0`, `boundary=[]`, `to_compress=old`. Summary = user. Window[0] = user.
- Assert: `history[0]["role"]=="user"` e `_get_window()[0]["role"]=="user"`. **PASS**.

---

## Verdetto revisore #40 (INTEGRALE)

**APPROVATO**

Il fix chiude correttamente R-comp-1 (riserva aperta in review #39): i messaggi al confine old/recent che precedono il primo user vengono ora piegati nel riepilogo invece di essere scartati silenziosamente. Il caso degenere (nessun user in `recent`, start=0) produce `boundary=[]` → comportamento identico alla versione precedente. L'invariante `_get_window` (history parte sempre da `role='user'`) è garantita perché il summary ha sempre `role='user'`. T53 e T54 coprono rispettivamente il caso nominale e il caso degenere, entrambi PASS. Nessuna violazione degli antipattern §5, nessuna regressione.

---

## Git diff --stat (commit cde4d94)

```
gas.py                    | 37 ++++++++++++------------
tests/test_unit_kernel.py | 71 +++++++++++++++++++++++++++++++++++++++++++++++
2 files changed, 91 insertions(+), 17 deletions(-)
```

---

## Delta test

| Metrica | Prima | Dopo |
|---------|-------|------|
| Test Windows | 190 PASS, 8 FAIL | **196 PASS, 7 FAIL** |
| FAIL rimasti | 8 (di cui T53 appena fallito) | **7 (tutti pre-esistenti bwrap/WinError32)** |
| Nuovi test | — | T53, T54 |
| T49-T52 (preesistenti compressione) | PASS | **PASS** (nessuna regressione) |
| CI Linux | — | **SUCCESS** run #28307518983 su `cde4d94` ✅ |

---

## §RISERVE

Nessuna riserva nuova. Osservazioni annotate durante il lavoro:

1. **Crescita summary**: con boundary = `keep_msgs-1` (caso peggiore), il summary cresce al massimo di `keep_msgs-1` righe in più, ognuna ≤ ~310 char. Con `HISTORY_KEEP_MSGS=20`, worst case: +19 righe × ~310 char ≈ +5.9KB nel singolo messaggio summary. Il summary viene poi gestito da `_cap_window_chars` che già taglia per `WINDOW_CHAR_CAP`. Nessuna interazione critica, ma annotato per VPS con log grande.

2. **T54 (degenere) già funzionava prima del fix**: il loop `for i, m in enumerate(recent)` con `start=0` default lasciava `recent` invariato anche nella vecchia versione. T54 è utile come regression guard per il ramo `for-break senza match`.
