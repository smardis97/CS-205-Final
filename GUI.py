from constants import *
import pygame
import abc
from utility import *
import Tile
import math
from Player import *


class GUI:
    #
    #
    #  TODO: Docstrings and readability comments
    #
    #
    def __init__(self, window, board):
        self.window = window
        self.board = board
        self.menu_state = MENU_MAIN
        self.menu_window = pygame.Surface(GUI_WINDOW_DIMENSIONS)
        self.left_display = pygame.Surface((BOARD_CENTERED_X, PYGAME_WINDOW_DEPTH))
        self.right_display = pygame.Surface((BOARD_CENTERED_X, PYGAME_WINDOW_DEPTH))
        self.board_background = pygame.image.load(BOARD_FILE)
        self.page_number = -1
        self.interactable = []
        self.labels = []
        self.prop_buttons = []
        self.card_content = []
        self.dice_results = (-1, -1)
        self.property_result = None
        self.current_player = None
        self.card_result = None
        self.special_event_type = None
        self.build_gui()

    def state_change(self, new_state):
        if new_state is not None:
            self.menu_state = new_state
            self.build_gui()

    def build_gui(self):
        self.clear_gui()
        window_center_x = GUI_WINDOW_DIMENSIONS[0] / 2
        window_center_y = GUI_WINDOW_DIMENSIONS[1] / 2
        y_interval = BUTTON_DIMENSIONS[1] + 10
        if self.current_player is not None:
            player = self.board.get_players()[self.current_player][0]
        else:
            player = None
        #
        # MAIN MENU ------------------------------------------------------------------------------------------ MAIN MENU
        #
        if self.menu_state == MENU_MAIN:
            self.labels.append(Label((window_center_x, 40), BLACK, "Main Menu"))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Play", ButtonOperands.play, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Quit", ButtonOperands.quit, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # NAME INPUT ---------------------------------------------------------------------------------------- NAME INPUT
        #
        elif self.menu_state == MENU_NAME:
            self.labels.append(Label((window_center_x, 40), BLACK, "Enter Name"))

            self.interactable.append(TextBox((window_center_x, window_center_y - 2 * y_interval),
                                              TEXT_BOX_COLOR, TEXT_BOX_HIGHLIGHT, TEXT_BOX_ACTIVE))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Confirm", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # COLOR SELECT ------------------------------------------------------------------------------------ COLOR SELECT
        #
        elif self.menu_state == MENU_COLOR:
            self.labels.append(Label((window_center_x, 40), BLACK, "Choose Color"))

            self.interactable.append(Button((window_center_x, window_center_y - 2 * y_interval),
                                            "Red", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, DARK_RED))

            self.interactable.append(Button((window_center_x, window_center_y - 1 * y_interval),
                                            "Blue", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, BLUE))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Green", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, GREEN))

            self.interactable.append(Button((window_center_x, window_center_y + 1 * y_interval),
                                            "Purple", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, LIGHT_PURPLE))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Orange", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, ORANGE))

            self.interactable.append(Button((window_center_x, window_center_y + 3 * y_interval),
                                            "Lime", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, LIME_GREEN))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # OPPONENT SELECT ------------------------------------------------------------------------------ OPPONENT SELECT
        #
        elif self.menu_state == MENU_OPP_SEL:
            self.labels.append(Label((window_center_x, 40), BLACK, "Select Opponents"))

            for i in range(1, 6):
                self.interactable.append(Button((window_center_x,
                                                 window_center_y - 2 * y_interval + i * y_interval),
                                                "{}".format(i), ButtonOperands.confirm,
                                                BUTTON_COLOR, BUTTON_HIGHLIGHT, i))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # START CONFIRMATION ------------------------------------------------------------------------ START CONFIRMATION
        #
        elif self.menu_state == MENU_START:
            self.labels.append(Label((window_center_x, 40), BLACK, "Ready?"))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval), BLACK,
                                     "Player: {}".format(self.board.get_human_players()[0])))

            self.labels.append(Label((window_center_x, window_center_y - y_interval), BLACK,
                                     "Opponents: {}".format(len(self.board.get_players()) - 1)))

            self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                            "Confirm", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Cancel", ButtonOperands.cancel, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # WAIT SCREEN -------------------------------------------------------------------------------------- WAIT SCREEN
        #
        elif self.menu_state == MENU_WAIT:
            self.labels.append(Label((window_center_x, window_center_y), BLACK, "Waiting..."))
        #
        # PLAYER DICE ROLL ---------------------------------------------------------------------------- PLAYER DICE ROLL
        #
        elif self.menu_state == MENU_DICE or self.menu_state == MENU_SE_DICE:
            self.labels.append(Label((window_center_x, 40), BLACK, "Roll Dice"))

            self.interactable.append(Button((window_center_x, window_center_y),
                                            "Roll", ButtonOperands.roll, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # PLAYER DICE RESULT ------------------------------------------------------------------------ PLAYER DICE RESULT
        #
        elif self.menu_state == MENU_RESULT or self.menu_state == MENU_SE_RESULT:
            self.labels.append(Label((window_center_x, 40), BLACK, "Result"))

            self.labels.append(DiceGraphic((window_center_x - DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[0]))

            self.labels.append(DiceGraphic((window_center_x + DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[1]))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.dice_results)))
        #
        # PLAYER BUY ---------------------------------------------------------------------------------------- PLAYER BUY
        #
        elif self.menu_state == MENU_BUY:
            if self.property_result is not None:
                self.labels.append(Label((window_center_x, 40), BLACK, "Purchase?"))

                self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                         BLACK, "{}".format(self.property_result.get_name())))

                self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                         BLACK, "$ - {}".format(self.property_result.get_purchase_value())))

                self.labels.append(Label((window_center_x, window_center_y - y_interval),
                                         BLACK, "Group: {}".format(self.property_result.get_group())))

                self.interactable.append(Button((window_center_x, window_center_y + y_interval),
                                                "Yes", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT, True))

                self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                                "No", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT, False))
            else:
                self.state_change(MENU_WAIT)
        #
        # CPU DICE RESULT ------------------------------------------------------------------------------ CPU DICE RESULT
        #
        elif self.menu_state == MENU_AI_ROLL:
            self.labels.append(Label((window_center_x, 40), BLACK, "{} Roll:".format(self.current_player)))

            self.labels.append(DiceGraphic((window_center_x - DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[0]))

            self.labels.append(DiceGraphic((window_center_x + DICE_OFFSET, window_center_y - y_interval),
                                           self.dice_results[1]))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.dice_results)))
        #
        # CPU BUY ---------------------------------------------------------------------------------------------- CPU BUY
        #
        elif self.menu_state == MENU_AI_BUY:
            self.labels.append(Label((window_center_x, 40), BLACK, "{} Purchased:".format(self.current_player)))

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "{}".format(self.property_result.get_name())))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                     BLACK, "Group: {}".format(self.property_result.get_group())))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))

        #
        # CPU RENT RESULT ------------------------------------------------------------------------------ CPU RENT RESULT
        #
        elif self.menu_state == MENU_AI_RENT:
            self.labels.append(Label((window_center_x, window_center_y - 4 * y_interval),
                                     BLACK, "{} paid".format(self.current_player)))

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "$ {}".format(self.board.get_rent_value(self.property_result.get_name()))))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                     BLACK, "to"))

            self.labels.append(Label((window_center_x, window_center_y - 1 * y_interval),
                                     BLACK, "{}".format(self.property_result.get_owner())))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # CPU SPECIAL RENT RESULT -------------------------------------------------------------- CPU SPECIAL RENT RESULT
        #
        elif self.menu_state == MENU_SE_AI_RENT:
            self.labels.append(Label((window_center_x, window_center_y - 4 * y_interval),
                                     BLACK, "{} paid".format(self.current_player)))

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "$ {}".format(self.special_event_type)))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                     BLACK, "to"))

            self.labels.append(Label((window_center_x, window_center_y - 1 * y_interval),
                                     BLACK, "{}".format(self.property_result.get_owner())))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # PLAYER RENT -------------------------------------------------------------------------------------- PLAYER RENT
        #
        elif self.menu_state == MENU_PLR_AI:
            self.labels.append(Label((window_center_x, window_center_y - 4 * y_interval),
                                     BLACK, "{}".format(self.property_result.get_name())))

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "You must pay:"))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                     BLACK, "$ {}".format(self.board.get_rent_value(self.property_result.get_name()))))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Pay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.property_result.get_owner(),
                                             self.board.get_rent_value(self.property_result.get_name()))))
        #
        # PLAYER SPECIAL RENT ---------------------------------------------------------------------- PLAYER SPECIAL RENT
        #
        elif self.menu_state == MENU_SE_PLR_RENT:
            self.labels.append(Label((window_center_x, window_center_y - 4 * y_interval),
                                     BLACK, "{}".format(self.property_result.get_name())))

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "You must pay:"))

            self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                     BLACK, "$ {}".format(self.special_event_type)))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Pay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.property_result.get_owner(),
                                             self.special_event_type)))
        #
        # PLAYER DEBT -------------------------------------------------------------------------------------- PLAYER DEBT
        #
        elif self.menu_state == MENU_DEBT:
            current_property = player.get_owned_properties()[self.page_number]
            sale_value = (current_property.get_purchase_value() +
                          current_property.get_num_houses() * current_property.get_house_cost()) / 2
            if self.page_number == -1:
                self.labels.append(Label((window_center_x, 40), BLACK, "You are in Debt"))

                self.labels.append(Label((window_center_x, window_center_y - 4 * y_interval), BLACK, "You owe:"))

                self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                         BLACK, "$ {}".format(player.getDebt())))

                self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval),
                                         BLACK, "Choose a property to sell:"))

                self.interactable.append(Button((window_center_x + window_center_x / 2, window_center_y + 4 * y_interval),
                                                ">>>", ButtonOperands.page_right, BUTTON_COLOR, BUTTON_HIGHLIGHT))
            else:
                self.labels.append(Label((window_center_x, window_center_y - 5 * y_interval), BLACK,
                                         "{}".format(player.get_owned_properties()[self.page_number].get_name())))

                self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval), BLACK,
                                         "Sells for:"))

                self.labels.append(Label((window_center_x, window_center_y - 2 * y_interval), BLACK,
                                         "$ {}".format(sale_value)))

                self.interactable.append(Button((window_center_x, window_center_y + 3 * y_interval), "Sell",
                                                ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT, current_property))

                if self.page_number < len(player.get_owned_properties()) - 1:
                    self.interactable.append(Button((window_center_x + window_center_x / 2, window_center_y + 4 * y_interval),
                                                    ">>>", ButtonOperands.page_right, BUTTON_COLOR, BUTTON_HIGHLIGHT))

                    self.interactable.append(Button((window_center_x - window_center_x / 2, window_center_y + 4 * y_interval),
                                                    "<<<", ButtonOperands.page_left, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # PLAYER CHANCE ---------------------------------------------------------------------------------- PLAYER CHANCE
        #
        elif self.menu_state == MENU_CHANCE:
            for message in self.card_content[1]:
                self.labels.append(Label((window_center_x, window_center_y - (4 - self.card_content[1].index(message)) * y_interval),
                                         BLACK, message))

            self.interactable.append(Button((window_center_x, window_center_y + 3 * y_interval),
                                            "Okay", ButtonOperands.chance, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            self.card_content[0]))
        #
        # PLAYER COMMUNITY CHEST ---------------------------------------------------------------- PLAYER COMMUNITY CHEST
        #
        elif self.menu_state == MENU_COM_CH:
            for message in self.card_content[1]:
                self.labels.append(Label((window_center_x, window_center_y - (4 - self.card_content[1].index(message)) * y_interval),
                                         BLACK, message))

            self.interactable.append(Button((window_center_x, window_center_y + 3 * y_interval),
                                            "Okay", ButtonOperands.community_chest, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            self.card_content[0]))
        #
        # PLAYER END TURN ------------------------------------------------------------------------------ PLAYER END TURN
        #
        elif self.menu_state == MENU_END:
            self.labels.append(Label((window_center_x, 40), BLACK, "End Turn?"))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "END TURN", ButtonOperands.end, BUTTON_COLOR, BUTTON_HIGHLIGHT))
        #
        # GAME OVER ------------------------------------------------------------------------------------------ GAME OVER
        #
        elif self.menu_state == MENU_OVER:
            self.labels.append(Label((window_center_x, window_center_y), BLACK, "You are Bankrupt"))

    def key_listener(self, event):
        for inter in self.interactable:
            if type(inter) == TextBox:
                inter.input(event)

    def mouse_update(self, mouse_event):
        for button in self.interactable:
            button.contains_mouse(mouse_event.__dict__['pos'])
        for button in self.prop_buttons:
            button.contains_mouse(mouse_event.__dict__['pos'])

    def mouse_click(self, mouse_event):
        for inter in self.interactable:
            self.state_change(inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                                          mstate=self.menu_state,
                                          player=self.current_player,
                                          property=self.property_result,
                                          board=self.board,
                                          gui=self))
        for inter in self.prop_buttons:
            self.state_change(inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                                          mstate=self.menu_state,
                                          player=self.current_player,
                                          property=self.property_result,
                                          board=self.board,
                                          gui=self))

    def draw_gui(self):
        self.window.screen.blit(self.board_background, (BOARD_CENTERED_X, 0))
        self.draw_tile_details_on_board()
        self.draw_players()
        self.menu_window.fill(GUI_WINDOW_COLOR)
        self.left_display.fill(GUI_WINDOW_COLOR)
        self.draw_left_display()
        self.right_display.fill(GUI_WINDOW_COLOR)
        self.draw_right_display()

        self.draw_border()
        for label in self.labels:
            self.menu_window.blit(label.draw(), label.get_position())
        for inter in self.interactable:
            self.menu_window.blit(inter.draw(), inter.get_position())
        if self.menu_state is not MENU_NONE:
            self.window.screen.blit(self.menu_window, GUI_WINDOW_POSITION)
        self.window.screen.blit(self.left_display, (0, 0))
        self.window.screen.blit(self.right_display, (PYGAME_WINDOW_WIDTH - BOARD_CENTERED_X, 0))

    def draw_players(self):
        board_state = [[] for i in range(40)]
        for player, data in self.board.get_players().items():
            board_state[data[1]].append(data[0])
        for i in range(40):
            tile_corners = TILE_BOUNDS[i]
            fit_across = math.floor((tile_corners[1][0] - tile_corners[0][0]) / PLAYER_GRAPHIC_DIAMETER)
            for player in board_state[i]:
                horizontal_pos = board_state[i].index(player) % fit_across
                vertical_pos = math.floor(board_state[i].index(player) / fit_across)
                position = (tile_corners[0][0] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * horizontal_pos,
                            tile_corners[0][1] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * vertical_pos)
                pygame.draw.circle(self.window.screen, player.color, vector_floor(position), PLAYER_GRAPHIC_RADIUS)
                if player.get_name() == self.current_player:
                    pygame.draw.circle(self.window.screen, BLACK, vector_floor(position), PLAYER_GRAPHIC_RADIUS + 1, 2)
                if self.board.get_players()[player.get_name()][0].is_human:
                    pygame.draw.circle(self.window.screen, BLACK, vector_floor(position), HUMAN_MARKER_RADIUS)

    def draw_tile_details_on_board(self):
        for name, details in self.board.get_properties().items():
            tile_position = TILE_BOUNDS[self.board.get_tiles().index(details)]
            if details.get_owner() is not None:
                owner = self.board.get_players()[details.get_owner()][0]
                pygame.draw.circle(self.window.screen, owner.color,
                                   vector_floor(vector_add(tile_position[1], OWNER_MARKER_POSITION)),
                                   OWNER_MARKER_RADIUS)
                if details.get_num_hotels() > 0:
                    rect = pygame.Surface(HOUSE_MARKER_DIMENSIONS)
                    rect.fill(RED)
                    self.window.screen.blit(rect, vector_floor(vector_add((tile_position[0][0], tile_position[1][1]),
                                                                          HOUSE_MARKER_POSITION)))
                elif details.get_num_houses() > 0:
                    rect = pygame.Surface(HOUSE_MARKER_DIMENSIONS)
                    rect.fill(GREEN)
                    num = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), HOUSE_MARKER_TEXT_SIZE),
                                                  str(details.get_num_houses()), True, BLACK)
                    rect.blit(num, HOUSE_MARKER_TEXT_OFFSET)
                    self.window.screen.blit(rect, vector_floor(vector_add((tile_position[0][0], tile_position[1][1]),
                                                                    HOUSE_MARKER_POSITION)))

    def draw_left_display(self):
        for name, cpu in self.board.get_players().items():
            if not cpu[0].is_human:
                position = (LEFT_MENU_OFFSET[0],
                            LEFT_MENU_OFFSET[1] + LEFT_MENU_SEPARATION * (self.board.turn_order.index(name) - 1))
                pygame.draw.circle(self.left_display, cpu[0].color, vector_floor(position), PLAYER_GRAPHIC_RADIUS)

                if cpu[0].get_name() == self.current_player:
                    pygame.draw.circle(self.left_display, BLACK, vector_floor(position), PLAYER_GRAPHIC_RADIUS + 1, 2)

                position = (position[0] + LEFT_MENU_TEXT_OFFSET[0],
                            position[1] + LEFT_MENU_TEXT_OFFSET[1])
                name_text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_TEXT_SIZE),
                                                    cpu[0].get_name(), True, BLACK)
                self.left_display.blit(name_text, vector_floor(position))

                position = (position[0], position[1] + LEFT_MENU_MARGIN)
                text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_SUBTEXT_SIZE),
                                               "$ {}".format(cpu[0].get_money()), True, BLACK)
                self.left_display.blit(text, vector_floor(position))

                if cpu[0].is_in_jail():
                    position = (position[0], position[1] + LEFT_MENU_MARGIN)
                    text = pygame.font.Font.render(
                        pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_SUBTEXT_SIZE),
                        "IN JAIL {}".format(cpu[0].jail_counter), True, RED)
                    self.left_display.blit(text, vector_floor(position))

    def draw_right_display(self):
        if len(self.board.get_human_players()) > 0:
            player = self.board.get_players()[self.board.get_human_players()[0]][0]

            base_position = RIGHT_MENU_OFFSET

            pygame.draw.circle(self.right_display, player.color,
                               vector_floor(base_position), PLAYER_GRAPHIC_RADIUS)
            pygame.draw.circle(self.right_display, BLACK, vector_floor(base_position), HUMAN_MARKER_RADIUS)

            if player.get_name() == self.current_player:
                pygame.draw.circle(self.right_display, BLACK, vector_floor(base_position), PLAYER_GRAPHIC_RADIUS + 1, 2)

            base_text_position = vector_add(base_position, RIGHT_MENU_TEXT_OFFSET)
            name_text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_TEXT_SIZE),
                                                player.get_name(), True, BLACK)
            self.right_display.blit(name_text, vector_floor(base_text_position))

            base_position = vector_add(base_position, (0, RIGHT_MENU_MARGIN))
            base_text_position = vector_add(base_position, RIGHT_MENU_TEXT_OFFSET)
            text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_TEXT_SIZE),
                                           "$ {}".format(player.get_money()), True, BLACK)
            self.right_display.blit(text, vector_floor(base_text_position))

            for property in player.get_owned_properties():
                index = player.get_owned_properties().index(property)
                icon_pos = vector_add(base_position, (- RIGHT_MENU_ICON_SIZE[0] / 2,
                                                      RIGHT_MENU_MARGIN + index * RIGHT_MENU_PROP_MARGIN - RIGHT_MENU_ICON_SIZE[1] / 2))
                text_pos = vector_add(base_text_position, (0, RIGHT_MENU_MARGIN + index * RIGHT_MENU_PROP_MARGIN))

                button_pos = vector_add(text_pos, (0, RIGHT_MENU_BUTTON_MARGIN))

                if property.get_group() != "Railroad" and property.get_group() != "Utility":
                    button = self.prop_buttons[index]
                    button.position = button_pos
                    button.absolute_pos = vector_add((PYGAME_WINDOW_WIDTH - BOARD_CENTERED_X, 0), button.position)
                    self.right_display.blit(button.draw(), button_pos)

                rect = pygame.Surface(RIGHT_MENU_ICON_SIZE)
                rect.fill(PROPERTY_COLOR[property.get_group()])
                self.right_display.blit(rect, icon_pos)

                text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_SUBTEXT_SIZE),
                                               property.get_name(), True, BLACK)
                self.right_display.blit(text, text_pos)

    def draw_border(self):
        pygame.draw.line(self.menu_window, BLACK, (0, GUI_BORDER_WIDTH / 2 - 1),
                         (GUI_WINDOW_DIMENSIONS[0], GUI_BORDER_WIDTH / 2 - 1), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, 0),
                         (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, GUI_WINDOW_DIMENSIONS[1]), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0], GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2),
                         (0, GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_BORDER_WIDTH / 2 - 1, GUI_WINDOW_DIMENSIONS[1]),
                         (GUI_BORDER_WIDTH / 2 - 1, 0), GUI_BORDER_WIDTH)

        pygame.draw.line(self.left_display, BLACK, (self.left_display.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, 0),
                         (self.left_display.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, self.left_display.get_size()[1]), GUI_BORDER_WIDTH)

        pygame.draw.line(self.right_display, BLACK, (GUI_BORDER_WIDTH / 2 - 1, 0),
                         (GUI_BORDER_WIDTH / 2 - 1, self.right_display.get_size()[1]), GUI_BORDER_WIDTH)

    def set_card(self, content):
        self.card_content = content

    def unset_card(self):
        self.card_content = []

    def set_special_event(self, event):
        self.special_event_type = event

    def unset_special_event(self):
        self.special_event_type = None

    def set_dice_result(self, dice):
        self.dice_results = dice

    def set_property(self, prop):
        self.property_result = prop

    def set_card_result(self, result):
        self.card_result = result

    def clear_gui(self):
        del self.interactable[:]
        self.interactable = []
        del self.labels[:]
        self.labels = []


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
        self.absolute_pos = vector_add(GUI_WINDOW_POSITION, self.get_position())
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
        bottom_right_corner = vector_add(self.absolute_pos, self.rect.get_size())
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
        self.absolute_pos = vector_add(GUI_WINDOW_POSITION, self.get_position())
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
        bottom_right_corner = vector_add(self.absolute_pos, self.rect.get_size())
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
    def chance(value, board, gui, **kwargs):
        print("Chance {}".format(value))
        current_player = board.get_players()[gui.current_player][0]
        if value == 1:
            board.player_direct_move(current_player.get_name(), 0)
            board.next_turn_phase()
        elif value == 2:
            board.player_direct_move(current_player.get_name(),
                                     board.tileList.index(board.get_properties()["Illinois Ave"]))
            board.set_special_event(1)
        elif value == 3:
            board.player_direct_move(current_player.get_name(),
                                     board.tileList.index(board.get_properties()["St. Charles Place"]))

            board.set_special_event(1)
        elif value == 4:
            board.set_special_event(2)
        elif value == 5:
            board.set_special_event(3)
        elif value == 6:
            current_player.give_money(50)
            board.next_turn_phase()
        elif value == 7:
            current_player.give_jail_card()
            board.next_turn_phase()
        elif value == 8:
            board.player_standard_move(current_player.get_name, -3)
            board.next_turn_phase()
        elif value == 9:
            current_player.go_to_jail()
            board.player_direct_move(current_player.get_name(), 10, False)
            board.next_turn_phase()
        elif value == 10:
            hotels = 0
            houses = 0
            for property in current_player.get_owned_properties():
                hotels += property.get_num_hotels()
                houses += property.get_num_houses()
            houses -= hotels
            board.take_money(current_player.get_name(), 25 * houses + 100 * hotels)

        elif value == 11:
            board.take_money(current_player.get_name(), 15)
            board.next_turn_phase()
        elif value == 12:
            board.player_direct_move(current_player.get_name(),
                                     board.tileList.index(board.get_properties()["Reading Railroad"]))
            board.set_special_event(1)
        elif value == 13:
            board.player_direct_move(current_player.get_name(),
                                     board.tileList.index(board.get_properties()["Boardwalk"]))
            board.set_special_event(1)
        elif value == 14:
            for player in board.get_players():
                if player[0] is not current_player.get_name():
                    board.take_money_from_player(current_player.get_name(), 50)
                    player[0].give_money(50)
            board.next_turn_phase()
        elif value == 15:
            current_player.give_money(150)
            board.next_turn_phase()
        elif value == 16:
            current_player.give_money(100)
            board.next_turn_phase()
        gui.unset_card()
        return MENU_WAIT

    @staticmethod
    def community_chest(value, board, gui, **kwargs):
        print("Community Chest {}".format(value))
        current_player = board.get_players()[gui.current_player][0]
        if value == 1:
            board.player_direct_move(current_player.get_name(), 0)
            board.next_turn_phase()
        elif value == 2:
            current_player.give_money(200)
            board.next_turn_phase()
        elif value == 3:
            board.take_money(current_player.get_name(), 50)
            board.next_turn_phase()
        elif value == 4:
            current_player.give_money(50)
            board.next_turn_phase()
        elif value == 5:
            current_player.give_jail_card()
            board.next_turn_phase()
        elif value == 6:
            board.player_direct_move(current_player.get_name(), 10, False)
        elif value == 7:
            for player in board.get_players():
                if player[0] is not current_player.get_name():
                    board.take_money(player[0], 50)
                    current_player.give_money(50)
            board.next_turn_phase()
        elif value == 8:
            current_player.give_money(100)
            board.next_turn_phase()
        elif value == 9:
            current_player.give_money(20)
            board.next_turn_phase()
        elif value == 10:
            current_player.give_money(100)
            board.next_turn_phase()
        elif value == 11:
            board.take_money(current_player.get_name(), 50)
            board.next_turn_phase()
        elif value == 12:
            board.take_money(current_player.get_name(), 50)
            board.next_turn_phase()
        elif value == 13:
            current_player.give_money(25)
            board.next_turn_phase()
        elif value == 14:
            hotels = 0
            houses = 0
            for property in current_player.get_owned_properties():
                hotels += property.get_num_hotels()
                houses += property.get_num_houses()
            houses -= hotels
            board.take_money(current_player.get_name(), 40 * houses + 115 * hotels)
            board.next_turn_phase()
        elif value == 15:
            current_player.give_money(10)
            board.next_turn_phase()
        elif value == 16:
            current_player.give_money(100)
            board.next_turn_phase()
        gui.unset_card()
        return MENU_WAIT

    @staticmethod
    def build(value, board, gui, **kwargs):
        prop = board.get_properties()[value]
        if gui.current_player == prop.get_owner():
            owner = board.get_players()[gui.current_player][0]
            if owner.get_money() >= prop.get_house_cost():
                prop.add_house()
                owner.take_money(prop.get_house_cost())

    @staticmethod
    def end(board, **kwargs):
        board.progress_turn()
        return MENU_WAIT

    @staticmethod
    def color(value,board, gui, **kwargs):
        board.get_players()[gui.current_player][0].set_color(value)
        return MENU_OPP_SEL

    @staticmethod
    def roll(board, gui, mstate, **kwargs):
        rolls = board.roll_dice()
        gui.set_dice_result(rolls)
        if mstate == MENU_SE_DICE:
            return MENU_SE_RESULT
        else:
            return MENU_RESULT

    @staticmethod
    def confirm(value, mstate, board, gui, **kwargs):
        if mstate == MENU_START:
            board.start_game()
            board.next_turn_phase()
            return MENU_WAIT
        elif mstate == MENU_NAME:
            for inter in gui.interactable:
                if type(inter) is TextBox:
                    board.reset_players()
                    board.add_player(Player(inter.text_content, True))
                    break
            return MENU_COLOR
        elif mstate == MENU_OPP_SEL:
            for i in range(value):
                board.add_player(Player("CPU_{}".format(i + 1)))
            return MENU_START
        elif mstate == MENU_RESULT or mstate == MENU_AI_ROLL:
            board.player_standard_move(value[0], value[1][0] + value[1][1])
            board.next_turn_phase()
            return MENU_WAIT
        elif mstate == MENU_SE_RESULT:
            gui.set_special_event(10 * (value[1][0] + value[1][1]))
            return MENU_SE_PLR_RENT
        elif mstate == MENU_AI_BUY:
            board.next_turn_phase()
            return MENU_WAIT
        elif mstate == MENU_AI_RENT:
            board.next_turn_phase()
            return MENU_WAIT
        elif mstate == MENU_PLR_AI or mstate == MENU_SE_PLR_RENT:
            board.pay_rent(value[0], value[1], value[2])
            board.next_turn_phase()
            return MENU_WAIT
        elif mstate == MENU_DEBT:
            board.property_sale(gui.current_player, value)
            return MENU_WAIT
        elif mstate == MENU_BUY:
            if 'player' in kwargs and 'property' in kwargs:
                if value:
                    board.run_purchase(kwargs['player'], kwargs['property'].get_name())
                    board.next_turn_phase()
                else:
                    # board.startAuction(kwargs['property'].getName(), exclude=kwargs['player'])
                    board.next_turn_phase()
            else:
                raise AttributeError
            return MENU_WAIT

    @staticmethod
    def cancel(board, **kwargs):
        board.reset_players()
        return MENU_MAIN

    @staticmethod
    def page_right(gui, **kwargs):
        gui.page_number += 1
        return MENU_WAIT

    @staticmethod
    def page_left(gui, **kwargs):
        gui.page_number -= 1
        return MENU_WAIT

    @staticmethod
    def play(**kwargs):
        return MENU_NAME

    @staticmethod
    def quit(**kwargs):
        exit(0)