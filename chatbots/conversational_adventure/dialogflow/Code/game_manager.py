from dungeon import Dungeon
from player import Player
from character import Character
from action import Action
from item import Item
from game import Game
import random

def default_welcome_intent_game(req, dngn, contexts):
    dngn.reset()
    dngn.set_mins(5,1,1,1)
    dngn.aux()
    dngn.game = Game()
    dngn.game.build_dungeon(dngn)
    dngn.set_player_room(idx = 1)
    #dngn.players[dngn.game.turn].inventory.append("key")
    for r in dngn.rooms:
        print(r.doors.values())
        if r.characters:
            print("Characters")
            for c in r.characters:
                print(c.name)
        if r.items:
            print("Items")
            for i in r.items:
                print(i.name)
    return {
            "fulfillmentText":"Hello there!, I am the Game Manager. Do you want to start the game?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/start-game",
                    "lifespanCount": 1,
                }
            ],
        }

def default_fallback_intent_game(req, dngn, contexts):
    print(contexts[0])
    print(contexts[1])
    return {
            "fulfillmentText":"I didn't get that. Can you repeat?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
        }
    
def start_game_yes(req, dngn, contexts):
    return {
            "fulfillmentText": dngn.game.describe_room(dngn.players[dngn.game.turn].room) + " What do you want to do?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],
        }
    
def start_game_no(req, dngn, contexts):
    return {
            "fulfillmentText":"What about now?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/start-game",
                    "lifespanCount": 1,
                }
            ],
            
        }

def describe_room(req, dngn, contexts):
    return {
            "fulfillmentText": dngn.game.describe_room(dngn.players[dngn.game.turn].room),
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],
            
        }

######################################################################################
######################################################################################

# Player actions

######################################################################################
######################################################################################
    
def move_room(req, dngn, contexts):
    direction = req["queryResult"]["parameters"]["direction"].lower()
    door = dngn.players[dngn.game.turn].room
    if (door.doors[direction] > 0):
        dngn.set_player_room(door.doors[direction])
        return {
                "fulfillmentText": dngn.game.describe_room(dngn.players[dngn.game.turn].room) + " What do you want to do?",
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],
                
            }
    else:            
        return {
                "fulfillmentText": "Sorry that is not a valid direction. " + 
                 dngn.game.describe_room(dngn.players[dngn.game.turn].room),
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],
                
            }

def check_inventory(req, dngn, contexts):
    return {
            "fulfillmentText": dngn.players[dngn.game.turn].get_inventory(),
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
        }


######################################################################################

# Player actions - character

######################################################################################

def greet_character_game(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    try:
        idx = next(idx for idx, elem in enumerate(dngn.players[dngn.game.turn].room.characters) if elem.name == name) 
        print(idx)
        return {
            "fulfillmentText":dngn.players[dngn.game.turn].room.characters[idx].greetings,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],            
        }
    except:
        return {
            "fulfillmentText":"Sorry, there is not a character with that name in the room. " + 
                 dngn.game.describe_room(dngn.players[dngn.game.turn].room),
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],            
        }

def info_character_game(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    if 1==1:
        idx = next(idx for idx, elem in enumerate(dngn.players[dngn.game.turn].room.characters) if elem.name == name)
        character = dngn.players[dngn.game.turn].room.characters[idx]
        item = req["queryResult"]["parameters"]["item"].lower().capitalize()
        if not character.info:
            answer = "There is nothing left for me to tell you."
        elif item:
            answer = dngn.game.find_item_answer(dngn, character)
            dngn.game.delete_answer(answer, character)
        else:
            answer = random.choice(character.info)
            dngn.game.delete_answer(answer, character)
        return {
            "fulfillmentText": answer,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],            
        }
    else:
        return {
            "fulfillmentText":"Sorry, there is not a character with that name in the room. " + 
                 dngn.game.describe_room(dngn.players[dngn.game.turn].room),
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],            
        }

######################################################################################

# Player actions - items

######################################################################################
    
def interact_game_object(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["item"].lower()
    action = req["queryResult"]["parameters"]["action"].lower()
    item = dngn.get_item(name)
    if item in dngn.players[dngn.game.turn].room.items or item in dngn.players[dngn.game.turn].inventory:
        if action in item.actions:
            return eval(action+"_item(item, dngn)")
        else:
            return {
                    "fulfillmentText":"You can not " + action + " the " + name + ".",
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                            "lifespanCount": 1,
                        }
                    ],            
                }
    else:
        return {
                "fulfillmentText":"There is no " + name + " in this room.",
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],            
            }

def take_item(item, dngn):
    if item in dngn.players[dngn.game.turn].inventory:
        return {
                "fulfillmentText":"You already have the " + item.name + " in your inventory.",
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],            
            }
    else:
        dngn.players[dngn.game.turn].inventory.append(item)
        dngn.players[dngn.game.turn].room.items.remove(item)
        return {
                "fulfillmentText":"You have taken the " + item.name + ".",
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],            
            }

def open_item(item, dngn):
    if all(item in dngn.players[dngn.game.turn].inventory for item in item.actions["open"].item_need):
        item.open = True
        return {
                "fulfillmentText":"You have opened the " + item.name + ". " + item.describe_item_in(),
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],            
            }
    else:
        missing = [item for item in item.actions["open"].item_need if not item in dngn.players[dngn.game.turn].inventory]        
        return {
                "fulfillmentText":item.describe_item_need(missing),
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],            
            }
    
def read_item(item, dngn):   
    return {
        "fulfillmentText":"You can read: " + item.actions["read"].effect,
        "outputContexts": [
            {
                "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                "lifespanCount": 1,
            }
        ],            
    }
    



        
