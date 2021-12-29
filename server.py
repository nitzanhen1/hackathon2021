# -- coding: utf-8 --

import socket
import enum
import time
import traceback
from socket import *
from threading import *
import struct
import random
from scapy.arch import get_if_addr

SERVER_IP = get_if_addr("eth2") #'172.99.0.37'
UDP_SERVER_PORT = 2037
TCP_SERVER_PORT = 12177
UDP_DEST_PORT = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MSG_TYPE = 0x2
event = Event()

class Server:
    def __init__(self):
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.udp_socket.bind(('172.99.255.255', UDP_SERVER_PORT))
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # as is
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcp_socket.bind((SERVER_IP, TCP_SERVER_PORT))
        #self.tcp_socket.listen(20)
        self.tcp_socket.settimeout(1)
        self.answers = []
        self.players_names = []
        self.players_sockets = []
        self.question = ''
        self.answer = ''

    def send_broadcast_messages(self, udp_socket):
        print(f"\033[94m Server started, listening on IP address {SERVER_IP}")
        message_to_send = struct.pack('Ibh', MAGIC_COOKIE, MSG_TYPE, TCP_SERVER_PORT)
        while len(self.players_names) < 2:
            udp_socket.sendto(message_to_send, ('<broadcast>', UDP_DEST_PORT))
            time.sleep(1)


    def accept_conn(self, broadcast_thread, tcp_socket):
        while len(self.players_names)<2: #broadcast_thread.is_alive() and
            try:
                client_socket, client_address = tcp_socket.accept()
                player = client_socket.recv(2048).decode()
                self.players_names.append(player)
                self.players_sockets.append(client_socket)
            except:
                continue

        time.sleep(10)
        self.go_question()
        q1 = self.question
        ans = self.answer
        player1_conn = Thread(target=self.playGame, args=(self.players_sockets[0],self.players_names[0],q1))
        player2_conn = Thread(target=self.playGame, args=(self.players_sockets[1],self.players_names[1],q1))

        self.answers=[]
        player1_conn.start()
        player2_conn.start()
        player1_conn.join(5)
        player2_conn.join(5)

        #TIMEOUT= 10
        #t_start = time.time()
        #while (time.time() - t_start < 10 and not event.is_set()):
        #    time.sleep(0.5)

        winner = "\033[91m Game Over!\n"
        winner += "\033[93m The correct answer was " + self.answer+"!\n"
        if(len(self.answers)==0):
            winner+= "\033[92m The game ended in a Draw!"
        else:
            winner += "\033[92m Congratulations to the winner: "
            if self.answers[0][0]==self.answer:
                winner += self.answers[0][1]
            else:
                if self.answers[0][1]==self.players_names[0]:
                    winner+=self.players_names[1]
                else:
                    winner+=self.players_names[0]

        try:
            self.players_sockets[0].send(winner.encode())
        except:
            print()

        try:
            self.players_sockets[1].send(winner.encode())
        except:
            print()

        print("\033[96m Game over, sending out offer requests...")

        self.players_sockets[0].close()
        self.players_sockets[1].close()
        self.players_names = []
        self.answers =[]
        self.players_sockets = []

    def playGame(self,player_socket, player_name,q1):
        msg = "\033[91m Welcome to Quick Maths.\n"
        msg += "\033[93m Player 1: "+str(self.players_names[0])
        msg += "\033[92m Player 2: "+str(self.players_names[1])
        msg += "\033[96m ==\n"
        msg += "\033[94m Please answer the following question as fast as you can:\n"
        msg += "\033[95m How much is "+str(q1)+"?"

        try:
            player_socket.send(msg.encode())
            player_socket.settimeout(10)
            ans_client = player_socket.recv(BUFFER_SIZE).decode()
            self.answers.append((ans_client,player_name))
            event.set()
        except:
            return

    def go_question(self):
        opp = random.choice(['+', '-'])
        ans = random.randint(0, 9)
        if opp == '+':
            op1 = random.randint(1, ans)
            op2 = ans - op1
        else:
            op1 = random.randint(ans, 100)
            op2 = op1 - ans
        self.question = str(op1) + opp + str(op2)
        self.answer = str(ans)


    def waiting_for_clients(self):
        """
            This function sends UDP broadcast messages each 1 sec
            for 10 seconds and listening for clients responses.
        """
        try:
            self.tcp_socket.listen(20)
        except:
            return
        broadcast_thread = Thread(target=self.send_broadcast_messages, args=(self.udp_socket,))
        accpt_conn_thread = Thread(target=self.accept_conn, args=(broadcast_thread, self.tcp_socket))
        broadcast_thread.start()
        accpt_conn_thread.start()
        broadcast_thread.join()
        accpt_conn_thread.join()


def Main():
    server = Server()
    while True:
        server.waiting_for_clients()

if __name__ == '__main__':
    Main()
