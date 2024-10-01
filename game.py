import random

from error import IndexError

class Game:
    def reset(self):
        self.player_list = []
        
        import action
        self.common_actions = [action.Dig, action.Attack]
        self.char_cards = [action.Miner, action.Thief, action.Swordman, action.Tanker]
        self.Deck = self.char_cards * 2
        self.randomShuffle = random.shuffle
        self.randomSelector = random.choice
        self.randomShuffle(self.Deck)

        self.dead_char_cards = []


    def request_block(self, current_player, action, target_player):
        """ 
        Ask each player if they want to block current player's action, the targetted player will be requested first.
        If someone wants to block, return the tuple (player, action). Else, return (None, None).
        """
        # change turn and bring the current_player to top of the list
        current_index = self.player_list.index(current_player)
        player_list = self.player_list[current_index:] + self.player_list[0:current_index]
        
        if target_player != None:
            # bring target_player to top of the list
            target_index = self.player_list.index(target_player)
            player_list.remove(target_player)
            player_list = [self.player_list[target_index]] + player_list
        
        for player in player_list:
            # other players (not current and dead player)
            if player == current_player or not player.alive: 
                continue
            
            blocking_action = player.confirm_block(current_player, action)
            if blocking_action != None: 
                # check if block is possible
                if not action.name in blocking_action.blocks:
                    continue       
            
                return player, blocking_action
            
        return None, None

    def request_lie_check(self, current_player, action, target_player):
        """ 
        Ask each player if they want to check current's player action is truth, the targetted player (if any) will be requested first.
        If someone wants to call, return the player. Else, return None
        """
        current_index = self.player_list.index(current_player)
        player_list = self.player_list[current_index:] + self.player_list[0:current_index]

        if target_player != None:
            target_index = self.player_list.index(target_player)
            player_list.remove(target_player)
            player_list = [self.player_list[target_index]] + player_list

        for player in player_list:
            if player == current_player or not player.alive: 
                continue
            if player.confirm_check_lie(current_player, action): 
                return player
        return None

    def add_card_to_deck(self, card):
        self.Deck.append(card)
        self.randomShuffle(self.Deck)
    
    def deal_card(self):
        if not len(self.Deck): 
            raise IndexError("There is no card in the character deck!")
        
        card = self.randomSelector(self.Deck)
        self.Deck.remove(card)
        return card

    def get_blocking_actions(self, action):
        blockers = []
        for card in Game.char_cards:
            if action.name in card.blocks:
                blockers.append(card)
                
        return blockers
            
Game = Game()