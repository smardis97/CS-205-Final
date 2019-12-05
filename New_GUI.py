from constants import *
import pygame
import abc
import utility
import Tile
import math
from Player import *


class GUI:
    def __init__(self, window, board):
        self.board = board
        self.window = window
        self.menu_state = MENU_MAIN
        self.menu_window = pygame.Surface(GUI_WINDOW_DIMENSIONS)
        self.left_menu = pygame.Surface((BOARD_CENTERED_X, PYGAME_WINDOW_DEPTH))
        self.right_menu = pygame.Surface((BOARD_CENTERED_X, PYGAME_WINDOW_DEPTH))
        self.board_background = pygame.image.load(BOARD_FILE)
        self.dice_results = (-1, -1)
        self.property_result = None
        self.current_player = None
        self.interactable = []
        self.labels = []
        self.build_gui()

    def state_change(self, new_state):
        if new_state is not None:
            self.menu_state = new_state
            self.build_gui()

    def offer_purchase(self, property):
        self.property_result = property
        self.state_change(MENU_BUY)

    def prompt_dice_roll(self):
        self.state_change(MENU_DICE)

    def build_gui(self):
        self.clear_gui()
        window_center_x = GUI_WINDOW_DIMENSIONS[0] / 2
        window_center_y = GUI_WINDOW_DIMENSIONS[1] / 2
        y_interval = BUTTON_DIMENSIONS[1] + 10
        if self.menu_state == MENU_MAIN:
            self.labels.append(Label((window_center_x, 40), BLACK, "Main Menu"))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Play", ButtonOperands.play, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Quit", ButtonOperands.quit, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        elif self.menu_state == MENU_NAME:
            self.labels.append(Label((window_center_x, 40), BLACK, "Enter Name"))

            self.interactable.append(TextBox((window_center_x, window_center_y - 2 * y_interval),
                                              TEXT_BOX_COLOR, TEXT_BOX_HIGHLIGHT, TEXT_BOX_ACTIVE))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Confirm", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        elif self.menu_state == MENU_COLOR:
            self.labels.append(Label((window_center_x, 40), BLACK, "Choose Color"))

            self.interactable.append(Button((window_center_x, window_center_y - 2 * y_interval),
                                            "Red", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, RED))

            self.interactable.append(Button((window_center_x, window_center_y - 1 * y_interval),
                                            "Blue", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, BLUE))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Green", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, GREEN))

            self.interactable.append(Button((window_center_x, window_center_y + 1 * y_interval),
                                            "Purple", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, PURPLE))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Orange", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, ORANGE))

            self.interactable.append(Button((window_center_x, window_center_y + 3 * y_interval),
                                            "Yellow", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, YELLOW))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        elif self.menu_state == MENU_OPP_SEL:
            self.labels.append(Label((window_center_x, 40), BLACK, "Select Opponents"))

            for i in range(1, 6):
                self.interactable.append(Button((window_center_x,
                                                 window_center_y - 2 * y_interval + i * y_interval),
                                                "{}".format(i), ButtonOperands.confirm,
                                                BUTTON_COLOR, BUTTON_HIGHLIGHT, i))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        elif self.menu_state == MENU_START:
            self.labels.append(Label((window_center_x, 40), BLACK, "Ready?"))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval), BLACK,
                                     "Player: {}".format(self.board.getHumanPlayers()[0])))

            self.labels.append(Label((window_center_x, window_center_y - y_interval), BLACK,
                                     "Opponents: {}".format(len(self.board.getPlayers()) - 1)))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Confirm", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))

        elif self.menu_state == MENU_WAIT:
            self.labels.append(Label((window_center_x, window_center_y), BLACK, "Waiting..."))
        elif self.menu_state == MENU_DICE:
            self.labels.append(Label((window_center_x, 40), BLACK, "Roll Dice"))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Roll", ButtonOperands.roll, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        elif self.menu_state == MENU_RESULT:
            self.labels.append(Label((window_center_x, 40), BLACK, "Result"))

            self.labels.append(DiceGraphic((window_center_x - DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[0]))

            self.labels.append(DiceGraphic((window_center_x + DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[1]))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.dice_results)))
        elif self.menu_state == MENU_BUY:
            if self.property_result is not None:
                self.labels.append(Label((window_center_x, 40), BLACK, "Purchase?"))

                self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                         BLACK, "{}".format(self.property_result.getName())))

                self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                         BLACK, "$ - {}".format(self.property_result.getPurchaseValue())))

                self.labels.append(Label((window_center_x, window_center_y - y_interval),
                                         BLACK, "Group: {}".format(self.property_result.getGroup())))

                self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                                "Yes", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT, True))

                self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                                "No", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT, False))
            else:
                self.state_change(MENU_WAIT)
        elif self.menu_state == MENU_OVER:
            pass

    def key_listener(self, event):
        for inter in self.interactable:
            if type(inter) == TextBox:
                inter.input(event)

    def mouse_update(self, mouse_event):
        for button in self.interactable:
            button.contains_mouse(mouse_event.__dict__['pos'])

    def mouse_click(self, mouse_event):
        for inter in self.interactable:
            self.state_change(inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                                          mstate=self.menu_state,
                                          player=self.current_player,
                                          property=self.property_result,
                                          board=self.board,
                                          gui=self))

    def clear_gui(self):
        del self.interactable[:]
        self.interactable = []
        del self.labels[:]
        self.labels = []

    def draw_gui(self):
        self.window.screen.blit(self.board_background, (BOARD_CENTERED_X, 0))
        self.draw_players()
        self.menu_window.fill(GUI_WINDOW_COLOR)
        self.left_menu.fill(GUI_WINDOW_COLOR)
        self.right_menu.fill(GUI_WINDOW_COLOR)

        self.draw_border()
        for label in self.labels:
            self.menu_window.blit(label.draw(), label.get_position())
        for inter in self.interactable:
            self.menu_window.blit(inter.draw(), inter.get_position())
        if self.menu_state is not MENU_NONE:
            self.window.screen.blit(self.menu_window, GUI_WINDOW_POSITION)
        self.window.screen.blit(self.left_menu, (0, 0))
        self.window.screen.blit(self.right_menu, (PYGAME_WINDOW_WIDTH - BOARD_CENTERED_X, 0))

    def draw_border(self):
        pygame.draw.line(self.menu_window, BLACK, (0, GUI_BORDER_WIDTH / 2 - 1),
                         (GUI_WINDOW_DIMENSIONS[0], GUI_BORDER_WIDTH / 2 - 1), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, 0),
                         (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, GUI_WINDOW_DIMENSIONS[1]), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0], GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2),
                         (0, GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_BORDER_WIDTH / 2 - 1, GUI_WINDOW_DIMENSIONS[1]),
                         (GUI_BORDER_WIDTH / 2 - 1, 0), GUI_BORDER_WIDTH)

        pygame.draw.line(self.left_menu, BLACK, (self.left_menu.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, 0),
                         (self.left_menu.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, self.left_menu.get_size()[1]), GUI_BORDER_WIDTH)

        pygame.draw.line(self.right_menu, BLACK, (GUI_BORDER_WIDTH / 2 - 1, 0),
                         (GUI_BORDER_WIDTH / 2 - 1, self.right_menu.get_size()[1]), GUI_BORDER_WIDTH)

    def set_dice_result(self, dice):
        self.dice_results = dice

    def draw_players(self):
        board_state = [[] for i in range(40)]
        for player, data in self.board.getPlayers().items():
            board_state[data[1]].append(data[0])
        for i in range(40):
            tile_corners = TILE_BOUNDS[i]
            fit_across = math.floor((tile_corners[1][0] - tile_corners[0][0]) / PLAYER_GRAPHIC_DIAMETER)
            for player in board_state[i]:
                horizontal_pos = board_state[i].index(player) % fit_across
                vertical_pos = math.floor(board_state[i].index(player) / fit_across)
                position = (tile_corners[0][0] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * horizontal_pos,
                            tile_corners[0][1] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * vertical_pos)
                pygame.draw.circle(self.window.screen, player.color, utility.vector_floor(position), PLAYER_GRAPHIC_RADIUS)
                if player.getName() == self.current_player:
                    pygame.draw.circle(self.window.screen, BLACK, utility.vector_floor(position), PLAYER_GRAPHIC_RADIUS, 2)




