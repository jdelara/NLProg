from player import Player
from character import Character
from item import Item

class Dungeon:
    def __init__(self):
        self.players = []
        self.rooms = 0
        self.characters = []
        self.items = []
    
    def set_mins(self, min_rooms, min_players, min_characters, min_items):
        self.min_rooms = min_rooms
        self.min_players = min_players
        self.min_characters = min_characters
        self.min_items = min_items    

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
            sen += "\t\t\t\t\t\t- Name: " + player.name + "\n\t\t\t\t\t\t- Health: " + str(player.health) + " HP\n"
        return sen

    # CHARACTER
    def add_character(self, character):
        self.characters.append(character)
    
    def get_character(self):
        return self.characters[-1]

    def check_character_name(self, name):
        return any(character.name == name for character in self.characters)
    
    def print_characters(self):
        sen = ""
        for character in self.characters:            
            sen += "\t\t\t\t\t\t- Name: " + character.name + "\n\t\t\t\t\t\t- Greeting: " + character.greetings + "\n\t\t\t\t\t\t- Information:\n"
            for inf in character.info:
                sen+= "\t"*8 + "- " + inf + "\n"
        return sen

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
            sen += "\t\t\t\t\t\t- Name: " + item.name + "\n\t\t\t\t\t\t\t\t- Actions: " +"\n"
            for key,value in item.actions.items():
                sen += "\t"*10 + "- " + key + "\n"
                sen += "\t"*12 + "- Description: " + value.desc + "\n"
                sen += "\t"*12 + "- Effect: " + value.effect + "\n"
                sen += "\t"*12 + "- Win Condition: " + ("Yes" if value.win else "No") + "\n"
                if (key == "open"):
                    sen += "\t"*12 + "- Items needed to open: " + ', '.join(value.item_need) + "\n"
                    sen += "\t"*12 + "- Items inside: " + ', '.join(value.item_in) + "\n"  
        return sen
    
    # DUNGEON
    def dungeon_info(self):
        return "The dungeon has:\n\t\t- " + str(len(self.players)) + " Player(s):\n" + self.print_players() + "\t\t- " + str(len(self.characters)) + \
         " Character(s):\n" + self.print_characters() + "\t\t- " + str(len(self.items)) + " Items(s):\n" + self.print_items() + "\t\t- " + str(self.rooms) + " room(s)."
        
    def is_playable(self):        
        return (self.rooms >= 5 and len(self.players) > 0 and len(self.characters) > 0 and len(self.items) > 0)

    def missing_values(self):
        msg = ""
        msg += "There must be at least 5 rooms. The current number of rooms is:\t" + str(self.rooms) + "\n" \
             if self.rooms < self.min_rooms else ""
        msg += "There must be at least 1 player. The current number of players is:\t" + str(len(self.players)) + "\n" \
             if (len(self.players) < self.min_players) else ""
        msg += "There must be at least 1 character. The current number of characters is:\t" + str(len(self.characters)) + "\n" \
             if (len(self.characters) < self.min_characters) else ""
        msg += "There must be at least 1 item. The current number of items is:\t" + str(len(self.items)) + "\n" \
             if (len(self.items) < self.min_items) else ""
        return {
                "fulfillmentText":"Your dungeon is missing some configuration\n" + msg + "What do you want to set up?",
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }

    def reset(self):
        self.players = []
        self.rooms = 0
        self.characters = []
        self.items = []
        