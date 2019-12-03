import random

class CommunityChest:
    def __init__(self,card):
        self.card = card



    def pickCard(self, player, playerList):
        if player in playerList:
            playerList.remove(player)



        #get a random number and return that card
        num = random.randint(1,16)

        if num == 1:
            player.giveMoney(self, 200)
            return "Advance to Go collect $200"
        elif num == 2:
            player.giveMoney(self, 200)
            return "Bank error in your favor. Collect $200"
        elif num == 3:
            player.takeMoney(self, 50)
            return "Doctor's fee, pay $50"
        elif num == 4:
            player.giveMoney(self, 50)
            return "From sale of stock you get $50"
        elif num == 5:
            #store this card
            return "Get out of jail free"
        elif num == 6:
            #Player.goToJail
            return "Go to jail"
        elif num == 7:
            #TODO make a list of players and remove the current player, iterate over the list and take 50 from each player
            for player in playerList:
                player.takeMoney(self, 50)
            return "Grand Opera Night Collect $50 from every player for opening night seats"
        elif num == 8:
            player.giveMoney(self, 100)
            return "Holiday fund matures, recieve $100"
        elif num == 9:
            player.giveMoney(self, 20)
            return"Income tax refund. Collect $20"
        elif num == 10:
            player.giveMoney(self, 100)
            return "Life insurance matures – Collect $100"
        elif num == 11:
            player.takeMoney(self, 50)
            return"Hospital Fees. Pay $50"
        elif num == 12:
            player.takeMoney(self, 50)
            return "School fees. Pay $50"
        elif num == 13:
            player.giveMoney(self, 25)
            return "Receive $25 consultancy fee"
        elif num == 14:
            #TODO method to get number of houses and hotels a player has
            propertyList = player.getOwnedProperties()
            numHouses = 0
            numHotels = 0
            for Properties in propertyList:
                numHouses +=Properties.getNumHouses(self)
                numHotels +=Properties.getNumHotels(self)
            player.takeMoney(self, numHouses * 40)
            player.takeMoney(self, numHotels * 115)
            return "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own"
        elif num == 15:
            player.giveMoney(self, 10)
            return "You have won second prize in a beauty contest. Collect $10"
        elif num == 16:
            player.giveMoney(self, 100)
            return "You inherit $100"


#edit players money