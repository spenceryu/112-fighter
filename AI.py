import pygame, random

# single-player AI for player
def moveAIFighter(player, other):
    # return a string for a piece of movement
    options = ['moveLeft', 'moveRight']
    aggroOptions = ['moveLeft', 'moveRight'] * 3
    increasedLeft = ['moveLeft'] * 3
    increasedRight = ['moveRight'] * 3
    # the AI is more likely to go in the direction it is facing
    if player.direction == 1:
        options += increasedRight
        aggroOptions += increasedRight
    else:
        options += increasedLeft
        aggroOptions += increasedLeft
    # increase likelihood of choosing other's direction
    if distance(player.x, other.x+10, player.y, other.y) <\
        distance(player.x, other.x, player.y, other.y):
        # more likely to move left
        options += increasedLeft
        aggroOptions += increasedLeft
    else: # more likely to move right
        options += increasedRight
        aggroOptions += increasedRight

    if player.canJump:
        aggroOptions += ['jump']
    if player.attackDelay <= 0:
        aggroOptions += ['attack']*5
    aggroDist = 100
    # the options for aggression are weighted towards attacking
    if distance(player.x,other.x,player.y,other.y) < aggroDist:
        return random.choice(aggroOptions)
    else:
        return random.choice(options)

def distance(x0,x1,y0,y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5