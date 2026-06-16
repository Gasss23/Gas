# 📄 REPORT — Memoria FASE 2 FETTA 2b (lettura/iniezione)

**Data:** 2026-06-16 · **Commit motore:** `f3c5f30` · **Suite:** 98/98, 0 FAIL (era 90)
**Review:** #14 — **APPROVATO CON RISERVE** (R1/R2/R3 tracciate in `stato_progetto.md`)

---

## Esito in breve

GAS ora **usa** la sua memoria. Due meccanismi, entrambi fail-safe e senza toccare la
finestra blindata del loop:

1. **Pin always-on** — a ogni turno il kernel inietta NEL MESSAGGIO SYSTEM un blocco
   compatto: i lead ATTIVI e le ultime azioni significative. Così GAS "vede" sempre con chi
   sta parlando e cosa ha già fatto, senza doverlo chiedere.
2. **Tool `ricorda()`** — di sola lettura: GAS può approfondire on-demand il diario o la
   scheda di un lead specifico.

Realizza la proposta §FINALE del report della fetta 2a. La fetta 2a (scrittura del diario)
è stata committata in `7a75368`; questa 2b in `f3c5f30`.

---

## Cosa è stato costruito (motore, `gas.py`)

- **`_memoria_pin()`**: costruisce il blocco (sezione "Lead attivi" filtrando i chiusi
  `STATI_CHIUSI`, sezione "Ultime azioni" escludendo il rumore di lettura `read_file`/
  `run_command`/`ricorda`). Appeso al system message in `run_turn`:
  `self.system_prompt + mem_pin`. **Calcolato UNA volta per turno** (no eco delle azioni in
  corso, no query ripetute nel loop a 10 iterazioni). Vive NEL system message → **FUORI
  dalla finestra**: `_get_window`/`_cap_window_chars` non sono toccati. Cap dedicato
  `MEMORY_PIN_CHAR_CAP=3000` che tronca il TESTO con marker (stesso principio di
  `_cap_tool_output`), **mai** slicing di sequenze di messaggi (§5).
- **Tool `ricorda(query?, contatto?, n=10)`**: aggiunto a `tools_schema` + ramo in
  `execute_tool_call`. SOLA LETTURA, in-process (codice fidato → niente filesystem/rete,
  quindi niente sandbox e niente snapshot perché non muta nulla). Pesca scheda+storia di un
  lead, oppure cerca nel diario, oppure ritorna gli ultimi eventi. Output capato da
  `_cap_tool_output` come ogni tool.
- **Fail-safe §9**: memoria `None`/degradata → `_memoria_pin()` ritorna "" e il turno
  prosegue; `_ricorda()` ritorna un messaggio gentile. Mai crash.

---

## VERIFICHE (eseguite dal vivo, output integrale)

### A. Suite completa — 98 PASS, 0 FAIL (era 90 → +8 T21)

```
[PASS] T21a pin: lead attivi + azioni vere, no chiusi/rumore
[PASS] T21b pin vuoto se memoria vuota o None — vuoto=''
[PASS] T21c ricorda per contatto -> scheda + storia
[PASS] T21d ricorda per query filtra il diario
[PASS] T21e ricorda default -> ultimi eventi
[PASS] T21f iniezione: pin nel system, 1 solo system, finestra parte da user — n_msgs=2 ruoli=['system', 'user']
[PASS] T21g memoria degradata/None -> pin vuoto, turno OK, ricorda non crasha
[PASS] T21h pin capato a MEMORY_PIN_CHAR_CAP (no slicing della storia) — len_pin=2624 cap=3000

=== RIEPILOGO: 98 PASS, 0 FAIL ===
```

### B. Round-trip agentico + prova d'iniezione (§7 — punto critico)

- **T21f** cattura il PAYLOAD REALE passato al provider durante un `run_turn`: il pin è nel
  messaggio `system`, c'è **UN SOLO** messaggio system, e la finestra conversazionale parte
  da `role:user` (`ruoli=['system','user']`). → nessun rischio di tool result orfani /
  Gemini 400: la finestra è strutturalmente identica a prima, il pin è "sopra" di essa.
