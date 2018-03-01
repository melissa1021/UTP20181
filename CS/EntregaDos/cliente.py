import zmq
import sys
import os
import threading

# Se obtienen los argumentos 
#serverIp = sys.argv[1]
#serverPort = sys.argv[2]

serverIp = 'localhost'   
serverPort = 1711
nombre = ""
logueado = False
Salir = False

def menu():

    os.system("clear")
    
    print("Selecciona una opcion")
    print("\t 1.Login")
    print("\t 2.Listado de conectados")
    print("\t 3.Hablarle a...")

    print("\t 9. Salir")

#Incializacion de sockets de habla y de escucha
context = zmq.Context()
serverSocket = context.socket(zmq.REQ)
serverSocket.connect("tcp://{}:{}".format(serverIp, serverPort))

clientSocket = context.socket(zmq.REP)


def escucharServer():
    while True:
        msg = clientSocket.recv_json()
        clientSocket.send_json({"status":1})
        print(msg["mensaje"])

def menuUsuario(Salir, logueado):

    while not Salir:
        
        menu()

        print("Esperando conexion")

        opcionMenu = int(input("Por ingresa una opcion "))

        if opcionMenu == 1:
            if logueado:
                print("Ya estas logueado")
                input("Presione cualquier tecla para continuar")
            else:
                nombre = input("Ingresa tu nickname ")
                IP = input("Ingresa tu IP ")
                puerto = input("Ingresa tu Puerto ")
                serverSocket.send_json({"op":"login", "nombre":nombre, "ip":IP, "puerto": puerto})
                respuesta = serverSocket.recv_json() 
                print(respuesta["status"])
                logueado = True
                clientSocket.bind("tcp://*:{}".format(puerto))
                input("Presione cualquier tecla para continuar")

        elif opcionMenu == 2:
            serverSocket.send_json({"op":"getClientes"})
            respuesta = serverSocket.recv_json()  
            print(respuesta["clientes"])
            input("Presione cualquier tecla para continuar")
            
        elif opcionMenu == 3:
            serverSocket.send_json({"op":"getClientes"})
            respuesta = serverSocket.recv_json()  

            print("Usuarios conectados...")
            print(respuesta["clientes"])
        
            usuario = input("Ingrese el nombre del usuario ")
            mensaje = input('Escriba el mensaje a enviar ')
            # Validar si escribio algo en el mensaje
            serverSocket.send_json({"op":"setMensaje","usuario":usuario,"remitente" : nombre, "mensaje":mensaje})
            respuesta = serverSocket.recv_json() 

        elif opcionMenu == 4:
            print(opcionMenu)
            
        elif opcionMenu == 5:
            print(opcionMenu)
            
        elif opcionMenu == 6:
            print(opcionMenu)
            
        elif opcionMenu == 7:
            print(opcionMenu)
        
        elif opcionMenu == 8:
            print(opcionMenu)
        
        elif opcionMenu == 9:
            Salir = True
    

hiloMenu = threading.Thread(target=menuUsuario(Salir, logueado))
hiloMenu.start()

hiloEscucha = threading.Thread(target=escucharServer)
hiloEscucha.start()