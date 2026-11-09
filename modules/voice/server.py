"""
HTTP voice endpoint per GAS — FASE 3, Fette 1+2+3.

Endpoint: POST /voice
  Body (testo):  JSON {"prompt": "<testo>"}
  Body (audio):  Content-Type audio/* oppure multipart/form-data con campo 'file'
  Auth:    Header "Authorization: Bearer <token>"

  Output testo (default):
    200:   JSON {"content": "<risposta>"}

  Output audio (se Accept: audio/mpeg o Accept: audio/*):
    200:   byte MP3 grezzi (Content-Type: audio/mpeg)
    502:   JSON {"error": "<msg>"}  — errore ElevenLabs (rete/quota)
    503:   JSON {"error": "<msg>"}  — TTS non disponibile (ELEVENLABS_API_KEY assente)

  Codici errore comuni:
    400:   JSON {"error": "<msg>"}  — prompt mancante/JSON invalido / audio vuoto o invalido
    401:   JSON {"error": "Unauthorized"}
    502:   JSON {"error": "<msg>"}  — errore Groq STT o ElevenLabs TTS (rete/quota)
    503:   JSON {"error": "<msg>"}  — STT/TTS non disponibile (chiave assente)
    500:   JSON {"error": "<msg>"}  — errore pipeline o kernel

Endpoint: GET /voce/conferma (V14, stesso Bearer)
  200: audio/mpeg di «Sì, signore?» con la voce attuale (ELEVENLABS_VOICE_ID), in cache per
       voce: un solo giro su ElevenLabs finché la voce non cambia. 503 senza chiave
       ElevenLabs, 502 se ElevenLabs fallisce: il client suona il bip.

Avvio: `python -m modules.voice.server` dalla cartella di Gas (carica il `.env` come la CLI).

Configurazione tramite variabili d'ambiente (da .env o export):
  GAS_VOICE_BIND      — bind address       (default: 127.0.0.1); fuori da 127.0.0.1 il server
                        parte SOLO con GAS_VOICE_RETE_PRIVATA=1 (tunnel privato dichiarato, R8)
                        e mai su tutte le interfacce («::» o equivalente IPv4); fuori da 127.0.0.1
                        solo un indirizzo IPv4 scritto per intero, mai un nome host né IPv6;
                        «localhost» vale come locale (dipende da /etc/hosts del computer)
  GAS_VOICE_MAX_FALLITI — tentativi con token sbagliato per IP in 10 minuti (default 10), poi
                        429 per 15 minuti a quell'IP, anche col token giusto (R8)
  GAS_VOICE_MAX_TESTO_ORA — richieste a TESTO al massimo nell'ultima ora (default 120), poi 429 (R8)
  GAS_VOICE_PORT      — porta TCP          (default: 8765)
  GAS_VOICE_TOKEN     — token bearer       OBBLIGATORIO: assente/vuoto → il server non parte
  GROQ_API_KEY        — chiave Groq        OBBLIGATORIO per STT audio; assente → 503
  ELEVENLABS_API_KEY  — chiave ElevenLabs  OBBLIGATORIO per output audio; assente → 503
  ELEVENLABS_VOICE_ID — voice id           (default: JBFqnCBsd6RMkjVDRZzb, George premade)
  GAS_VOICE_MAX_TURNI_ORA — richieste PARLATE al massimo nell'ultima ora (default 60), poi
                        429; conta ogni chiamata alla trascrizione (Groq) e, dalla V12, ogni
                        richiesta a testo che chiede la risposta a voce (sintesi ElevenLabs)
  GAS_VOCE_FORTE      — 1/true/on/yes/si/sì: ogni richiesta della voce va al solo cervello
                        forte (default spento; forte fermo → errore dichiarato, mai i gratuiti)
  GAS_VOICE_STT_LOGPROB_MIN / GAS_VOICE_STT_NO_SPEECH_MAX — soglie della trascrizione
                        incerta (default -1.0 / 0.8): sotto/sopra → «Non ho capito bene, puoi
                        ripetere?» senza turno (V6). Risposte 200 della voce con il campo
                        "capito" = testo trascritto, mostrato dalla pagina.
  GAS_VOICE_STT_ECO_NO_SPEECH — soglia (default 0.9) oltre la quale un'eco corta del
                        prompt di Whisper (2-3 parole contigue, es. «Gas, forte, lead.») è
                        scartata come silenzio; i comandi brevi detti davvero stanno sotto.

Cervello forte dalla voce (V1, chat M2): «/forte <richiesta>» (testo) oppure, nel parlato
trascritto, «forte <richiesta>» / «Gas forte <richiesta>» all'inizio della frase.
«forte» parlato senza richiesta → 200 con l'istruzione d'uso da ascoltare (nessun turno);
«/forte» scritto senza richiesta → 400.

Sicurezza:
  - Nasce chiuso su 127.0.0.1. Aprire all'esterno SOLO settando GAS_VOICE_BIND.
  - Confronto token a TEMPO COSTANTE via hmac.compare_digest (mai ==).
  - Nessun segreto scritto nei log; ogni tentativo fallito viene loggato con IP + esito.
  - I byte audio (ingresso e uscita) non vengono loggati né scritti su disco; le chiavi non compaiono nei log.
  - CAVEAT PRIVACY (STT): l'audio dell'utente viene inviato ai server Groq (terza parte).
  - CAVEAT PRIVACY (TTS): il testo del kernel viene inviato ai server ElevenLabs (terza parte).
    Trade-off dichiarato: per un agente che tocca dati/lead, questo è egress di dati.
  - Kernel GasKernel istanziato UNA VOLTA all'avvio (stateful, storia condivisa).
  - Single-thread nativo: http.server.HTTPServer senza ThreadingMixIn, nessun lock.
  - Fail-safe §9: eccezione in run_turn → 500 + log in gas_debug.log, server vivo.
"""
from __future__ import annotations

import base64
import hmac
import ipaddress
import http.client
import json
import logging
import os
import re
import subprocess
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from modules.voice.stt import GroqSTTError, TrascrizioneIncerta, parse_audio_body, transcribe_audio
from modules.voice.tts import DEFAULT_VOICE_ID as _TTS_DEFAULT_VOICE_ID
from modules.voice.tts import (ElevenLabsTTSError, add_shared_voice, list_shared_voices,
                               list_voices, synthesize_speech)
from modules.voice import prova_voci

log = logging.getLogger(__name__)
# V7 (R-614-3-M2): i tempi sono informazione, non un problema: logger dedicato a INFO, che
# finisce nel file gas_debug.log (il terminale resta a WARNING; i tempi sono già nella pagina).
_log_tempi = logging.getLogger("gas.voce.tempi")
_log_tempi.setLevel(logging.INFO)

_ENDPOINT = "/voice"

# V1 (chat M2): la barra di «/forte» non si detta e Whisper scrive «Forte, …»: la parola
# «forte» all'inizio del parlato (anche dopo «Gas», o «Gus» come lo trascrive Whisper)
# vale «/forte», anche dopo un saluto prima di «Gas» («Ehi Gas, forte …», V-2 ve #304).
# Parola intera: «fortemente…» o «forte» a metà frase restano testo normale. Limiti
# dichiarati: «Forte!» esclamazione, «forte-forte», «forte: …» vanno al forte (direzione
# sicura, costa budget: R-564-1-M2, V-1 ve #304); «Gas e forte …» o un saluto non in
# elenco restano normali (con GAS_VOCE_FORTE=1 vanno comunque al forte).
_PAROLA_FORTE = re.compile(
    r"^[^\w/]*(?:(?:(?:ehi|ehy|hey|ok|okay|ciao|senti)\W+)?(?:gas|gus)\b\W*)?forte(?!\w)(.*)$",
    re.IGNORECASE | re.DOTALL)
_USO_FORTE = "Uso: /forte <richiesta> (a voce: «forte <richiesta>»)"
# V2 (V-2 ve #304): a chi PARLA l'istruzione d'uso arriva come risposta da ascoltare
# (200, sintetizzata se il client vuole audio), non come errore 400. Nessun turno parte.
_USO_FORTE_PARLATO = ("Dopo «forte» dimmi cosa fare, per esempio: «Gas, forte: riassumi i lead "
                      "di oggi». Non ho avviato nessun lavoro.")
# V6: trascrizione incerta (stt.TrascrizioneIncerta) → si chiede di ripetere, nessun turno
_NON_HO_CAPITO = "Non ho capito bene, puoi ripetere?"
# V13 (prova sul Mac del 5 nov): «Hey Jarvis!» detto dentro la finestra d'ascolto arrivava
# al cervello come richiesta. Una trascrizione fatta SOLO della parola di attivazione (con
# un saluto e la punteggiatura) riceve una risposta fissa, senza turno.
# V14: niente «ok/okay» fra i saluti (V-1 bot #334: «Ok Gas.» può essere la conferma a una
# domanda di Gas e deve arrivare al cervello); la parola ripetuta («Hey Jarvis, Hey Jarvis»,
# Whisper la raddoppia spesso) vale ancora come sola attivazione (R-668-2-M2).
_ATTIVAZIONE_UNA = r"(?:(?:ehi|ehy|hey|ei|ciao)\W+)?(?:jarvis|gas|gus)"
_SOLO_ATTIVAZIONE = re.compile(
    rf"^[^\w]*{_ATTIVAZIONE_UNA}(?:\W+{_ATTIVAZIONE_UNA})*[^\w]*$", re.IGNORECASE)
