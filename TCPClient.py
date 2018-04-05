# Example TCP socket client that connects to a server that upper cases text
import sys
import os
import commands
from socket import *

# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000
ARXIU = 'ESPIRAL.txt'

# Optional server name argument
if len(sys.argv) > 1:
    serverName = sys.argv[1]

# Optional server port number
if len(sys.argv) > 2:
    serverPort = int(sys.argv[2])

# Request IPv4 and TCP communication
clientSocket = socket(AF_INET, SOCK_STREAM)

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

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))

option = raw_input('Choose your option, GET or PUT the file: ')

clientSocket.send(option)

if option == 'put' or option == 'PUT':
    # choose the file to transfer
    llistat = commands.getoutput('ls -I "*.py"')
    print ('')
    print (llistat)
    print ('')
    ARXIU = raw_input('Choose your file: ')
    print ("The file is:", ARXIU)
    # Send name File
    sentence = ARXIU
    clientSocket.send(sentence)

    comprovar = False

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8':
            comprovar = True
        elif paquet_size == '16':
            comprovar = True
        elif paquet_size == '32':
            comprovar = True
        elif paquet_size == '64':
            comprovar = True
        elif paquet_size == '128':
            comprovar = True
        elif paquet_size == '256':
            comprovar = True
        elif paquet_size == '512':
            comprovar = True
        elif paquet_size == '1024':
            comprovar = True
        else:
            print ("Error: try again")
            print ('')

    print ("The paquet size is", paquet_size, "bytes")
    clientSocket.send(paquet_size)
    print ('')

    print ('')
    print ('Start upload to server')
    print ('')
    # Wait server answer
    modifiedSentence = clientSocket.recv(512)
    if modifiedSentence != 'Perfecte':
        print("error en enviament de nom ARXIU")
        clientSocket.close()

    # Obrim el fitxer en mode lectura binaria i llegim el su contingut
    with open(ARXIU, "rb") as arxiu:
        buffer = arxiu.read()

    while True:
        # Send how many byte of file
        clientSocket.send(str(len(buffer)))

        mida = len(buffer)

        # Wait server answer
        rebut = clientSocket.recv(10)
        if rebut == "OK":
            # If is ok send file
            x = 0
            byte = ''
            auxili = mida

            tot = mida / int(paquet_size)
            print ('hauria de ser:', tot)
            print('mida arxiu:', mida)
            while x < mida:
                if auxili < int(paquet_size):
                    z = 0
                    w = x
                    while z < auxili:
                        byte += buffer[w]
                        z += 1
                        w += 1
                else:
                    z = 0
                    w = x
                    while z < int(paquet_size):
                        byte += buffer[w]
                        z += 1
                    w += 1
                x += int(paquet_size)
                clientSocket.send(byte)
                auxili -= int(paquet_size)

    # Close
    clientSocket.close()

elif (option == 'get' or option == 'GET'):
    # Receive
    llista = clientSocket.recv(2048)
    print ('')
    print (llista)
    print ('')
    ARXIU = raw_input('Choose your file: ')

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '8':
            comprovar = True
        elif paquet_size == '16':
            comprovar = True
        elif paquet_size == '32':
            comprovar = True
        elif paquet_size == '64':
            comprovar = True
        elif paquet_size == '128':
            comprovar = True
        elif paquet_size == '256':
            comprovar = True
        elif paquet_size == '512':
            comprovar = True
        elif paquet_size == '1024':
            comprovar = True
        else:
            print ("Error: try again")
            print ('')

    print ("The paquet size is", paquet_size, "bytes")
    clientSocket.send(paquet_size)
    modifiedSentence = clientSocket.recv(512)
    print ('')

    sData = "Temp"

    while True:
        clientSocket.send(ARXIU)
        sData = clientSocket.recv(int(paquet_size))
        fDownloadFile = open('arxiu', "wb")
        mida = clientSocket.recv(512)
        answer = 'OK size'
        clientSocket.send(answer)

    while sData:
        fDownloadFile.write(sData)
        sData = clientSocket.recv(int(paquet_size))
    clientSocket.close()

