import socket
from _thread import *
from queue import Queue


HOST = 'Jacobs-MBP-2.wv.cc.cmu.edu'
PORT = 64732

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")


serverMsg = Queue(5)
start_new_thread(handleServerMsg, (server, serverMsg))
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
        self.HealthBars = [HealthBar(0), HealthBar(1)]
        self.attacks = []
        self.Background = pygame.sprite.Group(Background())
        self.players = []
        self.whoAmI = None
        self.gameOver = False
        self.gameOverFont = pygame.font.Font(pygame.font.get_default_font(), 48)
        self.instructFont = pygame.font.Font(pygame.font.get_default_font(), 24)

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
        if (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            try:
                if msg.startswith("newPlayer"):
                    msg = msg.split()
                    newPID = int(msg[1])
                    if len(msg) > 2:
                        self.whoAmI = int(msg[2])
                    if newPID == 0:
                        self.players.append(pygame.sprite.Group(Fighter(self.width//4,self.height//2,0,1)))
                    else:
                        self.players.append(pygame.sprite.Group(Fighter(self.width//4*3,self.height//2,1,-1)))
                    self.attacks.append(pygame.sprite.Group())
                elif msg.startswith("playerMoved"):
                    msg = msg.split()
                    PID = int(msg[1])
                    if msg[2] != "None":
                        dx = int(msg[2])
                    else:
                        dx = None
                    if msg[3] != "None":
                        dir = int(msg[3])
                    else:
                        dir = None
                    if msg[4] != "None":
                        ySpeed = int(msg[4])
                    else:
                        ySpeed = None
                    if msg[5] != "None":
                        ax = int(msg[5])
                    else:
                        ax = None
                    if msg[6] != "None":
                        ay = int(msg[6])
                    else:
                        ay = None
                    if msg[7] != "None":
                        adir = int(msg[7])
                    else:
                        adir = None
                    if len(msg) > 8:
                        PID2 = int(msg[8])
                        if msg[9] != "None":
                            dx2 = int(msg[9])
                        else:
                            dx2 = None
                        if msg[10] != "None":
                            dir2 = int(msg[10])
                        else:
                            dir2 = None
                        if msg[11] != "None":
                            ySpeed2 = int(msg[11])
                        else:
                            ySpeed2 = None
                        if msg[12] != "None":
                            ax2 = int(msg[12])
                        else:
                            ax2 = None
                        if msg[13] != "None":
                            ay2 = int(msg[13])
                        else:
                            ay2 = None
                        if msg[14] != "None":
                            adir2 = int(msg[14])
                        else:
                            adir2 = None
                    if dx != None:
                        self.players[PID].update("x", [dx, dir, self.width, self.height], None, None)
                    if ySpeed != None:
                        self.players[PID].update("jump", ySpeed, None, None)
                    if ax != None:
                        self.attacks[PID].add(Attack(ax, ay, adir))
                    if len(msg) > 8:
                        if dx2 != None:
                            self.players[PID2].update("x", [dx2, dir2, self.width, self.height], None, None)
                        if ySpeed2 != None:
                            self.players[PID2].update("jump", ySpeed2, None, None)
                        if ax2 != None:
                            self.attacks[PID2].add(Attack(ax2, ay2, adir2))
                    
            except:
                print("failed")
            serverMsg.task_done()
        #Gravity
        for player in self.players:
            player.update("gravity", [self.width, self.height], None, None)
        
        if self.whoAmI != None:
            msg = []
            if self.isKeyPressed(pygame.K_UP) or self.isKeyPressed(pygame.K_DOWN) or self.isKeyPressed(pygame.K_LEFT) or self.isKeyPressed(pygame.K_RIGHT):
                self.players[self.whoAmI].update("move", msg, self.isKeyPressed, dt)
                if msg != None and msg[0] != "None None None None None None":
    #               print("sending: ", msg[0])
                    self.server.send((msg[0]+"\n").encode())
        
        for playersAttacks in self.attacks:
            if len(playersAttacks) != 0:
                for attack in playersAttacks:
                    attack.update(dt)
                    
        if len(self.players) > 1:           
            if(pygame.sprite.groupcollide(self.players[0], self.attacks[1], False, True)):
                self.HealthBars[0].health -= 10
            if(pygame.sprite.groupcollide(self.players[1], self.attacks[0], False, True)):
                self.HealthBars[1].health -= 10
            if(self.HealthBars[0].health <= 0):
                self.gameOver = True
                self.winner = "Player 1"
            if(self.HealthBars[1].health <= 0):
                self.gameOver = True
                self.winner = "Player 0"


    def redrawAll(self, screen):
        self.Background.draw(screen)
        if(self.gameOver):
            self.GameOverScreen(screen)
        else:
            for player in self.players:
                player.draw(screen)
            for HealthBar in self.HealthBars:
                HealthBar.drawHealth(screen)
            for group in self.attacks:
                group.draw(screen)

    def GameOverScreen(self, screen):
            #GameOverText
            text = ("%s Wins!") % (self.winner)
            width0, height0 = self.gameOverFont.size(text)
            texSurface = self.gameOverFont.render(text, True, (255,255,255))
            screen.blit(texSurface, (self.width//2-width0//2, self.height//2-height0//2))
            #Instruction Text
            text = "gg"
            width1, height1 = self.instructFont.size(text)
            texSurface = self.instructFont.render(text, True, (255,255,255))
            screen.blit(texSurface, (self.width//2-width1//2, self.height//2+height1+height0))

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, serverMsg=None, server=None, width=600, height=400, fps=50, title="112 Fighter Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.server = server
        self.serverMsg = serverMsg
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
    game = PygameGame(serverMsg, server)
    game.run()

if __name__ == '__main__':
    main()