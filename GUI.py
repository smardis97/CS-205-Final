from constants import *
import pygame
import abc
from utility import *
import Tile
import math
from Player import *


class GUI:
    """
    The GUI class handles all user facing information and user interaction.

    Attributes:
        window              (PYGAME_WINDOW):    Reference to the main window object that everything is displayed on.
        board               (Board):            The Board contains most information about the state of the game.
        menu_state          (str):              Identifies what information should be displayed in
                                                    the main central menu.
        menu_window         (pygame.Surface):   A Surface that contains all the information and
                                                    main input buttons for the player.
        left_display        (pygame.Surface):   A Surface that contains information about the non-human players.
        right_display       (pygame.Surface):   A Surface that contains information about the human
                                                    player and their properties.
        board_background    (pygame.image):     Image of the monopoly board displayed on the background.
        page_number         (int):              Index use to display the player's properties when
                                                    they're choosing one to sell.
        interactable        ([MenuObject]):     The main list of Buttons and TextBoxes for user input.
        labels              ([MenuObject]):     List of Labels that display information to the player.
        prop_buttons        ([Button]):         List of Buttons displayed in right_display to allow
                                                    the player to build houses.
        card_content        ([str, ...]):       From CardTile, list of strings explaining the card.
        dice_results        ((int, int)):       Results of the last dice roll.
        property_result     (Property(Tile)):   Reference to the last property landed on by the current player.
        current_player      (str):              Name of the player whose currently taking their turn.
        special_event       (int):              Int representing the amount charged during special events.
    """
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
        self.special_event = None
        self.build_gui()

    def state_change(self, new_state):
        """
        Changes menu_state to change what the menu will display.

        Parameters:
            new_state   (str):  String describing the new state of the menu.
        """
        if new_state is not None:
            self.menu_state = new_state
            # rebuild the gui once the state has changed to change display
            self.build_gui()

    def build_gui(self):
        """
        Clears current display then adds objects to interactable and labels based on menu_state.
        """
        # clear existing gui
        self.clear_gui()

        # set variables for improved readability
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
                                            "Orange", ButtonOperands.color, BUTTON_COLOR, BUTTON_HIGHLIGHT, BRIGHT_ORANGE))

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
        # CPU SELL -------------------------------------------------------------------------------------------- CPU SELL
        #
        elif self.menu_state == MENU_AI_SELL:
            self.labels.append(Label((window_center_x, 40), BLACK, "{} Sold:".format(self.current_player)))

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
                                     BLACK, "$ {}".format(self.special_event)))

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
                                     BLACK, "$ {}".format(self.special_event)))

            self.interactable.append(Button((window_center_x, window_center_y + 2 * y_interval),
                                            "Pay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            (self.current_player, self.property_result.get_owner(),
                                             self.special_event)))
        #
        # PLAYER DEBT -------------------------------------------------------------------------------------- PLAYER DEBT
        #
        elif self.menu_state == MENU_DEBT:
            current_property = player.get_owned_properties()[self.page_number]
            sale_value = current_property.get_sale_value()
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
        # PLAYER OUT OF JAIL ------------------------------------------------------------------------ PLAYER OUT OF JAIL
        #
        elif self.menu_state == MENU_OUT:

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval), BLACK, "You got out of Jail."))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                            self.dice_results))
        #
        # PLAYER STUCK IN JAIL -------------------------------------------------------------------- PLAYER STUCK IN JAIL
        #
        elif self.menu_state == MENU_JAIL:

            self.labels.append(Label((window_center_x, window_center_y - 3 * y_interval),
                                     BLACK, "You are stuck in Jail."))

            self.interactable.append(Button((window_center_x, window_center_y + 4 * y_interval),
                                            "Okay", ButtonOperands.confirm, BUTTON_COLOR, BUTTON_HIGHLIGHT))
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
        """
        Receives key input events from main. Passes them to TextBoxes in interactable.

        Parameters:
            event       (pygame.event):     Pygame event of type KEYUP or KEYDOWN
        """
        for inter in self.interactable:
            if type(inter) == TextBox:
                inter.input(event)

    def mouse_update(self, mouse_event):
        """
        Receives updates on the position of the mouse within the game window. Passes position to Buttons on screen.

        Parameters:
            mouse_event (pygame.event):     Pygame event of type MOUESMOTION
        """
        for button in self.interactable:
            button.contains_mouse(mouse_event.__dict__['pos'])
        for button in self.prop_buttons:
            button.contains_mouse(mouse_event.__dict__['pos'])

    def mouse_click(self, mouse_event):
        """
        Receives mouse input events from main. Passes them to objects in interactable and prop_buttons.

        Every button/textbox is passed the same set of arguments:
            active:     Whether the mouse is hovering over the button/textbox. Determines which is being clicked on.
            mstate:     The current state of the game menu. Determines the action for certain buttons.
            player:     The name of the current active player.
            property:   The most recently landed property.
            board:      The main game board.
            gui:        The main game gui.

        To a certain extent this is probably bad practice, but I couldn't find a better way to go about it
            in the time available.

        Parameters:
            mouse_event (pygame.event):     Pygame event of type MOUSEBUTTONDOWN
        """
        # pass click to contents of interactable
        for inter in self.interactable:
            self.state_change(inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                                          mstate=self.menu_state,
                                          player=self.current_player,
                                          property=self.property_result,
                                          board=self.board,
                                          gui=self))

        # pass click to contents of prop_buttons
        for inter in self.prop_buttons:
            self.state_change(inter.click(active=inter.contains_mouse(mouse_event.__dict__['pos']),
                                          mstate=self.menu_state,
                                          player=self.current_player,
                                          property=self.property_result,
                                          board=self.board,
                                          gui=self))

    def draw_gui(self):
        """
        Draws background, menus, players, and board details to the main game window.
        """
        # draw the board background first so that everthing else is on top of it.
        self.window.screen.blit(self.board_background, (BOARD_CENTERED_X, 0))

        # draw tile details: ownership and houses
        self.draw_tile_details_on_board()

        self.draw_players()

        # menus have the same background color as the board.
        self.menu_window.fill(GUI_WINDOW_COLOR)

        self.left_display.fill(GUI_WINDOW_COLOR)
        self.draw_left_display()

        self.right_display.fill(GUI_WINDOW_COLOR)
        self.draw_right_display()

        # draw menu borders
        self.draw_border()

        # draw all labels onto the main menu window
        for label in self.labels:
            self.menu_window.blit(label.draw(), label.get_position())

        # draw all buttons and textboxes to the main menu window
        for inter in self.interactable:
            self.menu_window.blit(inter.draw(), inter.get_position())

        # draw menus onto the main game screen
        self.window.screen.blit(self.menu_window, GUI_WINDOW_POSITION)
        self.window.screen.blit(self.left_display, (0, 0))
        self.window.screen.blit(self.right_display, (PYGAME_WINDOW_WIDTH - BOARD_CENTERED_X, 0))

    def draw_players(self):
        """
        Draws players onto the board.

        Players are shown as circles of radius PLAYER_GRAPHIC_RADIUS. The currently active player has a black ring
            around them, and the human player has a black dot in the center.
        The onscreen coordinates of each square on the board are calculated and stored in the TILE_BOUNDS list.
        The index that each tile's coordinates are stored in TILE_BOUNDS is the same that it is found in Board's tile_list.
        The bounds at each index are stored as a pair of tuples with the (x, y) coordinates
            for the top-left and bottom-right coordinates of each square on the board.

        First, a list of 40 empty lists is created, then each player is added to the list corresponding to their
            position on the board, which is also the same as the index of the coordinates of their square in TILE_BOUNDS.

        Then we iterate through this list, and for each square we draw the players positioned there starting from
            a position that is offset from the top-left corner by (PLAYER_TILE_OFFSET, PLAYER_TILE_OFFSET).
        Players stack up horizontally in the square, shifting over by PLAYER_TILE_OFFSET, each time.
        In order to ensure that all players are displayed within the bounds of the square they are supposed to be in,
            players only stack up horizontally as many as could fit across the width of the square when positioned
            edge-to-edge. Subsequent players are moved back to the leftmost position and shifted
            down by PLAYER_TILE_OFFSET.
        """
        board_state = [[] for i in range(40)]

        # add players to their position in the board
        for player, data in self.board.get_players().items():
            board_state[data[1]].append(data[0])
        for i in range(40):
            # TILE_BOUNDS is a list of tuples of tuples formulated as:
            # [((top_left_x, top_left_y), (bottom_right_x, bottom_right_y)), ...]
            # bounds of the current square
            tile_corners = TILE_BOUNDS[i]

            # number of players that can fit across the width of the tile
            fit_across = math.floor((tile_corners[1][0] - tile_corners[0][0]) / PLAYER_GRAPHIC_DIAMETER)
            for player in board_state[i]:
                # which column the player will be displayed in, the modulus of fit_across and
                #   the player's index in board_state
                horizontal_pos = board_state[i].index(player) % fit_across

                # which row the player will be displayed in, the quotient of fit_across
                #   and the player's index in board_state
                vertical_pos = math.floor(board_state[i].index(player) / fit_across)

                # The position of the first player is
                #   (top_left_x, top_left_y) + (PLAYER_TILE_OFFSET, PLAYER_TILE_OFFSET)
                # Every subsequent player is offset from this position by
                # (horizontal_pos * PLAYER_TILE_OFFSET, vertical_pos * PLAYER_TILE_OFFSET)
                position = (tile_corners[0][0] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * horizontal_pos,
                            tile_corners[0][1] + PlAYER_TILE_OFFSET + PlAYER_TILE_OFFSET * vertical_pos)

                # draw the player to the screen at the calculated position
                pygame.draw.circle(self.window.screen, player.color, vector_floor(position), PLAYER_GRAPHIC_RADIUS)

                # draw a ring around the player if it is currently their turn
                if player.get_name() == self.current_player:
                    pygame.draw.circle(self.window.screen, BLACK, vector_floor(position), PLAYER_GRAPHIC_RADIUS + 1, 2)

                # draw a dot at the center of the human player
                if self.board.get_players()[player.get_name()][0].is_human:
                    pygame.draw.circle(self.window.screen, BLACK, vector_floor(position), HUMAN_MARKER_RADIUS)

    def draw_tile_details_on_board(self):
        """
        Draws tile ownership and number of houses onto each property.

        Ownership is represented by a small circle matching the color of the player who owns the tile in the bottom
            right-hand corner of the square.
        Number of houses/hotels is shown by a square in the bottom-left corner of the square.
        Houses are shown as a green square with a number 1-3 representing the number of houses.
        Hotels are shown as a red square with no number.
        """
        # iterate through every property on the board.
        for name, details in self.board.get_properties().items():

            # the onscreen position of each property is stored in the element of TILE_BOUNDS corresponding to its
            #   order of appearance on the board.
            tile_position = TILE_BOUNDS[self.board.get_tiles().index(details)]

            # only draw details for owned tiles
            if details.get_owner() is not None:
                # set variables for improved readability
                owner = self.board.get_players()[details.get_owner()][0]

                # OWNER_MARKER_POSITION is the amount of offset from the bottom-right corner where the
                #   owner marker appears.
                # The marker is drawn in the owner's color
                pygame.draw.circle(self.window.screen, owner.color,
                                   vector_floor(vector_add(tile_position[1], OWNER_MARKER_POSITION)),
                                   OWNER_MARKER_RADIUS)

                # if the property contains a hotel then a red square is drawn
                if details.get_num_hotels() > 0:
                    rect = pygame.Surface(HOUSE_MARKER_DIMENSIONS)
                    rect.fill(RED)
                    self.window.screen.blit(rect, vector_floor(vector_add((tile_position[0][0], tile_position[1][1]),
                                                                          HOUSE_MARKER_POSITION)))

                # if the property contains any houses then a green square and number are drawn
                elif details.get_num_houses() > 0:
                    rect = pygame.Surface(HOUSE_MARKER_DIMENSIONS)
                    rect.fill(GREEN)
                    num = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), HOUSE_MARKER_TEXT_SIZE),
                                                  str(details.get_num_houses()), True, BLACK)

                    # draw the number onto the square, before drawing the square to the screen
                    rect.blit(num, HOUSE_MARKER_TEXT_OFFSET)
                    self.window.screen.blit(rect, vector_floor(vector_add((tile_position[0][0], tile_position[1][1]),
                                                                    HOUSE_MARKER_POSITION)))

    def draw_left_display(self):
        """
        Draws the content of the display to the left of the game board.

        The left display contains information about the non-human players.
        A circle of their color so you can tell which is which and who owns what.
        A ring around the player currently taking their turn.
        How much money they have.
        Whether they are in jail and how many turns of being in jail the have left.

        The first player is drawn at the position LEFT_MENU_OFFSET from the top-left corner.
        Every player after that is separated vertically by LEFT_MENU_SEPARATION from the player before it.
        Text about each player is offset from the circle representing that player by LEFT_MENU_TEXT_OFFSET
            which is intended to shift the text horizontally and line if up vertically with the circle.
        Data pertaining to the same player is separated from the line above it by LEFT_MENU_MARGIN.
        """
        # iterate through all players
        for name, cpu in self.board.get_players().items():
            # only draw non-human players
            if not cpu[0].is_human:
                # set to the position of the colored circle
                position = (LEFT_MENU_OFFSET[0],
                            LEFT_MENU_OFFSET[1] + LEFT_MENU_SEPARATION * (self.board.turn_order.index(name) - 1))
                pygame.draw.circle(self.left_display, cpu[0].color, vector_floor(position), PLAYER_GRAPHIC_RADIUS)

                # draw a black ring if the player is taking their turn
                if cpu[0].get_name() == self.current_player:
                    pygame.draw.circle(self.left_display, BLACK, vector_floor(position), PLAYER_GRAPHIC_RADIUS + 1, 2)

                # set to the position of the first line of text
                position = (position[0] + LEFT_MENU_TEXT_OFFSET[0],
                            position[1] + LEFT_MENU_TEXT_OFFSET[1])

                # text showing the player's name
                name_text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_TEXT_SIZE),
                                                    cpu[0].get_name(), True, BLACK)
                self.left_display.blit(name_text, vector_floor(position))

                # set to the position of the second line of text
                position = (position[0], position[1] + LEFT_MENU_MARGIN)

                # text showing how much money the player has
                text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_SUBTEXT_SIZE),
                                               "$ {}".format(cpu[0].get_money()), True, BLACK)
                self.left_display.blit(text, vector_floor(position))

                # show an additional line of text if the player is in jail
                if cpu[0].is_in_jail():
                    # set to the position of the third line of text
                    position = (position[0], position[1] + LEFT_MENU_MARGIN)

                    # text showing that the player is in jail and how many turns they have left
                    text = pygame.font.Font.render(
                        pygame.font.Font(pygame.font.get_default_font(), LEFT_MENU_SUBTEXT_SIZE),
                        "IN JAIL {}".format(cpu[0].jail_counter), True, RED)
                    self.left_display.blit(text, vector_floor(position))

    def draw_right_display(self):
        """
        Draws the content of the display to the right of the game board.

        The right display contains information about the human player and their properties. It also has buttons that
            allow the player to build houses on their properties.
        A circle of the same color as the player with the black dot marking them as the human controlled player.
        If it is currently the player's turn, a black ring is drawn as well.
        The player's name as it appears in menu messages.
        How much money they have.
        A list of the player's owned properties with an icon matching the color of the group each property belongs to.

        The colored circle is drawn offset from the top left corner of the display by RIGHT_MENU_OFFSET.
        The player's name is drawn offset from the colored circle's position by RIGHT_MENU_TEXT_OFFSET.
        The player's bank balance is draw offset vertically from the player's name by RIGHT_MENU_MARGIN.

        Each property icon is a colored square of size RIGHT_MENU_ICON_SIZE offset from the property above
            by RIGHT_MENU_PROP_MARGIN.
        The name of each property is drawn offset from the matching icon by half the icon's size.
        For properties that can contain houses (all except Railroads and Utilities), a button is offset vertically
            from the property name by RIGHT_MENU_BUTTON_MARGIN.
        """
        if len(self.board.get_human_players()) > 0:
            # set variable for readability
            player = self.board.get_players()[self.board.get_human_players()[0]][0]

            # start position for the player icon
            base_position = RIGHT_MENU_OFFSET

            pygame.draw.circle(self.right_display, player.color,
                               vector_floor(base_position), PLAYER_GRAPHIC_RADIUS)
            pygame.draw.circle(self.right_display, BLACK, vector_floor(base_position), HUMAN_MARKER_RADIUS)

            # draw an additional ring if it is the player's turn
            if player.get_name() == self.current_player:
                pygame.draw.circle(self.right_display, BLACK, vector_floor(base_position), PLAYER_GRAPHIC_RADIUS + 1, 2)

            # position of the player's name text
            base_text_position = vector_add(base_position, RIGHT_MENU_TEXT_OFFSET)
            name_text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_TEXT_SIZE),
                                                player.get_name(), True, BLACK)
            self.right_display.blit(name_text, vector_floor(base_text_position))

            # adjust positions vertically by RIGHT_MENU_MARGIN
            base_position = vector_add(base_position, (0, RIGHT_MENU_MARGIN))
            base_text_position = vector_add(base_position, RIGHT_MENU_TEXT_OFFSET)
            text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_TEXT_SIZE),
                                           "$ {}".format(player.get_money()), True, BLACK)
            self.right_display.blit(text, vector_floor(base_text_position))

            for property in player.get_owned_properties():
                # each listing is positioned by icon * RIGHT_MENU_PROP_MARGIN
                index = player.get_owned_properties().index(property)

                # relative positions for each element of the list
                icon_pos = vector_add(base_position, (- RIGHT_MENU_ICON_SIZE[0] / 2,
                                                      RIGHT_MENU_MARGIN + index * RIGHT_MENU_PROP_MARGIN - RIGHT_MENU_ICON_SIZE[1] / 2))
                text_pos = vector_add(base_text_position, (0, RIGHT_MENU_MARGIN + index * RIGHT_MENU_PROP_MARGIN))

                button_pos = vector_add(text_pos, (0, RIGHT_MENU_BUTTON_MARGIN))

                # draw buttons for buildable properties
                if property.get_group() != "Railroad" and property.get_group() != "Utility":
                    button = self.prop_buttons[index]
                    button.position = button_pos
                    button.absolute_pos = vector_add((PYGAME_WINDOW_WIDTH - BOARD_CENTERED_X, 0), button.position)
                    self.right_display.blit(button.draw(), button_pos)

                # drawing the icon and text
                rect = pygame.Surface(RIGHT_MENU_ICON_SIZE)
                rect.fill(PROPERTY_COLOR[property.get_group()])
                self.right_display.blit(rect, icon_pos)

                text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), RIGHT_MENU_SUBTEXT_SIZE),
                                               property.get_name(), True, BLACK)
                self.right_display.blit(text, text_pos)

    def draw_border(self):
        """
        Draw borders for the menus.
        """
        # draw border around the main central menu
        pygame.draw.line(self.menu_window, BLACK, (0, GUI_BORDER_WIDTH / 2 - 1),
                         (GUI_WINDOW_DIMENSIONS[0], GUI_BORDER_WIDTH / 2 - 1), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, 0),
                         (GUI_WINDOW_DIMENSIONS[0] - GUI_BORDER_WIDTH / 2, GUI_WINDOW_DIMENSIONS[1]), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_WINDOW_DIMENSIONS[0], GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2),
                         (0, GUI_WINDOW_DIMENSIONS[1] - GUI_BORDER_WIDTH / 2), GUI_BORDER_WIDTH)
        pygame.draw.line(self.menu_window, BLACK, (GUI_BORDER_WIDTH / 2 - 1, GUI_WINDOW_DIMENSIONS[1]),
                         (GUI_BORDER_WIDTH / 2 - 1, 0), GUI_BORDER_WIDTH)

        # draw borders on the outside of the game board
        pygame.draw.line(self.left_display, BLACK, (self.left_display.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, 0),
                         (self.left_display.get_size()[0] - GUI_BORDER_WIDTH / 2 - 1, self.left_display.get_size()[1]), GUI_BORDER_WIDTH)

        pygame.draw.line(self.right_display, BLACK, (GUI_BORDER_WIDTH / 2 - 1, 0),
                         (GUI_BORDER_WIDTH / 2 - 1, self.right_display.get_size()[1]), GUI_BORDER_WIDTH)

    def set_card(self, content):
        """
        Setter for card_content.

        Parameters:
            content     ((int, [str, ...])):    Tuple of int and a list of strings returned from CardTile.pick_card()
        """
        self.card_content = content

    def unset_card(self):
        """
        Clears contents of card_content.
        """
        self.card_content = []

    def set_special_event(self, event):
        """
        Sets value of special_event

        Parameters:
            event       (int):                  The nonstandard value to be charged during a special event.
        """
        self.special_event = event

    def set_dice_result(self, dice):
        """
        Sets the value of dice_results.

        Parameters:
            dice        ((int, int)):           Pair of ints representing the value rolled on each die.
        """
        self.dice_results = dice

    def set_property(self, prop):
        """
        Sets the value of property_result.

        Parameters:
            prop        (Property(Tile)):       The last property that the current player landed on.
        """
        self.property_result = prop

    def clear_gui(self):
        """
        Clears interactable and labels in preparation to rebuild the gui.
        """
        del self.interactable[:]
        self.interactable = []
        del self.labels[:]
        self.labels = []

