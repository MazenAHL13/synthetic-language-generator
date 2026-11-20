"""
chulupi_oraciones.py — Constructor de oraciones de referencia de Chulupi Lang v1.1.

Convierte una idea (esquema de §11 de chulupi_lang_spec.md) en:
  - la oración en modo B, la oración en modo A y la oración española (§9, §10);
  - la lista de palabras con sus ids (para el validador de §13);
  - las reglas [DERIVADA] que usa (DV-01 a DV-13, CH-702).

Uso:
    from chulupi_oraciones import generar
    r = generar(idea)      # r["b"], r["a"], r["es"], r["palabras"], r["dv"]

El léxico incluido es el de ejemplo (§4.1, ids L0001–L0025) más el léxico de
validación con raíces reales (§12.1, ids LV01–LV18), que solo sirve para pruebas.
"""
from chulupi_motor import construir_palabra

# ------------------------------------------------------------------ léxico
# id: (cat, clase_o_subcat, es_m, es_f, es_pl_m, es_pl_f, genero, contable, raiz)
LEXICO = {
    "L0001": ("N_HUM", "persona", "niño", "niña", "niños", "niñas", "var", "s", "lisqu"),
    "L0002": ("N_HUM", "persona", "hermano", "hermana", "hermanos", "hermanas", "var", "s", "pultiya"),
    "L0003": ("N_HUM", "persona", "maestro", "maestra", "maestros", "maestras", "var", "s", "yaruqhi"),
    "L0004": ("N_HUM", "persona", "mujer", "", "mujeres", "", "f", "s", "simlla"),
    "L0005": ("N_NOHUM", "vivienda", "casa", "", "casas", "", "f", "s", "chimula"),
    "L0006": ("N_NOHUM", "comida", "pan", "", "panes", "", "m", "n", "q'aspi"),
    "L0007": ("N_NOHUM", "lugar", "pueblo", "", "pueblos", "", "m", "s", "wirkha"),
    "L0008": ("N_NOHUM", "animal", "perro", "", "perros", "", "m", "s", "kirpu"),
    "L0009": ("N_NOHUM", "lugar", "mercado", "", "mercados", "", "m", "s", "pinqara"),
    "L0010": ("N_NOHUM", "herramienta", "palo", "", "palos", "", "m", "s", "salmi"),
    "L0011": ("N_NOHUM", "herramienta", "cuchillo", "", "cuchillos", "", "m", "s", "jitqu"),
    "L0012": ("N_NOHUM", "abstracto", "deuda", "", "deudas", "", "f", "s", "ch'alqu"),
    "L0013": ("V_MOV", "-", "ir", "", "", "", "-", "-", "tisqa"),
    "L0014": ("V_MOV", "-", "venir", "", "", "", "-", "-", "pajlla"),
    "L0015": ("V_INTR", "-", "dormir", "", "", "", "-", "-", "nuyk'a"),
    "L0016": ("V_TR", "-", "comer", "", "", "", "-", "-", "lamch'a"),
    "L0017": ("V_TR", "-", "ver", "", "", "", "-", "-", "ch'ixra"),
    "L0018": ("V_DITR", "-", "dar", "", "", "", "-", "-", "tulpha"),
    "L0019": ("V_TR", "-", "comprar", "", "", "", "-", "-", "nirqa"),
    "L0020": ("V_TR", "-", "cortar", "", "", "", "-", "-", "k'iyma"),
    "L0021": ("ADJ", "tamano", "grande", "grande", "grandes", "grandes", "-", "-", "jumpu"),
    "L0022": ("ADJ", "color", "rojo", "roja", "rojos", "rojas", "-", "-", "q'ulli"),
    "L0023": ("ADV_T", "pasado", "ayer", "", "", "", "-", "-", "jaskhi"),
    "L0024": ("ADV_T", "futuro", "mañana", "", "", "", "-", "-", "sik'uyu"),
    "L0025": ("ADV_T", "presente", "ahora", "", "", "", "-", "-", "nuspi"),
    # léxico de validación (raíces reales; solo pruebas, §12.1)
    "LV01": ("N_HUM", "persona", "niño", "niña", "niños", "niñas", "var", "s", "wawa"),
    "LV02": ("N_NOHUM", "comida", "pan", "", "panes", "", "m", "n", "t'ant'a"),
    "LV03": ("V_DITR", "-", "dar", "", "", "", "-", "-", "chura"),
    "LV04": ("N_HUM", "persona", "padre", "", "padres", "", "m", "s", "tata"),
    "LV05": ("N_NOHUM", "lugar", "pueblo", "", "pueblos", "", "m", "s", "marka"),
    "LV06": ("V_MOV", "-", "venir", "", "", "", "-", "-", "juta"),
    "LV07": ("V_MOV", "-", "ir", "", "", "", "-", "-", "sara"),
    "LV08": ("V_INTR", "-", "comer", "", "", "", "-", "-", "manq'a"),
    "LV09": ("V_TR", "-", "comer", "", "", "", "-", "-", "manq'a"),
    "LV10": ("N_NOHUM", "animal", "perro", "", "perros", "", "m", "s", "anu"),
    "LV11": ("N_NOHUM", "vivienda", "casa", "", "casas", "", "f", "s", "uta"),
    "LV12": ("N_HUM", "persona", "hermano", "hermana", "hermanos", "hermanas", "var", "s", "jila"),
    "LV13": ("N_HUM", "persona", "autoridad", "", "autoridades", "", "f", "s", "jilaqata"),
    "LV14": ("N_HUM", "persona", "mamá", "", "mamás", "", "f", "s", "mama"),
    "LV15": ("N_NOHUM", "animal", "zorro", "", "zorros", "", "m", "s", "tiwula"),
    "LV16": ("N_NOHUM", "animal", "ganso", "", "gansos", "", "m", "s", "wallata"),
    "LV17": ("V_INTR", "-", "encontrarse", "", "", "", "-", "-", "jikisi"),
    "LV18": ("V_TR", "-", "querer", "", "", "", "-", "-", "muna"),
}

