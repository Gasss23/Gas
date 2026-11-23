"""Gas usa il CRM parlando con l'operatore (Telegram e voce) — decisione 18 del 23-11,
`reports/crm/decisioni.md`.

Tre funzioni, chiamate dal kernel (gas.py) per gli strumenti `crm_consulta` e `crm_modifica`:

  * `consulta(store, cosa, cliente)` — SOLA LETTURA, testo per il modello. Che lo legga
    solo Opus lo garantisce il kernel (regola dei modelli, punto 10). Mai solleva.
  * `prepara(store, args, testo_operatore)` — controlla una modifica SENZA scrivere e la
    rende canonica: id al posto dei nomi, importo in centesimi. Ritorna gli argomenti
    canonici e la descrizione a parole che l'operatore legge nella richiesta di firma.
    Gli importi devono comparire nei messaggi dell'operatore (`testo_operatore`): se la
    cifra non c'è, il modello la chiede, non la inventa. Solleva ErroreCRM.
  * `applica(store, canonici)` — dopo la firma dell'operatore: ricontrolla e scrive.
    Accetta SOLO la forma canonica (che produce `prepara`): il modello non può saltare i
    controlli scrivendo da sé gli id. Solleva ErroreCRM.

Regole incise qui e nei test:
  * niente cancellazioni: «togliere» un cliente = stato «perso», i dati restano;
  * i soldi li detta l'operatore (vedi sopra) e li firma: niente cifre del modello;
  * i messaggi d'errore non citano dati di altri clienti oltre a quelli che il modello
    ha chiesto (in caso di nome ambiguo elencano i candidati: servono per scegliere).
"""
from __future__ import annotations

import logging
import re
import unicodedata
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from modules.crm import analisi, motore
from modules.crm.store import (
    CRMStore, ErroreCRM, NOME_MAX, STATI_CLIENTE, TIPI_MOVIMENTO, formatta_euro,
    normalizza_anagrafica, parse_importo, valida_data, valida_quando,
)

log = logging.getLogger(__name__)

VERSIONE_CANONICA = 1
ID_MAX = 2**62  # come lo store: oltre, un id non è valido (R-839-6)
CONSULTE: Tuple[str, ...] = ("riepilogo", "clienti", "cliente", "servizi", "promemoria",
                             "proposte")
AZIONI: Tuple[str, ...] = ("nuovo_cliente", "aggiorna_cliente", "stato_cliente",
                           "apri_servizio", "movimento", "promemoria", "annulla_promemoria")
CAMPI_CLIENTE: Tuple[str, ...] = ("nome", "telefono", "email", "note", "consenso_marketing",
                                  "opt_out", "followup_attivo", "presentato_da")
_CAMPI_BOOL = ("consenso_marketing", "opt_out", "followup_attivo")

# Argomenti che il MODELLO può passare, azione per azione (tutto il resto → rifiutato).
_ARGOMENTI: Dict[str, frozenset] = {
    "nuovo_cliente": frozenset({"azione", "nome", "telefono", "email", "note",
                                "consenso_marketing", "presentato_da"}),
    "aggiorna_cliente": frozenset({"azione", "cliente"} | set(CAMPI_CLIENTE)),
    "stato_cliente": frozenset({"azione", "cliente", "stato"}),
    "apri_servizio": frozenset({"azione", "cliente", "servizio", "importo", "data"}),
    "movimento": frozenset({"azione", "cliente", "servizio", "tipo", "importo", "data",
                            "nota"}),
    "promemoria": frozenset({"azione", "testo", "quando", "cliente"}),
    "annulla_promemoria": frozenset({"azione", "promemoria"}),
}
# Chiavi della forma CANONICA (la scrive solo `prepara`), azione per azione.
_CANONICI: Dict[str, frozenset] = {
    "nuovo_cliente": frozenset({"v", "azione", "nome", "telefono", "email", "note",
                                "consenso_marketing", "presentato_da_id"}),
    "aggiorna_cliente": frozenset({"v", "azione", "cliente_id", "campi"}),
    "stato_cliente": frozenset({"v", "azione", "cliente_id", "stato"}),
    "apri_servizio": frozenset({"v", "azione", "cliente_id", "servizio_id", "importo_cents",
                                "data"}),
    "movimento": frozenset({"v", "azione", "cliente_id", "posizione_id", "tipo",
                            "importo_cents", "data", "nota"}),
    "promemoria": frozenset({"v", "azione", "testo", "quando", "cliente_id"}),
    "annulla_promemoria": frozenset({"v", "azione", "promemoria_id"}),
}

USCITA_MAX = 8000          # caratteri massimi di una consultazione (contesto del modello)
RIGHE_ELENCO_MAX = 100
_GIORNI = ("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica")
_TIPO_A_PAROLE = {"deposito": "DEPOSITO (capitale in più)", "prelievo": "PRELIEVO (capitale in meno)",
                  "profitto": "PROFITTO", "perdita": "PERDITA", "commissione": "COMMISSIONE incassata"}
_STATO_A_PAROLE = {"attivo": "attivo", "in_pausa": "in pausa",
                   "perso": "perso (archiviato: i dati restano, non si cancella nulla)"}


