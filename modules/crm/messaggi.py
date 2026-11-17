"""Testi WhatsApp delle proposte e link wa.me — deterministici, zero modelli.

Perché senza modello: i messaggi contengono nome e guadagni del cliente, e la regola dei
modelli (19 ottobre) vuole i dati dei clienti solo sui modelli forti. Un modello di testo
fisso non manda nulla a nessuno, costa zero e non inventa numeri.

Regole dei testi (anche per chi li modificherà):
  * mai promettere guadagni futuri: si citano solo i risultati GIÀ ottenuti dal cliente,
    seguiti dalla nota sul rischio (`GAS_CRM_NOTA_RISCHIO`, vuota = niente nota);
  * niente urgenza finta («ultimi posti», «solo oggi»): il livello 3 è più DIRETTO
    (chiede una chiamata), non più ingannevole;
  * sempre la riga per dire STOP: chi la scrive non riceve più nulla (il motore lo
    rispetta, vedi `opt_out`).
"""
from __future__ import annotations

import os
import re
from typing import Dict, Optional
from urllib.parse import quote

from modules.crm.store import formatta_euro_tondo

NOTA_RISCHIO_DEFAULT = "I risultati passati non garantiscono quelli futuri."
RIGA_STOP = "Se preferisci non ricevere più proposte, rispondi STOP."

# {tipo: {livello: testo}}. Segnaposto: {nome} {periodo} («a ottobre» / «questo mese»)
# {risultato} («hai chiuso a +1.234 €» / «sei già a +1.234 €») {profitto} («+1.234 €»)
# {servizio_nuovo} {servizio_attuale} {aumento}
_TESTI: Dict[str, Dict[int, str]] = {
    "cross_sell": {
        1: ("Ciao {nome}! 👋 Complimenti: {periodo} con {servizio_attuale} {risultato}. "
            "Visto che ti stai trovando bene, ti va se ti racconto in 5 minuti come funziona "
            "anche {servizio_nuovo}? È il modo più semplice per diversificare."),
        2: ("Ciao {nome}, ti riscrivo perché {periodo} {risultato} 💪 Secondo me è il "
            "momento giusto per affiancare {servizio_nuovo} a {servizio_attuale}: ti preparo "
            "un riepilogo con capitale di partenza e come lavora. Te lo mando qui?"),
        3: ("{nome}, ti rubo un minuto: i tuoi numeri parlano chiaro ({profitto} {periodo}). "
            "Ci sentiamo 10 minuti questa settimana per capire se {servizio_nuovo} fa per te? "
            "Dimmi tu giorno e ora e ti chiamo io."),
    },
    "aumento_capitale": {
        1: ("Ciao {nome}! 🚀 Con {servizio_attuale} {periodo} {risultato}. Hai mai pensato "
            "di aumentare il capitale su quello che già ti sta funzionando? Se vuoi ti faccio "
            "vedere come cambierebbe con {aumento} in più."),
        2: ("Ciao {nome}, {servizio_attuale} sta andando bene ({profitto} {periodo}). "
            "Valutiamo insieme un aumento di {aumento}? Ti preparo due conti chiari, senza "
            "impegno."),
        3: ("{nome}, parliamoci chiaro: {servizio_attuale} per te funziona ({profitto} "
            "{periodo}). Ti va una chiamata di 10 minuti per decidere se aumentare di "
            "{aumento}? Dimmi tu quando."),
    },
    "referral": {
        1: ("Ciao {nome}! 🙌 Sono contento che le cose vadano bene ({profitto} {periodo}). "
            "Hai un amico o un collega a cui potrebbe interessare? Se me lo presenti lo "
            "seguo io personalmente, come faccio con te."),
        2: ("Ciao {nome}, una domanda veloce: conosci qualcuno che vorrebbe iniziare come "
            "hai fatto tu? Mandami pure il suo contatto qui, lo chiamo io con calma."),
        3: ("{nome}, ti chiedo un favore: se pensi a una persona a cui farebbe comodo quello "
            "che stai facendo tu, presentamela. Basta il nome e il numero, al resto penso io."),
    },
}


def nota_rischio() -> str:
    """Nota sul rischio in coda ai messaggi con numeri. Variabile assente → default;
    variabile presente ma vuota → nessuna nota (scelta esplicita dell'operatore)."""
    v = os.environ.get("GAS_CRM_NOTA_RISCHIO")
    return NOTA_RISCHIO_DEFAULT if v is None else v.strip()[:200]


def nome_breve(nome: str) -> str:
    """«Mario Rossi» → «Mario»; nome vuoto → stringa vuota."""
    parti = (nome or "").strip().split()
    return parti[0] if parti else ""


def periodo(mese_label: str, in_corso: bool) -> str:
    """«ottobre 2026» → «a ottobre» («ad aprile», «ad agosto»); mese in corso → «questo mese»."""
    if in_corso or not mese_label:
        return "questo mese"
    mese = mese_label.split(" ")[0]
    return ("ad " if mese.startswith("a") else "a ") + mese


def componi(tipo: str, livello: int, nome: str, mese_label: str, profitto_cents: int,
            servizio_nuovo: Optional[str] = None, servizio_attuale: Optional[str] = None,
            aumento_cents: Optional[int] = None, mese_in_corso: bool = False) -> str:
    """Testo del messaggio per (tipo, livello). Il mese in corso non è «chiuso»: si dice
    «questo mese sei già a…». Solleva KeyError su tipo sconosciuto."""
    liv = min(max(int(livello), 1), 3)
    modello = _TESTI[tipo][liv]
    profitto = "+" + formatta_euro_tondo(profitto_cents)
    corpo = modello.format(
        nome=nome_breve(nome) or "ciao",
        periodo=periodo(mese_label, mese_in_corso),
        risultato=("sei già a " if mese_in_corso else "hai chiuso a ") + profitto,
        profitto=profitto,
        servizio_nuovo=servizio_nuovo or "un nuovo servizio",
        servizio_attuale=servizio_attuale or "il tuo servizio",
        aumento=formatta_euro_tondo(aumento_cents or 0),
    )
    righe = [corpo]
    nota = nota_rischio()
    if nota:
        righe.append(nota)
    righe.append(RIGA_STOP)
    return "\n\n".join(righe)


def link_whatsapp(telefono: Optional[str], testo: str) -> Optional[str]:
    """Link che apre WhatsApp sul numero col messaggio già scritto: l'operatore lo rilegge
    e preme invio. None se il numero manca o non è in formato internazionale."""
    if not telefono or not re.fullmatch(r"\+[0-9]{8,15}", telefono):  # cifre ASCII (R-803-6)
        return None
    return f"https://wa.me/{telefono[1:]}?text={quote(testo, safe='')}"
