import socket
from earth_caveGeneration import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "2601:547:500:4880:7586:525f:3191:f4a8"
        self.port = 1050
        self.addr = (self.server, self.port)
        self.msg = self.connect()

    def getMsg(self):
        return self.msg

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode("UTF-8")
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode("UTF-8")

        except socket.error as e:
            print(e)