# --------------------------------------------------------------------- importi detti
_RE_NUMERO = re.compile(r"(?<![0-9])[0-9](?:[0-9.,]*[0-9])?")
_RE_MILA = re.compile(r"(?<![0-9.,])([0-9]{1,4}(?:[.,][0-9]{1,3})?)\s*(mila|k)\b", re.IGNORECASE)
# R-839-4: numeri che NON sono importi, tolti prima di cercarli: date («20/06»,
# «20-06-2026», «2026-06-20»), ore («15:30», «alle 15.30») e numeri di cliente o di
# promemoria («#12»).
_RE_NON_IMPORTI = re.compile(
    r"(?<![0-9])[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}(?![0-9])"
    r"|(?<![0-9.,])[0-9]{1,2}[/-][0-9]{1,2}(?:[/-][0-9]{2,4})?(?![0-9])"
    r"|(?<![0-9])[0-9]{1,2}:[0-9]{2}(?![0-9])"
    r"|\b(?:alle|dalle|ore|entro le)\s+[0-9]{1,2}[.,][0-9]{2}\b"
    r"|#\s*[0-9]+", re.IGNORECASE)


def importi_nel_testo(testo: str) -> Set[int]:
    """Tutti gli importi (in centesimi) che si leggono nel testo dell'operatore: cifre
    («1.500», «1500,50») e «N mila» / «Nk». Le parole («mille») non contano: in quel
    caso il modello chiede la cifra. Date, ore e «#numeri» non contano (R-839-4).
    LIMITE dichiarato: gli altri numeri del messaggio (un telefono, una quantità) contano
    ancora come importi possibili; la barriera vera resta la firma, che mostra la cifra
    per esteso. Mai solleva."""
    trovati: Set[int] = set()
    if not isinstance(testo, str):
        return trovati
    testo = _RE_NON_IMPORTI.sub(" ", testo)
    for m in _RE_NUMERO.finditer(testo):
        try:
            trovati.add(parse_importo(m.group(0)))
        except ErroreCRM:
            continue
    for m in _RE_MILA.finditer(testo):
        try:
            base = parse_importo(m.group(1).replace(".", ","))
        except ErroreCRM:
            continue
        trovati.add(base * 1000)
    return trovati


def _importo_arg(valore: Any) -> int:
    """Importo passato dal modello: cifre («1.500», «1500,50») oppure «N mila» / «Nk»."""
    if isinstance(valore, str):
        m = _RE_MILA.fullmatch(valore.strip())
        if m:
            return parse_importo(m.group(1).replace(".", ",")) * 1000
    return parse_importo(valore)


def _controlla_importo_detto(cents: int, testo_operatore: Optional[str]) -> None:
    if cents not in importi_nel_testo(testo_operatore or ""):
        raise ErroreCRM(
            f"l'importo {formatta_euro(cents)} non compare nei messaggi dell'operatore: "
            "chiedigli la cifra esatta (scritta in numeri) e non stimarla")


# --------------------------------------------------------------------- ricerca
def _norm(testo: str) -> str:
    """Per confrontare i nomi: maiuscole, spazi e accenti a parte («Nicolò» = «nicolo»)."""
    senza = "".join(ch for ch in unicodedata.normalize("NFKD", testo)
                    if not unicodedata.combining(ch))
    return " ".join(senza.casefold().split())


def _parole_a_inizio(cerca: str, nome: str) -> bool:
    """Ogni parola cercata è l'INIZIO di una parola del nome («ross» → «Mario Rossi»),
    mai un pezzo in mezzo (R-839-1: «Anna» non deve trovare «Marianna»)."""
    # parole divise anche da apostrofi e trattini: «amico» trova «D'Amico»
    parole_nome = [x for x in re.split(r"[^\w]+", nome) if x]
    parole = [x for x in re.split(r"[^\w]+", cerca) if x]
    return bool(parole) and all(any(pn.startswith(p) for pn in parole_nome) for p in parole)


def _rif_id(rif: Any, campo: str) -> Optional[int]:
    """«#12», «12» o 12 → 12; altrimenti None (è un nome)."""
    if isinstance(rif, bool):
        raise ErroreCRM(f"{campo}: valore non valido")
    if isinstance(rif, int):
        if rif > ID_MAX:
            raise ErroreCRM(f"{campo}: numero troppo grande")
        return rif if rif > 0 else None
    if isinstance(rif, str):
        m = re.fullmatch(r"\s*#?\s*([0-9]{1,12})\s*", rif)
        if m:
            return int(m.group(1))
    return None


def trova_cliente(store: CRMStore, rif: Any, campo: str = "cliente") -> Dict[str, Any]:
    """Il cliente indicato da `rif` (id o nome): vedi `cerca_cliente`."""
    return cerca_cliente(store, rif, campo)[0]


