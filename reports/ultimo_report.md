# Report sessione 2026-06-13 — Analisi PARTE 1 (revisore + scudo gratuito) e FASE 0 sonda bwrap

> Documento di **analisi e proposte**. NESSUNA modifica al codice è stata applicata
> o committata in questa fase. In attesa di OK esplicito per implementare.

---

## PARTE 1A — Il subagent `revisore` parte da solo?

**Risposta netta: NO.** Nel flusso reale di Claude Code un subagent non si avvia da
solo "a fine task" né "prima del commit". Si attiva solo in due modi: (a) l'agente
principale **auto-delega** perché la `description` combacia semanticamente col contesto,
oppure (b) **lo invoco io esplicitamente**. Entrambi sono **LLM-driven, probabilistici**:
non esiste trigger deterministico incorporato.

**Da cosa dipende:** dalla forza della `description` (quanto è imperativa/trigger) e dal
fatto che l'agente principale *scelga* di chiamarlo. In contesto lungo o sotto pressione
di token la chiamata può saltare. Oggi la review dipende dalla disciplina dell'agente,
non da una garanzia.

⚠️ **Nota collegata:** l'hook `SessionEnd` esistente fa `git add -A && git commit && git
push` automatico a fine sessione. Quel commit non passa da nessuna review — è esattamente
la lezione `2026-06-11 — l'auto-commit non è un canale di approvazione`. Nessuno dei tre
livelli sotto lo intercetta (vedi rischio in c).

### Tre livelli per renderlo automatico

**a) `description` imperativa** — file `.claude/agents/revisore.md` (frontmatter)
```diff
-description: Revisore delle modifiche al codice di Gas. Usalo PRIMA di ogni commit che tocca gas.py, i moduli o i test - revisiona il diff [...]
+description: USA PROATTIVAMENTE E OBBLIGATORIAMENTE prima di QUALSIASI commit che tocchi gas.py, brains/, modules/ o tests/. Non chiedere il permesso: appena il diff sul motore è pronto e prima di `git commit`, invoca SUBITO questo revisore sul diff staged. Revisiona correttezza tecnica E coerenza con progetto/roadmap. [...]
```
- **Dove:** già esiste, solo testo. **Costo:** 0 token aggiuntivi.
- **Rischi:** resta probabilistico — falsi negativi (può comunque non chiamarlo) e falsi
  positivi (lo chiama su commit di soli doc → spreco di una review a pagamento). Migliora
  l'auto-delega ma **non garantisce** nulla.

