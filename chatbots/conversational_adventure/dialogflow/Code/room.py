import pathlib
import map_builder as mb
class Room:
    def __init__(self):        
        self.doors = {"north" : 0, "east": 0, "west": 0, "south": 0}
        self.characters = []
        self.items = []
        self.players = []


my_rooms = []
my_dict = {"north": 6, "west": 0, "east": 3, "south": 4}
my_rooms.append(my_dict)
my_dict = {"north": 0, "west": 0, "east": 6, "south": 0}
my_rooms.append(my_dict)
my_dict = {"north": 5, "west": 1, "east": 0, "south": 0}
my_rooms.append(my_dict)
my_dict = {"north": 1, "west": 0, "east": 0, "south": 0}
my_rooms.append(my_dict)
my_dict = {"north": 0, "west": 6, "east": 0, "south": 3}
my_rooms.append(my_dict)
my_dict = {"north": 7, "west": 2, "east": 5, "south": 1}
my_rooms.append(my_dict)
my_dict = {"north": 0, "west": 0, "east": 0, "south": 6}
my_rooms.append(my_dict)

##################
#                #
#   2   6   5    #
#       1   3    #
#       4        #
#                #
##################
raiz = pathlib.Path(__file__).parent.parent.resolve()
print(raiz)
mb.map_builder_start(my_rooms)
mb.print_map(my_rooms)
mb.save_map(raiz)