def cerca_cliente(store: CRMStore, rif: Any,
                  campo: str = "cliente") -> Tuple[Dict[str, Any], Optional[str]]:
    """Il cliente indicato da `rif` (id o nome) e, se trovato per somiglianza, l'avviso da
    mettere nella firma. Il nome vale se identifica UN cliente: prima il nome uguale
    (maiuscole, spazi e accenti a parte), poi le parole cercate come INIZIO delle parole
    del nome («mario ross» → «Mario Rossi»; mai «Anna» → «Marianna», R-839-1). Se più
    clienti corrispondono → errore coi candidati, per far scegliere l'operatore."""
    if rif is None or (isinstance(rif, str) and not rif.strip()):
        raise ErroreCRM(f"{campo}: indica il cliente (nome o #numero)")
    cid = _rif_id(rif, campo)
    if cid is not None:
        c = store.cliente(cid)
        if c is None:
            raise ErroreCRM(f"{campo}: nessun cliente #{cid}")
        return c, None
    if not isinstance(rif, str) or len(rif) > NOME_MAX:
        raise ErroreCRM(f"{campo}: valore non valido")
    cerca = _norm(rif)
    tutti = store.clienti()
    uguali = [c for c in tutti if _norm(str(c["nome"])) == cerca]
    candidati = uguali or [c for c in tutti if _parole_a_inizio(cerca, _norm(str(c["nome"])))]
    if len(candidati) == 1:
        avviso = None if uguali else (f"ATTENZIONE: hai indicato «{rif.strip()}», trovato per "
                                      f"somiglianza {_nome(candidati[0])}")
        return candidati[0], avviso
    if not candidati:
        raise ErroreCRM(f"{campo}: nessun cliente si chiama «{rif.strip()}»")
    elenco = ", ".join(f"#{c['id']} {c['nome']}" for c in candidati[:10])
    raise ErroreCRM(f"{campo}: «{rif.strip()}» corrisponde a più clienti ({elenco}"
                    f"{' …' if len(candidati) > 10 else ''}): indica quale col #numero")


def trova_servizio(store: CRMStore, rif: Any) -> Dict[str, Any]:
    """Servizio per id, codice o nome (uguale, poi pezzo di nome se unico)."""
    if rif is None or (isinstance(rif, str) and not rif.strip()):
        raise ErroreCRM("servizio: indica il servizio (nome o codice)")
    servizi = store.servizi()
    sid = _rif_id(rif, "servizio")
    if sid is not None:
        for s in servizi:
            if int(s["id"]) == sid:
                return s
        raise ErroreCRM(f"servizio: nessun servizio #{sid}")
    if not isinstance(rif, str) or len(rif) > NOME_MAX:
        raise ErroreCRM("servizio: valore non valido")
    cerca = _norm(rif)
    uguali = [s for s in servizi if cerca in (_norm(str(s["codice"])), _norm(str(s["nome"])))]
    candidati = uguali or [s for s in servizi if cerca in _norm(str(s["nome"]))]
    if len(candidati) == 1:
        return candidati[0]
    nomi = ", ".join(f"{s['nome']} ({s['codice']})" for s in servizi) or "nessuno"
    if not candidati:
        raise ErroreCRM(f"servizio «{rif.strip()}» sconosciuto (servizi: {nomi})")
    raise ErroreCRM(f"servizio «{rif.strip()}» ambiguo (servizi: {nomi})")


def _posizione_per_movimento(store: CRMStore, cliente_id: int,
                             servizio: Any) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """La posizione del cliente su cui registrare: quella del servizio indicato, o
    l'unica non chiusa se il servizio non è indicato."""
    servizi = {int(s["id"]): s for s in store.servizi()}
    posz = store.posizioni(cliente_id)
    if servizio is not None and not (isinstance(servizio, str) and not servizio.strip()):
        srv = trova_servizio(store, servizio)
        for p in posz:
            if int(p["servizio_id"]) == int(srv["id"]):
                return p, srv
        raise ErroreCRM(f"il cliente non è nel servizio {srv['nome']}: prima va aperto "
                        "(azione apri_servizio)")
    aperte = [p for p in posz if p["stato"] != "chiusa"]
    if len(aperte) == 1:
        return aperte[0], servizi[int(aperte[0]["servizio_id"])]
    if not aperte:
        raise ErroreCRM("il cliente non è in nessun servizio: prima va aperto "
                        "(azione apri_servizio)")
    nomi = ", ".join(str(servizi[int(p["servizio_id"])]["nome"]) for p in aperte)
    raise ErroreCRM(f"il cliente è in più servizi ({nomi}): indica quale")


# --------------------------------------------------------------------- utilità
def _nome(c: Dict[str, Any]) -> str:
    return f"«{c['nome']}» (cliente #{c['id']})"


def _giorno_a_parole(quando: str) -> str:
    d = datetime.strptime(quando, "%Y-%m-%d %H:%M")
    return f"{_GIORNI[d.weekday()]} {d.strftime('%d-%m-%Y')} alle {d.strftime('%H:%M')}"


def _bool_arg(v: Any, campo: str) -> bool:
    if isinstance(v, bool):
        return v
    raise ErroreCRM(f"{campo}: deve essere true o false")


def _str_arg(v: Any, campo: str) -> Optional[str]:
    if v is None:
        return None
    if not isinstance(v, str):
        raise ErroreCRM(f"{campo}: deve essere testo")
    return v.strip() or None


def _telefono_libero(store: CRMStore, telefono: Optional[str], escluso: Optional[int]) -> None:
    """Il numero non deve essere già di un altro cliente (lo vieta anche il DB, ma va
    detto PRIMA della firma, non dopo)."""
    if telefono is None:
        return
    for c in store.clienti():
        if c["telefono"] == telefono and int(c["id"]) != escluso:
            raise ErroreCRM(f"il numero è già del cliente #{c['id']}")


