import Board
import Player
import random

def rollDice():
    dices = (random.randint(1,6), random.randint(1,6))
    return dices


def main():
    board = Board.Board()
    player = Player.Player(1200, True, "test")
    board.addPlayer(player)
    playerName = player.getName()
    print(playerName)
    sentinel = 'Y'
    while sentinel == 'Y':
        diceRoll = rollDice()
        dicYeSum = diceRoll[0] + diceRoll[1]
        board.playerStandardMove("test", dicYeSum)
        sentinel = input("Would you like to continue? Y/N: ")
        
main()







        



