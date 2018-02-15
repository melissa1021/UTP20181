import zmq
import sys

def main():
    if len(sys.argv) != 4:
        print("Error calling the program")
        exit()
    serverIp = sys.argv[1]
    serverPort = sys.argv[2]
    operation = sys.argv[3]

    context = zmq.Context()
    s = context.socket(zmq.REQ)
    s.connect("tcp://{}:{}".format(serverIp, serverPort))

    if operation == "list":
        s.send_json({"op": "list"})
        files = s.recv_json()
        print(files)
    else:
        print("Unsupported operation")

if __name__ == '__main__':
    main()
