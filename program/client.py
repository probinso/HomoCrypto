#this is all you have to do for sending it
import socket
def sendciphertext(cipher):
	ciphertext = str(cipher)
	BLOCKSIZE = 4096
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("CF416-18", 5050))
	client_socket.sendall(ciphertext)
	client_socket.close()

