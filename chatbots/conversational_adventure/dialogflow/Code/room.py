class Room:
    def __init__(self):        
        self.doors = {"north" : 0, "east": 0, "west": 0, "south": 0}
        self.characters = []
        self.items = []
        self.players = []
        self.visited = False
