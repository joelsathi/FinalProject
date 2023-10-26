from pydantic import BaseModel
from typing import Any

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    password: str
    account_type: str
    account_number: str
    balance: float
    transactions: list
    chat_history: list