def _controlla_chiavi(args: Dict[str, Any], ammesse: frozenset, azione: str) -> None:
    extra = sorted(set(args) - ammesse)
    if extra:
        raise ErroreCRM(f"argomenti non previsti per «{azione}»: {', '.join(extra)}")


# --------------------------------------------------------------------- prepara
def prepara(store: CRMStore, args: Any,
            testo_operatore: Optional[str]) -> Tuple[Dict[str, Any], str]:
    """Controlla la modifica chiesta dal modello e la rende canonica, SENZA scrivere.
    Ritorna (argomenti canonici, descrizione per la firma). Solleva ErroreCRM."""
    if not isinstance(args, dict):
        raise ErroreCRM("argomenti non validi")
    azione = args.get("azione")
    if azione not in AZIONI:
        raise ErroreCRM(f"azione non valida (ammesse: {', '.join(AZIONI)})")
    _controlla_chiavi(args, _ARGOMENTI[azione], azione)
    out, desc, avvisi = _prepara_azione(store, azione, args, testo_operatore)
    if avvisi:
        desc += ". " + ". ".join(avvisi)
    return out, desc


def _prepara_azione(store: CRMStore, azione: str, args: Dict[str, Any],
                    testo_operatore: Optional[str]) -> Tuple[Dict[str, Any], str, List[str]]:
    out: Dict[str, Any] = {"v": VERSIONE_CANONICA, "azione": azione}
    avvisi: List[str] = []

    def trova(rif: Any, campo: str = "cliente") -> Dict[str, Any]:
        c, avviso = cerca_cliente(store, rif, campo)
        if avviso:
            avvisi.append(avviso)
        return c

    if azione == "nuovo_cliente":
        nome = normalizza_anagrafica("nome", _str_arg(args.get("nome"), "nome"))
        assert nome is not None
        out["nome"] = nome
        for k in ("telefono", "email", "note"):
            v = normalizza_anagrafica(k, _str_arg(args.get(k), k))
            if v is not None:
                out[k] = v
        _telefono_libero(store, out.get("telefono"), None)
        if "consenso_marketing" in args:
            out["consenso_marketing"] = _bool_arg(args["consenso_marketing"], "consenso_marketing")
        pres = None
        if args.get("presentato_da") not in (None, ""):
            pres = trova(args["presentato_da"], "presentato_da")
            out["presentato_da_id"] = int(pres["id"])
        _valida_canonico(store, out)
        parti = [f"Aggiungi il nuovo cliente «{nome}»"]
        if out.get("telefono"):
            parti.append(f"telefono {out['telefono']}")
        if out.get("email"):
            parti.append(f"email {out['email']}")
        if pres is not None:
            parti.append(f"presentato da {_nome(pres)}")
        parti.append("consenso marketing " + ("DATO" if out.get("consenso_marketing") else "non dato"))
        desc = ", ".join(parti)
        omonimi = [c for c in store.clienti() if _norm(str(c["nome"])) == _norm(nome)]
        if omonimi:
            avvisi.append("ATTENZIONE: esiste già un cliente con questo nome ("
                          + ", ".join(f"#{c['id']}" for c in omonimi) + ")")
        return out, desc, avvisi

    if azione == "aggiorna_cliente":
        cli = trova(args.get("cliente"))
        campi: Dict[str, Any] = {}
        for k in CAMPI_CLIENTE:
            if k not in args:
                continue
            if k in _CAMPI_BOOL:
                campi[k] = _bool_arg(args[k], k)
            elif k == "presentato_da":
                if args[k] in (None, ""):
                    campi[k] = None
                else:
                    campi[k] = int(trova(args[k], "presentato_da")["id"])
            else:
                campi[k] = normalizza_anagrafica(k, _str_arg(args[k], k))
        if "telefono" in campi:
            _telefono_libero(store, campi["telefono"], int(cli["id"]))
        if not campi:
            raise ErroreCRM("niente da cambiare: indica almeno un campo")
        out.update(cliente_id=int(cli["id"]), campi=campi)
        _valida_canonico(store, out)
        return out, f"Aggiorna {_nome(cli)}: " + "; ".join(
            _campo_a_parole(store, k, v, cli.get(k)) for k, v in campi.items()), avvisi

    if azione == "stato_cliente":
        cli = trova(args.get("cliente"))
        stato = str(args.get("stato"))
        out.update(cliente_id=int(cli["id"]), stato=stato)
        _valida_canonico(store, out)
        if cli["stato"] == stato:
            raise ErroreCRM(f"il cliente è già nello stato «{stato}»")
        return out, (f"Cambia lo stato di {_nome(cli)}: da {cli['stato']} a "
                     f"{_STATO_A_PAROLE[stato]}"), avvisi

    if azione == "apri_servizio":
        cli = trova(args.get("cliente"))
        srv = trova_servizio(store, args.get("servizio"))
        out.update(cliente_id=int(cli["id"]), servizio_id=int(srv["id"]),
                   data=valida_data(args.get("data") or store.oggi().isoformat(),
                                    "data di apertura"))
        if out["data"] > store.oggi().isoformat():
            raise ErroreCRM("data di apertura nel futuro")
        vecchia = next((pos for pos in store.posizioni(int(cli["id"]))
                        if int(pos["servizio_id"]) == int(srv["id"])), None)
        if vecchia is not None and vecchia["stato"] == "attiva":
            raise ErroreCRM(f"il cliente è già nel servizio {srv['nome']}")
        if args.get("importo") not in (None, ""):
            out["importo_cents"] = _importo_arg(args["importo"])
            _controlla_importo_detto(out["importo_cents"], testo_operatore)
        _valida_canonico(store, out)
        if vecchia is not None:
            # R-839-3: lo store RIATTIVA la posizione di prima, che resta aperta dalla sua
            # data; il deposito non può essere datato prima di quella
            if "importo_cents" in out and out["data"] < str(vecchia["aperta_il"]):
                raise ErroreCRM(f"data {out['data']} prima dell'apertura del servizio "
                                f"({vecchia['aperta_il']})")
            desc = (f"Riattiva {_nome(cli)} nel servizio «{srv['nome']}» (era {vecchia['stato']}, "
                    f"aperto dal {vecchia['aperta_il']})")
            if "importo_cents" in out:
                desc += (f", con DEPOSITO di {formatta_euro(out['importo_cents'])} "
                         f"in data {out['data']}")
            return out, desc, avvisi
        desc = f"Metti {_nome(cli)} nel servizio «{srv['nome']}» dal {out['data']}"
        if "importo_cents" in out:
            desc += f", con capitale iniziale (DEPOSITO) di {formatta_euro(out['importo_cents'])}"
        return out, desc, avvisi

    if azione == "movimento":
        cli = trova(args.get("cliente"))
        pos, srv = _posizione_per_movimento(store, int(cli["id"]), args.get("servizio"))
        if args.get("importo") in (None, ""):
            raise ErroreCRM("importo: obbligatorio (chiedilo all'operatore)")
        cents = _importo_arg(args["importo"])
        _controlla_importo_detto(cents, testo_operatore)
        out.update(cliente_id=int(cli["id"]), posizione_id=int(pos["id"]),
                   tipo=args.get("tipo"), importo_cents=cents,
                   data=valida_data(args.get("data") or store.oggi().isoformat()))
        nota = _str_arg(args.get("nota"), "nota")
        if nota is not None:
            out["nota"] = nota
        _valida_canonico(store, out)
        store.valida_movimento(out["posizione_id"], out["tipo"], cents, out["data"],
                               "operatore", nota)
        if out["data"] < str(pos["aperta_il"]):
            raise ErroreCRM(f"data {out['data']} prima dell'apertura del servizio "
                            f"({pos['aperta_il']})")
        if out["tipo"] == "prelievo":
            capitale = store.capitale_minimo_dal(out["posizione_id"], out["data"])
            if capitale is None:
                raise ErroreCRM("database del CRM non disponibile")
            if cents > capitale:
                raise ErroreCRM(f"prelievo di {formatta_euro(cents)} maggiore del capitale "
                                f"disponibile dal {out['data']} ({formatta_euro(capitale)})")
        return out, (f"Registra per {_nome(cli)}, servizio «{srv['nome']}»: "
                     f"{_TIPO_A_PAROLE[out['tipo']]} di {formatta_euro(cents)} "
                     f"in data {out['data']}"), avvisi

    if azione == "promemoria":
        testo, quando = store.valida_promemoria(args.get("testo"), args.get("quando"))
        out.update(testo=testo, quando=quando)
        collegato: Optional[Dict[str, Any]] = None
        if args.get("cliente") not in (None, ""):
            collegato = trova(args["cliente"])
            out["cliente_id"] = int(collegato["id"])
        _valida_canonico(store, out)
        desc = f"Promemoria per {_giorno_a_parole(out['quando'])}: «{testo}»"
        if collegato is not None:
            desc += f", collegato a {_nome(collegato)}"
        return out, desc, avvisi

    # annulla_promemoria
    pid = _rif_id(args.get("promemoria"), "promemoria")
    if pid is None:
        raise ErroreCRM("promemoria: indica il numero del promemoria (#id)")
    out["promemoria_id"] = pid
    pr = _valida_canonico(store, out)
    if pr is None:  # non succede: _valida_canonico solleva prima
        raise ErroreCRM("promemoria non trovato")
    return out, f"Annulla il promemoria #{pid} del {pr['quando']}: «{pr['testo']}»", avvisi


