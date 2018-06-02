# Example UDP socket client that fires some text at a server
import sys
import commands
import os
from socket import *
import signal
import struct


# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000
ARXIU = 'ESPIRAL.txt'

# Optional server name argument
if (len(sys.argv) > 1):
    serverName = sys.argv[1]

# Optional server port number
if (len(sys.argv) > 2):
    serverPort = int(sys.argv[2])

# Request IPv4 and UDP communication
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Function for timeout
def handler(signum, frame):
    print '\n \n \n '
    print '-----------------------------------\n'
    print 'Error de timeout \n'
    print '-----------------------------------\n'

    clientSocket.close()
    exit()

# Inicialitzacions
proces = ''
auxiliar = 0
boolea5 = False
boolea10 = False
boolea20 = False
boolea30 = False
boolea40 = False
boolea50 = False
boolea60 = False
boolea70 = False
boolea80 = False
boolea90 = False
boolea95 = False
comprovar = False
nbloc = 0
aux = 0
getorput = 0

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))

# Hi to server
comprova_ack = False
while comprova_ack == False:
    hi_packet = struct.pack('HH', 4, nbloc)
    clientSocket.sendto(hi_packet, (serverName, serverPort))
    hi_ack, clientAddress = clientSocket.recvfrom(5)
    ack_hi = struct.unpack('HH', hi_ack)
    if ack_hi[0] == 4 and ack_hi[1] == nbloc:
        comprova_ack = True
    else:
        print hi_ack[4:]

nbloc += 1

# Capture the files on client
llistat = commands.getoutput('ls -I "*.py"')
print '\nList Client folder for PUT: '
print llistat
print '-------------------------------------\n'

# Receive list server folder
comprova_ack = False
list_ack = ''
list_packet = ''
while comprova_ack == False:
    list_packet, clientAddress = clientSocket.recvfrom(512)

    list_ack = struct.unpack('!HH', list_packet[0:4])
    if list_ack[0] == 3:
        nbloc = list_ack[1]
        ack_list = struct.pack('HH', 4, nbloc)
        clientSocket.sendto(ack_list, (serverName, serverPort))
        comprova_ack = True
    else:
        ack_buffer = struct.pack('HH', 5, nbloc)
        ack_buffer = 'Error packet recieve'
        clientSocket.sendto(ack_buffer, (serverName, serverPort))

nbloc += 1
print 'List Server folder for GET:'
print list_packet[4:]
print '-------------------------------------\n'

# Choose GET or OUT
option = raw_input('Choose your option, GET or PUT the file to server: ')

# Choose file name
ARXIU = raw_input('Choose your file: ')

# RRQ -> solicitud lectura (PUT) codi = 1
# WRQ -> Solicitud escritura (GET) codi = 2

if (option == 'put' or option == 'PUT'):
    getorput = 1

elif (option == 'get' or option == 'GET'):
    getorput = 2

else:
    print 'Error, select put or get'
    sys.exit()

# Send WRQ or RRQ packet
comprova_ack = False
while comprova_ack == False:
    option_packet = struct.pack('!H', getorput)
    option_packet += ARXIU + '0octet0'
    clientSocket.sendto(option_packet, (serverName, serverPort))
    option_ack, clientAddress = clientSocket.recvfrom(4)
    ack_option = struct.unpack('HH', option_ack)
    if ack_option[0] == 4:
        nbloc = ack_option[1]
        comprova_ack = True
    else:
        print option_ack[4:]

