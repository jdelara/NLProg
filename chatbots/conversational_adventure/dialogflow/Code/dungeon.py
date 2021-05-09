from player import Player
from character import Character
from item import Item

class Dungeon:
    def __init__(self):
        self.players = []
        self.rooms = 0
        self.characters = []
        self.items = []
    
    # ROOMS
    def set_number_of_rooms(self,number):
        self.rooms = number
    
    # PLAYER
    def add_player(self, player):
        self.players.append(player)
    
    def get_player(self):
        return self.players[-1]

    def check_player_name(self, name):
        return any(player.name == name for player in self.players)
    
    def print_players(self):
        sen = ""
        for player in self.players:            
            sen += "\t\t\t\t\t\t- Name: " + player.name + "\n\t\t\t\t\t\t- Health: " + str(player.health) + " HP\n\n"
        return sen[:-1]

    # CHARACTER
    def add_character(self, character):
        self.characters.append(character)
    
    def get_character(self):
        return self.characters[-1]

    def check_character_name(self, name):
        return any(character.name == name for character in self.characters)

    # ITEM
    def add_item(self, item):
        self.items.append(item)
    
    def get_item(self):
        return self.items[-1]

    def check_item_name(self, name):
        return any(item.name == name for item in self.items)
    
    def get_item_position(self, name):
        return str(sum(map(lambda x : x.name == name, self.items)))
    
    def print_items(self):
        sen = ""
        for item in self.items:            
            sen += "\t\t\t\t\t\t- Name: " + item.name + "\n\n"
        return sen[:-1]  
    
    
    def dungeon_info(self):
        return "The dungeon has:\n\t\t- " + str(len(self.players)) + " Player(s):\n" + self.print_players() + "\t\t- " + str(len(self.characters)) + \
         " Character(s):\n\t\t- " + str(len(self.items)) + " Items(s):\n" + self.print_items() + "\t\t- " + str(self.rooms) + " room(s)."
        
    def reset(self):
        self.players = []
        self.rooms = 0
        self.characters = []
        self.items = []
        