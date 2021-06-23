from room import Room
from dungeon import Dungeon
import random

class Game:
    def __init__(self):        
        self.turn = 0
        
    def build_dungeon(self, dngn):
        self.initialize_items(dngn)
        self.build_rooms_random(dngn)
        self.build_items(dngn)
        self.build_characters(dngn)


    def build_rooms_random(self, dngn):
        directions = ["north", "east", "west", "south"]
        dngn.rooms = [Room() for i in range(dngn.n_rooms)]
        for i in range(dngn.n_rooms):            
            count = sum(map(lambda x : dngn.rooms[i].doors[x]==0, dngn.rooms[i].doors.keys()))
            ceros_start = [idx for idx, element in enumerate(dngn.rooms[i].doors.values()) if element == 0]
            doors = random.randint(1,count) if count > 0 else 0
            positions = random.sample(ceros_start, doors)
            for pos in positions:
                dest_list = [idx for idx, element in enumerate(dngn.rooms) if element.doors[directions[3-pos]] == 0]                
                if (dest_list):
                    dest = random.choice(dest_list)+1
                    if not dest in dngn.rooms[i].doors.values() and not i+1 in dngn.rooms[dest-1].doors.values() and dest != i+1:
                        dngn.rooms[i].doors[directions[pos]] = dest
                        dngn.rooms[dest-1].doors[directions[3-pos]] = i+1                         

    def build_characters(self, dngn):
        for c in dngn.characters:
            ceros = [idx for idx, element in enumerate(dngn.rooms) if not element.characters]                    
            room = random.choice(ceros) if ceros else random.randint(0, dngn.n_rooms-1)
            dngn.rooms[room].characters.append(c)

    def build_items(self, dngn):
        for i in dngn.items:
            ceros = [idx for idx, element in enumerate(dngn.rooms) if not element.items]                    
            room = random.choice(ceros) if ceros else random.randint(0, dngn.n_rooms-1)
            dngn.rooms[room].items.append(i)      

    def describe_room(self, room):
        sen = ""
        for idx, c in enumerate(room.characters):
            sen += "You can see " + c.name + " standing in the middle of the room. " if idx == 0 else ""
            sen += c.name + " is also there. " if idx == 1 else ""
            sen += "And " + c.name + "." if idx > 1 else ""
        for idx,i in enumerate(room.items):
            sen += "You can see  a " + i.name + " in the center of the room. " if idx == 0 else ""
            sen += "There is also a " + i.name + ", " if idx == 1 else ""
            sen += "And a " + i.name + "." if idx > 1 else ""
            if i.open:
                sen += i.describe_item_in() 
        count = sum(map(lambda x : room.doors[x]>0, room.doors.keys()))
        if (count > 1):
            sen += "There are " + str(count) + " doors. "
            sen += "One to the north. " if room.doors["north"] > 0 else ""
            sen += "One to the south. " if room.doors["south"] > 0 else ""
            sen += "One to the east. " if room.doors["east"] > 0 else ""
            sen += "One to the west. " if room.doors["west"] > 0 else ""
        else:             
            sen += "There is " + str(count) + " door to the "
            sen += "north. " if room.doors["north"] > 0 else ""
            sen += "south. " if room.doors["south"] > 0 else ""
            sen += "east. " if room.doors["east"] > 0 else ""
            sen += "west. " if room.doors["west"] > 0 else ""
        sen += "\n"
        return sen 
    
    def find_item_answer(self, dngn, character):
        sens = []
        for item in dngn.items:
            for info in character.info:
                (sens.append(info) if item.name in info else None)
        return random.choice(list(set(sens)))
    
    def delete_answer(self, answer, character):
        character.info.remove(answer)
    
    def initialize_items(self, dngn):
        for item in dngn.items:
            if "open" in item.actions:
                for idx,aux in enumerate(item.actions["open"].item_in):      
                    item.actions["open"].item_in[idx] = next(elem for elem in dngn.items if elem.name == aux)                    
                    dngn.items.remove(item.actions["open"].item_in[idx])
        for character in dngn.characters:
            for idx,item in enumerate(character.items):
                character.items[idx] = next(elem for elem in dngn.items if elem.name == item)
                dngn.items.remove(character.items[idx])


        




