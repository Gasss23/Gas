# Ultimo report — 2026-11-23 — Gas usa il CRM: comandi da Telegram e voce

## DECISIONI UMANE RICHIESTE
1. Merge della PR #397: l'operatore ha detto «ok avvisami quando hai mergiato» (via al merge). Fetta di sicurezza: il secondo controllo su claude.ai col link della PR resta consigliato.
2. Da sapere: con «Sempre Opus» (decisione 19) se Opus non c'è (forte spento o tetto del giorno finito) Gas non risponde finché non torna; il tetto giornaliero del forte si consuma prima. A voce l'audio passa comunque da Groq (trascrizione) e la risposta da ElevenLabs. Per tornare al filtro per parole: `GAS_SOLO_OPUS=0` nel `.env`.
3. Privacy, da sapere: le conversazioni con Gas sui clienti restano nella storia di Gas (`.gas_history.json`), le richieste di firma nella sua memoria (`.gas_memory.db`), e i messaggi passano da Telegram come la chat di oggi. Nel diario di Gas non vanno nomi né cifre dei clienti.
4. Restano dalle fette prima: lista delle commissioni per servizio; sul Mac password delle copie nel `.env`, `pip install -r requirements.txt`, `pwd` della cartella di Gas, prova della copia e del ripristino; secondo controllo su claude.ai delle PR #387, #388, #389 e #391; decisione sulle parole di gravità del bot («alto», «severo», «serio», «elevato»).
5. Ereditata dalla chat Voce: rifare la registrazione della voce sul Mac con lo script corretto e incollare il riepilogo.

