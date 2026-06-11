# 🧠 Memoria del revisore

> Lezioni e pattern di errore accumulati dalle review, in ordine
> cronologico. Una lezione = 1-3 righe, datata. Aggiornata dal subagent
> revisore al termine di ogni review che produce lezioni nuove.

<!-- Le lezioni si aggiungono sotto questa riga -->
- 2026-06-11 — Ogni costante di cap va verificata contro il worst case dei guardrail ufficiali: il cap n*2=20 di _get_window cedeva proprio a 10 iterazioni × 1 tool call = 21 messaggi, producendo finestra vuota a metà turno. Fare sempre il conto esplicito.
- 2026-06-11 — Un payload vuoto o senza ancora user è peggio di uno lungo: i limiti di dimensione sulla finestra vanno applicati a granularità di messaggio (compattare i content dei tool più vecchi, struttura e tool_call_id intatti), mai escludendo l'user o orfanizzando tool call.
- 2026-06-11 — _get_window oggi non ha alcun cap rigido in byte/token: il limite è solo strutturale (ancora = ultimo user) + cap 8k per tool + 10 iterazioni; tool call parallele lo aggirano. Finché manca un WINDOW_CHAR_CAP, sorvegliare ogni modifica che aumenta i messaggi per iterazione.
- 2026-06-11 — Fix entrati via auto-commit senza review (es. 4c6fc3d) vanno revisionati retroattivamente appena scoperti: l'auto-commit non è un canale di approvazione.
- 2026-06-11 — Un guardrail sul filesystem (es. _safe_path su read/write_file) vale solo quanto run_command: la shell lo bypassa interamente (`cat ~/.bashrc` esfiltra comunque). Ogni claim di sandbox va verificato contro TUTTI i tool, non solo quelli citati nel finding.
- 2026-06-11 — Pattern corretto anti-traversal: `.resolve()` PRIMA di `is_relative_to(root)` con root anch'essa risolta a init — neutralizza `../`, path assoluti e symlink interni che puntano fuori (verificato empiricamente). Confronto component-wise, niente bug da prefisso di stringa.
- 2026-06-11 — `git -C <root>` risale ai repo genitori: se la root di Gas non ha un proprio .git ma sta dentro un repo esterno, lo snapshot "riesce" fotografando il repo SBAGLIATO e l'operazione passa. Ogni guardrail basato su git deve verificare `git rev-parse --show-toplevel == root` (fail-closed). Verificato empiricamente.
- 2026-06-11 — Pattern corretto per scatola nera senza rumore: root logger a WARNING + logger dedicato alzato a INFO + console handler a WARNING. Il check di livello avviene sul logger emittente, i handler filtrano solo per handler-level (verificato: 82 righe snapshot, 0 righe httpx).
- 2026-06-11 — Retention count-based su trigger per-tool-call: anche i comandi read-only consumano slot (ogni `ls` = uno snapshot). Prima di fidarsi del numero (100), fare il conto del worst case di rotazione in una sessione shell intensa.