nbloc += 1
if option == 'put' or option == 'PUT':
    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8' or paquet_size == '16' or paquet_size == '32' or paquet_size == '64' or paquet_size == '128' or paquet_size == '256' or paquet_size == '512' or paquet_size == '1024':
            comprovar = True
        else:
            print "Error: try again\n"
    nbloc += 1

    # Send size packet
    comprova_ack = False
    while comprova_ack == False:
        option_packet = struct.pack('!HH', 3, nbloc)
        option_packet += paquet_size
        clientSocket.sendto(option_packet, (serverName, serverPort))
        option_ack, clientAddress = clientSocket.recvfrom(4)
        ack_option = struct.unpack('HH', option_ack)
        if ack_option[0] == 4:
            nbloc = ack_option[1]
            comprova_ack = True
        else:
            print option_ack[4:]

    nbloc += 1
    print '\nPut the', ARXIU, 'with paquet size', paquet_size, '\n'
    print 'Start download from server\n'

    while True:
        # Agafem mida arxiu
        siz = os.stat(ARXIU).st_size
        # Send how many byte of file
        size_packet = ''

        # Send file size packet
        comprova_ack = False
        while comprova_ack == False:
            size_packet = struct.pack('!HH', 3, nbloc)
            size_packet += str(siz)
            clientSocket.sendto(size_packet, (serverName, serverPort))
            size_ack, clientAddress = clientSocket.recvfrom(4)
            ack_size = struct.unpack('HH', size_ack)
            if ack_size[0] == 4:
                comprova_ack = True
            else:
                print size_ack[4:]

        nbloc += 1

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(paquet_size))
        buffer_size = len(buffer)

        print 'File size: ', siz, '\n'
        count = 0
        # Send file
        while auxiliar < siz:
            # If nbloc > 65535 nbloc start to 0
            if nbloc > 65535:
                nbloc = 0
            buffer_packet = struct.pack('HH' + str(buffer_size) + 's', 3, nbloc, buffer)
            clientSocket.sendto(buffer_packet, (serverName, serverPort))

            # Set the signal handler and a 5-second alarm
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(30)

            buffer_ack, clientAddress = clientSocket.recvfrom(4)
            ack_buffer = struct.unpack('HH', buffer_ack)

            # Confirm
            if ack_buffer[0] == 4:
                buffer = arxiu.read(int(paquet_size))
                buffer_size = len(buffer)
                aux = auxiliar * 100 / siz
                auxiliar += int(paquet_size)
                nbloc += 1
                count += 1
            else:
                print buffer_ack[4:]

            # View %
            if (aux <= 5 and boolea5 == False):
                boolea5 = True
                proces = '[=>        5%          ]'
                print proces
            elif (aux >= 5 and aux <= 15 and boolea10 == False):
                boolea10 = True
                proces = '[===>      10%         ]'
                print proces
            elif (aux >= 15 and aux <= 25 and boolea20 == False):
                boolea20 = True
                proces = '[=====>    20%         ]'
                print proces
            elif (aux >= 25 and aux <= 35 and boolea30 == False):
                boolea30 = True
                proces = '[=======>  30%         ]'
                print proces
            elif (aux >= 35 and aux <= 45 and boolea40 == False):
                boolea40 = True
                proces = '[=========>40%         ]'
                print proces
            elif (aux >= 45 and aux <= 55 and boolea50 == False):
                proces = '[==========50%         ]'
                boolea50 = True
                print proces
            elif (aux >= 55 and aux <= 65 and boolea60 == False):
                boolea60 = True
                proces = '[==========60%>        ]'
                print proces
            elif (aux >= 65 and aux <= 75 and boolea70 == False):
                boolea70 = True
                proces = '[==========70%==>      ]'
                print proces
            elif (aux >= 75 and aux <= 85 and boolea80 == False):
                boolea80 = True
                proces = '[==========80%====>    ]'
                print proces
            elif (aux >= 85 and aux <= 95 and boolea90 == False):
                boolea90 = True
                proces = '[==========90%======>  ]'
                print proces
            elif (aux > 95 and boolea95 == False):
                boolea95 = True
                proces = '[==========95%=======> ]'
                print proces

        break
    
    proces = '[==========100%========]\n'
    print proces
    print 'Number packet sended: ', count