def _campo_a_parole(store: CRMStore, k: str, v: Any, prima: Any = None) -> str:
    if k == "consenso_marketing":
        return "consenso marketing " + ("DATO" if v else "TOLTO")
    if k == "opt_out":
        return ("STOP ai messaggi (il cliente non vuole più messaggi)" if v
                else "STOP revocato (il cliente accetta di nuovo i messaggi)")
    if k == "followup_attivo":
        return "follow-up mensile " + ("ACCESO" if v else "SPENTO")
    if k == "presentato_da":
        if v is None:
            return "presentato da: nessuno"
        c = store.cliente(int(v))
        return "presentato da " + (_nome(c) if c else f"#{v}")
    # R-839-7: il valore nuovo SOSTITUISCE quello di prima, che la firma deve mostrare
    vecchio = "(vuoto)" if prima in (None, "") else f"«{prima}»"
    nuovo = "(vuoto)" if v is None else f"«{v}»"
    if k == "note":
        return f"note: SOSTITUISCE la nota attuale {vecchio} con {nuovo}"
    return f"{k}: {nuovo} (prima: {vecchio})"


# --------------------------------------------------------------------- forma canonica
def _valida_canonico(store: CRMStore, c: Any) -> Optional[Dict[str, Any]]:
    """Controlli della forma canonica, gli stessi a `prepara` e ad `applica` (dopo la
    firma il DB può essere cambiato). Ritorna il promemoria per `annulla_promemoria`."""
    if not isinstance(c, dict) or c.get("v") != VERSIONE_CANONICA:
        raise ErroreCRM("modifica non in forma canonica: non si applica")
    azione = c.get("azione")
    if azione not in AZIONI:
        raise ErroreCRM("azione non valida")
    _controlla_chiavi(c, _CANONICI[azione], azione)

    def intero(k: str) -> int:
        v = c.get(k)
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= ID_MAX:
            raise ErroreCRM(f"{k}: id non valido")
        return v

    def cliente_esiste(k: str) -> Dict[str, Any]:
        cli = store.cliente(intero(k))
        if cli is None:
            raise ErroreCRM("cliente inesistente")
        return cli

    if azione in ("nuovo_cliente", "aggiorna_cliente"):
        campi_testo = c if azione == "nuovo_cliente" else c.get("campi")
        if not isinstance(campi_testo, dict):
            raise ErroreCRM("campi da aggiornare non validi")
        if azione == "nuovo_cliente" and "nome" not in c:
            raise ErroreCRM("nome: obbligatorio")
        for k in ("nome", "telefono", "email", "note"):
            if k in campi_testo:
                normalizza_anagrafica(k, campi_testo[k])
    if azione == "nuovo_cliente":
        if "presentato_da_id" in c:
            cliente_esiste("presentato_da_id")
        if "consenso_marketing" in c and not isinstance(c["consenso_marketing"], bool):
            raise ErroreCRM("consenso_marketing non valido")
    elif azione == "aggiorna_cliente":
        cid = int(cliente_esiste("cliente_id")["id"])
        campi = c.get("campi")
        if not isinstance(campi, dict) or not campi or set(campi) - set(CAMPI_CLIENTE):
            raise ErroreCRM("campi da aggiornare non validi")
        for k in _CAMPI_BOOL:
            if k in campi and not isinstance(campi[k], bool):
                raise ErroreCRM(f"{k} non valido")
        if campi.get("presentato_da") is not None:
            if intero_di(campi["presentato_da"]) == cid:
                raise ErroreCRM("un cliente non può presentare se stesso")
            if store.cliente(intero_di(campi["presentato_da"])) is None:
                raise ErroreCRM("presentato_da: cliente inesistente")
    elif azione == "stato_cliente":
        cliente_esiste("cliente_id")
        if c.get("stato") not in STATI_CLIENTE:
            raise ErroreCRM(f"stato non valido (ammessi: {', '.join(STATI_CLIENTE)})")
    elif azione == "apri_servizio":
        cliente_esiste("cliente_id")
        sid = intero("servizio_id")
        if not any(int(s["id"]) == sid for s in store.servizi()):
            raise ErroreCRM("servizio inesistente")
        valida_data(c.get("data"), "data di apertura")
        if "importo_cents" in c:
            intero("importo_cents")
    elif azione == "movimento":
        cid = int(cliente_esiste("cliente_id")["id"])
        pid = intero("posizione_id")
        if not any(int(p["id"]) == pid for p in store.posizioni(cid)):
            raise ErroreCRM("la posizione non è di questo cliente")
        if c.get("tipo") not in TIPI_MOVIMENTO:
            raise ErroreCRM(f"tipo di movimento non valido (ammessi: {', '.join(TIPI_MOVIMENTO)})")
        intero("importo_cents")
        valida_data(c.get("data"))
    elif azione == "promemoria":
        if not isinstance(c.get("testo"), str) or not c["testo"].strip():
            raise ErroreCRM("testo del promemoria: obbligatorio")
        valida_quando(c.get("quando"))
        if "cliente_id" in c:
            cliente_esiste("cliente_id")
    else:  # annulla_promemoria
        pid = intero("promemoria_id")
        for p in store.promemoria(solo_in_attesa=True):
            if int(p["id"]) == pid:
                return p
        raise ErroreCRM(f"nessun promemoria #{pid} in attesa (già mandato, annullato o inesistente)")
    return None


