import socket
import threading

#The IP is set to home address and port is set to a constant
#to ensure that the client and server has the same set of data

IP = input("enter ip address")
PORT = int(input("enter port number"))
#Initializing a server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connecting the server to a particular IP and Port
server.bind((IP,PORT))
#This ensures a maximum of 4 client connections to the server
server.listen(4)
#This list caries the active clients in the server
clients = []
#This list saves the clients username that they wish to be called
#during the conversation
nicknames= []
#This function is used to send a message from a client
#to every other client in that server
def broadcast(message):
    for client in clients:
        client.send(message)
#This fuction is used by thread to use the broadcast fuction if
#a client sends a message
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} has left the server!'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break
#This function connects the new client to the server and
#uses handle function for the client
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('MSG'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("nickname is {}".format(nickname))
        broadcast("{} has joined the server!".format(nickname).encode('utf-8'))
        client.send('You are now connected to server!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

#Start of code
print("server running.....")
receive()

