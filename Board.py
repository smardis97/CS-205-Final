from Tile import *
import Player
import constants
import random
from New_GUI import *

class Board:
    def __init__(self, window):
        self.tileList = []
        self.properties = {}  # {property-name, property-reference}
        self.turnOrder = []
        self.currentTurn = 0
        self.players = {}  # {"identifier", [player_reference, position]}
        self.gameStarted = False
        self.color_options = COLOR_SELECT
        self.constructBoard()
        self.currentTurn = 0
        self.next = False
        self.gui = GUI(window, self)
        self.e = -1

        self.constructBoard()

    def constructBoard(self):
        self.addTile(Go())
        self.addTile(Property(60, "Mediterranean Avenue", (2, 10, 30, 90, 160), "Purple", 50))
        self.addTile(CardTile())
        self.addTile(Property(60, "Baltic Avenue", (4, 20, 60, 180, 320, 450), "Purple", 50))
        self.addTile(Tax())
        self.addTile(Property(200, "Reading Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Property(100, "Oriental Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.addTile(CardTile())
        self.addTile(Property(100, "Vermont Avenue", (6, 30, 90, 270, 400, 550), "Light Blue", 50))
        self.addTile(Property(120, "Connecticut Avenue", (8, 40, 100, 300, 450, 600), "Light Blue", 50))

        self.addTile(Jail)
        self.addTile(Property(140, "St. Charles Place", (10, 50, 150, 450, 625, 750), "Pink", 100))
        self.addTile(Property(150, "Electric Company", (4, 10), "Utility"))
        self.addTile(Property(140, "States Avenue", (10, 50, 150, 450, 625), "Pink", 100))
        self.addTile(Property(160, "Virginia Avenue", (12, 60, 180, 500, 700), "Pink", 100))
        self.addTile(Property(200, "Pennsylvania Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Property(180, "St. James Place", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.addTile(CardTile())
        self.addTile(Property(180, "Tennessee Avenue", (14, 70, 200, 550, 750, 950), "Orange", 100))
        self.addTile(Property(200, "New York Avenue", (16, 80, 220, 600, 800, 1000), "Orange", 100))

        self.addTile(FreeParking())
        self.addTile(Property(220, "Kentucky Avenue", (18, 90, 250, 700, 875), "Red", 150))
        self.addTile(CardTile())
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
        self.addTile(CardTile())
        self.addTile(Property(320, "Pennsylvania Avenue", (28, 150, 450, 1000, 1200, 1400), "Green", 200))
        self.addTile(Property(200, "Short Line", (25, 50, 100, 200), "Railroad"))
        self.addTile(CardTile())
        self.addTile(Property(350, "Park Place", (35, 175, 500, 1100, 1300, 1500), "Blue", 200))
        self.addTile(Tax())
        self.addTile(Property(400, "Boardwalk", (50, 200, 600, 1400, 1700, 2000), "Blue", 200))

    def addPlayer(self, player):
        if not self.gameStarted:
            self.players[player.getName()] = [player, 0]
            self.turnOrder.append(player.getName())
            if not player.isPlayer:
                for name, player_data in self.players.items():
                    if player_data[0].color in self.color_options:
                        self.color_options.remove(player_data[0].color)
                if len(self.color_options) > 0:
                    player.setColor(self.color_options[0])
                else:
                    player.setColor(BLACK)
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
            self.players[name][0].giveMoney(200)
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
        if self.next:
            current_player = self.players[self.turnOrder[self.currentTurn]][0]
            landed_tile = self.tileList[self.players[self.turnOrder[self.currentTurn]][1]]
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
                else:
                    print("Not Property")
            elif self.e == 2:
                print(self.e)
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
        self.players[player][0].addProperty(self.properties[prop])
        self.players[player][0].takeMoney(self.properties[prop].getPurchaseValue())
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
        self.players[tenant][0].takeMoney(amount)
        self.players[landlord][0].giveMoney(amount)


    # TODO: only necessary for Jail?
    # refactor accordingly
    def playerDirectMove(self, name, destination):  # move without passing Go
        currentPos = self.players[name][1]
        self.players[name][1] = destination
        passGo = False
        if currentPos + destination >= constants.TILE_LIMIT:
            passGo = True

        if passGo:
            self.players[name][0].giveMoney(200)