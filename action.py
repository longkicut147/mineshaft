from player import Player
from error import *
from game import Game
ForceCoupCoins = 10

class Action:
    name = ""
    description = ""
    blocks = []
    hasTarget = False
    gold_required = 0
    hp_required = 0
            
    def play(self, player, target = None):
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


# Common choice

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
            raise not_enough_gold(self.gold_required)
            
        # target should be alive
        if target == None:
            raise TargetRequired
                        
        if not target.alive:
            raise InvalidTarget("Can not attack because target is dead")

        # if enough conditions -> success 
        player.gold -= 7
        target.take_damage(5)
        return True, "Success"




# character's skill choice

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
    description = "Attack. Sacrifice 3 hp to attack 5 hp on target player."
    hasTarget = True
    hp_required = 3
    
    def play(self, player:Player, target:Player = None):
        if player.hp < self.hp_required:
            raise not_enough_hp(self.hp_required)
        if target == None:
            raise TargetRequired
            
        player.take_damage(3)
        target.take_damage(5)
        
        return True, "Success"
        
# class Ambassador(Action):
#     name = "Ambassador"
#     description = "Exchange your influence with 2 cards from the Court Deck. Blocks Steal."
#     blocks = ["Captain"]
            
#     def play(self, player, target = None):
#         influenceRemaining = len(player.influence)
#         choices = list(player.influence)
        
#         deckCards = [GameState.DrawCard(), GameState.DrawCard()]
#         choices.append(deckCards[0])
#         choices.append(deckCards[1])
        
#         newInfluence = player.selectAmbassadorInfluence(list(choices), influenceRemaining)
#         if type(newInfluence) != list:
#             newInfluence = [newInfluence]
        
#         def ReturnCards():
#             GameState.AddToDeck(deckCards[0])
#             GameState.AddToDeck(deckCards[1])
            
#         if len(newInfluence) != influenceRemaining:
#             # There is a missing card. Try again.
#             ReturnCards()
#             raise InvalidTarget("Wrong number of cards given")

#         choicesCopy = list(choices) # this allow us to test for card duplicates
#         for card in newInfluence:
#             if not card in choicesCopy:
#                 # something is wrong. The player sent a card choice that is not part of the original choices.
#                 # try again.
#                 ReturnCards()
#                 raise InvalidTarget("Card given not part of valid choices")
            
#             choicesCopy.remove(card)
        
#         # give the player their new cards        
#         player.influence = list(newInfluence)

#         # return the unselected cards back to the Court Deck.
#         for card in newInfluence:
#             choices.remove(card)
            
#         for card in choices:
#             GameState.AddToDeck(card)
#         return True, "Success"