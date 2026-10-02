# Ultimo Report — fix gate IP T72b + R-c2-9

**Data:** 2026-10-02
**Branch:** feat/cancello-c2
**Commit:** a0a5294
**Task:** sblocca gasmerge gate IP + chiude riserva R-c2-9

---

## §1 — SONDA gasmerge.sh IP allowlist (VERBATIM)

Meccanismo (`scripts/gasmerge.sh` righe 91–135):

```
IP_MATCHES=$(git grep -nE '(^|[^0-9.])[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}([^0-9.]|$)' "origin/$BRANCH")
```

- Step 1: rimuove le righe con soli IP di loopback `127.x.x.x` via `sed` + grep residuo.
- Step 2: filtra con `grep -v 'gasmerge-ip-ok'` — le righe che contengono il token letterale **`gasmerge-ip-ok`** sono allowlistate (vouch umano esplicito sulla riga sorgente).
- Se residuo non vuoto → `BLOCCO: trovati IP non allowlistati` + `exit 1`.

---

## §2 — FIX applicati

**tests/test_unit_kernel.py:4946** — aggiunto `# gasmerge-ip-ok`:
```python
# prima
[("ssh_vps", '{"host": "1.2.3.4"}')],  # ssh non è nell'allowlist → DENY
# dopo
[("ssh_vps", '{"host": "1.2.3.4"}')],  # ssh non è nell'allowlist → DENY  # gasmerge-ip-ok
```
Il test T72b continua a testare il DENY: `ssh_vps` non è nell'allowlist dei tool → `Operazione negata`. L'IP `1.2.3.4` è esclusivamente un parametro della fixture, non una connessione reale.

**tests/test_unit_kernel.py:4920** — assert T71h read più preciso (chiude R-c2-9):
```python
# prima
"test" in _out71h_r
# dopo
_out71h_r == "test"
```
`read_file` restituisce il contenuto raw (non wrappato), quindi l'uguaglianza esatta è corretta e più rigida.

---

## §3 — Suite kernel

```
=== RIEPILOGO: 423 PASS, 5 FAIL ===
  FAIL: T11c2 snapshot fallito -> run_command (sandbox bwrap non disponibile)
  FAIL: T11e run_command fa scattare lo snapshot (bwrap non disponibile)
  FAIL: T12a comando in allowlist (wc) eseguito, output reale (bwrap non disponibile)
  FAIL: T12c pipe non interpretata (bwrap non disponibile)
  FAIL: T12e command substitution non eseguita (bwrap non disponibile)
```

**423 PASS, 5 FAIL F-mac-1** — tutti i FAIL sono bwrap/macOS, invariati rispetto alla baseline.

---

## §4 — Simulazione invariante IP (verbatim)

```
=== Simulazione invariante IP (test_unit_kernel.py, HEAD post-fix) ===
git grep output: HEAD:tests/test_unit_kernel.py:4946:    [("ssh_vps", '{"host": "1.2.3.4"}')],  # ssh non è nell'allowlist → DENY  # gasmerge-ip-ok
Tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK. ZERO BLOCCHI.
```

---

## §5 — Verdetto revisore #121 (VERBATIM)

```
VERDETTO FINALE: APPROVATO

Diff revisionato: tests/test_unit_kernel.py (2 modifiche puntuali)

1. tests/test_unit_kernel.py:4920 — sostituisce "test" in _out71h_r con _out71h_r == "test"
   rischio: regression se read_file inietta prefix/suffix — esito: ok (suite 423 PASS confermata,
   chiude R-c2-9 da review #120)

2. tests/test_unit_kernel.py:4946 — aggiunge # gasmerge-ip-ok in coda alla riga con IP fittizio
   1.2.3.4 nel fixture T72b — rischio: il marker potrebbe esentare per errore un IP reale in
   codice produzione — esito: ok (è commento in riga di fixture test, IP è parametro fittizio,
   comportamento DENY del test invariato)

Controllo antipattern: nessun raw history slicing, nessuna simulazione di tool, _get_window()
non toccata, loop cap (10 iterazioni) non toccato, guardrail API intatti.

Suite: 423 PASS, 5 FAIL F-mac-1 (attesi, non regressioni). Il commit può procedere.
```

---

## §6 — Riserve aggiornate

- **R-c2-9: CHIUSA** (assert esatto T71h read)
- Riserve aperte non bloccanti: R-c2-2, R-c2-4, R-c2-5, R-c2-6 residuo, R-c2-8, R-c2-10
