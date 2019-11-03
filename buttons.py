import pygame
from constants import *

pygame.font.init()

class BUTTONS:

    def __init__(self):
        pygame.init()
        self.smallFont = pygame.font.Font('freesansbold.ttf', 20)
        self.width = pygameWindowWidth
        self.depth = pygameWindowDepth
        self.screen = pygame.display.set_mode((pygameWindowWidth, pygameWindowDepth))
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

    def textObjects(self,text,font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()