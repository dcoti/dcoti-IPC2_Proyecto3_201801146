import re
import listasinteractivas
from tkinter import *
from tkinter.filedialog import askopenfilename
root = Tk()
root.withdraw()
root.update()

class Eventos:
    def __init__(self, Fecha, Usuario, Reportados, Error):
        self.Fecha = Fecha
        self.Usuario = Usuario
        self.Reportados = Reportados
        self.Error = Error

Entrada1 = ""
flagxml=False
dentcomilla=False
Salida=""
cont=0
Estado=0
Evento = None
listaEventos=[]

def AutomataUsuario(caracter):
    global dentcomilla, cont
    c = ord(caracter)
    if (ord(caracter)!=8221) & (ord(caracter)!=34) & (dentcomilla==False) & (caracter!="<") & (caracter!=">") & (ord(caracter)!=32) & (caracter!="\r"):
        return caracter
    elif ((ord(caracter)==8221) & (cont==0)) | ((ord(caracter)==34) & (cont==0)):
        dentcomilla=True
        cont=1
        return ""
    elif ((ord(caracter)==8221) & (cont==1)) | ((ord(caracter)==34) & (cont==1)):
        dentcomilla=False
        cont=0
        return ""
    elif (caracter=="<") | (caracter==">") | (ord(caracter)==32):
        return ""
    else:
        return ""

def gramaticaXML(linea):
    global Salida, Estado, flagxml, listaEventos, Evento
    if Estado==0:
        if re.match(r"[\t]*<EVENTO>",linea):
            Salida = Salida+linea+"\n"
            Estado=1
        elif re.match(r"</EVENTOS>", linea):
            Salida = Salida + linea + "\n"
            flagxml=False
        else:
            Estado=0
    elif Estado==1:
        Salida = Salida+linea+"\n"
        data=""
        for caracter in linea:
            if re.match(r"\d|\W", caracter):
                if (caracter!="\t") & (caracter!=",") & (ord(caracter)!=32) & (caracter!="<") & (caracter!=">") & (caracter!="\r"):
                    data = data + caracter
        Evento = Eventos(data, "", "", "")
        #listaFecha.append(data)
        Estado=2
    elif Estado==2:
        if re.match(r"[\t]*Reportado por:", linea):
            data=""
            for caracter in linea:
                if (caracter=="<") or (caracter==">") or (caracter=="\""):
                    pass
                else:
                    data = data + caracter
            Salida = Salida + data + "\n"
            flagusuario=False
            data=""
            for caracter in linea:
                if caracter==":":
                    flagusuario=True
                elif flagusuario:
                    result = AutomataUsuario(caracter)
                    data = data + result
        Evento.Usuario = data
        #listaUsuario.append(data)
        Estado=3
    elif Estado==3:
        if re.match(r"[\t]*Usuarios afectados:", linea):
            data = ""
            for caracter in linea:
                if (caracter=="<") | (caracter==">") | (caracter=="\""):
                    pass
                else:
                    data = data + caracter
            Salida = Salida + data + "\n"
            flagafectado=False
            data = ""
            for caracter in linea:
                if caracter==":":
                    flagafectado=True
                elif flagafectado:
                    result = AutomataUsuario(caracter)
                    data = data + result
            Evento.Reportados = data.split(",")
            #listaReportado.append(data.split(","))
            Estado=4
    elif Estado==4:
        if re.match(r"[\t]*Error:", linea):
            Salida = Salida + linea + "\n"
            data=""
            cont=0
            for caracter in linea:
                if re.match(r"\d", caracter):
                    if (ord(caracter)!=32) & (caracter!="-") & (caracter!="\r"):
                        data = data + caracter
                        cont=1
                elif ((ord(caracter)==32) | (ord(caracter)==95) | (ord(caracter)==45)) & (cont==1):
                    break
            Evento.Error = data
            #listaErrores.append(data)
            Estado=5
    elif Estado==5:
        if re.match(r"[\t]*</EVENTO>", linea):
            Salida = Salida + linea + "\n"
            listaEventos.append(Evento)
            Evento = None
            Estado=0
        else:
            Salida = Salida + linea + "\n"
            Estado = 5

def regresionActual(Entrada):
    global flagxml, Salida, Estado
    for linea in Entrada:
        if flagxml:
            gramaticaXML(linea)
        elif re.match(r"<EVENTOS>", linea):
            Salida = linea+"\n"
            Estado=0
            flagxml=True
    return Salida

def AbrirArchivo(Entrada):
    global listaEventos
    Entrada1 = Entrada.split("\n")
    regreso = regresionActual(Entrada1)
    listasinteractivas.listar(listaEventos)
    listasinteractivas.generarxml()
    return regreso

#def app():
#    ruta = askopenfilename(filetypes=[("Abrir Menú", "*.xml")])
#    if ruta == "":
#        print("No se eligio ningun menu")
#    else:
#        file = open(ruta, encoding='UTF-8')
#        data = file.read()
#        origen = AbrirArchivo(data)
        #print(origen)

#app()