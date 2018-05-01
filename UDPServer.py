# Simple UDP based server that upper cases text
import sys
import os
import commands
import json
from socket import *

# Default to listening on port 12000
serverPort = 12000

# Optional server port number
if (len(sys.argv) > 1):
    serverPort = int(sys.argv[1])

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
serverSocket.bind(('', serverPort))

os.system("ifconfig | grep -w inet")

print ''

print "The server is ready to receive"

llistat = commands.getoutput('ls -I "*.py"')

ack_hi, clientAdress = serverSocket.recvfrom(50)
hi_ack = json.loads(ack_hi)
nbloc = hi_ack[1]

llista = [3, nbloc, llistat]

check_llista = False
while check_llista == False:
    send_txt = json.dumps(llista)
    serverSocket.sendto(send_txt, clientAdress)

    ack_llista, clientAdress = serverSocket.recvfrom(50)
    llista_ack = json.loads(ack_llista)
    if llista_ack[1] == nbloc:
        check_llista = True

option, clientAdress = serverSocket.recvfrom(50)

llista = json.loads(option)

okjson = [4, nbloc]
send_txt = json.dumps(okjson)
serverSocket.sendto(send_txt, clientAdress)

codi = llista[0]
ARXIU = llista[1]

nbloc = 0

if codi == 1:
    print "Client select: PUT "
    print ''

    # Receive the file and confirm this
    print "The file is:", llista[1]
    print ''

    size_paq, clientAdress = serverSocket.recvfrom(50)
    paq_mida = json.loads(size_paq)

    mida_paq = paq_mida[2]

    print 'Paquet size:', mida_paq
    print ''

    nbloc = paq_mida[1]

    ack_paq_size = [4, nbloc]
    send_txt = json.dumps(ack_paq_size)
    serverSocket.sendto(send_txt, clientAdress)

    while True:
        # Receive the size of file
        file_size, clientAdress = serverSocket.recvfrom(50)
        size_file = json.loads(file_size)
        rebut = size_file[2]
        if size_file:
            print "File size:", rebut, 'Bytes'
            nbloc = size_file[1]
            print ''

            ack_file_size = [4, nbloc]
            send_txt = json.dumps(ack_file_size)
            serverSocket.sendto(send_txt, clientAdress)

            # Inicialitzem el contador que guarda la quantitat de
            # bytes rebuts
            buffer = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while buffer < int(rebut):
                    data_file, clientAdress = serverSocket.recvfrom(int(mida_paq) + 16)
                    print data_file
                    file_data = json.loads(data_file)
                    data = file_data[2]
                    nbloc = file_data[1]

                    ack_file_data = [4, nbloc]
                    send_txt = json.dumps(ack_file_data)
                    serverSocket.sendto(send_txt, clientAdress)
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

    size_paq, clientAdress = serverSocket.recvfrom(50)
    paq_mida = json.loads(size_paq)

    mida_paq = paq_mida[2]
    nbloc = paq_mida[1]

    print 'Paquet size:', mida_paq
    print ''

    ack_paq_size = [4, nbloc]
    send_txt = json.dumps(ack_paq_size)
    serverSocket.sendto(send_txt, clientAdress)

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
        serverSocket.sendto(send_txt, clientAdress)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(mida_paq))

        # Wait server answer file size
        ack_file_size, clientAdress = serverSocket.recvfrom(50)
        file_size_ack = json.loads(ack_file_size)
        if file_size_ack[1] == nbloc:
            # If is ok send file
            while buffer:
                # Send file byte to byte
                serverSocket.sendto(buffer, clientAdress)
                buffer = arxiu.read(int(mida_paq))

            break

    print 'Upload maded!!'

# Close
serverSocket.close()
