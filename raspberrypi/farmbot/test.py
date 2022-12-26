# client
import time
import socket

HOST = '192.168.12.4'
PORT = 7477

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, 7477))

while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print(data.decode('utf-8'))

    client_socket.sendall('recive'.encode())
client_socket.close()
