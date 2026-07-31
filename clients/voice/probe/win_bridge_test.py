"""
win_bridge_test.py — Windows only
Testa il forwarding WSL2 → Windows: fa POST a http://WSL_IP:PORT/ping
e verifica che il server GAS in WSL risponda.

Come trovare WSL_IP:
    In WSL:  hostname -I   (prende il primo IP, es. 172.x.x.x)
    In CMD:  wsl hostname -I

Dipendenze (pip install):
    requests

Uso:
    python win_bridge_test.py                         # default 127.0.0.1:8765
    python win_bridge_test.py --host 172.28.16.1 --port 8765
    python win_bridge_test.py --repeat 5              # invia 5 ping di fila
"""

import argparse
import sys
import time
import datetime
import json

try:
    import requests
except ImportError:
    print("[ERRORE] requests non installato. pip install requests")
    sys.exit(1)


def do_ping(url: str, timeout: float) -> dict:
    """Invia POST /ping e restituisce un dict con status, latenza, body."""
    t0 = time.perf_counter()
    try:
        resp = requests.post(url, json={"source": "win_bridge_test"}, timeout=timeout)
        latency_ms = (time.perf_counter() - t0) * 1000
        return {
            "ok": resp.status_code == 200,
            "status_code": resp.status_code,
            "latency_ms": round(latency_ms, 1),
            "body": resp.text[:200],
        }
    except requests.exceptions.ConnectionError as e:
        return {"ok": False, "error": f"ConnectionError: {e}"}
    except requests.exceptions.Timeout:
        return {"ok": False, "error": "Timeout"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Test bridge WSL2 → Windows")
    parser.add_argument("--host", default="127.0.0.1", help="IP del server WSL (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Porta (default 8765)")
    parser.add_argument("--repeat", type=int, default=1, help="Numero di ping")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout secondi per richiesta")
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}/ping"
    print(f"[INFO] Target: POST {url}")
    print(f"[INFO] Ripetizioni: {args.repeat}  Timeout: {args.timeout}s\n")

    ok_count = 0
    for i in range(1, args.repeat + 1):
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        result = do_ping(url, args.timeout)
        if result["ok"]:
            ok_count += 1
            print(f"[{ts}] #{i} OK  HTTP {result['status_code']}  {result['latency_ms']}ms  body={result['body']!r}")
        else:
            err = result.get("error", f"HTTP {result.get('status_code')}")
            print(f"[{ts}] #{i} FAIL  {err}")
        if i < args.repeat:
            time.sleep(0.5)

    print(f"\n=== RISULTATO: {ok_count}/{args.repeat} ping OK ===")
    if ok_count == args.repeat:
        print("[OK] Bridge WSL2→Windows operativo.")
    else:
        print("[FAIL] Bridge non raggiungibile.")
        print("Verificare:")
        print("  1. Il server WSL è avviato?  (python probe_bridge_server.py)")
        print("  2. Il firewall Windows blocca la porta?")
        print("     netsh advfirewall firewall add rule name='GAS-probe' dir=in action=allow protocol=TCP localport=8765")
        print(f"  3. L'IP WSL è corretto?  In WSL: hostname -I  (usare il primo IP, non 127.0.0.1)")
        sys.exit(1)


if __name__ == "__main__":
    main()
