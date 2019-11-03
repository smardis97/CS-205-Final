import Board
import Player
import random

def rollDice():
    dices = (random.randint(1,6), random.randint(1,6))
    return dices


def main():
    board = Board.Board()
    player = Player.Player("test")
    board.addPlayer(player)
    sentinel = 'Y'
    while sentinel == 'Y':
        diceRoll = rollDice()
        diceSum = diceRoll[0] + diceRoll[1]
        board.playerStandardMove("test", diceSum)


        sentinel = input("Would you like to continue? Y/N")
        



main()







        



