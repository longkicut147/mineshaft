class Card:
    def __init__(self, name):
        self.name = name

    def show(self):
        print("{}".format(self.name))

class Char_card(Card):
    pass

class Wild_card(Card):
    pass