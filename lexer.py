import ply.lex as lex

# 1. Definición de Palabras Reservadas
# Usamos un diccionario para buscar rápidamente si un identificador es una palabra clave.
reserved = {
    'rubrica': 'RUBRICA',
    'criterio': 'CRITERIO',
    'peso': 'PESO',
    'nivel': 'NIVEL',
    'total': 'TOTAL',
    'descripcion': 'DESCRIPCION'
}

# 2. Lista completa de Tokens
# PLY requiere una tupla llamada 'tokens'. Sumamos las reservadas a los tokens básicos.
tokens = (
    'ID',
    'NUMERO',
    'CADENA',
    'LBRACE',
    'RBRACE',
    'SEMI',
) + tuple(reserved.values())

# 3. Reglas de Expresiones Regulares para tokens simples
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI   = r';'

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# 4. Reglas complejas (usando funciones)

def t_CADENA(t):
    r'"[^"\n]*"'
    # Guardamos el valor exacto incluyendo comillas, o puedes hacer t.value[1:-1] para quitarlas
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value) # Convertimos el lexema a un entero
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificamos si el identificador es una palabra reservada
    t.type = reserved.get(t.value, 'ID')
    return t

# Regla para contar saltos de línea (fundamental para el reporte de errores)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función auxiliar para calcular la columna exacta
def find_column(input_str, token):
    line_start = input_str.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# 5. Manejo de Errores Léxicos
def t_error(t):
    columna = find_column(t.lexer.lexdata, t)
    # Formato exacto requerido por la especificación
    print(f"Error léxico [línea {t.lineno}, columna {columna}]: carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1) # Saltamos el carácter inválido para continuar el análisis

# 6. Construcción del Lexer
lexer = lex.lex()

# --- Bloque de Prueba ---
if __name__ == '__main__':
    # Programa de prueba válido con un error léxico intencional ('@')
    data = '''rubrica examen_final {
    criterio teoria @ peso 40 {
        nivel "excelente" 10;
    };
}'''

    # Inicializamos el lexer con los datos
    lexer.input(data)

    # Imprimimos los tokens reconocidos
    print("--- INICIANDO ANÁLISIS LÉXICO ---")
    while True:
        tok = lexer.token()
        if not tok:
            break      # Ya no hay más tokens
        col = find_column(data, tok)
        print(f"Token: {tok.type:12} Lexema: {str(tok.value):15} Línea: {tok.lineno:2} Columna: {col:2}")