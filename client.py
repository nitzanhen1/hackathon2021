# -- coding: utf-8 --

import random
import struct
import time
import traceback
from struct import *
from socket import *
import enum
from msvcrt import getch
from threading import Thread
#import keyboard
#from scapy.all import *



# CLIENT_IP = get_if_addr("eth0") # 172.1.0 (eth1)
# CLIENT_IP = '172.1.0/24'
CLIENT_IP = '172.0.0.1'
# CLIENT_IP = gethostbyname(gethostname())  # 172.99.0 (eth2)
localPORTUDP = 13117
#localPORTTCP = 2037
BUFFER_SIZE = 2048
MAGIC_COOKIE = 0xabcddcba
MSG_TYPE = 0x2

class Client:
    def __init__(self):
        self.team_name = "PD"+ str(random.randint(0,10))
        self.ip = CLIENT_IP
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)#?
        self.game_is_on = False

    def connect_to_server(self, server_ip, server_port):
        """
        This function sends a connection request to the server.
        """
        #self.tcp_socket.bind(('', localPORTTCP))
        self.tcp_socket.connect((server_ip, server_port))
        print("Connected to Server")

    def send_name(self):
        msg = self.team_name + '\n'
        self.tcp_socket.send(msg.encode())
        print("send"+ str(msg))

    def send_to_server(self, event):
        """
        This function sends an event to the server.
        :param event: event to send
        """
        try:
            print(event.name)
            self.tcp_socket.send(event.name.encode())
        except:
            print("something went wrong - with key pressing sending from CLIENT to SERVER")

    def start_run(self):
        """
        This function lets the client to listen for boradcast from the server,
        and then sends the Client's Team Name to the Server
        """
        print("Client Started, listening for offer requests...")
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #TODO try to delete
        self.udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #TODO change to port
        self.udp_socket.bind(('', localPORTUDP))  # bind socket to local port number ??

        while True:
            try:
                msg, server_address = self.udp_socket.recvfrom(BUFFER_SIZE) #read reply characters fromsocket into string
                unpacked_msg = struct.unpack('Ibh', msg) #unpacking the message for a tuple with :
                magic_cookie = unpacked_msg[0]
                msg_type = unpacked_msg[1]
                server_port = unpacked_msg[2]
                if magic_cookie != MAGIC_COOKIE or msg_type != MSG_TYPE:
                    continue
                print(f'Received offer from {server_address[0]}, attempting to connect...')
                self.connect_to_server(server_address[0], server_port)
                self.send_name()
                while True:  #game
                    try:
                        data = self.tcp_socket.recv(BUFFER_SIZE).decode()  #questions
                        print(data)
                        ans = input()  #TODO: verify 1 char, time out
                        print(ans)
                        self.tcp_socket.send(ans.encode())
                    except:
                        print('bad')
                        self.tcp_socket.close()  # why?
                        break

                break
            except:
                continue
        self.udp_socket.close()

client=Client()
client.start_run()