from player import Player
from constant import *
from deck import Deck
import pygame



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
                other_player = [player for player in self.player_alive if player != current_player]
                # khi đến lượt thì cộng 1 vàng
                current_player.gold += 1
                chat_log.append(f"den luot {current_player.name}:")
                
                # bước 1: chọn hành động
                choices = [self.skip, self.miner, self.swordman, self.thief, self.disguise,
                            self.swap, self.discard, self.gun, self.heal, self.buy]
                chat_log.append(f"chon hanh dong muon lam: ")
                choice = current_player.input[-1]
                for i in choices:
                    if choice == i.__name__():
                        choice = i

                # bước 2: chọn đối tượng (nếu cần)
                if choice == self.swordman or choice == self.thief or choice == self.swap or choice == self.discard:
                    opponent_choices = other_player
                    chat_log.append(f"chon doi tuong muon {choice.__name__()}")
                    opponent = current_player.input[-1]
                    for i in opponent_choices:
                        if opponent == i.name:
                            opponent = i
                else:
                    opponent = None

                # bước 3: kiểm tra nói dối (cho các hành động của character card)
                if choice == self.swordman or choice == self.thief or choice == self.miner:
                    for player in range(len(other_player)):
                        chat_log.append(f"co tin {current_player} khong: ")
                        k = player.input[-1]
                        if k=="khong tin":
                            if choice != current_player.ch_cards[0].name:
                                # nếu nói dối, người đó trừ 4 máu và không được thực hiện hành động
                                current_player.take_damage(4)
                                return
                            else:
                                # nếu nói thật, người kiểm tra trừ 4 máu
                                other_player[player].take_damage(4)
                                # và được thực hiện hành động
                                if opponent:
                                    choice(opponent)
                                else:
                                    choice()
                                    return
                        elif k=="tin":
                            pass
                    choice()
                else:
                    pass

                # tăng "hiện tại" lên 1 -> "tiếp theo"
                self.current = (self.current + 1) % len(self.player_alive)


    def game_setup(self):
        ch_deck = Deck()
        wc_deck = Deck()
        ch_deck.build_char_deck()
        wc_deck.build_wildcard_deck()
        ch_deck.shuffle()
        wc_deck.shuffle()
        for player in self.player_alive:
            player.get_ch_card(ch_deck)
            player.get_wc_card(wc_deck)



            
        

        