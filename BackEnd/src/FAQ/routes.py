import json
from fastapi import (
    APIRouter,
    Response,
    status,
    Request,
    HTTPException,
    Header,
    Form,
    Depends,
)
from fastapi.responses import JSONResponse
from .models import UserModel
from FireBaseDB.access_db import GetAccountDetails, auth
from fastapi.security import OAuth2PasswordBearer
from FireBaseDB.access_db import get_latest_chat_history

faq_router = APIRouter(
    prefix="/faq",
)


@faq_router.get("/", include_in_schema=False)
async def login(request: Request):
    req_json = await request.json()
    email = req_json["email"]
    password = req_json["password"]
    try:
        token = auth.sign_in_with_email_and_password(email, password)
        jwt = token["refreshToken"]
        return JSONResponse(content={"token": jwt}, status_code=200)
    except:
        return HTTPException(
            detail={"message": "There was an error logging in"}, status_code=400
        )