_RISPOSTA_ATTIVAZIONE = "Dimmi."
# V15 (contratto dell'operatore via M1, 5 nov, lato client la chat Mani): una trascrizione
# PARLATA fatta solo di «pausa», «standby» o «basta così» (anche con la parola di attivazione
# davanti, stessa normalizzazione del filtro «Dimmi.») non va al cervello: risposta fissa
# breve e intestazione «X-Gas-Comando: pausa»; il client chiude la conversazione e torna ad
# aspettare «Hey Jarvis» (non è uno standby profondo).
_SOLO_PAUSA = re.compile(
    rf"^[^\w]*(?:{_ATTIVAZIONE_UNA}\W+)*(?:pausa|stand[\s-]*by|basta(?:\s+cos[iì])?)[^\w]*$",
    re.IGNORECASE)
RISPOSTA_PAUSA = "Va bene."
COMANDO_PAUSA = "pausa"
# V15: «X-Gas-Seguito: 1» = turno nella finestra di conversazione, SENZA parola di
# attivazione (il client lo dice). Il cervello decide prima se il parlato è rivolto a Gas;
# se no (persone che parlano fra loro, TV) risponde solo col segno fisso: niente voce,
# niente testo al client, «X-Gas-Comando: fine» (il client chiude la conversazione).
SEGNO_NON_PER_ME = "[NON_PER_ME]"
COMANDO_FINE = "fine"
# V15 (V-1 bot #339, sì di M1): nel seguito il forte ha chiesto uno strumento (che non c'è):
# invece di chiudere in silenzio Gas dice come ottenere l'azione.
RISPOSTA_SERVE_ATTIVAZIONE = "Per farlo ripetimelo dicendo prima Hey Jarvis."
# R-675-3-M2: anche le varianti senza parentesi o in minuscolo («NON_PER_ME», «non per me»),
# ma solo se la risposta è SOLO il segno: «Non per me è un problema, …» resta una risposta.
# V-2 ve #339: il segno esatto con le parentesi vale anche se il modello aggiunge altro dopo
# («[NON_PER_ME] (parlato fra persone)»): quel testo non va letto ad alta voce.
# V-2 bot #339 su be60a21 (sì dell'operatore via M1): nel seguito il segno tra parentesi
# chiude OVUNQUE stia («Non è rivolto a me [NON_PER_ME] (era la TV).»), anche scritto con
# spazi («[NON PER ME]», R-676-1-M2): quel testo non va mai letto ad alta voce. Le forme
# senza parentesi valgono solo come risposta intera.
_NON_PER_ME = re.compile(
    r"\[\s*non[_\s-]+per[_\s-]+me\s*\]|^\W*non[_\s-]+per[_\s-]+me\W*$", re.IGNORECASE)
ISTRUZIONE_SEGUITO = (
    "Questa frase è stata captata dal microfono nella finestra di conversazione, SENZA che "
    "l'operatore dicesse la parola di attivazione: può essere rivolta a te oppure no "
    "(persone che parlano fra loro, la TV, una telefonata). Se NON è chiaramente rivolta a "
    f"te, rispondi SOLO con {SEGNO_NON_PER_ME} e nient'altro, senza usare strumenti. "
    "Se è rivolta a te, rispondi normalmente, ma sappi che in questo turno NON hai "
    "strumenti: se ti chiede un'azione (scrivere, salvare, cercare, ricordare) non dire mai "
    "di averla fatta; rispondi che per farla deve ripeterla dicendo prima la parola di "
    "attivazione.")
# V14 (chat M2, «Sì, signore?» deciso dall'operatore; contratto con la chat Mani via M1):
# GET /voce/conferma → audio/mpeg della frase detta con la voce attuale, suonato dal client
# H24 al posto del bip dopo la parola di attivazione. In cache in memoria: un solo giro su
# ElevenLabs per voce (la chiave della cache contiene l'id della voce, quindi se la voce
# cambia si rigenera). ElevenLabs assente o in errore → 503/502 pulito, il client usa il bip.
_ENDPOINT_CONFERMA = "/voce/conferma"
CONFERMA_TIMEOUT_S = 5.0  # V15 (V-2 bot #335): la conferma non può tenere il server 30 s
CONFERMA_PAUSA_ERRORE_S = 60.0
FRASE_CONFERMA = "Sì, signore?"


# V3 (chat M2): con «X-Gas-Formato: audio+testo» (pagina del browser) la risposta è JSON
# con il testo intero (a schermo) e l'audio della sola parte parlata, corta: le prime
# frasi, entro _PARLATO_MAX_CHAR. Il resto si legge.
_FORMATO_AUDIO_TESTO = "audio+testo"
# V7b (chat M2): come «audio+testo», ma la risposta arriva a righe JSON (NDJSON) mentre la
# voce viene sintetizzata frase per frase: la pagina comincia a parlare dopo la prima frase.
_FORMATO_PEZZI = "audio+testo+pezzi"
# V10 (chat M2, «voce senza schermo»): per il client H24 del Mac (clients/voice/ascolto.py),
# che non ha uno schermo. Stesse righe NDJSON di _FORMATO_PEZZI, ma il turno usa
# ISTRUZIONE_VOCE (niente dettaglio da leggere) e si dice TUTTA la risposta divisa in frasi,
# entro _PARLATO_VOCE_MAX_CHAR, senza «Il resto è a schermo».
_FORMATO_PEZZI_VOCE = "audio+pezzi"
_PARLATO_VOCE_MAX_CHAR = 1500
# V-1 bot #330: senza schermo un taglio deve sentirsi (nessuno legge «content»)
_PARLATO_VOCE_RESTO = "C'è altro, chiedimi se vuoi il resto."
_PARLATO_MAX_FRASI = 3
_PARLATO_MAX_CHAR = 400
_PARLATO_RESTO = " Il resto è a schermo."
_FINE_FRASE = re.compile(r"(?<=[.!?…])\s+")
_ABBREVIAZIONE = re.compile(r"(?:^|\s)(?:dott|dr|sig|sigg|sig\.ra|ing|avv|prof|arch|geom|"
                            r"rag|ecc|es|pag|n|nr|tel|art|cap|vs)\.$", re.IGNORECASE)


# V6 (chat M2, «capire meglio»): le frasi brevi non devono perdere il filo, e la richiesta
# è una trascrizione che può storpiare qualche parola.
_CONTESTO_VOCE = (
    "Brevità non vuol dire perdere il filo: rispondi a quello che l'operatore intende, "
    "tenendo conto di quello che vi siete detti prima in questa conversazione. La sua "
    "frase arriva da una trascrizione vocale e può avere parole storpiate (per esempio "
    "«Gus» per «Gas»): se una parola non torna, interpretala dal contesto; se la "
    "richiesta resta ambigua, fai una sola domanda per chiarire invece di indovinare. "
    # C1, voce rapida (ordine dell'operatore via M1, 6 nov): niente risposte fuori tema
    "Rispondi solo all'ultima cosa che l'operatore ha detto: il resto della conversazione è "
    "contesto, non argomenti da riprendere né domande ancora da sistemare.")
# V3: istruzione per i soli turni PARLATI (gas.py `run_turn(istruzione_turno=...)`: vale per
# quel turno, nel messaggio system, fuori dalla cronologia). Il testo scritto resta com'è.
# V13 (chat M2, prova di Jarvis sul Mac del 5 nov, decisione dell'operatore): risposte a
# voce più corte, al massimo 2 frasi, senza premesse; niente «… sì o no?» in coda a ogni
# risposta (a voce stanca), domanda solo se serve per fare quello che è stato chiesto.
ISTRUZIONE_VOCE = (
    "Stai parlando a voce con l'operatore, in una conversazione rapida. Rispondi con una "
    "o due frasi brevi, mai più di due, senza premesse, senza ripetere la domanda, senza "
    "elenchi né formattazione. Dai subito un parere o una proposta "
    "concreta (anche «no, meglio così»). "
    "Non chiudere con domande né con offerte («vuoi che…?», «sì o no?»): fai una domanda "
    "solo se senza la risposta non puoi fare quello che ti è stato chiesto. Se il risultato è lungo, "
    "riassumilo in una frase."
    + " " + _CONTESTO_VOCE)
# V4 (V-1 bot #311): con la pagina del browser c'è uno schermo: prima le frasi da dire,
# poi, dopo una riga vuota, il dettaglio da leggere (non viene detto a voce).
ISTRUZIONE_VOCE_SCHERMO = (
    "Stai parlando a voce con l'operatore, in una conversazione rapida, e lui ha anche uno "
    "schermo. Apri con una o due frasi brevi da dire a voce, mai più di due, senza "
    "premesse né elenchi né formattazione: "
    "dai subito un parere o una proposta concreta (anche «no, meglio così»). "
    "Non chiudere con domande né con offerte («vuoi che…?», «sì o no?»): fai una domanda "
    "solo se senza la risposta non puoi fare quello che ti è stato chiesto. Se servono "
    "dettagli (dati, elenchi, analisi, testo lungo), scrivili DOPO una riga vuota: quella "
    "parte non viene letta a voce, l'operatore la legge a schermo."
    + " " + _CONTESTO_VOCE)
_PARAGRAFO = re.compile(r"\n[ \t]*\n")

# V13 (chat M2): data e ora LOCALI della macchina che fa girare il server (il Mac) scritte
# nell'istruzione del turno parlato, così «che ore sono» non costa un giro dello strumento
# data_ora (un giro = una chiamata in più al cervello, secondi di attesa a voce).
_GIORNI = ("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica")
_MESI = ("gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
         "settembre", "ottobre", "novembre", "dicembre")


