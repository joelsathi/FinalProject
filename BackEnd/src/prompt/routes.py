import json
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from .models import PromptModel
from FireBaseDB.access_db import GetAccountDetails, auth
from FireBaseDB.access_db import get_latest_chat_history
from FireBaseDB.write_db import delete_chat_history
from .utils import get_response

prompt_router = APIRouter(prefix="/prompt")

@prompt_router.delete("/delete", include_in_schema=False)
async def delete(request: Request):
    try:
        req_json = await request.json()
        jwt = req_json.get('token')

        if not jwt:
            raise HTTPException(status_code=400, detail="Token is required.")

        token = auth.refresh(jwt)
        account_number = token['userId']

        delete_chat_history(account_number)

        return JSONResponse(content={'token': jwt, 'message': 'Chat history deleted successfully'}, status_code=200)
    except:
        return HTTPException(status_code=400, detail={'message': 'There was an error logging in'})

@prompt_router.get("/all-chats", include_in_schema=False)
async def get_all_chats(request: Request):
    try:
        req_json = await request.json()
        jwt = req_json.get('token')

        if not jwt:
            raise HTTPException(status_code=400, detail="Token is required.")

        token = auth.refresh(jwt)
        account_number = token['userId']

        chat_history = get_latest_chat_history(account_number)
        return JSONResponse(content={'token': jwt, 'chat': chat_history}, status_code=200)
    except:
        return HTTPException(status_code=400, detail={'message': 'There was an error logging in'})

@prompt_router.post("/new", include_in_schema=False)
async def get_output_llm(request: Request):
    try:
        req_json = await request.json()
        jwt = req_json.get('token')
        user_msg = req_json.get('user_msg')

        if not jwt or not user_msg:
            raise HTTPException(status_code=400, detail="Token and user_msg are required.")

        token = auth.refresh(jwt)
        # response = ''
        try:
            response = get_response(user_msg, token)
        except Exception as e:
            response = f'An error occurred: {str(e)}'
        return JSONResponse(content={'token': jwt, 'response': response}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=400, detail={'message': f'An error occurred: {str(e)}'})
