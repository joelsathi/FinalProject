import uvicorn
import json

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import pyrebase

from LLM.llm_out import generate_llama2_response
from FireBaseDB.access_db import auth, pyrebase_db
from Src.auth.routes import user_router
from Src.prompt.routes import prompt_router

app = FastAPI()
allow_origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods
    allow_headers=["*"],  # This allows all headers
)

app.include_router(user_router)
app.include_router(prompt_router)

@app.get("/")
def get_root(response: Response):
    return {"message": "Welcome to Joel!"}

# temporary routes
@app.get("/about")
def get_about(response: Response):
    return {"project_name": "Joel", "description": "Banking Chatbot", "version": "0.0.1"}