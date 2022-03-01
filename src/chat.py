import socket
import threading
import queue
import sys
import random
import os


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
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000)
    serverPort = int(input("Input the port of server: "))
    print("Client IP = "+str(host))
    print("Port = "+str(port))
    server = (str(serverIP),serverPort)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))

    userName = input('Ener your username: ')
    if userName == '':
        userName = 'GuestUser'+str(random.randint(1,1000))
        print('Your guest username is: '+userName)
    s.sendto(userName.encode('utf-8'),server)
    threading.Thread(target=ReceiveData,args=(s,)).start()
    while True:
        data = input()
        if data == 'qqq':
            break
        elif data=='':
            continue
        data = '['+userName+']' + '->'+ data
        s.sendto(data.encode('utf-8'),server)
    s.sendto(data.encode('utf-8'),server)
    s.close()
    os._exit(1)



#Server
#Run chat.py
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    host = socket.gethostbyname(socket.gethostname())
    port = int(input("Input server port: "))
    print('Server hosting on IP-> '+str(host))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData,args=(s,recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    s.sendto(data.encode('utf-8'),c)
    s.close()
#Server

