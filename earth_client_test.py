import pygame
import math
from earth_network_test import Network
from earth_player_test import *
from earth_player2 import *
from earth_caveGeneration import *
from earth_terrainBlock import *
from earth_mob import *
from UITest import UIElement


#code for dirty sprites was referenced but not copied from https://www.youtube.com/watch?v=Pu5_8F_KaHI
#code for dirty spriteswas referenced but not copied from http://n0nick.github.io/blog/2012/06/03/quick-dirty-using-pygames-dirtysprite-layered/

#gets blocks inside the window for better speed
def getMapInsideBounds(terrainMap, scrollX, scrollY, transparent = False):
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

#initializes map
def getMap():
    terrainMap = constructCave(150, 2000, 4, 4, 4, .5)
    #terrainMap = [([1] * 2000) for i in range(150)]
    return terrainMap


pygame.init()
terrainMap = getMap()

# clickMap from http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
clickMap = [([0] * 2000) for i in range(168)]
terrainMap[17][1022] = dict()
mainClock = pygame.time.Clock()
win = pygame.display.set_mode((760, 650))
background = pygame.Surface(win.get_size())
scrollBackground = 0
background.blit(pygame.image.load("backgrounddirt.png"), (0, 0))
#fullbackground image modified from https://i.pinimg.com/originals/f3/64/b7/f364b7d0a49566891789d291b8b2e53f.png
background.blit(pygame.image.load("fullbackground.png"), (0, 0))

#images retrieved from https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwj81YvUpvnlAhVPmlkKHeghBsQQjhx6BAgBEAI&url=https%3A%2F%2Fwww.scirra.com%2Fstore%2Fbackgrounds-for-games%2Fpixel-cave-parallax-bg-3048&psig=AOvVaw2N7auZsunNJBdKhYpoU6gT&ust=1574356909149299
#and https://img.itch.io/aW1hZ2UvMTMwMDQ5LzU5OTgzMi5wbmc=/original/c0%2Fhep.png
pygame.display.set_caption("First Game")
terrainSprites = getMapInsideBounds(terrainMap,
                                    20000, 0)
terrainSprites.clear(win, background)
clientNumber = 0
startMouseOver = 1
helpMouseOver = 1

#from https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
startBtn = UIElement(
        center_position=(380, 580),
        font_size=35,
        bg_rgb=(255,255,255),
        text_rgb=(46,128,69),
        text="Start",
    )

