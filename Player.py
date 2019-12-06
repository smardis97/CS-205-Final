from constants import *


class Player:
    def __init__(self, name="", is_player=False, money=1200):
        self.money = money
        self.is_player = is_player
        self.debt = 0
        self.color = WHITE
        self.has_jail_card = False
        self.owned_properties = []
        self.name = name
        self.in_jail = False
        self.jail_counter = 3

    def ai_purchase(self, prop):
        return True

    def ai_sell_property(self):
        saleAmounts = []
        for prop in self.owned_properties:
            amount = (prop.getPurchaseValue() + prop.getNumHouses() * prop.getHouseCose()) / 2
            saleAmounts.append(amount)
        sell = min(saleAmounts)
        return self.owned_properties[saleAmounts.index(sell)]

    def has_property(self, prop):
        for p in self.owned_properties:
            if p == prop:
                return True
        return False

    def give_money(self, amount):
        self.money += amount

    def take_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return 0
        else:
            self.money = 0
            return -1 * (self.money - amount)

    def add_property(self, prop):
        self.owned_properties.append(prop)

    def add_jail_card(self):
        self.has_jail_card = True

    def remove_jail_card(self):
        self.has_jail_card = False

    def go_to_jail(self):
        self.in_jail = True

    def get_out_of_jail(self):
        self.in_jail = False
        self.jail_counter = 3

    def set_color(self, color):
        self.color = color

    def jail_count_down(self):
        self.jail_counter -= 1
        if self.jail_counter == 0:
            self.get_out_of_jail()

    def add_debt(self, amount):
        self.debt += amount

    def remove_debt(self, amount):
        if self.debt < amount:
            self.give_money(amount - self.debt)
            self.debt = 0
        else:
            self.debt -= amount

    def get_name(self):
        return self.name

    def get_money(self):
        return self.money

    def get_owned_properties(self):
        return self.owned_properties

    def get_jail_card(self):
        return self.has_jail_card

    def get_debt(self):
        return self.debt
