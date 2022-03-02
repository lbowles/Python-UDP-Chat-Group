
from audioop import add
from ctypes import addressof
import socket
import threading
import queue
import sys
import random
import os
import time

#older version
#TODO: add comments
#TODO: when client exits, store all the messages and then when they rejoin display them
# when disconnected store message in array 

#Client
#Run chat.py <ip address of server>
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

def RunClient(serverIP):
    #client connection information
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000)
    serverPort = int(input("Input the port of server: "))
    print("Client IP = "+str(host))
    print("Client Port = "+str(port))
    print("Welcome to the chatroom, type 'Exit' to exit")
    print("")
    #server connection information
    server = (str(serverIP),serverPort)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    #username input
    userName = input('Enter your username: ')
    if userName == '':
        userName = 'GuestUser'+str(random.randint(1,1000))
        print('Your guest username is: '+userName)
    #connection and starting new thread to server
    s.sendto(userName.encode('utf-8'),server)
    threading.Thread(target=ReceiveData,args=(s,)).start()
    #sends first connection confirmation message
    firstMessage = str("FIRST1923")
        #sending data to server
    s.sendto(firstMessage.encode('utf-8'),server)

    #checking if user wants to exit chatroom
    while True:
        data = input()
        if data == 'Exit':
            break
        elif data=='':
            continue
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        data = '['+current_time+", "+userName+']' + '-> '+ data
        #sending data to server
        s.sendto(data.encode('utf-8'),server)
    #sending message to server
    s.sendto(data.encode('utf-8'),server)
    s.close()
    os._exit(1)




#Server
#Run chat.py
#establish UDP Connection, this will be used to get incoming client data
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    #server information
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("Input server port: "))
    print('Server hosting on IP = '+str(host))
    #create and assign server socket
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    recvPackets = queue.Queue()
    print('The server is running')

    #creates new thread for every client connection
    threading.Thread(target=RecvData,args=(s,recvPackets)).start()
    w, h = 500, 500
    arrCount = 0
    offlineClients = [[0 for x in range(w)] for y in range(h)]

    #constantly checks for new messages from clients
    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            #adds client information to ative client list
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            
            if data.endswith('FIRST1923'):
                arrTempMsg = ""
                for ip in clients:
                    arrTempMsg= arrTempMsg + ip[0]+" "
                message="Connected Clients ["+arrTempMsg+"]"
                s.sendto(message.encode('utf-8'),addr) 
            else :
                
                #stores messages for when a client is disconnected 
                j=0
                while j<len(offlineClients) :
                    if isinstance(offlineClients[j][0], str):
                        k=0
                        while isinstance(offlineClients[j][k],str):  
                            k=k+1
                        offlineClients[j][k] = data
                    j=j+1

                #sends client any messages that it missed
                print(offlineClients)
                if offlineClients :
                    x=0
                    while x<len(offlineClients) :
                        if addr[0]==offlineClients[x][0]:
                            print("MISSED MESSAGES")
                            z = 1 
                            while isinstance(offlineClients[x][z], str):
                                message = (offlineClients[x][z])
                                s.sendto(message.encode('utf-8'),addr)
                                z=z+1
                            offlineClients[x][0] = 0
                        x=x+1

                #disconnects client
                if data.endswith('Exit'):
                    clients.remove(addr)
                    offlineClients[arrCount][0] =addr[0]
                    arrCount=arrCount+1
                    continue
                #sends client confirmation of delivered messages
                if data :
                    for x in clients:
                        if x==addr:
                            message = "<<-- Message Delivered -->>"
                            s.sendto(message.encode('utf-8'),x)
                print(str(addr)+data)
                #sends incoming message to all connected clients
                for c in clients:
                    if c!=addr:
                        s.sendto(data.encode('utf-8'),c)
    s.close()
#Server

if __name__ == '__main__':
    if len(sys.argv)==1:
        RunServer()
    elif len(sys.argv)==2:
        RunClient(sys.argv[1])