def intero_di(v: Any) -> int:
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= ID_MAX:
        raise ErroreCRM("id non valido")
    return v


# --------------------------------------------------------------------- applica
def applica(store: CRMStore, canonici: Any) -> str:
    """Scrive la modifica FIRMATA dall'operatore. Solo forma canonica, ricontrollata.
    Autore «operatore»: la cifra e la modifica le ha dettate e firmate lui.
    Ritorna l'esito a parole; solleva ErroreCRM."""
    _valida_canonico(store, canonici)
    c = canonici
    azione = c["azione"]
    if azione == "nuovo_cliente":
        nuovo = store.aggiungi_cliente(
            c["nome"], telefono=c.get("telefono"), email=c.get("email"),
            consenso_marketing=bool(c.get("consenso_marketing", False)),
            presentato_da=c.get("presentato_da_id"), note=c.get("note"))
        return f"Cliente aggiunto: #{nuovo}."
    if azione == "aggiorna_cliente":
        campi = dict(c["campi"])
        for k in _CAMPI_BOOL:
            if k in campi:
                campi[k] = int(campi[k])
        store.aggiorna_cliente(c["cliente_id"], **campi)
        return f"Cliente #{c['cliente_id']} aggiornato."
    if azione == "stato_cliente":
        store.aggiorna_cliente(c["cliente_id"], stato=c["stato"])
        return f"Cliente #{c['cliente_id']}: stato «{c['stato']}»."
    if azione == "apri_servizio":
        pid = store.apri_posizione(c["cliente_id"], c["servizio_id"], data=c["data"],
                                   capitale_iniziale_cents=c.get("importo_cents"))
        return f"Cliente #{c['cliente_id']} nel servizio (posizione #{pid})."
    if azione == "movimento":
        mid = store.registra_movimento(c["posizione_id"], c["tipo"], c["importo_cents"],
                                       data=c["data"], fonte="operatore", nota=c.get("nota"))
        return f"Movimento registrato (#{mid})."
    if azione == "promemoria":
        nuovo = store.aggiungi_promemoria(c["testo"], c["quando"], c.get("cliente_id"),
                                          nel_passato=True)
        return f"Promemoria #{nuovo} salvato per il {c['quando']}."
    store.annulla_promemoria(c["promemoria_id"])
    return f"Promemoria #{c['promemoria_id']} annullato."


