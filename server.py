import socket
import threading
import sys 
import select

host = "127.0.0.1"
port = 5555 # Choose any random port which is not so common (like 80)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the server to IP Address
server.bind((host, port))
#Start Listening Mode
server.listen()
#List to contain the Clients getting connected and nicknames
clients = []
nicknames = []

#Broadcasting Method
def broadcast(message):
    for client in clients:
        client.send(message)

# Recieving Messages from client then broadcasting
def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)  
            broadcast(message)   # As soon as message recieved, broadcast it.
        
        except:
            if client in clients:
                index = clients.index(client)
                #Index is used to remove client from list after getting diconnected
                client.remove(client)
                client.close
                nickname = nicknames[index]
                broadcast(f'{nickname} left the Chat!'.encode('ascii'))
                nicknames.remove(nickname)
                break

# Main Recieve method
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # Ask the clients for Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client.send('PASS'.encode('ascii'))
        password = client.recv(1024).decode('ascii')
        # I know it is lame, but my focus is mainly for Chat system and not a Login System
        if password != '1234':
            client.send('REFUSE'.encode('ascii'))
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the Chat'.encode('ascii'))
        client.send('Connected to the Server!'.encode('ascii'))

        # Handling Multiple Clients Simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


#Calling the main method
print('Server is Listening ...')
recieve()

 
#if __name__ == "__main__":

#    sys.exit(chat_server())