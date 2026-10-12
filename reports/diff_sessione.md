# Diff della sessione — 2026-10-11 — chiavi private e credenziali vietate

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `_CHIAVE_PRIVATA_RE` in `_nome_da_segreto`: chiavi ssh, `*.pem/*.key/*.p12/*.pfx/*.ppk/*.jks/*.keystore/*.kdbx` (anche copie), `secret(s)*`, `credential(s)*`, `.ssh/.gnupg/.aws/.netrc/.pgpass/.pypirc/.htpasswd` illeggibili; `livello_scrittura` → 3 per i nomi da segreto. Perché: decisione dell'operatore («vietale», V-1 verifica esterna #184). Poi varianti dei nomi (copie, prefissi/suffissi, .kube/.docker/.npmrc, token.json…) su richiesta dell'operatore dopo bot e verifica esterna #188.
- `tests/test_unit_gate.py`, `tests/test_unit_kernel.py` (T86) — test di lettura/scrittura e round-trip agentico.
- `.claude/agents/memoria_revisore.md` — review #289, #290, #291.
- `reports/` — report di fine task, stato del progetto.
