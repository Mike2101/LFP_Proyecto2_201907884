from clases.clasesP import *

#miau

reservadasLenguaje = {
    'CREAR-BD': 'CrearBD',
    'ELIMINARBD': 'EliminarBD',
    'CREARCOLECCION':'CrearColeccion',
    'ELIMINARCOLECCION':'EliminarColeccion',
    'INSERTARUNICO':'InsertarUnico',
    'ACTUALIZARUNICO':'ActualizarUnico',
    'ELIMINARUNICO':'EliminarUnico',
    'BUSCARTODO':'BuscarTodo',
    'BUSCARUNICO':'BuscarUnico',
    'IGUAL':'=',
    'PARIZQ':'(',
    'PARDER':')',
    'PUNTO-COMA':';',
    'COMA':',',
    'TOKEN-SET':'$set',
    #'COMILLAS': '"',
    'NUEVA': 'nueva'
}

global lexema
global linea
global columna
global listaMostrarTokens # Servira para mostrar todos los lexemas, tokens, linea, columna en cuestion
global listaErrores #lista de errores captados en el analisis
global listaReservadas #lista de reservadas
global listaLexemasCharValidos #lista de caracteres regados y validos
global listaLexemasValidos #lista de lexemas reconocidos

listaMostrarTokens = []
listaErrores = []
listaReservadas = []
listaLexemasCharValidos = []
listaLexemasValidos = []

global listaMostrarErrores #lista de errores captados en el analisis solo se muestran en consola
listaMostrarErrores = []

global listaGeneral
listaGeneral = [] #muestra todos los tokens recopilados en el analisis, ver tabla de tokens

global listaParalistadeComandos #lista de los tokens en orden de lectura
listaParalistadeComandos = []

global listaComandos #lista de listas de tokens, cada lista tiene los tokens en orden hasta un punto y coma
listaComandos = [] #lista de listas de objetos lexemas, cada lista tiene los lexemas en orden de entrada hasta un punto y coma

global listaMongoDB #muestra la salida en la caja de texto
listaMongoDB = []

#-----------------------------------Analizador Lexico--------------------------------------------

def imprimirTodo():
    print("---------------------------Lista de lexemas reservados---------------------------")
    print("Forma de impresion: [Lexema, Token, Linea, Columna]\n")
    if len(listaReservadas) == 0:
        print("No hay lexemas que sean palabras reservadas")
    else:
        for lexema in listaReservadas:
          print(lexema)
    print("---------------------------Lista de otros lexemas unicos (caracteres)---------------------------")
    if len(listaLexemasCharValidos) == 0:
        print("No hay otros lexemas unicos")
    else:
        for lexema in listaLexemasCharValidos:
          print(lexema)
    print("---------------------------Lista de Tokens---------------------------")
    if len(listaMostrarTokens) == 0:
        print("No hay tokens reconocidos")
    else:
        for token in listaMostrarTokens:
          print(token)
    print("---------------------------Lista de lexemas validos---------------------------")
    if len(listaLexemasValidos) == 0:
        print("No hay lexemas validos")
    else:
        for lexema in listaLexemasValidos:
          print(lexema)
    print("---------------------------Lista de errores lexicos---------------------------")
    if len(listaErrores) == 0:
        print("No hay Error lexicos")
    else:
        for lexema in listaErrores:
          print(lexema)

def get_key(lexema):
    return list(reservadasLenguaje.keys())[list(reservadasLenguaje.values()).index(lexema)]

def obtenerComentarioMultilinea(string):
    global linea
    global columna
    lexema = '/*'
    posString = 0

    while string:
        char = string[posString]
        posString +=1

        if char == '\n':
            linea +=1
            columna = 0
            lexema += char
            string = string[posString:]
            posString = 0

        elif char == '\t':
            columna +=4
            lexema += char
            string = string[posString:]
            posString = 0

        elif char == ' ':
            columna +=1
            lexema += char
            string = string[posString:]
            posString = 0

        elif char == '*':
            substring = string[0:2]
            if substring == '*/':
                lexema += substring
                return lexema, string[posString+1:]
            
        else: 
            lexema+=char
    
    return None, None

