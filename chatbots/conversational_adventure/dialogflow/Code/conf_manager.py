from dungeon import Dungeon
from player import Player
from character import Character
from action import Action
from item import Item
import fallback



def testing(req, dngn, contexts):
    print("ENTRO")
    return {                 
        "fulfillmentText": "testing not telegram",
        "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    "\'<b>'TELEGRAM TESTING A BOT\'<\b>'"
                ]                
            },            
            "platform": "TELEGRAM",
            "parse_mode": "HTML"
        },
        {
            "text": {
                "text": [
                    "testing not telegram"
                ]
            }
        }
        ],
    } 
        
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

WELCOME

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def default_welcome_intent_conf(req, dngn, contexts):
    dngn.reset()
    dngn.set_mins(5,1,1,1)
    dngn.aux()
    return {
            "fulfillmentText":"Hello traveller! I am your Dungeon Configurator Assistant.\n" \
                + "Have in mind that the minimum requirements for the cave to be playable are:\n" + \
                "\t\t-" + str(dngn.min_rooms) + " room(s)\n\t\t-" + str(dngn.min_players) + " player(s)\n\t\t-" \
                     + str(dngn.min_characters) + " character(s)\n\t\t-" + str(dngn.min_items) + " item(s)\n" + \
                "What's the first thing you want to set up?",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],
        }


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

ROOM

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def new_room_select_number(req, dngn, contexts):
    rooms = int(req["queryResult"]["parameters"]["number"])
    dngn.set_number_of_rooms(rooms)
    return {
            "fulfillmentText":"So " + str(rooms) + " rooms. What else do you want to set up?",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],
        }

def new_room(req, dngn, contexts):
    return {
            "fulfillmentText":"Great! How many rooms do you want the game to have?",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/number-of-rooms",
                    "lifespanCount": 1,
                }
            ],
        }

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

PLAYER

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def new_player(req, dngn, contexts):
    return {
            "fulfillmentText":"You will now set up a new player. Choose a name for him or her.",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-configuration",
                    "lifespanCount": 1,
                }
            ],
        }

def player_name(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["playerName"].lower().capitalize()
    if not dngn.check_player_name(name):
        player = Player(name)
        dngn.add_player(player)
        return {
                "fulfillmentText":"How much HP (health points) will " + name + " have?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/hp-player",
                        "lifespanCount": 1,
                    }
                ],         
            }
    else:
        return {
                "fulfillmentText":"Name '" + name + "' is already taken by another player. Please, choose another name.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-configuration",
                        "lifespanCount": 1,
                    }
                ],         
            }

def player_health(req, dngn, contexts):
    player = dngn.get_player()
    health = req["queryResult"]["parameters"]["health"]
    if health > 0:
        player.set_health(health)
        return {
                "fulfillmentText":"So " + player.get_name() + " will have " + str(health) + " HP. What else do you want to set up?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"Player's health must a number greater than 0. Please, type a valid number.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/hp-player",
                        "lifespanCount": 1,
                    }
                ],           
            }

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

ITEM

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def new_item(req, dngn, contexts):
    return {
            "fulfillmentText":"You will now set up a new item. Please, name the item.",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/item-configuration",
                    "lifespanCount": 1,
                }
            ],
        }

def item_name(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["item"].lower()
    if not dngn.check_item_name(name):
        item = Item(name)
        dngn.add_item(item)
        return {
                "fulfillmentText":"So a " + name + ". Items will have a list of actions available:\n" \
                "\t\t - Take\n\t\t - Consume\n\t\t - Open\n\t\t - Read\nPlease, select one or more between the options given", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/action-item",
                        "parameters": {
                            "name": name
                            },
                        "lifespanCount": 1,
                    }
                ],         
            }
    else:
        return {
                "fulfillmentText":"Item '" + name + "' already exists. Do you want to create another item with the same name?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/exists-item",
                        "parameters": {
                            "item": name,
                            },
                        "lifespanCount": 2,
                    }
                ],         
            }
