import zmq
import sys
import os

def main():
    if len(sys.argv) != 5:
        print("Error calling the program")
        exit()

    serverIp = sys.argv[1]
    serverPort = sys.argv[2]
    operation = sys.argv[3]
    filename = sys.argv[4]

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
    elif operation == "partes":
            s.send_json({"op":"partes", "file":filename})
            files = s.recv_json()
            print(files)
    elif operation == "parteN":
            s.send_json({"op":"parteN", "numP":sys.argv[5]})
            file = s.recv()
            with open("down-"+ operation, "wb") as output:
                output.write(file)        


if __name__ == '__main__':
    main()
