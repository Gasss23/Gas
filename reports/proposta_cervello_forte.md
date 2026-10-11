# Proposta — cervello forte (Claude via API)

> FETTA 3 del comando dell'operatore del 2026-10-11. **Solo sonda e proposta: nessun codice del motore.**
> Fatti verificati con ricerca il 2026-10-11 sulle pagine ufficiali (link in fondo), non a memoria.

## 1. Fatti verificati

| Tema | Fatto | Fonte |
|---|---|---|
| Crediti nei piani | Max 5x: **100 $/mese**; Max 20x: **200 $/mese** (Team fino a 500 $, Pro/Free/Enterprise esclusi). Si possono richiedere dopo 7 giorni di piano attivo. | [1] |
| Cosa coprono | API Claude (Messages e Batch), Managed Agents, Agent SDK, Playground. **NON** Claude Code né l'uso extra nelle app. | [1] |
| Scadenza | Scadono a fine ciclo di fatturazione, **niente riporto**. | [1] |
| Collegamento alla Console | claude.ai → Impostazioni → Fatturazione → sezione «API credits» → si sceglie UNA organizzazione della Console (serve ruolo Owner/Admin/Billing lì) e si accettano i termini. Il collegamento **non si cambia da soli** (serve il supporto). I crediti compaiono in Console → Settings → Billing → «Promotional credits». Nessuna carta richiesta. | [1] |
| Quando finiscono | Se l'organizzazione non ha altri crediti, **le richieste si fermano** con l'errore «Your credit balance is too low to access the Anthropic API…» fino ai crediti del mese dopo. Nessun addebito sul piano Claude. Se si sono comprati crediti, o c'è la ricarica automatica, si continua a pagare quelli. | [1] |
| Tetti di spesa | Le chiamate pagate coi crediti contano nel tetto mensile dell'organizzazione. Per limitare un progetto si può dargli un **workspace dedicato con il suo limite di spesa**. | [1] |
| Prezzi (USD per milione di token, entrata/uscita) | Opus 5.5: **4 / 20**; Sonnet 5.5: **2 / 10**; Haiku 5.5: **0,10 / 0,50** (prompt ≤100k token); Fable 5.1: 10 / 50. Batch: −50%. | [2] |
| Dati dell'API | I dati trattenuti **non si usano per l'addestramento** senza permesso esplicito. Di default prompt e risposte **non vengono trattenuti**, salvo i «Covered Models» (Fable 5/5.1, Mythos 5/5.1), che richiedono **30 giorni** di conservazione. | [3] |
| Client attuale | L'API Claude ha un livello compatibile con l'SDK OpenAI (`base_url = https://api.anthropic.com/v1/`): tool/function calling supportato. Anthropic lo dichiara **per test e confronto, non come soluzione di produzione a lungo termine**; `strict` ignorato, niente prompt caching, `tool_choice` forzato vietato su Opus/Sonnet 5.5 (Gas usa `"auto"`: ok). | [4] |

## 2. Le decisioni del supervisore reggono?

Tutte reggono, con due note:

