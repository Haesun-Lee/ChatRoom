import socket, select
from datetime import datetime
from datetime import timedelta

EXIT = ":Exit"
HAPPY = ":)"
SAD = ":("
TIME = ":mytime"
PLUS_HOUR = ":+1hr"
# broadcast function
def send_to_all (sock, message):
	for socket in connected_list:	# messages will be sent to other clients
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				# if connection == false
				socket.close()
				connected_list.remove(socket)


if __name__ == "__main__":
	name="" # username
	userpassword = ""
	password = []
	chatroom_password = "1234"
 	record={} # username record to avoid duplication
	connected_list = [] # connected user list
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.bind(("localhost", port))
	server_socket.listen(10) # clients can connect up to 10 connections
	connected_list.append(server_socket)

	print "*************************Listening for the clients*************************" 

	while 1:
        # Get the list sockets which are ready 
		rList,wList,error_sockets = select.select(connected_list,[],[])

		for sock in rList:
			# new connection starrts
			if sock == server_socket: 
				# Handle the case in which there is a new connection recieved through server_socket
				sockfd, addr = server_socket.accept()
				name=sockfd.recv(buffer)
				print name
				password = name.split('@')
				print password
				name = password[0]
				userpassword = password[1]
				connected_list.append(sockfd)
				record[addr]=""
				#print "record and conn list ",record,connected_list
                
                # check username duplication
				if name in record.values():
					sockfd.send("\r Username already exist! Try using other username! \n")
					del record[addr]
					connected_list.remove(sockfd)
					sockfd.close()
					continue
				else:
                    #add name and address
					record[addr]=name
					#password=sockfd.recv(buffer)
					#print password
					if len(userpassword)>5:
						sockfd.send("\r The passcode is restricted to a maximum of 5 alpha-numeric characters only. \n")
						del record[addr]
						connected_list.remove(sockfd)
						sockfd.close()
						continue
					if userpassword == chatroom_password:
						print "input password : " + userpassword
						print "Client (%s, %s) connected" % addr," [",record[addr],"]"
						print "Password correct!! "+password[0]+" joined the chat room!"
						sockfd.send("\rWelcome to chat room.\n"+ "* Enter ':Exit' to leave the chatroom\n"+"* Use ':)' to send [feel happy] and ':(' to send [feel sad]\n"+"* Use ':mytime' to send the current time and ':+1hr' to send current time + 1hour\n")
						send_to_all(sockfd, "\r "+name+" joined the conversation \n")
					else:
						print "password incorrect!! Closing the chatroom"
						sockfd.send("INCORRECT")
						continue
						
      					
  
  
			#Some incoming message from a client
			else:
				# Data from client
				try:
					data1 = sock.recv(buffer)
					data=data1[:data1.index("\n")]
                    
                    #get addr of client sending the message
					i,p=sock.getpeername()
					if data == EXIT:
						msg="\r "+record[(i,p)]+" left the conversation \n"
						send_to_all(sock,msg)
						print "Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]"
						del record[(i,p)]
						connected_list.remove(sock)
						sock.close()
						continue
  
					elif data == HAPPY:
						msg="\r"+record[(i,p)]+" : "+"[feeling happy]\n"
						send_to_all(sock,msg)
						continue
  
					elif data == SAD:
						msg="\r"+record[(i,p)]+" : "+"[feeling sad]\n"
						send_to_all(sock,msg)
						continue
                        #print"1"
					elif data == TIME:
						now = datetime.now()
						current_time = now.strftime("%H:%M:%S")
						msg="\r"+record[(i,p)]+" : "+current_time +"\n"
						send_to_all(sock,msg)
						continue
					
					elif data == PLUS_HOUR:
						now = datetime.now()+timedelta(hours=1)
						current_time = now.strftime("%H:%M:%S")
						msg="\r"+record[(i,p)]+" : "+current_time +"\n"
						send_to_all(sock,msg)
						continue
            
  
					else:
						msg="\r "+record[(i,p)]+": "+data+"\n"
						send_to_all(sock,msg)
            
                #abrupt user exit
				except:
					(i,p)=sock.getpeername()
					send_to_all(sock, "\r"+record[(i,p)]+" left the conversation unexpectedly\n")
					print "Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n"
					del record[(i,p)]
					connected_list.remove(sock)
					sock.close()
					continue

	server_socket.close()

