import pygame

class InventoryBlock(pygame.sprite.Sprite):
    textures = ["graveltexture.png", "graveltexture.png", "emoji_face.png"]
    def __init__(self, row, col, cellSize, blockType, number):
        pygame.sprite.Sprite.__init__(self)
        #self.winHeight = height
        #self.winWidth = width
        self.row = row
        self.col = col
        self.cellSize = cellSize
        self.x = col * cellSize
        self.y = row * cellSize + 350  # need to change this at some point
        self.blockType = 0
        self.image = pygame.image.load(
            InventoryBlock.textures[self.blockType]).convert()
        self.rect = pygame.Rect(self.x, self.y, self.cellSize, self.cellSize)
        self.scrollX = 2000
        self.scrollY = 0


    def draw(self, win):
            pygame.draw.rect(win, (0, 255, 0), (self.rect))
