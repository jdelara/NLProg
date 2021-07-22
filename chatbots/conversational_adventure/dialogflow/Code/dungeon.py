from player import Player
from character import Character
from item import Item
from action import Action
from game import Game

class Dungeon:
    def __init__(self):
        self.name = ""
        self.players = []
        self.n_rooms = 0
        self.characters = []
        self.items = []
        self.rooms = []
        self.game = Game()
    
    def set_mins(self, min_rooms, min_players, min_characters, min_items):
        self.min_rooms = min_rooms
        self.min_players = min_players
        self.min_characters = min_characters
        self.min_items = min_items    

    # ROOMS
    def set_number_of_rooms(self,number):
        self.n_rooms = number
    
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
    
    def players_list(self):
        sen = ""
        for player in self.players:            
            sen += "\t\t- " + player.name + "\n"
        return sen

    def set_player_room(self, idx):
        self.players[self.game.turn].room = self.rooms[idx-1]
        self.rooms[idx-1].players.append(self.players[self.game.turn])
        self.rooms[idx-1].visited = True
    
    def remain_players(self):        
        return [player.name for player in self.players if not player.human_id]        

    def print_remain_players(self):
        sen = ""
        players = self.remain_players()
        for player in players:
            sen += "\n\t\t- " + player
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
            sen+= "\t\t\t\t\t\t- Character items:\n"
            for item in character.items:
                sen+= "\t"*8 + "- " + item + "\n"
        return sen
    
    def characters_list(self):
        sen = ""
        for character in self.characters:            
            sen += "\t\t- " + character.name + "\n"
        return sen

    # ITEM
    def add_item(self, item):
        self.items.append(item)
    
    def get_item(self, name):
        return next(item for item in self.items if item.name == name)

    def check_item_name(self, name):
        return any(item.name == name for item in self.items)
    
    def get_item_position(self, name):
        return str(sum(map(lambda x : x.name == name, self.items)))
    
    def print_items(self):
        sen = ""
        for item in self.items:            
            sen += "\t\t\t\t\t\t- Name: " + item.name + "\n"
            sen += "\t\t\t\t\t\t- Item is inside of: " + (item.inside if item.inside else "Nothing") + "\n"
            sen += "\t\t\t\t\t\t\t\t- Actions: " +"\n"
            for key,value in item.actions.items():
                sen += "\t"*10 + "- " + key + "\n"
                sen += "\t"*12 + "- Description: " + value.desc + "\n"
                sen += "\t"*12 + "- Effect: " + value.effect + "\n"
                sen += "\t"*12 + "- Win Condition: " + ("Yes" if value.win else "No") + "\n"
                sen += "\t"*12 + "- Win Condition: " + ("Yes" if value.lose else "No") + "\n"
                if (key == "open"):
                    sen += "\t"*12 + "- Items needed to open: " + ', '.join(value.item_need) + "\n"
                    sen += "\t"*12 + "- Items inside: " + ', '.join(value.item_in) + "\n"  
                
        return sen

    def items_list(self):
        sen = ""
        for item in self.items:            
            sen += "\t\t- " + item.name + "\n"
        return sen
    
    def set_items_inside(self):
        for item in self.items:
            if "open" in item.actions:
                for i in self.items:
                    i.inside = item.name if i in item.actions["open"].item_in else None
    
    def missing_items(self):
        missing_items = []
        for item in self.items:
            if "open" in item.actions:
                missing_items.extend([i for i in item.actions["open"].item_need if not self.check_item_name(i)])
                missing_items.extend([i for i in item.actions["open"].item_in if not self.check_item_name(i)])
        for character in self.characters:
            missing_items.extend([i for i in character.items if not self.check_item_name(i)])
        return missing_items
    
    def win_condition(self):
        for item in self.items:
            try:
                next(action for action in item.actions if item.actions[action].win)
                return True
            except:
                pass
        return False
                
                   

            
    
    # HUMAN
    def human_has_player(self, id):
        players_id = [player.human_id for player in self.players]
        return id in players_id
    
    def describe_turn(self):
        return " *Turn of " + self.players[self.game.turn].name + ".* \n\n" if len(self.players) > 1 else ""

    # DUNGEON
    def dungeon_info(self):
        return "The dungeon has:\n\t\t- " + str(len(self.players)) + " Player(s):\n" + self.print_players() + "\t\t- " + str(len(self.characters)) + \
         " Character(s):\n" + self.print_characters() + "\t\t- " + str(len(self.items)) + " Items(s):\n" + self.print_items() + "\t\t- " + str(self.n_rooms) + " room(s)."
        
    def is_playable(self):        
        return (self.n_rooms >= 5 and len(self.players) > 0 and len(self.characters) > 0 and len(self.items) > 0)
    
    def change_turn(self):
        self.game.turn = self.game.turn+1 if self.game.turn < len(self.players) - 1 else 0

    def missing_values(self):
        msg = ""
        msg += "There must be at least 5 rooms. The current number of rooms is:\t" + str(self.n_rooms) + "\n" \
             if self.n_rooms < self.min_rooms else ""
        msg += "There must be at least 1 player. The current number of players is:\t" + str(len(self.players)) + "\n" \
             if (len(self.players) < self.min_players) else ""
        msg += "There must be at least 1 character. The current number of characters is:\t" + str(len(self.characters)) + "\n" \
             if (len(self.characters) < self.min_characters) else ""
        msg += "There must be at least 1 item. The current number of items is:\t" + str(len(self.items)) + "\n" \
             if (len(self.items) < self.min_items) else ""
        return msg
        
        
    def check_turn(self, id):
        return self.players[self.game.turn].human_id == id

    def reset(self):
        self.name = ""
        self.players = []
        self.n_rooms = 0
        self.characters = []
        self.items = []
        self.rooms = []
        self.game = Game()
    
    def aux(self):
        self.reset()
        player1 = Player("Marcus")
        player1.health = 100
        player2 = Player("Mary")
        player2.health = 115
        self.players.append(player1)
        #self.players.append(player2)
        #--------------------------------------------------------------------------------------
        self.n_rooms = 6
        #--------------------------------------------------------------------------------------
        item1 = Item("potion")
        action1 = Action("You can take the item")
        action2 = Action("You can consume the item", "It will kill the player", True)        
        item1.add_action("take", action1)
        item1.add_action("consume", action2)
        item1.actions["consume"].hp = 50
        item1.inside = "chest"
        item2 = Item("chest")
        #action1 = Action("You can open the item", "", False, False, ["key", "bomb"], ["potion", "rock", "book", "lamp"])
        action1 = Action("You can open the item", "", False, False, ["key"], ["potion", "rock", "book"])
        item2.add_action("open", action1)
        item3 = Item("book")
        action1 = Action("You can take the item")
        action2 = Action("You can read the item", "In order to end, one must consume the beverage.", False, True)
        item3.add_action("take", action1)
        item3.add_action("read", action2)
        item3.inside = "chest"
        item4 = Item("key")
        action1 = Action("You can take the item")
        item4.add_action("take", action1)
        item5 = Item("rock")
        action1 = Action("You can take the item")
        item5.add_action("take", action1)
        item5.inside = "chest"

        self.items.append(item1)
        self.items.append(item2)
        self.items.append(item3)
        self.items.append(item4)
        self.items.append(item5)
        #--------------------------------------------------------------------------------------
        character1 = Character("Magnus the red")
        character1.greetings = "Hello traveller"
        character1.info.append("Take this key, it will open a treasure.")
        character1.info.append("Remember where you come from and where you are going. Many adventurers get lost in these rooms")
        character1.items.append("key")
        character2 = Character("Mortek the brave")
        character2.greetings = "Greetins adventurer"
        character2.info.append("You have to find Magnus the red, he will give you something you need.")
        self.characters.append(character1)
        self.characters.append(character2)

        self.name = "testing_game"

         
        