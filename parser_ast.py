import ply.yacc as yacc
# Importamos los tokens y el lexer que ya hiciste
from lexer import tokens, find_column

hubo_error_sintactico = False
# ==========================================
# PRECEDENCIA DE OPERADORES
# ==========================================
precedence = (
    ('left', 'MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL', 'IGUALDAD', 'DISTINTO'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
)

# ==========================================
# NODOS DEL ÁRBOL DE SINTAXIS ABSTRACTA (AST)
# ==========================================

class NodoAST:
    pass

class ProgramaNode(NodoAST):
    def __init__(self, sentencias):
        self.sentencias = sentencias
        
class RubricaNode(NodoAST):
    def __init__(self, nombre, criterios):
        self.nombre = nombre
        self.criterios = criterios  # Lista de objetos CriterioNode

class CriterioNode(NodoAST):
    def __init__(self, nombre, peso, niveles, linea, columna):
        self.nombre = nombre
        self.peso = peso            # Valor entero
        self.niveles = niveles      # Lista de objetos NivelNode
        self.linea = linea          # Guardamos la posición para el análisis semántico
        self.columna = columna

class NivelNode(NodoAST):
    def __init__(self, descripcion, puntos):
        self.descripcion = descripcion # Cadena de texto
        self.puntos = puntos            # Valor entero

class AsignacionNode(NodoAST):
    def __init__(self, identificador, expresion):
        self.identificador = identificador
        self.expresion = expresion

class IfNode(NodoAST):
    def __init__(self, condicion, bloque_verdadero):
        self.condicion = condicion
        self.bloque_verdadero = bloque_verdadero

class OpBinariaNode(NodoAST):
    def __init__(self, izq, operador, der):
        self.izq = izq
        self.operador = operador
        self.der = der
        
class DeclaracionNode(NodoAST):
    def __init__(self, tipo, identificador, expresion):
        self.tipo = tipo
        self.identificador = identificador
        self.expresion = expresion
# ==========================================
# REGLAS GRAMATICALES Y CONSTRUCCIÓN DEL AST
# ==========================================

def p_programa(p):
    'programa : lista_sentencias'
    p[0] = ProgramaNode(p[1]) # Ahora ProgramaNode guardará una lista de sentencias

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_sentencia(p):
    '''sentencia : rubrica
                 | declaracion
                 | asignacion
                 | estructura_if'''
    p[0] = p[1]

def p_declaracion(p):
    'declaracion : TIPO_NUMERO ID IGUAL expresion SEMI'
    p[0] = DeclaracionNode(p[1], p[2], p[4])

def p_rubrica(p):
    'rubrica : RUBRICA ID LBRACE lista_criterios RBRACE'
    p[0] = RubricaNode(p[2], p[4])

def p_lista_criterios_multiples(p):
    'lista_criterios : lista_criterios criterio'
    p[1].append(p[2])
    p[0] = p[1]

def p_lista_criterios_unico(p):
    'lista_criterios : criterio'
    p[0] = [p[1]]

def p_criterio(p):
    'criterio : CRITERIO ID PESO NUMERO LBRACE lista_niveles RBRACE SEMI'
    # Capturamos la posición del token 'CRITERIO' para el reporte de errores semánticos
    linea = p.lineno(1)
    columna = find_column(p.lexer.lexdata, p.slice[1])
    
    p[0] = CriterioNode(p[2], p[4], p[6], linea, columna)

def p_lista_niveles_multiples(p):
    'lista_niveles : lista_niveles nivel'
    p[1].append(p[2])
    p[0] = p[1]

def p_lista_niveles_unico(p):
    'lista_niveles : nivel'
    p[0] = [p[1]]

def p_nivel(p):
    '''nivel : NIVEL CADENA NUMERO SEMI
             | NIVEL CADENA MENOS NUMERO SEMI'''
    if len(p) == 5:
        # Caso positivo: nivel "excelente" 10;
        p[0] = NivelNode(p[2], int(p[3]))
    else:
        # Caso negativo: nivel "malo" -2; (p[3] es el '-', p[4] es el número)
        p[0] = NivelNode(p[2], -int(p[4]))

def p_asignacion(p):
    'asignacion : ID IGUAL expresion SEMI'
    p[0] = AsignacionNode(p[1], p[3])

def p_estructura_if(p):
    'estructura_if : SI LPAREN expresion RPAREN LBRACE lista_sentencias RBRACE'
    p[0] = IfNode(p[3], p[6])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion IGUALDAD expresion
                 | expresion DISTINTO expresion'''
    p[0] = OpBinariaNode(p[1], p[2], p[3])

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = p[1]

def p_expresion_id(p):
    'expresion : ID'
    p[0] = p[1]
# ==========================================
# MANEJO DE ERRORES SINTÁCTICOS
# ==========================================
# Recuperación de errores en sentencias (Modo Pánico)
def p_sentencia_error(p):
    '''sentencia : error SEMI
                 | error RBRACE'''
    print(f"Modo pánico: Error recuperado, ignorando tokens hasta encontrar '{p[2]}'")
    p[0] = None  # Devolvemos None para no meter basura al AST

def p_error(p):
    global hubo_error_sintactico
    hubo_error_sintactico = True
    if p:
        columna = find_column(p.lexer.lexdata, p)
        print(f"Error sintáctico [línea {p.lineno}, columna {columna}]: token inesperado '{p.value}'")
        # Aquí se puede implementar el modo pánico para recuperar errores si es necesario
    else:
        print("Error sintáctico: Fin de archivo inesperado (EOF)")

# Construir el parser
parser = yacc.yacc()

if __name__ == '__main__':
    codigo = '''
    x = 10;
    rubrica examen_final {
        criterio teoria peso 40 {
            nivel "excelente" 10;
            nivel "bueno" 7;
        };
        criterio practica peso 60 {
            nivel "excelente" 10;
        };
    }
    '''

    ast = parser.parse(codigo)
    if ast:
        print("¡Análisis sintáctico exitoso! AST construido.")
        
        # Ahora recorremos la lista de sentencias
        for sentencia in ast.sentencias:
            if isinstance(sentencia, RubricaNode):
                print(f"Rúbrica detectada: {sentencia.nombre}")
                for crit in sentencia.criterios:
                    print(f"  -> Criterio: {crit.nombre} (Peso: {crit.peso})")
                    for niv in crit.niveles:
                        print(f"     * Nivel: {niv.descripcion} -> {niv.puntos} pts")
            
            elif isinstance(sentencia, AsignacionNode):
                print(f"Asignación detectada: Variable '{sentencia.identificador}'")