# ULTIMO REPORT — 2026-10-08 — FASE 4.5 fetta 1: `gas notte` + cancello rinforzato

## Riassunto

Nuovo comando `python3 gas.py notte`: Gas esegue da solo i compiti scritti in `~/.gas_notte.yaml`,
ognuno da zero, con riepilogo in `~/Gas/.gas_notte/ultimo_giro.md` e tetto di spesa di default.
Il bot di verifica ha trovato un buco reale (Gas poteva scrivere codice che il giro notturno avrebbe
eseguito fuori sandbox): chiuso nel cancello. Oggi Gas di notte NON sviluppa codice.

## DECISIONI UMANE RICHIESTE

1. PR #160: merge quando il bot di verifica dà success sul nuovo commit (la sessione lo fa da sola
   se tutto è positivo, su richiesta dell'operatore).
2. Sul Mac, dopo il merge: seguire `reports/setup_notte.md` (catalogo, tetto di spesa, timer launchd).
3. Da sapere (R-222-4): Gas non può più scrivere file `.py`/`.sh`, né `scripts/`, `CLAUDE.md`/`AGENTS.md` (a ogni livello),
   `gas_identity.md`, `requirements*`; non può leggere `.gas_notte/`. Se serve diversamente, decidilo tu.
4. Ancora aperte da prima: lezioni #4, #5, #6 (parere: approva 6 e 5, rifiuta 4); firma `fab385e4…`.

## Esito

- **Fetta 1 FASE 4.5 — comando `gas notte`**: FATTA — `modules/notte/`, `notte_cmd` in `gas.py`; review #220.
- **Correzioni verifica esterna #160 (V-1 MEDIA budget, V-2, V-3)**: FATTA — `d0cfc17`; review #221.
- **Correzione bot di verifica #160 (V-1 MEDIA catena di avvio fuori sandbox)**: FATTA — cancello
  `modules/gate/gate.py`; review #222 e #223 (chiusa anche R-222-1 MEDIA, script `.sh` e file di primo livello).
- **Correzione bot di verifica #160 su `d3a593d` (BOCCIATO, V-1 MEDIA: file d'istruzioni degli agenti scrivibili sotto il primo livello)**: FATTA — `c120bda`, review #224 e #225; anche V-2 (esempio senza `git`) e R-224-1 (`AGENTS.override.md`).
- **Allineamento a main**: FATTA — `bcf2d5c` (merge senza cambi di file).
- **Test**: notte 26, gate 132 (158 insieme), `pytest tests/` 777 passed; kernel 707 PASS 0 FAIL in locale, 709 in CI (scarto fisso noto, V-3 del bot).
- **Template launchd + catalogo + guida**: FATTA — `scripts/notte/`, `reports/setup_notte.md`.
- **Riepilogo su Telegram al mattino**: DEFERITA — fetta 2.
- **Tetto di tempo per compito/giro (R-220-3)**: DEFERITA — fetta 2.
- **R-220-2, R-223-1, R-223-2 (BASSE)**: DEFERITE — in `reports/stato_progetto.md` voce 6.
- **Prova reale sul Mac (launchd)**: DEFERITA — non riproducibile qui; la fa l'operatore.

## Anomalie

- `gh` non autenticato in questo ambiente: PR e CI lette con gli strumenti GitHub della sessione.
- Il bot di verifica ha BOCCIATO il commit `680dafb` (V-1 MEDIA): motivo reale, corretto in `d0cfc17`.
- Il bot di verifica ha BOCCIATO anche `d3a593d` (V-1 MEDIA): motivo reale, corretto in `c120bda`.
- Il primo tentativo del bot su `d3a593d` era stato annullato: rilanciato dall'agente (richiesta "Riprova" dell'operatore).
