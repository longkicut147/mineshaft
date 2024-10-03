import action as action
from player import Player
from game import Game

import random
import os

Players = []
player_alive = []
current_player = 0

available_action = []

class TERMINAL(Player):
    show_block_options = True         # global variable to show possible options for blocking. set to True every turn


    def confirm_check_lie(self, active_player, action): 
        if len(player_alive) > 2:
            longestName = [len(player.name) for player in player_alive]
            longestName = max(longestName)            
            name = self.name + "," + (" " * (longestName - len(self.name)))
        else:
            name = self.name + ","
        
        choice = input("%s check if %s is lying? (Y/N)? " % (name, active_player.name))
        choice = choice.upper()
        
        # if syntax is wrong, ask again
        if not choice.strip() in ('Y', 'N', ''):
            print("\n Type Y to check. \n Type N or enter to allow.\n")
            return self.confirm_check_lie(active_player, action)
            
        if choice == 'Y':
            return True

        return False 
            

    def confirm_block(self, active_player, opponent_action):
        # returns action player uses to block action. return None if player allows action
        card_blockers = []
        
        for card in Game.char_cards:
            if opponent_action.name in card.blocks:
                card_blockers.append(card)

        blockers = len(card_blockers) + 1   # +1 for the option to not block
        
        if TERMINAL.show_block_options:
            TERMINAL.show_block_options = False            
            
            print("\n%s can be blocked with:" % (opponent_action.name))
            for i, card in enumerate(card_blockers):
                print(" %i: %s" % (i + 1, card.name))
            print(" %i: Allow\n" % (blockers))            
        
        # draw to terminal
        if len(player_alive) > 2:
            longestName = [len(player.name) for player in player_alive]
            longestName = max(longestName)
            name = self.name + "," + (" " * (longestName - len(self.name)))
        else:
            name = self.name + ","
        

        choice = input("%s do you want to block %s? " % (name, opponent_action.name))
        choice = choice.strip()
        if choice == "":
            choice = str(blockers)      # do not block
        
        if not choice.isnumeric():
            print(" Select a number between 1-%i. Or enter to allow" % blockers)
            return self.confirm_block(active_player, opponent_action)
        choice = int(choice) - 1
        
        if choice == len(card_blockers):
            return None         # player decides not to block
        
        if not (choice >= 0 and choice < len(card_blockers)):
            print(" Select a number between 1-%i. Press enter to allow %s's %s." % (blockers, active_player.name, opponent_action.name))
            return self.confirm_block(active_player, opponent_action)
            
        block = card_blockers[choice - 1]
        
        print("\n\n%s is blocking with %s" % (self.name, block.name))
        return block


def clear_screen(headerMessage, headerSize = 10):
    os.system('cls' if os.name == 'nt' else 'clear')
    dic = {
    '\\' : b'\xe2\x95\x9a',
    '-'  : b'\xe2\x95\x90',
    '/'  : b'\xe2\x95\x9d',
    '|'  : b'\xe2\x95\x91',
    '+'  : b'\xe2\x95\x94',
    '%'  : b'\xe2\x95\x97',
    }

    def decode(x):
        return (''.join(dic.get(i, i.encode('utf-8')).decode('utf-8') for i in x))

    print(decode("+%s%%" % ('-' * headerSize)))
    print(decode("|%s|"  % (headerMessage.center(headerSize))))
    print(decode("\\%s/" % ('-' * headerSize)))
        

def Print_Deck():
    print("There are %i cards in the character Deck" % (len(Game.char_Deck)))
    print("There are %i cards in the wildcard Deck"% (len(Game.wild_Deck)))


def Print_revealed_cards():
    size = len(Game.dead_char_cards)
    if size == 0:
        return
        
    print("\nThere are %i cards that has been revealed:" % (size))

    reveals = [card.name for card in Game.dead_char_cards]
    reveals.sort()
    for card in reveals:
        print("   ", card)


def Print_actions():
    for i, action in enumerate(available_action):
        if action.name != "Tanker":
            print(" %i: %s" % (i + 1, action.name))
    print(" X: Exit the game")

        
def setup_actions():
    global available_action
    available_action = [action.Dig, action.Attack, action.Buy,
                        action.Miner, action.Thief, action.Swordman, action.Tanker,
                        action.Disguise, action.Discard, action.Swap, action.Gun, action.Heal]
    

def setup_game():
    # Generate the player list
    # Shuffle the player list    
    Game.reset()
    setup_actions()
        
    numberof_player = 4
    
    def create_player(number):
        player = TERMINAL()
        player.name = input("Player #%i: What is your name? " % (number + 1))
        if player.name.strip() == "":
            return create_player(number)
        return player

    print("\n")
    for i in range(numberof_player):
        Players.append(create_player(i))

    global player_alive
    player_alive = [player for player in Players if player.alive]
    

