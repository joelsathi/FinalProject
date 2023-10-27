import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form
from fastapi.responses import JSONResponse
from .models import PromptModel

prompt_router = APIRouter(
    prefix="/prompt",
)

@prompt_router.post("/")
async def get_response(response: Response, request:Request):
    user_input = request['user_msg']
    jwt_token = request['token']