# ------------------------------------------------------------------ español: conjugación
# huecos: 0 = 1sg, 1 = 2sg (tú), 2 = 3sg, 3 = 1pl, 4 = 3pl (ellos / ustedes)
CONJ = {
    "ir": dict(pres="voy vas va vamos van", pret="fui fuiste fue fuimos fueron", fut="iré irás irá iremos irán", part="ido", ger="yendo"),
    "venir": dict(pres="vengo vienes viene venimos vienen", pret="vine viniste vino vinimos vinieron", fut="vendré vendrás vendrá vendremos vendrán", part="venido", ger="viniendo"),
    "dormir": dict(pres="duermo duermes duerme dormimos duermen", pret="dormí dormiste durmió dormimos durmieron", fut="dormiré dormirás dormirá dormiremos dormirán", part="dormido", ger="durmiendo"),
    "comer": dict(pres="como comes come comemos comen", pret="comí comiste comió comimos comieron", fut="comeré comerás comerá comeremos comerán", part="comido", ger="comiendo"),
    "ver": dict(pres="veo ves ve vemos ven", pret="vi viste vio vimos vieron", fut="veré verás verá veremos verán", part="visto", ger="viendo"),
    "dar": dict(pres="doy das da damos dan", pret="di diste dio dimos dieron", fut="daré darás dará daremos darán", part="dado", ger="dando"),
    "comprar": dict(pres="compro compras compra compramos compran", pret="compré compraste compró compramos compraron", fut="compraré comprarás comprará compraremos comprarán", part="comprado", ger="comprando"),
    "cortar": dict(pres="corto cortas corta cortamos cortan", pret="corté cortaste cortó cortamos cortaron", fut="cortaré cortarás cortará cortaremos cortarán", part="cortado", ger="cortando"),
    "querer": dict(pres="quiero quieres quiere queremos quieren", pret="quise quisiste quiso quisimos quisieron", fut="querré querrás querrá querremos querrán", part="querido", ger="queriendo"),
    "encontrarse": dict(pres="encuentro encuentras encuentra encontramos encuentran", pret="encontré encontraste encontró encontramos encontraron", fut="encontraré encontrarás encontrará encontraremos encontrarán", part="encontrado", ger="encontrando", refl=True),
}
REFL = ["me", "te", "se", "nos", "se"]
HABER = dict(pres="he has ha hemos han".split(), imp="había habías había habíamos habían".split())
ESTAR = "estoy estás está estamos están".split()
SER = "soy eres es somos son".split()
TENER = "tengo tienes tiene tenemos tienen".split()


