import sys
import os
import parser_ast
from semantic import AnalizadorSemantico

def ejecutar_compilador(ruta_archivo):
    # 1. Verificar si el archivo existe
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo '{ruta_archivo}' no existe.")
        return

    print(f"📖 Leyendo archivo fuente: {ruta_archivo}\n")
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        codigo_fuente = archivo.read()

    # 2. Reiniciar la bandera de errores sintácticos por seguridad
    parser_ast.hubo_error_sintactico = False

    print("========================================")
    print("Fase 1 y 2: Análisis Léxico y Sintáctico")
    print("========================================")
    
    # El parser de PLY ejecuta automáticamente el lexer de forma interna
    ast = parser_ast.parser.parse(codigo_fuente)

    # 3. Validar si la sintaxis fue correcta y se generó el AST
    if ast and not parser_ast.hubo_error_sintactico:
        print("¡Análisis sintáctico exitoso! AST construido correctamente.\n")
        
        print("========================================")
        print("Fase 3: Análisis Semántico")
        print("========================================")
        print("Iniciando verificación de reglas del dominio...")
        
        analizador = AnalizadorSemantico()
        es_valido = analizador.analizar(ast)
        
        print("========================================")
        if es_valido:
            print("¡Compilación Exitosa! El programa es completamente válido.")
        else:
            print("El programa tiene errores semánticos que deben corregirse.")
            
    else:
        print("========================================")
        print("\n La compilación se detuvo debido a errores en las fases previas (Léxico/Sintáctico).")

if __name__ == '__main__':
    # Validar que el usuario pase el archivo por argumento en la terminal
    if len(sys.argv) < 2:
        print("Error: No se especificó ningún archivo de entrada.")
        print("Uso correcto: python main.py <nombre_archivo.rub>")
        sys.argv.append(None) # Evita que colapse si se ejecuta vacío desde ciertos IDEs
        
        # Opcional: Si olvidas pasar el parámetro, puedes definir un archivo por defecto aquí para pruebas rápidas
        # ejecutar_compilador("prueba_valida.rub")
    else:
        ejecutar_compilador(sys.argv[1])