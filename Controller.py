import Player
import random

class Controller:
    def __init__(self, playerList):
        self.players = playerList;
        self.sentinel = False;
    def rollDice(self):
        dices = (random.randInt(1,6), random.randInt(1,6));
        return dices;
    def pairCheck(self, dices):
        if dices[0] == dices[1]:
            return True;
        else:
            return False;
    #def playerCheck():


    def run(self, Player, Tile):
        self.sentinel = True;
        while self.sentinel:


        



