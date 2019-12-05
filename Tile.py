import Player
import CommunityChest

class Tile:
    def onLand(self, player):
        raise NotImplementedError


# initialize numHouses to 0 in main
class Property(Tile):
    def __init__(self, purchaseValue, name, rent, group, house_cost=None):
        self.name = name
        self.purchaseValue = purchaseValue
        self.group = group
        self.owner = None
        self.rent = rent
        Tile.__init__(self)
        self.numHouses = 0
        self.house_cost = house_cost

    def setOwner(self, owner):
        self.owner = owner

    def setPurchaseValue(self, value):
        self.purchaseValue = value

    def setGroup(self, group):
        self.group = group

    def setName(self, name):
        self.name = name

    def setRent(self, rent):
        self.rent = rent

    def setHouseCost(self, house_cost):
        self.house_cost = house_cost

    def getOwner(self):
        return self.owner

    def getPurchaseValue(self):
        return self.purchaseValue

    def getGroup(self):
        return self.group

    def getName(self):
        return self.name

    def getRent(self):
        return self.rent

    def getHouseCost(self):
        return self.house_cost

    def addHouse(self):
        self.numHouses += 1

    def getNumHouses(self):
        if self.numHouses > 3:
            return self.numHouses - 1
        return self.numHouses

    def getNumHotels(self):
        return max([self.numHouses - 3, 0])

    def onLand(self, player):
        return self
        # print("You have reached " + self.getName())
        # if self.owner is None:
        #     playerAnswer = input("Would you like to purchase " + self.getName() + " ? Y/N ")
        #     if playerAnswer == 'Y':
        #         if player.getMoney() >= self.getPurchaseValue():
        #             player.takeMoney(self.getPurchaseValue())
        #             player.addProperty(self)
        #             self.owner = player
        #         else:
        #             print("You cannot afford this property.")
        #     elif playerAnswer == 'N':
        #         None
        # elif self.getOwner().getName() == player.getName():
        #     playerAnswer2 = input("Would you like to build a house? Y/N ")
        #     if playerAnswer2 == 'Y':
        #         self.numHouses += 1;
        #     else:
        #         None
        # else:
        #     print("This property is owned by " + self.getOwner().getName())
        #     debt = player.takeMoney(self.rent[self.getNumHouses()])
        #     if debt == 0:
        #         print("You paid rent!")
        #     else:
        #         print("You owe " + debt)
        #         print("You must sell one of your properties back to the bank")
        #     self.getOwner().giveMoney(self.rent[self.getNumHouses()])

            
        


class Go(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You passed GO")
        player.giveMoney(200)


class Parking(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("Free parking!")

# TODO: flesh out functionality
class GoToJail(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You've reached the Go to Jail tile")
        if player.getJailCard():
            player.removeJailCard()
            print("You used your get out of jail card!")
        else:
            player.goToJail()        
        pass

class CardTile(Tile):  # TODO: argument for card type
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached the community chest")
        pass

class Jail(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached the Jail Tile")
        pass


class FreeParking(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached Free Parking")
        pass


class Tax(Tile):  # TODO: argument for tax type
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached Tax")
        pass