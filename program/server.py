#the server listening on port 5050, when a client connects and gives data will parse and send to whatever
from subprocess import call
import socket
import os
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("CF416-18", 5050))
server_socket.listen(1)

BLOCKSIZE = 4096
ciphertext = ''

myBlock = 50

filename = "SEARCH_SPACE"
numFileO = 100

while 1:
	client_socket, address = server_socket.accept()
	while 1:
		data = client_socket.recv(BLOCKSIZE)
#parse through sent string and make it to its glory, for any sending to hadoop, do it after cipher = map
		if not data:
			cipher = ciphertext.replace('[', '')
			cipher = cipher.replace("'", '')
			cipher = cipher.replace(']', '')
			cipher = cipher.replace('L', '')
			cipher = cipher.strip(' ')
			cipher = cipher.split(',')
			cipher = map(int,cipher)
			client_socket.close()

			break;
		ciphertext = ciphertext + data
	
	"""
	f = open(filename,"w")
	f.writelines(["%i\n" % item for item in cipher])
	f.close()
	
	loc = os.getcwd() + "/" + filename
	

	hdop = "/data/hadoop/bin/bin/hadoop "
	args = "fs -copyFromLocal " + loc + " /hdfs/tmp/" + filename
	
	oper = (hdop + args).split(" ")
	call(oper)
	break
	"""

	overlap = (len(cipher)//8) - 1
	fr = open(filename)
	Tsize = os.path.size(fr)
	whole = fr.read()
	fr.close()
	whole = whole.replace('[', '')
	whole = whole.replace("'", '')
	whole = whole.replace(']', '')
	whole = whole.replace('L', '')
	whole = whole.strip(' ')
	whole = whole.split(',')
	whole = map(int,whole)

	Jmp = ( ( len(whole) // 8 ) // 50 ) + overlap * 8 

	for i in range(myBlock):
		fw = open(filename + "_" + str(i),"w")

		fw.write(str(len(cipher))+"\n")

		for y in cipher
			fw.write(str(y)+"\n")

		for y in whole[Jmp*8:(i+1)*Jmp]:
			fw.write(str(y)+"\n")

		fw.close()
	break;

server_socket.close()
