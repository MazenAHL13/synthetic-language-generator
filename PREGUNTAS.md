# Preguntas abiertas: generador de Chulupi Lang

Cada pregunta da la regla afectada, el problema y una propuesta. Mientras nadie decida otra cosa, el notebook aplica la propuesta.

## Abiertas

### P-02 · `idea.schema.yaml` no es YAML válido (CH-1102)
- **Problema.** Algunas líneas usan `X | Y` para decir "X o Y": `od_coord: [NP, NP] | null`, `adv_t: "id ADV_T" | null`, `ser: {adj: "id ADJ"} | {np: NP}`. Un lector de YAML no las acepta.
- **Propuesta.** En la v1.2, entrecomillar esos valores (`od_coord: "[NP, NP] | null"`). Mientras tanto, el notebook los entrecomilla al leerlos (`cargar_yaml`, sección 1) y lo avisa. Solo cambia la lectura, no el significado.

### P-03 · `excluye` de `slots.yaml` frente a las plantillas ESTAR y TENER (CH-601)
- **Problema 1.** `excluye` tiene `[LOC, AFF]` y `[LOC, Q.INF]`, pero la plantilla ESTAR exige LOC seguido de AFF o Q.INF (`utankthwa`, `kawkinkisa`). Aplicada a todas las palabras, la lista rechaza formas atestiguadas.
- **Problema 2.** El texto de CH-601 dice "LOC solo [lleva] VBLZ.KA". `excluye` no prohíbe LOC + TOP.
- **Propuesta.** `excluye` se aplica solo a las palabras NP_NORMAL, porque ESTAR, TENER y SER ya fijan su estructura. Además se aplica el texto de CH-601: tras LOC solo puede ir VBLZ.KA. En la v1.2, decirlo en `slots.yaml` y añadir `[LOC, TOP]`.

### P-06 · Modo del filtro de palabras reales (CH-306)
- **Problema.** `palabras_reales.txt` llegó con 43.437 palabras distintas. Por su tamaño parece salir de un corpus (¿AmericasNLP?), no solo de la guía. CH-306.3 dice que el modo depende de la fuente: "guía" si solo sale de la guía (umbral 1) y "corpus" si incluye AmericasNLP (umbral 5). `generador_raices.yaml` dice `modo: guia`.
- **Datos.** Con un léxico del tamaño de CH-407 (3.130 entradas), el modo "guía" descarta entre el 34 % y el 57 % de los candidatos según la categoría, y el "corpus" entre el 23 % y el 55 %. Ninguno pasa del 60 % (CH-306.5). Las 25 raíces de §4.1 pasan en los dos modos (ninguna palabra real empieza por ellas).
- **Propuesta.** Que el equipo confirme de dónde sale la lista. Mientras tanto se mantiene `MODO_FILTRO = "guia"`, el valor de la especificación y el más estricto. Si la lista es de corpus, cambiar a `"corpus"` antes de generar el léxico de producción: cambiar el modo cambia las raíces (CH-309).

### P-05 · Léxico de prueba frente a léxico de producción (CH-402, CH-1201); afecta a F2 y F3
- **Problema.** `lexico_sin_raices.csv` no está. Según lo pedido, se usan las 25 entradas de §4.1, que ya traen raíz. Los 40 casos de `casos_prueba.json` esperan justo esas raíces (`lisqu`, `ch'ixra`…). Cuando llegue el léxico real, el generador de raíces dará otras y los 40 casos fallarían.
- **Propuesta.** (a) Con el respaldo de §4.1, las raíces de la especificación se conservan y solo se validan (CH-201 a CH-310). (b) Los 40 casos siempre se prueban con un léxico fijo de prueba (§4.1 + LV01–LV18), aparte del léxico de producción.

### P-09 · Demostrativo sujeto de "ser": "eso" o "ese" (CH-1008, regla 1 y regla 5)
- **Problema.** El nuevo ejemplo de la regla 5 dice "eso es pan" (demostrativo neutro). Pero la regla 1 y el ejemplo `Aka-xa chimula-wa.` → "Esta es una casa." hacen que el demostrativo concuerde con el nombre. Con esa regla sale "Ese es pan.".
- **Propuesta.** Se mantiene la concordancia, que es lo que hacen el prototipo y la regla 1: "Ese es pan.". Si el equipo quiere el neutro ("esto / eso / aquello") con nombres no contables, hay que decirlo en una regla.