# --------------------------------------------------------------------- consulta
def consulta(store: CRMStore, cosa: Any, cliente: Any = None) -> str:
    """Testo per il modello (sola lettura). Mai solleva: errore → «Errore: …»."""
    try:
        if cosa not in CONSULTE:
            raise ErroreCRM(f"cosa non valida (ammesse: {', '.join(CONSULTE)})")
        # prima si prova che il DB risponde: una lettura fallita non deve sembrare
        # «nessun promemoria» o «nessun servizio»
        foto = store.fotografia()
        if foto is None:
            raise ErroreCRM("database del CRM non disponibile")
        if cosa == "promemoria":
            testo = _elenco_promemoria(store)
        elif cosa == "servizi":
            testo = _elenco_servizi(store)
        else:
            p = analisi.panoramica(analisi.costruisci(foto, store.oggi()))
            if cosa == "riepilogo":
                testo = _riepilogo(store, p)
            elif cosa == "clienti":
                testo = _elenco_clienti(p)
            elif cosa == "proposte":
                testo = _elenco_proposte(store, p)
            else:
                cli = trova_cliente(store, cliente)
                testo = _scheda_cliente(store, p, int(cli["id"]))
    except ErroreCRM as e:
        return f"Errore: {e}"
    except Exception as e:  # §9: mai crash del turno
        log.warning("CRM agente: consultazione %r fallita (%s)", cosa, type(e).__name__)
        return "Errore: consultazione del CRM non riuscita"
    if len(testo) > USCITA_MAX:
        testo = testo[:USCITA_MAX].rsplit("\n", 1)[0] + "\n… (tagliato: chiedi un cliente alla volta)"
    return testo


def _riepilogo(store: CRMStore, p: Dict[str, Any]) -> str:
    k = p["kpi"]
    attesa = len(store.promemoria(solo_in_attesa=True))
    return "\n".join([
        f"CRM — {p['mese_label']}",
        f"Clienti attivi: {k['clienti_attivi']} (paganti {k['clienti_paganti']}, "
        f"con 2+ servizi {k['clienti_multi_servizio']}); clienti in archivio o in pausa: "
        f"{len(p['clienti']) - k['clienti_attivi']}",
        f"Capitale gestito: {formatta_euro(k['capitale_totale_cents'])}",
        f"Profitto dei clienti nel mese: {formatta_euro(k['profitto_clienti_mese_cents'], segno=True)}",
        f"Commissioni nel mese: {formatta_euro(k['commissioni_mese_cents'])} "
        f"(mese prima {formatta_euro(k['commissioni_mese_prec_cents'])})",
        f"Opportunità aperte: {k['opportunita_aperte']}",
        f"Promemoria in attesa: {attesa}",
    ] + [f"· {s['nome']} ({s['codice']}): {s['clienti_attivi']} clienti attivi, capitale "
         f"{formatta_euro(s['capitale_cents'])}, commissioni del mese "
         f"{formatta_euro(s['commissioni_mese_cents'])}" for s in p["servizi"]])


def _elenco_clienti(p: Dict[str, Any]) -> str:
    nomi_srv = {int(s["id"]): str(s["nome"]) for s in p["servizi"]}
    righe = [f"Clienti: {len(p['clienti'])}"]
    for c in p["clienti"][:RIGHE_ELENCO_MAX]:
        servizi = ", ".join(nomi_srv.get(int(s), f"#{s}") for s in c["servizi_attivi"]) or "nessuno"
        righe.append(f"#{c['id']} {c['nome']} — {c['stato']} — capitale "
                     f"{formatta_euro(c['capitale_cents'])} — servizi: {servizi}")
    if len(p["clienti"]) > RIGHE_ELENCO_MAX:
        righe.append(f"… altri {len(p['clienti']) - RIGHE_ELENCO_MAX}: chiedi per nome")
    return "\n".join(righe)


