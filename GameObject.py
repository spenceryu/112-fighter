import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(GameObject, self).__init__()
        self.x, self.y, self.image = x, y, image
        self.width,self.height = self.image.get_size()
        self.updateRect()

    #Update Box Around Object
    def updateRect(self):
        self.rect = pygame.Rect(self.x-self.width//2,self.y-self.height//2,
                                self.width,self.height)

