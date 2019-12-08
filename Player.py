from constants import *
import random


class Player:
    #
    #
    #  TODO: Docstrings and readability comments
    #
    #
    def __init__(self, name="", is_human=False, money=1200):
        self.money = money
        self.debt = 0
        self.is_human = is_human
        self.name = name
        self.owned_properties = []
        self.color = WHITE
        self.has_jail_card = False
        self.in_jail = False
        self.jail_counter = 3

    def ai_purchase(self, prop):
        return True

    def ai_sell_property(self):
        sale_amounts = []
        for prop in self.owned_properties:
            amount = prop.get_sale_price()
            sale_amounts.append(amount)
        sell = min(sale_amounts)
        return self.owned_properties[sale_amounts.index(sell)]

    def ai_build(self):
        if len(self.owned_properties) > 0:
            choice = random.randint(0, len(self.owned_properties) - 1)
            choice_prop = self.owned_properties[choice]
            if choice_prop.get_group() is not "Railroad" and choice_prop.get_group() is not "Utility":
                if self.money / 2 > choice_prop.get_house_cost():
                    chance = random.randint(0, 100)
                    if chance > 50:
                        return choice_prop

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

    def is_in_jail(self):
        return self.in_jail

    def get_jail_card(self):
        return self.has_jail_card

    def get_debt(self):
        return self.debt
