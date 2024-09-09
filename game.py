from player import Player
from deck import Deck




class Game(Player):
    def __init__(self, player_A, player_B, player_C, player_D):
        self.player_alive = [player_A, player_B, player_C, player_D]
        self.current = 0

    def round(self):
        while len(self.player_alive) > 1:
            self.player_alive = [player for player in self.player_alive if player.alive]
            for _ in range(len(self.player_alive)):
                # đến lượt người chơi hiện tại
                current_player = self.player_alive[self.current]
                print("{}'s turn!".format(current_player.name))
                other_player = [player for player in self.player_alive if player != current_player]

                current_player.gold += 1
                # đối tượng của hành động là bản thân hoặc các người chơi khác
                current_player.move(current_player, other_player)

                # tăng "hiện tại" lên 1 -> "tiếp theo"
                self.current = (self.current + 1) % len(self.player_alive)


    def setup(self):
        # chuẩn bị bài và chia bài
        ch_deck = Deck()
        wc_deck = Deck()
        ch_deck.build_char_deck()
        wc_deck.build_wildcard_deck()
        ch_deck.shuffle()
        wc_deck.shuffle()
        for player in self.player_alive:
            player.get_ch_card(ch_deck)
            player.get_wc_card(wc_deck)


            
        

        