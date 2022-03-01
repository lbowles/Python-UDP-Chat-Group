import socket
import threading
import queue
import sys
import random
import os


#Client
#Run chat.py <server ip>
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

def RunClient(serverIP):
    host = socket.gethostbyname(socket.gethostname())
    clientPort = random.randint(6000,10000)
    serverPort = int(input("Enter server port: "))
    print('Client IP = '+str(host))
    print('Client Port = '+str(clientPort))
    print("Welcome to the chatroom, type 'Exit' to exit")
    print("")
    server = (str(serverIP),serverPort)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,clientPort))

    username = input('Enter your username: ')
    if username == '':
        username = 'Guest'+str(random.randint(1,1000))
        print('Your name is:'+username)
    s.sendto(username.encode('utf-8'),server)
    threading.Thread(target=ReceiveData,args=(s,)).start()
    while True:
        data = input()
        if data == 'Exit':
            break
        elif data=='':
            continue
        data = '<'+username+'>' + '|'+ data
        s.sendto(data.encode('utf-8'),server)
    s.sendto(data.encode('utf-8'),server)
    s.close()
    os._exit(1)



#Server
# Run chat.py 
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    host = socket.gethostbyname(socket.gethostname())
    serverPort = int(input("Enter server port: "))
    print('Server hosting on IP-> '+str(host))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,serverPort))
    clients = set()
    recvPackets = queue.Queue()
    print('The server is running')

    threading.Thread(target=RecvData,args=(s,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('Exit'):
                clients.remove(addr)
                continue
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    s.sendto(data.encode('utf-8'),c)
    s.close()

if __name__ == '__main__':
    if len(sys.argv)==1:
        RunServer()
    elif len(sys.argv)==2:
        RunClient(sys.argv[1])