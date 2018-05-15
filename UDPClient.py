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
fmt = ''
nbloc = 0

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))

option = raw_input('Choose your option, GET or PUT the file to server: ')

clientSocket.sendto(option, (serverName, serverPort))

if (option == 'put' or option == 'PUT'):
    # choose the file to transfer
    llistat = commands.getoutput('ls -I "*.py"')
    print ''
    print llistat
    print ''
    ARXIU = raw_input('Choose your file: ')

    print "The file is:", ARXIU
    print ''
    # Send name File
    message = ARXIU
    clientSocket.sendto(message, (serverName, serverPort))
    okarxiu, serverAddress = clientSocket.recvfrom(10)

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8':
            fmt = '8'
            comprovar = True
        elif paquet_size == '16':
            fmt = '16'
            comprovar = True
        elif paquet_size == '32':
            fmt = '32'
            comprovar = True
        elif paquet_size == '64':
            fmt = '64'
            comprovar = True
        elif paquet_size == '128':
            fmt = '128'
            comprovar = True
        elif paquet_size == '256':
            fmt = '256'
            comprovar = True
        elif paquet_size == '512':
            fmt = '512'
            comprovar = True
        elif paquet_size == '1024':
            fmt = '1024'
            comprovar = True
        else:
            print ("Error: try again")
            print ''

    print "The paquet size is", paquet_size, "Bytes"
    clientSocket.sendto(paquet_size, (serverName, serverPort))
    print ''

    print 'Start upload to server'
    print ''

    # Wait server answer
    modifiedMessage, serverAddress = clientSocket.recvfrom(512)
    if modifiedMessage != 'Perfecte':
        print "error en enviament de nom ARXIU"
        clientSocket.close()

    while True:
        # Obrim el fitxer en mode lectura binaria i llegim el su contingut
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        # Send how many byte of file
        clientSocket.sendto(str(len(size)), (serverName, serverPort))

        siz = len(size)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(paquet_size))
        buffer_size = len(buffer)

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
    # Receive
    llista, clientAddress = clientSocket.recvfrom(2048)
    print ''
    print llista
    print ''
    ARXIU = raw_input('Choose your file: ')

    # Send name File
    sentence = ARXIU
    clientSocket.sendto(sentence, clientAddress)
    okarxiu, serverAddress = clientSocket.recvfrom(10)

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8':
            fmt = '8'
            comprovar = True
        elif paquet_size == '16':
            fmt = '16'
            comprovar = True
        elif paquet_size == '32':
            fmt = '32'
            comprovar = True
        elif paquet_size == '64':
            fmt = '64'
            comprovar = True
        elif paquet_size == '128':
            fmt = '128'
            comprovar = True
        elif paquet_size == '256':
            fmt = '256'
            comprovar = True
        elif paquet_size == '512':
            fmt = '512'
            comprovar = True
        elif paquet_size == '1024':
            fmt = '1024'
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