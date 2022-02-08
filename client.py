import socket
import threading
import sys 

nickname = input("Choose Your Name:")
password = input("Enter Password:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect to a host
client.connect(('127.0.0.1',5555))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection is Refused !! Wrong Password")
                        stop_thread = True
            else:
                print(message)
        except:
            print('Error Occured while Connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        #Getting Messages 
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()


#if __name__ == "__main__":

#    sys.exit(chat_client())