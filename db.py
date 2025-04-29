from pymongo import MongoClient

client = MongoClient("mongodb+srv://callbot:callbot@cluster0.a3lcyab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Adjust URI as needed
db = client["AudioBot"]
settings_collection = db["UserSettings"]
user_collection = db["UserList"]


default_settings = {
    "panBoundary": 100,
    "jumpPercentage": 5,
    "timeLtoR": 10000,
    "volumeMultiplier": 6,
    "speedMultiplier": 0.92,
    "reverb": {
        "room_size": 0.8,
        "damping": 1,
        "width": 0.5,
        "wet_level": 0.3,
        "dry_level": 0.8
    }
}

def get_user_settings(chat_id):
    user = settings_collection.find_one({"chat_id": chat_id})
    if not user:
        settings_collection.insert_one({"chat_id": chat_id, "settings": default_settings})
        return default_settings
    return user["settings"]

def update_user_setting(chat_id, key, value):
    settings_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {f"settings.{key}": value}},
        upsert=True
    )

def reset_user_settings(chat_id):
    """
    Resets the user's settings to the default settings.
    """
    settings_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"settings": default_settings}},
        upsert=True
    )




def register_user(chat_id):
    user_collection.update_one(
        {"_id": chat_id},  # `_id` is Telegram chat ID
        {"$setOnInsert": {"joined": True}},
        upsert=True
    )



def get_all_users():
    return [user["chat_id"] for user in user_collection.find()]

