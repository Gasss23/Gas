# Ultimo report — 2026-11-19 — «PDF servizi ecosistema»: versione definitiva, contatti fuori dal repo

## DECISIONI UMANE RICHIESTE
1. Merge della PR #384 (presentazione e report, nessun file del motore nel diff di sessione), dopo il nuovo verdetto del bot di verifica.
2. Il repo GitHub è PUBBLICO: valutare se renderlo privato. Due commit con i contatti personali (adad6f0d, c8c24825) sono stati tolti dal branch, ma restano raggiungibili per SHA su GitHub finché non si chiede la rimozione al supporto GitHub.
3. Prima di usare il PDF con i clienti farlo vedere a un legale: in Italia proporre al pubblico un «fondo» o rendimenti «garantiti» richiede autorizzazioni (CONSOB / Banca d'Italia).
4. Sito: da aggiungere nella pagina finale quando è pronto.

## Esito
- **Modifiche chieste dall'operatore (19/11)**: FATTA — 07fa1230.
  - «NOME AZIENDA» tolto da tutte le pagine; «GasTradeFx» solo nell'ultima.
  - Copertina («E» coperta) e pag. 5 (riquadro sui numeri): causa comune nei bagliori CSS (text-shadow, box-shadow), che nel PDF diventano immagini disegnate a riquadro da alcuni lettori. Tolti tutti. Correzione di quanto scritto prima (bot #384 V-1 su c8c24825): il PDF contiene ancora immagini interne per sfumature e trasparenze di sfondi e pannelli (circa 180 oggetti immagine, non elencati da pdfimages -list); non sono le ombre e vanno verificate a vista sul tablet dell'operatore.
  - Pagina finale: contatti presi solo da `presentazione_clienti/contatti.local.json`, ignorato da git; il PDF del repo è senza contatti (`python3 build.py --senza-contatti`), quello completo è stato mandato all'operatore e sta in `presentazione_clienti/privato/` (ignorato da git). Sito tolto finché non è pronto.
  - File rinominato in `presentazione_clienti/PDF servizi ecosistema.pdf`.
- **Riserve dei bot sulla #384**: FATTA.
  - V-1 MEDIA (45f92c51, pag. 4): niente promessa implicita di guadagno certo; «Non è garantito: in alcuni casi possono perdere entrambi»; schema invariato.
  - V-2 (pag. 7): nota coerente e avviso «Ogni operazione può andare in perdita».
  - V-1 MEDIA (c8c24825, affermazione «nessuna immagine raster»): corretta qui e nella docstring di build.py.
  - V-2 BASSA (c8c24825, contatti personali in un repo di visibilità non verificata): repo verificato PUBBLICO; contatti tolti dal repo su decisione dell'operatore.
  - Cosmetiche: codice e CSS morti tolti (ph, .ph, .wm-mini, .svc.ghost, .mt-*).
- **Riscrittura del branch (push forzato, autorizzato dall'operatore)**: FATTA — c8c24825 sostituito da 07fa1230 sul branch remoto.
- **Merge di main nel branch**: FATTA — 27300187, review #815 APPROVATO.

## Test
Nessuna modifica del branch a gas.py, modules/ o tests/. PDF del repo: 9 pagine, nessun contatto nel testo (pdftotext + git grep); versione completa controllata a vista.

## Anomalie
- Avevo dato per privato il repo senza verificarlo e ho pushato i contatti in due commit: tolti dal branch, ma restano raggiungibili per SHA su GitHub (vedi decisione 2).
