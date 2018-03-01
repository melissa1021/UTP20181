import zmq
import sys
import os
import threading
import pyaudio
import wave
import datetime

# Se obtienen los argumentos 
#serverIp = sys.argv[1]
#serverPort = sys.argv[2]

#Declaracion de variables globales
serverIp = 'localhost'   
serverPort = 1711
nombre = ""
logueado = False
Salir = False
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def menu():

    os.system("clear")
    
    print("Selecciona una opcion")
    print("\t 1.Login")
    print("\t 2.Listado de conectados")
    print("\t 3.Enviar texto...")
    print("\t 4.Enviar nota de voz...")

    print("\t 9. Salir")

#Incializacion de sockets de habla y de escucha
context = zmq.Context()
serverSocket = context.socket(zmq.REQ)
serverSocket.connect("tcp://{}:{}".format(serverIp, serverPort))

clientSocket = context.socket(zmq.REP)

def reproducirSonido(pr_Audio):
    
    print("Reproducir audio "+pr_Audio)

    wf = wave.open(pr_Audio, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()


def grabarAudio(pr_Nombre):

    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = pr_Nombre+".wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Grabando")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return WAVE_OUTPUT_FILENAME

def escucharServer():
    while True:

        msg = clientSocket.recv_json()

        if msg["tipo"] == "txt":   
            print("\n##############\n")
            print(msg["mensaje"])
            print("\n##############\n")
            print("Ingresa una opcion: ")
        else:
            reproducirSonido(msg["mensaje"])

        clientSocket.send_json({"status":1})

def menuUsuario(Salir, logueado):

    while not Salir:
        
        menu()
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
            serverSocket.send_json({"op":"sendMensaje","usuario":usuario,"remitente" : nombre, "mensaje":mensaje})
            respuesta = serverSocket.recv_json() 

        elif opcionMenu == 4:
            serverSocket.send_json({"op":"getClientes"})
            respuesta = serverSocket.recv_json()  

            print("Usuarios conectados...")
            print(respuesta["clientes"])

            fechaHora = datetime.datetime.now()
            usuario = input("Ingrese el nombre del usuario ")
            mensaje = grabarAudio(nombre+"_a_"+usuario+str(fechaHora.month)+str(fechaHora.hour)+str(fechaHora.second))
      
            #grabarAudio("audioPrueba")
            # Validar si escribio algo en el mensaje
            serverSocket.send_json({"op":"sendAudio","usuario":usuario,"remitente" : nombre, "mensaje":mensaje})
            respuesta = serverSocket.recv_json() 
            
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
    

hiloEscucha = threading.Thread(target=escucharServer)
hiloEscucha.daemon = True
hiloEscucha.start()

hiloMenu = threading.Thread(name = "menuInicio", target=menuUsuario, args = (Salir, logueado))
hiloMenu.start()