def hueco(persona, plural):
    if persona == 4 or (persona == 1 and plural):
        return 3
    if persona in (2, 3) and plural:
        return 4
    return {1: 0, 2: 1, 3: 2}[persona]


PRON_B = {1: "naya", 2: "juma", 3: "jupa", 4: "jiwasa"}
DEM_B = {"DEM.1": "aka", "DEM.2": "uka", "DEM.3": "khuri"}
NUM_B = {"NUM.3": "kimsa", "NUM.4": "pusi", "NUM.6": "suxta", "NUM.10": "tunka"}
DEM_ES = {"DEM.1": ("este", "esta", "estos", "estas"), "DEM.2": ("ese", "esa", "esos", "esas"),
          "DEM.3": ("aquel", "aquella", "aquellos", "aquellas")}
DEICT_ES = {"DEM.1": "aquí", "DEM.2": "ahí", "DEM.3": "allá"}
NUM_ES = {"NUM.3": "tres", "NUM.4": "cuatro", "NUM.6": "seis", "NUM.10": "diez"}
PERS = {1: "P1", 2: "P2", 3: "P3", 4: "P4"}
FUTP = {1: "FUT.1", 2: "FUT.2", 3: "FUT.3", 4: "FUT.4"}
TRANS = {(1, 2): "T12", (2, 1): "T21", (3, 1): "T31", (3, 2): "T32", (3, 4): "T34"}
CLIT = {(1, 2): "te", (2, 1): "me", (3, 1): "me", (3, 2): "te", (3, 4): "nos"}


# ------------------------------------------------------------------ reglas [DERIVADA]
ORAC = {"AFF", "Q.YN", "NEG.TI", "Q.INF"}
PERS_IDS = {"P1", "P2", "P3", "P4", "P3.REM", "T12", "T21", "T31", "T32", "T34", "FUT.1", "FUT.2", "FUT.3", "FUT.4"}


def reglas_derivadas(ids, tipo="VERBO"):
    """CH-702: devuelve la lista de DV que usa una palabra. tipo: VERBO, ESTAR, TENER, SER."""
    s = []
    o = ids[-1] if ids and ids[-1] in ORAC else None
    p = next((i for i in ids if i in PERS_IDS), None)
    rem = "REM.C" in ids or "REM.L" in ids
    if tipo == "VERBO":
        if p == "T32" and o: s.append("DV-01")
        if p in ("T12", "T21", "T31", "T34") and o: s.append("DV-02")
        if o in ("Q.YN", "NEG.TI") and p in ("P2", "P3", "P4") and not rem: s.append("DV-03")
        if (p in ("FUT.1", "FUT.2") and o) or (p == "FUT.4" and o in ("Q.YN", "NEG.TI")): s.append("DV-04")
        if rem and o: s.append("DV-05")
        if "PL.V" in ids and (p in ("FUT.1", "FUT.3", "FUT.4") or "REM.L" in ids): s.append("DV-06")
        if "PL.V" in ids and p and p.startswith("T"): s.append("DV-07")
        if "NEG" in ids and p not in ("P1", "FUT.3"): s.append("DV-08")
        if "PROG" in ids and p != "P3": s.append("DV-09")
    else:
        if tipo == "ESTAR" and p != "P1": s.append("DV-10")
        if tipo == "TENER" and p in ("P2", "P4"): s.append("DV-11")
        if tipo == "SER" and p in ("P2", "P4"): s.append("DV-12")
        if o == "Q.YN": s.append("DV-13")
    return sorted(set(s))


# ------------------------------------------------------------------ utilidades NP
def L(i):
    return LEXICO[i]


def genero_np(np):
    g = L(np["n"])[6]
    return np.get("genero") or "m" if g == "var" else g


def es_plural(np):
    return bool(np.get("plural")) or bool(np.get("num"))


