# server
import socket
import time

HOST = ''
PORT = 7477

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(('', 7477))
server_socket.listen()
client_socket, addr = server_socket.accept()

print('Connected by', addr)

while True:
    order = input('input')
    client_socket.sendall(order.encode('utf-8'))
    time.sleep(1)
    data = client_socket.recv(1024)
    if not data:
        break
    print('addr:{} data:{}'.format(addr, data.decode()))

client_socket.close()
server_socket.close()