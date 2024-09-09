from mineshaft.player import Player
from mineshaft.deck import Deck




class Game(Player):
    def __init__(self, player_A, player_B, player_C, player_D):
        self.player_alive = [player_A, player_B, player_C, player_D]
        self.current = 0


    def win_check(self):
        if len(self.player_alive) == 1:
            print("Winner: ", self.player_alive[0].show_name())
            return True
        else:
            return False
        # nếu chỉ còn 1 người sống thì ng đó thắng và sự kiện win là true -> end

    def alive_check(self):
        self.player_alive = [player for player in self.player_alive if player.alive]
        # print(len(self.player_alive))


    def status(self, num):
        for item in range(num):
            self.player_alive[item].show_name()
            self.player_alive[item].show_hp()
            self.player_alive[item].show_gold()
            print("")


    


    # mỗi vòng, mỗi người chơi có lượt đi
    def round(self):
        self.alive_check()

        for _ in range(len(self.player_alive)):
            # đến lượt người chơi hiện tại
            current_player = self.player_alive[self.current]
            print("{}'s turn!".format(current_player.name))
            other_player = [player for player in self.player_alive if player != current_player]

            current_player.gold += 1
            # đối tượng của hành động là bản thân hoặc các người chơi khác
            current_player.move(current_player, other_player)

            # hiện kết quả sau lượt
            self.status(len(self.player_alive))

            # tăng "hiện tại" lên 1 -> "tiếp theo"
            self.current = (self.current + 1) % len(self.player_alive)




    def play(self):

        ch_deck = Deck()
        wc_deck = Deck()
        ch_deck.build_char_deck()
        wc_deck.build_wildcard_deck()
        ch_deck.shuffle()
        wc_deck.shuffle()

        player_A.get_ch_card(ch_deck)
        player_A.get_wc_card(wc_deck)

        player_B.get_ch_card(ch_deck)
        player_B.get_wc_card(wc_deck)

        player_C.get_ch_card(ch_deck)
        player_C.get_wc_card(wc_deck)

        player_D.get_ch_card(ch_deck)
        player_D.get_wc_card(wc_deck)


        while self.win_check() == False:
            self.round()


player_A = Player("long pakistan")
player_B = Player("long da den")
player_C = Player("long da trang")
player_D = Player("long da vang")
game = Game(player_A, player_B, player_C, player_D)
# game.play()

            
        

        