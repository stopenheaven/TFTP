# TCP server program that upper cases text sent from the client
from socket import *
import sys
import os
import commands
import json

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

print ''

print 'The server is ready to receive'

connectionSocket, addr = serverSocket.accept()

llistat = commands.getoutput('ls -I "*.py"')

llista = [3, nbloc, llistat]

check_llista = False
while check_llista == False:
    send_txt = json.dumps(llista)
    connectionSocket.send(send_txt)

    ack_llista = connectionSocket.recv(50)
    llista_ack = json.loads(ack_llista)
    if llista_ack[1] == nbloc:
        check_llista = True

option = connectionSocket.recv(50)

llista = json.loads(option)

okjson = [4, nbloc]
send_txt = json.dumps(okjson)
connectionSocket.send(send_txt)

codi = llista[0]
ARXIU = llista[1]

nbloc = 0

if codi == 1:
    print "Client select: PUT "
    print ''

    # Receive the file and confirm this
    print "The file is:", llista[1]
    print ''


    size_paq = connectionSocket.recv(50)
    paq_mida = json.loads(size_paq)

    mida_paq = paq_mida[2]

    print 'Paquet size:', mida_paq
    print ''

    nbloc = paq_mida[1]

    ack_paq_size = [4, nbloc]
    send_txt = json.dumps(ack_paq_size)
    connectionSocket.send(send_txt)

    while True:
        # Receive the size of file
        file_size = connectionSocket.recv(50)
        size_file = json.loads(file_size)
        rebut = size_file[2]
        if size_file:
            print "File size:", rebut, 'Bytes'
            nbloc = size_file[1]
            print ''

            ack_file_size = [4, nbloc]
            send_txt = json.dumps(ack_file_size)
            connectionSocket.send(send_txt)

            # Inicialitzem el contador que guarda la quantitat de
            # bytes rebuts
            buffer = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while (buffer < int(rebut)):
                    data_file = connectionSocket.recv(int(mida_paq)+16)
                    print data_file
                    file_data = json.loads(data_file)
                    data = file_data[2]
                    nbloc = file_data[1]

                    ack_file_data = [4, nbloc]
                    send_txt = json.dumps(ack_file_data)
                    connectionSocket.send(send_txt)
                    if not len(data):
                        # Si no rebem dades sortim del bucle
                        break
                    # Escrivim cada byte en l'arxiu i
                    # augmentem el buffer
                    arxiu.write(data)
                    buffer += int(mida_paq)

                print "File downloaded successfully"
            break

elif codi == 2:
    print "Client select: GET "
    print ''

    print "ARXIU:", ARXIU

    size_paq = connectionSocket.recv(50)
    paq_mida = json.loads(size_paq)

    mida_paq = paq_mida[2]
    nbloc = paq_mida[1]

    print 'Paquet size:', mida_paq
    print ''

    ack_paq_size = [4, nbloc]
    send_txt = json.dumps(ack_paq_size)
    connectionSocket.send(send_txt)

    # Obrim el fitxer en mode lectura binaria i llegim el seu contingut
    with open(ARXIU, "rb") as arxiu:
        buffer = arxiu.read()

    while True:
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        # Send how many byte of file
        siz = len(size)
        # Send how many byte of file
        mida_file = [3, nbloc, siz]
        send_txt = json.dumps(mida_file)
        connectionSocket.send(send_txt)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(mida_paq))

        # Wait server answer file size
        ack_file_size = connectionSocket.recv(50)
        file_size_ack = json.loads(ack_file_size)
        if file_size_ack[1] == nbloc:
            # If is ok send file
            while buffer:
                # Send file byte to byte
                connectionSocket.send(buffer)
                buffer = arxiu.read(int(mida_paq))

            break

    print 'Upload maded!!'

# Close
connectionSocket.close()
