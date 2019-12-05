import pygame
from constants import *


class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.width = PYGAME_WINDOW_WIDTH
        self.depth = PYGAME_WINDOW_DEPTH
        self.screen = pygame.display.set_mode((PYGAME_WINDOW_WIDTH, PYGAME_WINDOW_DEPTH))

    def Prepare(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
        self.screen.fill((255, 255, 255))
        # pygame.display.flip()

    def Reveal(self):
        pygame.display.update()