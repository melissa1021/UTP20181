from pathlib import Path
import math
import zmq
import sys
import os

tamano_trozo = 1024

def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loading {}".format(filename))
        files[filename] = file
    return files

def partes(localPath):
    #Retorna el tamano el megas
    b = os.path.getsize(localPath)
    return math.ceil(b/(1024*1024))

def main():
    if len(sys.argv) != 3:
        print("Error calling the program")
        exit()

    port = sys.argv[1]
    filesDir = sys.argv[2]

    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:{}".format(port))

    files = loadFiles(filesDir)
    print(files)

    while True:
        print("Waiting for request")
        msg = s.recv_json()
        if msg["op"] == "list":
            s.send_json({"files": list(files.keys())})
        elif msg["op"] == "download":
            with open(sys.argv[2]+msg["file"],"rb") as input:
	            data = input.read()
	            s.send(data)
        elif msg["op"] == "partes":
            data = partes(sys.argv[2]+msg["file"])
            s.send_json({"partes": data})
        elif  msg["op"] == "parteN":
            with open(sys.argv[2]+msg["file"],"rb") as input:
                if nmsg["numP"] == "0":
                        data = input.read(tamano_trozo)
                else:
                    posicion = sys.argv[5]*tamano_trozo
                    input.seek(posicion)
                    data = input.read(tamano_trozo)
                    
                s.send(data)
            

if __name__ == "__main__":
    main()