- I test storici della finestra (T3 cutoff dentro catena tool → parte da user, T4 zero tool
  orfani) restano **verdi**: `_get_window`/`_cap_window_chars` non sono toccati.

### C. Prova-di-scope (commit motore `f3c5f30`)

```
 gas.py                    | 132 ++++++++++++++++++++++++++++++++++++++++++++--
 tests/test_unit_kernel.py | 132 ++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 261 insertions(+), 3 deletions(-)
```

- **NESSUNA riga +/- ridefinisce** `_get_window`, `_cap_window_chars`, `_msg_chars`,
  `_bwrap_prefix`, `_snapshot`, `_vet_command`, la lista `providers`, `WINDOW_CHAR_CAP`.
- `modules/memory/store.py` (schema fetta 1) **NON toccato**.
- L'**unica** modifica alla macchina della finestra è la riga del payload:
  ```
  - payload = [{"role": "system", "content": self.system_prompt}] + self._get_window()
  + payload = [{"role": "system", "content": self.system_prompt + mem_pin}] + self._get_window()
  ```
  (`+ self._get_window()` byte-identico). Le 3 cancellazioni sono le 3 righe modificate
  (import, schema tool read_file, payload). **Scope rispettato.**

### D. Prova dal vivo (round-trip reale: pin iniettato + `ricorda`)

Memoria pre-popolata (lead Mario interessato + 2 eventi), poi `run_turn` in cui il modello
finto chiama `ricorda(contatto='mario')` e poi conclude:

```
=== SYSTEM MESSAGE iniettato (pin always-on) ===
# MEMORIA (sola lettura — usa il tool 'ricorda' per approfondire il diario o un lead)
## Lead attivi
- Mario Rossi [interessato] → prossima: inviare preventivo entro venerdi (ultimo: 2026-06-16)
## Ultime azioni
- [write_file] path='offerta.txt' | [OK] bozza creata
- [messaggio] DM inviato a Mario su Instagram

=== OUTPUT del tool ricorda(contatto='mario') ===
CONTATTO Mario Rossi [interessato] — prossima: inviare preventivo entro venerdi — note: —
Storia:
- [messaggio] DM inviato a Mario su Instagram

=== EVENTI === ['tool_res', 'final']
```

Il pin compare nel system message; `ricorda` recupera scheda + storia del lead. Il turno si
chiude regolarmente.

---

## Riserve (review #14, minori, non bloccanti — in `stato_progetto.md`)
- **R1**: il match del contatto in `_ricorda` è substring case-insensitive su chiave+nome e
  prende il PRIMO → una query corta può colpire il lead sbagliato senza avvisare di match
  multipli. Difesa candidata: segnalare match multipli o richiedere match esatto sulla chiave.
- **R2**: costanti `MEMORY_PIN_*`/`DIARIO_NOISE_TIPI` hardcoded (come `WINDOW_CHAR_CAP`);
  valutare override via env al deploy VPS.
- **R3**: euristica `MEMORY_PIN_EVENTS*5` per filtrare il rumore: se gli ultimi ~30 eventi
  fossero TUTTI rumore, "Ultime azioni" risulterebbe vuota pur con azioni vere più indietro
  (recuperabili via `ricorda`).

---

## Stato finale
- **Fetta 2b (lettura/iniezione): ATTIVA.** Con la 2a (scrittura) la memoria di GAS è ora un
  ciclo completo: scrive da sé ogni azione e la rilegge (pin always-on + tool `ricorda`),
  senza toccare la finestra blindata. Suite **98/98**. Review #14 APPROVATO CON RISERVE.
- **Prossimo, da valutare** (non in questa fetta): scrittura dei CONTATTI dal loop/da tool
  dedicati (oggi la rubrica si popola solo a mano/in-process); chiusura riserve R1/R2/R3;
  poi Vector DB (FASE 2) per i ricordi a lungo termine semantici.