def obtenerComentarioUnilinea(string):
    global linea
    global columna
    lexema = '--- '
    posString = 0

    while string:
        char = string[posString]
        posString +=1

        if char == '\n':
            return lexema, string[posString:]
 
        else: 
            lexema+=char
    
    return None, None

def obtenerLexemaPalabra(string):
    global linea 
    global columna
    posString = 0
    lexema = ''

    while string:
        char = string[posString]
        posString +=1
        
        if char.isalpha():
            lexema+=char

        elif char == '_' or char == '-' or char.isdigit():
            lexema+=char
        
        elif char == '\n' or char == ' ' or char == '\t' or char == '"':
            return lexema, string[posString:]
        elif char == '(':
            return lexema, string[posString-1:]
        
    return None, None

def obtenerLexemaParametro(string): #el parametro string es la cadena de entrada cortada desde la posicion del caracter "
    global linea
    global columna

    lexema = ''
    pos_String = 0 #El nuevo string cortado empieza en 0

    while string:
        char = string[pos_String]
        pos_String+=1

        if char == '{':
            lexema+=char

            while string:
                char = string[pos_String]
                pos_String+=1

                if char == '\n': 
                    linea+=1
                    columna = 1
                    string = string[pos_String:]
                    pos_String = 0

                elif char == ' ':
                    string = string[pos_String:]
                    columna+=1
                    pos_String = 0

                elif char == '\t':
                    columna+=4
                    string = string[pos_String:]
                    pos_String = 0
                
                elif char == ')':
                    return lexema, string[pos_String-1:]
                
                else:
                    lexema+=char

                '''
                elif char in reservadasLenguaje.values():
                    lexema = char
                    l = [lexema, get_key(lexema), linea, columna]
                    listaLexemasCharValidos.append(l)
                    listaMostrarTokens.append(get_key(lexema))
                    #listaTokens.append(get_key(lexema))
                    string = string[pos_String:]
                    columna+=1
                    pos_String = 0
                    '''

        elif char == '"' or char == "”":
            # por si existieran n cantidad de espacios, para evitar errores en el analisis
            return lexema, string[pos_String:]
        
        else:
            lexema += char

    return None, None

#--------------------------------------Sintactico----------------------------------------------

#----------------------------------No Tienen parametros------------------------------------

def analizarCrearBD(comando):
    #Usar un codigo de referencia para saber que parte del comando se esta analizando
    # 0 = crearBD   #1 -> ID  #2 -> = #3 -> nueva #4 -> CrearBD #5 = (  #6 -> ) #7 -> ;
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "CrearBD":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo =, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return 
        elif codigoReferencia == 4:
            if dato.lexema == "CrearBD":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra CrearBD")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra CrearBD")
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo (")
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == ")":
                codigoReferencia = 7
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo )")
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.lexema == ";":
                print("Se creo la base de datos: ", identificador)
                listaMongoDB.append('use('+ '\"'+identificador+'\"'+');') 
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ;")
                listaErrores.append(error)
                return 

def analizarEliminarBD(comando):
    #Usar un codigo de referencia para saber que parte del comando se esta analizando
    # 0 = crearBD   #1 -> ID  #2 -> = #3 -> nueva #4 -> CrearBD #5 = (  #6 -> ) #7 -> ;
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "EliminarBD":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo =")
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva")
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "EliminarBD":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra EliminarBD")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra EliminarBD")
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error("Sintactico", "Se esperaba el simbolo (", dato.fila, dato.columna)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == ")":
                codigoReferencia = 7
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error("Sintactico", "Se esperaba el simbolo )", dato.fila, dato.columna)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.lexema == ";":
                print("Se Elimino la base de datos:", identificador)
                listaMongoDB.append('db.dropDatabase();')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba ;")
                listaErrores.append(error)
                return

#----------------------------------Tienen un parametro------------------------------------

