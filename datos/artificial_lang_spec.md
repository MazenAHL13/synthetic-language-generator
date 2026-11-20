# Chulupi Lang — Especificación v1

**Versión:** 1.1.1 (CH-406: BEN solo con `V_TR` y `V_DITR`; CH-1103: R21 y R22; `pesos.yaml`: `categoria_verbo` y `oi_V_TR`; CH-1008, regla 5: no contables sin artículo). La 1.1 corrigió la parte 1 de la 1.0 (CH-104, CH-306, CH-308) y añadió CH-406 y CH-407 · **Fuente única:** `guia_estructural_aymara_v3.md` (en adelante, "la guía").
**Para quién:** el equipo que programa el generador. No hace falta saber lingüística: cada regla dice qué hacer, con ejemplos.

## Cómo leer este documento

- **Etiquetas.**
  - **[DECISIÓN CHULUPI]**: elección libre del proyecto. La guía no decide, o da variantes y elegimos una.
  - **[DERIVADA]**: regla deducida de un patrón documentado, pero sin una forma atestiguada igual. Todas se listan en el **Anexo A** para verificarlas con el corpus.
  - **[ATESTIGUADO]**: forma igual a una de la tabla 10.1 de la guía.
- **Referencias.** "§" = sección de la guía. L1 y L2 = los dos libros de la guía. "Dx" = decisión del proyecto en la guía.
- **Reglas.** Cada regla tiene un ID `CH-xxx`, su base en la guía y al menos un ejemplo en los dos modos.
- **Glosas.** Se usan las abreviaturas de la guía. La glosa es la misma en los dos modos (solo cambian las formas).
- **Ejemplos.** Formato: `forma-segmentada` — GLOSA — "español". El guion solo separa morfemas en las glosas; **no se escribe** en la salida.
- **Archivos que el programa lee** (bloques `yaml` de este documento): `alfabeto.yaml`, `fonotactica.yaml`, `generador_raices.yaml`, `morfemas.yaml`, `slots.yaml`, `paradigmas.yaml`, `idea.schema.yaml`, `pesos.yaml`. Además: `lexico.csv` y `palabras_reales.txt`.

---

## 0. Resumen

1. Chulupi Lang es un lenguaje ficticio: tiene la gramática del aymara (orden SOV, sufijos, caída de vocales) y raíces inventadas.
2. Tiene dos modos con la misma gramática y las mismas raíces. **Modo B:** sufijos y palabras gramaticales reales del aymara, con la escritura de L2. **Modo A:** sufijos y palabras gramaticales inventados, con un mapeo fijo desde B.
3. El programa parte de una **idea** (JSON, §11 de este documento), arma la oración en B, la pasa a A con el mapeo y genera la oración española.
4. Alfabeto: 3 vocales (a, i, u), 3 vocales largas (ä, ï, ü) y 26 consonantes. El apóstrofo es U+0027.
5. Raíces: de 2 o 3 sílabas, una por palabra española, filtradas contra palabras aymaras reales. Las palabras solo se combinan si son semánticamente compatibles (CH-406).
6. Verbo: SIMP con 9 transiciones; FUT, REM.C y REM.L solo con objeto de 3.ª persona; plural `-pxa`; progresivo `-ska`; negación `jani … -ka … -ti`.
7. Nombre: plural `-naka`, posesivos 1–4, 8 casos y objeto directo sin sufijo (con la vocal final completa).
8. Oración: Sujeto – Tiempo – Lugar – COM/CAUSE – Objeto indirecto – Objeto directo – Verbo. Los sufijos `-wa`, `-xa`, `-ti` y `-sa` van en posiciones fijas o elegidas con pesos.
9. "Ser", "estar" y "tener" van solo en SIMP, en afirmativas o preguntas sí/no.
10. Cada idea produce exactamente una oración B, una A y una española. La única excepción es el género de la 3.ª persona humana, que fija el campo `genero`.

### 0.1 Tabla de [DECISIÓN CHULUPI]

| N.º | Decisión | Regla | Base en la guía |
|---|---|---|---|
| DC-01 | Apóstrofo interno U+0027; `’ ‘ ʼ ´ `` ` se convierten en `'` | CH-102 | D3 (nivel b); fijado por el equipo |
| DC-02 | Mayúscula solo en la primera letra de la oración; punto final; preguntas con `¿…?`; sin comas | CH-106 | L2 p.235 (`¿Jilamaxa jutaniti?`) |
| DC-03 | Aspiradas y glotalizadas: solo al inicio de sílaba; un solo grafema de ese tipo por raíz (puede repetirse); oclusivas del mismo punto, iguales | CH-205 | §8.3 (L2 p.41–42) |
| DC-04 | Codas de raíz: solo consonantes simples de una lista; sin consonante doble en la raíz | CH-206 | §8.3 (L2 p.58–59) |
| DC-05 | Prohibido `l` + `l` o `l` + `ll` entre sílabas | CH-207 | §8.1 (`ll` es una sola letra) |
| DC-06 | Raíces inventadas sin vocal larga | CH-209 | §8.2 |
| DC-07 | Número de sílabas por categoría, con probabilidades | CH-301 | §8.3 ("raíces mayormente bisílabas") |
| DC-08 | Plantillas de sílaba según la posición en la raíz | CH-302 | §8.3 (V, CV, VC, CVC) |
| DC-09 | Pesos de consonantes y vocales | CH-303 | La guía no da frecuencias |
| DC-10 | Todas las raíces verbales terminan en `-a` | CH-304 | §5.1 (predominio de /u/), §3.4 (paradigmas de L2 solo con raíces en -a) |
| DC-11 | Paso de aspiración/glotalización con probabilidad 0,30 | CH-305 | §8.3 |
| DC-12 | Filtro contra palabras reales. **Con la lista de AmericasNLP:** se descarta la raíz igual a una palabra real o que sea el inicio de 5 o más palabras distintas. **Solo con la lista de la guía:** se descarta si es igual o es el inicio de alguna. *(v1.1: antes era "igual o inicio de alguna" en los dos casos.)* | CH-306 | Equipo (P4; corrección v1.1) |
| DC-13 | Una raíz no puede ser igual a un morfema ni a una palabra gramatical (B o A) | CH-307 | — |
| DC-14 | Una raíz no puede terminar en la forma de un sufijo (B o A) de **3 grafemas o más**. Puede terminar en `-ta`, `-sa`, `-na`, etc., como en aymara real. *(v1.1: antes eran 2 grafemas o más.)* | CH-308 | Corrección v1.1 |
| DC-15 | Diccionario fijo: un sentido español = una raíz, generado una vez | CH-309 | — |
| DC-16 | Una raíz no puede ser igual a otra raíz + un sufijo | CH-310 | — |
| DC-17 | Frecuencias Zipf con exponente 0,9 dentro de cada categoría | CH-403 | — |
| DC-18 | Cobertura mínima: cada entrada aparece al menos 20 veces | CH-404 | — |
| DC-19 | Género español en el léxico: humanos m / f / var; el resto, fijo | CH-405 | — |
| DC-20 | Mapeo A **por forma**: una misma cadena B da una misma cadena A | CH-501 | Equipo (P2) |
| DC-21 | El alargamiento vocálico (`¨`) se conserva igual en A | CH-502 | §8.2 |
| DC-22 | Tabla fija de formas A | CH-503 | — |
| DC-23 | REM segmentado: REM.C `-yä-` (`-¨-` en 3.ª), REM.L `-tä-`, + persona; 3.ª persona `-na` | CH-511 | §3.4, §8.2; L1 p.143 |
| DC-24 | REM.L con `-tä-`, no `-tay-` | CH-512 | §3.4, §13 #15 |
| DC-25 | FUT 1.ª persona `-¨`, no `-ŋa` | CH-513 | §3.4 |
| DC-26 | `-kama` solo sobre raíz nominal de 2 sílabas sin otros sufijos | CH-514 | §5.2.1, §13 #5 |
| DC-27 | `-layku` conserva siempre la vocal anterior (débil) | CH-515 | §5.2 (L2 p.62–63) |
| DC-28 | Demostrativos y numerales son palabras gramaticales (reales en B) | CH-516 | Equipo (P3) |
| DC-29 | `nänaka` es una palabra propia; ningún otro nombre se contrae | CH-517 | D12; §5.2 (`wawanaka ~ wänaka`) |
| DC-30 | No se usan `maya/mä`, `paya/pä`, `khaya/khä` | CH-518 | D8, §13 #6 |
| DC-31 | Interrogativos de v1: `khiti`, `kuna`, `kawki` | CH-519 | §6, §8.4 |
| DC-32 | Palabras gramaticales de L1 sin rasgos que diverjan de L2 se aceptan tal cual | CH-520 | D1 |
| DC-33 | Sin nombres propios en v1 | CH-521 | §10.2 |
| DC-34 | En el verbo, PL, PROG y NEG se excluyen entre sí | CH-603 | D11; §12 #6–7 |
| DC-35 | Transiciones con objeto 1, 2 o 4 solo en SIMP | CH-604 | Equipo (P1) |
| DC-36 | Negación solo en SIMP y FUT | CH-605 | Equipo (P5) |
| DC-37 | Progresivo solo en SIMP, nunca en negativas | CH-606 | — |
| DC-38 | La vocal propia de cada sufijo ante un oracional sigue las marcas c/v de L1 | CH-702 | §3.1, §5.1 |
| DC-39 | Los grupos y las consonantes dobles que deja la elisión se escriben enteros | CH-706 | §5.2 (L2 p.64–65) |
| DC-40 | Orden de complementos ampliado con COM, CAUSE y UNTIL | CH-901 | D10, §1 |
| DC-41 | Campo `posicion_wa` con 4 valores | CH-902 | §1, §4, §4.1 |
| DC-42 | `-xa` en el sujeto; si no hay sujeto, en el adverbio de tiempo | CH-903 | §4.1 |
| DC-43 | `-ti` de pregunta sí/no siempre en el verbo o el predicado | CH-904 | §4.1 |
| DC-44 | `janiwa` justo después del sujeto | CH-905 | §7.3 B; L2 p.231 |
| DC-45 | El interrogativo queda en el lugar del constituyente que reemplaza | CH-906 | D10 |
| DC-46 | Coordinación: 2 miembros, como sujeto de 3.ª persona o como objeto directo | CH-907 | D13 |
| DC-47 | Ser, estar y tener: solo SIMP, afirmativa o pregunta sí/no; "estar" admite además "¿dónde está?" | CH-908 | §8.4, §13 #14 |
| DC-48 | COMPL.RU solo con verbos `V_DITR` | CH-909 | D9, §13 #7 |
| DC-49 | COMPL.RU y BEN no van en la misma oración | CH-910 | §7.3 A |
| DC-50 | Posesión: poseedor pronominal omitido; poseedor nominal humano | CH-911 | §1 |
| DC-51 | Frase nominal: como máximo demostrativo o numeral + 1 adjetivo | CH-912 | §1 |
| DC-52 | El plural se marca siempre; `-pxa` marca solo plural del sujeto | CH-913 | Equipo (ajuste 2); D12 |
| DC-53 | El objeto directo es siempre no humano | CH-914 | §13 #7 |
| DC-54 | Verbo transitivo en X>3: objeto directo obligatorio | CH-915 | — |
| DC-55 | "Aquí / ahí / más allá" = demostrativo + LOC | CH-916 | §2.1 (L2 p.160, `ukana`) |
| DC-56 | Español: SIMP en presente o pretérito según el adverbio; REM.C → pretérito perfecto compuesto; REM.L → pluscuamperfecto; FUT → futuro simple; PROG → estar + gerundio | CH-1001 a CH-1005 | §3.2, §8.2 |
| DC-57 | Español: 4.ª persona = "nosotros" | CH-1006 | D12 |
| DC-58 | Español: hay pronombre sujeto solo si lo hay en aymara | CH-1007 | — |
| DC-59 | Español: reglas fijas de artículos | CH-1008 | §6 (no hay artículos) |
| DC-60 | Español: clíticos `le/les` y `me/te/nos`; el pronombre aymara con `-ru` no añade "a mí"; "tú" y "ustedes" | CH-1009 | — |
| DC-61 | Español: género de la 3.ª persona humana por el campo `genero` | CH-1010 | Equipo (ajuste 2) |
| DC-62 | Español: orden fijo de los constituyentes | CH-1011 | — |
| DC-63 | Pesos de la idea y muestreo estratificado | CH-1104 a CH-1113 | Equipo (ajuste 3) |
| DC-64 | Coherencia semántica: clases (`clase_sem`) para los nombres; clases aceptadas por cada verbo (`suj_clases`, `obj_clases`, `instr_clases`, `loc_clases`) y por cada adjetivo (`mod_clases`); reglas generales para el resto. El generador de ideas solo combina palabras compatibles | CH-406 | Equipo (v1.1), siguiendo a Ri y Tsuruoka (2022) |
| DC-65 | Tamaño objetivo del léxico por categoría; `lexico.csv` lo produce el rol 1 | CH-407 | Equipo (v1.1) |
| DC-66 | VBLZ.LONG tras POSR no se escribe, pero protege la vocal anterior (reproduce `utanithwa`) | CH-705 | §8.4 (L2 p.47, 57); L1 p.71 |
| DC-67 | Compatibilidad entre adverbio de tiempo y tiempo verbal | CH-917 | §3.2 |
| DC-68 | Tope de reglas [DERIVADA] en los datos: ≤ 50 % de pares con alguna, ≤ 15 % por cada una | V30 (CH-1302) | Anexo A |

---

## 1. Alfabeto

Los dos modos usan el mismo alfabeto: el oficial de L2 (§8.1; D1).

### CH-101 · Letras permitidas

Base: §8.1 (L2 p.35, 40).

| Tipo | Grafemas | Unicode (si hace falta) |
|---|---|---|
| Vocales | `a` `i` `u` | U+0061, U+0069, U+0075 |
| Vocales largas | `ä` `ï` `ü` | U+00E4, U+00EF, U+00FC (precompuestas) |
| Oclusivas simples | `p` `t` `ch` `k` `q` | |
| Aspiradas | `ph` `th` `chh` `kh` `qh` | |
| Glotalizadas | `p'` `t'` `ch'` `k'` `q'` | apóstrofo U+0027 |
| Fricativas | `s` `j` `x` | |
| Nasales | `m` `n` `ñ` | `ñ` = U+00F1 |
| Laterales | `l` `ll` | |
| Vibrante | `r` | |
| Semiconsonantes | `w` `y` | |

Un **grafema** es una unidad del alfabeto, aunque tenga varias letras (`chh`, `ch'`, `ll`). Toda regla de este documento cuenta grafemas, no caracteres.

Ejemplo (entrada → salida del validador):
- B: `tisqthwa` → válida (grafemas t, i, s, q, th, w, a).
- A: `tisqphyi` → válida (grafemas t, i, s, q, ph, y, i).

### CH-102 · Apóstrofo [DECISIÓN CHULUPI]

Base: D3, nivel (b). El carácter interno lo fijó el equipo.

- En todos los datos generados, el apóstrofo es **U+0027** (`'`).
- Antes de comparar o validar texto de otras fuentes, se convierten a U+0027: U+2019 `’`, U+2018 `‘`, U+02BC `ʼ`, U+00B4 `´` y U+0060 `` ` ``.
- Si hace falta publicar con la norma de L2, se reemplaza `'` por `’` al final, sin más cambios.

Ejemplo:
- B: `lamch’thwa` (entrada con U+2019) → `lamch'thwa`.
- A: `lamch’phyi` → `lamch'phyi`.

### CH-103 · Vocal larga

Base: D2; §8.2.

- Se escribe solo con los precompuestos `ä ï ü`.
- Antes de validar, el texto se normaliza a NFC. Así `a` + U+0308 (diéresis combinante) pasa a `ä`.
- En Chulupi la vocal larga solo la producen los sufijos y las palabras gramaticales, nunca las raíces (CH-209).

Ejemplo, `tisqa` "ir" en FUT 1.ª persona:
- B: `tisqa-¨` → `tisqä` — ir-1>3.FUT — "iré".
- A: `tisqa-¨` → `tisqä`. Las dos formas coinciden porque este sufijo es solo alargamiento (CH-502).

### CH-104 · Letras prohibidas

Base: §8.1 (L2 p.44).

Están prohibidos:
- `b`, `c` (salvo dentro de `ch`), `d`, `e`, `f`, `g`, `h` (salvo dentro de `ph th chh kh qh`), `o`, `v`, `z`;
- `ŋ` (§3.4: variante oral);
- vocales con tilde (`á é í ó ú`), `ë`, `ö` y la diéresis combinante U+0308 tras la normalización;
- dígitos y guiones dentro de una palabra.

Ejemplos (los mismos en los dos modos):
- `tisqe` → inválida (`e`).
- `tishwa` → inválida: `sh` no es un grafema, así que queda una `h` suelta (t-i-s-**h**-w-a).
- Contraejemplo: `tisqhwa` **es válida** (t-i-s-qh-w-a). Es otra cadena, no una palabra mal escrita.

### CH-105 · Segmentación en grafemas

Base: §8.1.

Se recorre la palabra de izquierda a derecha y en cada posición se toma **el grafema más largo** que coincida, en este orden:

```
chh, ch', ch, ph, p', th, t', kh, k', qh, q', ll,
a, i, u, ä, ï, ü, p, t, k, q, s, j, x, m, n, ñ, l, r, w, y
```

Si en una posición no coincide ninguno, la palabra es inválida.

