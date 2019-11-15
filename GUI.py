import sys
import pickle
from pygameWindow import PYGAME_WINDOW
import pygame
from constants import *
from buttons import BUTTONS
sys.path.insert(0, '..')

pygameWindow = PYGAME_WINDOW()
buttons = BUTTONS()


def homePage():
    # title for home page
    welcomeText = "Welcome to Monopoly"
    welcomeFont = pygame.font.Font('freesansbold.ttf', 60)
    welcome = welcomeFont.render(welcomeText,False,(0, 0, 0))
    pygameWindow.screen.blit(welcome,(450,200))
    buttons.homeButtons()
def plainBase():
    graph = pygame.image.load('images/plainBackground.png')
    graph = pygame.transform.scale(graph, (940, 940))
    pygameWindow.screen.blit(graph, (280, 0))
    graph = pygame.image.load('images/horse.jpeg')
    graph = pygame.transform.scale(graph, (40, 40))
    pygameWindow.screen.blit(graph, (1100, 830))

def music():
    pygame.mixer.init()
    pygame.mixer.music.load("happyDreams.mp3")
    pygame.mixer.music.play(-1)

music()
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygameWindow.Prepare()
    if buttons.programState == 0:
        homePage()
    elif buttons.programState == 1:
        plainBase()
        buttons.DrawButtons()

    pygameWindow.Reveal()
