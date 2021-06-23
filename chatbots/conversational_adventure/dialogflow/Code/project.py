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
#intents = ["New-Character", "New-Object", "New-Player", "New-Room", "New-Room-select-number", "Settings"]
dngn = Dungeon()
dngn.aux()
parameters_conf = "(req, dngn, contexts_conf)"
parameters_game = "(req, dngn, contexts_game)"
contexts_conf = ["context 1", "context 2"]
contexts_game = ["context 1", "context 2"]

@app.route('/webhook_conf', methods=['POST'])
def webhook_conf():
    req = request.get_json(force=True)
    save_context(req, contexts_conf)
    func = req["queryResult"]["intent"]["displayName"].lower().replace("-", "_")
    return eval(func + parameters_conf)


@app.route('/webhook_game', methods=['POST'])
def webhook_game():
    req = request.get_json(force=True)
    save_context(req, contexts_game)
    func = req["queryResult"]["intent"]["displayName"].lower().replace("-", "_")
    print(func)
    print("\n"*6)
    return eval(func + parameters_game)


def save_context(req, contexts):
    contexts[1] = contexts[0]
    try:
        context = req["queryResult"]["outputContexts"][0]["name"].split("/")[-1]
        contexts[0] = context if context != "__system_counters__" else contexts[0]
    except:
        contexts[0] = "context 1"
    """print("Contexto 0 -->", contexts[0])
    print("Contexto 1 -->", contexts[1])"""
    return contexts