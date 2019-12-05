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
    graph = pygame.image.load('images/welcome-0.jpg')
    graph = pygame.transform.scale(graph, (910, 910))
    pygameWindow.screen.blit(graph, (290, 0))
    # welcomeText = "Welcome to Monopoly"
    # welcomeFont = pygame.font.Font('freesansbold.ttf', 60)
    # welcome = welcomeFont.render(welcomeText,False,(0, 0, 0))
    # pygameWindow.screen.blit(welcome,(450,200))
    buttons.homeButtons()

def music():
    pygame.mixer.init()
    pygame.mixer.music.load("happyDreams.mp3")
    pygame.mixer.music.play(-1)
def userMovingPosition():
    pygame.draw.circle(pygameWindow.screen,black,(buttons.circleX,buttons.circleY),buttons.circleRadius)


music()
username = ""
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                username += str(chr(event.key))
            if event.key == pygame.K_b:
                username += chr(event.key)
            if event.key == pygame.K_c:
                username += chr(event.key)
            if event.key == pygame.K_d:
                username += chr(event.key)
            if event.key == pygame.K_e:
                username += str(chr(event.key))
            if event.key == pygame.K_f:
                username += chr(event.key)
            if event.key == pygame.K_g:
                username += chr(event.key)
            if event.key == pygame.K_h:
                username += chr(event.key)
            if event.key == pygame.K_i:
                username += str(chr(event.key))
            if event.key == pygame.K_j:
                username += chr(event.key)
            if event.key == pygame.K_k:
                username += chr(event.key)
            if event.key == pygame.K_l:
                username += chr(event.key)
            if event.key == pygame.K_m:
                username += str(chr(event.key))
            if event.key == pygame.K_n:
                username += chr(event.key)
            if event.key == pygame.K_o:
                username += chr(event.key)
            if event.key == pygame.K_p:
                username += chr(event.key)
            if event.key == pygame.K_q:
                username += str(chr(event.key))
            if event.key == pygame.K_r:
                username += chr(event.key)
            if event.key == pygame.K_s:
                username += chr(event.key)
            if event.key == pygame.K_t:
                username += chr(event.key)
            if event.key == pygame.K_u:
                username += str(chr(event.key))
            if event.key == pygame.K_v:
                username += chr(event.key)
            if event.key == pygame.K_w:
                username += chr(event.key)
            if event.key == pygame.K_x:
                username += chr(event.key)
            if event.key == pygame.K_y:
                username += chr(event.key)
            if event.key == pygame.K_z:
                username += chr(event.key)
            if event.key == pygame.K_SPACE:
                username += chr(event.key)
            if event.key == pygame.K_RETURN:
                buttons.programState = 2

    pygameWindow.Prepare()
    if buttons.programState == 2:
        homePage()
    elif buttons.programState == 1:
        buttons.enterUserName(username)
    elif buttons.programState == 0:
        buttons.plainBase(username)
        # buttons.drawButtons()
        # userMovingPosition()

    pygameWindow.Reveal()
