"""Lettura con lexbor, spenta per default (modules/web/lexbor.py, R-ve246-5, fette 19-21 chat Mani).
Senza selectolax (oggi in CI) i test che lo usano si saltano; quelli del ripiego girano sempre."""
import logging
import threading
import time

import pytest

import modules.web.leggi as web
from modules.web import lexbor

con_lexbor = pytest.mark.skipif(not lexbor._DISPONIBILE, reason="selectolax non installato")


def _testo(pagina: str) -> str:
    return web._componi("http://x.test/", {"tipo": "text/html", "charset": "utf-8", "corpo": pagina.encode(),
                                            "troncato": False})["testo"]


@pytest.fixture
def acceso(monkeypatch):
    monkeypatch.setenv("GAS_WEB_LEXBOR", "1")
    monkeypatch.setattr(lexbor, "_FIGLIO_OK", None)  # la sonda riparte a ogni test
    monkeypatch.setattr(lexbor, "_RIPROVA_DOPO", 0.0)
    monkeypatch.setattr(lexbor, "_SONDE_FALLITE", 0)


def test_spento_per_default(monkeypatch):
    """Senza GAS_WEB_LEXBOR=1 la lettura con lexbor non parte nemmeno."""
    monkeypatch.delenv("GAS_WEB_LEXBOR", raising=False)
    assert not lexbor.attivo()

    def vietato(*a, **k):
        raise AssertionError("lexbor chiamato da spento")
    monkeypatch.setattr(lexbor, "testo_visibile", vietato)
    assert "VIS" in _testo("<p>VIS</p>")


