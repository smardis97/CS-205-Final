import sys
import pickle
from pygameWindow import PYGAME_WINDOW
import pygame
sys.path.insert(0, '..')

pygameWindow = PYGAME_WINDOW()

def terminate():
    pygame.quit()
    sys.exit()

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygameWindow.Prepare()

    pygameWindow.Reveal()