class MenuObject:
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, color):
        self.position = position
        self.color = color

    @abc.abstractmethod
    def get_position(self):
        return NotImplemented

    @abc.abstractmethod
    def draw(self):
        return NotImplemented

    @abc.abstractmethod
    def contains_mouse(self, mouse_pos):
        return NotImplemented

    @abc.abstractmethod
    def click(self, active=False, **kwargs):
        return NotImplemented


class Button(MenuObject):
    def __init__(self, position, text, func, color, highlight, value=None):
        MenuObject.__init__(self, position, color)
        self.absolute_pos = utility.vector_add(GUI_WINDOW_POSITION, self.get_position())
        self.rect = pygame.Surface(BUTTON_DIMENSIONS)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(),
                                                             BUTTON_TEXT_SIZE
                                                             ),
                                            text, True, BUTTON_TEXT_COLOR)
        self.highlight = highlight if highlight is not None else color
        self.action = func
        self.value = value
        self.hover = False

    def draw(self):
        color = self.color if not self.hover else self.highlight
        self.rect.fill(color)
        self.rect.blit(self.text, self.text_offset())
        return self.rect

    def get_position(self):
        return self.position[0] - (BUTTON_DIMENSIONS[0] / 2), \
               self.position[1] - (BUTTON_DIMENSIONS[1] / 2)

    def text_offset(self):
        x_offset = (self.rect.get_size()[0] / 2) - (self.text.get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.text.get_size()[1] / 2)
        return x_offset, y_offset

    def contains_mouse(self, mouse_pos):
        top_left_corner = self.absolute_pos
        bottom_right_corner = utility.vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        if active:
            return self.action(value=self.value, **kwargs)


