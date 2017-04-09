import pygame, random

# single-player AI for player
def moveAIFighter(player, other):
    # return a string for a piece of movement
    options = ['moveLeft', 'moveRight']*50
    aggroOptions = ['moveLeft', 'moveRight']
    if player.canJump:
        options += ['jump']
        aggroOptions += ['jump']*2
    if player.attackDelay <= 0:
        options += ['attack']
        aggroOptions += ['attack']*5 + ['']*10
    aggroDist = 100
    # the options for aggression are weighted towards attacking
    if distance(player.x,other.x,player.y,other.y) < aggroDist:
        return random.choice(aggroOptions)
    else:
        return random.choice(options)

def distance(x0,x1,y0,y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5