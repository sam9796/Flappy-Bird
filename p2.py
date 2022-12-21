import random
import sys
import pygame
import math
from pygame.locals import *
FPS=30
SCREENWIDTH=289
SCREENHEIGHT=512
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='sprites/bird.png'
BACKGROUND='sprites/background.png'
PIPE='sprites/pipe.png'
pygame.display.set_caption("Flappy Bird")
def welcomeScreen():
    """
    shows welcome images on the screen
    :return:
    """
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2
    messagex=int(SCREENWIDTH-GAME_SPRITES['message'].get_width())/2
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    basey=int(SCREENHEIGHT-GAME_SPRITES['base'].get_height())
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and  (event.key==pygame.K_UP or event.key==pygame.K_SPACE):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT) / 2
    basex=0
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerFlapAccv = -8
    playerFlapped=False
    score=0
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    upperPipes=[
        {'x':200+SCREENWIDTH,'y':newPipe1[0]['y']},
        {'x':200+SCREENWIDTH+SCREENWIDTH/2,'y':newPipe2[0]['y']}
    ]
    lowerPipes=[
        {'x':200+SCREENWIDTH,'y':newPipe1[1]['y']},
        {'x':200+SCREENWIDTH+SCREENWIDTH/2,'y':newPipe2[1]['y']}
    ]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_UP or event.key==pygame.K_SPACE):
                playerVelY=playerFlapAccv
                playerFlapped=True
                GAME_SOUNDS['wing'].play()

        collide=isCollide(playerx,playery,upperPipes,lowerPipes)
        if collide:
            return
        playersc=playerx+GAME_SPRITES['player'].get_width()/2;
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            pipemid=upperPipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if playersc>=pipemid and playersc<pipemid+4:
                score+=1
                GAME_SOUNDS['point'].play()
        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=1
        if playerFlapped:
            playerFlapped=False
        playery+=playerVelY
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX
        if 0<upperPipes[0]['x']<5:
            newPipe=getRandomPipe();
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        if upperPipes[0]['x']+GAME_SPRITES['pipe'][0].get_width()<=0:
            upperPipes.pop(0)
            lowerPipes.pop(0)
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        alp=str(score)
        width=0
        for key in alp:
            width+=GAME_SPRITES['numbers'][int(key)].get_width();
        off=(SCREENWIDTH - width)/2
        for key in alp:
            img=GAME_SPRITES['numbers'][int(key)]
            SCREEN.blit(img, (off, SCREENHEIGHT * 0.12))
            off+=GAME_SPRITES['numbers'][int(key)].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx,playery,upperPipes,lowerPipes):
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    if playery+GAME_SPRITES['player'].get_height()>=GROUNDY:
        GAME_SOUNDS['hit'].play();
        return True;
    for pipe in upperPipes:
        if playery<pipeHeight+pipe['y'] and playerx+GAME_SPRITES['player'].get_width()>=pipe['x'] and playerx<pipe['x']+GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play();
            return True
    for pipe in lowerPipes:
        if playery+GAME_SPRITES['player'].get_height()>pipe['y'] and playerx+GAME_SPRITES['player'].get_width()>=pipe['x'] and playerx<pipe['x']+GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play();
            return True;
def getRandomPipe():
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    h1=(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-5*GAME_SPRITES['player'].get_height())/2
    offset=h1/5
    l1=(random.randint(0,(4*h1)/5))
    choose=random.randint(1,2)
    if choose==1:
        ytop=h1+l1-pipeHeight
        ybottom=(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-(h1-l1))
    else :
        ytop = h1 - l1 - pipeHeight
        ybottom = (SCREENHEIGHT - GAME_SPRITES['base'].get_height() - (h1 + l1))
    pipex=SCREENWIDTH+10
    return [{'x':pipex,'y':ytop},
            {'x':pipex,'y':ybottom}]


if __name__=="__main__":
    pygame.init()
    FPSCLOCK =pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    GAME_SPRITES['numbers']=(
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),)
    GAME_SPRITES['message']=pygame.image.load('sprites/message.png').convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE),
    )
    GAME_SPRITES['base']=pygame.image.load('sprites/base.png').convert_alpha()
    GAME_SOUNDS['die']=pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    while True:
        welcomeScreen()
        mainGame()
        FPSCLOCK.tick(FPS)













