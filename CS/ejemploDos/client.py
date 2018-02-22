import zmq
import sys
import os

# Tamaño del trozo o porcion de bit que vamos a pasar por red,
tamanoTrozo = (1024*1024)

def main():
    # Se verifica que existan por lo menos cuatro parametros IP Puerto MetodoOperacion NombreArchivo
    if len(sys.argv) < 4:
        print("Verifica que existan por lo menos cuatro parametros IP Puerto MetodoOperacion NombreArchivo")
        exit()

    # Se obtienen los argumentos 
    serverIp = sys.argv[1]
    serverPort = sys.argv[2]
    operation = sys.argv[3]
    filename = sys.argv[4]

    # Conexion con el servidor de sockets
    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(serverIp, serverPort))

    # Se verifica cual fue el metodo u operacion que el cliente solicito para enviar esto al servidor
    if operation == "list":
        # Opcion list envia al servidor la petición de listar todos los archivos de carpeta en que inicio y me los imprima en consola.
        s.send_json({"op": "list"})
        files = s.recv_json()
        print(files)

    elif operation == "download":
        #Opcion de descargar un archivo especifico, le debemos enviar al servidor el nombre del archivo y me lo pone en la carpeta raiz que me entrego el cliente.
            s.send_json({"op":"download", "file":filename})
            file = s.recv()
            with open("down-"+ operation, "wb") as output:
                output.write(file)

    elif operation == "descargapartes":
        # Descargar partes primero le envia al servidor la peticion de conocer de cuantas partes se compone el archivo, 
        # luego hacemos un for desde la parte 0 a la N solicitando cada una de sus partes y las vamos uniendo para obtener 
        # el total del archivo. Se realiza de esta manera para no saturar el servidor y que este pueda ir entragando parte 
        # por parte a cada cliente que solicita.

        # Solicitud de cantidad de partes que se guarda en la variable cantidad
            s.send_json({"op":"partes", "file":filename})
            files = s.recv_json()
            cantidad = files["partes"]

        # Guardamos el archivo por partes con la palabra  "Final" adelante.
            destino = "final" + filename

        # Se hace un recorrido desde la parte 0 a la N, se hace la peticion de cada parte al servidor, 
        # una vez este contesta nos retorna el binario con esa parte solicitada
        # la vamos "pegando" al final del binario para al final obtener el total

            for x in range(0, cantidad):
                # Solicitud de cada una de las partes
                s.send_json({"op":"parteN", "file":filename, "numP":x})
                # Binario de la parte solicitada
                file = s.recv()
                
                # Abrimos el archivo final y le pegamos al final el binario recibido hasta obtener el total
                with open(destino, "ab") as dest:
                    dest.write(file)


if __name__ == '__main__':
    main()