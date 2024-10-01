from deck import*
from game import Game
from error import *
from action import *
Force_to_Attack = 10

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = "name"
        self.char_card = []
        self.char_card.append(Game.deal_card())
        self.wild_cards = []
        self.wild_cards.append(Game.deal_card())
        self.gold = 1
        self.hp = 10
        self.alive = True
        Game.player_list.append(self)


    def take_damage(self, damage):
        if self.alive == True:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                # nếu máu về 0 thì chết
                self.alive = False
                revealed_card = self.char_card.pop()
                Game.dead_char_cards.append(revealed_card)
            

    def confirm_check_lie(self, current_player, action): 
        # return True if player confirms to check_lie on current player's action. returns False if player allows action.
        return False
            
    def confirm_block(self, current_player, opponent_action):
        # returns action used by player to blocks action. return None if player allows action.
        return None


    def change_card(self):
        card = self.char_card[0]
        self.char_card.remove(card)
        Game.add_card_to_deck(card)
        # give player a new card
        newcard = Game.deal_card()
        self.char_card.append(newcard)


    def play(self, action, target = None):
        """
        1. Check if player is alive. If not, throw exception.
        2. Check if player has 10 gold. If they do, throw exception unless player attack.
        3. Check if any player wants to check for lie from current player
           a. If someone wants to check for lie, do check step
        4. Check if a player wants to block
           a. If current player wants to check for lie, do check step
        5. Play action if successful
        check step: If someone check for lie, reveal card. 
                   If card is the action played, -5 hp from current player.
                   Else, -5 hp from checking player        
        """        

        # Step 1 and 2
        if not self.alive or (target != None and not target.alive):
            raise DeadPlayer
            
        if target == self:
            raise TargetRequired
            
        if self.gold < action.gold_required:
            raise NotEnoughGold(action.gold_required)
        
        if self.hp < action.hp_required:
            raise NotEnoughHP(action.hp_required)
        
        if self.gold >= Force_to_Attack and action != Attack:
            raise ActionNotAllowed("Player has %i gold. Attack is the only choice" % (self.gold))
        

        # Step 3
        checking_player:Player = None
        # request player to check for lie if action is character actions
        if action in Game.char_cards:
            checking_player = Game.request_lie_check(self, action, target)
            
        if checking_player != None:
            # step 4.1
            if action == self.char_card:
                self.change_card()
                checking_player.take_damage(5)
            else:
                self.change_card()
                self.take_damage(5)

                message = "%s loses 5 hp for lying to use %s" % (self.name, action.name)
                return False, message             
        

        # Step 4
        blocking_player = None
        
        # only check lie for character actions, not common actions or wildcard actions
        if len(Game.get_blocking_actions(action)):
            blocking_player, blocking_action = Game.request_block(self, action, target)
        
        if blocking_player != None:
            # Step 3.1
            if self.confirm_check_lie(blocking_player, blocking_action):
                if blocking_action in blocking_player.char_card:
                    self.take_damage(5)
                    blocking_player.change_card(blocking_action)
                    message = "%s has %s. %s loses 5 hp." % (blocking_player.name, blocking_action.name, self.name)
                    return False, message
                else:
                    blocking_player.take_damage(5)
                    blocking_player.change_card(blocking_action)
            else:
                message = "Blocked by %s" % blocking_player.name
                return False, message


        # Step 5
        status, response = action.play(action, self, target)
        return status, response
    