# Report task: GAS risponde SEMPRE in italiano

**Data:** 2026-09-21  
**Branch:** feat/lang-rule-italian  
**Commit motore:** 32dd6c2

---

## Problema

Nel test vocale 4b (PR #90) GAS rispondeva in inglese fino al 3° turno.
Il system prompt non forzava l'italiano in modo esplicito e forte.

## Sonda preliminare

| File | Situazione pre-modifica |
|------|------------------------|
| `gas.py:48` | `"- Rispondi sempre in italiano, in modo conciso e diretto.\n"` — regola debole, niente "dal primo messaggio" né "anche se l'utente scrive in un'altra lingua" |
| `gas_identity.md` | Nessuna regola di lingua. Viene iniettata **prima** di `_GAS_SYSTEM_PROMPT_BASE`, quindi è il posto più autorevole. |

## Modifiche applicate (minime e chirurgiche)

### 1. `gas.py:48` — regola base rafforzata
```
- LINGUA: Rispondi SEMPRE in italiano, dal primo messaggio, anche se l'utente scrive in un'altra lingua. Sii conciso e diretto.
```
(sostituisce la riga debole precedente)

### 2. `gas_identity.md` — regola aggiunta in testa
```
LINGUA: Rispondi SEMPRE in italiano, dal primo messaggio, anche se l'utente scrive in un'altra lingua.
```
Posizionata prima di qualsiasi testo identitario perché l'identity viene iniettata per prima nel system prompt quando il file esiste.

### 3. `tests/test_unit_kernel.py` — test T63a/b/c/d
- **T63a**: `_GAS_SYSTEM_PROMPT_BASE` contiene il marker "anche se l'utente scrive in un'altra lingua"
- **T63b**: `_build_system_prompt` senza `gas_identity.md` → contiene la regola
- **T63c**: `_build_system_prompt` con `gas_identity.md` → contiene la regola
- **T63d**: il file `gas_identity.md` reale deployato contiene la regola

Tutti e 4 **PASS**. I 5 FAIL invariati sono bwrap/sandbox (Linux-only, attivi solo in CI).

## Verdetto revisore (review #100) — VERBATIM

**APPROVATO**

> `gas.py:48` — sostituisce regola debole con regola forte — rischio: ~4 token aggiuntivi + potenziale duplicazione con gas_identity.md quando entrambi attivi — esito: **ok** (enfasi intenzionale per compliance LLM; ridondanza difensiva deliberata).
>
> `gas_identity.md:1-2` — aggiunge regola LINGUA IN CIMA al file identity, prima di qualsiasi altro testo — rischio: budget token (~200 token dichiarati in CLAUDE.md §6) + possibile conflitto logico con gas.py:48 — esito: **ok** (budget ampliamente rispettato; posizionamento in testa garantisce priorità; coesistenza con la regola in base è ridondanza consapevole e difensiva, non conflitto).
>
> `tests/test_unit_kernel.py:3685-3723` (blocco T63, 4 test) — T63a verifica presenza marker in `_GAS_SYSTEM_PROMPT_BASE`; T63b/T63c verificano `_build_system_prompt` senza/con gas_identity.md; T63d verifica il file reale deployato. Rischio: T63c quasi tautologico (scrive il marker, lo rilegge); path resolution `parents[1]` = /Users/gas/Gas corretto — esito: **ok** (T63d è il test con valore reale; pattern mkdtemp+git init già consolidato; struttura test corretta).
>
> Antipattern Wall of Shame: ASSENTI. Guardrail (loop cap, _get_window, _cap_window_chars, eccezioni provider): NON TOCCATI. Coerenza roadmap: implementa esattamente l'ordine operatore 2026-09-21.
>
> Rischio esplicitamente escluso: comportamento runtime reale con utenti che scrivono in lingue diverse — non verificabile senza sessione live con provider LLM reale.

## STOP gate rispettato

- Voce TTS non toccata (nessun cambio a lingua/voce ElevenLabs)
- Cascata/provider non toccata
- Memoria, sandbox non toccate
- Nessun refactor fuori scope

## Stato post-task

- `reports/stato_progetto.md` aggiornato (item 5: ✅ COMPLETATO)
- PR feat/lang-rule-italian pronta per merge
