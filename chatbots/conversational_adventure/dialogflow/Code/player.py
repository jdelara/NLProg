class Player:
    def __init__(self, name):
        self.name = name
        self.health = 0
    
    def get_name(self):
        return self.name

    def set_health(self, health):
        self.health = health