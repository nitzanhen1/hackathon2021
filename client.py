# -- coding: utf-8 --

import random
import struct
from socket import *
from threading import Thread

localPORTUDP = 13117
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MSG_TYPE = 0x2

class Client:
    def __init__(self):
        self.team_name = "PyCharmers"
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.udp_socket.bind(('', localPORTUDP))

    def connect_to_server(self, server_ip, server_port):
        """
        This function sends a connection request to the server.
        """
        try:
            self.tcp_socket.connect((server_ip, server_port))
        except:
            return

    def send_name(self):
        try:
            msg = self.team_name + '\n'
            self.tcp_socket.send(msg.encode())
        except:
            return

    def start_run(self):
        """
        This function lets the client to listen for boradcast from the server,
        and then sends the Client's Team Name to the Server
        """
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        print(" Client Started, listening for offer requests...")

        while True:
            try:
                msg, server_address = self.udp_socket.recvfrom(BUFFER_SIZE) #read reply characters fromsocket into string
                unpacked_msg = struct.unpack('Ibh', msg) #unpacking the message for a tuple with :
                magic_cookie = unpacked_msg[0]
                msg_type = unpacked_msg[1]
                server_port = unpacked_msg[2]
                if magic_cookie != MAGIC_COOKIE or msg_type != MSG_TYPE:
                    continue
                print(f' Received offer from {server_address[0]}, attempting to connect...')
                self.connect_to_server(server_address[0], server_port)
                self.send_name()
                self.connected()
                break;
            except:
                continue

    def connected(self):
        while True:  # game
            try:
                #server welcome msg
                question = self.tcp_socket.recv(BUFFER_SIZE).decode()  # questions
                print(question)
                break
            except:
                continue
        play_thread = Thread(target=self.playGame, args=())
        play_thread.start()
        while True:
            try:
                # server game over msg
                winner = self.tcp_socket.recv(BUFFER_SIZE).decode()
                print(winner)
                self.tcp_socket.close()
                print("\033[97m server disconnected, listening for offer requests...")
                break
            except:
                continue



    def playGame(self):
        try:
            ans = input()[0]
            self.tcp_socket.send(ans.encode())
        except:
            return


client=Client()
while True:
    client.start_run()