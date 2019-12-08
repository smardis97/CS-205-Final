import random


from Tile import *
from constants import *
from GUI import *

class Board:
    """
    The Board class contains all data about the state of the game, and controls the progression of events.

    Attributes:
        gui                 (GUI):                      Handles all user facing information and user interaction.
        tile_list           ([Tile]):                   Contains all 40 tiles in the order they are
                                                            traversed on the board.
        turn_order          ([str]):                    List of player names in the order they take their turn.
        properties          ({str: Property(Tile)}):    Dict of all properties by name.
        players             ({str: [Player, int]}):      Dict of all players and their position on the
                                                            board by player name.
        current_turn        (int):                      Index of turn_order for whose turn it is.
        game_started        (bool):                     Whether the game has been started yet.
        color_options       ([(int, int, int)]):        List of possible colors for player avatars.
        special_event       (int):                      Identifies special situations that don't fit the game's
                                                            normal turn progression.
        next_phase          (bool):                     Tells Board that the player has acknowledged the most
                                                            recent event and can continue.
        current_turn_phase  (int):                      Identifies which part of the normal phases of a turn
                                                            has been reached.
    """
    def __init__(self, window):
        self.gui = GUI(window, self)
        self.tile_list = []
        self.turn_order = []
        self.properties = {}  # {property-name: property-reference}
        self.players = {}  # {"player-name": [player_reference, position]}                position is index of tile_list
        self.current_turn = 0
        self.game_started = False
        self.color_options = COLOR_SELECT
        self.special_event = 0
        self.next_phase = False
        self.current_turn_phase = -1
        self.construct_board()

    def construct_board(self):
        """
        Adds data about the game spaces to tile_list in the order they appear on the board.
        """
        self.add_tile(Go())
        self.add_tile(Property(60, "Mediterranean Avenue", (2, 10, 30, 90, 160), "Purple", 50))
        self.add_tile(CardTile("Community Chest"))
        self.add_tile(Property(60, "Baltic Avenue", (4, 20, 60, 180, 320, 450), "Purple", 50))
        self.add_tile(Tax("Income"))
        self.add_tile(Property(200, "Reading Railroad", (25, 50, 100, 200), "Railroad"))
        self.add_tile(Property(100, "Oriental Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.add_tile(CardTile("Chance"))
        self.add_tile(Property(100, "Vermont Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.add_tile(Property(120, "Connecticut Avenue", (8, 40, 100, 300, 450, 600), "Light Blue", 50))

        self.add_tile(Jail())
        self.add_tile(Property(140, "St. Charles Place", (10, 50, 150, 450, 625, 750), "Pink", 100))
        self.add_tile(Property(150, "Electric Company", (4, 10), "Utility"))
        self.add_tile(Property(140, "States Avenue", (10, 50, 150, 450, 625), "Pink", 100))
        self.add_tile(Property(160, "Virginia Avenue", (12, 60, 180, 500, 700), "Pink", 100))
        self.add_tile(Property(200, "Pennsylvania Railroad", (25, 50, 100, 200), "Railroad"))
        self.add_tile(Property(180, "St. James Place", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.add_tile(CardTile("Community Chest"))
        self.add_tile(Property(180, "Tennessee Avenue", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.add_tile(Property(200, "New York Avenue", (16, 80, 220, 600, 800, 1000), "Orange", 100))

        self.add_tile(FreeParking())
        self.add_tile(Property(220, "Kentucky Avenue", (18, 90, 250, 700, 875), "Red", 150))
        self.add_tile(CardTile("Chance"))
        self.add_tile(Property(220, "Indiana Avenue", (18, 90, 250, 700, 875), "Red", 150))
        self.add_tile(Property(240, "Illinois Avenue", (20, 100, 300, 750, 925, 1100), "Red", 150))
        self.add_tile(Property(200, "B. & O. Railroad", (25, 50, 100, 200), "Railroad"))
        self.add_tile(Property(260, "Atlantic Avenue", (22, 110, 330, 800, 975, 1150), "Yellow", 150))
        self.add_tile(Property(260, "Ventnor Avenue", (22, 110, 330, 800, 975, 1150), "Yellow", 150))
        self.add_tile(Property(150, "Water Works", (4, 10), "Utility"))
        self.add_tile(Property(280, "Marvin Gardens", (24, 120, 360, 850, 1025, 1200), "Yellow", 150))

        self.add_tile(GoToJail())
        self.add_tile(Property(300, "Pacific Avenue", (26, 130, 390, 900, 1100, 1275), "Green", 200))
        self.add_tile(Property(300, "North Carolina Avenue", (26, 130, 390, 900, 1100, 1275), "Green", 200))
        self.add_tile(CardTile("Community Chest"))
        self.add_tile(Property(320, "Pennsylvania Avenue", (28, 150, 450, 1000, 1200, 1400), "Green", 200))
        self.add_tile(Property(200, "Short Line", (25, 50, 100, 200), "Railroad"))
        self.add_tile(CardTile("Chance"))
        self.add_tile(Property(350, "Park Place", (35, 175, 500, 1100, 1300, 1500), "Blue", 200))
        self.add_tile(Tax("Luxury"))
        self.add_tile(Property(400, "Boardwalk", (50, 200, 600, 1400, 1700, 2000), "Blue", 200))

    def update(self):
        """
        Controls the main flow of the game. Updates the gui to display information to the player.

        Updates gui about whose turn it currently is.
        Draws gui.


        Checks for special events that need to be handled.  >>>~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*~~*  Special Event
        special_event:
            7: Current Player has lost.
            6: Current Player owes money.
            5: Part 2 of Chance card 5; either buy the Railroad or pay double rent.
            4: Part 2 of Chance card 4; either buy the Utility or pay 10 times the amount rolled.
            3: Part 1 of Chance card 5; advance to the next Railroad.
            2: Part 1 of Chance card 4; advance to the next Utility
            1: For Chance and Community Chest cards the move the Player a second time. Check the landed tile.


        Checks if the player is ready to move to the next phase of the turn.  >>> ~~*~~*~~*~~*~~*~~*~~*~~*   Normal Turn
        current_turn_phase:
            0: Movement Phase: Current Player rolls, and then moves.
            1: Tile Landing Phase: Upon landing on a tile, Board determines what happens depending on the tile.
            2: AI Build Phase: Allows AI players to build houses/hotels. >>>NOT IMPLEMENTED<<<
            3: End Turn Phase: Allows the Player to end their turn. Human Players can build before ending their turn.
        """
        self.turn_update()
        self.gui.draw_gui()

        # set variables for better readability
        if len(self.turn_order) > 0:
            # lol what a mess
            current_player = self.players[self.turn_order[self.current_turn]][0]
            landed_tile = self.tile_list[self.players[current_player.get_name()][1]]
        else:
            current_player = None
            landed_tile = None

        ################################################################################################################
        # CURRENT PLAYER HAS LOST ------------------------------------------------------------ CURRENT PLAYER HAS LOST #
        ################################################################################################################
        if self.special_event == 7:
            self.turn_order.remove(current_player.get_name())
            del self.players[current_player.get_name()]
            if current_player.is_human:
                self.gui.state_change(MENU_OVER)
            self.progress_turn()
        ################################################################################################################
        # CURRENT PLAYER OWES MONEY -------------------------------------------------------- CURRENT PLAYER OWES MONEY #
        ################################################################################################################
        elif self.special_event == 6:
            if len(current_player.get_owned_properties()) > 0:  # player still has properties to sell
                if current_player.is_human:
                    self.gui.state_change(MENU_DEBT)
                else:
                    sell_off = current_player.ai_debt()
                    self.property_sale(current_player.get_name(), sell_off)
                    self.gui.state_change(MENU_AI_SELL)
            else:  # current_player has no more properties to sell
                self.set_special_event(7)
        ################################################################################################################
        # CHANCE: RAILROAD PART 2 ------------------------------------------------------------ CHANCE: RAILROAD PART 2 #
        ################################################################################################################
        # Advance to the nearest Railroad.               ###########/
        # If unowned, you may buy it from the bank.      ######/
        # If owned, pay the owner twice the usual rent.  ###/
        ##################################################/
        elif self.special_event == 5:
            #
            # Tile is already owned
            #
            if landed_tile.get_owner() is not None:
                if current_player.is_human:
                    self.gui.state_change(MENU_SE_PLR_RENT)
                else:
                    self.pay_rent(current_player.get_name(), landed_tile.get_owner(), 2 * self.get_rent_value(landed_tile.get_name()))
                    self.gui.state_change(MENU_SE_AI_RENT)
            #
            # Tile is not owned
            #
            else:
                if current_player.is_human:
                    self.gui.state_change(MENU_BUY)
                    self.next_phase = False
                else:
                    if current_player.ai_purchase(landed_tile):
                        self.run_purchase(current_player.get_name(),
                                          landed_tile.get_name())
                        self.gui.state_change(MENU_AI_BUY)
                        self.next_phase = False
                    else:
                        self.next_turn_phase()
            self.set_special_event(0)
        ################################################################################################################
        # CHANCE: UTILITY PART 2 -------------------------------------------------------------- CHANCE: UTILITY PART 2 #
        ################################################################################################################
        # Advance to the nearest Utility.                                     ###########/
        # If unowned, you may buy it from the bank.                           ######/
        # If owned, throw dice and pay the owner ten time the amount rolled.  ###/
        #######################################################################/
        elif self.special_event == 4:
            #
            # Tile is already owned
            #
            if landed_tile.get_owner() is not None:
                if current_player.is_human:
                    self.gui.state_change(MENU_SE_DICE)
                else:
                    rolls = self.roll_dice()
                    self.gui.set_special_event(10 * sum(rolls))
                    self.pay_rent(current_player.get_name(), landed_tile.get_owner(), 10 * sum(rolls))
                    self.gui.state_change(MENU_SE_AI_RENT)
                self.set_special_event(0)
            #
            # Tile is not owned
            #
            else:
                if current_player.is_human:
                    self.gui.state_change(MENU_BUY)
                    self.next_phase = False
                else:
                    if current_player.ai_purchase(landed_tile):
                        self.run_purchase(current_player.get_name(),
                                          landed_tile.get_name())
                        self.gui.state_change(MENU_AI_BUY)
                        self.next_phase = False
                    else:
                        self.next_turn_phase()
            self.set_special_event(0)
        ##\
        #####\
        #########\
        ##############\
        ########################\
        ################################################################################################################
        # CHANCE: RAILROAD PART 1 ------------------------------------------------------------ CHANCE: RAILROAD PART 1 #
        ################################################################################################################
        elif self.special_event == 3:
            self.move_to_next_railroad(current_player.get_name())
        ##\
        #####\
        #########\
        ##############\
        ########################\
        ################################################################################################################
        # CHANCE: UTILITY PART 1 -------------------------------------------------------------- CHANCE: UTILITY PART 1 #
        ################################################################################################################
        elif self.special_event == 2:
            self.move_to_next_utility(current_player.get_name())
        ##\
        #####\
        #########\
        ##############\
        ########################\
        ################################################################################################################
        # SECOND TILE LAND -------------------------------------------------------------------------- SECOND TILE LAND #
        ################################################################################################################
        elif self.special_event == 1:
            self.current_turn_phase -= 1
            self.set_special_event(0)
            self.next_turn_phase()
        ################################################################################################################
        # NORMAL TURN ------------------------------------------------------------------------------------ NORMAL TURN #
        ################################################################################################################
        elif self.next_phase:
            self.increment_phase_counter()
            #
            # MOVEMENT PHASE ---------------------------------------------------------------------------- MOVEMENT PHASE
            #
            if self.current_turn_phase == 0:
                if current_player.is_human:
                    self.gui.state_change(MENU_DICE)
                    self.next_phase = False
                else:
                    rolls = self.roll_dice()
                    self.gui.set_dice_result(rolls)
                    self.gui.state_change(MENU_AI_ROLL)
                    self.next_phase = False
            #
            # TILE LANDING PHASE -------------------------------------------------------------------- TILE LANDING PHASE
            #
            elif self.current_turn_phase == 1:
                #=======================
                # LANDED ON A PROPERTY                                                              landed on a property
                #=======================
                if type(landed_tile) is Property:

                    if current_player.is_human:
                        #
                        # Tile is not owned
                        #
                        if landed_tile.get_owner() is None:
                            self.gui.state_change(MENU_BUY)
                            self.next_phase = False
                        #
                        # Tile is already owned
                        #
                        else:
                            self.gui.state_change(MENU_PLR_AI)
                            self.next_phase = False

                    # current player is ai
                    else:
                        #
                        # Tile is not owned
                        #
                        if landed_tile.get_owner() is None:
                            # if ai wants to buy
                            if current_player.ai_purchase(landed_tile):
                                self.run_purchase(current_player.get_name(),
                                                  landed_tile.get_name())
                                self.gui.state_change(MENU_AI_BUY)
                                self.next_phase = False
                            else:
                                self.next_turn_phase()
                        #
                        # Tile is already owned
                        #
                        else:
                            self.pay_rent(current_player.get_name(), landed_tile.get_owner(),
                                          self.get_rent_value(landed_tile.get_name()))
                            self.gui.state_change(MENU_AI_RENT)
                            self.next_phase = False
                # =====================================
                # LANDED ON CHANCE OR COMMUNITY CHEST                                                          card tile
                # =====================================
                elif type(landed_tile) is CardTile:

                    if current_player.is_human:
                        self.gui.set_card(landed_tile.pick_card())
                        if landed_tile.cardType == "Community Chest":
                            self.gui.state_change(MENU_COM_CH)
                        else:
                            self.gui.state_change(MENU_CHANCE)
                        self.next_phase = False

                    else:
                        choice = landed_tile.pick_card()[0]
                        if landed_tile.cardType == "Community Chest":
                            self.gui.state_change(ButtonOperands.community_chest(choice, self, self.gui))
                        else:
                            self.gui.state_change(ButtonOperands.chance(choice, self, self.gui))
                # =================
                # LANDED ON A TAX                                                                                    tax
                # =================
                elif type(landed_tile) is Tax:
                    if landed_tile.get_tax() == "Luxury":
                        self.take_money_from_player(current_player.get_name(), 75)
                    elif landed_tile.get_tax() == "Income":
                        self.take_money_from_player(current_player.get_name(), 200)
                # =======================
                # LANDED ON GO TO JAIL                                                                        go to jail
                # =======================
                elif type(landed_tile) is GoToJail:
                    current_player.go_to_jail()
                    self.player_direct_move(current_player.get_name(), 10, False)
            #
            # AI CONSTRUCTION PHASE -------------------------------------------------------------- AI CONSTRUCTION PHASE
            #
            elif self.current_turn_phase == 2:
                if not current_player.is_human:
                    choice = current_player.ai_build()
                    if choice is not None and choice.get_num_houses() < 4:
                        choice.add_house()
                        self.take_money_from_player(current_player.get_name(), choice.get_house_cost())
            #
            # PLAYER END TURN -------------------------------------------------------------------------- PLAYER END TURN
            #
            elif self.current_turn_phase == 3:
                if current_player.is_human:
                    self.gui.state_change(MENU_END)
                    self.next_phase = False
                else:
                    self.progress_turn()

    def player_standard_move(self, name, roll):
        """
        Moves the player forward based on how much they rolled. Give them 200 if they pass Go

        Parameters:
            name    (str):      The name of the player being moved.
            roll    (int):      Sum of the dice the player rolled, how far they are being moved.
        """
        # set variables for better readability
        pass_go = False
        current_pos = self.players[name][1]

        # index of tile_list corresponding to their destination tile
        destination = (current_pos + roll) % TILE_LIMIT

        # if the player overflows TILE_LIMIT, then they must have passed or reached Go
        if current_pos + roll >= TILE_LIMIT:
            pass_go = True

        # move player to their new position
        self.players[name][1] = destination
        if pass_go:
            self.players[name][0].give_money(200)

        # inform gui if the player landed on a Property
        self.turn_event(self.tile_list[destination])

    def player_direct_move(self, name, destination, pass_go=True):
        """
        Moves the player directly to the destination tile. Give money for passing Go only if pass_go is True.

        Parameters:
            name            (str):      The name of the player being moved.
            destination     (int):      Index of tile_list of the destination tile.
            pass_go         (bool):     Whether the player will receive money when/if they pass Go
        """
        # set variables for better readability
        player = self.players[name][0]
        current_pos = self.players[name][1]

        # move player to their new position
        self.players[name][1] = destination

        # if they are already past their new location, then they must pass go to get there
        if current_pos > destination:
            # only give money if player is allowed to pass Go
            # player will not pass go when sent to Jail
            if pass_go:
                player.give_money(200)

        # inform gui if the player landed on a Property
        self.turn_event(self.tile_list[destination])

    def add_player(self, player):
        """
        Adds the new player to players as long as the game has not been started.

        Parameters:
            player (Player): The new player object to be added to the game.

        Returns:
            bool: Whether the player was successfully added to the game or not.
        """
        if not self.game_started:
            # add the new player to players
            # players is a dict keyed by player name containing a list with the player object and their position
            self.players[player.get_name()] = [player, 0]

            # add the new player to turn_order
            self.turn_order.append(player.get_name())
            if not player.is_human:
                # for ai players, color is selected from color_options once the colors taken by all existing
                #   players have been removed.
                for name, player_data in self.players.items():
                    if player_data[0].color in self.color_options:
                        self.color_options.remove(player_data[0].color)
                if len(self.color_options) > 0:
                    player.set_color(self.color_options[0])
                else:
                    player.set_color(BLACK)
            # reset color_options to use with the next new player
            self.color_options = COLOR_SELECT
            return True
        else:
            return False

    def reset_players(self):
        """
        Reset players and turn_order to empty.
        """
        self.turn_order.clear()
        self.players.clear()

    def add_tile(self, tile):
        """
        Add the new tile to tile_list if tile_list is not already full.

        Parameters:
            tile (Tile): The new Tile object to be added to tile_list.

        Returns:
            bool: Whether the Tile was successfully added to tile_list or not.
        """
        if len(self.tile_list) >= TILE_LIMIT:
            return False
        else:
            self.tile_list.append(tile)
            if isinstance(tile, Property):
                self.properties[tile.get_name()] = tile
            return True

    def turn_event(self, tile):
        """
        Updates gui.property_result if the player landed on a Property.

        Parameters:
            tile (Tile): The Tile that the player just landed on.
        """
        if type(tile) is Property:
            self.gui.set_property(tile)

    def turn_update(self):
        """
        Updates gui.current_player to the player that is currently taking their turn.
        """
        if len(self.turn_order) > 0:
            self.gui.current_player = self.turn_order[self.current_turn]
        else:
            self.gui.current_player = None

    def progress_turn(self):
        """
        Increments current_turn to the index of the next player.
        """
        self.current_turn = (self.current_turn + 1) % len(self.players)

        # reset turn phase
        self.current_turn_phase = -1
        self.next_turn_phase()

    def increment_phase_counter(self):
        """
        Increments current_turn_phase to the next phase.
        """
        self.current_turn_phase = (self.current_turn_phase + 1) % TURN_STAGE_COUNT

    def next_turn_phase(self):
        """
        Sets next_phase to True, allowing Board to run the next phase of the current turn.
        """
        self.next_phase = True

    def set_special_event(self, event_index):
        """
        Sets special_event to the parameter value. Allows Board to handle nonstandard turn progression.

        Parameters:
            event_index (int): Value of the new special_event.
        """
        self.special_event = event_index
        self.next_phase = False

    def run_purchase(self, player_name, property_name):
        """
        Processes the purchase of the named property by the player.

        Parameters:
            player_name     (str):      Name of the player buying property.
            property_name   (str):      Name of the property being bought.
        """
        # set variables for better readability
        buyer = self.players[player_name][0]
        property_tile = self.properties[property_name]

        # set values to finalize purchase
        property_tile.set_owner(player_name)
        buyer.add_property(property_tile)
        self.take_money_from_player(player_name, property_tile.get_purchase_value())

        # for the human player's properties, add a button to the right-hand display that allows them to build houses
        if self.get_human_players()[0] == player_name:
            self.gui.prop_buttons.append(
                Button((-100, -100), "Build: {}".format(property_tile.get_house_cost()),
                       ButtonOperands.build, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                       property_name))

    def pay_rent(self, tenant_name, landlord_name, amount):
        """
        Pay money from tenant to landlord.

        Parameters:
            tenant_name     (str):      Name of the player paying rent.
            landlord_name   (str):      Name of the player being payed.
            amount          (int):      Amount of rent being payed.
        """
        self.take_money_from_player(tenant_name, amount)
        self.players[landlord_name][0].give_money(amount)

    def property_sale(self, player_name, property_tile):
        """
        Process sale of property by the named player.

        Parameters:
            player_name     (str):              Name of the player selling property.
            property_tile   (Property(Tile)):   Reference to the property being sold.
        """
        # set variables for better readability
        player = self.players[player_name][0]
        property_index = player.get_owned_properties.index(property_tile)  # index of property in player's properties

        # remove the build button for property if player is human
        if player.is_human:
            self.gui.prop_buttons.pop(property_index)

        # remove debt corresponding to the value of the sold property
        player.remove_debt(property_tile.get_sale_price())

        player.get_owned_properties.remove(property_tile)

        # reset owner and num_houses for property
        property_tile.set_owner(None)
        property_tile.num_houses = 0

        # if player has sold off all their debt, proceed with normal turn progress
        if player.get_debt() == 0:
            self.set_special_event(0)
            self.next_turn_phase()

        # player is still in debt
        else:
            self.set_special_event(6)

    def take_money_from_player(self, player_name, amount):
        """
        Take money from the named player. Set events accordingly if player ends up in debt.

        Parameters:
            player_name     (str):      Name of the player paying money.
            amount          (int):      Amount of money being taken.
        """
        # set variables for better readability
        player = self.players[player_name][0]

        # if player has less money than they need to pay, set their debt accordingly.
        if player.get_money() < amount:
            debt = amount - player.get_money()
            player.take_money(amount)
            player.add_debt(debt)
            self.set_special_event(6)

        # player has enough money to pay cost
        else:
            player.take_money(amount)

    def move_to_next_utility(self, player_name):
        """
        Move the player forward until they reach the next Utility.

        Parameters:
            player_name (str): Name of the player being moved.
        """
        # set variables for better readability
        current_pos = self.players[player_name][1]

        destination = current_pos
        for dist in range(1, TILE_LIMIT):  # walk forward until reaching a Utility tile.
            destination = (current_pos + dist) % TILE_LIMIT  # set destination to an index of tile_list
            if type(self.tile_list[destination]) is Property:
                if self.tile_list[destination].get_group() == "Utility":
                    break

        # move the player to the destination tile
        self.player_direct_move(player_name, destination)
        # set special_event for next stage of event progression
        self.set_special_event(4)

    def move_to_next_railroad(self, player_name):
        """
        Move the player forward until they reach the next Railroad.

        Parameters:
            player_name (str): Name of the player being moved.
        """
        # set variables for better readability
        current_pos = self.players[player_name][1]

        destination = current_pos
        for dist in range(1, TILE_LIMIT):  # walk forward until reaching a Railroad tile.
            destination = (current_pos + dist) % TILE_LIMIT  # set destination to an index of tile_list
            if type(self.tile_list[destination]) is Property:
                if self.tile_list[destination].get_group() == "Railroad":
                    break

        # move the player to the destination tile
        self.player_direct_move(player_name, destination)
        # set gui special event value to twice normal rent
        self.gui.set_special_event(2 * self.get_rent_value(self.tile_list[destination].get_name()))
        # set special_event for next stage of event progression
        self.set_special_event(5)

    def roll_dice(self):
        """
        Choose two random numbers between 1 and 6.
        """
        dice = (random.randint(1, 6), random.randint(1, 6))
        return dice

    def start_game(self):
        """
        Set game_started, prevents adding more players.
        """
        self.game_started = True

    def get_tiles(self):
        """
        Getter for tile_list.

        Returns:
            [Tile]      tile_list
        """
        return self.tile_list

    def get_properties(self):
        """
        Getter for properties.

        Returns:
            {str: Property(Tile)}   properties
        """
        return self.properties

    def get_players(self):
        """
        Getter for players.

        Returns:
            {str: [Player, int]}    players
        """
        return self.players

    def get_human_players(self):
        """
        Gets a list of names of players where is_human is True.

        Returns:
            [str]       List of player names where is_human is True.
        """
        human_players = []
        for name, player in self.players.items():
            if player[0].is_human:
                human_players.append(name)
        return human_players

    def get_rent_value(self, property_name):
        """
        Get the current cost of rent for the named property.

        For normal properties, rent is based on the number of houses. A hotel is equivalent to 4 houses.
        For Utilities and Railroads, rent is based on how many total Utilities or Railroads the property owner has.

        Parameters:
            property_name (str): Name of the property to check rent for.

        Returns:
            int     Amount of rent to be charged.
        """
        # set variables for readability
        property_tile = self.properties[property_name]

        if property_tile.get_group() is not "Railroad" and property_tile.get_group() is not "Utility":
            return property_tile.get_rent()[property_tile.get_num_houses()]
        else:
            owned_count = 0
            for name, prop_tile in self.properties.items():  # find all properties with the same owner and group
                if prop_tile.get_owner() == property_tile.get_owner() and \
                                prop_tile.get_group() == property_tile.get_group():
                    owned_count += 1
            return property_tile.get_rent()[owned_count - 1] # subtract one to get the proper index of rent tuple
