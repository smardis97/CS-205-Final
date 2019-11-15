import pygame
from constants import *
import sys
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
    def DrawButtons(self):
        mouse = pygame.mouse.get_pos()
        # print(mouse[0],mouse[1])
        if self.width/2+50 > mouse[0] > self.width/2-50 and 250 > mouse[1] > 200:
            pygame.draw.rect(self.screen, lightGreen, (self.width/2-50, 200, 100, 50))
        else:
            pygame.draw.rect(self.screen, green, (self.width/2-50, 200, 100, 50))

        if self.width/2+50 > mouse[0] > self.width/2-50 and 325 > mouse[1] > 275:
            pygame.draw.rect(self.screen, lightBlue, (self.width/2-50, 275, 100, 50))
        else:
            pygame.draw.rect(self.screen, blue, (self.width/2-50, 275, 100, 50))

        if self.width/2+50 > mouse[0] > self.width/2-50 and 400 > mouse[1] > 350:
            pygame.draw.rect(self.screen, lightGreen, (self.width/2-50, 350, 100, 50))
        else:
            pygame.draw.rect(self.screen, green, (self.width/2-50, 350, 100, 50))

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