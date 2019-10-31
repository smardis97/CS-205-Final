import Tile
import Player
import constants

class Board:
    def __init__(self):
        self.tileList = []
        self.properties = {}  # {property-name, property-reference}
        self.players = {}  # {"identifier", (player_reference, position)}
        self.gameStarted = False
        self.constructBoard()

    def constructBoard(self):
        pass

    def addPlayer(self, player):
        if not self.gameStarted:
            self.players[player.name] = (player, 0)
            return True
        else:
            return False

    def addTile(self, tile):
        if len(self.tileList) >= constants.TILE_LIMIT:
            return False
        else:
            self.tileList.append(tile)
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
        self.tileList[destination].onLand(self.players[name][0])


    # TODO: only necessary for Jail?
    # refactor accordingly
    def playerDirectMove(self, name, destination):  # move without passing Go
        self.players[name][1] = destination