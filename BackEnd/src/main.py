import uvicorn
import firebase_admin
import pyrebase
import json
 
from firebase_admin import credentials, auth
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

cred = credentials.Certificate('botmora_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))
app = FastAPI()
allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)

@app.get("/")
def get_root(response: Response):
    return {"message": "Welcome to Joel!"}

# temporary routes
@app.get("/about")
def get_about(response: Response):
    return {"project_name": "Joel", "description": "Banking Chatbot", "version": "0.0.1"}

# added to allow request from frontend
@app.middleware("http")
async def cors_middleware(request, call_next):
    response = await call_next(request)
    # response.headers["Access-Control-Allow-Origin"] = "*"
    # Front-end host address
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    return response