#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

if len(sys.argv) != 3:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")
try:
    login = sys.argv[2].split('@')[0]
    server = sys.argv[2].split('@')[1].split(':')[0]
    port = int(sys.argv[2].split(':')[-1])
    metodo = sys.argv[1]
    peticion = metodo + " sip:" + login + "@" + server + " SIP/2.0\r\n\r\n"

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((server, port))

    print("Enviando:", peticion)  
    my_socket.send(bytes(peticion, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    list_rec = data.decode('utf-8').split()
    if list_rec[1] == "100" and list_rec[4] == "180" and list_rec[7] == "200":
        metodo = "ACK"
        peticion = metodo + " sip:" + login + "@" + server + " SIP/2.0\r\n\r\n"
        print("Enviando", peticion)
        my_socket.send(bytes(peticion, 'utf-8') + b'\r\n')
    print("Terminando socket...")

    # Cerramos todo
    my_socket.close()
    print("Fin.")
except:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")
        
