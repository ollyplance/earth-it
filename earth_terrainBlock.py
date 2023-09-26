import pygame

#terrain block class, deals with drawing of the blocks and

#code for dirty sprites was referenced but not copied from https://www.youtube.com/watch?v=Pu5_8F_KaHI
#code for dirty sprites was referenced but not copied from http://n0nick.github.io/blog/2012/06/03/quick-dirty-using-pygames-dirtysprite-layered/

class TerrainBlock(pygame.sprite.DirtySprite):
    textures = ["graveltexture.png", "stonetexture.png", "graveltexture.png",
    "chest.png", "wood.png", "leaves.png",
    "grass.png", "dirt.png", "woodplank.png", "stonesword.png",
    "stonepickaxe.png", "stick.png", "diamonds.png", "iron.png", "sand.png",
    "glass.png", "coal.png", "flower1.png", "flower2.png", "flower3.png",
    "torch.png", "ironpickaxe.png", "diamondpickaxe.png", "ironsword.png",
    "diamondsword.png"]
    #I made images
    def __init__(self, row, col, cellSize, blockType):
        pygame.sprite.DirtySprite.__init__(self)
        #self.winHeight = height
        #self.winWidth = width
        self.row = row
        self.col = col
        self.cellSize = cellSize
        self.x = col * cellSize
        self.y = row * cellSize
        self.blockType = blockType
        if(isinstance(self.blockType, dict)):
            self.blockType = 3
        self.image = pygame.image.load(
            TerrainBlock.textures[self.blockType]).convert_alpha()
        self.rect = pygame.Rect(self.x, self.y, self.cellSize, self.cellSize)
        self.scrollX = 2000
        self.scrollY = 0

    def update(self, scrollX, scrollY):
        self.scrollX = scrollX
        self.scrollY = scrollY
        self.rect = pygame.Rect(
            self.x - self.scrollX, self.y - self.scrollY, self.cellSize, self.cellSize)
        self.image = pygame.image.load(
            TerrainBlock.textures[self.blockType]).convert_alpha()
        self.dirty = 1

    def draw(self, win):
        pygame.draw.rect(win, (self.rect))

    def __repr__(self):
        return f"{self.x}, {self.y}"
