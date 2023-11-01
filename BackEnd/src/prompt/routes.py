import json
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from .models import PromptModel
from FireBaseDB.access_db import GetAccountDetails, auth
from FireBaseDB.access_db import get_latest_chat_history
from FireBaseDB.write_db import delete_chat_history
from .utils import get_response

prompt_router = APIRouter(prefix="/prompt")

@prompt_router.delete("/delete", include_in_schema=False)
async def delete(request: Request, authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(detail={'message': 'Authorization header is missing'}, status_code=401)

    # Check if the header starts with 'Bearer ' and extract the token
    if not authorization.startswith('Bearer '):
        raise HTTPException(detail={'message': 'Invalid Authorization header format'}, status_code=401)

    jwt = authorization[7:]  # Extract the token part after 'Bearer '

    try:

        if not jwt:
            raise HTTPException(status_code=400, detail="Token is required.")

        token = auth.refresh(jwt)
        account_number = token['userId']

        delete_chat_history(account_number)

        return JSONResponse(content={'token': jwt, 'message': 'Chat history deleted successfully'}, status_code=200)
    except:
        return HTTPException(status_code=400, detail={'message': 'There was an error logging in'})

@prompt_router.get("/all-chats", include_in_schema=False)
async def get_past_conversations(request: Request, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(detail={'message': 'Authorization header is missing'}, status_code=401)

    # Check if the header starts with 'Bearer ' and extract the token
    if not authorization.startswith('Bearer '):
        raise HTTPException(detail={'message': 'Invalid Authorization header format'}, status_code=401)

    token = authorization[7:]  # Extract the token part after 'Bearer '

    try:
        user = auth.refresh(token)
        account_number = user['userId']
        chat_history = get_latest_chat_history(account_number, limit=10)
        return JSONResponse(content=chat_history, status_code=200)
    except Exception as e:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)

@prompt_router.post("/new_msg", include_in_schema=False)
async def get_output_llm(request: Request, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(detail={'message': 'Authorization header is missing'}, status_code=401)

    # Check if the header starts with 'Bearer ' and extract the token
    if not authorization.startswith('Bearer '):
        raise HTTPException(detail={'message': 'Invalid Authorization header format'}, status_code=401)

    token = authorization[7:]  # Extract the token part after 'Bearer '

    try:
        token = auth.refresh(token)
        try:
            req_json = await request.json()
        except:
            raise HTTPException(status_code=400, detail="Request body is required.")
        try:
            user_msg = req_json.get("user_msg")
        except:
            raise HTTPException(status_code=400, detail="user_msg is required.")
        try:
            response = get_response(user_msg, token)
            return JSONResponse(content={'data': response}, status_code=200)
        except Exception as e:
            response = f'An error occurred: {str(e)}'
            return JSONResponse(content={'message': "Couldn't fetch data from LLM", 'response':response}, status_code=400)
    except Exception as e:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)