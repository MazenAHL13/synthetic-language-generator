# Preguntas abiertas: generador de Chulupi Lang

Cada pregunta da la regla afectada, el problema y una propuesta. Mientras nadie decida otra cosa, el notebook aplica la propuesta.

## Abiertas

### P-01 · Nombre del archivo de la especificación (sin regla CH)
- **Problema.** CLAUDE.md dice `datos/chulupi_lang_spec.md`, pero el archivo se llama `datos/artificial_lang_spec.md`. Su contenido es la v1.1.
- **Propuesta.** Renombrarlo a `chulupi_lang_spec.md`. Mientras tanto, el notebook acepta los dos nombres (celda 0.3).

### P-02 · `idea.schema.yaml` no es YAML válido (CH-1102)
- **Problema.** Algunas líneas usan `X | Y` para decir "X o Y": `od_coord: [NP, NP] | null`, `adv_t: "id ADV_T" | null`, `ser: {adj: "id ADJ"} | {np: NP}`. Un lector de YAML no las acepta.
- **Propuesta.** En la v1.2, entrecomillar esos valores (`od_coord: "[NP, NP] | null"`). Mientras tanto, el notebook los entrecomilla al leerlos (`cargar_yaml`, sección 1) y lo avisa. Solo cambia la lectura, no el significado.

### P-03 · `excluye` de `slots.yaml` frente a las plantillas ESTAR y TENER (CH-601)
- **Problema 1.** `excluye` tiene `[LOC, AFF]` y `[LOC, Q.INF]`, pero la plantilla ESTAR exige LOC seguido de AFF o Q.INF (`utankthwa`, `kawkinkisa`). Aplicada a todas las palabras, la lista rechaza formas atestiguadas.
- **Problema 2.** El texto de CH-601 dice "LOC solo [lleva] VBLZ.KA". `excluye` no prohíbe LOC + TOP.
- **Propuesta.** `excluye` se aplica solo a las palabras NP_NORMAL, porque ESTAR, TENER y SER ya fijan su estructura. Además se aplica el texto de CH-601: tras LOC solo puede ir VBLZ.KA. En la v1.2, decirlo en `slots.yaml` y añadir `[LOC, TOP]`.

### P-04 · Falta la fuente del filtro de palabras reales (CH-306); afecta a F2
- **Problema.** `palabras_reales.txt` no está en `datos/`. CH-306 dice que se arma con "todas las cadenas entre acentos graves de la guía", pero la guía (`guia_estructural_aymara_v3.md`) tampoco está. Las cadenas de la especificación no sirven: mezclan formas reales con raíces inventadas (`tisqa`, `chimula`), y estas se filtrarían contra sí mismas.
- **Propuesta.** Que el equipo entregue `palabras_reales.txt` (o la guía) antes de F2. Si no llega, la sección 6 avisa y genera las raíces sin el filtro CH-306, que queda marcado como pendiente en el informe.

### P-05 · Léxico de prueba frente a léxico de producción (CH-402, CH-1201); afecta a F2 y F3
- **Problema.** `lexico_sin_raices.csv` no está. Según lo pedido, se usan las 25 entradas de §4.1, que ya traen raíz. Los 40 casos de `casos_prueba.json` esperan justo esas raíces (`lisqu`, `ch'ixra`…). Cuando llegue el léxico real, el generador de raíces dará otras y los 40 casos fallarían.
- **Propuesta.** (a) Con el respaldo de §4.1, las raíces de la especificación se conservan y solo se validan (CH-201 a CH-310). (b) Los 40 casos siempre se prueban con un léxico fijo de prueba (§4.1 + LV01–LV18), aparte del léxico de producción.

## Decisiones tomadas

- **20-11-2026 · Lugar de los 40 casos (CH-1201).** Necesitan el constructor de oraciones (sección 8). La sección 4 prueba CH-710. Los 40 casos van al final de la sección 8, y la sección 10 repite todas las pruebas antes de generar. Lo decidió el responsable del proyecto.

## Errores del prototipo corregidos

- Ninguno por ahora. El motor (`chulupi_motor.py`) da las mismas salidas que la especificación en los 102 casos de CH-710, los 64 paradigmas y los 16 ejemplos de §7.1.