@con_lexbor
@pytest.mark.parametrize("pagina, visibili, nascosti", [
    # R-ve246-5: il browser ignora «</canvas>» e «</object>» quando sopra c'è un elemento che li
    # ferma, e il resto resta dentro; la lettura di leggi.py lo mostrava
    ("<p>W0</p><canvas>W1<p/></canvas>W2", ("W0",), ("W1", "W2")),
    ("<p>W0</p><canvas><div>W1</canvas>W2", ("W0",), ("W1", "W2")),
    ("<p>W0</p><object> W1 <template> W2 </object> W4 </template> W5", ("W0",), ("W1", "W2", "W4", "W5")),
    ("<p>W0</p><object> W1 <select> W2 </object> W3", ("W0",), ("W1", "W2", "W3")),
    # con gli script attivi noscript è testo grezzo (R-ve261-2)
    ("<p>W0</p><template><noscript></template>W1</noscript>W2", ("W0",), ("W1", "W2")),
    # il titolo va nella sua riga, mai nel testo; quello di svg non conta
    ("<p>W0</p><svg><title>W1</title></svg><title>W2</title>W3", ("W0", "W3", "Titolo: W2"), ("W1",)),
    # pagina a frame: il browser non mostra testo
    ("<frameset>W1</frameset>W2", (), ("W1", "W2")),
    # quello che il browser non mostra mai (fetta 20): attributo hidden (anche su html e body),
    # dialog chiuso, details chiuso tranne il primo summary, datalist, rp
    ("<p>W0</p><div hidden>W1</div><p hidden=until-found>W2</p><dialog>W3</dialog><dialog open>W4</dialog>",
     ("W0", "W4"), ("W1", "W2", "W3")),
    ("<p hidden=false>W1</p><p hidden=''>W2</p><p>W0</p>", ("W0",), ("W1", "W2")),
    # contenuto di riserva di video e audio, interno di meter e progress (R-ve277-5)
    ("<p>W0</p><video>W1<p>W2</p></video><audio controls>W3</audio><meter>W4</meter><progress>W5</progress>W6",
     ("W0", "W6"), ("W1", "W2", "W3", "W4", "W5")),
    ("<body hidden><p>W1</p>", (), ("W1",)),
    ("<html hidden><body><p>W1</p>", (), ("W1",)),
    ("<p>W0</p><details><summary>W1</summary>W2<p>W3</p><summary>W4</summary></details>"
     "<details open><summary>W5</summary>W6</details>", ("W0", "W1", "W5", "W6"), ("W2", "W3", "W4")),
    ("<p>W0</p><datalist><option>W1</datalist><ruby>W2<rp>(</rp><rt>W3</rt><rp>)</rp></ruby>",
     ("W0", "W2", "W3"), ("W1", "(")),
    # del select solo quello che il browser mostra: l'opzione scelta (l'ultima con selected, se
    # no la prima; vale label), tutte con multiple o size > 1 (V-1 bot / V-4 ve #277)
    ("<p>W0</p><select><option>W1</option>W2<div>W3</div><option>W4</option></select>W5",
     ("W0", "W1", "W5"), ("W2", "W3", "W4")),
    ("<select><option selected>W1<option>W2<option selected>W3<option label=W5>W4</select>",
     ("W3",), ("W1", "W2", "W4", "W5")),
    ("<select><option label=W5>W4</select>", ("W5",), ("W4",)),
    # il testo dell'opzione passa dalla stessa visita: niente script né elementi nascosti dentro
    ("<select><option>W1<script>W2</script><span hidden>W3</span></select>", ("W1",), ("W2", "W3")),
    # opzioni dentro contenitori fra il select e l'opzione: fuori dalla «list of options» quelle
    # dentro datalist e quelle non HTML (in svg); object e canvas ci restano e la tendina mostra
    # la scelta (R-527-1, R-ve277-3, R-548-2)
    ("<select><datalist><option selected>W1</datalist><option>W2</select>", ("W2",), ("W1",)),
    ("<select><svg><option selected>W1</svg><option>W2</select>", ("W2",), ("W1",)),
    # un'opzione HTML dentro foreignObject è nella lista, anche sotto un datalist di svg, che non è
    # il datalist HTML (B-547-1, R-548-1)
    ("<select><svg><foreignObject><option selected>W1</option></foreignObject></svg><option>W2</select>",
     ("W1",), ("W2",)),
    ("<select><svg><datalist><foreignObject><option selected>W1</option></foreignObject></datalist></svg>"
     "<option>W2</select>", ("W1",), ("W2",)),
    ("<select><object><option selected>W1</object><option>W2</select>", ("W1",), ("W2",)),
    ("<select><canvas><option selected>W1</canvas><option>W2</select>", ("W1",), ("W2",)),
    ("<select multiple><object><option>W1</object><canvas><option>W2</canvas><option>W3</select>",
     ("W3",), ("W1", "W2")),
    ("<select><!--W1--><div><!--W2--><option>W3</option></div></select>", ("W3",), ("W1", "W2")),
    # hidden e disabled sull'opzione, come il browser (R-527-1, R-527-3): nella lista aperta le
    # nascoste non si vedono; nella tendina si vede la scelta anche se nascosta (segnaposto),
    # se no la prima non disabilitata
    ("<select multiple><option hidden>W1<option>W2</select>", ("W2",), ("W1",)),
    ("<select><option hidden>W1<option>W2</select>", ("W1",), ("W2",)),
    ("<select><option hidden selected>W1<option>W2</select>", ("W1",), ("W2",)),
    ("<select><option disabled>W1<option>W2</select>", ("W2",), ("W1",)),
    # size letto come il browser: spazi, poi le cifre ASCII in testa
    ("<select size=3abc><option>W1<option>W2</select>", ("W1", "W2"), ()),
    ("<select size=' 2'><option>W1<option>W2</select>", ("W1", "W2"), ()),
    ("<select size=1_0><option>W1<option>W2</select>", ("W1",), ("W2",)),
    ("<select size=\u0663><option>W1<option>W2</select>", ("W1",), ("W2",)),
    # «+2» vale 2; con migliaia di cifre il valore non vale: tendina (V-1, V-3 ve #277 ter)
    ("<select size=+2><option>W1<option>W2</select>", ("W1", "W2"), ()),
    ("<select size=" + "9" * 5000 + "><option>W1<option>W2</select>", ("W1",), ("W2",)),
    ("<select size=0000000000003><option>W1<option>W2</select>", ("W1", "W2"), ()),
    ("<select size=21474836470><option>W1<option>W2</select>", ("W1",), ("W2",)),
    ("<select size=2147483647><option>W1<option>W2</select>", ("W1", "W2"), ()),
    ("<select size=2147483648><option>W1<option>W2</select>", ("W1",), ("W2",)),
    # la scelta della tendina sulla «list of options» dello standard: conta anche l'opzione in un
    # sotto-albero nascosto, l'optgroup disabled più vicino la disabilita (R-ve277-3, R-529-1)
    ("<select><div hidden><option selected>W1</option></div><option>W2</select>", ("W1",), ("W2",)),
    ("<select><optgroup disabled><div><option>W1</div></optgroup><option>W2</select>", ("W2",), ("W1",)),
    ("<select multiple><div hidden><option>W1</div><option>W2</select>", ("W2",), ("W1",)),
    # un optgroup dentro un altro non dà opzioni
    ("<select><optgroup><div><optgroup><option>W1</optgroup></div></optgroup><option>W2</select>", ("W2",), ("W1",)),
    # un title HTML dentro foreignObject o mi vale come titolo; quello di svg no (R-520-4)
    ("<svg><foreignObject><title>W1</title></foreignObject></svg><title>W2</title><p>W0</p>",
     ("W0", "Titolo: W1"), ("W2",)),
    ("<math><mi><title>W1</title></mi></math><p>W0</p>", ("W0", "Titolo: W1"), ()),
    ("<math><annotation-xml><title>W1</title></annotation-xml></math><math><annotation-xml encoding=TEXT/html>"
     "<title>W2</title></annotation-xml></math><p>W0</p>", ("W0", "Titolo: W2"), ("W1",)),
    # il punto d'integrazione vale solo nel suo namespace: desc in math, mi in svg, math dentro
    # svg, svg dentro mrow non riportano a HTML (B-547-1)
    ("<math><desc><title>W1</title></desc></math><svg><mi><title>W2</title></mi></svg><svg><math><mi><title>W3"
     "</title></mi></math></svg><math><mrow><svg><foreignObject><title>W4</title></foreignObject></svg></mrow>"
     "</math><title>W5</title><p>W0</p>", ("W0", "Titolo: W5"), ("W1", "W2", "W3", "W4")),
    # svg dentro mi è svg (R-548-1)
    ("<math><mi><svg><title>W1</title></svg></mi></math><title>W2</title><p>W0</p>", ("W0", "Titolo: W2"), ("W1",)),
    # mglyph dentro mi resta math; svg dentro annotation-xml è svg, col suo foreignObject
    ("<math><mi><mglyph><title>W1</title></mglyph></mi></math><math><annotation-xml><svg><foreignObject>"
     "<title>W2</title></foreignObject></svg></annotation-xml></math><p>W0</p>", ("W0", "Titolo: W2"), ("W1",)),
    ("<select multiple><option>W1<optgroup><option>W2</optgroup></select><select size=3><option>W3"
     "<option>W4</select><select size=x><option>W5<option>W6</select>", ("W1", "W2", "W3", "W4", "W5"), ("W6",)),
    # shadow DOM dichiarativo come il browser (scelta 3 dell'operatore, 2026-10-28): si vede lo
    # shadow, negli slot i figli assegnati; i figli non assegnati no
    ("<p>W0</p><div><template shadowrootmode=open>W1<slot></slot></template>W2</div>", ("W0", "W1", "W2"), ()),
    ("<p>W0</p><div><template shadowrootmode=closed>W1</template>W2<b>W3</b></div>", ("W0", "W1"), ("W2", "W3")),
    ("<p>W0</p><x-a><template shadowrootmode=OPEN><slot name=n>W1</slot></template><i slot=n>W2</i>W3</x-a>",
     ("W0", "W2"), ("W1", "W3")),
    ("<p>W0</p><div><template shadowrootmode=open><slot name=n>W1</slot></template>W2</div>", ("W0", "W1"), ("W2",)),
    # host non valido o modo sbagliato: template normale, nascosto; si vedono i figli
    ("<p>W0</p><a><template shadowrootmode=open>W1</template>W2</a><div><template shadowrootmode=x>W3"
     "</template>W4</div><X1><template shadowrootmode=open>W5</template>W6</X1>", ("W0", "W2", "W4", "W6"),
     ("W1", "W3", "W5")),
    # vale solo il primo template; dentro lo shadow valgono le regole di sempre
    ("<p>W0</p><div><template shadowrootmode=open>W1<p hidden>W2</p><script>W3</script></template>"
     "<template shadowrootmode=open>W4</template></div>", ("W0", "W1"), ("W2", "W3", "W4")),
    # testo grezzo, commenti, attributi
    ("<p>W0</p><script>W1</script><!--W2--><a title='W3'>W4</a><textarea>W5</textarea>",
     ("W0", "W4", "W5"), ("W1", "W2", "W3")),
])
def test_lettura_come_il_browser(acceso, pagina, visibili, nascosti):
    t = _testo(pagina)
    assert all(v in t for v in visibili) and not any(n in t for n in nascosti), t