class Oracion:
    def __init__(self, modo):
        self.modo, self.palabras, self.dv = modo, [], []

    def w(self, base, ids, tipo=None):
        forma = construir_palabra(base, ids, self.modo)
        self.palabras.append({"base": base, "ids": list(ids), "forma": forma})
        if tipo:
            self.dv += reglas_derivadas(ids, tipo)
        return forma


def np_aymara(O, np, caso=None, orac=None):
    """CH-912: [poseedor-GEN] [DEM|NUM] [ADJ] NÚCLEO-sufijos."""
    out = []
    if np.get("poseedor"):
        out.append(np_aymara(O, np["poseedor"], "GEN"))
    if np.get("dem"):
        out.append(O.w(DEM_B[np["dem"]], []))
    if np.get("num"):
        out.append(O.w(NUM_B[np["num"]], []))
    if np.get("adj"):
        out.append(O.w(L(np["adj"])[8], []))
    ids = []
    if np.get("plural") and not np.get("num"):
        ids.append("PL")
    if np.get("poseedor"):
        ids.append("POSS.3")
    elif np.get("poss"):
        ids.append("POSS.%d" % np["poss"])
    if caso:
        ids.append(caso)
    if orac:
        ids.append(orac)
    out.append(O.w(L(np["n"])[8], ids))
    return " ".join(out)


def pron_aymara(O, persona, plural, caso=None, orac=None):
    base, ids = PRON_B[persona], []
    if plural:
        if persona == 1:
            base = "nänaka"                       # CH-517
        else:
            ids.append("PL")
    if caso:
        ids.append(caso)
    if orac:
        ids.append(orac)
    return O.w(base, ids)


def ids_verbo(I, orac):
    S = I["sujeto"]
    sp, op, t = S["persona"], I.get("objeto_persona", 3), I.get("tiempo", "SIMP")
    ids = []
    if I["modalidad"] == "negativa":
        ids.append("NEG")
    elif S.get("plural"):
        ids.append("PL.V")
    elif I.get("aspecto") == "progresivo":
        ids.append("PROG")
    if op != 3:
        ids.append(TRANS[(sp, op)])
    elif t == "SIMP":
        ids.append(PERS[sp])
    elif t == "FUT":
        ids.append(FUTP[sp])
    else:
        ids += [t, "P3.REM" if sp == 3 else PERS[sp]]
    if orac:
        ids.append(orac)
    return ids


