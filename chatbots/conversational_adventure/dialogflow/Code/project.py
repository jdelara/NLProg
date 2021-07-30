from flask import Flask, request
import json
import sys
from conf_manager import *
from game_manager import *
from dungeon import Dungeon


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Default webpage'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

"""
 





"""
# ***************************************************************
#   Inizialición de parámetros
# ***************************************************************
dngn = Dungeon()
parameters_conf = "(req, dngn, contexts_conf)"
parameters_game = "(req, dngn, contexts_game)"
contexts_conf = ["context 1", "context 2"]
contexts_game = ["context 1", "context 2"]


# ***************************************************************
#   RUTA DEL WEBHOOK DE CONFIGURACION
# *************************************************************** 
@app.route('/webhook_conf', methods=['POST'])
def webhook_conf():
    req = request.get_json(force=True)
    save_context(req, contexts_conf)
    func = req["queryResult"]["intent"]["displayName"].lower().replace("-", "_")
    return eval(func + parameters_conf)

# ***************************************************************
#   RUTA DEL WEBHOOK DE JUEGO
# *************************************************************** 
@app.route('/webhook_game', methods=['POST'])
def webhook_game():
    req = request.get_json(force=True)
    #print(json.dumps(req, indent=4, sort_keys=True))
    human_id = str(req["originalDetectIntentRequest"]["payload"]["data"]["from"]["id"])
    save_context(req, contexts_game)
    if not dngn.game.started or dngn.check_turn(human_id):
        func = req["queryResult"]["intent"]["displayName"].lower().replace("-", "_")
        return eval(func + parameters_game)
    else:
        return {
            "fulfillmentText":"", 
            "outputContexts": [
                {
                    "name": "projects/game-chatbot-yauk/agent/sessions/410c82f8-1436-8d1b-0845-53acdefe9d30/contexts/"+contexts_game[0],
                    "lifespanCount": 1,
                }
            ],         
        }      

# ***************************************************************
#   Función que guarda el contexto actual y el último utilizado
#   a no ser que haya error.
# *************************************************************** 
def save_context(req, contexts):
    contexts[1] = contexts[0]
    try:
        context = req["queryResult"]["outputContexts"][0]["name"].split("/")[-1]
        contexts[0] = context if context != "__system_counters__" else contexts[0]
    except:
        contexts[0] = "context 1"
    return contexts