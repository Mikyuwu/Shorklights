from fastapi import APIRouter, FastAPI, UploadFile, File, Depends
from routes.authRoutes import get_authentificated_user
from database.dbHelper import get_db_connection
from helpers.returnResult import return_result
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import Form
from bson import ObjectId
from typing import List
import os
import paramiko

router = APIRouter(prefix="/sshPayloads")

client = get_db_connection()
ServersCollections = client.Shorklights.Servers

def get_servers_details(servers):
    try:
        servers_details = []
        for server in servers:
            server_data = ServersCollections.find_one({"_id": ObjectId(server)})
            if server_data:
                servers_details.append({
                    "ip": server_data["ip"],
                    "username": server_data["username"],
                    "password": server_data["password"]
                })
        return servers_details
    except Exception as e:
        raise e

@router.get("/")
def read_root():
    return {
        "message": "Partie SSH-Payloads de l'API Shorklights",
    }

@router.post("/playSound")
def index_sound(file: UploadFile = File(None), sound: str = None, current_user: tuple = Depends(get_authentificated_user)):
    try:
        if file and file.content_type in ["audio/mpeg", "audio/mp3"]:
            with open('/app/assets/' + file.filename, "wb") as f:
                f.write(file.file.read())
            file.file.close()
            sound = {
                "name": file.filename,
                "path": "/app/assets/" + file.filename
            }
        else:
            raise ValueError("Invalid file type. Only mp3 files are allowed.")

        if sound is not None:
            return execute_payload('playSound', sound=sound)
        else :
            raise ValueError("No sound selected")
    except Exception as e:
        return return_result(False, message=str(e), status_code=400)

@router.post("/changeWallpaper")
def index_wallpaper(file: UploadFile = File(None), wallpaper: str = None, servers: List[str] = Form(...), current_user: tuple = Depends(get_authentificated_user)):
    try:
        if file and file.content_type in ['image/png', 'image/jpeg']:
            with open('/app/assets/' + file.filename, "wb") as f:
                f.write(file.file.read())
            file.file.close()
            wallpaper = {
                "name": file.filename,
                "path": "/app/assets/" + file.filename
            }
        else:
            raise ValueError("Invalid file type. Only png and jpeg files are allowed.")

        if wallpaper is not None:
            return execute_payload('changeWallpaper', wallpaper=wallpaper, servers=servers)
        else :
            raise ValueError("No wallpaper selected")
    except Exception as e:
        return return_result(False, message=str(e), status_code=400)

def execute_payload(type, wallpaper = None, sound = None, servers: List[str] = Form(...)):
    try:
        servers_details = get_servers_details(servers)
        with ThreadPoolExecutor() as executor:
            match type:
                case 'changeWallpaper':
                    futures = { executor.submit(change_wallpaper, server["ip"], server["username"], server["password"], wallpaper): server for server in servers_details}
                case 'playSound':
                    futures = { executor.submit(play_sound, server["ip"], sound): server for server in servers_details }
                case _:
                    raise ValueError("Invalid payload type")
            results = [future.result() for future in as_completed(futures)]
        return return_result(True, message="Payload executed successfully", data=results)
    except Exception as e:
        return return_result(False, message=str(e), status_code=400)

def change_wallpaper(ip, username, password, wallpaper):
    try:
        print("Payload sent to: ", ip)
        print(wallpaper)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        if not os.path.exists(wallpaper["path"]):
            raise FileNotFoundError(f"Wallpaper file not found at {wallpaper['path']}")

        sftp = client.open_sftp()

        sftp.put(wallpaper["path"], f'/home/{username}/{wallpaper["name"]}')
        sftp.close()

        client.exec_command(f'gsettings set org.gnome.desktop.background picture-uri "file:///home/{username}/{wallpaper["name"]}"')
        client.close()
    except Exception as e: raise e

def play_sound(ip, sound):
    try:
        print("Payload sent to: ", ip)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username='uha40', password='uha40')

        if not os.path.exists(sound["path"]):
            raise FileNotFoundError(f"Sound file not found at {sound['path']}")

        sftp = client.open_sftp()
        sftp.put(sound['path'], f'/home/uha40/Bureau/{sound["name"]}')
        sftp.close()

        client.exec_command(f'mpg123 /home/uha40/Bureau/{sound["name"]}')
        client.close()
    except Exception as e: raise e


    # To stop // pidof mpg123 | xargs kill -9