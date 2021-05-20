class Item:
    def __init__(self, name):
        self.name = name
        self.actions = {}
    
    def add_action(self, name, action):
        self.actions[name] = action
    
    def get_action(self, name):
        return self.actions[name]
        
    