def ora_per_voce(adesso: Optional[datetime] = None) -> str:
    """V13: la frase con data e ora locali (fuso della macchina) per l'istruzione del turno
    parlato. `adesso` solo per i test; deve avere il fuso (aware)."""
    ora = adesso if adesso is not None else datetime.now().astimezone()
    fuso = ora.tzname() or ora.strftime("UTC%z")
    # V-2 bot #334: «ore 1:30», senza lo zero iniziale che il modello potrebbe ripetere.
    # V-1 bot #334: il system prompt di base dice «per data e ora usa data_ora»: qui si dice
    # esplicitamente che per questo turno vale l'ora scritta, senza lo strumento.
    return (f"Adesso è {_GIORNI[ora.weekday()]} {ora.day} {_MESI[ora.month - 1]} {ora.year}, "
            f"ore {ora.hour}:{ora:%M} (ora locale, fuso {fuso}). In questo turno, per l'ora o "
            "la data rispondi con questa e NON usare data_ora: vale al posto dell'indicazione "
            "generale di usarlo.")


def istruzione_turno_voce(schermo: bool, adesso: Optional[datetime] = None) -> str:
    """V3/V4 + V13: l'istruzione del turno parlato (con o senza schermo) più data e ora."""
    base = ISTRUZIONE_VOCE_SCHERMO if schermo else ISTRUZIONE_VOCE
    return f"{base} {ora_per_voce(adesso)}"


def _dividi_frasi(testo: str) -> List[str]:
    """Frasi di un testo già su una riga; «Dott. Rossi» non è una fine frase (R-574-4-M2)."""
    frasi: List[str] = []
    for pezzo in (f for f in _FINE_FRASE.split(testo) if f):
        if frasi and _ABBREVIAZIONE.search(frasi[-1]):
            frasi[-1] = f"{frasi[-1]} {pezzo}"
        else:
            frasi.append(pezzo)
    return frasi


def frasi_parlate(testo: str) -> List[str]:
    """V7b: la parte parlata (vedi parte_parlata) divisa in frasi, da sintetizzare una alla
    volta. Unite di nuovo con uno spazio danno esattamente parte_parlata(testo)."""
    return _dividi_frasi(parte_parlata(testo))


def frasi_voce(testo: str) -> List[str]:
    """V10: tutta la risposta da dire a voce (senza schermo), divisa in frasi. Tetto
    _PARLATO_VOCE_MAX_CHAR: si tengono le frasi intere che ci stanno; se già la prima è più
    lunga si taglia all'ultimo spazio. Col taglio il parlato arriva a _PARLATO_VOCE_MAX_CHAR
    più l'avviso (1500 + 1 + 37 caratteri, V-2 bot #330 su ae3258e). Mai «Il resto è a schermo» (qui uno schermo non c'è):
    se qualcosa resta fuori si aggiunge _PARLATO_VOCE_RESTO (V-1 bot #330), così il taglio
    si sente."""
    testo = " ".join(testo.split())
    tutte = _dividi_frasi(testo)
    frasi: List[str] = []
    lunghezza = 0
    for f in tutte:
        nuova = lunghezza + len(f) + (1 if frasi else 0)
        if nuova > _PARLATO_VOCE_MAX_CHAR:
            break
        frasi.append(f)
        lunghezza = nuova
    if not frasi and testo:  # prima frase già troppo lunga: taglio all'ultimo spazio
        # R-660-2-M2: si guarda anche il carattere subito dopo il tetto, così una parola che
        # finisce proprio al tetto (seguita da uno spazio) non si perde
        testa = testo[:_PARLATO_VOCE_MAX_CHAR + 1]
        frasi = [testo if len(testo) <= _PARLATO_VOCE_MAX_CHAR
                 else testa.rsplit(" ", 1)[0] if " " in testa
                 else testo[:_PARLATO_VOCE_MAX_CHAR]]
    if testo and " ".join(frasi) != testo:
        frasi.append(_PARLATO_VOCE_RESTO)
    return frasi


# Velocità (9 nov, decisione dell'operatore via M1): le frasi fisse del server si sintetizzano
# una volta sola per processo e voce, poi l'MP3 viene dalla memoria (niente attesa né costo
# ElevenLabs per «Dimmi.», «Non ho capito…», «Il resto è a schermo.»…). Solo testi fissi del
# codice, mai testo del modello o dell'operatore.
_FRASI_FISSE = frozenset({
    _RISPOSTA_ATTIVAZIONE, RISPOSTA_PAUSA, RISPOSTA_SERVE_ATTIVAZIONE, _NON_HO_CAPITO,
    _USO_FORTE_PARLATO, _PARLATO_VOCE_RESTO, _PARLATO_RESTO.strip(),
})
_CACHE_FRASI_MAX = 32
_cache_frasi: Dict[Tuple[Any, str, str], bytes] = {}


def sintesi(frase: str, api_key: str, voice_id: str) -> bytes:
    """synthesize_speech con la cache delle frasi fisse. La chiave contiene la funzione di
    sintesi stessa (cambia nei test) e la voce; mai in cache un audio vuoto. Gli errori di
    ElevenLabs passano al chiamante come prima."""
    if frase not in _FRASI_FISSE:
        return synthesize_speech(frase, api_key, voice_id)
    chiave = (synthesize_speech, voice_id, frase)
    audio = _cache_frasi.get(chiave)
    if audio is None:
        audio = synthesize_speech(frase, api_key, voice_id)
        if audio:
            if len(_cache_frasi) >= _CACHE_FRASI_MAX:
                _cache_frasi.clear()
            _cache_frasi[chiave] = audio
    return audio


def parte_parlata(testo: str) -> str:
    """Le prime frasi di `testo` da dire a voce (≤ _PARLATO_MAX_FRASI frasi e
    ≤ _PARLATO_MAX_CHAR caratteri); se il testo è più lungo aggiunge «Il resto è a
    schermo.». Testo corto → identico. V4: si dice solo il primo paragrafo (il dettaglio
    dopo la riga vuota, chiesto da ISTRUZIONE_VOCE_SCHERMO, si legge a schermo)."""
    pezzi = _PARAGRAFO.split(testo.strip(), maxsplit=1)
    if len(pezzi) == 2 and pezzi[1].strip():
        primo = parte_parlata(pezzi[0])
        return primo if primo.endswith(_PARLATO_RESTO) else primo + _PARLATO_RESTO
    testo = " ".join(testo.split())  # R-574-4-M2: a capo e spazi doppi non contano
    frasi = _dividi_frasi(testo)
    parlato = ""
    for f in frasi[:_PARLATO_MAX_FRASI]:
        prova = f"{parlato} {f}".strip()
        if len(prova) > _PARLATO_MAX_CHAR:
            break
        parlato = prova
    if not parlato:  # prima frase già troppo lunga: taglio all'ultimo spazio
        parlato = testo[:_PARLATO_MAX_CHAR].rsplit(" ", 1)[0] if len(testo) > _PARLATO_MAX_CHAR else testo
    return parlato if parlato == testo else parlato + _PARLATO_RESTO


# V4 (V-2 ve #311): tetto LATO SERVER alle richieste a voce, oltre a quello della pagina: un
# client diverso o rotto non fa partire turni senza fine. GAS_VOICE_MAX_TURNI_ORA (default
# 60) richieste a voce (chiamate a Groq, V5) nell'ultima ora, poi 429 finché la finestra non scorre.
_MAX_TURNI_ORA_DEFAULT = 60


def _max_turni_ora() -> int:
    try:
        n = int(os.environ.get("GAS_VOICE_MAX_TURNI_ORA") or _MAX_TURNI_ORA_DEFAULT)
    except ValueError:
        log.warning("GAS_VOICE_MAX_TURNI_ORA non numerica: uso %d", _MAX_TURNI_ORA_DEFAULT)
        return _MAX_TURNI_ORA_DEFAULT
    return n if n > 0 else _MAX_TURNI_ORA_DEFAULT


# R8 fetta 1 (chat M2, sicurezza): C1 — tetto ai tentativi con token sbagliato per IP;
# C2 — tetto alle richieste a testo. Soglie proposte all'operatore in
# reports/proposta_voce_sicura.md; tutte e due configurabili.
_MAX_FALLITI_DEFAULT = 10  # tentativi falliti per IP in _FALLITI_FINESTRA_S, poi blocco
_FALLITI_FINESTRA_S = 600.0
_FALLITI_BLOCCO_S = 900.0
_FALLITI_MAX_IP = 1024  # IP ricordati al massimo (memoria limitata anche sotto attacco)
_MAX_TESTO_ORA_DEFAULT = 120


def _intero_env(nome: str, default: int) -> int:
    """Intero positivo da env; vuoto, non numerico o <= 0 → default (con avviso se scritto male)."""
    grezzo = os.environ.get(nome, "").strip()
    if not grezzo:
        return default
    try:
        n = int(grezzo)
    except ValueError:
        log.warning("%s non numerica: uso %d", nome, default)
        return default
    return n if n > 0 else default


def _bind_locale(bind: str) -> bool:
    """R8: indirizzo raggiungibile solo dal computer stesso (loopback IP o «localhost»; mai un
    nome host qualsiasi, anche se comincia con «127.», R-720-3-M2)."""
    b = bind.strip().lower()
    if b == "localhost":
        return True
    try:
        # solo IPv4 (bot #358 V-2): HTTPServer è solo IPv4, «::1» lo farebbe cadere all'avvio
        ip = ipaddress.ip_address(b)
        return isinstance(ip, ipaddress.IPv4Address) and ip.is_loopback
    except ValueError:
        return False


def _bind_tutte_le_interfacce(bind: str) -> bool:
    """R8 (bot #358 V-1): indirizzo «non specificato» (tutte le interfacce, IPv4 o IPv6): anche
    dentro un tunnel esporrebbe il server in chiaro sulle interfacce pubbliche."""
    try:
        return ipaddress.ip_address(bind.strip()).is_unspecified
    except ValueError:
        return False


