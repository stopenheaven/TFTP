# TCP server program that upper cases text sent from the client
from socket import *
import sys
import os
import commands
import struct

# Default port number server will listen on
serverPort = 12000
nbloc = 0

# Optional server port number
if (len(sys.argv) > 1):
    serverPort = int(sys.argv[1])

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET, SOCK_STREAM)

# The welcoming port that clients first use to connect
serverSocket.bind(('', serverPort))

# Start listening on the welcoming port
serverSocket.listen(1)
os.system("ifconfig | grep -w inet")

print 'The server is ready to receive'

connectionSocket, addr = serverSocket.accept()

getorput = connectionSocket.recv(128)

if (getorput == 'PUT' or getorput == 'put'):
    print "Client select:", getorput
    print ''

    # Receive the file and confirm this
    ARXIU = connectionSocket.recv(512)
    print "The file is:", ARXIU
    print ''
    okarxiu = 'ok_arxiu'
    connectionSocket.send(okarxiu)

    mida_paq = connectionSocket.recv(512)
    print 'Paquet size:', mida_paq
    print ''

    sentence = 'Perfecte'
    connectionSocket.send(sentence)

    while True:
        # Receive the size of file
        rebut = connectionSocket.recv(1024).strip()
        if rebut:
            print "File size:", rebut, 'Bytes'
            print ''
        # Verifiquem que el que rebem sigui un numero, en cas que
        # sigui aixi enviem OK al client indicant que estem llestos
        # per rebre l'arxiu
        if rebut.isdigit():
            connectionSocket.send("OK")

            # Inicialitzem el contador que guarda la quantitat de
            # bytes rebuts
            buffer = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while (buffer < int(rebut)):
                    data_packet = serverSocket.recv(int(mida_paq) + 4)

                    data = struct.unpack('HH' + str(len(data_packet) - 4) + 's', data_packet)

                    if not len(data[2]):
                        # Si no rebem dades sortim del bucle
                        break
                    # Escrivim cada byte en l'arxiu i augmentem el buffer

                    arxiu.write(data[2])
                    buffer += len(data_packet)

                buffer -= 4
                print "File downloaded successfully"
            break

elif (getorput == 'GET' or getorput == 'get'):
    print "Client select:", getorput
    print ''

    llistat = commands.getoutput('ls -I "*.py"')
    connectionSocket.send(llistat)

    # Receive the file and confirm this
    ARXIU = connectionSocket.recv(512)
    print "ARXIU:", ARXIU
    okarxiu = 'ok_arxiu'
    connectionSocket.send(okarxiu)

    mida_paq = connectionSocket.recv(512)
    print 'Paquet size:', mida_paq, 'Bytes'
    print ''

    sentence = 'Perfecte'
    connectionSocket.send(sentence)

    # Obrim el fitxer en mode lectura binaria i llegim el su contingut
    with open(ARXIU, "rb") as arxiu:
        buffer = arxiu.read()

    while True:
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        # Send how many byte of file
        connectionSocket.send(str(len(size)))

        siz = len(size)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(mida_paq))

        # Wait server answer
        rebut = connectionSocket.recv(10)
        if rebut == "OK":
            # If is ok send file
            while buffer:
                # Send file byte to byte
                buffer_packet = struct.pack('HH' + str(mida_paq) + 's', 3, nbloc, buffer)

                serverSocket.send(buffer_packet)

                buffer = arxiu.read(int(mida_paq))
                nbloc += 1
            break

    print 'Upload maded!'

# Close
connectionSocket.close()
