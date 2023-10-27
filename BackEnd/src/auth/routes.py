import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form
from fastapi.responses import JSONResponse
from .models import UserModel
from ...FireBaseDB.access_db import GetAccountDetails, auth

user_router = APIRouter(
    prefix="/auth",
)

@user_router.post("/login", include_in_schema=False)
async def login(request: Request):
   req_json = await request.json()
   email = req_json['email']
   password = req_json['password']
   try:
       user = auth.sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)