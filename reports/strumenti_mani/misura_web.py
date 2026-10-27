"""Strumento di misura della chat Mani (fette 19-20): lettura con lexbor contro la lettura di sempre.
Non è un test, non gira in CI ed è fuori dal perimetro di review (sta in reports/, nessuno lo
importa). Serve html5lib (oracolo) e selectolax. I percorsi del corpus sono quelli
dell'ambiente cloud del 2026-10-27.
Uso: python3 reports/strumenti_mani/misura_web.py corpus|fuzz SEED N|tempi|robustezza SEED N
(con IN_PROCESSO=1 il codice del figlio gira nel processo, senza tetto di memoria)."""
import os, re, sys, time, random, logging, subprocess, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
logging.disable(logging.CRITICAL)
import modules.web.leggi as w
import html5lib

def leggi(html: str, lex: bool) -> str:
    os.environ["GAS_WEB_LEXBOR"] = "1" if lex else "0"
    t = w._componi("http://x.test/", {"tipo": "text/html", "charset": "utf-8", "corpo": html.encode("utf-8", "replace"), "troncato": False})["testo"]
    righe = t.split("\n")[2:-1]
    return "\n".join(r for r in righe if not r.startswith("Titolo: "))

NASC = set(w._TAG_NASCOSTI) | {"title", "head"}
def oracolo_html5lib(html: str) -> str:
    doc = html5lib.parse(html, namespaceHTMLElements=False)
    out, pila = [], [("el", doc)]
    while pila:
        tipo, x = pila.pop()
        if tipo == "testo":
            out.append(x); continue
        tag = x.tag.rsplit("}", 1)[-1] if isinstance(x.tag, str) else ""
        if tag in NASC:
            continue
        seq = [("testo", x.text)] if x.text else []
        for f in x:
            seq.append(("el", f))
            if f.tail: seq.append(("testo", f.tail))
        pila.extend(reversed(seq))
    return " ".join(out)

def corpus():
    files = []
    for radice in ("/usr/local/go1.25.1/doc", "/opt/node22/lib/node_modules/npm/docs/output", "/usr/share/doc", "/opt/google-cloud-sdk", "/root/.rustup/toolchains", "/usr/lib/libreoffice", "/usr/lib/python3"):
        files += glob.glob(radice + "/**/*.htm*", recursive=True)
    files = sorted(set(f for f in files if os.path.isfile(f) and os.path.getsize(f) > 2000))
    tot_o = tot_n = 0; ugu = 0; diffs = []
    to = tn = 0.0
    for f in files:
        h = open(f, "rb").read().decode("utf-8", "replace")
        a = time.perf_counter(); o = leggi(h, False); b = time.perf_counter(); n = leggi(h, True); c = time.perf_counter()
        to += b - a; tn += c - b
        po, pn = o.split(), n.split()
        tot_o += len(po); tot_n += len(pn)
        if po == pn: ugu += 1
        else:
            so, sn = set(po), set(pn)
            diffs.append((f, len(po), len(pn), sorted(so - sn)[:6], sorted(sn - so)[:6]))
    print(f"pagine {len(files)}, testo identico (parole) {ugu}, diverse {len(diffs)}")
    print(f"parole totali oggi {tot_o}, lexbor {tot_n}; tempo totale oggi {to:.2f}s, lexbor {tn:.2f}s")
    diffs.sort(key=lambda d: -abs(d[1] - d[2]))
    for d in diffs[:12]:
        print("  ", d[0][-70:], "oggi", d[1], "lexbor", d[2], "| solo oggi:", d[3], "| solo lexbor:", d[4])

ATOMI = ["<canvas>", "</canvas>", "<object>", "</object>", "<template>", "</template>", "<svg>", "</svg>", "<math>", "<mi>",
         "<foreignObject>", "<desc>", "<table>", "<td>", "<tr>", "</table>", "<select>", "</select>", "<p>", "</p>", "<p/>",
         "<div>", "</div>", "<b>", "</b>", "<button>", "<ul>", "<li>", "</ul>", "<frameset>", "<title>", "</title>", "<title/>",
         "<script>", "</script>", "<style>", "</style>", "<!--", "-->", "<textarea>", "</textarea>", "<iframe>", "</iframe>",
         "<a title='</canvas>'>", "<marquee>", "</marquee>", "<font color=r>", "<br>", "<img>", "<h1>", "</h1>", " "]
