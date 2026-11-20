# Graph Report - Chulupi-lang  (2026-11-20)

## Corpus Check
- 9 files · ~86,328 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: .csv 2, (none) 1, .ipynb 1)

## Summary
- 191 nodes · 419 edges · 15 communities (11 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 23 edges (avg confidence: 0.81)
- Token cost: 229,159 input · 0 output

## Community Hubs (Navigation)
- Motor morfológico (prototipo)
- Alfabeto y raíces
- Oraciones del prototipo
- Reglas del proyecto y decisiones
- Morfemas y morfofonología
- Orden y oracionales
- Palabras gramaticales y casos
- Lado español
- Fuentes y reglas derivadas
- Verbo, negación y predicados
- Pesos, coherencia y verificación
- Prueba de generación y cuotas
- Entregable y conjugaciones
- Casos y léxico de prueba
- Trabajo por fases

## God Nodes (most connected - your core abstractions)
1. `Chulupi Lang Especificación v1.1.2` - 103 edges
2. `CH-1103 Restricciones de combinación R1–R22` - 17 edges
3. `Algoritmo completo del generador de raíces (§3.1)` - 13 edges
4. `CH-701 Algoritmo construir_palabra (elisión izquierda a derecha)` - 13 edges
5. `CH-901 Orden de constituyentes S–JANI–T–L–COM/CAUSE–OI–OD–V` - 13 edges
6. `np_es()` - 12 edges
7. `construir_palabra()` - 10 edges
8. `CH-306 Filtro contra palabras reales (trie, modo guía/corpus)` - 10 edges
9. `CH-406 Coherencia semántica (clase_sem y clases aceptadas)` - 10 edges
10. `CH-1302 Verificaciones V01–V31` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Decisión: Especificación 1.1.1` --references--> `chulupi_lang_spec.md`  [EXTRACTED]
  PREGUNTAS.md → claude.md
- `Decisión P-07: conjugador de borrador (conjugaciones.csv)` --conceptually_related_to--> `Entregable: notebook Jupyter (Colab y VS Code)`  [INFERRED]
  PREGUNTAS.md → claude.md
- `Decisión P-08: corrección de CH-1008 regla 5` --references--> `chulupi_lang_spec.md`  [EXTRACTED]
  PREGUNTAS.md → claude.md
- `Decisión P-01: nombre de la especificación` --references--> `chulupi_lang_spec.md`  [EXTRACTED]
  PREGUNTAS.md → claude.md
- `Error corregido: genero_np (incumplía CH-1010)` --implements--> `Principio: reutilizar el prototipo y anotar errores`  [INFERRED]
  PREGUNTAS.md → claude.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Pipeline idea → B → A → español** — datos_chulupi_lang_spec_ch_1101_1102, datos_chulupi_lang_spec_ch_901, datos_chulupi_lang_spec_ch_701, datos_chulupi_lang_spec_ch_501, datos_chulupi_lang_spec_lado_espanol [EXTRACTED 1.00]
- **Filtros de aceptación de raíces CH-306..CH-310** — datos_chulupi_lang_spec_ch_306, datos_chulupi_lang_spec_ch_307, datos_chulupi_lang_spec_ch_308, datos_chulupi_lang_spec_ch_309, datos_chulupi_lang_spec_ch_310 [EXTRACTED 1.00]
- **Puertas de calidad antes de generar** — datos_chulupi_lang_spec_ch_710, datos_chulupi_lang_spec_ch_1201, datos_chulupi_lang_spec_ch_1302, datos_chulupi_lang_spec_ch_1013 [INFERRED 0.85]
- **Filtro de palabras reales CH-306 (modo guía/corpus)** — preguntas_p_06, preguntas_p_14, preguntas_decision_p_04 [EXTRACTED 1.00]
- **Errores del prototipo corregidos en chulupi_oraciones.py** — preguntas_error_genero_np, preguntas_error_ser_adjetivo, datos_chulupi_oraciones, claude_prototipo_referencia [INFERRED 0.85]
- **Reglas de trabajo del proyecto** — claude_especificacion_manda, claude_prototipo_referencia, claude_no_inventar_reglas, claude_entregable_notebook, claude_trabajo_por_fases [EXTRACTED 1.00]

## Communities (15 total, 4 thin omitted)

### Community 0 - "Motor morfológico (prototipo)"
Cohesion: 0.09
Nodes (10): clases(), construir_ambos(), construir_palabra(), normalizar(), segmentar(), validar_palabra(), generar(), Casos (+2 more)

### Community 1 - "Alfabeto y raíces"
Cohesion: 0.11
Nodes (28): alfabeto.yaml, Algoritmo completo del generador de raíces (§3.1), Corpus AmericasNLP es–aym, CH-102 Apóstrofo U+0027, CH-103 Vocal larga (NFC, ä ï ü), CH-104 Letras prohibidas, CH-105 Segmentación en grafemas (más largo primero), CH-106 Mayúsculas y puntuación (+20 more)

### Community 2 - "Oraciones del prototipo"
Cohesion: 0.15
Nodes (19): adj_es(), articulo(), es_plural(), genero_np(), hueco(), ids_verbo(), L(), nombre_es() (+11 more)

### Community 3 - "Reglas del proyecto y decisiones"
Cohesion: 0.10
Nodes (10): claude.md (instrucciones del proyecto), chulupi_lang_spec.md, PREGUNTAS.md (preguntas abiertas), Decisión: Especificación 1.1.1, Decisión: Especificación 1.1.2, Decisión P-01: nombre de la especificación, Decisión P-04: palabras_reales.txt entregado (CH-306), Decisión P-08: corrección de CH-1008 regla 5 (+2 more)

### Community 4 - "Morfemas y morfofonología"
Cohesion: 0.16
Nodes (17): Propiedades antes/después de cada sufijo (§5.0), CH-1201 Regla de los casos de prueba, CH-308 La raíz no termina en sufijo de ≥3 grafemas, CH-501 Mapeo A por forma (homófonos), CH-502 El alargamiento se conserva en A, CH-503 Tabla fija de formas A (7 condiciones), CH-504 Tabla de morfemas (nombre, verbo, oracionales), CH-701 Algoritmo construir_palabra (elisión izquierda a derecha) (+9 more)

### Community 5 - "Orden y oracionales"
Cohesion: 0.22
Nodes (11): CH-1001–CH-1005 Tiempos españoles (SIMP, REM.C, REM.L, FUT, PROG), CH-511–CH-513 Remotos segmentados, REM.L -tä-, FUT.1 -¨, CH-514 -kama restringido (raíz de 2 sílabas), CH-601 Plantilla del nombre (N0–N7; NP_NORMAL, ESTAR, TENER, SER), CH-901 Orden de constituyentes S–JANI–T–L–COM/CAUSE–OI–OD–V, CH-902 Posición de -wa (posicion_wa), CH-903 Posición de -xa (tópico), CH-904 -ti de pregunta sí/no (+3 more)

### Community 6 - "Palabras gramaticales y casos"
Cohesion: 0.31
Nodes (10): Los 40 casos de prueba C01–C40 (casos_prueba.json), CH-1101–CH-1102 Esquema de la idea (idea.schema.yaml), CH-505 Palabras gramaticales (pronombres, interrogativos, DEM, NUM), CH-515 -layku débil, CH-516–CH-521 Demostrativos, nänaka, sin maya/paya, interrogativos, sin nombres propios, CH-707 Nada se borra entre palabras, CH-708 Palabras gramaticales en modo A, CH-916 Adverbios de lugar = DEM + LOC (+2 more)

### Community 7 - "Lado español"
Cohesion: 0.27
Nodes (10): CH-1006–CH-1009 Personas, pronombre, artículos, clíticos, CH-1010 Género de la 3.ª persona humana (campo genero), CH-1011–CH-1012 Orden y forma escrita del español, CH-1013 Una traducción por oración ficticia, CH-401 Categorías léxicas (N_HUM, N_NOHUM, V_INTR, V_MOV, V_TR, V_DITR, ADJ, ADV_T), CH-405 Género español en el léxico, CH-604 Transiciones solo en SIMP, CH-909–CH-910 COMPL.RU y exclusión con BEN (+2 more)

### Community 8 - "Fuentes y reglas derivadas"
Cohesion: 0.20
Nodes (9): CH-101 Letras permitidas (alfabeto L2), CH-207 Prohibido l + l, CH-702 Vocal propia ante oracionales (marcas c/v de L1), guia_estructural_aymara_v3.md (la guía), L1 (libro de la guía), L2 (libro de la guía, escritura oficial), Paradigmas completos (§8) y paradigmas.yaml, Reglas DERIVADA DV-01..DV-13 (Anexo A) (+1 more)

### Community 9 - "Verbo, negación y predicados"
Cohesion: 0.33
Nodes (10): CH-1103 Restricciones de combinación R1–R22, CH-602 Plantilla del verbo (V0–V6), CH-603 PL.V, PROG y NEG se excluyen, CH-605 Negación solo en SIMP y FUT, CH-606 Progresivo solo en SIMP, CH-905 Negación jani-wa, CH-906 Pregunta de información (interrogativo in situ), CH-907 Coordinación (2 miembros con -mpi) (+2 more)

### Community 10 - "Pesos, coherencia y verificación"
Cohesion: 0.32
Nodes (8): CH-1104–CH-1113 Pesos y muestreo estratificado (pesos.yaml), CH-1301 Formato de cada par (JSONL), CH-1302 Verificaciones V01–V31, CH-403 Frecuencias Zipf (exponente 0,9), CH-404 Cobertura mínima (20 apariciones), CH-406 Coherencia semántica (clase_sem y clases aceptadas), CH-911–CH-912 Posesión y frase nominal, Ri y Tsuruoka (2022)

## Knowledge Gaps
- **12 isolated node(s):** `CH-515 -layku débil`, `CH-707 Nada se borra entre palabras`, `Decisión: Especificación 1.1.1`, `Decisión P-11 (verbos): categoria_verbo y luego Zipf`, `Decisión P-13: COM instrumento o compañía` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 38 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Chulupi Lang Especificación v1.1.2` connect `Palabras gramaticales y casos` to `Alfabeto y raíces`, `Morfemas y morfofonología`, `Orden y oracionales`, `Lado español`, `Fuentes y reglas derivadas`, `Verbo, negación y predicados`, `Pesos, coherencia y verificación`?**
  _High betweenness centrality (0.263) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `CH-901 Orden de constituyentes S–JANI–T–L–COM/CAUSE–OI–OD–V` (e.g. with `CH-902 Posición de -wa (posicion_wa)` and `CH-903 Posición de -xa (tópico)`) actually correct?**
  _`CH-901 Orden de constituyentes S–JANI–T–L–COM/CAUSE–OI–OD–V` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `CH-515 -layku débil`, `CH-707 Nada se borra entre palabras`, `Decisión: Especificación 1.1.1` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Motor morfológico (prototipo)` be split into smaller, more focused modules?**
  _Cohesion score 0.09274193548387097 - nodes in this community are weakly interconnected._
- **Why does `Decisión: Especificación 1.1.2` connect `Reglas del proyecto y decisiones` to `Motor morfológico (prototipo)`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `Alfabeto y raíces` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Why does `claude.md (instrucciones del proyecto)` connect `Reglas del proyecto y decisiones` to `Motor morfológico (prototipo)`, `Oraciones del prototipo`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._