def _elenco_servizi(store: CRMStore) -> str:
    servizi = store.servizi()
    if not servizi:
        return "Nessun servizio nel CRM."
    return "\n".join(["Servizi:"] + [
        f"#{s['id']} {s['nome']} (codice {s['codice']})" + ("" if s["attivo"] else " — non attivo")
        for s in servizi])


def _elenco_promemoria(store: CRMStore) -> str:
    righe = store.promemoria(solo_in_attesa=True)
    if not righe:
        return "Nessun promemoria in attesa."
    out = [f"Promemoria in attesa: {len(righe)}"]
    for r in righe[:RIGHE_ELENCO_MAX]:
        riga = f"#{r['id']} {_giorno_a_parole(str(r['quando']))} — {r['testo']}"
        if r["cliente_id"] is not None:
            c = store.cliente(int(r["cliente_id"]))
            riga += f" (cliente #{r['cliente_id']}{' ' + str(c['nome']) if c else ''})"
        out.append(riga)
    return "\n".join(out)


def _elenco_proposte(store: CRMStore, p: Dict[str, Any]) -> str:
    nomi = {int(c["id"]): str(c["nome"]) for c in p["clienti"]}
    aperte = [r for r in store.proposte() if r["stato"] in ("da_approvare", "inviata")]
    if not aperte:
        return "Nessuna proposta aperta."
    out = [f"Proposte aperte: {len(aperte)} (si approvano dalla dashboard del CRM)"]
    for r in aperte[:RIGHE_ELENCO_MAX]:
        out.append(f"#{r['id']} {nomi.get(int(r['cliente_id']), '?')} (cliente #{r['cliente_id']}) "
                   f"— {r['tipo']} — {r['stato']} — {r['motivo']}")
    return "\n".join(out)


def _scheda_cliente(store: CRMStore, p: Dict[str, Any], cid: int) -> str:
    riga = next((c for c in p["clienti"] if int(c["id"]) == cid), None)
    if riga is None:
        raise ErroreCRM("cliente inesistente")
    nomi_srv = {int(s["id"]): str(s["nome"]) for s in p["servizi"]}
    sino = lambda b: "sì" if b else "no"  # noqa: E731
    out = [
        f"Cliente #{cid}: {riga['nome']}",
        f"Stato: {riga['stato']} · telefono: {riga['telefono'] or '—'} · email: {riga['email'] or '—'}",
        f"Consenso marketing: {sino(riga['consenso_marketing'])} · STOP ai messaggi: "
        f"{sino(riga['opt_out'])} · follow-up mensile: {'acceso' if riga['followup_attivo'] else 'spento'}",
        f"Cliente dal: {str(riga['creato_il'])[:10]}"
        + (f" · presentato da #{riga['presentato_da']} {riga['presentato_da_nome'] or ''}".rstrip()
           if riga["presentato_da"] else ""),
        f"Capitale: {formatta_euro(riga['capitale_cents'])} · profitto del mese: "
        f"{formatta_euro(riga['profitto_mese_cents'], segno=True)} · commissioni totali: "
        f"{formatta_euro(riga['commissioni_totali_cents'])} ({riga['pagamenti']} pagamenti)",
        "Servizi:",
    ]
    for sid, cella in riga["celle"].items():
        out.append(f"- {nomi_srv.get(int(sid), '#' + sid)} (posizione #{cella['posizione_id']}, "
                   f"{cella['stato']}): capitale {formatta_euro(cella['capitale_cents'])}, "
                   f"profitto del mese {formatta_euro(cella['profitto_mese_cents'], segno=True)}")
    if not riga["celle"]:
        out.append("- nessuno")
    movimenti = store.movimenti(cid)[-10:]
    if movimenti:
        out.append("Ultimi movimenti:")
        for m in movimenti:
            extra = " [stornato]" if m["stornato"] else (" [storno]" if m["storno_di"] else "")
            out.append(f"- {m['data']} {nomi_srv.get(int(m['servizio_id']), '?')}: {m['tipo']} "
                       f"{formatta_euro(m['importo_cents'])} (#{m['id']}){extra}")
    aperte = [r for r in store.proposte(cid) if r["stato"] in ("da_approvare", "inviata")]
    for r in aperte:
        out.append(f"Proposta aperta #{r['id']}: {r['tipo']} ({r['stato']}) — {r['motivo']}")
    for r in store.promemoria(solo_in_attesa=True):
        if r["cliente_id"] is not None and int(r["cliente_id"]) == cid:
            out.append(f"Promemoria #{r['id']} {_giorno_a_parole(str(r['quando']))}: {r['testo']}")
    out.append("Motore delle proposte: " + motore.spiega(store, cid))
    note = (store.cliente(cid) or {}).get("note")
    if note:
        out.append(f"Note: {note}")
    return "\n".join(out)


__all__ = ["CONSULTE", "AZIONI", "consulta", "prepara", "applica", "importi_nel_testo",
           "trova_cliente", "cerca_cliente", "trova_servizio"]
