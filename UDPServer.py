# Simple UDP based server that upper cases text
import sys
import os
import commands
from socket import *
import struct
import signal

# Default to listening on port 12000
serverPort = 12000
nbloc = 0

# Optional server port number
if (len(sys.argv) > 1):
    serverPort = int(sys.argv[1])

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Function for timeout
def handler(signum, frame):
    print '\n \n \n '
    print '------------------------------------- \n'
    print 'Error de timeout \n'
    print '-------------------------------------\n'

    serverSocket.close()
    exit()

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

# Inicialitzacions
auxiliar=0
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
    else:
        ack_buffer = struct.pack('HH', 5, nbloc)
        ack_buffer = 'Error packet recieve'
        serverSocket.sendto(ack_buffer, clientAddress)


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
        else:
            ack_buffer = struct.pack('HH', 5, nbloc)
            ack_buffer = 'Error packet recieve'
            serverSocket.sendto(ack_buffer, clientAddress)

    print 'Paquet size:', mida_paq, '\n'

    while True:
        # Recieve file size
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
            else:
                ack_buffer = struct.pack('HH', 5, nbloc)
                ack_buffer = 'Error packet recieve'
                serverSocket.sendto(ack_buffer, clientAddress)

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

                    # Set the signal handler and a 5-second alarm
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(30)

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
                        ack_buffer = 'Error packet recieve'
                        serverSocket.sendto(ack_buffer, clientAddress)

                if buffer == int(rebut):
                    print "File downloaded successfully"
                else:
                    print "An error/incomplete file has happened"
            break

elif (getorput == 2):
    print "Client select: GET\n"

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
        else:
            ack_buffer = struct.pack('HH', 5, nbloc)
            ack_buffer = 'Error packet recieve'
            serverSocket.sendto(ack_buffer, clientAddress)

    print 'Paquet size:', mida_paq, '\n'

    while True:
        # Agafem mida arxiu
        siz = os.stat(ARXIU).st_size
        # Send how many byte of file
        size_packet = ''

        # Send file size
        comprova_ack = False
        while comprova_ack == False:
            size_packet = struct.pack('!HH', 3, nbloc)
            size_packet += str(siz)
            serverSocket.sendto(size_packet, clientAddress)
            size_ack, clientAddress = serverSocket.recvfrom(4)
            ack_size = struct.unpack('HH', size_ack)
            if ack_size[0] == 4:
                comprova_ack = True
        nbloc += 1

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(mida_paq))
        buffer_size = len(buffer)

        print 'File size: ', siz, '\n'

        # If is ok send file
        while auxiliar < siz:
            # Send file byte to byte
            if nbloc > 65535:
                nbloc = 0
            buffer_packet = struct.pack('HH' + str(buffer_size) + 's', 3, nbloc, buffer)
            serverSocket.sendto(buffer_packet, clientAddress)

            # Set the signal handler and a 5-second alarm
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)

            buffer_ack, clientAddress = serverSocket.recvfrom(4)
            ack_buffer = struct.unpack('HH', buffer_ack)

            if ack_buffer[0] == 4:
                buffer = arxiu.read(int(mida_paq))
                buffer_size = len(buffer)
                aux = auxiliar * 100 / siz
                auxiliar += int(mida_paq)
                nbloc += 1
        break
    print 'Upload maded'
    # Close
serverSocket.close()