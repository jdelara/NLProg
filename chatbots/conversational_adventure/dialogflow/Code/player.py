class Player:
    def __init__(self, name):
        self.name = name
        self.health = 0
        self.room = None
        self.inventory = []        
        self.human_name = ""
        self.human_id = ""
        self.notes = []
    
    def get_name(self):
        return self.name

    def set_health(self, health):
        self.health = health
    
    def get_inventory(self):
        sen = ""
        if not self.inventory:
            sen = "You do not have any items at the time."
        else:
            for i in self.inventory:
                sen += "You have a " + i.name + ". "
        return sen 
    
    def get_notes(self):
        sen = ""
        for note in self.notes:
            sen += "\t\t - " + note + "\n"
        return sen