class Label(MenuObject):
    def __init__(self, position, color, text):
        MenuObject.__init__(self, position, color)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), MENU_LABEL_SIZE),
                                            text, True, self.color)

    def draw(self):
        return self.text

    def get_position(self):
        return self.position[0] - (self.text.get_size()[0] / 2), self.position[1] - (self.text.get_size()[1] / 2)

    def contains_mouse(self, mouse_pos):
        return False

    def click(self, active=False, **kwargs):
        pass


class TextBox(MenuObject):
    def __init__(self, position, color=TEXT_BOX_COLOR, highlight=TEXT_BOX_HIGHLIGHT, activec=TEXT_BOX_ACTIVE):
        MenuObject.__init__(self, position, color)
        self.absolute_pos = utility.vector_add(GUI_WINDOW_POSITION, self.get_position())
        self.rect = pygame.Surface(TEXT_BOX_DIMENSIONS)
        self.text_content = ""
        self.highlight = highlight
        self.active_color = activec
        self.hover = False
        self.active = False

    def input(self, key_event):
        if key_event.type == pygame.KEYDOWN:
            if key_event.__dict__['key'] == 8:
                if len(self.text_content) > 0:
                    self.text_content = self.text_content[:-1]
            elif 'unicode' in key_event.__dict__:
                self.text_content += key_event.__dict__['unicode']

    def draw(self):
        self.rect.fill(self.get_color())
        self.rect.blit(self.get_text(), self.text_offset())
        return self.rect

    def get_position(self):
        return self.position[0] - (TEXT_BOX_DIMENSIONS[0] / 2), \
               self.position[1] - (TEXT_BOX_DIMENSIONS[1] / 2)

    def get_color(self):
        if self.active:
            color = self.active_color
        elif self.hover:
            color = self.highlight
        else:
            color = self.color
        return color

    def get_text(self):
        return pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), TEXT_BOX_TEXT_SIZE),
                                       self.text_content, True, TEXT_BOX_TEXT_COLOR)

    def text_offset(self):
        x_offset = (self.rect.get_size()[0] / 2) - (self.get_text().get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.get_text().get_size()[1] / 2)
        return x_offset, y_offset

    def contains_mouse(self, mouse_pos):
        top_left_corner = self.absolute_pos
        bottom_right_corner = utility.vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        self.active = active


class DiceGraphic(MenuObject):
    def __init__(self, position, value):
        MenuObject.__init__(self, position, DICE_GRAPHIC_COLOR)
        self.rect = pygame.Surface(DICE_GRAPHIC_DIMENSIONS)
        self.value = value
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), DICE_TEXT_SIZE),
                                            str(self.value), True, DICE_TEXT_COLOR)

    def text_offset(self):
        x_offset = (self.rect.get_size()[0] / 2) - (self.text.get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.text.get_size()[1] / 2)
        return x_offset, y_offset

    def draw(self):
        self.rect.fill(self.color)
        self.rect.blit(self.text, self.text_offset())
        return self.rect

    def get_position(self):
        return self.position[0] - (self.rect.get_size()[0] / 2), self.position[1] - (self.rect.get_size()[1] / 2)

    def contains_mouse(self, mouse_pos):
        return False

    def click(self, active=False, **kwargs):
        pass


class ButtonOperands:
    @staticmethod
    def end(board, **kwargs):
        board.progressTurn()
        return MENU_WAIT

    @staticmethod
    def color(value,board, gui, **kwargs):
        board.getPlayers()[gui.current_player][0].setColor(value)
        return MENU_OPP_SEL

    @staticmethod
    def roll(board, gui, **kwargs):
        rolls = board.rollDice()
        gui.set_dice_result(rolls)
        return MENU_RESULT

    @staticmethod
    def confirm(value, mstate, board, gui, **kwargs):
        if mstate == MENU_START:
            board.startGame()
            return MENU_WAIT
        elif mstate == MENU_NAME:
            for inter in gui.interactable:
                if type(inter) is TextBox:
                    board.resetPlayers()
                    board.addPlayer(Player(inter.text_content, True))
                    break
            return MENU_COLOR
        elif mstate == MENU_OPP_SEL:
            for i in range(value):
                board.addPlayer(Player("CPU_{}".format(i + 1)))
            return MENU_START
        elif mstate == MENU_RESULT:
            board.playerStandardMove(value[0], value[1][0] + value[1][1])
            return MENU_END
        elif mstate == MENU_BUY:
            if 'player' in kwargs and 'property' in kwargs:
                if value:
                    pass
                    # board.runPurchase(kwargs['player'], kwargs['property'].getName())
                else:
                    pass
                    # board.startAuction(kwargs['property'].getName(), exclude=kwargs['player'])
            else:
                raise AttributeError

    @staticmethod
    def cancel(board, **kwargs):
        board.resetPlayers()
        return MENU_MAIN

    @staticmethod
    def play(**kwargs):
        return MENU_NAME

    @staticmethod
    def quit(**kwargs):
        exit(0)