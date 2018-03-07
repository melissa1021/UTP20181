import zmq
import sys
import os
import threading
import pyaudio
import wave
import datetime


def main():
    # Se obtienen los argumentos 
    #serverIp = sys.argv[1]
    #serverPort = sys.argv[2]

    #Declaracion de variables globales
    serverIp = 'localhost'   
    serverPort = 1711
    Login = False
    CHUNK = 1024*10
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    mensajes = []

    #Incializacion de sockets de habla y de escucha
    context = zmq.Context()
    serverSocket = context.socket(zmq.REQ)
    serverSocket.connect("tcp://{}:{}".format(serverIp, serverPort))

    clientSocket = context.socket(zmq.REP)

    poller = zmq.Poller()
    poller.register(clientSocket, zmq.POLLIN)
    poller.register(sys.stdin, zmq.POLLIN)
    
    def menu(pr_Login):
       
        os.system("clear")
        if not pr_Login:
            print("\t 1.Login")
        else:
            print("\t 2.Listado de conectados")
            print("\t 3.Enviar texto...")
            print("\t 4.Enviar nota de voz...")
            print("\t 9. Salir")

        print("\n")
        print(mensajes)
        print("\t Ingresa una opcion..")

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

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    
        frames = []
        RECORD_SECONDS = int(input("Cuantos segundos quiere grabar"))
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Grabacion terminada")

        stream.stop_stream()
        stream.close()
        p.terminate()

        return frames

 
    def menuUsuario(Login):

 
        while True:
            
            menu(Login)

            avisoSistema = dict(poller.poll())

            if clientSocket in avisoSistema:   
                     
                msg = clientSocket.recv_json()
                
                if msg["tipo"] == "txt":   
                    mensajes.append(msg["mensaje"])
                else:
                    mensajes.append(msg["remitente"]+" envio un archivo de audio.")
                    reproducirSonido(msg["mensaje"])

                clientSocket.send_json({"status":1})
            
            if sys.stdin.fileno() in avisoSistema: 

                opcionMenu =  int(input())

                if opcionMenu == 1:
                    
                    if Login:
                        print("Ya estas logueado")
                        input("Presione cualquier tecla para continuar")
                    else:
                        nombre = input("Ingresa tu nickname ")
                        IP = input("Ingresa tu IP ")
                        puerto = input("Ingresa tu Puerto ")
                        serverSocket.send_json({"op":"login", "nombre":nombre, "ip":IP, "puerto": puerto})
                        respuesta = serverSocket.recv_json() 
                        if respuesta["status"] == 1:
                            print("Ahora estas conectado..")
                            Login = True
                        else:
                            Login = False
                   
                        clientSocket.bind("tcp://*:{}".format(puerto))

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
                    sys.exit()
            else:
                print("Descarto ambos")

    menuUsuario(False)

    
if __name__ == '__main__':
    main()