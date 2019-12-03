import Board
import Player
import random

def rollDice():
    dices = (random.randint(1,6), random.randint(1,6))
    return dices

def winLose(Player,playerList):
    #if a player has no more properties to mortgage, and no more money they lose
    if(Player.getMoney()<=0 and len(Player.getOwnedProperties())<1):
        #removePlayer
        print("remove player")
        #after a player is removed check the length of the list, if the length of the list is 1 that player must be the winner
        if(len(playerList)==1):
            print(playerList.index(0).getName+"wins")




def main():
    #test winLose
    p2 = Player.Player(1200,True,"test2")
    p3 = Player.Player(0,True,"test3")
    playerList = [p2,p3]
    winLose(p3,playerList)



    board = Board.Board()
    player = Player.Player(1200, True, "test")
    board.addPlayer(player)
    playerName = player.getName()
    print(playerName)
    sentinel = 'Y'
    while sentinel == 'Y':
        diceRoll = rollDice()
        diceSum = diceRoll[0] + diceRoll[1]
        board.playerStandardMove("test", diceSum)
        sentinel = input("Would you like to continue? Y/N: ")
        
main()







        



