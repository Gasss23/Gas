# ULTIMO REPORT — 2026-10-27 — Mani fetta 19: prova della lettura con lexbor, spenta (R6, chat Mani, PR #275)

## DECISIONI UMANE RICHIESTE
1. Merge della PR #275 (https://github.com/Gasss23/Gas/pull/275): la mergio da solo solo con APPROVATO pulito del bot sull'head, altrimenti serve il tuo OK. Il merge NON accende niente: la lettura resta spenta.
2. **Accendere la lettura con lexbor?** Per accenderla servono, nell'ordine:
   - R-521-1 e R-521-2 sistemate (piccole, nella mia area);
   - un'occhiata ai 5 casi con `<select>`;
   - la chat Motore: selectolax in `requirements.txt` e in CI, e la variabile `GAS_WEB_LEXBOR=1` sul VPS.
3. Poi, una alla volta: R-ve252-2 e R-ve255-1 (XHTML malformato), tempo di rete 12 s, R-ve235-7.

## Esito
- **PR #272 (fetta 18)** — MERGIATA dall'operatore («mergia», 1212a17), con bot e verifica esterna APPROVATO CON RISERVE (solo BASSE: due test mancanti e R-518-1).
- **Prova lexbor (R-ve246-5)** — FATTA, spenta per default.
  - `modules/web/lexbor.py`: lexbor (selectolax, script attivi) gira in un processo figlio, con 4 s di tempo massimo e 1 GiB di memoria. Parte solo con `GAS_WEB_LEXBOR=1`, dopo una sonda del figlio. Su ogni errore Gas torna alla lettura di sempre.
  - `leggi.py`: la lettura di oggi è spostata in `_testo_e_titolo`, senza cambiarla; `_componi` prova lexbor solo se è acceso e la pagina non è XHTML.
- **Riserve della review**:
  - #520: R-520-1, R-520-2 e R-520-3 → FATTE; R-520-4 COSMETICA → DEFERITA.
  - #521: R-521-1 e R-521-2 BASSE, R-521-3 COSMETICA → DEFERITE, prima dell'accensione.

## Misure della prova (script nello scratchpad, fuori dal repo)
1. **Costo di lexbor:** è quadratico su decine di migliaia di tag annidati che a ogni apertura scandiscono la pila. Sono 31 tag (div, section, ul…): 50 mila ≈ 6 s, 100 mila ≈ 23 s. Lo stesso vale per migliaia di attributi diversi in un tag (50 mila ≈ 8 s).
   - La chiamata in C non si interrompe: da qui il processo figlio.
   - Un controllo con espressioni regolari prima di lexbor era aggirabile (`</div>` nei commenti, `>` negli attributi) ed è stato scartato.
   - Col figlio, le pagine patologiche si fermano a 4 s e passano alla lettura di sempre.
2. **Sicurezza:** oracolo indipendente html5lib su 60 mila pagine casuali senza template/svg/math (seed 7-9, 20 mila ciascuno).
   - Fughe: oggi 48 + 40 + 41 = 129, con lexbor 0 + 3 + 2 = 5, tutte con `<select>`.
   - Perdite: oggi 2.975 / 2.907 / 2.831, con lexbor 1.860 / 1.765 / 1.764.
   - Con template/svg/math html5lib 1.1 segue uno standard vecchio (`</p>` nel contenuto estraneo, `</template>` con ul/p aperti) e non fa da oracolo.
3. **Casi noti di R-ve246-5** (`<canvas>W0<p/></canvas>W1` e altri): tutti nascosti con lexbor, mostrati oggi.
4. **Pagine vere:** 131 pagine di documentazione locali, 127 con le stesse parole; le 4 diverse sono file di test sui charset. Tempo 15,8 s contro 10,6 s, cioè circa 40 ms in più a pagina per il figlio.
5. **Robustezza:** 200 mila pagine con NUL, surrogati e riferimenti enormi: nessuna eccezione né crash.
6. **Suite vecchia con lexbor acceso:** 11 FAIL.
   - 3 sono test dei log del percorso html.parser.
   - 8 sono casi frameset/template che codificano il «verso sicuro»: lì il browser mostra il testo, e lexbor e html5lib concordano su tutti e 7 i casi provati.

## Test
- Web suite (spenta): 441 + 20 nuovi = 461 passed, 1 skipped su Python 3.13.16 (con selectolax); 443 passed, 19 skipped su 3.11 (senza); 451 passed, 11 skipped col parser vecchio forzato.
- Mutazioni del ramo lexbor, tutte prese (FAIL su 20 test): corpo senza `_pulisci` 1, titolo senza tetto 1, senza sonda 1, sonda ripetuta 1, acceso sempre 1, titolo non nascosto 1, nascosti ignorati 5, script spenti 1, titolo di svg accettato 1, blocchi senza a capo 1, anche in XHTML 1. Prima della sonda anche «senza tempo massimo» (1).

## RICHIESTE ALLA CHAT MOTORE
1. Solo se l'operatore decide di accendere la lettura con lexbor:
   - aggiungere `selectolax` (versione da fissare, oggi 1.0.2) a `requirements-dev.txt`, così i test di `tests/test_unit_web_lexbor.py` girano in CI invece di saltarsi;
   - aggiungerlo a `requirements.txt` del VPS;
   - mettere `GAS_WEB_LEXBOR=1` nell'ambiente di Gas.

## Anomalie
- Push dei commit riuscito solo dopo nuovi tentativi (errore del server GitHub, fetta 18).
- `gh` non autenticato nel cloud: PR, etichetta e stato CI passano dall'integrazione GitHub.
- Nel cloud niente rete verso siti veri: le «pagine vere» sono documentazione HTML installata sulla macchina.
