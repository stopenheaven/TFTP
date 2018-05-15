# Example UDP socket client that fires some text at a server
import sys
import commands
import os
from socket import *
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
    ARXIU = int(sys.argv[2])

# Request IPv4 and UDP communication
clientSocket = socket(AF_INET, SOCK_DGRAM)

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

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))
# clientSocket.settimeout(10)

# Hi to server
comprova_ack = False
while comprova_ack == False:
    hi_packet = struct.pack('HH', 4, nbloc)
    clientSocket.sendto(hi_packet, (serverName, serverPort))
    hi_ack, clientAddress = clientSocket.recvfrom(5)
    ack_hi = struct.unpack('HH', hi_ack)
    if ack_hi[0] == 4 and ack_hi[1] == nbloc:
        comprova_ack = True

llistat = commands.getoutput('ls -I "*.py"')
print 'List Client folder for put: '
print llistat
print '\n-------------------------------------\n'

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
print 'List Server folder for get:'
print list_packet[4:]
print '\n-------------------------------------\n'

option = raw_input('Choose your option, GET or PUT the file to server: ')
getorput = 0
ARXIU = raw_input('Choose your file: ')

if (option == 'put' or option == 'PUT'):
    getorput = 1

elif (option == 'get' or option == 'GET'):
    getorput = 2

else:
    print 'Error, select put or get'
    sys.exit()

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

if option == 'put' or option == 'PUT':
    # choose the file to transfer

    print "The file is:", ARXIU, '\n'

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8' or paquet_size == '16' or paquet_size == '32' or paquet_size == '64' or paquet_size == '128' or paquet_size == '256' or paquet_size == '512' or paquet_size == '1024':
            comprovar = True
        else:
            print "Error: try again\n"

    comprova_ack = False
    while comprova_ack == False:
        option_packet = struct.pack('!HH', 3, nbloc)
        option_packet += paquet_size
        clientSocket.sendto(option_packet, (serverName, serverPort))
        option_ack, clientAddress = clientSocket.recvfrom(4)
        ack_option = struct.unpack('HH', option_ack)
        print ack_option[0]
        if ack_option[0] == 4:
            nbloc = ack_option[1]
            comprova_ack = True

    print "The paquet size is", paquet_size, "Bytes\n"
    print 'Start upload to server\n'

    while True:
        # Obrim el fitxer en mode lectura binaria i llegim el su contingut
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        siz = len(size)
        # Send how many byte of file
        size_packet = ''
        comprova_ack = False
        while comprova_ack == False:
            size_packet = struct.pack('!HH', 3, nbloc)
            size_packet += str(siz)
            clientSocket.sendto(size_packet, (serverName, serverPort))
            size_ack, clientAddress = clientSocket.recvfrom(4)
            ack_size = struct.unpack('HH', size_ack)
            print ack_size[0]
            if ack_size[0] == 4:
                comprova_ack = True
        clientSocket.sendto(size_packet, (serverName, serverPort))

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(paquet_size))
        buffer_size = len(buffer)
        print buffer_size
        print siz

        # Wait server answer
        rebut, serverAddress = clientSocket.recvfrom(10)
        if rebut == "OK":
            # If is ok send file
            while buffer:
                # Send file byte to byte

                buffer_packet = struct.pack('HH'+str(buffer_size)+'s', 3, nbloc, buffer)

                clientSocket.sendto(buffer_packet, (serverName, serverPort))
                buffer = arxiu.read(int(paquet_size))
                buffer_size = len(buffer)
                aux = auxiliar * 100 / siz
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
                auxiliar += int(paquet_size)
                nbloc += 1
            break
    proces = '[==========100%========]'
    print proces

    # Close
    clientSocket.close()

elif (option == 'get' or option == 'GET'):

    ARXIU = raw_input('Choose your file: ')

    # Send name File
    sentence = ARXIU
    clientSocket.sendto(sentence, clientAddress)
    okarxiu, serverAddress = clientSocket.recvfrom(10)

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8' or paquet_size == '16' or paquet_size == '32' or paquet_size == '64' or paquet_size == '128' or paquet_size == '256' or paquet_size == '512' or paquet_size == '1024':
            comprovar = True
        else:
            print ("Error: try again")
            print ''

    print "The paquet size is", paquet_size, "Bytes"
    clientSocket.sendto(paquet_size, (serverName, serverPort))
    print ''

    # Wait server answer
    modifiedSentence, clientAddress = clientSocket.recvfrom(512)
    if modifiedSentence != 'Perfecte':
        print "error en enviament de nom ARXIU"
        clientSocket.close()

    while True:
        # Receive the size of file
        rebut, clientAddress = clientSocket.recvfrom(1024)
        if rebut:
            print "File size:", rebut, 'Bytes'
            print 'Start download from server'
            print ''
        # Verifiquem que el que rebem sigui un numero, en cas que
        # sigui aixi enviem OK al client indicant que estem llestos
        # per rebre l'arxiu
        if rebut.isdigit():
            clientSocket.sendto("OK", clientAddress)

            # Inicialitzem el contador que guarda la quantitat de
            # bytes rebuts
            buffer = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                mida = int(rebut)

                while (buffer < mida):
                    data_packet, clientAddress = clientSocket.recvfrom(int(paquet_size) + 4)

                    data = struct.unpack('HH' + str(len(data_packet) - 4) + 's', data_packet)

                    if not len(data[2]):
                        # Si no rebem dades sortim del bucle
                        break
                    # Escrivim cada byte en l'arxiu i augmentem el buffer

                    arxiu.write(data[2])
                    buffer += len(data_packet)-4

                    aux = auxiliar * 100 / mida
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
                    auxiliar += int(paquet_size)

                proces = '[==========100%========]'
                print proces
                print ''

                if buffer == int(rebut):
                    print "File downloaded successfully"
                else:
                    print "An error/incomplete file has happened"
            break

clientSocket.close()