elif option == 'get' or option == 'GET':

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8' or paquet_size == '16' or paquet_size == '32' or paquet_size == '64' or paquet_size == '128' or paquet_size == '256' or paquet_size == '512' or paquet_size == '1024':
            comprovar = True
        else:
            print "Error: try again\n"
    nbloc += 1

    # Send packet size
    comprova_ack = False
    while comprova_ack == False:
        option_packet = struct.pack('!HH', 3, nbloc)
        option_packet += paquet_size
        clientSocket.sendto(option_packet, (serverName, serverPort))
        option_ack, clientAddress = clientSocket.recvfrom(4)
        ack_option = struct.unpack('HH', option_ack)
        if ack_option[0] == 4:
            nbloc = ack_option[1]
            comprova_ack = True
        else:
            print option_ack[4:]

    nbloc += 1
    print '\nGet the', ARXIU, 'with paquet size', paquet_size, '\n'
    print 'Start upload to server\n'

    while True:
        # Recieve file size packet
        comprova_ack = False
        while comprova_ack == False:
            size_packet, clientAddress = clientSocket.recvfrom(46)
            size_ack = struct.unpack('!HH', size_packet[0:4])
            rebut = size_packet[4:]
            nbloc = size_ack[1]
            if size_ack[0] == 3:
                ack_size = struct.pack('HH', 4, nbloc)
                clientSocket.sendto(ack_size, (serverName, serverPort))
                comprova_ack = True
            else:
                ack_buffer = struct.pack('HH', 5, nbloc)
                ack_buffer = 'Error packet recieve'
                clientSocket.sendto(ack_buffer, (serverName, serverPort))

        if rebut:
            print "File size:", rebut, 'Bytes\n'
        # Verifiquem que el que rebem sigui un numero, en cas que
        # sigui aixi enviem OK al client indicant que estem llestos
        # per rebre l'arxiu

        if rebut.isdigit():
            # Inicialitzem el contador que guarda la quantitat de bytes rebuts
            buffer = 0

            count = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while (buffer < int(rebut)):

                    data_packet, clientAddress = clientSocket.recvfrom(int(paquet_size) + 4)

                    data = struct.unpack('HH' + str(len(data_packet) - 4) + 's', data_packet)

                    # Set the signal handler and a 5-second alarm
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(30)

                    if not len(data[2]):
                        # Si no rebem dades sortim del bucle
                        break

                    if nbloc + 1 > 65535:
                        nbloc = -1

                    if nbloc + 1 == data[1]:
                        nbloc = data[1]
                        ack_buffer = struct.pack('HH', 4, nbloc)
                        clientSocket.sendto(ack_buffer, (serverName, serverPort))
                        # Escrivim cada byte en l'arxiu i augmentem el buffer
                        arxiu.write(data[2])
                        buffer += len(data_packet) - 4
                        aux = auxiliar * 100 / int(rebut)
                        auxiliar += int(paquet_size)
                        count += 1

                    else:
                        ack_buffer = struct.pack('HH', 5, nbloc)
                        ack_buffer = 'Error packet recieve'
                        clientSocket.sendto(ack_buffer, (serverName, serverPort))

                    # View %
                    if (aux <= 5 and boolea5 == False):
                        boolea5 = True
                        proces = '[=>        5%          ]'
                        print proces
                    elif (aux >= 5 and aux <= 15 and boolea10 == False):
                        boolea10 = True
                        proces = '[===>      10%         ]'
                        print proces
                    elif (aux >= 15 and aux <= 25 and boolea20 == False):
                        boolea20 = True
                        proces = '[=====>    20%         ]'
                        print proces
                    elif (aux >= 25 and aux <= 35 and boolea30 == False):
                        boolea30 = True
                        proces = '[=======>  30%         ]'
                        print proces
                    elif (aux >= 35 and aux <= 45 and boolea40 == False):
                        boolea40 = True
                        proces = '[=========>40%         ]'
                        print proces
                    elif (aux >= 45 and aux <= 55 and boolea50 == False):
                        proces = '[==========50%         ]'
                        boolea50 = True
                        print proces
                    elif (aux >= 55 and aux <= 65 and boolea60 == False):
                        boolea60 = True
                        proces = '[==========60%>        ]'
                        print proces
                    elif (aux >= 65 and aux <= 75 and boolea70 == False):
                        boolea70 = True
                        proces = '[==========70%==>      ]'
                        print proces
                    elif (aux >= 75 and aux <= 85 and boolea80 == False):
                        boolea80 = True
                        proces = '[==========80%====>    ]'
                        print proces
                    elif (aux >= 85 and aux <= 95 and boolea90 == False):
                        boolea90 = True
                        proces = '[==========90%======>  ]'
                        print proces
                    elif (aux > 95 and boolea95 == False):
                        boolea95 = True
                        proces = '[==========95%=======> ]'
                        print proces
            
            
            proces = '[==========100%========]\n'
            print proces
            print 'Number packets recieved: ', count

            if buffer == int(rebut):
                print "\nFile downloaded successfully"
            else:
                print "\nAn error/incomplete file has happened"
        break

# Close
clientSocket.close()
