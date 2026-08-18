# Ultimo Report — fix/gasmerge-loopback-ok

**Data:** 2026-08-18
**Branch:** fix/gasmerge-loopback-ok

---

## DECISIONI UMANE RICHIESTE

1. Merge della PR #63 (fix(gasmerge): loopback 127.x.x.x sempre esente dall'invariante IP) — dopo che CI è verde, eseguire `gasmerge 63` da WSL.

---

## Esito fette

**Fetta unica — Loopback exemption invariante IP:** `FATTA`

- Modificata sezione INVARIANTE IP di `scripts/gasmerge.sh`: logica a 2 stadi (step 1: rimuovi righe loopback-only via `sed -E`; step 2: applica `gasmerge-ip-ok` sul residuo).
- Invariante di sicurezza critica mantenuta: riga con `127.0.0.1` + `93.42.17.8` BLOCCA ancora (il loopback non maschera l'IP reale).
- 7 nuovi test in `TestLoopbackExemption`; suite totale: 20/20 PASS.
- Revisore #74: APPROVATO 2026-08-18.
- PR #63 aperta, CI in corso.

**IPv6 (::1):** SALTATA — stop gate esplicito del task. La regex è IPv4-only; estensione a IPv6 richiede ok operatore separato.