@con_lexbor
@pytest.mark.parametrize("pagina, atteso", [
    ("<div><template shadowrootmode=open>A<slot></slot>B</template>L</div>", "ALB"),
    # al primo slot col nome; gli altri con lo stesso nome mostrano la riserva, anche se il
    # primo è nascosto
    ("<div><template shadowrootmode=open><slot>P</slot><slot>Q</slot></template>L</div>", "LQ"),
    ("<div><template shadowrootmode=open><b hidden><slot></slot></b><slot>Q</slot></template>L</div>", "Q"),
    # il testo va solo allo slot senza nome
    ("<div><template shadowrootmode=open><slot name=n>R</slot>|<slot></slot></template>T<i slot=n>N</i></div>",
     "N|T"),
    # shadow annidati: lo slot dello shadow dentro va ai figli dell'host dentro, cioè allo slot
    # dello shadow fuori, che va ai figli dell'host fuori
    ("<x-a><template shadowrootmode=open>A[<x-b><template shadowrootmode=open>B[<slot></slot>]</template>"
     "<slot></slot></x-b>]</template>L</x-a>", "A[B[L]]"),
    # anche body può essere un host; uno slot fuori dagli shadow mostra il suo contenuto
    ("<body><template shadowrootmode=open>S<slot></slot></template>L<slot>F</slot></body>", "SLF"),
    # un template dentro svg non ha contenuto HTML: niente errore, nessuno shadow (R-539-1)
    ("<svg><x-a><template shadowrootmode=open>S</template>L</x-a></svg><p>P</p>", "SLP"),
    # uno slot dentro svg non è uno slot; i nomi riservati non sono host (R-539-2)
    ("<div><template shadowrootmode=open><svg><slot></slot></svg><slot>Q</slot></template>L</div>", "L"),
    # uno slot in mi dentro svg resta svg: non prende il nome (B-547-1)
    ("<div><template shadowrootmode=open><svg><mi><slot></slot></mi></svg><slot>Q</slot></template>L</div>", "L"),
    # in foreignObject lo slot torna HTML e prende il nome (R-540-1)
    ("<div><template shadowrootmode=open><svg><foreignObject><slot></slot></foreignObject></svg><slot>Q</slot>"
     "</template>L</div>", "LQ"),
    # option dentro option (lexbor e lo standard le annidano): la seconda non è nella lista, si
    # legge la prima col suo testo intero (R-528-3)
    ("<select><option>A<div><option selected>B</select>", "\nAB\n"),
    ("<font-face><template shadowrootmode=open>S</template>L</font-face>", "L"),
    # per lo standard di oggi anche «x-a!» e «x-a:b» sono host («valid element local name» di DOM,
    # V-2 ve #288 riletta alla fonte); validi anche «.» e lettere non ASCII
    ("<x-a!><template shadowrootmode=open>S</template>L</x-a!><x-a:b><template shadowrootmode=open>T"
     "</template>M</x-a:b>", "ST"),
    ("<x.y-é><template shadowrootmode=open>S</template>L</x.y-é>", "S"),
    # il template dello shadow non è un figlio dell'host: col nome di uno slot non gli toglie
    # la riserva (V-3 ve #288)
    ("<div><template shadowrootmode=open slot=n><slot name=n>R</slot></template>L</div>", "R"),
    # dentro un'opzione si legge il suo testo (option.text, i discendenti): lo slot mostra la riserva,
    # non i figli dell'host (V-1 bot #288)
    ("<div><template shadowrootmode=open><select><option><slot>F</slot></option></select></template>L</div>",
     "\nF\n"),
    # shadow vuoto: niente testo, nemmeno i figli dell'host (bot #288 su 759edea)
    ("<div><template shadowrootmode=open></template>L</div>", ""),
    # limite dichiarato: se l'adoption agency sposta il template, l'host perde lo shadow (il
    # browser mostrerebbe «S»; V-1 bot e ve #288 su 6627250)
    ("<b><div><template shadowrootmode=open>S</template>L</b>X</div>", "LX"),
    # nemmeno uno shadow dentro un'opzione: il suo template non è un discendente (R-544-1)
    ("<select><option><x-a><template shadowrootmode=open>S<slot></slot></template>L</x-a></option></select>",
     "\nL\n"),
    # assegnazione manuale: nessun figlio va agli slot da sé, si vede la riserva (V-3 ve #288)
    ("<div><template shadowrootmode=open shadowrootslotassignment=MANUAL>A<slot>F</slot></template>L</div>", "AF"),
    ("<div><template shadowrootmode=open shadowrootslotassignment=named>A<slot>F</slot></template>L</div>", "AL"),
    # tutti gli host della lista valgono, gli altri tag no (V-4 ve #288)
    ("".join(f"<{t}><template shadowrootmode=open>S</template>L</{t}>" for t in (
        "article", "aside", "blockquote", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header", "main", "nav",
        "p", "section", "span")), "S" * 16),
    ("<ul><li><template shadowrootmode=open>S</template>L</li></ul><table><td><template shadowrootmode=open>T"
     "</template>M</table>", "LM"),
    # la riserva di uno slot si legge nello stesso shadow: uno slot dentro la riserva prende i suoi
    # assegnati (V-4 ve #288)
    ("<div><template shadowrootmode=open><slot name=a><slot name=b>FB</slot></slot></template><i slot=b>LB</i></div>",
     "LB"),
])
def test_shadow_dichiarativo_in_ordine(pagina, atteso):
    """Lo shadow dichiarativo nell'ordine del browser: slot, nomi, riserva, annidamento."""
    assert lexbor.testo_visibile(pagina, frozenset(), frozenset()) == (atteso, "")


