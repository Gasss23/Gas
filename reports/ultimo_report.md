# ULTIMO REPORT — 2026-10-23 — R2 via B, fetta 1: Claude come cervello forte via `claude -p`

## DECISIONI UMANE RICHIESTE

1. Merge della PR della fetta (vedi §0 dell'handoff): verdetto del revisore APPROVATO CON RISERVE, quindi il merge spetta all'operatore (regola CLAUDE.md §10).
2. Per accendere il cervello forte, più avanti: sul Mac `claude` loggato con l'account Max di Gas, `GAS_CLAUDE_CLI=1` nel `.env` di Gas, nessuna `ANTHROPIC_API_KEY`. NON ancora: prima vanno chiuse R-494-1/2 e fatte le fette budget e catalogo.

## Esito

- **Fetta 1 — adattatore `brains/claude_cli.py` + rung «forte» in `gas.py`**: `FATTA`. Claude risponde solo in JSON fisso, senza strumenti propri, MCP o skill (`--tools "" --strict-mcp-config --disable-slash-commands --setting-sources ""`), in una cartella temporanea vuota, con l'ambiente ripulito da `ANTHROPIC_*` e dai segreti; il system prompt passa da un file nella cartella temporanea. Le chiamate agli strumenti le esegue `run_turn` (cancello, tetti, diario). Il rung parte solo con `cervello="forte"` e `GAS_CLAUDE_CLI=1`; non ripiega mai sui gratuiti. Oggi è dormiente: nessun chiamante passa `cervello="forte"`.
- **Review**: #492 BOCCIATO (iniezione di tag nella trascrizione) → #493 APPROVATO CON RISERVE (neutralizzazione che corrompeva il codice) → #494 APPROVATO CON RISERVE (due BASSE, R-494-1/2, tracciate in `stato_progetto.md`).
- **Merge di main (PR #255, chat Mani)**: conflitti solo nei report e nella memoria del revisore; review #495 APPROVATO.
- **Test**: `tests/test_unit_claude_cli.py` 12 passed; kernel 1029 PASS 0 FAIL (T99a-f); pytest completo 2118 passed, 1 skipped (prima delle correzioni R-493: solo l'adattatore è cambiato dopo); nuovo passo CI «Run claude-cli suite».
- **Documenti**: cifra corretta a 4,60 $/giorno in `r2_regole_abbonamento.md`, decisione via B registrata lì e nella roadmap.
- **Fette successive R2**: `DEFERITA — prossime sessioni` (budget dedicato, `cervello: forte` nel catalogo notturno e opzione CLI, riga del doctor, setup del Mac).

## Anomalie

- Nessuna prova dal vero col login Max: qui la CLI gira con un altro account. Il messaggio esatto di limite raggiunto non è stato provocato.
