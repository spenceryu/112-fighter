import pygame, os
from GameObject import GameObject
from Attack import Attack
import AI
import random

class Fighter(GameObject):
    def __init__(self, x, y, player, direction):
        #Initalize variables
        self.direction = direction
        self.xSpeed = 5
        self.ySpeed = 10
        self.canJump = True
        self.player = player
        self.attackDelay = random.randint(1, 1000)
        #Load and Scale Image
        bigSprites = ['kosbie.png', 'rohan.png', 'andersen.png', 'rohan2.png']*100
        otherSprites = os.listdir('Images/TAs_Teachers')[1:]
        playerSprites = bigSprites + otherSprites
        playerID = random.choice(playerSprites)
        fileSprite = 'Images/TAs_Teachers/%s' % (playerID)

        self.imageRight = pygame.transform.scale(pygame.image.load(fileSprite).convert_alpha(), (50,50))
        self.imageLeft = pygame.transform.flip(pygame.transform.scale(pygame.image.load(fileSprite).convert_alpha(), (50,50)), True, False)
        self.image = self.imageRight
        self.faceInDir()
        #Call GameObject Init
        super(Fighter, self).__init__(x,y,self.image)

    #Update Object, should be called each frame
    def update(self, keysDown, screenWidth, screenHeight, attacks, other, dt):
        if(self.player == 0):
            self.movePlayerFighter(keysDown, dt, attacks)
        else:
            self.moveAIFighter(other, dt, attacks)
        #Gravity
        if(self.ySpeed < 10):
            self.ySpeed += 1
        self.y += self.ySpeed
        #Update Box
        self.updateRect()

        self.faceInDir()

        #Check for collitions
        if(self.rect.left < 0):
            self.x = self.width//2
        if(self.rect.right > screenWidth):
            self.x = screenWidth-self.width//2
        if(self.rect.top < 0):
            self.y = self.height//2
        if(self.rect.bottom > screenHeight):
            self.y = screenHeight-self.height//2
            self.canJump = True
        #Update Box
        self.updateRect()

    def movePlayerFighter(self, keysDown, dt, attacks):
        #Move The Charecter
        if keysDown(pygame.K_LEFT):
            self.moveLeft()
        if keysDown(pygame.K_RIGHT):
            self.moveRight()
        if keysDown(pygame.K_UP):
            if(self.canJump):
                self.jump()

        self.attackDelay -= dt

        if keysDown(pygame.K_DOWN) and self.attackDelay <= 0:
            self.attack(attacks)

    def moveAIFighter(self, other, dt, attacks):
        self.attackDelay -= dt
        move = AI.moveAIFighter(self, other)
        if(move == "moveLeft"):
            self.moveLeft()
        if(move == "moveRight"):
            self.moveRight()
        if(move == "jump"):
            self.jump()
        if(move == "attack"):
            self.attack(attacks)

    def faceInDir(self):
        if(self.direction == 1):
            self.image = self.imageRight
        else:
            self.image = self.imageLeft

    def jump(self):
        self.ySpeed = -15
        self.canJump = False
    
    def moveLeft(self):
        self.x -= self.xSpeed
        self.direction = -1

    def moveRight(self):
        self.x += self.xSpeed
        self.direction = 1

    def attack(self, attacks):
        attacks[self.player].add(Attack(self.x+self.width//2*self.direction,self.y,self.direction))
        self.attackDelay = 500 + random.randint(1, 1000)
