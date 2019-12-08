import pygame
from constants import *


class PygameWindow:
    """
    The PygameWindow class contains the data about the actual window that the game is displayed in.

    Attributes:
        width       (int):              The horizontal dimension of the displayed window.
        depth       (int):              The vertical dimension of the displayed window.
        screen      (pygame.Surface):   The actual graphics object that the game is drawn onto.
    """

    def __init__(self):
        pygame.init()
        self.width = PYGAME_WINDOW_WIDTH
        self.depth = PYGAME_WINDOW_DEPTH
        self.screen = pygame.display.set_mode((self.width, self.depth))

    def prepare(self):
        """
        Prepares the window to be drawn.
        """
        self.screen.fill((255, 255, 255))

    def reveal(self):
        """
        Draws the window onto the monitor once all changes have been made.
        """
        pygame.display.update()