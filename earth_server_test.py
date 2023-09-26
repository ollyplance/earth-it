import socket
from _thread import *
import sys
from earth_playerData import PlayerData
from earth_caveGeneration import *
from earth_zombieData import *
import pickle

# server code modified and partly copied from https://techwithtim.net/tutorials/python-online-game-tutorial/sending-objects/
#deals with the server side and deals with enemy health

server = ""
port = 10120

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

currentPlayer = 0
players = [PlayerData(20350, 320, 20, 40), PlayerData(20380, 320, 20, 40), ZombieData(20100, 320, 20, 40), 10, 0]


def threaded_client(conn, player):
    conn.send(pickle.dumps([players[player], players[2]]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data[0]
            players[2] = data[1]
            players[2].move_towards_player(players[0].x, players[1].x)
            #send in position of mouse through person, see if clicked and then change data here
            #do not send in individual lives
            print(players[0].collideWithEnemy, players[1].collideWithEnemy)
            if(players[0].collideWithEnemy):
                if(players[0].inventoryBlockSelected == 9):
                    players[3] -= 2
                elif(players[0].inventoryBlockSelected == 23):
                    players[3] -= 4
                elif(players[0].inventoryBlockSelected == 24):
                    players[3] -= 5
                else:
                    players[3] -= 1
                players[0].collideWithEnemy = False

            if(players[1].collideWithEnemy):
                if(players[1].inventoryBlockSelected == 9):
                    players[3] -= 2
                elif(players[1].inventoryBlockSelected == 23):
                    players[3] -= 4
                elif(players[1].inventoryBlockSelected == 24):
                    players[3] -= 5
                else:
                    players[3] -= 1
                players[1].collideWithEnemy = False

            if(players[3] <= 0):
                players[2].died = True

            if(players[2].died):
                players[4] += 1
                if(players[4] > 300):
                    players[2].lives = 10
                    players[3] = 10
                    players[4] = 0
                    players[2].died = False


            players[2].lives = players[3]
            print(f"player2lives: {players[3]}")

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = [players[0], players[2]]
                else:
                    reply = [players[1], players[2]]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