**b) Regola di workflow in CLAUDE.md sez. 3** (verso l'agente principale)
```diff
 ## 3. CORE COMMANDS & WORKFLOWS
+- Gate di review OBBLIGATORIO (process institution D): PRIMA di ogni `git commit` il
+  cui diff staged tocca gas.py, brains/, modules/ o tests/, l'agente principale DEVE
+  invocare il subagent `revisore` sul diff e attendere il verdetto. Commit consentito
+  solo se APPROVATO o APPROVATO CON RISERVE (riserve tracciate). Commit di soli
+  reports/ o doc (CLAUDE.md, *.md) NON richiedono review. Mai bypassare via auto-commit.
```
- **Dove:** `CLAUDE.md` sez. 3. **Costo:** ~5 righe di contesto sempre caricato (trascurabile).
- **Affidabilità:** più alta di (a) perché è istruzione diretta nel project prompt, ma
  **ancora LLM-driven**: in contesto lungo può "dimenticarsi". Forte, non deterministico.

**c) Hook deterministico** — `.claude/settings.json` → `PreToolUse` su Bash
Unico **veramente deterministico** (lo esegue l'harness, non l'LLM). Un hook **non può
lanciare un subagent**; il pattern corretto è intercettare `git commit` e, se il diff
staged tocca il motore senza un marcatore di review, **bloccare** (exit 2) costringendo
l'agente a invocare il revisore.
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "cd /workspaces/Gas && CMD=$(cat); echo \"$CMD\" | grep -q 'git commit' || exit 0; git diff --cached --name-only | grep -Eq '^(gas\\.py|brains/|modules/|tests/)' || exit 0; test -f .claude/.review_ok && exit 0; echo 'BLOCCATO: il diff tocca il motore. Invoca il subagent revisore e crea .claude/.review_ok dopo APPROVATO prima di committare.' >&2; exit 2"
          }
        ]
      }
    ]
  }
}
```
- **Dove:** `.claude/settings.json`. **Costo token:** l'hook in sé 0 token LLM; paghi solo
  la review che forza.
- **Rischi:**
  - **Loop di Stop hook:** con uno `Stop` hook a `decision: block` l'agente viene riavviato
    e può riprovare a fermarsi → **loop infinito**. Va protetto controllando
    `stop_hook_active`. Per questo si propone `PreToolUse`, non `Stop`.
  - **Falsi positivi sul matcher:** `git commit` arriva in forme diverse (heredoc, `&&`,
    `git -C`); il grep può non matchare → review saltata. Matcher fragile per natura.
  - **Buco dell'auto-commit:** il commit dell'hook `SessionEnd` gira come comando shell
    diretto, non come tool call Bash dell'agente → il `PreToolUse` non lo intercetta.
    Resta un canale non revisionato da chiudere a parte.
  - Stato extra da mantenere: marcatore `.claude/.review_ok` (crearlo dopo APPROVATO,
    invalidarlo a ogni nuovo diff).

**Raccomandazione:** **(b) + (c)** insieme. (b) istruzione primaria, (c) rete di sicurezza
deterministica. (a) da fare comunque (costo zero). Da soli: (a) debole, (c) deterministico
ma cieco sulla semantica.

---

## PARTE 1B — Scudo gratuito del paracadute (budget ZERO)

**Audit.** La pipeline reale è **inline** in `gas.py`: `run_turn` (righe 389–398) e
`doctor` (480–484), via client `OpenAI(base_url=...)` in loop. ⚠️ I moduli
`brains/*_brain.py` (incluso `openrouter_brain.py`) sono **codice morto/legacy**: non sono
cablati in `run_turn`, e violano il Wall of Shame (`messages[-8:]`,
`messages[:2]+messages[-6:]` in groq_brain/claude_brain) e non supportano il loop a tool.
**Non vanno cablati** — si riusa solo la lista di model-id `:free` di `openrouter_brain.py`
come riferimento. La strada pulita è aggiungere **rung alla lista inline**, già
OpenAI-compatibile e già fail-safe (`if not os.environ.get(env): continue`).

### Modifica proposta (NON applicata) — `gas.py`, dentro `run_turn`
```diff
         GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
         GROQ_URL   = "https://api.groq.com/openai/v1"
+        OPENROUTER_URL = "https://openrouter.ai/api/v1"
+        OLLAMA_URL = os.environ.get("GAS_OLLAMA_URL")  # es. http://localhost:11434/v1; assente nel Codespace
 
         if compito == "semplice":
             providers = [
                 ("gemini-flash-lite", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash-lite"),
                 ("gemini-flash",      "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash"),
                 ("groq",              "GROQ_API_KEY",   GROQ_URL,   "llama-3.3-70b-versatile"),
+                # Rung gratuiti, ultimi: skip pulito se manca chiave/endpoint (sez. 9, mai crash)
+                ("openrouter", "OPENROUTER_API_KEY", OPENROUTER_URL, "qwen/qwen-2.5-72b-instruct:free"),
+                ("ollama",     "GAS_OLLAMA_URL",     OLLAMA_URL,     "qwen2.5:7b"),
             ]
         else:
             providers = [
                 ("gemini-flash", "GEMINI_API_KEY", GEMINI_URL, "gemini-2.5-flash"),
                 ("groq",         "GROQ_API_KEY",   GROQ_URL,   "llama-3.3-70b-versatile"),
+                ("openrouter",   "OPENROUTER_API_KEY", OPENROUTER_URL, "qwen/qwen-2.5-72b-instruct:free"),
+                ("ollama",       "GAS_OLLAMA_URL",     OLLAMA_URL,     "qwen2.5:7b"),
             ]
```
Il gate del loop usa già `env` come nome-variabile da controllare: per Ollama si usa
**`GAS_OLLAMA_URL`** sia come "chiave" (presenza) sia come base_url → se non settata,
**skip pulito**; se l'endpoint è giù, l'`except Exception → continue` esistente lo salta
senza crash. **Coerente con sez. 9.** Stessa coppia di rung va aggiunta a `doctor`
(lista 480–484) per il ping.

⚠️ **Due cautele oneste:**
1. **Tool-calling sui free:** la pipeline manda `tools=self.tools_schema,
   tool_choice="auto"`. Molti modelli OpenRouter `:free` **non supportano i tool** → su
   quel rung il loop agentico degraderebbe a sola risposta testuale (niente
   `read_file`/`write_file`). Vanno scelti free **tool-capable** e tenuti come **ultimo
   gradino** (rete di salvataggio testuale), non come brain operativo.
2. **Header OpenRouter:** opzionale ma consigliato passare
   `default_headers={"HTTP-Referer":..., "X-Title":"Gas"}`; non obbligatorio.

### Cosa devi configurare tu
- **OpenRouter:** crea account gratuito → genera `OPENROUTER_API_KEY` → mettila nei
  secrets/env del Codespace e del VPS. Una sola chiave; il failover tra free si gestisce
  con la lista o con `extra_body={"models":[...]}`.
- **Ollama:** **non gira nel Codespace**. Sul **PC/VPS** di deploy: installa Ollama
  (`curl -fsSL https://ollama.com/install.sh | sh`), `ollama pull qwen2.5:7b`
  (tool-capable), poi `export GAS_OLLAMA_URL=http://localhost:11434/v1`. È il "pavimento"
  offline.
- Nessuna nuova dipendenza Python: il client `OpenAI` esistente parla con entrambi.

### Correzione nota obsoleta
La nota **"Gemini free tier: 20 req/giorno"** **non è in CLAUDE.md** — è in
**`reports/stato_progetto.md:47`**. È **obsoleta**: oggi il free tier Gemini ha RPD molto
più alti (e variabili per modello). Da correggere (segnalato, non modificato ora). Inoltre
`doctor` già elenca `OPENROUTER_API_KEY` come opzionale "non in cascata" (riga 470):
cablarla chiude quella incoerenza.

---

## PARTE 2 — FASE 0: esito sonda ambiente (read-only)

| Check | Esito |
|---|---|
| `bwrap --version` | ❌ **ASSENTE** (`command not found`, exit 127) — binario non installato |
| `/proc/sys/user/max_user_namespaces` | ✅ **31745** (>0 → user namespaces abilitati) |
| `kernel/unprivileged_userns_clone` | ✅ **1** (userns non privilegiati permessi) |
| Privilegi | utente **`codespace` (uid 1000), NON root**, nessun setuid |
| Test bwrap reale | ❌ fallito, **ma solo perché bwrap manca** (non per i namespace) |
| `unshare --user --map-root-user --net /bin/true` | ✅ **OK** — user+net namespace funzionano **senza root** |
| `unshare --net` (senza user-ns) | ❌ negato (serve user-ns, atteso) |
| `apt-cache policy bubblewrap` | vuoto (liste apt non disponibili senza `apt-get update`) |

**Lettura:** la **tecnologia** di sandbox OS **è disponibile qui** — i namespace utente+rete
funzionano anche da non-root. Manca **solo il binario `bwrap`**. Due strade, da decidere
alla FASE 1:
1. **Installare bubblewrap** (`sudo apt-get install -y bubblewrap`, da verificare se
   sudo+rete pacchetti disponibili nel Codespace) — API pulita, standard del progetto.
2. **Usare `unshare`** (già presente, `util-linux 2.39.3`) come motore namespace
   **zero-dipendenze** — più grezzo ma funziona subito senza installazioni.

**Buona notizia:** contrariamente all'ipotesi "Codespace = namespace bloccati", il sandbox
OS è **testabile già qui** (non solo sul VPS), quindi i test che mordono della FASE 3 (rete
bloccata, FS read-only) si possono eseguire davvero in questo ambiente.

---

## STATO E PROSSIMI PASSI

🛑 **Fermo come da istruzioni.** Nessuna modifica applicata o committata (oltre a questo
report). In attesa di **OK esplicito** per procedere. Quando lo dai, indica:
- **1A:** quale combinazione (consiglio **b+c**, con a gratis).
- **1B:** se cablare i due rung gratuiti + correggere la nota in `stato_progetto.md`.
- **FASE 1 bwrap:** motore preferito (**installare bubblewrap** o usare **`unshare`**) e
  default di `GAS_SANDBOX_MODE` (argomentato in FASE 1).
