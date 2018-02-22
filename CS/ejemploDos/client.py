import zmq
import sys
import os
import md5

tamanoTrozo = (1024*1024)

def main():
    if len(sys.argv) < 2:
        print("Error calling the program")
        exit()

    serverIp = sys.argv[1]
    serverPort = sys.argv[2]
    operation = sys.argv[3]
    filename = sys.argv[4]
    #parteDescargar = 0

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(serverIp, serverPort))

    if operation == "list":
        print('entro a list')
        s.send_json({"op": "list"})
        files = s.recv_json()
        print(files)

    elif operation == "download":
            s.send_json({"op":"download", "file":filename})
            file = s.recv()
            with open("down-"+ operation, "wb") as output:
                output.write(file)

    elif operation == "descargapartes":

            listadoDescarga = []

            s.send_json({"op":"partes", "file":filename})
            files = s.recv_json()
            cantidad = files["partes"]
            destino = "final" + filename

            for x in range(0, cantidad):
                s.send_json({"op":"parteN", "file":filename, "numP":x})
                file = s.recv()
                with open(destino, "ab") as dest:
                    dest.write(file)

    elif operation == "partes":
            s.send_json({"op":"partes", "file":filename})
            files = s.recv_json()
            print(files)

    elif operation == "parteN":
            s.send_json({"op":"parteN", "file":filename, "numP":parteDescargar})
            file = s.recv()
            with open("{} part{}".format(filename, parteDescargar), "wb") as output:
                output.write(file)


if __name__ == '__main__':
    main()