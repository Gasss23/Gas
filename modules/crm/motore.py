"""Il CRM che «legge se stesso»: trova le opportunità e prepara il messaggio.

Ciclo (una «scansione», idempotente, deterministica, zero modelli e zero token):
  1. le proposte inviate da troppi giorni senza risposta diventano «senza_risposta»
     (contano per alzare il livello di insistenza della volta dopo);
  2. le proposte da approvare di clienti che non si possono più contattare (STOP, consenso
     tolto, cliente non attivo) diventano «superate»;
  3. per ogni cliente si decide la PROSSIMA MIGLIORE AZIONE, se c'è.

Quando un cliente è contattabile (tutte vere):
  * cliente attivo, consenso ai messaggi dato, nessuno STOP, numero WhatsApp presente;
  * ha già pagato almeno `pagamenti_min` commissioni («è contento»);
  * nessuna proposta già aperta (una alla volta: niente raffiche);
  * dall'ultimo messaggio sono passati almeno `pausa_giorni`, e negli ultimi 30 giorni
    ne ha ricevuti meno di `max_messaggi_30g`;
  * nel mese in corso o in quello prima ha fatto almeno `soglia_cents` di profitto.

Quale azione (in quest'ordine):
  * se di recente ha detto NO a un nuovo servizio → AUMENTO DI CAPITALE sul servizio che
    gli rende di più (regola dell'operatore: «non vuole un altro servizio? aumenta quello»);
  * altrimenti NUOVO SERVIZIO (cross-sell): tra quelli che non ha e a cui non ha detto no
    di recente, quello col miglior punteggio = commissione stimata + affinità («chi ha il
    suo servizio spesso prende anche questo»);
  * se ha da poco accettato qualcosa, prima la PRESENTAZIONE di un amico (referral);
  * se non resta altro: aumento di capitale, poi referral.

Insistenza crescente: livello = 1 + no/silenzi degli ultimi 90 giorni (massimo 3). Il
livello cambia il TONO del messaggio (più diretto), mai le regole sopra: STOP, consenso
e tetti valgono sempre.

L'invio NON lo fa il motore: la proposta nasce «da_approvare» e la conferma l'operatore
(principio del 19 ottobre: ciò che esce verso il mondo aspetta la firma).
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from modules.crm import analisi
from modules.crm.messaggi import componi
from modules.crm.store import CRMStore, ErroreCRM, formatta_euro_tondo

log = logging.getLogger(__name__)

ARROTONDA_CAPITALE_CENTS = 10_000  # i capitali suggeriti si arrotondano a 100 €


def _env_int(nome: str, default: int, minimo: int = 0, massimo: int = 10**12) -> int:
    grezzo = os.environ.get(nome, "").strip()
    if not grezzo:
        return default
    try:
        v = int(grezzo)
    except ValueError:
        log.warning("CRM: %s=%r non è un intero: uso %d", nome, grezzo[:20], default)
        return default
    if not minimo <= v <= massimo:
        log.warning("CRM: %s=%d fuori dai limiti (%d…%d): uso %d", nome, v, minimo, massimo, default)
        return default
    return v


@dataclass(frozen=True)
class Regole:
    soglia_cents: int = 100_000          # 1.000 € di profitto nel mese
    pagamenti_min: int = 1               # commissioni già pagate per essere «contento»
    pausa_giorni: int = 7                # giorni minimi tra due messaggi
    max_messaggi_30g: int = 4            # tetto messaggi in 30 giorni
    pausa_dopo_no_giorni: int = 30       # dopo un no, quello stesso obiettivo si ripropone tra…
    attesa_risposta_giorni: int = 5      # inviata da più di… senza esito → senza_risposta
    aumento_pct: int = 50                # aumento di capitale suggerito, % del capitale
    referral_giorni: int = 60            # al massimo una richiesta di presentazione ogni…
    finestra_insistenza_giorni: int = 90

    @classmethod
    def da_env(cls) -> "Regole":
        return cls(
            soglia_cents=_env_int("GAS_CRM_SOGLIA_EURO", 1000, 0, 10**9) * 100,
            pagamenti_min=_env_int("GAS_CRM_PAGAMENTI_MIN", 1, 0, 1000),
            pausa_giorni=_env_int("GAS_CRM_PAUSA_GIORNI", 7, 1, 365),
            max_messaggi_30g=_env_int("GAS_CRM_MAX_MESSAGGI_30G", 4, 1, 30),
            pausa_dopo_no_giorni=_env_int("GAS_CRM_PAUSA_DOPO_NO_GIORNI", 30, 1, 3650),
            attesa_risposta_giorni=_env_int("GAS_CRM_ATTESA_RISPOSTA_GIORNI", 5, 1, 90),
            aumento_pct=_env_int("GAS_CRM_AUMENTO_PCT", 50, 1, 1000),
            referral_giorni=_env_int("GAS_CRM_REFERRAL_GIORNI", 60, 1, 3650),
        )


@dataclass
class Azione:
    tipo: str
    livello: int
    motivo: str
    messaggio: str
    valore_stimato_cents: int
    servizio_id: Optional[int] = None
    posizione_id: Optional[int] = None


@dataclass
class Decisione:
    azione: Optional[Azione] = None
    esclusione: Optional[str] = None


@dataclass
class EsitoScansione:
    create: List[int] = field(default_factory=list)
    superate: List[int] = field(default_factory=list)
    senza_risposta: List[int] = field(default_factory=list)
    esclusi: Dict[int, str] = field(default_factory=dict)
    valore_nuovo_cents: int = 0
    errore: Optional[str] = None

    def come_dict(self) -> Dict[str, Any]:
        return {"create": self.create, "superate": self.superate,
                "senza_risposta": self.senza_risposta,
                "esclusi": {str(k): v for k, v in self.esclusi.items()},
                "valore_nuovo_cents": self.valore_nuovo_cents, "errore": self.errore}


def _giorno(ts: Optional[str]) -> Optional[date]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts)).date()
    except ValueError:
        try:
            return date.fromisoformat(str(ts)[:10])
        except ValueError:
            return None


def _arrotonda_su(cents: int, passo: int = ARROTONDA_CAPITALE_CENTS) -> int:
    return -(-cents // passo) * passo if cents > 0 else 0


def motivo_non_contattabile(cliente: Dict[str, Any]) -> Optional[str]:
    """Motivo «duro» per cui un cliente non va contattato, o None."""
    if cliente.get("stato") != "attivo":
        return "cliente non attivo"
    if cliente.get("opt_out"):
        return "ha chiesto STOP ai messaggi"
    if not cliente.get("consenso_marketing"):
        return "manca il consenso ai messaggi promozionali"
    if not cliente.get("telefono"):
        return "manca il numero WhatsApp"
    return None


def valuta_cliente(d: analisi.Dati, cliente_id: int, regole: Regole,
                   affinita: Optional[Dict[Tuple[int, int], int]] = None) -> Decisione:
    """Decide la prossima migliore azione per un cliente. Funzione PURA (niente DB)."""
    cliente = d.clienti[cliente_id]
    duro = motivo_non_contattabile(cliente)
    if duro:
        return Decisione(esclusione=duro)
    m = analisi.metriche_cliente(d, cliente_id)
    if m.pagamenti < regole.pagamenti_min:
        return Decisione(esclusione="non ha ancora pagato la prima commissione")

    oggi = d.oggi
    sue = [p for p in d.proposte if int(p["cliente_id"]) == cliente_id]
    if any(p["stato"] in ("da_approvare", "inviata") for p in sue):
        return Decisione(esclusione="ha già una proposta aperta")
    invii = [g for g in (_giorno(p.get("inviata_il")) for p in sue) if g is not None]
    if invii:
        ultimo = max(invii)
        if (oggi - ultimo).days < regole.pausa_giorni:
            return Decisione(esclusione=f"ultimo messaggio {(oggi - ultimo).days} giorni fa "
                                        f"(pausa minima {regole.pausa_giorni})")
        recenti = sum(1 for g in invii if (oggi - g).days < 30)
        if recenti >= regole.max_messaggi_30g:
            return Decisione(esclusione=f"già {recenti} messaggi negli ultimi 30 giorni")

    mese = d.mese
    if m.profitto_mese_cents >= regole.soglia_cents and m.profitto_mese_cents >= m.profitto_mese_prec_cents:
        rif_mese, rif_profitto = mese, m.profitto_mese_cents
    elif m.profitto_mese_prec_cents >= regole.soglia_cents:
        rif_mese, rif_profitto = analisi.mese_precedente(mese), m.profitto_mese_prec_cents
    elif m.profitto_mese_cents >= regole.soglia_cents:
        rif_mese, rif_profitto = mese, m.profitto_mese_cents
    else:
        migliore = max(m.profitto_mese_cents, m.profitto_mese_prec_cents)
        return Decisione(esclusione=f"profitto del mese {formatta_euro_tondo(migliore)}, "
                                    f"sotto la soglia di {formatta_euro_tondo(regole.soglia_cents)}")
    mese_label = analisi.etichetta_mese(rif_mese)
    in_corso = rif_mese == mese

    def _entro(p: Dict[str, Any], giorni: int) -> bool:
        g = _giorno(p.get("esito_il"))
        return g is not None and (oggi - g).days < giorni

    negativi = [p for p in sue if p["stato"] in ("rifiutata", "senza_risposta")
                and _entro(p, regole.finestra_insistenza_giorni)]
    livello = min(1 + len(negativi), 3)

    attive = [p for p in m.posizioni if p.stato == "attiva"]
    # servizio che gli rende di più nel mese di riferimento (citato nel messaggio)
    attuale = max(attive, key=lambda p: (p.profitto_per_mese.get(rif_mese, 0), -p.id), default=None)
    nome_attuale = str(d.servizi[attuale.servizio_id]["nome"]) if attuale else None
    profitto_msg = attuale.profitto_per_mese.get(rif_mese, 0) if attuale else rif_profitto
    if profitto_msg <= 0:
        profitto_msg = rif_profitto
    base_motivo = (f"{mese_label}: +{formatta_euro_tondo(rif_profitto)} di profitto "
                   f"(soglia {formatta_euro_tondo(regole.soglia_cents)}); "
                   f"servizi attivi {len(attive)} su {sum(1 for s in d.servizi.values() if s['attivo'])}")

    no_recente_cross = any(p["tipo"] == "cross_sell" and p["stato"] == "rifiutata"
                           and _entro(p, regole.pausa_dopo_no_giorni) for p in sue)
    accettata_recente = any(p["stato"] == "accettata" and _entro(p, 30) for p in sue)
    referral_recente = any(p["tipo"] == "referral" and p["stato"] != "scartata"
                           and (oggi - (_giorno(p.get("creata_il")) or date.min)).days
                           < regole.referral_giorni for p in sue)

    def _bloccato(tipo: str, servizio_id: Optional[int] = None,
                  posizione_id: Optional[int] = None) -> bool:
        """Stesso obiettivo rifiutato/ignorato di recente, o accettato da poco."""
        for p in sue:
            if p["tipo"] != tipo:
                continue
            if servizio_id is not None and p["servizio_id"] != servizio_id:
                continue
            if posizione_id is not None and p["posizione_id"] != posizione_id:
                continue
            if p["stato"] in ("rifiutata", "senza_risposta") and _entro(p, regole.pausa_dopo_no_giorni):
                return True
            if p["stato"] == "accettata" and _entro(p, 30):
                return True
        return False

    def _cross() -> Optional[Azione]:
        posseduti = {p.servizio_id for p in m.posizioni if p.stato != "chiusa"}
        capitali = [p.capitale_cents for p in attive if p.capitale_cents > 0]
        medio = sum(capitali) // len(capitali) if capitali else 0
        aff = affinita or {}
        candidati = []
        for s in d.servizi.values():
            sid = int(s["id"])
            if not s["attivo"] or sid in posseduti or _bloccato("cross_sell", servizio_id=sid):
                continue
            capitale = max(int(s["capitale_minimo_cents"]), _arrotonda_su(medio // 2))
            roi, fonte = analisi.roi_atteso_bp(d, sid)
            stima = analisi.commissione_stimata_cents(s, capitale, roi)
            legame = max((aff.get((a, sid), 0) for a in posseduti), default=0)
            # punteggio: commissione stimata, +fino al 50% se è un abbinamento frequente
            punteggio = stima + analisi.div_tonda(stima * legame, 20_000)
            candidati.append((punteggio, -int(s["priorita"]), -sid, s, stima, legame, fonte))
        if not candidati:
            return None
        candidati.sort(reverse=True)
        _, _, _, s, stima, legame, fonte = candidati[0]
        motivo = f"{base_motivo}. Proponi «{s['nome']}»: ~{formatta_euro_tondo(stima)}/mese di commissioni ({fonte})"
        if legame:
            motivo += f"; lo ha il {analisi.div_tonda(legame, 100)}% di chi ha i suoi servizi"
        return Azione(
            tipo="cross_sell", livello=livello, motivo=motivo, valore_stimato_cents=stima,
            servizio_id=int(s["id"]),
            messaggio=componi("cross_sell", livello, str(cliente["nome"]), mese_label,
                              profitto_msg, servizio_nuovo=str(s["nome"]),
                              servizio_attuale=nome_attuale, mese_in_corso=in_corso),
        )

    def _aumento() -> Optional[Azione]:
        candidati = []
        for p in attive:
            if p.capitale_cents <= 0 or _bloccato("aumento_capitale", posizione_id=p.id):
                continue
            roi = analisi.roi_posizione_bp(p, mese)
            if roi is None or roi <= 0:
                continue
            candidati.append((roi, -p.id, p))
        if not candidati:
            return None
        candidati.sort(reverse=True)
        roi, _, p = candidati[0]
        s = d.servizi[p.servizio_id]
        delta = _arrotonda_su(analisi.div_tonda(p.capitale_cents * regole.aumento_pct, 100))
        stima = analisi.commissione_stimata_cents(s, delta, roi)
        motivo = (f"{base_motivo}. Aumento di {formatta_euro_tondo(delta)} su «{s['nome']}» "
                  f"(rende {analisi.formatta_bp(roi)} al mese): "
                  f"~{formatta_euro_tondo(stima)}/mese di commissioni")
        if no_recente_cross:
            motivo += "; ha detto no a un nuovo servizio, quindi si punta su quello che ha"
        return Azione(
            tipo="aumento_capitale", livello=livello, motivo=motivo, valore_stimato_cents=stima,
            servizio_id=p.servizio_id, posizione_id=p.id,
            messaggio=componi("aumento_capitale", livello, str(cliente["nome"]), mese_label,
                              p.profitto_per_mese.get(rif_mese, 0) or profitto_msg,
                              servizio_attuale=str(s["nome"]), aumento_cents=delta,
                              mese_in_corso=in_corso),
        )

    def _referral() -> Optional[Azione]:
        if referral_recente or _bloccato("referral"):
            return None
        paganti = [analisi.metriche_cliente(d, cid) for cid in d.clienti]
        paganti = [x for x in paganti if x.pagamenti > 0]
        mesi3 = [analisi.mese_precedente(mese, k) for k in range(1, 4)]
        tot = sum(p.commissioni_per_mese.get(x, 0) for p in d.posizioni.values() for x in mesi3)
        stima = analisi.div_tonda(tot, 3 * len(paganti)) if paganti else 0
        motivo = (f"{base_motivo}. Chiedi una presentazione: un cliente nuovo vale "
                  f"~{formatta_euro_tondo(stima)}/mese di commissioni (media degli ultimi 3 mesi)")
        return Azione(
            tipo="referral", livello=livello, motivo=motivo, valore_stimato_cents=stima,
            messaggio=componi("referral", livello, str(cliente["nome"]), mese_label, profitto_msg,
                              mese_in_corso=in_corso),
        )

    ordine: Tuple[Callable[[], Optional[Azione]], ...]
    if no_recente_cross:
        ordine = (_aumento, _referral)
    elif accettata_recente:
        ordine = (_referral, _cross, _aumento)
    else:
        ordine = (_cross, _aumento, _referral)
    for scelta in ordine:
        azione = scelta()
        if azione is not None:
            return Decisione(azione=azione)
    return Decisione(esclusione="nessuna proposta adatta (servizi già proposti o rifiutati di recente)")


def scansiona(store: CRMStore, oggi: Optional[date] = None,
              regole: Optional[Regole] = None, autore: str = "motore") -> EsitoScansione:
    """Una scansione completa. Non solleva: gli errori finiscono in `errore` e nel log."""
    esito = EsitoScansione()
    reg = regole or Regole.da_env()
    giorno = oggi or store.oggi()
    foto = store.fotografia()
    if foto is None:
        esito.errore = "database non disponibile"
        return esito
    d = analisi.costruisci(foto, giorno)

    # 1. inviate senza esito da troppo → senza_risposta
    for p in d.proposte:
        g = _giorno(p.get("inviata_il"))
        if p["stato"] == "inviata" and g is not None and (giorno - g).days >= reg.attesa_risposta_giorni:
            try:
                store.transiziona_proposta(int(p["id"]), "senza_risposta", autore=autore)
                esito.senza_risposta.append(int(p["id"]))
            except ErroreCRM as e:
                log.warning("CRM: proposta %s non chiusa: %s", p["id"], e)
    # 2. da approvare di clienti non più contattabili → superata
    for p in d.proposte:
        if p["stato"] != "da_approvare":
            continue
        cliente = d.clienti.get(int(p["cliente_id"]))
        if cliente is not None and motivo_non_contattabile(cliente):
            try:
                store.transiziona_proposta(int(p["id"]), "superata", autore=autore)
                esito.superate.append(int(p["id"]))
            except ErroreCRM as e:
                log.warning("CRM: proposta %s non superata: %s", p["id"], e)
    if esito.senza_risposta or esito.superate:
        foto = store.fotografia()
        if foto is None:
            esito.errore = "database non disponibile"
            return esito
        d = analisi.costruisci(foto, giorno)

    # 3. prossima migliore azione per cliente
    aff = analisi.affinita_bp(d)
    for cid in sorted(d.clienti):
        try:
            dec = valuta_cliente(d, cid, reg, aff)
        except Exception as e:  # un cliente con dati strani non ferma gli altri (§9)
            log.warning("CRM: valutazione del cliente %s fallita: %s", cid, e)
            esito.esclusi[cid] = "errore nella valutazione (vedi gas_debug.log)"
            continue
        if dec.azione is None:
            esito.esclusi[cid] = dec.esclusione or "nessuna azione"
            continue
        a = dec.azione
        try:
            # chiave = cliente: al massimo UNA proposta aperta per cliente anche con due
            # scansioni concorrenti (indice unico parziale sul DB)
            nuovo = store.crea_proposta(
                cliente_id=cid, tipo=a.tipo, chiave=f"cliente:{cid}", motivo=a.motivo,
                messaggio=a.messaggio, valore_stimato_cents=a.valore_stimato_cents,
                livello=a.livello, servizio_id=a.servizio_id, posizione_id=a.posizione_id,
                autore=autore,
            )
        except ErroreCRM as e:
            log.warning("CRM: proposta per il cliente %s non creata: %s", cid, e)
            esito.esclusi[cid] = f"proposta non salvata: {e}"
            continue
        if nuovo is not None:
            esito.create.append(nuovo)
            esito.valore_nuovo_cents += a.valore_stimato_cents
    return esito


def spiega(store: CRMStore, cliente_id: int, oggi: Optional[date] = None,
           regole: Optional[Regole] = None) -> str:
    """Perché il motore farebbe (o non farebbe) qualcosa con questo cliente, a parole.
    Sola lettura: non crea proposte."""
    foto = store.fotografia()
    if foto is None:
        return "database non disponibile"
    d = analisi.costruisci(foto, oggi or store.oggi())
    if cliente_id not in d.clienti:
        return "cliente inesistente"
    dec = valuta_cliente(d, cliente_id, regole or Regole.da_env(), analisi.affinita_bp(d))
    if dec.azione is None:
        return f"Nessuna proposta ora: {dec.esclusione}."
    return f"Proposta pronta ({dec.azione.tipo}, livello {dec.azione.livello}): {dec.azione.motivo}."


__all__ = ["Regole", "Azione", "Decisione", "EsitoScansione", "valuta_cliente", "scansiona",
           "spiega", "motivo_non_contattabile"]
