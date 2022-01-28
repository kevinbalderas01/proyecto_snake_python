import random
import pygame
import sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20


CELL_WIDTH = WINDOWWIDTH // CELLSIZE
CELL_HEIGHT = WINDOWHEIGHT // CELLSIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0


def main():
    global FPS_CLOCK , DISP_SURF , BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISP_SURF = pygame.display.set_mode((WINDOWWIDTH , WINDOWHEIGHT))
    BASIC_FONT = pygame.font.SysFont('Cambria',18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():

    #Posición aleatoria de la serpiente
    startx = random.randint(5 , CELL_WIDTH-6)
    starty = random.randint(5 , CELL_HEIGHT-6)

    wormCoords = [{'x':startx , 'y':starty} ,
                  {'x':startx-1 , 'y':starty} ,
                  {'x':startx-2 , 'y':starty}]

    #O sea que la serpiente se moverá al incio del juego
    direction = RIGHT

    #Se dibuja la manzana a comer
    apple = getRandomLocation(wormCoords)
    #Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and (direction !=RIGHT):
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and (direction !=LEFT):
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and (direction !=DOWN):
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and (direction !=UP):
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        #Revisamos que no hallamos chocado contra el muro (4 esquinas)
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELL_WIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELL_HEIGHT:
            return #Game over

        #Checamos que no nos hallamos mordido
        for worm in wormCoords[1:]:
            if worm['x'] == wormCoords[HEAD]['x'] and worm['y'] == wormCoords[HEAD]['y']:
                return #Game over

        #Revisamos si se comio una manzana
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation(wormCoords)
        else:
            del wormCoords[-1]

        #Movimiento de la serpiente
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'] , 'y':wormCoords[HEAD]['y']-1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'] , 'y':wormCoords[HEAD]['y']+1}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x']+1 , 'y':wormCoords[HEAD]['y']}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x']-1 , 'y':wormCoords[HEAD]['y']}
        wormCoords.insert(0 , newHead)

        #Se dibujan los elementos
        DISP_SURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords)-3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def showStartScreen():
    titleFont = pygame.font.SysFont('Cambria' , 100)
    #Letras blancas con fondo verdoso
    titleSurf1 = titleFont.render('Wormy!' , True , WHITE , DARKGREEN)
    #Letras verdes sin color de fondo
    titleSurf2 = titleFont.render('Wormy!' , True , GREEN)

    degree1 = 0
    degree2 = 0

    while True:
        DISP_SURF.fill(BGCOLOR)
        #Rotación de letras blancas con fondo verdoso
        rotatedSurf1 = pygame.transform.rotate(titleSurf1 , degree1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2 , WINDOWHEIGHT /2)
        DISP_SURF.blit(rotatedSurf1 , rotatedRect1)
        #Rotación de letras verdes
        rotatedSurf2 = pygame.transform.rotate(titleSurf2 , degree2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH/2 , WINDOWHEIGHT /2)
        DISP_SURF.blit(rotatedSurf2 , rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        degree1 +=3
        degree2 +=7

def drawPressKeyMsg():
    pressKeySurf = BASIC_FONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH-200 , WINDOWHEIGHT-30)
    DISP_SURF.blit(pressKeySurf , pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) ==0:
        return False
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def getRandomLocation(wormCoords):
    pos_apple = {'x':random.randint(0 , CELL_WIDTH -1) , 'y':random.randint(0 , CELL_HEIGHT-1)}
    for cube in wormCoords:
        if cube['x'] == pos_apple['x'] and cube['y'] == pos_apple['y']:
            pos_apple = {'x':CELLSIZE-1 , 'y':CELLSIZE-1}
    return pos_apple

def terminate():
    pygame.quit()
    sys.exit()

def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(DISP_SURF , DARKGRAY , (x , 0) , (x , WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISP_SURF , DARKGRAY , (0 , y) , (WINDOWWIDTH , y))

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        #Se dibuja el segmento externo
        wormFirstRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISP_SURF , DARKGREEN , wormFirstRect)
        #Se dibuja el segmento interno
        wormSecondRect = pygame.Rect(x+4,y+4,CELLSIZE-8,CELLSIZE-8)
        pygame.draw.rect(DISP_SURF , GREEN , wormSecondRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)#Objeto Rect
    pygame.draw.rect(DISP_SURF, RED , appleRect)

def drawScore(cubes):
    scoreSurf = BASIC_FONT.render('Score: %s'%(cubes) , True , WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-120 , 10)
    DISP_SURF.blit(scoreSurf , scoreRect)

def showGameOverScreen():
    gameOverScreen = pygame.font.SysFont('Cambria' , 150)
    gameSurf = gameOverScreen.render('Game' , True , WHITE)
    overSurf = gameOverScreen.render('Over' , True , WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2 , 10)
    overRect.midtop = (WINDOWWIDTH / 2 , gameRect.height + 10 +25)

    DISP_SURF.blit(gameSurf , gameRect)
    DISP_SURF.blit(overSurf , overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()
    while True:
        if checkForKeyPress():
            pygame.event.get() #Clear event queue
            return

if __name__ == '__main__':
    main()
