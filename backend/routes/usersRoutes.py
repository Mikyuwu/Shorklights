from fastapi import APIRouter, FastAPI, Depends
from bson import ObjectId
from database.dbHelper import get_db_connection
from routes.authRoutes import get_admin_user, get_password_hash
from pymongo.errors import DuplicateKeyError
from models.users import Users, UsersCreate

from helpers.returnResult import return_result

router = APIRouter(prefix="/users")

client = get_db_connection()
UsersCollections = client.Shorklights.Users
RolesCollections = client.Shorklights.Roles

def get_role_id(role_name: str):
    role = RolesCollections.find_one({"name": role_name})
    if role:
        return role["_id"]
    else:
        return None

def get_role_name(role_id: str):
    role = RolesCollections.find_one({"_id": ObjectId(role_id)})
    if role:
        return role["name"]
    else:
        return None

@router.get("/")
def read_root():
    return {
        "message": "Partie Utilisateurs de l'API Shorklights",
    }

@router.post("/addUser")
def add_user(user: UsersCreate, current_user: tuple = Depends(get_admin_user)):
    try:
        role_id = get_role_id(user.role)
        if role_id is None:
            return return_result(False, message="Invalid role, please enter a valid one", status_code=400)

        user_dict = user.dict(exclude={"role"})
        user_dict["password"] = get_password_hash(user.password)
        user_dict["role_id"] = role_id

        result = UsersCollections.insert_one(user_dict)
        return return_result(True, "User added successfully", status_code=201)
    except DuplicateKeyError:
        return return_result(False, message="Username already exists", status_code=400)
    except Exception as e:
        return return_result(False, "Unexpected error happened while adding the user", status_code=400)

@router.put("/editUser/{id}")
def edit_user(id: str, user: UsersCreate, current_user: tuple = Depends(get_admin_user)):
    for field_name, value in user.dict().items():
        if value == "":
            return return_result(False, message=f"{field_name} cannot be empty", status_code=400)
    try:
        role_id = get_role_id(user.role)
        if role_id is None:
            return return_result(False, message="Invalid role, please enter a valid one", status_code=400)

        user_dict = user.dict(exclude={"role"})
        user_dict["password"] = get_password_hash(user.password)
        user_dict["role_id"] = role_id


        result = UsersCollections.update_one(
            {"_id": ObjectId(id)},
            {"$set": user_dict}
        )

        if result.matched_count == 0:
            return return_result(False, message="User not found", status_code=404)
        return return_result(True, message="User updated successfully")
    except DuplicateKeyError:
        return return_result(False, message="Username already exists", status_code=400)
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)

@router.get("/getUsers")
def get_users(current_user: tuple = Depends(get_admin_user)):
    try:
        db = client.Shorklights.Users
        userlist = []
        for user in db.find({}, {"password": 0}):
            user["_id"] = str(user["_id"])  # so it's JSON serializable ✨
            userlist.append(user)

            role_name = get_role_name(user["role_id"])
            if role_name is None:
                user["role"] = None
            else:
                user["role"] = role_name
            user.pop("role_id", None)

        return return_result(True, data=userlist)
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)

@router.delete("/deleteUser/{id}")
def delete_user(id: str, current_user: tuple = Depends(get_admin_user)):
    if not ObjectId.is_valid(id):
        return return_result(False, message="Invalid ID format", status_code=400)
    try:
        result = UsersCollections.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return return_result(False, message="User not found", status_code=404)
        return return_result(True, message="User deleted successfully")
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)