from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as MessageBox
import os

from analizadores import *

class VentanaInicial():

    def __init__(self):
        self.Ventana = Tk()
        self.Ventana.geometry("850x530")
        self.Ventana.resizable(0,0)
        self.Ventana.title("Proyecto 2 - LFP")
        self.Ventana.config(bg="#33FF90")

        #funciones de los botones
        def abrirArchivo():
            #metodo para abrir un archivo con explorador de archivos
            self.txtArea.delete("1.0",END)
            self.archivo = filedialog.askopenfilename(initialdir = "/",title = "Abrir Archivo para analisis",filetypes = (("Archivos txt","*.txt"),("Archivos json","*.json"),("Archivos lfp","*.lfp")))
            #print(self.archivo)
            try:
                self.archivo = open(self.archivo, "r")
                self.contenido = self.archivo.read()
                #print(self.contenido)
                self.txtArea.insert(INSERT,self.contenido)
                self.archivo.close()
            except: 
                MessageBox.Message("Advertencia","No se pudo abrir el archivo")
        
        def limpiarCajadeTexto():
            self.contenido = self.txtArea.get("1.0",END)
            if self.contenido == "\n" or self.contenido == None:
                MessageBox.showwarning(message="No hay contenido para limpiar", title="Advertencia")
            else:
                MessageBox.askyesno("Advertencia","¿Desea guardar el contenido?")
                if MessageBox == "yes":
                    guardarArchivo()
                else:
                    self.txtArea.delete("1.0",END)

        def guardarArchivo():
            #metodo para guardar un archivo con explorador de archivos
            self.archivo = filedialog.asksaveasfilename(initialdir = "/",title = "Guardar Archivo",filetypes = (("Archivos txt","*.txt"),("Archivos json","*.json"),("Archivos lfp,","*.lfp")))
            print(self.archivo)
            try:
                self.archivo = open(self.archivo, "w")
                self.contenido = self.txtArea.get("1.0",END)
                self.archivo.write(self.contenido)
                self.archivo.close()
            except: 
                MessageBox.Message("Advertencia","No se pudo guardar el archivo")

        def cerrarApp():
           #cierra la app
           self.Ventana.quit()

        def dialogAnalizador():
          MessageBox.showwarning(message="No hay nada que analizar", title="Advertencia")

        def escribirArchivo():   
            try:
                file = open("comandosMongoDB.txt","w")
                h = 1
                file.write("---------------Comandos validos para MongoDB---------------\n")
                if len(listaMongoDB) == 0:
                    file.write("No hay comandos validos\n")
                else:
                    for comando in listaMongoDB:
                        file.write(str(h)+"). "+comando)
                        file.write('\n')
                        h+=1
                file.close()
                MessageBox.showinfo(message="Se escribio el archivo", title="Informacion")
                os.system("comandosMongoDB.txt")
            except:
                MessageBox.showwarning(message="No se pudo escribir el archivo", title="Advertencia")

        def outPutComandosYArchivo():

            if len(listaMongoDB) == 0:
                self.txtOutput.insert(INSERT,'sin comandos validos, revise su entrada')
                self.txtOutput.insert(INSERT,'\n')
            else:
                for comando in listaMongoDB:
                    self.txtOutput.insert(INSERT,comando)
                    self.txtOutput.insert(INSERT,'\n')

            escribirArchivo()

        def analizarArchivo():

            #limpiar el txt output
            self.txtOutput.delete("1.0",END)
            self.contenido = self.txtArea.get("1.0",END)
            self.contenido+='\n'
            
            #limpiar todas las listas
            listaErrores.clear()
            listaLexemasValidos.clear()
            listaMostrarTokens.clear()
            listaReservadas.clear()
            listaGeneral.clear()
            listaLexemasCharValidos.clear()
            listaParalistadeComandos.clear()
            listaComandos.clear()
            listaMostrarErrores.clear()
            listaMongoDB.clear()

            if self.contenido == "\n\n":
                dialogAnalizador()
            else:    
                LecturaLexemas(self.contenido)
                imprimirTodo()
                VerComandos()

                #Escribir el archivo aqui y abrirlo, tambien mostrarlo en el txt output
                outPutComandosYArchivo()
                MessageBox.showinfo(message="Se realizo todo el analisis", title="Informacion")

        #abrir una ventana de ayuda y esconder la ventana inicial
        def cerrarVenErrores():
            self.Ventana.deiconify()
            self.VentanaErrores.destroy()

        def cerrarVenTokens():
            self.Ventana.deiconify()
            self.VentanaTokens.destroy()

        def ventVerErrores():
            self.Ventana.withdraw()
            self.VentanaErrores = Toplevel()
            self.VentanaErrores.geometry("920x500")
            self.VentanaErrores.resizable(0,0)
            self.VentanaErrores.title("Errores")
            self.VentanaErrores.config(bg="#06CC21")
            self.VentanaErrores.protocol("WM_DELETE_WINDOW", cerrarVenErrores)

            self.treeE = ttk.Treeview(self.VentanaErrores, columns=("Numero","Valor","Tipo","Descripcion"), show='headings')
            self.treeE.column("Numero", width=150, minwidth=150, stretch=NO)
            self.treeE.column("Valor", width=150, minwidth=150, stretch=NO)
            self.treeE.column("Tipo", width=150, minwidth=150, stretch=NO)
            self.treeE.column("Descripcion", width=450, minwidth=450, stretch=NO)
            self.treeE.heading("Numero", text="Numero")
            self.treeE.heading("Valor", text="Valor")
            self.treeE.heading("Tipo", text="Tipo")
            self.treeE.heading("Descripcion", text="Descripcion")
            self.treeE.pack()
            self.treeE.place(x=10, y=10,height=480,width=902)

            c = 1
            copiaListaErrores = listaErrores.copy()
            for error in copiaListaErrores:
                #lista errores es una lista de objetos errores
                self.treeE.insert("", END, values=(c,error.lexema,error.tipo,error.descripcion))
                c+=1
            
        def ventVerTokens():
            self.Ventana.withdraw()
            self.VentanaTokens = Toplevel()
            self.VentanaTokens.geometry("620x500")
            self.VentanaTokens.resizable(0,0)
            self.VentanaTokens.title("Tokens")
            self.VentanaTokens.config(bg="#06CC21")
            self.VentanaTokens.protocol("WM_DELETE_WINDOW", cerrarVenTokens)

            #la tabla de tokens 
            self.tree = ttk.Treeview(self.VentanaTokens, columns=("Numero","Lexema", "Token", "Fila", "Columna"), show='headings')
            self.tree.column("Numero", width=120, minwidth=120, stretch=NO)
            self.tree.column("Lexema", width=120, minwidth=120, stretch=NO)
            self.tree.column("Token", width=120, minwidth=120, stretch=NO)
            self.tree.column("Fila", width=120, minwidth=120, stretch=NO)
            self.tree.column("Columna", width=120, minwidth=120, stretch=NO)
            self.tree.heading("Numero", text="Numero")
            self.tree.heading("Lexema", text="Lexema")
            self.tree.heading("Token", text="Token")
            self.tree.heading("Fila", text="Fila")
            self.tree.heading("Columna", text="Columna")
            self.tree.pack()
            self.tree.place(x=10, y=10,height=480,width=602)

            c = 1
            for lista in listaGeneral:
                self.tree.insert("",END,values=(c,lista[0],lista[1],lista[2],lista[3]))
                c+=1    

        self.bttnAbrir= Button(self.Ventana, text="Abrir Archivo",font="Sans-serif",border= 2,background="#06CC21",foreground="black", command=abrirArchivo)
        self.bttnAbrir.pack()
        self.bttnAbrir.place(x=10, y=10,height=30,width=130)

        self.bttnGuardar = Button(self.Ventana, text="Guardar Archivo",font="Sans-serif",background="#06CC21",foreground="black", command=guardarArchivo)
        self.bttnGuardar.pack()
        self.bttnGuardar.place(x=140, y=10,height=30,width=130)

        self.bttnLimpiar = Button(self.Ventana, text="Limpiar",font="Sans-serif",background="#06CC21",foreground="black",command = limpiarCajadeTexto)
        self.bttnLimpiar.pack()
        self.bttnLimpiar.place(x=270, y=10,height=30,width=100)

        self.bttnAnalizar = Button(self.Ventana, text="Analizar",font="Sans-serif",background="#06CC21",foreground="black",command=analizarArchivo) #Assignar comando
        self.bttnAnalizar.pack()
        self.bttnAnalizar.place(x=370, y=10,height=30,width=120)
        
        self.bttnErr = Button(self.Ventana, text="Errores",font="Sans-serif",background="#06CC21",foreground="black",command=ventVerErrores) #Assignar comando
        self.bttnErr.pack()
        self.bttnErr.place(x=490, y=10,height=30,width=100)

        self.bttnTokens = Button(self.Ventana, text="Tokens",font="Sans-serif",background="#06CC21",foreground="black",command=ventVerTokens) #Assignar comando
        self.bttnTokens.pack()
        self.bttnTokens.place(x=590, y=10,height=30,width=100)

        self.bttnExit = Button(self.Ventana, text="Salir",font="Sans-serif",background="#06CC21",foreground="black", command=cerrarApp)
        self.bttnExit.pack()
        self.bttnExit.place(x=740, y=10,height=30,width=100)

        self.txtArea = Text(self.Ventana)
        self.txtArea.pack()
        self.txtArea.place(x=10, y=50,height=470,width=550)

        self.txtOutput = Text(self.Ventana)
        self.txtOutput.pack()
        self.txtOutput.place(x=570, y=50,height=470,width=270)