import socket

#Create a socket 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

#Connect to the server
client_socket.connect((host,port))

#Send a message
message = "Hello, Server!"
client_socket.send(message.encode())

#Receive a response
response = client_socket.recv(1024).decode()
print("Response from server:", response)

#Close the connection
client_socket.close()