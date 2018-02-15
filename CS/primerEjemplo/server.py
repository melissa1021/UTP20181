import zmq
import sys
import os

def loadFiles(path):
    files = {}
    dataDir = os.fsencode(path)
    for file in os.listdir(dataDir):
        filename = os.fsdecode(file)
        print("Loading {}".format(filename))
        files[filename] = file
    return files

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
        else:
            print("Operacion no implementada")

if __name__ == "__main__":
    main()
