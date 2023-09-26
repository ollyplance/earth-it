import pygame
from earth_network import Network
from earth_player import *
from earth_player2 import *
from earth_caveGeneration import *
from earth_terrainBlock import *
from earth_inventory import *
from earth_mob import *


# def getMap():
#     terrainMap = constructCave(150, 2000, 4, 4, 3, .5)
#     #terrainMap = [([1] * 2000) for i in range(150)]
#     top = [([0] * 2000) for i in range(18)]
#     terrainMap = top + terrainMap
#     terrainMap[18][1021] = dict()
#     terrainMap[18][1023] = dict()
#     return terrainMap


def getMapInsideBounds(terrainMap, scrollX, scrollY):
    blocklist = []
    colStart = (scrollX // 20)
    rowStart = int(scrollY // 20)
    for row in range(rowStart, rowStart + 33):
        for col in range(colStart - 1, colStart + 39):
            if(terrainMap[row][col] != 0):
                blocklist.append(TerrainBlock(
                    row, col, 20, terrainMap[row][col]))
    blocks = pygame.sprite.LayeredDirty(blocklist)
    return blocks


pygame.init()
terrainMap = []

# clickMap from http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
clickMap = [([0] * 2000) for i in range(168)]
mainClock = pygame.time.Clock()
win = pygame.display.set_mode((760, 650))
background = pygame.Surface(win.get_size())
background.blit(pygame.image.load("background.png"), (0, 0))
pygame.display.set_caption("First Game")
# terrainSprites = getMapInsideBounds(terrainMap,
#                                     20000, 0)
# terrainSprites.clear(win, background)
clientNumber = 0
# zombie1 = Zombie(20100, 320, 20, 40, terrainMap)


def read_msg(str):
    if(str is not None):
        str = str.split(",")
        return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])
    return None
    


def make_msg(tup, terrainChanged):
    return str(int(tup[0])) + "," + str(int(tup[1])) + ',' + str(terrainChanged[0]) + ',' + \
        str(terrainChanged[1]) + ',' + str(terrainChanged[2])


def redrawWindow(player, player2):
    terrainSprites = getMapInsideBounds(terrainMap,
                                        player.scrollX, player.scrollY)
    terrainSprites.clear(win, background)
    terrainSprites.update(0, player.scrollX, player.scrollY)
    spriteRects = terrainSprites.draw(win)
    pygame.display.update(spriteRects)
    player.draw(win)
    player2.draw(win)
    zombie1.draw(win, terrainMap)

    font = pygame.font.Font('freesansbold.ttf', 20)
    count = 0
    for block in player.inventory:
        count += 1
        if(count == player.inventoryPicked):
            rect = pygame.Rect(55 + 20 * (count) +
                               (count - 1) * 50, 15, 60, 60)
            pygame.draw.rect(win, (0, 0, 255), rect)
            player.inventoryBlockSelected = block
        if(player.inventory[block] == 0):
            rect = pygame.Rect(60 + 20 * (count) +
                               (count - 1) * 50, 20, 50, 50)
            pygame.draw.rect(win, (255, 0, 0), rect)
        else:
            image = pygame.image.load(TerrainBlock.textures[block]).convert()
            image = pygame.transform.scale(image, (50, 50))
            win.blit(image, (60 + 20 * (count) + (count - 1) * 50, 20))
            # referenced/copied from: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
            text = font.render(
                f'{player.inventory[block]}', True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (90 + 20 * (count) + (count - 1) * 50, 35)
            win.blit(text, textRect)

    for i in range(9, len(player.inventory), -1):
        if(i == player.inventoryPicked):
            rect = pygame.Rect(55 + 20 * (i) + (i - 1) * 50, 15, 60, 60)
            pygame.draw.rect(win, (0, 0, 255), rect)
            player.inventoryBlockSelected = 0
        rect = pygame.Rect(60 + 20 * (i) + (i - 1) * 50, 20, 50, 50)
        pygame.draw.rect(win, (255, 0, 0), rect)

    if(player.chestClicked != None):
        rect = pygame.Rect(60, 150, 640, 400)
        pygame.draw.rect(win, (255, 225, 143), rect)
        chestRow = player.chestClicked[0]
        chestCol = player.chestClicked[1]
        i = 0
        for block in player.terrainMap[chestRow][chestCol]:
            i += 1
            if(player.terrainMap[chestRow][chestCol][block] == 0):
                rect = pygame.Rect(60 + 20 * (((i - 1) % 8) + 1) +
                                   (((i - 1) % 8)) * 60, 270 + 70 * ((i - 1) // 8), 50, 50)
                pygame.draw.rect(win, (0, 0, 0), rect)
            else:
                image = pygame.image.load(
                    TerrainBlock.textures[block]).convert()
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
            pygame.draw.rect(win, (0, 0, 0), rect)

    # for i in range(9, len(player.inventory), -1):
    #     if(i == player.inventoryPicked):
    #         rect = pygame.Rect(55 + 20*(i) + (i-1)*50, 15, 60, 60)
    #         pygame.draw.rect(win, (0, 0, 255), rect)
    #         player.inventoryBlockSelected = 0
    #     rect = pygame.Rect(60 + 20*(i) + (i-1)*50, 20, 50, 50)
    #     pygame.draw.rect(win, (255, 0, 0), rect)

    pygame.display.update()


def main():
    run = True
    n = Network()

    while (n is None): 
        pass
    
    startPos = read_msg(n.getMsg())
    p = Player(startPos[0], startPos[1], 20, 40, terrainMap, clickMap)
    p2 = Player2(20350, 320, 20, 40, terrainMap, clickMap)
    clock = pygame.time.Clock()

    while run:
        p2Msg = read_msg(n.send(make_msg((p.x, p.y), [0, 0, 0])))
        p2.x = p2Msg[0] - p.scrollX
        p2.y = p2Msg[1] - p.scrollY
        p2.terrainMap[p.terrainChanged[0]
                      ][p.terrainChanged[1]] = p.terrainChanged[2]

        # listB = [([0] * len(p2Msg[2][0])) for i in range(len(p2Msg[2]))]
        # for row in range(len(p2Msg[2])):
        #     for col in range(len(p2Msg[2][0])):
        #         p2.terrainMap[row][col] = int(p2Msg[2][row][col])

        p2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        terrainSprites = getMapInsideBounds(terrainMap,
                                            p.scrollX, p.scrollY)
        p.checkMove(terrainSprites)
        redrawWindow(p, p2)


main()
