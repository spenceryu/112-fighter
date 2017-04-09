'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
from Fighter import *
from GameObject import *
from Attack import *
from HealthBar import *
from Background import *

class PygameGame(object):

    def init(self):
        self.fighterGroup0 = pygame.sprite.Group(Fighter(self.width//2,self.height//2,0,1))
        self.fighterGroup1 = pygame.sprite.Group(Fighter(self.width//2,self.height//2,1,-1))
        self.fighters = [self.fighterGroup0, self.fighterGroup1]
        self.HealthBars = [HealthBar(0), HealthBar(1)]
        self.attackGroup0 = pygame.sprite.Group()
        self.attackGroup1 = pygame.sprite.Group()
        self.attacks = [self.attackGroup0, self.attackGroup1]
        self.Background = pygame.sprite.Group(Background())

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if(keyCode == pygame.K_t):
            self.HealthBars[0].health -= 10

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        for (i, fighter) in enumerate(self.fighters):
            other = self.fighters[(i+1)%2].sprites()[0]
            fighter.update(self.isKeyPressed, self.width, self.height, self.attacks, other, dt)
        for i in range(len(self.attacks)):
            self.attacks[i].update(dt)


    def redrawAll(self, screen):
        self.Background.draw(screen)
        self.fighterGroup0.draw(screen)
        self.fighterGroup1.draw(screen)
        for HealthBar in self.HealthBars:
            HealthBar.drawHealth(screen)
        for group in self.attacks:
            group.draw(screen)



    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Fighter Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()