# ------------------------------------------------------------------ §9 aymara
def oracion_aymara(I, modo):
    O = Oracion(modo)
    pred, mod, S = I["predicado"], I["modalidad"], I["sujeto"]
    inter = I.get("interrogativo")
    expreso = S.get("expreso", "ninguno")
    suj_expreso = expreso != "ninguno" and inter != "quien_suj"
    # CH-902: destino de -wa
    destino = None
    if mod == "afirmativa":
        if pred != "verbo":
            destino = "pred"
        else:
            destino = I.get("posicion_wa", "verbo")
            if destino == "sujeto" and not suj_expreso:
                destino = "verbo"
            if destino == "complemento":
                cands = [k for k in ("lugar", "comcausa", "oi") if I.get(k)
                         and (k != "lugar" or (I[k].get("caso") in ("ALL", "UNTIL") and not I[k].get("deictico")))]
                destino = cands[-1] if cands else "verbo"
    partes = []
    # 1. sujeto (CH-903)
    if inter == "quien_suj":
        partes.append(O.w("khiti", ["Q.INF"]))
    elif suj_expreso:
        if expreso == "coordinado":
            a, b = S["coord"]
            partes.append(np_aymara(O, a, "COM"))
            partes.append(np_aymara(O, b, "COM", "AFF" if destino == "sujeto" else None))
        else:
            orac = "AFF" if destino == "sujeto" else "TOP"
            if expreso == "pronombre":
                partes.append(pron_aymara(O, S["persona"], S.get("plural"), None, orac))
            elif expreso == "demostrativo":
                partes.append(O.w(DEM_B[S["dem"]], (["PL"] if S.get("plural") else []) + [orac]))
            else:
                partes.append(np_aymara(O, S["np"], None, orac))
    # 2. jani (CH-905)
    if mod == "negativa":
        partes.append(O.w("jani", ["AFF"]))
    # 3. tiempo
    if I.get("adv_t"):
        top = expreso == "ninguno" and inter is None
        partes.append(O.w(L(I["adv_t"])[8], ["TOP"] if top else []))
    if pred == "verbo":
        Lg = I.get("lugar")
        if Lg:
            o = "AFF" if destino == "lugar" else None
            if inter == "donde_all":
                partes.append(O.w("kawki", ["ALL", "Q.INF"]))
            elif Lg.get("deictico"):
                partes.append(O.w(DEM_B[Lg["deictico"]], ["LOC"]))
            else:
                partes.append(np_aymara(O, Lg["np"], Lg["caso"], o))
        C = I.get("comcausa")
        if C:
            partes.append(np_aymara(O, C["np"], C["caso"], "AFF" if destino == "comcausa" else None))
        OI = I.get("oi")
        if OI or inter == "quien_oi":
            o = "AFF" if destino == "oi" else None
            if inter == "quien_oi":
                partes.append(O.w("khiti", ["COMPL.RU", "Q.INF"]))
            elif I.get("oi_pronombre_expreso"):
                partes.append(pron_aymara(O, I["objeto_persona"], False, "COMPL.RU", o))
            else:
                partes.append(np_aymara(O, OI["np"], OI["funcion"], o))
        if inter == "que_od":
            partes.append(O.w("kuna", ["Q.INF"]))
        elif I.get("od_coord"):
            a, b = I["od_coord"]
            partes.append(np_aymara(O, a, "COM"))
            partes.append(np_aymara(O, b, "COM"))
        elif I.get("od"):
            partes.append(np_aymara(O, I["od"]))
        orac = {"afirmativa": "AFF" if destino == "verbo" else None, "negativa": "NEG.TI",
                "pregunta_si_no": "Q.YN", "pregunta_info": None}[mod]
        partes.append(O.w(L(I["verbo"])[8], ids_verbo(I, orac), "VERBO"))
    else:
        P, sp = I["pnom"], S["persona"]
        orac = {"afirmativa": "AFF", "pregunta_si_no": "Q.YN", "pregunta_info": "Q.INF"}[mod]
        if pred == "ser":
            base = L(P["adj"])[8] if "adj" in P else L(P["np"]["n"])[8]
            if sp == 3:
                ids = (["PL"] if (S.get("plural") and "np" in P) else []) + [orac]
                partes.append(O.w(base, ids))
            else:
                partes.append(O.w(base, ["VBLZ.LONG", PERS[sp], orac], "SER"))
        elif pred == "estar":
            if inter == "donde_estar":
                partes.append(O.w("kawki", ["LOC", "VBLZ.KA", PERS[sp], "Q.INF"], "ESTAR"))
            elif P.get("deictico"):
                partes.append(O.w(DEM_B[P["deictico"]], ["LOC", "VBLZ.KA", PERS[sp], orac], "ESTAR"))
            else:
                np = P["np"]
                if np.get("dem"): partes.append(O.w(DEM_B[np["dem"]], []))
                if np.get("num"): partes.append(O.w(NUM_B[np["num"]], []))
                if np.get("adj"): partes.append(O.w(L(np["adj"])[8], []))
                ids = (["PL"] if np.get("plural") else []) + (["POSS.%d" % np["poss"]] if np.get("poss") else []) \
                    + ["LOC", "VBLZ.KA", PERS[sp], orac]
                partes.append(O.w(L(np["n"])[8], ids, "ESTAR"))
        elif pred == "tener":
            np = P["np"]
            if np.get("dem"): partes.append(O.w(DEM_B[np["dem"]], []))
            if np.get("num"): partes.append(O.w(NUM_B[np["num"]], []))
            if np.get("adj"): partes.append(O.w(L(np["adj"])[8], []))
            ids = (["PL"] if (np.get("plural") and not np.get("num")) else []) + ["POSR"] \
                + ([] if sp == 3 else ["VBLZ.LONG", PERS[sp]]) + [orac]
            partes.append(O.w(L(np["n"])[8], ids, "TENER"))
    s = " ".join(partes)
    s = s[0].upper() + s[1:]                                   # CH-106
    s = "¿" + s + "?" if mod in ("pregunta_si_no", "pregunta_info") else s + "."
    return s, O.palabras, sorted(set(O.dv))


