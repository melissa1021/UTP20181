from pathlib import Path
import math
import zmq
import sys
import os

tamano_trozo = 1024*1024

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
    # Verificamos si nos envian exactamente 3 argumentos
    if len(sys.argv) < 2:
        print("Por favor ingresa las variables 1 Puerto / 2 Carpeta de archivos")
        exit()

    # Guardamos dichos argumentos en las variables, 
    # port -> puerto 
    # filesdir ->directorio de archivos 

    port = sys.argv[1]
    filesDir = sys.argv[2]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    # Se cargan todo los archivos a la variable files, por meido del procedimiento files
    files = loadFiles(filesDir)
    print(files)

    # inciamos un demonio o cliclo infinito para esperar que un socket se conecte y nos hable
    while True:
        print("Waiting for request")

        # Recibimos la peticion en un socket y o recibimos en JSON
        msg = s.recv_json()

        # De acuerdo al apeticion recibida filtramos y hacemos el proceso necesario.
        if msg["op"] == "list":
            # Se listan el total de archivos y se retornan en un JSON con clave files.
            s.send_json({"files": list(files.keys())})

        elif msg["op"] == "download":

            # Solicitud de un archivo especifico, recibe en el JSON con clave file, el nombre le archivo solicitado y se lo retorna completo al cliente.
            with open(sys.argv[2]+msg["file"],"rb") as input:
	            data = input.read()
	            s.send(data)

        elif msg["op"] == "partes":
            # Retorna la cantidad de partes que contiene un archivo, cada parte es de tamaño (tamano_trozo) para eso utiliza la funcion definida arriba 'partes'
            data = partes(sys.argv[2]+msg["file"])

            # Una vez obtenido la cantidad de partes se retornan por el mismo socket que nos hablaron
            s.send_json({"partes": data})
            
        elif  msg["op"] == "parteN":

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

if __name__ == "__main__":
    main()