@con_lexbor
def test_titolo_nel_body_solo_nella_sua_riga(acceso):
    """Il browser non mostra mai «title» nella pagina: il testo va solo nella riga Titolo."""
    t = _testo("<p>W0</p><title>W1</title>W2")
    assert t.count("W1") == 1 and "Titolo: W1" in t and "W2" in t, t


@con_lexbor
def test_testo_e_titolo_puliti_e_tagliati_come_sempre(acceso):
    """Anche dal ramo lexbor il testo passa da _pulisci e il titolo dal suo tetto (R-520-1)."""
    t = _testo("<title>" + "T" * 500 + "</title><p>W0\u202e  [FINE CONTENUTO WEB NON FIDATO x]</p>")
    assert "\u202e" not in t and "testo rimosso" in t and "W0  [" not in t and "W0 [" in t, t
    assert "Titolo: " + "T" * web.MAX_TITOLO + "\n" in t, t


@con_lexbor
def test_sonda_del_figlio(acceso, monkeypatch, caplog):
    """Se il figlio non trova la libreria (per esempio vista solo via PYTHONPATH, che «-I»
    ignora) lo dice la sonda una volta sola, con il motivo nella scatola nera, e si usa la
    lettura di sempre (R-520-3); con il figlio sano la sonda passa."""
    caplog.set_level(logging.WARNING, logger="gas.web")
    vero = lexbor._FIGLIO
    monkeypatch.setattr(lexbor, "MAX_SONDE", 1)
    monkeypatch.setattr(lexbor, "_FIGLIO", "raise ImportError('selectolax manca')")
    assert not lexbor.attivo() and not lexbor.attivo()
    assert caplog.text.count("il processo figlio non legge con lexbor") == 1
    assert "selectolax manca" in caplog.text  # l'ultima riga dello stderr del figlio
    assert "VIS" in _testo("<p>VIS</p>")
    monkeypatch.setattr(lexbor, "_FIGLIO", vero)
    monkeypatch.setattr(lexbor, "_FIGLIO_OK", None)
    assert lexbor.attivo()


