from dungeon import Dungeon
from player import Player
from character import Character
from item import Item
import fallback

"""

WELCOME

"""


def default_welcome_intent(req, dngn, contexts):
    dngn.reset()
    print("Entro en el welcome intent")
    return {
            "fulfillmentText":"Hello traveller! I am your Dungeon Configurator Assistant. What do you want to set up?",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],
        }


"""

ROOM

"""

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
    print("Entrando en new room")
    return {
            "fulfillmentText":"Great! How many rooms do you want the game to have?",
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/number-of-rooms",
                    "lifespanCount": 1,
                }
            ],
        }

"""

PLAYER

"""

def new_player(req, dngn, contexts):
    print("Entrando en new player")
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
    print("Entrando en player name")
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
    print("Entrando en player health")
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

"""

ITEM

"""

def new_item(req, dngn, contexts):
    print("Entrando en new item")
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
    print("Entrando en item name")
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
    print("Entrando a item exists yes")
    name = req["queryResult"]["outputContexts"][0]["parameters"]["item"].lower()
    name += "_"+dngn.get_item_position(name)
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
    print("Entrando a item exists no")
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
    print("Entrando en item action")
    return {
                "fulfillmentText":"TBI", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                        "lifespanCount": 1,
                    }
                ],         
            }

"""

CHARACTER

"""

def new_character(req, dngn, contexts):
    print("Entrando en new character")
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
    print("Entrando en character name")
    name = req["queryResult"]["parameters"]["characterName"].lower().capitalize()
    if not dngn.check_character_name(name):
        character = Character(name)
        dngn.add_character(character)
        return {
                "fulfillmentText":"So " + name + ". What will the purpose of this character be?", 
                "outputContexts": [
                    {
                        "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/purpose-character",
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

def character_purpose(req, dngn, contexts):
    print("Entrando en character purpose")
    character = dngn.get_character()
    purpose = req["queryResult"]["queryText"]
    character.set_desc(purpose)

    try:
        character.add_item(req["queryResult"]["parameters"]["item"][0],  req["queryResult"]["parameters"]["place"])        
    except IndexError:
        print("Index out of range")
    except:
        print("Another exception")

    return {
            "fulfillmentText":"BUENO ALGO ES ALGO", 
            "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-selection",
                    "lifespanCount": 1,
                }
            ],           
        }


"""

SETTINGS

"""

def settings(req, dngn, contexts):
    
    print("Entro en settings")
    return {
        "fulfillmentText": dngn.dungeon_info(),
        "outputContexts": [
                {
                    "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/"+contexts[0],
                    "lifespanCount": 1,
                }
            ],
        }

def end_configuration(req, dngn, contexts):
    print("entrando en end-configuration")
    dngn_info = dngn.dungeon_info()
    dngn = Dungeon()
    return {
            "fulfillmentText":"Your dungeon is now finished. " + dngn_info,
        }

def save_context(req, contexts):
    contexts[1] = contexts[0]
    try:
        contexts[0] = req["queryResult"]["outputContexts"][0]["name"].split("/")[-1]
    except:
        print("\nEntrando en el except\n")
        contexts[0] = "context 1"
    return contexts

"""

FALLBACK

"""

def default_fallback_intent(req, dngn, contexts):
    print("Entro en default fallback intent")
    print(contexts[0])
    print(contexts[1])
    return fallback.getFallback(req, contexts[0])
    


        