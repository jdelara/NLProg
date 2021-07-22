from conf_manager import character_name
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import pathlib
import math

def get_size(sizes):
    north = east = 0
    for size in sizes:
        north = size["south"] if size["south"]>north else north
        east = size["east"] if size["east"]>east else east
    return (north+1, east+1) 

def get_map_name(name):
    name = name.split()
    return name[0][0].upper() + name[0][-1]

def draw_character(screen, position_x, position_y, size, room, idx):
    pg.font.init() 
    row = round(math.sqrt(len(room.characters) + len(room.players) + len(room.items)))
    print(len(room.characters) + len(room.players) + len(room.items))
    print(position_x)
    print(position_y)
    print(size)
    print("******************************")
    if row > 0:
        myfont = pg.font.SysFont('Arial', int((size/(row*row)-size/5)))
        column = row
        painted_x = 1
        painted_y = 1
        margen = size/(row*2)   

        for character in room.characters:
            textsurface = myfont.render(get_map_name(character.name), False, green)
            rect = textsurface.get_rect()
            position_x = position_x + margen * (painted_x*2-1)
            position_y = position_y + margen * (painted_y*2-1)
            print(position_x)
            print(position_y)
            rect.center = position_x, position_y
            screen.blit(textsurface,rect)
            pg.draw.rect(screen, blue, rect, -1)
            #pg.draw.circle(screen, black, rect.center, int(size/(row*row)), 2)
            if painted_x == row-1:
                painted_x = 1
                painted_y = painted_y + 1
            else:
                painted_x += 1
            print("_____________________________")

        for item in room.items:
            textsurface = myfont.render(get_map_name(item.name), False, pink)
            rect = textsurface.get_rect()
            position_x = position_x + margen * (painted_x*2-1)
            position_y = position_y + margen * (painted_y*2-1)
            print(position_x)
            print(position_y)
            rect.center = position_x, position_y
            screen.blit(textsurface,rect)
            pg.draw.rect(screen, blue, rect, -1)
            #pg.draw.circle(screen, black, rect.center, int(size/(row*row)), 2)
            if painted_x == row-1:
                painted_x = 1
                painted_y = painted_y + 1
            else:
                painted_x += 1
            print("_____________________________")

        for player in room.players:
            textsurface = myfont.render(get_map_name(player.name), False, blue)
            rect = textsurface.get_rect()
            position_x = position_x + margen * (painted_x*2-1)
            position_y = position_y + margen * (painted_y*2-1)
            print(position_x)
            print(position_y)
            rect.center = position_x, position_y
            screen.blit(textsurface,rect)
            pg.draw.rect(screen, blue, rect, -1)
            #pg.draw.circle(screen, black, rect.center, int(size/(row*row)), 2)
            if painted_x == row-1:
                painted_x = 1
                painted_y = painted_y + 1
            else:
                painted_x += 1
            print("_____________________________")


def draw_room(screen, position_x, position_y, size, room, idx):
    rect = None
    # norte
    if room.visited or not room.visited:
        rect = pg.Rect(position_x, position_y, size, size)
        #rect.center = (position,position)    
        pg.draw.rect(screen, white, rect)
        pg.draw.rect(screen, blue, rect, 2)  
        draw_character(screen, position_x, position_y, size, room, idx)
        if room.doors["north"] > 0:
            draw_corridor(screen, (position_x + size*2/5, position_y-size/2), (size/5, size/2))
            pg.draw.line(screen, red, (position_x + size*2/5,position_y+3), (position_x + size*3/5,position_y+3), 5)
        # sur
        if room.doors["south"] > 0:
            draw_corridor(screen, (position_x + size*2/5, position_y+size), (size/5, size/2))
            pg.draw.line(screen, red, (position_x + size*2/5,position_y+size-3), (position_x + size*3/5,position_y+size-3), 5)
        # este
        if room.doors["east"] > 0:
            draw_corridor(screen, (position_x+size,position_y + size*2/5), (size/2,size/5))
            pg.draw.line(screen, red, (position_x+size-3,position_y + size*2/5), (position_x+size-3,position_y + size*3/5), 5) 
        # oeste
        if room.doors["west"] > 0:
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
    i = 0
    for size,room in zip(sizes, rooms):
        position_x = max_sizes[1] - size["east"] - 1
        position_x = (base + base/2) * position_x + margen
        position_y = max_sizes[0] - size["south"] - 1
        position_y = (base + base/2) * position_y + margen
        draw_room(screen, position_x, position_y, base, room, i)
        i += 1
    
def save_map(path):
    fname = path
    pg.image.save(screen, fname)

def map_builder_start(rooms):
    global width, height, margen, sizes, max_sizes, max_size, base, screen
    width = 1000
    height = 1000
    margen = 50

    sizes = set_sizes([room.doors for room in rooms])
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
green = (128,255,0)
pink = (255,0,255)

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