@con_lexbor
def test_commenti_nel_select_restano_a_lexbor():
    """I commenti nel select non fanno cadere il figlio nel ripiego: la guardia sui nodi non
    elemento si vede solo chiamando lexbor direttamente (R-528-1)."""
    letto = lexbor.testo_visibile("<select><!--W1--><div><!--W2--><option>W3</option></div></select>",
                                  frozenset(), frozenset())
    assert letto is not None and letto[0].split() == ["W3"], letto


@con_lexbor
def test_molte_opzioni_annidate_restano_lineari():
    """Le opzioni si raccolgono scendendo una volta sola: 2000 div annidati e 20 mila opzioni
    stanno dentro il tempo massimo del figlio (R-527-2: con la risalita quadratica il figlio lo
    superava). Niente soglia in secondi qui: su una macchina lenta darebbe falsi rossi (R-bot277-4)."""
    pagina = "<select multiple>" + "<div>" * 2000 + "<option>x</option>" * 20000
    assert lexbor.testo_visibile(pagina, frozenset(), frozenset()) is not None


@con_lexbor
def test_size_enorme_non_fa_cadere_il_figlio():
    """Un size di migliaia di cifre non fa cadere il figlio sul ripiego (V-1 ve #277 ter)."""
    pagina = "<select size=" + "9" * 5000 + "><option>A<option>B</select>"
    assert lexbor.testo_visibile(pagina, frozenset(), frozenset()) == ("\nA\n", "")


