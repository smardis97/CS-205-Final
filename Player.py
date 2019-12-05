

class Player:
    def __init__(self, name="", is_player=False, money=1200):
        self.money = money
        self.isPlayer = is_player
        self.hasJailCard = False
        self.ownedProperties = []
        self.name = name
        self.inJail = False

    def getMoney(self):
        return self.money

    def takeMoney(self, amount):
        if self.money >= amount:
            self.money -= amount
            return 0
        else:
            self.money = 0
            return -1 * (self.money - amount)

    def giveMoney(self, amount):
        self.money += amount

    def hasProperty(self, prop):
        for p in self.ownedProperties:
            if p == prop:
                return True
        return False

    def getName(self):
        return self.name

    def addProperty(self, prop):
        self.ownedProperties.append(prop)
        
    def getJailCard(self):
        return self.hasJailCard

    def addJailCard(self):
        self.hasJailCard = True

    def removeJailCard(self):
        self.hasJailCard = False

    def goToJail(self):
        self.inJail = True

    def getOutOfJail(self):
        self.inJail = False

    def getOwnedProperties(self):
        return self.ownedProperties

    def aiPurchase(self,property, purchase_cost,player):
        if (property.getRent()<9):
            return False

        if (purchase_cost*1.5>=player.getMoney()):
            return False

        else:
            return True


    def aiBuild(self, build_bool,property,player):
        numBuilt =0
        if (player.getMoney()*3.5<property.getHouseCost()):
            build_bool = False

        while(player.getMoney()*3.5>=property.getHouseCost()):
            numBuilt+=1
            build_bool= False

        build_dict = {
            property:numBuilt
        }

        return build_dict