# main loop
def game():

    global player_alive, current_player, Running
    
    Running = True
    while Running and len(player_alive) > 1:
        player = Players[current_player]
        TERMINAL.show_block_options = True
        
        def Print_player_status():            
            Player_list = Players[current_player:] + Players[0:current_player]
            paddingWidth = 16
            headerList = []
            rowWidth = 0
            

            headerStr = ""
            for player_info in Player_list:            
                name = player_info.name 
                if len(name) > paddingWidth - 4: 
                    name = name[:paddingWidth - 4] + "... "
                
                padding = " " * (paddingWidth - len(name))
                headerStr += name + padding

            headerStr = headerStr.rstrip()
            rowWidth = max(rowWidth, len(headerStr) + 4)
            headerStr = "  " + headerStr
            headerList.append(headerStr)
            

            goldStr = ""
            for player_info in Player_list:            
                gold = "gold: %2i" % (player_info.gold)
                padding = " " * (paddingWidth - len(gold))
                goldStr += gold + padding
            
            goldStr = "  " + goldStr.rstrip()
            rowWidth = max(rowWidth, len(goldStr))
            headerList.append(goldStr)


            hpStr = ""
            for player_info in Player_list:            
                hp = "hp:   %2i" % (player_info.hp)
                padding = " " * (paddingWidth - len(hp))
                hpStr += hp + padding
            
            hpStr = "  " + hpStr.rstrip()
            rowWidth = max(rowWidth, len(hpStr))
            headerList.append(hpStr)
            

            headerStr = "  ________" + (paddingWidth * " ")
            rowWidth = max(rowWidth, len(headerStr))
            headerList.append(headerStr)
            
            for i, header in enumerate(headerList):
                headerList[i] += " " * (rowWidth - len(headerList[i]))
            

            clear_screen("|\n|".join(headerList), rowWidth)
            print("")
            Print_Deck()
            Print_revealed_cards()
            print("\n%s's cards are: " % (player.name))
            player_char_card = " and ".join([card.name for card in player.char_card])
            print("    " + player_char_card)
            player_wild_cards = " and ".join([card.name for card in player.wild_cards])
            print("    " + player_wild_cards)

        
        def change_turn():
            global current_player
            current_player += 1
            # reset to first player if loop out of 4
            if current_player >= len(Players): 
                current_player = 0
            
            global player_alive 
            player_alive = [player for player in Players if player.alive]
        

        def choose_action():    
            choice = input ("Action: ")
            if not choice.isnumeric():
                if choice.upper() == "X":
                    confirm = input ("\nAre you sure you want to exit (Y/N)? ")
                    if confirm.upper() != "Y":                      
                        choose_action()
                        return  
                    global Running    
                    Running = False
                    return
                choose_action()
                return
            
            choice = int(choice) - 1
            if not (choice >= 0 and choice < len(available_action)):
                choose_action()
                return
            
            status = False
            
            def choose_target():
                targets = list(Players)
                targets.remove(player)
                targets = [player for player in targets if player.alive]
                # if only 2 players left then the only target is opponent
                if len(targets) == 1:
                    return targets[0]
                
                print("")
                for i, iter_player in enumerate(targets):
                    print(" %i: %s" % (i + 1, iter_player.name))
                target = input ("Choose a target: ")
                
                if not target.isnumeric():
                    return choose_target()
                target = int(target) - 1
                if target < 0 or target >= len(targets):
                    return choose_target()
                
                return targets[target]


            def choose_card():
                cards = Game.char_cards

                print("")
                for i, iter_card in enumerate(cards):
                    print(" %i: %s" % (i + 1, iter_card.name))
                card = input ("Guess player's character card: ")

                if not card.isnumeric():
                    return choose_card()
                card = int(card) - 1
                if card < 0 or card >= len(cards):
                    return choose_card()
                
                return cards[card]


            if player.gold < available_action[choice].gold_required:
                print(" You need %i gold to %s. You only have %i gold." % (available_action[choice].gold_required, available_action[choice].name, player.gold))
                choose_action()
                return
            
            if player.hp < available_action[choice].hp_required:
                print(" You need %i hp to %s. You only have %i hp." % (available_action[choice].hp_required, available_action[choice].name, player.hp))
                choose_action()
                return
                
            if player.gold >= action.Force_to_Attack and available_action[choice].name != "Attack":
                print("Player has %i gold. Must use attack" % (player.gold))
                choose_action()
                return            
            

            target = None
            if available_action[choice].hasTarget:
                target = choose_target()
            
            card = None
            if available_action[choice].chooseCard:
                card = choose_card()

            try:
                header = []
                headerStr = "%s's action is %s" % (player.name, available_action[choice].name)
                headerLen = len(headerStr) + 4
                headerStr = headerStr.center(headerLen)
                header.append(headerStr)
                
                if not target is None:
                    headerStr = " (target: %s)" % (target.name)
                    headerStr += " " * (headerLen - len(headerStr))
                    header.append(headerStr)
                
                clear_screen("|\n|".join(header), headerLen)
                
                print("")
                status, response = player.play(available_action[choice], target, card)

            except action.ActionNotAllowed as e:
                print(e.message)
                choose_action()
                return
            except action.NotEnoughGold as exc:
                print(" You need %i gold to %s. You only have %i gold." % (exc.gold_required, available_action[choice].name, player.gold))
                choose_action()
                return
            except action.NotEnoughHP as exc:
                print(" You need %i hp to %s. You only have %i hp." % (exc.hp_required, available_action[choice].name, player.hp))
                choose_action()
                return
            except action.BlockOnly:
                print("You cannot play %s as an action" % (available_action[choice].name))
                choose_action()
                return
            except action.TargetRequired:
                print("You need to select a target.\n")
                Print_actions()
                choose_action()
                return
            except action.DontHaveCard:
                print("You don't have that wildcard.\n")
                Print_actions()
                choose_action()
                return
                            
            if status == False:
                print(response)


        if player.alive:
            Print_player_status()
            print("\nAvailable actions:")
            Print_actions()
            choose_action()
            
        change_turn()

        if Running: 
            input("\n%s, press enter to take your turn..." % Players[current_player].name)
        
    if len(player_alive) == 1: 
        clear_screen("The winner is %s" % (player_alive[0].name), 79)



 
def main():
    clear_screen("Game setup", 50)
    setup_game()
    clear_screen("Game start", 50)

    input("\n%s, press enter to start the game..." % (Players[0].name))
    game()
    
if __name__ == "__main__":
    main()