@pytest.mark.parametrize("valore, atteso", [
    ("0", 0), ("000", 0), (" +0", 0), ("0x", 0), ("007", 7), ("2147483647", 2147483647),
    ("2147483648", None), ("", None), (None, None), ("+", None), ("x0", None), ("-1", None),
    ("-0", 0), (" -000", 0), ("-", None), ("+-1", None), ("--0", None),
])
def test_intero_come_il_browser(valore, atteso):
    """intero() del figlio, presa dal suo sorgente: gira anche senza selectolax; «0» vale 0,
    non None (R-bot280-1, R-536-1)."""
    import ast
    albero = ast.parse(lexbor._FIGLIO)
    nodo = next(n for n in albero.body if isinstance(n, ast.FunctionDef) and n.name == "intero")
    spazio: dict = {}
    exec(compile(ast.Module([nodo], type_ignores=[]), "_FIGLIO", "exec"), spazio)
    assert spazio["intero"](valore) == atteso


@con_lexbor
def test_sonda_riuscita_non_aspetta_il_lock(acceso):
    """Dopo una sonda riuscita la lettura con lexbor resta accesa anche mentre il lock è preso
    (V-3(c) ve #277 ter: senza il controllo iniziale chi arriva leggerebbe col ripiego)."""
    lexbor._FIGLIO_OK = True
    assert lexbor._SONDA.acquire(blocking=False)
    try:
        assert lexbor.attivo()
    finally:
        lexbor._SONDA.release()


@con_lexbor
def test_titolo_con_molti_title_in_svg_entro_il_tempo():
    """Il titolo si cerca scendendo una volta sola: migliaia di title in svg sotto mille g non
    superano TEMPO_MAX (prima la risalita da ogni title era quadratica, B-547-1)."""
    pagina = "<svg>" + "<g>" * 1000 + "<title>t</title>" * 10000 + "</svg><title>Y</title><p>x"
    assert lexbor.testo_visibile(pagina, frozenset({"svg"}), frozenset()) == ("x", "Y")


def test_spento_fuori_da_linux_senza_sonde(acceso, monkeypatch):
    """Fuori da Linux la lettura con lexbor è spenta subito, senza sonde (R-ve277-4)."""
    monkeypatch.setattr(lexbor, "_DISPONIBILE", True)
    monkeypatch.setattr(lexbor.sys, "platform", "darwin")

    def vietato(*a, **k):
        raise AssertionError("sonda fuori da Linux")
    monkeypatch.setattr(lexbor, "_esegui", vietato)
    assert not lexbor.attivo() and lexbor._SONDE_FALLITE == 0


def test_sonda_gia_fatta_da_chi_teneva_il_lock(acceso, monkeypatch):
    """Chi prende il lock dopo una sonda riuscita di un altro non ne fa una seconda: il controllo
    si ripete sotto il lock (R-526-1)."""
    monkeypatch.setattr(lexbor, "_DISPONIBILE", True)

    class Lock:
        def acquire(self, blocking=True):
            lexbor._FIGLIO_OK = True  # l'altro ha finito la sonda mentre si aspettava il lock
            return True

        def release(self):
            pass
    monkeypatch.setattr(lexbor, "_SONDA", Lock())

    def vietato(*a, **k):
        raise AssertionError("seconda sonda")
    monkeypatch.setattr(lexbor, "_esegui", vietato)
    assert lexbor.attivo()


def test_ultima_riga_dello_stderr_pulita():
    """Nella scatola nera va solo l'ultima riga dello stderr del figlio, stampabile e corta (R-525-3)."""
    assert lexbor._ultima_riga("Traceback\n  ...\nImportError: x\u202ey\x00z\n".encode()) == "ImportError: x?y?z"
    assert lexbor._ultima_riga(("E" * 500).encode()) == "E" * 200
    assert lexbor._ultima_riga(b"") == "" and lexbor._ultima_riga(b"\xff\xfe") == "\ufffd\ufffd"


