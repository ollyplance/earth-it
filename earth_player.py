import pygame


class Player(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height, terrainMap, clickMap):
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
        self.scrollXMargin = 250
        self.scrollY = 0
        self.scrollYMargin = 310
        self.blockBelow = None
        self.mouseClicked = False
        self.inventory = dict()
        self.clickMap = clickMap
        self.inventoryPicked = 1
        self.inventoryBlockSelected = None
        self.chestClicked = None
        self.terrainChanged = [0, 0, 0]


    def checkMove(self, blocks):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[2]:
                if(self.chestClicked == None):
                    self.mouseClicked = True
            else:
                self.mouseClicked = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                (row, col) = self.convertClickMap(pos)
                if(self.chestClicked != None):
                    # create slots from the inventory
                    # check if position is in one of the inventory slots
                    # if it is, subtract one from the item in the block
                    # add one into the item in the terrain
                    i = 0
                    chestRow = self.chestClicked[0]
                    chestCol = self.chestClicked[1]
                    for block in self.terrainMap[chestRow][chestCol]:
                        i += 1
                        chestItem = pygame.Rect(
                            60 + 20 * (((i - 1) % 8) + 1) + (((i - 1) % 8)) * 60, 270 + 70 * ((i - 1) // 8), 50, 50)
                        if(chestItem.collidepoint(pos)):
                            if(self.terrainMap[chestRow][chestCol][block] > 0):
                                self.terrainMap[chestRow][chestCol][block] -= 1
                                self.inventory[block] = self.inventory.get(
                                    block, 0) + 1

                    count = 0
                    for block in self.inventory:
                        count += 1
                        rect = pygame.Rect(
                            60 + 20 * (count) + (count - 1) * 50, 20, 50, 50)
                        chestScreen = pygame.Rect(60, 150, 640, 400)
                        if(rect.collidepoint(pos)):
                            chestRow = self.chestClicked[0]
                            chestCol = self.chestClicked[1]
                            if(self.inventory[block] > 0):
                                self.terrainMap[chestRow][chestCol][block] = self.terrainMap[chestRow][chestCol].get(
                                    block, 0) + 1
                                self.inventory[block] -= 1
                        elif(not chestScreen.collidepoint(pos)):
                            self.chestClicked = None

                elif(isinstance(self.terrainMap[row][col], dict)):
                    self.chestClicked = (row, col)

                elif(self.terrainMap[row][col] == 0 and self.inventoryBlockSelected != 0 and self.inventory[self.inventoryBlockSelected] > 0):
                    self.terrainMap[row][col] = self.inventoryBlockSelected
                    self.terrainChanged = [
                        row, col, self.inventoryBlockSelected]
                    self.inventory[self.inventoryBlockSelected] -= 1

        if(self.mouseClicked):
            pos = pygame.mouse.get_pos()
            (row, col) = self.convertClickMap(pos)
            self.clickMap[row][col] += 1
            if(self.clickMap[row][col] % 10 == 0):
                if(self.terrainMap[row][col] != 0):
                    self.inventory[self.terrainMap[row][col]] = \
                        self.inventory.get(self.terrainMap[row][col], 0) + 1
                self.terrainMap[row][col] = 0
                self.terrainChanged = [row, col, 0]

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if(self.jumping):
                self.move((-1) * self.xvel, 0, blocks)
            else:
                self.move((-1) * self.xvel, 1, blocks)

        if keys[pygame.K_d]:
            if(self.jumping):
                self.move((1) * self.xvel, 0, blocks)
            else:
                self.move((1) * self.xvel, 1, blocks)

        if(not self.jumping and not self.falling):
            if keys[pygame.K_SPACE]:
                self.jumping = True
                self.jumpCount = 5.272

        elif(self.jumping and not self.falling):
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
            self.move(0, yval, blocks)
            self.jumpCount -= 2
        elif(not self.falling and not self.jumping):
            self.jumpCount = 0
            self.jumping = False
            self.falling = False

        if keys[pygame.K_1]:
            self.inventoryPicked = 1
        if keys[pygame.K_2]:
            self.inventoryPicked = 2
        if keys[pygame.K_3]:
            self.inventoryPicked = 3
        if keys[pygame.K_4]:
            self.inventoryPicked = 4
        if keys[pygame.K_5]:
            self.inventoryPicked = 5
        if keys[pygame.K_6]:
            self.inventoryPicked = 6
        if keys[pygame.K_7]:
            self.inventoryPicked = 7
        if keys[pygame.K_8]:
            self.inventoryPicked = 8
        if keys[pygame.K_9]:
            self.inventoryPicked = 9

    def convertClickMap(self, pos):
        (x, y) = pos
        col = (x + self.scrollX) // 20
        row = (y + self.scrollY) // 20
        return (int(row), int(col))

# move function modified from https://stackoverflow.com/questions/44721130/pygame-collision-detection-with-walls
    def move(self, xvel, yvel, blocks):
        blocks.update(0, self.scrollX, self.scrollY)
        if(xvel != 0):
            self.x += xvel
            self.makePlayerVisible()
            self.rect = pygame.Rect(
                self.x - self.scrollX, self.y - self.scrollY, self.width, self.height)
            blockList = pygame.sprite.spritecollide(self, blocks, 0)
            for block in blockList:
                if(xvel < 0):
                    self.x = block.x + block.cellSize
                elif(xvel > 0):
                    self.x = block.x - self.width
                break

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

            self.makePlayerVisible()
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

            self.makePlayerVisible()
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

        self.makePlayerVisible()
        self.rect = pygame.Rect(self.x - self.scrollX,
                                self.y - self.scrollY, self.width, self.height)

# fix this for scrollX and Y
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
        self.rect = pygame.Rect(self.x - self.scrollX,
                                self.y - self.scrollY, self.width, self.height)
        self.dirty = 1

    def draw(self, win):
        self.rect = pygame.Rect(self.x - self.scrollX,
                                self.y - self.scrollY, self.width, self.height)
        pygame.draw.rect(win, (0, 0, 255), (self.rect))
