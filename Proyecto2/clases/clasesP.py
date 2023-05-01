class Lexema:
    def __init__(self, lexema, token, fila, columna):
        self.lexema = lexema
        self.token = token
        self.fila = fila
        self.columna = columna

    def __str__(self): # Para imprimir el objeto
        return str(self.lexema) + " " + str(self.tipo) + " " + str(self.fila) + " " + str(self.columna)

    def getLexema(self):
        return self.lexema

    def getToken(self):
        return self.token

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
   
class Error:
    def __init__(self,lexema, tipo, fila, columna, descripcion):
        self.lexema = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.descripcion = descripcion
    
    def getError(self):
        return str(self.lexema) + " " + str(self.tipo) + " " + str(self.fila) + " " + str(self.columna) + " " + str(self.descripcion)
    
    def getLexema(self):
        return self.lexema

    def getTipo(self):
        return self.tipo

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
    
    def getDescripcion(self):
        return self.descripcion
