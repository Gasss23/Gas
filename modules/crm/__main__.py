"""Riga di comando del CRM: `python -m modules.crm <comando>`.

Comandi:
  serve [--demo] [--porta N]     dashboard in tempo reale (token in GAS_CRM_TOKEN)
  scan [--demo]                  una scansione del motore delle opportunità
  riepilogo [--demo]             numeri principali in testo
  spiega ID [--demo]             perché il motore propone (o no) qualcosa a un cliente
  demo                           crea il DB dimostrativo (.gas_crm_demo.db)
  servizio --codice C --nome N --modello M [--commissione 25] [--fissa 99] [--minimo 1000]
           [--rendimento 3] [--priorita 10]
  cliente --nome N [--telefono T] [--email E] [--consenso]
  posizione --cliente ID --servizio CODICE [--capitale 10.000] [--data AAAA-MM-GG]
  movimento --cliente ID --servizio CODICE --tipo T --importo 1.234,56 [--data …] [--nota …]
  import FILE.csv                movimenti da CSV: telefono;servizio;tipo;importo;data;nota

Il DB vero è `.gas_memory.db` nella cartella di Gas (stesso file della memoria, così il
backup lo copre); `GAS_CRM_DB` lo cambia. `--demo` usa `.gas_crm_demo.db`.
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
import secrets
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from modules.crm import analisi, motore
from modules.crm.store import (CRMStore, ErroreCRM, default_db_path, formatta_euro,
                               normalizza_telefono, parse_importo, parse_percentuale_bp)

ROOT = Path(__file__).resolve().parents[2]


def _env_int(nome: str, default: int, minimo: int, massimo: int) -> int:
    """Intero da variabile d'ambiente; vuoto, non numerico o fuori limiti → default con un
    avviso nel log, mai un crash (§9, R-803-8)."""
    grezzo = os.environ.get(nome, "").strip()
    if not grezzo:
        return default
    try:
        v = int(grezzo)
    except ValueError:
        logging.warning("CRM: %s=%r non è un intero: uso %d", nome, grezzo[:20], default)
        return default
    if not minimo <= v <= massimo:
        logging.warning("CRM: %s=%d fuori dai limiti: uso %d", nome, v, default)
        return default
    return v


def _db(demo: bool) -> Path:
    if demo:
        from modules.crm.demo import percorso_demo
        return percorso_demo(ROOT)
    env = os.environ.get("GAS_CRM_DB", "").strip()
    if env and not Path(env).name.startswith(".gas_memory"):
        # R-803-10: i file .gas_memory* sono illeggibili dagli strumenti di Gas (cancello);
        # un nome diverso perde quella protezione e i dati dei clienti diventano leggibili
        print(f"ATTENZIONE: GAS_CRM_DB={env} non si chiama .gas_memory*: gli strumenti di Gas "
              "potrebbero leggerlo. Usa un nome che inizia con .gas_memory.", file=sys.stderr)
    return Path(env) if env else default_db_path(ROOT)


def _store(demo: bool) -> CRMStore:
    st = CRMStore(_db(demo))
    if not st.available:
        print(f"ERRORE: database non apribile: {st.db_path}")
        sys.exit(1)
    return st


def _servizio_da_codice(st: CRMStore, codice: str) -> int:
    for s in st.servizi():
        if s["codice"] == codice.strip().lower():
            return int(s["id"])
    raise ErroreCRM(f"servizio sconosciuto: {codice}")


def _posizione(st: CRMStore, cliente_id: int, codice: str) -> int:
    sid = _servizio_da_codice(st, codice)
    for p in st.posizioni(cliente_id):
        if int(p["servizio_id"]) == sid:
            return int(p["id"])
    raise ErroreCRM("il cliente non è in quel servizio: aprilo prima con `posizione`")


def cmd_serve(a: argparse.Namespace) -> int:
    from modules.crm import server
    st = _store(a.demo)
    token = server.token_da_env()
    nuovo = False
    if token is None:
        if not a.demo:
            print("STOP: manca GAS_CRM_TOKEN (almeno 16 caratteri) nel file delle chiavi. "
                  "Il CRM con dati veri non parte senza token.")
            return 1
        token, nuovo = secrets.token_urlsafe(24), True
    if a.demo and not st.clienti():
        from modules.crm.demo import popola
        popola(st)
    host = os.environ.get("GAS_CRM_BIND", "127.0.0.1").strip() or "127.0.0.1"
    avvisa = None
    if os.environ.get("GAS_CRM_AVVISI_TELEGRAM", "").strip().lower() in ("1", "true", "on", "si", "sì"):
        from modules.telegram.bot import invia_notifica
        avvisa = invia_notifica
    stato = server.Stato(st, token, demo=a.demo,
                         scan_minuti=_env_int("GAS_CRM_SCAN_MINUTI", 10, 1, 1440),
                         avvisa=avvisa, memoria_db=None if a.demo else st.db_path)

    def pronto(url: str) -> None:
        print(f"CRM Gas {'(DEMO) ' if a.demo else ''}in ascolto su {url}")
        if nuovo:
            # solo in demo (dati inventati): link di accesso con il token nel frammento,
            # che il browser non manda al server
            print(f"Accesso demo: {url}#t={token}")
        print("Ctrl+C per fermare.")
    try:
        server.avvia(stato, host=host, porta=a.porta, pronto=pronto)
    except ValueError as e:
        print(f"STOP: {e}")
        return 1
    except OSError as e:
        print(f"STOP: porta {a.porta} non disponibile ({e})")
        return 1
    return 0


def cmd_scan(a: argparse.Namespace) -> int:
    esito = motore.scansiona(_store(a.demo))
    if esito.errore:
        print(f"ERRORE: {esito.errore}")
        return 1
    print(f"Nuove proposte: {len(esito.create)} (valore stimato "
          f"{formatta_euro(esito.valore_nuovo_cents)}/mese) · senza risposta: "
          f"{len(esito.senza_risposta)} · superate: {len(esito.superate)}")
    return 0


def cmd_riepilogo(a: argparse.Namespace) -> int:
    st = _store(a.demo)
    foto = st.fotografia()
    if foto is None:
        print("ERRORE: database non disponibile")
        return 1
    p = analisi.panoramica(analisi.costruisci(foto))
    k = p["kpi"]
    print(f"CRM — {p['mese_label']}")
    print(f"  clienti attivi {k['clienti_attivi']} (paganti {k['clienti_paganti']}, "
          f"con 2+ servizi {k['clienti_multi_servizio']})")
    print(f"  capitale gestito {formatta_euro(k['capitale_totale_cents'])}")
    print(f"  profitto clienti nel mese {formatta_euro(k['profitto_clienti_mese_cents'], segno=True)}")
    print(f"  commissioni nel mese {formatta_euro(k['commissioni_mese_cents'])} "
          f"(mese prima {formatta_euro(k['commissioni_mese_prec_cents'])})")
    print(f"  opportunità aperte {k['opportunita_aperte']} "
          f"(~{formatta_euro(k['valore_opportunita_cents'])}/mese)")
    for s in p["servizi"]:
        print(f"  · {s['nome']}: {s['clienti_attivi']} clienti, capitale "
              f"{formatta_euro(s['capitale_cents'])}, commissioni del mese "
              f"{formatta_euro(s['commissioni_mese_cents'])}")
    return 0


def cmd_spiega(a: argparse.Namespace) -> int:
    print(motore.spiega(_store(a.demo), a.id))
    return 0


def cmd_demo(_a: argparse.Namespace) -> int:
    from modules.crm.demo import popola
    st = _store(True)
    try:
        n = popola(st)
    except RuntimeError as e:
        print(f"STOP: {e} ({st.db_path})")
        return 1
    esito = motore.scansiona(st)
    print(f"Demo pronta in {st.db_path}: {n['servizi']} servizi, {n['clienti']} clienti, "
          f"{len(esito.create)} opportunità trovate dal motore.")
    return 0


def cmd_servizio(a: argparse.Namespace) -> int:
    st = _store(a.demo)
    sid = st.aggiungi_servizio(
        a.codice, a.nome, a.modello,
        commissione_bp=parse_percentuale_bp(a.commissione or "0"),
        commissione_fissa_cents=parse_importo(a.fissa) if a.fissa else 0,
        capitale_minimo_cents=parse_importo(a.minimo) if a.minimo else 0,
        rendimento_stimato_bp=parse_percentuale_bp(a.rendimento or "0"),
        priorita=a.priorita, descrizione=a.descrizione)
    print(f"Servizio #{sid} creato.")
    return 0


def cmd_cliente(a: argparse.Namespace) -> int:
    cid = _store(a.demo).aggiungi_cliente(a.nome, telefono=a.telefono, email=a.email,
                                          consenso_marketing=a.consenso)
    print(f"Cliente #{cid} creato.")
    return 0


def cmd_posizione(a: argparse.Namespace) -> int:
    st = _store(a.demo)
    pid = st.apri_posizione(a.cliente, _servizio_da_codice(st, a.servizio), data=a.data)
    if a.capitale:
        st.registra_movimento(pid, "deposito", parse_importo(a.capitale), data=a.data,
                              nota="capitale iniziale")
    print(f"Posizione #{pid} aperta.")
    return 0


def cmd_apertura(a: argparse.Namespace) -> int:
    st = _store(a.demo)
    st.anticipa_apertura(_posizione(st, a.cliente, a.servizio), a.data)
    print("Data di apertura aggiornata.")
    return 0


def cmd_movimento(a: argparse.Namespace) -> int:
    st = _store(a.demo)
    mid = st.registra_movimento(_posizione(st, a.cliente, a.servizio), a.tipo,
                                parse_importo(a.importo), data=a.data, nota=a.nota)
    print(f"Movimento #{mid} registrato.")
    return 0


def cmd_import(a: argparse.Namespace) -> int:
    """CSV con intestazione: telefono;servizio;tipo;importo;data;nota (separatore ; o ,).
    TUTTO O NIENTE (R-803-3): ogni riga si controlla con gli stessi controlli dello store
    (tipo, importo, data non futura, nota); se anche una sola è sbagliata non si scrive
    nulla, altrimenti si scrive tutto in una sola transazione."""
    st = _store(a.demo)
    try:
        testo = Path(a.file).read_text(encoding="utf-8-sig")
        righe_testo = testo.splitlines()
        if not righe_testo:
            print("Import FERMATO: file vuoto.")
            return 1
        dialetto = csv.Sniffer().sniff(righe_testo[0], delimiters=";,")
        righe = list(csv.DictReader(righe_testo, dialect=dialetto))
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        print(f"Import FERMATO: file non leggibile ({type(e).__name__}).")
        return 1
    clienti_tel = {c["telefono"]: int(c["id"]) for c in st.clienti() if c["telefono"]}
    pronti: List[Tuple[int, str, int, Optional[str], Optional[str]]] = []
    errori: List[str] = []
    for n, r in enumerate(righe, start=2):
        try:
            tel = normalizza_telefono(r.get("telefono"))
            if tel not in clienti_tel:
                raise ErroreCRM(f"nessun cliente col telefono {tel}")
            pid = _posizione(st, clienti_tel[tel], str(r.get("servizio") or ""))
            riga = (pid, str(r.get("tipo") or "").strip(), parse_importo(r.get("importo")),
                    (r.get("data") or "").strip() or None, (r.get("nota") or "").strip() or None)
            st.valida_movimento(*riga[:4], fonte="import", nota=riga[4])
            pronti.append(riga)
        except ErroreCRM as e:
            errori.append(f"riga {n}: {e}")
    if errori:
        print("Import FERMATO, nessuna riga scritta:")
        for riga_errore in errori[:50]:
            print("  " + riga_errore)
        return 1
    st.registra_movimenti(pronti, fonte="import")
    print(f"Importati {len(pronti)} movimenti.")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m modules.crm", description="CRM clienti di Gas")
    sub = p.add_subparsers(dest="comando", required=True)

    def nuovo(nome: str, fn, aiuto: str) -> argparse.ArgumentParser:
        sp = sub.add_parser(nome, help=aiuto)
        sp.add_argument("--demo", action="store_true", help="usa il DB dimostrativo")
        sp.set_defaults(fn=fn)
        return sp

    sp = nuovo("serve", cmd_serve, "dashboard in tempo reale")
    sp.add_argument("--porta", type=int, default=_env_int("GAS_CRM_PORT", 8770, 1024, 65535))
    nuovo("scan", cmd_scan, "una scansione del motore")
    nuovo("riepilogo", cmd_riepilogo, "numeri principali")
    sp = nuovo("spiega", cmd_spiega, "spiega le scelte del motore su un cliente")
    sp.add_argument("id", type=int)
    sub.add_parser("demo", help="crea il DB dimostrativo").set_defaults(fn=cmd_demo)
    sp = nuovo("servizio", cmd_servizio, "aggiungi un servizio")
    sp.add_argument("--codice", required=True)
    sp.add_argument("--nome", required=True)
    sp.add_argument("--modello", required=True,
                    choices=("percentuale_profitto", "percentuale_capitale_annua", "fisso_mensile"))
    sp.add_argument("--commissione", help="percentuale, es. 25 o 2,5")
    sp.add_argument("--fissa", help="euro al mese, es. 99")
    sp.add_argument("--minimo", help="capitale minimo in euro")
    sp.add_argument("--rendimento", help="stima INTERNA del rendimento mensile in %%")
    sp.add_argument("--priorita", type=int, default=100)
    sp.add_argument("--descrizione")
    sp = nuovo("cliente", cmd_cliente, "aggiungi un cliente")
    sp.add_argument("--nome", required=True)
    sp.add_argument("--telefono")
    sp.add_argument("--email")
    sp.add_argument("--consenso", action="store_true", help="ha dato il consenso ai messaggi")
    sp = nuovo("posizione", cmd_posizione, "metti un cliente in un servizio")
    sp.add_argument("--cliente", type=int, required=True)
    sp.add_argument("--servizio", required=True, help="codice del servizio")
    sp.add_argument("--capitale")
    sp.add_argument("--data")
    sp = nuovo("movimento", cmd_movimento, "registra un movimento")
    sp.add_argument("--cliente", type=int, required=True)
    sp.add_argument("--servizio", required=True)
    sp.add_argument("--tipo", required=True,
                    choices=("deposito", "prelievo", "profitto", "perdita", "commissione"))
    sp.add_argument("--importo", required=True)
    sp.add_argument("--data")
    sp.add_argument("--nota")
    sp = nuovo("apertura", cmd_apertura, "anticipa la data di apertura di un servizio (per lo storico)")
    sp.add_argument("--cliente", type=int, required=True)
    sp.add_argument("--servizio", required=True)
    sp.add_argument("--data", required=True)
    sp = nuovo("import", cmd_import, "importa movimenti da CSV")
    sp.add_argument("file")
    return p


def _carica_chiavi() -> None:
    """Legge il `.env` di Gas con le STESSE regole del kernel (`gas._carica_dotenv`: non
    sovrascrive l'ambiente, mai valori nel log, `GAS_NO_DOTENV=1` lo spegne). Se il kernel
    non si importa (dipendenze mancanti) si prosegue con l'ambiente così com'è."""
    try:
        from gas import _carica_dotenv
        _carica_dotenv(ROOT / ".env")
    except Exception as e:  # §9: il CRM parte comunque, con le variabili già esportate
        logging.warning("CRM: .env non letto (%s): uso solo le variabili esportate", type(e).__name__)


def main(argv: Optional[List[str]] = None) -> int:
    logging.basicConfig(filename=str(ROOT / "gas_debug.log"), level=logging.WARNING,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    a = parser().parse_args(argv)
    _carica_chiavi()
    if a.comando == "demo":
        a.demo = True
    try:
        return int(a.fn(a))
    except ErroreCRM as e:
        print(f"ERRORE: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
