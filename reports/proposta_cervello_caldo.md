# Proposta — cervello forte «caldo» per la voce (chat M2, 2 novembre)

Solo proposta: **nessun codice finché l'operatore non sceglie**. Il cambio toccherebbe `brains/claude_cli.py` e forse `gas.py`.

## Il problema

A ogni turno col cervello forte `brains/claude_cli.py` lancia da zero `claude -p` (CLI di Claude Code, login dell'abbonamento Max). Il processo si avvia, legge la configurazione, risponde ed esce. Se un turno usa strumenti di Gas, `run_turn` lo rilancia per ogni giro del ciclo. Quanto pesa l'avvio **non è misurato**: la documentazione non dà numeri. La V7a (ramo `feat/voce-v7-m2`) mostra il tempo del «cervello» nella pagina e in `gas_debug.log`, ma dentro c'è anche il ragionamento del modello.

## Prima cosa da fare: misurare (5 minuti sul Mac, nessun codice)

Nel Terminale, due volte ciascuno:
1. `time (echo "rispondi solo: ok" | claude -p --tools "" --setting-sources "" --no-session-persistence)`: avvio più una risposta minima.
2. Lo stesso con un prompt lungo (~2 000 parole): conta quanto pesa il contesto rispetto all'avvio.

Se l'avvio vale meno di 1–2 s su un turno a voce di 8–15 s, il processo caldo serve a poco. In quel caso conviene altro: risposte più corte, la voce frase per frase della V7b, il cervello normale per le domande semplici.

## Le tre strade

| | A. Processo pre-avviato | B. Sessione calda con l'Agent SDK | C. Com'è oggi |
|---|---|---|---|
| Idea | Mentre l'operatore parla e Whisper trascrive, `claude -p` è già partito e aspetta la domanda sullo stdin | Un processo `ClaudeSDKClient` resta acceso fra un turno e l'altro e riceve le domande in streaming | Un processo nuovo a ogni chiamata |
| Risparmio | L'avvio, se l'avvio avviene davvero prima di leggere lo stdin: **da verificare** | L'avvio e forse parte del contesto | — |
| Cosa tocca | `brains/claude_cli.py`: un processo «di scorta» (Popen) per il modello forte, sostituito dopo ogni uso; il system prompt per turno va passato quando parte la domanda, non all'avvio (oggi è un file passato all'avvio, da ripensare) | Nuova dipendenza (`claude-agent-sdk`, Python asincrono) e un client nuovo in `brains/`; probabilmente anche `gas.py` per tenere vivo il processo | Niente |
| Rischio | Basso: ogni turno resta senza memoria (stateless) e le regole di oggi non cambiano (niente strumenti di Claude, lista di variabili permesse, codice nei tag). Un processo di scorta inutilizzato consuma poca memoria | **Alto**: la sessione accumula la conversazione per conto suo, fuori da `_get_window` e dal tetto della finestra di Gas. Si rischiano doppioni della storia, contesto che cresce, costi che salgono e il rischio di un taglio della cronologia sbagliato (§5 di CLAUDE.md). Bisogna verificare che i tool integrati si spengano del tutto: la doc dice che `disallowed_tools` toglie i tool nominati, ma non c'è una frase su «nessun tool» (**da verificare**). Un processo lungo va poi sorvegliato (crash, login scaduto, interrupt da svuotare: la doc avverte che `interrupt()` non svuota il buffer) | Nessuno |
| Regole d'uso | Come oggi (via B del 23 ottobre: `claude -p` col login dell'abbonamento) | **Da verificare**: vedi sotto | Come oggi |

## Regole d'uso dell'abbonamento (cosa dice la documentazione letta il 2 novembre)

Pagine lette: `code.claude.com/docs/en/agent-sdk/overview`, `.../quickstart`, `.../authentication`, `.../headless`.
- Agent SDK, frase identica in overview e quickstart: «Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods described in the Quickstart instead.» Il quickstart usa `ANTHROPIC_API_KEY`. La doc **non dice** in modo esplicito se un uso personale dell'SDK col login dell'abbonamento sia permesso: **da verificare** con il supporto o le pagine di supporto (non lette).
- `claude -p` senza `--bare` usa la stessa catena di credenziali della CLI: «Subscription OAuth credentials from `/login`. This is the default for Claude Pro, Max, Ultra, Team, and Enterprise users». Con `--bare` invece no: «bare mode doesn't use your subscription login». Quindi `--bare`, che accorcia l'avvio, **non** si può usare con l'abbonamento.
- Resta valida l'ambiguità già scritta in `reports/r2_regole_abbonamento.md`: Consumer Terms §3.7 sull'uso automatico, rischio accettato dall'operatore il 23 ottobre per `claude -p`. Passare all'SDK è un uso diverso da quello deciso allora: **va rideciso**.

## Proposta

1. **Misurare** (sezione sopra) e mandare i numeri a M1.
2. Se l'avvio pesa più di ~2 s: **strada A**, in una fetta piccola su `brains/claude_cli.py`, con revisore, test e prova sul Mac. Regole d'uso invariate.
3. **Strada B solo dopo** che l'operatore ha chiarito le regole d'uso dell'SDK con l'abbonamento, e con un piano per tenere la storia sotto `_get_window`. Oggi non la consiglio.

Decide l'operatore: misurare sì o no, poi A, B o niente.