# ------------------------------------------------------------------ §10 español
def articulo(g, pl, definido=True):
    if definido:
        return {("m", False): "el", ("f", False): "la", ("m", True): "los", ("f", True): "las"}[(g, pl)]
    return "" if pl else ("un" if g == "m" else "una")


def nombre_es(np):
    e, g, pl = L(np["n"]), genero_np(np), es_plural(np)
    if e[6] == "var":
        return (e[4] if g == "m" else e[5]) if pl else (e[2] if g == "m" else e[3])
    return e[4] if pl else e[2]


def adj_es(a, g, pl):
    e = L(a)
    return (e[4] if g == "m" else e[5]) if pl else (e[2] if g == "m" else e[3])


def np_es(np, art="def"):
    """CH-1008. art: def | indef | nada"""
    g, pl, e = genero_np(np), es_plural(np), L(np["n"])
    out = []
    if np.get("dem"):
        out.append(DEM_ES[np["dem"]][(2 if pl else 0) + (1 if g == "f" else 0)])
    elif np.get("num"):
        out.append(NUM_ES[np["num"]])
    elif np.get("poss"):
        p = np["poss"]
        if p == 4:
            out.append({("m", False): "nuestro", ("f", False): "nuestra", ("m", True): "nuestros", ("f", True): "nuestras"}[(g, pl)])
        else:
            out.append({1: ("mi", "mis"), 2: ("tu", "tus"), 3: ("su", "sus")}[p][1 if pl else 0])
    elif np.get("poseedor") or art == "def":
        out.append(articulo(g, pl, True))
    elif art == "indef" and e[7] == "s":
        a = articulo(g, pl, False)
        if a:
            out.append(a)
    out.append(nombre_es(np))
    if np.get("adj"):
        out.append(adj_es(np["adj"], g, pl))
    if np.get("poseedor"):
        out.append(prep("de", np_es(np["poseedor"], "def")))
    return " ".join(out)


def prep(p, s):
    if p == "a" and s.startswith("el "):
        return "al " + s[3:]
    if p == "de" and s.startswith("el "):
        return "del " + s[3:]
    return p + " " + s


def pron_es(p, pl, g):
    if p == 1:
        return "nosotros" if pl else "yo"
    if p == 2:
        return "ustedes" if pl else "tú"
    if p == 4:
        return "nosotros"
    return ("ellas" if g == "f" else "ellos") if pl else ("ella" if g == "f" else "él")


