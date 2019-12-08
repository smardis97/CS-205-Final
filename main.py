import pygame
import GUI
import Board
from pygameWindow import PygameWindow


def main():
    """
    The actual run loop of the game.
    """
    game_window = PygameWindow()
    game_board = Board.Board(game_window)
    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                game_board.gui.key_listener(event)
            if event.type == pygame.MOUSEMOTION:
                game_board.gui.mouse_update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_board.gui.mouse_click(event)

        game_window.prepare()

        game_board.update()

        game_window.reveal()

main()
