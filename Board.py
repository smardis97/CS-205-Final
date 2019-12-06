from Tile import *
import Player
import constants
import random
from GUI import *

class Board:
    def __init__(self, window):
        self.tileList = []
        self.properties = {}  # {property-name, property-reference}
        self.turnOrder = []
        self.currentTurn = 0
        self.players = {}  # {"identifier", [player_reference, position]}
        self.gameStarted = False
        self.color_options = COLOR_SELECT
        self.spEvent = 0
        self.constructBoard()
        self.currentTurn = 0
        self.next = False
        self.gui = GUI(window, self)
        self.e = -1

        self.constructBoard()

    def constructBoard(self):
        self.addTile(Go())
        self.addTile(Property(60, "Mediterranean Avenue", (2, 10, 30, 90, 160), "Purple", 50))
        self.addTile(CardTile("Community Chest"))
        self.addTile(Property(60, "Baltic Avenue", (4, 20, 60, 180, 320, 450), "Purple", 50))
        self.addTile(Tax("Income"))
        self.addTile(Property(200, "Reading Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Property(100, "Oriental Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.addTile(CardTile("Chance"))
        self.addTile(Property(100, "Vermont Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.addTile(Property(120, "Connecticut Avenue", (8, 40, 100, 300, 450, 600), "Light Blue", 50))

        self.addTile(Jail)
        self.addTile(Property(140, "St. Charles Place", (10, 50, 150, 450, 625, 750), "Pink", 100))
        self.addTile(Property(150, "Electric Company", (4, 10), "Utility"))
        self.addTile(Property(140, "States Avenue", (10, 50, 150, 450, 625), "Pink", 100))
        self.addTile(Property(160, "Virginia Avenue", (12, 60, 180, 500, 700), "Pink", 100))
        self.addTile(Property(200, "Pennsylvania Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Property(180, "St. James Place", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.addTile(CardTile("Community Chest"))
        self.addTile(Property(180, "Tennessee Avenue", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.addTile(Property(200, "New York Avenue", (16, 80, 220, 600, 800, 1000), "Orange", 100))

        self.addTile(FreeParking())
        self.addTile(Property(220, "Kentucky Avenue", (18, 90, 250, 700, 875), "Red", 150))
        self.addTile(CardTile("Chance"))
        self.addTile(Property(220, "Indiana Avenue", (18, 90, 250, 700, 875), "Red", 150))
        self.addTile(Property(240, "Illinois Avenue", (20, 100, 300, 750, 925, 1100), "Red", 150))
        self.addTile(Property(200, "B. & O. Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Property(260, "Atlantic Avenue", (22, 110, 330, 800, 975, 1150), "Yellow", 150))
        self.addTile(Property(260, "Ventnor Avenue", (22, 110, 330, 800, 975, 1150), "Yellow", 150))
        self.addTile(Property(150, "Water Works", (4, 10), "Utility"))
        self.addTile(Property(280, "Marvin Gardens", (24, 120, 360, 850, 1025, 1200), "Yellow", 150))

        self.addTile(GoToJail())
        self.addTile(Property(300, "Pacific Avenue", (26, 130, 390, 900, 1100, 1275), "Green", 200))
        self.addTile(Property(300, "North Carolina Avenue", (26, 130, 390, 900, 1100, 1275), "Green", 200))
        self.addTile(CardTile("Community Chest"))
        self.addTile(Property(320, "Pennsylvania Avenue", (28, 150, 450, 1000, 1200, 1400), "Green", 200))
        self.addTile(Property(200, "Short Line", (25, 50, 100, 200), "Railroad"))
        self.addTile(CardTile("Chance"))
        self.addTile(Property(350, "Park Place", (35, 175, 500, 1100, 1300, 1500), "Blue", 200))
        self.addTile(Tax("Luxury"))
        self.addTile(Property(400, "Boardwalk", (50, 200, 600, 1400, 1700, 2000), "Blue", 200))

    def addPlayer(self, player):
        if not self.gameStarted:
            self.players[player.get_name()] = [player, 0]
            self.turnOrder.append(player.get_name())
            if not player.isPlayer:
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

    def removePlayer(self, player_name):
        turnIndex = self.turnOrder.index(player_name)
        self.turnOrder.pop(turnIndex)
        return True

    def addTile(self, tile):
        if len(self.tileList) >= TILE_LIMIT:
            return False
        else:
            self.tileList.append(tile)
            if isinstance(tile, Property):
                self.properties[tile.getName()] = tile
            return True

    def playerStandardMove(self, name, roll):  # move, pass Go if applicable
        passGo = False
        currentPos = self.players[name][1]
        destination = (currentPos + roll) % constants.TILE_LIMIT
        if currentPos + roll >= constants.TILE_LIMIT:
            passGo = True
        self.players[name][1] = destination
        if passGo:
            self.players[name][0].give_money(200)
        self.turnEvent(self.tileList[destination])

    def getTiles(self):
        return self.tileList

    def getProperties(self):
        return self.properties

    def getPlayers(self):
        return self.players

    def gameStarted(self):
        return self.gameStarted

    def startGame(self):
        self.gameStarted = True

    def turnEvent(self, tile):
        if type(tile) is Property:
            self.gui.set_property(tile)


    def update(self):
        self.turnUpdate()
        self.gui.draw_gui()

        if len(self.turnOrder) > 0:
            current_player = self.players[self.turnOrder[self.currentTurn]][0]
            landed_tile = self.tileList[self.players[self.turnOrder[self.currentTurn]][1]]
        else:
            current_player = None
            landed_tile = None

        if self.spEvent == 7:  # player has lost
            self.turnOrder.remove(current_player.getName())
            del self.players[current_player.player.get_name()]
            if current_player.isPlayer:
                self.gui.state_change(MENU_OVER)
            self.progressTurn()
        elif self.spEvent == 6:  # player owes money
            if len(current_player.ownedProperties) > 0:
                if current_player.isPlayer:
                    self.gui.state_change(MENU_DEBT)
                else:
                    sell_off = current_player.aiDebt()
                    self.propertySale(current_player.getName(), sell_off)
                    self.gui.state_change(MENU_AI_SELL)
            else:
                self.specialEvent(7)
        elif self.spEvent == 5:  # chance 5 pt2
            if current_player.isPlayer:
                self.gui.state_change(MENU_SE_PLR_RENT)
            else:
                # TODO: Case for unowned property
                self.payRent(current_player.getName(), landed_tile.getOwner(), self.getRent(landed_tile.getName()))
                self.gui.state_change(MENU_SE_AI_RENT)
            self.specialEvent(0)
        elif self.spEvent == 4:  # chance 4 pt2
            if current_player.isPlayer:
                self.gui.state_change(MENU_SE_DICE)
            else:
                # TODO: Case for unowned property
                rolls = self.rollDice()
                self.gui.set_sp_ev(10 * sum(rolls))
                self.payRent(current_player.getName(), landed_tile.getOwner(), 10 * sum(rolls))
                self.gui.state_change(MENU_SE_AI_RENT)
            self.specialEvent(0)
        elif self.spEvent == 3:  # chance 5 pt1
            self.nextRailroad(current_player.getName())
        elif self.spEvent == 2:  # chance 4 pt1
            self.nextUtility(current_player.getName())
        elif self.spEvent == 1:  # double move
            self.e -= 1
            self.specialEvent(0)
            self.nextEvent()
        elif self.next:
            self.eventIndex()
            if self.e == 0:
                if current_player.isPlayer:
                    self.gui.state_change(MENU_DICE)
                    self.next = False
                else:
                    rolls = self.rollDice()
                    self.gui.set_dice_result(rolls)
                    self.gui.state_change(MENU_AI_ROLL)
                    self.next = False
            elif self.e == 1:
                # if currently landed tile is a Property
                if type(landed_tile) is Property:
                    # if the current player is a human
                    if current_player.isPlayer:
                        # if landed tile in unowned
                        if landed_tile.getOwner() is None:
                            self.gui.state_change(MENU_BUY)
                            self.next = False
                        else:
                            self.gui.state_change(MENU_PLR_AI)
                            self.next = False
                    # current player is ai
                    else:
                        # if landed tile in unowned
                        if landed_tile.getOwner() is None:
                            # if ai wants to buy
                            if current_player.aiPurchase(landed_tile):
                                self.runPurchase(current_player.getName(),
                                                 landed_tile.getName())
                                self.gui.state_change(MENU_AI_BUY)
                                self.next = False
                            else:
                                self.nextEvent()
                        else:
                            self.payRent(current_player.getName(), landed_tile.getOwner(),
                                         self.getRent(landed_tile.getName()))
                            self.gui.state_change(MENU_AI_RENT)
                            self.next = False
                # if not
                elif type(landed_tile) is CardTile:
                    if current_player.isPlayer:
                        self.gui.set_card(landed_tile.pickCard())
                        if landed_tile.cardType == "Community Chest":
                            self.gui.state_change(MENU_COM_CH)
                        else:
                            self.gui.state_change(MENU_CHANCE)
                        self.next = False
                    else:
                        choice = landed_tile.pickCard()[0]
                        if landed_tile.cardType == "Community Chest":
                            self.gui.state_change(ButtonOperands.community_chest(choice, self, self.gui))
                        else:
                            self.gui.state_change(ButtonOperands.chance(choice, self, self.gui))
                elif type(landed_tile) is Tax:
                    if landed_tile.getType() == "Luxury":
                        self.takeMoney(current_player.getName(), 75)
                    elif landed_tile.getType() == "Income":
                        self.takeMoney(current_player.getName(), 200)
                elif type(landed_tile) is GoToJail:
                    current_player.goToJail()
                    self.playerDirectMove(current_player.getName(), 10, False)
            elif self.e == 2:  # AI build houses
                pass
            elif self.e == 3:
                if current_player.isPlayer:
                    self.gui.state_change(MENU_END)
                    self.next = False
                else:
                    self.progressTurn()


    def resetPlayers(self):
        self.turnOrder.clear()
        self.players.clear()

    def getHumanPlayers(self):
        humanPlayers = []
        for name, player in self.players.items():
            if player[0].isPlayer:
                humanPlayers.append(name)
        return humanPlayers

    def rollDice(self):
        dice = (random.randint(1, 6), random.randint(1, 6))
        return dice

    def turnUpdate(self):
        if len(self.turnOrder) > 0:
            self.gui.current_player = self.turnOrder[self.currentTurn]
        else:
            self.gui.current_player = None

    def progressTurn(self):
        self.currentTurn = (self.currentTurn + 1) % len(self.players)
        self.e = -1
        self.nextEvent()

    def eventIndex(self):
        self.e = (self.e + 1) % EVENT_COUNT

    def nextEvent(self):
        self.next = True
        
    def runPurchase(self, player, prop):
        self.properties[prop].setOwner(player)
        self.players[player][0].add_property(self.properties[prop])
        self.takeMoney(player, self.properties[prop].getPurchaseValue())
        if self.getHumanPlayers()[0] == player:
            self.gui.prop_buttons.append(Button((-100, -100), "Build: {}".format(self.properties[prop].getHouseCost()),
                                                ButtonOperands.build, BUTTON_COLOR, BUTTON_HIGHLIGHT,
                                                prop))

    def getRent(self, prop):
        if self.properties[prop].getGroup() is not "Railroad" and self.properties[prop].getGroup() is not "Utility":
            return self.properties[prop].getRent()[self.properties[prop].getNumHouses()]
        else:
            owned_count = 0
            for name, property in self.properties.items():
                if property.getOwner() == self.properties[prop].getOwner() and\
                    property.getGroup() == self.properties[prop].getGroup():
                    owned_count += 1
            return self.properties[prop].getRent()[owned_count - 1]

    def payRent(self, tenant, landlord, amount):
        self.takeMoney(tenant, amount)
        self.players[landlord][0].give_money(amount)

    def specialEvent(self, se):
        self.spEvent = se
        self.next = False

    def nextUtility(self, player_name):
        current_pos = self.players[player_name][1]
        destination = current_pos
        for dist in range(1, TILE_LIMIT):
            destination = (current_pos + dist) % TILE_LIMIT
            if type(self.tileList[destination]) is Property:
                if self.tileList[destination].getGroup() == "Utility":
                    break
        self.playerDirectMove(player_name, destination)
        self.specialEvent(4)

    def nextRailroad(self, player_name):
        current_pos = self.players[player_name][1]
        destination = current_pos
        for dist in range(1, TILE_LIMIT):
            destination = (current_pos + dist) % TILE_LIMIT
            if type(self.tileList[destination]) is Property:
                if self.tileList[destination].getGroup() == "Railroad":
                    break
        self.playerDirectMove(player_name, destination)
        self.gui.set_sp_ev(2 * self.getRent(self.tileList[destination].get_name()))
        self.specialEvent(5)

    def takeMoney(self, player_name, amount):
        player = self.players[player_name][0]
        if player.get_money() < amount:
            debt = amount - player.get_money()
            player.take_money(amount)
            player.add_debt(debt)
            self.specialEvent(6)
        else:
            player.take_money(amount)

    def propertySale(self, player_name, property):
        player = self.players[player_name][0]
        prop_index = player.ownedProperties.index(property)
        if player.isPlayer:
            self.gui.prop_buttons.pop(prop_index)
        player.remove_debt((property.getPurchaseValue() + property.getHouseCost() * property.getNumHouses()) / 2)
        player.ownedProperties.remove(property)
        property.setOwner(None)
        property.numHouses = 0
        if player.get_debt() == 0:
            self.specialEvent(0)
            self.nextEvent()
        else:
            self.specialEvent(6)


    # TODO: only necessary for Jail?
    # refactor accordingly
    def playerDirectMove(self, name, destination, passGo=True):  # move without passing Go
        player = self.players[name][0]
        current_pos = self.players[name][1]
        self.players[name][1] = destination
        if current_pos > destination:  # must pass go
            if passGo:
                player.give_money(200)
        self.turnEvent(self.tileList[destination])
