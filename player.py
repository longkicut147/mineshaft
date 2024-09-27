from deck import*
from game import Game
from error import *
from action import *

class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = "name"
        self.char_card = []
        self.char_card.append(Game.deal_card())
        self.wild_cards = []
        
        self.gold = 1
        self.hp = 10
        self.alive = True
        Game.player_list.append(self)


    # nhận sát thương
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
        """ return True if player confirms to check_lie on current player's action. returns False if player allows action. """
        return False
            
    def confirm_block(self, current_player, opponentAction):
        """ returns action used by player to blocks action. return None if player allows action. """
        return None
        
    # def selectAmbassadorInfluence(self, choices, influenceRemaining):
    #     """ returns one or two cards from the choices. """
        
    #     selected = []
    #     for i in range(influenceRemaining):
    #         card = random.choice(choices)
    #         selected.append(card)
    #         choices.remove(card)
            
    #     return selected


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
        2. Check if player has at least 12 gold. If they do, throw exception unless coup is played.
        3. Check if any player wants to call bluff from active player
           a. If someone wants to call bluff, do Call step
        4. Check if a player wants to block
           a. If active player wants to call bluff, do Call step (todo: official rules says any play can call bluff. implement later)
        5. Play action if successful
        Call step: If someone call the bluff, reveal card. 
                   If card is the action played, remove influence from player.
                   Else, remove influence from calling player        
        """        
        if not self.alive or (target != None and not target.alive):
            raise DeadPlayer
            
        if target == self:
            raise TargetRequired
            
        if self.gold < action.gold_required:
            raise not_enough_gold(action.gold_required)
        
        if self.hp < action.hp_required:
            raise not_enough_hp(action.hp_required)
        
        if self.gold >= Force_to_Attack and action != Attack:
            raise ActionNotAllowed("Player has %i gold. Attack is the only choice" % (self.gold))
        
        # Step 3
        checking_player:Player = None
        # request player to check for lie if action is characters' skill
        if action in Game.char_cards:
            checking_player = Game.request_lie_check(self, action, target)
            
        if checking_player != None:
            # step 4.a
            if action == self.char_card:
                self.change_card()
                checking_player.take_damage(5)
            else:
                self.change_card()
                self.take_damage(5)

                message = "Bluffing %s failed for %s" % (action.name, self.name)
                return False, message             
        
        # Step 4
        blocking_player = None
        
        # should only call bluff for cards, not common actions
        if len(Game.get_blocking_actions(action)):
            blocking_player, blocking_action = Game.request_block(self, action, target)
        
        if blocking_player != None:
            # Step 3.a
            if self.confirm_check_lie(blocking_player, blocking_action):
                if blocking_action in blocking_player.char_card:
                    self.take_damage(5)
                    message = "Player %s has %s. Player %s loses 5 hp." % (blocking_player.name, blocking_action.name, self.name)
                    blocking_player.changeCard(blocking_action)
                    return False, message
                else:
                    blocking_player.take_damage(5)
            else:
                message = "Blocked by %s" % blocking_player.name
                return False, message
                
        # Step 5
        status, response = action.play(action, self, target)
        return status, response
    




























    # def disguise(self):
    #     if "disguise" in self.wc_cards:
    #         self.ch_cards.pop()
    #         self.get_ch_card(self.ch_deck)
    #         self.wc_cards.remove("disguise")
    #     else:
    #         print("you don't have disguise")

    # def swap(self, opponent):
    #     if "swap" in self.wc_cards:
    #         self.ch_cards[0], opponent.ch_cards[0] = opponent.ch_cards[0], self.ch_cards[0]
    #         self.wc_cards.remove("swap")
    #     else:
    #         print("you don't have swap")

    # def discard(self, opponent):
    #     if "discard" in self.wc_cards:
    #         opponent.ch_cards.pop()
    #         opponent.get_ch_card(self.ch_deck)
    #         self.wc_cards.remove("discard")
    #     else:
    #         print("you don't have discard")

    # def gun(self, opponent):
    #     if "gun" in self.wc_cards:
    #         card = str(input("guess opponent's card: "))
    #         if card == opponent.ch_cards[0]:
    #             opponent.take_damage(5)
    #         self.wc_cards.remove("gun")
    #     else:
    #         print("you don't have gun")

    # def heal(self):
    #     if "heal" in self.wc_cards:
    #         if self.hp <6:
    #             self.hp = 8
    #         else:
    #             self.hp = 10
    #         self.wc_cards.remove("heal")
    #     else:
    #         print("you don't have heal")

    # def attack(self, opponent):
    #     if self.gold >= 7:
    #         self.gold -= 7
    #         opponent.take_damage(5)
    #     else:
    #         print("not enough gold")        


        

