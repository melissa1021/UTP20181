from pathlib import Path
import math
import zmq
import sys
import os

tamano_trozo = 1024*1024
conectados = {}


def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loading {}".format(filename))
        files[filename] = file
    return files

def partes(localPath):
    # Retorna el tamano del archivo buscado, para ello utiliza os.path.getSize eso me retorna el total de bits, 
    # luego lo dividimos para obtener el total de megas y pasar por red una mega a la vez y no saturar el servidor
    b = os.path.getsize(localPath)
    return math.ceil(b/(1024*1024))

def main():
    '''
    # Verificamos si nos envian exactamente 3 argumentos
    if len(sys.argv) < 2:
        print("Por favor ingresa las variables 1 Puerto / 2 Carpeta de archivos")
        exit()

    # Guardamos dichos argumentos en las variables, 
    # port -> puerto 
    # filesdir ->directorio de archivos 

    #port = sys.argv[1]
    '''
    port = 1711
 
    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))



    # inciamos un demonio o cliclo infinito para esperar que un socket se conecte y nos hable
    while True:
        print("Esperando conexion")

        # Recibimos la peticion en un socket y o recibimos en JSON
        msg = s.recv_json()
        
        # Recibe la opcion
        opcion =  msg["op"]

        # De acuerdo al apeticion recibida filtramos y hacemos el proceso necesario.
        if opcion == "login":
            print(msg["nombre"])
            ipCliente = msg["ip"]
            puertoCliente = msg["puerto"]
            socketCliente = context.socket(zmq.REQ)
            socketCliente.connect("tcp://{}:{}".format(ipCliente, puertoCliente))

            conectados[msg["nombre"]] = socketCliente
            s.send_json({"status": 1})

        elif opcion == "getClientes":
            print(conectados.keys())
            s.send_json({"clientes": str(conectados.keys()), "status": 1})

        elif opcion == "sendMensaje":
            destinatario = conectados.get(msg["usuario"])

            mensajeDestinatario = msg["mensaje"]
            print(msg["remitente"]+" dice: "+mensajeDestinatario)
            destinatario.send_json({"mensaje": msg["remitente"]+" dice :"+mensajeDestinatario, "tipo" : "txt"})
            s.send_json({"status": 1})
            destinatario.recv_json() 

        elif opcion == "sendAudio":
            destinatario = conectados.get(msg["usuario"])

            mensajeDestinatario = msg["mensaje"]
            destinatario.send_json({"remitente" : msg["remitente"], "mensaje": mensajeDestinatario, "tipo" : "audio"})
            s.send_json({"status": 1})
            destinatario.recv_json() 

        elif opcion == "desconectar":

            # Para no saturar el servidor y dar la impresion de concurrencia, se pediran los archivos por trozos, 
            # para ello el cliente nos pedira el numero del trozo que quiere y se lo retornaremos como binario, es responsabilidad del cliente unir nuevamente los trozos
            with open(sys.argv[2]+msg["file"],"rb") as input:

                # En caso del que este solicitando el primer trozo se hace un read desde 0 por defecto hasta tamano_trozo
                if msg["numP"] == "0":
                    data = input.read(tamano_trozo)
                else:
                
                # Cuando es un trozo diferente se parsea el numero a int se multiplica por el tamaño de cada trozo, 
                # luego se busca con input.seek donde esta ubicado esa porcion de bits y se retorna al cliente.
                    posicion = int(msg["numP"])*tamano_trozo
                    input.seek(posicion)
                    data = input.read(tamano_trozo)

                s.send(data)

        elif opcion == "notificarTodos":
            print("Seamos optimistas")


if __name__ == "__main__":
    main()