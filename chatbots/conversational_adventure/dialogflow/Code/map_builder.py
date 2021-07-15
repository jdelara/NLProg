import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import pathlib

def get_size(sizes):
    north = east = 0
    for size in sizes:
        north = size["south"] if size["south"]>north else north
        east = size["east"] if size["east"]>east else east
    return (north+1, east+1) 

def draw_room(screen, position_x, position_y, size, room):
    rect = pg.Rect(position_x, position_y, size, size)
    #rect.center = (position,position)    
    pg.draw.rect(screen, white, rect)
    pg.draw.rect(screen, blue, rect, 2)   
    # norte
    if room["north"] > 0:
        draw_corridor(screen, (position_x + size*2/5, position_y-size/2), (size/5, size/2))
        pg.draw.line(screen, red, (position_x + size*2/5,position_y+3), (position_x + size*3/5,position_y+3), 5)
    # sur
    if room["south"] > 0:
        draw_corridor(screen, (position_x + size*2/5, position_y+size), (size/5, size/2))
        pg.draw.line(screen, red, (position_x + size*2/5,position_y+size-3), (position_x + size*3/5,position_y+size-3), 5)
    # este
    if room["east"] > 0:
        draw_corridor(screen, (position_x+size,position_y + size*2/5), (size/2,size/5))
        pg.draw.line(screen, red, (position_x+size-3,position_y + size*2/5), (position_x+size-3,position_y + size*3/5), 5) 
    # oeste
    if room["west"] > 0:
        draw_corridor(screen, (position_x-size/2,position_y + size*2/5), (size/2,size/5))
        pg.draw.line(screen, red, (position_x+3,position_y + size*2/5), (position_x+3,position_y + size*3/5), 5)  
    return rect

def draw_corridor(screen, position, size):
    rect = pg.Rect(position,size)
    pg.draw.rect(screen, white, rect)
    pg.draw.rect(screen, blue, rect, 2) 
    return 0

def get_direction(room1, room2, my_rooms):
    return list(my_rooms[room1].keys())[list(my_rooms[room1].values()).index(room2+1)]

def set_sizes(rooms):
    my_sizes = []
    for idx in range(len(rooms)):
        my_dict = {}
        highest_south = 0
        current_south = 0
        highest_east = 0
        current_east = 0
        to_visit = [idx]
        visited = [idx]
        last_dir = None
        while(to_visit):
            if rooms[to_visit[-1]]["north"] > 0 and rooms[to_visit[-1]]["north"]-1 not in visited:
                to_visit.append(rooms[to_visit[-1]]["north"]-1)
                visited.append(to_visit[-1])
                last_dir = "north"          
            elif rooms[to_visit[-1]]["west"] > 0 and rooms[to_visit[-1]]["west"]-1 not in visited:
                to_visit.append(rooms[to_visit[-1]]["west"]-1)
                visited.append(to_visit[-1])
                last_dir = "west"                                   
            elif rooms[to_visit[-1]]["east"] > 0 and rooms[to_visit[-1]]["east"]-1 not in visited:
                to_visit.append(rooms[to_visit[-1]]["east"]-1)
                visited.append(to_visit[-1])
                last_dir = "east"                            
            elif rooms[to_visit[-1]]["south"] > 0 and rooms[to_visit[-1]]["south"]-1 not in visited:
                to_visit.append(rooms[to_visit[-1]]["south"]-1)
                visited.append(to_visit[-1])
                last_dir = "south"            
            else:
                try:
                    last_dir = get_direction(to_visit[-1], to_visit[-2], rooms)                
                    to_visit.remove(to_visit[-1])
                except:
                    last_dir = None
                    to_visit.remove(to_visit[-1]) 
            current_south += 1 if last_dir == "south" else 0
            current_south -= 1 if last_dir == "north" else 0
            current_east += 1 if last_dir == "east" else 0
            current_east -= 1 if last_dir == "west" else 0
            highest_south = current_south if current_south > highest_south else highest_south
            highest_east = current_east if current_east > highest_east else highest_east
            

        my_dict["south"] = highest_south
        my_dict["east"] = highest_east 
        my_sizes.append(my_dict)
    return my_sizes

def print_map(rooms):
    for size,room in zip(sizes, rooms):
        position_x = max_sizes[1] - size["east"] - 1
        position_x = (base + base/2) * position_x + margen
        position_y = max_sizes[0] - size["south"] - 1
        position_y = (base + base/2) * position_y + margen
        draw_room(screen, position_x, position_y, base, room)
    
def save_map(raiz):
    fname = str(raiz)+"\imagenes\map.png"
    pg.image.save(screen, fname)

def map_builder_start(rooms):
    global width, height, margen, sizes, max_sizes, max_size, base, screen
    width = 1000
    height = 1000
    margen = 50

    sizes = set_sizes(rooms)
    max_sizes = get_size(sizes)

    max_size = max(max_sizes)
    base = (2*(width-2*margen))/(max_size*2+max_size-1)
    height = int((max_sizes[0]*base+(max_sizes[0]-1)*base/2) + 2*margen)
    width = int((max_sizes[1]*base+(max_sizes[1]-1)*base/2) + 2*margen)
    screen = pg.display.set_mode((width, height))
    screen.fill(grey)

white = (255, 255, 255)
blue = (0, 0, 255)
grey = (179, 176, 176)
red = (255, 0, 0)
black = (0, 0, 0)

width = 0
height = 0
margen = 0

sizes = None
max_sizes = None
max_size = 0

base = 0
height = 0
width = 0

screen = None



"""raiz = pathlib.Path(__file__).parent.parent.resolve()

white = (255, 255, 255)
blue = (0, 0, 255)
grey = (179, 176, 176)
red = (255, 0, 0)
black = (0, 0, 0)

width = 1000
height = 1000
margen = 50

sizes = get_size(set_sizes(rooms))

max_size = max(sizes)
base = (2*(width-2*margen))/(max_size*2+max_size-1)
height = int((sizes[0]*base+(sizes[0]-1)*base/2) + 2*margen)
width = int((sizes[1]*base+(sizes[1]-1)*base/2) + 2*margen)"""

