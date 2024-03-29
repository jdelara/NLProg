from room import Room
import random

class Game:
    def __init__(self):        
        self.turn = 0
        self.started = False
        
    def build_dungeon(self, dngn):
        self.initialize_items(dngn)
        self.build_rooms_arranged(dngn)
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
                    dest_list.remove(i) if i in dest_list else dest_list                    
                    dest = random.choice(dest_list)+1 if dest_list else None
                    while(dest_list):
                        if dest in dngn.rooms[i].doors.values() or i+1 in dngn.rooms[dest-1].doors.values():
                            dest_list.remove(dest-1)
                            dest = random.choice(dest_list)+1 if dest_list else None
                        else:
                            break
                    if (dest_list):                
                        dngn.rooms[i].doors[directions[pos]] = dest
                        dngn.rooms[dest-1].doors[directions[3-pos]] = i+1
        if any(all(value == 0 for value in item.doors.values()) for item in dngn.rooms):
            dngn.rooms = [dict.fromkeys(item.rooms, 0) for item in dngn.rooms]
            for room in dngn.rooms:
                print(room.doors)
            self.build_rooms_random()
        
    def build_rooms_arranged(self, dngn):
        directions = ["north", "east", "west", "south"]
        dngn.rooms = [Room() for i in range(dngn.n_rooms)]        
        ceros_start = [idx for idx, element in enumerate(dngn.rooms[0].doors.values()) if element == 0]
        doors = random.randint(1,3)
        positions = random.sample(ceros_start, doors)        
        for pos in positions:
            dest_list = [idx for idx, element in enumerate(dngn.rooms) if element.doors[directions[3-pos]] == 0 and idx != 0]
            values = list(dngn.rooms[0].doors.values())    
            dest = [x for x in dest_list if x+1 not in values]                
            dest = random.choice(dest)            
            dngn.rooms[0].doors[directions[pos]] = dest+1
            dngn.rooms[dest].doors[directions[3-pos]] = 1
        for i in range(1,dngn.n_rooms):
            count = sum(map(lambda x : dngn.rooms[i].doors[x]==0, dngn.rooms[i].doors.keys()))
            if count == 4: 
                dest_list = []            
                while(not dest_list and self.check_rooms(dngn.rooms, i)):
                    dir = random.randint(0,3)
                    dest_list = [idx for idx, element in enumerate(dngn.rooms) if element.doors[directions[3-dir]] == 0 and idx != i and idx < i]                             
                dest = random.choice(dest_list)+1 if dest_list else None           
                if dest:                                     
                    dngn.rooms[i].doors[directions[dir]] = dest
                    dngn.rooms[dest-1].doors[directions[3-dir]] = i+1
                    next_room = dngn.rooms[dest-1]   
                    if dir == 0 or dir == 3: # sur/norte este                        
                        if next_room.doors["east"]-1 >= 0:
                            middle_room = dngn.rooms[next_room.doors["east"]-1]
                            if middle_room.doors[directions[3-dir]]-1 >= 0:
                                final_room = dngn.rooms[middle_room.doors[directions[3-dir]]-1]
                                dngn.rooms[i].doors["east"] = middle_room.doors[directions[3-dir]] if final_room.doors["west"] == 0 else 0
                                final_room.doors["west"] = i+1 if final_room.doors["west"] == 0 else final_room.doors["west"]                              
                    else: # este/oeste norte
                        if next_room.doors["north"]-1 >= 0:
                            middle_room = dngn.rooms[next_room.doors["north"]-1]
                            if middle_room.doors[directions[3-dir]]-1 >= 0:
                                final_room = dngn.rooms[middle_room.doors[directions[3-dir]]-1]
                                dngn.rooms[i].doors["north"] = middle_room.doors[directions[3-dir]] if final_room.doors["south"] == 0 else 0
                                final_room.doors["south"] = i+1 if final_room.doors["south"] == 0 else final_room.doors["south"]                        
                    if dir == 0 or dir == 3: # sur/norte oeste
                        if next_room.doors["west"]-1 >= 0:
                            middle_room = dngn.rooms[next_room.doors["west"]-1]
                            if middle_room.doors[directions[3-dir]]-1 >= 0:
                                final_room = dngn.rooms[middle_room.doors[directions[3-dir]]-1]                       
                                dngn.rooms[i].doors["west"] = middle_room.doors[directions[3-dir]] if final_room.doors["east"] == 0 else 0
                                final_room.doors["east"] = i+1 if final_room.doors["east"] == 0 else final_room.doors["east"]                        
                    else: # este/oeste sur
                        if next_room.doors["south"]-1 >= 0:
                            middle_room = dngn.rooms[next_room.doors["south"]-1]
                            if middle_room.doors[directions[3-dir]]-1 >= 0:
                                final_room = dngn.rooms[middle_room.doors[directions[3-dir]]-1]
                                dngn.rooms[i].doors["south"] = middle_room.doors[directions[3-dir]] if final_room.doors["north"] == 0 else 0
                                final_room.doors["north"] = i+1 if final_room.doors["north"] == 0 else final_room.doors["north"]                       
        self.print_aux(dngn)  
        print("\n") 


    def print_aux(self,dngn):
        for idx,r in enumerate(dngn.rooms):
            print(idx+1, list(r.doors.values()))
                        
    def check_rooms(self,rooms, idx):
        for i in range(idx):
            if sum(map(lambda x : rooms[i].doors[x]==0, rooms[i].doors.keys())) > 0:
                return True
        return False

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

    def describe_room(self, room, dngn):
        sen = ""
        room.players.remove(dngn.players[dngn.game.turn])
        for idx, p in enumerate(room.players):
            sen += "You can see " + p.name + " standing in the middle of the room. " if idx == 0 else ""
            sen += p.name + " is also there. " if idx == 1 else ""
            sen += "And " + p.name + "." if idx > 1 else ""
        room.players.append(dngn.players[dngn.game.turn])
        for idx, c in enumerate(room.characters):
            sen += "You can see " + c.name + " standing in the middle of the room. " if idx == 0 else ""
            sen += c.name + " is also there. " if idx == 1 else ""
            sen += "And " + c.name + "." if idx > 1 else ""
        for idx,i in enumerate(room.items):
            if not i.inside:
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
        for item in character.items:
            for info in character.info:
                (sens.append(info) if item.name in info else None)
        return random.choice(list(set(sens))) if sens else "Sorry, I don't posses any information about what you are asking"
    
    def delete_answer(self, answer, character):
        character.info.remove(answer)
    
    def initialize_items(self, dngn):
        for item in dngn.items:
            item.inside = next(elem for elem in dngn.items if elem.name == item.inside) if item.inside else None               
        for item in dngn.items:
            if "open" in item.actions:
                for idx,aux in enumerate(item.actions["open"].item_in):      
                    item.actions["open"].item_in[idx] = next(elem for elem in dngn.items if elem.name == aux)                    
                    dngn.items.remove(item.actions["open"].item_in[idx])
                for idx,aux in enumerate(item.actions["open"].item_need):      
                    item.actions["open"].item_need[idx] = next(elem for elem in dngn.items if elem.name == aux)            
        for character in dngn.characters:
            for idx,item in enumerate(character.items):
                character.items[idx] = next(elem for elem in dngn.items if elem.name == item)
                dngn.items.remove(character.items[idx])
    
    def command_list(self):
        sen = ""
        sen += "There is a list of actions available for the player: \n"
        sen += "\t\t - Type 'describe room' to get a description of the current room the player is in.\n"
        sen += "\t\t - Type 'check inventory' to take a look to the player's inventory.\n"
        sen += "\t\t - Type 'see map' to get a picture of the current visited rooms.\n"
        sen += "\t\t - Type 'take note' to write something down in your notebook.\n"
        sen += "\t\t - Type 'read notes' to take a look at your written notes.\n"
        return sen
    
    def button_telegram_fulfillmentMessages(self, text):
        return [
                {
                "payload": {
                    "telegram": {
                        "parse_mode": "Markdown",
                        "text": text,
                        "reply_markup": {
                            "keyboard": [
                                    [
                                        {
                                            "text": "Go north",
                                            "request_contact": False,
                                            "request_location": False
                                        },
                                        
                                    ],
                                    [
                                        {
                                            "text": "Go west",
                                            "request_contact": False,
                                            "request_location": False
                                        },
                                        {
                                            "text": "Go east",
                                            "request_contact": False,
                                            "request_location": False
                                        }
                                    ],
                                    [
                                        {
                                            "text": "Go south",
                                            "request_contact": False,
                                            "request_location": False
                                        }
                                    ]
                                ],
                                "resize_keyboard": True,
                                "one_time_keyboard": True,
                                "selective": False
                            }
                        },
                        "payloadMessage": None,
                        "source": "TELEGRAM"
                        }
                    }
                ]



        




