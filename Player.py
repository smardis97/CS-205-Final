from constants import *


class Player:
    def __init__(self, name="", is_player=False, money=1200):
        self.money = money
        self.isPlayer = is_player
        self.debt = 0
        self.color = WHITE
        self.hasJailCard = False
        self.ownedProperties = []
        self.name = name
        self.inJail = False
        self.jailCount = 3

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
        self.jailCount = 3

    def getOwnedProperties(self):
        return self.ownedProperties

    def setColor(self, color):
        self.color = color

    def aiPurchase(self, prop):
        return True

    def jailCountDown(self):
        self.jailCount -= 1
        if self.jailCount == 0:
            self.getOutOfJail()

    def addDebt(self, amount):
        self.debt += amount

    def removeDebt(self, amount):
        if self.debt < amount:
            self.giveMoney(amount - self.debt)
            self.debt = 0
        else:
            self.debt -= amount

    def getDebt(self):
        return self.debt
