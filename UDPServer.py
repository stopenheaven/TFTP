# Simple UDP based server that upper cases text
import sys
import os
import commands
from socket import *
import struct

# Default to listening on port 12000
serverPort = 12000
nbloc = 0

# Optional server port number
if (len(sys.argv) > 1):
    serverPort = int(sys.argv[1])

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.settimeout(10)

# Specify the welcoming port of the server
serverSocket.bind(('', serverPort))

os.system("ifconfig | grep -w inet")

print "The server is ready to receive"

# Hi from client
comprova_ack = False
while comprova_ack == False:
    hi_packet, clientAddress = serverSocket.recvfrom(5)
    hi_ack = struct.unpack('HH', hi_packet)
    if hi_ack[0] == 4:
        nbloc = hi_ack[1]
        ack_hi = struct.pack('HH', 4, nbloc)
        serverSocket.sendto(ack_hi, clientAddress)
        comprova_ack = True

# Send list Server folder
llistat = commands.getoutput('ls -I "*.py"')
comprova_ack = False
while comprova_ack == False:
    list_packet = struct.pack('!HH', 3, nbloc)
    list_packet += llistat

    serverSocket.sendto(list_packet, clientAddress)
    list_ack, clientAddress = serverSocket.recvfrom(5)
    ack_list = struct.unpack('HH', list_ack)
    if ack_list[0] == 4 and ack_list[1] == nbloc:
        comprova_ack = True

getorput = ''
ARXIU = ''
nbloc += 1
# Recieve decision get or put
comprova_ack = False
while comprova_ack == False:
    option_packet, clientAddress = serverSocket.recvfrom(46)
    option_ack = struct.unpack('!H', option_packet[0:2])
    getorput = option_ack[0]

    ARXIU = option_packet[2:-7]
    if option_ack[0] == 1 or option_ack[0] == 2:
        ack_option = struct.pack('HH', 4, nbloc)
        serverSocket.sendto(ack_option, clientAddress)
        comprova_ack = True

if (getorput == 1):
    print "Client select: PUT\n"

    print "File:", ARXIU, '\n'

    # Recieve packet size
    comprova_ack = False
    while comprova_ack == False:
        mida_packet, clientAddress = serverSocket.recvfrom(46)
        mida_ack = struct.unpack('!HH', mida_packet[0:4])
        mida_paq = mida_packet[4:]
        nbloc = mida_ack[1]

        if mida_ack[0] == 3:
            ack_paq = struct.pack('HH', 4, nbloc)
            serverSocket.sendto(ack_paq, clientAddress)
            comprova_ack = True

    print 'Paquet size:', mida_paq
    print ''

    while True:
        # Rebem la longitud que envia el client
        comprova_ack = False
        while comprova_ack == False:
            size_packet, clientAddress = serverSocket.recvfrom(46)
            size_ack = struct.unpack('!HH', size_packet[0:4])
            rebut = size_packet[4:]
            nbloc = size_ack[1]

            if size_ack[0] == 3:
                ack_size = struct.pack('HH', 4, nbloc)
                serverSocket.sendto(ack_size, clientAddress)
                comprova_ack = True
        if rebut:
            print "File size:", rebut, 'Bytes\n'
        # Verifiquem que el que rebem sigui un numero, en cas que
        # sigui aixi enviem OK al client indicant que estem llestos
        # per rebre l'arxiu

        if rebut.isdigit():
            # Inicialitzem el contador que guarda la quantitat de bytes rebuts
            buffer = 0

            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while (buffer < int(rebut)):

                    data_packet, clientAddress = serverSocket.recvfrom(int(mida_paq)+4)

                    data = struct.unpack('HH'+str(len(data_packet)-4)+'s', data_packet)

                    if not len(data[2]):
                        # Si no rebem dades sortim del bucle
                        break

                    if nbloc+1 > 65535:
                        nbloc = -1

                    if nbloc+1 == data[1]:
                        nbloc = data[1]
                        ack_buffer = struct.pack('HH', 4, nbloc)
                        serverSocket.sendto(ack_buffer, clientAddress)
                        # Escrivim cada byte en l'arxiu i augmentem el buffer
                        arxiu.write(data[2])
                        buffer += len(data_packet)-4

                    else:
                        ack_buffer = struct.pack('HH', 5, nbloc)
                        serverSocket.sendto(ack_buffer, clientAddress)

                if buffer == int(rebut):
                    print "File downloaded successfully"
                else:
                    print "An error/incomplete file has happened"
            break

elif (getorput == 2):
    print "Client select: GET\n"

    print "File:", ARXIU, '\n'
    okarxiu = 'ok_arxiu'
    serverSocket.sendto(okarxiu, clientAddress)

    mida_paq, clientAddress = serverSocket.recvfrom(512)
    print 'Paquet size:', mida_paq, 'Bytes'
    print ''

    sentence = 'Perfecte'
    serverSocket.sendto(sentence, clientAddress)

    # Obrim el fitxer en mode lectura binaria i llegim el su contingut
    with open(ARXIU, "rb") as arxiu:
        buffer = arxiu.read()

    while True:
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        # Send how many byte of file
        serverSocket.sendto(str(len(size)), clientAddress)

        siz = len(size)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(mida_paq))

        # Wait server answer
        rebut, clientAddress = serverSocket.recvfrom(10)
        if rebut == "OK":
            # If is ok send file
            while buffer:
                # Send file byte to byte
                buffer_packet = struct.pack('HH' + str(mida_paq) + 's', 3, nbloc, buffer)

                serverSocket.sendto(buffer_packet, clientAddress)

                buffer = arxiu.read(int(mida_paq))
                nbloc += 1

            break

    print 'Upload maded!'

    # Close
serverSocket.close()