## Esito
- **Richiesta dell'operatore** («posso usare il mio agente IA e dargli comandi per utilizzare il crm? aggiungere, togliere, ricordarmi»), con la proposta scelta «Sì, fallo tu qui»: registrata come decisione 18 in `reports/crm/decisioni.md`; notizia in `reports/bacheca.md` (questa chat tocca `gas.py`, cancello e bot Telegram).
- **Tappa 1, lato CRM**: FATTA (commit f7a4c12c, review #839-CRM APPROVATO CON RISERVE). Promemoria nello store (mai cancellati, reclamo prima dell'invio), `modules/crm/agente.py` (consulta, prepara senza scrivere, applica solo la forma canonica dopo la firma).
- **Riserve #839-CRM**: CHIUSE nel commit della tappa 2. R-839-1 MEDIA (il nome si cerca solo a inizio parola: «Anna» non trova più «Marianna»; se trovato per somiglianza la firma lo dice); R-839-2..7 BASSE (test per i mutanti, prelievo oltre il capitale e riattivazione detti prima della firma, date/ore/#numeri non sono importi, garanzia dei promemoria dichiarata, id enormi, la firma mostra il valore sostituito) e le cosmetiche.
- **Tappa 2, aggancio a Gas**: FATTA (commit c8d4f977, review #840-CRM APPROVATO CON RISERVE; riserve corrette in 0afc1a79 — review #841-CRM BOCCIATO perché il nuovo controllo dei telefoni scattava dentro i codici delle firme, poi #842-CRM APPROVATO CON RISERVE — e test rinforzati in 070e7ad3, review #843-CRM APPROVATO CON RISERVE; marcatore sull'IP di prova di un test in e98be2cc, review #844-CRM APPROVATO, dopo che il controllo degli IP del fine-task aveva fermato il primo push). PR #397.
  - `crm_consulta` (sola lettura) e `crm_modifica` (sempre alla firma su Telegram, con la descrizione per esteso).
  - Dati del CRM solo a Claude Opus: una richiesta che parla di clienti, promemoria o soldi va a Opus dalla prima chiamata; un modello diverso che chiama gli strumenti riceve un diniego e il turno passa a Opus.
  - Importi solo se scritti dall'operatore nel messaggio del turno (non valgono le cifre lette dal CRM né quelle del modello).
  - Niente modifiche dai compiti in sottofondo; diario e progressi su Telegram senza dati dei clienti.
  - Promemoria su Telegram dal giro di ogni minuto del bot.
- **Guida**: `reports/crm/guida.md` spiega come usare il CRM parlando con Gas.
- **Verifica esterna PR #397**: APPROVATO CON RISERVE (commento sulla PR). V-1 MEDIA: i dati di un cliente nuovo senza parole del CRM passano prima dal modello normale → dichiarato e rinviato a te (decisione 3); la sua affermazione che la frase «usa la parola cliente» mancasse nella guida era sbagliata (c'era, l'ha cercata alla lettera). V-2 BASSA: «20 mila» o «1 500» ammettono più cifre (la firma mostra quella vera). V-3 BASSA: CI dell'ultimo commit non ancora pronta alla scrittura dell'handoff.
- **Bot di verifica su 82afe955**: failure, ma per un verdetto incoerente del bot (APPROVATO CON RISERVE con «FINDING: nessuno»), non per il codice. Riparte sul commit nuovo.
- **Scelta dell'operatore «Sempre Opus»** (decisione 19, dopo la nota V-1): FATTA (d409cc8a, review #848-CRM APPROVATO CON RISERVE). `GAS_SOLO_OPUS` acceso di default: ogni turno (Telegram, voce, terminale, notte, sottofondo, riflessione) va solo a Opus; col forte spento Gas si ferma e lo dice. La V-1 della verifica esterna e R-840-2 sono superate con l'interruttore acceso (valgono solo con `GAS_SOLO_OPUS=0`). R-848-1 MEDIA (documenti che promettevano «anche ciò che dici» senza dire di Groq ed ElevenLabs): corretta in d814eb3d. Registrata in CLAUDE.md §2 e in bacheca.
- **Bot di verifica su ea67777b**: APPROVATO CON RISERVE (V-1 MEDIA, la stessa della verifica esterna: superata dalla decisione 19; V-2 COSMETICA sulla guida: corretta).
- **Dopo la verifica esterna**: provato ad allargare il filtro a email ed euro → fa fallire due test vecchi scritti contro i blocchi inutili (T115c6, T80ad): lasciato a te. Correzione di R-843-1 → review #845-CRM BOCCIATO (perdeva telefoni col «+» e i trattini): tolta, R-843-1 dichiarata (#846-CRM); commento corretto (#847-CRM).
- **Anomalia nel fine-task**: un primo tentativo di scrivere l'handoff ha fatto eseguire alla shell i testi tra apici inversi (tra cui `pip install -r requirements.txt` nel container, la suite del kernel e `claude -p` senza input, finito in errore). Nessun file scritto, nessun commit né push; cambiati solo log e cache ignorati da git. Rifatto con file temporanei.

## Test
- Motore: `python tests/test_unit_kernel.py` → 1212 PASS, 0 FAIL (prima 1191; nuovi T118a-g, T118c2, T118e2, T118f2, T119a-f). Anche con gli UUID delle firme forzati ad avere 7 cifre di fila: 1206 PASS. Adattati due test vecchi alla regola nuova: T80 («per il cliente Rossi» → «per Rossi») e T116h («ricordami» → «poi sistemo»).
- CRM: `pytest tests/test_unit_crm.py` → 150 passed (prima 139).
- Le altre suite della CI (pytest): 3512 passed anche con «Sempre Opus» (le suite pytest lo spengono in `tests/conftest.py` per provare la cascata).

## Riserve aperte
- R-848-2 BASSA (il doctor non avvisa che col forte spento Gas resta muto), R-848-3 BASSA (lo «Sempre Opus» è provato solo nella suite del kernel); cosmetiche #848. R-840-2 e V-1 della verifica esterna valgono solo con `GAS_SOLO_OPUS=0`. R-842-2 BASSA (formati di telefono non riconosciuti, dichiarati), R-842-3 BASSA (numeri lunghi che iniziano con 0 o 3 presi per telefoni, dichiarato), R-843-1 BASSA («+1.500.000» preso per telefono, dichiarato; correzione rinviata per prudenza). V-2/V-3 BASSE della verifica esterna. Cosmetiche nei verdetti #842/#843. Non verificato: Telegram, voce e `claude -p` veri.
- Dal CRM: R-836-1 COSMETICA.
- Ereditate dalla chat Voce (in `reports/stato_progetto.md`): R-813M1-1 BASSA, note basse del bot #390 (V-1/V-2/V-3), R-810M1-2 BASSA attenuata, note basse #382 V-1/V-2 e #383 V-2/V-3, punteggi della voce da lontano non verificati.