#redraws the whole window acording to the player
def redrawWindow(player, player2, zombie):
    #draws the homescreen
    if(player.homeScreen):
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

        win.fill((255,255,255))

        player.homeScreen = startBtn.update(pygame.mouse.get_pos(), mouse_up)
        startBtn.draw(win)
        #earthfont in picture obtained from: https://www.fontspace.com/category/earth
        earthlogo = pygame.image.load("earthitlogo.png")
        earthlogorect = earthlogo.get_rect()
        earthlogorect.center = (380, 70)
        win.blit(earthlogo, earthlogorect)
        earth = pygame.image.load("earthpixelart.png")
        earthrect = earth.get_rect()
        earthrect.center = (380, 330)
        win.blit(earth, earthrect)
        pygame.display.update()

        #draws the wait screen
    elif(player2.homeScreen):
        win.fill((255,255,255))
        earth = pygame.image.load("earthpixelart.png")
        earthrect = earth.get_rect()
        earthrect.center = (380, 330)
        win.blit(earth, earthrect)
        font = pygame.font.Font('TheWorldIsYoursBold-rDg9.ttf', 35)
        text = font.render("Waiting for other player to join...", True, (46,128,69))
        textRect = text.get_rect()
        textRect.center = (380,580)
        win.blit(text, textRect)
        pygame.display.update()
    #draws the game
    else:
        background.blit(pygame.image.load("backgrounddirt.png"), (0, 0))
        background.blit(pygame.image.load("fullbackground.png"), (((-1)*(player.scrollBackgroundX + 5000)//5,
            (-1)*player.scrollBackgroundY)))
        terrainSprites = getMapInsideBounds(terrainMap,
                                        player.scrollX, player.scrollY)
        terrainSprites.clear(win, background)
        terrainSprites.update(player.scrollX, player.scrollY)
        spriteRects = terrainSprites.draw(win)
        pygame.display.update(spriteRects)
        player.draw(win)
        player2.draw(win)
        if(not zombie.died):
            zombie.draw(win, terrainMap, player.scrollX, player.scrollY)
        else:
            zombie.countSinceDied += 1
            if(zombie.countSinceDied > 40):
                zombie.countSinceDied = 0
                zombie.lives = 10
                x = random.randint(player.x - 700, player.x + 700)
                zombie.died = False
                # while(zombie.died):
                #     x = random.randint(player.x - 700, player.x + 700)
                #     col = (x + player.scrollX) // 20
                #     for y in range(player.y - 100, player.y + 100, 20):
                #         row = (y + player.scrollY) // 20
                #         if(terrainMap[row][col] == 0 and terrainMap[row - 1][col] == 0
                #             and terrainMap[row + 1][col] != 0):
                #             zombie.died = False
        if(pygame.sprite.collide_rect(player, zombie)):
            if(not player.inMoster):
                player.inMoster = True
                player.lives -= 1
        else:
            player.inMoster = False
        font = pygame.font.Font('freesansbold.ttf', 20)
        count = 0
        #draws inventory slots
        for block in player.inventory:
            count += 1
            if(count == player.inventoryPicked):
                selectsprite = pygame.image.load("selectsprite.png").convert_alpha()
                rect = pygame.Rect(55 + 20 * (count) +
                                   (count - 1) * 50, 15, 60, 60)
                win.blit(selectsprite, rect)
                player.inventoryBlockSelected = block
            if(player.inventory[block] == 0):
                rect = pygame.Rect(60 + 20 * (count) + (count - 1) * 50, 20, 50, 50)
                pygame.draw.rect(win, (88, 91, 92), rect)
            else:
                image = pygame.image.load(TerrainBlock.textures[block]).convert_alpha()
                image = pygame.transform.scale(image, (50, 50))
                win.blit(image, (60 + 20 * (count) + (count - 1) * 50, 20))
                # font display referenced/copied from: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
                text = font.render(
                    f'{player.inventory[block]}', True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (90 + 20 * (count) + (count - 1) * 50, 35)
                win.blit(text, textRect)

        for i in range(9, len(player.inventory), -1):
            if(i == player.inventoryPicked):
                selectsprite = pygame.image.load("selectsprite.png").convert_alpha()
                rect = pygame.Rect(55 + 20 * (i) + (i - 1) * 50, 15, 60, 60)
                win.blit(selectsprite, rect)
                player.inventoryBlockSelected = 0
            rect = pygame.Rect(60 + 20 * (i) + (i - 1) * 50, 20, 50, 50)
            pygame.draw.rect(win, (88, 91, 92), rect)

        #detects zombie player collision
        if(player.chestClicked == None and not player.craftingClicked
            and not zombie.rect.collidepoint(pygame.mouse.get_pos())):
            pos = pygame.mouse.get_pos()
            if(-160 < pos[0] - (player.x - player.scrollX) < 160
                and -160 < pos[1] - (player.y - player.scrollY) < 160):
                mouseHover = pygame.Rect((((pos[0] + player.scrollX) // 20)*20) - (player.scrollX),
                    (((pos[1] + player.scrollY) // 20)*20) - (player.scrollY), 20, 20)
                pygame.draw.rect(win, (255,0,0), mouseHover, 2)

        #draws chest screen
        if(player.chestClicked != None):
            rect = pygame.Rect(60, 150, 640, 400)
            pygame.draw.rect(win, (88, 91, 92), rect)
            chestRow = player.chestClicked[0]
            chestCol = player.chestClicked[1]
            i = 0
            for block in player.terrainMap[chestRow][chestCol]:
                i += 1
                if(player.terrainMap[chestRow][chestCol][block] == 0):
                    rect = pygame.Rect(60 + 20 * (((i - 1) % 8) + 1) +
                                       (((i - 1) % 8)) * 60, 270 + 70 * ((i - 1) // 8), 50, 50)
                    pygame.draw.rect(win, (73, 64, 36), rect)
                else:
                    image = pygame.image.load(
                        TerrainBlock.textures[block]).convert_alpha()
                    image = pygame.transform.scale(image, (50, 50))
                    win.blit(image, (60 + 20 * (((i - 1) % 8) + 1) +
                                     (((i - 1) % 8)) * 60, 270 + 70 * ((i - 1) // 8)))
                    # referenced/copied from: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
                    text = font.render(
                        f'{player.terrainMap[chestRow][chestCol][block]}', True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = (90 + 20 * (i) + (i - 1)
                                       * 60, 285 + 70 * ((i - 1) // 8))
                    win.blit(text, textRect)

            for i in range(32, len(player.terrainMap[chestRow][chestCol]), -1):
                rect = pygame.Rect(60 + 20 * (((i - 1) % 8) + 1) +
                                   (((i - 1) % 8)) * 60, 270 + 70 * ((i - 1) // 8), 50, 50)
                pygame.draw.rect(win, (73, 64, 36), rect)
        #draws crafting screen
        if(player.craftingClicked):
            rect = pygame.Rect(60, 150, 640, 400)
            pygame.draw.rect(win, (88, 91, 92), rect)
            selectsprite = pygame.image.load("selectsprite.png").convert_alpha()
            selectedRect = pygame.Rect(75 + 20 * (player.craftingBlockClicked[1] + 1) +
                                           (player.craftingBlockClicked[1] * 60), 265 + 70 *
                                           player.craftingBlockClicked[0], 60, 60)
            win.blit(selectsprite, selectedRect)
            for row in range(len(player.craftingBlock)):
                for col in range(len(player.craftingBlock[0])):
                    if(player.craftingBlock[row][col] == 0):
                        rect = pygame.Rect(80 + 20 * (col + 1) +
                                           (col * 60), 270 + 70 * row, 50, 50)
                        pygame.draw.rect(win, (124,109,60), rect)
                    else:
                        image = pygame.image.load(
                            TerrainBlock.textures[player.craftingBlock[row][col]]).convert_alpha()
                        image = pygame.transform.scale(image, (50, 50))
                        win.blit(image, (80 + 20 * (col + 1) +
                                           (col * 60), 270 + 70 * row))

            craftButton = pygame.Rect(360, 315, 285, 100)
            pygame.draw.rect(win, (124,109,60), craftButton)
            font = pygame.font.Font('TheWorldIsYoursBold-rDg9.ttf', 35)
            text = font.render("Craft", True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (503, 365)
            win.blit(text, textRect)


        craftingimg = pygame.image.load("craftingtable.png").convert_alpha()
        craftingimg = pygame.transform.scale(craftingimg, (50, 50))
        win.blit(craftingimg, (640, 90))
        pygame.display.update()


def main():
    run = True
    n = Network()
    pData = n.getP()
    p = Player(pData[0].x, pData[0].y, 20, 40, terrainMap, clickMap)
    p2 = Player2(20380, 320, 20, 40)
    z = Zombie(pData[1].x, pData[1].y, 20, 40, terrainMap)
    clock = pygame.time.Clock()


    while run:
        #run code referenced from https://techwithtim.net/tutorials/python-online-game-tutorial/sending-objects/
        if(not p.homeScreen):
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            #all sockets sending and recieving of data
            pData[0].x = p.x
            pData[0].y = p.y
            pData[0].lives = p.lives
            pData[0].homeScreen = p.homeScreen
            pData[0].movingDir = p.movingDir
            pData[0].spritenum = p.spritenum
            pData[0].terrainChanged = p.terrainChanged
            pData[0].collideWithEnemy = p.collideWithEnemy
            pData[0].inventoryBlockSelected = p.inventoryBlockSelected

            z.update()
            
            pData[1].x = z.x
            pData[1].y = z.y
            pData[1].lives = z.lives
            # pData[1].died = z.died
            p.terrainChanged = [0,0,0]
            p2Data = n.send(pData)

            p.collideWithEnemy = False

            p2.x = p2Data[0].x - p.scrollX
            p2.y = p2Data[0].y - p.scrollY
            p2.lives = p2Data[0].lives
            p2.homeScreen = p2Data[0].homeScreen
            p2.movingDir = p2Data[0].movingDir
            p2.spritenum = p2Data[0].spritenum
            p.terrainMap[p2Data[0].terrainChanged[0]][p2Data[0].terrainChanged[1]] = p2Data[0].terrainChanged[2]
            p2Data[0].terrainChanged = [0,0,0]
            p2.update()

            z.x = p2Data[1].x
            z.y = p2Data[1].y
            if(p2Data[1].xMove < 0):
                z.xMove = math.floor(p2Data[1].xMove)
            else:
                z.xMove = math.ceil(p2Data[1].xMove)
            if(p2Data[1].yMove < 0):
                z.yMove = math.floor(p2Data[1].yMove)
            else:
                z.yMove = math.ceil(p2Data[1].yMove)

            z.lives = p2Data[1].lives
            z.died = p2Data[1].died
            if(not p2.homeScreen):
                terrainSpritesWOFlowers = getMapInsideBounds(terrainMap,
                                        p.scrollX, p.scrollY, True)
                p.checkMove(terrainSpritesWOFlowers, z)

        redrawWindow(p, p2, z)

main()