def _bind_ip_letterale(bind: str) -> bool:
    """R8 (R-727-1-M2, R-728-1/2-M2): fuori da 127.0.0.1 si accetta solo un indirizzo IPv4
    scritto per intero (il server, HTTPServer, è solo IPv4). Un nome host, una forma abbreviata
    («0», «0x0»…) o un IPv6 (anche «IPv4 dentro IPv6», che secondo la versione di Python sfugge
    al controllo «tutte le interfacce») verrebbero risolti dal socket in un altro indirizzo, o
    farebbero cadere l'avvio con un errore non gestito."""
    try:
        return isinstance(ipaddress.ip_address(bind.strip()), ipaddress.IPv4Address)
    except ValueError:
        return False


def _env_acceso(nome: str) -> bool:
    return os.environ.get(nome, "").strip().lower() in ("1", "true", "on", "yes", "si", "sì")


def _voce_tutta_forte() -> bool:
    """GAS_VOCE_FORTE acceso: regole di _env_flag in gas.py (1/true/on/yes/si) più «sì»
    con l'accento (nota #565-M2: scritto in italiano, non deve restare spento in silenzio)."""
    return os.environ.get("GAS_VOCE_FORTE", "").strip().lower() in ("1", "true", "on", "yes", "si", "sì")


def cervello_voce(prompt: str, parlato: bool) -> tuple[Optional[str], str]:
    """(cervello, richiesta) per una richiesta della voce: «forte» solo cervello forte,
    «uso» prefisso senza richiesta (fail-closed: mai ai gratuiti), None turno normale.
    «/forte» vale sempre; la parola parlata solo se `parlato` (testo trascritto)."""
    from brains.router import prefisso_forte
    if not prompt.strip():
        return "uso", ""  # V-3 ve #304: fail-closed anche fuori dal gestore
    cervello, prompt = prefisso_forte(prompt)
    if cervello is None and parlato:
        m = _PAROLA_FORTE.match(prompt)
        if m:
            richiesta = re.sub(r"^\W+", "", m.group(1)).strip()
            if not richiesta:
                return "uso", ""
            cervello, prompt = "forte", richiesta
    if cervello is None and _voce_tutta_forte():
        cervello = "forte"
    return cervello, prompt


def _token_ok(received: str, expected: str) -> bool:
    """Confronto a tempo costante. False se uno dei due è vuoto."""
    if not received or not expected:
        return False
    return hmac.compare_digest(received.encode("utf-8"), expected.encode("utf-8"))


