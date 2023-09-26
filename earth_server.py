import socket
from _thread import *
import sys
from earth_caveGeneration import *


server = "2601:547:500:4880:7586:525f:3191:f4a8"
port = 1050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_msg(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])


def make_msg(tup, terrainChanged):
    return str(int(tup[0])) + "," + str(int(tup[1])) + ',' + str(terrainChanged[0]) + ',' + \
        str(terrainChanged[1]) + ',' + str(terrainChanged[2])


pos = [(20350, 320), (20380, 320)]

# terrainMap = constructCave(150, 2000, 4, 4, 3, .5)
# top = [([0] * 2000) for i in range(18)]
# terrainMap = top + terrainMap

terrainChanged = [[0, 0, 0], [0, 0, 0]]


def threaded_client(conn, player):
    conn.send(str.encode(make_msg(pos[player], [0, 0, 0])))

    reply = ""
    while True:
        try:
            data = read_msg(conn.recv(2048).decode("UTF-8"))
            pos[player] = data[0], data[1]
            terrainChanged[player] = data[2], data[3], data[4]

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                    tChan = terrainChanged[0]
                else:
                    reply = pos[1]
                    tChan = terrain[1]

                print("Received: ", data)
                print("Sending : ", reply + tChan)

            conn.sendall(str.encode(make_msg(reply, tChan)))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
