# Report — R-crm-1b Fetta 3: dedup telefono
**Data:** 2026-07-27
**Branch:** feature/crm-dup-telefono
**Commit motore:** f6259eb

---

## DECISIONI UMANE RICHIESTE

1. **Merge della PR** `feature/crm-dup-telefono → main` (CI verde su `c8ab4be` — run `30241988037` ✅).
2. **Decidere se esporre** `normalizza_telefono` / `rileva_duplicati_telefono` in `gas doctor`, CLI `check-dups`, o tool `ricorda` — non fatto per stop gate; proposto nel report.

---

## Esito fette

**Fetta UNICA — R-crm-1b fetta 3 (dedup telefono):** `FATTA`

Due funzioni aggiunte in `modules/memory/store.py`:

### 1. `normalizza_telefono(telefono: Optional[str]) -> str`
Funzione pura e fail-safe. Regole in ordine:
- `None` o `""` → `""`
- Normalizzazione Unicode NFKC
- `'+'` mantenuto SOLO se è il primo carattere non-spazio; tutte le cifre estratte, resto scartato
- Se le cifre iniziano con `"00"` (e non c'era `+`) → sostituisce `"00"` con `"+"`
- Gate di plausibilità:
  - Con `+`: deve matchare `^\+\d{8,15}$` → restituisce così; altrimenti `""`
  - Senza `+` (cifre nude): assume IT (+39) SOLO se mobile `^3\d{8,9}$` oppure fisso `^0\d{7,10}$` → `"+39"` + cifre (lo `0` iniziale del fisso non viene rimosso)
  - Qualsiasi altra sequenza (nomi, email, ID numerici) → `""`

### 2. `rileva_duplicati_telefono(self) -> List[Dict[str, Any]]`
Specchio 1:1 di `rileva_duplicati_email`:
- SOLA LETTURA su `contatti WHERE merged_into IS NULL`
- Indicizza `chiave_norm` e `contatto` di ogni riga via `normalizza_telefono`; solo i non-vuoti generano segnale
- Diario: tipo `"sospetto_duplicato_telefono"`, token idempotente `[k=<telefono>|<id_lo>-<id_hi>]`
- Pre-check `SELECT ... LIKE ESCAPE` prima di ogni `append_diario`; FAIL-OPEN §9 se il pre-check degrada
- `[] se not self.available`

Esportata `normalizza_telefono` da `modules/memory/__init__.py` (`__all__` aggiornato).

---

## Test reali eseguiti

Suite completa `tests/test_unit_kernel.py`: **272 PASS, 0 FAIL**.

22 nuovi test T60a–T60m:

| Test | Verifica |
|------|----------|
| T60a | Separatori/spazi/parentesi rimossi (`+39 (333) 123-4567` → `+393331234567`) |
| T60b | `+39 333 123 4567` → forma canonica |
| T60c | `0039 333 123 4567` → `+393331234567` (prefisso 00→+) |
| T60d | Mobile nudo `3331234567` → `+393331234567` |
| T60e | Fisso nudo `06 1234567` → `+39061234567` (0 preservato) |
| T60f | Equivalenza: `333 123 4567` == `+39 3331234567` |
| T60g | Gate: `anna`/`a@b.com`/`12345`/`1234567890123456` → `""` |
| T60h | `None`/`""` → `""` |
| T60i | 2 schede stesso telefono → 1 coppia + 1 riga diario `sospetto_duplicato_telefono` |
| T60j | Idempotenza: 2ª chiamata → diario invariato, coppia ancora ritornata |
| T60k | FAIL-OPEN: DROP TABLE diario → nessun crash, coppia ritornata, `append_diario` chiamato |
| T60l | Store non available (DB corrotto) → `[]` senza crash |
| T60m | Nomi/email non generano segnale telefono |

---

## Revisore

**Review #67 — APPROVATO CON RISERVE**

Elementi esaminati:
- `re.sub(r"[^\d]", "", testo)` rimuove correttamente `+` interni (lezione #49 recepita)
- Lettura doppia `(chiave_norm, contatto)` via `.get()` safe (pattern identico a `rileva_duplicati_email`)
- T60k fail-open: in-process, nessuna simulazione output — conforme §5 CLAUDE.md
- Guardrail §8 (loop cap), §9 (fail-safe), §5 (no tool simulation) verificati ✓

Riserve non bloccanti: R1 e R2 (vedi handoff §7).

---

## Stop gate rispettati

- ✅ NON esposto in `gas doctor`, CLI, `_memoria_pin`, tool `ricorda`
- ✅ Non toccato `rileva_duplicati_email` né `normalizza_chiave` né schema DB
- ✅ NON emerge necessità di colonna `telefono_norm` (normalizzazione at-query-time)
- ✅ Branch distinto da `feature/crm-dup-detect` (non cancellato)
- ✅ Test eseguiti davvero, output reale

---

## Prossimi passi suggeriti (da decidere umanamente)

- Esposizione in `gas doctor` / CLI `check-dups` / tool `ricorda`
- Test R2: scheda A con telefono come chiave primaria + scheda B con telefono in `contatto` in coppia
- Valutare se accorpare con una futura fetta CLI
