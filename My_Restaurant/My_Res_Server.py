# Server for My_Restaurant's Kitchen and Waiter Systems.
# Server will be created using sockets and its processes will be controlled using threads
# Author O. Raphael Mapp


import socket
import threading
from tkinter import ttk
import tkinter as tk

HOST = '127.0.0.1.'
PORT = 55556
running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def bindSockets():
    # function will connect our clients, kitchen and waiter windows, to the server
    try:
        server.bind((HOST,PORT))
        server.listen(5)
    except ConnectionAbortedError:
        print('Socket binding error' + '\n' + 'Retrying. . .')
        bindSockets()

# lists to store clients and addresses that are appended by receive connections function
clients = []
addresses = []

# broadcast function
def broadcast(order):
    """:arg order -> will be received from waiter machine and sent to kitchen machine
    """
    for client in clients:
        client.send(order)

# handle connections function
def handle(client):
    """':arg client -> any machine that is connected to server will be enabled to send msgs
    and have them broadcast
    """
    while True:
        try:
            order = client.recv(1024)
            broadcast(order)
        except Exception as e:
            print(f'Program failed because of error: {str(e)}')
            break


# receive function Accepts users connecting to server, appends them to clients list and starts thread
def receiveConnections():
    """ accepts connections from clients, appends them and their addresses to respective lists
    and assigns them a thread
    """
    for c in clients:
        c.close()
    del clients[:]
    del addresses[:]

    # while loop to ensure server is always waiting to accept potential connections
    while True:
        try:
            client, address = server.accept()
            server.setblocking(1)       # prevents timeout
            clients.append(client)
            addresses.append(address)
            print(f"(str{client}) connected with {str(address[0])}!")
        except ConnectionAbortedError:
            print('Error establishing connections')
            break

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

bindSockets()
print('Incoming orders . .')
receiveConnections()

