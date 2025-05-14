from pymongo import MongoClient
import os
import time

def get_db_connection():
    DB_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "")
    DB_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "")

    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@db:27017/")
            client.admin.command('ping')
            return client
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(2)

    raise Exception("Database connection failed after 3 attempts")

def init_db():
    client = get_db_connection()
    if "Shorklights" in client.list_database_names():
        print("✅ Database 'Shorklights' already exists. No action needed.")
        return

    print("🔄 Initializing database...")

    db = client.Shorklights

    usersCollection = db.create_collection("Users", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "password", "role_id"],
            "properties": {
                "username": {
                    "bsonType": "string",
                },
                "password": {
                    "bsonType": "string",
                },
                "role_id": {
                    "bsonType": "objectId",
                }
            }
        }
    })

    serversCollection = db.create_collection("Servers", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "ip", "username", "password"],
            "properties": {
                "name": {
                    "bsonType": "string",
                },
                "ip": {
                    "bsonType": "string",
                },
                "username": {
                    "bsonType": "string",
                },
                "password": {
                    "bsonType": "string",
                },
            }
        }
    })

    rolesCollection = db.create_collection("Roles", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "bsonType": "string",
                },
            }
        }
    })

    serversCollection.create_index("ip", unique=True)
    rolesCollection.create_index("name", unique=True)
    usersCollection.create_index("username", unique=True)

    rolesCollection.insert_many([
        {"name": "shork"},
        {"name": "member"},
    ])

    usersCollection.insert_one({
        "username": "changeme",
        "password": "$2b$12$8e75P3AX..ReJY1eEV5zueXZWbVt/AyMnFyL6z4eNPbuU1QludQBq",
        "role_id": rolesCollection.find_one({"name": "shork"})["_id"]
    })

