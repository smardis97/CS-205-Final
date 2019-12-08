import random
import abc


class Tile:
    """
    The Tile class is a base class for all objects that represent spaces on the board.
    """
    __metaclass__=abc.ABCMeta

    def __init__(self):
        pass


class Property(Tile):
    """
    The Property class holds information about property spaces on the board.

    Attributes:
        purchase_value      (int):              The cost to buy the property from the bank.
        name                (str):              Name of the property.
        rent                ((int, int, ...)):  Tuple of values for how much rent this property will charge.
                                                    Based on either the number of houses, or the number of
                                                    properties in the group the owner has.
        group               (str):              Which property group this property belongs to.
        house_cost          (int):              How much money it costs to build a house on this property.
        owner               (str):              The name of the owner of this property.
        num_houses          (int):              The number of houses built on this property.
    """
    def __init__(self, purchase_value, name, rent, group, house_cost=None):
        Tile.__init__(self)
        self.purchase_value = purchase_value
        self.name = name
        self.rent = rent
        self.group = group
        self.house_cost = house_cost
        self.owner = None
        self.num_houses = 0

    def set_owner(self, owner):
        """
        Setter for the owner of this property.
        """
        self.owner = owner

    def add_house(self):
        """
        Adds a house as long as there is not already a hotel (4 houses) on this property.
        """
        if self.num_houses < 4:
            self.num_houses += 1

    def get_purchase_value(self):
        """
        Getter for the purchase_value of this property.
        """
        return self.purchase_value

    def get_name(self):
        """
        Getter for the name of this property.
        """
        return self.name

    def get_rent(self):
        """
        Getter for the list of possible rent values for this property.
        """
        return self.rent

    def get_group(self):
        """
        Getter for the group this property is in.
        """
        return self.group

    def get_house_cost(self):
        """
        Getter for the cost of a house on this property.
        """
        return self.house_cost

    def get_owner(self):
        """
        Getter for the owner of this property.
        """
        return self.owner

    def get_num_houses(self):
        """
        Getter for the number of houses on this property.
        """
        if self.num_houses > 3:
            return 0
        return self.num_houses

    def get_num_hotels(self):
        """
        Getter for the number of hotels on this property.
        """
        return max([self.num_houses - 3, 0])

    def get_sale_price(self):
        """
        Getter for the sale price of this property.
        """
        return (self.purchase_value + self.num_houses * self.house_cost) / 2

class Go(Tile):
    """
    Represents the Go square on the Board.
    """
    def __init__(self):
        Tile.__init__(self)

class GoToJail(Tile):
    """
    Represents the Go To Jail square on the Board.
    """
    def __init__(self):
        Tile.__init__(self)

class CardTile(Tile):
    """
    Represents the Chance and Community Chest squares on the Board.
    """
    def __init__(self, card_type):
        Tile.__init__(self)
        self.card_type = card_type

    def pick_card(self):
        """
        Chooses a card randomly based on what type of tile this square is.

        Returns:
            (int, [str, ...]):      Tuple with the first element being the number of the selected card, and the second
                                        element being a list of text to display in the menu.
        """
        choice = random.randint(1, 16)

        if self.card_type == "Community Chest":
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
                return choice, ["Community Chest:", "Grand Opera Night", "Collect $ 50 from every", "player for opening night", "seats"]
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
        elif self.card_type == "Chance":
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
                return choice, ["Chance:", "Make general repairs", "on all your properties", "$ 25 for each house", "$ 100 for each hotel"]
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
    """
    Represents the Jail square on the Board.
    """
    def __init__(self):
        Tile.__init__(self)


class FreeParking(Tile):
    """
    Represents the Free Parking square on the Board.
    """
    def __init__(self):
        Tile.__init__(self)


class Tax(Tile):
    """
    Represents the Luxury Tax and Income Tax squares on the board.
    """
    def __init__(self, tax):
        Tile.__init__(self)
        self.tax = tax

    def get_tax(self):
        """
        Getter for the value this square charges.
        """
        return self.tax