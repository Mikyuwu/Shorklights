from pydantic import BaseModel, Field
from bson import ObjectId

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid role_id")
        return ObjectId(v)

class Users(BaseModel):
    username: str
    password: str
    role_id: PydanticObjectId