########################################################################################################################
#**********************************************************************************************************************#
#                                                                                                                      #
# MenuObject ============================================================================================== MenuObject #
#                                                                                                                      #
#**********************************************************************************************************************#
########################################################################################################################
class MenuObject:
    """
    The MenuObject class is an abstract class extended by all of the objects that interact with the player through
        the menus.

    Attributes:
        position    ((int, int)):       Describes the position of the >>CENTER<< of the object relative to the
                                            top-left corner of the menu it's drawn on.
        color       ((int, int, int)):  The color of the object.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, position, color):
        self.position = position
        self.color = color

    @abc.abstractmethod
    def get_position(self):
        """
        Getter for the position of the top-left corner of the object.

        Returns:
            (int, int): Position of the top-left corner of the object.
        """
        return NotImplemented

    @abc.abstractmethod
    def draw(self):
        """
        Returns a Pygame Surface of the entire content of the object to be drawn onto another surface.

        Returns:
            pygame.Surface: The complete graphical depiction of the object including additional text to display.
        """
        return NotImplemented

    @abc.abstractmethod
    def contains_mouse(self, mouse_pos):
        """
        Checks whether the mouse is contained in the bounds of this object.

        Parameters:
            mouse_pos   ((int, int)):   Absolute position of the mouse relative to the main game window.

        Returns:
            bool: Whether the give mouse position intersects with this objects position on screen.
        """
        return NotImplemented

    @abc.abstractmethod
    def click(self, active=False, **kwargs):
        """
        Called to activate the onclick functionality of this MenuObject.

        Parameters:
            active      (bool):             Whether this object has actually been clicked on.
                                                Usually a call to self.contains_mouse
            **kwargs    ({key: arg, ...}):  A set of keyword arguments to pass on to this object's specified
                                                onclick function, if it exists.
        """
        return NotImplemented

########################################################################################################################
#**********************************************************************************************************************#
#                                                                                                                      #
# Button ====================================================================================================== Button #
#                                                                                                                      #
#**********************************************************************************************************************#
########################################################################################################################
class Button(MenuObject):
    """
    The Button class is an subclass of MenuObject that is used to create clickable buttons in menus.

    Attributes:
        absolute_pos    ((int, int)):           The position of the Button relative to the top-left
                                                    corner of the main game window.
        rect            (pygame.Surface):       The main graphical representation of the button.
        text            (pygame.Surface):       The text written on the Button.
        highlight       ((int, int, int)):      The color drawn on the button when the mouse is hovering over it.
        action          (function):             Callable function that is called when the button is clicked.
        value           (type varies):          Additional values that are passed to the action function.
        hover           (bool):                 Whether the mouse is hovering over this button.
    """
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

    def get_position(self):
        """
        Getter for the position of the top-left corner of the object.

        Returns:
            (int, int): Position of the top-left corner of the object.
        """
        return self.position[0] - (BUTTON_DIMENSIONS[0] / 2), \
               self.position[1] - (BUTTON_DIMENSIONS[1] / 2)

    def draw(self):
        """
        Returns a Pygame Surface of the entire content of the object to be drawn onto another surface.

        Returns:
            pygame.Surface: The complete graphical depiction of the object including additional text to display.
        """
        color = self.color if not self.hover else self.highlight
        self.rect.fill(color)

        # draw text onto rect before returning rect to be drawn
        self.rect.blit(self.text, self.text_offset())
        return self.rect

    def contains_mouse(self, mouse_pos):
        """
        Checks whether the mouse is contained in the bounds of this object.

        Parameters:
            mouse_pos   ((int, int)):   Absolute position of the mouse relative to the main game window.

        Returns:
            bool: Whether the give mouse position intersects with this objects position on screen.
        """
        top_left_corner = self.absolute_pos
        bottom_right_corner = vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        """
        Called to activate the onclick functionality of this MenuObject.

        Parameters:
            active      (bool):             Whether this object has actually been clicked on.
                                                Usually a call to self.contains_mouse
            **kwargs    ({key: arg, ...}):  A set of keyword arguments to pass on to this object's specified
                                                onclick function, if it exists.
        """
        if active:
            return self.action(value=self.value, **kwargs)

    def text_offset(self):
        """
        Returns the position of the top-left corner of the text relative to the center of the object.

        Returns:
            (int, int): Coordinates relative to center of object.
        """
        x_offset = (self.rect.get_size()[0] / 2) - (self.text.get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.text.get_size()[1] / 2)
        return x_offset, y_offset

########################################################################################################################
#**********************************************************************************************************************#
#                                                                                                                      #
# Label ======================================================================================================== Label #
#                                                                                                                      #
#**********************************************************************************************************************#
########################################################################################################################
class Label(MenuObject):
    def __init__(self, position, color, text):
        MenuObject.__init__(self, position, color)
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), MENU_LABEL_SIZE),
                                            text, True, self.color)

    def get_position(self):
        """
        Getter for the position of the top-left corner of the object.

        Returns:
            (int, int): Position of the top-left corner of the object.
        """
        return self.position[0] - (self.text.get_size()[0] / 2), self.position[1] - (self.text.get_size()[1] / 2)

    def draw(self):
        """
        Returns a Pygame Surface of the entire content of the object to be drawn onto another surface.

        Returns:
            pygame.Surface: The complete graphical depiction of the object including additional text to display.
        """
        return self.text

    def contains_mouse(self, mouse_pos):
        """
        Checks whether the mouse is contained in the bounds of this object.

        Parameters:
            mouse_pos   ((int, int)):   Absolute position of the mouse relative to the main game window.

        Returns:
            bool: Whether the give mouse position intersects with this objects position on screen.
        """
        return False

    def click(self, active=False, **kwargs):
        """
        Called to activate the onclick functionality of this MenuObject.

        Parameters:
            active      (bool):             Whether this object has actually been clicked on.
                                                Usually a call to self.contains_mouse
            **kwargs    ({key: arg, ...}):  A set of keyword arguments to pass on to this object's specified
                                                onclick function, if it exists.
        """
        pass

########################################################################################################################
#**********************************************************************************************************************#
#                                                                                                                      #
# TextBox ==================================================================================================== TextBox #
#                                                                                                                      #
#**********************************************************************************************************************#
########################################################################################################################
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

    def get_position(self):
        """
        Getter for the position of the top-left corner of the object.

        Returns:
            (int, int): Position of the top-left corner of the object.
        """
        return self.position[0] - (TEXT_BOX_DIMENSIONS[0] / 2), \
               self.position[1] - (TEXT_BOX_DIMENSIONS[1] / 2)

    def draw(self):
        """
        Returns a Pygame Surface of the entire content of the object to be drawn onto another surface.

        Returns:
            pygame.Surface: The complete graphical depiction of the object including additional text to display.
        """
        self.rect.fill(self.get_color())
        self.rect.blit(self.get_text(), self.text_offset())
        return self.rect

    def contains_mouse(self, mouse_pos):
        """
        Checks whether the mouse is contained in the bounds of this object.

        Parameters:
            mouse_pos   ((int, int)):   Absolute position of the mouse relative to the main game window.

        Returns:
            bool: Whether the give mouse position intersects with this objects position on screen.
        """
        top_left_corner = self.absolute_pos
        bottom_right_corner = vector_add(self.absolute_pos, self.rect.get_size())
        x_contains = top_left_corner[0] <= mouse_pos[0] <= bottom_right_corner[0]
        y_contains = top_left_corner[1] <= mouse_pos[1] <= bottom_right_corner[1]
        self.hover = x_contains and y_contains
        return self.hover

    def click(self, active=False, **kwargs):
        """
        Called to activate the onclick functionality of this MenuObject.

        Parameters:
            active      (bool):             Whether this object has actually been clicked on.
                                                Usually a call to self.contains_mouse
            **kwargs    ({key: arg, ...}):  A set of keyword arguments to pass on to this object's specified
                                                onclick function, if it exists.
        """
        self.active = active

    def text_offset(self):
        """
        Returns the position of the top-left corner of the text relative to the center of the object.

        Returns:
            (int, int): Coordinates relative to center of object.
        """
        x_offset = (self.rect.get_size()[0] / 2) - (self.get_text().get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.get_text().get_size()[1] / 2)
        return x_offset, y_offset

    def input(self, key_event):
        """
        Takes key input to add characters to text_content.

        Parameters:
            key_event (pygame.event): An incoming KEYUP or KEYDOWN event.
        """
        if key_event.type == pygame.KEYDOWN:
            if key_event.__dict__['key'] == 8:  # backspace
                if len(self.text_content) > 0:
                    self.text_content = self.text_content[:-1]
            elif 'unicode' in key_event.__dict__:
                if self.active:
                    self.text_content += key_event.__dict__['unicode']

    def get_color(self):
        """
        Returns a color based on the current state of the TextBox.

        Returns:
            (int, int, int): Color
        """
        if self.active:
            color = self.active_color
        elif self.hover:
            color = self.highlight
        else:
            color = self.color
        return color

    def get_text(self):
        """
        Returns a Pygame Surface of the text_content to draw to the screen.

        Returns:
            pygame.Surface: The text_content rendered to a Surface to be drawn.
        """
        return pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), TEXT_BOX_TEXT_SIZE),
                                       self.text_content, True, TEXT_BOX_TEXT_COLOR)







########################################################################################################################
#**********************************************************************************************************************#
#                                                                                                                      #
# DiceGraphic ============================================================================================ DiceGraphic #
#                                                                                                                      #
#**********************************************************************************************************************#
########################################################################################################################
class DiceGraphic(MenuObject):
    """
    The DiceGraphic class is shows the face of a die with the parameter value to display on the menu.

    Attributes:
        rect        (pygame.Surface):       The square die background.
        value       (int):                  The value displayed on the die.
        text        (pygame.Surface):       A Surface containing text of the dice value.
    """
    def __init__(self, position, value):
        MenuObject.__init__(self, position, DICE_GRAPHIC_COLOR)
        self.rect = pygame.Surface(DICE_GRAPHIC_DIMENSIONS)
        self.value = value
        self.text = pygame.font.Font.render(pygame.font.Font(pygame.font.get_default_font(), DICE_TEXT_SIZE),
                                            str(self.value), True, DICE_TEXT_COLOR)

    def get_position(self):
        """
        Getter for the position of the top-left corner of the object.

        Returns:
            (int, int): Position of the top-left corner of the object.
        """
        return self.position[0] - (self.rect.get_size()[0] / 2), self.position[1] - (self.rect.get_size()[1] / 2)

    def draw(self):
        """
        Returns a Pygame Surface of the entire content of the object to be drawn onto another surface.

        Returns:
            pygame.Surface: The complete graphical depiction of the object including additional text to display.
        """
        self.rect.fill(self.color)
        self.rect.blit(self.text, self.text_offset())
        return self.rect

    def contains_mouse(self, mouse_pos):
        """
        Checks whether the mouse is contained in the bounds of this object.

        Parameters:
            mouse_pos   ((int, int)):   Absolute position of the mouse relative to the main game window.

        Returns:
            bool: Whether the give mouse position intersects with this objects position on screen.
        """
        return False

    def click(self, active=False, **kwargs):
        """
        Called to activate the onclick functionality of this MenuObject.

        Parameters:
            active      (bool):             Whether this object has actually been clicked on.
                                                Usually a call to self.contains_mouse
            **kwargs    ({key: arg, ...}):  A set of keyword arguments to pass on to this object's specified
                                                onclick function, if it exists.
        """
        pass

    def text_offset(self):
        """
        Returns the position of the top-left corner of the text relative to the center of the object.

        Returns:
            (int, int): Coordinates relative to center of object.
        """
        x_offset = (self.rect.get_size()[0] / 2) - (self.text.get_size()[0] / 2)
        y_offset = (self.rect.get_size()[1] / 2) - (self.text.get_size()[1] / 2)
        return x_offset, y_offset


class ButtonOperands:
    """
    ButtonOperands contains all the static methods called by Buttons.
    """

    @staticmethod
    def chance(value, board, gui, **kwargs):
        """
        Runs operations for all Chance cards


        Parameters:
            value       (int):                  Integer representing which card was pulled.
            board       (Board.Board):          Reference to the game board.
            gui         (GUI):                  Reference to the game GUI.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        # set variable for readability
        current_player = board.get_players()[gui.current_player][0]

        # Advance to Go
        if value == 1:
            board.player_direct_move(current_player.get_name(), 0)
            board.next_turn_phase()

        # Advance to Illinois Ave.
        elif value == 2:
            board.player_direct_move(current_player.get_name(),
                                     board.tile_list.index(board.get_properties()["Illinois Avenue"]))
            board.set_special_event(1)

        # Advance to St. Charles Place
        elif value == 3:
            board.player_direct_move(current_player.get_name(),
                                     board.tile_list.index(board.get_properties()["St. Charles Place"]))
            board.set_special_event(1)

        # Advance to nearest Utility. If unowned, you may buy it from the Bank.
        # If owned throw dice and pay owner a total ten times the amount thrown.
        elif value == 4:
            board.set_special_event(2)

        # Advance to nearest Railroad. If unowned, you may buy it from the Bank.
        # If owned pay the owner twice the usual rent.
        elif value == 5:
            board.set_special_event(3)

        # Bank pays you a dividend of $50
        elif value == 6:
            current_player.give_money(50)
            board.next_turn_phase()

        # Get out of Jail free.
        elif value == 7:
            current_player.add_jail_card()
            board.next_turn_phase()

        # Go back three spaces.
        elif value == 8:
            board.player_standard_move(current_player.get_name(), -3)
            board.next_turn_phase()

        # Go to Jail.
        elif value == 9:
            current_player.go_to_jail()
            board.player_direct_move(current_player.get_name(), 10, False)
            board.next_turn_phase()

        # Make general repairs on all your properties, pay $25 for each house, and $ 100 for each hotel.
        elif value == 10:
            hotels = 0
            houses = 0
            for property in current_player.get_owned_properties():
                hotels += property.get_num_hotels()
                houses += property.get_num_houses()
            board.take_money_from_player(current_player.get_name(), 25 * houses + 100 * hotels)
            board.next_turn_phase()

        # Pay poor tax, $15.
        elif value == 11:
            board.take_money_from_player(current_player.get_name(), 15)
            board.next_turn_phase()

        # Advance to Reading Railroad.
        elif value == 12:
            board.player_direct_move(current_player.get_name(),
                                     board.tile_list.index(board.get_properties()["Reading Railroad"]))
            board.set_special_event(1)

        # Advance to Boardwalk
        elif value == 13:
            board.player_direct_move(current_player.get_name(),
                                     board.tile_list.index(board.get_properties()["Boardwalk"]))
            board.set_special_event(1)

        # You have been have been elected Chairman of the Board. Pay each player $50.
        elif value == 14:
            for player in board.get_players():
                if player[0] is not current_player.get_name():
                    board.take_money_from_player(current_player.get_name(), 50)
                    player[0][0].give_money(50)
            board.next_turn_phase()

        # Your building and loan matures. Collect $150.
        elif value == 15:
            current_player.give_money(150)
            board.next_turn_phase()

        # You have won a crossword competition, collect $100.
        elif value == 16:
            current_player.give_money(100)
            board.next_turn_phase()
        gui.unset_card()
        return MENU_WAIT

    @staticmethod
    def community_chest(value, board, gui, **kwargs):
        """
        Runs operations for all Community Chest cards


        Parameters:
            value       (int):                  Integer representing which card was pulled.
            board       (Board.Board):          Reference to the game board.
            gui         (GUI):                  Reference to the game GUI.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        # set variable for readability
        current_player = board.get_players()[gui.current_player][0]

        # Advance to Go.
        if value == 1:
            board.player_direct_move(current_player.get_name(), 0)
            board.next_turn_phase()

        # Bank error in your favor. Collect $200.
        elif value == 2:
            current_player.give_money(200)
            board.next_turn_phase()

        # Doctor's fee, pay $50.
        elif value == 3:
            board.take_money_from_player(current_player.get_name(), 50)
            board.next_turn_phase()

        # From sale of stock you get $50.
        elif value == 4:
            current_player.give_money(50)
            board.next_turn_phase()

        # Get out of Jail free.
        elif value == 5:
            current_player.add_jail_card()
            board.next_turn_phase()

        # Go to Jail.
        elif value == 6:
            board.player_direct_move(current_player.get_name(), 10, False)
            board.next_turn_phase()

        # Grand Opera Night. Collect $50 from every player for opening night seats.
        elif value == 7:
            for player in board.get_players():
                if player is not current_player.get_name():
                    board.take_money_from_player(player, 50)
                    current_player.give_money(50)
            board.next_turn_phase()

        # Holiday fund matures receive $100.
        elif value == 8:
            current_player.give_money(100)
            board.next_turn_phase()

        # Income tax refund. Collect $20
        elif value == 9:
            current_player.give_money(20)
            board.next_turn_phase()

        # Life insurance matures. Collect $100.
        elif value == 10:
            current_player.give_money(100)
            board.next_turn_phase()

        # Hospital fees. Pay $50.
        elif value == 11:
            board.take_money_from_player(current_player.get_name(), 50)
            board.next_turn_phase()

        # School fees. Pay $50.
        elif value == 12:
            board.take_money_from_player(current_player.get_name(), 50)
            board.next_turn_phase()

        # Receive $25 consultancy fee.
        elif value == 13:
            current_player.give_money(25)
            board.next_turn_phase()

        # You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.
        elif value == 14:
            hotels = 0
            houses = 0
            for property in current_player.get_owned_properties():
                hotels += property.get_num_hotels()
                houses += property.get_num_houses()
            board.take_money_from_player(current_player.get_name(), 40 * houses + 115 * hotels)
            board.next_turn_phase()

        # You have won second prize in a beauty contest. Collect $10.
        elif value == 15:
            current_player.give_money(10)
            board.next_turn_phase()

        # You inherit $100.
        elif value == 16:
            current_player.give_money(100)
            board.next_turn_phase()
        gui.unset_card()
        return MENU_WAIT

    @staticmethod
    def build(value, board, gui, **kwargs):
        """
        Builds a house on the specified property if it is the owner's turn and they have enough money.

        Parameters:
            value       (int):                  The index of the property being built on.
            board       (Board.Board):          A reference to the game board.
            gui         (GUI):                  A reference to the game GUI
            **kwargs    ({key: arg, ...}):      Additional arguments passed to button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        prop = board.get_properties()[value]
        if gui.current_player == prop.get_owner():
            owner = board.get_players()[gui.current_player][0]
            if owner.get_money() >= prop.get_house_cost():
                prop.add_house()
                owner.take_money(prop.get_house_cost())

    @staticmethod
    def end(board, **kwargs):
        """
        Ends the current player's turn.

        Parameters:
            board       (Board.Board):          A reference to the game board.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        board.progress_turn()
        return MENU_WAIT

    @staticmethod
    def color(value, board, gui, **kwargs):
        """
        Assigns a color to the human player

        Parameters:
            value       ((int, int, int)):      The RGB values of the selected color.
            board       (Board.Board):          A reference to the game board.
            gui         (GUI):                  A reference to the game GUI
            **kwargs    ({key: arg, ...}):      Additional arguments passed to button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        board.get_players()[gui.current_player][0].set_color(value)
        return MENU_OPP_SEL

    @staticmethod
    def roll(board, gui, mstate, **kwargs):
        """
        Rolls dice and sets the result in the gui.

        Parameters:
            board       (Board.Board):          A reference to the game board.
            gui         (GUI):                  A reference to the game GUI
            mstate      (str):                  The current state of the gui.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        rolls = board.roll_dice()
        gui.set_dice_result(rolls)
        if mstate == MENU_SE_DICE:
            return MENU_SE_RESULT
        else:
            return MENU_RESULT

    @staticmethod
    def confirm(value, mstate, board, gui, **kwargs):
        """
        Acknowledges the presented information and progresses to the next state, passing along any values.


        Parameters:
            value       (varies):               Information relevant to the current state of the gui.
            mstate      (str):                  The current state of the gui.
            board       (Board.Board):          Reference to the game board.
            gui         (GUI):                  Reference to the game GUI.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        #
        # From Start Menu ------------------------------------------------------------------------------ From Start Menu
        #
        if mstate == MENU_START:
            board.start_game()
            board.next_turn_phase()
            return MENU_WAIT

        #
        # From Name Menu -------------------------------------------------------------------------------- From Name Menu
        #
        elif mstate == MENU_NAME:
            for inter in gui.interactable:
                if type(inter) is TextBox:
                    board.reset_players()
                    board.add_player(Player(inter.text_content, True))
                    break
            return MENU_COLOR

        #
        # From Opponent Select Menu ---------------------------------------------------------- From Opponent Select Menu
        #
        elif mstate == MENU_OPP_SEL:
            for i in range(value):
                board.add_player(Player("CPU_{}".format(i + 1)))
            return MENU_START

        #
        # From Dice Result ---------------------------------------------------------------------------- From Dice Result
        #
        elif mstate == MENU_RESULT or mstate == MENU_AI_ROLL:
            # set variable for readability
            player = board.players[value[0]][0]
            if player.is_in_jail():
                # if the player rolled a pair OR has a get-out-of-jail-free card
                if value[1][0] == value[1][1] or player.get_jail_card():
                    player.get_out_of_jail()
                    if player.is_human:
                        return MENU_OUT
                    else:
                        board.player_standard_move(player.get_name(), value[1][0] + value[1][1])
                        board.next_turn_phase()
                        return MENU_WAIT
                else:
                    # counts down to automatic release
                    player.jail_count_down()
                    if player.is_human:
                        if player.is_in_jail():
                            return MENU_JAIL
                        else:
                            return MENU_OUT
                    else:
                        board.next_turn_phase()
                        return MENU_WAIT
            else:
                board.player_standard_move(player.get_name(), value[1][0] + value[1][1])
                board.next_turn_phase()
                return MENU_WAIT

        #
        # From Special Event Result ---------------------------------------------------------- From Special Event Result
        #
        elif mstate == MENU_SE_RESULT:
            gui.set_special_event(10 * (value[1][0] + value[1][1]))
            return MENU_SE_PLR_RENT

        #
        # From AI Purchase Menu ------------------------------------------------------------------ From AI Purchase Menu
        #
        elif mstate == MENU_AI_BUY:
            board.next_turn_phase()
            return MENU_WAIT

        #
        # From AI Rent Result ---------------------------------------------------------------------- From AI Rent Result
        #
        elif mstate == MENU_AI_RENT or mstate == MENU_SE_AI_RENT:
            board.next_turn_phase()
            return MENU_WAIT

        #
        # From Player Rent Result -------------------------------------------------------------- From Player Rent Result
        #
        elif mstate == MENU_PLR_AI or mstate == MENU_SE_PLR_RENT:
            board.pay_rent(value[0], value[1], value[2])
            board.next_turn_phase()
            return MENU_WAIT

        #
        # From Player Debt ---------------------------------------------------------------------------- From Player Debt
        #
        elif mstate == MENU_DEBT:
            board.property_sale(gui.current_player, value)
            return MENU_WAIT

        #
        # From Player Purchase -------------------------------------------------------------------- From Player Purchase
        #
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

        #
        # From In Jail or Jail Escape ------------------------------------------------------ From In Jail or Jail Escape
        #
        elif mstate == MENU_JAIL or mstate == MENU_OUT:
            board.next_turn_phase()
            return MENU_WAIT

    @staticmethod
    def cancel(board, **kwargs):
        """
        Resets the player list and returns to the main menu.


        Parameters:
            board       (Board.Board):          Reference to the game board.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        board.reset_players()
        return MENU_MAIN

    @staticmethod
    def page_right(gui, **kwargs):
        """
        Increases the page number to display the next property.


        Parameters:
            gui         (GUI):                  Reference to the game GUI.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        gui.page_number += 1
        return MENU_WAIT

    @staticmethod
    def page_left(gui, **kwargs):
        """
        Decreases the page number to display the previous property.


        Parameters:
            gui         (GUI):                  Reference to the game GUI.
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        gui.page_number -= 1
        return MENU_WAIT

    @staticmethod
    def play(**kwargs):
        """
        Presents the name input menu.


        Parameters:
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.

        Returns:
            str: The next menu_state to be displayed on the gui.
        """
        return MENU_NAME

    @staticmethod
    def quit(**kwargs):
        """
        Exits the game.


        Parameters:
            **kwargs    ({key: arg, ...}):      Additional arguments passed to the Button.
        """
        exit(0)