import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form, Depends
from fastapi.responses import JSONResponse
from .models import UserModel
from FireBaseDB.access_db import GetAccountDetails, auth
from fastapi.security import OAuth2PasswordBearer
from FireBaseDB.access_db import get_latest_chat_history

user_router = APIRouter(
    prefix="/auth",
)

@user_router.post("/login", include_in_schema=False)
async def login(request: Request):
   req_json = await request.json()
   email = req_json['email']
   password = req_json['password']
   try:
       token = auth.sign_in_with_email_and_password(email, password)
       jwt = token['refreshToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)
   
@user_router.get("/past_conversations", include_in_schema=False)
async def get_past_conversations(request: Request):
    req_json = await request.json()
    # get the token from the headers
    jwt = req_json['token']
    try:
        user = auth.refresh(jwt)
        # return JSONResponse(content={'token': user}, status_code=200)
        account_number = user['userId']
        chat_history = get_latest_chat_history(account_number, limit=5)
        return JSONResponse(content={'token': jwt, 'history': chat_history}, status_code=200)
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)