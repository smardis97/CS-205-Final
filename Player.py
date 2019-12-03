
#import pygame


class Player:
    def __init__(self, money=1200, is_player=False, name=""):
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

    def add_property(self, property):
        self.ownedProperties.append(property)
        
    def get_jail_card(self):
        return self.hasJailCard

    def add_jail_card(self):
        self.hasJailCard = True;

    def remove_jail_card(self):
        self.hasJailCard = False

    def goToJail(self):
        self.inJail = True

    def getOutOfJail(self):
        self.inJail = False

    def getOwnedProperties(self):
        return self.ownedProperties

    def getName(self):
        return self.name

    def getMoney(self):
        return self.money;