class VoiceHandler(BaseHTTPRequestHandler):
    """Handler HTTP per POST /voice. Kernel e token iniettati dal runner prima del bind."""

    kernel: Any = None
    token: str = ""
    _capito: Optional[str] = None  # V6: trascrizione della richiesta in corso (per istanza)
    _tempi: Optional[Dict[str, float]] = None  # V7: secondi per pezzo della richiesta in corso
    _t0: float = 0.0
    _parlato: bool = False  # V11: la richiesta in corso è a voce (audio), non a testo
    turni_parlati: List[float] = []  # V4/V5: istanti delle chiamate a Groq (tetto orario)
    prove_voci: List[float] = []  # V8: istanti delle prove di voce ElevenLabs (tetto orario)
    # V8 (R-624-1-M2): id delle voci mostrate dall'ultimo elenco (già filtrate: niente
    # cloni); la prova accetta solo queste, non un id qualunque scritto a mano
    voci_ammesse: frozenset = frozenset()
    # V14: («voce», frase) e MP3 di «Sì, signore?»; una sola voce in cache (None = vuota)
    conferma_cache: Optional[Tuple[Tuple[str, str], bytes]] = None
    # V15 (V-2 bot #335): ultimo fallimento della conferma (chiave, istante): per
    # CONFERMA_PAUSA_ERRORE_S non si richiama ElevenLabs (server a un thread: niente attese
    # ripetute con ElevenLabs giù), il client suona il bip.
    conferma_errore: Optional[Tuple[Tuple[str, str], float]] = None
    _comando: Optional[str] = None  # V15: X-Gas-Comando della risposta in corso
    # V8b: voci della libreria mostrate dall'ultima ricerca {id: (proprietario, nome)};
    # si aggiungono all'account solo queste
    libreria_ammesse: Dict[str, Any] = {}
    aggiunte_voci: List[float] = []  # V8b: istanti delle aggiunte all'account (tetto orario)
    # R8 fetta 1 (C1): per IP, istanti dei tentativi falliti e fine del blocco (monotonic)
    falliti: Dict[str, List[float]] = {}
    bloccati: Dict[str, float] = {}
    turni_testo: List[float] = []  # R8 fetta 1 (C2): istanti delle richieste a testo

    def log_message(self, fmt: str, *args: Any) -> None:
        log.info(fmt, *args)

    def _segna(self, pezzo: str, inizio: float) -> None:
        """V7: secondi spesi in un pezzo della richiesta (trascrizione, cervello, voce)."""
        if self._tempi is not None:
            self._tempi[pezzo] = round(time.monotonic() - inizio, 2)

    def _chiudi_tempi(self, code: int) -> Optional[Dict[str, float]]:
        """V7: tempi della richiesta + totale nel server; una riga INFO nel solo
        gas_debug.log (logger gas.voce.tempi) per ogni richiesta che ha speso qualcosa.
        Solo numeri."""
        if self._tempi is None or not self._tempi:
            return None
        tempi = dict(self._tempi, server=round(time.monotonic() - self._t0, 2))
        self._tempi = None  # una sola volta per richiesta
        _log_tempi.info("tempi voce (%s): %s", code,
                        " ".join(f"{k}={v:.2f}s" for k, v in tempi.items()))
        return tempi

    def _send_json(self, code: int, payload: Dict[str, Any]) -> None:
        tempi = self._chiudi_tempi(code)
        if tempi is not None:
            payload = dict(payload, tempi=tempi)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_audio(self, data: bytes, tipo: str = "audio/mpeg") -> None:
        tempi = self._chiudi_tempi(200)
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        if tempi is not None:  # V7: con l'MP3 grezzo i tempi viaggiano in un'intestazione
            self.send_header("X-Gas-Tempi", ";".join(f"{k}={v}" for k, v in tempi.items()))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _wants_audio(self) -> bool:
        """True se il client dichiara Accept: audio/mpeg o audio/* (non audio generico */*).
        Retrocompatibile: senza header (o Accept: application/json) → False → risposta JSON."""
        accept = self.headers.get("Accept", "")
        return "audio/mpeg" in accept or "audio/*" in accept

    def _check_auth(self) -> bool:
        """Verifica il token bearer. Logga ogni fallimento con IP; MAI il token ricevuto."""
        hdr = self.headers.get("Authorization", "")
        parts = hdr.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            log.warning("AUTH FAIL ip=%s motivo=header_mancante_o_malformato", self.client_address[0])
            return False
        if not _token_ok(parts[1].strip(), self.token):
            log.warning("AUTH FAIL ip=%s motivo=token_non_valido", self.client_address[0])
            return False
        return True

    def _autorizza(self) -> bool:
        """R8 fetta 1 (C1): controllo del token con tetto ai tentativi falliti per IP. Manda da sé
        la risposta di rifiuto (429 se l'IP è bloccato, 401 se il token è sbagliato) e dice se
        la richiesta può proseguire. Un IP bloccato riceve 429 anche col token giusto, finché il
        blocco non scade: chi indovina non può sapere quando ha indovinato. Nel log solo IP ed
        esito, mai il token."""
        cls = type(self)
        ip = str(self.client_address[0])
        adesso = time.monotonic()
        # sempre copie riassegnate sulla classe del server: mai un dict condiviso con
        # VoiceHandler o con altri server nello stesso processo (test)
        bloccati = {k: v for k, v in cls.bloccati.items() if v > adesso}
        falliti = {k: v for k, v in cls.falliti.items() if v and adesso - v[-1] < _FALLITI_FINESTRA_S}
        if ip in bloccati:
            cls.bloccati, cls.falliti = bloccati, falliti
            log.warning("AUTH BLOCCATO ip=%s", ip)
            self._send_json(429, {"error": "Troppi tentativi non autorizzati: riprova più tardi."})
            return False
        if self._check_auth():
            cls.bloccati, cls.falliti = bloccati, falliti
            return True
        parti = self.headers.get("Authorization", "").split(" ", 1)
        if len(parti) != 2 or parti[0].lower() != "bearer" or not parti[1].strip():
            # bot #358 V-1: senza «Bearer <token>» non si sta provando un token, quindi non
            # conta per il blocco. Una pagina web qualsiasi può mandare al server locale
            # richieste senza header (img, fetch no-cors) ma non può aggiungere Authorization
            # senza preflight, che qui fallisce: così non può bloccare la voce dell'operatore.
            cls.bloccati, cls.falliti = bloccati, falliti
            self._send_json(401, {"error": "Unauthorized"})
            return False
        recenti = [t for t in falliti.pop(ip, []) if adesso - t < _FALLITI_FINESTRA_S] + [adesso]
        if len(recenti) >= _intero_env("GAS_VOICE_MAX_FALLITI", _MAX_FALLITI_DEFAULT):
            if len(bloccati) < _FALLITI_MAX_IP:
                bloccati[ip] = adesso + _FALLITI_BLOCCO_S
                log.warning("AUTH BLOCCO ip=%s per %d s", ip, int(_FALLITI_BLOCCO_S))
            cls.bloccati, cls.falliti = bloccati, falliti
            self._send_json(429, {"error": "Troppi tentativi non autorizzati: riprova più tardi."})
            return False
        if len(falliti) < _FALLITI_MAX_IP:
            falliti[ip] = recenti
        cls.bloccati, cls.falliti = bloccati, falliti
        self._send_json(401, {"error": "Unauthorized"})
        return False

    def end_headers(self) -> None:
        """V15: un comando per il client (oggi solo «pausa») viaggia in X-Gas-Comando, in ogni
        formato di risposta (JSON, MP3, NDJSON)."""
        if self._comando:
            self.send_header("X-Gas-Comando", self._comando)
        super().end_headers()

    def do_POST(self) -> None:
        self._comando = None
        self._t0 = time.monotonic()
        self._tempi = {}
        self._capito = None  # V-3 bot #318: mai il «capito» di un'altra richiesta (keep-alive)
        self._finiti_jobs = None  # R-711-3-M2: mai i compiti di un'altra richiesta
        self._parlato = False
        if self.path in ("/voci/prova", "/voci/aggiungi"):  # V8/V8b: prova o aggiunta di una voce
            if not self._autorizza():
                return
            try:
                n = int(self.headers.get("Content-Length", 0) or 0)
            except ValueError:
                n = -1
            if not 0 <= n <= 4096:
                self._send_json(400, {"error": "Content-Length non valido"})
                return
            self._tempi = None
            corpo = self.rfile.read(n) if n else b""
            (self._prova_voce if self.path == "/voci/prova" else self._aggiungi_voce)(corpo)
            return
        if self.path != _ENDPOINT:
            self._send_json(404, {"error": "Not Found"})
            return

        if not self._autorizza():
            return

        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
        except ValueError:
            self._send_json(400, {"error": "Content-Length non valido"})
            return
        raw = self.rfile.read(length) if length > 0 else b""
        # V-2 bot #322: il caricamento dell'audio dalla pagina è «rete», non tempo del server
        self._t0 = time.monotonic()

        content_type = self.headers.get("Content-Type", "")
        ct_base = content_type.split(";")[0].strip().lower()
        is_audio = ct_base.startswith("audio/") or ct_base == "multipart/form-data"

        self._parlato = is_audio
        if is_audio:
            # V4 (V-2 ve #311, R-580-2-M2): tetto orario delle richieste a voce controllato PRIMA
            # della trascrizione, così oltre il tetto non si spende nemmeno Groq
            tetto = _max_turni_ora()
            if len(self._turni_recenti()) >= tetto:
                self._send_json(429, {"error": (
                    f"Troppe richieste a voce nell'ultima ora ({tetto}, GAS_VOICE_MAX_TURNI_ORA): "
                    "nessun lavoro avviato. Riprova più tardi o scrivi.")})
                return
            prompt = self._do_stt(raw, content_type)
            if prompt is None:
                return  # risposta (errore o «non ho capito») già inviata
            self._capito = prompt  # V6: la pagina mostra «Ho capito: …»
            if _SOLO_PAUSA.match(prompt):  # V15: «pausa»/«standby»: nessun turno, il client si ferma
                self._comando = COMANDO_PAUSA
                if self._seguito():
                    # V-2 bot #339 su 312cd86: nel seguito «basta!» può venire dalla stanza o
                    # dalla TV: la conversazione si chiude lo stesso, ma senza voce
                    self._send_json(200, {"content": "", "pausa": True})
                    return
                self._rispondi_senza_turno(RISPOSTA_PAUSA, "pausa")
                return
            if _SOLO_ATTIVAZIONE.match(prompt):  # V13: solo «Hey Jarvis»: nessun turno
                # Bot #350 V-5: anche la sola parola di attivazione dice i compiti finiti
                # (i turni dopo sono seguiti, dove non si leggono)
                finiti = "" if self._seguito() else self._compiti_finiti()
                self._rispondi_senza_turno(_RISPOSTA_ATTIVAZIONE, "attivazione", prefisso=finiti)
                return
        else:
            try:
                data: Dict[str, Any] = json.loads(raw) if raw else {}
            except (json.JSONDecodeError, ValueError):
                self._send_json(400, {"error": "Body JSON non valido"})
                return

            prompt = (data.get("prompt") or "").strip()
            if not prompt:
                self._send_json(400, {"error": "Campo 'prompt' mancante o vuoto"})
                return

        # R-ve269-2 + V1: «/forte», «forte …» parlato o GAS_VOCE_FORTE → solo forte, mai ai gratuiti
        cervello, prompt = cervello_voce(prompt, parlato=is_audio)
        if cervello == "uso":
            if not is_audio:
                self._send_json(400, {"error": _USO_FORTE})
            elif self._seguito():  # V-1 ve #339: «forte» captato dalla stanza: niente voce
                self._chiudi_seguito()
            else:
                self._rispondi_senza_turno(_USO_FORTE_PARLATO, "uso")
            return

        testo_ora: Optional[float] = None
        if not is_audio:
            # R8 fetta 1 (C2): tetto orario anche alle richieste a testo (ogni turno spende il
            # cervello); controllato prima del turno, così oltre il tetto non parte nessun lavoro.
            # Controllato PRIMA di V12 (un testo rifiutato qui non consuma il tetto voce,
            # R-720-1-M2) ma contato DOPO, solo se anche V12 lascia passare (R-722-1-M2)
            tetto_testo = _intero_env("GAS_VOICE_MAX_TESTO_ORA", _MAX_TESTO_ORA_DEFAULT)
            adesso = time.monotonic()
            testi = [t for t in type(self).turni_testo if adesso - t < 3600]
            if len(testi) >= tetto_testo:
                type(self).turni_testo = testi
                self._send_json(429, {"error": (
                    f"Troppe richieste a testo nell'ultima ora ({tetto_testo}, "
                    "GAS_VOICE_MAX_TESTO_ORA): nessun lavoro avviato. Riprova più tardi.")})
                return
            type(self).turni_testo = testi
            testo_ora = adesso

        if (not is_audio and self._sintesi_a_testo()
                and os.environ.get("ELEVENLABS_API_KEY", "").strip()):
            # V12 (R-663-1-M2, decisione dell'operatore): anche una richiesta a TESTO che chiede
            # la risposta a voce spende ElevenLabs, quindi conta nel tetto orario; controllata
            # prima del turno, così oltre il tetto non parte nessun lavoro. Senza chiave
            # ElevenLabs non si spende nulla e non conta (R-665-3-M2, come i rifiuti locali V5)
            tetto = _max_turni_ora()
            if len(self._turni_recenti()) >= tetto:
                self._send_json(429, {"error": (
                    f"Troppe richieste a voce nell'ultima ora ({tetto}, GAS_VOICE_MAX_TURNI_ORA): "
                    "nessun lavoro avviato. Riprova più tardi o chiedi la risposta solo a testo.")})
                return
            type(self).turni_parlati = self._turni_recenti() + [time.monotonic()]

        if testo_ora is not None:
            type(self).turni_testo = type(self).turni_testo + [testo_ora]

        t_cervello: Optional[float] = None
        try:
            result_content: Optional[str] = None
            strumento_negato = False  # V15: turno effimero che chiedeva uno strumento
            kw: Dict[str, Any] = {}
            if cervello == "forte":
                kw["cervello"] = "forte"
            if is_audio:  # V3/V4: risposte a voce corte, col dettaglio a schermo se c'è
                kw["istruzione_turno"] = istruzione_turno_voce(self._vuole_audio_testo())
                if self._seguito():  # V15: prima decidere se il parlato è per Gas
                    kw["istruzione_turno"] += " " + ISTRUZIONE_SEGUITO
                    # R-675-1-M2: parlato della stanza (terzi, TV) = possibili dati personali:
                    # solo il cervello forte, mai i gratuiti (CLAUDE.md §2); forte fermo →
                    # errore dichiarato e il client chiude la conversazione. NB: la trascrizione
                    # (Groq Whisper) riceve l'audio anche qui, come per tutta la voce: rischio
                    # accettato dall'operatore il 6 nov (V-2 bot #339, R-684-2-M2)
                    kw["cervello"] = "forte"
                    # R-675-1-M2 (scelta A dell'operatore): turno effimero nel kernel: nessuno
                    # strumento offerto, niente storia condivisa del parlato della stanza
                    kw["effimero"] = True
            t_cervello = time.monotonic()
            if is_audio:  # voce rapida (fetta 2): profilo del turno parlato nel kernel
                kw["voce"] = True
            turno = self.kernel.run_turn(prompt, **kw)
            try:
                for event in turno:
                    etype = event.get("type")
                    if etype == "final":
                        result_content = event.get("content", "")
                        strumento_negato = bool(event.get("strumento_negato"))
                        self._segna("cervello", t_cervello)
                        break
                    elif etype == "error":
                        self._segna("cervello", t_cervello)
                        self._send_json(500, {"error": event.get("content", "Errore pipeline")})
                        return
                    # type="tool_res": consumato in silenzio
            finally:
                # R-677-1-M2: il kernel chiude il turno (e il turno effimero rimette la storia
                # vera) SUBITO, non quando il generatore viene raccolto
                close = getattr(turno, "close", None)
                if callable(close):
                    close()
        except Exception as exc:
            if t_cervello is not None:  # R-614-1-M2: anche un cervello che si rompe ha un tempo
                self._segna("cervello", t_cervello)
            log.warning("run_turn eccezione: %s", exc)
            self._send_json(500, {"error": "Errore interno del kernel"})
            return

        if result_content is None:
            if t_cervello is not None:  # V-2 ve #322: turno finito senza final né error (V-3 bot: tipo)
                self._segna("cervello", t_cervello)
            self._send_json(500, {"error": "Nessuna risposta dal kernel"})
            return

        if is_audio and self._seguito() and strumento_negato:
            self._rispondi_senza_turno(RISPOSTA_SERVE_ATTIVAZIONE, "serve_attivazione")
            return

        if is_audio and self._seguito() and (_NON_PER_ME.search(result_content)
                                             or not result_content.strip()):
            # V15: parlato non rivolto a Gas: niente voce né testo (privacy della stanza)
            log.info("turno di seguito non rivolto a Gas: conversazione chiusa")
            self._chiudi_seguito()
            return

        if is_audio and self._seguito():
            # V15 punto 1 (sì dell'operatore via M1, V-1 (a) bot #339): il seguito rivolto a
            # Gas entra nella storia vera (il turno effimero non l'ha scritta), così il
            # seguito dopo lo ricorda. Il generatore è già chiuso: storia vera ripristinata.
            registra = getattr(self.kernel, "registra_seguito", None)
            if callable(registra):
                try:
                    if not registra(prompt, result_content):
                        log.warning("seguito rivolto a Gas non salvato nella storia")
                except Exception as exc:  # §9: la risposta parte lo stesso
                    log.warning("registra_seguito eccezione: %s", exc)

        # Fetta 3.2: compiti in sottofondo finiti, solo nei turni a voce di attivazione
        finiti = self._compiti_finiti() if (is_audio and not self._seguito()) else ""

        if self._vuole_audio_testo() or self._vuole_righe_senza_schermo():
            self._do_audio_testo_response(result_content, prefisso=finiti)
        elif self._wants_audio() and self._formato() != _FORMATO_PEZZI_VOCE:
            self._do_tts_response(f"{finiti} {result_content}".strip() if finiti else result_content)
        else:
            if finiti:
                result_content = f"{finiti}\n\n{result_content}"
            out: Dict[str, Any] = {"content": result_content}
            if self._capito is not None:
                out["capito"] = self._capito
            self._send_json(200, out)
            # R-711-2-M2: a testo il client lo mostra; segnati DOPO l'invio riuscito
            self._segna_finiti_letti()

    def _compiti_finiti(self) -> str:
        """Fetta 3.2 (chat M2, 7 nov): la frase sui compiti in sottofondo finiti e non ancora
        letti (al massimo 2, ultime 24 ore), da dire PRIMA della risposta; "" se non ce ne
        sono. Chiamata solo nei turni a voce di attivazione (mai nel seguito: parlato della
        stanza). Fail-safe §9: un errore dà "" e la risposta parte com'è."""
        try:
            from modules import sottofondo
            root = getattr(self.kernel, "root", None)
            if root is None:
                return ""
            jobs = sottofondo.da_leggere(root)
            if not jobs:
                return ""
            frase = sottofondo.frase_finiti(jobs)
            # Ve #350 V-1: segnati letti solo DOPO la consegna (_segna_finiti_letti): se la
            # sintesi fallisce o il client chiude, li si ridice alla prossima attivazione
            self._finiti_jobs = jobs
            return frase.strip()
        except Exception as exc:
            log.warning("compiti finiti non letti a voce: %s", exc)
            return ""

    def _segna_finiti_letti(self) -> None:
        """Ve #350 V-1: i compiti detti in questa risposta diventano «letti» solo ora che la
        consegna è riuscita. Una volta sola; mai eccezioni (§9)."""
        jobs = getattr(self, "_finiti_jobs", None)
        self._finiti_jobs = None
        if not jobs:
            return
        try:
            from modules import sottofondo
            sottofondo.segna_letti(getattr(self.kernel, "root", None), jobs)
        except Exception as exc:
            log.warning("segno di lettura dei compiti non scritto: %s", exc)

    def _rispondi_senza_turno(self, testo: str, segno: str, prefisso: str = "") -> None:
        """Risposta parlata fissa senza lavoro del kernel («uso», «non ho capito», «dimmi»), nel
        formato chiesto dal client; `segno` è il campo JSON che la distingue. `prefisso`:
        compiti finiti da dire prima (fetta 3.2, solo per «dimmi»)."""
        if self._vuole_audio_testo() or self._vuole_righe_senza_schermo():
            self._do_audio_testo_response(testo, {segno: True}, prefisso=prefisso)
        elif self._wants_audio() and os.environ.get("ELEVENLABS_API_KEY", "").strip():
            self._do_tts_response(f"{prefisso} {testo}".strip() if prefisso else testo)
        else:  # V-2 bot #318: senza TTS il messaggio arriva lo stesso, come testo (mai un 503)
            if prefisso:
                testo = f"{prefisso}\n\n{testo}"
            out: Dict[str, Any] = {"content": testo, segno: True}
            if self._capito is not None:
                out["capito"] = self._capito
            self._send_json(200, out)
            self._segna_finiti_letti()  # R-711-2-M2: dopo l'invio riuscito

    def _turni_recenti(self) -> List[float]:
        """Istanti delle richieste a voce (chiamate a Groq) e, dalla V12, delle richieste a testo
        con risposta a voce, nell'ultima ora (tetto GAS_VOICE_MAX_TURNI_ORA)."""
        adesso = time.monotonic()
        return [t for t in self.turni_parlati if adesso - t < 3600]

    def _chiudi_seguito(self) -> None:
        """V15: chiude la conversazione senza voce né testo (X-Gas-Comando: fine)."""
        self._comando = COMANDO_FINE
        self._send_json(200, {"content": "", "fine": True})

    def _seguito(self) -> bool:
        """V15: il client dice che il turno è nella finestra di conversazione, senza parola
        di attivazione (X-Gas-Seguito: 1). Vale solo per il parlato."""
        return self._parlato and self.headers.get("X-Gas-Seguito", "").strip() == "1"

    def _formato(self) -> str:
        return self.headers.get("X-Gas-Formato", "").strip().lower()

    def _vuole_audio_testo(self) -> bool:
        return self._formato() in (_FORMATO_AUDIO_TESTO, _FORMATO_PEZZI)

    def _sintesi_a_testo(self) -> bool:
        """V12: la richiesta (a testo) chiede una risposta sintetizzata da ElevenLabs: gli
        stessi rami della risposta finale che chiamano la sintesi."""
        return self._vuole_audio_testo() or (
            self._wants_audio() and self._formato() != _FORMATO_PEZZI_VOCE)

    def _vuole_righe_senza_schermo(self) -> bool:
        """V10: il client H24 chiede le righe NDJSON ma non ha uno schermo. V11 (V-1 bot #330
        su ae3258e): solo per le richieste a voce, che passano dal tetto orario; una richiesta a
        testo con questo formato riceve solo il testo (JSON), mai la sintesi ElevenLabs."""
        return self._formato() == _FORMATO_PEZZI_VOCE and self._parlato

    def _do_audio_testo_response(self, text: str, extra: Optional[Dict[str, Any]] = None,
                                 prefisso: str = "") -> None:
        """V3: JSON {"content": testo intero, "audio": base64 MP3 della parte parlata}.
        Senza chiave ElevenLabs o con errore TTS la risposta arriva lo stesso, solo testo
        (+ "errore_voce"): a schermo si legge, mai un 503 al posto della risposta.
        Fetta 3.2 (bot #350 V-1): `prefisso` (compiti finiti) si dice per primo FUORI dal
        limite della parte parlata, così non toglie spazio alla risposta; a schermo è il
        primo paragrafo."""
        out: Dict[str, Any] = {"content": f"{prefisso}\n\n{text}" if prefisso else text,
                               **(extra or {})}
        if self._capito is not None:  # V6: quello che Whisper ha sentito, per la pagina
            out["capito"] = self._capito
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        # Bot #352 (f6de3e6) V-1, regola unica: con uno schermo i compiti sono consegnati
        # quando il testo arriva (anche se la voce fallisce); senza schermo solo se detti.
        # R-711-2-M2: il segno parte sempre DOPO l'invio riuscito.
        schermo = not self._vuole_righe_senza_schermo()
        consegnati = False
        if not (text.strip() or prefisso):  # R-710-1-M2: col prefisso si sintetizza lo stesso
            pass
        elif not api_key:
            out["errore_voce"] = "TTS non disponibile: ELEVENLABS_API_KEY non configurata"
            consegnati = schermo
        else:
            voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID
            prima = _dividi_frasi(" ".join(prefisso.split())) if prefisso else []

            def resto(frasi: List[str]) -> List[str]:  # R-711-3-M2: niente lambda
                return frasi if text.strip() else []
            if self._formato() == _FORMATO_PEZZI:
                self._do_pezzi_response(out, prima + resto(frasi_parlate(text)), api_key,
                                        voice_id, n_prefisso=len(prima), schermo=True)
                return
            if self._vuole_righe_senza_schermo():  # V10: tutto a voce, frase per frase
                self._do_pezzi_response(out, prima + resto(frasi_voce(text)), api_key,
                                        voice_id, n_prefisso=len(prima))
                return
            t = time.monotonic()
            try:
                parlato = " ".join(prima + ([parte_parlata(text)] if text.strip() else []))
                out["audio"] = base64.b64encode(
                    sintesi(parlato, api_key, voice_id)).decode("ascii")
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
                out["errore_voce"] = f"Errore TTS ElevenLabs: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs TTS network error: %s", exc)
                out["errore_voce"] = "Errore di rete verso ElevenLabs TTS"
            finally:  # R-614-1-M2: anche un TTS fallito o in timeout ha il suo tempo
                self._segna("voce", t)
            consegnati = True  # ramo MP3 unico: formato con schermo, il testo arriva sempre
        self._send_json(200, out)
        if consegnati:
            self._segna_finiti_letti()

    def _do_pezzi_response(self, primo: Dict[str, Any], frasi: List[str], api_key: str,
                           voice_id: str, n_prefisso: int = 0, schermo: bool = False) -> None:
        """V7b: risposta a righe JSON (NDJSON), una sintesi per frase.
        Riga 1: `primo` (content, capito, …) + "audio" della prima frase + "pezzi" (frasi
        totali). Poi una riga {"audio": …} per ogni frase successiva, appena pronta. Ultima
        riga {"fine": true, "tempi": …}. Un errore TTS a metà → riga {"errore_voce": …} e
        stop (il testo è già a schermo). Il client che chiude la connessione ferma la
        sintesi (niente spesa per frasi che nessuno ascolta)."""
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.end_headers()  # HTTP/1.0: niente Content-Length, la fine è la chiusura

        def riga(obj: Dict[str, Any]) -> bool:
            try:
                self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n")
                self.wfile.flush()
                return True
            except OSError as exc:  # pagina chiusa o interrotta: si smette di sintetizzare
                log.warning("voce a pezzi: client chiuso (%s)", type(exc).__name__)
                return False

        t_tutta = time.monotonic()
        aperto = True
        for i, frase in enumerate(frasi):
            uscita: Dict[str, Any] = dict(primo, pezzi=len(frasi)) if i == 0 else {}
            t = time.monotonic()
            errore: Optional[str] = None
            try:
                uscita["audio"] = base64.b64encode(
                    sintesi(frase, api_key, voice_id)).decode("ascii")
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
                errore = f"Errore TTS ElevenLabs: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs TTS network error: %s", exc)
                errore = "Errore di rete verso ElevenLabs TTS"
            if i == 0:
                self._segna("voce", t)  # tempo fino alla prima frase: quello che si sente
            if errore is not None:
                uscita["errore_voce"] = errore
            aperto = riga(uscita)
            if aperto and ((schermo and i == 0)
                           or (errore is None and n_prefisso and i + 1 == n_prefisso)):
                # ve #350 V-1: con lo schermo i compiti arrivano con la prima riga (content),
                # anche se la voce fallisce; senza schermo quando ne sono state dette le frasi
                self._segna_finiti_letti()
            if errore is not None or not aperto:
                break
        self._segna("voce_tutta", t_tutta)
        tempi = self._chiudi_tempi(200)
        if aperto:
            riga({"fine": True, **({"tempi": tempi} if tempi else {})})

    def _do_tts_response(self, text: str) -> None:
        """Sintetizza text via ElevenLabs e invia i byte MP3. Invia l'errore HTTP se fallisce.
        Se text è vuoto salta la chiamata ElevenLabs e risponde JSON vuoto (mai crash)."""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "TTS non disponibile: ELEVENLABS_API_KEY non configurata"})
            return

        if not text:
            self._send_json(200, {"content": ""})
            return

        voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID

        t = time.monotonic()
        try:
            audio = sintesi(text, api_key, voice_id)
            self._segna("voce", t)
        except ElevenLabsTTSError as exc:
            self._segna("voce", t)  # R-614-1-M2
            log.warning("ElevenLabs TTS error status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"Errore TTS ElevenLabs: {exc.message}"})
            return
        except OSError as exc:
            self._segna("voce", t)  # R-614-1-M2
            log.warning("ElevenLabs TTS network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs TTS"})
            return

        self._send_audio(audio)
        self._segna_finiti_letti()  # ve #350 V-1: solo a sintesi e invio riusciti

    def _do_stt(self, raw: bytes, content_type: str) -> Optional[str]:
        """Trascrive audio → testo via Groq Whisper.
        Invia la risposta HTTP di errore e ritorna None se qualcosa va storto."""
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "STT non disponibile: GROQ_API_KEY non configurata"})
            return None

        if not raw:
            self._send_json(400, {"error": "Audio vuoto"})
            return None

        try:
            audio_bytes, filename = parse_audio_body(raw, content_type)
        except ValueError as exc:
            self._send_json(400, {"error": f"Audio non valido: {exc}"})
            return None

        # V5 (R-581-2-M2, R-585-1-M2): conta per GAS_VOICE_MAX_TURNI_ORA ogni chiamata a Groq,
        # subito prima di farla: anche «forte» senza richiesta e le trascrizioni vuote o
        # fallite spendono, quindi contano; i rifiuti locali (chiave assente, audio vuoto o
        # non valido) no, così l'errore utile (503/400) resta visibile.
        type(self).turni_parlati = self._turni_recenti() + [time.monotonic()]
        t = time.monotonic()
        try:
            text = transcribe_audio(audio_bytes, filename, api_key)
        except TrascrizioneIncerta as exc:
            self._segna("trascrizione", t)
            # V6: Groq ha risposto ma il testo è probabilmente sbagliato: si chiede di
            # ripetere invece di rispondere a caso. Nel log solo il motivo, mai il parlato.
            log.info("trascrizione scartata: %s", exc.motivo)
            if self._seguito():  # R-676-3 (review Mani): rumore della stanza → chiude, niente voce
                self._chiudi_seguito()
                return None
            self._capito = exc.testo
            self._rispondi_senza_turno(_NON_HO_CAPITO, "non_capito")
            return None
        except GroqSTTError as exc:
            self._segna("trascrizione", t)
            if exc.status == 400:
                self._send_json(400, {"error": f"Formato audio non accettato da Groq: {exc.message}"})
            else:
                self._send_json(502, {"error": f"Errore Groq STT: {exc.message}"})
            return None
        except OSError as exc:
            self._segna("trascrizione", t)
            log.warning("Groq STT network error: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso Groq STT"})
            return None

        self._segna("trascrizione", t)
        if not text:
            if self._seguito():  # R-676-3: silenzio nella finestra di conversazione → chiude
                self._chiudi_seguito()
                return None
            self._send_json(400, {"error": "Trascrizione vuota (silenzio o formato non supportato)"})
            return None

        return text

    def _method_not_allowed(self) -> None:
        self._send_json(405, {"error": "Method Not Allowed"})

    # ── V8 (chat M2): «prova voci» — elenco delle voci e prova con una frase fissa ──

    def do_GET(self) -> None:
        self._comando = None
        self._t0 = time.monotonic()
        self._tempi = None
        if self.path == _ENDPOINT_CONFERMA:  # V14
            if not self._autorizza():
                return
            self._conferma()
            return
        if self.path not in ("/voci/elenco", "/voci/libreria"):
            self._method_not_allowed()
            return
        if not self._autorizza():
            return
        if self.path == "/voci/libreria":
            self._libreria()
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        attuale = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID
        out: Dict[str, Any] = {"voci": [], "attuale": attuale, "frasi": list(prova_voci.FRASI_PROVA),
                               "piper": prova_voci.piper_disponibile() is not None}
        type(self).voci_ammesse = frozenset()  # R-625-2-M2: valgono solo le voci di questo elenco
        if not api_key:
            out["errore"] = "ELEVENLABS_API_KEY non configurata: niente voci ElevenLabs"
        else:
            try:
                out["voci"] = prova_voci.ordina_voci(list_voices(api_key), attuale)
                type(self).voci_ammesse = frozenset(v["id"] for v in out["voci"])
            except ElevenLabsTTSError as exc:
                log.warning("ElevenLabs elenco voci status=%s: %s", exc.status, exc.message)
                out["errore"] = f"Elenco voci ElevenLabs non disponibile: {exc.message}"
            except OSError as exc:
                log.warning("ElevenLabs elenco voci rete: %s", exc)
                out["errore"] = "Errore di rete verso ElevenLabs"
        self._send_json(200, out)

    def _conferma(self) -> None:
        """V14: GET /voce/conferma — «Sì, signore?» in MP3 con la voce attuale, dalla cache se
        c'è già per quella voce (nessuna spesa), altrimenti un giro su ElevenLabs e in cache.
        La cache tiene una sola voce: cambiando voce la vecchia frase si butta."""
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "Conferma non disponibile: ELEVENLABS_API_KEY non configurata"})
            return
        voice_id = (os.environ.get("ELEVENLABS_VOICE_ID") or _TTS_DEFAULT_VOICE_ID).strip() or _TTS_DEFAULT_VOICE_ID
        chiave = (voice_id, FRASE_CONFERMA)
        cache = type(self).conferma_cache
        if cache is not None and cache[0] == chiave:
            self._send_audio(cache[1])
            return
        errore = type(self).conferma_errore
        if (errore is not None and errore[0] == chiave
                and time.monotonic() - errore[1] < CONFERMA_PAUSA_ERRORE_S):
            self._send_json(502, {"error": "Conferma non disponibile (errore recente di ElevenLabs)"})
            return
        try:
            audio = synthesize_speech(FRASE_CONFERMA, api_key, voice_id,
                                      timeout=CONFERMA_TIMEOUT_S)
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs conferma status=%s: %s", exc.status, exc.message)
            audio, motivo = b"", f"Errore TTS ElevenLabs: {exc.message}"
        except (OSError, http.client.HTTPException) as exc:  # R-669-1-M2: anche IncompleteRead
            log.warning("ElevenLabs conferma rete: %s", exc)
            audio, motivo = b"", "Errore di rete verso ElevenLabs TTS"
        else:
            motivo = "Errore TTS ElevenLabs: audio vuoto"
        if not audio:  # mai in cache una risposta vuota: il client ripiega sul bip
            type(self).conferma_errore = (chiave, time.monotonic())
            self._send_json(502, {"error": motivo})
            return
        type(self).conferma_errore = None
        type(self).conferma_cache = (chiave, audio)
        self._send_audio(audio)

    def _libreria(self) -> None:
        """V8b: GET /voci/libreria — le migliori voci della libreria condivisa (da aggiungere
        all'account per provarle in italiano), con l'anteprima pubblica e l'avviso su costi e
        limiti. Un errore (piano senza libreria, API diversa) torna nel JSON, mai un crash."""
        type(self).libreria_ammesse = {}
        out: Dict[str, Any] = {"voci": [], "avviso": prova_voci.AVVISO_LIBRERIA}
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            out["errore"] = "ELEVENLABS_API_KEY non configurata"
            self._send_json(200, out)
            return
        try:
            voci = prova_voci.ordina_libreria(list_shared_voices(api_key, prova_voci.FILTRI_LIBRERIA))
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs libreria status=%s: %s", exc.status, exc.message)
            out["errore"] = (f"Libreria ElevenLabs non disponibile ({exc.message}). Se il messaggio "
                             "parla di piano o permessi, il tuo piano non la include.")
            self._send_json(200, out)
            return
        except OSError as exc:
            log.warning("ElevenLabs libreria rete: %s", exc)
            out["errore"] = "Errore di rete verso ElevenLabs"
            self._send_json(200, out)
            return
        type(self).libreria_ammesse = {v["id"]: (v["proprietario"], v["nome"]) for v in voci}
        out["voci"] = voci
        self._send_json(200, out)

    def _aggiungi_voce(self, raw: bytes) -> None:
        """V8b: POST /voci/aggiungi {"voce": id} — aggiunge all'account una voce della
        libreria appena mostrata (mai un id qualunque). Tetto 5 aggiunte/ora: ogni aggiunta
        cambia l'account (e probabilmente occupa uno spazio voce: da verificare)."""
        try:
            voce = (json.loads(raw) if raw else {}).get("voce")
        except (ValueError, AttributeError):
            self._send_json(400, {"error": "Body JSON non valido"})
            return
        voce_info = type(self).libreria_ammesse.get(voce) if isinstance(voce, str) else None
        if voce_info is None:
            self._send_json(409, {"error": "Voce non nella libreria mostrata: ricarica la pagina"})
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "ELEVENLABS_API_KEY non configurata"})
            return
        adesso = time.monotonic()
        recenti = [t for t in type(self).aggiunte_voci if adesso - t < 3600]
        if len(recenti) >= 5:
            self._send_json(429, {"error": "Troppe voci aggiunte nell'ultima ora (5): riprova più tardi."})
            return
        type(self).aggiunte_voci = recenti + [adesso]
        proprietario, nome = voce_info
        try:
            nuovo = add_shared_voice(api_key, proprietario, voce, f"Gas - {nome}")
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs aggiunta voce status=%s: %s", exc.status, exc.message)
            if exc.status == 200:   # V-2 bot #326: ha risposto «ok» senza un id leggibile
                self._send_json(502, {"error": "Esito incerto: ElevenLabs ha risposto ma senza l'id "
                                               "della voce. Controlla l'account prima di riprovare."})
                return
            self._send_json(502, {"error": f"ElevenLabs non ha aggiunto la voce: {exc.message}"})
            return
        except OSError as exc:
            log.warning("ElevenLabs aggiunta voce rete: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs"})
            return
        self._send_json(200, {"id": nuovo, "nome": nome})

    def _prova_voce(self, raw: bytes) -> None:
        """POST /voci/prova {"voce": id | "piper", "frase": 0..N-1} → audio della frase
        fissa con quella voce. Tetto proprio (GAS_VOICE_MAX_PROVE_ORA, default 40/ora):
        ogni prova spende caratteri ElevenLabs."""
        try:
            data = json.loads(raw) if raw else {}
            voce = data.get("voce")
            frase = data.get("frase", 0)
        except (ValueError, AttributeError):
            self._send_json(400, {"error": "Body JSON non valido"})
            return
        if not isinstance(frase, int) or isinstance(frase, bool) or not 0 <= frase < len(prova_voci.FRASI_PROVA):
            self._send_json(400, {"error": "Frase di prova non valida"})
            return
        if voce != prova_voci.PIPER and not prova_voci.voce_valida(voce):
            self._send_json(400, {"error": "Voce non valida"})
            return
        if voce != prova_voci.PIPER and voce not in type(self).voci_ammesse:
            self._send_json(409, {"error": "Voce non nell'elenco: ricarica la pagina «prova voci» "
                                           "(si provano solo le voci elencate, mai cloni)"})
            return
        testo = prova_voci.FRASI_PROVA[frase]
        if voce == prova_voci.PIPER:
            modello = prova_voci.piper_disponibile()
            if modello is None:
                self._send_json(503, {"error": "Piper non disponibile: servono il comando "
                                               "«piper» e GAS_PIPER_MODEL nel .env"})
                return
            try:
                audio = prova_voci.sintetizza_piper(testo, modello)
            except (OSError, subprocess.SubprocessError) as exc:
                log.warning("Piper errore: %s", type(exc).__name__)
                self._send_json(502, {"error": "Piper non è riuscito a parlare"})
                return
            self._send_audio(audio, "audio/wav")
            return
        # V-3 bot #326: il tetto conta solo le prove con ElevenLabs; Piper (locale e gratis) no
        adesso = time.monotonic()
        recenti = [t for t in type(self).prove_voci if adesso - t < 3600]
        try:
            tetto = max(1, int(os.environ.get("GAS_VOICE_MAX_PROVE_ORA", "") or 40))
        except ValueError:
            tetto = 40
        if len(recenti) >= tetto:
            self._send_json(429, {"error": f"Troppe prove di voce nell'ultima ora ({tetto}, "
                                           "GAS_VOICE_MAX_PROVE_ORA). Riprova più tardi."})
            return
        api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
        if not api_key:
            self._send_json(503, {"error": "TTS non disponibile: ELEVENLABS_API_KEY non configurata"})
            return
        type(self).prove_voci = recenti + [adesso]
        try:
            audio = synthesize_speech(testo, api_key, voce)
        except ElevenLabsTTSError as exc:
            log.warning("ElevenLabs prova voce status=%s: %s", exc.status, exc.message)
            self._send_json(502, {"error": f"Errore TTS ElevenLabs: {exc.message}"})
            return
        except OSError as exc:
            log.warning("ElevenLabs prova voce rete: %s", exc)
            self._send_json(502, {"error": "Errore di rete verso ElevenLabs TTS"})
            return
        self._send_audio(audio)

    do_PUT = _method_not_allowed
    do_DELETE = _method_not_allowed
    do_PATCH = _method_not_allowed


