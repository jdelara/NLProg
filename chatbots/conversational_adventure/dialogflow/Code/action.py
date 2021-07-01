class Action:
    def __init__(self, desc, effect="", win=False, lose=False, item_need=[], item_in=[]):
        self.desc = desc
        self.effect = effect
        self.win = win
        self.lose = lose
        self.item_need = item_need
        self.item_in = item_in
        
    
    def set_item_need(self, items):
        self.item_need.extend(items)
    
    def set_item_in(self, items):
        self.item_in.extend(items)
    
    