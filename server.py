# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:29:01 2021

@author: ניצן חן
"""

import socket
import threading

HEADER = 64
'''
PORT = 13117
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
'''
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

UDPserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPserver.bind(('', 13117))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()