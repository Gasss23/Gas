"""Conti del CRM — funzioni PURE sulla fotografia del DB (nessuna scrittura).

Tutto in centesimi e punti base interi; gli arrotondamenti sono «a metà verso l'alto»
fatti con interi (`_div`), mai float. Sono le stesse funzioni che usano la dashboard e il
motore delle opportunità: un numero mostrato e un numero usato per decidere coincidono.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional, Set, Tuple

MESI_IT = ("gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
           "agosto", "settembre", "ottobre", "novembre", "dicembre")


def _div(num: int, den: int) -> int:
    """Divisione intera arrotondata a metà verso l'alto (anche per i negativi, in modulo)."""
    if den <= 0:
        raise ValueError("denominatore non positivo")
    if num >= 0:
        return (num + den // 2) // den
    return -((-num + den // 2) // den)


div_tonda = _div  # nome pubblico per gli altri moduli del CRM


def formatta_bp(bp: int) -> str:
    """Punti base → percentuale italiana: 235 → «2,35%», −50 → «−0,50%»."""
    a = abs(int(bp))
    return ("−" if bp < 0 else "") + f"{a // 100},{a % 100:02d}%"


def mese_di(giorno: date) -> str:
    return f"{giorno.year:04d}-{giorno.month:02d}"


def mese_precedente(mese: str, n: int = 1) -> str:
    anno, m = int(mese[:4]), int(mese[5:7])
    tot = anno * 12 + (m - 1) - n
    return f"{tot // 12:04d}-{tot % 12 + 1:02d}"


def etichetta_mese(mese: str) -> str:
    return f"{MESI_IT[int(mese[5:7]) - 1]} {mese[:4]}"


def ultimi_mesi(mese: str, n: int) -> List[str]:
    """Gli n mesi che finiscono con `mese` (compreso), dal più vecchio."""
    return [mese_precedente(mese, k) for k in range(n - 1, -1, -1)]


@dataclass
class Posizione:
    id: int
    cliente_id: int
    servizio_id: int
    stato: str
    aperta_il: str
    capitale_cents: int = 0
    profitto_per_mese: Dict[str, int] = field(default_factory=dict)
    commissioni_per_mese: Dict[str, int] = field(default_factory=dict)
    pagamenti: int = 0

    @property
    def profitto_totale_cents(self) -> int:
        return sum(self.profitto_per_mese.values())

    @property
    def commissioni_totali_cents(self) -> int:
        return sum(self.commissioni_per_mese.values())


@dataclass
class Dati:
    servizi: Dict[int, Dict[str, Any]]
    clienti: Dict[int, Dict[str, Any]]
    posizioni: Dict[int, Posizione]
    proposte: List[Dict[str, Any]]
    per_cliente: Dict[int, List[Posizione]]
    oggi: date

    @property
    def mese(self) -> str:
        return mese_di(self.oggi)


def costruisci(fotografia: Dict[str, List[Dict[str, Any]]], oggi: Optional[date] = None) -> Dati:
    """Indici e saldi dalla fotografia di `CRMStore.fotografia()`. I movimenti stornati e
    gli storni non contano; contano solo i movimenti fino a `oggi` compreso."""
    giorno = oggi or date.today()
    limite = giorno.isoformat()
    servizi = {int(s["id"]): s for s in fotografia["servizi"]}
    clienti = {int(c["id"]): c for c in fotografia["clienti"]}
    posizioni: Dict[int, Posizione] = {}
    per_cliente: Dict[int, List[Posizione]] = defaultdict(list)
    for p in fotografia["posizioni"]:
        pos = Posizione(id=int(p["id"]), cliente_id=int(p["cliente_id"]),
                        servizio_id=int(p["servizio_id"]), stato=str(p["stato"]),
                        aperta_il=str(p["aperta_il"]))
        posizioni[pos.id] = pos
        per_cliente[pos.cliente_id].append(pos)
    for m in fotografia["movimenti"]:
        if m.get("storno_di") is not None or m.get("stornato"):
            continue
        if str(m["data"]) > limite:
            continue
        trovata = posizioni.get(int(m["posizione_id"]))
        if trovata is None:
            continue
        pos = trovata
        imp = int(m["importo_cents"])
        mese = str(m["data"])[:7]
        tipo = m["tipo"]
        if tipo == "deposito":
            pos.capitale_cents += imp
        elif tipo == "prelievo":
            pos.capitale_cents -= imp
        elif tipo == "profitto":
            pos.profitto_per_mese[mese] = pos.profitto_per_mese.get(mese, 0) + imp
        elif tipo == "perdita":
            pos.profitto_per_mese[mese] = pos.profitto_per_mese.get(mese, 0) - imp
        elif tipo == "commissione":
            pos.commissioni_per_mese[mese] = pos.commissioni_per_mese.get(mese, 0) + imp
            pos.pagamenti += 1
    return Dati(servizi=servizi, clienti=clienti, posizioni=posizioni,
                proposte=list(fotografia["proposte"]), per_cliente=dict(per_cliente),
                oggi=giorno)


# ---------------------------------------------------------------- metriche
def roi_posizione_bp(pos: Posizione, mese_corrente: str, mesi: int = 3) -> Optional[int]:
    """Rendimento mensile medio della posizione sugli ultimi `mesi` mesi CHIUSI, in bp,
    sul capitale di oggi. None se il capitale non è positivo o non c'è nessun risultato
    registrato in quei mesi (nessun dato ≠ zero)."""
    finestra = [mese_precedente(mese_corrente, k) for k in range(1, mesi + 1)]
    if pos.capitale_cents <= 0 or not any(m in pos.profitto_per_mese for m in finestra):
        return None
    netto = sum(pos.profitto_per_mese.get(m, 0) for m in finestra)
    return _div(netto * 10_000, pos.capitale_cents * mesi)


def roi_servizio_bp(d: Dati, servizio_id: int, mesi: int = 3) -> Optional[int]:
    """Rendimento mensile medio OSSERVATO del servizio (tutti i clienti, pesato sul
    capitale). None senza dati: allora vale la stima interna del servizio."""
    finestra = [mese_precedente(d.mese, k) for k in range(1, mesi + 1)]
    capitale = 0
    netto = 0
    con_dati = False
    for pos in d.posizioni.values():
        if pos.servizio_id != servizio_id or pos.capitale_cents <= 0:
            continue
        capitale += pos.capitale_cents
        netto += sum(pos.profitto_per_mese.get(m, 0) for m in finestra)
        con_dati = con_dati or any(m in pos.profitto_per_mese for m in finestra)
    if capitale <= 0 or not con_dati:
        return None
    return _div(netto * 10_000, capitale * mesi)


def roi_atteso_bp(d: Dati, servizio_id: int) -> Tuple[int, str]:
    """(rendimento mensile da usare per le stime, fonte): osservato se c'è, altrimenti la
    stima interna del servizio."""
    oss = roi_servizio_bp(d, servizio_id)
    if oss is not None:
        return oss, "osservato"
    return int(d.servizi[servizio_id].get("rendimento_stimato_bp") or 0), "stimato"


def commissione_stimata_cents(servizio: Dict[str, Any], capitale_cents: int,
                              roi_bp: int) -> int:
    """Commissione MENSILE attesa per noi su `capitale_cents` nel servizio. Mai negativa."""
    modello = servizio["modello_commissione"]
    if capitale_cents <= 0:
        return int(servizio.get("commissione_fissa_cents") or 0) if modello == "fisso_mensile" else 0
    if modello == "percentuale_profitto":
        profitto = _div(capitale_cents * max(roi_bp, 0), 10_000)
        return _div(profitto * int(servizio["commissione_bp"]), 10_000)
    if modello == "percentuale_capitale_annua":
        return _div(capitale_cents * int(servizio["commissione_bp"]), 10_000 * 12)
    return int(servizio.get("commissione_fissa_cents") or 0)


def affinita_bp(d: Dati) -> Dict[Tuple[int, int], int]:
    """(a, b) → quota (bp) dei clienti con il servizio a ATTIVO che hanno attivo anche b.
    È il CRM che legge se stesso: «chi ha a, spesso prende anche b»."""
    attivi: Dict[int, Set[int]] = {}
    for cid, posz in d.per_cliente.items():
        attivi[cid] = {p.servizio_id for p in posz if p.stato == "attiva"}
    con_a: Dict[int, int] = defaultdict(int)
    con_ab: Dict[Tuple[int, int], int] = defaultdict(int)
    for servizi in attivi.values():
        for a in servizi:
            con_a[a] += 1
            for b in servizi:
                if a != b:
                    con_ab[(a, b)] += 1
    return {k: _div(v * 10_000, con_a[k[0]]) for k, v in con_ab.items()}


@dataclass
class MetricheCliente:
    cliente_id: int
    capitale_cents: int
    profitto_mese_cents: int
    profitto_mese_prec_cents: int
    profitto_totale_cents: int
    commissioni_totali_cents: int
    commissioni_mese_cents: int
    pagamenti: int
    servizi_attivi: List[int]
    posizioni: List[Posizione]


def metriche_cliente(d: Dati, cliente_id: int) -> MetricheCliente:
    posz = d.per_cliente.get(cliente_id, [])
    mese = d.mese
    prec = mese_precedente(mese)
    return MetricheCliente(
        cliente_id=cliente_id,
        capitale_cents=sum(p.capitale_cents for p in posz if p.stato != "chiusa"),
        profitto_mese_cents=sum(p.profitto_per_mese.get(mese, 0) for p in posz),
        profitto_mese_prec_cents=sum(p.profitto_per_mese.get(prec, 0) for p in posz),
        profitto_totale_cents=sum(p.profitto_totale_cents for p in posz),
        commissioni_totali_cents=sum(p.commissioni_totali_cents for p in posz),
        commissioni_mese_cents=sum(p.commissioni_per_mese.get(mese, 0) for p in posz),
        pagamenti=sum(p.pagamenti for p in posz),
        servizi_attivi=sorted(p.servizio_id for p in posz if p.stato == "attiva"),
        posizioni=list(posz),
    )


# ---------------------------------------------------------------- panoramica
def panoramica(d: Dati, mesi_serie: int = 12) -> Dict[str, Any]:
    """Tutto quello che serve alla dashboard, in un dizionario serializzabile in JSON."""
    mese = d.mese
    prec = mese_precedente(mese)
    servizi_ord = sorted(d.servizi.values(), key=lambda s: (int(s["priorita"]), int(s["id"])))
    slot = {int(s["id"]): i for i, s in enumerate(servizi_ord)}
    nomi_servizi = {int(s["id"]): str(s["nome"]) for s in servizi_ord}
    nomi_clienti = {cid: str(c["nome"]) for cid, c in d.clienti.items()}

    proposte_aperte: Dict[int, Dict[str, Any]] = {}
    ultimo_contatto: Dict[int, str] = {}
    for p in d.proposte:
        cid = int(p["cliente_id"])
        if p["stato"] in ("da_approvare", "inviata"):
            proposte_aperte[cid] = p
        if p.get("inviata_il"):
            ultimo_contatto[cid] = max(ultimo_contatto.get(cid, ""), str(p["inviata_il"]))

    righe_clienti: List[Dict[str, Any]] = []
    attivi = 0
    multi = 0
    tot_servizi_attivi = 0
    for cid, c in sorted(d.clienti.items(), key=lambda kv: str(kv[1]["nome"]).lower()):
        m = metriche_cliente(d, cid)
        if c["stato"] == "attivo":
            attivi += 1
            tot_servizi_attivi += len(m.servizi_attivi)
            if len(m.servizi_attivi) >= 2:
                multi += 1
        celle = {}
        for pos in m.posizioni:
            celle[str(pos.servizio_id)] = {
                "posizione_id": pos.id,
                "stato": pos.stato,
                "capitale_cents": pos.capitale_cents,
                "profitto_mese_cents": pos.profitto_per_mese.get(mese, 0),
                "profitto_mese_prec_cents": pos.profitto_per_mese.get(prec, 0),
                "roi_bp": roi_posizione_bp(pos, mese),
            }
        aperta = proposte_aperte.get(cid)
        righe_clienti.append({
            "id": cid,
            "nome": c["nome"],
            "telefono": c["telefono"],
            "email": c["email"],
            "stato": c["stato"],
            "consenso_marketing": bool(c["consenso_marketing"]),
            "opt_out": bool(c["opt_out"]),
            "presentato_da": c["presentato_da"],
            "presentato_da_nome": nomi_clienti.get(int(c["presentato_da"])) if c["presentato_da"] else None,
            "pagante": m.pagamenti > 0,
            "pagamenti": m.pagamenti,
            "capitale_cents": m.capitale_cents,
            "profitto_mese_cents": m.profitto_mese_cents,
            "profitto_mese_prec_cents": m.profitto_mese_prec_cents,
            "profitto_totale_cents": m.profitto_totale_cents,
            "commissioni_totali_cents": m.commissioni_totali_cents,
            "commissioni_mese_cents": m.commissioni_mese_cents,
            "servizi_attivi": m.servizi_attivi,
            "celle": celle,
            "proposta_aperta": None if aperta is None else {
                "id": aperta["id"], "tipo": aperta["tipo"], "stato": aperta["stato"],
                "valore_stimato_cents": aperta["valore_stimato_cents"]},
            "ultimo_contatto": ultimo_contatto.get(cid),
            "creato_il": c["creato_il"],
        })

    righe_servizi: List[Dict[str, Any]] = []
    for s in servizi_ord:
        sid = int(s["id"])
        posz = [p for p in d.posizioni.values() if p.servizio_id == sid]
        clienti_attivi = sum(1 for p in posz if p.stato == "attiva"
                             and d.clienti.get(p.cliente_id, {}).get("stato") == "attivo")
        roi = roi_servizio_bp(d, sid)
        righe_servizi.append({
            "id": sid, "codice": s["codice"], "nome": s["nome"], "descrizione": s["descrizione"],
            "modello_commissione": s["modello_commissione"],
            "commissione_bp": s["commissione_bp"],
            "commissione_fissa_cents": s["commissione_fissa_cents"],
            "capitale_minimo_cents": s["capitale_minimo_cents"],
            "rendimento_stimato_bp": s["rendimento_stimato_bp"],
            "priorita": s["priorita"], "attivo": bool(s["attivo"]), "slot": slot[sid],
            "clienti_attivi": clienti_attivi,
            "penetrazione_bp": _div(clienti_attivi * 10_000, attivi) if attivi else 0,
            "capitale_cents": sum(p.capitale_cents for p in posz if p.stato != "chiusa"),
            "profitto_mese_cents": sum(p.profitto_per_mese.get(mese, 0) for p in posz),
            "commissioni_mese_cents": sum(p.commissioni_per_mese.get(mese, 0) for p in posz),
            "commissioni_totali_cents": sum(p.commissioni_totali_cents for p in posz),
            "roi_osservato_bp": roi,
        })

    serie_mesi = ultimi_mesi(mese, mesi_serie)
    comm_serie = [sum(p.commissioni_per_mese.get(x, 0) for p in d.posizioni.values()) for x in serie_mesi]
    prof_serie = [sum(p.profitto_per_mese.get(x, 0) for p in d.posizioni.values()) for x in serie_mesi]

    conteggio: Dict[str, int] = defaultdict(int)
    for p in d.proposte:
        conteggio[str(p["stato"])] += 1
    decise = conteggio["accettata"] + conteggio["rifiutata"]
    aperte = [p for p in d.proposte if p["stato"] in ("da_approvare", "inviata")]

    def _proposta(p: Dict[str, Any]) -> Dict[str, Any]:
        cid = int(p["cliente_id"])
        c = d.clienti.get(cid, {})
        return {
            "id": p["id"], "cliente_id": cid, "cliente_nome": nomi_clienti.get(cid, "?"),
            "telefono": c.get("telefono"),
            "tipo": p["tipo"], "stato": p["stato"], "livello": p["livello"],
            "servizio_id": p["servizio_id"],
            "servizio_nome": nomi_servizi.get(int(p["servizio_id"])) if p["servizio_id"] else None,
            "motivo": p["motivo"], "messaggio": p["messaggio"],
            "valore_stimato_cents": p["valore_stimato_cents"],
            "creata_il": p["creata_il"], "inviata_il": p["inviata_il"],
            "esito_il": p["esito_il"],
        }

    chiuse = sorted((p for p in d.proposte if p["stato"] not in ("da_approvare", "inviata")),
                    key=lambda p: str(p.get("esito_il") or p["aggiornata_il"]), reverse=True)[:30]
    aperte_ord = sorted(aperte, key=lambda p: (p["stato"] != "da_approvare",
                                               -int(p["valore_stimato_cents"]), int(p["id"])))

    capitale_totale = sum(r["capitale_cents"] for r in righe_clienti if r["stato"] == "attivo")
    return {
        "oggi": d.oggi.isoformat(),
        "mese": mese,
        "mese_label": etichetta_mese(mese),
        "mese_prec_label": etichetta_mese(prec),
        "kpi": {
            "clienti_totali": len(d.clienti),
            "clienti_attivi": attivi,
            "clienti_paganti": sum(1 for r in righe_clienti if r["pagante"] and r["stato"] == "attivo"),
            "clienti_multi_servizio": multi,
            "servizi_per_cliente_x100": _div(tot_servizi_attivi * 100, attivi) if attivi else 0,
            "servizi_attivi": sum(1 for s in righe_servizi if s["attivo"]),
            "capitale_totale_cents": capitale_totale,
            "profitto_clienti_mese_cents": prof_serie[-1],
            "profitto_clienti_mese_prec_cents": prof_serie[-2] if len(prof_serie) > 1 else 0,
            "commissioni_mese_cents": comm_serie[-1],
            "commissioni_mese_prec_cents": comm_serie[-2] if len(comm_serie) > 1 else 0,
            "commissioni_totali_cents": sum(p.commissioni_totali_cents for p in d.posizioni.values()),
            "opportunita_aperte": len(aperte),
            "opportunita_da_approvare": conteggio["da_approvare"],
            "valore_opportunita_cents": sum(int(p["valore_stimato_cents"]) for p in aperte),
            "tasso_accettazione_bp": _div(conteggio["accettata"] * 10_000, decise) if decise else None,
        },
        "imbuto": {k: conteggio[k] for k in ("da_approvare", "inviata", "senza_risposta",
                                             "accettata", "rifiutata", "scartata", "superata")},
        "serie": {"mesi": serie_mesi, "etichette": [etichetta_mese(x) for x in serie_mesi],
                  "commissioni_cents": comm_serie, "profitto_clienti_cents": prof_serie},
        "servizi": righe_servizi,
        "clienti": righe_clienti,
        "proposte_aperte": [_proposta(p) for p in aperte_ord],
        "proposte_recenti": [_proposta(p) for p in chiuse],
    }
