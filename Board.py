from Tile import *
import Player
import constants
import random
from GUI import *

class Board:
    #
    #
    #  TODO: Docstrings and readability comments
    #
    #
    def __init__(self, window):
        self.gui = GUI(window, self)
        self.tile_list = []
        self.turn_order = []
        self.properties = {}  # {property-name: property-reference}
        self.players = {}  # {"identifier": [player_reference, position]}
        self.current_turn = 0
        self.game_started = False
        self.color_options = COLOR_SELECT
        self.special_event = 0
        self.next_phase = False
        self.current_turn_phase = -1
        self.construct_board()

    def construct_board(self):
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
        self.turn_update()
        self.gui.draw_gui()

        if len(self.turn_order) > 0:
            current_player = self.players[self.turn_order[self.current_turn]][0]
            landed_tile = self.tile_list[self.players[self.turn_order[self.current_turn]][1]]
        else:
            current_player = None
            landed_tile = None

        ################################################################################################################
        # CURRENT PLAYER HAS LOST ------------------------------------------------------------ CURRENT PLAYER HAS LOST #
        ################################################################################################################
        if self.special_event == 7:  # player has lost
            self.turn_order.remove(current_player.get_name())
            del self.players[current_player.get_name()]
            if current_player.is_human:
                self.gui.state_change(MENU_OVER)
            self.progress_turn()
        ################################################################################################################
        # CURRENT PLAYER OWES MONEY -------------------------------------------------------- CURRENT PLAYER OWES MONEY #
        ################################################################################################################
        elif self.special_event == 6:  # player owes money
            if len(current_player.get_owned_properties) > 0:
                if current_player.is_human:
                    self.gui.state_change(MENU_DEBT)
                else:
                    sell_off = current_player.ai_debt()
                    self.property_sale(current_player.get_name(), sell_off)
                    self.gui.state_change(MENU_AI_SELL)
            else:
                self.set_special_event(7)
        elif self.special_event == 5:  # chance 5 pt2
            if current_player.is_human:
                self.gui.state_change(MENU_SE_PLR_RENT)
            else:
                # TODO: Case for unowned property
                self.pay_rent(current_player.get_name(), landed_tile.get_owner(), self.get_rent_value(landed_tile.get_name()))
                self.gui.state_change(MENU_SE_AI_RENT)
            self.set_special_event(0)
        elif self.special_event == 4:  # chance 4 pt2
            if current_player.is_human:
                self.gui.state_change(MENU_SE_DICE)
            else:
                # TODO: Case for unowned property
                rolls = self.roll_dice()
                self.gui.set_special_event(10 * sum(rolls))
                self.pay_rent(current_player.get_name(), landed_tile.get_owner(), 10 * sum(rolls))
                self.gui.state_change(MENU_SE_AI_RENT)
            self.set_special_event(0)
        elif self.special_event == 3:  # chance 5 pt1
            self.move_to_next_railroad(current_player.get_name())
        elif self.special_event == 2:  # chance 4 pt1
            self.move_to_next_utility(current_player.get_name())
        elif self.special_event == 1:  # double move
            self.current_turn_phase -= 1
            self.set_special_event(0)
            self.next_turn_phase()
        elif self.next_phase:
            self.increment_phase_counter()
            if self.current_turn_phase == 0:
                if current_player.is_human:
                    self.gui.state_change(MENU_DICE)
                    self.next_phase = False
                else:
                    rolls = self.roll_dice()
                    self.gui.set_dice_result(rolls)
                    self.gui.state_change(MENU_AI_ROLL)
                    self.next_phase = False
            elif self.current_turn_phase == 1:
                # if currently landed tile is a Property
                if type(landed_tile) is Property:
                    # if the current player is a human
                    if current_player.is_human:
                        # if landed tile in unowned
                        if landed_tile.get_owner() is None:
                            self.gui.state_change(MENU_BUY)
                            self.next_phase = False
                        else:
                            self.gui.state_change(MENU_PLR_AI)
                            self.next_phase = False
                    # current player is ai
                    else:
                        # if landed tile in unowned
                        if landed_tile.get_owner() is None:
                            # if ai wants to buy
                            if current_player.ai_purchase(landed_tile):
                                self.run_purchase(current_player.get_name(),
                                                  landed_tile.get_name())
                                self.gui.state_change(MENU_AI_BUY)
                                self.next_phase = False
                            else:
                                self.next_turn_phase()
                        else:
                            self.pay_rent(current_player.get_name(), landed_tile.get_owner(),
                                          self.get_rent_value(landed_tile.get_name()))
                            self.gui.state_change(MENU_AI_RENT)
                            self.next_phase = False
                # if not
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
                elif type(landed_tile) is Tax:
                    if landed_tile.get_tax() == "Luxury":
                        self.take_money_from_player(current_player.get_name(), 75)
                    elif landed_tile.get_tax() == "Income":
                        self.take_money_from_player(current_player.get_name(), 200)
                elif type(landed_tile) is GoToJail:
                    current_player.go_to_jail()
                    self.player_direct_move(current_player.get_name(), 10, False)
            elif self.current_turn_phase == 2:  # AI build houses
                pass
            elif self.current_turn_phase == 3:
                if current_player.is_human:
                    self.gui.state_change(MENU_END)
                    self.next_phase = False
                else:
                    self.progress_turn()

    def player_standard_move(self, name, roll):  # move, pass Go if applicable
        pass_go = False
        current_pos = self.players[name][1]
        destination = (current_pos + roll) % constants.TILE_LIMIT
        if current_pos + roll >= constants.TILE_LIMIT:
            pass_go = True
        self.players[name][1] = destination
        if pass_go:
            self.players[name][0].give_money(200)
        self.turn_event(self.tile_list[destination])

    def player_direct_move(self, name, destination, pass_go=True):  # move without passing Go
        player = self.players[name][0]
        current_pos = self.players[name][1]
        self.players[name][1] = destination
        if current_pos > destination:  # must pass go
            if pass_go:
                player.give_money(200)
        self.turn_event(self.tile_list[destination])

    def add_player(self, player):
        if not self.game_started:
            self.players[player.get_name()] = [player, 0]
            self.turn_order.append(player.get_name())
            if not player.is_human:
                for name, player_data in self.players.items():
                    if player_data[0].color in self.color_options:
                        self.color_options.remove(player_data[0].color)
                if len(self.color_options) > 0:
                    player.set_color(self.color_options[0])
                else:
                    player.set_color(BLACK)
            self.color_options = COLOR_SELECT
            return True
        else:
            return False

    def remove_player(self, player_name):
        turn_index = self.turn_order.index(player_name)
        self.turn_order.pop(turn_index)
        return True

    def reset_players(self):
        self.turn_order.clear()
        self.players.clear()

    def add_tile(self, tile):
        if len(self.tile_list) >= TILE_LIMIT:
            return False
        else:
            self.tile_list.append(tile)
            if isinstance(tile, Property):
                self.properties[tile.get_name()] = tile
            return True

    def turn_event(self, tile):
        if type(tile) is Property:
            self.gui.set_property(tile)

    def turn_update(self):
        if len(self.turn_order) > 0:
            self.gui.current_player = self.turn_order[self.current_turn]
        else:
            self.gui.current_player = None

    def progress_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        self.current_turn_phase = -1
        self.next_turn_phase()

    def increment_phase_counter(self):
        self.current_turn_phase = (self.current_turn_phase + 1) % TURN_STAGE_COUNT

    def next_turn_phase(self):
        self.next_phase = True

    def set_special_event(self, event_index):
        self.special_event = event_index
        self.next_phase = False

    def run_purchase(self, player, prop):
        self.properties[prop].set_owner(player)
        self.players[player][0].add_property(self.properties[prop])
        self.take_money_from_player(player, self.properties[prop].get_purchase_value())
        if self.get_human_players()[0] == player:
            self.gui.prop_buttons.append(
                Button((-100, -100), "Build: {}".format(self.properties[prop].get_house_cost()),
                       ButtonOperands.build, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                       prop))

    def pay_rent(self, tenant, landlord, amount):
        self.take_money_from_player(tenant, amount)
        self.players[landlord][0].give_money(amount)

    def property_sale(self, player_name, property):
        player = self.players[player_name][0]
        prop_index = player.get_owned_properties.index(property)
        if player.is_human:
            self.gui.prop_buttons.pop(prop_index)
        player.remove_debt((property.get_purchase_value() + property.get_house_cost() * property.get_num_houses()) / 2)
        player.get_owned_properties.remove(property)
        property.set_owner(None)
        property.numHouses = 0
        if player.get_debt() == 0:
            self.set_special_event(0)
            self.next_turn_phase()
        else:
            self.set_special_event(6)

    def take_money_from_player(self, player_name, amount):
        player = self.players[player_name][0]
        if player.get_money() < amount:
            debt = amount - player.get_money()
            player.take_money(amount)
            player.add_debt(debt)
            self.set_special_event(6)
        else:
            player.take_money(amount)

    def move_to_next_utility(self, player_name):
        current_pos = self.players[player_name][1]
        destination = current_pos
        for dist in range(1, TILE_LIMIT):
            destination = (current_pos + dist) % TILE_LIMIT
            if type(self.tile_list[destination]) is Property:
                if self.tile_list[destination].get_group() == "Utility":
                    break
        self.player_direct_move(player_name, destination)
        self.set_special_event(4)

    def move_to_next_railroad(self, player_name):
        current_pos = self.players[player_name][1]
        destination = current_pos
        for dist in range(1, TILE_LIMIT):
            destination = (current_pos + dist) % TILE_LIMIT
            if type(self.tile_list[destination]) is Property:
                if self.tile_list[destination].get_group() == "Railroad":
                    break
        self.player_direct_move(player_name, destination)
        self.gui.set_special_event(2 * self.get_rent_value(self.tile_list[destination].get_name()))
        self.set_special_event(5)

    def roll_dice(self):
        dice = (random.randint(1, 6), random.randint(1, 6))
        return dice

    def start_game(self):
        self.game_started = True

    def get_tiles(self):
        return self.tile_list

    def get_properties(self):
        return self.properties

    def get_players(self):
        return self.players

    def get_human_players(self):
        human_players = []
        for name, player in self.players.items():
            if player[0].is_human:
                human_players.append(name)
        return human_players

    def get_rent_value(self, prop):
        if self.properties[prop].get_group() is not "Railroad" and self.properties[prop].get_group() is not "Utility":
            return self.properties[prop].get_rent()[self.properties[prop].get_num_houses()]
        else:
            owned_count = 0
            for name, property in self.properties.items():
                if property.get_owner() == self.properties[prop].get_owner() and \
                                property.get_group() == self.properties[prop].get_group():
                    owned_count += 1
            return self.properties[prop].get_rent()[owned_count - 1]
