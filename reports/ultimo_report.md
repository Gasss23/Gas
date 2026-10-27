# ULTIMO REPORT — 2026-10-27 — Mani fetta 20: lettura con lexbor pronta per l'accensione, ancora spenta (R6, chat Mani, PR #277)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #277 (https://github.com/Gasss23/Gas/pull/277): la mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK. Il merge non accende niente.
2. **Accensione**: serve la chat Motore (vedi RICHIESTE ALLA CHAT MOTORE). Dopo, sul VPS (Linux): `GAS_WEB_LEXBOR=1`.
3. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #275 (fetta 19)** — MERGIATA dall'operatore («mergia», a0bf5c9), con bot e verifica esterna APPROVATO CON RISERVE (solo BASSE e cosmetiche).
- **Preparazione dell'accensione** — FATTA, lettura ancora spenta per default:
  - R-521-1 (sonda con lock non bloccante) e R-521-2 (sonda finita oltre il tempo riprovata dopo 600 s): FATTE.
  - Solo Linux: fuori da Linux il figlio esce con 3, perché il tetto RLIMIT_AS altrove non vale, e si usa la lettura di sempre (V-1 bot #275): FATTA.
  - Ultima riga dello stderr del figlio nel warning, ripulita e tagliata (V-2 bot #275): FATTA.
  - Stima dei tempi con la sonda, circa 23 s nel caso peggiore (V-2 bot / V-3 verifica esterna #275): FATTA.
  - R-521-3 e R-524-1 (cosmetiche): FATTE.
  - Casi con `<select>`: erano testo dentro un select fuori dalle opzioni. Il figlio ora nasconde select, datalist, rp, gli elementi con attributo `hidden` e i dialog chiusi, come il browser: FATTA.
- **Review**:
  - #525 APPROVATO CON RISERVE: R-525-1 (`nodo.attrs`), R-525-2 (test del lock), R-525-3 (test della pulizia dello stderr) → FATTE.
  - #526 APPROVATO CON RISERVE: R-526-1 COSMETICA (doppio controllo sotto lock senza test) → DEFERITA.
  - R-520-4 COSMETICA resta aperta.

## Prove (codice finale ab5eb1d)
- Web suite: 441 (main) + 28 test lexbor = 469 passed, 1 skipped su 3.13.16 (con selectolax); 444 passed, 26 skipped su 3.11 senza selectolax. Parser vecchio forzato: 459 passed, 11 skipped.
- Suite vecchia con `GAS_WEB_LEXBOR=1`: ancora 11 FAIL, gli stessi della fetta 19 (3 test dei log, 8 casi frameset/template dove il browser mostra il testo).
- Mutazioni, tutte prese (FAIL su 27-28 test):
  - senza lock: 1;
  - timeout che spegne per sempre: 1;
  - risonda subito: 1;
  - anche fuori da Linux: 1;
  - hidden ignorato: 1;
  - dialog chiuso visibile: 1;
  - select visibile: 1;
  - rp visibile: 1;
  - stderr non nel log: 2;
  - lock bloccante: 1;
  - senza isprintable: 1;
  - senza taglio a 200: 1.
- Oracolo html5lib su 60 mila pagine senza template/svg/math (seed 7-9):
  - fughe: con lexbor 0 + 0 + 0, oggi 48 + 40 + 41;
  - perdite: con lexbor 2.808 / 2.717 / 2.700, oggi 2.975 / 2.907 / 2.831. Le perdite con lexbor salgono rispetto alla fetta 19 perché html5lib conta come visibile il testo dei select, che il browser non mostra.
- 131 pagine di documentazione locali: 127 con le stesse parole, come prima.

## RICHIESTE ALLA CHAT MOTORE
1. Per accendere la lettura con lexbor (decisione dell'operatore: «prepara l'accensione»):
   - aggiungere `selectolax==1.0.2` a `requirements-dev.txt`, così in CI girano i 25 test lexbor oggi saltati (isolamento del figlio compreso);
   - aggiungerlo a `requirements.txt` del VPS;
   - mettere `GAS_WEB_LEXBOR=1` nell'ambiente di Gas sul VPS (Linux). Sul Mac resta spenta da sola.

## Anomalie
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
