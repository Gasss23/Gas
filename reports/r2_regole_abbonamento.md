# R2 — Regole d'uso dell'abbonamento Claude per Gas (verifica del 23 ottobre 2026)

> Verifica chiesta dalla roadmap (R2: «riverificare sulla pagina ufficiale prima di costruire»). Fatta dalla chat Motore il 23 ottobre 2026 leggendo le pagine ufficiali. Le frasi tra virgolette sono citazioni testuali.

## Fonti lette
- https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan (aggiornamenti del 15 giugno e del 7 ottobre 2026)
- https://support.claude.com/en/articles/17154008 (crediti API mensili inclusi nei piani)
- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://www.anthropic.com/legal/consumer-terms (in vigore dall'8 ottobre 2025)

## Cosa dicono
1. **Login dell'abbonamento (OAuth) con `claude -p` / Agent SDK**: permesso nei limiti del piano. «You can still use the Claude Agent SDK, `claude -p`, and third-party apps with your subscription limits.» I limiti sono la finestra di 5 ore e quello settimanale, condivisi con Claude e Claude Code.
2. **Ma per l'uso automatico c'è un'ambiguità**: le Consumer Terms (sez. 3, punto 7) vietano di accedere ai servizi «through automated or non-human means, whether through a bot, script, or otherwise», salvo «via an Anthropic API Key or where we otherwise explicitly permit it». Le pagine di supporto non dicono chiaramente se un agente che gira da solo su un server con il login dell'abbonamento sia «explicitly permitted».
3. **Crediti API inclusi nel Max 5x: 100 $ al mese** (Max 20x: 200 $). Coprono la Messages API, Managed Agents e l'Agent SDK, ma `claude -p` e SDK solo «when you run them yourself with an API key from your linked Claude Console organization». Con il login dell'abbonamento invece si consumano i limiti del piano, non i crediti. I crediti non si accumulano tra un mese e l'altro; finiti i crediti, le richieste si fermano fino al mese dopo e «Usage is never charged to your Claude plan». Per attivarli serve collegare un'organizzazione della Console (una sola, dopo 7 giorni sul piano).
4. **Attenzione tecnica**: se nel sistema c'è `ANTHROPIC_API_KEY`, Claude Code usa la chiave e non l'abbonamento.
5. Il consumo residuo dell'abbonamento si vede con `/status` (interattivo); non c'è un modo documentato per leggerlo da un programma.

## Conseguenza per R2 (proposta della chat Motore, decide l'operatore)
- **Via A — API key con i 100 $ al mese inclusi nel Max (consigliata)**: è la strada esplicitamente permessa per l'uso automatico (API key → Commercial Terms). Il consumo di Gas è separato dall'abbonamento che usi tu con Claude Code (non tocca i tuoi limiti), ha un tetto naturale (100 $ al mese, poi si ferma, mai addebiti in più) e si misura dai token di ogni risposta, che Gas già registra. Il tetto del 20% al giorno diventa circa 3,30 $ al giorno sui 100 $ mensili, oppure un tetto giornaliero a scelta.
- **Via B — `claude -p` col login dell'abbonamento**: usa i limiti del piano (5 ore + settimanale) che condividi con lo sviluppo, il consumo residuo non si legge da programma, e l'uso automatico su server è ambiguo per le Consumer Terms. Sconsigliata finché Anthropic non lo chiarisce.
- Nota: la decisione del 19 ottobre «crediti API da 100 $: non usati per ora» era stata presa quando i crediti non erano inclusi nel piano; con l'aggiornamento del 7 ottobre sono inclusi nel Max 5x.

## Da decidere (operatore)
1. Via A o via B.
2. Se via A: collegare l'organizzazione Console al piano Max (impostazioni dell'account claude.ai), creare una API key dedicata a Gas e metterla nel `.env` del Mac (`ANTHROPIC_API_KEY` solo nel `.env` di Gas, non nel profilo della shell, altrimenti anche Claude Code la userebbe al posto dell'abbonamento).
