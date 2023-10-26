import json
from fastapi import APIRouter, Response, status, Request, HTTPException, Header, Form
from fastapi.responses import JSONResponse
from .models import UserModel
from ...FireBaseDB.access_db import GetAccountDetails

user_router = APIRouter(
    prefix="/auth",
)

@user_router.get("/AccountDetails")
async def get_account_details(Request: Request):
    return get_account_details(Request['token']['localId'])