import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form, Depends
from fastapi.responses import JSONResponse
from .models import UserModel
from FireBaseDB.access_db import GetAccountDetails, auth, GetAccountEmail, GetAccountName
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
       return JSONResponse(content={'token': jwt, 'email': email, 'name':'Sada',"user_id": "12345"}, status_code=status.HTTP_200_OK)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@user_router.get("/auth-status", include_in_schema=False)
async def checkStatus(request: Request, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(detail={'message': 'Authorization header is missing'}, status_code=401)

    # Check if the header starts with 'Bearer ' and extract the token
    if not authorization.startswith('Bearer '):
        raise HTTPException(detail={'message': 'Invalid Authorization header format'}, status_code=401)

    token = authorization[7:]  # Extract the token part after 'Bearer
    try:
        token = auth.refresh(token)
        email = GetAccountEmail(token['userId'])
        name = GetAccountName(token['userId'])
        return JSONResponse(content={'status': 'success', 'data' : {'email':email, 'name':name}}, status_code=200)
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@user_router.get("/logout", include_in_schema=False)
async def logout(request: Request):
    return JSONResponse(content={'status': 'success'}, status_code=200)