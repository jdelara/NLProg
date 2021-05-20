from dungeon import Dungeon
from player import Player
from character import Character
from action import Action
from item import Item
import fallback

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

WELCOME

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def default_welcome_intent(req, dngn, contexts):
    dngn.reset()
    dngn.set_mins(5,1,1,1)
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
    rooms = int(req["queryResult"]["parameters"]["number"][0])
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
                "fulfillmentText":"So " + name + ". How much HP (health points) will " +
                name + " have?", 
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
    name = req["queryResult"]["outputContexts"][0]["parameters"]["item"].lower()
    name += " "+dngn.get_item_position(name)
    item = Item(name)
    dngn.add_item(item)
    return {
                "fulfillmentText":"Great!.Items will have a list of actions available:\n" \
                    "\t\t - Take\n\t\t - Consume\n\t\t - Open\n\t\t - Read\nPlease, select one or more between the options given", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/action-item",
                        "lifespanCount": 1,
                    }
                ],         
            }

def item_exists_no(req, dngn, contexts):
    return {
                "fulfillmentText":"Ok. Select another name for the item:", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/item-configuration",
                        "lifespanCount": 1,
                    }
                ],         
            }

def item_action(req, dngn, contexts): 
    actions = req["queryResult"]["parameters"]["action"]
    return eval("item_"+actions[0].lower()+"(dngn, actions)")

def item_take(dngn, actions, msg = ""):   
    item = dngn.get_item()
    action = Action("You can take the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":"Will taking the " + item.name + " be a winning condition?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_consume(dngn, actions, msg = ""):
    item = dngn.get_item()
    action = Action("You can consume the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nHow would the consumption of this item affect the player?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/item-consumption",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
    
def item_consumption(req, dngn, contexts):
    index = [idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith(contexts[0])]
    actions = req["queryResult"]["outputContexts"][index[0]]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].effect = req["queryResult"]["queryText"]
    return {
            "fulfillmentText":"Will consuming the " + item.name + " be a winning condition?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
    

def item_open(dngn, actions, msg = ""):
    item = dngn.get_item()
    action = Action("You can open the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nIs there anything you need to open the " + item.name + "?" , 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/open-need",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }
def open_need(req, dngn, contexts):
    index = [idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith(contexts[0])]
    actions = req["queryResult"]["outputContexts"][index[0]]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].set_item_need(req["queryResult"]["parameters"]["item"])
    return {
            "fulfillmentText":"What will the " + item.name + " have inside?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/open-in",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def open_in(req, dngn, contexts):
    index = [idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith(contexts[0])]
    actions = req["queryResult"]["outputContexts"][index[0]]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].set_item_in(req["queryResult"]["parameters"]["item"])
    return {
            "fulfillmentText":"Will opening the " + item.name + " be a winning condition?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def item_read(dngn, actions, msg = ""):
    item = dngn.get_item()
    action = Action("You can read the " + item.name)
    item.add_action(actions[0].lower(),action)
    return {
            "fulfillmentText":msg+"\nWhat is written in the " + item.name +"?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/read-description",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }

def read_description(req, dngn, contexts):
    index = [idx for idx, element in enumerate(req["queryResult"]["outputContexts"]) if element["name"].endswith(contexts[0])]
    actions = req["queryResult"]["outputContexts"][index[0]]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].desc = req["queryResult"]["queryText"]
    return {
            "fulfillmentText":"Will reading the " + item.name + " be a winning condition?", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/win-condition",
                    "parameters": {
                        "action": actions
                        },
                    "lifespanCount": 1,
                }
            ],         
        }


def win_condition_yes(req, dngn, contexts):
    actions = req["queryResult"]["outputContexts"][0]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].win = True
    if(actions[1:]):
        return eval("item_"+actions[1].lower()+"(dngn, actions[1:], 'To " + actions[0].lower() + " the " + item.name + " will be a winning condition')")
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
    actions = req["queryResult"]["outputContexts"][0]["parameters"]["action"]
    item = dngn.get_item()
    item.actions[actions[0].lower()].win = False
    if(actions[1:]):
        return eval("item_"+actions[1].lower()+"(dngn, actions[1:], 'To " + actions[0].lower() + " the " + item.name + " will NOT be a winning condition')")
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

def new_character(req, dngn, contexts):
    return {
            "fulfillmentText":"You will now set up a new character. Choose a name for him or her.",
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

def greet_character(req, dngn, contexts):
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

DUNGEON

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def end_configuration(req, dngn, contexts):
    dngn_info = dngn.dungeon_info()
    if(dngn.is_playable()):
        dngn = Dungeon()
        return {
                "fulfillmentText":"Your dungeon is now finished. " + dngn_info,
            }
    else:
        return(dngn.missing_values())


def save_context(req, contexts):
    print(contexts)
    print("\n")
    contexts[1] = contexts[0]
    try:
        context = req["queryResult"]["outputContexts"][0]["name"].split("/")[-1]
        contexts[0] = context if context != "__system_counters__" else contexts[0]
    except:
        contexts[0] = "context 1"
    print(contexts)
    print("-----------------------------\n")
    return contexts


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

FALLBACK

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def default_fallback_intent(req, dngn, contexts):
    return fallback.getFallback(req, contexts[0])
    


        