@con_lexbor
def test_una_sonda_alla_volta(acceso, monkeypatch):
    """Con molte letture insieme alla prima chiamata parte una sola sonda; chi arriva mentre
    gira usa la lettura di sempre (R-521-1)."""
    vero = lexbor.subprocess.run
    sonde = []

    def spia(argomenti, **opzioni):
        if opzioni.get("input") == b"<title>t</title><p>x</p>":
            sonde.append(1)
            time.sleep(0.3)
        return vero(argomenti, **opzioni)
    monkeypatch.setattr(lexbor.subprocess, "run", spia)
    esiti = []
    fili = [threading.Thread(target=lambda: esiti.append(lexbor.attivo())) for _ in range(8)]
    for f in fili:
        f.start()
    for f in fili:
        f.join()
    # chi arriva mentre la sonda gira non aspetta: ha False e legge come sempre (R-525-2)
    assert len(sonde) == 1 and esiti.count(True) >= 1 and esiti.count(False) >= 1 and lexbor.attivo()


@con_lexbor
def test_sonda_oltre_il_tempo_si_riprova(acceso, monkeypatch, caplog):
    """Una sonda finita oltre il tempo (avvio a freddo) non spegne la lettura per sempre: si
    riprova dopo RIPROVA_SONDA secondi (R-521-2; anche un errore si riprova, fino a MAX_SONDE)."""
    caplog.set_level(logging.WARNING, logger="gas.web")
    monkeypatch.setattr(lexbor, "TEMPO_MAX", 0.01)
    monkeypatch.setattr(lexbor, "RIPROVA_SONDA", 0.2)
    assert not lexbor.attivo() and lexbor._FIGLIO_OK is None and "si riprova" in caplog.text
    assert not lexbor.attivo() and caplog.text.count("si riprova") == 1  # prima di RIPROVA_SONDA non si risonda
    monkeypatch.setattr(lexbor, "TEMPO_MAX", 4.0)
    time.sleep(0.25)
    assert lexbor.attivo()


@con_lexbor
def test_sonda_fallita_si_riprova_poi_si_spegne(acceso, monkeypatch, caplog):
    """Un errore della sonda (anche passeggero, come un fork negato) non spegne subito: si
    riprova dopo RIPROVA_SONDA, e solo dopo MAX_SONDE fallimenti si spegne (V-3 bot e ve #277)."""
    caplog.set_level(logging.WARNING, logger="gas.web")
    vero = lexbor.subprocess.run
    monkeypatch.setattr(lexbor, "RIPROVA_SONDA", 0.0)
    guasti = [1]

    def a_volte(argomenti, **opzioni):
        if guasti:
            guasti.pop()
            raise BlockingIOError("fork negato")
        return vero(argomenti, **opzioni)
    monkeypatch.setattr(lexbor.subprocess, "run", a_volte)
    assert not lexbor.attivo() and "si riprova" in caplog.text and lexbor._FIGLIO_OK is None
    assert lexbor.attivo()  # il guasto era passeggero
    monkeypatch.setattr(lexbor, "_FIGLIO_OK", None)
    monkeypatch.setattr(lexbor, "_SONDE_FALLITE", 0)
    monkeypatch.setattr(lexbor, "_FIGLIO", "raise ImportError('selectolax manca')")
    for _ in range(lexbor.MAX_SONDE):
        assert not lexbor.attivo()
    assert lexbor._FIGLIO_OK is False and "sonde fallite" in caplog.text


@con_lexbor
def test_fuori_da_linux_il_figlio_si_rifiuta(acceso, monkeypatch, caplog):
    """Il tetto di memoria (RLIMIT_AS) vale solo su Linux: altrove il figlio esce con 3 e la
    lettura resta quella di sempre (V-1 bot #275)."""
    caplog.set_level(logging.WARNING, logger="gas.web")
    monkeypatch.setattr(lexbor, "MAX_SONDE", 1)
    monkeypatch.setattr(lexbor, "_FIGLIO", lexbor._FIGLIO.replace('!= "linux"', '!= "nessuno"'))
    assert not lexbor.attivo() and "solo Linux" in caplog.text
    assert "VIS" in _testo("<p>VIS</p>")


@con_lexbor
def test_blocchi_a_capo(acceso):
    assert "W0\nW1" in _testo("<p>W0</p>W1") and "W2 W3" in _testo("<p>W2 <b>W3</b></p>")


