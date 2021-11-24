import socket
import time

listensocket = socket.socket()
Port = 8000
maxConnections = 2
IP = socket.gethostname()

listensocket.bind((''.Port))
listensocket.listen(maxConnections)
print(f"Server started at {IP} on port {str(Port)}")

(clientsocket, address) = listensocket.accept()
print(f"New connection made!")

running = True

while running:
    message = clientsocket.recv(1024).decode()
    print(message)

    


