"""Dati DIMOSTRATIVI per vedere il CRM pieno: servizi e clienti INVENTATI.

Vanno in un file separato (`.gas_crm_demo.db`), mai nel DB vero. I numeri di telefono sono
volutamente non assegnabili (+39 000 …): nessun messaggio può arrivare a una persona vera.
I nomi dei servizi sono segnaposto: quelli veri li configura l'operatore.
"""
from __future__ import annotations

import random
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

from modules.crm import analisi
from modules.crm.store import CRMStore

SERVIZI_DEMO: Tuple[Tuple[str, str, str, int, int, int, int, str], ...] = (
    # codice, nome, modello, commissione_bp, fissa_cents, capitale_min_cents, rend_bp, descrizione
    ("copy-oro", "Copy Oro", "percentuale_profitto", 2500, 0, 100_000, 300,
     "Copia delle operazioni sull'oro (DEMO)"),
    ("conto-gestito", "Conto Gestito", "percentuale_profitto", 3000, 0, 500_000, 250,
     "Conto gestito su più mercati (DEMO)"),
    ("segnali-vip", "Segnali VIP", "fisso_mensile", 0, 9_900, 0, 0,
     "Abbonamento ai segnali (DEMO)"),
    ("fondo-protetto", "Fondo Protetto", "percentuale_capitale_annua", 200, 0, 1_000_000, 120,
     "Linea prudente (DEMO)"),
    ("academy", "Academy", "fisso_mensile", 0, 4_900, 0, 0, "Formazione mensile (DEMO)"),
)

NOMI = ("Marco Bianchi", "Giulia Romano", "Luca Esposito", "Sara Colombo", "Andrea Ricci",
        "Francesca Marino", "Matteo Greco", "Chiara Bruno", "Davide Gallo", "Elena Conti",
        "Simone De Luca", "Martina Costa", "Alessandro Giordano", "Valentina Mancini",
        "Federico Rizzo", "Alessia Lombardi", "Stefano Moretti", "Ilaria Barbieri",
        "Roberto Fontana", "Silvia Santoro", "Paolo Mariani", "Laura Rinaldi",
        "Nicola Caruso", "Giorgia Ferrara", "Emanuele Galli", "Beatrice Martini")


def _mesi_indietro(oggi: date, n: int) -> List[date]:
    """Il giorno 28 (o oggi, se il mese è quello corrente) degli ultimi n mesi, dal più vecchio."""
    out = []
    for k in range(n - 1, -1, -1):
        m = analisi.mese_precedente(analisi.mese_di(oggi), k)
        g = date(int(m[:4]), int(m[5:7]), 28)
        out.append(min(g, oggi))
    return out


