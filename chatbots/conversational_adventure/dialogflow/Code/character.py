from item import Item

class Character:
    def __init__(self, name):
        self.name = name
        self.desc = ""
        self.items = {}

    def set_desc(self, desc):
        self.desc = desc
    
    def add_item(self, item, place=None):
        self.items[item]=place