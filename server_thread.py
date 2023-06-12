from socket import *
import socket
import threading
import logging
import time
import sys
import datetime
import pytz

class ProcessTheClient(threading.Thread):
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(32)
            if data:
                if data.startswith(b"TIME") and data.endswith(b"\r\n"):
                    wib = pytz.timezone('Asia/Jakarta')
                    current_time = datetime.datetime.now(wib).strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode('utf-8'))
                    logging.warning(f"Received message from {self.address}: {data.decode('utf-8').strip()}")

            else:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#Parameter socket.AF_Inet merupakan socket yang digunakan untuk IPv4 address family, dimana merupakan address yang paling sering digunakan untuk TCP/IP Networking. Dengan melakukan passing pada parameter ini, socket akan dibuat menjadi TCP socket.
#Transport protokol yang digunakan pada socket dideterminasi pada Parameter socket.SOCK_STREAM, dimana itu merupakan spesifikasi dari sebuah tipe socket yang biasanya digunakan pada komunikasi TCP.
#Jika ingin menggunakan transport protokol UDP, dapat menggunakan socket.SOCK_DGRAM sebagai tipe socketnya.
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0',45000)) #Mengganti bind port address socket menjadi 45000
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()

if __name__=="__main__":
    main()

