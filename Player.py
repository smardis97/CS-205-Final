import pygame


class Player:
    def __init__(self, money=1200, isPlayer=False):
        self.money = money
        self.isPlayer = isPlayer
        self.hasJailCard = False
        self.ownedProperties = []

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

    #
    # TODO: add_property, add_jail_card, remove_jail_card, 
    #
    #