def oracion_espanol(I):
    pred, mod, S = I["predicado"], I["modalidad"], I["sujeto"]
    sp, pl, g = S["persona"], bool(S.get("plural")), S.get("genero") or "m"
    inter, expreso = I.get("interrogativo"), S.get("expreso", "ninguno")
    sujeto = ""
    if inter == "quien_suj":
        sp, pl = 3, False
    elif expreso == "pronombre":
        sujeto = pron_es(sp, pl, g)                                    # CH-1007
    elif expreso == "nombre":
        sujeto = np_es(S["np"], "def")
    elif expreso == "coordinado":
        sujeto = " y ".join(np_es(x, "def") for x in S["coord"])
        pl = True
    h = hueco(sp, pl)
    resto = []
    if pred == "verbo":
        v = L(I["verbo"])[2]
        c, t, adv = CONJ[v], I.get("tiempo", "SIMP"), I.get("adv_t")
        if I.get("aspecto") == "progresivo":                           # CH-1005
            vf = ESTAR[h] + " " + c["ger"]
        elif t == "SIMP":                                              # CH-1001
            vf = c["pret" if (adv and L(adv)[1] == "pasado") else "pres"].split()[h]
        elif t == "FUT":                                               # CH-1004
            vf = c["fut"].split()[h]
        elif t == "REM.C":                                             # CH-1002
            vf = HABER["pres"][h] + " " + c["part"]
        else:                                                          # CH-1003
            vf = HABER["imp"][h] + " " + c["part"]
        if c.get("refl"):
            vf = REFL[h] + " " + vf
        op, cl = I.get("objeto_persona", 3), ""
        if op != 3:                                                    # CH-1009
            cl = CLIT[(S["persona"], op)] + " "
        OI = I.get("oi")
        if (OI and OI["funcion"] == "COMPL.RU" and op == 3) or inter == "quien_oi":
            cl = "les " if (OI and OI.get("np", {}).get("plural")) else "le "
        if inter != "que_od":
            if I.get("od_coord"):
                resto.append(" y ".join(np_es(x, "nada" if L(x["n"])[7] == "n" else "def") for x in I["od_coord"]))
            elif I.get("od"):
                D = I["od"]
                simple = not (D.get("plural") or D.get("dem") or D.get("poss") or D.get("poseedor") or D.get("num"))
                resto.append(np_es(D, "nada" if (L(D["n"])[7] == "n" and simple) else "def"))
        if OI and inter != "quien_oi" and not I.get("oi_pronombre_expreso") and OI.get("np"):
            resto.append(prep("a" if OI["funcion"] == "COMPL.RU" else "para", np_es(OI["np"], "def")))
        Lg = I.get("lugar")
        if Lg and inter != "donde_all":
            if Lg.get("deictico"):
                resto.append(DEICT_ES[Lg["deictico"]])
            else:
                resto.append(prep({"ALL": "a", "ABL": "de", "LOC": "en", "UNTIL": "hasta"}[Lg["caso"]], np_es(Lg["np"], "def")))
        C = I.get("comcausa")
        if C:
            resto.append(prep("con" if C["caso"] == "COM" else "por", np_es(C["np"], "def")))
        if adv:
            resto.append(L(adv)[2])
        verbo = cl + vf
    else:
        P = I["pnom"]
        if pred == "ser":
            verbo = SER[h]
            if "adj" in P:
                resto.append(adj_es(P["adj"], g, pl))
            else:
                npp = dict(P["np"], plural=pl)
                resto.append(np_es(npp, "nada" if L(npp["n"])[0] == "N_HUM" else "indef"))
            if expreso == "demostrativo":
                sujeto = DEM_ES[S["dem"]][(2 if pl else 0) + (1 if genero_np(P["np"]) == "f" else 0)]
        elif pred == "estar":
            verbo = ESTAR[h]
            if inter != "donde_estar":
                resto.append(DEICT_ES[P["deictico"]] if P.get("deictico") else prep("en", np_es(P["np"], "def")))
        else:
            verbo = TENER[h]
            np = P["np"]
            resto.append(np_es(np, "indef" if L(np["n"])[7] == "s" else "nada"))
    neg = "no " if mod == "negativa" else ""
    if mod == "pregunta_info":                                         # CH-1011
        q = {"quien_suj": "Quién", "que_od": "Qué", "donde_all": "A dónde",
             "quien_oi": "A quién", "donde_estar": "Dónde"}[inter]
        partes = [q, verbo] + ([sujeto] if sujeto else []) + resto
    else:
        partes = ([sujeto] if sujeto else []) + [neg + verbo] + resto
    s = " ".join(x for x in partes if x)
    s = s[0].upper() + s[1:]
    return "¿" + s + "?" if mod in ("pregunta_si_no", "pregunta_info") else s + "."


def generar(idea):
    b, palabras_b, dv = oracion_aymara(idea, "B")
    a, palabras_a, _ = oracion_aymara(idea, "A")
    return {"b": b, "a": a, "es": oracion_espanol(idea), "palabras": palabras_b, "palabras_a": palabras_a, "dv": dv}


if __name__ == "__main__":
    idea = {"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "L0018",
            "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "L0004"}},
            "oi": {"funcion": "COMPL.RU", "np": {"n": "L0001", "genero": "m"}}, "od": {"n": "L0006"},
            "lugar": {"caso": "LOC", "np": {"n": "L0009"}}, "adv_t": "L0023", "posicion_wa": "verbo"}
    r = generar(idea)
    print(r["b"]); print(r["a"]); print(r["es"]); print(r["dv"])
