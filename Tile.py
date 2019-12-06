import random

class Tile:
    def onLand(self, player):
        raise NotImplementedError


# initialize numHouses to 0 in main
class Property(Tile):
    def __init__(self, purchaseValue, name, rent, group, house_cost=None):
        Tile.__init__(self)
        self.name = name
        self.purchaseValue = purchaseValue
        self.mortgaged = False
        self.group = group
        self.owner = None
        self.rent = rent
        self.numHouses = 0
        self.house_cost = house_cost

    def setOwner(self, owner):
        self.owner = owner

    def setPurchaseValue(self, value):
        self.purchaseValue = value

    def setGroup(self, group):
        self.group = group

    def setName(self, name):
        self.name = name

    def setRent(self, rent):
        self.rent = rent

    def setHouseCost(self, house_cost):
        self.house_cost = house_cost

    def getOwner(self):
        return self.owner

    def getPurchaseValue(self):
        return self.purchaseValue

    def getGroup(self):
        return self.group

    def getName(self):
        return self.name

    def getRent(self):
        return self.rent

    def getHouseCost(self):
        return self.house_cost

    def addHouse(self):
        if self.numHouses < 4:
            self.numHouses += 1

    def getNumHouses(self):
        if self.numHouses > 3:
            return self.numHouses - 1
        return self.numHouses

    def getNumHotels(self):
        return max([self.numHouses - 3, 0])

    def onLand(self, player):
        return self
        # print("You have reached " + self.getName())
        # if self.owner is None:
        #     playerAnswer = input("Would you like to purchase " + self.getName() + " ? Y/N ")
        #     if playerAnswer == 'Y':
        #         if player.getMoney() >= self.getPurchaseValue():
        #             player.takeMoney(self.getPurchaseValue())
        #             player.addProperty(self)
        #             self.owner = player
        #         else:
        #             print("You cannot afford this property.")
        #     elif playerAnswer == 'N':
        #         None
        # elif self.getOwner().getName() == player.getName():
        #     playerAnswer2 = input("Would you like to build a house? Y/N ")
        #     if playerAnswer2 == 'Y':
        #         self.numHouses += 1;
        #     else:
        #         None
        # else:
        #     print("This property is owned by " + self.getOwner().getName())
        #     debt = player.takeMoney(self.rent[self.getNumHouses()])
        #     if debt == 0:
        #         print("You paid rent!")
        #     else:
        #         print("You owe " + debt)
        #         print("You must sell one of your properties back to the bank")
        #     self.getOwner().giveMoney(self.rent[self.getNumHouses()])

            
        


class Go(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You passed GO")
        player.give_money(200)


class Parking(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("Free parking!")

# TODO: flesh out functionality
class GoToJail(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You've reached the Go to Jail tile")
        if player.get_jail_card():
            player.remove_jail_card()
            print("You used your get out of jail card!")
        else:
            player.go_to_jail()
        pass

class CardTile(Tile):  # TODO: argument for card type
    def __init__(self, cardType):
        Tile.__init__(self)
        self.cardType = cardType

    def pickCard(self):
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
                return choice, ["Chance:", "Advance to", "nearest Utility", "If owned, throw dice", "Pay the owner 10 time", "the amount rolled"]
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

    def onLand(self, player):
        print("You reached the community chest")
        pass

class Jail(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached the Jail Tile")
        pass


class FreeParking(Tile):
    def __init__(self):
        Tile.__init__(self)

    def onLand(self, player):
        print("You reached Free Parking")
        pass


class Tax(Tile):  # TODO: argument for tax type
    def __init__(self, tax):
        Tile.__init__(self)
        self.tax = tax

    def getType(self):
        return self.tax

    def onLand(self, player):
        print("You reached Tax")
        pass