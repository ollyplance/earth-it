import pygame

#data for sockets to transfer. I needed to do this because it was
#too much for sockets to handle before. You have to send little amounts

class PlayerData():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.terrainChanged = [0,0,0]
        self.lives = 5
        self.died = False
        self.homeScreen = True
        self.movingDir = 0
        self.spritenum = 0
        self.collideWithEnemy = False
        self.inventoryBlockSelected = 0

    def __repr__(self):
        return f"{self.x}, {self.y}"
