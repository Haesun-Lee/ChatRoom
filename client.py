import socket, select, string, sys, argparse




def display(name) :
	you=name +" : "
	sys.stdout.write(you)
	sys.stdout.flush()

def main():
    
    #if len(sys.argv)<2:
        #host = input("Enter host ip address: ")
    #else:
        #host = sys.argv[1]
    

    #port = 5001
    
    # enter user name!
    #name=input("Enter username: ")
    #password = input("Enter Password:")
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-join', action="store_true")
    parser.add_argument('-host')
    parser.add_argument('-port')
    parser.add_argument('-username')
    parser.add_argument('-passcode')
    args = parser.parse_args()

    host = args.host
    port = args.port
    name = args.username
    password = args.passcode

    print(host + port + name + password)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connecting to the server host
    try :
        #print("testing try")
        s.connect((host, int(port)))
        
    except :
        print ("Server connection fail")
        sys.exit()

    name = name + "@" + password 
    #if connection == true
    s.send(name.encode("utf-8"))
    print(name)
    #s.sendall(b"@")
    #s.send(password.encode("utf-8"))
    #print(password)
    display(name)
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [])
        
        for sock in rList:
            # data from the server
            if sock == s:
                data = sock.recv(4096).decode("utf-8")
                if not data :
                    print (' \r disconnected from the server\n ')
                    sys.exit()
                elif data == "INCORRECT":
                    print (' \r disconnected from the server\n ')
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display(name)
        
            #user entered a message
            else :
                msg=sys.stdin.readline()
                s.send(msg.encode("utf-8"))
                display(name)

if __name__ == "__main__":
    main()
