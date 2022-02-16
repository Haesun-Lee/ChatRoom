import socket, select, string, sys


def display(name) :
	you=name +" : "
	sys.stdout.write(you)
	sys.stdout.flush()

def main():

    if len(sys.argv)<2:
        host = raw_input("Enter host ip address: ")
    else:
        host = sys.argv[1]

    port = 5001
    
    # enter user name!
    name=raw_input("Enter username: ")
    password = input("Enter Password:")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connecting to the server host
    try :
        s.connect((host, port))
    except :
        print "Server connection fail"
        sys.exit()

    #if connection == true
    s.send(name)
    display(name)
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [])
        
        for sock in rList:
            # data from the server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print ' \r disconnected from the server\n '
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    display(name)
        
            #user entered a message
            else :
                msg=sys.stdin.readline()
                s.send(msg)
                display(name)

if __name__ == "__main__":
    main()
