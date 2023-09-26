#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
# updated by Ping-Ya Chao
#############################

import socket
import threading
from queue import Queue

from cmu_112_graphics import *
from tkinter import *
from dots import *
import random


##########################################
# customize the functions within MyApp
##########################################

class MyApp(App):
    ## 2 new functions specific to sockets! ##
    @staticmethod
    def setUpServer():
        HOST = ""  # put your IP address here if playing on multiple computers
        PORT = 50001

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOST, PORT))
        print("connected to server")

        serverMsg = Queue(100)
        threading.Thread(target=MyApp.handleServerMsg, args=(server, serverMsg)).start()

        return server, serverMsg

    @staticmethod
    def handleServerMsg(server, serverMsg):
        server.setblocking(1)
        msg = ""
        command = ""
        while True:
            msg += server.recv(10).decode("UTF-8")
            command = msg.split("\n")
            while len(command) > 1:
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverMsg.put(readyMsg)
                command = msg.split("\n")

    ## You've seen the remaining function structure in the 112 animation framework! ##
    def appStarted(self):
        self.server, self.serverMsg = self.setUpServer()
        self.me = Dot("Lonely", self.width/2, self.height/2)
        self.otherStrangers = dict()

    def keyPressed(self, event):
        dx, dy = 0, 0
        msg = ""

        # moving
        if event.key in ["Up", "Down", "Left", "Right"]:
            speed = 5
            if event.key == "Up":
                dy = -speed
            elif event.key == "Down":
                dy = speed
            elif event.key == "Left":
                dx = -speed
            elif event.key == "Right":
                dx = speed
            # move myself
            self.me.move(dx, dy)
            # update message to send
            msg = f"playerMoved {dx} {dy}\n"

        # teleporting
        elif event.key == "Space":
            # get a random coordinate
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            # teleport myself
            self.me.teleport(x, y)
            # update the message
            msg = f"playerTeleported {x} {y}\n"

        elif event.key == "c":
            num = self.me.num + 1
            self.me.num = num
            msg = f"numberChanged {num}\n"

        # send the message to other players!
        if msg != "":
            print("sending: " + msg)
            self.server.send(msg.encode())

    # timerFired receives instructions and executes them
    def timerFired(self):
        while self.serverMsg.qsize() > 0:
            msg = self.serverMsg.get(False)
            try:
                print("received: " + msg + "\n")
                msg = msg.split()
                command = msg[0]

                if command == "myIDis":
                    myPID = msg[1]  # Note: pID is just an abbreviation for player ID
                    self.me.changePID(myPID)

                elif command == "newPlayer":
                    newPID = msg[1]
                    x = self.width/2
                    y = self.height/2
                    self.otherStrangers[newPID] = Dot(newPID, x, y)

                elif command == "playerMoved":
                    pID = msg[1]
                    dx = int(msg[2])
                    dy = int(msg[3])
                    self.otherStrangers[pID].move(dx, dy)

                elif command == "playerTeleported":
                    pID = msg[1]
                    x = int(msg[2])
                    y = int(msg[3])
                    self.otherStrangers[pID].teleport(x, y)

                elif command == "numberChanged":
                    pID = msg[1]
                    num = int(msg[2])
                    self.otherStrangers[pID].numChange(num)

            except:
                print("failed")
            self.serverMsg.task_done()

    def redrawAll(self, canvas):
        # draw other players
        for playerName in self.otherStrangers:
            self.otherStrangers[playerName].drawDot(canvas, "blue")
        # draw me
        self.me.drawDot(canvas, "red")

MyApp(width=200, height=200)
