from player import Player
from error import *
from game import Game
Force_to_Attack = 10

class Action:
    name = ""
    description = ""
    blocks = []
    hasTarget = False
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
        if target == None:
            raise TargetRequired
        if not target.alive:
            raise InvalidTarget("Can not attack because target is dead")

        player.gold -= 7
        target.take_damage(5)

        return True, "Success"


class Buy(Action):
    name = "Buy"
    description = "Pay 3 gold to buy a wild card."
    gold_required = 3

    def play(self, player:Player, target:Player = None):
        if player.gold < self.gold_required:
            raise NotEnoughGold(self.gold_required)
        if len(Game.wild_Deck) == 0:
            raise IndexError

        player.gold -= 3
        deckCard = Game.deal_wild_card()
        player.wild_cards.append(deckCard)

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

    def play(self, player:Player, target:Player=None):
        if Disguise not in player.wild_cards:
            raise DontHaveCard
        if len(Game.char_Deck) == 0:
            raise IndexError
        player.wild_cards.remove(Disguise)
        
        Player.change_card(player)

        return True, "Success"
    

class Swap(Action):
    name = "Swap"
    description = "Change your character card with a player."
    hasTarget = True

    def play(self, player:Player, target:Player = None):
        if Swap not in player.wild_cards:
            raise DontHaveCard
        if target == None:
            raise TargetRequired
        player.wild_cards.remove(Swap)
            
        target.char_card[0], player.char_card[0] = player.char_card[0], target.char_card[0]

        return True, "Success"
    

class Discard(Action):
    name = "Discard"
    description = "Force a player to change their character card."
    hasTarget = True    

    def play(self, player:Player, target:Player = None):
        if Discard not in player.wild_cards:
            raise DontHaveCard
        if target == None:
            raise TargetRequired  
        player.wild_cards.remove(Discard)

        Player.change_card(target)

        return True, "Success"      


class Gun(Action):
    name = "Gun"
    description = "Guess target's character card. If they have it, attack 5 hp on them."
    hasTarget = True   

    def play(self, player:Player, target:Player = None):
        if Gun not in player.wild_cards:
            raise DontHaveCard
        if target == None:
            raise TargetRequired
        if not target.alive:
            raise InvalidTarget("Can not attack because target is dead")
        player.wild_cards.remove(Gun)
            
        target.take_damage(5)

        return True, "Success"


class Heal(Action):
    name = "Heal"
    description = "Set your hp to 8."

    def play(self, player:Player, target:Player=None):
        if Heal not in player.wild_cards:
            raise DontHaveCard
        player.wild_cards.remove(Heal)
        
        player.hp = 8

        return True, "Success"  