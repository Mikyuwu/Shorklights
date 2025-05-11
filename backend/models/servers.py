from pydantic import BaseModel, Field, validator
from fastapi import HTTPException
from typing import Optional
import ipaddress

class Servers(BaseModel):
    name: str
    ip: str = Field(..., strict=True)
    username: str
    password: str

    @validator("ip")
    def validate_ip(cls, v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid IP address format")
        return v