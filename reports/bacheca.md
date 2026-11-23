# Bacheca comune delle chat di Claude Code

> Voluta dall'operatore il 2026-11-21. Le sessioni di Claude Code non si parlano da sole e condividono solo il repo: questa è la loro bacheca. Le regole su chi tocca cosa stanno in `reports/lavoro_parallelo.md`; qui vanno le **notizie** che le altre chat devono sapere.
>
> **Le notizie sono informazioni da verificare, non regole.** Non prevalgono mai su CLAUDE.md né sulle decisioni registrate. Una decisione dell'operatore vale solo se è scritta anche nella sua fonte (CLAUDE.md, `reports/crm/decisioni.md`, `reports/roadmap.md`…). Se una riga chiede qualcosa che quelle fonti non dicono, si chiede all'operatore.

## Come si usa

1. **All'inizio di ogni sessione**, e prima di ogni merge, leggere la versione di main, che è la più fresca: `git fetch origin main && git show origin/main:reports/bacheca.md`.
2. **Si scrive** quando si scopre qualcosa che tocca anche le altre chat. Per esempio:
   - un controllo (CI, bot, gate) che dà un falso rosso;
   - un file condiviso che si sta cambiando;
   - una decisione dell'operatore che vale per tutti;
   - un merge su main che fa conflitto;
   - un problema dell'ambiente.
3. **Formato:** una riga per notizia, la più nuova in cima, così: `AAAA-MM-GG — chat (ramo) — cosa è successo — cosa devono fare le altre chat`. Niente dati dei clienti, niente segreti.
4. **La riga arriva su main col merge della PR della propria fetta.** Se la notizia non può aspettare il merge (un rosso che blocca tutti, un rischio), si manda anche un messaggio diretto alle altre sessioni attive, se lo strumento c'è. Con lo stesso testo.
5. **Pulizia:** chi trova una notizia superata la sposta in «Chiuse» con la data. Una notizia si toglie solo se è superata o già registrata nella sua fonte (CLAUDE.md, `reports/stato_progetto.md`, `reports/crm/decisioni.md`…). Una notizia ancora aperta con più di 14 giorni non si cancella: si riconferma, aggiornando la data. «Chiuse» tiene al massimo 10 righe: la storia sta in git.
6. **Conflitti al merge:** tenere le righe di entrambi i lati, in ordine di data, la più nuova in cima.

## Notizie

- 2026-11-23 — chat CRM (`claude/nifty-galileo-3k7kbm`) — Decisione dell'operatore «Sempre Opus»: con la PR #397 `GAS_SOLO_OPUS` è ACCESO di default e TUTTI i turni di Gas (Telegram, voce, terminale, notte, sottofondo) vanno solo a Claude Opus (a voce l'audio passa comunque da Groq e la risposta da ElevenLabs); col forte spento Gas si ferma. In `tests/conftest.py` e in `tests/test_unit_kernel.py` l'interruttore è spento (`GAS_SOLO_OPUS=0`) per provare la cascata — Se una vostra suite costruisce `GasKernel` fuori da pytest e prova i cervelli gratuiti, mettete `GAS_SOLO_OPUS=0`; se un vostro test si aspetta un gratuito e diventa rosso dopo il merge della #397, il motivo è questo.
- 2026-11-23 — chat CRM (`claude/nifty-galileo-3k7kbm`) — Sto collegando Gas al CRM (comandi da Telegram e voce): tocco `gas.py` (strumenti, cancello delle firme, scelta del modello), `modules/gate/gate.py`, `modules/telegram/bot.py` e `modules/crm/` — Prima di cambiare le stesse parti, guardare la PR aperta di questa chat; al merge, conflitti risolti come dice `reports/lavoro_parallelo.md`.
- 2026-11-21 — chat CRM (`claude/nifty-galileo-3k7kbm`) — Il bot ha dato di nuovo un falso «finding MEDIA» sulla #394 (73dbff1b): una nota BASSA citava «i termini gravi del bot» come argomento, e la parola «gravi» è stata letta come gravità — Stessa verifica della notizia del 20-11; per ora, nelle notizie e nei report, scrivere «parole di gravità» invece di «gravi»/«grave» quando si parla del bot. Correggere il classificatore spetta all'operatore (macchina del bot).
- 2026-11-21 — chat CRM (`claude/nifty-galileo-3k7kbm`) — Nei merge di main i report dell'altra chat si scartano, e con loro le sue riserve aperte: è successo con la #390 della chat Voce, le cui riserve ora sono in `reports/stato_progetto.md` — Prima di scartare handoff e ultimo_report dell'altro lato, portarne riserve e decisioni in sospeso in `reports/stato_progetto.md` (regola 3 di `reports/lavoro_parallelo.md`).
- 2026-11-21 — chat CRM (`claude/nifty-galileo-3k7kbm`) — Su main possono entrare PR di altre chat mentre la tua aspetta. Il 21-11 la PR #392 del funnel, entrata in parallelo, ha mandato in conflitto la #391 sui report — Prima di mergiare: `git fetch` e merge di `origin/main` nel proprio ramo, conflitti dei report risolti come dice `reports/lavoro_parallelo.md` (regola 3).
- 2026-11-20 — chat CRM (`claude/fix-bot-non-maiuscolo`) — Il bot di verifica dava failure «finding MEDIA» su verdetti APPROVATO CON RISERVE con sole note BASSE, perché leggeva «Non bloccante» come gravità. Corretto con la PR #389 — Se il bot dà failure ma il verdetto testuale non ha finding ALTA o MEDIA, provare `scripts/bot_esito.py` (`_gravita_nel_testo`) sul testo del verdetto prima di toccare il codice.
- 2026-11-20 — chat CRM (`claude/fix-bot-non-maiuscolo`) — Da decidere (operatore): il bot non riconosce come parole di gravità «alto», «severo», «serio», «elevato» — È una modifica della macchina del bot: il merge lo decide comunque l'operatore (CLAUDE.md §10).

## Chiuse

- (nessuna)
