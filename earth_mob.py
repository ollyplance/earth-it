import pygame
from earth_terrainBlock import *
import math

#this is the mob class, almost all of the functions are similar to the player class

class Zombie(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height, terrainMap):
        pygame.sprite.DirtySprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xvel = 2
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
        self.xMove = 0
        self.yMove = 0
        self.lives = 10
        self.sprites = []
        #image modified from https://www.spriters-resource.com/download/77319/
        self.standingsprite = pygame.image.load(f"zombiestanding.png")
        self.movingDir = 0
        self.spritenum = 0
        self.makeSprites()
        self.died = False
        self.countSinceDied = 0

    def makeSprites(self):
        #images modified from https://www.spriters-resource.com/download/77319/
        self.sprites = [pygame.image.load(f"zombiewalking{n}.png") for n in range(1,5)]

    def getMapInsideBounds(self, terrainMap, scrollX, scrollY, transparent = False):
        blocklist = []
        colStart = (scrollX // 20)
        rowStart = int(scrollY // 20)
        transparentList = [17,18,19,20]
        if(not transparent):
            for row in range(rowStart, rowStart + 33):
                for col in range(colStart - 1, colStart + 39):
                    if(terrainMap[row][col] != 0):
                        blocklist.append(TerrainBlock(
                            row, col, 20, terrainMap[row][col]))
            blocks = pygame.sprite.LayeredDirty(blocklist)
            return blocks
        if(transparent):
            for row in range(rowStart, rowStart + 33):
                for col in range(colStart - 1, colStart + 39):
                    if(terrainMap[row][col] != 0 and terrainMap[row][col] not in transparentList):
                        blocklist.append(TerrainBlock(
                            row, col, 20, terrainMap[row][col]))
            blocks = pygame.sprite.LayeredDirty(blocklist)
            return blocks

    # move function modified from https://stackoverflow.com/questions/44721130/pygame-collision-detection-with-walls
    def move(self, xvel, yvel, blocks):
        blocks.update(self.scrollX, self.scrollY)
        if(xvel != 0):
            self.x += xvel
            self.rect = pygame.Rect(
                self.x - self.scrollX, self.y - self.scrollY, self.width, self.height)
            blockList = pygame.sprite.spritecollide(self, blocks, 0)
            for block in blockList:
                if(xvel < 0):
                    self.x = block.x + block.cellSize
                elif(xvel > 0):
                    self.x = block.x - self.width
                break
            if(blockList != [] and not self.jumping and not self.falling):
                self.jumping = True
                self.jumpCount = 5.272

        if(yvel != 0):
            if(yvel > 0):
                self.falling = True
            (row, col) = self.getMapCords()
            bBelow = None
            r = row
            if(self.blockBelow == None or xvel != 0):
                while(bBelow == None and r < len(self.terrainMap)):
                    if(r >= 0):
                        if(self.terrainMap[r][col] != 0):
                            bBelow = r
                    r += 1
            self.blockBelow = bBelow
            self.y += yvel

            if(self.blockBelow != None and self.y > ((self.blockBelow * 20) + self.scrollY)):
                self.y = (self.blockBelow * 20) + self.scrollY
                self.blockBelow = None
                self.falling = False

            self.rect = pygame.Rect(
                self.x - self.scrollX, self.y - self.scrollY, self.width, self.height)
            blockList = pygame.sprite.spritecollide(self, blocks, 0)
            for block in blockList:
                if(yvel < 0):
                    self.y = block.y + block.cellSize
                elif(yvel > 0):
                    self.y = block.y - self.height
                    self.falling = False
                break

            self.rect = pygame.Rect(
                self.x - self.scrollX, self.y - self.scrollY, self.width, self.height)
            blockList = pygame.sprite.spritecollide(
                self, blocks, 0)
            for block in blockList:
                if(yvel < 0):
                    self.y = block.y + block.cellSize
                elif(yvel > 0):
                    self.y = block.y - self.height
                    self.falling = False
                break

        self.rect = pygame.Rect(self.x,
                                self.y, self.width, self.height)

    def getMapCords(self):
        x = self.x
        y = self.y
        col = x // 20
        row = (y) // 20
        return int(row), col

# copied from: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#sidescrollerExamples
# scrolls to make the player visible as needed
    def makePlayerVisible(self):
        if (self.x < self.scrollX + self.scrollXMargin):
            self.scrollX = self.x - self.scrollXMargin
        if (self.x > self.scrollX + self.width + 760 - self.scrollXMargin):
            self.scrollX = self.x - 760 + self.scrollXMargin - self.width
        if (self.y < self.scrollY + self.scrollYMargin):
            self.scrollY = self.y - self.scrollYMargin
        if (self.y > self.scrollY + self.height + 650 - self.scrollYMargin):
            self.scrollY = self.y - 650 + self.scrollYMargin - self.height

    def update(self):
        self.makePlayerVisible()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dirty = 1

    def draw(self, win, terrainMap, scrollX, scrollY):

        blocks = self.getMapInsideBounds(terrainMap,
                                         int(self.scrollX), int(self.scrollY), True)

        if(self.jumping and not self.falling):
            if self.jumpCount >= 0:
                yval = (-1) * (self.jumpCount**2) * .5
                self.move(0, yval, blocks)
                self.jumpCount -= 2
            else:
                self.jumpCount = 0
                self.jumping = False
                self.falling = True

        if(self.falling):
            yval = (1) * (self.jumpCount**2) * .5
            self.move(self.xMove*self.xvel, yval, blocks)
            self.jumpCount -= 2
        elif(not self.falling and not self.jumping):
            self.jumpCount = 0
            self.jumping = False
            self.falling = False

        if(self.jumping):
            self.spritenum += 1
            self.move(self.xMove*self.xvel, 0, blocks)
        else:
            self.spritenum += 1
            self.move(self.xMove*self.xvel, 1, blocks)

        if(self.xMove < 0):
            self.movingDir = -1
        elif(self.xMove > 0):
            self.movingDir = 1
        else:
            self.movingDir = 0
        self.rect = pygame.Rect(self.x - scrollX, self.y - scrollY, self.width, self.height)
        if(self.movingDir == -1):
            self.image = pygame.transform.flip(self.sprites[self.spritenum % 4], True, False)
        elif(self.movingDir == 1):
            self.image = self.sprites[self.spritenum % 4]
        else:
            self.image = self.standingsprite

        win.blit(self.image, self.rect)
        healthleft = pygame.Rect(self.x - scrollX - 5, self.y - scrollY - 5, 3*self.lives, 3)
        pygame.draw.rect(win, (255, 0, 0), healthleft)

