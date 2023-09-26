import pygame
from earth_terrainBlock import *


class Mob(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height, terrainMap):
        pygame.sprite.DirtySprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xvel = 10
        self.jumping = False
        self.falling = False
        self.left = False
        self.right = False
        self.jumpCount = 5.272
        self.terrainMap = terrainMap
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.image = pygame.image.load("emoji_face.png")
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.scrollX = 20000
        self.scrollXMargin = 0
        self.scrollY = 0
        self.scrollYMargin = 0
        self.blockBelow = None


class Zombie2(Mob):
    def update(self):
        self.rect = pygame.Rect(self.x,
                                self.y, self.width, self.height)
        self.dirty = 1

    def draw(self, win):
        self.rect = pygame.Rect(self.x,
                                self.y, self.width, self.height)
        pygame.draw.rect(win, (28, 133, 56), (self.rect))

    def __repr__(self):
        return f"{self.x},{self.y}"
