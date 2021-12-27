# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:29:11 2021

@author: ניצן חן
"""
'''
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
'''
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
        self.team_name = "PD1"
        self.ip = CLIENT_IP
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.udp_socket.bind(('', localPORTUDP))  # bind socket to local port number ??
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
        #self.udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        #self.udp_socket.bind(('', localPORTUDP))  # bind socket to local port number ??

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
                try:
                    print('good')
                    # send team name to server
                    self.send_name()
                except:
                    print('bad')
                    self.tcp_socket.close() # why?
                    continue
                break
            except:
                continue
        self.udp_socket.close()

client=Client()
client.start_run()