### P-10 · Transición frente a la cuota de persona (CH-1104, CH-1109)
- **Problema.** CH-1104 fija la persona del sujeto en la cuota. CH-1109 dice que "se elige primero la transición; fija la persona del sujeto". Las dos cosas no pueden pasar a la vez.
- **Propuesta.** Manda la cuota (CH-1104). En SIMP, con un verbo `obj_persona = s`, la transición se sortea solo entre `objeto_3` y las transiciones cuyo sujeto es la persona de la cuota, renormalizando los pesos. Con persona 4 no hay transición. Así, las transiciones salen algo menos que el 7 % cada una.

### P-12 · Adverbio de tiempo con "ser", "estar" y "tener" (CH-901, CH-1011)
- **Problema.** CH-901 dice que en estos predicados "no hay posiciones 4 a 7", así que la posición 3 (tiempo) quedaría permitida. Pero CH-1011 ("sujeto – verbo – predicado") y el español del prototipo no escriben el adverbio: "Yo tengo pan ayer" saldría sin "ayer" en español.
- **Propuesta.** Estos predicados no llevan `adv_t`. El validador lo rechaza (CH-908) y el generador no lo sortea.

### P-11b · Categoría de los nombres fuera del sujeto (CH-402, CH-403)
- **Problema.** `sujeto_clase_humana` (v1.1.2) decide la categoría del sujeto. Otras funciones también aceptan `N_HUM` y `N_NOHUM`: la compañía (COM, `persona|animal`) y CAUSE (`abstracto|persona`). Para ellas no hay pesos.
- **Propuesta.** Las dos categorías pesan lo mismo (0,5 / 0,5) y después se aplica Zipf dentro de la elegida. Si el equipo quiere otros pesos, añadirlos a `pesos.yaml`.

### P-14 · Palabras gramaticales del modo A frente a CH-306 en modo "guía"
- **Problema.** Tras cambiar `mulu` → `sipu`, ninguna palabra gramatical del modo A es una palabra real. Pero en modo "guía" (umbral 1) tres no pasarían el filtro de prefijos: `muqi` (`muqintasitayna`…), `tilu` (`tilunjamaw`) y `yuli` (`yuliax`). En modo "corpus" (umbral 5) pasan todas.
- **Propuesta.** La prueba exige que no sean palabras reales y que pasen el umbral "corpus". Si el equipo decide el modo "guía" en P-06, habría que cambiar esas tres formas en la v1.2 (no las cambio: son decisiones de la tabla de formas A, CH-503).

### P-15 · Pares duplicados con un léxico pequeño (V27, CH-1104)
- **Problema.** Con el léxico de ejemplo (26 entradas), de 100.000 ideas 37.968 son repetidas. V27 las descarta y quedan 62.032 pares. Las ideas de "ser", "estar" y "tener" se repiten más, así que pierden peso: V28 avisa en 18 marginales (`ser.afirmativa`: 0,7 % frente a 6 %).
- **Propuesta.** No se completan los pares que faltan: con 26 palabras, completar solo repetiría más las verbales. Con el léxico de producción (≈ 3.130 entradas) los duplicados deberían ser pocos. Si no lo son, decidir si se completa hasta `N_PARES`.

### P-16 · Detalles de la v1.1.2 que se interpretaron
- **Problema.** La especificación 1.1.2 no llegó en el mensaje. Los cambios se escribieron a partir de su descripción. Tres puntos no estaban dichos:
  1. `pasado_remoto` tampoco va con el progresivo, como `pasado` en CH-917.
  2. El lugar de "estar en" (N-LOC-VBLZ.KA) cuenta como frase de lugar: no lleva numeral.
  3. Con un poseedor, la frase lleva POSS.3, así que una frase con UNTIL tampoco lleva poseedor (R10, CH-601).
- **Propuesta.** Confirmar los tres. Si llega el texto de la 1.1.2, comparar con `datos/chulupi_lang_spec.md`.

## Decisiones tomadas

- **20-11-2026 · Especificación 1.1.2** (en `datos/chulupi_lang_spec.md`; ver P-16):
  - INT.QUE en modo A es `sipu` (antes `mulu`, palabra real: "mulu mulu" = gato montés). Cambiado en CH-505, `morfemas.yaml`, CH-906, CH-1011, C32 (`casos_prueba.json`) y `chulupi_motor.py`.
  - ADV_T `pasado_remoto` (CH-401, CH-402, CH-917, CH-1001). "ayer" (`pasado`) solo va con SIMP. Entrada de prueba L0026 "antes", raíz `lasmiq'a` generada por §3 (semilla `semilla_raices + 26`, pasa CH-201 a CH-310). El ejemplo de CH-903 pasa a usar "antes".
  - CAUSE solo con `V_MOV` y `V_INTR` (CH-406).
  - Columna `admite_ben` (CH-402, CH-406): BEN solo si es `s`. En el ejemplo: comprar, cortar y dar `s`; comer y ver `n`.
  - Las frases de lugar no llevan numeral (CH-912).
  - `pesos.yaml`: `sujeto_clase_humana: 0.60`.
  - Lo decidió el responsable del proyecto.
