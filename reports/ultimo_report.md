# Ultimo Report — fix/gasmerge-loopback-ok

**Data:** 2026-08-18
**Branch:** fix/gasmerge-loopback-ok
**Commit motore:** 134579b

---

## §SCOPE & ESITO

**Scope:** Insegnare all'invariante IP di `scripts/gasmerge.sh` che gli indirizzi di loopback (blocco 127.0.0.0/8) sono sempre leciti, senza marker esplicito. Nessun altro comportamento modificato.

**Esito:** COMPLETATO — 20/20 test passano (7 nuovi + 13 preesistenti). Revisore: APPROVATO.

---

## §MODIFICA

### `scripts/gasmerge.sh` — sezione INVARIANTE IP (righe ~96-132)

La logica a singolo stadio (`git grep → grep -v gasmerge-ip-ok → BLOCCO`) è diventata a due stadi:

**Step 1 — filtro loopback:** per ogni riga trovata da `git grep`, si cancellano tutti i `127.x.x.x` via `sed -E`. Se nel residuo resta ancora un IPv4 quad-dotted, la riga originale NON è loopback-only e passa allo step 2. Se il residuo è pulito, la riga è esente.

**Step 2 — filtro gasmerge-ip-ok (invariato):** applicato solo al residuo non-loopback; comportamento identico a prima.

Invariante di sicurezza mantenuta: una riga con `127.0.0.1` E `93.42.17.8` → il loopback viene rimosso dalla copia di analisi, resta `93.42.17.8` → la riga originale supera allo step 2 → BLOCCO (il loopback non maschera l'IP reale).

### `tests/test_unit_gasmerge.py` — classe `TestLoopbackExemption` (7 nuovi test)

| Test | Contenuto | Atteso | Esito |
|------|-----------|--------|-------|
| 1 | `127.0.0.1` only | NON blocca | ✅ PASS |
| 2 | `127.0.0.53` only | NON blocca | ✅ PASS |
| 3 | `0.0.0.0` | BLOCCA | ✅ PASS |
| 4 | `93.42.17.8` | BLOCCA | ✅ PASS |
| 5 (CRITICO) | `127.0.0.1` + `93.42.17.8` stessa riga | BLOCCA | ✅ PASS |
| 6 | `93.42.17.8 # gasmerge-ip-ok` | NON blocca | ✅ PASS |
| 7 | branch senza IP (regressione) | NON blocca | ✅ PASS |

---

## §DIFF REALE

```diff
diff --git a/scripts/gasmerge.sh b/scripts/gasmerge.sh
index 88d4153..5470586 100755
--- a/scripts/gasmerge.sh
+++ b/scripts/gasmerge.sh
@@ -94,23 +94,39 @@ set -e
 case "$IP_RC" in
   1) echo "0 IP trovati — OK" ;;
   0)
-    # IPs trovati: filtra le righe che portano il marker di allowlist esplicito.
+    # Step 1: rimuovi le righe con soli IP di loopback (127.x.x.x).
+    # Logica: per ogni riga, cancella tutti i 127.x.x.x con sed; se nel residuo
+    # resta ancora un IPv4 quad-dotted, la riga originale non è loopback-only e
+    # viene tenuta. Una riga con loopback E un IP non-loopback non è esente.
     set +e
-    RESIDUAL=$(echo "$IP_MATCHES" | grep -v 'gasmerge-ip-ok')
-    FILTER_RC=$?
+    NON_LOOPBACK=$(echo "$IP_MATCHES" | while IFS= read -r line; do
+      stripped=$(echo "$line" | sed -E 's/\b127\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b//g')
+      if echo "$stripped" | grep -qE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b'; then
+        echo "$line"
+      fi
+    done)
     set -e
-    case "$FILTER_RC" in
-      1) echo "Tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK" ;;
-      0)
-        echo "BLOCCO: trovati IP non allowlistati nell'albero del branch:"
-        echo "$RESIDUAL"
-        exit 1
-        ;;
-      *)
-        echo "BLOCCO: errore nel filtro allowlist (rc=$FILTER_RC) — gate IP non verificato"
-        exit 1
-        ;;
-    esac
+    if [ -z "$NON_LOOPBACK" ]; then
+      echo "Tutti gli IP sono loopback (127.x.x.x) — OK"
+    else
+      # Step 2: filtra le righe che portano il marker di allowlist esplicito.
+      set +e
+      RESIDUAL=$(echo "$NON_LOOPBACK" | grep -v 'gasmerge-ip-ok')
+      FILTER_RC=$?
+      set -e
+      case "$FILTER_RC" in
+        1) echo "Tutti gli IP sono allowlistati (gasmerge-ip-ok) — OK" ;;
+        0)
+          echo "BLOCCO: trovati IP non allowlistati nell'albero del branch:"
+          echo "$RESIDUAL"
+          exit 1
+          ;;
+        *)
+          echo "BLOCCO: errore nel filtro allowlist (rc=$FILTER_RC) — gate IP non verificato"
+          exit 1
+          ;;
+      esac
+    fi
     ;;
   *)
     echo "BLOCCO: git grep uscito con codice $IP_RC — verifica IP NON eseguita"
```

---

## §VERDETTO REVISORE (VERBATIM)

> **VERDETTO FINALE: APPROVATO**
>
> **Elementi verificati:**
>
> - `scripts/gasmerge.sh:103` — sed ERE `\b127\.[0-9]{1,3}...\b` rimuove correttamente solo i `127.x.x.x`; `0.0.0.0` e IP pubblici passano intatti. Esito: OK.
> - `scripts/gasmerge.sh:104` — grep-qE sul residuo determina se la riga ha ancora IP non-loopback; traccia esplicita per il caso critico riga mista dimostra che `93.42.17.8` sopravvive alla strip e forza BLOCCO. Esito: OK (critico).
> - `tests/test_unit_gasmerge.py:504` — `test_mixed_loopback_and_public_blocks` asserisce `returncode != 0` e `"BLOCCO" in stdout` in AND; entrambe le asserzioni sono discriminanti e mordono la barriera reale. Esito: OK.
>
> **Rischio esplicitamente escluso:** comportamento di `\b` in sed non-GNU (macOS BSD sed) — non verificabile nell'ambiente target Linux/WSL e non rilevante per CI e deploy VPS.

---

## §DECISIONI UMANE RICHIESTE

Nessuna. La modifica è autocontenuta e ha scope ben definito.

**IPv6 (::1):** lo script è IPv4-only by design. La regex non è stata estesa a IPv6 come da stop gate esplicito. Se serve, proporre separatamente.
