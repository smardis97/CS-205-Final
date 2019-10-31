class Tile:
    def onLand(self):
        raise NotImplementedError


#initialize numHouses to 0 in main
class Properties(Tile):
    def __init__(self, purchaseValue, group, name, owner, baseRent,numHouses):
        self.name = name
        self.purchaseValue = purchaseValue
        self.group = group
        self.owner = owner
        self.baseRent = baseRent
        Tile.__init__(self)
        self.numHouses = numHouses

    
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