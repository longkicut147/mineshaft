# Coup specific exceptions
#   TargetRequired
#   not_enough_gold
#   not_enough_hp
#   BlockOnly
#   DeadPlayer
#   InvalidTarget
#   ActionNotAllowed
#   MajorError
class TargetRequired(Exception):
    pass

class BlockOnly(Exception):
    pass

class DeadPlayer(Exception):
    pass

class not_enough_gold(Exception):
    def __init__(self, gold_required):
        self.gold_required = gold_required

class not_enough_hp(Exception):
    def __init__(self, hp_required):
        self.hp_required = hp_required
        
class InvalidTarget(Exception):    
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class ActionNotAllowed(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class MajorError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
