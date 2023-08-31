import requests
import json

url = "http://localhost:5005/model/parse"

def nlu_respond(phrase: str):
    nlu_data = json.dumps({'text': f"{phrase}"})
    nlu_resp = requests.post(url, data=nlu_data).json()
    return nlu_resp

def run_test():
    url = "http://localhost:5005/model/parse"
    obj = {"text": "Hi?"}
    response = requests.post(url, data=json.dumps(obj))
    print(response.json())

print(nlu_respond("Hi"))