from flask import Flask, redirect, render_template, request, Response
from flask_cors import CORS
import base64
import EntradasXML as xml
import listasinteractivas
import os
from flask import jsonify

salida=None
alterado=None
retornousuario=None
retornoerror=None
app = Flask(__name__)
cors = CORS(app, resourse={r"/*": {"origin": "*"}})

@app.route('/')
def init():
    return redirect('inicio')

@app.route('/inicio')
def inicio():
    return render_template('Inicio.html')

@app.route('/abrirArchivo', methods=['POST'])
def abrirArchivo():
    global salida, alterado
    salida=""
    datos = request.get_json()
    if datos['data'] == '':
        return {"msg": 'Error en contenido'}
    contenido = base64.b64decode(datos['data']).decode('utf-8')
    salida=contenido
    print(salida)
    alterado = xml.AbrirArchivo(salida)
    return salida

@app.route('/abrirArchivo', methods=['GET'])
def get_events():
    global alterado
    data = alterado
    return Response(response=data,
                    mimetype='text/plain',
                    content_type='text/plain')

#metodo para llamar al xml
@app.route('/llamarxml', methods=['GET'])
def llamar():

    archivoentrante = open('estadistica.xml', 'r')
    lecturaxml = archivoentrante.read()
    archivoentrante.close()

    return Response(lecturaxml, mimetype='text/xml')

#metodo para borrar listas y archivos
@app.route('/borrar', methods=['GET'])
def borrar():
    xml.listaEventos=[]
    listasinteractivas.listaux2=[]
    listasinteractivas.listaux1=[]
    listasinteractivas.fechas=[]
    listasinteractivas.usuarios=[]
    listasinteractivas.Afectados=[]
    listasinteractivas.errores=[]
    os.remove('estadistica.xml')

    return Response('Se ha resetado el servidor', mimetype='text/plain')

#@app.route('/pruebafalla', methods=['POST', 'GET'])
#def prueba():
#    fech = request.data.decode("utf-8")
#    print(fech)
#    return Response(fech, mimetype='text/plain')

#ruta para pedir la fecha e iterar los usuarios
@app.route('/peticionuser', methods=['POST', 'GET'])
def usuario():
    global retornousuario
    if retornousuario!=None:
        retornousuario=None
    fecha = request.data.decode('utf-8')
    lista = listasinteractivas.usuarioxfecha(fecha)
    user=[]
    cont=[]
    for list in lista:
        user.append(list.user)
        cont.append(list.cant)
    retornousuario = {'usuario': user,
                      'contador': cont,
                      'type': 'bar'
               }

    print(user)
    print(cont)

    return jsonify(retornousuario)

@app.route('/graficauser', methods=['GET'])
def graficauser():
    global retornousuario

    return jsonify(retornousuario)

#ruta para pedir la fecha e iterar los errores
@app.route('/peticionerror', methods=['POST', 'GET'])
def error():
    global retornoerror
    if retornoerror!=None:
        retornoerror=None
    fecha = request.data.decode('utf-8')
    lista = listasinteractivas.errorxfecha(fecha)
    user=[]
    cont=[]
    for list in lista:
        user.append(list.user)
        cont.append(list.cant)

    retornoerror = {'usuario': user,
                    'contador': cont,
                    'type': '"linear"'
               }

    print(user)
    print(cont)

    return jsonify(retornoerror)

@app.route('/graficaerror', methods=['GET'])
def graficaerror():
    global retornousuario

    return jsonify(retornousuario)


#ruta para abrir la documentacion oficial
@app.route('/documentacion', methods=['GET'])
def documentacion():

    os.startfile('ENSAYO-PROYECTO3-IPC2.pdf')

    return 'documentacion abierta'

if __name__ == '__main__':
    #app.run(threaded=True,port=5000)
    app.run(debug=True)