def getFallback(req, context):
    if (context=="player-configuration"):
        return {
                    "fulfillmentText":"Sorry, " + req["queryResult"]["queryText"] + " is not a valid name. Could you try again?",
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/player-configuration",
                            "lifespanCount": 1,
                        }
                    ],
                }
    elif (context=="number-of-rooms"):
        return {
                    "fulfillmentText":"Sorry, '" + req["queryResult"]["queryText"] + "' is not a valid number. Could you try again?",
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/number-of-rooms",
                            "lifespanCount": 1,
                        }
                    ],
                }
    elif (context=="hp-player"):
        return {
                    "fulfillmentText":"Sorry, '" + req["queryResult"]["queryText"] + "' is not a valid number. Could you try again?",
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/hp-player",
                            "lifespanCount": 1,
                        }
                    ],
                }                
    else:
        return {
                    "fulfillmentText":"Sorry, Could you repeat that again?",
                    "outputContexts": [
                        {
                            "name": "projects/conf-chatbot-phqj/agent/sessions/af802176-92a2-ba51-7ed0-2632e0b95e77/contexts/" + context,
                            "lifespanCount": 1,
                        }
                    ],
                }