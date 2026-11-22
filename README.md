# Sistema Avanzado de Figuras 3D – Fase 4: Manejo de excepciones

**Curso:** Programación (213023) – UNAD
**Estudiante:** Ashley Caroline Cera Yopasá – Grupo 213023_571

## Descripción
Continuación del proyecto de la Fase 3. El sistema crea cubos, esferas y cilindros (clase abstracta `Figura3D` y clases derivadas), calcula su volumen y área superficial y, en esta fase, controla los errores con excepciones para que el programa sea estable y no se cierre ante datos incorrectos.

## Manejo de excepciones implementado
- **Excepciones propias:** `FiguraError` (base), `DimensionInvalidaError`, `TipoFiguraInvalidoError`.
- **Validación de medidas:** se rechazan valores negativos, cero, texto, `True/False`, `nan` e infinito.
- **try / except / else / finally:** al guardar el reporte en un archivo (el archivo siempre se cierra).
- **Errores de Python controlados:** `ValueError`, `TypeError`, `IndexError`, `ZeroDivisionError`, `OSError`, `KeyboardInterrupt`, `EOFError`.

## Cómo ejecutar
```bash
python figuras3d.py --demo   # demostración automática de casos correctos e incorrectos
python figuras3d.py          # menú interactivo
```

## Referencia
Van Rossum, G., & Drake Jr., F. L. (2024). *El tutorial de Python: Errores y excepciones*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
