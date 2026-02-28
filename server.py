import socket
#Create a socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' #Localhost
port = 12345

#Bind the socket to an address and port
server_socket.bind((host, port))

#Listen for incoming connections
server_socket.listen(5)
print("Server listening on port", port)

#Accept a connection
client_socket, addr = server_socket.accept()
print("Connected to client:", addr)

#Receive data from the client
data = client_socket.recv(1024).decode()
print("Received:", data)

#Close the connection
client_socket.close()
server_socket.close()