def analizarCrearColeccion(comando):
    #Usar un codigo de referencia para saber que parte del comando se esta analizando
    #
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "CrearColeccion":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo =, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "CrearColeccion":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra CrearColeccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra CrearColeccion")
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo (, pero se encontro: " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')  
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \", pero se encontro: " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == "PARAMETRO-NOMBRE":
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro NOMBRE, pero se encontro: " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \", pero se encontro: " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ")":
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo )")
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == ";":
                print("Se creo una coleccion con nombre: ", parametroName)
                listaMongoDB.append('db.createCollection("'+parametroName+'");')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ;")
                listaErrores.append(error)
                return

def analizarEliminarColeccion(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "EliminarColeccion":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "EliminarColeccion":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra EliminarColeccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra EliminarColeccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro nombre coleccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ")":
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == ";":
                print("Se elimino la coleccion: ", parametroName)
                listaMongoDB.append('db.'+parametroName+'.drop();')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return

#-----------------------------------Tienen 2 parametros-----------------------------------

def analizarInsertarUnico(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "InsertarUnico":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "InsertarUnico":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra InsertarUnico")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra InsertarUnico pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ',':
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo , ")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo , pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == '"':
                codigoReferencia = 11
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 11:
            if dato.token == 'PARAMETRO-JSON':
                parametroJson = dato.lexema
                codigoReferencia = 12
            else:
                print("Error sintactico: Se esperaba un parametro de tipo JSON de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro JSON pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 12:
            if dato.lexema == '"':
                codigoReferencia = 13
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 13:
            if dato.lexema == ")":
                codigoReferencia = 14
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 14:
            if dato.lexema == ";":
                print("Se inserto", parametroJson, "para:", parametroName)
                listaMongoDB.append('db.'+parametroName+'.insertOne('+parametroJson+');')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return

def analizarActualizarUnico(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "ActualizarUnico":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "ActualizarUnico":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra ActualizarUnico")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra ActualizarUnico pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba el nombre de la coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el nombre de la coleccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ',':
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo , ")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo , pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == '"':
                codigoReferencia = 11
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 11:
            if dato.token == 'PARAMETRO-JSON':
                parametroJson = dato.lexema
                codigoReferencia = 12
            else:
                print("Error sintactico: Se esperaba un parametro de tipo JSON de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro JSON pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 12:
            if dato.lexema == '"':
                codigoReferencia = 13
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 13:
            if dato.lexema == ")":
                codigoReferencia = 14
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 14:
            if dato.lexema == ";":
                print("Se inserto", parametroJson, "para:", parametroName)
                listaMongoDB.append('db.'+parametroName+'.updateOne('+parametroJson+');')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
    
def analizarEliminarUnico(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "EliminarUnico":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "EliminarUnico":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra EliminarUnico")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra EliminarUnico pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro nombre coleccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ',':
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo , ")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo , pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == '"':
                codigoReferencia = 11
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 11:
            if dato.token == 'PARAMETRO-JSON':
                parametroJson = dato.lexema
                codigoReferencia = 12
            else:
                print("Error sintactico: Se esperaba un parametro de tipo JSON de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro JSON pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 12:
            if dato.lexema == '"':
                codigoReferencia = 13
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 13:
            if dato.lexema == ")":
                codigoReferencia = 14
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 14:
            if dato.lexema == ";":
                print("Se inserto", parametroJson, "para:", parametroName)
                listaMongoDB.append('db.'+parametroName+'.deleteOne('+parametroJson+');')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return

#----------------------------------Tienen un parametro------------------------------------

def analizarBuscarUnico(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "BuscarUnico":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "BuscarUnico":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra BuscarUnico")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra BuscarUnico pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro nombre coleccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ")":
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == ";":
                print("Se hizo la busqueda de uno de los elementos para:", parametroName)
                listaMongoDB.append('db.'+parametroName+'.findOne();')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return

def analizarBuscarTodos(comando):
    codigoReferencia = 0
    while comando:
        dato = comando.pop(0)

        if codigoReferencia == 0 and dato.lexema == "BuscarTodo":
            codigoReferencia = 1
        elif codigoReferencia == 1:
            if dato.token != "IDENTIFICADOR":
                print("Error sintactico: Se esperaba un identificador")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un identificador, pero se encontro: "+dato.lexema)
                listaErrores.append(error)
                return
            else:
                identificador = dato.lexema     
                codigoReferencia = 2
        elif codigoReferencia == 2:
            if dato.lexema == "=":
                codigoReferencia = 3
            else:
                print("Error sintactico: Se esperaba el simbolo =")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo = pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return      
        elif codigoReferencia == 3:
            if dato.lexema == "nueva":
                codigoReferencia = 4
            else:
                print("Error sintactico: Se esperaba la palabra nueva")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra nueva pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 4:
            if dato.lexema == "BuscarTodo":
                codigoReferencia = 5
            else:
                print("Error sintactico: Se esperaba la palabra BuscarTodo")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba la palabra BuscarUnico pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 5:
            if dato.lexema == "(":
                codigoReferencia = 6
            else:
                print("Error sintactico: Se esperaba el simbolo (")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ( pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 6:
            if dato.lexema == '"':
                codigoReferencia = 7
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 7:
            if dato.token == 'PARAMETRO-NOMBRE':
                parametroName = dato.lexema
                codigoReferencia = 8
            else:
                print("Error sintactico: Se esperaba un parametro de tipo nombre de coleccion")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba un parametro nombre coleccion pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 8:
            if dato.lexema == '"':
                codigoReferencia = 9
            else:
                print('Error sintactico: Se esperaba el simbolo "')
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo \" pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 9:
            if dato.lexema == ")":
                codigoReferencia = 10
            else:
                print("Error sintactico: Se esperaba el simbolo )")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ) pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
        elif codigoReferencia == 10:
            if dato.lexema == ";":
                print("Se hizo la busqueda de todos los elementos para:", parametroName)
                listaMongoDB.append('db.'+parametroName+'.find();')
                return
            else:
                print("Error sintactico: Se esperaba el simbolo ;")
                error = Error(dato.lexema,"Sintactico", dato.fila, dato.columna, "Se esperaba el simbolo ; pero se encontro " + dato.lexema)
                listaErrores.append(error)
                return
    
def VerComandos():
    print("-------------------------------------------------------------------------------------------------------------------")
    #print("Comandos recopilados: \n", listaComandos)
    '''
    for lista in listaComandos:
        for lexema in lista:
            print(lexema.lexema, lexema.token, lexema.fila, lexema.columna)
            print("---------------------------------------------------------------------------------------------------------------")
    '''

    if len(listaComandos) == 0:
        print("No se encontraron comandos")
        return

    while listaComandos:
        comando = listaComandos.pop(0)

        if comando[0].lexema == "CrearBD":
            analizarCrearBD(comando)  
        elif comando[0].lexema == "EliminarBD":
            analizarEliminarBD(comando)
        elif comando[0].lexema == "CrearColeccion":
            analizarCrearColeccion(comando)
        elif comando[0].lexema == "EliminarColeccion":
            analizarEliminarColeccion(comando)
        elif comando[0].lexema == "InsertarUnico":
            analizarInsertarUnico(comando)
        elif comando[0].lexema == "EliminarUnico":
            analizarEliminarUnico(comando)
        elif comando[0].lexema == "ActualizarUnico":
            analizarActualizarUnico(comando)
        elif comando[0].lexema == "BuscarUnico":
            analizarBuscarUnico(comando)
        elif comando[0].lexema == "BuscarTodo":
            analizarBuscarTodos(comando)
        else:
            print("Comando que inicia con", comando[0].lexema, "no reconocido")
            error = Error(comando[0].lexema,"Sintactico", comando[0].fila, comando[0].columna, "Comando que iniciaba con " + comando[0].lexema + " no reconocido, no es ejecutable")
            listaErrores.append(error)
    print("-------------------------------------------------------------------------------------------------------------------") 

def LecturaLexemas(string):

    global linea
    global columna
    global lexema

    lexema = ''
    linea = 1 #Linea del string
    columna = 1 #Columna del string
    posString = 0 #Posicion del string

    while string:

        char = string[posString]
        posString+=1
        
        if char.isalpha():
            lexema, string = obtenerLexemaPalabra(string)
            if lexema and string:
                
                if lexema in reservadasLenguaje.values():
                    l = [lexema,get_key(lexema),linea,columna]
                    listaReservadas.append(l)
                    listaGeneral.append(l)
                    listaMostrarTokens.append(get_key(lexema))

                    # objeto lexema recopilado
                    newLexema = Lexema(lexema, get_key(lexema), linea, columna)
                    listaParalistadeComandos.append(newLexema)

                elif (('-' or '_') in lexema) and (len(lexema) != 1 and lexema[0].isalpha()):
                    l = [lexema, "IDENTIFICADOR", linea, columna]
                    listaLexemasValidos.append(l)
                    listaMostrarTokens.append('IDENTIFICADOR')
                    listaGeneral.append(l)

                    # objeto lexema recopilado
                    newLexema = Lexema(lexema, 'IDENTIFICADOR', linea, columna)
                    listaParalistadeComandos.append(newLexema)
        
                elif (len(lexema) == 1) and (lexema.isalpha()) or (len(lexema) != 1):
                     
                     l = [lexema,'IDENTIFICADOR',linea,columna]
                     listaGeneral.append(l)

                     #objeto lexema recopilado
                     newL = Lexema(lexema, 'IDENTIFICADOR', linea, columna)
                     listaParalistadeComandos.append(newL)

                columna+=len(lexema)
                posString = 0

        elif char == '\t' or char == '    ':
            columna+=4
            string = string[4:]
            posString = 0

        elif char == ' ':
            columna+=1
            string = string[1:]
            posString = 0

        elif char == '\n':
            columna = 1
            linea += 1
            string = string[1:]
            posString = 0
        
        elif char in reservadasLenguaje.values():
            
            if char == ';':
                lexema = char
                # objeto lexema recopilado
                newLexema = Lexema(lexema, get_key(lexema), linea, columna)
                listaParalistadeComandos.append(newLexema)

                print("------------Se añadio un comando a la lista de comandos-------------")
                listaComandos.append(listaParalistadeComandos.copy()) #Agrega la lista de parametros a la lista de comandos
                listaParalistadeComandos.clear() #Limpia la lista de parametros para el siguiente comando
                print("------------Se limpio la lista de parametros------------------------")
                
                lexema = char
                l = [lexema, get_key(lexema), linea, columna]
                listaLexemasCharValidos.append(l)
                listaMostrarTokens.append(get_key(lexema))
                listaGeneral.append(l)
                
                string = string[1:]
                columna+=1

            else:
                lexema = char
                l = [lexema, get_key(lexema), linea, columna]
                listaLexemasCharValidos.append(l)
                listaMostrarTokens.append(get_key(lexema))
                listaGeneral.append(l)

                # objeto lexema recopilado
                newLexema = Lexema(lexema, get_key(lexema), linea, columna)
                listaParalistadeComandos.append(newLexema)

                string = string[1:]
                columna+=1
            posString = 0

        elif char == '"' or char == "“":
            lexema = char
            l = [lexema,'COMILLAS', linea, columna]
            listaMostrarTokens.append('COMILLAS')
            listaLexemasCharValidos.append(l)
            listaGeneral.append(l)

            # objeto lexema recopilado
            newLexemaC = Lexema(lexema, 'COMILLAS', linea, columna)
            listaParalistadeComandos.append(newLexemaC)

            lexema , string = obtenerLexemaParametro(string[posString:])
            if lexema and string:
                columna+=1
                if '{' in lexema:
                    #verificarParametroJson(lexema)
                    #listaMostrarTokens.append(l)
                    listaMostrarTokens.append("PARAMETRO-JSON")
                    lexema = lexema.replace("\n", "")
                    lexema = lexema.replace("\t", "")
                    lexema = lexema.replace(" ", "")
                    #quitarle el ultimo caracter a lexema
                    lexema = lexema[:-1]
                    listaMostrarTokens.append('COMILLAS')
                    l = [lexema,'PARAMETRO-JSON', linea, columna]
                    l2 = ['"','COMILLAS', linea, columna]
                    listaLexemasValidos.append(l)
                    listaLexemasValidos.append(l2)
                    listaGeneral.append(l)
                    listaGeneral.append(l2)

                    # objeto lexema recopilado
                    newLexema = Lexema(lexema, 'PARAMETRO-JSON', linea, columna)
                    listaParalistadeComandos.append(newLexema)

                    newLex2 = Lexema('"', 'COMILLAS', linea, columna)
                    listaParalistadeComandos.append(newLex2)
                    
                    columna+=len(lexema)+1

                else: 
                    #l = [lexema,'PARAMETRO-NOMBRE', linea, columna]
                    #listaMostrarTokens.append(l)
                    listaMostrarTokens.append("PARAMETRO-NOMBRE")
                    listaMostrarTokens.append('COMILLAS')
                    l = [lexema,'PARAMETRO-NOMBRE', linea, columna]
                    l2 = ['"','COMILLAS', linea, columna]
                    listaLexemasValidos.append(l)
                    listaLexemasValidos.append(l2)
                    listaGeneral.append(l)
                    listaGeneral.append(l2)

                    newLexemaName = Lexema(lexema, 'PARAMETRO-NOMBRE', linea, columna)
                    listaParalistadeComandos.append(newLexemaName)

                    newLex2 = Lexema('"', 'COMILLAS', linea, columna)
                    listaParalistadeComandos.append(newLex2)
                    
                    columna+=len(lexema)+1

            posString = 0
        
        elif char == '/':
            subString = string[0:2]
            if subString == '/*':
                string = string[2:]
                lexema, string = obtenerComentarioMultilinea(string) 
                if lexema and string:
                    l = [lexema,'COMENTARIO-MULTILINEA', linea, columna]
                    listaLexemasValidos.append(l)
                    #listaTokens.append("COMENTARIO-MULTILINEA")
                    listaGeneral.append(l)
                    columna += len(lexema)

            else:
                lexema = char
                #l = [lexema, 'ERROR-LEXICO', linea, columna]
                #listaErrores.append(l)
                string = string[1:]

                newErrComentario = Error(lexema, 'Lexico', linea, columna, "Caracter invalido")
                listaErrores.append(newErrComentario)
                columna+=1

            posString = 0

        elif char == '-': #si el caracter es un guion, se verifica si es un comentario de una linea
            subString = string[0:3]
            if subString == '---':
                string = string[3:]
                lexema, string = obtenerComentarioUnilinea(string)
                if lexema and string:
                    l = [lexema,'COMENTARIO-UNILINEA', linea, columna]
                    listaLexemasValidos.append(l)
                    #listaTokens.append("COMENTARIO-UNILINEA")
                    listaGeneral.append(l)
                    columna += len(lexema)

            else:
                lexema = char
                #l = [lexema, 'ERROR-LEXICO', linea, columna]
                #listaErrores.append(l)
                string = string[1:]
                newErrComentario = Error(lexema, 'Lexico', linea, columna, "Caracter invalido")
                listaErrores.append(newErrComentario)
                columna+=1

            posString = 0

        else:
            lexema = char
            l = [lexema, 'ERROR-LEXICO', linea, columna]
            listaMostrarErrores.append(l)
            string = string[1:]

            newErrComentario = Error(lexema, 'Lexico', linea, columna, "Caracter invalido")
            listaErrores.append(newErrComentario)

            columna+=1
            posString = 0

text = '''

CrearBD ejemplo = nueva CrearBD();

CrearColeccion colec = nueva CrearColeccion("NombreColeccion"); --- queso

ActualizarUnico actualizadoc = nueva ActualizarUnico("NombreColeccion","
{
 "nombre" : "Obra Literaria",
 "autor" : "Jorge Luis"
 }
"); 

EliminarColeccion eliminacolec = nueva
EliminarColeccion("NombreColeccion");

--- hola mundo

/* comentario 
multilinea */ '''

text2 = '''
ActualizarUnico actualizadoc = nueva ActualizarUnico("NombreColeccion","
{
 "nombre" : "Obra Literaria",
 "autor" : "Jorge Luis"
 }
");
'''

#LecturaLexemas(text)
#imprimirTodo()
#VerComandos()""