# Proyecto: generador de Chulupi Lang

- La especificación normativa es datos/chulupi_lang_spec.md (v1.1). Toda regla tiene un ID CH-xxx. Si el código y la especificación no coinciden, manda la especificación.
- datos/chulupi_motor.py y datos/chulupi_oraciones.py son un prototipo de referencia: reutiliza su lógica. Si encuentras un error, corrígelo y anota qué regla incumplía.
- No inventes reglas lingüísticas. Toda ambigüedad va a PREGUNTAS.md (ID de la regla + propuesta) y sigues con lo demás.
- El entregable es un notebook de Jupyter que debe correr de principio a fin en Google Colab con "Ejecutar todo", y también en VS Code.
- Los usuarios del notebook no son lingüistas ni programadores expertos: todo se explica en español claro, con frases cortas.
- Trabaja por fases. Al final de cada fase: ejecuta el notebook completo, muestra los resultados de las pruebas, haz un commit y espera mi "ok".