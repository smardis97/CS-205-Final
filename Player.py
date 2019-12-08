from constants import *
import random


class Player:
    """
    The Player class holds all the information about each player instance.

    Attributes:
        money               (int):                      How much money the player has.
        debt                (int):                      How much money the player owes to the bank.
        is_human            (bool):                     Whether the player is human controlled.
        name                (str):                      The name of the player.
        owned_properties    ([Property(Tile), ...]):    A list of properties owned by this player.
        color               ((int, int, int)):          The RGB values that this player is displayed with.
        has_jail_card       (bool):                     Whether this player has a get-out-of-jail-free card.
        in_jail             (bool):                     Whether this player is currently in jail.
        jail_counter        (int):                      Number of turns until the player is
                                                            automatically released from jail.
    """
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

    def ai_purchase(self, property_tile):
        """
        Controls logic for the AI to choose whether to buy the property they just landed on.

        Parameters:
            property_tile   (Property(Tile)):       The tile to make a decision on.

        Returns:
            bool:           Whether the player will buy this property.
        """
        if property_tile.get_purchase_value() < self.money / 2:
            return True
        else:
            return False

    def ai_sell_property(self):
        """
        Controls logic for the AI to choose which property to sell.

        Returns:
            Property(Tile): Which owned property the player will sell.
        """
        sale_amounts = []
        for prop in self.owned_properties:
            amount = prop.get_sale_price()
            sale_amounts.append(amount)
        sell = min(sale_amounts) # sells the least valuable tile first.
        return self.owned_properties[sale_amounts.index(sell)]

    def ai_build(self):
        """
        Controls logic for the AI to choose whether to build a house this turn.

        Returns:
            Property(Tile): Which property the AI wants to build a house on.
        """
        if len(self.owned_properties) > 0:
            choice = random.randint(0, len(self.owned_properties) - 1)
            choice_prop = self.owned_properties[choice]
            if choice_prop.get_group() is not "Railroad" and choice_prop.get_group() is not "Utility":
                if self.money / 2 > choice_prop.get_house_cost():
                    chance = random.randint(0, 100)
                    if chance > 50:
                        return choice_prop

    def has_property(self, prop):
        """
        Whether the player owns the asked property.

        Parameters:
            prop:   (Property(Tile)):   The property being searched for.

        Returns:
            bool:   Whether the player owns the asked property.
        """
        for p in self.owned_properties:
            if p == prop:
                return True
        return False

    def give_money(self, amount):
        """
        Gives this player the specified amount of money.

        Parameters:
            amount  (int):      The amount to be given to the player.
        """
        self.money += amount

    def take_money(self, amount):
        """
        Takes the specified amount of money from the player.

        Returns:
            amount  (int):      Amount to be taken from the player.
        """
        if self.money >= amount:
            self.money -= amount
            return 0
        else:
            self.money = 0
            return -1 * (self.money - amount)

    def add_property(self, prop):
        """
        Adds the specified property to owned_properties.

        Parameters:
            prop    (Property(Tile)):   The property being added.
        """
        self.owned_properties.append(prop)

    def add_jail_card(self):
        """
        Sets has_jail_card to True.
        """
        self.has_jail_card = True

    def remove_jail_card(self):
        """
        Sets has_jail_card to False.
        """
        self.has_jail_card = False

    def go_to_jail(self):
        """
        Sets in_jail to True.
        """
        self.in_jail = True

    def get_out_of_jail(self):
        """
        Sets in_jail to False, and resets jail_counter.
        """
        self.in_jail = False
        self.jail_counter = 3

    def set_color(self, color):
        """
        Sets color to the specified color.
        """
        self.color = color

    def jail_count_down(self):
        """
        Counts down jail_counter and unsets in_jail when it reaches zero.
        """
        self.jail_counter -= 1
        if self.jail_counter == 0:
            self.get_out_of_jail()

    def add_debt(self, amount):
        """
        Adds the specified amount of debt.
        """
        self.debt += amount

    def remove_debt(self, amount):
        """
        Removes the specified amount of debt.
        """
        if self.debt <= amount:
            self.give_money(amount - self.debt)
            self.debt = 0
        else:
            self.debt -= amount

    def get_name(self):
        """
        Getter for the player's name.
        """
        return self.name

    def get_money(self):
        """
        Getter for the player's money.
        """
        return self.money

    def get_owned_properties(self):
        """
        Getter for the player's owned properties.
        """
        return self.owned_properties

    def is_in_jail(self):
        """
        Getter for in_jail.
        """
        return self.in_jail

    def get_jail_card(self):
        """
        Getter for has_jail_card.
        """
        return self.has_jail_card

    def get_debt(self):
        """
        Getter for the player's debt.
        """
        return self.debt
