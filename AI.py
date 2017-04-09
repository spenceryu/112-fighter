import pygame, random

# single-player AI for player
def moveAIFighter(player, other):
    # return a string for a piece of movement
    options = ['moveLeft', 'moveRight', 'jump', 'attack']
    aggroOptions = ['moveLeft', 'moveRight'] + ['jump']*2 + ['attack']*5
    aggroDist = 100
    # the options for aggression are weighted towards attacking
    if distance(player.x,other.x,player.y,other.y) < aggroDist:
        return random.choice(aggroOptions)
    else:
        return random.choice(options)

def distance(x0,x1,y0,y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5