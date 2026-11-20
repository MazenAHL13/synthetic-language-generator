"""
test_chulupi.py — Pruebas del prototipo de Chulupi Lang v1.1.

Ejecutar:  python -m unittest test_chulupi -v

1. CH-710.1  Regresión con raíces reales (modo B = forma atestiguada).   regresion_ch710.json
2. CH-710.2  Paralelismo: mismas decisiones en modo B y modo A.
3. §12       Los 40 casos de prueba dan exactamente la salida esperada. casos_prueba.json
4. §12       Los casos [ATESTIGUADO] reproducen la forma de la guía.
5. CH-1013   Una traducción por oración ficticia (salvo género).
6. CH-709    Toda palabra generada es válida.
"""
import json
import os
import unittest

from chulupi_motor import construir_palabra, validar_palabra
from chulupi_oraciones import generar

AQUI = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(AQUI, "regresion_ch710.json"), encoding="utf-8"))
CASOS = json.load(open(os.path.join(AQUI, "casos_prueba.json"), encoding="utf-8"))
PALABRAS_GENERO = {"el", "la", "los", "las", "un", "una", "él", "ella", "ellos", "ellas",
                   "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
                   "aquel", "aquella", "aquellos", "aquellas", "nuestro", "nuestra", "nuestros", "nuestras",
                   "al", "del"}


class Regresion(unittest.TestCase):
    def test_igualdad_modo_B(self):
        fallas = []
        for c in REG:
            obtenido = construir_palabra(c["raiz"], c["ids"], "B")
            if obtenido != c["esperado"]:
                fallas.append((c["raiz"], c["ids"], c["esperado"], obtenido, c["fuente"]))
        self.assertEqual(fallas, [], f"{len(fallas)} casos de CH-710 no coinciden")

    def test_paralelismo_modo_A(self):
        fallas = []
        for c in REG:
            _, _, dec_b = construir_palabra(c["raiz"], c["ids"], "B", traza=True)
            _, _, dec_a = construir_palabra(c["raiz"], c["ids"], "A", traza=True)
            if dec_b != dec_a:
                fallas.append((c["raiz"], c["ids"], dec_b, dec_a))
        self.assertEqual(fallas, [])


class Casos(unittest.TestCase):
    def test_40_casos(self):
        self.assertEqual(len(CASOS), 40)
        for c in CASOS:
            r = generar(c["idea"])
            with self.subTest(caso=c["id"]):
                self.assertEqual(r["b"], c["esperado"]["b"])
                self.assertEqual(r["a"], c["esperado"]["a"])
                self.assertEqual(r["es"], c["esperado"]["es"])
                self.assertEqual(r["dv"], c["dv"])

    def test_atestiguados(self):
        for c in CASOS:
            if c["atestiguado"]:
                with self.subTest(caso=c["id"]):
                    self.assertEqual(generar(c["idea"])["b"], c["atestiguado"])

    def test_palabras_validas(self):
        for c in CASOS:
            r = generar(c["idea"])
            for frase in (r["b"], r["a"]):
                for w in frase.strip("¿?.").lower().split():
                    self.assertEqual(validar_palabra(w), [], (c["id"], w))


class UnaTraduccion(unittest.TestCase):
    """CH-1013: mismas ideas salvo 'genero' -> misma oración ficticia; el español solo cambia en género."""

    def test_genero(self):
        import copy
        base = next(c for c in CASOS if c["id"] == "C12")["idea"]
        f = copy.deepcopy(base)
        f["sujeto"]["genero"] = "f"
        rm, rf = generar(base), generar(f)
        self.assertEqual(rm["b"], rf["b"])
        self.assertEqual(rm["a"], rf["a"])
        dif = [(x, y) for x, y in zip(rm["es"].split(), rf["es"].split()) if x != y]
        for x, y in dif:
            self.assertTrue(x.strip("¿?.").lower() in PALABRAS_GENERO or x[:-1] == y[:-1], (x, y))


if __name__ == "__main__":
    unittest.main(verbosity=2)
