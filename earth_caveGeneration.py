import random

#creates the map for the game

#This algorithm was retrieved from https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664
#but modified from Java and the the specifications of what I need

oreCombintations = [[[0,1,0,0],[0,1,1,1],[1,1,1,0]],[[1,1],[0,1]], [[1,0],[1,1]],
                    [[1,1],[1,0]], [[1,0],[1,0]], [[0,1],[1,0]], [[1,0],[0,1]],
                    [[1,1],[0,0]], [[1,1],[1,1]], [[0,1,0],[1,1,1],[0,1,0]],
                    [[1,1],[1,1],[1,0]], [[1,0],[0,0]]]

oreTypes = [16,12,13]

def constructCave(rows, cols, birthLimit, deathLimit, numberOfSteps,
                  chanceToStartAlive):
    terrainMap = initialiseMap(makeMap(rows, cols), chanceToStartAlive)
    for i in range(numberOfSteps):
        terrainMap = doSimulationStep(terrainMap, birthLimit, deathLimit)
    top = [([0] * 2000) for i in range(18)]
    terrainMap = top + terrainMap
    # for row in range(18, len(terrainMap)):
    #     for col in range(len(terrainMap[0])):
    #         if(terrainMap[row][col] == 1):
    #             r = random.random()
    #             if(r <= .5):
    #                 terrainMap[row][col] = 2
    #sets trees
    chanceForTree = .1
    chanceForFlower = .2
    for col in range(len(terrainMap[17])-10):
        rTree = random.random()
        if(rTree < chanceForTree and terrainMap[17][col-5] != 4 and terrainMap[17][col-4] != 4 and
            terrainMap[17][col-3] != 4 and terrainMap[17][col-2] != 4 and terrainMap[17][col-1] != 4
            and terrainMap[18][col] != 0):
            terrainMap[17][col] = 4
            terrainMap[16][col] = 4
            terrainMap[15][col] = 5
            terrainMap[14][col] = 5
            terrainMap[13][col] = 5
            terrainMap[14][col+1] = 5
            terrainMap[14][col-1] = 5
            terrainMap[15][col+1] = 5
            terrainMap[15][col-1] = 5
        rFlower = random.random()
        if(rFlower < chanceForFlower and terrainMap[17][col] == 0 and terrainMap[18][col] != 0):
            terrainMap[17][col] = 17
    #sets dirt and grass
    for col in range(len(terrainMap[0])):
        if(terrainMap[18][col] != 0):
            terrainMap[18][col] = 6
        if(terrainMap[19][col] != 0):
            terrainMap[19][col] = 7
    #algorithm for dirt
    chanceForDirt = .6
    for row in range(20, len(terrainMap) - 1):
        for col in range(len(terrainMap[0])):
            r = random.random()
            if(row <= 23):
                if(r < chanceForDirt**(row-19) and terrainMap[row][col] != 0):
                    terrainMap[row][col] = 7
            else:
                if(r < .05 and terrainMap[row][col] != 0):
                    terrainMap[row][col] = 7

    chanceForCoal = .1
    for row in range(24, len(terrainMap) - 10):
        for col in range(10, len(terrainMap[0]) - 10):
            r = random.random()
            rIndex = random.randint(0,len(oreCombintations)-1)
            if(r < chanceForCoal and checkOre(row,col,rIndex, terrainMap)):
                for r in range(len(oreCombintations[rIndex])):
                    for c in range(len(oreCombintations[rIndex][0])):
                        if(oreCombintations[rIndex][r][c] == 1):
                            terrainMap[row + r][col + c] = 16

    chanceForIron = .08
    for row in range(30, len(terrainMap) - 10):
        for col in range(10, len(terrainMap[0]) - 10):
            r = random.random()
            rIndex = random.randint(0,len(oreCombintations)-1)
            if(r < chanceForIron and checkOre(row,col,rIndex,terrainMap)):
                for r in range(len(oreCombintations[rIndex])):
                    for c in range(len(oreCombintations[rIndex][0])):
                        if(oreCombintations[rIndex][r][c] == 1):
                            terrainMap[row + r][col + c] = 13

    chanceForDiamond = .06
    for row in range(35, len(terrainMap) - 10):
        for col in range(10, len(terrainMap[0]) - 10):
            r = random.random()
            rIndex = random.randint(0,len(oreCombintations)-1)
            if(r < chanceForDiamond and checkOre(row,col,rIndex, terrainMap)):
                for r in range(len(oreCombintations[rIndex])):
                    for c in range(len(oreCombintations[rIndex][0])):
                        if(oreCombintations[rIndex][r][c] == 1):
                            terrainMap[row + r][col + c] = 12

def checkOre(row, col, rIndex, terrainMap):
    for r in range(len(oreCombintations[rIndex])):
        for c in range(len(oreCombintations[rIndex][0])):
            if(oreCombintations[rIndex][r][c] == 1):
                if(terrainMap[row + r][col + c] == 0 or terrainMap[row + r][col + c] in oreTypes):
                    return False
    return True

def makeMap(rows, cols):
    caveMap = [([0] * cols) for row in range(rows)]
    return caveMap


def initialiseMap(lmap, chanceToStartAlive):
    for i in range(len(lmap)):
        for j in range(len(lmap[0])):
            r = random.random()
            if(r <= chanceToStartAlive):
                lmap[i][j] = 1
    return lmap


def doSimulationStep(oldMap, birthLimit, deathLimit):
    newMap = makeMap(len(oldMap), len(oldMap[0]))
    for row in range(len(oldMap)):
        for col in range(len(oldMap[0])):
            result = countAliveNeighbors(oldMap, row, col)
            if(oldMap[row][col] == 1):
                if(result < deathLimit):
                    newMap[row][col] = 0
                else:
                    newMap[row][col] = 1
            else:
                if(result > birthLimit):
                    newMap[row][col] = 1
                else:
                    newMap[row][col] = 0
    return newMap


def countAliveNeighbors(map, row, col):
    count = 0
    for drow in [-1, 0, +1]:
        for dcol in [-1, 0, +1]:
            neighborRow = row + drow
            neighborCol = col + dcol
            if(drow == 0 and dcol == 0):
                pass
            elif(neighborRow < 0 or neighborCol < 0 or neighborRow >= len(map)
                 or neighborCol >= len(map[0])):
                count += 1
            elif(map[neighborRow][neighborCol] == 1):
                count += 1
    return count