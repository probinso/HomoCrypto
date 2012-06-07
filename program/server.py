#the server listening on port 5050, when a client connects and gives data will parse and send to whatever
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("CF416-18", 5050))
server_socket.listen(1)

BLOCKSIZE = 4096
ciphertext = ''
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
server_socket.close()
