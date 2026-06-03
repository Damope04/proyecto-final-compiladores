from parser_ast import (
    ProgramaNode, RubricaNode, CriterioNode, NivelNode,
    DeclaracionNode, AsignacionNode, IfNode, OpBinariaNode
)

class AnalizadorSemantico:
    def __init__(self):
        # La Tabla de Símbolos es un simple diccionario en Python
        self.tabla_simbolos = {} 
        self.errores = []

    def analizar(self, ast):
        """Punto de entrada para comenzar el análisis del AST"""
        self.visit(ast)
        
        if self.errores:
            print("\n Se encontraron errores semánticos:")
            for error in self.errores:
                print(f"  - {error}")
            return False
        else:
            print("\n ¡Análisis semántico completado sin errores!")
            print("Tabla de símbolos final:", self.tabla_simbolos)
            return True

    def visit(self, nodo):
        """Método despachador: decide qué hacer según el tipo de nodo"""
        if isinstance(nodo, ProgramaNode):
            for sentencia in nodo.sentencias:
                self.visit(sentencia)
                
        elif isinstance(nodo, DeclaracionNode):
            # REGLA: No se puede declarar la misma variable dos veces
            if nodo.identificador in self.tabla_simbolos:
                self.errores.append(f"Variable duplicada: '{nodo.identificador}' ya fue declarada.")
            else:
                # Guardamos la variable en la tabla de símbolos
                self.tabla_simbolos[nodo.identificador] = nodo.tipo
            self.visit(nodo.expresion)

        elif isinstance(nodo, AsignacionNode):
            # REGLA: No se puede asignar a una variable que no existe
            if nodo.identificador not in self.tabla_simbolos:
                self.errores.append(f"Variable no declarada: Intentaste usar '{nodo.identificador}' sin declararla antes.")
            self.visit(nodo.expresion)

        elif isinstance(nodo, RubricaNode):
            # REGLAS DEL DOMINIO: Los pesos deben sumar 100 y los nombres no deben repetirse
            nombres_criterios = set()
            suma_pesos = 0
            
            for crit in nodo.criterios:
                if crit.nombre in nombres_criterios:
                    self.errores.append(f"Criterio duplicado: '{crit.nombre}' aparece más de una vez en la rúbrica '{nodo.nombre}'.")
                nombres_criterios.add(crit.nombre)
                
                suma_pesos += crit.peso
                self.visit(crit)
                
            if suma_pesos != 100:
                self.errores.append(f"Error de rúbrica '{nodo.nombre}': La suma de los pesos es {suma_pesos}, pero debe ser exactamente 100.")

        elif isinstance(nodo, CriterioNode):
            if nodo.peso < 0:
                self.errores.append(f"Peso inválido: El criterio '{nodo.nombre}' tiene un peso negativo ({nodo.peso}).")
            for nivel in nodo.niveles:
                self.visit(nivel)

        elif isinstance(nodo, NivelNode):
            if nodo.puntos < 0:
                self.errores.append(f"Puntos inválidos: El nivel '{nodo.descripcion}' tiene puntos negativos ({nodo.puntos}).")

        elif isinstance(nodo, IfNode):
            self.visit(nodo.condicion)
            for sent in nodo.bloque_verdadero:
                self.visit(sent)

        elif isinstance(nodo, OpBinariaNode):
            self.visit(nodo.izq)
            self.visit(nodo.der)
            
if __name__ == '__main__':
    import parser_ast  # Importamos el módulo completo para detectar los cambios de sus variables reales

    # Código de prueba con errores intencionales
    codigo_prueba = '''
    numero x = 10;
    x = 20;
    y = 5;  // ERROR SEMÁNTICO: 'y' no está declarada

    rubrica evaluacion_web {
        criterio frontend peso 50 {
            nivel "excelente" 10;
            nivel "malo" -2;  // ERROR SEMÁNTICO: puntos negativos
        };
        criterio backend peso 60 { // ERROR SEMÁNTICO: 50 + 60 = 110 (no da 100)
            nivel "bueno" 8;
        };
    }
    '''

    print("Construyendo AST...")
    # Usamos el parser del módulo importado
    ast = parser_ast.parser.parse(codigo_prueba)
    
    # PROTECCIÓN: Verificamos que el AST exista y que el parser no haya levantado la bandera de error
    if ast and not parser_ast.hubo_error_sintactico:
        print("Iniciando análisis semántico...")
        analizador = AnalizadorSemantico()
        analizador.analizar(ast)
    else:
        print("\n El análisis semántico no se ejecutó debido a errores en las fases previas (Léxico/Sintáctico).")