import zmq
import sys
import os

context = zmq.Context()
poller = zmq.Poller()
poller.register(sys.stdin, zmq.POLLIN)
n = 1

while n < 3:
    
    n += 1
    
    avisoSistema = dict(poller.poll())
    tecladoOk = avisoSistema.get(sys.stdin.fileno(),False)

    print(tecladoOk)
    if sys.stdin.fileno() in avisoSistema:
        print("Teclado")
    else:
        print("No fileno ")
    
    if sys.stdin.read in avisoSistema:
        print("Teclado")
    else:
        print("No read ")
    
    if sys.stdin.readable in avisoSistema:
        print("Teclado")
    else:
        print("No readable ")

    if sys.stdin.readline in avisoSistema:
        print("readline")
    else:
        print("No readline ")

    if sys.stdin.buffer in avisoSistema:
        print("buffer")
    else:
        print("No buffer ")

    
