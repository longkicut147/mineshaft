class TargetRequired(Exception):
    pass

class BlockOnly(Exception):
    pass

class DeadPlayer(Exception):
    pass

class NotEnoughGold(Exception):
    def __init__(self, gold_required):
        self.gold_required = gold_required

class NotEnoughHP(Exception):
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

class IndexError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
    
class DontHaveCard(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message