from flask import Flask, request
import json
import sys
from intent_manager import *
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
parameters = "(req, dngn, contexts)"
contexts = ["context 1", "context 2"]

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    contexs = save_context(req, contexts)
    func = req["queryResult"]["intent"]["displayName"].lower().replace("-", "_")
    return eval(func + parameters)