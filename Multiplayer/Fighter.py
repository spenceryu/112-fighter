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
        self.attackDelay = 500
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
    def update(self, choice, msg, keysDown, dt):
        if choice == "move":
            msg.append(self.movePlayerFighter(keysDown, dt))
        elif choice == "gravity":
            if(self.ySpeed < 10):
                self.ySpeed += 1
            self.y += self.ySpeed
            
            self.updateRect()
            if(self.rect.left < 0):
                self.x = self.width//2
            if(self.rect.right > msg[0]):
                self.x = msg[0]-self.width//2
            if(self.rect.top < 0):
                self.y = self.height//2
            if(self.rect.bottom > msg[1]):
                self.y = msg[1]-self.height//2
                self.canJump = True
            #Update Box
            self.updateRect()
        elif choice == "x":
            self.x += msg[0]
            self.direction = msg[1]
            
            self.updateRect()
            self.faceInDir()
            
            if(self.rect.left < 0):
                self.x = self.width//2
            if(self.rect.right > msg[2]):
                self.x = msg[2]-self.width//2
            if(self.rect.top < 0):
                self.y = self.height//2
            if(self.rect.bottom > msg[3]):
                self.y = msg[3]-self.height//2
                self.canJump = True
            #Update Box
            self.updateRect()
        elif choice == "jump":
            self.ySpeed = msg
        
    def movePlayerFighter(self, keysDown, dt):
        #Move The Charecter
        msg = ''
        if keysDown(pygame.K_LEFT):
            msg = msg + self.moveLeft()
        elif keysDown(pygame.K_RIGHT):
            msg = msg + self.moveRight()
        else:
            msg = msg + "None"+" " + "None"
        if keysDown(pygame.K_UP):
            if(self.canJump):
                msg = msg +" " + self.jump()
            else:
                msg = msg +" " + "None"
        else:
            msg = msg +" " + "None"

        self.attackDelay -= dt

        if keysDown(pygame.K_DOWN) and self.attackDelay <= 0:
            msg = msg +" " + self.attack()
            self.attackDelay = 500
        else:
            msg = msg +" " + "None"+" " + "None"+" " + "None"
        
        return msg


    def faceInDir(self):
        if(self.direction == 1):
            self.image = self.imageRight
        else:
            self.image = self.imageLeft

    def jump(self):
        self.canJump = False
        return str(-15)
    
    def moveLeft(self):
        dx = -self.xSpeed
        dir = -1
        return str(dx) + " " + str(dir)

    def moveRight(self):
        dx = self.xSpeed
        dir = 1
        return str(dx) + " " + str(dir)

    def attack(self):
        return str(self.x+self.width//2*self.direction) +" " + str(self.y) +" " +str(self.direction)
