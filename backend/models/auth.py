from pydantic import BaseModel, validator
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str