# Ultimo Report — fix/gasmerge-loopback-ok (self-block chiuso)

**Data:** 2026-08-18
**Branch:** fix/gasmerge-loopback-ok

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #63 — dopo CI verde, eseguire `gasmerge 63` da WSL.

---

## Esito fette

**Fetta A — Loopback exemption invariante IP (sessione precedente):** `FATTA`
gasmerge.sh: gate IP a 2 stadi, loopback 127.x.x.x sempre esente, riga mista ancora blocca.
7 nuovi test (TestLoopbackExemption). Revisore #74 APPROVATO.

**Fetta B — Chiusura self-block TestLoopbackExemption:** `FATTA`
gasmerge scandisce l'intero albero del branch: TestLoopbackExemption conteneva righe
con IP pubblici (zero-route, un IP pubblico di test) senza marker, bloccando il merge.
Intervento: marker `# gasmerge-ip-ok` sulle righe di codice (fixture/chiamate);
IP letterali rimossi da docstring e messaggi d'assert.
Fixture stringa invariate — i test verificano ancora gli stessi indirizzi.
`scripts/gasmerge.sh` NON toccato. 20/20 PASS. Revisore #75 APPROVATO.
Anche i vecchi file di report (handoff.md, diff_sessione.md) contenevano IP nudi
senza marker: sovrascritti con versioni pulite.

**Verifica 2 stadi post-commit:** RESIDUAL vuoto — gate IP passa su tutto l'albero.

**IPv6 (::1):** `SALTATA — stop gate esplicito`
Regex IPv4-only by design; estensione richiede ok operatore separato.