- **20-11-2026 · P-01 resuelta.** La especificación se llama `datos/chulupi_lang_spec.md`, como dice CLAUDE.md. El notebook solo busca ese nombre.
- **20-11-2026 · Prueba del proceso completo.** 100.000 pares con el léxico de ejemplo, en `salida/prueba_lexico_ejemplo/`, marcados "NO USAR PARA ENTRENAR" (campo `uso` y `LEEME.txt`). La carpeta no va al control de versiones. Lo decidió el responsable del proyecto.
- **20-11-2026 · Especificación 1.1.1.** Cambios copiados en `datos/chulupi_lang_spec.md`:
  - CH-406: BEN solo con `V_TR` y `V_DITR`; `V_MOV` y `V_INTR` no llevan objeto indirecto.
  - CH-1103: R21 (un lexema no se repite en la idea) y R22 (solo entradas `L…` del léxico de producción; `LV01`–`LV18` solo para pruebas).
  - `pesos.yaml`: `categoria_verbo` y `oi_otros` → `oi_V_TR`.
  - El notebook comprueba la versión 1.1.1. Lo decidió el responsable del proyecto.
- **20-11-2026 · P-11 (verbos).** Primero la categoría con `categoria_verbo`, después Zipf dentro de ella. Los nombres siguen abiertos (P-11). Lo decidió el responsable del proyecto.
- **20-11-2026 · P-13 confirmada.** COM es instrumento si el verbo tiene `instr_clases`. Si no, es compañía, solo con `V_MOV` o `V_INTR` y sujeto `persona` (también `khiti`, CH-906). Si no cabe ninguna de las dos, no hay COM. Una prueba lo comprueba en 10.000 ideas.
- **20-11-2026 · P-07 resuelta (§10).** El borrador de las conjugaciones forma parte de la tarea. La celda 7.2 genera `datos/conjugaciones.csv` con un conjugador propio, sin bibliotecas: regulares, cambios de vocal, cambios de escritura y una tabla de irregulares. Cada fila nueva lleva `revisado = n`; el notebook avisa sin detenerse, y las filas que ya existen no se tocan nunca. Control: para los 10 verbos del prototipo da exactamente sus formas. El error claro queda solo para los verbos que no están en la tabla. Lo decidió el responsable del proyecto.
- **20-11-2026 · P-08 resuelta (CH-1008, regla 5).** Era un error de la especificación; el prototipo tenía razón. La regla 5 pasa a decir: "nombre no humano: 'un / una' si es contable y singular; nada si es plural o no contable". Se corrigió en `datos/chulupi_lang_spec.md` y en el notebook, con una prueba ("Ese es pan."). Lo decidió el responsable del proyecto.
- **20-11-2026 · P-04 resuelta (CH-306).** El equipo entregó `datos/palabras_reales.txt`. La sección 6 aplica el filtro con esa lista. Queda abierto el modo (P-06).
- **20-11-2026 · Lugar de los 40 casos (CH-1201).** Necesitan el constructor de oraciones (sección 8). La sección 4 prueba CH-710. Los 40 casos van al final de la sección 8, y la sección 10 repite todas las pruebas antes de generar. Lo decidió el responsable del proyecto.

## Errores del prototipo corregidos

- **Motor.** Ninguno. El motor (`chulupi_motor.py`) da las mismas salidas que la especificación en los 102 casos de CH-710, los 64 paradigmas y los 16 ejemplos de §7.1.
- **`chulupi_oraciones.py`, `genero_np` (incumplía CH-1010).** Por la precedencia de `or … if … else`, un nombre de género fijo tomaba el `genero` de la idea: `{"n": "L0004", "genero": "m"}` daba "el mujer". Corregido en la sección 7: el campo solo cuenta si el nombre es `var`.
- **`chulupi_oraciones.py`, "ser" + adjetivo (incumplía CH-405).** El adjetivo concordaba con `sujeto.genero`, que no existe en sujetos no humanos: "La casa es rojo". Corregido: con un sujeto nombre, concuerda con el género de ese nombre ("La casa es roja").
- Ninguna de las dos correcciones cambia los 40 casos de CH-1201.
