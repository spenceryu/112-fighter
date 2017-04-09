import pygame, os
from GameObject import GameObject 

class Background(GameObject):
    def __init__(self):
        self.filepath = os.path.join('Images', 'background.jpg')
        self.image = pygame.transform.scale(pygame.image.load(self.filepath).convert_alpha(), (600,400))
        super(Background, self).__init__(300,200,self.image)