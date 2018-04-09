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

# Open the TCP connection to the server at the specified port
clientSocket.connect((serverName, serverPort))

option = raw_input('Choose your option, GET or PUT the file: ')

clientSocket.send(option)

if (option == 'put' or option == 'PUT'):
	# choose the file to transfer
	llistat = commands.getoutput('ls -I "*.py"')
	print ''
	print llistat
	print ''
	ARXIU = raw_input('Choose your file: ')
	print "The file is:", ARXIU
	# Send name File
	sentence = ARXIU
	clientSocket.send(sentence)
	okarxiu = clientSocket.recv(10)

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
			print ''

	print "The paquet size is", paquet_size, "Bytes"
	clientSocket.send(paquet_size)
	print ''

	print 'Start upload to server'
	print ''
	# Wait server answer
	modifiedSentence = clientSocket.recv(512)
	if modifiedSentence != 'Perfecte':
		print "error en enviament de nom ARXIU"
		clientSocket.close()

	while True:
		# Obrim el fitxer en mode lectura binaria i llegim el su contingut
		with open(ARXIU, "rb") as arxiu_size:
			size = arxiu_size.read()
		# Send how many byte of file
		clientSocket.send(str(len(size)))

		siz = len(size)

		arxiu = open(ARXIU, 'rb')
		buffer = arxiu.read(int(paquet_size))

		# Wait server answer
		rebut = clientSocket.recv(10)
		if rebut == "OK":
			# If is ok send file
			while buffer:
				# Send file byte to byte
				clientSocket.send(buffer)
				buffer = arxiu.read(int(paquet_size))
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
			break
	proces = '[==========100%========]'
	print proces

	# Close
	clientSocket.close()

elif (option == 'get' or option == 'GET'):
	# Receive
	llista = clientSocket.recv(2048)
	print ''
	print llista
	print ''
	ARXIU = raw_input('Choose your file: ')

	# Send name File
	sentence = ARXIU
	clientSocket.send(sentence)
	okarxiu = clientSocket.recv(10)

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
			print ''

	print "The paquet size is", paquet_size, "Bytes"
	clientSocket.send(paquet_size)
	print ''

	# Wait server answer
	modifiedSentence = clientSocket.recv(512)
	if modifiedSentence != 'Perfecte':
		print "error en enviament de nom ARXIU"
		clientSocket.close()

	while True:
		# Receive the size of file
		rebut = clientSocket.recv(1024).strip()
		if rebut:
			print "File size:", rebut, 'Bytes'
			print ''
		# Verifiquem que el que rebem sigui un numero, en cas que
		# sigui aixi enviem OK al client indicant que estem llestos
		# per rebre l'arxiu
		if rebut.isdigit():
			clientSocket.send("OK")

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

	buffer = buffer - int(paquet_size) + 1

	if buffer == int(rebut):
		print "File downloaded successfully"
	else:
		print "An error/incomplete file has happened"


clientSocket.close()
