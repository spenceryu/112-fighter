import pygame

class HealthBar(object):
    # each player number (1,2) has its own health bar
    def __init__(self, name):
        self.name = name
        self.health = 100
    def drawHealth(self, surface):
        margin = 20
        scale = 10 # of health bar
        if self.name == 0 and self.health >= 0:
            pygame.draw.rect(surface, (255-255/100*self.health, 255/100*self.health, 0),
                (margin, margin, scale/100*self.health*margin, margin))
        if self.name == 1 and self.health >= 0:
            offset = margin * (scale+5)
            pygame.draw.rect(surface, (255-255/100*self.health, 255/100*self.health, 0),
                (offset+margin, margin, scale/100*self.health*margin, margin))