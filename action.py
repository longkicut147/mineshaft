from player import Player
from error import *
from game import Game
Force_to_Attack = 10

class Action:
    name = ""
    description = ""
    blocks = []
    hasTarget = False
    consumable = False
    gold_required = 0
    hp_required = 0
            
    def play(self, player:Player, target:Player = None):
        """
        should be overrriden by child classes
        returns (status, response): 
            status:     True/False if action is successful or not
            response:   String explaining status. Usually reserved for explanation of why an action failed.
        Example:
            return True, "Success"
            return False, "Failed because it was blocked"
        """
        return False, None


# Common actions

class Dig(Action):
    name = "Dig"
    description = "Get 1 gold."
    
    def play(self, player:Player, target:Player = None):
        player.gold += 1
        return True, "Success"
    
class Attack(Action):
    name = "Attack"
    description = "Pay 7 gold to attack 5 hp on target player."
    hasTarget = True
    gold_required = 7
    
    def play(self, player:Player, target:Player = None):
        if player.gold < self.gold_required:
            raise NotEnoughGold(self.gold_required)
            
        # target should be alive
        if target == None:
            raise TargetRequired
                        
        if not target.alive:
            raise InvalidTarget("Can not attack because target is dead")

        # if enough conditions -> success 
        player.gold -= 7
        target.take_damage(5)
        return True, "Success"




# character actions

class Miner(Action):
    name = "Miner"
    description = "Get 2 gold."
            
    def play(self, player:Player, target:Player = None):
        player.gold += 2
        return True, "Success"
        
class Thief(Action):
    name = "Thief"
    description = "Steal 1 gold from target. Blocks Thief."
    blocks = ["Thief"]
    hasTarget = True
            
    def play(self, player:Player, target:Player = None):
        if target == None:
            raise TargetRequired

        steal = 0
        if target.gold >= 1:
            steal = 1
        player.gold += steal

        target.gold -= steal
        if target.gold < 0: 
            target.gold = 0
        
        return True, "Success"
        
class Tanker(Action):
    name = "Tanker"
    description = "Blocks Swordman and Thief."
    blocks = ["Swordman", "Thief"]
            
    def play(self, player:Player, target:Player = None):
        raise BlockOnly
        
class Swordman(Action):
    name = "Swordman"
    description = "Sacrifice 3 hp to attack 5 hp on target player."
    hasTarget = True
    hp_required = 3
    
    def play(self, player:Player, target:Player = None):
        if player.hp < self.hp_required:
            raise NotEnoughHP(self.hp_required)
        if target == None:
            raise TargetRequired
            
        player.take_damage(3)
        target.take_damage(5)
        
        return True, "Success"
    



# wild card actions

class Disguise(Action):
    name = "Disguise"
    description = "Change your character card."
    consumable = True

    def play(self, player:Player, target:Player=None):
        if Disguise not in player.wild_cards:
            raise DontHaveCard

        player.wild_cards.pop()
        deckCard = Game.deal_card()

        selfCard = player.char_card[0]
        Game.add_card_to_deck(selfCard)

        player.char_card.append(deckCard)
        Game.randomShuffle(self.Deck)
        return True, "Success"
    
class Swap(Action):
    name = "Swap"
    description = "Change your character card with a player."
    consumable = True 
    hasTarget = True

    def play(self, player:Player, target:Player = None):
        if Disguise not in player.wild_cards:
            raise DontHaveCard

        if target == None:
            raise TargetRequired
            
        target.char_card[0], player.char_card[0] = player.char_card[0], target.char_card[0]
        
        return True, "Success"

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