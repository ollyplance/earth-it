import pygame
from earth_terrainBlock import *
import math

#zombie data class that also moves the player

class ZombieData():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lives = 10
        self.died = False

#modified from https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame
#determines closest player and moves in that direction
    def move_towards_player(self, playerX, player2X):
        # Find direction vector (dx, dy) between enemy and player.
        if(self.died):
            self.x = 20100
        else:
            dx, dy = min(playerX - self.x, player2X - self.x), 0
            if(dx > 200 or dx < -200):
                dx = 0
            dist = math.hypot(dx, dy)
            if(dist == 0):
                dist = .01
            dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.

            self.xMove = dx
            self.yMove = dy

    def __repr__(self):
        return f"{self.x}, {self.y}"

