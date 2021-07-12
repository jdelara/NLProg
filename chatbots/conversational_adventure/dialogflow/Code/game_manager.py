from dungeon import Dungeon
from player import Player
from character import Character
from action import Action
from item import Item

import random

def default_welcome_intent_game(req, dngn, contexts):
    dngn.reset()
    dngn.set_mins(5,1,1,1)
    dngn.aux()
    dngn.game.build_dungeon(dngn)
    for player in dngn.players:
        player.room = dngn.rooms[0]
        dngn.rooms[0].players.append(player)  
    key = dngn.characters[0].items[0]
    dngn.players[dngn.game.turn].inventory.append(key)
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
            "fulfillmentText":"Hello there!, I am the Game Manager. Choose a character to play as:" + dngn.print_remain_players(),            
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/select-player",
                    "lifespanCount": 1,
                }
            ]            
        }

def default_fallback_intent_game(req, dngn, contexts):
    return {
            "fulfillmentText":"I didn't get that. Can you repeat?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
        }

def select_player(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    if not name in dngn.remain_players():
        return {
            "fulfillmentText":"Sorry, '" + name + "' is not a valid name. Select one from the list: " + dngn.print_remain_players(),
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/select-player",
                    "lifespanCount": 1,
                }
            ],            
        }
    else:
        player = next(player for player in dngn.players if player.name == name)
        human_name = req["originalDetectIntentRequest"]["payload"]["data"]["from"]["first_name"]
        human_id = str(req["originalDetectIntentRequest"]["payload"]["data"]["from"]["id"])
        if not dngn.human_has_player(human_id):   
            player.human_name = human_name
            player.human_id = human_id
            if dngn.remain_players():
                return {
                    "fulfillmentText":name + " assigned to " + player.human_name + ". Select another player from the list. " + 
                        dngn.print_remain_players(),                        
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/select-player",
                            "lifespanCount": 1,
                        }
                    ],
                }            
            else:
                dngn.game.started = True
                text = name + " assigned to " + player.human_name + ". All players have been selected. Game is starting.\n\n\n" + \
                        dngn.describe_turn() + dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn)
                return {
                    "fulfillmentText":text,
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                            "lifespanCount": 1,
                        }
                    ],
                    "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                    "payload":{}
                }
        else:
            return {
                    "fulfillmentText":human_name + " has already selected a player. Please, choose a player from the list below:" + dngn.print_remain_players(),
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/select-player",
                            "lifespanCount": 1,
                        }
                    ],
                }

def describe_room(req, dngn, contexts):
    text = dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn)
    return {
            "fulfillmentText": text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],  
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}          
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
        dngn.players[dngn.game.turn].room.players.remove(dngn.players[dngn.game.turn])
        dngn.set_player_room(door.doors[direction])
        dngn.change_turn()
        text = dngn.describe_turn() + dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn) + " What do you want to do?"
        return {
                "fulfillmentText":  text,
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],
                "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                "payload":{} 
            }
    else:   
        text = "Sorry that is not a valid direction. " + dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn)         
        return {
                "fulfillmentText": text,
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],
                "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                "payload":{} 
            }

def check_inventory(req, dngn, contexts):
    text = dngn.players[dngn.game.turn].get_inventory()
    return {
            "fulfillmentText": text,            
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{} 
        }


######################################################################################

# Player actions - character

######################################################################################

def greet_character_game(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    try:
        idx = next(idx for idx, elem in enumerate(dngn.players[dngn.game.turn].room.characters) if elem.name == name) 
        text = dngn.players[dngn.game.turn].room.characters[idx].greetings
        return {
            "fulfillmentText": text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ], 
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}            
        }
    except:
        text = "Sorry, there is not a character with that name in the room. " + dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn)
        return {
            "fulfillmentText": text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],    
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}         
        }

def info_character_game(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    try:
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
        if any(i.name in answer for i in character.items):
            item = next(item for item in character.items if item.name in answer)
            answer += " You've recieved a " + item.name + " from " + character.name + "."
            dngn.players[dngn.game.turn].inventory.append(item)
        return {
            "fulfillmentText": answer,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ], 
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(answer),
            "payload":{}           
        }
    except:
        text = "Sorry, there is not a character with that name in the room. " + dngn.game.describe_room(dngn.players[dngn.game.turn].room, dngn)
        return {
            "fulfillmentText":text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],     
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(answer),
            "payload":{}        
        }

######################################################################################

# Player actions - items

######################################################################################
    
