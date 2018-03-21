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
    #Login = False
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
            print("\t 5.Realizar llamada...")
            print("\t 9. Salir")

        print("\n")
        print("\t".join(mensajes)+"\n")
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

    def grabarAudio():
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) 
        frames = []
        RECORD_SECONDS = 3
        #RECORD_SECONDS = int(input("Cuantos segundos quiere grabar "))
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Grabacion terminada")
        stream.stop_stream()
        stream.close()
        p.terminate()
        return frames

    def grabarAudiollamada():
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) 
        frames = []
        RECORD_SECONDS = 3
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
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
                    listadoClientes = respuesta["clientes"]
                    print(listadoClientes)
                
                    usuario = input("Ingrese el nombre del usuario ")
                    if usuario in listadoClientes:
                        mensaje = input('Escriba el mensaje a enviar ')
                        # Validar si escribio algo en el mensaje
                        serverSocket.send_json({"op":"sendMensaje","usuario":usuario,"remitente" : nombre, "mensaje":mensaje})
                        respuesta = serverSocket.recv_json() 
                    else:
                        print("Por favor elije un usuario valido...")
                        input("Presiona cualquier tecla para continuar...")

                elif opcionMenu == 4:
                    serverSocket.send_json({"op":"getClientes"})
                    respuesta = serverSocket.recv_json()  

                    print("Usuarios conectados...")
                    listadoClientes = respuesta["clientes"]
                    print(listadoClientes)
                    usuario = input("Ingrese el nombre del usuario ")

                    if usuario in listadoClientes:
                        mensaje = grabarAudio()
                        
                        serverSocket.send(mensaje)
                        respuesta = serverSocket.recv() 
                        #serverSocket.send_json({"op":"sendAudio","usuario":usuario,"remitente" : nombre, "mensaje":open(mensaje)})
                        #respuesta = serverSocket.recv_json() 
                    else:
                        print("Por favor elije un usuario valido...")
                        input("Presiona cualquier tecla para continuar...")
                
				#Opcion para hacer una llamada   
				
                elif opcionMenu == 5:
                    #obtiene el listado de clientes e imprime los usuarios conectados
                    serverSocket.send_json({"op":"getClientes"})
                    respuesta = serverSocket.recv_json()  

                    print("Usuarios conectados...")
                    listadoClientes = respuesta["clientes"]
                    print(listadoClientes)
                    #Se ingresa el usuario con el que se desea realizar la llamada
                    usuario = input("Ingrese el nombre del usuario ")

                    if usuario in listadoClientes:
                        llamada = True 
                        #Se crea un ciclo para que envie audios cada 3 segundos
                        while(llamada == 'true'):						
                            mensaje=""
                            mensaje = grabarAudio()
                            serverSocket.send("sendAudio-"+nombre+"-"+mensaje)
                            respuesta = serverSocket.recv()
                            input("Presiona una tecla para finalizar la llamada")
                            if input != "":
                                llamada = False
                    else:
                        print("Por favor elije un usuario valido...")
                        input("Presiona cualquier tecla para continuar...")
                    
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