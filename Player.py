import pygame


class Player:
    def __init__(self, money=1200, is_player=False):
        self.money = money
        self.is_player = is_player
        self.has_jail_card = False
        self.owned_properties = []

    def take_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return 0
        else:
            self.money = 0
            return -1 * (self.money - amount)

    def give_money(self, amount):
        self.money += amount

    def has_property(self, prop):
        for p in self.owned_properties:
            if p == prop:
                return True
        return False

    #
    # TODO: add_property, add_jail_card, remove_jail_card, 
    #
    #