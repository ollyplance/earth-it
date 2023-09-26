import pygame

#code was referenced but not copied from https://www.youtube.com/watch?v=Pu5_8F_KaHI
#code was referenced but not copied from http://n0nick.github.io/blog/2012/06/03/quick-dirty-using-pygames-dirtysprite-layered/

#player class, has elements for keys clicked and mouse pressed for each player. Detects collisions

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
        self.scrollYMargin = 290
        self.blockBelow = None
        self.mouseClicked = False
        self.inventory = dict()
        self.clickMap = clickMap
        self.inventoryPicked = 1
        self.inventoryBlockSelected = None
        self.chestClicked = None
        self.terrainChanged = [0, 0, 0]
        self.lives = 5
        self.homeScreen = True
        self.movingDir = 0
        self.sprites = []
        #image retrieved from https://www.spriters-resource.com/download/77275/
        self.standingsprite = pygame.image.load("standingsprite.png")
        self.spritenum = 0
        self.craftingClicked = False
        self.craftingBlock = [[0,0,0],[0,0,0],[0,0,0]]
        self.craftingBlockClicked = (0,0)
        self.craftingRecepies = [[[1,1,1],[0,11,0],[0,11,0]], [[0,0,4],[0,0,0],[0,0,0]], [[0,1,0],[0,1,0],[0,11,0]],
                    [[0,0,8],[0,0,8],[0,0,0]], [[8,8,8],[8,0,8],[8,8,8]], [[0,0,16],[0,0,11],[0,0,0]], [[0,13,0],[0,13,0],[0,11,0]],
                    [[0,12,0],[0,12,0],[0,11,0]], [[13,13,13],[0,11,0],[0,11,0]]]
        self.craftingRecepiesKey = [(10, 1), (8, 4), (9,1), (11,4), (3, 1), (20,4), (23,1), (24,1), (21,1), (22,1)]
        self.inventoryKeys = []
        self.inMonster = False
        self.cantPlace = [9,10,11,21,22,23,24]
        self.scrollBackgroundX = self.scrollX - 20000
        self.scrollBackgroundY = self.scrollY
        self.makeSprites()
        self.collideWithEnemy = False

    def makeSprites(self):
        #images retrieved from https://www.spriters-resource.com/download/77275/
        self.sprites = [pygame.image.load(f"walkingsprite{n}.png") for n in range(1,5)]

    #deletes item from dictionary if it is empty
    def checkInventory(self):
        #referenced from https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
        self.inventoryKeys = []
        for i in self.inventory.keys():
            self.inventoryKeys.append(i)

        for elem in self.inventoryKeys:
            if(self.inventory[elem] <= 0):
                if(len(self.inventory) > 1):
                    self.inventory.pop(elem)
                    count = 0
                    for block in self.inventory:
                        count += 1
                        if(count == self.inventoryPicked):
                            self.inventoryBlockSelected = block
                        else:
                            self.inventoryBlockSelected = 0

    #checks to see if the user wants to move the player, or has clicked or jumped,
    #handles crafting and chest clicking
    def checkMove(self, blocks, enemy):
        #Move check functions referenced/modiefied from https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement/
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
                if(pygame.Rect(enemy.x - self.scrollX, enemy.y, 20, 40).collidepoint(pos)
                        and -160 < pos[0] - (self.x - self.scrollX) < 160
                        and -160 < pos[1] - (self.y - self.scrollY) < 160):
                    self.collideWithEnemy = True
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
                                self.terrainChanged = [chestRow, chestCol, self.terrainMap[chestRow][chestCol]]

                    count = 0
                    for block in self.inventory:
                        count += 1
                        rect = pygame.Rect(
                            60 + 20 * (count) + (count - 1) * 50, 20, 50, 50)
                        if(rect.collidepoint(pos)):
                            chestRow = self.chestClicked[0]
                            chestCol = self.chestClicked[1]
                            if(self.inventory[block] > 0):
                                self.terrainMap[chestRow][chestCol][block] = self.terrainMap[chestRow][chestCol].get(
                                    block, 0) + 1
                                self.inventory[block] -= 1
                                self.terrainChanged = [chestRow, chestCol, self.terrainMap[chestRow][chestCol]]
                    self.checkInventory()

                #works with the chest system
                if(self.craftingClicked):
                    for row in range(len(self.craftingBlock)):
                        for col in range(len(self.craftingBlock[0])):
                            craftingItem = pygame.Rect(80 + 20 * (row + 1) +
                                               (row * 60), 270 + 70 * col, 50, 50)
                            if(craftingItem.collidepoint(pos)):
                                self.craftingBlockClicked = (col, row)
                                if(self.craftingBlock[col][row] != 0):
                                    self.inventory[self.craftingBlock[col][row]] = \
                                        self.inventory.get(self.craftingBlock[col][row], 0) + 1
                                    self.craftingBlock[col][row] = 0

                    count = 0
                    for block in self.inventory:
                        count += 1
                        rect = pygame.Rect(
                            60 + 20 * (count) + (count - 1) * 50, 20, 50, 50)
                        if(rect.collidepoint(pos)):
                            row = self.craftingBlockClicked[1]
                            col = self.craftingBlockClicked[0]
                            if(self.craftingBlock[col][row] == 0):
                                self.craftingBlock[col][row] = block
                                self.inventory[block] -= 1
                    self.checkInventory()

                    craftButton = pygame.Rect(360, 315, 285, 100)
                    if(craftButton.collidepoint(pos)):
                        if(self.craftingBlock in self.craftingRecepies):
                            i = self.craftingRecepies.index(self.craftingBlock)
                            block = self.craftingRecepiesKey[i][0]
                            self.inventory[block] = self.inventory.get(block, 0) + self.craftingRecepiesKey[i][1]
                            self.craftingBlock = [[0,0,0],[0,0,0],[0,0,0]]

                #determines if a chest is clicked
                elif(isinstance(self.terrainMap[row][col], dict) and
                        -160 < pos[0] - (self.x - self.scrollX) < 160
                        and -160 < pos[1] - (self.y - self.scrollY) < 160):
                    self.chestClicked = (row, col)

                #determines if crafting block was clicked
                elif(pygame.Rect(640, 90, 50, 50).collidepoint(pos)):
                    self.craftingClicked = True

                #deals with placing block on screen
                self.checkInventory()
                if(self.terrainMap[row][col] == 0 and self.inventoryBlockSelected != 0
                        and self.inventory[self.inventoryBlockSelected] > 0
                        and self.chestClicked == None and not self.craftingClicked and
                         -160 < pos[0] - (self.x - self.scrollX) < 160
                        and -160 < pos[1] - (self.y - self.scrollY) < 160):
                    if(self.inventoryBlockSelected == 3):
                        self.terrainMap[row][col] = dict()
                        self.terrainChanged = [row, col, dict()]
                        self.inventory[self.inventoryBlockSelected] -= 1
                        self.checkInventory()
                    elif(not self.inventoryBlockSelected in self.cantPlace):
                        self.terrainMap[row][col] = self.inventoryBlockSelected
                        self.terrainChanged = [row, col, self.inventoryBlockSelected]
                        self.inventory[self.inventoryBlockSelected] -= 1
                        self.checkInventory()

        #breaking of blocks on screen
        if(self.mouseClicked):
            pos = pygame.mouse.get_pos()
            if(-160 < pos[0] - (self.x - self.scrollX) < 160
                and -160 < pos[1] - (self.y - self.scrollY) < 160):
                (row, col) = self.convertClickMap(pos)
                if(self.inventoryBlockSelected == 22):
                    self.clickMap[row][col] += 5
                elif(self.inventoryBlockSelected == 21):
                    self.clickMap[row][col] += 4
                elif(self.inventoryBlockSelected == 10):
                    self.clickMap[row][col] += 2
                else:
                    self.clickMap[row][col] += 1
                if(self.clickMap[row][col] > 10):
                    if(self.terrainMap[row][col] != 0):
                        self.inventory[self.terrainMap[row][col]] = \
                            self.inventory.get(self.terrainMap[row][col], 0) + 1
                    self.terrainMap[row][col] = 0
                    self.clickMap[row][col] = 0
                    self.terrainChanged = [row, col, 0]

        keys = pygame.key.get_pressed()
        #checks moving keys
        if(not self.jumping and not self.falling):
            self.move(0, 1, blocks)

        if keys[pygame.K_a]:
            self.spritenum += 1
            self.movingDir = -1
            if(self.jumping):
                self.move((-1) * self.xvel, 0, blocks)
            else:
                self.move((-1) * self.xvel, 1, blocks)
        elif(not keys[pygame.K_d]):
            self.movingDir = 0

        if keys[pygame.K_d]:
            self.spritenum += 1
            self.movingDir = 1
            if(self.jumping):
                self.move((1) * self.xvel, 0, blocks)
            else:
                self.move((1) * self.xvel, 1, blocks)
        elif(not keys[pygame.K_a]):
            self.movingDir = 0

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
        if keys[pygame.K_t]:
            self.inventory = {9:1, 23:1, 24:1, 10:1, 21:1, 22:1}
        if keys[pygame.K_l]:
            self.inventory = {16:1, 11:4}
        if keys[pygame.K_c]:
            self.inventory = {2:16, 4:16, 6:16, 7:16, 12:16}
        if keys[pygame.K_e]:
            self.chestClicked = None
            if(self.craftingClicked):
                self.craftingClicked = False
                for row in range(len(self.craftingBlock)):
                    for col in range(len(self.craftingBlock[0])):
                        if(self.craftingBlock[row][col] != 0):
                            self.inventory[self.craftingBlock[row][col]] = \
                                self.inventory.get(self.craftingBlock[row][col], 0) + 1
                self.craftingBlock = [[0,0,0],[0,0,0],[0,0,0]]

    def convertClickMap(self, pos):
        (x, y) = pos
        col = (x + self.scrollX) // 20
        row = (y + self.scrollY) // 20
        return (int(row), int(col))