1. **Gradino «forte» solo su richiesta esplicita** — regge. Nota: oggi `_cascata_provider` ha solo 'semplice'/'complesso'; serve un terzo valore ('forte') scelto SOLO da campo del catalogo o da opzione di riga di comando, mai da `classifica_compito`.
2. **Chiave nel `.env` con nome proprio** — regge. Proposta: `GAS_CLAUDE_API_KEY`. Viene già tolta all'ambiente di `run_command` (`_sanitized_subprocess_env` scarta ogni variabile con `KEY` nel nome: da provare con un test); va aggiunta al `doctor` (solo «presente/assente», mai il valore).
3. **Tetto di spesa giornaliero dedicato e controllo prima di OGNI chiamata** — regge. Oggi `GAS_DAILY_TOKEN_BUDGET` si controlla solo a inizio turno (riserva F2 di `reports/roadmap.md`, «budget non ricontrollato dentro il turno»; non è il finding F2 già chiuso in stato_progetto). Serve: (a) prezzo Claude in `_PROVIDER_PRICE_PER_MTok`; (b) `GAS_CLAUDE_BUDGET_USD_GIORNO`; (c) controllo dentro il ciclo `for _ in range(10)`, PRIMA di `create`. In più, rete esterna: **workspace dedicato con limite di spesa** nella Console (decisione dell'operatore).
4. **Crediti finiti o errore → cascata gratuita, dichiarata** — regge: l'errore «credit balance too low» è un errore del provider come gli altri (§9). Va solo classificato come QUOTA nel doctor e dichiarato all'utente (Model Awareness, §8).
5. **Modelli in `brains/model_ids.py`, sovrascrivibili da env** — regge: `MODEL_CLAUDE_FORTE = os.environ.get("GAS_MODEL_CLAUDE_FORTE", "claude-sonnet-5-5")`.

**Nota sui dati:** i Fable/Mythos richiedono 30 giorni di conservazione; per un agente che legge codice e lead conviene restare su Opus/Sonnet 5.5 (nessuna conservazione di default).

**Nota sul client:** il livello OpenAI-compatibile è la via più corta (stesso client e stesso formato dei tool di oggi), ma Anthropic non lo garantisce per la produzione. Proposta: partire da lì (fetta 2) e valutare l'SDK nativo `anthropic` solo se serve (prompt caching, errori più precisi).

## 3. Come si aggancia (sonda del codice, 2026-10-11)

- Cascata: `gas.py::_cascata_provider(compito)` restituisce tuple `(nome, env_chiave, base_url, modello)`; `run_turn` crea `OpenAI(base_url=url, api_key=os.environ.get(env))` e chiama `chat.completions.create(model, messages, tools=self.tools_schema, tool_choice="auto")`. Un rung Claude entra come tupla `("claude-forte", "GAS_CLAUDE_API_KEY", "https://api.anthropic.com/v1/", MODEL_CLAUDE_FORTE)` IN TESTA solo per compito='forte', seguita dalla cascata gratuita normale.
- Formato dei tool: `tools_schema` è già in formato OpenAI `{"type":"function","function":{...}}`, supportato senza modifiche dal livello compatibile.
- Costi: `_log_tokens` + `_daily_cost_usd` leggono `_PROVIDER_PRICE_PER_MTok[provider]`: serve il prezzo del rung, e il test T38a (controllo di sottoinsieme, non si rompe) può essere esteso al nuovo provider. Per il tetto dedicato (Fetta 3) `_daily_cost_usd` deve poter filtrare per provider: oggi somma tutto.
- Altri punti da toccare nella Fetta 2: `TOOL_CAPABLE_MODELS` (senza il modello Claude `run_turn` scrive a ogni giro l'avviso «tool-blind»); la lista dei provider del `doctor` è scritta a mano e non deriva da `_cascata_provider`; il ping del doctor verso Claude è una chiamata a pagamento (minima, `max_tokens=1`) a ogni esecuzione: farlo solo se la chiave c'è e dichiararlo.
- Notte: `modules/notte/notte.py` legge il catalogo YAML; il campo `cervello: forte` va validato come gli altri campi (valore ignoto → avviso, compito saltato).

## 4. Fette proposte (ognuna con test, revisore, verifica esterna)

1. **Fetta 1 — tetto per chiamata (chiude F2), senza Claude.** Controllo di `GAS_DAILY_TOKEN_BUDGET` prima di ogni `create` dentro il ciclo. Test: turno che sfora a metà → si ferma, dichiarato.
2. **Fetta 2 — rung Claude spento di default.** `model_ids.py`, prezzo, tupla in cascata solo per 'forte', chiave tolta da `run_command`, doctor (ping `max_tokens=1`, esito OK/QUOTA/KO). Test con client finto: 'forte' usa Claude per primo; 'semplice'/'complesso' MAI; crediti finiti → ricaduta dichiarata; chiave mai nei log né nell'ambiente di `run_command`.
3. **Fetta 3 — tetto dedicato.** `GAS_CLAUDE_BUDGET_USD_GIORNO`, controllato prima di ogni chiamata Claude; superato → cascata gratuita, dichiarato.
4. **Fetta 4 — scelta esplicita.** Campo `cervello: forte` nel catalogo notturno + opzione da riga di comando (es. `gas.py --forte`). Test: senza campo/opzione Claude non parte mai.

## 5. Rischi

- **Spesa:** il ciclo agentico fa fino a 10 chiamate per turno e la storia cresce a ogni iterazione. Stima prudente su Opus 5.5 (4 $/M in entrata, 20 $/M in uscita): da 20k a 40k token in entrata e ~1k in uscita per chiamata → 0,10–0,18 $ a chiamata, **fino a ~1,5–2 $ a turno pieno**; Sonnet 5.5 circa la metà. Tetto giornaliero + limite del workspace sono necessari.
- **Livello compatibile non da produzione:** possibili differenze silenziose (campi ignorati). Mitigazione: test reali con piccola spesa prima di attivarlo di notte.
- **Dati:** il codice e la rubrica lead escono verso Anthropic (come oggi verso Gemini/Groq). Niente Fable/Mythos (30 giorni di conservazione).
- **Collegamento crediti irreversibile in autonomia:** l'organizzazione Console scelta resta quella (si cambia solo col supporto).
- **Confusione di costi:** i crediti NON coprono Claude Code (lo sviluppo continua a costare come oggi).

## 6. Cosa deve fare l'operatore

1. Su claude.ai → Impostazioni → Fatturazione → «API credits»: collegare UNA organizzazione della Console (meglio una dedicata a Gas).
2. Nella Console: creare un **workspace «gas»** con limite di spesa mensile (es. 50 $), poi una chiave API in quel workspace.
3. Mettere la chiave SOLO nel `.env` di Gas come `GAS_CLAUDE_API_KEY=` (mai in chat, mai nel repo).
4. NON attivare la ricarica automatica (così, finiti i crediti, le richieste si fermano e Gas ricade sulla cascata gratuita).
5. Decidere: modello di default del gradino forte (proposta: Sonnet 5.5, 2/10 $; Opus 5.5 su richiesta) e tetto giornaliero (proposta: 2 $/giorno).
6. Dare il via alla Fetta 1.

## Fonti

1. [API credits for Max and Team plans — Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)
2. [Pricing — Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/pricing)
3. [API and data retention — Claude Platform Docs](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention)
4. [OpenAI SDK compatibility — Claude Platform Docs](https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/openai-sdk)
