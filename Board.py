import Tile
import Player
import constants

class Board:
    def __init__(self):
        self.tileList = []
        self.properties = {}  # {property-name, property-reference}
        self.turnOrder = []
        self.players = {}  # {"identifier", [player_reference, position]}
        self.gameStarted = False
        self.constructBoard()

    def constructBoard(self):
        self.addTile(Tile.Go())
        self.addTile(Tile.Property(60, "Mediterranean Avenue", (2, 10, 30, 90, 160), 50, "Brown"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(60, "Baltic Avenue", (4, 20, 60, 180, 320, 450), 50, "Brown"))
        self.addTile(Tile.Tax())
        self.addTile(Tile.Property(200, "Reading Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Tile.Property(100, "Oriental Avenue", (6, 30, 90, 270, 400, 550), 50, "Light Blue"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(100, "Vermont Avenue", (6, 30, 90, 270, 400, 550), 50, "Light Blue"))
        self.addTile(Tile.Property(120, "Connecticut Avenue", (8, 40, 100, 300, 450, 600), 50, "Light Blue"))

        self.addTile(Tile.Jail)
        self.addTile(Tile.Property(140, "St. Charles Place", (10, 50, 150, 450, 625, 750), 100, "Pink"))
        self.addTile(Tile.Property(150, "Electric Company", (4, 10), "Utility"))
        self.addTile(Tile.Property(140, "States Avenue", (10, 50, 150, 450, 625), 100, "Pink"))
        self.addTile(Tile.Property(160, "Virginia Avenue", (12, 60, 180, 500, 700), 100, "Pink"))
        self.addTile(Tile.Property(200, "Pennsylvania Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Tile.Property(180, "St. James Place", (14, 70, 200, 550, 750, 950), 100, "Orange"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(180, "Tennessee Avenue", (14, 70, 200, 550, 750, 950), 100, "Orange"))
        self.addTile(Tile.Property(200, "New York Avenue", (16, 80, 220, 600, 800, 1000), 100, "Orange"))

        self.addTile(Tile.FreeParking())
        self.addTile(Tile.Property(220, "Kentucky Avenue", (18, 90, 250, 700, 875), 150, "Red"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(220, "Indiana Avenue", (18, 90, 250, 700, 875), 150, "Red"))
        self.addTile(Tile.Property(240, "Illinois Avenue", (20, 100, 300, 750, 925, 1100), 150, "Red"))
        self.addTile(Tile.Property(200, "B. & O. Railroad", (25, 50, 100, 200), "Railroad"))
        self.addTile(Tile.Property(260, "Atlantic Avenue", (22, 110, 330, 800, 975, 1150), 150, "Yellow"))
        self.addTile(Tile.Property(260, "Ventnor Avenue", (22, 110, 330, 800, 975, 1150), 150, "Yellow"))
        self.addTile(Tile.Property(150, "Water Works", (4, 10), "Utility"))
        self.addTile(Tile.Property(280, "Marvin Gardens", (24, 120, 360, 850, 1025, 1200), 150, "Yellow"))

        self.addTile(Tile.GoToJail())
        self.addTile(Tile.Property(300, "Pacific Avenue", (26, 130, 390, 900, 1100, 1275), 200, "Green"))
        self.addTile(Tile.Property(300, "North Carolina Avenue", (26, 130, 390, 900, 1100, 1275), 200, "Green"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(320, "Pennsylvania Avenue", (28, 150, 450, 1000, 1200, 1400), 200, "Green"))
        self.addTile(Tile.Property(200, "Short Line", (25, 50, 100, 200), "Railroad"))
        self.addTile(Tile.CardTile())
        self.addTile(Tile.Property(350, "Park Place", (35, 175, 500, 1100, 1300, 1500), 200, "Blue"))
        self.addTile(Tile.Tax())
        self.addTile(Tile.Property(400, "Boardwalk", (50, 200, 600, 1400, 1700, 2000), 200, "Blue"))

    def addPlayer(self, player):
        if not self.gameStarted:
            self.players[player.getName()] = [player, 0]
            self.turnOrder.append(player.getName())
            return True
        else:
            return False

    def removePlayer(self, player_name):
        turnIndex = self.turnOrder.index(player_name)
        self.turnOrder.pop(turnIndex)
        return True

    def addTile(self, tile):
        if len(self.tileList) >= constants.TILE_LIMIT:
            return False
        else:
            self.tileList.append(tile)
            if isinstance(tile, Tile.Property):
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
        self.tileList[destination].onLand()

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


    # TODO: only necessary for Jail?
    # refactor accordingly
    def playerDirectMove(self, name, destination):  # move without passing Go
        self.players[name][1] = destination