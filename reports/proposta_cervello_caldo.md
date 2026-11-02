# Proposta — cervello forte «caldo» per la voce (chat M2, 2 novembre)

Solo proposta: **nessun codice finché l'operatore non sceglie**. Il cambio toccherebbe `brains/claude_cli.py` e forse `gas.py`.

## Il problema

A ogni turno col cervello forte `brains/claude_cli.py` lancia da zero `claude -p` (CLI di Claude Code, login dell'abbonamento Max). Il processo si avvia, legge la configurazione, risponde ed esce. Se un turno usa strumenti di Gas, `run_turn` lo rilancia per ogni giro del ciclo. Quanto pesa l'avvio **non è misurato**: la documentazione non dà numeri. La V7a (ramo `feat/voce-v7-m2`) mostra il tempo del «cervello» nella pagina e in `gas_debug.log`, ma dentro c'è anche il ragionamento del modello.

## Prima cosa da fare: misurare (5 minuti sul Mac, nessun codice)

Va misurato col comando VERO di Gas, preso dal codice stesso (`ClaudeCliClient.comando`, `.env` di Gas caricato prima come fa la CLI, stesse variabili d'ambiente filtrate da `_ambiente_pulito`: niente `ANTHROPIC_API_KEY`, quindi login dell'abbonamento come in Gas; stesso modello forte e stesso schema), lanciato da una cartella vuota (V-1/V-2 bot #320). Lo script stampa binario e modello usati, per controllo. Dal Terminale, nella cartella di Gas:

```
cd ~/Gas && python3 - <<'PY'
import json, os, subprocess, tempfile, time
from gas import _carica_dotenv
_carica_dotenv()   # come la CLI di Gas: il .env (binario, login) prima di tutto
from brains.claude_cli import ClaudeCliClient, _ambiente_pulito
from brains.model_ids import MODEL_CLAUDE_FORTE
modello = MODEL_CLAUDE_FORTE   # lo stesso valore di Gas (fissato all'import, come in gas.py)
with tempfile.TemporaryDirectory() as d:
    sistema = os.path.join(d, "sistema.txt")
    open(sistema, "w").write("Rispondi in una frase.")
    cmd = ClaudeCliClient().comando(modello, sistema)
    print("binario:", cmd[0], "· modello:", modello)
    for domanda in ["rispondi solo: ok"] * 2 + ["riassumi: " + "parola " * 2000] * 2:
        t = time.monotonic()
        p = subprocess.run(cmd, input=domanda, capture_output=True, text=True, cwd=d,
                           env=_ambiente_pulito(), timeout=300)
        tot = time.monotonic() - t
        try:
            api = (json.loads(p.stdout).get("duration_api_ms") or 0) / 1000
        except ValueError:
            print("risposta non JSON:", (p.stderr or p.stdout)[:200]); continue
        print(f"totale {tot:.1f}s · modello {api:.1f}s · avvio e resto {tot - api:.1f}s")
PY
```

Il numero da confrontare con la soglia è **«avvio e resto»** (totale meno il tempo del modello). Il campo `duration_api_ms` nella risposta JSON di `claude -p` è **da verificare**: se manca, «modello» esce 0 e allora si confronta con `time claude --version` (solo l'avvio del programma, che sottostima l'avvio vero).

Se «avvio e resto» vale meno di 1–2 s su un turno a voce di 8–15 s, il processo caldo serve a poco. In quel caso conviene altro: risposte più corte, la voce frase per frase della V7b, il cervello normale per le domande semplici.

## Le tre strade

| | A. Processo pre-avviato | B. Sessione calda con l'Agent SDK | C. Com'è oggi |
|---|---|---|---|
| Idea | Mentre l'operatore parla e Whisper trascrive, `claude -p` è già partito e aspetta la domanda sullo stdin | Un processo `ClaudeSDKClient` resta acceso fra un turno e l'altro e riceve le domande in streaming | Un processo nuovo a ogni chiamata |
| Risparmio | L'avvio, se l'avvio avviene davvero prima di leggere lo stdin: **da verificare**. Nei turni con strumenti (più chiamate di fila) si risparmia solo se il processo di scorta seguente è già pronto quando serve: con un solo processo di riserva, di sicuro solo sulla prima chiamata (V-3 bot #320) | L'avvio e forse parte del contesto | — |
| Cosa tocca | `brains/claude_cli.py`: un processo «di scorta» (Popen) per il modello forte, sostituito dopo ogni uso; il system prompt per turno va passato quando parte la domanda, non all'avvio (oggi è un file passato all'avvio, da ripensare) | Nuova dipendenza (`claude-agent-sdk`, Python asincrono) e un client nuovo in `brains/`; probabilmente anche `gas.py` per tenere vivo il processo | Niente |
| Rischio | Medio, con un nodo aperto (V-1 bot #320): ogni turno resta senza memoria e restano niente strumenti di Claude e lista di variabili permesse, MA il system prompt di ogni turno (codice casuale dei ruoli, istruzioni sui dati non fidati, pin dei lead) oggi arriva con `--system-prompt-file` all'avvio. Se il processo parte prima, quel prompt non si può mettere nello stdin (varrebbe come testo dell'utente e si indebolirebbe la difesa del codice casuale per chiamata, review #496 che chiude R-494-1/2): va trovato un modo sicuro, per esempio un file scritto prima che la CLI lo legga, da verificare. Memoria del processo di scorta (è un processo Node): da misurare | **Alto**: la sessione accumula la conversazione per conto suo, fuori da `_get_window` e dal tetto della finestra di Gas. Si rischiano doppioni della storia, contesto che cresce, costi che salgono e il rischio di un taglio della cronologia sbagliato (§5 di CLAUDE.md). Bisogna verificare che i tool integrati si spengano del tutto: la doc dice che `disallowed_tools` toglie i tool nominati, ma non c'è una frase su «nessun tool» (**da verificare**). Un processo lungo va poi sorvegliato (crash, login scaduto, interrupt da svuotare: la doc avverte che `interrupt()` non svuota il buffer) | Nessuno |
| Regole d'uso | Come oggi (via B del 23 ottobre: `claude -p` col login dell'abbonamento), con il rischio del futuro default `--bare` (sotto) | **Da verificare**: vedi sotto | Come oggi, con lo stesso rischio del futuro default `--bare` |

## Regole d'uso dell'abbonamento (cosa dice la documentazione letta il 2 novembre)

Pagine lette: `code.claude.com/docs/en/agent-sdk/overview`, `.../quickstart`, `.../authentication`, `.../headless`.
- Agent SDK, frase identica in overview e quickstart: «Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods described in the Quickstart instead.» Il quickstart usa `ANTHROPIC_API_KEY`. La doc **non dice** in modo esplicito se un uso personale dell'SDK col login dell'abbonamento sia permesso: **da verificare** con il supporto o le pagine di supporto (non lette).
- `claude -p` senza `--bare` usa la stessa catena di credenziali della CLI: «Subscription OAuth credentials from `/login`. This is the default for Claude Pro, Max, Ultra, Team, and Enterprise users». Con `--bare` invece no: «bare mode doesn't use your subscription login». Quindi `--bare`, che accorcia l'avvio, **non** si può usare con l'abbonamento.
- **Rischio nuovo, vale anche per il cervello forte di oggi (strade A e C; V-1 bot #320)**: la pagina headless dice che `--bare` «is the recommended mode for scripted and SDK calls, and will become the default for -p in a future release». In modalità bare il login dell'abbonamento non viene mai letto: il giorno in cui cambierà il default, `claude -p` come lo lancia Gas smetterà di usare il login Max (errore di login, o un'altra via se c'è una chiave). Da fare, a parte da questa proposta: controllare a ogni avvio o nel `doctor` la versione della CLI, e verificare se esiste un flag esplicito per restare non-bare (**da verificare**). Lo segnalo a M1 come rischio per R2.
- Resta valida l'ambiguità già scritta in `reports/r2_regole_abbonamento.md`: Consumer Terms §3.7 sull'uso automatico, rischio accettato dall'operatore il 23 ottobre per `claude -p`. Passare all'SDK è un uso diverso da quello deciso allora: **va rideciso**.

## Proposta

1. **Misurare** (sezione sopra) e mandare i numeri a M1.
2. Se «avvio e resto» pesa più di ~2 s: **strada A**, in una fetta piccola su `brains/claude_cli.py`, con revisore, test e prova sul Mac, solo dopo aver risolto il nodo del system prompt (sopra). Regole d'uso come oggi, con il rischio del futuro default `--bare` che vale per tutto il cervello forte.
3. **Strada B solo dopo** che l'operatore ha chiarito le regole d'uso dell'SDK con l'abbonamento, e con un piano per tenere la storia sotto `_get_window`. Oggi non la consiglio.

Decide l'operatore: misurare sì o no, poi A, B o niente.
