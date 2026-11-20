"""
chulupi_motor.py — Motor morfofonológico de referencia de Chulupi Lang v1.1.

Implementa §1 (grafemas), §2 (validación de palabras), §5 (morfemas B/A),
§7 (algoritmo CH-701 a CH-709) de chulupi_lang_spec.md.

Uso mínimo:
    from chulupi_motor import construir_palabra
    construir_palabra("tisqa", ["P1", "AFF"], "B")   # -> "tisqthwa"
    construir_palabra("tisqa", ["P1", "AFF"], "A")   # -> "tisqphyi"

Es un prototipo de referencia: la fuente normativa es la especificación.
"""
import re
import unicodedata

# ---------------------------------------------------------------- §1 CH-105
GRAFEMAS = ["chh", "ch'", "ch", "ph", "p'", "th", "t'", "kh", "k'", "qh", "q'", "ll",
            "a", "i", "u", "ä", "ï", "ü",
            "p", "t", "k", "q", "s", "j", "x", "m", "n", "ñ", "l", "r", "w", "y"]
VOC_CORTAS = {"a", "i", "u"}
LARGA = {"a": "ä", "i": "ï", "u": "ü"}
VOC_LARGAS = set(LARGA.values())
APOSTROFOS = {"’": "'", "‘": "'", "ʼ": "'", "´": "'", "`": "'"}


def normalizar(texto):
    """CH-102, CH-103: NFC, apóstrofo U+0027, minúsculas."""
    t = unicodedata.normalize("NFC", texto)
    for k, v in APOSTROFOS.items():
        t = t.replace(k, v)
    return t.lower()


def segmentar(palabra):
    """CH-105: grafema más largo primero. Lanza ValueError si sobra algo."""
    out, i = [], 0
    while i < len(palabra):
        for g in GRAFEMAS:
            if palabra.startswith(g, i):
                out.append(g)
                i += len(g)
                break
        else:
            raise ValueError(f"carácter no permitido en {palabra!r} (posición {i})")
    return out


def clases(grafemas):
    """C = consonante, V = vocal corta, L = vocal larga."""
    return "".join("V" if g in VOC_CORTAS else "L" if g in VOC_LARGAS else "C" for g in grafemas)


RE_PALABRA = re.compile(r"^C?[VL](C{1,6}[VL])*$")   # CH-202..CH-208


def validar_palabra(palabra):
    """CH-709: devuelve lista de errores (vacía si es válida)."""
    errores = []
    try:
        g = segmentar(palabra)
    except ValueError as e:
        return [str(e)]
    if not RE_PALABRA.match(clases(g)):
        errores.append(f"estructura inválida {clases(g)}")
    if g[0] in ("x", "r"):
        errores.append("empieza por x o r (CH-202)")
    if "lll" in palabra:
        errores.append("cadena lll (CH-207)")
    return errores


# ---------------------------------------------------------------- §5 CH-504
# id: (forma B, forma A, antes, después)   V = conserva, C = borra, "-" = no actúa
MORFEMAS = {
    # nombre
    "PL": ("naka", "sulu", "V", "V"),
    "POSS.1": ("ja", "lu", "V", "V"), "POSS.2": ("ma", "qi", "V", "V"),
    "POSS.3": ("pa", "chu", "V", "V"), "POSS.4": ("sa", "khu", "V", "V"),
    "POSR": ("ni", "phu", "V", "V"),
    "GEN": ("na", "mu", "V", "V"), "LOC": ("na", "mu", "V", "V"),
    "ALL": ("ru", "llu", "V", "V"), "COMPL.RU": ("ru", "llu", "V", "V"),
    "ABL": ("ta", "ku", "V", "V"), "COM": ("mpi", "nku", "V", "V"),
    "BEN": ("taki", "puli", "V", "V"), "UNTIL": ("kama", "chiwi", "V", "V"),
    "CAUSE": ("layku", "tiwqa", "V", "V"),
    "VBLZ.KA": ("ka", "ñu", "C", "-"), "VBLZ.LONG": ("¨", "¨", "V", "-"),
    # verbo
    "PL.V": ("pxa", "mtu", "V", "-"), "PROG": ("ska", "nchi", "V", "-"), "NEG": ("ka", "ñu", "C", "-"),
    "REM.C": ("yä", "jü", "V", "-"), "REM.L": ("tä", "wü", "V", "-"),
    "P1": ("tha", "phi", "C", "C"), "P2": ("ta", "ku", "C", "V"),
    "P3": ("i", "u", "C", "V"), "P4": ("tana", "kilu", "C", "C"),
    "P3.REM": ("na", "mu", "-", "V"),
    "T12": ("sma", "jmi", "C", "V"), "T21": ("ista", "ulqa", "C", "V"),
    "T31": ("itu", "uqu", "C", "V"), "T32": ("tama", "kiqu", "C", "C"),
    "T34": ("istu", "ulqu", "C", "V"),
    "FUT.1": ("¨", "¨", "V", "V"), "FUT.2": ("¨ta", "¨ku", "V", "V"),
    "FUT.3": ("ni", "phu", "V", "V"), "FUT.4": ("ñäni", "thäqi", "V", "V"),
    # oracionales
    "AFF": ("wa", "yi", "-", "-"), "TOP": ("xa", "xu", "-", "-"),
    "Q.YN": ("ti", "ji", "-", "-"), "NEG.TI": ("ti", "ji", "-", "-"),
    "Q.INF": ("sa", "khu", "-", "-"),
}

