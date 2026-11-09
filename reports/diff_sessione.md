# Diff della sessione — 2026-11-09 — Server voce più sicuro, R8 fetta 1 (chat M2)

- `modules/voice/server.py` — `_autorizza()` (tetto ai tentativi falliti per IP, usato in tutti i controlli del token), tetto alle richieste a testo prima del tetto voce e contato dopo, avvio fail-closed fuori da 127.0.0.1 (`_bind_locale` con `ipaddress`), helper `_intero_env`, `_env_acceso`, `_bind_tutte_le_interfacce`, `_bind_ip_letterale`, `_host_ammesso` (Host solo «localhost» o IP, DNS rebinding); richieste senza token non contano per il blocco; (mai su tutte le interfacce; fuori da 127.0.0.1 solo IPv4 scritto per intero); docstring delle variabili nuove.
- `tests/test_unit_voice_server.py` — `TestR8Limiti` e test `test_r8_*` (indirizzi non locali d'esempio in IPv6, gate IP).
- `reports/proposta_voce_sicura.md` — proposta con opzioni, raccomandazione, stato e limiti noti.
- `.claude/agents/memoria_revisore.md` — review #720, #722, #723, #724, #726, #727, #728, #729, #730, #731, #732, #733 (merge di main, #357 di Mani).
- `reports/*` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
