import pygame

#all same references from Player class but just for faster and more effecient drawing
#only has the necessary code

class Player2(pygame.sprite.DirtySprite):
    def __init__(self, x, y, width, height):
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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.image = pygame.image.load("emoji_face.png")
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.scrollX = 20000
        self.scrollY = 0
        self.blockBelow = None
        self.inventory = dict()
        self.lives = 5
        self.homeScreen = True
        self.movingDir = 0
        self.sprites = []
        #images retrieved from https://www.spriters-resource.com/download/77319/
        self.standingsprite = pygame.image.load("oppstanding.png")
        self.spritenum = 0
        self.makeSprites()

    def makeSprites(self):
        #images retreived from https://www.spriters-resource.com/download/77319/
        self.sprites = [pygame.image.load(f"oppwalking{n}.png") for n in range(1,5)]

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dirty = 1

    def draw(self, win):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if(self.movingDir == -1):
            self.image = pygame.transform.flip(self.sprites[self.spritenum % 4], True, False)
        elif(self.movingDir == 1):
            self.image = self.sprites[self.spritenum % 4]
        else:
            self.image = self.standingsprite
        win.blit(self.image, self.rect)
        healthleft = pygame.Rect(self.x - 5, self.y - 5, 6*self.lives, 3)
        pygame.draw.rect(win, (255, 0, 0), healthleft)

    def __repr__(self):
        return f"{self.x}, {self.y}"
