import Tile
import Player
import constants

class Board:
    def __init__(self):
        self.tileList = []
        self.players = {}  # {"identifier", player_reference} TODO: change? I think this should be reworked
        self.gameStarted = False


    def addPlayer(self, player):
        if not self.gameStarted:
            self.players[player.name] = player
            return True
        else:
            return False

    def addTile(self, tile):
        if len(self.tileList) >= constants.TILE_LIMIT:
            return False
        else:
            self.tileList.append(tile)
            return True