# move function greatly modified from https://stackoverflow.com/questions/44721130/pygame-collision-detection-with-walls
# move function that moves the player and detects the blocks
    def move(self, xvel, yvel, blocks):
        blocks.update(self.scrollX, self.scrollY)
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
                print(yvel)
                if(yvel > 100):
                    self.lives = 0
                elif(yvel > 97):
                    self.lives -= 3
                elif(yvel > 71):
                    self.lives -= 1
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
        self.scrollBackgroundX = self.scrollX - 20000
        self.scrollBackgroundY = self.scrollY

    def update(self):
        self.makePlayerVisible()
        self.rect = pygame.Rect(self.x - self.scrollX,
                                self.y - self.scrollY, self.width, self.height)
        self.dirty = 1

    #draws the player with their health bar and with their sprite in the correct direction
    def draw(self, win):
        if(self.lives <= 0):
            self.x = 20350
            self.y = 320
            self.inventory = dict()
            self.scrollX = 20000
            self.scrollY = 0
            self.lives = 5

        self.rect = pygame.Rect(self.x - self.scrollX,
                                self.y - self.scrollY, self.width, self.height)

        if(self.movingDir == -1):
            self.image = pygame.transform.flip(self.sprites[self.spritenum % 4], True, False)
        elif(self.movingDir == 1):
            self.image = self.sprites[self.spritenum % 4]
        else:
            self.image = self.standingsprite

        win.blit(self.image, self.rect)
        healthleft = pygame.Rect(self.x - self.scrollX - 5, self.y - self.scrollY - 5, 6*self.lives, 3)
        pygame.draw.rect(win, (255, 0, 0), healthleft)

        font = pygame.font.Font('freesansbold.ttf', 20)