def item_exists_yes(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"]) if elem["name"].endswith("exists-item"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["item"].lower()
    name += " "+dngn.get_item_position(name)
    item = Item(name)
    dngn.add_item(item)
    return {
                "fulfillmentText":"Great!.Items will have a list of actions available:\n" \
                    "\t\t - Take\n\t\t - Consume\n\t\t - Open\n\t\t - Read\nPlease, select one or more between the options given", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/action-item",
                        "parameters": {
                            "name": name
                            },
                        "lifespanCount": 1,
                    }
                ],         
            }

def item_exists_no(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"]) if elem["name"].endswith("exists-item"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["item"].lower()
    return {
                "fulfillmentText":"Ok. Select another name for the item:", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/item-configuration",
                        "parameters": {
                            "name": name
                            },
                        "lifespanCount": 1,
                    }
                ],         
            }

def item_action(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"]) if elem["name"].endswith("action-item"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"].lower()  
    actions = req["queryResult"]["parameters"]["action"]
    return eval("item_"+actions[0].lower()+"(dngn, actions, name)")

def item_take(dngn, actions, name, msg = ""):   
    item = dngn.get_item(name)
    action = Action("You can take the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":"Will taking the " + item.name + " be a winning condition, losing condition or none of them", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_consume(dngn, actions, name, msg = ""):
    item = dngn.get_item(name)
    action = Action("You can consume the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nHow would the consumption of this item affect the player?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/item-consumption",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
    
def item_consumption(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("item-consumption"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    item.actions[actions[0].lower()].effect = req["queryResult"]["queryText"]
    return {
            "fulfillmentText":"Will consuming the " + item.name + " be a winning condition, losing condition or none of them", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
    

def item_open(dngn, actions,name, msg = ""):
    item = dngn.get_item(name)
    action = Action("You can open the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nIs there anything you need to open the " + item.name + "?" , 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/open-need",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
def item_open_need(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("open-need"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    item.actions[actions[0].lower()].set_item_need(req["queryResult"]["parameters"]["item"])
    return {
            "fulfillmentText":"What will the " + item.name + " have inside?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/open-in",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_open_in(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("open-in"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    item.actions[actions[0].lower()].set_item_in(req["queryResult"]["parameters"]["item"])
    for i in dngn.items:
        i.inside = item.name if i.name == req["queryResult"]["parameters"]["item"] else None
    return {
            "fulfillmentText":"Will opening the " + item.name + " be a winning condition, losing condition or none of them", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_read(dngn, actions, name, msg = ""):
    item = dngn.get_item(name)
    action = Action("You can read the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nWhat is written in the " + item.name +"?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/read-description",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_read_description(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("read-description"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    item.actions[actions[0].lower()].desc = req["queryResult"]["queryText"]
    return {
            "fulfillmentText":"Will reading the " + item.name + " be a winning condition, losing condition or none of them", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions,
                        "name": name
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def win_condition(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("win-condition"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    if req["queryResult"]["parameters"]["win"]:
        item.actions[actions[0].lower()].win = True
        item.actions[actions[0].lower()].lose = False
        sen = " will be a winning condition')"        
    elif req["queryResult"]["parameters"]["lose"]:
        item.actions[actions[0].lower()].win = False
        item.actions[actions[0].lower()].lose = True
        sen = " will be a losing condition')"
    else:
        item.actions[actions[0].lower()].win = False
        item.actions[actions[0].lower()].lose = False
        sen = " will not be neither a winning nor a losing condition')"
    if (actions[1:]):
        return eval("item_"+actions[1].lower()+"(dngn, actions[1:], name, 'To " + actions[0].lower() \
            + " the " + item.name + sen)
    else:
        return {
                "fulfillmentText":"Perfect! The " + item.name + " has been set up. What else do you want to configure?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],         
            }

def win_condition_yes(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("win-condition"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    
    if(actions[1:]):
        return eval("item_"+actions[1].lower()+"(dngn, actions[1:], name, 'To " + actions[0].lower() \
            + " the " + item.name + " will be a winning condition')")
    else:
        return {
                "fulfillmentText":"Perfect! The " + item.name + " has been set up. What else do you want to configure?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],         
            }

def win_condition_no(req, dngn, contexts):
    idx = next(idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith("win-condition"))
    actions = req["queryResult"]["outputContexts"][idx]["parameters"]["action"]
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["name"]
    item = dngn.get_item(name)
    item.actions[actions[0].lower()].win = False
    if(actions[1:]):
        return eval("item_"+actions[1].lower()+"(dngn, actions[1:], name, 'To " + actions[0].lower() \
             + " the " + item.name + " will NOT be a winning condition')")
    else:
        return {
                "fulfillmentText":"Perfect! The " + item.name + " has been set up. What else do you want to configure?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],         
            }
        

    
    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

CHARACTER

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def new_character(req, dngn, contexts, msg ="You will now set up a new character. "):
    return {
            "fulfillmentText":msg+"Choose a name for him or her.",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/character-configuration",
                    "lifespanCount": 1,
                }
            ],
        }

def character_name(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    if not dngn.check_character_name(name):
        character = Character(name)
        dngn.add_character(character)
        return {
                "fulfillmentText":"So " + name + ". How will " + name + " greet you?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/greet-character",
                        "lifespanCount": 1,
                    }
                ],         
            }
    else:
        return {
                "fulfillmentText":"Name '" + name + "' is already taken by another character. Please, choose another name.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/character-configuration",
                        "lifespanCount": 1,
                    }
                ],         
            }

def greet_character_conf(req, dngn, contexts):
    character = dngn.get_character()
    character.greetings = req["queryResult"]["queryText"]
    return {
            "fulfillmentText":"What kind of information " + character.name + " will provide?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/inf-character",
                    "lifespanCount": 1,
                }
            ],           
        }

def inf_character(req, dngn, contexts):
    character = dngn.get_character()
    character.info.append(req["queryResult"]["queryText"])
    character.items.extend(req["queryResult"]["parameters"]["item"])
    return {
            "fulfillmentText":"Anything else?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/inf-character-else",
                    "lifespanCount": 1,
                }
            ],           
        }

def inf_character_else_yes(req, dngn, contexts):  
    character = dngn.get_character()
    return {
            "fulfillmentText":"Ok, what else will" + character.name + "tell you?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/inf-character",
                    "lifespanCount": 1,
                }
            ],           
        }

def inf_character_else_no(req, dngn, contexts):  
    return {
            "fulfillmentText":"Great, what else do you want to set up?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],           
        }


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

SETTINGS

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def settings(req, dngn, contexts):
    return {
        "fulfillmentText": dngn.dungeon_info(),
        "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
        }


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

UPDATE

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#################################################
#------------------  Player  -------------------#
#################################################

def change_player(req, dngn, contexts):  
    if(dngn.players):   
        return {
                "fulfillmentText":"Which player do you want to modify?\n" + dngn.players_list() , 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"The dungeon has no players yet. What do you want to set up?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }

def modify_player_selection(req, dngn, contexts):  
    name = req["queryResult"]["parameters"]["playerName"].lower().capitalize()
    if dngn.check_player_name(name):
        return {
                "fulfillmentText":"What do you want to modify from " + name + ", the name or the health points?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-stat",
                        "parameters": {
                            "player": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"There is no player called '" + name + "'. Please, select one from the list\n" + dngn.players_list(), 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-stat",
                        "parameters": {
                            "player": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }

def modify_player_stat(req, dngn, contexts): 
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-player-stat"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["player"].lower().capitalize()  
    stat = req["queryResult"]["parameters"]["stat"].lower()
    if (stat == "name"):
        return {
            "fulfillmentText":"Select a new name for " + name + ".\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-name",
                        "parameters": {
                            "player": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    elif (stat == "hp" or stat == "health"):
        return {
            "fulfillmentText":"How much HP (health points) will " + name + " have?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-health",
                        "parameters": {
                            "player": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
            "fulfillmentText":"Sorry, could you repeat that?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-stat",
                        "parameters": {
                            "character": name
                        },
                        "lifespanCount": 1,
                    }
                ],
        }
    
def modify_player_name(req, dngn, contexts):    
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-player-name"))
    old_name = req["queryResult"]["outputContexts"][idx]["parameters"]["player"].lower().capitalize()
    new_name = req["queryResult"]["parameters"]["playerName"].lower().capitalize()
    if not dngn.check_player_name(new_name):            
        idx = next(idx for idx, player in enumerate(dngn.players) if old_name==player.name)
        dngn.players[idx].name = new_name
        return {
            "fulfillmentText":"Name " + old_name + " is now " + new_name + ".\nWhat do you want to set up next?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"Name '" + new_name + "' is already taken by another player. Please, choose another name.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-name",
                        "parameters": {
                            "player": old_name
                        },
                        "lifespanCount": 1,
                    }
                ],         
            }

def modify_player_health(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-player-health"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["player"].lower().capitalize()
    health = req["queryResult"]["parameters"]["health"]
    idx = next(idx for idx, player in enumerate(dngn.players) if name==player.name)
    dngn.players[idx].health = health
    return {
        "fulfillmentText":name + " health points set to " + str(health) + ".\nWhat do you want to set up next?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],           
        }

#################################################
#----------------- Character  ------------------#
#################################################

def change_character(req, dngn, contexts):  
    if(dngn.characters):
        return {
                "fulfillmentText":"Which character do you want to modify?\n" + dngn.characters_list() , 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"The dungeon has no characters yet. What do you want to set up?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }

def modify_character_selection(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    index = [idx for idx, character in enumerate(dngn.characters) if name==character.name]
    if (index):
        return {
                "fulfillmentText":"What do you want to modify from " + name + ", the name, the way he/she will greet the player or the info " + \
                "he/she will provide?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-stat",
                        "parameters": {
                            "character": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"Name '" + name + "' does not exist. Please, select one from the list.\n" + dngn.characters_list(), 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }

def modify_character_stat(req, dngn, contexts):  
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-character-stat"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["character"] 
    stat = req["queryResult"]["parameters"]["stat"].lower()
    if (stat == "name"):
        return {
            "fulfillmentText":"Select a new name for " + name + ".", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-name",
                        "parameters": {
                            "character": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    elif (stat == "info" or stat == "information"):
        idx = next(idx for idx, character in enumerate(dngn.characters) if name==character.name)
        dngn.characters[idx].info = []    
        return {
            "fulfillmentText":"What will " + name + " tell you?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-info",
                        "parameters": {
                            "character": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    elif (stat == "greetings" or stat == "greet"):
        return {
            "fulfillmentText":"How will " + name + " greet the player?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-greet",
                        "parameters": {
                            "character": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
            "fulfillmentText":"Sorry, could you repeat that?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-stat",
                        "parameters": {
                            "character": name
                        },
                        "lifespanCount": 1,
                    }
                ],   
        }    

def modify_character_name(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-character-name"))
    old_name = req["queryResult"]["outputContexts"][idx]["parameters"]["character"].lower().capitalize()
    new_name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    if not dngn.check_character_name(new_name):            
        idx = next(idx for idx, character in enumerate(dngn.characters) if old_name==character.name)
        dngn.characters[idx].name = new_name
        return {
            "fulfillmentText":"Name " + old_name + " is now " + new_name + ".\nWhat do you want to set up next?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"Name '" + new_name + "' is already taken by another character. Please, choose another name.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-player-name",
                        "parameters": {
                            "player": old_name
                        },
                        "lifespanCount": 1,
                    }
                ],         
            }
        
def modify_character_greet(req, dngn, contexts):    
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-character-greet"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["character"]  
    idx = next(idx for idx, character in enumerate(dngn.characters) if name==character.name)
    dngn.characters[idx].greetings = req["queryResult"]["queryText"]
    return {
        "fulfillmentText":"Greeting modified. What else do you want to set up?\n", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],           
        }    

def modify_character_info(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-character-info"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["character"]  
    idx = next(idx for idx, character in enumerate(dngn.characters) if name==character.name)
    dngn.characters[idx].info.append(req["queryResult"]["queryText"])
    return {
            "fulfillmentText":"Anything else?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-inf-character-else",
                    "parameters": {
                        "character": name
                        },
                    "lifespanCount": 1,
                }
            ],           
        }  

def modify_inf_character_else_yes(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-in-character-else"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["character"]
    return {
            "fulfillmentText":"Ok, what else will " + name + " tell you?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-character-info",
                    "parameters": {
                        "character": name
                        },
                    "lifespanCount": 1,
                }
            ],           
        }

def modify_inf_character_else_no(req, dngn, contexts):
    return {
            "fulfillmentText":"Great!, what else do you want to set up?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],           
        }

#################################################
#-------------------- Item  --------------------#
#################################################

def change_item(req, dngn, contexts):  
    if(dngn.items):
        return {
                "fulfillmentText":"Which item do you want to modify?\n" + dngn.items_list() , 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-item-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"The dungeon has no characters yet. What do you want to set up?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }
    
def modify_item_selection(req, dngn, contexts):      
    name = req["queryResult"]["parameters"]["item"].lower()
    index = [idx for idx, item in enumerate(dngn.items) if name==item.name]
    if (index):
        return {
                "fulfillmentText":"What do you want to modify from " + name + ", the name or the actions?\n", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-item-stat",
                        "parameters": {
                            "item": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    else:
        return {
                "fulfillmentText":"Name '" + name + "' does not exist. Please, select one from the list.\n" + dngn.items_list(), 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-item-selection",
                        "lifespanCount": 1,
                    }
                ],           
            }

def modify_item_stat(req, dngn, contexts):  
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-item-stat"))
    name = req["queryResult"]["outputContexts"][idx]["parameters"]["item"] 
    stat = req["queryResult"]["parameters"]["stat"].lower()
    if (stat == "name"):
        return {
            "fulfillmentText":"Select a new name for the '" + name + "'.", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-item-name",
                        "parameters": {
                            "item": name
                            },
                        "lifespanCount": 1,
                    }
                ],           
            }
    elif (stat == "action" or stat == "actions"):
        item = dngn.get_item(name)
        item.actions = {}
        return {
            "fulfillmentText":"You are about to reset the actions for the " + name + ". List of actions available:\n" \
                "\t\t - Take\n\t\t - Consume\n\t\t - Open\n\t\t - Read\nPlease, select one or more between the options given",  
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/action-item",
                        "parameters": {
                            "name": name
                        },
                        "lifespanCount": 1,
                    }
                ], 
        }
    else:
        return {
            "fulfillmentText":"Sorry, could you repeat that?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/modify-item-stat",
                        "parameters": {
                            "item": name
                        },
                        "lifespanCount": 1,
                    }
                ], 
        }
    

def modify_item_name(req, dngn, contexts):
    idx = next(idx for idx, elem in enumerate(req["queryResult"]["outputContexts"])if elem["name"].endswith("modify-item-name"))
    old_name = req["queryResult"]["outputContexts"][idx]["parameters"]["item"].lower()
    new_name = req["queryResult"]["parameters"]["newItem"].lower()
    print(old_name)
    print(new_name)
    print("\n\n")
    idx = next(idx for idx, item in enumerate(dngn.items) if old_name==item.name)
    if dngn.check_item_name(new_name):
        new_name += " "+dngn.get_item_position(new_name)
    dngn.items[idx].name = new_name    
    return {
            "fulfillmentText":"Item renamed to " + new_name + ". What else do you want to set up?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "parameters": {
                        "player": old_name
                    },
                    "lifespanCount": 1,
                }
            ],         
        }


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DELETE

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def delete_item(req, dngn, contexts):
    if(dngn.items):
        return {
            "fulfillmentText": "Which one do you want to delete?\n" + dngn.items_list(),
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-item-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    else:
        return {
            "fulfillmentText": "There are no items created. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }

def delete_item_selection(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["item"]
    try:
        idx = next(idx for idx, item in enumerate(dngn.items) if item.name == name)
        dngn.items.pop(idx)
        return {
            "fulfillmentText": "The item '" + name + "' has been deleted successfully. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    except:
        return {
                "fulfillmentText": "There is no item called '" + name + "'. Please, choose one from the list.\n" + dngn.items_list(),
                "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-player-selection",
                            "lifespanCount": 1,
                        }
                    ],
                }
    

def delete_character(req, dngn, contexts):
    if(dngn.characters):
        return {
            "fulfillmentText": "Which one do you want to delete?\n" + dngn.characters_list(),
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-character-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    else:
        return {
            "fulfillmentText": "There are no characters created yet. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }

def delete_character_selection(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    try:
        idx = next(idx for idx, character in enumerate(dngn.characters) if name==character.name)
        dngn.characters.pop(idx)
        return {
            "fulfillmentText": "The character '" + name + "' has been deleted successfully. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    except:
        return {
                "fulfillmentText": "There is no character called '" + name + "'. Please, repeat the name.\n" + dngn.characters_list(),
                "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-player-selection",
                            "lifespanCount": 1,
                        }
                    ],
                }
    
def delete_player(req, dngn, contexts):
    if(dngn.players):
        return {
            "fulfillmentText": "Which one do you want to delete?\n" + dngn.players_list(),
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    else:
        return {
            "fulfillmentText": "There are no players created yet. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }

def delete_player_selection(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["playerName"].lower().capitalize()
    try:
        idx = next(idx for idx, player in enumerate(dngn.players) if name==player.name)
        dngn.players.pop(idx)
        return {
            "fulfillmentText": "The player '" + name + "' has been deleted successfully. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    except:
        return {
            "fulfillmentText": "There is no player called '" + name + "'. Please, repeat the name.\n" + dngn.players_list(),
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/delete-player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DUNGEON

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def end_configuration(req, dngn, contexts):
    missing_items = dngn.missing_items()
    if not missing_items:
        if(dngn.is_playable()): 
            dngn.set_items_inside()       
            return {
                    "fulfillmentText":"Your dungeon is almost finished. Please choose a name for this it.",
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/dungeon-name",
                            "lifespanCount": 1,
                        }
                    ],
                }            
        else:
            return {
                "fulfillmentText":"Your dungeon is missing some configuration\n" + dngn.missing_values() + "What do you want to set up?",
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }
    else:
        return {
                    "fulfillmentText":"You can't finish the dungeon because there are some items not created yet:\n\t\t-" + '\n\t\t- '.join(missing_items),
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/dungeon-name",
                            "lifespanCount": 1,
                        }
                    ],
                }

def dungeon_name(req, dngn, contexts):
    name = req["queryResult"]["parameters"]["dungeon"].title()
    # COMPROBACION DE SI YA EXISTE
    dngn.name = name
    return {
            "fulfillmentText":"'" + name + "' is now finished. " + dngn.dungeon_info(),            
        }   
    

def reset_game(req, dngn, contexts):
    return {
            "fulfillmentText": "You are about to reset the configuration. This action cannot be undone. Are you sure?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/reset-game",
                        "lifespanCount": 1,
                    }
                ],
            }

def reset_game_yes(req, dngn, contexts):
    dngn.reset()
    return {
            "fulfillmentText": "All data has been deleted. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }

def reset_game_no(req, dngn, contexts):
    return {
            "fulfillmentText": "Ok. What do you want to set up next?",
            "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],
            }





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

FALLBACK

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def default_fallback_intent_conf(req, dngn, contexts):
    return fallback.getFallback(req, contexts[0])       