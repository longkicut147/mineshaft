import pygame
import sys
from constant import *
from player import Player
from deck import Deck
from game import Game

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board game niga")

# Set font
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Player data
player_A = Player("sau")
player_B = Player("loi")
player_C = Player("tu")
player_D = Player("khuoc")
game = Game(player_A, player_B, player_C, player_D)

def players_stats():
    global players
    players = [
        {"color": BLACK, "name": player_A.name, "hp": player_A.hp, "gold": player_A.gold, "wild_card": len(player_A.wc_cards)},
        {"color": BLACK, "name": player_B.name, "hp": player_B.hp, "gold": player_B.gold, "wild_card": len(player_B.wc_cards)},
        {"color": BLACK, "name": player_C.name, "hp": player_C.hp, "gold": player_C.gold, "wild_card": len(player_C.wc_cards)},
        {"color": BLACK, "name": player_D.name, "hp": player_D.hp, "gold": player_D.gold, "wild_card": len(player_D.wc_cards)}
    ]

# Function to draw the game board
def draw_board(chat_input, cursor_visible):
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
    chat_height = board_height - deck_height - 80  # Adjust height to accommodate input bar
    # Chat surface
    chat_surface = pygame.Surface((chat_width, chat_height))
    chat_surface.fill(LIGHTGRAY)
    # Chat messages
    for i, line in enumerate(chat_log):
        chat_text = small_font.render(line, True, BLACK)
        chat_surface.blit(chat_text, (10, i * 30 + scroll_y))
    # Draw chat surface
    screen.blit(chat_surface, (chat_x, chat_y))

    # Chat input bar with border
    input_bar_y = chat_y + chat_height + 10
    pygame.draw.rect(screen, BLACK, (chat_x, input_bar_y, chat_width, 30), 2)  # Black border
    pygame.draw.rect(screen, WHITE, (chat_x + 2, input_bar_y + 2, chat_width - 4, 26))  # White input area

    # Render chat input
    chat_input_text = small_font.render(chat_input, True, BLACK)
    screen.blit(chat_input_text, (chat_x + 5, input_bar_y + 5))

    # Blinking cursor
    if cursor_visible:
        cursor_x = chat_x + 5 + small_font.size(chat_input)[0]  # Cursor position at the end of the text
        pygame.draw.line(screen, BLACK, (cursor_x, input_bar_y + 5), (cursor_x, input_bar_y + 25), 2)  # Draw cursor

# Main loop
def main():
    global scroll_y
    chat_input = ""
    cursor_visible = True  # Controls whether the cursor is visible
    cursor_timer = 0       # Timer to handle blinking cursor
    running = True

    game.game_setup()
    players_stats()

    chat_log.append(f"chao mung {len(game.player_alive)} nguoi choi")

    while running:
        for event in pygame.event.get():
            # Event to quit game
            if event.type == pygame.QUIT:
                running = False
            # Event for mouse scroll
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:  # Scroll down
                    scroll_y = max(scroll_y - scroll_speed, -(len(chat_log) * 30 - (screen_height - screen_height / 4 - 60)))  # Limit scroll up
                elif event.button == 4:  # Scroll up
                    scroll_y = min(scroll_y + scroll_speed, 0)  # limit scroll down
            # Event for key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if chat_input.strip():
                        Player.input.append(chat_input.strip())
                    chat_input = ""  # Clear input after sending message
                elif event.key == pygame.K_BACKSPACE:
                    chat_input = chat_input[:-1]  # Remove last character
                else:
                    chat_input += event.unicode  # Add character to input

        # Blinking cursor logic
        cursor_timer += 1
        if cursor_timer >= 30:  # Blink every half a second (assuming 60 FPS)
            cursor_visible = not cursor_visible
            cursor_timer = 0

        
        game.round()

        # Draw the board including the chat and input bar with a cursor
        draw_board(chat_input, cursor_visible)
        pygame.display.flip()

        # FPS
        clock.tick(FPS)
    # Running = False -> Close game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
