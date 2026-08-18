# Diff Sessione — 2026-08-18

**Branch:** fix/gasmerge-loopback-ok
**Commit motore:** 134579b

## File toccati

| File | Tipo | Cosa è cambiato |
|------|------|-----------------|
| `scripts/gasmerge.sh` | FIX | Invariante IP: filtro loopback 127.x.x.x a 2 stadi (step 1: rimuovi loopback-only; step 2: gasmerge-ip-ok sul residuo) |
| `tests/test_unit_gasmerge.py` | TEST | Classe `TestLoopbackExemption` con 7 nuovi test (127.0.0.1, 127.0.0.53, 0.0.0.0, IP pubblico, riga mista, marker, regressione) |
| `.claude/agents/memoria_revisore.md` | DOC | Aggiornato contatore review #74, 2026-08-18 |

## Perché

La pipeline vocale FASE 3 gira su localhost (127.0.0.1 come endpoint), e il gate bloccava ad ogni fetta con IP non allowlistato. La modifica insegna al gate che 127.x.x.x è sempre lecito senza marker. La sicurezza chiave (riga mista = blocco) è coperta da test dedicato e verificata esplicitamente dal revisore.

## Suite al commit

20/20 PASS (pytest tests/test_unit_gasmerge.py — 7 nuovi + 13 preesistenti).
