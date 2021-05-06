import socket 
import select #what is the use of select? 
import sys 
from thread import *
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 

IP_address = str(sys.argv[1])
PORT = int(sys.argv[2])

server.bind((IP_address,PORT))

server.listen(100)

list_of_clients = []

def clientthread(conn, addr):
    global list_of_clients
    conn.send("Welcome to the chatroom!")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                message_send = "<"+addr[0]+"> "+ message
                print(message_send)
                broadcast(message_send,conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message.encode()) 
            except: 
                clients.close() 
                remove(clients)
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+' connected')
    start_new_thread(clientthread, (conn,addr))
conn.close()
server.close()