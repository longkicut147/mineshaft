import pygame
import sys
from constant import *
from player import Player
from deck import Deck


# Initialize Pygame
pygame.init()

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

    def game_setup(self):
        ch_deck = Deck()
        wc_deck = Deck()
        ch_deck.build_char_deck()
        wc_deck.build_wildcard_deck()
        ch_deck.shuffle()
        wc_deck.shuffle()
        for player in game.player_alive:
            player.get_ch_card(ch_deck)
            player.get_wc_card(wc_deck)

# Set screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board game niga")

# Set font
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Set chat log
chat_log = []

# Player data
player_A = Player("long pakistan")
player_B = Player("long da den")
player_C = Player("long da trang")
player_D = Player("long da vang")
game = Game(player_A, player_B, player_C, player_D)
def players_stats():
    global players
    players = [
        {"color": BLACK, "name": player_A.name, "hp": player_A.hp, "gold": player_A.gold, "wild_card": len(player_A.wc_cards)},
        {"color": BLACK, "name": player_B.name, "hp": player_B.hp, "gold": player_B.gold, "wild_card": len(player_B.wc_cards)},
        {"color": BLACK, "name": player_C.name, "hp": player_C.hp, "gold": player_C.gold, "wild_card": len(player_C.wc_cards)},
        {"color": BLACK, "name": player_D.name, "hp": player_D.hp, "gold": player_D.gold, "wild_card": len(player_D.wc_cards)}
    ]



def draw_board():
    # Background color
    screen.fill(LIGHTGRAY)

    # Top Navigation Bar
    pygame.draw.rect(screen, GRAY, (0, 0, screen_width, screen_height/4))

    # Player areas
    for i, player in enumerate(players):
        # Area
        x = (i + 1) * spacing + i * player_width
        y = screen_height / 30
        pygame.draw.rect(screen, player["color"], (x, y, player_width, player_height))
        # Spacing
        text_spacing = player_height // 5
        # Text
        name_text = small_font.render(f"{player['name']}", True, WHITE)
        hp_text = small_font.render(f"HP: {player['hp']}", True, WHITE)
        gold_text = small_font.render(f"Gold: {player['gold']}", True, WHITE)
        wild_card_text = small_font.render(f"Wild Card: {player['wild_card']}", True, WHITE)
        # Draw
        screen.blit(name_text, (x + 10, y + 10))
        screen.blit(hp_text, (x + 10, y + 2 * text_spacing))
        screen.blit(gold_text, (x + 10, y + 3 * text_spacing))
        screen.blit(wild_card_text, (x + 10, y + 4 * text_spacing))

    # Main board 
    board_x = 50
    board_y = screen_height / 4 + 10
    board_width = screen_width - 100
    board_height = screen_height - (screen_height / 4 + 50)
    pygame.draw.rect(screen, BLACK, (board_x, board_y, board_width, board_height), 2)

    # Draw the dividing line for the deck
    deck_height = screen_height/12
    pygame.draw.line(screen, BLACK, (board_x, board_y + deck_height), (board_x + board_width-1, board_y + deck_height), 2)
    # Draw deck
    cards_in_ch_deck = small_font.render(f"{10} cards in character deck", True, BLACK)
    cards_in_wc_deck = small_font.render(f"{10} wild cards left", True, BLACK)
    screen.blit(cards_in_ch_deck, (board_x + 10, board_y + 10))
    screen.blit(cards_in_wc_deck, (board_x + 10, board_y + 10 + screen_height/30))

    # Chat area
    chat_x = board_x + 10
    chat_y = board_y + deck_height + 20  # Below the deck
    chat_width = board_width - 20
    chat_height = board_height - deck_height - 30
    # Chat surface
    chat_surface = pygame.Surface((chat_width, chat_height))
    chat_surface.fill(LIGHTGRAY)
    # Chat messages
    for i, line in enumerate(chat_log):
        chat_text = small_font.render(line, True, BLACK)
        chat_surface.blit(chat_text, (10, i * 30 + scroll_y))
    # Draw chat surface
    screen.blit(chat_surface, (chat_x, chat_y))




# Main loop
def main():
    global scroll_y
    running = True

    game.game_setup()
    # ch_deck = Deck()
    # wc_deck = Deck()
    # ch_deck.build_char_deck()
    # wc_deck.build_wildcard_deck()
    # ch_deck.shuffle()
    # wc_deck.shuffle()
    # for player in game.player_alive:
    #     player.get_ch_card(ch_deck)
    #     player.get_wc_card(wc_deck)
    # update players stats
    players_stats()

    chat_log.append(f"chao mung {len(game.player_alive)} nguoi choi")

    while running:
        for event in pygame.event.get():
            # Event quit game
            if event.type == pygame.QUIT:
                running = False
            # Event mouse scroll
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Scroll down
                    scroll_y = max(scroll_y - scroll_speed, -(len(chat_log) * 30 - (screen_height - screen_height / 4 - 60)))  # Limit scroll up
                elif event.button == 4:  # Scroll up
                    scroll_y = min(scroll_y + scroll_speed, 0)  # limit scroll down



        draw_board()
        pygame.display.flip()

    # running = False -> tắt
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
