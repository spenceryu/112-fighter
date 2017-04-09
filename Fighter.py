import pygame
from GameObject import GameObject
from Attack import Attack
import random

class Fighter(GameObject):
    def __init__(self, x, y, player):
        #Initalize variables
        self.xSpeed = 5
        self.ySpeed = 10
        self.canJump = True
        self.player = player
        self.attackDelay = random.randint(1, 1000)
        #Load and Scale Image
        if(self.player == 0):
            image = pygame.transform.scale(pygame.image.load('Images/sprite0.png').convert_alpha(), (50,50))
        elif(self.player == 1):
            image = pygame.transform.scale(pygame.image.load('Images/sprite1.png').convert_alpha(), (50,50))
        #Call GameObject Init
        super(Fighter, self).__init__(x,y,image)

    #Update Object, should be called each frame
    def update(self, keysDown, screenWidth, screenHeight, attacks, dt):
        if(self.player == 0):
            #Move The Charecter
            if keysDown(pygame.K_LEFT):
                self.x -= self.xSpeed
            if keysDown(pygame.K_RIGHT):
                self.x += self.xSpeed
            if keysDown(pygame.K_UP):
                if(self.canJump):
                    self.jump()

            self.attackDelay -= dt

            if keysDown(pygame.K_DOWN and self.attackDelay <= 0):
                attacks[self.player].add(Attack(self.x+self.width//2,self.y))
                self.attackDelay = 500 + random.randint(1, 1000)
        #Gravity
        if(self.ySpeed < 10):
            self.ySpeed += 1
        self.y += self.ySpeed
        #Update Box
        self.updateRect()

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

    def jump(self):
        self.ySpeed = -15
        self.canJump = False
    ########
