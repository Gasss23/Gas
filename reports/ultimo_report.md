# Ultimo report — 2026-11-23 — Gas usa il CRM: comandi da Telegram e voce

## DECISIONI UMANE RICHIESTE
1. Merge della PR #397 (codice di Gas: cancello delle firme, scelta del modello, strumenti nuovi). È una fetta di sicurezza: secondo controllo su claude.ai col link della PR.
2. Falsi allarmi del filtro «solo Opus» (R-840-2, decidi tu): un messaggio con «clienti», «commissione», «versato», «deposito» o un numero lungo che inizia con 0 o 3 va solo a Opus; se il cervello forte è spento o al tetto, quel turno (e il successivo) si ferma con «contiene dati di clienti». Scelte: tenere così (privacy prima), togliere qualche parola, o un messaggio più chiaro.
3. Privacy, da sapere e confermare: le conversazioni con Gas sui clienti restano nella storia di Gas (`.gas_history.json`), le richieste di firma nella sua memoria (`.gas_memory.db`), e i messaggi passano da Telegram come la chat di oggi. Nel diario di Gas non vanno nomi né cifre dei clienti. A voce i dati passano da Groq (trascrizione) ed ElevenLabs (voce).
4. Restano dalle fette prima: lista delle commissioni per servizio; sul Mac password delle copie nel `.env`, `pip install -r requirements.txt`, `pwd` della cartella di Gas, prova della copia e del ripristino; secondo controllo su claude.ai delle PR #387, #388, #389 e #391; decisione sulle parole di gravità del bot («alto», «severo», «serio», «elevato»).
5. Ereditata dalla chat Voce: rifare la registrazione della voce sul Mac con lo script corretto e incollare il riepilogo.

## Esito
- **Richiesta dell'operatore** («posso usare il mio agente IA e dargli comandi per utilizzare il crm? aggiungere, togliere, ricordarmi»), con la proposta scelta «Sì, fallo tu qui»: registrata come decisione 18 in `reports/crm/decisioni.md`; notizia in `reports/bacheca.md` (questa chat tocca `gas.py`, cancello e bot Telegram).
- **Tappa 1, lato CRM**: FATTA (commit f7a4c12c, review #839-CRM APPROVATO CON RISERVE). Promemoria nello store (mai cancellati, reclamo prima dell'invio), `modules/crm/agente.py` (consulta, prepara senza scrivere, applica solo la forma canonica dopo la firma).
- **Riserve #839-CRM**: CHIUSE nel commit della tappa 2. R-839-1 MEDIA (il nome si cerca solo a inizio parola: «Anna» non trova più «Marianna»; se trovato per somiglianza la firma lo dice); R-839-2..7 BASSE (test per i mutanti, prelievo oltre il capitale e riattivazione detti prima della firma, date/ore/#numeri non sono importi, garanzia dei promemoria dichiarata, id enormi, la firma mostra il valore sostituito) e le cosmetiche.
- **Tappa 2, aggancio a Gas**: FATTA (commit c8d4f977, review #840-CRM APPROVATO CON RISERVE; riserve corrette in 0afc1a79 — review #841-CRM BOCCIATO perché il nuovo controllo dei telefoni scattava dentro i codici delle firme, poi #842-CRM APPROVATO CON RISERVE — e test rinforzati in 070e7ad3, review #843-CRM APPROVATO CON RISERVE). PR #397.
  - `crm_consulta` (sola lettura) e `crm_modifica` (sempre alla firma su Telegram, con la descrizione per esteso).
  - Dati del CRM solo a Claude Opus: una richiesta che parla di clienti, promemoria o soldi va a Opus dalla prima chiamata; un modello diverso che chiama gli strumenti riceve un diniego e il turno passa a Opus.
  - Importi solo se scritti dall'operatore nel messaggio del turno (non valgono le cifre lette dal CRM né quelle del modello).
  - Niente modifiche dai compiti in sottofondo; diario e progressi su Telegram senza dati dei clienti.
  - Promemoria su Telegram dal giro di ogni minuto del bot.
- **Guida**: `reports/crm/guida.md` spiega come usare il CRM parlando con Gas.
- **Anomalia nel fine-task**: un primo tentativo di scrivere l'handoff ha fatto eseguire alla shell i testi tra apici inversi (tra cui `pip install -r requirements.txt` nel container, la suite del kernel e `claude -p` senza input, finito in errore). Nessun file scritto, nessun commit né push; cambiati solo log e cache ignorati da git. Rifatto con file temporanei.

## Test
- Motore: `python tests/test_unit_kernel.py` → 1206 PASS, 0 FAIL (prima 1191; nuovi T118a-g, T118c2, T118e2, T118f2). Anche con gli UUID delle firme forzati ad avere 7 cifre di fila: 1206 PASS. Adattati due test vecchi alla regola nuova: T80 («per il cliente Rossi» → «per Rossi») e T116h («ricordami» → «poi sistemo»).
- CRM: `pytest tests/test_unit_crm.py` → 150 passed (prima 139).
- Le altre suite della CI (pytest): 3512 passed (sull'albero di 0afc1a79; 070e7ad3 cambia solo un commento in gas.py, test e guida).

## Riserve aperte
- **R-840-2 MEDIA, decide l'operatore** (vedi decisione 2). R-842-2 BASSA (formati di telefono non riconosciuti, dichiarati), R-842-3 BASSA (numeri lunghi che iniziano con 0 o 3 presi per telefoni, dichiarato), R-843-1 BASSA («+1.500.000» preso per telefono, non dichiarato). Cosmetiche nei verdetti #842/#843. Non verificato: Telegram, voce e `claude -p` veri.
- Dal CRM: R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`): R-813M1-1 BASSA, note basse del bot #390 (V-1/V-2/V-3), R-810M1-2 BASSA attenuata, note basse #382 V-1/V-2 e #383 V-2/V-3, punteggi della voce da lontano non verificati.
