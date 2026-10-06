# ULTIMO REPORT — 2026-10-06 — F-mac-2: docstring raw in normalizza_telefono + guardia T79a

## Decisioni umane richieste

1. Merge della PR #135 — rischio nullo (i byte eseguibili non cambiano: `ast.dump` identico).
2. Ordine di merge della notte: ogni PR riscrive i report canonici; dopo un merge le altre vanno riallineate a main.

## Esito per fette

- **F-mac-2**: FATTA — la docstring di `normalizza_telefono` (`modules/memory/store.py` righe 440-453, non `:204` come diceva il finding) aveva `\+`/`\d` in una stringa non raw: SyntaxWarning da 3.12 (Mac: 3.14). Ora `r"""`, testo identico.
- **Guardia T79a**: FATTA — compila gas.py, brains/, modules/ con SyntaxWarning e DeprecationWarning come errori (R-169-1: su 3.11 della CI l'escape è DeprecationWarning, senza questo il test era vacuo in CI).
- **Prove**: kernel 652 PASS / 0 FAIL su 3.11 (venv uv) e 3.13; sul codice vecchio T79a FAIL su entrambi.
- **Review**: #169 APPROVATO CON RISERVE (R-169-1 MEDIA, R-169-2 cosmetica: chiuse) → #171 APPROVATO.
- **Round-trip agentico (§7)**: coperto dalla suite kernel esistente (nessun byte eseguibile cambiato).

## Anomalie

- Nessuna. `gh` non autenticato: PR via connettore GitHub.
