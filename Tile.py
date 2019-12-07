import random
import abc

#
#
#  TODO: Docstrings and readability comments
#
#

class Tile:
    __metaclass__=abc.ABCMeta

    def __init__(self):
        pass


class Property(Tile):
    def __init__(self, purchase_value, name, rent, group, house_cost=None):
        Tile.__init__(self)
        self.purchase_value = purchase_value
        self.name = name
        self.rent = rent
        self.group = group
        self.house_cost = house_cost
        self.mortgaged = False
        self.owner = None
        self.num_houses = 0

    def set_owner(self, owner):
        self.owner = owner

    def add_house(self):
        if self.num_houses < 4:
            self.num_houses += 1

    def get_purchase_value(self):
        return self.purchase_value

    def get_name(self):
        return self.name

    def get_rent(self):
        return self.rent

    def get_group(self):
        return self.group

    def get_house_cost(self):
        return self.house_cost

    def get_owner(self):
        return self.owner

    def get_num_houses(self):
        if self.num_houses > 3:
            return self.num_houses - 1
        return self.num_houses

    def get_num_hotels(self):
        return max([self.num_houses - 3, 0])

    def get_sale_price(self):
        return (self.purchase_value + self.num_houses * self.house_cost) / 2

class Go(Tile):
    def __init__(self):
        Tile.__init__(self)

class Parking(Tile):
    def __init__(self):
        Tile.__init__(self)

class GoToJail(Tile):
    def __init__(self):
        Tile.__init__(self)

class CardTile(Tile):
    def __init__(self, card_type):
        Tile.__init__(self)
        self.cardType = card_type

    def pick_card(self):
        choice = random.randint(1, 16)

        if self.cardType == "Community Chest":
            if choice == 1:
                return choice, ["Community Chest:", "Advance to Go", "collect $ 200"]
            elif choice == 2:
                return choice, ["Community Chest:", "Bank error", "in your favor.", "Collect $ 200"]
            elif choice == 3:
                return choice, ["Community Chest:", "Doctor's fee", "pay $ 50"]
            elif choice == 4:
                return choice, ["Community Chest:", "From sale of stock", "you get $ 50"]
            elif choice == 5:
                return choice, ["Community Chest:", "Get out of Jail", "Free"]
            elif choice == 6:
                return choice, ["Community Chest:", "Go to Jail"]
            elif choice == 7:
                return choice, ["Community Chest:", "Grand Opera Night", "Collect $ 50 form every", "player for opening night", "seats"]
            elif choice == 8:
                return choice, ["Community Chest:", "Holiday fund matures", "receive $ 100"]
            elif choice == 9:
                return choice, ["Community Chest:", "Income tax refund.", "Collect $ 20"]
            elif choice == 10:
                return choice, ["Community Chest:", "Life insurance matures", "Collect $ 100"]
            elif choice == 11:
                return choice, ["Community Chest:", "Hospital Fees.", "Pay $ 50"]
            elif choice == 12:
                return choice, ["Community Chest:", "School fees.", "Pay $ 50"]
            elif choice == 13:
                return choice, ["Community Chest:", "Receive $ 25", "consultancy fee"]
            elif choice == 14:
                return choice, ["Community Chest:", "You are assessed", "for street repairs:", "Pay $ 40 per house", "and", "$ 115 per hotel", "you own"]
            elif choice == 15:
                return choice, ["Community Chest:", "You have won second prize", "in a beauty contest.", "Collect $ 10"]
            elif choice == 16:
                return choice, ["Community Chest:", "You inherit", "$ 100"]
        elif self.cardType == "Chance":
            if choice == 1:
                return choice, ["Chance:", "Advance to Go", "Collect $ 200"]
            elif choice == 2:
                return choice, ["Chance:", "Advance to", "Illinois Ave", "If you pass Go", "Collect $ 200"]
            elif choice == 3:
                return choice, ["Chance:", "Advance to", "St. Charles Place", "If you pass Go", "Collect $ 200"]
            elif choice == 4:
                return choice, ["Chance:", "Advance to", "nearest Utility", "If owned, throw dice", "Pay the owner 10 times", "the amount rolled"]
            elif choice == 5:
                return choice, ["Chance:", "Advance to", "nearest Railroad", "Pay the owner twice", "the usual rent."]
            elif choice == 6:
                return choice, ["Chance:", "Bank pays you", "dividend of $ 50"]
            elif choice == 7:
                return choice, ["Chance:", "Get out of Jail", "Free"]
            elif choice == 8:
                return choice, ["Chance:", "Go back", "three spaces."]
            elif choice == 9:
                return choice, ["Chance:", "Go to Jail"]
            elif choice == 10:
                return choice, ["Chance:", "Make general repairs", "on all you properties", "$ 25 for each house", "$ 100 for each hotel"]
            elif choice == 11:
                return choice, ["Chance:", "Pay poor tax", "$ 15"]
            elif choice == 12:
                return choice, ["Chance:", "Advance to", "Reading Railroad", "If you pass Go", "Collect $ 200"]
            elif choice == 13:
                return choice, ["Chance:", "Advance to", "Boardwalk"]
            elif choice == 14:
                return choice, ["Chance:", "You have been elected", "Chairman of the Board", "Pay each player $ 50"]
            elif choice == 15:
                return choice, ["Chance:", "Your building and", "loan matures", "Collect $ 150"]
            elif choice == 16:
                return choice, ["Chance:", "You have won a", "crossword competition", "Collect $ 100"]


class Jail(Tile):
    def __init__(self):
        Tile.__init__(self)


class FreeParking(Tile):
    def __init__(self):
        Tile.__init__(self)


class Tax(Tile):
    def __init__(self, tax):
        Tile.__init__(self)
        self.tax = tax

    def get_tax(self):
        return self.tax