@con_lexbor
def test_oltre_il_tempo_si_usa_la_lettura_di_sempre(acceso, monkeypatch, caplog):
    """Una pagina che costa troppo a lexbor (quadratica) si ferma al tempo massimo: il figlio
    muore e si legge come prima (FAIL-SAFE §9)."""
    monkeypatch.setattr(lexbor, "TEMPO_MAX", 0.3)
    caplog.set_level(logging.WARNING, logger="gas.web")
    assert lexbor.testo_visibile("<div>" * 100000 + "X", frozenset(), frozenset()) is None
    assert "oltre" in caplog.text
    assert "VIS" in _testo("<div>" * 100000 + "VIS")


@con_lexbor
@pytest.mark.parametrize("figlio", ["import os; os.abort()", "import sys; sys.stdout.write('non json')",
                                    "raise MemoryError"])
def test_figlio_rotto_si_usa_la_lettura_di_sempre(acceso, monkeypatch, caplog, figlio):
    """Un crash del codice C, un'uscita sbagliata o la memoria finita uccidono il figlio, non Gas."""
    monkeypatch.setattr(lexbor, "_FIGLIO", figlio)
    caplog.set_level(logging.WARNING, logger="gas.web")
    assert lexbor.testo_visibile("<p>X</p>", frozenset(), frozenset()) is None
    assert "fallita" in caplog.text
    assert "VIS" in _testo("<p>VIS</p>")


def test_senza_libreria_si_usa_la_lettura_di_sempre(acceso, monkeypatch):
    monkeypatch.setattr(lexbor, "_DISPONIBILE", False)
    assert not lexbor.attivo() and lexbor.testo_visibile("<p>X</p>", frozenset(), frozenset()) is None
    assert "VIS" in _testo("<p>VIS</p>")


@con_lexbor
def test_testo_non_codificabile_si_usa_la_lettura_di_sempre(acceso):
    """Un surrogato solitario non passa al figlio: None, e leggi.py legge come prima."""
    assert lexbor.testo_visibile("<p>\udc80</p>", frozenset(), frozenset()) is None


@con_lexbor
def test_xhtml_resta_a_leggi(acceso, monkeypatch):
    """lexbor legge solo HTML: le pagine application/xhtml+xml restano alla lettura di sempre."""
    def vietato(*a, **k):
        raise AssertionError("lexbor chiamato su XHTML")
    monkeypatch.setattr(lexbor, "testo_visibile", vietato)
    t = web._componi("http://x.test/", {"tipo": "application/xhtml+xml", "charset": "utf-8",
                                         "corpo": b"<p>VIS</p>", "troncato": False})["testo"]
    assert "VIS" in t


@con_lexbor
def test_figlio_non_carica_moduli_dalla_cartella(monkeypatch, tmp_path):
    """Con «-I» il figlio non mette la cartella corrente nel percorso dei moduli: un
    «resource.py» scritto lì (Gas può scrivere file) non viene eseguito (V-2 ve #275)."""
    spia = tmp_path / "ESEGUITO"
    (tmp_path / "resource.py").write_text(f"open({str(spia)!r}, 'w').write('x')\n")
    monkeypatch.chdir(tmp_path)
    assert lexbor.testo_visibile("<p>W0</p>", frozenset(), frozenset()) == ("W0", "")
    assert not spia.exists()


@con_lexbor
def test_figlio_isolato_e_con_tetto_di_memoria(monkeypatch):
    """Il figlio parte con «-I», senza l'ambiente del padre (niente LD_PRELOAD e simili) e
    con il tetto di memoria: sotto l'ingombro dell'interprete (circa 16 MB) non riesce nemmeno a
    caricare la libreria, con margine ampio dalla soglia di riuscita (V-2 ve #275, R-523-1, R-524-1)."""
    vero = lexbor.subprocess.run
    visti = []

    def spia(argomenti, **opzioni):
        visti.append((argomenti, opzioni))
        return vero(argomenti, **opzioni)
    monkeypatch.setattr(lexbor.subprocess, "run", spia)
    assert lexbor.testo_visibile("<p>W0</p>", frozenset(), frozenset()) == ("W0", "")
    argomenti, opzioni = visti[-1]
    assert argomenti[1] == "-I" and opzioni["env"] == {}
    monkeypatch.setattr(lexbor, "MEMORIA_MAX", 4 << 20)
    assert lexbor.testo_visibile("<p>W0</p>", frozenset(), frozenset()) is None
