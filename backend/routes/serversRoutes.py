from fastapi import APIRouter, FastAPI
from bson import ObjectId
from database.dbHelper import get_db_connection
from models.servers import Servers
from helpers.returnResult import return_result
from pymongo.errors import DuplicateKeyError
from fastapi.exceptions import RequestValidationError

router = APIRouter(prefix="/servers")

client = get_db_connection()
ServersCollections = client.Shorklights.Servers

@router.get("/")
def read_root():
    return {
        "message": "Partie Servers de l'API Shorklights",
    }

@router.get("/getServers")
def getServers():
    try:
        serverlist = []
        for server in ServersCollections.find():
            server["_id"] = str(server["_id"])  # so it's JSON serializable ✨
            serverlist.append(server)
        return return_result(True, data=serverlist)
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)

@router.post("/addServer")
def addServer(server: Servers):
    try:
        ServersCollections.insert_one(server.dict())
        return return_result(True, message="Server added successfully")
    except DuplicateKeyError:
        return return_result(False, message="IP already exists", status_code=400)
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)

@router.put("/updateServer/{id}")
def updateServer(id: str, server: Servers):
    # validate that no field is empty
    for field_name, value in server.dict().items():
        if value == "":
            return return_result(False, message=f"{field_name} cannot be empty", status_code=400)
    try:
        result = ServersCollections.update_one(
            {"_id": ObjectId(id)},
            {"$set": server.dict()}
        )
        if result.matched_count == 0:
            return return_result(False, message="Server not found", status_code=404)
        return return_result(True, message="Server updated successfully")
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)

@router.delete("/deleteServer/{id}")
def deleteServer(id: str):
    if not ObjectId.is_valid(id):
        return return_result(False, message="Invalid ID format", status_code=400)
    try:
        result = ServersCollections.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return return_result(False, message="Server not found", status_code=404)
        return return_result(True, message="Server deleted successfully")
    except Exception:
        return return_result(False, message="Unexpected error occurred", status_code=400)
