# -- coding: utf-8 --

import socket
import enum
import time
import traceback
from socket import *
from threading import *
import struct
import random

SERVER_IP = gethostbyname(gethostname())
UDP_SERVER_PORT = 2037  # //TODO: random?
TCP_SERVER_PORT = 12177   #TODO: check?
UDP_DEST_PORT = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MSG_TYPE = 0x2
event = Event()

class Server:
    def __init__(self):
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.players_names = []
        self.players_sockets = []
        self.players_addr = []
        self.game_treads = {}#?
        self.players = {}#?
        self.answers =[]
        self.equations = {'1+1':'2', '1+2':'3'}#TODO change to dict+change the questions

    def send_broadcast_messages(self, udp_socket):
        print("in broadcast")
        print(f"Server started, listening on IP address {SERVER_IP}")  #TODO where?
        message_to_send = struct.pack('Ibh', MAGIC_COOKIE, MSG_TYPE, TCP_SERVER_PORT)
        while len(self.players_names) < 2:
            udp_socket.sendto(message_to_send, ('<broadcast>', UDP_DEST_PORT))
            time.sleep(1)


    def accept_conn(self, broadcast_thread, tcp_socket):
        print("in accept")
        while broadcast_thread.is_alive() and len(self.players_names)<2:
            print(len(self.players_names))
            try:
                client_socket, client_address = tcp_socket.accept()
                player = client_socket.recv(2048).decode()
                self.players_names.append(player)
                print(player)
                self.players_sockets.append(client_socket)
                self.players_addr.append(client_address)
                print("client connected:"+ str(player)+" sock: "+ str(client_socket)+" addr: "+str(client_address))
            except timeout:
                # traceback.print_exc()
                continue
        time.sleep(3)# TODO 10 sec

        questions = list(self.equations)
        inx = random.randint(0, len(questions) - 1)
        q1 = questions[inx]
        ans = self.equations[q1]
        player1_conn = Thread(target=self.playGame, args=(self.players_sockets[0],self.players_names[0],q1))
        player2_conn = Thread(target=self.playGame, args=(self.players_sockets[1],self.players_names[1],q1))
        self.answers=[]
        player1_conn.start()
        player2_conn.start()

        TIMEOUT= 10
        t_start = time.time()
        while (time.time() - t_start < 10 and not event.is_set()):
            time.sleep(0.5)

        #player1_conn.join()
        #player2_conn.join()
        print(self.answers)

        winner = "Game Over!\n"
        winner += "The correct answer was " + ans+"!\n"
        if(len(self.answers)==0):
            winner+= "The game ended in a Draw!"
        else:
            winner += "Congratulations to the winner:\n"
            if self.answers[0][0]==ans:
                winner += self.answers[0][1]
            else:
                if(self.answers[0][1]==self.players_names[0]):
                    winner+=self.players_names[1]
                else:
                    winner+=self.players_names[0]
        print(winner)

        print(self.answers)
        try:
            self.players_sockets[0].send(winner.encode())
        except:
            print(f" disconnected: {self.players_names[0]}")
        self.players_sockets[0].close()

        try:
            self.players_sockets[1].send(winner.encode())
        except:
            print(f" disconnected: {self.players_names[1]}")
        self.players_sockets[1].close()

        print("Game over, sending out offer requests...")


        while True:#TODO: delete
            print("end game")
            time.sleep(4)

    def playGame(self,player_socket, player_name,q1):
        msg = "Welcome to Quick Maths.\n"
        msg += "Player 1: "+str(self.players_names[0])
        msg += "Player 2: "+str(self.players_names[1])
        msg += "==\n"
        msg += "Please answer the following question as fast as you can:\n"
        msg += "How much is "+str(q1)+"?"
        player_socket.send(msg.encode())

        player_socket.settimeout(10)
        try:
            ans_client = player_socket.recv(BUFFER_SIZE).decode()
            self.answers.append((ans_client,player_name))
            event.set()
            print(ans_client)
            print(player_name)
            # if ans_client[0] == ans:
        except timeout:
            print("timeout")


    def waiting_for_clients(self):
        """
            This function sends UDP broadcast messages each 1 sec
            for 10 seconds and listening for clients responses.
        """
        self.udp_socket.bind((SERVER_IP, UDP_SERVER_PORT))
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # as is

        self.tcp_socket.bind((SERVER_IP, TCP_SERVER_PORT))
        self.tcp_socket.listen(20)
        self.tcp_socket.settimeout(1) # ???
        broadcast_thread = Thread(target=self.send_broadcast_messages, args=(self.udp_socket,))
        accpt_conn_thread = Thread(target=self.accept_conn, args=(broadcast_thread, self.tcp_socket))
        broadcast_thread.start()
        accpt_conn_thread.start()
        # broadcast_thread.join() #????
        accpt_conn_thread.join()
        self.udp_socket.close()
        self.tcp_socket.close()


def Main():
    server = Server()
    while True:
        server.waiting_for_clients()
        #t1 = threading.Thread(target=acceptThreadFunction, args=(server,))
        #t1.start()
        #server.waitForClients()
        #server.manageGame()


if __name__ == '__main__':
    Main()

#server=Server()
#while True:
#server.waiting_for_clients()