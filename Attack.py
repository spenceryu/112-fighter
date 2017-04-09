import pygame
from GameObject import GameObject


class Attack(GameObject):
    def __init__(self, x, y):
        image = pygame.transform.scale(pygame.image.load('Images/fist.png'), (25,25))
        #Call GameObject Init
        super(Attack, self).__init__(x,y,image)
        self.lifetime = 500 # Time is ms

    def update(self, dt):
        self.lifetime -= dt
        if(self.lifetime <= 0):
            self.kill()