# CH-505: palabras gramaticales (forma B -> forma A)
GRAMATICALES = {
    "naya": "muqi", "juma": "tilu", "jupa": "kaxi", "jiwasa": "wiqutu", "nänaka": "müsulu",
    "jani": "yuli", "khiti": "simu", "kuna": "sipu", "kawki": "yaqu",
    "aka": "ilmi", "uka": "ulmi", "khuri": "phiqa",
    "kimsa": "musqi", "pusi": "tayli", "suxta": "wichqa", "tunka": "qanti",
}


# ---------------------------------------------------------------- §7 CH-701
def construir_palabra(base, ids, modo="B", traza=False):
    """
    base : raíz (de lexico.csv o real) o palabra gramatical en su forma B.
    ids  : lista de ids de morfemas en orden (CH-601, CH-602).
    modo : "B" o "A".
    traza: si es True devuelve (palabra, pasos, decisiones).
           'decisiones' es la secuencia usada en la prueba de paralelismo (CH-710.2).
    """
    if modo not in ("B", "A"):
        raise ValueError("modo debe ser 'B' o 'A'")
    forma0 = GRAMATICALES.get(base, base) if modo == "A" else base
    g = segmentar(forma0)
    despues_prev, id_prev, protegida = "V", "RAIZ", False
    pasos, decisiones = [f"raíz `{forma0}`"], []
    for k, mid in enumerate(ids):
        b, a, antes, despues = MORFEMAS[mid]
        f = b if modo == "B" else a
        if mid == "REM.C" and k + 1 < len(ids) and ids[k + 1] == "P3.REM":   # CH-511
            f = "¨"
        if mid == "VBLZ.LONG" and id_prev == "POSR":                         # CH-705
            protegida, despues_prev, id_prev = True, "V", mid
            decisiones.append("proteger")
            pasos.append(f"+ {mid} tras POSR: no se escribe; protege `{g[-1]}` (CH-705) → `{''.join(g)}`")
            continue
        if f.startswith("¨"):                                                # CH-704
            if g[-1] in VOC_CORTAS:
                g[-1] = LARGA[g[-1]]
            resto = f[1:]
            if resto:
                g += segmentar(resto)
            protegida, despues_prev, id_prev = False, despues, mid
            decisiones.append("alargar")
            pasos.append(f"+ {mid} `{f}`: alarga → `{''.join(g)}`")
            continue
        borrar = antes == "C" or (antes == "-" and despues_prev == "C")      # CH-702
        ultima = g[-1]
        if borrar and ultima in VOC_CORTAS and not protegida:
            g = g[:-1]
            d = "borrar"
        elif borrar and protegida:
            d = "protegida-no-borra"
        elif borrar and ultima in VOC_LARGAS:
            d = "larga-no-borra"                                             # CH-703
        else:
            d = "conservar"
        decisiones.append(d)
        protegida = False
        g += segmentar(f)                                                    # CH-706
        despues_prev, id_prev = despues, mid
        pasos.append(f"+ {mid} `{f}` (antes {antes}): {d} → `{''.join(g)}`")
    palabra = "".join(g)
    errores = validar_palabra(palabra)
    if errores:                                                              # CH-709
        raise ValueError(f"palabra inválida {palabra!r} ({base} + {ids}): {errores}")
    if traza:
        return palabra, pasos, decisiones
    return palabra


def construir_ambos(base, ids):
    """Devuelve (forma B, forma A)."""
    return construir_palabra(base, ids, "B"), construir_palabra(base, ids, "A")


if __name__ == "__main__":
    for base, ids in [("tisqa", ["P1", "AFF"]), ("tisqa", ["PL.V", "REM.C", "P3.REM"]),
                      ("chimula", ["POSR", "VBLZ.LONG", "P1", "AFF"]), ("ch'ixra", ["T32", "AFF"])]:
        print(base, ids, construir_ambos(base, ids))
