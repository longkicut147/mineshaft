import random

from error import MajorError

class Game:
    def reset(self):
        self.player_list = []
        
        import action
        self.common_actions = [action.Dig, action.Attack]
        self.char_cards = [action.Miner, action.Thief, action.Swordman, action.Tanker]
        self.Deck = self.char_cards * 2
        random.shuffle(self.Deck)
        
        self.dead_char_cards = []
        
        # separating these function allow outside modules (like the unit test) to change the behavior of
        # shuffling and selecting a card
        self.randomShuffle = random.shuffle
        self.randomSelector = random.choice


    def request_block(self, current_player, action, target_player):
        """ 
        Ask each player if they want to block current player's action.
        Requests are performed in a clockwise rotation (http://boardgamegeek.com/article/18425206#18425206). However,
        for the sake of game flow, the targetted player (if any) will be requested first.
        If someone wants to block, return the tuple (player, action). Else, return (None, None).
        """
        # xoay lượt, đến lượt ai xoay người đó lên đầu
        current_index = self.player_list.index(current_player)
        player_list = self.player_list[current_index:] + self.player_list[0:current_index]
        
        if target_player != None:
            # chuyển target_player lên đầu player_list
            target_index = self.player_list.index(target_player)
            player_list.remove(target_player)
            player_list = [self.player_list[target_index]] + player_list
        
        for player in player_list:
            # bỏ qua người đang đến lượt và người chết
            if player == current_player or not player.alive: 
                continue
            
            blocking_action = player.confirmBlock(current_player, action)
            
            if blocking_action != None: 
                # kiểm tra có block được không (nếu action có trong list block action)
                if not action.name in blocking_action.blocks:
                    continue       
            
                return player, blocking_action
            
        return None, None

    def request_lie_check(self, current_player, action, target_player):
        """ 
        Ask each player if they want to call active player's (possible) bluff.
        Requests are performed in a clockwise rotation (http://boardgamegeek.com/article/18425206#18425206). However,
        for the sake of game flow, the targetted player (if any) will be requested first.
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
            if player.confirmCall(current_player, action): 
                return player
        return None

    def add_card_to_deck(self, card):
        self.Deck.append(card)
        self.randomShuffle(self.Deck)
    
    def deal_card(self):
        if not len(self.Deck): 
            raise MajorError("There is no card in the court deck!")
        
        card = self.randomSelector(self.Deck)
        self.Deck.remove(card)
        return card

    def get_blocking_actions(self, action):
        blockers = []
        for card in Game.char_cards:
            if action.name in card.blocks:
                blockers.append(card)
                
        return blockers
            
Game = Game()     # global variable
