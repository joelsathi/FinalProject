# from rasa.nlu.model import Interpreter

# model_path = "BackEnd\\IntentClassifier\\models\\nlu-20230829-104255-nimble-index.tar.gz"  # Path to the trained NLU model directory
# interpreter = Interpreter.load(model_path)

# user_input = "Hello, how are you?"
# result = interpreter.parse(user_input)
# intent = result.get("intent")
# intent_name = intent.get("name")
# confidence = intent.get("confidence")
# intent_ranking = result.get("intent_ranking")

# from rasa.core.agent import Agent

# # agent = Agent.load(model_path='BackEnd\\IntentClassifier\\models\\nlu-20230829-104255-nimble-index.tar.gz')
# agent = Agent.load(model_path='C:\\Users\\Sanu\\Desktop\\FinalProject\\BackEnd\\IntentClassifier\\models\\nlu-20230829-104255-nimble-index.tar.gz')
# # For Rasa 3')
# # result = agent.parse_message(
# #                 message_data='Hello there')
# import asyncio
# asyncio.run(agent.parse_message(
#                 message_data='Bye'))

# intent = result.get("intent")
# print(intent.get("name"))

from rasa.nlu.model import Interpreter