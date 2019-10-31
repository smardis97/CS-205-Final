class Tile:
    def onLand(self):
        raise NotImplementedError


#initialize numHouses to 0 in main
class Properties(Tile):
    def __init__(self, purchaseValue, group, name, owner, baseRent,numHouses,house_cost):
        self.name = name
        self.purchaseValue = purchaseValue
        self.group = group
        self.owner = owner
        self.baseRent = baseRent
        Tile.__init__(self)
        self.numHouses = numHouses
        self.house_cost = house_cost

    
    def setOwner(self, owner):
        self.owner = owner
    def setPurchaseValue(self, value):
        self.purchaseValue = value
    def setGroup(self, group):
        self.group = group
    def setName(self, name):
        self.name = name
    def setBaseRent(self,baseRent):
        self.baseRent = baseRent
    def setHouseCost(self,house_cost):
        self.house_cost = house_cost
    def getOwner(self):
        return self.owner
    def getPurchaseValue(self):
        return self.purchaseValue
    def getGroup(self):
        return self.group
    def getName(self):
        return self.name
    def getBaseRent(self):
        return self.baseRent
    def getHouseCost(self):
        return self.house_cost

    def addHouse(self):
        self.numHouses+=1

    def getNumHouses(self):
        return self.numHouses





    #def onLand(self):


class Go(Tile):
    def onLand(self):
        return 200

class Parking(Tile):
    def onLand(self):
        None


# TO-DO:
# class goToJail(Tile):
#     #def onLand(self):

# class cardTile(Tile):
#     #def onLand(self):