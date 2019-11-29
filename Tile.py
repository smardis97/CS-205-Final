import Player

class Tile:
    def onLand(self, player):
        raise NotImplementedError


# initialize numHouses to 0 in main
class Property(Tile):
    def __init__(self, purchaseValue, name, rent, house_cost=None, group=None):
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
        return self.numHouses

    def getNumHotels(self):
        return self.numHotels

    def onLand(self, player):
        print("You have reached " + self.getName())
        if self.owner == None:
            playerAnswer = input("Would you like to purchase " + self.getName() + " ? Y/N")
            if playerAnswer == 'Y':
                player.add_property(self)
                self.owner = player
            if playerAnswer == 'N':
                None
        else:
            print("This property is owned by " + self.getOwner.getName())
            player.takeMoney(self.rent)
            self.getOwner.giveMoney(self.rent)

            
        


class Go(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You passed GO")
        return 200


class Parking(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        None

# TODO: flesh out functionality
class GoToJail(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You've reached the Go to Jail tile")
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
        ("You reached Free Parking")
        pass


class Tax(Tile):  # TODO: argument for tax type
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        ("You reached Tax")
        pass