def interact_game_object(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["item"].lower()
    action = req["queryResult"]["parameters"]["action"].lower()
    try:
        item = dngn.get_item(name)
    except:
        item = None
    if item in dngn.players[dngn.game.turn].room.items or item in dngn.players[dngn.game.turn].inventory:
        action = "consume" if action == "drink" else action
        if action in item.actions:
            return eval(action+"_item(item, dngn)")
        else:
            text = "You can not " + action + " the " + name + "."
            return {
                    "fulfillmentText":text,
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                            "lifespanCount": 1,
                        }
                    ],
                    "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                    "payload":{}              
                }
    else:
        text = "There is no " + name + " in this room."
        return {
                "fulfillmentText":text,
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],  
                "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                "payload":{}            
            }

def take_item(item, dngn):
    if item in dngn.players[dngn.game.turn].inventory:
        text = "You already have the " + item.name + " in your inventory."
        return {
                "fulfillmentText":text,
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ], 
                "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                "payload":{}           
            }
    else:
        dngn.players[dngn.game.turn].inventory.append(item)
        dngn.players[dngn.game.turn].room.items.remove(item)        
        item.inside.actions["open"].item_in.remove(item) if item.inside else None
        item.inside = None        
        if item.actions["take"].win:
            return end_game()
        if item.actions["take"].lose:
            return game_over()
        else:
            dngn.change_turn()
            text = "You have taken the " + item.name + "."
            return {
                    "fulfillmentText":"You have taken the " + item.name + ".",
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                            "lifespanCount": 1,
                        }
                    ],  
                    "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                    "payload":{}           
                }

def open_item(item, dngn):
    if all(item in dngn.players[dngn.game.turn].inventory for item in item.actions["open"].item_need):
        item.open = True
        for i in item.actions["open"].item_in:
            dngn.items.append(i)
            dngn.players[dngn.game.turn].room.items.append(i)
        if item.actions["open"].win:
            return end_game()        
        if item.actions["open"].lose:
            return game_over()
        else:
            dngn.change_turn()
            text = "You have opened the " + item.name + ". " + item.describe_item_in()
            return {
                    "fulfillmentText":text,
                    "outputContexts": [
                        {
                            "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                            "lifespanCount": 1,
                        }
                    ], 
                    "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                    "payload":{}           
                }
    else:
        missing = [item for item in item.actions["open"].item_need if not item in dngn.players[dngn.game.turn].inventory]   
        text = item.describe_item_need(missing)     
        return {
                "fulfillmentText":text,
                "outputContexts": [
                    {
                        "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                        "lifespanCount": 1,
                    }
                ],   
                "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
                "payload":{}           
            }
    
def read_item(item, dngn):   
    if item.actions["read"].win:
        return end_game()
    if item.actions["read"].lose:
        return game_over()
    else:
        dngn.change_turn()
        text = "You can read: " + item.actions["read"].effect
        return {
            "fulfillmentText":text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ], 
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}             
        }

def consume_item(item, dngn): 
    dngn.items.remove(item)
    dngn.players[dngn.game.turn].inventory.remove(item) if item in dngn.items else None
    item.inside.actions["open"].item_in.remove(item) if item.inside else None
    item.inside = None
    dngn.player[dngn.game.turn].health += item.actions["consume"].hp
    if item.actions["consume"].win and dngn.player[dngn.game.turn].health > 0:
        return end_game()
    if item.actions["consume"].lose or dngn.player[dngn.game.turn].health <= 0:
        return game_over()
    else:
        dngn.change_turn()
        text = "You have consumed the " + item.name + "."
        return {
            "fulfillmentText":text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],     
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}         
        }

def take_note(req, dngn, contexts):
    return {
            "fulfillmentText":"What do you want to write as a note?",
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/write-note",
                    "lifespanCount": 1,
                }
            ],            
        }

def write_note(req, dngn, contexts):
    dngn.players[dngn.game.turn].notes.append(req["queryResult"]["queryText"])
    text = "Note saved."
    return {
            "fulfillmentText":text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ], 
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}            
        }

def read_notes(req, dngn, contexts):
    answer = dngn.players[dngn.game.turn].get_notes() if dngn.players[dngn.game.turn].notes else "You do not have any notes for the moment."
    return {
            "fulfillmentText": answer,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ],   
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(answer),
            "payload":{}          
        }
######################################################################################

# Extra

######################################################################################

def game_over():
    return {
        "fulfillmentText":"GAME OVER",        
    }

def end_game():
    return {
        "fulfillmentText":"CONGRATULATIONS, YOU HAVE COMPLETED THE DUNGEON",        
    }

def help(req, dngn, contexts):
    text = dngn.game.command_list()
    return {
            "fulfillmentText":text,
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/player-action",
                    "lifespanCount": 1,
                }
            ], 
            "fulfillmentMessages":dngn.game.button_telegram_fulfillmentMessages(text),
            "payload":{}  
        }





        
