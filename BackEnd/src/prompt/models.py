from pydantic import BaseModel
from typing import Any

class PromptModel(BaseModel):
    prompt: str