def _carica_env() -> None:
    """Carica il `.env` accanto a gas.py come fa la CLI di Gas (V-1 bot #304: senza,
    GAS_VOCE_FORTE scritto nel `.env` restava spento senza segnale). Stesse regole di
    gas._carica_dotenv (la shell vince, GAS_NO_DOTENV=1 lo spegne). Fail-safe §9."""
    try:
        from gas import _carica_dotenv
        _carica_dotenv()
    except Exception as exc:  # gas.py assente o rotto: si prosegue con l'ambiente
        log.warning(".env non caricato dal server voce: %s", type(exc).__name__)


def run_server(root_dir: Optional[str] = None) -> int:
    """Avvia il server HTTP voice. Blocca fino a KeyboardInterrupt.
    Exit code: 0 = uscita pulita, 1 = configurazione mancante."""

    # V2 (V-3 ve #304): import e kernel richiedono qualche secondo, prima di ogni altra riga
    print("… gas voice: avvio in corso (carico Gas, qualche secondo)…", flush=True)
    root = Path(root_dir or os.getcwd()).resolve()
    import sys as _sys
    _sys.path.insert(0, str(root if (root / "gas.py").exists() else root.parent))
    _carica_env()

    token = os.environ.get("GAS_VOICE_TOKEN", "").strip()
    if not token:
        print("✗ gas voice: GAS_VOICE_TOKEN non configurato (fail-closed).")
        print("  Genera un token casuale e impostalo: export GAS_VOICE_TOKEN=$(openssl rand -hex 32)")
        return 1

    bind = (os.environ.get("GAS_VOICE_BIND") or "127.0.0.1").strip() or "127.0.0.1"
    try:
        port = int(os.environ.get("GAS_VOICE_PORT") or "8765")
    except ValueError:
        print("✗ gas voice: GAS_VOICE_PORT non è un numero intero valido.")
        return 1

    if _bind_tutte_le_interfacce(bind):
        # bot #358 V-1: mai su tutte le interfacce, nemmeno con la rete privata dichiarata
        print(f"✗ gas voice: GAS_VOICE_BIND={bind} ascolterebbe su tutte le interfacce, anche pubbliche.")
        print("  Usa 127.0.0.1 oppure l'indirizzo del tunnel privato (con GAS_VOICE_RETE_PRIVATA=1).")
        return 1

    if not _bind_locale(bind) and not _bind_ip_letterale(bind):
        # R-727-1-M2: un nome host o una forma abbreviata potrebbe legarsi a tutte le interfacce
        print(f"✗ gas voice: GAS_VOICE_BIND={bind} non è un indirizzo IPv4 scritto per intero.")
        print("  Fuori da 127.0.0.1 usa l'indirizzo IPv4 del tunnel privato, non un nome né IPv6.")
        return 1

    if not _bind_locale(bind) and not _env_acceso("GAS_VOICE_RETE_PRIVATA"):
        # R8 fetta 1 (fail-closed): fuori da 127.0.0.1 il traffico è in chiaro (token, audio,
        # risposte); si parte solo dentro una rete privata cifrata dichiarata (tunnel)
        print(f"✗ gas voice: GAS_VOICE_BIND={bind} non è locale e la connessione è in chiaro.")
        print("  Usa un tunnel privato (es. Tailscale) e dichiaralo con GAS_VOICE_RETE_PRIVATA=1,")
        print("  oppure resta su 127.0.0.1. Vedi reports/proposta_voce_sicura.md.")
        return 1

    from gas import GasKernel  # import pigro: non richiede gas.py al semplice import del modulo

    kernel = GasKernel(root_dir=str(root))

    VoiceHandler.kernel = kernel
    VoiceHandler.token = token

    server = HTTPServer((bind, port), VoiceHandler)
    print(f"✓ gas voice: in ascolto su http://{bind}:{port}{_ENDPOINT}")
    if _voce_tutta_forte():
        print("  GAS_VOCE_FORTE acceso: ogni richiesta va al solo cervello forte.")
    print("  Ctrl-C per uscire.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ gas voice: interruzione ricevuta, uscita.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":  # avvio: python -m modules.voice.server (dalla cartella di Gas)
    import sys as _sys
    _sys.exit(run_server())
