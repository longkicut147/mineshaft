import pygame
import sys
from constant import *
from player import Player
from deck import Deck
from game import Game, Timer

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board game Mineshaft")

# Set font
font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Player data
player_A = Player("A")
player_B = Player("B")
player_C = Player("C")
player_D = Player("D")
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
        x = (i + 1) * spacing + i * player_width
        y = screen_height / 30
        pygame.draw.rect(screen, player["color"], (x, y, player_width, player_height))
        text_spacing = player_height // 5
        name_text = small_font.render(f"{player['name']}", True, WHITE)
        hp_text = small_font.render(f"HP: {player['hp']}", True, WHITE)
        gold_text = small_font.render(f"Gold: {player['gold']}", True, WHITE)
        wild_card_text = small_font.render(f"Wild Card: {player['wild_card']}", True, WHITE)
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

    # Draw deck dividing line and card details
    deck_height = screen_height/12
    pygame.draw.line(screen, BLACK, (board_x, board_y + deck_height), (board_x + board_width - 1, board_y + deck_height), 2)
    cards_in_ch_deck = small_font.render(f"{10} cards in character deck", True, BLACK)
    cards_in_wc_deck = small_font.render(f"{10} wild cards left", True, BLACK)
    screen.blit(cards_in_ch_deck, (board_x + 10, board_y + 10))
    screen.blit(cards_in_wc_deck, (board_x + 10, board_y + 10 + screen_height / 30))

    # Chat area
    chat_x = board_x + 10
    chat_y = board_y + deck_height + 20
    chat_width = board_width - 20
    chat_height = board_height - deck_height - 80
    chat_surface = pygame.Surface((chat_width, chat_height))
    chat_surface.fill(LIGHTGRAY)

    # Calculate maximum scroll position
    max_scroll_y = -(len(chat_log) * 30 - chat_height)

    # Auto-scroll only if at the bottom or new message is added
    if auto_scroll:
        scroll_y = max_scroll_y

    # Chat messages
    for i, line in enumerate(chat_log):
        chat_text = small_font.render(line, True, BLACK)
        chat_surface.blit(chat_text, (10, i * 30 + scroll_y))

    # Draw chat surface
    screen.blit(chat_surface, (chat_x, chat_y))

    # Chat input bar with border
    input_bar_y = chat_y + chat_height + 10
    pygame.draw.rect(screen, BLACK, (chat_x, input_bar_y, chat_width, 30), 2)
    pygame.draw.rect(screen, WHITE, (chat_x + 2, input_bar_y + 2, chat_width - 4, 26))

    # Render chat input
    chat_input_text = small_font.render(chat_input, True, BLACK)
    screen.blit(chat_input_text, (chat_x + 5, input_bar_y + 5))

    # Blinking cursor
    if cursor_visible:
        cursor_x = chat_x + 5 + small_font.size(chat_input)[0]
        pygame.draw.line(screen, BLACK, (cursor_x, input_bar_y + 5), (cursor_x, input_bar_y + 25), 2)
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
    running = True
    chat_input = ""
    
    # chat_log scroll movement
    global scroll_y
    global auto_scroll
    scroll_y = 0
    cursor_visible = True  # Controls whether the cursor is visible
    cursor_timer = 0       # Timer to handle blinking cursor
    auto_scroll = True     # Auto scroll when new messages added


    # set up
    game.game_setup()
    players_stats()
    chat_log.append(f"chao mung {len(game.player_alive)} nguoi choi")

    phase1 = True
    choice_phase = False
    choice_time = Timer(10000)

    phase2 = False
    trust_phase = False
    trust_time = Timer(10000)


    # main loop
    while running:
        current_player = game.player_alive[game.current]
        choices = [Player.skip, Player.miner, Player.heal, Player.disguise,
                Player.thief, Player.swap, Player.discard, Player.gun, Player.swordman, Player.attack]
        other_players = [player for player in game.player_alive if player != current_player]

        # event handle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if chat_input.strip():
                        current_player.input.append(chat_input.strip())
                        chat_input = ""  # Clear input after sending
                        auto_scroll = True  # Re-enable auto-scroll on new message
                elif event.key == pygame.K_BACKSPACE:
                    chat_input = chat_input[:-1]
                else:
                    chat_input += event.unicode

        # Blinking cursor logic
        cursor_timer += 1
        if cursor_timer >= 30:  # Blink every half a second (assuming 60 FPS)
            cursor_visible = not cursor_visible
            cursor_timer = 0

        
        # game logic
        if len(game.player_alive) ==1:
            chat_log.append("game, set.")
        if phase1:
            if not choice_phase:
                chat_log.append(f"{current_player.name}'s turn start, make your choice:")
                choice_phase = True  # Đánh dấu lượt đã bắt đầu
                choice_time.activate()  # Bắt đầu đếm thời gian lượt

            # Cập nhật timer để kết thúc lượt khi đủ thời gian
            choice_time.update()

            if not choice_time.active: # khi hết thời gian đếm
                # bước 1: chọn hành động 
                choices = [Player.skip, Player.miner, Player.heal, Player.disguise,
                        Player.thief, Player.swap, Player.discard, Player.gun, Player.swordman, Player.attack]
                other_players = [player for player in game.player_alive if player != current_player]

                if len(current_player.input) == 2:
                    # kiểm tra 2 giá trị người chơi nhập vào có đúng cú pháp "hành động Enter đối tượng" không
                    if current_player.input[0] in [i.__name__ for i in choices] and current_player.input[1] in [i.name for i in other_players]:
                        choice = current_player.input[0]
                        for i in choices:
                            if choice == i.__name__:
                                choice = i
                        # nếu các lựa chọn cần đối tượng thì chọn dối tượng
                        if choice in [Player.swordman, Player.thief, Player.swap, Player.discard, Player.gun, Player.attack]:
                            opponent = current_player.input[1]
                            for i in other_players:
                                if opponent == i.name:
                                    opponent = i
                            if choice in [Player.swordman, Player.thief]:
                                choice(current_player, opponent)
                                chat_log.append(f"{current_player.name} use {choice.__name__} to {opponent.name}")
                                phase1 = False
                                phase2 = True
                            else:
                                choice(current_player, opponent)
                                chat_log.append(f"{current_player.name} use {choice.__name__} to {opponent.name}")
                                chat_log.append(f"{current_player.name}'s turn end.")
                                chat_log.append("")
                                current_player.input.clear()
                                game.current = (game.current + 1) % game.num_player
                                choice_phase = False
                                trust_phase = False
                                players_stats()
                        else:
                            # nếu muốn chọn các hành động không cần đối tượng mà nhập 2 giá trị thì không cần dùng opponent
                            if choice in [Player.miner]:
                                choice(current_player)
                                chat_log.append(f"{current_player.name} use {choice.__name__}")
                                phase1 = False
                                phase2 = True
                            else:
                                choice(current_player)
                                chat_log.append(f"{current_player.name} use {choice.__name__}")
                                chat_log.append(f"{current_player.name}'s turn end.")
                                chat_log.append("")
                                current_player.input.clear()
                                game.current = (game.current + 1) % game.num_player
                                choice_phase = False
                                trust_phase = False
                                players_stats()
                    else:
                        chat_log.append(f"{current_player.name} syntax error, use skip instead")
                        current_player.skip()
                        chat_log.append(f"{current_player.name}'s turn end.")
                        chat_log.append("")
                        current_player.input.clear()
                        game.current = (game.current + 1) % game.num_player
                        choice_phase = False
                        trust_phase = False
                        players_stats()

                elif len(current_player.input) == 1:
                    # kiểm tra 1 gia trị người chơi nhập vào có nằm trong mục hành động không
                    if current_player.input[0] in [i.__name__ for i in choices]:
                        choice = current_player.input[0]
                        for i in choices:
                            if choice == i.__name__:
                                choice = i                    
                        # nếu muốn chọn các hành động cần đối tượng mà chỉ nhập 1 giá trị thì skip vì lỗi
                        if choice in [Player.swordman, Player.thief, Player.swap, Player.discard, Player.gun, Player.attack]:
                            chat_log.append(f"{current_player.name} syntax error, use skip instead")
                            current_player.skip()
                            chat_log.append(f"{current_player.name}'s turn end.")
                            chat_log.append("")
                            current_player.input.clear()
                            game.current = (game.current + 1) % game.num_player
                            choice_phase = False
                            trust_phase = False
                            players_stats()
                        elif choice in [Player.miner]:
                            choice(current_player)
                            chat_log.append(f"{current_player.name} use {choice.__name__}")
                            phase1 = False
                            phase2 = True
                        else:
                            choice(current_player)
                            chat_log.append(f"{current_player.name} use {choice.__name__}")
                            chat_log.append(f"{current_player.name}'s turn end.")
                            chat_log.append("")
                            current_player.input.clear()
                            game.current = (game.current + 1) % game.num_player
                            choice_phase = False
                            trust_phase = False
                            players_stats()
                    else:
                        chat_log.append(f"{current_player.name} syntax error, use skip instead")
                        current_player.skip()
                        chat_log.append(f"{current_player.name}'s turn end.")
                        chat_log.append("")
                        current_player.input.clear()
                        game.current = (game.current + 1) % game.num_player
                        choice_phase = False
                        trust_phase = False
                        players_stats()

                # nếu hết thời gian mà không nhập gì hoặc nhập quá nhiều hoặc nhập linh tinh thì mặc định là skip
                else:
                    chat_log.append("Time's out")
                    current_player.skip()
                    chat_log.append(f"{current_player.name}'s turn end.")
                    chat_log.append("")
                    current_player.input.clear()
                    game.current = (game.current + 1) % game.num_player
                    choice_phase = False
                    trust_phase = False
                    players_stats()
                

        if phase2:
            if not trust_phase:
                chat_log.append(f"Believe {current_player.name}?")
                trust_phase = True  # Đánh dấu lượt đã bắt đầu
                trust_time.activate()  # Bắt đầu đếm thời gian lượt

            # Cập nhật timer để kết thúc lượt khi đủ thời gian
            trust_time.update()

            if not trust_time.active: # khi hết thời gian đếm
                chat_log.append("pass")

                # chuyển sang người chơi tiếp theo và reset tất cả lại từ đầu
                chat_log.append(f"{current_player.name}'s turn end.")
                chat_log.append("")
                current_player.input.clear()
                game.current = (game.current + 1) % game.num_player
                phase1 = True
                phase2 = False
                choice_phase = False
                trust_phase = False
                players_stats()



        # Draw the board including the chat and input bar with a cursor
        # players_stats()
        draw_board(chat_input, cursor_visible)
        pygame.display.flip()
        
        # FPS
        clock.tick(FPS)

        
    # Running = False -> Close game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
