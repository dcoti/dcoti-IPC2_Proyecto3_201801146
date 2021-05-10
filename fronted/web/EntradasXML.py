Salida2 = ""

def AbrirArchivo(Entrada):
    global Salida2
    Salida2 = Entrada
    for evento in Entrada:
        print(evento)