Ejemplo:
- B: `ch'ixrthwa` → [ch', i, x, r, th, w, a].
- A: `ch'ixrphyi` → [ch', i, x, r, ph, y, i].

### CH-106 · Mayúsculas y puntuación [DECISIÓN CHULUPI]

Base: L2 escribe la mayúscula inicial y `¿…?` (`¿Jilamaxa jutaniti?`, L2 p.235).

- Solo el primer carácter de la oración va en mayúscula (`Ch'…`, `Ä…`). Todo lo demás va en minúscula.
- Las afirmativas y negativas terminan en `.`; las preguntas se escriben `¿…?`. En la v1 no hay comas.
- Los validadores trabajan sobre la oración en minúsculas y sin puntuación.

Ejemplo:
- B: `Nayaxa tisqthwa.` — A: `Muqixu tisqphyi.` — ES: "Yo voy."

```yaml
# alfabeto.yaml
version: 1
normalizacion:
  unicode: NFC
  apostrofo_interno: "'"
  apostrofos_a_convertir: ["’", "‘", "ʼ", "´", "`"]
vocales: [a, i, u]
vocales_largas: {a: "ä", i: "ï", u: "ü"}
consonantes:
  oclusiva_simple:   [p, t, ch, k, q]
  oclusiva_aspirada: [ph, th, chh, kh, qh]
  oclusiva_glotal:   ["p'", "t'", "ch'", "k'", "q'"]
  fricativa:         [s, j, x]
  nasal:             [m, n, "ñ"]
  lateral:           [l, ll]
  vibrante:          [r]
  semiconsonante:    [w, y]
punto_de_articulacion:          # para CH-205
  p:  [p, ph, "p'"]
  t:  [t, th, "t'"]
  ch: [ch, chh, "ch'"]
  k:  [k, kh, "k'"]
  q:  [q, qh, "q'"]
orden_segmentacion: [chh, "ch'", ch, ph, "p'", th, "t'", kh, "k'", qh, "q'", ll,
                     a, i, u, "ä", "ï", "ü",
                     p, t, k, q, s, j, x, m, n, "ñ", l, r, w, y]
prohibidos: [b, c, d, e, f, g, h, o, v, z, "ŋ", "á", "é", "í", "ó", "ú", "ë", "ö", "̈"]
nota_prohibidos: "c y h solo son inválidas cuando no forman parte de un grafema de la lista."
puntuacion: {afirmativa: ".", pregunta_abre: "¿", pregunta_cierra: "?"}
```

---

## 2. Fonotáctica

Hay dos niveles de control:
- **Raíz** (las inventadas): plantilla estricta.
- **Palabra** (cualquier palabra de salida, en los dos modos): reglas mínimas, porque la elisión crea grupos de consonantes legales (§5.2, L2 p.64–65).

Notación: tras segmentar (CH-105), cada grafema se cambia por su **clase**: `C` = consonante, `V` = vocal corta, `L` = vocal larga. Ejemplo: `tisqthwa` → `CVCCCCV`.

### CH-201 · Plantilla de la raíz

Base: §8.3 (L2 p.58–59: sílabas V, CV, VC, CVC; raíces mayormente bisílabas).

- Sílabas permitidas: V, CV, VC, CVC.
- Solo la primera sílaba puede empezar por vocal.
- La última sílaba es siempre CV.
- Mínimo 2 sílabas.

Comprobación sobre la cadena de clases:

```
^C?V(C{1,2}V)+$
```

Si entre dos vocales hay 2 consonantes, la primera es coda y debe estar permitida (CH-206).

Ejemplos (raíz común a los dos modos):
- `lamch'a` → `CVCCV` → válida (`lam.ch'a`).
- `lamch'tra` → `CVCCCCV` → inválida (4 consonantes seguidas).

### CH-202 · Inicio de palabra

Base: §8.3 (L2 p.42, 44; L1 p.41).

Vale para todas las palabras de los dos modos:
- Nunca hay 2 consonantes al inicio.
- La palabra no empieza por `x` ni por `r`.

Ejemplos (iguales en los dos modos): `xiku` → inválida; `rupa` → inválida; `smiqa` → inválida.

### CH-203 · Final de palabra

Base: §0.2 (L2 p.32, 60, 75); D6.

Toda palabra termina en vocal, corta o larga.

Ejemplos:
- B: `tisqä` ✓, `tisqth` ✗.
- A: `tisqä` ✓, `tisqph` ✗.

### CH-204 · Sin vocales seguidas

Base: §5.1 ("No hay grupos vocálicos", L1 p.71).

No puede haber dos vocales juntas (cortas o largas).

Ejemplos:
- B: `tisqaiwa` ✗ (debe ser `tisqiwa`).
- A: `tisqauyi` ✗ (debe ser `tisquyi`).

### CH-205 · Aspiradas y glotalizadas por raíz [DECISIÓN CHULUPI]

Base: §8.3 (L2 p.41–42). La guía dice que una raíz "admite más de una" y que las oclusivas del mismo punto "generalmente" comparten el rasgo. Esta regla es más estricta, pero cabe dentro de la guía.

Llamamos **laringalizado** a todo grafema aspirado o glotalizado: `ph th chh kh qh p' t' ch' k' q'`.

1. Un laringalizado solo puede ir al inicio de sílaba.
2. Una raíz tiene como máximo **un** grafema laringalizado distinto (puede aparecer dos veces: `t'ant'a`).
3. Si una raíz tiene dos oclusivas del mismo punto, son el mismo grafema.

Estas reglas valen solo para la raíz, no para los sufijos que se le añaden.

```
def laringales_ok(grafemas):
    lar = [g for g in grafemas if g in LARINGALIZADOS]
    if len(set(lar)) > 1: return False                  # regla 2
    for i, g in enumerate(grafemas):
        if g in LARINGALIZADOS and es_coda(grafemas, i): return False   # regla 1
    for punto, serie in PUNTO_DE_ARTICULACION.items():  # regla 3
        presentes = [g for g in grafemas if g in serie]
        if len(presentes) >= 2 and len(set(presentes)) > 1: return False
    return True
```

Ejemplos (raíz común a los dos modos):
- `q'aspi` ✓.
- `q'aspha` ✗ (dos laringalizados distintos).
- `t'ata` ✗ (`t'` y `t` del mismo punto, distintos).

### CH-206 · Codas de la raíz [DECISIÓN CHULUPI]

Base: §8.3 (L2 p.58–59). La guía no dice qué consonantes pueden cerrar sílaba.

- Codas permitidas: `p t ch k q s j x m n l r w y`.
- No pueden ser coda: `ñ`, `ll` ni los laringalizados.
- La coda no puede ser igual al inicio de la sílaba siguiente: no hay consonantes dobles dentro de una raíz.

Ejemplos (raíz común):
- `pajlla` ✓ (coda `j`).
- `tañqa` ✗ (coda `ñ`).
- `tissa` ✗ (`s` + `s`).

### CH-207 · `l` + `l` [DECISIÓN CHULUPI]

Base: §8.1 (`ll` es una sola letra).

- En la raíz, una coda `l` no puede ir antes de `l` ni de `ll`: `l` + `l` se leería como `ll`.
- El validador de palabras rechaza toda cadena `lll`.

Ejemplo (raíz común): `kalla` se lee siempre `ka.lla`; la raíz `kal.la` es imposible.

### CH-208 · Grupos en palabras con sufijos

Base: §5.2 (L2 p.64–65: hasta 6 consonantes seguidas, "se escribe el grupo").

- Entre dos vocales puede haber de 1 a 6 consonantes.
- Fuera de la raíz no se controla la composición del grupo: lo que deja la elisión es legal.

Expresión regular sobre la cadena de clases (incluye CH-202, CH-203 y CH-204; la regla de `x`/`r` se comprueba aparte):

```
^C?[VL](C{1,6}[VL])*$
```

Ejemplos:
- B: `tisqkiti` → `CVCCCVCV` ✓.
- A: `tisqñuji` → `CVCCCVCV` ✓.
- Referencia real: `jiskht'kthti` (L2 p.65) → 6 consonantes seguidas ✓.

### CH-209 · Raíces sin vocal larga [DECISIÓN CHULUPI]

Base: §8.2 (en aymara real hay vocales largas léxicas, `qüña`; aquí se excluyen).

Las raíces inventadas solo llevan `a i u`. Así, una vocal larga en una palabra siempre indica un sufijo.

Ejemplos (raíz común): `tisqa` ✓; `tïsqa` ✗.

```yaml
# fonotactica.yaml
clases: {C: consonante, V: vocal_corta, L: vocal_larga}
raiz:
  regex_clases: "^C?V(C{1,2}V)+$"
  vocales_permitidas: [a, i, u]            # CH-209
  codas_permitidas: [p, t, ch, k, q, s, j, x, m, n, l, r, w, y]   # CH-206
  prohibido_coda_igual_a_inicio: true      # CH-206
  prohibido_l_antes_de: [l, ll]            # CH-207
  laringalizados: [ph, th, chh, kh, qh, "p'", "t'", "ch'", "k'", "q'"]
  max_laringalizados_distintos: 1          # CH-205
  laringalizado_solo_inicio_de_silaba: true
  armonia_mismo_punto: true
palabra:
  regex_clases: "^C?[VL](C{1,6}[VL])*$"    # CH-202, CH-203, CH-204, CH-208
  iniciales_prohibidas: [x, r]             # CH-202
  cadenas_prohibidas: ["lll"]              # CH-207
```

---

## 3. Generador de raíces inventadas

El generador corre **una sola vez** y escribe `lexico.csv` (CH-309). El generador de oraciones nunca inventa raíces: solo las lee.

### CH-301 · Número de sílabas [DECISIÓN CHULUPI]

Base: §8.3 ("raíces mayormente bisílabas"). No hay raíces de 1 sílaba (la única de la guía, `sa-`, es irregular).

| Categoría | 2 sílabas | 3 sílabas |
|---|---|---|
| Nombres (`N_HUM`, `N_NOHUM`) | 0,70 | 0,30 |
| Verbos (`V_*`) | 0,75 | 0,25 |
| Adjetivos (`ADJ`) | 0,60 | 0,40 |
| Adverbios de tiempo (`ADV_T`) | 0,50 | 0,50 |

Ejemplo: la raíz de "ir" salió con 2 sílabas: `tis.qa`.
- B: `tisqthwa` — ir-1>3.SIMP-AFF — "voy".
- A: `tisqphyi`.

### CH-302 · Plantilla de cada sílaba [DECISIÓN CHULUPI]

Base: §8.3; CH-201.

| Posición | V | CV | VC | CVC |
|---|---|---|---|---|
| Primera | 0,10 | 0,65 | 0,05 | 0,20 |
| Intermedia | — | 0,70 | — | 0,30 |
| Última | — | 1,00 | — | — |

Ejemplo: "ir" = [CVC, CV] → `tis` + `qa`.

### CH-303 · Pesos de consonantes y vocales [DECISIÓN CHULUPI]

Base: la guía no da frecuencias. Los pesos dan raíces variadas y evitan abusar de las letras raras.

- **Inicio de sílaba** (solo consonantes simples; las laringalizadas salen en CH-305): p 0,07 · t 0,09 · ch 0,07 · k 0,09 · q 0,08 · s 0,07 · j 0,06 · x 0,04 · m 0,07 · n 0,06 · ñ 0,02 · l 0,06 · ll 0,04 · r 0,05 · w 0,05 · y 0,08.
  - En la **primera** sílaba se quitan `x` y `r` y se renormaliza (CH-202).
- **Coda:** p 0,06 · t 0,04 · ch 0,04 · k 0,08 · q 0,08 · s 0,14 · j 0,08 · x 0,06 · m 0,10 · n 0,10 · l 0,10 · r 0,08 · w 0,02 · y 0,02.
- **Vocales:** a 0,45 · i 0,25 · u 0,30.

Ejemplo: "ir" → inicios `t`, `q`; coda `s`; vocales `i`, `a`.

### CH-304 · Las raíces verbales terminan en `-a` [DECISIÓN CHULUPI]

Base: §3.4 (los paradigmas de L2 solo muestran raíces en -a: `sara-`, `muna-`, `lura-`); §5.1 (tras /u/ la /i/ de `-itu` se pierde: `us-utu`); L2 p.176 (la `-i` de 3.ª persona desaparece tras /u/: `thuqhuwa`).

En los verbos, la vocal de la última sílaba es siempre `a`. Así se evitan reglas que la guía no documenta para i/u.

Ejemplo, `tisqa` + 3>3.SIMP:
- B: `tisq-i` → `tisqi` — ir-3>3.SIMP — "va".
- A: `tisq-u` → `tisqu`.

### CH-305 · Paso de laringalización [DECISIÓN CHULUPI]

Base: §8.3; CH-205.

1. Con probabilidad 0,30, se elige al azar una oclusiva simple (`p t ch k q`) que esté al inicio de una sílaba de la raíz.
2. Se convierte en aspirada (probabilidad 0,5) o glotalizada (0,5).
3. Si otra oclusiva del mismo punto está al inicio de otra sílaba, se convierte en el mismo grafema (armonía).
4. Si una oclusiva del mismo punto está en coda, la raíz se descarta (CH-205, regla 3).

Ejemplo: `lamcha` → se elige `ch`, glotalizada → `lamch'a` "comer".
- B: `lamch'-i` → `lamch'i` — comer-3>3.SIMP — "come".
- A: `lamch'u`.

### CH-306 · Filtro contra palabras reales [DECISIÓN CHULUPI]

Base: decisión del equipo (P4).

1. **Lista `palabras_reales.txt`.** Se arma con dos fuentes:
   - **Ya:** todas las cadenas entre acentos graves de la guía. A cada cadena se le quitan `- . : ( ) † ‡ ¨` y los espacios, se parte por `/` y `~`, y se pasa a minúsculas. Por ejemplo, `chur-t-wa` → `churtwa` y `sara-:` → `sara`.
   - **Cuando esté disponible:** todos los tokens del lado aymara del *train* de AmericasNLP.
2. **Normalización** (igual para la lista y para las raíces): NFC, minúsculas, apóstrofos convertidos según CH-102, y separación en tokens por todo carácter que no sea letra del alfabeto ni `'`.
3. **Regla.** Sea `n(r)` el número de palabras **distintas** de la lista que empiezan por `r` (contando `r` misma si está en la lista). Una raíz `r` se descarta si:
   - **Modo "guía"** (la lista solo sale de la guía): `r` está en la lista, o `n(r) ≥ 1`.
   - **Modo "corpus"** (la lista incluye AmericasNLP): `r` está en la lista, o `n(r) ≥ 5`.

   El modo se fija en `generador_raices.yaml` (`filtro_real.modo`). Al pasar de "guía" a "corpus" hay que regenerar todo el léxico (CH-309).
4. **Implementación.** Un *trie* de la lista. Cada nodo guarda cuántas palabras distintas pasan por él (`n`) y si es final de palabra. Para `r`, se baja por el *trie*:
   - si `r` no es un nodo, `n(r) = 0`;
   - si es un nodo final, `r` es una palabra real.
5. **Control.** Si más del 60 % de los candidatos de una categoría se descarta, se registra un aviso. El generador sigue intentando hasta 1.000 veces por entrada y después falla con un error.

Ejemplos (filtro común a los dos modos):
- `sara` ✗ en los dos modos (palabra real).
- `kulla` ✗ en modo "guía" (inicio de `kullaka`, §2.1). En modo "corpus" solo se descarta si 5 o más palabras distintas del corpus empiezan por `kulla`.
- `lapi` ✗ en modo "guía" (inicio de `lapisa`, §8.3).
- `tisqa` ✓.

### CH-307 · Raíz ≠ morfema o palabra gramatical [DECISIÓN CHULUPI]

Una raíz no puede ser igual a ninguna forma de `morfemas.yaml` (B ni A) ni a ninguna palabra gramatical (B ni A; §5 de este documento).

Ejemplos: `muqi` ✗ (pronombre 1 del modo A); `naya` ✗ (pronombre 1 del modo B, y además real).

### CH-308 · La raíz no termina en un sufijo [DECISIÓN CHULUPI]

Base: reduce la ambigüedad de segmentación entre raíz y sufijo.

- Una raíz no puede terminar en ninguna forma de sufijo (B o A) de **3 grafemas o más**.
- Las terminaciones cortas (`-ta`, `-sa`, `-na`, `-ka`, `-ru`…) están permitidas, como en aymara real (`marka`, `wawa`, `t'ant'a`).
- La lista exacta se calcula desde `morfemas.yaml`. Por eso las raíces se generan **después** de fijar la tabla de formas A (CH-503). Con la tabla de §5 de este documento, las terminaciones prohibidas son:
  - **B:** `naka`, `taki`, `kama`, `layku`, `tana`, `tama`, `ista`, `istu`, `itu`, `ñäni`, `pxa`, `ska`, `sma`, `mpi`.
  - **A:** `sulu`, `puli`, `chiwi`, `tiwqa`, `kilu`, `kiqu`, `ulqa`, `ulqu`, `uqu`, `thäqi`, `mtu`, `nchi`, `jmi`, `nku`.

Ejemplos (filtro común):
- `kurnaka` ✗ (termina en B `-naka`).
- `pilampi` ✗ (B `-mpi`).
- `wisulu` ✗ (A `-sulu`).
- `chimuka` ✓ (`-ka` tiene 2 grafemas).
- `chimula` ✓.

### CH-309 · Diccionario fijo [DECISIÓN CHULUPI]

- Cada **sentido** español (una fila de `lexico.csv`) recibe exactamente una raíz, y dos sentidos nunca comparten raíz.
- El generador de raíces usa una semilla fija (`semilla_raices` en `generador_raices.yaml`) y recorre el léxico por `id`. Así el resultado es reproducible.
- `lexico.csv` se guarda bajo control de versiones. Cambiar una raíz exige subir la versión del léxico y regenerar todos los datos.

Ejemplo: "ir" (L0013) → `tisqa` en todas las oraciones y en los dos modos.

### CH-310 · Raíz ≠ otra raíz + sufijo [DECISIÓN CHULUPI]

Para todo par de raíces `r1`, `r2` y toda forma de sufijo `s` (B o A, de 1 grafema o más, sin contar `-¨`): `r2 != r1 + s`. La prueba se hace al aceptar cada raíz nueva, contra todas las ya aceptadas, en los dos sentidos.

Ejemplo: si ya existe `kirpu`, se rechaza `kirpuru` (= `kirpu` + B `-ru`) y también `kirpullu` (= `kirpu` + A `-llu`).

### 3.1 Algoritmo completo

```
entrada: lexico_sin_raices (ordenado por id), morfemas.yaml, palabras_gramaticales,
         palabras_reales.txt, semilla
salida:  lexico.csv con la columna raiz llena

rng = Random(semilla)
trie = construir_trie(normalizar(palabras_reales))
prohibidas_iguales = formas_morfemas(B, A) ∪ palabras_gramaticales(B, A)
terminaciones_prohibidas = {s for s in formas_sufijos(B, A) if len(grafemas(s)) >= 3}
aceptadas = {}

para cada entrada e en el léxico:
    repetir hasta 1000 veces:
        n = elegir_silabas(e.categoria)                     # CH-301
        silabas = []
        para i en 1..n:
            plantilla = elegir_plantilla(posicion(i, n))    # CH-302
            silabas.append(rellenar(plantilla, pesos))      # CH-303; sin x/r en i=1
        si e.categoria es verbo: vocal final = 'a'          # CH-304
        r = unir(silabas)
        r = laringalizar(r, p=0.30)                         # CH-305
        si no es_raiz_valida(r): continuar                  # CH-201..CH-209
        si trie.es_palabra(r): continuar                    # CH-306
        si trie.n(r) >= UMBRAL[modo]: continuar             # CH-306: guía = 1, corpus = 5
        si r in prohibidas_iguales: continuar               # CH-307
        si algun s en terminaciones_prohibidas con r.endswith(s): continuar   # CH-308
        si r in aceptadas: continuar                        # CH-309
        si choca_raiz_mas_sufijo(r, aceptadas): continuar   # CH-310
        aceptadas[r] = e.id; e.raiz = r; salir del bucle
    si no se aceptó ninguna: ERROR(e.id)
```

Traza de ejemplo ("ir", verbo):
- Paso 1, 2 sílabas: [CVC, CV] → `tis` + `qa`.
- Paso 2, vocal final `a`: ya lo era.
- Paso 3, laringalización: no se aplica (sorteo > 0,30).
- Paso 4, filtros: los pasa todos → `tisqa`.
- Uso, la misma raíz en los dos modos:
  - B: `tisq-th-wa` → `tisqthwa`.
  - A: `tisq-ph-yi` → `tisqphyi`.

```yaml
# generador_raices.yaml
semilla_raices: 20261119
silabas:                       # CH-301
  N_HUM:   {2: 0.70, 3: 0.30}
  N_NOHUM: {2: 0.70, 3: 0.30}
  V_INTR:  {2: 0.75, 3: 0.25}
  V_MOV:   {2: 0.75, 3: 0.25}
  V_TR:    {2: 0.75, 3: 0.25}
  V_DITR:  {2: 0.75, 3: 0.25}
  ADJ:     {2: 0.60, 3: 0.40}
  ADV_T:   {2: 0.50, 3: 0.50}
plantillas:                    # CH-302
  primera:    {V: 0.10, CV: 0.65, VC: 0.05, CVC: 0.20}
  intermedia: {CV: 0.70, CVC: 0.30}
  ultima:     {CV: 1.00}
inicio:                        # CH-303
  {p: .07, t: .09, ch: .07, k: .09, q: .08, s: .07, j: .06, x: .04,
   m: .07, n: .06, "ñ": .02, l: .06, ll: .04, r: .05, w: .05, y: .08}
inicio_prohibido_primera_silaba: [x, r]
coda:
  {p: .06, t: .04, ch: .04, k: .08, q: .08, s: .14, j: .08, x: .06,
   m: .10, n: .10, l: .10, r: .08, w: .02, y: .02}
vocales: {a: .45, i: .25, u: .30}
vocal_final_verbos: a          # CH-304
laringalizacion:               # CH-305
  probabilidad: 0.30
  tipo: {aspirada: 0.5, glotalizada: 0.5}
filtro_real:                   # CH-306
  archivo: palabras_reales.txt
  modo: guia                   # guia | corpus
  descartar_si_igual: true
  umbral_prefijo: {guia: 1, corpus: 5}   # nº mínimo de palabras distintas que empiezan por la raíz
  aviso_si_rechazo_mayor_que: 0.60
  max_intentos: 1000
terminacion_prohibida_min_grafemas: 3     # CH-308
```

---

## 4. Léxico

### CH-401 · Categorías y por qué importan

Base: §7.3 A (COMPL.RU), §2 (casos), D9, §13 #7.

| Código | Qué es | Para qué sirve en la gramática |
|---|---|---|
| `N_HUM` | Nombre de persona (`clase_sem = persona`) | Solo estos pueden ser COMPL.RU (CH-909), poseedor con GEN (CH-911) y beneficiario. Tienen `genero` (CH-1010). |
| `N_NOHUM` | Nombre no humano; su `clase_sem` es cualquiera salvo `persona` (CH-406) | El objeto directo, los lugares, los instrumentos y las causas se eligen por su clase (CH-406). |
| `V_INTR` | Verbo intransitivo sin movimiento ("dormir") | Admite LOC; no admite OD, ALL, ABL ni UNTIL. |
| `V_MOV` | Verbo de movimiento ("ir", "venir") | Admite ALL (destino), ABL (origen) y UNTIL; no admite OD ni LOC. |
| `V_TR` | Verbo transitivo ("comer", "ver") | OD obligatorio en X>3 (CH-915). Con `obj_persona = s`, admite transiciones con objeto 1/2/4 (CH-604). |
| `V_DITR` | Verbo con destinatario ("dar") | Como `V_TR`, y además admite COMPL.RU (`rige_ru = s`, CH-909). Sus transiciones con objeto 1/2/4 marcan al destinatario. |
| `ADJ` | Adjetivo; `subcat` = `tamano`, `color` u `otro` | Va antes del nombre (CH-912) y puede ser predicado de "ser". Solo modifica nombres de las clases de su `mod_clases` (CH-406). |
| `ADV_T` | Adverbio de tiempo; `subcat` = `pasado`, `presente` o `futuro` | Limita el tiempo verbal y decide el tiempo español del SIMP (CH-1001). |

No están en el léxico:
- **Adverbios de lugar.** "Aquí", "ahí" y "más allá" son demostrativo + LOC (CH-916).
- **Palabras gramaticales.** Pronombres, `jani`, interrogativos, demostrativos y numerales (§5.2 de este documento).

Ejemplo de CH-401 (COMPL.RU solo con `N_HUM`):
- Idea: dar, 1>3.SIMP, sujeto `naya`, destinatario "niño" (`N_HUM`), OD "pan".
- B: `Naya-xa lisqu-ru q'aspi tulph-th-wa.` → `Nayaxa lisquru q'aspi tulphthwa.` — 1-TOP niño-COMPL.RU pan dar-1>3.SIMP-AFF — "Yo le doy pan al niño."
- A: `Muqi-xu lisqu-llu q'aspi tulph-ph-yi.` → `Muqixu lisqullu q'aspi tulphphyi.`
- Rechazo: el mismo verbo con destinatario "perro" (`N_NOHUM`) no es una idea válida (CH-909).

Ejemplo de CH-401 (`V_MOV` + ALL):
- B: `Jupaxa wirkharu tisqiwa.` — 3-TOP pueblo-ALL ir-3>3.SIMP-AFF — "Él va al pueblo." (`genero = m`).
- A: `Kaxixu wirkhallu tisquyi.`

### CH-402 · Formato de `lexico.csv`

**Quién lo produce.** El **rol 1** entrega `lexico_sin_raices.csv` con todas las columnas de esta tabla salvo `raiz` y `silabas`. El generador de raíces (§3) llena esas dos y escribe `lexico.csv`. Nadie más modifica el archivo.

**Formato.** UTF-8 (NFC), separador `,`, una fila por sentido. Las listas de clases van separadas por `|`. `-` significa "no aplica" o "usar la regla general de CH-406"; cada columna dice cuál de los dos.

| Columna | Valores | Uso |
|---|---|---|
| `id` | `L0001`… | Clave única |
| `cat` | `N_HUM`, `N_NOHUM`, `V_INTR`, `V_MOV`, `V_TR`, `V_DITR`, `ADJ`, `ADV_T` | CH-401 |
| `subcat` | ADJ: `tamano`/`color`/`otro`; ADV_T: `pasado`/`presente`/`futuro`; resto: `-` | CH-401 |
| `clase_sem` | Nombres: una clase de CH-406; resto: `-` | CH-406 |
| `es_m` | Forma base española: masculino singular, o infinitivo en los verbos | §10 |
| `es_f` | Femenino singular (`N_HUM` con `genero = var` y `ADJ`); vacío en el resto | §10 |
| `es_pl_m`, `es_pl_f` | Plurales españoles | §10 |
| `genero` | `m`, `f`, `var` (nombres); `-` (resto) | CH-405 |
| `contable` | `s`/`n` (nombres); `-` (resto) | Artículos (CH-1008) |
| `raiz` | Raíz inventada (la llena §3) | CH-3xx |
| `silabas` | 2 o 3 (la llena §3) | CH-514 (`-kama`) |
| `rango` | Rango de frecuencia dentro de la categoría (1 = más frecuente) | CH-403 |
| `rige_ru` | Verbos: `s`/`n` (solo `V_DITR` puede ser `s`); resto: `-` | CH-909 |
| `obj_persona` | `V_TR` y `V_DITR`: `s`/`n`; resto: `-` | CH-604 |
| `suj_clases` | Verbos: lista obligatoria de clases del sujeto; resto: `-` | CH-406 |
| `obj_clases` | `V_TR` y `V_DITR`: lista obligatoria de clases del OD (nunca `persona`); resto: `-` | CH-406, CH-914 |
| `instr_clases` | Verbos: clases aceptadas como instrumento con COM; `-` = el verbo no admite instrumento | CH-406 |
| `loc_clases` | Verbos: clases aceptadas con LOC; `-` = regla general; `NINGUNA` = no admite LOC | CH-406 |
| `mod_clases` | `ADJ`: lista obligatoria de clases que puede modificar; resto: `-` | CH-406 |
| `notas` | Texto libre | — |

**Rango.** Se toma de la frecuencia del lema en el lado español del *train* de AmericasNLP (es–aym), para acercarse al dominio real. Si un lema no aparece ahí, va al final de su categoría, ordenado alfabéticamente.

### CH-403 · Frecuencias (Zipf) [DECISIÓN CHULUPI]

Dentro de cada categoría, la probabilidad de elegir la entrada de rango `k` es:

```
p(k) = (1 / k^0.9) / Σ_j (1 / j^0.9)
```

- El exponente 0,9 (algo menor que 1) aplana un poco la curva: las palabras frecuentes dominan sin acaparar.
- Cuando CH-406 restringe las candidatas (por ejemplo, solo `comida`), la fórmula se aplica sobre las candidatas, conservando su orden de rango.

Ejemplo: si "pan" es el nombre de rango 1 entre los de `clase_sem = comida`, `q'aspi` sale unas 8 veces más que la comida de rango 10 (1,000 frente a 0,126).
- B: `Nayaxa q'aspi lamch'thwa.` — 1-TOP pan comer-1>3.SIMP-AFF — "Yo como pan."
- A: `Muqixu q'aspi lamch'phyi.`

### CH-404 · Cobertura mínima [DECISIÓN CHULUPI]

- Después de muestrear todo el conjunto, se cuenta cuántas veces aparece cada entrada.
- Para cada entrada con menos de 20 apariciones, se generan ideas extra que la obliguen (fijando ese lema y muestreando el resto con CH-406) hasta llegar a 20.
- Esas ideas se mezclan con el resto.

Ejemplo: si "palo" (`salmi`, `herramienta`) aparece 12 veces, se añaden 8 ideas con `salmi`. Por ejemplo, como objeto de "comprar" (que acepta `herramienta`):
- B: `Jupaxa salmi nirqiwa.` — 3-TOP palo comprar-3>3.SIMP-AFF — "Él compra el palo."
- A: `Kaxixu salmi nirquyi.`

### CH-405 · Género español en el léxico [DECISIÓN CHULUPI]

- `N_HUM` con dos formas españolas (niño/niña): `genero = var`. La forma la decide el campo `genero` de la idea (CH-1010).
- `N_HUM` con una sola forma (mujer): `genero` fijo.
- `N_NOHUM` (incluidos los animales): género gramatical fijo del español ("perro" = m). En v1 los animales no usan el campo `genero`.
- `ADJ`: `es_m` / `es_f` concuerdan con el nombre al que modifican, o con el sujeto si son predicado.

Ejemplo (`lisqu` = niño/niña):
- B: `Lisquxa tisqiwa.` — niño-TOP ir-3>3.SIMP-AFF.
- A: `Lisquxu tisquyi.`
- ES: "El niño va." (`genero = m`) / "La niña va." (`genero = f`).

### CH-406 · Coherencia semántica [DECISIÓN CHULUPI]

Base: decisión del equipo (v1.1). Un lenguaje artificial cuyas palabras co-ocurren de forma coherente transfiere mejor (Ri y Tsuruoka, 2022). La guía no trata la semántica léxica.

**1. Clases de los nombres (`clase_sem`).** Todo nombre tiene exactamente una clase.

| Clase | Qué incluye | Ejemplos |
|---|---|---|
| `persona` | Todo `N_HUM` (y nada más) | niño, mujer, maestro |
| `animal` | Animales | perro, llama, pájaro |
| `comida` | Alimentos sólidos | pan, papa, carne |
| `bebida` | Líquidos que se beben | agua, leche, chicha |
| `ropa` | Prendas y tejidos | poncho, aguayo, sombrero |
| `herramienta` | Objetos para hacer algo | palo, cuchillo, pala |
| `recipiente` | Objetos que contienen | olla, vaso, bolsa |
| `planta` | Plantas y sus partes | árbol, flor, hierba |
| `lugar` | Lugares abiertos o poblados | pueblo, mercado, río, cerro |
| `vivienda` | Construcciones y sus partes | casa, cuarto, corral |
| `tiempo` | Nombres de periodos | día, noche, año |
| `abstracto` | Ideas, sucesos, estados | deuda, trabajo, fiesta |
| `objeto` | Otros objetos concretos | piedra, libro, mesa |

**2. Clases que acepta cada palabra.**
- Verbos: `suj_clases` (siempre); `obj_clases` (siempre en `V_TR` y `V_DITR`); `instr_clases` y `loc_clases` (opcionales).
- Adjetivos: `mod_clases` (siempre).

**3. Reglas generales**, para todo lo que no fija una columna:

| Función | Clases aceptadas |
|---|---|
| Sujeto | `suj_clases` del verbo. Los pronombres de 1.ª, 2.ª y 4.ª persona y `jupa` cuentan como `persona`. |
| Objeto directo | `obj_clases` del verbo; nunca `persona` (CH-914). |
| COMPL.RU | `persona` (CH-909). |
| BEN | `persona`; solo con `V_TR` y `V_DITR` (v1.1.1). `V_MOV` y `V_INTR` no llevan objeto indirecto. |
| COM, instrumento | `instr_clases` del verbo; si es `-`, el verbo no admite instrumento. |
| COM, compañía | `persona` o `animal`; solo con `V_MOV` o `V_INTR` y sujeto de clase `persona`. |
| LOC | `loc_clases` del verbo; si es `-`: `lugar` o `vivienda`; si es `NINGUNA`: no admite LOC. Los `V_MOV` llevan siempre `NINGUNA`. |
| ALL, ABL | `lugar` o `vivienda` (solo con `V_MOV`). |
| UNTIL | `lugar`, `vivienda` o `tiempo` (solo con `V_MOV`; además CH-514). |
| CAUSE | `abstracto`, o `persona` (nombre o pronombre). |
| Adjetivo (modificador o predicado de "ser") | `mod_clases` del adjetivo. |
| Poseedor (GEN) | `persona`. |
| Poseído | Cualquier clase salvo `tiempo`. |
| "Estar en": sujeto | Cualquier clase salvo `lugar`, `tiempo` y `abstracto`. |
| "Estar en": lugar | `lugar`, `vivienda` o `recipiente`. |
| "Tener": poseedor | `persona`. |
| "Tener": lo poseído | `animal`, `comida`, `bebida`, `ropa`, `herramienta`, `recipiente`, `planta`, `vivienda`, `objeto`. |

**4. Cómo lo usa el generador de ideas.** El orden importa:
1. Elige primero el predicado (verbo, adjetivo de "ser", o "estar"/"tener").
2. Para cada función, filtra el léxico con estas reglas.
3. Dentro de las candidatas, muestrea con Zipf (CH-403).
4. Si alguna función obligatoria queda sin candidatas, descarta la idea y vuelve a empezar.

El validador (§13 de este documento) vuelve a comprobar todas las restricciones en cada par.

Ejemplos:
- ✓ Instrumento compatible ("cortar" acepta `herramienta`):
  - B: `Nayaxa jitqumpi q'aspi k'iymthwa.` — 1-TOP cuchillo-COM pan cortar-1>3.SIMP-AFF — "Yo corto pan con el cuchillo."
  - A: `Muqixu jitqunku q'aspi k'iymphyi.`
- ✗ "Yo como el palo": `salmi` es `herramienta` y "comer" solo acepta `comida`. La idea se descarta en los dos modos.
- ✗ "Él compra pan con el palo": "comprar" tiene `instr_clases = -`. La idea se descarta.

### CH-407 · Tamaño objetivo del léxico [DECISIÓN CHULUPI]

Lo fija el equipo (v1.1). El rol 1 debe llegar a estas cifras aproximadas. El reparto entre los tipos de verbo es una decisión de este documento.

| Categoría | Entradas |
|---|---|
| `N_HUM` | 300 |
| `N_NOHUM` | 1.700 (cada `clase_sem` con al menos 30) |
| `V_INTR` | 150 |
| `V_MOV` | 100 |
| `V_TR` | 450 |
| `V_DITR` | 100 |
| **Verbos en total** | **800** |
| `ADJ` | 300 |
| `ADV_T` | 30 |
| **Total** | **≈ 3.130** |

Ejemplo, con uno de los 30 `ADV_T`:
- B: `Nayaxa jaskhi wirkharu tisqthwa.` — 1-TOP ayer pueblo-ALL ir-1>3.SIMP-AFF — "Yo fui al pueblo ayer."
- A: `Muqixu jaskhi wirkhallu tisqphyi.`

### 4.1 Entradas de ejemplo

Estas raíces son **ejemplos**. Cumplen CH-201 a CH-310 contra la guía. Cuando llegue la lista de AmericasNLP, el filtro CH-306 puede reemplazar alguna; los ejemplos de este documento se regenerarán con el léxico final.

```csv
id,cat,subcat,clase_sem,es_m,es_f,es_pl_m,es_pl_f,genero,contable,raiz,silabas,rango,rige_ru,obj_persona,suj_clases,obj_clases,instr_clases,loc_clases,mod_clases,notas
L0001,N_HUM,-,persona,niño,niña,niños,niñas,var,s,lisqu,2,1,-,-,-,-,-,-,-,
L0002,N_HUM,-,persona,hermano,hermana,hermanos,hermanas,var,s,pultiya,3,2,-,-,-,-,-,-,-,
L0003,N_HUM,-,persona,maestro,maestra,maestros,maestras,var,s,yaruqhi,3,3,-,-,-,-,-,-,-,
L0004,N_HUM,-,persona,mujer,,mujeres,,f,s,simlla,2,4,-,-,-,-,-,-,-,
L0005,N_NOHUM,-,vivienda,casa,,casas,,f,s,chimula,3,1,-,-,-,-,-,-,-,
L0006,N_NOHUM,-,comida,pan,,panes,,m,n,q'aspi,2,2,-,-,-,-,-,-,-,
L0007,N_NOHUM,-,lugar,pueblo,,pueblos,,m,s,wirkha,2,3,-,-,-,-,-,-,-,
L0008,N_NOHUM,-,animal,perro,,perros,,m,s,kirpu,2,4,-,-,-,-,-,-,-,
L0009,N_NOHUM,-,lugar,mercado,,mercados,,m,s,pinqara,3,5,-,-,-,-,-,-,-,
L0010,N_NOHUM,-,herramienta,palo,,palos,,m,s,salmi,2,6,-,-,-,-,-,-,-,
L0011,N_NOHUM,-,herramienta,cuchillo,,cuchillos,,m,s,jitqu,2,7,-,-,-,-,-,-,-,
L0012,N_NOHUM,-,abstracto,deuda,,deudas,,f,s,ch'alqu,2,8,-,-,-,-,-,-,-,
L0013,V_MOV,-,-,ir,,,,-,-,tisqa,2,1,n,-,persona|animal,-,-,NINGUNA,-,
L0014,V_MOV,-,-,venir,,,,-,-,pajlla,2,2,n,-,persona|animal,-,-,NINGUNA,-,
L0015,V_INTR,-,-,dormir,,,,-,-,nuyk'a,2,1,n,-,persona|animal,-,-,-,-,
L0016,V_TR,-,-,comer,,,,-,-,lamch'a,2,1,n,n,persona|animal,comida,herramienta,-,-,
L0017,V_TR,-,-,ver,,,,-,-,ch'ixra,2,2,n,s,persona|animal,animal|comida|bebida|ropa|herramienta|recipiente|planta|vivienda|objeto,-,-,-,
L0018,V_DITR,-,-,dar,,,,-,-,tulpha,2,1,s,s,persona,comida|bebida|ropa|herramienta|recipiente|animal|planta|objeto,-,-,-,
L0019,V_TR,-,-,comprar,,,,-,-,nirqa,2,3,n,n,persona,comida|bebida|ropa|herramienta|recipiente|animal,-,-,-,
L0020,V_TR,-,-,cortar,,,,-,-,k'iyma,2,4,n,n,persona,comida|planta|ropa,herramienta,-,-,
L0021,ADJ,tamano,-,grande,grande,grandes,grandes,-,-,jumpu,2,1,-,-,-,-,-,-,persona|animal|comida|ropa|herramienta|recipiente|planta|lugar|vivienda|objeto,
L0022,ADJ,color,-,rojo,roja,rojos,rojas,-,-,q'ulli,2,2,-,-,-,-,-,-,animal|comida|bebida|ropa|herramienta|recipiente|planta|vivienda|objeto,
L0023,ADV_T,pasado,-,ayer,,,,-,-,jaskhi,2,1,-,-,-,-,-,-,-,
L0024,ADV_T,futuro,-,mañana,,,,-,-,sik'uyu,3,2,-,-,-,-,-,-,-,
L0025,ADV_T,presente,-,ahora,,,,-,-,nuspi,2,3,-,-,-,-,-,-,-,
```

Ejemplo con entradas de la tabla (LOC + `V_INTR`; `chimula` es `vivienda`, aceptada por la regla general de LOC):
- B: `Naya-xa chimula-na nuyk'-th-wa.` → `Nayaxa chimulana nuyk'thwa.` — 1-TOP casa-LOC dormir-1>3.SIMP-AFF — "Yo duermo en la casa."
- A: `Muqi-xu chimula-mu nuyk'-ph-yi.` → `Muqixu chimulamu nuyk'phyi.`

---

## 5. Inventario de morfemas

### 5.0 Dos propiedades de cada sufijo

Toda la caída de vocales (§5.3 de la guía, nivel a) se calcula con dos columnas de la tabla. El algoritmo completo está en §7 de este documento.

**`antes`**: qué le hace el sufijo a la vocal **corta** final de lo que tiene delante.
- `V`: la conserva (sufijo "débil" de L2, "pide vocal" de L1).
- `C`: la borra (sufijo "fuerte" de L2, "pide consonante" de L1).
- `—`: no le hace nada; decide el morfema anterior con su columna `después`. Es el caso de los oracionales, que "se acomodan" (L1 p.70).

**`después`**: qué pasa con la vocal final **propia** del sufijo cuando le sigue un morfema con `antes = —` (un oracional).
- `C`: la pierde.
- `V`: la conserva.

Si le sigue un morfema con `antes = V` o `C`, manda ese morfema. Al final de palabra la vocal siempre se conserva (CH-203).

Además:
- Una vocal larga nunca se borra (L1 p.71; CH-703).
- Para "tener", VBLZ.LONG tras POSR no se escribe, pero protege la vocal anterior (CH-705).

Ejemplo, `tisqa` + P1 (`antes C`, `después C`) + AFF (`antes —`):
- P1 borra la `a` de la raíz: `tisq` + `tha`.
- AFF no decide; P1 tiene `después C`, así que su `a` cae: `tisq` + `th` + `wa`.
- B: `tisqthwa` — ir-1>3.SIMP-AFF — "voy" (patrón de `sarthwa`, L2 p.176).
- A: `tisqphyi`.

### CH-501 · Mapeo A por forma [DECISIÓN CHULUPI]

Base: decisión del equipo (P2).

- Cada **cadena** B distinta recibe **una** cadena A. Si dos morfemas B se escriben igual (homófonos), su forma A también es igual. Así el modo A conserva la ambigüedad del modo B.
- Las propiedades `antes` / `después` siguen siendo las de cada morfema (id), no las de la cadena.
- Si una forma B empieza con alargamiento (`¨ta`), su forma A es `¨` + la forma A de la parte segmental, si esa parte existe como cadena en la tabla (`ta` → `ku`, así que `¨ta` → `¨ku`).

Homófonos B de la v1 y su forma A común:

| Cadena B | Ids | Cadena A |
|---|---|---|
| `-ta` | P2, ABL | `-ku` |
| `-sa` | POSS.4, Q.INF | `-khu` |
| `-ni` | POSR, FUT.3 | `-phu` |
| `-na` | GEN, LOC, P3.REM | `-mu` |
| `-ka` | VBLZ.KA, NEG (INCOMPL) | `-ñu` |
| `-ti` | Q.YN, NEG.TI | `-ji` |
| `-ru` | ALL, COMPL.RU | `-llu` |

Ejemplo (`-ta` de 2.ª persona y `-ta` ablativo):
- B: `tisq-ta-wa` → `tisqtawa` — ir-2>3.SIMP-AFF — "vas"; `wirkha-ta` → `wirkhata` — pueblo-ABL — "del pueblo".
- A: `tisq-ku-yi` → `tisqkuyi`; `wirkha-ku` → `wirkhaku`.

### CH-502 · El alargamiento se conserva en A [DECISIÓN CHULUPI]

Base: §8.2 (en L2 el alargamiento es un morfema: `-¨`).

- Un morfema que es solo alargamiento (FUT.1, VBLZ.LONG y el alomorfo `-¨-` de REM.C) no tiene letras que reemplazar: en A es el mismo alargamiento.
- Si un sufijo B tiene vocal larga en una sílaba (`-yä-`, `-ñäni`), su forma A tiene vocal larga en la misma sílaba (`-jü-`, `-thäqi`).
- Consecuencia: `raíz + FUT.1` es igual en los dos modos.

Ejemplo:
- B: `tisqa-¨` → `tisqä` — ir-1>3.FUT — "iré".
- A: `tisqa-¨` → `tisqä`.

### CH-503 · Tabla fija de formas A [DECISIÓN CHULUPI]

Las formas A de la tabla CH-504 son fijas. Cumplen estas condiciones, que el script de CH-1301 comprueba:
1. Mismo número de sílabas que la forma B.
2. Mismo tipo de inicio: vocal, una consonante o dos consonantes (`-sma` → `-jmi`).
3. Vocal larga en la misma sílaba (CH-502).
4. Solo letras del alfabeto (CH-101).
5. No son iguales a ningún sufijo real citado en la guía (§2, §3, §4).
6. Dos cadenas B distintas nunca tienen la misma forma A.
7. Toda palabra que formen pasa CH-202 a CH-208.

Las palabras gramaticales A (CH-505) pasan además el filtro CH-306, como las raíces. Si una no lo pasa, se cambia y se sube la versión de `morfemas.yaml`.

Ejemplo de la condición 2:
- B: `ch'ixr-sma-wa` → `ch'ixrsmawa` — ver-1>2.SIMP-AFF — "te veo".
- A: `ch'ixr-jmi-yi` → `ch'ixrjmiyi`.

### CH-504 · Tabla de morfemas

Abreviaturas de la tabla:
- **Slot:** posición en la palabra (§6 de este documento).
- **Antes / Después:** ver 5.0.
- **Se combina con / No se combina con:** restricciones de v1. Las de orden están en §6.

#### Nombre

| Id | Función | B | A | Slot | Antes | Después | Se combina con | No se combina con | Guía |
|---|---|---|---|---|---|---|---|---|---|
| PL | plural | `-naka` | `-sulu` | N1 | V | V | nombres, pronombres 2/3/4, demostrativos; POSS, caso y POSR después | numeral en la frase (§13 #11); `naya` (usa `nänaka`) | §2; §2.1 (L2 p.152) |
| POSS.1 | poseedor 1 | `-ja` | `-lu` | N2 | V | V | PL antes; caso después | POSR; pronombres | D4; §2.1 (L2 p.149) |
| POSS.2 | poseedor 2 | `-ma` | `-qi` | N2 | V | V | ídem | ídem; variante elidida `an-ma` (§13 #5) | §2.1; §5.2.1 |
| POSS.3 | poseedor 3 | `-pa` | `-chu` | N2 | V | V | ídem | ídem | §2.1 (L2 p.148) |
| POSS.4 | poseedor 4 | `-sa` | `-khu` | N2 | V | V | ídem | ídem | §2.1 (L2 p.148) |
| POSR | "tener" | `-ni` | `-phu` | N3 | V | V | PL antes; VBLZ.LONG o AFF/Q.YN después | POSS (L1 p.205); caso; pronombres | §2; §8.4 (L2 p.57) |
| GEN | poseedor (de) | `-na` | `-mu` | N4 | V | V | poseedor `persona`; PL y POSS antes | cualquier sufijo después | §2.1 (L2 p.154) |
| LOC | en | `-na` | `-mu` | N4 | V | V | VBLZ.KA después | oracionales después (CH-901) | §2.1 (L2 p.158) |
| ALL | a, hacia (no humano) | `-ru` | `-llu` | N4 | V | V | oracionales después | `persona` | D9; §2.1 (L2 p.155–156) |
| COMPL.RU | a (destinatario humano) | `-ru` | `-llu` | N4 | V | V | `persona`; pronombres | BEN en la oración (CH-910) | D9; §7.3 A |
| ABL | de, desde | `-ta` | `-ku` | N4 | V | V | — | `-wa` después (L1 p.280–281) | §2.1 (L2 p.158–159) |
| COM | con | `-mpi` | `-nku` | N4 | V | V | oracionales después | — | §2.1 (L2 p.159–160) |
| BEN | para | `-taki` | `-puli` | N4 | V | V | oracionales después | COMPL.RU en la oración | §2.1 (L2 p.158) |
| UNTIL | hasta | `-kama` | `-chiwi` | N4 | V | V | raíz nominal de 2 sílabas sin otros sufijos | PL, POSS antes; raíz de 3 sílabas (CH-514) | §5.2.1 |
| CAUSE | por, a causa de | `-layku` | `-tiwqa` | N4 | V | V | oracionales después | — | §2.1 (L2 p.160–161); CH-515 |
| VBLZ.KA | estar (en) | `-ka` | `-ñu` | N5 | C | (le sigue persona) | solo tras LOC; P1, P2, P3, P4 después | todo lo demás | §7.1; §5.2 (L2 p.50, `utankthwa`) |
| VBLZ.LONG | ser | `-¨` | `-¨` | N5 | V | (vocal larga) | raíz nominal o adjetivo sin sufijos (+ P1/P2/P4); tras POSR (CH-705) | P3; PL; caso | §8.2 (L2 p.49–52); §8.4 |

#### Verbo

| Id | Función | B | A | Slot | Antes | Después | Se combina con | No se combina con | Guía |
|---|---|---|---|---|---|---|---|---|---|
| PL.V | plural del sujeto | `-pxa` | `-mtu` | V1 | V | (le sigue persona o tiempo) | todos los tiempos y personas | PROG, NEG (CH-603) | D11; §3.4 (L2 p.181, 184–185) |
| PROG | progresivo | `-ska` | `-nchi` | V1 | V | (ídem) | solo SIMP | PL.V, NEG, FUT, REM (CH-606) | D11; §3.4 (L2 p.202) |
| NEG | INCOMPL de la negación | `-ka` | `-ñu` | V1 | C | (ídem) | SIMP, FUT; exige NEG.TI | PL.V, PROG, REM (CH-605) | D9; §3.3; L2 p.65, 231 |
| REM.C | pasado visto | `-yä-` ante P1, P2, P4; `-¨-` ante P3.REM | `-jü-`; `-¨-` | V4 | V | (vocal larga) | P1, P2, P4, P3.REM | transiciones; NEG; PROG | §3.4 (L2 p.184–185); §8.2 |
| REM.L | pasado no visto | `-tä-` | `-wü-` | V4 | V | (vocal larga) | ídem | ídem | §3.4 (L2 p.186) |
| P1 | 1(>3) | `-tha` | `-phi` | V5, N6 | C | C | SIMP, REM, ser, estar, tener | FUT | D5; L2 p.176 |
| P2 | 2(>3) | `-ta` | `-ku` | V5, N6 | C | V | ídem | FUT | L2 p.177 |
| P3 | 3>3 | `-i` | `-u` | V5, N6 | C | V | SIMP; estar | REM, FUT; ser, tener | L2 p.176 |
| P4 | 4(>3) | `-tana` | `-kilu` | V5, N6 | C | C | SIMP, REM, ser, estar, tener | FUT | L2 p.178, 184 |
| P3.REM | 3 en REM | `-na` | `-mu` | V5 | — | V | solo tras REM.C (`-¨-`) o REM.L | todo lo demás | §3.4 (`saräna`, `saratäna`) |
| T12 | 1>2 | `-sma` | `-jmi` | V5 | C | V | SIMP; `obj_persona = s` | FUT, REM | §3.4 (L2 p.179) |
| T21 | 2>1 | `-ista` | `-ulqa` | V5 | C | V | ídem | ídem | §3.4 (L2 p.179) |
| T31 | 3>1 | `-itu` | `-uqu` | V5 | C | V | ídem | ídem | §3.4 (L2 p.180) |
| T32 | 3>2 | `-tama` | `-kiqu` | V5 | C | C [DERIVADA] | ídem | ídem | §3.4 (L2 p.180); L1 p.144 (`-tam`, c_c) |
| T34 | 3>4 | `-istu` | `-ulqu` | V5 | C | V | ídem | ídem | §3.4 (L2 p.180) |
| FUT.1 | 1>3 FUT | `-¨` | `-¨` | V5 | V | V | — | REM | §3.4; §8.2 (L2 p.55) |
| FUT.2 | 2>3 FUT | `-¨ta` | `-¨ku` | V5 | V | V | — | REM | §8.2 (L2 p.55) |
| FUT.3 | 3>3 FUT | `-ni` | `-phu` | V5 | V | V | — | REM | §3.4 (L2 p.189) |
| FUT.4 | 4>3 FUT | `-ñäni` | `-thäqi` | V5 | V | V | — | REM | §3.4 (L2 p.190) |

La columna **Después** de las personas sale de las marcas c/v de L1 (p.144–145), usadas como análisis (CH-702):
- `-tha`, `-tana` y `-tama` pierden la vocal (L1 c_c);
- las demás la conservan (L1 c_v, y v_v en el FUT).

Atestiguado en L2: `sarthwa`, `manq'tawa`, `manq'tanwa`, `jutaniti`, `lurañäniwa`. Lo no atestiguado lleva [DERIVADA] (Anexo A).

#### Oracionales

| Id | Función | B | A | Slot | Antes | Después | Se combina con | No se combina con | Guía |
|---|---|---|---|---|---|---|---|---|---|
| AFF | afirmativo | `-wa` | `-yi` | N7, V6 | — | (final) | ver CH-902 | objeto sin sufijo, ABL, LOC; preguntas | §4; §4.1 (L2 p.230) |
| TOP | tópico | `-xa` | `-xu` | N7 | — | (final) | sujeto o adverbio de tiempo (CH-903) | verbo | §4.1 (L2 p.231) |
| Q.YN | pregunta sí/no | `-ti` | `-ji` | N7, V6 | — | (final) | verbo o predicado (CH-904) | AFF en la oración | §4.1 (L2 p.235) |
| NEG.TI | `-ti` de la negación | `-ti` | `-ji` | V6 | — | (final) | verbo con NEG | AFF en el verbo | §3.3; §4.1 (L2 p.231) |
| Q.INF | pregunta de información | `-sa` | `-khu` | N7 | — | (final) | interrogativo (CH-906) | AFF en la oración | §4.1 (L2 p.236) |

### CH-505 · Palabras gramaticales

Base: §2 (pronombres, demostrativos; L1 p.182–183), D12 (plurales de L2), §6 (interrogativos), §3.3 (`jani`), CH-516, CH-519.

| Id | Función | B | A | Sílabas | Admite | Guía |
|---|---|---|---|---|---|---|
| PRON.1 | yo / nosotros (sin "tú") | `naya` | `muqi` | 2 | TOP, AFF, COMPL.RU, COM, BEN, CAUSE | §2; L2 p.33 |
| PRON.1.PL | nosotros (sin "tú"), plural | `nänaka` | `müsulu` | 3 | ídem | D12 (L2 p.181, 184); CH-517 |
| PRON.2 | tú | `juma` | `tilu` | 2 | ídem + PL | §2; L2 p.33 |
| PRON.3 | él / ella | `jupa` | `kaxi` | 2 | ídem + PL | §2; L2 p.33 |
| PRON.4 | tú y yo | `jiwasa` | `wiqutu` | 3 | ídem + PL | §2; D12 |
| NEG.PAL | no | `jani` | `yuli` | 2 | solo AFF | §3.3; §7.3 B |
| INT.QUIEN | quién | `khiti` | `simu` | 2 | Q.INF; COMPL.RU + Q.INF | §6; L2 p.231 (`khitisa`) |
| INT.QUE | qué | `kuna` | `mulu` | 2 | Q.INF | §6; L1 p.282 |
| INT.DONDE | dónde | `kawki` | `yaqu` | 2 | ALL + Q.INF; LOC + VBLZ.KA + persona + Q.INF | §6; L2 p.236 |
| DEM.1 | este / aquí | `aka` | `ilmi` | 2 | sin sufijo (modificador); LOC; TOP (sujeto de "ser"); LOC + VBLZ.KA | §2 (L1 p.183) |
| DEM.2 | ese / ahí | `uka` | `ulmi` | 2 | ídem | §2; L2 p.160 (`ukana`) |
| DEM.3 | aquel / más allá | `khuri` | `phiqa` | 2 | ídem | §2 (L1 p.183) |
| NUM.3 | tres | `kimsa` | `musqi` | 2 | solo modificador | §1 (L1 p.249) |
| NUM.4 | cuatro | `pusi` | `tayli` | 2 | ídem | §1 (L1 p.204) |
| NUM.6 | seis | `suxta` | `wichqa` | 2 | ídem | §8.3 (L2 p.42) |
| NUM.10 | diez | `tunka` | `qanti` | 2 | ídem | §1 (L1 p.208); §5.2.1 (`tunkakama`) |

Plurales de pronombres:
- `naya` → `nänaka` (A `müsulu`), forma propia.
- El resto, pronombre + PL: `jumanaka` / `tilusulu`, `jupanaka` / `kaxisulu`, `jiwasanaka` / `wiqutusulu`.

Ejemplo:
- B: `Juma-naka-xa tisqa-px-ta-wa.` → `Jumanakaxa tisqapxtawa.` — 2-PL-TOP ir-PL-2>3.SIMP-AFF — "Ustedes van."
- A: `Tilu-sulu-xu tisqa-mt-ku-yi.` → `Tilusuluxu tisqamtkuyi.`

### CH-511 · Segmentación de los remotos [DECISIÓN CHULUPI]

Base: §3.4 (paradigma de L2: `sarayätha`, `sarayäta`, `saräna`, `sarayätana`; `saratätha`, `saratäta`, `saratäna`, `saratätana`); L1 p.143 (las terminaciones del SIMP reaparecen en los tiempos compuestos); D5.

- REM.C = `-yä-` + P1 / P2 / P4. En 3.ª persona: `-¨-` + P3.REM `-na`.
- REM.L = `-tä-` + P1 / P2 / P4 / P3.REM.
- P3.REM (`-na`) solo aparece en los remotos.

Ejemplos:
- B: `tisqa-yä-tha` → `tisqayätha` — ir-REM.C-1 — "he ido (lo viví)"; `tisqa-¨-na` → `tisqäna` — ir-REM.C-3.
- A: `tisqa-jü-phi` → `tisqajüphi`; `tisqa-¨-mu` → `tisqämu`.

### CH-512 · REM.L con `-tä-` [DECISIÓN CHULUPI]

Base: §3.4 (L2 da `saratätha ~ sarataytha`, `saratäna ~ saratayna`); §13 #15 (`-taya` es variante no normativa).

Se usa `-tä-` en las cuatro personas. La serie queda uniforme y el mapeo A es más simple. `-tayna` no se genera.

Ejemplo:
- B: `tisqa-tä-na` → `tisqatäna` — ir-REM.L-3 — "había ido (no lo vi)".
- A: `tisqa-wü-mu` → `tisqawümu`.

### CH-513 · FUT 1.ª persona = `-¨` [DECISIÓN CHULUPI]

Base: §3.4 (`sarä ~ saraŋa`; `ŋ` no está en el alfabeto).

Ejemplo:
- B: `tisqa-¨` → `tisqä` — ir-1>3.FUT — "iré".
- A: `tisqä`.

### CH-514 · `-kama` restringido [DECISIÓN CHULUPI]

Base: §5.2.1 (con raíz de 2 sílabas, L1 y L2 coinciden en conservar la vocal: `utakama`, `markakama`); §13 #5 (no generar variantes de los dúctiles).

UNTIL solo va sobre una raíz nominal de 2 sílabas, sin PL ni POSS. La vocal se conserva siempre.

Ejemplos:
- B: `wirkha-kama` → `wirkhakama` — pueblo-UNTIL — "hasta el pueblo".
- A: `wirkhachiwi`.
- ✗ `pinqara-kama` (3 sílabas); ✗ `wirkha-ja-kama` (con POSS).

### CH-515 · `-layku` débil [DECISIÓN CHULUPI]

Base: §5.2 (L2 p.62–63 pone `-layku` entre los débiles); §2.1 (`jumalaykuwa`, L2 p.160–161). L1 elide tras raíz de 3 o más vocales (§5.2.1). Para la escritura manda L2 (D1).

La vocal anterior se conserva siempre, también tras raíz de 3 sílabas.

Ejemplo:
- B: `pultiya-layku` → `pultiyalayku` — hermano-CAUSE — "por el hermano".
- A: `pultiyatiwqa`.

### CH-516 · Demostrativos y numerales son palabras gramaticales [DECISIÓN CHULUPI]

Base: decisión del equipo (P3).

Son reales en B e inventados en A (CH-505). No están en `lexico.csv`.

Ejemplo:
- B: `kimsa kirpu` — tres perro — "tres perros"; `aka chimula` — este casa — "esta casa".
- A: `musqi kirpu`; `ilmi chimula`.

### CH-517 · `nänaka` [DECISIÓN CHULUPI]

Base: D12 (L2 da `nänaka`, p.181, 184); §5.2 (`wawanaka ~ wänaka`: dos formas, sin regla de elección).

- El plural de `naya` es siempre `nänaka` (palabra propia en CH-505).
- Ningún otro nombre se contrae: siempre forma completa con `-naka`.

Ejemplo:
- B: `Nänaka-xa tisqa-px-th-wa.` → `Nänakaxa tisqapxthwa.` — 1.PL-TOP ir-PL-1>3.SIMP-AFF — "Nosotros vamos."
- A: `Müsulu-xu tisqa-mt-ph-yi.` → `Müsuluxu tisqamtphyi.`

### CH-518 · Sin `maya`, `paya`, `khaya` [DECISIÓN CHULUPI]

Base: D8; §13 #6 (dos formas escritas válidas y ninguna regla de elección).

- No se generan "uno" ni "dos" como numerales, ni el demostrativo `khaya`.
- Para "aquel / allá" se usa `khuri` (CH-505).

Ejemplos:
- B: `pusi chimula` — cuatro casa — "cuatro casas". A: `tayli chimula`.
- ✗ Una idea con numeral 1 o 2 es inválida.

### CH-519 · Interrogativos de v1 [DECISIÓN CHULUPI]

Base: §6 (L1 p.185–187); §8.4 (`kawkha` pendiente). `qawqha` y `kamisa` quedan fuera de v1 (CH-906).

Solo se usan `khiti`, `kuna` y `kawki`.

Ejemplo:
- B: `¿Khiti-sa tisqa-ni?` → `¿Khitisa tisqani?` — quién-Q.INF ir-3>3.FUT — "¿Quién irá?"
- A: `¿Simukhu tisqaphu?`

### CH-520 · Formas de L1 sin divergencias [DECISIÓN CHULUPI]

Base: D1 (una forma de L1 no se convierte). Las que no tienen ningún rasgo que difiera entre L1 y L2 (ni `:`, ni `-ta`/`-tha`, ni elisión, ni apóstrofo) no necesitan conversión y se aceptan tal cual. Es el caso de `kuna`, `khuri`, `kimsa` y `pusi`.

Ejemplo:
- B: `Khuri-na nuyk'-th-wa.` → `Khurina nuyk'thwa.` — DEM.3-LOC dormir-1>3.SIMP-AFF — "Duermo más allá."
- A: `Phiqamu nuyk'phyi.`

### CH-521 · Sin nombres propios [DECISIÓN CHULUPI]

Base: §10.2 (`Juwanti Mamanïthwa` es hipotética); §8.3 (los préstamos se refonemizan, regla no modelada).

En v1 ninguna idea lleva nombres propios.

Ejemplo:
- ✗ "María va al pueblo": idea inválida.
- La versión válida usa un `N_HUM`: B `Simllaxa wirkharu tisqiwa.` — mujer-TOP pueblo-ALL ir-3>3.SIMP-AFF — "La mujer va al pueblo." A `Simllaxu wirkhallu tisquyi.`

### 5.1 `morfemas.yaml`

```yaml
# morfemas.yaml — version 1.1
# antes/despues: V = conserva, C = borra, "-" = no actúa (ver 5.0)
# derivada: true = la propiedad marcada no tiene forma atestiguada (Anexo A)
sufijos:
  # --- nombre ---
  - {id: PL,        glosa: PL,       b: naka,  a: sulu,  slot: N1, antes: V, despues: V, guia: "§2.1"}
  - {id: POSS.1,    glosa: POSS.1,   b: ja,    a: lu,    slot: N2, antes: V, despues: V, guia: "D4"}
  - {id: POSS.2,    glosa: POSS.2,   b: ma,    a: qi,    slot: N2, antes: V, despues: V, guia: "§2.1"}
  - {id: POSS.3,    glosa: POSS.3,   b: pa,    a: chu,   slot: N2, antes: V, despues: V, guia: "§2.1"}
  - {id: POSS.4,    glosa: POSS.4,   b: sa,    a: khu,   slot: N2, antes: V, despues: V, guia: "§2.1"}
  - {id: POSR,      glosa: POSR,     b: ni,    a: phu,   slot: N3, antes: V, despues: V, guia: "§2; §8.4"}
  - {id: GEN,       glosa: GEN,      b: na,    a: mu,    slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: LOC,       glosa: LOC,      b: na,    a: mu,    slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: ALL,       glosa: ALL,      b: ru,    a: llu,   slot: N4, antes: V, despues: V, guia: "D9"}
  - {id: COMPL.RU,  glosa: COMPL.RU, b: ru,    a: llu,   slot: N4, antes: V, despues: V, guia: "D9"}
  - {id: ABL,       glosa: ABL,      b: ta,    a: ku,    slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: COM,       glosa: COM,      b: mpi,   a: nku,   slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: BEN,       glosa: BEN,      b: taki,  a: puli,  slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: UNTIL,     glosa: UNTIL,    b: kama,  a: chiwi, slot: N4, antes: V, despues: V, guia: "§5.2.1", restriccion: "raiz_2_silabas_sin_sufijos"}
  - {id: CAUSE,     glosa: CAUSE,    b: layku, a: tiwqa, slot: N4, antes: V, despues: V, guia: "§2.1"}
  - {id: VBLZ.KA,   glosa: VBLZ.KA,  b: ka,    a: "ñu",  slot: N5, antes: C, despues: "-", guia: "§7.1", solo_tras: [LOC]}
  - {id: VBLZ.LONG, glosa: VBLZ.LONG, b: "¨",  a: "¨",   slot: N5, antes: V, despues: "-", guia: "§8.2", invisible_tras: [POSR]}
  # --- verbo ---
  - {id: PL.V,   glosa: PL,      b: pxa,  a: mtu,  slot: V1, antes: V, despues: "-", guia: "D11"}
  - {id: PROG,   glosa: PROG,    b: ska,  a: nchi, slot: V1, antes: V, despues: "-", guia: "D11"}
  - {id: NEG,    glosa: INCOMPL, b: ka,   a: "ñu", slot: V1, antes: C, despues: "-", guia: "D9; §3.3"}
  - {id: REM.C,  glosa: REM.C,   b: "yä", a: "jü", slot: V4, antes: V, despues: "-", guia: "§3.4",
     alomorfo: {ante: P3.REM, b: "¨", a: "¨"}}
  - {id: REM.L,  glosa: REM.L,   b: "tä", a: "wü", slot: V4, antes: V, despues: "-", guia: "§3.4"}
  - {id: P1,     glosa: "1",     b: tha,  a: phi,  slot: [V5, N6], antes: C, despues: C, guia: "D5"}
  - {id: P2,     glosa: "2",     b: ta,   a: ku,   slot: [V5, N6], antes: C, despues: V, guia: "§3.4"}
  - {id: P3,     glosa: "3>3",   b: i,    a: u,    slot: [V5, N6], antes: C, despues: V, guia: "§3.4"}
  - {id: P4,     glosa: "4",     b: tana, a: kilu, slot: [V5, N6], antes: C, despues: C, guia: "§3.4; §8.4"}
  - {id: P3.REM, glosa: "3",     b: na,   a: mu,   slot: V5, antes: "-", despues: V, guia: "§3.4", solo_tras: [REM.C, REM.L]}
  - {id: T12,    glosa: "1>2",   b: sma,  a: jmi,  slot: V5, antes: C, despues: V, guia: "§3.4"}
  - {id: T21,    glosa: "2>1",   b: ista, a: ulqa, slot: V5, antes: C, despues: V, guia: "§3.4"}
  - {id: T31,    glosa: "3>1",   b: itu,  a: uqu,  slot: V5, antes: C, despues: V, guia: "§3.4"}
  - {id: T32,    glosa: "3>2",   b: tama, a: kiqu, slot: V5, antes: C, despues: C, guia: "§3.4; L1 p.144", derivada: [despues]}
  - {id: T34,    glosa: "3>4",   b: istu, a: ulqu, slot: V5, antes: C, despues: V, guia: "§3.4"}
  - {id: FUT.1,  glosa: "1>3.FUT", b: "¨",    a: "¨",     slot: V5, antes: V, despues: V, guia: "§3.4"}
  - {id: FUT.2,  glosa: "2>3.FUT", b: "¨ta",  a: "¨ku",   slot: V5, antes: V, despues: V, guia: "§8.2"}
  - {id: FUT.3,  glosa: "3>3.FUT", b: ni,     a: phu,     slot: V5, antes: V, despues: V, guia: "§3.4"}
  - {id: FUT.4,  glosa: "4>3.FUT", b: "ñäni", a: "thäqi", slot: V5, antes: V, despues: V, guia: "§3.4"}
  # --- oracionales ---
  - {id: AFF,    glosa: AFF,   b: wa, a: yi,  slot: [N7, V6], antes: "-", guia: "§4"}
  - {id: TOP,    glosa: TOP,   b: xa, a: xu,  slot: N7,       antes: "-", guia: "§4.1"}
  - {id: Q.YN,   glosa: Q.YN,  b: ti, a: ji,  slot: [N7, V6], antes: "-", guia: "§4.1"}
  - {id: NEG.TI, glosa: NEG,   b: ti, a: ji,  slot: V6,       antes: "-", guia: "§3.3"}
  - {id: Q.INF,  glosa: Q.INF, b: sa, a: khu, slot: N7,       antes: "-", guia: "§4.1"}
palabras_gramaticales:
  - {id: PRON.1,    b: naya,    a: muqi,   persona: 1, admite: [TOP, AFF, COMPL.RU, COM, BEN, CAUSE]}
  - {id: PRON.1.PL, b: "nänaka", a: "müsulu", persona: 1, plural: true, admite: [TOP, AFF, COMPL.RU, COM, BEN, CAUSE]}
  - {id: PRON.2,    b: juma,    a: tilu,   persona: 2, admite: [PL, TOP, AFF, COMPL.RU, COM, BEN, CAUSE]}
  - {id: PRON.3,    b: jupa,    a: kaxi,   persona: 3, admite: [PL, TOP, AFF, COMPL.RU, COM, BEN, CAUSE]}
  - {id: PRON.4,    b: jiwasa,  a: wiqutu, persona: 4, admite: [PL, TOP, AFF, COMPL.RU, COM, BEN, CAUSE]}
  - {id: NEG.PAL,   b: jani,    a: yuli,   admite: [AFF]}
  - {id: INT.QUIEN, b: khiti,   a: simu,   admite: [Q.INF, "COMPL.RU+Q.INF"]}
  - {id: INT.QUE,   b: kuna,    a: mulu,   admite: [Q.INF]}
  - {id: INT.DONDE, b: kawki,   a: yaqu,   admite: ["ALL+Q.INF", "LOC+VBLZ.KA+PERS+Q.INF"]}
  - {id: DEM.1,     b: aka,     a: ilmi,   admite: ["", LOC, TOP, "LOC+VBLZ.KA+PERS"]}
  - {id: DEM.2,     b: uka,     a: ulmi,   admite: ["", LOC, TOP, "LOC+VBLZ.KA+PERS"]}
  - {id: DEM.3,     b: khuri,   a: phiqa,  admite: ["", LOC, TOP, "LOC+VBLZ.KA+PERS"]}
  - {id: NUM.3,     b: kimsa,   a: musqi,  valor: 3,  admite: [""]}
  - {id: NUM.4,     b: pusi,    a: tayli,  valor: 4,  admite: [""]}
  - {id: NUM.6,     b: suxta,   a: wichqa, valor: 6,  admite: [""]}
  - {id: NUM.10,    b: tunka,   a: qanti,  valor: 10, admite: [""]}
```

---

## 6. Orden de los slots

### CH-601 · Plantilla del nombre

Base: §2 (L1 p.196–197); §2.1 (L2: raíz – número – persona – caso, `uta-naka-ja-na`); §7.1–7.2 (verbalizadores).

| Slot | Contenido | Ids |
|---|---|---|
| N0 | Raíz nominal, adjetivo (solo para "ser"), pronombre, demostrativo o interrogativo | `RAIZ_N` |
| N1 | Plural | PL |
| N2 | Posesivo | POSS.1 – POSS.4 |
| N3 | Poseedor ("tener") | POSR |
| N4 | Caso (uno solo) | GEN, LOC, ALL, COMPL.RU, ABL, COM, BEN, UNTIL, CAUSE |
| N5 | Verbalizador | VBLZ.KA, VBLZ.LONG |
| N6 | Persona del predicado nominal | P1, P2, P3, P4 |
| N7 | Oracional (uno solo) | TOP, AFF, Q.YN, Q.INF |

Las palabras nominales tienen 4 formas posibles. En notación de ids, separados por espacio:

```
NP_NORMAL : ^RAIZ_N( PL)?( POSS\.[1-4])?( (GEN|LOC|ALL|COMPL\.RU|ABL|COM|BEN|UNTIL|CAUSE))?( (TOP|AFF|Q\.YN|Q\.INF))?$
ESTAR     : ^RAIZ_N( PL)?( POSS\.[1-4])? LOC VBLZ\.KA (P1|P2|P3|P4)( (AFF|Q\.YN|Q\.INF))?$
TENER     : ^RAIZ_N( PL)? POSR( VBLZ\.LONG (P1|P2|P4))?( (AFF|Q\.YN))?$
SER       : ^RAIZ_N VBLZ\.LONG (P1|P2|P4)( (AFF|Q\.YN))?$
```

Restricciones que la expresión regular no recoge:
- POSS y POSR no van juntos (L1 p.205); POSR no lleva caso.
- PL no va si la frase tiene numeral (§13 #11).
- UNTIL no lleva PL ni POSS (CH-514).
- GEN no lleva nada después; LOC solo VBLZ.KA (CH-901).
- ABL y LOC no llevan AFF (L1 p.280–281).
- "Tener" con P3 no lleva VBLZ.LONG ni persona: termina en POSR (+ oracional), como `utaniwa` (L2 p.49–52).
- "Ser" con 3.ª persona no lleva VBLZ.LONG: es `NP_NORMAL` + AFF (CH-908).
- Q.INF solo en interrogativos (CH-906).

Ejemplo (`NP_NORMAL`):
- B: `chimula-naka-ja-na` → `chimulanakajana` — casa-PL-POSS.1-LOC — "en mis casas" (orden de `utanakajana`, L2 p.162).
- A: `chimula-sulu-lu-mu` → `chimulasululumu`.

### CH-602 · Plantilla del verbo

Base: §3 (L1 p.97: derivativos – flexión – oracionales); §3.4 (L2).

| Slot | Contenido | Ids |
|---|---|---|
| V0 | Raíz verbal | `RAIZ_V` |
| V1 | Plural, progresivo o negación (como máximo uno; CH-603) | PL.V, PROG, NEG |
| V4 | Tiempo remoto | REM.C, REM.L |
| V5 | Persona / transición (fusionada con el tiempo en SIMP y FUT) | P1–P4, T12–T34, FUT.1–FUT.4, P3.REM |
| V6 | Oracional | AFF, Q.YN, NEG.TI |

(Los números V2 y V3 se reservan para derivativos de versiones futuras.)

```
VERBO : ^RAIZ_V( (PL\.V|PROG|NEG))?( (P1|P2|P3|P4|T12|T21|T31|T32|T34)| (FUT\.[1-4])| (REM\.C|REM\.L) (P1|P2|P3\.REM|P4))( (AFF|Q\.YN|NEG\.TI))?$
```

Restricciones adicionales:
- NEG ⇔ NEG.TI.
- NEG solo con SIMP o FUT (CH-605).
- PROG solo con SIMP y sin NEG (CH-606).
- T12–T34 solo en SIMP (CH-604) y con `obj_persona = s`.
- REM.C toma el alomorfo `-¨-` ante P3.REM (CH-511).

Ejemplo:
- B: `tisqa-pxa-yä-tha` → `tisqapxayätha` — ir-PL-REM.C-1 — "hemos ido (lo vivimos)" (patrón de `sarapxayätha`, L2 p.185).
- A: `tisqa-mtu-jü-phi` → `tisqamtujüphi`.

### CH-603 · PL.V, PROG y NEG se excluyen [DECISIÓN CHULUPI]

Base: D11; §12 #6 (orden de `-pxa` y `-ska` no documentado en L2); §12 #7 y §3.3 (con negación, L1 predice `sarapkiti` y el análisis de L2 daría `sarapxkiti`, sin atestiguar).

- El slot V1 tiene como máximo un morfema.
- Una negativa con sujeto plural marca el plural con `-naka` en el sujeto expreso (CH-913).

Ejemplos:
- ✗ `tisqa-pxa-ka-i-ti` (PL.V + NEG).
- ✓ B: `Jupa-naka-xa jani-wa tisq-k-i-ti.` → `Jupanakaxa janiwa tisqkiti.` — 3-PL-TOP NEG-AFF ir-INCOMPL-3>3.SIMP-NEG — "Ellos no van."
- ✓ A: `Kaxisuluxu yuliyi tisqñuji.`

### CH-604 · Transiciones solo en SIMP [DECISIÓN CHULUPI]

Base: decisión del equipo (P1); §3.4 (L2 solo da transiciones en SIMP); §13 #1 y #12 (no convertir las de L1).

T12, T21, T31, T32 y T34 solo van en SIMP. En FUT, REM.C y REM.L el objeto es siempre de 3.ª persona.

Ejemplos:
- ✓ B: `ch'ixr-itu-wa` → `ch'ixrituwa` — ver-3>1.SIMP-AFF — "me ve". A: `ch'ixruquyi`.
- ✗ "me verá" (3>1.FUT).

### CH-605 · Negación solo en SIMP y FUT [DECISIÓN CHULUPI]

Base: decisión del equipo (P5). L2 atestigua SIMP (`jiskht'kthti`, p.65) y FUT 3.ª (`jutkaniti`, p.231). Las otras personas del FUT son [DERIVADA] (Anexo A).

Ejemplos:
- ✓ B: `Jani-wa tisq-ka-¨-ti.` → `Janiwa tisqkäti.` — NEG-AFF ir-INCOMPL-1>3.FUT-NEG — "No iré." [DERIVADA]
- ✓ A: `Yuliyi tisqñüji.`
- ✗ NEG + REM.C o REM.L.

### CH-606 · Progresivo solo en SIMP afirmativo o pregunta [DECISIÓN CHULUPI]

Base: §3.4 (L2 p.202, `saraskaña`); §2.1 (`ukawjana ikiski`, L2 p.167). No hay datos de `-ska` con otros tiempos ni con negación.

Ejemplos:
- B: `Jupa-xa tisqa-sk-i-wa.` → `Jupaxa tisqaskiwa.` — 3-TOP ir-PROG-3>3.SIMP-AFF — "Él está yendo."
- A: `Kaxixu tisqanchuyi.`
- ✗ PROG + FUT; ✗ PROG + NEG.

```yaml
# slots.yaml
nombre:
  orden: [N0, N1, N2, N3, N4, N5, N6, N7]
  slots:
    N0: [RAIZ_N]
    N1: [PL]
    N2: [POSS.1, POSS.2, POSS.3, POSS.4]
    N3: [POSR]
    N4: [GEN, LOC, ALL, COMPL.RU, ABL, COM, BEN, UNTIL, CAUSE]
    N5: [VBLZ.KA, VBLZ.LONG]
    N6: [P1, P2, P3, P4]
    N7: [TOP, AFF, Q.YN, Q.INF]
  plantillas:
    NP_NORMAL: '^RAIZ_N( PL)?( POSS\.[1-4])?( (GEN|LOC|ALL|COMPL\.RU|ABL|COM|BEN|UNTIL|CAUSE))?( (TOP|AFF|Q\.YN|Q\.INF))?$'
    ESTAR:     '^RAIZ_N( PL)?( POSS\.[1-4])? LOC VBLZ\.KA (P1|P2|P3|P4)( (AFF|Q\.YN|Q\.INF))?$'
    TENER:     '^RAIZ_N( PL)? POSR( VBLZ\.LONG (P1|P2|P4))?( (AFF|Q\.YN))?$'
    SER:       '^RAIZ_N VBLZ\.LONG (P1|P2|P4)( (AFF|Q\.YN))?$'
  excluye:
    - [POSS, POSR]
    - [POSR, CASO]
    - [PL, NUMERAL_EN_FRASE]
    - [UNTIL, PL]
    - [UNTIL, POSS]
    - [ABL, AFF]
    - [LOC, AFF]
    - [LOC, Q.INF]
    - [GEN, CUALQUIERA_DESPUES]
verbo:
  orden: [V0, V1, V4, V5, V6]
  slots:
    V0: [RAIZ_V]
    V1: [PL.V, PROG, NEG]          # máximo uno (CH-603)
    V4: [REM.C, REM.L]
    V5:
      SIMP:  [P1, P2, P3, P4, T12, T21, T31, T32, T34]
      FUT:   [FUT.1, FUT.2, FUT.3, FUT.4]
      REM:   [P1, P2, P3.REM, P4]
    V6: [AFF, Q.YN, NEG.TI]
  plantilla: '^RAIZ_V( (PL\.V|PROG|NEG))?( (P1|P2|P3|P4|T12|T21|T31|T32|T34)| (FUT\.[1-4])| (REM\.C|REM\.L) (P1|P2|P3\.REM|P4))( (AFF|Q\.YN|NEG\.TI))?$'
  reglas:
    - "NEG <=> NEG.TI"                       # CH-602
    - "NEG => tiempo in [SIMP, FUT]"         # CH-605
    - "PROG => tiempo == SIMP"               # CH-606
    - "T* => tiempo == SIMP and verbo.obj_persona == s"   # CH-604
    - "REM.C antes de P3.REM => alomorfo ¨"  # CH-511
```

---


## 7. Morfofonología

Esta sección dice cómo se une una raíz (o una palabra gramatical) con sus sufijos. Solo trata la **elisión dentro de la palabra** (§5.3 de la guía, nivel a).

Entre palabras nunca se borra nada (CH-707): el objeto directo, los modificadores y cualquier palabra se escriben con su vocal final completa (D6; §13 #2–#4).

### CH-701 · Algoritmo

Base: §5.1 (L1 p.67–70: la influencia es regresiva y la decide cada sufijo); §5.2 (L2 p.60–66: sufijos fuertes y débiles); §5.3.

La palabra se construye **de izquierda a derecha**, un morfema cada vez. Para cada morfema, el orden de aplicación es:
1. Elegir la forma: modo B o A, y alomorfo si lo hay (CH-511).
2. Si la forma empieza por `¨`, alargar la vocal anterior (CH-704).
3. Si no, decidir si se borra la vocal corta final de lo que ya hay (CH-702, CH-703, CH-705).
4. Pegar la forma, sin reducir los grupos de consonantes (CH-706).

Al terminar, la última vocal de la palabra no se toca nunca (CH-203) y la palabra se valida (CH-709).

```
función construir_palabra(base, ids, modo):
    # base: raíz de lexico.csv o id de palabra gramatical (CH-505)
    forma0 = base.raiz si es raíz; si no: base.b (modo B) o base.a (modo A)
    g = segmentar(forma0)                    # CH-105, lista de grafemas
    despues_prev = "V"; id_prev = "RAIZ"; protegida = falso
    para k, id en enumerar(ids):
        m = MORFEMAS[id]
        f = m.b si modo == "B" si no m.a
        # 1. alomorfo
        si id == "REM.C" y ids[k+1] == "P3.REM": f = "¨"          # CH-511
        si id == "VBLZ.LONG" y id_prev == "POSR":                # CH-705
            protegida = verdadero; despues_prev = "V"; id_prev = id; continuar
        # 2. alargamiento
        si f empieza por "¨":                                    # CH-704
            si g[-1] en {a,i,u}: g[-1] = LARGA[g[-1]]            # a→ä, i→ï, u→ü
            resto = f[1:]
            si resto != "": g += segmentar(resto)
            protegida = falso; despues_prev = m.despues; id_prev = id; continuar
        # 3. borrado
        borrar = (m.antes == "C") o (m.antes == "-" y despues_prev == "C")   # CH-702
        si borrar y g[-1] en {a,i,u} y no protegida:             # CH-703: la larga nunca
            g = g[:-1]
        protegida = falso
        # 4. pegar
        g += segmentar(f)                                        # CH-706
        despues_prev = m.despues; id_prev = id
    palabra = unir(g)
    validar(palabra)                                             # CH-709
    devolver palabra
```

Ejemplo:
- B: `tisqa` + P1 + AFF → `tisqthwa` — ir-1>3.SIMP-AFF — "voy".
- A: `tisqphyi`.

El detalle paso a paso está en 7.1.

### CH-702 · Vocal propia ante oracionales [DECISIÓN CHULUPI]

Base: §3.1 (marcas c/v de L1 p.144–145, usadas como **análisis**, no como conversión de cadenas; D5, §13 #1); §5.1 (L1 p.68: `-wa` no impone nada).

- Un oracional (`antes = —`) no decide nada. Decide la columna `después` del morfema anterior (CH-504).
- Las personas que en L1 llevan la marca "consonante después" (c_c) pierden su vocal: P1 `-tha`, P4 `-tana`, T32 `-tama`.
- El resto la conserva.
- Lo que no está atestiguado en L2 lleva [DERIVADA]:

| DV | Regla derivada | Ejemplo B → A | Patrón en que se apoya |
|---|---|---|---|
| DV-01 | T32 `-tama` pierde su vocal ante oracional | `ch'ixrtamwa` → `ch'ixrkiqyi` | L1 `-tam` c_c (p.144); como `-tana` → `-tan` (`manq'tanwa`, L2 p.178) |
| DV-02 | T12, T21, T31 y T34 conservan su vocal ante oracional | `ch'ixrituwa` → `ch'ixruquyi` | L1 c_v (p.144) |
| DV-03 | Ante `-ti`: P2 y P3 conservan su vocal; P4 la pierde | `ch'ixrtati`, `ch'ixriti`, `ch'ixrtanti` | Igual que ante `-wa` (`manq'tawa`, `luriwa`, `manq'tanwa`); `-ti` va "donde iría `-wa`" (L1 p.299) |
| DV-04 | FUT.1 y FUT.2 ante oracional, y FUT.4 ante `-ti`: conservan | `tisqäwa`, `tisqätawa`, `tisqañäniti` | L1 FUT v_v (p.145); como `jutaniti` y `lurañäniwa` |
| DV-05 | Remotos ante oracional: P1 y P4 pierden la vocal; P2 y P3.REM la conservan | `tisqayäthwa`, `tisqatätanwa`, `tisqänawa` | Misma persona que en SIMP (L1 p.143) |
| DV-06 | PL.V conserva su vocal ante FUT.3, FUT.4 y REM.L, y se alarga con FUT.1 | `tisqapxani`, `tisqapxatätha`, `tisqapxä` | Como `sarapxayätha` y `sarapxäta` |
| DV-07 | PL.V pierde su vocal ante las transiciones | `ch'ixrapxitu` | Las transiciones son fuertes como P1 (`sarapxtha`); L1 `parla-p-x-itu` (p.112) |
| DV-08 | NEG con personas distintas de P1 y FUT.3 | `tisqkiti`, `tisqkäti` | `jiskht'kthti`, `jutkaniti`; L1 `sar-k-i-ti` (p.111) |
| DV-09 | PROG con personas distintas de P3 | `tisqaskthwa` | `saraski`; L1 `aka-n-ka-s-k-t-wa` (p.162) |
| DV-10 | ESTAR con P2, P3 y P4 | `chimulanktawa`, `chimulankiwa` | `utankthwa`; L1 `misa taypi-n-k-i-w` (p.237) |
| DV-11 | TENER con P2 y P4 | `chimulanitawa` | `utanithwa` |
| DV-12 | SER con P2 y P4 | `jumpütawa` | `jach'äthwa` |
| DV-13 | Q.YN en predicados de ser, estar y tener | `chimulankthti` | Regla de `-ti` de DV-03 |

Ejemplo (DV-01):
- B: `ch'ixr-tam-wa` → `ch'ixrtamwa` — ver-3>2.SIMP-AFF — "te ve".
- A: `ch'ixr-kiq-yi` → `ch'ixrkiqyi`.

### CH-703 · La vocal larga nunca se borra

Base: §5.1 (L1 p.71: "una vocal larga final nunca se suprime"). Atestiguado: `sarayätha` (L2 p.185), `jach'äthwa` (L2 p.51).

Ejemplo:
- B: `tisqa-yä-tha` → `tisqayätha` (P1 pide borrar, pero `ä` es larga).
- A: `tisqajüphi`.

### CH-704 · Alargamiento

Base: §8.2 (L2: `-¨`, `churä`, `saräna`, `jaqïña`); D2.

- `¨` convierte la vocal corta anterior en larga: `a`→`ä`, `i`→`ï`, `u`→`ü`.
- Si la vocal ya es larga, no cambia.
- Si a `¨` le sigue una parte segmental (`¨ta`), esa parte se pega después.

Ejemplo:
- B: `tisqa-¨ta` → `tisqäta` — ir-2>3.FUT — "irás" (como `saräta`, L2 p.187).
- A: `tisqa-¨ku` → `tisqäku`.

### CH-705 · VBLZ.LONG tras POSR [DECISIÓN CHULUPI]

Base: §8.4 (L2 escribe `utanithwa` y `masinakanithwa` sin diéresis, p.47, 57); §5.1 (L1 p.71: la vocal ante un sufijo "pide consonante" revela un alargamiento oculto). Elegimos este análisis porque reproduce la forma atestiguada con el mismo morfema de "ser".

- Tras POSR, VBLZ.LONG no se escribe, pero **protege** la vocal anterior: el sufijo siguiente no la borra.
- En 3.ª persona, "tener" no lleva VBLZ.LONG (CH-601).

Ejemplo:
- B: `chimula-ni-(¨)-tha-wa` → `chimulanithwa` — casa-POSR-VBLZ.LONG-1-AFF — "tengo una casa".
- A: `chimula-phu-(¨)-phi-yi` → `chimulaphuphyi`.

### CH-706 · Los grupos se escriben enteros [DECISIÓN CHULUPI]

Base: §5.2 (L2 p.64–65: "se escribe el grupo", `jutthwa`, `jiskht'kthti`). No se aplica la reducción de geminadas de L1 (p.68).

- Las consonantes que quedan juntas tras la elisión se escriben todas.
- Dos consonantes iguales seguidas también: `jutthwa`.

Ejemplo:
- B: `tisqa-ka-tha-ti` → `tisqkthti` — ir-INCOMPL-1>3.SIMP-NEG.
- A: `tisqñphji` (4 consonantes seguidas).

### CH-707 · Nada se borra entre palabras

Base: D6 (b); §5.3 b1–b3; §13 #2–#4.

- Cada palabra se construye por separado.
- El objeto directo, los adjetivos, los demostrativos y los numerales conservan su vocal final.

Ejemplo:
- B: `Nayaxa q'aspi lamch'thwa.` (no `*q'asp`) — "Yo como pan."
- A: `Muqixu q'aspi lamch'phyi.`

### CH-708 · Palabras gramaticales en el modo A

- En el modo A, una palabra gramatical se reemplaza por su forma A de CH-505 **antes** de añadir sufijos.
- Los sufijos se añaden con el mismo algoritmo.
- Excepción: el plural de `naya` es su propia palabra (`nänaka` / `müsulu`, CH-517).

Ejemplo:
- B: `jiwasa-naka-xa` → `jiwasanakaxa` — 4-PL-TOP.
- A: `wiqutu-sulu-xu` → `wiqutusuluxu`.

### CH-709 · Validación de cada palabra

Toda palabra construida debe pasar CH-101 a CH-105 y CH-202 a CH-208. Si una no pasa, es un error del programa: no se descarta en silencio, se registra con la raíz y los ids.

Ejemplo:
- B `tisqkthti` → clases `CVCCCCCV` ✓.
- A `tisqñphji` → `CVCCCCCV` ✓.

### CH-710 · Pruebas de regresión con raíces reales

Base: decisión del equipo (v1.1). Es la prueba de que las reglas de §5 a §7 reproducen L2.

1. **Prueba de igualdad (modo B).** El motor de CH-701, en modo B, recibe raíces **reales** del aymara y listas de ids. Debe producir **exactamente** la forma atestiguada en la guía. Si un solo caso falla, alguna regla está mal y el generador no se usa hasta corregirla. La lista tiene 102 casos: las formas pedidas por el equipo y todas las de la tabla 10.1 (y de §2.1, §3.4, §4.1, §8.2) que caen en el alcance v1.
2. **Prueba de paralelismo (modo A).** Para cada caso, el motor corre también en modo A. En cada paso, la decisión (borrar, conservar, alargar o proteger) debe ser la misma que en B. El motor registra esa secuencia de decisiones y la compara.
3. **Cuándo se ejecuta.** Antes de cada generación y en cada cambio de `morfemas.yaml`.

Quedan **fuera** de la lista, por estar fuera de v1:
- `sarañajawa` (INF, #8);
- `alani` (glosa pendiente, #11);
- `wakwa` (`-wa` sobre objeto sin sufijo, fuera de CH-902, #13);
- `jiskht'kthti` (MOM `-t'a-`, #14);
- `jutipana` (SUB, #17);
- `ch'uqisa` (`-sa` CAT, #18);
- `pä/paya` (CH-518, #9);
- `thuqhuwa` (raíz en `-u`: la `-i` de 3.ª desaparece, regla excluida por CH-304).

Las frases de la tabla 10.1 que sí entran se prueban palabra por palabra. Por ejemplo, #1 = `nayaxa` + `wawaru` + `t'ant'a` + `churtha`.

Ejemplo:
- Entrada `{raiz: "sara", ids: [PL.V, REM.C, P1]}` → esperado `sarapxayätha` (L2 p.181).
- Salida del prototipo: `sarapxayätha` ✓.
- Modo A del mismo caso: `saramtujüphi`, con la secuencia de decisiones [conservar, conservar, larga-no-borra], igual a la de B.

El prototipo de referencia pasa los 102 casos.

```yaml
# regresion_raices_reales.yaml — CH-710 (modo B). Cada caso: raíz real, ids, forma esperada, fuente.
casos:
  - {raiz: "sara", ids: [P1, AFF], esperado: "sarthwa", fuente: "L2 p.176"}
  - {raiz: "manq'a", ids: [P2, AFF], esperado: "manq'tawa", fuente: "L2 p.177"}
  - {raiz: "manq'a", ids: [P4, AFF], esperado: "manq'tanwa", fuente: "L2 p.178"}
  - {raiz: "lura", ids: [P3, AFF], esperado: "luriwa", fuente: "L2 p.61"}
  - {raiz: "lura", ids: [P1, AFF], esperado: "lurthwa", fuente: "L2 p.61"}
  - {raiz: "lura", ids: [P2, AFF], esperado: "lurtawa", fuente: "L2 p.61"}
  - {raiz: "juta", ids: [P1, AFF], esperado: "jutthwa", fuente: "L2 p.64"}
  - {raiz: "manq'a", ids: [P1, AFF], esperado: "manq'thwa", fuente: "L2 p.64"}
  - {raiz: "muna", ids: [P1], esperado: "muntha", fuente: "L2 p.61, 67"}
  - {raiz: "apa", ids: [P2], esperado: "apta", fuente: "L2 p.61"}
  - {raiz: "sara", ids: [P1], esperado: "sartha", fuente: "L2 p.184"}
  - {raiz: "sara", ids: [P2], esperado: "sarta", fuente: "L2 p.184"}
  - {raiz: "sara", ids: [P3], esperado: "sari", fuente: "L2 p.184"}
  - {raiz: "sara", ids: [P4], esperado: "sartana", fuente: "L2 p.184"}
  - {raiz: "chura", ids: [P1], esperado: "churtha", fuente: "L2 p.155"}
  - {raiz: "chura", ids: [P3], esperado: "churi", fuente: "L2 p.155"}
  - {raiz: "manq'a", ids: [P3], esperado: "manq'i", fuente: "L2 p.243"}
  - {raiz: "awata", ids: [P3], esperado: "awati", fuente: "L2 p.68"}
  - {raiz: "irnaqa", ids: [P1], esperado: "irnaqtha", fuente: "L2 p.160–161"}
  - {raiz: "chura", ids: [T12], esperado: "chursma", fuente: "L2 p.179"}
  - {raiz: "chura", ids: [T21], esperado: "churista", fuente: "L2 p.179"}
  - {raiz: "chura", ids: [T31], esperado: "churitu", fuente: "L2 p.180"}
  - {raiz: "chura", ids: [T32], esperado: "churtama", fuente: "L2 p.180"}
  - {raiz: "chura", ids: [T34], esperado: "churistu", fuente: "L2 p.180"}
  - {raiz: "sara", ids: [FUT.1], esperado: "sarä", fuente: "L2 p.55, 187"}
  - {raiz: "sara", ids: [FUT.2], esperado: "saräta", fuente: "L2 p.187"}
  - {raiz: "sara", ids: [FUT.3], esperado: "sarani", fuente: "L2 p.189"}
  - {raiz: "sara", ids: [FUT.4], esperado: "sarañäni", fuente: "L2 p.190"}
  - {raiz: "chura", ids: [FUT.1], esperado: "churä", fuente: "L2 p.55"}
  - {raiz: "chura", ids: [FUT.2], esperado: "churäta", fuente: "L2 p.55"}
  - {raiz: "chura", ids: [FUT.3], esperado: "churani", fuente: "L2 p.55"}
  - {raiz: "chura", ids: [FUT.4], esperado: "churañäni", fuente: "L2 p.55"}
  - {raiz: "juta", ids: [FUT.3], esperado: "jutani", fuente: "L2 p.156"}
  - {raiz: "juta", ids: [FUT.3, Q.YN], esperado: "jutaniti", fuente: "L2 p.235"}
  - {raiz: "achu", ids: [FUT.3, AFF], esperado: "achuniwa", fuente: "L2 p.234"}
  - {raiz: "lura", ids: [FUT.4, AFF], esperado: "lurañäniwa", fuente: "L2 p.61"}
  - {raiz: "thuqhu", ids: [FUT.4], esperado: "thuqhuñäni", fuente: "L2 p.200"}
  - {raiz: "sara", ids: [REM.C, P1], esperado: "sarayätha", fuente: "L2 p.185"}
  - {raiz: "sara", ids: [REM.C, P2], esperado: "sarayäta", fuente: "L2 p.185"}
  - {raiz: "sara", ids: [REM.C, P3.REM], esperado: "saräna", fuente: "L2 p.185"}
  - {raiz: "sara", ids: [REM.C, P4], esperado: "sarayätana", fuente: "L2 p.185"}
  - {raiz: "muna", ids: [REM.C, P1], esperado: "munayätha", fuente: "L2 p.56"}
  - {raiz: "muna", ids: [REM.C, P3.REM], esperado: "munäna", fuente: "L2 p.56"}
  - {raiz: "sara", ids: [REM.L, P1], esperado: "saratätha", fuente: "L2 p.186"}
  - {raiz: "sara", ids: [REM.L, P2], esperado: "saratäta", fuente: "L2 p.186"}
  - {raiz: "sara", ids: [REM.L, P3.REM], esperado: "saratäna", fuente: "L2 p.186"}
  - {raiz: "sara", ids: [REM.L, P4], esperado: "saratätana", fuente: "L2 p.186"}
  - {raiz: "muna", ids: [REM.L, P1], esperado: "munatätha", fuente: "L2 p.56"}
  - {raiz: "muna", ids: [REM.L, P3.REM], esperado: "munatäna", fuente: "L2 p.56"}
  - {raiz: "sara", ids: [PL.V, P1], esperado: "sarapxtha", fuente: "L2 p.181"}
  - {raiz: "sara", ids: [PL.V, P3], esperado: "sarapxi", fuente: "L2 p.181, 184"}
  - {raiz: "jikisi", ids: [PL.V, P3], esperado: "jikisipxi", fuente: "L2 p.160"}
  - {raiz: "sara", ids: [PL.V, FUT.2], esperado: "sarapxäta", fuente: "L2 p.181"}
  - {raiz: "sara", ids: [PL.V, REM.C, P1], esperado: "sarapxayätha", fuente: "L2 p.181"}
  - {raiz: "sara", ids: [PL.V, REM.C, P3.REM], esperado: "sarapxäna", fuente: "L2 p.185"}
  - {raiz: "sara", ids: [PROG, P3], esperado: "saraski", fuente: "L2 p.202 (patrón de saraskaña)"}
  - {raiz: "iki", ids: [PROG, P3], esperado: "ikiski", fuente: "L2 p.167"}
  - {raiz: "juta", ids: [NEG, FUT.3, NEG.TI], esperado: "jutkaniti", fuente: "L2 p.231"}
  - {raiz: "uta", ids: [LOC, VBLZ.KA, P1, AFF], esperado: "utankthwa", fuente: "L2 p.50"}
  - {raiz: "uta", ids: [POSR, VBLZ.LONG, P1, AFF], esperado: "utanithwa", fuente: "L2 p.57"}
  - {raiz: "masi", ids: [PL, POSR, VBLZ.LONG, P1, AFF], esperado: "masinakanithwa", fuente: "L2 p.47"}
  - {raiz: "uta", ids: [POSR, AFF], esperado: "utaniwa", fuente: "L2 p.49–52"}
  - {raiz: "jach'a", ids: [VBLZ.LONG, P1, AFF], esperado: "jach'äthwa", fuente: "L2 p.51"}
  - {raiz: "uta", ids: [POSS.1], esperado: "utaja", fuente: "L2 p.149"}
  - {raiz: "phisi", ids: [POSS.2], esperado: "phisima", fuente: "L2 p.148"}
  - {raiz: "anu", ids: [POSS.3], esperado: "anupa", fuente: "L2 p.148"}
  - {raiz: "phuchha", ids: [POSS.4], esperado: "phuchhasa", fuente: "L2 p.148"}
  - {raiz: "anu", ids: [PL], esperado: "anunaka", fuente: "L2 p.152"}
  - {raiz: "uta", ids: [PL, POSS.1, LOC], esperado: "utanakajana", fuente: "L2 p.162"}
  - {raiz: "tata", ids: [POSS.1, GEN], esperado: "tatajana", fuente: "L2 p.154"}
  - {raiz: "uta", ids: [POSS.3], esperado: "utapa", fuente: "L2 p.154"}
  - {raiz: "wawa", ids: [COMPL.RU], esperado: "wawaru", fuente: "L2 p.155"}
  - {raiz: "tata", ids: [POSS.2, COMPL.RU], esperado: "tatamaru", fuente: "L2 p.155"}
  - {raiz: "marka", ids: [ALL], esperado: "markaru", fuente: "L2 p.156"}
  - {raiz: "uta", ids: [ALL, AFF], esperado: "utaruwa", fuente: "L2 p.68"}
  - {raiz: "marka", ids: [ABL], esperado: "markata", fuente: "L2 p.255"}
  - {raiz: "marka", ids: [POSS.1, ABL], esperado: "markajata", fuente: "L2 p.158"}
  - {raiz: "qala", ids: [ABL, AFF], esperado: "qalatawa", fuente: "L2 p.158–159"}
  - {raiz: "pampa", ids: [LOC], esperado: "pampana", fuente: "L2 p.158"}
  - {raiz: "uka", ids: [LOC], esperado: "ukana", fuente: "L2 p.160"}
  - {raiz: "wawa", ids: [POSS.3, BEN], esperado: "wawapataki", fuente: "L2 p.255"}
  - {raiz: "jila", ids: [POSS.1, BEN, AFF], esperado: "jilajatakiwa", fuente: "L2 p.158"}
  - {raiz: "tiwula", ids: [COM], esperado: "tiwulampi", fuente: "L2 p.160"}
  - {raiz: "wallata", ids: [COM, AFF], esperado: "wallatampiwa", fuente: "L2 p.160"}
  - {raiz: "marka", ids: [UNTIL, AFF], esperado: "markakamawa", fuente: "L2 p.160"}
  - {raiz: "uta", ids: [UNTIL], esperado: "utakama", fuente: "L2 p.62"}
  - {raiz: "qullu", ids: [UNTIL], esperado: "qullukama", fuente: "L2 p.62"}
  - {raiz: "juma", ids: [CAUSE, AFF], esperado: "jumalaykuwa", fuente: "L2 p.160"}
  - {raiz: "kawki", ids: [ALL, Q.INF], esperado: "kawkirusa", fuente: "L2 p.236"}
  - {raiz: "khiti", ids: [Q.INF], esperado: "khitisa", fuente: "L2 p.231"}
  - {raiz: "naya", ids: [TOP], esperado: "nayaxa", fuente: "L2 p.155"}
  - {raiz: "juma", ids: [TOP], esperado: "jumaxa", fuente: "L2 p.177"}
  - {raiz: "jiwasa", ids: [TOP], esperado: "jiwasaxa", fuente: "L2 p.178"}
  - {raiz: "jupa", ids: [PL, TOP], esperado: "jupanakaxa", fuente: "L2 p.184"}
  - {raiz: "jani", ids: [AFF], esperado: "janiwa", fuente: "L2 p.231"}
  - {raiz: "anu", ids: [TOP], esperado: "anuxa", fuente: "L2 p.243"}
  - {raiz: "tata", ids: [TOP], esperado: "tataxa", fuente: "L2 p.68"}
  - {raiz: "awicha", ids: [TOP], esperado: "awichaxa", fuente: "L2 p.68"}
  - {raiz: "jilaqata", ids: [TOP], esperado: "jilaqataxa", fuente: "L2 p.231"}
  - {raiz: "jila", ids: [POSS.2, TOP], esperado: "jilamaxa", fuente: "L2 p.235"}
  - {raiz: "mama", ids: [POSS.1, AFF], esperado: "mamajawa", fuente: "L2 p.230"}
  - {raiz: "mara", ids: [TOP], esperado: "maraxa", fuente: "L2 p.234"}
```

### 7.1 Ejemplos paso a paso

Cada ejemplo muestra la forma subyacente (raíz + formas de los morfemas) y cada paso del algoritmo CH-701, en los dos modos.
- "Antes —; decide X (después C)" quiere decir que el oracional no decide y manda la columna `después` del morfema X.
- Cubren lo pedido por el equipo: transiciones (7.4 y 7.5), NEG + FUT (7.6 y 7.8), PL.V + REM.C (7.9 y 7.10), ESTAR (7.13) y TENER (7.14).

**Ejemplo 7.1 · Persona 1 del SIMP + AFF**

- Entrada: `tisqa` + `P1 AFF` — ir-1>3.SIMP-AFF — "voy". Estado: patrón atestiguado (`sarthwa`, L2 p.176).
- Subyacente B: `tisqa` + `tha` + `wa`
- Subyacente A: `tisqa` + `phi` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + P1 `tha` (antes C): borra `a` → `tisqtha` | + P1 `phi` (antes C): borra `a` → `tisqphi` |
| 2 | + AFF `wa` (antes —; decide P1 (después C)): borra `a` → `tisqthwa` | + AFF `yi` (antes —; decide P1 (después C)): borra `i` → `tisqphyi` |
| **Salida** | **`tisqthwa`** | **`tisqphyi`** |

**Ejemplo 7.2 · Persona 2 del SIMP + AFF**

- Entrada: `tisqa` + `P2 AFF` — ir-2>3.SIMP-AFF — "vas". Estado: patrón atestiguado (`manq'tawa`, L2 p.177).
- Subyacente B: `tisqa` + `ta` + `wa`
- Subyacente A: `tisqa` + `ku` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + P2 `ta` (antes C): borra `a` → `tisqta` | + P2 `ku` (antes C): borra `a` → `tisqku` |
| 2 | + AFF `wa` (antes —; decide P2 (después V)): conserva la vocal → `tisqtawa` | + AFF `yi` (antes —; decide P2 (después V)): conserva la vocal → `tisqkuyi` |
| **Salida** | **`tisqtawa`** | **`tisqkuyi`** |

**Ejemplo 7.3 · Persona 4 del SIMP + AFF**

- Entrada: `tisqa` + `P4 AFF` — ir-4>3.SIMP-AFF — "vamos". Estado: patrón atestiguado (`manq'tanwa`, L2 p.178).
- Subyacente B: `tisqa` + `tana` + `wa`
- Subyacente A: `tisqa` + `kilu` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + P4 `tana` (antes C): borra `a` → `tisqtana` | + P4 `kilu` (antes C): borra `a` → `tisqkilu` |
| 2 | + AFF `wa` (antes —; decide P4 (después C)): borra `a` → `tisqtanwa` | + AFF `yi` (antes —; decide P4 (después C)): borra `u` → `tisqkilyi` |
| **Salida** | **`tisqtanwa`** | **`tisqkilyi`** |

**Ejemplo 7.4 · Transición 3>1 + AFF**

- Entrada: `ch'ixra` + `T31 AFF` — ver-3>1.SIMP-AFF — "me ve". Estado: [DERIVADA] DV-02.
- Subyacente B: `ch'ixra` + `itu` + `wa`
- Subyacente A: `ch'ixra` + `uqu` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `ch'ixra` | raíz `ch'ixra` |
| 1 | + T31 `itu` (antes C): borra `a` → `ch'ixritu` | + T31 `uqu` (antes C): borra `a` → `ch'ixruqu` |
| 2 | + AFF `wa` (antes —; decide T31 (después V)): conserva la vocal → `ch'ixrituwa` | + AFF `yi` (antes —; decide T31 (después V)): conserva la vocal → `ch'ixruquyi` |
| **Salida** | **`ch'ixrituwa`** | **`ch'ixruquyi`** |

**Ejemplo 7.5 · Transición 3>2 + AFF**

- Entrada: `ch'ixra` + `T32 AFF` — ver-3>2.SIMP-AFF — "te ve". Estado: [DERIVADA] DV-01.
- Subyacente B: `ch'ixra` + `tama` + `wa`
- Subyacente A: `ch'ixra` + `kiqu` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `ch'ixra` | raíz `ch'ixra` |
| 1 | + T32 `tama` (antes C): borra `a` → `ch'ixrtama` | + T32 `kiqu` (antes C): borra `a` → `ch'ixrkiqu` |
| 2 | + AFF `wa` (antes —; decide T32 (después C)): borra `a` → `ch'ixrtamwa` | + AFF `yi` (antes —; decide T32 (después C)): borra `u` → `ch'ixrkiqyi` |
| **Salida** | **`ch'ixrtamwa`** | **`ch'ixrkiqyi`** |

**Ejemplo 7.6 · NEG + FUT (1.ª persona)**

- Entrada: `tisqa` + `NEG FUT.1 NEG.TI` — ir-INCOMPL-1>3.FUT-NEG — "(no) iré". Estado: [DERIVADA] DV-04, DV-08.
- Subyacente B: `tisqa` + `ka` + `¨` + `ti`
- Subyacente A: `tisqa` + `ñu` + `¨` + `ji`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + NEG `ka` (antes C): borra `a` → `tisqka` | + NEG `ñu` (antes C): borra `a` → `tisqñu` |
| 2 | + FUT.1 `¨`: alarga `a` → `ä` → `tisqkä` | + FUT.1 `¨`: alarga `u` → `ü` → `tisqñü` |
| 3 | + NEG.TI `ti` (antes —; decide FUT.1 (después V)): conserva la vocal → `tisqkäti` | + NEG.TI `ji` (antes —; decide FUT.1 (después V)): conserva la vocal → `tisqñüji` |
| **Salida** | **`tisqkäti`** | **`tisqñüji`** |

**Ejemplo 7.7 · NEG + SIMP (1.ª persona)**

- Entrada: `tisqa` + `NEG P1 NEG.TI` — ir-INCOMPL-1>3.SIMP-NEG — "(no) voy". Estado: patrón atestiguado (`jiskht'kthti`, L2 p.65).
- Subyacente B: `tisqa` + `ka` + `tha` + `ti`
- Subyacente A: `tisqa` + `ñu` + `phi` + `ji`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + NEG `ka` (antes C): borra `a` → `tisqka` | + NEG `ñu` (antes C): borra `a` → `tisqñu` |
| 2 | + P1 `tha` (antes C): borra `a` → `tisqktha` | + P1 `phi` (antes C): borra `u` → `tisqñphi` |
| 3 | + NEG.TI `ti` (antes —; decide P1 (después C)): borra `a` → `tisqkthti` | + NEG.TI `ji` (antes —; decide P1 (después C)): borra `i` → `tisqñphji` |
| **Salida** | **`tisqkthti`** | **`tisqñphji`** |

**Ejemplo 7.8 · NEG + FUT (3.ª persona)**

- Entrada: `tisqa` + `NEG FUT.3 NEG.TI` — ir-INCOMPL-3>3.FUT-NEG — "(no) irá". Estado: patrón atestiguado (`jutkaniti`, L2 p.231).
- Subyacente B: `tisqa` + `ka` + `ni` + `ti`
- Subyacente A: `tisqa` + `ñu` + `phu` + `ji`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + NEG `ka` (antes C): borra `a` → `tisqka` | + NEG `ñu` (antes C): borra `a` → `tisqñu` |
| 2 | + FUT.3 `ni` (antes V): conserva la vocal → `tisqkani` | + FUT.3 `phu` (antes V): conserva la vocal → `tisqñuphu` |
| 3 | + NEG.TI `ti` (antes —; decide FUT.3 (después V)): conserva la vocal → `tisqkaniti` | + NEG.TI `ji` (antes —; decide FUT.3 (después V)): conserva la vocal → `tisqñuphuji` |
| **Salida** | **`tisqkaniti`** | **`tisqñuphuji`** |

**Ejemplo 7.9 · PL.V + REM.C (1.ª persona)**

- Entrada: `tisqa` + `PL.V REM.C P1` — ir-PL-REM.C-1 — "hemos ido (lo vivimos)". Estado: patrón atestiguado (`sarapxayätha`, L2 p.181).
- Subyacente B: `tisqa` + `pxa` + `yä` + `tha`
- Subyacente A: `tisqa` + `mtu` + `jü` + `phi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + PL.V `pxa` (antes V): conserva la vocal → `tisqapxa` | + PL.V `mtu` (antes V): conserva la vocal → `tisqamtu` |
| 2 | + REM.C `yä` (antes V): conserva la vocal → `tisqapxayä` | + REM.C `jü` (antes V): conserva la vocal → `tisqamtujü` |
| 3 | + P1 `tha` (antes C): no hay vocal que borrar → `tisqapxayätha` | + P1 `phi` (antes C): no hay vocal que borrar → `tisqamtujüphi` |
| **Salida** | **`tisqapxayätha`** | **`tisqamtujüphi`** |

**Ejemplo 7.10 · PL.V + REM.C (3.ª persona)**

- Entrada: `tisqa` + `PL.V REM.C P3.REM` — ir-PL-REM.C-3 — "han ido (lo vi)". Estado: patrón atestiguado (`sarapxäna`, L2 p.185).
- Subyacente B: `tisqa` + `pxa` + `yä` + `na`
- Subyacente A: `tisqa` + `mtu` + `jü` + `mu`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + PL.V `pxa` (antes V): conserva la vocal → `tisqapxa` | + PL.V `mtu` (antes V): conserva la vocal → `tisqamtu` |
| 2 | + REM.C `¨` (alomorfo ante P3.REM): alarga `a` → `ä` → `tisqapxä` | + REM.C `¨` (alomorfo ante P3.REM): alarga `u` → `ü` → `tisqamtü` |
| 3 | + P3.REM `na` (antes —; decide REM.C (después -)): conserva la vocal → `tisqapxäna` | + P3.REM `mu` (antes —; decide REM.C (después -)): conserva la vocal → `tisqamtümu` |
| **Salida** | **`tisqapxäna`** | **`tisqamtümu`** |

**Ejemplo 7.11 · REM.L (4.ª persona) + AFF**

- Entrada: `tisqa` + `REM.L P4 AFF` — ir-REM.L-4-AFF — "habíamos ido (no lo vimos)". Estado: [DERIVADA] DV-05.
- Subyacente B: `tisqa` + `tä` + `tana` + `wa`
- Subyacente A: `tisqa` + `wü` + `kilu` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + REM.L `tä` (antes V): conserva la vocal → `tisqatä` | + REM.L `wü` (antes V): conserva la vocal → `tisqawü` |
| 2 | + P4 `tana` (antes C): no hay vocal que borrar → `tisqatätana` | + P4 `kilu` (antes C): no hay vocal que borrar → `tisqawükilu` |
| 3 | + AFF `wa` (antes —; decide P4 (después C)): borra `a` → `tisqatätanwa` | + AFF `yi` (antes —; decide P4 (después C)): borra `u` → `tisqawükilyi` |
| **Salida** | **`tisqatätanwa`** | **`tisqawükilyi`** |

**Ejemplo 7.12 · PROG + AFF**

- Entrada: `tisqa` + `PROG P3 AFF` — ir-PROG-3>3.SIMP-AFF — "está yendo". Estado: patrón atestiguado (`saraski`, L2 p.202).
- Subyacente B: `tisqa` + `ska` + `i` + `wa`
- Subyacente A: `tisqa` + `nchi` + `u` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `tisqa` | raíz `tisqa` |
| 1 | + PROG `ska` (antes V): conserva la vocal → `tisqaska` | + PROG `nchi` (antes V): conserva la vocal → `tisqanchi` |
| 2 | + P3 `i` (antes C): borra `a` → `tisqaski` | + P3 `u` (antes C): borra `i` → `tisqanchu` |
| 3 | + AFF `wa` (antes —; decide P3 (después V)): conserva la vocal → `tisqaskiwa` | + AFF `yi` (antes —; decide P3 (después V)): conserva la vocal → `tisqanchuyi` |
| **Salida** | **`tisqaskiwa`** | **`tisqanchuyi`** |

**Ejemplo 7.13 · ESTAR**

- Entrada: `chimula` + `LOC VBLZ.KA P1 AFF` — casa-LOC-VBLZ.KA-1-AFF — "estoy en la casa". Estado: patrón atestiguado (`utankthwa`, L2 p.50).
- Subyacente B: `chimula` + `na` + `ka` + `tha` + `wa`
- Subyacente A: `chimula` + `mu` + `ñu` + `phi` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `chimula` | raíz `chimula` |
| 1 | + LOC `na` (antes V): conserva la vocal → `chimulana` | + LOC `mu` (antes V): conserva la vocal → `chimulamu` |
| 2 | + VBLZ.KA `ka` (antes C): borra `a` → `chimulanka` | + VBLZ.KA `ñu` (antes C): borra `u` → `chimulamñu` |
| 3 | + P1 `tha` (antes C): borra `a` → `chimulanktha` | + P1 `phi` (antes C): borra `u` → `chimulamñphi` |
| 4 | + AFF `wa` (antes —; decide P1 (después C)): borra `a` → `chimulankthwa` | + AFF `yi` (antes —; decide P1 (después C)): borra `i` → `chimulamñphyi` |
| **Salida** | **`chimulankthwa`** | **`chimulamñphyi`** |

**Ejemplo 7.14 · TENER**

- Entrada: `chimula` + `POSR VBLZ.LONG P1 AFF` — casa-POSR-VBLZ.LONG-1-AFF — "tengo una casa". Estado: patrón atestiguado (`utanithwa`, L2 p.57).
- Subyacente B: `chimula` + `ni` + `¨` + `tha` + `wa`
- Subyacente A: `chimula` + `phu` + `¨` + `phi` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `chimula` | raíz `chimula` |
| 1 | + POSR `ni` (antes V): conserva la vocal → `chimulani` | + POSR `phu` (antes V): conserva la vocal → `chimulaphu` |
| 2 | + VBLZ.LONG tras POSR: no se escribe; protege la `i` (CH-705) → `chimulani` | + VBLZ.LONG tras POSR: no se escribe; protege la `u` (CH-705) → `chimulaphu` |
| 3 | + P1 `tha` (antes C): `i` protegida por VBLZ.LONG: no se borra (CH-705) → `chimulanitha` | + P1 `phi` (antes C): `u` protegida por VBLZ.LONG: no se borra (CH-705) → `chimulaphuphi` |
| 4 | + AFF `wa` (antes —; decide P1 (después C)): borra `a` → `chimulanithwa` | + AFF `yi` (antes —; decide P1 (después C)): borra `i` → `chimulaphuphyi` |
| **Salida** | **`chimulanithwa`** | **`chimulaphuphyi`** |

**Ejemplo 7.15 · SER**

- Entrada: `jumpu` + `VBLZ.LONG P1 AFF` — grande-VBLZ.LONG-1-AFF — "soy grande". Estado: patrón atestiguado (`jach'äthwa`, L2 p.51).
- Subyacente B: `jumpu` + `¨` + `tha` + `wa`
- Subyacente A: `jumpu` + `¨` + `phi` + `yi`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `jumpu` | raíz `jumpu` |
| 1 | + VBLZ.LONG `¨`: alarga `u` → `ü` → `jumpü` | + VBLZ.LONG `¨`: alarga `u` → `ü` → `jumpü` |
| 2 | + P1 `tha` (antes C): no hay vocal que borrar → `jumpütha` | + P1 `phi` (antes C): no hay vocal que borrar → `jumpüphi` |
| 3 | + AFF `wa` (antes —; decide P1 (después C)): borra `a` → `jumpüthwa` | + AFF `yi` (antes —; decide P1 (después C)): borra `i` → `jumpüphyi` |
| **Salida** | **`jumpüthwa`** | **`jumpüphyi`** |

**Ejemplo 7.16 · Cadena nominal**

- Entrada: `chimula` + `PL POSS.1 LOC` — casa-PL-POSS.1-LOC — "en mis casas". Estado: patrón atestiguado (`utanakajana`, L2 p.162).
- Subyacente B: `chimula` + `naka` + `ja` + `na`
- Subyacente A: `chimula` + `sulu` + `lu` + `mu`

| Paso | Modo B | Modo A |
|---|---|---|
| 0 | raíz `chimula` | raíz `chimula` |
| 1 | + PL `naka` (antes V): conserva la vocal → `chimulanaka` | + PL `sulu` (antes V): conserva la vocal → `chimulasulu` |
| 2 | + POSS.1 `ja` (antes V): conserva la vocal → `chimulanakaja` | + POSS.1 `lu` (antes V): conserva la vocal → `chimulasululu` |
| 3 | + LOC `na` (antes V): conserva la vocal → `chimulanakajana` | + LOC `mu` (antes V): conserva la vocal → `chimulasululumu` |
| **Salida** | **`chimulanakajana`** | **`chimulasululumu`** |


## 8. Paradigmas completos

Base: §3.4 (paradigmas de L2), CH-504, CH-601 a CH-606, CH-701.

**Cómo leer las tablas.**
- Verbo de ejemplo: `ch'ixra` "ver" (`V_TR`, `obj_persona = s`). Admite todas las celdas.
- Todas las formas las calcula el algoritmo CH-701; las tablas son la salida del prototipo.
- **Celda** = sujeto>objeto. En FUT, REM.C y REM.L el objeto es siempre 3 (CH-604).
- **B / A**: forma sin oracional. **+ AFF / + Q.YN**: con `-wa`/`-yi` o `-ti`/`-ji` al final.
- **†** = la forma usa al menos una regla [DERIVADA]. **Estado** lista cuáles (DV-xx, CH-702).
- "Atestiguado (patrón)": todas las formas de la fila siguen un patrón con forma atestiguada en L2 (CH-710).
- **Español**: traducción de referencia del verbo solo. La oración española completa sale de §10. El SIMP va en presente; con un adverbio de pasado, en pretérito (CH-1001).

#### 8.1 SIMP (9 transiciones)

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 | `P1` | `ch'ixrtha` | `ch'ixrthwa` | `ch'ixrthti` | `ch'ixrphi` | `ch'ixrphyi` | `ch'ixrphji` | veo | atestiguado (patrón) |
| 2>3 | `P2` | `ch'ixrta` | `ch'ixrtawa` | `ch'ixrtati`† | `ch'ixrku` | `ch'ixrkuyi` | `ch'ixrkuji`† | ves | DV-03 |
| 3>3 | `P3` | `ch'ixri` | `ch'ixriwa` | `ch'ixriti`† | `ch'ixru` | `ch'ixruyi` | `ch'ixruji`† | ve | DV-03 |
| 4>3 | `P4` | `ch'ixrtana` | `ch'ixrtanwa` | `ch'ixrtanti`† | `ch'ixrkilu` | `ch'ixrkilyi` | `ch'ixrkilji`† | vemos | DV-03 |
| 1>2 | `T12` | `ch'ixrsma` | `ch'ixrsmawa`† | `ch'ixrsmati`† | `ch'ixrjmi` | `ch'ixrjmiyi`† | `ch'ixrjmiji`† | te veo | DV-02 |
| 2>1 | `T21` | `ch'ixrista` | `ch'ixristawa`† | `ch'ixristati`† | `ch'ixrulqa` | `ch'ixrulqayi`† | `ch'ixrulqaji`† | me ves | DV-02 |
| 3>1 | `T31` | `ch'ixritu` | `ch'ixrituwa`† | `ch'ixrituti`† | `ch'ixruqu` | `ch'ixruquyi`† | `ch'ixruquji`† | me ve | DV-02 |
| 3>2 | `T32` | `ch'ixrtama` | `ch'ixrtamwa`† | `ch'ixrtamti`† | `ch'ixrkiqu` | `ch'ixrkiqyi`† | `ch'ixrkiqji`† | te ve | DV-01 |
| 3>4 | `T34` | `ch'ixristu` | `ch'ixristuwa`† | `ch'ixristuti`† | `ch'ixrulqu` | `ch'ixrulquyi`† | `ch'ixrulquji`† | nos ve | DV-02 |

#### 8.2 FUT

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 | `FUT.1` | `ch'ixrä` | `ch'ixräwa`† | `ch'ixräti`† | `ch'ixrä` | `ch'ixräyi`† | `ch'ixräji`† | veré | DV-04 |
| 2>3 | `FUT.2` | `ch'ixräta` | `ch'ixrätawa`† | `ch'ixrätati`† | `ch'ixräku` | `ch'ixräkuyi`† | `ch'ixräkuji`† | verás | DV-04 |
| 3>3 | `FUT.3` | `ch'ixrani` | `ch'ixraniwa` | `ch'ixraniti` | `ch'ixraphu` | `ch'ixraphuyi` | `ch'ixraphuji` | verá | atestiguado (patrón) |
| 4>3 | `FUT.4` | `ch'ixrañäni` | `ch'ixrañäniwa` | `ch'ixrañäniti`† | `ch'ixrathäqi` | `ch'ixrathäqiyi` | `ch'ixrathäqiji`† | veremos | DV-04 |

#### 8.3 REM.C (pasado visto)

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 | `REM.C P1` | `ch'ixrayätha` | `ch'ixrayäthwa`† | `ch'ixrayäthti`† | `ch'ixrajüphi` | `ch'ixrajüphyi`† | `ch'ixrajüphji`† | he visto | DV-05 |
| 2>3 | `REM.C P2` | `ch'ixrayäta` | `ch'ixrayätawa`† | `ch'ixrayätati`† | `ch'ixrajüku` | `ch'ixrajükuyi`† | `ch'ixrajükuji`† | has visto | DV-05 |
| 3>3 | `REM.C P3.REM` | `ch'ixräna` | `ch'ixränawa`† | `ch'ixränati`† | `ch'ixrämu` | `ch'ixrämuyi`† | `ch'ixrämuji`† | ha visto | DV-05 |
| 4>3 | `REM.C P4` | `ch'ixrayätana` | `ch'ixrayätanwa`† | `ch'ixrayätanti`† | `ch'ixrajükilu` | `ch'ixrajükilyi`† | `ch'ixrajükilji`† | hemos visto | DV-05 |

#### 8.4 REM.L (pasado no visto)

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 | `REM.L P1` | `ch'ixratätha` | `ch'ixratäthwa`† | `ch'ixratäthti`† | `ch'ixrawüphi` | `ch'ixrawüphyi`† | `ch'ixrawüphji`† | había visto | DV-05 |
| 2>3 | `REM.L P2` | `ch'ixratäta` | `ch'ixratätawa`† | `ch'ixratätati`† | `ch'ixrawüku` | `ch'ixrawükuyi`† | `ch'ixrawükuji`† | habías visto | DV-05 |
| 3>3 | `REM.L P3.REM` | `ch'ixratäna` | `ch'ixratänawa`† | `ch'ixratänati`† | `ch'ixrawümu` | `ch'ixrawümuyi`† | `ch'ixrawümuji`† | había visto | DV-05 |
| 4>3 | `REM.L P4` | `ch'ixratätana` | `ch'ixratätanwa`† | `ch'ixratätanti`† | `ch'ixrawükilu` | `ch'ixrawükilyi`† | `ch'ixrawükilji`† | habíamos visto | DV-05 |

#### 8.5 Plural del sujeto (PL.V) en todos los tiempos

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 PL | `PL.V P1` | `ch'ixrapxtha` | `ch'ixrapxthwa` | `ch'ixrapxthti` | `ch'ixramtphi` | `ch'ixramtphyi` | `ch'ixramtphji` | vemos | atestiguado (patrón) |
| 2>3 PL | `PL.V P2` | `ch'ixrapxta` | `ch'ixrapxtawa` | `ch'ixrapxtati`† | `ch'ixramtku` | `ch'ixramtkuyi` | `ch'ixramtkuji`† | ven | DV-03 |
| 3>3 PL | `PL.V P3` | `ch'ixrapxi` | `ch'ixrapxiwa` | `ch'ixrapxiti`† | `ch'ixramtu` | `ch'ixramtuyi` | `ch'ixramtuji`† | ven | DV-03 |
| 4>3 PL | `PL.V P4` | `ch'ixrapxtana` | `ch'ixrapxtanwa` | `ch'ixrapxtanti`† | `ch'ixramtkilu` | `ch'ixramtkilyi` | `ch'ixramtkilji`† | vemos | DV-03 |
| 1>2 PL | `PL.V T12` | `ch'ixrapxsma`† | `ch'ixrapxsmawa`† | `ch'ixrapxsmati`† | `ch'ixramtjmi`† | `ch'ixramtjmiyi`† | `ch'ixramtjmiji`† | te vemos | DV-02, DV-07 |
| 2>1 PL | `PL.V T21` | `ch'ixrapxista`† | `ch'ixrapxistawa`† | `ch'ixrapxistati`† | `ch'ixramtulqa`† | `ch'ixramtulqayi`† | `ch'ixramtulqaji`† | me ven | DV-02, DV-07 |
| 3>1 PL | `PL.V T31` | `ch'ixrapxitu`† | `ch'ixrapxituwa`† | `ch'ixrapxituti`† | `ch'ixramtuqu`† | `ch'ixramtuquyi`† | `ch'ixramtuquji`† | me ven | DV-02, DV-07 |
| 3>2 PL | `PL.V T32` | `ch'ixrapxtama`† | `ch'ixrapxtamwa`† | `ch'ixrapxtamti`† | `ch'ixramtkiqu`† | `ch'ixramtkiqyi`† | `ch'ixramtkiqji`† | te ven | DV-01, DV-07 |
| 3>4 PL | `PL.V T34` | `ch'ixrapxistu`† | `ch'ixrapxistuwa`† | `ch'ixrapxistuti`† | `ch'ixramtulqu`† | `ch'ixramtulquyi`† | `ch'ixramtulquji`† | nos ven | DV-02, DV-07 |
| 1>3 PL | `PL.V FUT.1` | `ch'ixrapxä`† | `ch'ixrapxäwa`† | `ch'ixrapxäti`† | `ch'ixramtü`† | `ch'ixramtüyi`† | `ch'ixramtüji`† | veremos | DV-04, DV-06 |
| 2>3 PL | `PL.V FUT.2` | `ch'ixrapxäta` | `ch'ixrapxätawa`† | `ch'ixrapxätati`† | `ch'ixramtüku` | `ch'ixramtükuyi`† | `ch'ixramtükuji`† | verán | DV-04 |
| 3>3 PL | `PL.V FUT.3` | `ch'ixrapxani`† | `ch'ixrapxaniwa`† | `ch'ixrapxaniti`† | `ch'ixramtuphu`† | `ch'ixramtuphuyi`† | `ch'ixramtuphuji`† | verán | DV-06 |
| 4>3 PL | `PL.V FUT.4` | `ch'ixrapxañäni`† | `ch'ixrapxañäniwa`† | `ch'ixrapxañäniti`† | `ch'ixramtuthäqi`† | `ch'ixramtuthäqiyi`† | `ch'ixramtuthäqiji`† | veremos | DV-04, DV-06 |
| 1>3 REM.C PL | `PL.V REM.C P1` | `ch'ixrapxayätha` | `ch'ixrapxayäthwa`† | `ch'ixrapxayäthti`† | `ch'ixramtujüphi` | `ch'ixramtujüphyi`† | `ch'ixramtujüphji`† | hemos visto | DV-05 |
| 2>3 REM.C PL | `PL.V REM.C P2` | `ch'ixrapxayäta` | `ch'ixrapxayätawa`† | `ch'ixrapxayätati`† | `ch'ixramtujüku` | `ch'ixramtujükuyi`† | `ch'ixramtujükuji`† | han visto | DV-05 |
| 3>3 REM.C PL | `PL.V REM.C P3.REM` | `ch'ixrapxäna` | `ch'ixrapxänawa`† | `ch'ixrapxänati`† | `ch'ixramtümu` | `ch'ixramtümuyi`† | `ch'ixramtümuji`† | han visto | DV-05 |
| 4>3 REM.C PL | `PL.V REM.C P4` | `ch'ixrapxayätana` | `ch'ixrapxayätanwa`† | `ch'ixrapxayätanti`† | `ch'ixramtujükilu` | `ch'ixramtujükilyi`† | `ch'ixramtujükilji`† | hemos visto | DV-05 |
| 1>3 REM.L PL | `PL.V REM.L P1` | `ch'ixrapxatätha`† | `ch'ixrapxatäthwa`† | `ch'ixrapxatäthti`† | `ch'ixramtuwüphi`† | `ch'ixramtuwüphyi`† | `ch'ixramtuwüphji`† | habíamos visto | DV-05, DV-06 |
| 2>3 REM.L PL | `PL.V REM.L P2` | `ch'ixrapxatäta`† | `ch'ixrapxatätawa`† | `ch'ixrapxatätati`† | `ch'ixramtuwüku`† | `ch'ixramtuwükuyi`† | `ch'ixramtuwükuji`† | habían visto | DV-05, DV-06 |
| 3>3 REM.L PL | `PL.V REM.L P3.REM` | `ch'ixrapxatäna`† | `ch'ixrapxatänawa`† | `ch'ixrapxatänati`† | `ch'ixramtuwümu`† | `ch'ixramtuwümuyi`† | `ch'ixramtuwümuji`† | habían visto | DV-05, DV-06 |
| 4>3 REM.L PL | `PL.V REM.L P4` | `ch'ixrapxatätana`† | `ch'ixrapxatätanwa`† | `ch'ixrapxatätanti`† | `ch'ixramtuwükilu`† | `ch'ixramtuwükilyi`† | `ch'ixramtuwükilji`† | habíamos visto | DV-05, DV-06 |

#### 8.6 Negación (SIMP y FUT)

| Celda | Ids | B | A | Español | Estado |
|---|---|---|---|---|---|
| 1>3 | `NEG P1 NEG.TI` | `janiwa ch'ixrkthti` | `yuliyi ch'ixrñphji` | no veo | atestiguado (patrón) |
| 2>3 | `NEG P2 NEG.TI` | `janiwa ch'ixrktati`† | `yuliyi ch'ixrñkuji`† | no ves | DV-03, DV-08 |
| 3>3 | `NEG P3 NEG.TI` | `janiwa ch'ixrkiti`† | `yuliyi ch'ixrñuji`† | no ve | DV-03, DV-08 |
| 4>3 | `NEG P4 NEG.TI` | `janiwa ch'ixrktanti`† | `yuliyi ch'ixrñkilji`† | no vemos | DV-03, DV-08 |
| 1>2 | `NEG T12 NEG.TI` | `janiwa ch'ixrksmati`† | `yuliyi ch'ixrñjmiji`† | no te veo | DV-02, DV-08 |
| 2>1 | `NEG T21 NEG.TI` | `janiwa ch'ixrkistati`† | `yuliyi ch'ixrñulqaji`† | no me ves | DV-02, DV-08 |
| 3>1 | `NEG T31 NEG.TI` | `janiwa ch'ixrkituti`† | `yuliyi ch'ixrñuquji`† | no me ve | DV-02, DV-08 |
| 3>2 | `NEG T32 NEG.TI` | `janiwa ch'ixrktamti`† | `yuliyi ch'ixrñkiqji`† | no te ve | DV-01, DV-08 |
| 3>4 | `NEG T34 NEG.TI` | `janiwa ch'ixrkistuti`† | `yuliyi ch'ixrñulquji`† | no nos ve | DV-02, DV-08 |
| 1>3 FUT | `NEG FUT.1 NEG.TI` | `janiwa ch'ixrkäti`† | `yuliyi ch'ixrñüji`† | no veré | DV-04, DV-08 |
| 2>3 FUT | `NEG FUT.2 NEG.TI` | `janiwa ch'ixrkätati`† | `yuliyi ch'ixrñükuji`† | no verás | DV-04, DV-08 |
| 3>3 FUT | `NEG FUT.3 NEG.TI` | `janiwa ch'ixrkaniti` | `yuliyi ch'ixrñuphuji` | no verá | atestiguado (patrón) |
| 4>3 FUT | `NEG FUT.4 NEG.TI` | `janiwa ch'ixrkañäniti`† | `yuliyi ch'ixrñuthäqiji`† | no veremos | DV-04, DV-08 |

#### 8.7 Progresivo (PROG, solo SIMP)

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1>3 | `PROG P1` | `ch'ixrasktha`† | `ch'ixraskthwa`† | `ch'ixraskthti`† | `ch'ixranchphi`† | `ch'ixranchphyi`† | `ch'ixranchphji`† | estoy viendo | DV-09 |
| 2>3 | `PROG P2` | `ch'ixraskta`† | `ch'ixrasktawa`† | `ch'ixrasktati`† | `ch'ixranchku`† | `ch'ixranchkuyi`† | `ch'ixranchkuji`† | estás viendo | DV-03, DV-09 |
| 3>3 | `PROG P3` | `ch'ixraski` | `ch'ixraskiwa` | `ch'ixraskiti`† | `ch'ixranchu` | `ch'ixranchuyi` | `ch'ixranchuji`† | está viendo | DV-03 |
| 4>3 | `PROG P4` | `ch'ixrasktana`† | `ch'ixrasktanwa`† | `ch'ixrasktanti`† | `ch'ixranchkilu`† | `ch'ixranchkilyi`† | `ch'ixranchkilji`† | estamos viendo | DV-03, DV-09 |
| 1>2 | `PROG T12` | `ch'ixrasksma`† | `ch'ixrasksmawa`† | `ch'ixrasksmati`† | `ch'ixranchjmi`† | `ch'ixranchjmiyi`† | `ch'ixranchjmiji`† | te estoy viendo | DV-02, DV-09 |
| 2>1 | `PROG T21` | `ch'ixraskista`† | `ch'ixraskistawa`† | `ch'ixraskistati`† | `ch'ixranchulqa`† | `ch'ixranchulqayi`† | `ch'ixranchulqaji`† | me estás viendo | DV-02, DV-09 |
| 3>1 | `PROG T31` | `ch'ixraskitu`† | `ch'ixraskituwa`† | `ch'ixraskituti`† | `ch'ixranchuqu`† | `ch'ixranchuquyi`† | `ch'ixranchuquji`† | me está viendo | DV-02, DV-09 |
| 3>2 | `PROG T32` | `ch'ixrasktama`† | `ch'ixrasktamwa`† | `ch'ixrasktamti`† | `ch'ixranchkiqu`† | `ch'ixranchkiqyi`† | `ch'ixranchkiqji`† | te está viendo | DV-01, DV-09 |
| 3>4 | `PROG T34` | `ch'ixraskistu`† | `ch'ixraskistuwa`† | `ch'ixraskistuti`† | `ch'ixranchulqu`† | `ch'ixranchulquyi`† | `ch'ixranchulquji`† | nos está viendo | DV-02, DV-09 |

#### 8.8 "Ser" (`jumpu` "grande")

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `VBLZ.LONG P1` | `jumpütha` | `jumpüthwa` | `jumpüthti`† | `jumpüphi` | `jumpüphyi` | `jumpüphji`† | soy grande | DV-13 |
| 2 | `VBLZ.LONG P2` | `jumpüta`† | `jumpütawa`† | `jumpütati`† | `jumpüku`† | `jumpükuyi`† | `jumpükuji`† | eres grande | DV-12, DV-13 |
| 4 | `VBLZ.LONG P4` | `jumpütana`† | `jumpütanwa`† | `jumpütanti`† | `jumpükilu`† | `jumpükilyi`† | `jumpükilji`† | somos grandes | DV-12, DV-13 |

#### 8.9 "Estar en" (`chimula` "casa")

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| P1 | `LOC VBLZ.KA P1` | `chimulanktha` | `chimulankthwa` | `chimulankthti`† | `chimulamñphi` | `chimulamñphyi` | `chimulamñphji`† | estoy en la casa | DV-13 |
| P2 | `LOC VBLZ.KA P2` | `chimulankta`† | `chimulanktawa`† | `chimulanktati`† | `chimulamñku`† | `chimulamñkuyi`† | `chimulamñkuji`† | estás en la casa | DV-10, DV-13 |
| P3 | `LOC VBLZ.KA P3` | `chimulanki`† | `chimulankiwa`† | `chimulankiti`† | `chimulamñu`† | `chimulamñuyi`† | `chimulamñuji`† | está en la casa | DV-10, DV-13 |
| P4 | `LOC VBLZ.KA P4` | `chimulanktana`† | `chimulanktanwa`† | `chimulanktanti`† | `chimulamñkilu`† | `chimulamñkilyi`† | `chimulamñkilji`† | estamos en la casa | DV-10, DV-13 |

#### 8.10 "Tener" (`chimula` "casa")

| Celda | Ids | B | B + AFF | B + Q.YN | A | A + AFF | A + Q.YN | Español | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `POSR VBLZ.LONG P1` | `chimulanitha` | `chimulanithwa` | `chimulanithti`† | `chimulaphuphi` | `chimulaphuphyi` | `chimulaphuphji`† | tengo una casa | DV-13 |
| 2 | `POSR VBLZ.LONG P2` | `chimulanita`† | `chimulanitawa`† | `chimulanitati`† | `chimulaphuku`† | `chimulaphukuyi`† | `chimulaphukuji`† | tienes una casa | DV-11, DV-13 |
| 4 | `POSR VBLZ.LONG P4` | `chimulanitana`† | `chimulanitanwa`† | `chimulanitanti`† | `chimulaphukilu`† | `chimulaphukilyi`† | `chimulaphukilji`† | tenemos una casa | DV-11, DV-13 |


**Notas.**
1. **Negación.** La negación siempre lleva `jani-wa` / `yuli-yi` como palabra aparte, después del sujeto (CH-905). La tabla 8.6 la muestra delante del verbo solo para leerla mejor.
2. **"Ser" en 3.ª persona** no tiene verbo: `Jupaxa jumpuwa.` / `Kaxixu jumpuyi.` "Él es grande." (CH-908).
3. **"Tener" en 3.ª persona** termina en POSR: `Jupaxa chimulaniwa.` / `Kaxixu chimulaphuyi.` "Él tiene una casa." (atestiguado, `utaniwa`, L2 p.49–52).
4. **Plural en "ser", "estar" y "tener".** No hay PL.V en los predicados nominales (CH-601). Su plural se marca **siempre** con `-naka` en el sujeto expreso (CH-913). Ejemplo: `Jumanakaxa chimulanktawa.` / `Tilusuluxu chimulamñkuyi.` "Ustedes están en la casa."
5. **Persona de "ser" y "estar".** Concuerda con el sujeto: 1, 2, 3 o 4.

```yaml
# paradigmas.yaml — celdas → ids (el motor de §7 calcula la forma).
# 'prueba' = formas esperadas con el verbo de ejemplo ch'ixra (modo B / modo A), sin oracional.
verbo_prueba: "ch'ixra"
celdas:
  - {tiempo: SIMP, celda: "1>3", ids: [P1], prueba: {b: "ch'ixrtha", a: "ch'ixrphi"}}
  - {tiempo: SIMP, celda: "2>3", ids: [P2], prueba: {b: "ch'ixrta", a: "ch'ixrku"}}
  - {tiempo: SIMP, celda: "3>3", ids: [P3], prueba: {b: "ch'ixri", a: "ch'ixru"}}
  - {tiempo: SIMP, celda: "4>3", ids: [P4], prueba: {b: "ch'ixrtana", a: "ch'ixrkilu"}}
  - {tiempo: SIMP, celda: "1>2", ids: [T12], prueba: {b: "ch'ixrsma", a: "ch'ixrjmi"}}
  - {tiempo: SIMP, celda: "2>1", ids: [T21], prueba: {b: "ch'ixrista", a: "ch'ixrulqa"}}
  - {tiempo: SIMP, celda: "3>1", ids: [T31], prueba: {b: "ch'ixritu", a: "ch'ixruqu"}}
  - {tiempo: SIMP, celda: "3>2", ids: [T32], prueba: {b: "ch'ixrtama", a: "ch'ixrkiqu"}}
  - {tiempo: SIMP, celda: "3>4", ids: [T34], prueba: {b: "ch'ixristu", a: "ch'ixrulqu"}}
  - {tiempo: FUT, celda: "1>3", ids: [FUT.1], prueba: {b: "ch'ixrä", a: "ch'ixrä"}}
  - {tiempo: FUT, celda: "2>3", ids: [FUT.2], prueba: {b: "ch'ixräta", a: "ch'ixräku"}}
  - {tiempo: FUT, celda: "3>3", ids: [FUT.3], prueba: {b: "ch'ixrani", a: "ch'ixraphu"}}
  - {tiempo: FUT, celda: "4>3", ids: [FUT.4], prueba: {b: "ch'ixrañäni", a: "ch'ixrathäqi"}}
  - {tiempo: REM.C, celda: "1>3", ids: [REM.C, P1], prueba: {b: "ch'ixrayätha", a: "ch'ixrajüphi"}}
  - {tiempo: REM.C, celda: "2>3", ids: [REM.C, P2], prueba: {b: "ch'ixrayäta", a: "ch'ixrajüku"}}
  - {tiempo: REM.C, celda: "3>3", ids: [REM.C, P3.REM], prueba: {b: "ch'ixräna", a: "ch'ixrämu"}}
  - {tiempo: REM.C, celda: "4>3", ids: [REM.C, P4], prueba: {b: "ch'ixrayätana", a: "ch'ixrajükilu"}}
  - {tiempo: REM.L, celda: "1>3", ids: [REM.L, P1], prueba: {b: "ch'ixratätha", a: "ch'ixrawüphi"}}
  - {tiempo: REM.L, celda: "2>3", ids: [REM.L, P2], prueba: {b: "ch'ixratäta", a: "ch'ixrawüku"}}
  - {tiempo: REM.L, celda: "3>3", ids: [REM.L, P3.REM], prueba: {b: "ch'ixratäna", a: "ch'ixrawümu"}}
  - {tiempo: REM.L, celda: "4>3", ids: [REM.L, P4], prueba: {b: "ch'ixratätana", a: "ch'ixrawükilu"}}
  - {tiempo: SIMP, celda: "1>3", plural_sujeto: true, ids: [PL.V, P1], prueba: {b: "ch'ixrapxtha", a: "ch'ixramtphi"}}
  - {tiempo: SIMP, celda: "2>3", plural_sujeto: true, ids: [PL.V, P2], prueba: {b: "ch'ixrapxta", a: "ch'ixramtku"}}
  - {tiempo: SIMP, celda: "3>3", plural_sujeto: true, ids: [PL.V, P3], prueba: {b: "ch'ixrapxi", a: "ch'ixramtu"}}
  - {tiempo: SIMP, celda: "4>3", plural_sujeto: true, ids: [PL.V, P4], prueba: {b: "ch'ixrapxtana", a: "ch'ixramtkilu"}}
  - {tiempo: SIMP, celda: "1>2", plural_sujeto: true, ids: [PL.V, T12], prueba: {b: "ch'ixrapxsma", a: "ch'ixramtjmi"}, derivada: [DV-07]}
  - {tiempo: SIMP, celda: "2>1", plural_sujeto: true, ids: [PL.V, T21], prueba: {b: "ch'ixrapxista", a: "ch'ixramtulqa"}, derivada: [DV-07]}
  - {tiempo: SIMP, celda: "3>1", plural_sujeto: true, ids: [PL.V, T31], prueba: {b: "ch'ixrapxitu", a: "ch'ixramtuqu"}, derivada: [DV-07]}
  - {tiempo: SIMP, celda: "3>2", plural_sujeto: true, ids: [PL.V, T32], prueba: {b: "ch'ixrapxtama", a: "ch'ixramtkiqu"}, derivada: [DV-07]}
  - {tiempo: SIMP, celda: "3>4", plural_sujeto: true, ids: [PL.V, T34], prueba: {b: "ch'ixrapxistu", a: "ch'ixramtulqu"}, derivada: [DV-07]}
  - {tiempo: FUT, celda: "1>3", plural_sujeto: true, ids: [PL.V, FUT.1], prueba: {b: "ch'ixrapxä", a: "ch'ixramtü"}, derivada: [DV-06]}
  - {tiempo: FUT, celda: "2>3", plural_sujeto: true, ids: [PL.V, FUT.2], prueba: {b: "ch'ixrapxäta", a: "ch'ixramtüku"}}
  - {tiempo: FUT, celda: "3>3", plural_sujeto: true, ids: [PL.V, FUT.3], prueba: {b: "ch'ixrapxani", a: "ch'ixramtuphu"}, derivada: [DV-06]}
  - {tiempo: FUT, celda: "4>3", plural_sujeto: true, ids: [PL.V, FUT.4], prueba: {b: "ch'ixrapxañäni", a: "ch'ixramtuthäqi"}, derivada: [DV-06]}
  - {tiempo: REM.C, celda: "1>3", plural_sujeto: true, ids: [PL.V, REM.C, P1], prueba: {b: "ch'ixrapxayätha", a: "ch'ixramtujüphi"}}
  - {tiempo: REM.C, celda: "2>3", plural_sujeto: true, ids: [PL.V, REM.C, P2], prueba: {b: "ch'ixrapxayäta", a: "ch'ixramtujüku"}}
  - {tiempo: REM.C, celda: "3>3", plural_sujeto: true, ids: [PL.V, REM.C, P3.REM], prueba: {b: "ch'ixrapxäna", a: "ch'ixramtümu"}}
  - {tiempo: REM.C, celda: "4>3", plural_sujeto: true, ids: [PL.V, REM.C, P4], prueba: {b: "ch'ixrapxayätana", a: "ch'ixramtujükilu"}}
  - {tiempo: REM.L, celda: "1>3", plural_sujeto: true, ids: [PL.V, REM.L, P1], prueba: {b: "ch'ixrapxatätha", a: "ch'ixramtuwüphi"}, derivada: [DV-06]}
  - {tiempo: REM.L, celda: "2>3", plural_sujeto: true, ids: [PL.V, REM.L, P2], prueba: {b: "ch'ixrapxatäta", a: "ch'ixramtuwüku"}, derivada: [DV-06]}
  - {tiempo: REM.L, celda: "3>3", plural_sujeto: true, ids: [PL.V, REM.L, P3.REM], prueba: {b: "ch'ixrapxatäna", a: "ch'ixramtuwümu"}, derivada: [DV-06]}
  - {tiempo: REM.L, celda: "4>3", plural_sujeto: true, ids: [PL.V, REM.L, P4], prueba: {b: "ch'ixrapxatätana", a: "ch'ixramtuwükilu"}, derivada: [DV-06]}
  - {tiempo: SIMP, celda: "1>3", negativa: true, ids: [NEG, P1, NEG.TI], prueba: {b: "ch'ixrkthti", a: "ch'ixrñphji"}}
  - {tiempo: SIMP, celda: "2>3", negativa: true, ids: [NEG, P2, NEG.TI], prueba: {b: "ch'ixrktati", a: "ch'ixrñkuji"}, derivada: [DV-03, DV-08]}
  - {tiempo: SIMP, celda: "3>3", negativa: true, ids: [NEG, P3, NEG.TI], prueba: {b: "ch'ixrkiti", a: "ch'ixrñuji"}, derivada: [DV-03, DV-08]}
  - {tiempo: SIMP, celda: "4>3", negativa: true, ids: [NEG, P4, NEG.TI], prueba: {b: "ch'ixrktanti", a: "ch'ixrñkilji"}, derivada: [DV-03, DV-08]}
  - {tiempo: SIMP, celda: "1>2", negativa: true, ids: [NEG, T12, NEG.TI], prueba: {b: "ch'ixrksmati", a: "ch'ixrñjmiji"}, derivada: [DV-02, DV-08]}
  - {tiempo: SIMP, celda: "2>1", negativa: true, ids: [NEG, T21, NEG.TI], prueba: {b: "ch'ixrkistati", a: "ch'ixrñulqaji"}, derivada: [DV-02, DV-08]}
  - {tiempo: SIMP, celda: "3>1", negativa: true, ids: [NEG, T31, NEG.TI], prueba: {b: "ch'ixrkituti", a: "ch'ixrñuquji"}, derivada: [DV-02, DV-08]}
  - {tiempo: SIMP, celda: "3>2", negativa: true, ids: [NEG, T32, NEG.TI], prueba: {b: "ch'ixrktamti", a: "ch'ixrñkiqji"}, derivada: [DV-01, DV-08]}
  - {tiempo: SIMP, celda: "3>4", negativa: true, ids: [NEG, T34, NEG.TI], prueba: {b: "ch'ixrkistuti", a: "ch'ixrñulquji"}, derivada: [DV-02, DV-08]}
  - {tiempo: FUT, celda: "1>3", negativa: true, ids: [NEG, FUT.1, NEG.TI], prueba: {b: "ch'ixrkäti", a: "ch'ixrñüji"}, derivada: [DV-04, DV-08]}
  - {tiempo: FUT, celda: "2>3", negativa: true, ids: [NEG, FUT.2, NEG.TI], prueba: {b: "ch'ixrkätati", a: "ch'ixrñükuji"}, derivada: [DV-04, DV-08]}
  - {tiempo: FUT, celda: "3>3", negativa: true, ids: [NEG, FUT.3, NEG.TI], prueba: {b: "ch'ixrkaniti", a: "ch'ixrñuphuji"}}
  - {tiempo: FUT, celda: "4>3", negativa: true, ids: [NEG, FUT.4, NEG.TI], prueba: {b: "ch'ixrkañäniti", a: "ch'ixrñuthäqiji"}, derivada: [DV-04, DV-08]}
  - {tiempo: SIMP, celda: "1>3", progresivo: true, ids: [PROG, P1], prueba: {b: "ch'ixrasktha", a: "ch'ixranchphi"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "2>3", progresivo: true, ids: [PROG, P2], prueba: {b: "ch'ixraskta", a: "ch'ixranchku"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "3>3", progresivo: true, ids: [PROG, P3], prueba: {b: "ch'ixraski", a: "ch'ixranchu"}}
  - {tiempo: SIMP, celda: "4>3", progresivo: true, ids: [PROG, P4], prueba: {b: "ch'ixrasktana", a: "ch'ixranchkilu"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "1>2", progresivo: true, ids: [PROG, T12], prueba: {b: "ch'ixrasksma", a: "ch'ixranchjmi"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "2>1", progresivo: true, ids: [PROG, T21], prueba: {b: "ch'ixraskista", a: "ch'ixranchulqa"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "3>1", progresivo: true, ids: [PROG, T31], prueba: {b: "ch'ixraskitu", a: "ch'ixranchuqu"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "3>2", progresivo: true, ids: [PROG, T32], prueba: {b: "ch'ixrasktama", a: "ch'ixranchkiqu"}, derivada: [DV-09]}
  - {tiempo: SIMP, celda: "3>4", progresivo: true, ids: [PROG, T34], prueba: {b: "ch'ixraskistu", a: "ch'ixranchulqu"}, derivada: [DV-09]}
oracional:
  AFF: "añadir AFF al final"
  Q.YN: "añadir Q.YN al final"
predicados_nominales:
  SER:   {"1": [VBLZ.LONG, P1], "2": [VBLZ.LONG, P2], "4": [VBLZ.LONG, P4], "3": "sin verbo: NP_NORMAL + AFF (CH-908)"}
  ESTAR: {"1": [LOC, VBLZ.KA, P1], "2": [LOC, VBLZ.KA, P2], "3": [LOC, VBLZ.KA, P3], "4": [LOC, VBLZ.KA, P4]}
  TENER: {"1": [POSR, VBLZ.LONG, P1], "2": [POSR, VBLZ.LONG, P2], "4": [POSR, VBLZ.LONG, P4], "3": [POSR]}
```

---

## 9. Sintaxis

Todas las oraciones salen de una idea (§11 de este documento).
- Primero se arma el **orden de constituyentes**.
- Después cada palabra se construye con §7.
- Al final se ponen la mayúscula y la puntuación (CH-106).

Los ejemplos dan B (con glosa), A y español. Las tres salidas las calcula el prototipo de referencia.

### CH-901 · Orden de constituyentes [DECISIÓN CHULUPI]

Base: D10; §1 (L2 p.255: tiempo – lugar – objeto indirecto – objeto directo – verbo); L2 p.241, 243 (SOV). L2 no ubica COM, CAUSE ni UNTIL: los ponemos después del lugar y antes del objeto indirecto.

| Posición | Constituyente | Qué puede ser |
|---|---|---|
| 1 | Sujeto (S) | pronombre, frase nominal, demostrativo (solo en "ser"), coordinación (CH-907) o interrogativo `khiti` |
| 2 | `jani-wa` | solo en negativas (CH-905) |
| 3 | Tiempo (T) | adverbio de tiempo, sin sufijo de caso |
| 4 | Lugar (L) | ALL, ABL, UNTIL (con `V_MOV`) o LOC (frase nominal o deíctico, CH-916) |
| 5 | COM o CAUSE | uno de los dos como máximo |
| 6 | Objeto indirecto (OI) | COMPL.RU o BEN (nunca los dos, CH-910) |
| 7 | Objeto directo (OD) | frase nominal sin sufijo, o coordinación |
| 8 | Verbo (V) | §6 y §8 de este documento |

- Cada posición tiene como máximo un constituyente.
- Si una posición está vacía, se salta.
- En "ser", "estar" y "tener", la posición 8 es el predicado nominal (CH-908) y no hay posiciones 4 a 7.

Ejemplo:
- B: `Simlla-xa jaskhi pinqara-na lisqu-ru q'aspi tulph-i-wa.` → `Simllaxa jaskhi pinqarana lisquru q'aspi tulphiwa.` — mujer-TOP ayer mercado-LOC niño-COMPL.RU pan dar-3>3.SIMP-AFF.
- A: `Simllaxu jaskhi pinqaramu lisqullu q'aspi tulphuyi.`
- ES: "La mujer le dio pan al niño en el mercado ayer."

### CH-902 · Posición de `-wa` [DECISIÓN CHULUPI]

Base: §1 y §4 (L1 p.280–281, 297: `-wa` va en el elemento que responde la pregunta subyacente; uno solo por oración); §4.1 (L2 p.230). L2 atestigua las cuatro opciones:
- en el verbo: `sarthwa`;
- en el sujeto: `mamajawa jutani`;
- en un complemento con caso: `utaruwa sari`, `jilajatakiwa`, `markakamawa sari`, `wallatampiwa`;
- en ningún sitio: `churtha`, `churi`, `jutani`.

El campo `posicion_wa` de la idea vale para **oraciones verbales afirmativas**:

| Valor | Dónde va `-wa` | Si no se puede |
|---|---|---|
| `verbo` | en el verbo | — |
| `sujeto` | en el sujeto expreso, en lugar de `-xa`; en una coordinación, en el segundo miembro | → `verbo` |
| `complemento` | en el complemento con ALL, UNTIL, COM, CAUSE, COMPL.RU o BEN **más cercano al verbo** | → `verbo` |
| `ninguna` | ninguna palabra lleva `-wa` | — |

Nunca va `-wa` en: el objeto directo, ABL, LOC, el adverbio de tiempo ni el deíctico.

En los demás tipos de oración la posición es fija:
- negativa: en `jani` (CH-905);
- "ser", "estar", "tener" afirmativas: en el predicado;
- preguntas: no hay `-wa`.

El español es el mismo en los cuatro casos. Ejemplos (idea: la maestra, ir, FUT, al pueblo):

| `posicion_wa` | B | A |
|---|---|---|
| `verbo` | `Yaruqhixa wirkharu tisqaniwa.` | `Yaruqhixu wirkhallu tisqaphuyi.` |
| `sujeto` | `Yaruqhiwa wirkharu tisqani.` | `Yaruqhiyi wirkhallu tisqaphu.` |
| `complemento` | `Yaruqhixa wirkharuwa tisqani.` | `Yaruqhixu wirkhalluyi tisqaphu.` |
| `ninguna` | `Yaruqhixa wirkharu tisqani.` | `Yaruqhixu wirkhallu tisqaphu.` |

- Glosa (fila `verbo`): maestro-TOP pueblo-ALL ir-3>3.FUT-AFF.
- ES: "La maestra irá al pueblo."
- Caso de respaldo: con `posicion_wa = complemento` y solo un LOC (no admite `-wa`), va al verbo: `Nayaxa chimulana nuyk'thwa.` / `Muqixu chimulamu nuyk'phyi.` "Yo duermo en la casa."

### CH-903 · Posición de `-xa` [DECISIÓN CHULUPI]

Base: §4.1 (L2 p.231: "por lo general marca el sujeto"); §1 (L2 p.255: `Wasüruxa…` sin sujeto).

1. El sujeto expreso lleva `-xa`. Excepciones: si lleva `-wa` (CH-902), si es coordinado (CH-907) o si es el interrogativo.
2. Si no hay **ningún** sujeto expreso (ni interrogativo) y hay adverbio de tiempo, el adverbio lleva `-xa`.
3. Ninguna otra palabra lleva `-xa`.

Ejemplo (regla 2):
- B: `Jaskhi-xa pinqara-ta pajlla-tä-na-wa.` → `Jaskhixa pinqarata pajllatänawa.` — ayer-TOP mercado-ABL venir-REM.L-3-AFF.
- A: `Jaskhixu pinqaraku pajllawümuyi.`
- ES: "Había venido del mercado ayer."

### CH-904 · `-ti` de pregunta sí/no [DECISIÓN CHULUPI]

Base: §4.1 (L2 p.235: `¿Jilamaxa jutaniti?`). L1 permite `-ti` en otros elementos (p.282), pero no lo modelamos.

- `-ti` va siempre en el verbo, o en el predicado de "ser", "estar" y "tener".
- No hay `-wa` en la oración. El sujeto lleva `-xa`, igual que en una afirmativa.

Ejemplo:
- B: `¿Pultiya-ma-xa pajlla-ni-ti?` → `¿Pultiyamaxa pajllaniti?` — hermano-POSS.2-TOP venir-3>3.FUT-Q.YN.
- A: `¿Pultiyaqixu pajllaphuji?`
- ES: "¿Tu hermano vendrá?"

### CH-905 · Negación [DECISIÓN CHULUPI]

Base: §3.3, §7.3 B (L1 p.283, 299–302: `jani` + `-wa`, `-ti` donde iría `-wa`); L2 p.231 (`Jilaqataxa janiwa jutkaniti`).

- La palabra `jani-wa` (A `yuli-yi`) va justo después del sujeto, o al principio si no hay sujeto.
- El verbo lleva NEG (`-ka`) y NEG.TI (`-ti`).
- Es el único `-wa` de la oración.
- Solo en SIMP y FUT (CH-605); sin PL.V (CH-603).

Ejemplo:
- B: `Kirpu-xa jani-wa q'aspi lamch'-ka-ni-ti.` → `Kirpuxa janiwa q'aspi lamch'kaniti.` — perro-TOP NEG-AFF pan comer-INCOMPL-3>3.FUT-NEG.
- A: `Kirpuxu yuliyi q'aspi lamch'ñuphuji.`
- ES: "El perro no comerá pan."

### CH-906 · Pregunta de información [DECISIÓN CHULUPI]

Base: §1 y §6 (L1 p.282: un solo `-sa` por oración; `kawki-ru-s`); L2 p.236 (`¿kawkirusa sarañäni?`); D10 (sin permutaciones). El interrogativo **queda en el lugar** del constituyente que reemplaza.

| `interrogativo` | Reemplaza a | Forma B → A | Condiciones |
|---|---|---|---|
| `quien_suj` | sujeto | `khiti-sa` → `simu-khu` | sujeto de 3.ª singular; verbo `suj_clases` ∋ `persona` |
| `que_od` | objeto directo | `kuna-sa` → `mulu-khu` | verbo `V_TR` o `V_DITR` en X>3 |
| `donde_all` | lugar ALL | `kawki-ru-sa` → `yaqu-llu-khu` | verbo `V_MOV` |
| `quien_oi` | COMPL.RU | `khiti-ru-sa` → `simu-llu-khu` | verbo `V_DITR` en X>3 |
| `donde_estar` | predicado de "estar" | `kawki-n-k-PERS-sa` → `yaqu-m-ñ-PERS-khu` | solo "estar" |

- No hay `-wa`. El verbo va sin oracional.
- Si hay sujeto expreso (y no es el interrogativo), lleva `-xa`.

Ejemplos:
- B: `¿Kirpu-xa kuna-sa lamch'-i?` → `¿Kirpuxa kunasa lamch'i?` — perro-TOP qué-Q.INF comer-3>3.SIMP. A: `¿Kirpuxu mulukhu lamch'u?` ES: "¿Qué come el perro?"
- B: `¿Khiti-ru-sa q'aspi tulph-ta?` → `¿Khitirusa q'aspi tulphta?` — quién-COMPL.RU-Q.INF pan dar-2>3.SIMP. A: `¿Simullukhu q'aspi tulphku?` ES: "¿A quién le das pan?"
- B: `¿Juma-xa kawki-n-k-ta-sa?` → `¿Jumaxa kawkinktasa?` — 2-TOP dónde-LOC-VBLZ.KA-2-Q.INF. A: `¿Tiluxu yaqumñkukhu?` ES: "¿Dónde estás tú?"

### CH-907 · Coordinación [DECISIÓN CHULUPI]

Base: D13; §1 (L1 p.208, 255: cada miembro lleva `-mpi`); L2 p.160 (`Tiwulampi wallatampiwa jikisipxi`).

- Exactamente 2 miembros, cada uno `N-mpi`, sin PL y con como máximo un adjetivo.
- **Como sujeto:**
  - solo nombres de 3.ª persona;
  - el verbo lleva PL.V (es plural, CH-913);
  - sin `-xa`;
  - si `posicion_wa = sujeto`, `-wa` va en el 2.º miembro (como en L2).
- **Como objeto directo:** nombres compatibles con `obj_clases`.
- Prohibido:
  - en negativas (el plural no se podría marcar, CH-913);
  - en preguntas de información;
  - con un complemento COM en la misma oración (evita confundir "y" con "con").

Ejemplos:
- B: `Kirpu-mpi lisqu-mpi-wa pinqara-ru tisqa-px-i.` → `Kirpumpi lisqumpiwa pinqararu tisqapxi.` — perro-COM niño-COM-AFF mercado-ALL ir-PL-3>3.SIMP. A: `Kirpunku lisqunkuyi pinqarallu tisqamtu.` ES: "El perro y la niña van al mercado." (`genero = f`)
- B: `Nayaxa q'aspimpi jitqumpi nirqayäthwa.` — 1-TOP pan-COM cuchillo-COM comprar-REM.C-1-AFF. A: `Muqixu q'aspinku jitqunku nirqajüphyi.` ES: "Yo he comprado pan y el cuchillo."

### CH-908 · "Ser", "estar" y "tener" [DECISIÓN CHULUPI]

Base:
- "ser": §1 y §6 (`misa-x jach'a-wa`, L1 p.172); L2 p.243 (`akaxa kunasa`); `jach'äthwa` (L2 p.51).
- "estar": `utankthwa` (L2 p.50).
- "tener": `utanithwa`, `utaniwa` (L2 p.49–57); §13 #14 (solo formas atestiguadas o su patrón).

Siempre en SIMP, y solo afirmativa (`-wa` en el predicado) o pregunta sí/no (`-ti` en el predicado). "Estar" admite además "¿dónde está?" (CH-906). No hay negación (P5, CH-605).

| Predicado | 3.ª persona | 1.ª, 2.ª y 4.ª persona | Compatibilidad (CH-406) |
|---|---|---|---|
| ser + adjetivo | `S-xa ADJ-wa` | `S-xa ADJ-¨-PERS-wa` | sujeto ∈ `mod_clases` del adjetivo |
| ser + nombre | `DEM-xa N-wa`, o `S-xa N-wa` con S y N `persona` | `S-xa N-¨-PERS-wa` (N `persona`) | sujeto demostrativo + cualquier nombre; o sujeto humano + nombre humano |
| estar en | `S-xa [mods] N-(naka)-(POSS)-n-k-i-wa` o `DEM-n-k-i-wa` | igual, con PERS | lugar: `lugar`, `vivienda`, `recipiente` o deíctico |
| tener | `S-xa [NUM \| ADJ] N-(naka)-ni-wa` | `… N-(naka)-ni-(¨)-PERS-wa` | poseedor `persona`; poseído según CH-406 |

Plural del sujeto: siempre sujeto expreso con `-naka` (CH-913). En "ser" de 3.ª persona con nombre, el nombre predicado también lleva `-naka`.

Ejemplos:
- B: `Chimula-xa jumpu-wa.` — casa-TOP grande-AFF. A: `Chimulaxu jumpuyi.` ES: "La casa es grande."
- B: `Naya-xa jumpu-¨-th-wa.` → `Nayaxa jumpüthwa.` — 1-TOP grande-VBLZ.LONG-1-AFF. A: `Muqixu jumpüphyi.` ES: "Yo soy grande."
- B: `Aka-xa chimula-wa.` — este-TOP casa-AFF. A: `Ilmixu chimulayi.` ES: "Esta es una casa."
- B: `Jumaxa yaruqhïtawa.` — 2-TOP maestro-VBLZ.LONG-2-AFF [DERIVADA, DV-12]. A: `Tiluxu yaruqhïkuyi.` ES: "Tú eres maestra." (`genero = f`)
- B: `Kirpu-xa chimula-ja-n-k-i-wa.` → `Kirpuxa chimulajankiwa.` — perro-TOP casa-POSS.1-LOC-VBLZ.KA-3-AFF [DV-10]. A: `Kirpuxu chimulalumñuyi.` ES: "El perro está en mi casa."
- B: `¿Aka-n-k-tan-ti?` → `¿Akanktanti?` — DEM.1-LOC-VBLZ.KA-4-Q.YN [DV-10, DV-13]. A: `¿Ilmimñkilji?` ES: "¿Estamos aquí?"
- B: `Nayaxa kimsa kirpunithwa.` — 1-TOP tres perro-POSR-VBLZ.LONG-1-AFF. A: `Muqixu musqi kirpuphuphyi.` ES: "Yo tengo tres perros."
- B: `Pultiyajaxa q'ulli jitquniwa.` — hermano-POSS.1-TOP rojo cuchillo-POSR-AFF. A: `Pultiyaluxu q'ulli jitquphuyi.` ES: "Mi hermana tiene un cuchillo rojo."

### CH-909 · COMPL.RU [DECISIÓN CHULUPI]

Base: D9; §7.3 A; §13 #7 (hace falta saber qué verbos rigen `-ru`).

- COMPL.RU solo con verbos `rige_ru = s` (`V_DITR`).
- Con objeto de 3.ª persona, COMPL.RU es un nombre `persona` (CH-406) y es opcional.
- Con objeto 1, 2 o 4 (transiciones), el destinatario es esa persona. Puede expresarse con el pronombre + `-ru` (campo `oi_pronombre_expreso`), según L1 `naya-r parla-p-x-itu` (p.112).
- En el español no cambia nada (CH-1009).

Ejemplo:
- B: `Jupa-xa naya-ru q'aspi tulph-itu-wa.` → `Jupaxa nayaru q'aspi tulphituwa.` — 3-TOP 1-COMPL.RU pan dar-3>1.SIMP-AFF [DV-02].
- A: `Kaxixu muqillu q'aspi tulphuquyi.`
- ES: "Él me da pan."

### CH-910 · COMPL.RU y BEN no van juntos [DECISIÓN CHULUPI]

Base: §7.3 A (L1 p.218: `-taki` tiene precedencia y vuelve relacionales a `-ru` y `-ta`). La posición OI admite uno solo. BEN es siempre `persona`.

Ejemplo:
- B: `Nayaxa jaskhi pultiyajataki jitqu nirqthwa.` — 1-TOP ayer hermano-POSS.1-BEN cuchillo comprar-1>3.SIMP-AFF.
- A: `Muqixu jaskhi pultiyalupuli jitqu nirqphyi.`
- ES: "Yo compré el cuchillo para mi hermano ayer."
- ✗ La misma idea con un COMPL.RU además.

### CH-911 · Posesión [DECISIÓN CHULUPI]

Base: §1 (L1 p.224, 247: el poseedor pronominal puede omitirse); §2.1 (L2 p.154: `tatajana utapa`).

- Poseedor pronominal: **se omite**. Queda solo el posesivo (`chimula-ja` "mi casa").
- Poseedor nominal: `N_HUM` de 3.ª persona con GEN, antes de la frase. Lo poseído lleva POSS.3.
- Un poseedor por frase. El poseedor no lleva modificadores.

Ejemplo:
- B: `Nayaxa yaruqhi-na chimula-pa ch'ixr-th-wa.` → `Nayaxa yaruqhina chimulapa ch'ixrthwa.` — 1-TOP maestro-GEN casa-POSS.3 ver-1>3.SIMP-AFF.
- A: `Muqixu yaruqhimu chimulachu ch'ixrphyi.`
- ES: "Yo veo la casa del maestro."

### CH-912 · Frase nominal [DECISIÓN CHULUPI]

Base: §1 (L1 p.248–252: demostrativo/numeral + tamaño + color + núcleo; el sufijo va solo en el núcleo); D6 (todas las palabras con vocal completa).

- Orden: `[poseedor-GEN] [DEM | NUM] [ADJ] NÚCLEO-sufijos`.
- Como máximo un demostrativo **o** un numeral, y un adjetivo (que cumpla `mod_clases`).
- Un demostrativo no va con poseedor ni con posesivo.
- Un numeral excluye PL en el núcleo (§13 #11).

Ejemplo:
- B: `Jiwasaxa uka jumpu kirpu nirqañäniwa.` — 4-TOP ese grande perro comprar-4>3.FUT-AFF.
- A: `Wiqutuxu ulmi jumpu kirpu nirqathäqiyi.`
- ES: "Nosotros compraremos ese perro grande."

### CH-913 · El plural se marca siempre [DECISIÓN CHULUPI]

Base: decisión del equipo (ajuste 2); D12 (L2 p.181, 242: la concordancia tiende a ser obligatoria).

Si `sujeto.plural = true`:

| Tipo de oración | Marca obligatoria |
|---|---|
| Verbal afirmativa o pregunta | PL.V en el verbo **y** `-naka` en el sujeto expreso (pronombre o nombre). Con numeral, sin `-naka`. Coordinación: sin `-naka`. |
| Verbal negativa | Sujeto expreso **obligatorio** con `-naka` (o `nänaka`); sin PL.V (CH-603). No se permiten sujetos con numeral ni coordinados. |
| Ser, estar, tener | Sujeto expreso obligatorio con `-naka`. |
| Pregunta de información con `quien_suj` | Prohibido el plural. |

Además:
- `-pxa` (PL.V) **solo** marca plural del sujeto. El plural del objeto se marca con `-naka` en el OD.
- Un sujeto sin plural es siempre singular. Así, una oración nunca tiene dos traducciones por número.

Ejemplos:
- B: `Lisqu-naka-xa wirkha-ta pajlla-px-¨-na-wa.` → `Lisqunakaxa wirkhata pajllapxänawa.` — niño-PL-TOP pueblo-ABL venir-PL-REM.C-3-AFF [DV-05]. A: `Lisqusuluxu wirkhaku pajllamtümuyi.` ES: "Las niñas han venido del pueblo." (`genero = f`)
- B: `Nänakaxa janiwa akana nuyk'kthti.` — 1.PL-TOP NEG-AFF DEM.1-LOC dormir-INCOMPL-1>3.SIMP-NEG. A: `Müsuluxu yuliyi ilmimu nuyk'ñphji.` ES: "Nosotros no dormimos aquí."
- B: `Pusi kirpuxa q'aspi lamch'apxiwa.` — cuatro perro-TOP pan comer-PL-3>3.SIMP-AFF. A: `Tayli kirpuxu q'aspi lamch'amtuyi.` ES: "Cuatro perros comen pan."

### CH-914 · El objeto directo es no humano [DECISIÓN CHULUPI]

Base: §13 #7; §2.1 (L2 p.154: acusativo `-ø`); D9.

- El OD es siempre un nombre `N_NOHUM` sin sufijo de caso, con la vocal final completa (D6).
- Un objeto humano solo se expresa como persona de la transición (CH-604) o como COMPL.RU (CH-909).

Ejemplo:
- B: `Kirpu-xa ch'ixr-istu-wa.` → `Kirpuxa ch'ixristuwa.` — perro-TOP ver-3>4.SIMP-AFF [DV-02].
- A: `Kirpuxu ch'ixrulquyi.`
- ES: "El perro nos ve."

### CH-915 · OD obligatorio en X>3 [DECISIÓN CHULUPI]

- Con `V_TR` o `V_DITR` y objeto de 3.ª persona, el OD es obligatorio, salvo que lo reemplace `kuna-sa`. Así el español no necesita adivinar "lo/la".
- Con objeto 1, 2 o 4:
  - `V_TR`: no hay OD (el objeto es la persona);
  - `V_DITR`: el OD (la cosa) es obligatorio.

Ejemplo:
- B: `Jumaxa jitqumpi q'aspi k'iymtawa.` — 2-TOP cuchillo-COM pan cortar-2>3.SIMP-AFF.
- A: `Tiluxu jitqunku q'aspi k'iymkuyi.`
- ES: "Tú cortas pan con el cuchillo."
- ✗ La misma idea sin `q'aspi`.

### CH-916 · Adverbios de lugar [DECISIÓN CHULUPI]

Base: §2.1 (L2 p.160: `ukana irnaqtha` "ahí trabajo"); §1 (L1: demostrativo + LOC).

- "Aquí", "ahí" y "más allá" = `aka-na`, `uka-na`, `khuri-na` (A `ilmi-mu`, `ulmi-mu`, `phiqa-mu`).
- Ocupan la posición de lugar con verbos que admiten LOC.
- Con VBLZ.KA forman "estar aquí / ahí / allá".

Ejemplo:
- B: `Kirpu-xa uka-na nuyk'-i-wa.` → `Kirpuxa ukana nuyk'iwa.` — perro-TOP DEM.2-LOC dormir-3>3.SIMP-AFF.
- A: `Kirpuxu ulmimu nuyk'uyi.`
- ES: "El perro duerme ahí."

### CH-917 · Adverbio de tiempo y tiempo verbal [DECISIÓN CHULUPI]

Base: §3.2 (SIMP: presente o pasado; FUT: futuro; REM: pasado).

| `ADV_T.subcat` | Tiempos permitidos |
|---|---|
| `pasado` | SIMP (no progresivo), REM.C, REM.L |
| `presente` | SIMP (incluido el progresivo) |
| `futuro` | FUT |

Sin adverbio, cualquier tiempo.

Ejemplo:
- B: `Sik'uyu-xa pajlla-¨ta-wa.` → `Sik'uyuxa pajllätawa.` — mañana-TOP venir-2>3.FUT-AFF [DV-04].
- A: `Sik'uyuxu pajlläkuyi.`
- ES: "Vendrás mañana."
- ✗ `sik'uyu` con REM.L.

### CH-918 · Otros complementos (CAUSE, UNTIL, COM)

Base: §2.1 (L2 p.160–161); CH-406; CH-514.
- CAUSE y COM (instrumento o compañía) van en la posición 5.
- UNTIL va en la posición 4 (lugar), solo con `V_MOV`.

Ejemplos:
- B: `Simllaxa ch'alqulaykuwa pajllatäna.` — mujer-TOP deuda-CAUSE-AFF venir-REM.L-3 (`posicion_wa = complemento`). A: `Simllaxu ch'alqutiwqayi pajllawümu.` ES: "La mujer había venido por la deuda."
- B: `Jiwasaxa wirkhakamawa tisqañäni.` — 4-TOP pueblo-UNTIL-AFF ir-4>3.FUT. A: `Wiqutuxu wirkhachiwiyi tisqathäqi.` ES: "Nosotros iremos hasta el pueblo."
- B: `Nayaxa jaskhi pinqararu kirpumpi tisqthwa.` — 1-TOP ayer mercado-ALL perro-COM ir-1>3.SIMP-AFF (COM de compañía). A: `Muqixu jaskhi pinqarallu kirpunku tisqphyi.` ES: "Yo fui al mercado con el perro ayer."

```yaml
# sintaxis (parte de slots.yaml)
orden_constituyentes: [S, JANI, T, L, COMCAUSE, OI, OD, V]          # CH-901
posicion_wa:                                                         # CH-902
  valores: [verbo, sujeto, complemento, ninguna]
  complemento_admite: [ALL, UNTIL, COM, CAUSE, COMPL.RU, BEN]
  complemento_elegido: mas_cercano_al_verbo
  respaldo: verbo
  fijo: {negativa: jani, ser: predicado, estar: predicado, tener: predicado, pregunta_si_no: ninguno, pregunta_info: ninguno}
top:                                                                 # CH-903
  - sujeto_expreso_si_no_lleva_wa_ni_es_coordinado_ni_interrogativo
  - si_no_hay_sujeto_expreso: adverbio_de_tiempo
q_yn_en: [verbo, predicado]                                          # CH-904
jani_despues_de: S                                                   # CH-905
interrogativos:                                                      # CH-906
  quien_suj:   {palabra: INT.QUIEN, ids: [Q.INF], reemplaza: S}
  que_od:      {palabra: INT.QUE,   ids: [Q.INF], reemplaza: OD}
  donde_all:   {palabra: INT.DONDE, ids: [ALL, Q.INF], reemplaza: L}
  quien_oi:    {palabra: INT.QUIEN, ids: [COMPL.RU, Q.INF], reemplaza: OI}
  donde_estar: {palabra: INT.DONDE, ids: [LOC, VBLZ.KA, PERS, Q.INF], reemplaza: PREDICADO}
coordinacion: {miembros: 2, sufijo: COM, funciones: [S_3a_persona, OD], prohibida_en: [negativa, pregunta_info], excluye: [COM]}   # CH-907
adv_tiempo_compatibilidad:                                           # CH-917
  pasado: [SIMP, REM.C, REM.L]
  presente: [SIMP]
  futuro: [FUT]
```

---

## 10. Lado español

El español se genera **desde la misma idea**, no traduciendo la oración aymara. Cada idea da una sola oración española. La única variación permitida entre ideas que producen la misma oración ficticia es el género de la 3.ª persona humana (CH-1010).

El rol que programa el español necesita:
- un conjugador verificado (presente, pretérito indefinido, futuro, participio y gerundio de cada verbo de `lexico.csv`, con sus irregulares);
- las formas de `haber`, `estar`, `ser` y `tener`.

### CH-1001 · Tiempo del SIMP [DECISIÓN CHULUPI]

Base: §3.2 (SIMP "se traduce como presente o pasado", L1 p.143).

- Si la idea tiene un adverbio de tiempo `pasado`: **pretérito indefinido** ("fui").
- En otro caso: **presente** ("voy").

Ejemplo:
- B: `Nayaxa jaskhi wirkharu tisqthwa.` / A: `Muqixu jaskhi wirkhallu tisqphyi.` → "Yo fui al pueblo ayer."
- Sin `jaskhi`: "Yo voy al pueblo."

### CH-1002 · REM.C → pretérito perfecto compuesto [DECISIÓN CHULUPI]

Base: §3.2 (L1 p.147: "se traduce con el pretérito perfecto"). L2 traduce `munayätha` como "yo quería" (p.56); no lo seguimos, para que cada tiempo aymara tenga un tiempo español distinto. El "lo vi" no se traduce.

Ejemplo:
- B: `Lisqunakaxa wirkhata pajllapxänawa.` / A: `Lisqusuluxu wirkhaku pajllamtümuyi.` → "Las niñas han venido del pueblo."

### CH-1003 · REM.L → pluscuamperfecto [DECISIÓN CHULUPI]

Base: §3.2 (L1 p.148); §8.2 (L2 p.56: "había querido"). El "no lo vi" no se traduce.

Ejemplo:
- B: `Simllaxa ch'alqulaykuwa pajllatäna.` / A: `Simllaxu ch'alqutiwqayi pajllawümu.` → "La mujer había venido por la deuda."

### CH-1004 · FUT → futuro simple [DECISIÓN CHULUPI]

Base: §3.2; §8.2 (L2 p.55: "yo daré").

Nunca se usa "ir a + infinitivo".

Ejemplo:
- B: `Yaruqhixa wirkharu tisqaniwa.` / A: `Yaruqhixu wirkhallu tisqaphuyi.` → "La maestra irá al pueblo."

### CH-1005 · PROG → "estar" en presente + gerundio [DECISIÓN CHULUPI]

Base: §3.3 (L1 p.111: "estar yendo").

Ejemplo:
- B: `Lisquxa nuspi q'aspi lamch'askiwa.` — niño-TOP ahora pan comer-PROG-3>3.SIMP-AFF.
- A: `Lisquxu nuspi q'aspi lamch'anchuyi.`
- ES: "El niño está comiendo pan ahora."

### CH-1006 · Personas [DECISIÓN CHULUPI]

Base: D12. El español no distingue la 4.ª persona de la 1.ª plural.

| Aymara | Verbo español | Pronombre (si se expresa) |
|---|---|---|
| 1 | 1.ª singular | yo |
| 1 plural (`nänaka`) | 1.ª plural | nosotros |
| 2 | 2.ª singular (tú) | tú |
| 2 plural | 3.ª plural (ustedes) | ustedes |
| 3 | 3.ª singular | él / ella (CH-1010) |
| 3 plural | 3.ª plural | ellos / ellas (CH-1010) |
| 4 y 4 plural | 1.ª plural | nosotros |

"Nosotros" va siempre en masculino.

Ejemplo:
- B: `Q'aspi lamch'añäniwa.` / A: `Q'aspi lamch'athäqiyi.` → "Comeremos pan." (4.ª persona, sin pronombre).

### CH-1007 · Pronombre sujeto [DECISIÓN CHULUPI]

- El español lleva pronombre sujeto **si y solo si** la oración aymara lo lleva.
- Los demostrativos sujeto de "ser" se traducen como demostrativos ("esta es…", CH-1008).

Ejemplo:
- B: `Jumanakaxa pajllapxtawa.` / A: `Tilusuluxu pajllamtkuyi.` → "Ustedes vienen."
- Sin `jumanaka` (no permitido en v1 si es plural y negativa; sí en afirmativa): "Vienen."

### CH-1008 · Artículos y determinantes [DECISIÓN CHULUPI]

Base: §6 (el aymara no tiene artículos). Regla fija, por orden de prioridad:

1. Con demostrativo: "este / ese / aquel" (+ femenino o plural), sin artículo.
2. Con numeral: el numeral, sin artículo.
3. Con posesivo y sin poseedor: "mi, tu, su, nuestro…".
4. Con poseedor: artículo definido + nombre + "de" + poseedor ("la casa del maestro").
5. Predicado de "ser":
   - nombre no humano: "un / una" si es contable y singular; nada si es plural o no contable ("es una casa", "son casas", "eso es pan");
   - nombre humano: sin artículo ("eres maestra").
6. Lo poseído en "tener": "un / una" si es contable y singular; nada si es plural o no contable ("tengo una casa", "tengo casas", "tengo pan").
7. Objeto directo no contable, sin otro determinante: sin artículo ("come pan").
8. Todo lo demás (sujeto, OD contable, complementos): artículo definido. Se contraen "a el" → "al" y "de el" → "del".

El adjetivo va **después** del nombre y concuerda en género y número.

Ejemplos:
- B: `Pultiyajaxa q'ulli jitquniwa.` / A: `Pultiyaluxu q'ulli jitquphuyi.` → "Mi hermana tiene un cuchillo rojo." (reglas 3 y 6).
- B: `Aka-xa chimula-wa.` / A: `Ilmixu chimulayi.` → "Esta es una casa." (regla 5; el demostrativo concuerda con el nombre predicado).

### CH-1009 · Clíticos y tratamiento [DECISIÓN CHULUPI]

- COMPL.RU de 3.ª persona → "le" (singular) o "les" (plural) delante del verbo, más "a + frase" ("le doy pan al niño").
- Transiciones → "me / te / nos" delante del verbo: 1>2 te, 2>1 me, 3>1 me, 3>2 te, 3>4 nos.
- El pronombre aymara con `-ru` en una transición (`nayaru`) **no** añade "a mí": el clítico ya lo dice. Así, la versión con pronombre y la versión sin él dan el mismo español.
- 2.ª persona singular = "tú"; plural = "ustedes" (español de Bolivia). No se usa "usted" ni "vosotros".
- Con `quien_oi`: "¿A quién le…?".

Ejemplo:
- B: `Jupaxa nayaru q'aspi tulphituwa.` / A: `Kaxixu muqillu q'aspi tulphuquyi.` → "Él me da pan."
- Sin `nayaru`, el español es igual.

### CH-1010 · Género de la 3.ª persona humana [DECISIÓN CHULUPI]

Base: decisión del equipo (ajuste 2); D12 (ni las personas ni los pronombres aymaras marcan género).

- El campo `genero` (`m` / `f`) de cada referente humano de 3.ª persona decide:
  - el pronombre (él / ella, ellos / ellas);
  - la forma del nombre `var` (niño / niña);
  - el artículo y la concordancia del adjetivo.
- Nombres de género fijo (`mujer`): el campo se ignora.
- Plural mixto: `m`.

Dos ideas que solo difieren en `genero` dan la misma oración ficticia y dos españolas. El control de calidad lo acepta (CH-1013).

Ejemplo:
- B: `Jupaxa nuyk'iwa.` / A: `Kaxixu nuyk'uyi.` → "Él duerme." (`m`) / "Ella duerme." (`f`).

### CH-1011 · Orden de la oración española [DECISIÓN CHULUPI]

- **Afirmativa y negativa:** Sujeto – (no) – clíticos + verbo – OD – OI ("a…", "para…") – lugar – COM / CAUSE ("con…", "por…") – tiempo.
- **Pregunta sí/no:** el mismo orden, entre `¿…?`, sin inversión.
- **Pregunta de información:** interrogativo – (clíticos) + verbo – sujeto – resto. Los interrogativos son: "Quién", "Qué", "A dónde", "A quién", "Dónde".
- **Ser / estar / tener:** sujeto – verbo – predicado.
- **Coordinación:** "X y Y".

Ejemplos:
- B: `Simllaxa jaskhi pinqarana lisquru q'aspi tulphiwa.` / A: `Simllaxu jaskhi pinqaramu lisqullu q'aspi tulphuyi.` → "La mujer le dio pan al niño en el mercado ayer."
- B: `¿Kirpuxa kunasa lamch'i?` / A: `¿Kirpuxu mulukhu lamch'u?` → "¿Qué come el perro?"

### CH-1012 · Forma escrita del español

- Mayúscula inicial y punto final, o `¿…?`.
- Tildes correctas.
- Sin dobles espacios.
- Los numerales v1 se escriben en letras: tres, cuatro, seis, diez.

Ejemplo:
- B: `Nayaxa kimsa kirpunithwa.` / A: `Muqixu musqi kirpuphuphyi.` → "Yo tengo tres perros."

### CH-1013 · Una traducción por oración ficticia

- Para cada idea, el español es una función determinista de la idea.
- Agrupando todos los pares por oración ficticia (B o A), las traducciones españolas de un mismo grupo solo pueden diferir en palabras de género:
  - artículo, pronombre, forma `m` / `f` del nombre, adjetivo concordado.
- Si difieren en cualquier otra cosa, hay un error en la generación (CH-1301).

Ejemplo:
- El grupo `Kaxixu nuyk'uyi.` contiene "Él duerme." y "Ella duerme.": aceptado.
- Si contuviera "Él dormía.": error.

---

## 11. Esquema de la idea

Una **idea** es un objeto JSON. El generador de ideas lo produce, aplicando CH-406 y las restricciones de esta sección. El constructor la convierte en B, A y español.

### CH-1101 · Campos

```json
{
  "id": "I000001",
  "predicado": "verbo",
  "modalidad": "afirmativa",
  "tiempo": "SIMP",
  "aspecto": "simple",
  "verbo": "L0018",
  "sujeto": {
    "persona": 3,
    "plural": false,
    "expreso": "nombre",
    "np": {"n": "L0004", "genero": null, "plural": false, "dem": null, "num": null, "adj": null, "poss": null, "poseedor": null},
    "coord": null,
    "dem": null,
    "genero": "f"
  },
  "objeto_persona": 3,
  "oi_pronombre_expreso": false,
  "od": {"n": "L0006", "plural": false, "dem": null, "num": null, "adj": null, "poss": null, "poseedor": null},
  "od_coord": null,
  "oi": {"funcion": "COMPL.RU", "np": {"n": "L0001", "genero": "m"}},
  "lugar": {"caso": "LOC", "np": {"n": "L0009"}, "deictico": null},
  "comcausa": null,
  "adv_t": "L0023",
  "interrogativo": null,
  "pnom": null,
  "posicion_wa": "verbo"
}
```

Esta idea da:
- B: `Simllaxa jaskhi pinqarana lisquru q'aspi tulphiwa.`
- A: `Simllaxu jaskhi pinqaramu lisqullu q'aspi tulphuyi.`
- ES: "La mujer le dio pan al niño en el mercado ayer."

### CH-1102 · Valores permitidos

```yaml
# idea.schema.yaml
predicado: [verbo, ser, estar, tener]
modalidad: [afirmativa, negativa, pregunta_si_no, pregunta_info]
tiempo: [SIMP, FUT, REM.C, REM.L]
aspecto: [simple, progresivo]
verbo: "id de lexico.csv con cat V_* (solo si predicado = verbo)"
sujeto:
  persona: [1, 2, 3, 4]
  plural: bool
  expreso: [pronombre, nombre, ninguno, coordinado, demostrativo]
  np: NP            # si expreso = nombre
  coord: [NP, NP]   # si expreso = coordinado
  dem: [DEM.1, DEM.2, DEM.3]   # si expreso = demostrativo
  genero: [m, f, null]         # obligatorio si es 3.ª persona humana (pronombre, o nombre var)
objeto_persona: [1, 2, 3, 4]
oi_pronombre_expreso: bool
od: NP | null
od_coord: [NP, NP] | null
oi: {funcion: [COMPL.RU, BEN], np: NP} | null
lugar: {caso: [ALL, ABL, LOC, UNTIL], np: NP | null, deictico: [DEM.1, DEM.2, DEM.3, null]} | null
comcausa: {caso: [COM, CAUSE], np: NP} | null
adv_t: "id ADV_T" | null
interrogativo: [quien_suj, que_od, donde_all, quien_oi, donde_estar, null]
pnom:                                   # solo si predicado != verbo
  ser:   {adj: "id ADJ"} | {np: NP}
  estar: {np: NP} | {deictico: DEM.x}
  tener: {np: NP}
posicion_wa: [verbo, sujeto, complemento, ninguna]
NP:
  n: "id N_*"
  genero: [m, f, null]                  # obligatorio si n es N_HUM con genero = var
  plural: bool
  dem: [DEM.1, DEM.2, DEM.3, null]
  num: [NUM.3, NUM.4, NUM.6, NUM.10, null]
  adj: "id ADJ" | null
  poss: [1, 2, 3, 4, null]
  poseedor: NP | null                   # N_HUM, sin modificadores
```

### CH-1103 · Restricciones de combinación

El generador las cumple y el validador (CH-1301) las vuelve a comprobar.

| # | Restricción | Regla |
|---|---|---|
| R1 | `objeto_persona ≠ 3` ⇒ `tiempo = SIMP` y `verbo.obj_persona = s` | CH-604 |
| R2 | Transiciones válidas: 1>2, 2>1, 3>1, 3>2, 3>4. Nunca sujeto 4 con objeto 4, ni sujeto = objeto | §3.1 |
| R3 | `modalidad = negativa` ⇒ `tiempo ∈ {SIMP, FUT}`, `aspecto = simple` | CH-605, CH-606 |
| R4 | `aspecto = progresivo` ⇒ `tiempo = SIMP` | CH-606 |
| R5 | `oi.funcion = COMPL.RU` ⇒ `verbo.rige_ru = s` y `oi.np` es `N_HUM` (o pronombre de la transición) | CH-909 |
| R6 | `oi` es uno solo: COMPL.RU **o** BEN | CH-910 |
| R7 | `od.n` ∈ `obj_clases` del verbo y nunca `N_HUM` | CH-406, CH-914 |
| R8 | `V_TR` / `V_DITR` con `objeto_persona = 3` ⇒ `od` (o `que_od`) obligatorio; `V_TR` con objeto 1/2/4 ⇒ `od = null` | CH-915 |
| R9 | `lugar.caso ∈ {ALL, ABL, UNTIL}` ⇒ `V_MOV`; `LOC` ⇒ el verbo no tiene `loc_clases = NINGUNA` | CH-401, CH-406 |
| R10 | `UNTIL` ⇒ raíz de 2 sílabas, `np` sin plural ni posesivo | CH-514 |
| R11 | `sujeto.plural` ⇒ marcas de CH-913 (sujeto expreso obligatorio en negativas y predicados nominales; numeral o coordinación prohibidos en negativas) | CH-913 |
| R12 | `num` ≠ null ⇒ `plural = false` en el NP (el numeral ya es plural) | §13 #11 |
| R13 | Sin numerales 1 o 2; sin `khaya` | CH-518 |
| R14 | `adv_t` compatible con `tiempo` | CH-917 |
| R15 | `predicado ≠ verbo` ⇒ `tiempo = SIMP`, `modalidad ∈ {afirmativa, pregunta_si_no}`, o `pregunta_info` con `donde_estar` | CH-908 |
| R16 | `ser` + nombre ⇒ sujeto demostrativo, o sujeto y nombre `persona`; `ser` 1/2/4 + nombre ⇒ nombre `persona`; demostrativo sujeto ⇒ predicado nombre | CH-908 |
| R17 | `interrogativo` ⇒ `modalidad = pregunta_info`, y sus condiciones de CH-906; `quien_suj` ⇒ sujeto singular | CH-906, CH-913 |
| R18 | `coord` / `od_coord` ⇒ no negativa, no pregunta_info, `comcausa.caso ≠ COM` | CH-907 |
| R19 | `genero` obligatorio en todo referente humano de 3.ª persona cuyo español dependa del género | CH-1010 |
| R20 | Todas las palabras compatibles según CH-406 | CH-406 |
| R21 | Un mismo lexema no aparece dos veces en la idea (evita "para los niños con el niño") | v1.1.1 |
| R22 | Solo entradas `L…` del léxico de producción; nunca las del léxico de validación `LV01`–`LV18` | §12.1 |

Ejemplo de rechazo:
- Idea con `tiempo = FUT`, `objeto_persona = 1`: R1 falla y se descarta.
- La versión válida en SIMP: B `Kirpuxa ch'ixrituwa.` / A `Kirpuxu ch'ixruquyi.` / ES "El perro me ve."

### CH-1104 a CH-1113 · Pesos [DECISIÓN CHULUPI]

Base: decisión del equipo (ajuste 3). Los pesos buscan:
- datos equilibrados entre tipos de oración, personas y tiempos;
- más peso a lo frecuente en aymara (3.ª persona; §13 #13: remotos de 1.ª/2.ª poco frecuentes);
- y que las reglas [DERIVADA] no dominen el corpus.

**Muestreo estratificado (CH-1104).**
1. Se fijan cuotas para cada combinación de `predicado × modalidad × tiempo × persona del sujeto`. La cuota es el producto de los pesos marginales × el total de ideas.
2. El generador produce ideas hasta llenar cada cuota.
3. Las combinaciones imposibles (R1–R20) se quitan y su cuota se reparte proporcionalmente entre las demás.
4. El resto de los campos se sortea con sus pesos, dentro de cada idea.

```yaml
# pesos.yaml — CH-1104 a CH-1113
predicado_modalidad:          # CH-1105 (suma 1)
  verbo.afirmativa: 0.42
  verbo.negativa: 0.14
  verbo.pregunta_si_no: 0.10
  verbo.pregunta_info: 0.09
  ser.afirmativa: 0.06
  ser.pregunta_si_no: 0.02
  estar.afirmativa: 0.05
  estar.pregunta_si_no: 0.015
  estar.pregunta_info: 0.015
  tener.afirmativa: 0.07
  tener.pregunta_si_no: 0.02
categoria_verbo: {V_INTR: 0.20, V_MOV: 0.25, V_TR: 0.40, V_DITR: 0.15}   # P-11: se sortea la categoría y luego Zipf dentro (CH-403)
tiempo:                       # CH-1106 (solo verbales)
  general:  {SIMP: 0.40, FUT: 0.25, REM.C: 0.15, REM.L: 0.20}
  negativa: {SIMP: 0.60, FUT: 0.40}
aspecto:                      # CH-1107
  progresivo_si_SIMP_y_no_negativa: 0.15
persona_sujeto:               # CH-1108
  general: {1: 0.22, 2: 0.22, 3: 0.40, 4: 0.16}
  REM.C:   {1: 0.15, 2: 0.10, 3: 0.60, 4: 0.15}
  REM.L:   {1: 0.10, 2: 0.10, 3: 0.70, 4: 0.10}
transicion:                   # CH-1109 (SIMP, verbo con obj_persona = s)
  objeto_3: 0.65
  T12: 0.07
  T21: 0.07
  T31: 0.07
  T32: 0.07
  T34: 0.07              # se elige primero la transición; fija la persona del sujeto
sujeto:                       # CH-1110
  plural: 0.30
  expreso_1_2_4: {pronombre: 0.50, ninguno: 0.50}
  expreso_3:     {nombre: 0.60, pronombre: 0.20, ninguno: 0.15, coordinado: 0.05}
  genero: {m: 0.50, f: 0.50}
complementos:                 # CH-1111
  cuantos_opcionales: {0: 0.30, 1: 0.45, 2: 0.20, 3: 0.05}
  tipo: {tiempo: 0.30, lugar: 0.35, comcausa: 0.20, oi: 0.15}
  lugar_V_MOV: {ALL: 0.55, ABL: 0.30, UNTIL: 0.15}
  lugar_LOC: {np: 0.75, deictico: 0.25}
  comcausa: {COM: 0.70, CAUSE: 0.30}
  oi_V_DITR: {COMPL.RU: 0.70, BEN: 0.30}
  oi_V_TR: {BEN: 1.00}           # BEN solo con V_TR y V_DITR (CH-406, v1.1.1)
  oi_pronombre_expreso: 0.40     # en transiciones con V_DITR
  od_coord: 0.05
np:                           # CH-1112
  modificador: {ninguno: 0.55, adj: 0.20, dem: 0.08, num: 0.07, poss: 0.07, poseedor: 0.03}
  plural_no_sujeto: 0.25         # si el nombre es contable y no hay numeral
  num: {NUM.3: 0.35, NUM.4: 0.30, NUM.6: 0.20, NUM.10: 0.15}
  dem: {DEM.1: 0.40, DEM.2: 0.40, DEM.3: 0.20}
  poss: {1: 0.30, 2: 0.25, 3: 0.30, 4: 0.15}
posicion_wa: {verbo: 0.50, ninguna: 0.20, sujeto: 0.15, complemento: 0.15}   # CH-1113
interrogativo:                # CH-1113
  verbo: {quien_suj: 0.35, que_od: 0.30, donde_all: 0.20, quien_oi: 0.15}
ser:
  pnom: {adj: 0.60, np: 0.40}
  sujeto_con_np: {demostrativo: 0.60, humano: 0.40}
```

Notas:
- Si un valor sorteado no es posible para la idea (por ejemplo, `donde_all` con un verbo que no es `V_MOV`), se vuelve a sortear entre los valores posibles, renormalizando.
- Tras generar todo, se aplica la cobertura del léxico (CH-404).

Ejemplo (una idea sorteada):
- Sorteos: `verbo.afirmativa`, `REM.L`, persona 3, `expreso_3 = nombre`, 1 complemento (`comcausa = CAUSE`), `posicion_wa = complemento`.
- Resultado: B `Simllaxa ch'alqulaykuwa pajllatäna.` / A `Simllaxu ch'alqutiwqayi pajllawümu.` / ES "La mujer había venido por la deuda."

---

## 12. Casos de prueba

### 12.1 Léxico de validación

Los casos marcados [ATESTIGUADO] usan **raíces reales** para que el modo B reproduzca exactamente una oración de la guía.
- Las raíces reales viven en un léxico aparte (ids `LV01`–`LV18`).
- Solo se usa en pruebas, **nunca** para generar datos de entrenamiento.
- No pasa por los filtros CH-306 a CH-310.
- Un mismo verbo real puede tener dos sentidos: `manq'a` intransitivo (C05, C06) y transitivo (C07).

| Id | Raíz | Cat. | Clase | Español |
|---|---|---|---|---|
| LV01 | `wawa` | N_HUM | persona | niño / niña |
| LV02 | `t'ant'a` | N_NOHUM | comida | pan (no contable) |
| LV03 | `chura` | V_DITR | — | dar |
| LV04 | `tata` | N_HUM | persona | padre |
| LV05 | `marka` | N_NOHUM | lugar | pueblo |
| LV06 | `juta` | V_MOV | — | venir |
| LV07 | `sara` | V_MOV | — | ir |
| LV08 | `manq'a` | V_INTR | — | comer (sin objeto) |
| LV09 | `manq'a` | V_TR | — | comer |
| LV10 | `anu` | N_NOHUM | animal | perro |
| LV11 | `uta` | N_NOHUM | vivienda | casa |
| LV12 | `jila` | N_HUM | persona | hermano / hermana |
| LV13 | `jilaqata` | N_HUM | persona | autoridad (f) |
| LV14 | `mama` | N_HUM | persona | mamá |
| LV15 | `tiwula` | N_NOHUM | animal | zorro |
| LV16 | `wallata` | N_NOHUM | animal | ganso |
| LV17 | `jikisi` | V_INTR | — | encontrarse |
| LV18 | `muna` | V_TR | — | querer |

### 12.2 Convenciones

- Las ideas van en el esquema de CH-1102. Para abreviar se omiten los campos nulos o falsos. Valores por defecto: `aspecto = simple`, `objeto_persona = 3`, `oi_pronombre_expreso = false`.
- `oi` puede ir sin `np` en dos casos: cuando el destinatario es el pronombre de la transición (`oi_pronombre_expreso = true`) o cuando lo reemplaza `quien_oi`.
- **Estado:**
  - **[ATESTIGUADO]:** B es idéntica a la forma de la guía (con su página).
  - **[DERIVADA] DV-xx:** la oración usa esas reglas derivadas.
  - **Patrón atestiguado:** todas las palabras siguen un patrón con forma atestiguada.
- **Español de los [ATESTIGUADO].** Sigue las reglas de §10, no la traducción de L2. Por ejemplo, el SIMP sin adverbio va en presente (CH-1001) aunque L2 traduzca en pasado. La traducción de L2 se da solo como referencia.
- Los 40 casos, con sus ids por palabra, están en `casos_prueba.json`. `test_chulupi.py` los comprueba (Anexo B).

### 12.3 Cobertura

| Qué | Casos |
|---|---|
| Persona 1 / 1 plural | C01, C04, C13, C17, C18, C30 / C23 |
| Persona 2 / 2 plural | C05, C19, C24, C27, C32, C33, C39 / C29 |
| Persona 3 / 3 plural | C02, C03, C07–C10, C14, C16, C20–C22, C26, C31, C34, C37, C38 / C11, C12, C26, C36, C40 |
| Persona 4 / 4 plural | C06, C15, C28 / C25, C35 |
| Transiciones 1>2, 2>1, 3>1, 3>2, 3>4 | C18, C19, C20, C21, C22 |
| SIMP / FUT / REM.C / REM.L | C01… / C03, C09, C10, C14, C15, C17, C27, C28, C31 / C23, C26, C32 / C24, C25 |
| Progresivo | C30 |
| ALL / COMPL.RU / ABL / LOC | C03, C08, C25, C31 / C01, C02, C20 / C23 / C29, C30 (deíctico) |
| GEN / COM / BEN / UNTIL / CAUSE | C27 / C28 (instrumento), C11 y C24 (coordinación) / C26 / C16 / C25 |
| POSS.1 / .2 / .3 / .4 | C14 / C02, C10 / C27 / C38 |
| Declarativa / negativa / sí-no | casi todas / C09, C22, C28, C29 / C10, C19, C38, C39 |
| Pregunta de información (5 tipos) | C15 (donde_all), C31 (quien_suj), C32 (que_od), C33 (quien_oi), C34 (donde_estar) |
| Ser (adjetivo / demostrativo + nombre / humano) | C35 / C36 / C37 |
| Estar / tener | C34, C38 / C39, C40 |
| Coordinación (sujeto / OD) | C11 / C24 |
| `posicion_wa` verbo / sujeto / complemento / ninguna | C04… / C11, C14 / C08, C16, C25 / C01, C02, C03, C07, C12, C13, C17, C24, C27 |
| `-xa` en adverbio sin sujeto | C21 |
| Adverbio pasado / presente / futuro | C21 / C30 / C27 |
| Demostrativo / numeral / adjetivo modificador | C20 / C40 / C39 |

### 12.4 Los 40 casos

**C01** — SIMP 1>3 · V_DITR · COMPL.RU · OD · pronombre 1 · posicion_wa=ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV03", "sujeto": {"persona": 1, "expreso": "pronombre"}, "oi": {"funcion": "COMPL.RU", "np": {"n": "LV01", "genero": "m"}}, "od": {"n": "LV02"}, "posicion_wa": "ninguna"}`
- B: `Nayaxa wawaru t'ant'a churtha.`
- A: `Muqixu wawallu t'ant'a churphi.`
- ES: "Yo le doy pan al niño."
- Estado: [ATESTIGUADO] L2 p.155 (10.1 #1) — traducción de L2: "Yo le di pan al niño"

**C02** — SIMP 3>3 · sujeto omitido · COMPL.RU + POSS.2 · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV03", "sujeto": {"persona": 3, "expreso": "ninguno", "genero": "m"}, "oi": {"funcion": "COMPL.RU", "np": {"n": "LV04", "poss": 2}}, "od": {"n": "LV02"}, "posicion_wa": "ninguna"}`
- B: `Tatamaru t'ant'a churi.`
- A: `Tataqillu t'ant'a churu.`
- ES: "Le da pan a tu padre."
- Estado: [ATESTIGUADO] L2 p.155 (10.1 #2) — traducción de L2: "Le dio pan a tu padre"

**C03** — FUT 3 · V_MOV · ALL · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "FUT", "verbo": "LV06", "sujeto": {"persona": 3, "expreso": "ninguno", "genero": "m"}, "lugar": {"caso": "ALL", "np": {"n": "LV05"}}, "posicion_wa": "ninguna"}`
- B: `Markaru jutani.`
- A: `Markallu jutaphu.`
- ES: "Vendrá al pueblo."
- Estado: [ATESTIGUADO] L2 p.156 (10.1 #3) — traducción de L2: "Vendrá al pueblo"

**C04** — SIMP 1 · AFF en verbo

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV07", "sujeto": {"persona": 1, "expreso": "pronombre"}, "posicion_wa": "verbo"}`
- B: `Nayaxa sarthwa.`
- A: `Muqixu sarphyi.`
- ES: "Yo voy."
- Estado: [ATESTIGUADO] L2 p.176 (10.1 #4) — traducción de L2: "Yo voy/fui"

**C05** — SIMP 2 · AFF en verbo

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV08", "sujeto": {"persona": 2, "expreso": "pronombre"}, "posicion_wa": "verbo"}`
- B: `Jumaxa manq'tawa.`
- A: `Tiluxu manq'kuyi.`
- ES: "Tú comes."
- Estado: [ATESTIGUADO] L2 p.177 (10.1 #5) — traducción de L2: "Tú comes/comiste"

**C06** — SIMP 4 · AFF en verbo

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV08", "sujeto": {"persona": 4, "expreso": "pronombre"}, "posicion_wa": "verbo"}`
- B: `Jiwasaxa manq'tanwa.`
- A: `Wiqutuxu manq'kilyi.`
- ES: "Nosotros comemos."
- Estado: [ATESTIGUADO] L2 p.178 (10.1 #6) — traducción de L2: "Nosotros comemos/comimos"

**C07** — SIMP 3 · OD · sujeto nombre · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV09", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "LV10"}}, "od": {"n": "LV02"}, "posicion_wa": "ninguna"}`
- B: `Anuxa t'ant'a manq'i.`
- A: `Anuxu t'ant'a manq'u.`
- ES: "El perro come pan."
- Estado: [ATESTIGUADO] L2 p.243 (10.1 #10) — traducción de L2: "El perro come pan"

**C08** — SIMP 3 · ALL · posicion_wa=complemento

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV07", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "LV04"}}, "lugar": {"caso": "ALL", "np": {"n": "LV11"}}, "posicion_wa": "complemento"}`
- B: `Tataxa utaruwa sari.`
- A: `Tataxu utalluyi saru.`
- ES: "El padre va a la casa."
- Estado: [ATESTIGUADO] L2 p.68 (10.1 #12) — traducción de L2: "El padre/señor fue/va a la casa"

**C09** — Negativa FUT 3

- Idea: `{"predicado": "verbo", "modalidad": "negativa", "tiempo": "FUT", "verbo": "LV06", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "LV13"}}}`
- B: `Jilaqataxa janiwa jutkaniti.`
- A: `Jilaqataxu yuliyi jutñuphuji.`
- ES: "La autoridad no vendrá."
- Estado: [ATESTIGUADO] L2 p.231 (10.1 #15) — traducción de L2: "La autoridad no vendrá"

**C10** — Pregunta sí/no FUT 3 · POSS.2

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_si_no", "tiempo": "FUT", "verbo": "LV06", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "LV12", "poss": 2, "genero": "m"}}}`
- B: `¿Jilamaxa jutaniti?`
- A: `¿Jilaqixu jutaphuji?`
- ES: "¿Tu hermano vendrá?"
- Estado: [ATESTIGUADO] L2 p.235 (10.1 #16) — traducción de L2: "¿Vendrá tu hermano?"

**C11** — Coordinación de sujeto · PL.V · posicion_wa=sujeto

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV17", "sujeto": {"persona": 3, "plural": true, "expreso": "coordinado", "coord": [{"n": "LV15"}, {"n": "LV16"}]}, "posicion_wa": "sujeto"}`
- B: `Tiwulampi wallatampiwa jikisipxi.`
- A: `Tiwulanku wallatankuyi jikisimtu.`
- ES: "El zorro y el ganso se encuentran."
- Estado: [ATESTIGUADO] L2 p.160 (10.1 #19) — traducción de L2: "El zorro y el ganso se encuentran"

**C12** — Plural 3 (pronombre + PL.V) · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV07", "sujeto": {"persona": 3, "plural": true, "expreso": "pronombre", "genero": "m"}, "posicion_wa": "ninguna"}`
- B: `Jupanakaxa sarapxi.`
- A: `Kaxisuluxu saramtu.`
- ES: "Ellos van."
- Estado: [ATESTIGUADO] L2 p.184 (10.1 #20) — traducción de L2: "Ellos/ellas van/fueron"

**C13** — SIMP 1 · sujeto omitido · OD · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV18", "sujeto": {"persona": 1, "expreso": "ninguno"}, "od": {"n": "LV02"}, "posicion_wa": "ninguna"}`
- B: `T'ant'a muntha.`
- A: `T'ant'a munphi.`
- ES: "Quiero pan."
- Estado: [ATESTIGUADO] L2 p.67 (10.1 #22) — traducción de L2: "Quiero pan"

**C14** — FUT 3 · POSS.1 · posicion_wa=sujeto

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "FUT", "verbo": "LV06", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "LV14", "poss": 1}}, "posicion_wa": "sujeto"}`
- B: `Mamajawa jutani.`
- A: `Mamaluyi jutaphu.`
- ES: "Mi mamá vendrá."
- Estado: [ATESTIGUADO] L2 p.230 (§4.1) — traducción de L2: "Mi mamá vendrá"

**C15** — Pregunta de información (donde_all) · FUT 4

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_info", "tiempo": "FUT", "verbo": "LV07", "sujeto": {"persona": 4, "expreso": "ninguno"}, "interrogativo": "donde_all", "lugar": {"caso": "ALL"}}`
- B: `¿Kawkirusa sarañäni?`
- A: `¿Yaqullukhu sarathäqi?`
- ES: "¿A dónde iremos?"
- Estado: [ATESTIGUADO] L2 p.236 (§4.1) — traducción de L2: "¿A dónde iremos?"

**C16** — UNTIL · posicion_wa=complemento

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "LV07", "sujeto": {"persona": 3, "expreso": "ninguno", "genero": "m"}, "lugar": {"caso": "UNTIL", "np": {"n": "LV05"}}, "posicion_wa": "complemento"}`
- B: `Markakamawa sari.`
- A: `Markachiwiyi saru.`
- ES: "Va hasta el pueblo."
- Estado: [ATESTIGUADO] L2 p.160 (§2.1) — traducción de L2: "Fue hasta el pueblo"

**C17** — FUT 1 · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "FUT", "verbo": "LV07", "sujeto": {"persona": 1, "expreso": "pronombre"}, "posicion_wa": "ninguna"}`
- B: `Nayaxa sarä.`
- A: `Muqixu sarä.`
- ES: "Yo iré."
- Estado: [ATESTIGUADO] L2 p.55 (§8.2) — traducción de L2: "Yo iré"

**C18** — Transición 1>2

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "L0017", "sujeto": {"persona": 1, "expreso": "pronombre"}, "objeto_persona": 2, "posicion_wa": "verbo"}`
- B: `Nayaxa ch'ixrsmawa.`
- A: `Muqixu ch'ixrjmiyi.`
- ES: "Yo te veo."
- Estado: [DERIVADA] DV-02

**C19** — Transición 2>1 · pregunta sí/no

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_si_no", "tiempo": "SIMP", "verbo": "L0017", "sujeto": {"persona": 2, "expreso": "pronombre"}, "objeto_persona": 1}`
- B: `¿Jumaxa ch'ixristati?`
- A: `¿Tiluxu ch'ixrulqaji?`
- ES: "¿Tú me ves?"
- Estado: [DERIVADA] DV-02

**C20** — Transición 3>1 · V_DITR · pronombre con COMPL.RU · demostrativo

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "L0018", "sujeto": {"persona": 3, "expreso": "pronombre", "genero": "m"}, "objeto_persona": 1, "oi_pronombre_expreso": true, "oi": {"funcion": "COMPL.RU"}, "od": {"n": "L0006", "dem": "DEM.1"}, "posicion_wa": "verbo"}`
- B: `Jupaxa nayaru aka q'aspi tulphituwa.`
- A: `Kaxixu muqillu ilmi q'aspi tulphuquyi.`
- ES: "Él me da este pan."
- Estado: [DERIVADA] DV-02

**C21** — Transición 3>2 · adverbio pasado con TOP (sin sujeto) · SIMP → pretérito

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "verbo": "L0017", "sujeto": {"persona": 3, "expreso": "ninguno", "genero": "f"}, "objeto_persona": 2, "adv_t": "L0023", "posicion_wa": "verbo"}`
- B: `Jaskhixa ch'ixrtamwa.`
- A: `Jaskhixu ch'ixrkiqyi.`
- ES: "Te vio ayer."
- Estado: [DERIVADA] DV-01

**C22** — Transición 3>4 · negativa SIMP

- Idea: `{"predicado": "verbo", "modalidad": "negativa", "tiempo": "SIMP", "verbo": "L0017", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "L0008"}}, "objeto_persona": 4}`
- B: `Kirpuxa janiwa ch'ixrkistuti.`
- A: `Kirpuxu yuliyi ch'ixrñulquji.`
- ES: "El perro no nos ve."
- Estado: [DERIVADA] DV-02, DV-08

**C23** — REM.C 1 plural (nänaka + PL.V) · ABL

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "REM.C", "verbo": "L0014", "sujeto": {"persona": 1, "plural": true, "expreso": "pronombre"}, "lugar": {"caso": "ABL", "np": {"n": "L0009"}}, "posicion_wa": "verbo"}`
- B: `Nänakaxa pinqarata pajllapxayäthwa.`
- A: `Müsuluxu pinqaraku pajllamtujüphyi.`
- ES: "Nosotros hemos venido del mercado."
- Estado: [DERIVADA] DV-05

**C24** — REM.L 2 · coordinación de OD · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "REM.L", "verbo": "L0017", "sujeto": {"persona": 2, "expreso": "pronombre"}, "od_coord": [{"n": "L0008"}, {"n": "L0011"}], "posicion_wa": "ninguna"}`
- B: `Jumaxa kirpumpi jitqumpi ch'ixratäta.`
- A: `Tiluxu kirpunku jitqunku ch'ixrawüku.`
- ES: "Tú habías visto el perro y el cuchillo."
- Estado: patrón atestiguado

**C25** — REM.L 4 plural · ALL + CAUSE · posicion_wa=complemento

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "REM.L", "verbo": "L0013", "sujeto": {"persona": 4, "plural": true, "expreso": "pronombre"}, "lugar": {"caso": "ALL", "np": {"n": "L0007"}}, "comcausa": {"caso": "CAUSE", "np": {"n": "L0012"}}, "posicion_wa": "complemento"}`
- B: `Jiwasanakaxa wirkharu ch'alqulaykuwa tisqapxatätana.`
- A: `Wiqutusuluxu wirkhallu ch'alqutiwqayi tisqamtuwükilu.`
- ES: "Nosotros habíamos ido al pueblo por la deuda."
- Estado: [DERIVADA] DV-06

**C26** — REM.C 3 plural (nombre + PL.V) · BEN · OD

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "REM.C", "verbo": "L0019", "sujeto": {"persona": 3, "plural": true, "expreso": "nombre", "np": {"n": "L0003", "plural": true, "genero": "m"}}, "oi": {"funcion": "BEN", "np": {"n": "L0001", "genero": "f"}}, "od": {"n": "L0006"}, "posicion_wa": "verbo"}`
- B: `Yaruqhinakaxa lisqutaki q'aspi nirqapxänawa.`
- A: `Yaruqhisuluxu lisqupuli q'aspi nirqamtümuyi.`
- ES: "Los maestros han comprado pan para la niña."
- Estado: [DERIVADA] DV-05

**C27** — FUT 2 · GEN (poseedor) + POSS.3 · adverbio futuro · ninguna

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "FUT", "verbo": "L0017", "sujeto": {"persona": 2, "expreso": "pronombre"}, "adv_t": "L0024", "od": {"n": "L0005", "poseedor": {"n": "L0003", "genero": "m"}}, "posicion_wa": "ninguna"}`
- B: `Jumaxa sik'uyu yaruqhina chimulapa ch'ixräta.`
- A: `Tiluxu sik'uyu yaruqhimu chimulachu ch'ixräku.`
- ES: "Tú verás la casa del maestro mañana."
- Estado: patrón atestiguado

**C28** — Negativa FUT 4 · COM instrumento · OD

- Idea: `{"predicado": "verbo", "modalidad": "negativa", "tiempo": "FUT", "verbo": "L0020", "sujeto": {"persona": 4, "expreso": "pronombre"}, "comcausa": {"caso": "COM", "np": {"n": "L0011"}}, "od": {"n": "L0006"}}`
- B: `Jiwasaxa janiwa jitqumpi q'aspi k'iymkañäniti.`
- A: `Wiqutuxu yuliyi jitqunku q'aspi k'iymñuthäqiji.`
- ES: "Nosotros no cortaremos pan con el cuchillo."
- Estado: [DERIVADA] DV-04, DV-08

**C29** — Negativa SIMP 2 plural · LOC

- Idea: `{"predicado": "verbo", "modalidad": "negativa", "tiempo": "SIMP", "verbo": "L0015", "sujeto": {"persona": 2, "plural": true, "expreso": "pronombre"}, "lugar": {"caso": "LOC", "np": {"n": "L0005"}}}`
- B: `Jumanakaxa janiwa chimulana nuyk'ktati.`
- A: `Tilusuluxu yuliyi chimulamu nuyk'ñkuji.`
- ES: "Ustedes no duermen en la casa."
- Estado: [DERIVADA] DV-03, DV-08

**C30** — Progresivo 1 · adverbio presente · LOC deíctico · OD

- Idea: `{"predicado": "verbo", "modalidad": "afirmativa", "tiempo": "SIMP", "aspecto": "progresivo", "verbo": "L0020", "sujeto": {"persona": 1, "expreso": "pronombre"}, "adv_t": "L0025", "lugar": {"caso": "LOC", "deictico": "DEM.1"}, "od": {"n": "L0006"}, "posicion_wa": "verbo"}`
- B: `Nayaxa nuspi akana q'aspi k'iymaskthwa.`
- A: `Muqixu nuspi ilmimu q'aspi k'iymanchphyi.`
- ES: "Yo estoy cortando pan aquí ahora."
- Estado: [DERIVADA] DV-09

**C31** — Pregunta de información (quien_suj) · FUT · ALL

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_info", "tiempo": "FUT", "verbo": "L0013", "sujeto": {"persona": 3}, "interrogativo": "quien_suj", "lugar": {"caso": "ALL", "np": {"n": "L0009"}}}`
- B: `¿Khitisa pinqararu tisqani?`
- A: `¿Simukhu pinqarallu tisqaphu?`
- ES: "¿Quién irá al mercado?"
- Estado: patrón atestiguado

**C32** — Pregunta de información (que_od) · REM.C 2

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_info", "tiempo": "REM.C", "verbo": "L0019", "sujeto": {"persona": 2, "expreso": "pronombre"}, "interrogativo": "que_od"}`
- B: `¿Jumaxa kunasa nirqayäta?`
- A: `¿Tiluxu mulukhu nirqajüku?`
- ES: "¿Qué has comprado tú?"
- Estado: patrón atestiguado

**C33** — Pregunta de información (quien_oi) · SIMP 2

- Idea: `{"predicado": "verbo", "modalidad": "pregunta_info", "tiempo": "SIMP", "verbo": "L0018", "sujeto": {"persona": 2, "expreso": "ninguno"}, "interrogativo": "quien_oi", "oi": {"funcion": "COMPL.RU"}, "od": {"n": "L0006"}}`
- B: `¿Khitirusa q'aspi tulphta?`
- A: `¿Simullukhu q'aspi tulphku?`
- ES: "¿A quién le das pan?"
- Estado: patrón atestiguado

**C34** — Estar · pregunta de información (donde_estar) · 3

- Idea: `{"predicado": "estar", "modalidad": "pregunta_info", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "L0008"}}, "interrogativo": "donde_estar", "pnom": {}}`
- B: `¿Kirpuxa kawkinkisa?`
- A: `¿Kirpuxu yaqumñukhu?`
- ES: "¿Dónde está el perro?"
- Estado: [DERIVADA] DV-10

**C35** — Ser + adjetivo · 4 plural

- Idea: `{"predicado": "ser", "modalidad": "afirmativa", "sujeto": {"persona": 4, "plural": true, "expreso": "pronombre"}, "pnom": {"adj": "L0021"}}`
- B: `Jiwasanakaxa jumpütanwa.`
- A: `Wiqutusuluxu jumpükilyi.`
- ES: "Nosotros somos grandes."
- Estado: [DERIVADA] DV-12

**C36** — Ser + nombre · demostrativo plural (3)

- Idea: `{"predicado": "ser", "modalidad": "afirmativa", "sujeto": {"persona": 3, "plural": true, "expreso": "demostrativo", "dem": "DEM.2"}, "pnom": {"np": {"n": "L0005"}}}`
- B: `Ukanakaxa chimulanakawa.`
- A: `Ulmisuluxu chimulasuluyi.`
- ES: "Esas son casas."
- Estado: patrón atestiguado

**C37** — Ser + nombre humano (3) · sin artículo

- Idea: `{"predicado": "ser", "modalidad": "afirmativa", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "L0004"}}, "pnom": {"np": {"n": "L0003", "genero": "f"}}}`
- B: `Simllaxa yaruqhiwa.`
- A: `Simllaxu yaruqhiyi.`
- ES: "La mujer es maestra."
- Estado: patrón atestiguado

**C38** — Estar + POSS.4 · pregunta sí/no · 3

- Idea: `{"predicado": "estar", "modalidad": "pregunta_si_no", "sujeto": {"persona": 3, "expreso": "nombre", "np": {"n": "L0008"}}, "pnom": {"np": {"n": "L0005", "poss": 4}}}`
- B: `¿Kirpuxa chimulasankiti?`
- A: `¿Kirpuxu chimulakhumñuji?`
- ES: "¿El perro está en nuestra casa?"
- Estado: [DERIVADA] DV-10, DV-13

**C39** — Tener + adjetivo · pregunta sí/no · 2

- Idea: `{"predicado": "tener", "modalidad": "pregunta_si_no", "sujeto": {"persona": 2, "expreso": "pronombre"}, "pnom": {"np": {"n": "L0005", "adj": "L0021"}}}`
- B: `¿Jumaxa jumpu chimulanitati?`
- A: `¿Tiluxu jumpu chimulaphukuji?`
- ES: "¿Tú tienes una casa grande?"
- Estado: [DERIVADA] DV-11, DV-13

**C40** — Tener + numeral · 3 plural

- Idea: `{"predicado": "tener", "modalidad": "afirmativa", "sujeto": {"persona": 3, "plural": true, "expreso": "nombre", "np": {"n": "L0002", "plural": true, "genero": "m"}}, "pnom": {"np": {"n": "L0008", "num": "NUM.3"}}}`
- B: `Pultiyanakaxa kimsa kirpuniwa.`
- A: `Pultiyasuluxu musqi kirpuphuyi.`
- ES: "Los hermanos tienen tres perros."
- Estado: patrón atestiguado

### CH-1201 · Regla de los casos de prueba

- Antes de cada generación, el constructor debe producir **exactamente** las salidas B, A y ES de los 40 casos.
- Los 17 casos [ATESTIGUADO] deben dar en B la forma de la guía, carácter por carácter.
- Si un caso falla, la generación no se hace.

Ejemplo:
- C11 debe dar B `Tiwulampi wallatampiwa jikisipxi.` (L2 p.160), A `Tiwulanku wallatankuyi jikisimtu.` y ES "El zorro y el ganso se encuentran."

---

## 13. Lista de verificación automática

### CH-1301 · Formato de cada par generado

Cada par se guarda en una línea de un archivo JSONL. Las verificaciones trabajan sobre estos campos, no sobre el texto suelto.

```json
{"id": "P00000001", "version_spec": "1.1", "version_lexico": "1.0", "idea": {"…": "esquema CH-1102"},
 "b": "Nayaxa jaskhi wirkharu tisqthwa.", "a": "Muqixu jaskhi wirkhallu tisqphyi.",
 "es": "Yo fui al pueblo ayer.",
 "palabras_b": [["naya", ["TOP"]], ["jaskhi", []], ["wirkha", ["ALL"]], ["tisqa", ["P1", "AFF"]]],
 "dv": []}
```

### CH-1302 · Verificaciones

Todas las verificaciones se hacen en cada par. Las de la sección H se hacen sobre el conjunto completo.

**Acción:**
- **D:** descartar el par y registrarlo.
- **E:** error del programa; se detiene la generación.
- **A:** aviso en el informe.

| # | Qué se comprueba | Cómo | Regla | Acción | Ejemplo de fallo |
|---|---|---|---|---|---|
| **A. Formato** | | | | | |
| V01 | El par tiene todos los campos de CH-1301 | esquema JSON | CH-1301 | E | falta `palabras_b` |
| V02 | Texto en NFC, apóstrofo U+0027, sin dobles espacios | comparar con `normalizar()` | CH-102, CH-103 | E | `lamch’thwa` (U+2019) |
| V03 | Mayúscula inicial y puntuación según la modalidad | regex `^¿?[A-ZÁÉÍÓÚÄÏÜÑ]` + final `.` / `?` | CH-106, CH-1012 | E | pregunta sin `¿` |
| **B. Ortografía y fonotáctica (B y A)** | | | | | |
| V04 | Solo letras del alfabeto | `segmentar()` sin error | CH-101, CH-104, CH-105 | E | `tishwa` |
| V05 | Cada palabra pasa la regex de clases y no empieza por x/r | `validar_palabra()` | CH-202 a CH-208 | E | `tisqaiwa` |
| V06 | Las raíces cumplen CH-201 a CH-209 y están en `lexico.csv` | buscar raíz | CH-2xx, CH-309 | E | raíz desconocida |
| V07 | Ninguna forma prohibida en B: el carácter `ŋ`; palabras que terminan en `tayna` o contienen `taya` tras un morfema verbal; las palabras completas `maya`, `paya`, `khaya`, `mä`, `pä`, `khä` | lista negra (por id de morfema y por palabra completa) | CH-512, CH-513, CH-518 | E | `tisqatayna` |
| **C. Morfología** | | | | | |
| V08 | La secuencia de ids de cada palabra cumple la plantilla y las restricciones de §6 | regex de `slots.yaml` | CH-601 a CH-606 | E | `PL.V NEG` |
| V09 | Reconstruir cada palabra desde (base, ids) da la misma forma | `construir_palabra()` | CH-701 | E | — |
| V10 | Las pruebas de regresión y los 40 casos pasan (antes de generar) | `test_chulupi.py` | CH-710, CH-1201 | E | `sarapxi` ≠ esperado |
| **D. Modo A** | | | | | |
| V11 | A tiene las mismas palabras, bases e ids que B | comparar `palabras_b` con el análisis de A | CH-501 | E | una palabra de más |
| V12 | A = reconstrucción en modo A de `palabras_b` | `construir_palabra(…, "A")` | CH-501, CH-708 | E | — |
| V13 | Ninguna palabra A contiene una forma B de sufijo o palabra gramatical en su lugar | comparar morfema a morfema | CH-503 | E | `muqixa` |
| **E. Sintaxis** | | | | | |
| V14 | Orden de constituyentes | posiciones de `palabras_b` | CH-901 | E | OD antes del OI |
| V15 | Como máximo un AFF; ninguno en OD, ABL, LOC, adverbio ni deíctico; AFF según `posicion_wa` o la posición fija | contar ids | CH-902 | E | dos `-wa` |
| V16 | TOP solo en el sujeto o, sin sujeto, en el adverbio | ids | CH-903 | E | `-xa` en el verbo |
| V17 | Negativa ⇔ `jani-wa` + NEG + NEG.TI; Q.YN solo en verbo/predicado; un Q.INF y solo en interrogativos | ids | CH-904 a CH-906 | E | NEG sin `jani` |
| V18 | Coordinación de 2 miembros con COM, sin COM aparte | ids | CH-907 | E | — |
| **F. Idea** | | | | | |
| V19 | La idea cumple R1 a R20 | validador de ideas | CH-1103 | D | FUT con objeto 1 |
| V20 | Compatibilidad semántica de todas las palabras | clases de `lexico.csv` | CH-406 | D | "comer el palo" |
| V21 | Plural del sujeto marcado según CH-913 | ids PL / PL.V / `nänaka` | CH-913 | E | sujeto plural sin marca |
| **G. Español** | | | | | |
| V22 | `es` = español reconstruido desde la idea | `oracion_espanol()` | §10 | E | — |
| V23 | Tiempo español según tiempo, aspecto y adverbio | tabla CH-1001 a CH-1005 | CH-1001 a CH-1005 | E | REM.L traducido en pretérito |
| V24 | Pronombre español ⇔ pronombre aymara | comparar | CH-1007 | E | "Yo voy" sin `naya` |
| V25 | Concordancia de género y número (artículo, nombre, adjetivo, pronombre) | con `genero` y `plural` de la idea | CH-1008, CH-1010 | E | "la maestro" |
| **H. Conjunto completo** | | | | | |
| V26 | Una traducción por oración ficticia: en cada grupo con la misma B (y la misma A), los españoles solo difieren en palabras de género | agrupar por `b` | CH-1013 | E | "Él duerme." y "Él dormía." |
| V27 | Sin pares duplicados (misma idea completa) | hash de la idea | — | D (se queda uno) | — |
| V28 | Distribución dentro de ±10 % relativo de `pesos.yaml` en cada marginal | conteo | CH-1104 a CH-1113 | A | REM.C 1.ª = 30 % |
| V29 | Cobertura: cada entrada del léxico aparece al menos 20 veces | conteo | CH-404 | A, y se completa | `salmi` 12 veces |
| V30 | Proporción de pares con alguna [DERIVADA] ≤ 50 %, y de cada DV por separado ≤ 15 % | conteo de `dv` | Anexo A | A | DV-02 en el 22 % |
| V31 | Ninguna raíz inventada choca con `palabras_reales.txt` actualizada | CH-306 | CH-306 | E (regenerar léxico) | — |

Ejemplo (V15):
- `Yaruqhiwa wirkharuwa tisqani.` tiene dos AFF → error.
- La forma correcta con `posicion_wa = sujeto` es `Yaruqhiwa wirkharu tisqani.` (A `Yaruqhiyi wirkhallu tisqaphu.`).

---

## 14. Preguntas abiertas para el equipo

Cada pregunta trae la recomendación de este documento. Mientras no se decida otra cosa, el generador aplica la recomendación.

1. **Orden de CAUSE/COM frente al lugar (CH-901).** L2 atestigua `Jumalaykuwa ukana irnaqtha` "por ti trabajo ahí" (L2 p.160–161): CAUSE **antes** del lugar. CH-901 pone el lugar antes. *Recomendación:* cambiar CH-901 a T – COM/CAUSE – L – OI – OD – V en v1.2, para que esta oración también sea reproducible. Cambiarían unos pocos ejemplos de §9 y los casos C25 y C28.
2. **`-täna` frente a `-tayna` (CH-512).** L2 da las dos formas, y `pampana ikitayna` (L2 p.158) usa `-tayna`. *Recomendación:* contar las dos en AmericasNLP. Si `-tayna` es mucho más frecuente, usarla en la 3.ª persona.
3. **Orden de las verificaciones [DERIVADA].** *Recomendación:* verificar primero DV-02, DV-03, DV-05 y DV-08, que son las más frecuentes en los datos (Anexo A).
4. **Plural + negación y plural + progresivo (CH-603).** Habría que decidir entre `sarapkiti` (patrón de L1) y `sarapxkiti`, y entre `-pxaska-` y `-skapxa-`. *Recomendación:* decidirlo con el corpus para v2. Mientras tanto siguen excluidos.
5. **Raíces verbales en -i/-u (CH-304).** Son frecuentes en aymara real (`iki-`, `thuqhu-`, `usu-`). *Recomendación:* en v2, documentar la regla de `thuqhuwa` (L2 p.176) y la de `us-utu` (L1 p.69) y permitir esas raíces.
6. **SIMP sin adverbio (CH-1001).** Se traduce siempre en presente, aunque muchas oraciones reales en SIMP son pasado. *Recomendación:* mantenerlo, para que la traducción sea única. Medir en el corpus qué proporción de SIMP se traduce en pasado; si pasa del 40 %, dar más peso a los adverbios de pasado.
7. **Umbral del filtro (CH-306).** *Recomendación:* medir la tasa de rechazo con el umbral 5. Si pasa del 60 % en alguna categoría, subirlo.
8. **Objeto directo humano (CH-914).** L1 atestigua `Mariy q'ipi-xa` "llevó a María" (p.72). *Recomendación:* dejarlo para v2, con información léxica por verbo.
9. **"Ser" con nombre en 1/2/4 plural.** El nombre predicado no lleva `-naka` (`Nänakaxa yaruqhïthwa`). *Recomendación:* verificarlo con el corpus.
10. **Apóstrofo publicado.** *Recomendación:* datos internos con U+0027; la conversión a U+2019 solo al publicar (CH-102).
11. **Tope de [DERIVADA] (V30).** *Recomendación:* empezar con ≤ 50 % del total y ≤ 15 % por DV, y ajustar cuando se verifiquen.
12. **`-ti` de pregunta sí/no en otros constituyentes** (L1 p.282, `Mariya-t…`). *Recomendación:* para v2, junto con las permutaciones de orden.
13. **`-kama` solo en raíces de 2 sílabas (CH-514).** *Recomendación:* si el corpus confirma la condición de L1 (vocal elidida con 3 o más vocales), ampliarlo en v2.
14. **Léxico de validación.** *Recomendación:* ampliarlo con más oraciones atestiguadas de L2 a medida que se revisen otras páginas, y añadirlas a CH-710 y CH-1201.

---

## Anexo A · Lista de reglas [DERIVADA]

Estas reglas se deducen de un patrón documentado, sin una forma atestiguada igual en L2. Se verifican con el corpus de AmericasNLP (lado aymara, normalizado con CH-102 y CH-103).

**Cómo verificarlas:**
1. Contar las dos variantes posibles con la expresión regular de la tabla.
2. Revisar a mano 50 aciertos de cada variante (la regex da falsos positivos).
3. Si la variante "Chulupi" es claramente minoritaria, cambiar la regla y subir la versión.

La columna "Frecuencia en datos" es una estimación con los pesos de `pesos.yaml`.

| DV | Regla (CH-702) | Ejemplo B → A | Patrón en que se apoya | Variante Chulupi / alternativa (regex sobre tokens) | Frecuencia en datos |
|---|---|---|---|---|---|
| DV-01 | T32 `-tama` pierde su vocal ante oracional | `ch'ixrtamwa` → `ch'ixrkiqyi` | L1 `-tam` c_c; `-tana` → `-tan` | `tam(wa\|ti)$` / `tama(wa\|ti)$` | baja |
| DV-02 | T12, T21, T31 y T34 conservan su vocal ante oracional | `ch'ixrituwa` → `ch'ixruquyi` | L1 c_v (p.144) | `(sma\|ista\|itu\|istu)(wa\|ti)$` / `(sm\|ist\|it)(wa\|ti)$` | media |
| DV-03 | Ante `-ti`: P2 y P3 conservan su vocal; P4 la pierde | `ch'ixrtati`, `ch'ixriti`, `ch'ixrtanti` | igual que ante `-wa` | `(ta\|i\|tan)ti$` / `(t\|tana)ti$` | alta |
| DV-04 | FUT.1 y FUT.2 ante oracional, y FUT.4 ante `-ti`: conservan | `tisqäwa`, `tisqätawa`, `tisqañäniti` | L1 FUT v_v | `(ä\|äta)(wa\|ti)$`, `ñäniti$` / `ätwa$`, `ñänti$` | media |
| DV-05 | Remotos ante oracional: P1 y P4 pierden la vocal; P2 y P3.REM la conservan | `tisqayäthwa`, `tisqatätanwa`, `tisqänawa` | igual persona que en SIMP | `(yä\|tä)(thwa\|tanwa\|tawa)$`, `änawa$` / `(yä\|tä)(thawa\|tanawa)$`, `änwa$` | media |
| DV-06 | PL.V conserva su vocal ante FUT.3, FUT.4 y REM.L, y se alarga con FUT.1 | `tisqapxani`, `tisqapxatätha`, `tisqapxä` | `sarapxayätha`, `sarapxäta` | `px(ani\|añäni\|atä\|ä)` / `px(ni\|ñäni\|tä)` | media |
| DV-07 | PL.V pierde su vocal ante las transiciones | `ch'ixrapxitu` | `sarapxtha`; L1 `parla-p-x-itu` | `px(sma\|ista\|itu\|tama\|istu)` / `pxa(sma\|…)` | baja |
| DV-08 | NEG con personas distintas de P1 y FUT.3 | `tisqkiti`, `tisqkäti` | `jiskht'kthti`, `jutkaniti`; L1 `sar-k-i-ti` | `k(ta\|i\|tan\|sma\|ista\|itu\|tama\|istu\|ä\|äta\|añäni)ti$` / `ka(ta\|i…)ti$` | alta |
| DV-09 | PROG con personas distintas de P3 | `tisqaskthwa` | `saraski`; L1 `aka-n-ka-s-k-t-wa` | `sk(tha\|thwa\|ta\|tana\|sma\|ista\|itu\|tama\|istu)` / `ska(tha\|…)` | baja |
| DV-10 | ESTAR con P2, P3 y P4 | `chimulanktawa`, `chimulankiwa` | `utankthwa`; L1 `taypi-n-k-i-w` | `nk(ta\|i\|tan)(wa\|ti\|sa)$` / `naka(ta\|…)` | media |
| DV-11 | TENER con P2 y P4 | `chimulanitawa` | `utanithwa` | `ni(ta\|tan)wa$` / `nï(ta\|tan)wa$` | baja |
| DV-12 | SER con P2 y P4 | `jumpütawa` | `jach'äthwa` | `[äïü](ta\|tan)wa$` / `[aiu]ka(ta\|tan)wa$` | baja |
| DV-13 | Q.YN en predicados de ser, estar y tener | `chimulankthti` | regla de `-ti` de DV-03 | `(nk\|ni\|[äïü])(th\|ta\|tan\|i)?ti$` | baja |

---

## Anexo B · Prototipo de referencia

Se entrega junto con este documento. Es una **referencia**, no el generador final. Si el prototipo y la especificación no coinciden, manda la especificación y el prototipo se corrige.

| Archivo | Contenido | Secciones |
|---|---|---|
| `chulupi_motor.py` | Grafemas, validación de palabras, tabla de morfemas B/A, palabras gramaticales y el algoritmo CH-701 con traza de decisiones | §1, §2, §5, §7 |
| `chulupi_oraciones.py` | Léxico de ejemplo y de validación, constructor de oraciones B/A (§9), español (§10) y etiquetado de [DERIVADA] (CH-702) | §9, §10, §11, §12.1 |
| `test_chulupi.py` | Pruebas: regresión CH-710 (igualdad y paralelismo), 40 casos, [ATESTIGUADO], palabras válidas, una traducción por oración (CH-1013) | CH-710, CH-1201, CH-1013 |
| `regresion_ch710.json` | Los 102 casos de CH-710 | CH-710 |
| `casos_prueba.json` | Los 40 casos de §12, con idea, salida esperada, ids por palabra y DV | §12 |

Para ejecutarlo: `python -m unittest test_chulupi -v` (Python 3.8 o superior, sin dependencias).

El prototipo **no** incluye:
- el generador de raíces (§3);
- el generador de ideas con pesos (§11);
- el validador de ideas R1–R20 completo;
- el verificador de §13.

Esas piezas corresponden a los roles del equipo.

*Fin de la especificación.*
