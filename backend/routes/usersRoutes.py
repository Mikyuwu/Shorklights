from fastapi import APIRouter, FastAPI
from database.dbHelper import get_db_connection
from models.users import Users

router = APIRouter(prefix="/users")

@router.get("/")
def read_root():
    return {
        "message": "Partie Utilisateurs de l'API Shorklights",
    }

@router.post("/addUser")
def addUser(user: Users):
    try:
        client = get_db_connection()
        db = client.Shorklights
        users = db.Users

        user_dict = user.dict()
        result = users.insert_one(user_dict)
        return {
            "success": True,
            "message": "User added successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }