# TCP server program that upper cases text sent from the client
from socket import *
import sys
import os
import commands

# Default port number server will listen on
serverPort = 12000

# Optional server port number
if (len(sys.argv) > 1):
	serverPort = int(sys.argv[1])

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET,SOCK_STREAM)

# The welcoming port that clients first use to connect
serverSocket.bind(('',serverPort))

# Start listening on the welcoming port
serverSocket.listen(1)
os.system("ifconfig | grep -w inet")

print ('The server is ready to receive')

connectionSocket, addr = serverSocket.accept()

getorput = connectionSocket.recv(128)

if (getorput == 'PUT' or getorput == 'put'):
	print ("Client select:", getorput)
	print ('')

	# Receive the file and confirm this
	ARXIU = connectionSocket.recv(512)
	print ("The file is:", ARXIU)
	print ('')
	mida_paq = connectionSocket.recv(512)
	print ('Paquet size:', mida_paq)

	sentence = 'Perfecte'
	connectionSocket.send(sentence)

	while True:
		# Receive the size of file
		rebut = connectionSocket.recv(1024).strip()
		if rebut:
			print ("File size:", rebut)
			print ('')
		# Verifiquem que el que rebem sigui un numero, en cas que
		# sigui aixi enviem OK al client indicant que estem llestos
		# per rebre l'arxiu
		if rebut.isdigit():
			connectionSocket.send("OK")

			# Inicialitzem el contador que guarda la quantitat de
			# bytes rebuts
			buffer = 0
			iteracions = 0
			# Obrim l'arxiu en mode escriptura
			with open("arxiu", "wb") as arxiu:
				# Ens preparem per rebre l'arxiu amb longitud
				# especifica
				while (buffer < int(rebut)):
					data = connectionSocket.recv(int(mida_paq))
					if not len(data):
						# Si no rebem dades sortim del bucle
						break
					# Escrivim cada byte en l'arxiu i
					# augmentem el buffer
					arxiu.write(data)
					buffer += int(mida_paq)
					iteracions +=1

				tot=int(rebut)/int(mida_paq)
				print ('hauria de ser:', tot)
				print ('mida bufer:', buffer)
				print ('iteracions:', iteracions)
				if buffer == int(rebut):
					print ("File downloaded successfully")
				else:
					print ("An error/incomplete file has happened")
			break

elif (getorput == 'GET' or getorput == 'get'):
	print ("Client select:", getorput)
	print ('')

llistat = commands.getoutput('ls -I "*.py"')
connectionSocket.send(llistat)

# Receive the file and confirm this
mida_paq = connectionSocket.recv(10)
print ('Paquet size:', mida_paq)
sentence = 'OK, mida'
connectionSocket.send(sentence)

arxiu_mida = open(ARXIU, "rb")
arx_size = arxiu_mida.read()

size_=len(arx_size)
connectionSocket.send(size_)
modifiedSentence = connectionSocket.recv(10)

while True:
    ARXIU = connectionSocket.recv(512)
    print ("The file is:", ARXIU)
    print ('')

    arxiu = open(ARXIU, "rb")
    sRead = arxiu.read()
    while sRead:
        connectionSocket.send(sRead)
        sRead = arxiu.read(int(mida_paq))
    print ("Sending Completed")
    break

# Close
connectionSocket.close()
serverSocket.close()
