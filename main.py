import pygame
import GUI
import Board
from pygameWindow import PYGAME_WINDOW


def main():
    gameWindow = PYGAME_WINDOW()
    gameBoard = Board.Board(gameWindow)
    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                gameBoard.gui.key_listener(event)
            if event.type == pygame.MOUSEMOTION:
                gameBoard.gui.mouse_update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameBoard.gui.mouse_click(event)

        gameWindow.Prepare()

        gameBoard.update()

        gameWindow.Reveal()

main()
