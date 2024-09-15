from player import Player
from constant import *
from deck import Deck
# from timer import Timer
import pygame

from pygame.time import get_ticks

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False
    
    def activate(self):
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()




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


    


            
        

        