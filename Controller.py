import Board
import Player
import random

def rollDice(self):
    dices = (random.randint(1,6), random.randint(1,6))
    return dices



def main():
    board = Board.Board()
    player1 = Player.Player("test")
    player2 = Player.Player("test2")
    board.addPlayer(player1)
    board.addPlayer(player2)



    return 0;









        