def popola(store: CRMStore, oggi: date | None = None, seme: int = 23) -> Dict[str, int]:
    """Riempie un DB VUOTO con dati dimostrativi coerenti. Ritorna i conteggi."""
    if store.clienti() or store.servizi():
        raise RuntimeError("il DB demo non è vuoto: cancella il file e riprova")
    rnd = random.Random(seme)
    giorno = oggi or date.today()
    sid: Dict[str, int] = {}
    for i, (cod, nome, modello, bp, fisso, cap_min, rend, desc) in enumerate(SERVIZI_DEMO):
        sid[cod] = store.aggiungi_servizio(cod, nome, modello, commissione_bp=bp,
                                           commissione_fissa_cents=fisso,
                                           capitale_minimo_cents=cap_min,
                                           rendimento_stimato_bp=rend, priorita=(i + 1) * 10,
                                           descrizione=desc, autore="demo")
    # profili: (servizi, capitale base in euro, rendimento medio bp, mesi di anzianità)
    profili = [
        (["copy-oro"], 8_000, 520, 10), (["copy-oro", "segnali-vip"], 15_000, 610, 12),
        (["conto-gestito"], 25_000, 380, 9), (["copy-oro"], 30_000, 450, 7),
        (["segnali-vip"], 0, 0, 5), (["copy-oro", "conto-gestito"], 40_000, 420, 12),
        (["fondo-protetto"], 60_000, 110, 8), (["copy-oro"], 5_000, 300, 3),
        (["conto-gestito", "fondo-protetto"], 80_000, 260, 11), (["academy"], 0, 0, 4),
        (["copy-oro"], 22_000, 560, 6), (["copy-oro", "academy"], 12_000, 480, 8),
        (["conto-gestito"], 18_000, 410, 5), (["copy-oro"], 3_000, 200, 1),
        (["copy-oro", "conto-gestito", "segnali-vip"], 55_000, 470, 12),
        (["fondo-protetto"], 35_000, 100, 6), (["copy-oro"], 26_000, 590, 9),
        (["segnali-vip", "academy"], 0, 0, 7), (["conto-gestito"], 45_000, 360, 10),
        (["copy-oro"], 9_500, 430, 4), (["copy-oro", "fondo-protetto"], 70_000, 330, 12),
        (["conto-gestito"], 12_000, 150, 2), (["copy-oro"], 17_000, 640, 8),
        (["academy"], 0, 0, 2), (["copy-oro", "segnali-vip"], 20_000, 500, 6),
        (["conto-gestito"], 32_000, 440, 7),
    ]
    clienti: List[int] = []
    for i, (nome, (servizi, cap, rend, anz)) in enumerate(zip(NOMI, profili)):
        telefono = f"+39000000{1000 + i}"
        presentato = clienti[rnd.randrange(len(clienti))] if clienti and rnd.random() < 0.25 else None
        cid = store.aggiungi_cliente(nome, telefono=telefono,
                                     email=f"cliente{i + 1}@esempio.invalid",
                                     consenso_marketing=(i not in (7, 19)),
                                     presentato_da=presentato, autore="demo",
                                     note="Cliente dimostrativo")
        clienti.append(cid)
        mesi = _mesi_indietro(giorno, anz)
        for j, cod in enumerate(servizi):
            inizio = mesi[min(j * 2, len(mesi) - 1)]
            apertura = date(inizio.year, inizio.month, 1)
            pid = store.apri_posizione(cid, sid[cod], data=apertura.isoformat(), autore="demo")
            serv = SERVIZI_DEMO[[s[0] for s in SERVIZI_DEMO].index(cod)]
            modello, bp, fisso = serv[2], serv[3], serv[4]
            capitale = 0 if modello == "fisso_mensile" else (cap * 100 if j == 0 else cap * 60)
            if capitale > 0:
                store.registra_movimento(pid, "deposito", capitale, data=apertura.isoformat(),
                                         fonte="demo", nota="capitale iniziale")
            for g in mesi[min(j * 2, len(mesi) - 1):]:
                if capitale > 0 and modello != "fisso_mensile":
                    r = rend + rnd.randint(-260, 260)
                    if rnd.random() < 0.12:
                        r = -abs(r) // 2
                    esito = capitale * r // 10_000
                    if esito > 0:
                        store.registra_movimento(pid, "profitto", esito, data=g.isoformat(), fonte="demo")
                    elif esito < 0:
                        store.registra_movimento(pid, "perdita", -esito, data=g.isoformat(), fonte="demo")
                    if g.month == giorno.month and g.year == giorno.year:
                        continue  # la commissione del mese in corso si incassa a fine mese
                    if modello == "percentuale_profitto" and esito > 0:
                        store.registra_movimento(pid, "commissione", esito * bp // 10_000,
                                                 data=g.isoformat(), fonte="demo")
                    elif modello == "percentuale_capitale_annua":
                        store.registra_movimento(pid, "commissione", capitale * bp // 120_000,
                                                 data=g.isoformat(), fonte="demo")
                elif modello == "fisso_mensile":
                    # l'abbonamento si incassa il primo del mese, anche quello in corso
                    store.registra_movimento(pid, "commissione", fisso,
                                             data=date(g.year, g.month, 1).isoformat(),
                                             fonte="demo")
            if capitale > 0 and anz >= 6 and rnd.random() < 0.3:
                extra = mesi[len(mesi) // 2]
                store.registra_movimento(pid, "deposito", capitale // 4, data=extra.isoformat(),
                                         fonte="demo", nota="versamento aggiuntivo")
    # qualche stato particolare, per vedere i casi limite
    store.aggiorna_cliente(clienti[21], autore="demo", stato="in_pausa")
    store.aggiorna_cliente(clienti[13], autore="demo", opt_out=True)
    return {"servizi": len(sid), "clienti": len(clienti)}


def percorso_demo(root: Path) -> Path:
    return Path(root) / ".gas_crm_demo.db"
