#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            lista = line.decode('utf-8').split()
            print("El cliente nos manda " + line.decode('utf-8'))
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

                if lista[0] == "INVITE":
                    self.wfile.write(b"\r\n" + b"SIP/2.0 100 Trying" + b"\r\n" + 
                                     b"SIP/2.0 180 Ring" + b"\r\n" + b"SIP/2.0 Ok" +
                                     b"\r\n")
                elif lista[0] == "BYE":
                    self.wfile.write(b" SIP/2.0 Ok" + b"\r\n")
                elif line[0] != "INVITE" or "ACK" or "BYE":
                    self.wfile.write(b" SIP/2.0 405 Method Not Allowed")


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
        ip = sys.argv[1]
        serv = socketserver.UDPServer((ip, port), EchoHandler)
        print("Lanzando servidor UDP de eco...")
        serv.serve_forever()
    else:
        sys.exit("Usage: python server.py IP port audio_file")
