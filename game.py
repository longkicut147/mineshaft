from player import Player
from constant import *
from deck import Deck
from timer import Timer
import pygame

class Game(Player):
    def __init__(self, player_A, player_B, player_C, player_D):
        self.player_alive = [player_A, player_B, player_C, player_D]
        self.num_player = len(self.player_alive)
        self.current_player = 0


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


    def player_turn(self):
        chat_log.append(f"{self.player_alive[self.current_player].name}'s turn start.")
        # bắt đầu lượt -> đếm giờ -> sau 10 giây hết lượt
        time = Timer(10)
        time.activate()


        time.deactivate()
        chat_log.append(f"{self.player_alive[self.current_player].name}'s turn end.")
        self.current_player = (self.current_player + 1) % self.num_player


    def round(self):
        if len(self.player_alive) ==1:
            chat_log.append("game, set.")
        else:
            self.player_turn()


            
        

        