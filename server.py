#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print("El cliente nos manda " + line.decode('utf-8'))
            lista = line.decode('utf-8')
            (metodo, direccion, sip) = lista.split()
            if metodo == "INVITE":
                self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n" + b"\r\n"
                                 b"SIP/2.0 180 Ring" + b"\r\n" + b"\r\n"
                                 b"SIP/2.0 200 OK" + b"\r\n" + b"\r\n")
            elif metodo == "ACK":
                aEjecutar = "./mp32rtp -i " + ip + " -p 23032 < "
                aEjecutar += fichero_audio
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            elif metodo == "BYE":
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n")
            elif metodo != "INVITE" or "BYE":
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed" + b"\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request" + b"\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 4:
        port = int(sys.argv[2])
        ip = sys.argv[1]
        fichero_audio = sys.argv[3]
        serv = socketserver.UDPServer((ip, port), EchoHandler)
        print("Listening")
        serv.serve_forever()
    else:
        sys.exit("Usage: python server.py IP port audio_file")
