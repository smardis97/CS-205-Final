import pygame
from constants import *
import sys
import random

sys.path.insert(0, '..')

pygame.font.init()

class BUTTONS:

    def __init__(self):
        pygame.init()
        self.smallFont = pygame.font.Font('freesansbold.ttf', 20)
        self.width = pygameWindowWidth
        self.depth = pygameWindowDepth
        self.screen = pygame.display.set_mode((pygameWindowWidth, pygameWindowDepth))
        self.programState = 0
        self.musicState = True
        self.dice1=random.randint(1,6)
        self.dice2=random.randint(1,6)
    def DrawButtons(self):
        mouse = pygame.mouse.get_pos()
        # start
        if self.width/2+50 > mouse[0] > self.width/2-50 and 250 > mouse[1] > 200:
            pygame.draw.rect(self.screen, lightGreen, (self.width/2-50, 200, 100, 50))
        else:
            pygame.draw.rect(self.screen, green, (self.width/2-50, 200, 100, 50))
        # dice
        if self.width/2+50 > mouse[0] > self.width/2-50 and 325 > mouse[1] > 275:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2-50, 275, 100, 50))
            if mouse[0]==1:
                sumDice=self.dice1+self.dice2

        else:
            pygame.draw.rect(self.screen, blue, (self.width/2-50, 275, 100, 50))
        # reset
        if self.width/2+50 > mouse[0] > self.width/2-50 and 400 > mouse[1] > 350:
            pygame.draw.rect(self.screen, lightGreen, (self.width/2-50, 350, 100, 50))
        else:
            pygame.draw.rect(self.screen, green, (self.width/2-50, 350, 100, 50))
        # quit
        if self.width/2+50 > mouse[0] > self.width/2-50 and 475 > mouse[1] > 425:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2-50, 425, 100, 50))
        else:
            pygame.draw.rect(self.screen, blue, (self.width/2-50, 425, 100, 50))

        startSurf, startRect = self.textObjects("Start",self.smallFont)
        diceSurf, diceRect = self.textObjects("Dice",self.smallFont)
        resetSurf, resetRect = self.textObjects("Reset",self.smallFont)
        quitSurf, quitRect = self.textObjects("Quit",self.smallFont)


        startRect.center=(self.width/2, 200+25)
        diceRect.center=(self.width/2, 275+25)
        resetRect.center=(self.width/2, 350+25)
        quitRect.center=(self.width/2, 425+25)

        self.screen.blit(startSurf, startRect)
        self.screen.blit(diceSurf, diceRect)
        self.screen.blit(resetSurf, resetRect)
        self.screen.blit(quitSurf, quitRect)

    def homeButtons(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # start
        if self.width/2+100 > mouse[0] > self.width/2-100 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightGreen, (self.width/2-100, 470, 200, 100))
            if click[0] == 1:
                self.programState = 1
        else:
            pygame.draw.rect(self.screen, green, (self.width/2-100, 470, 200, 100))
        # music
        if self.width/2-200 > mouse[0] > self.width/2-400 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2-400, 470, 200, 100))
            if click[0] == 1 and self.musicState:
                pygame.mixer.music.pause()
                self.musicState = False
            elif click[0] == 1 and not self.musicState:
                pygame.mixer.music.unpause()
                self.musicState = True

        else:
            pygame.draw.rect(self.screen, blue, (self.width/2-400, 470, 200, 100))
        # quit
        if self.width/2+400 > mouse[0] > self.width/2+200 and 570 > mouse[1] > 470:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2+200, 470, 200, 100))
            if click[0] ==1:
                pygame.display.quit()
                pygame.quit()
                exit()
        else:
            pygame.draw.rect(self.screen, blue, (self.width/2+200, 470, 200, 100))

        startSurf, startRect = self.textObjects("Start",self.smallFont)
        musicSurf, musicRect = self.textObjects("Music",self.smallFont)
        quitSurf, quitRect = self.textObjects("Quit",self.smallFont)


        startRect.center=(self.width/2-100+100, 470+50)
        musicRect.center=(self.width/2-400+100, 470+50)
        quitRect.center=(self.width/2+200+100, 470+50)

        self.screen.blit(startSurf, startRect)
        self.screen.blit(musicSurf, musicRect)
        self.screen.blit(quitSurf, quitRect)

    def textObjects(self,text,font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def plainBase(self):
        # background
        # boardWidth=910
        # boardDepth=910
        # boardStartX=295
        pygame.draw.rect(self.screen, backgroundGreen, (295, 0, 910, 910))
        # each rectangle 70*140
        for i in range(0,10):
            pygame.draw.line(self.screen, (0, 0, 0), [295+140+i*70, 0], [295+140+i*70, 140])
            pygame.draw.line(self.screen, (0, 0, 0), [295, 140+i*70], [295+140, 140+i*70])
            pygame.draw.line(self.screen, (0, 0, 0), [295+140+i*70, 910-140], [295+140+i*70, 910])
            pygame.draw.line(self.screen, (0, 0, 0), [295+910-140, 140+i*70], [pygameWindowWidth-295, 140+i*70])
        pygame.draw.lines(self.screen, (0, 0, 0), True, [(295+140,140),(295+140,910-140),(295+910-140,910-140),(295+910-140,140)])
        ## eight colors rectangles
        ## small rectangle size 70*15
        smallDepth = 35
        # green
        pygame.draw.rect(self.screen, green, (295+910-140-70+1, 910-140+1, 69, smallDepth))
        pygame.draw.rect(self.screen, green, (295+910-140-70*2+1, 910-140+1, 69, smallDepth))
        pygame.draw.rect(self.screen, green, (295+910-140-70*4+1, 910-140+1, 69, smallDepth))

        # blue
        pygame.draw.rect(self.screen, blue, (295+140+1, 910-140+1, 69, smallDepth))
        pygame.draw.rect(self.screen, blue, (295+140+70*2+1, 910-140+1, 69, smallDepth))

        # brown
        pygame.draw.rect(self.screen, brown, (295+140-smallDepth, 910-140-70+1, smallDepth, 69))
        pygame.draw.rect(self.screen, brown, (295+140-smallDepth, 910-140-70*3+1, smallDepth, 69))

        # slightblue
        pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+1, smallDepth, 69))
        pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+70+1, smallDepth, 69))
        pygame.draw.rect(self.screen, slightBlue, (295+140-smallDepth, 140+70*3+1, smallDepth, 69))

        # purple
        pygame.draw.rect(self.screen, purple, (295+140+1, 140-smallDepth, 69, smallDepth))
        pygame.draw.rect(self.screen, purple, (295+140+70*2+1, 140-smallDepth, 69, smallDepth))
        pygame.draw.rect(self.screen, purple, (295+140+70*3+1, 140-smallDepth, 69, smallDepth))

        # orange
        pygame.draw.rect(self.screen, orange, (295+910-140-70+1, 140-smallDepth, 69, smallDepth))
        pygame.draw.rect(self.screen, orange, (295+910-140-70*2+1, 140-smallDepth, 69, smallDepth))
        pygame.draw.rect(self.screen, orange, (295+910-140-70*4+1, 140-smallDepth, 69, smallDepth))

        # red
        pygame.draw.rect(self.screen, red, (295+910-140+1, 140+1, smallDepth, 69))
        pygame.draw.rect(self.screen, red, (295+910-140+1, 140+70*2+1, smallDepth, 69))
        pygame.draw.rect(self.screen, red, (295+910-140+1, 140+70*3+1, smallDepth, 69))

        # yellow
        pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70+1, smallDepth, 69))
        pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70*3+1, smallDepth, 69))
        pygame.draw.rect(self.screen, yellow, (295+910-140+1, 910-140-70*4+1, smallDepth, 69))

