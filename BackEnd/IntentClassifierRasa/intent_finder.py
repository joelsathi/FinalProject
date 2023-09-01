import requests
import json

url = "http://localhost:5005/model/parse"

def get_intent(phrase: str):
    nlu_data = json.dumps({'text': f"{phrase}"})
    nlu_resp = requests.post(url, data=nlu_data).json()
    if nlu_resp['intent']['confidence'] > 0.5:
        return nlu_resp['intent']['name']
    else:
        return "intent not found"

def run_test():
    url = "http://localhost:5005/model/parse"
    obj = {"text": "do you know my accont type"}
    response = requests.post(url, data=json.dumps(obj))
    print(response.json())