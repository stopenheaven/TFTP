# Simple UDP based server that upper cases text
import sys
import os
import commands
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

print "The server is ready to receive"

getorput, clientAddress = serverSocket.recvfrom(512)

if (getorput == 'PUT' or getorput == 'put'):
	print "Client select:", getorput
	print ''

	# Receive the file and confirm this
	ARXIU, clientAddress = serverSocket.recvfrom(512)
	print "File:", ARXIU
	print ''
	okarxiu = 'ok_arxiu'
	serverSocket.sendto(okarxiu, clientAddress)

	mida_paq, clientAddress = serverSocket.recvfrom(512)
	print 'Paquet size:', mida_paq
	print ''

	message = 'Perfecte'
	serverSocket.sendto(message, clientAddress)

	while True:
		# Rebem la longitud que envia el client
		rebut, clientAddress = serverSocket.recvfrom(2048)
		if rebut:
			print "File size:", rebut
			print ''
		# Verifiquem que el que rebem sigui un numero, en cas que
		# sigui aixi enviem OK al client indicant que estem llestos
		# per rebre l'arxiu
		if rebut.isdigit():
			serverSocket.sendto('OK', clientAddress)

			# Inicialitzem el contador que guarda la quantitat de bytes rebuts
			buffer = 0
			# Obrim l'arxiu en mode escriptura
			with open("arxiu", "wb") as arxiu:
				# Ens preparem per rebre l'arxiu amb longitud
				# especifica
				while (buffer < int(rebut)):
					data, clientAddress = serverSocket.recvfrom(int(mida_paq))
					if not len(data):
						# Si no rebem dades sortim del bucle
						break
					# Escrivim cada byte en l'arxiu i augmentem el buffer
					arxiu.write(data)
					buffer += int(mida_paq)

				buffer = buffer - int(mida_paq) + 1

				if buffer == int(rebut):
					print "File downloaded successfully"
				else:
					print "An error/incomplete file has happened"
			break

elif (getorput == 'GET' or getorput == 'get'):
	print "Client select:", getorput
	print ''

	llistat = commands.getoutput('ls -I "*.py"')
	serverSocket.sendto(llistat, clientAddress)

	# Receive the file and confirm this
	ARXIU, clientAddress = serverSocket.recvfrom(512)
	print "ARXIU:", ARXIU
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
				serverSocket.sendto(buffer, clientAddress)
				buffer = arxiu.read(int(mida_paq))

			break

	print 'Upload maded!'

	# Close
	serverSocket.close()