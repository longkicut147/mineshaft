from mineshaft.deck import*


class Player:
    def __init__(self, name):
        self.name = name
        self.ch_cards = []
        self.wc_cards = []
        self.gold = 0
        self.hp = 10
        self.alive = True
        self.truth = True

    def show_name(self):
        print("{}".format(self.name))

    # lấy bài từ deck về bài của người chơi
    def get_ch_card(self, ch_deck):
        self.ch_cards.append(ch_deck.deal())
    
    def get_wc_card(self, wc_deck):
        self.wc_cards.append(wc_deck.deal())

    def show_card(self):
        for card in self.ch_cards:
            card.show()
        for card in self.wc_cards:
            card.show()

    # nhận sát thương
    def take_damage(self, damage):
        if self.alive == True:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                # nếu máu về 0 thì chết
                self.alive = False
    
    def show_hp(self):
        print("{}".format(self.hp))

    # nhận vàng
    def earn(self, e_gold):
        if self.gold + e_gold <= 7:
            self.gold += e_gold
        else:
            print("can't earn more gold")

    # tiêu vàng          
    def spend(self, s_gold):
        if self.gold - s_gold >= 0:
            self.gold -= s_gold
        else:
            print("not enough gold")

    def show_gold(self):
        print("{}".format(self.gold))


    # các chức năng có thể sử dụng
    def skip(self):
        pass

    def miner(self):
        if self.gold < 7:
            self.earn(1)
        else:
            self.earn(0)


    def swordman(self, opponent):
        if self.hp > 1 and opponent.name != "tanker":
            self.take_damage(1)
            opponent.take_damage(5)
        else:
            print("can't swordman")

    def thief(self, opponent):
        if opponent.gold >= 1 and opponent.name != "tanker":
            self.earn(1)
            opponent.spend(1)
        else:
            print("can't thief")

    def disguise(self):
        if "disguise" in self.wc_cards:
            self.ch_cards.pop()
            self.get_ch_card(self.ch_deck)
            self.wc_cards.remove("disguise")
        else:
            print("you don't have disguise")

    def swap(self, opponent):
        if "swap" in self.wc_cards:
            self.ch_cards[0], opponent.ch_cards[0] = opponent.ch_cards[0], self.ch_cards[0]
            self.wc_cards.remove("swap")
        else:
            print("you don't have swap")

    def discard(self, opponent):
        if "discard" in self.wc_cards:
            opponent.ch_cards.pop()
            opponent.get_ch_card(self.ch_deck)
            self.wc_cards.remove("discard")
        else:
            print("you don't have discard")

    def gun(self, opponent):
        if "gun" in self.wc_cards:
            card = str(input("guess opponent's card: "))
            if card == opponent.ch_cards[0]:
                opponent.take_damage(5)
            self.wc_cards.remove("gun")
        else:
            print("you don't have gun")

    def heal(self):
        if "heal" in self.wc_cards:
            if self.hp <6:
                self.hp = 8
            else:
                self.hp = 10
            self.wc_cards.remove("heal")
        else:
            print("you don't have heal")

    def buy_wc(self, wc_deck):
        if len(wc_deck)>0:
            self.get_wc_card(wc_deck)
            self.spend(3)
        else:
            print("wild card sold out")



    # chọn chức năng để sử dụng
    def move(self, current_player, other_player):

        # bước 1: chọn hành động
        choices = [self.skip, self.miner, self.swordman, self.thief, self.disguise,
                    self.swap, self.discard, self.gun, self.heal, self.buy_wc]
        i = int(input())
        choice = choices[i-1]
        # tạo tạm một list với tên của các method để đem so sánh khi kiểm tra nói dối
        choices_str = ["skip", "miner", "swordman", "thief", "disguise",
                    "swap", "discard", "gun", "heal", "buy_wc"]
        choice_str = choices_str[i-1]


        # bước 2: chọn đối tượng (nếu cần)
        if choice == self.swordman or choice == self.thief or choice == self.swap or choice == self.discard:
            opponent_choices = other_player
            j = int(input())
            opponent = opponent_choices[j-1]
        else:
            opponent = None


        # bước 3: kiểm tra nói dối (cho các hành động của character card)
        if choice == self.swordman or choice == self.thief or choice == self.miner:
            for player in range(len(other_player)):
                print(other_player[player].name, "kiểm tra? (0 là có tin, 1 là không tin): ")
                k = int(input())
                if k==1:
                    if choice_str != current_player.ch_cards[0].name:
                        # nếu nói dối, người đó trừ 4 máu và không được thực hiện hành động
                        current_player.take_damage(4)
                    else:
                        # nếu nói thật, người kiểm tra trừ 4 máu
                        other_player[player].take_damage(4)
                        # và được thực hiện hành động
                        if opponent:
                            choice(opponent)
                        else:
                            choice()
                    return
        else:
            pass


        

