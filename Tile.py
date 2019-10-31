class Tile:
    def onLand(self):
        raise NotImplementedError



class Properties(Tile):
    def __init__(self, value, group, name, owner):
        self.name = name
        self.value = value
        self.group = group
        self.owner = owner
        Tile.__init__(self)
    
    def setOwner(self, owner):
        self.owner = owner
    def setValue(self, value):
        self.value = value
    def setGroup(self, group):
        self.group = group
    def setName(self, name):
        self.name = name
    def getOwner(self):
        return self.owner
    def getValue(self):
        return self.value
    def getGroup(self):
        return self.group
    def getName(self):
        return self.name

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