M = re.compile(r"T\d+x")
def fuzz(seed, n):
    rng = random.Random(seed); f_o = f_n = 0; p_o = p_n = 0; es = []
    for _ in range(n):
        pezzi = []
        for k in range(rng.randint(2, 12)):
            pezzi.append(rng.choice(ATOMI)); pezzi.append(f"T{k}x")
        p = "".join(pezzi)
        orc = set(M.findall(oracolo_html5lib(p)))
        o = set(M.findall(leggi(p, False))); nn = set(M.findall(leggi(p, True)))
        if o - orc: f_o += 1
        if nn - orc:
            f_n += 1
            if len(es) < 6: es.append((p, sorted(nn - orc)))
        if orc - o: p_o += 1
        if orc - nn: p_n += 1
    print(f"seed {seed}: {n} pagine; oracolo html5lib. FUGHE oggi {f_o}, lexbor {f_n}; PERDITE oggi {p_o}, lexbor {p_n}")
    for e in es: print("   fuga lexbor:", e)

def tempi():
    casi = {
        "testo 2 MB": "<p>" + "parola " * 300000 + "</p>",
        "100k div annidati": "<div>" * 100000 + "X" + "</div>" * 100000,
        "400k <svg>": "<svg>" * 400000,
        "200k tag p": "<p>x</p>" * 200000,
        "100k attributi": "<a " + " ".join(f"a{i}=b" for i in range(100000)) + ">X",
        "200k template": "<template>" * 200000 + "X",
        "commento senza fine": "<!--" + "x" * 2000000,
        "300k tabelle": "<table><td>" * 30000,
    }
    for nome, h in casi.items():
        for lex in (False, True):
            a = time.perf_counter(); leggi(h, lex); b = time.perf_counter()
            print(f"{nome:22s} {'lexbor' if lex else 'oggi  '} {b - a:6.2f}s")

def robustezza(seed, n):
    rng = random.Random(seed)
    from selectolax.lexbor import LexborHTMLParser
    pezzi = ATOMI + ["\x00", "�", "&#0;", "&#xD800;", "&#99999999;", "<![CDATA[", "]]>", "<?x", "</", "<!", "\udc80", "é", "<" * 3]
    for _ in range(n):
        s = "".join(rng.choice(pezzi) for _ in range(rng.randint(1, 60)))
        try:
            os.environ["GAS_WEB_LEXBOR"] = "1"
            w._componi("http://x.test/", {"tipo": "text/html", "charset": "utf-8", "corpo": s.encode("utf-8", "surrogatepass"), "troncato": False})
        except Exception as e:
            print("ECCEZIONE", type(e).__name__, repr(s)[:120]); return
    print(f"seed {seed}: {n} pagine senza eccezioni né crash")


def _in_processo():
    """Per il fuzz: lo stesso codice del figlio, eseguito qui (senza tetto di memoria)."""
    import io, json
    from modules.web import lexbor as L
    codice = "\n".join(r for r in L._FIGLIO.splitlines() if "setrlimit" not in r)
    def tv(html, nascosti, blocchi):
        out = io.StringIO(); vecchi = sys.argv, sys.stdin, sys.stdout
        sys.argv = ["x", "0", json.dumps(sorted(nascosti)), json.dumps(sorted(blocchi))]
        sys.stdin = io.TextIOWrapper(io.BytesIO(html.encode("utf-8")), encoding="utf-8"); sys.stdout = out
        try:
            exec(codice, {"__name__": "figlio"})
        finally:
            sys.argv, sys.stdin, sys.stdout = vecchi
        d = json.loads(out.getvalue()); return d["testo"], d["titolo"]
    L.testo_visibile = tv
if os.environ.get("IN_PROCESSO") == "1":
    _in_processo()

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "corpus": corpus()
    elif cmd == "fuzz": fuzz(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "tempi": tempi()
    elif cmd == "robustezza": robustezza(int(sys.argv[2]), int(sys.argv[3]))
