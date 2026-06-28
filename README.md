# RubicaLang: Analizador de Rúbricas de Evaluación

**RubicaLang** es un Lenguaje de Dominio Específico (DSL) diseñado e implementado como proyecto final para la asignatura de Compiladores. Su propósito principal es formalizar, estructurar y validar sistemas de evaluación académica mediante rúbricas, garantizando la consistencia lógica de las ponderaciones y calificaciones.

**Autor:** Daniel Morales Pérez  
**Ficha de Dominio:** Estudiante 23

---

## Características del Compilador

Este proyecto implementa el pipeline completo de un analizador (Front-end) utilizando la herramienta **PLY (Python Lex-Yacc)**:

1. **Análisis Léxico (`lexer.py`):** Tokenización del código fuente, reconocimiento de palabras reservadas del dominio (`rubrica`, `criterio`, `peso`, `nivel`, etc.) y reporte de errores léxicos posicionales.
2. **Análisis Sintáctico (`parser_ast.py`):** Implementación de una gramática LALR(1) en notación EBNF. Genera un Árbol de Sintaxis Abstracta (AST) e incluye recuperación de errores mediante **Modo Pánico**.
3. **Análisis Semántico (`semantic.py`):** Recorrido del AST mediante el patrón *Visitor* para validar:
   * Declaración única y uso válido de variables.
   * **Regla del Dominio 1:** La suma de los pesos de los criterios dentro de una rúbrica debe ser exactamente `100`.
   * **Regla del Dominio 2:** Los puntos cualitativos asignados a los niveles de evaluación no pueden ser negativos.

---

## Instrucciones de Ejecución Paso a Paso

Para garantizar que el compilador funcione correctamente y no haya conflictos con otras librerías de tu sistema, sigue estos pasos para preparar el entorno y ejecutar las pruebas.

### 1. Preparación del Entorno (Recomendado)

Asegúrate de tener **Python 3.x** instalado. Se recomienda usar un entorno virtual para instalar la dependencia `ply` de forma aislada.

Abre tu terminal en la raíz del proyecto y ejecuta:

**En Windows (PowerShell/CMD):**
```bash
# Crear el entorno virtual llamado 'venv'
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\activate

# Instalar la librería requerida
pip install ply