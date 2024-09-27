from deck import*
from game import Game


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = "name"
        self.ch_card = Game.deal_card()
        # self.wc_cards = []
        self.gold = 1
        self.hp = 10
        self.alive = True
        Game.player_list.append(self)


    # nhận sát thương
    def take_damage(self, damage):
        if self.alive == True:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                # nếu máu về 0 thì chết
                self.alive = False
                Game.dead_char_cards.append(loses)
    


    # # các chức năng có thể sử dụng
    # def skip(self):
    #     if self.gold < 7:
    #         self.earn(1)
    #     else:
    #         self.earn(0)

    # def miner(self):
    #     if self.gold < 7:
    #         self.earn(2)
    #     else:
    #         self.earn(0)


    # def swordman(self, opponent):
    #     if self.hp > 1 and opponent.name != "tanker":
    #         self.take_damage(1)
    #         opponent.take_damage(5)
    #     else:
    #         print("can't swordman")

    # def thief(self, opponent):
    #     if opponent.gold >= 1 and opponent.name != "tanker":
    #         self.earn(1)
    #         opponent.spend(1)
    #     else:
    #         print("can't thief")

    # def disguise(self):
    #     if "disguise" in self.wc_cards:
    #         self.ch_cards.pop()
    #         self.get_ch_card(self.ch_deck)
    #         self.wc_cards.remove("disguise")
    #     else:
    #         print("you don't have disguise")

    # def swap(self, opponent):
    #     if "swap" in self.wc_cards:
    #         self.ch_cards[0], opponent.ch_cards[0] = opponent.ch_cards[0], self.ch_cards[0]
    #         self.wc_cards.remove("swap")
    #     else:
    #         print("you don't have swap")

    # def discard(self, opponent):
    #     if "discard" in self.wc_cards:
    #         opponent.ch_cards.pop()
    #         opponent.get_ch_card(self.ch_deck)
    #         self.wc_cards.remove("discard")
    #     else:
    #         print("you don't have discard")

    # def gun(self, opponent):
    #     if "gun" in self.wc_cards:
    #         card = str(input("guess opponent's card: "))
    #         if card == opponent.ch_cards[0]:
    #             opponent.take_damage(5)
    #         self.wc_cards.remove("gun")
    #     else:
    #         print("you don't have gun")

    # def heal(self):
    #     if "heal" in self.wc_cards:
    #         if self.hp <6:
    #             self.hp = 8
    #         else:
    #             self.hp = 10
    #         self.wc_cards.remove("heal")
    #     else:
    #         print("you don't have heal")

    # def attack(self, opponent):
    #     if self.gold >= 7:
    #         self.gold -= 7
    #         opponent.take_damage(5)
    #     else:
    #         print("not enough gold")        


        

