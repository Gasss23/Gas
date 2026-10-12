# ULTIMO REPORT — T80u5: il tetto di annidamento non dipende più dalla versione di Python

> Task del 2026-10-12, su richiesta dell'operatore («intanto apri una PR per sistemare T80u5»).
> Ramo: **`fix/test-t80u5-portabile`** (da `origin/main` = `f6396ba`).

## Il problema, misurato

Un check della sessione ha rilevato che sulla **main** la suite del kernel dà **818 PASS e 1 FAIL**
(`T80u5`) usando il `.venv` del progetto, che su questa macchina è **Python 3.14.7**.
La CI non lo vedeva perché pinna **Python 3.11** (`.github/workflows/ci.yml:44`, dove il commento
«venv WSL è 3.12.3» è stale rispetto a questa macchina).

`T80u5` asseriva che un JSON annidato 100.000 livelli venisse scartato con il motivo
«JSON annidato oltre il limite di ricorsione». Quell'esito dipendeva dal fatto che `json.loads`
sollevasse `RecursionError`. Misurato su 3.14.7: `json.loads` **parsa senza errore** annidamenti
da 200 fino a 100.000 livelli, quindi:

1. l'`except RecursionError` era **codice morto** su 3.14;
2. `_analizza_riflessione` costruiva **100k dict annidati** (misurati dal revisore: 1,2 MB di input
   → **18,4 MB di picco**, 36 ms) per poi buttarli e scartare l'input con un motivo **falso**
   («recap mancante» invece di «annidato»);
3. il motivo nel `gas_debug.log` **cambiava con la versione di Python**, su un input che arriva
   dal modello.

## Cosa ho cambiato

- **`gas.py`**: `_RIFLESSIONE_MAX_PROFONDITA = 50` e la funzione pura `_troppo_annidato()`, che conta
  l'annidamento di `{`/`[` **solo fuori dalle stringhe JSON** (gestisce l'escape `\`) ed **esce al
  primo sforamento**. `_analizza_riflessione` controlla il tetto **prima** di `json.loads` e scarta
  con «JSON annidato oltre il limite (50 livelli)». L'`except RecursionError` **resta** come rete di
  sicurezza, con il suo messaggio distinto.
- **`tests/test_unit_kernel.py`**: `T80u5` aggiornata al messaggio nuovo; **T80u6** (confine esatto
  50 vs 51, parentesi dentro le stringhe e dopo un escape non contano, JSON legittimo ancora
  accettato, uscita anticipata su 1,2 MB di input annidato); **T80u7** (la rete `except
  RecursionError` è viva e il suo messaggio resta distinto da quello del tetto).

Il tetto è una **costante di modulo, non configurabile da env di proposito**: una riflessione
legittima è profonda 2, il margine è 25x, e un `GAS_...=0` renderebbe `_troppo_annidato` sempre vera,
cioè **ogni** riflessione rifiutata e la cascata a 4 rung bruciata a ogni turno (verificato dal
revisore con `limite=0/-1/-100`).

## Numeri REALI

| Misura | Base (`f6396ba`) | Dopo |
|---|---|---|
| Suite kernel (`.venv`, Python 3.14.7) | **818 PASS, 1 FAIL** (T80u5) | **821 PASS, 0 FAIL** |
| `pytest -q` | 1031 passed, 1 skipped | **1031 passed, 1 skipped** |

Sonda con `sys.setrecursionlimit(80)`: il tetto scatta prima di `json.loads`, nessuna eccezione
sfugge, messaggio identico.

**NON VERIFICATO**: il comportamento su **Python 3.11/3.12**. Su questa macchina esiste solo il
`.venv` (3.14.7) e non ho installato altri interpreti. La prova è la **CI** (`unit-suite`, pinnata
3.11). Il tetto però short-circuita prima del parser, quindi l'esito non può dipendere dal parser.

## Review

Review **#297 APPROVATO CON RISERVE** → quattro riserve, **tutte corrette prima del commit**:

- **R-297-1** (BASSA) — difetto reale del mio test: l'input degenere `'{"a":'*2000000 + '1'` **non
  arrivava mai** al tetto (senza `}` finale scattava `j <= i`), e il cronometro misurava la
  costruzione della stringa. **CHIUSA**: input ora CHIUSO (200k livelli, 1,2 MB), si cronometra la
  chiamata, misurato **0,007 ms** con il motivo del tetto.
- **R-297-2** (BASSA) — la rete `except RecursionError` restava senza nessun test e sopravviveva solo
  grazie a un commento. **CHIUSA**: T80u7 la esercita forzando `json.loads` a sollevare.
- **R-297-3** (BASSA) — `_troppo_annidato` solleva `TypeError` su input non-`str` ed è documentata
  «PURA». **CHIUSA**: precondizione dichiarata nella docstring, con il chiamante che la garantisce.
- **R-297-4** (COSMETICA) — claim sul costo imprecisa e commento stale di T80u5. **CHIUSA**.

Il revisore ha verificato che i test **mordono**, con due mutazioni su `gas.py`: `return False` in
testa a `_troppo_annidato` → 2 FAIL; ingresso in stringa ignorato → 1 FAIL.

## Proposte NON implementate (fuori perimetro di questa fetta)

1. **`ci.yml:44`**: il commento sulla versione del venv è stale (dice 3.12.3, questa macchina ha
   3.14.7). Soprattutto: **la CI prova una sola versione di Python**, quindi una divergenza come
   questa resta invisibile. Proposta: matrice `3.11` + la versione del venv dell'operatore.
2. **Buchi residui della denylist credenziali** (dal check delle PR #184/#185, non toccati qui):
   `token*.json` con suffisso — `token_cache.json` è leggibile perché la regex vuole il punto subito
   dopo `token` — più i già tracciati `kubeconfig` senza punto, `mywallet.dat`, `.vault-token`,
   `.dockercfg`, `_netrc`, `clientsecret.json`, `*.gpg/*.asc`.
3. **`rifletti()` chiama `create` senza `max_tokens`** (`gas.py:2786`, nota del revisore R-297-4):
   la lunghezza della risposta grezza dipende dal default del provider.
