from mineshaft.cards import*
import random



class Deck:
    def __init__(self):
        self.deck = []

    def build_char_deck(self):
        for ch in ["miner", "tanker", "thief", "swordman"]:
            # 4 người thì có 8 thẻ nhân vật
            for i in range(2):
                self.deck.append(Card(ch))

    def build_wildcard_deck(self):
        for wc in ["disguise", "shield", "swap", "gun", "discard"]:
            # và 5 thẻ wild card
            self.deck.append(Card(wc))

    def show(self):
        for card in self.deck:
            card.show()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
    