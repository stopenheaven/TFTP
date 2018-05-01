# Example TCP socket client that connects to a server that upper cases text
import sys
import os
import commands
from socket import *
import json

# RRQ -> solicitud lectura (PUT)
# WRQ -> Solicitud escritura (GET)
#       codi(1=RRQ, 2=WRQ) | nom del fitxer | 0 | mode | 0
# DATA -> paquet de dades
#       codi | nbloc | dades
# ACK -> paquet assentiment
#       codi | nbloc
# ERR -> paquet error
#       codi | codi error | misstage error | 0

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
nbloc = 0

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))

llista_arxius = clientSocket.recv(50)
list = json.loads(llista_arxius)
nbloc = list[1]

ack_llista = [4, nbloc]
send_txt = json.dumps(ack_llista)
clientSocket.send(send_txt)
nbloc += 1

llista = list[2]

desition = raw_input('Choose see files from SERVER or CLIENT: ')
option = ''
if desition == 'server' or desition == 'SERVER':
    # Receive
    print 'Files from Server:'
    print llista
    print ''
    option = 2

elif desition == 'client' or desition == 'CLIENT':
    # choose the file to transfer
    llistat = commands.getoutput('ls -I "*.py"')
    print 'Files from Client:'
    print llistat
    print ''
    option = 1

else:
    print 'Error choose SERVER or CLIENT'
    exit()

ARXIU = raw_input('Choose your file: ')
print "The file is:", ARXIU

options = [option, ARXIU, 0, 'NETASCII', 0]

send_txt = json.dumps(options)
clientSocket.send(send_txt)

okjson = clientSocket.recv(50)
ackjson = json.loads(okjson)

nbloc = ackjson[1] + 1

if option == 1:

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (1, 8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '1':
            comprovar = True
        elif paquet_size == '8':
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
            print ''

    print "The paquet size is", paquet_size, "Bytes"
    mida_paq = [3, nbloc, paquet_size]
    send_txt = json.dumps(mida_paq)

    clientSocket.send(send_txt)
    print ''

    # Wait server answer paquet size
    ack_paq_size = clientSocket.recv(50)
    paq_size_ack = json.loads(ack_paq_size)
    if paq_size_ack[1] != nbloc:
        print "error en enviament de nom ARXIU"
        clientSocket.close()

    print 'Start upload to server'
    print ''

    nbloc += 1

    while True:
        # Obrim el fitxer en mode lectura binaria i llegim el su contingut
        with open(ARXIU, "rb") as arxiu_size:
            size = arxiu_size.read()
        siz = len(size)
        # Send how many byte of file
        mida_file = [3, nbloc, siz]
        send_txt = json.dumps(mida_file)
        clientSocket.send(send_txt)

        arxiu = open(ARXIU, 'rb')
        buffer = arxiu.read(int(paquet_size))

        # Wait server answer file size
        ack_file_size = clientSocket.recv(50)
        file_size_ack = json.loads(ack_file_size)
        if file_size_ack[1] == nbloc:
            nbloc += 1
            # If is ok send file
            while buffer:
                # Send file byte to byte
                paq_buffer = [3, nbloc, buffer]
                print buffer
                send_txt = json.dumps(paq_buffer)
                clientSocket.send(send_txt)

                ack_buffer = clientSocket.recv(50)
                buffer_ack = json.loads(ack_buffer)

                if buffer_ack[1] == nbloc:
                    buffer = arxiu.read(int(paquet_size))
                    aux = auxiliar * 100 / siz
                    if aux <= 5 and boolea5 == False:
                        boolea5 = True
                        proces = '[=>        5%          ]'
                        print proces
                    elif 5 <= aux <= 15 and boolea10 == False:
                        boolea10 = True
                        proces = '[===>      10%         ]'
                        print proces
                    elif 15 <= aux <= 25 and boolea20 == False:
                        boolea20 = True
                        proces = '[=====>    20%         ]'
                        print proces
                    elif 25 <= aux <= 35 and boolea30 == False:
                        boolea30 = True
                        proces = '[=======>  30%         ]'
                        print proces
                    elif 35 <= aux <= 45 and boolea40 == False:
                        boolea40 = True
                        proces = '[=========>40%         ]'
                        print proces
                    elif 45 <= aux <= 55 and boolea50 == False:
                        proces = '[==========50%         ]'
                        boolea50 = True
                        print proces
                    elif 55 <= aux <= 65 and boolea60 == False:
                        boolea60 = True
                        proces = '[==========60%>        ]'
                        print proces
                    elif 65 <= aux <= 75 and boolea70 == False:
                        boolea70 = True
                        proces = '[==========70%==>      ]'
                        print proces
                    elif 75 <= aux <= 85 and boolea80 == False:
                        boolea80 = True
                        proces = '[==========80%====>    ]'
                        print proces
                    elif 85 <= aux <= 95 and boolea90 == False:
                        boolea90 = True
                        proces = '[==========90%======>  ]'
                        print proces
                    elif aux > 95 and boolea95 == False:
                        boolea95 = True
                        proces = '[==========95%=======> ]'
                        print proces
                    auxiliar += int(paquet_size)
                    nbloc += 1
            break
    proces = '[==========100%========]'
    print proces

    print ''

    print "File uploaded successfully"

    # Close
    clientSocket.close()

elif option == 2:

    # Choose the paquet size how you want transfer
    while comprovar == False:
        paquet_size = raw_input('Choose the paquet size (1, 8, 16, 32, ... , 1024 bytes): ')
        if paquet_size == '1':
            comprovar == True
        elif paquet_size == '8':
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
            print ''

    print "The paquet size is", paquet_size, "Bytes"
    mida_paq = [3, nbloc, paquet_size]
    send_txt = json.dumps(mida_paq)

    clientSocket.send(send_txt)
    print ''

    # Wait server answer paquet size
    ack_paq_size = clientSocket.recv(50)
    paq_size_ack = json.loads(ack_paq_size)
    if paq_size_ack[1] != nbloc:
        print "error en enviament de nom ARXIU"
        clientSocket.close()

    while True:
        # Receive the size of file
        file_size = clientSocket.recv(50)
        size_file = json.loads(file_size)
        rebut = size_file[2]
        if size_file:
            print "File size:", rebut, 'Bytes'
            nbloc = size_file[1]
            print ''

            ack_file_size = [4, nbloc]
            send_txt = json.dumps(ack_file_size)
            clientSocket.send(send_txt)

            # Inicialitzem el contador que guarda la quantitat de
            # bytes rebuts
            buffer = 0
            # Obrim l'arxiu en mode escriptura
            with open("arxiu", "wb") as arxiu:
                # Ens preparem per rebre l'arxiu amb longitud
                # especifica
                while (buffer < int(rebut)):
                    data = clientSocket.recv(int(paquet_size))
                    if not len(data):
                        # Si no rebem dades sortim del bucle
                        break
                    # Escrivim cada byte en l'arxiu i
                    # augmentem el buffer
                    arxiu.write(data)
                    buffer += int(paquet_size)

                    aux = auxiliar * 100 / int(rebut)
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
                break
    proces = '[==========100%========]'
    print proces
    print ''

    print "File downloaded successfully"

clientSocket.close()
