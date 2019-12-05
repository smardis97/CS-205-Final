import random

class Chance:
    def __init__(self, card, playerList):
        self.card = card
        self.playerList = playerList




    def pickCard(self, Player, playerList, Board):
        if Player in playerList:
            playerList.remove(Player)

        num = random.randint(1,16)

        if num == 1:
            #TODO move player to go
            Board.playerDirectMove(self,Player.getName(),0)
            Player.giveMoney(self,200)
            return "Advance to go Collect $200"

        elif num == 2:
            #TODO determine if player passed go
            Board.playerDirectMove(self,Player.getName(),24)
            return "Advance to Illinois Ave—If you pass Go, collect $200"

        elif num == 3:
            #TODO move player to St.Charles Place
            #TODO determine if player pased go
            Board.playerDirectMove(self,Player.getName(),11)
            return "Advance to St. Charles Place – If you pass Go, collect $200"

        elif num == 4:
            #TODO determine where the player is and advance it until it reaches a utility Tile
            #TODO check if the utility is owned
            #roll = random.randint(1, 12)
            #TODO pay roll*10
           return "Advance token to nearest Utility. If unowned, you may buy it from the Bank. " \
                  "If owned, throw dice and pay owner a total ten times the amount thrown."

        elif num == 5:
            #TODO same logic as case 4
            return "Advance token to the nearest Railroad and pay owner twice the rental to which he/she " \
                   "is otherwise entitled. If Railroad is unowned, you may buy it from the Bank."


        elif num == 6:
            Player.giveMoney(self,50)
            return "Bank pays you dividend of $50"

        elif num == 7:
            #TODO get out of jail free
            return "Get Out of Jail Free"

        elif num == 8:
            #TODO move player 3 spaces backwards
            Board.playerStandardMove(self,Player.getName(),-3)
            return "Go Back 3 Spaces"

        elif num == 9:
            Player.goToJail()
            return "Go to Jail–Go directly to Jail–Do not pass Go, do not collect $200"

        elif num == 10:
            propertyList = Player.getOwnedProperties()
            numHouses = 0
            numHotels = 0
            for Properties in propertyList:
                numHouses += Properties.getNumHouses(self)
                numHotels += Properties.getNumHotels(self)
            Player.takeMoney(self, numHouses * 25)
            Player.takeMoney(self, numHotels * 100)
            return "Make general repairs on all your property–For each house pay $25–For each hotel $100"

        elif num == 11:
            Player.takeMoney(self,15)
            return "Pay poor tax of $15"

        elif num == 12:


            Board.playerDirectMove(self,Player.getName(),5)
            return "Take a trip to Reading Railroad–If you pass Go, collect $200"

        elif num == 13:
            Board.playerDirectMove(self,Player.getName(),39)
            return "Take a walk on the Boardwalk–Advance token to Boardwalk"

        elif num == 14:
            numPlayers = self.len(playerList)
            Player.takeMoney(self,numPlayers)
            for Player in playerList:
                Player.giveMoney(self,50)
            return "You have been elected Chairman of the Board–Pay each player $50"

        elif num == 15:
            Player.giveMoney(self,150)
            return "Your building and loan matures—Collect $150"

        elif num == 16:
            Player.giveMoney(self,100)
            return "You have won a crossword competition—Collect $100"