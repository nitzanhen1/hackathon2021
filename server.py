"""
Created on Fri Dec 24 18:29:01 2021

@author: ניצן חן
"""
import socket

'''
import socket
import threading

HEADER = 64
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
'''



import enum
import time
import traceback
from socket import *
from threading import *
import struct
import random

SERVER_IP = gethostbyname(gethostname())
UDP_SERVER_PORT = 12177  # //TODO: random?
TCP_SERVER_PORT = 2037  #TODO: check?
UDP_DEST_PORT = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MSG_TYPE = 0x2

class Server:
    def _init_(self):
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.connections = {} # Players: "player1":
        self.game_treads = {}#?
        self.players = {}#?
        self.equations = {'1+1':'2', '1+2':'3'}#TODO change to dict+change the questions

    def send_broadcast_messages(self, udp_socket):
        print(f"Server started, listening on IP address {SERVER_IP}")  #TODO where?
        message_to_send = struct.pack('Ibh', MAGIC_COOKIE, MSG_TYPE, TCP_SERVER_PORT)
        while len(self.connections) < 2:
            udp_socket.sendto(message_to_send, ('<broadcast>', UDP_DEST_PORT))
            time.sleep(1)


    def accept_conn(self, broadcast_thread, tcp_socket):
        while broadcast_thread.is_alive():
            print(len(self.connections))
            try:
                client_socket, client_address = tcp_socket.accept()
                player = client_socket.recv(2048).decode()
                print(player)
                self.connections[player] = (client_socket,  client_address)
                print("client connected:"+ str(player)+" sock: "+ str(client_socket)+" addr: "+str(client_address))
            except timeout:
                # traceback.print_exc()
                continue
        time.sleep(3)# TODO 10 sec
        self.playGame()


        while True:#TODO: delete
            print("play game")
            time.sleep(1)

    def playGame(self):
        players= list(self.connections)
        player1 = players[0]
        player2 = players[1]
        msg = "Welcome to Quick Maths.\n"
        msg += "Player 1: "+str(player1)
        msg += "Player 2: "+str(player2)
        msg += "==\n"
        msg += "Please answer the following question as fast as you can:\n"
        questions = list(self.equations)  # TODO: save attribute
        inx = random.randint(0,len(questions)-1)
        q1 = questions[inx]
        ans = self.equations[q1]
        msg += "How much is "+str(q1)+"?"
        for player,tup_client in self.connections.items():
            tup_client[0].send(msg.encode())
        #TODO : time out 10 seconds
        winner = "Game Over!\n"
        winner += "The correct answer was " + ans+"!\n"
        winner += "Congratulations to the winner:\n"
        ans_client, addr_client = self.tcp_socket.recv(BUFFER_SIZE).decode()
        #if ans_client[0] == ans:








    def waiting_for_clients(self):
        """
            This function sends UDP broadcast messages each 1 sec
            for 10 seconds and listening for clients responses.
        """
        self.udp_socket.bind(('', UDP_SERVER_PORT))
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # as is

        self.tcp_socket.bind(('', TCP_SERVER_PORT))
        self.tcp_socket.listen(20)
        self.tcp_socket.settimeout(1) # ???
        broadcast_thread = Thread(target=self.send_broadcast_messages, args=(self.udp_socket,))
        accpt_conn_thread = Thread(target=self.accept_conn, args=(broadcast_thread, self.tcp_socket))
        broadcast_thread.start()
        accpt_conn_thread.start()
        # broadcast_thread.join() # Changed by Peleg.
        accpt_conn_thread.join()
        self.udp_socket.close()
        self.tcp_socket.close()




server=Server()
#while True:
server.waiting_for_clients()